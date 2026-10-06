#!/usr/bin/env python3
"""Check registry metadata without upgrading open bridge obligations to proofs."""
from pathlib import Path
import csv
import sys
from collections import Counter

LEAN_ROOT = Path(__file__).resolve().parents[1]
REPO = Path(__file__).resolve().parents[2]
CLAIM_MAP = REPO / "02_REGISTRY" / "claims.csv"
ASSUMPTION_LEDGER = REPO / "02_REGISTRY" / "assumptions.csv"
REQUIRED = {
    "D0-FOUND-001",
    "D0-PHI-HURWITZ-001",
    "D0-PHASE-UNFOLD-002",
    "D0-LEAN-CORE-001",
    "D0-LEAN-BRIDGE-001",
}
ALLOWED_STATUSES = {
    "LEAN_PROVED",
    "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS",
    "PYTHON_CERTIFIED",
    "EMPIRICAL_PASSPORT",
    "OPEN",
    "UNPROVED",
    "DEPRECATED",
}
CORE_STATUSES = {"CORE-FORMALIZED", "CORE_FORMALIZED"}
OPEN_RELEASE_STATUSES = {
    "FRONTIER",
    "PROOF-TARGET",
    "CERT-CANDIDATE",
    "OPERATOR-SCAFFOLD-COMPLETE",
    "OPERATOR-SCAFFOLD-CERTIFIED",
    "SPIN-FLAVOUR-TRANSFER-CERTIFIED",
    "EMPIRICAL-PASSPORT-CANDIDATE",
    "LOWER-BOUND-TARGET",
    "THEOREM-TARGET-SHARPENED",
    "PROOF-OBLIGATION-EXPOSED",
}
PROVED_LEAN_STATUSES = {"LEAN_PROVED", "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS"}
OPEN_PROOF_STATUSES = {"OPEN", "UNPROVED"}


def read_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def split_ids(value: str) -> list[str]:
    return [x.strip() for x in value.replace(",", ";").split(";") if x.strip()]


def validate_rows(rows: list[dict[str, str]], assumptions: set[str],
                  required: set[str] | None = None) -> list[str]:
    """Pure metadata validation; this does not type-check Lean declarations."""
    required = REQUIRED if required is None else required
    counts = Counter(row.get("claim_id", "").strip() for row in rows)
    failures = [f"missing required claim {claim}" for claim in sorted(required - counts.keys())]
    for claim, count in sorted(counts.items()):
        if not claim:
            failures.append("empty claim_id")
        elif count > 1:
            failures.append(f"{claim}: duplicate claim_id")

    for row in rows:
        claim = row.get("claim_id", "").strip()
        status = row.get("lean_status", "").strip()
        release_status = row.get("release_status", "").strip()
        if status not in ALLOWED_STATUSES:
            failures.append(f"{claim}: bad lean_status {status!r}")
        if status in PROVED_LEAN_STATUSES and (
            not row.get("lean_module", "").strip()
            or not row.get("lean_theorem", "").strip()
        ):
            failures.append(f"{claim}: LEAN_PROVED claim missing Lean module/theorem")

        uses_bridge = row.get("uses_bridge_assumptions", "").strip().lower() == "true"
        assumption_ids = split_ids(row.get("assumption_ids", ""))
        if uses_bridge and not assumption_ids:
            failures.append(f"{claim}: bridge claim missing assumption_ids")
        if not uses_bridge and assumption_ids:
            failures.append(f"{claim}: assumption_ids present but uses_bridge_assumptions is false")
        for aid in assumption_ids:
            if aid not in assumptions:
                failures.append(f"{claim}: missing assumption ledger row {aid}")

        if release_status in CORE_STATUSES and status != "LEAN_PROVED":
            failures.append(f"{claim}: core release status must be LEAN_PROVED")
        # An unproved bridge may be registered as an explicitly open obligation.
        # Its assumption ledger remains mandatory; it is never a closed proof.
        open_bridge_target = (
            status in OPEN_PROOF_STATUSES and release_status in OPEN_RELEASE_STATUSES
        )
        if uses_bridge and status not in {
            "LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS", "PYTHON_CERTIFIED"
        } and not open_bridge_target:
            failures.append(
                f"{claim}: bridge claim must be explicitly conditional/certified "
                "or an OPEN/UNPROVED obligation with an open release status"
            )
    return failures


def main() -> int:
    for path in (CLAIM_MAP, ASSUMPTION_LEDGER):
        if not path.exists():
            print(f"FAIL missing {path}")
            return 1
    try:
        rows = read_csv(CLAIM_MAP)
        assumptions = {row["assumption_id"] for row in read_csv(ASSUMPTION_LEDGER)}
        failures = validate_rows(rows, assumptions)
    except (OSError, csv.Error, KeyError) as exc:
        print(f"FAIL cannot read registry: {exc}")
        return 1
    if failures:
        print("FAIL")
        for failure in failures:
            print(failure)
        return 1
    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
