#!/usr/bin/env python3
from pathlib import Path
import csv
import sys

ROOT = Path(__file__).resolve().parents[1]
CLAIM_MAP = ROOT / "docs" / "CLAIM_TO_LEAN_MAP.csv"
ASSUMPTION_LEDGER = ROOT / "docs" / "LEAN_ASSUMPTION_LEDGER.csv"
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
    "DEPRECATED",
}
CORE_STATUSES = {"CORE-FORMALIZED", "CORE_FORMALIZED"}


def read_csv(path: Path):
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def split_ids(value: str) -> list[str]:
    return [x.strip() for x in value.replace(",", ";").split(";") if x.strip()]


def main() -> int:
    if not CLAIM_MAP.exists():
        print(f"FAIL missing {CLAIM_MAP}")
        return 1
    if not ASSUMPTION_LEDGER.exists():
        print(f"FAIL missing {ASSUMPTION_LEDGER}")
        return 1

    rows = read_csv(CLAIM_MAP)
    assumptions = {row["assumption_id"] for row in read_csv(ASSUMPTION_LEDGER)}
    seen = {row.get("claim_id", "") for row in rows}
    failures = []

    for claim in sorted(REQUIRED - seen):
        failures.append(f"missing required claim {claim}")

    for row in rows:
        claim = row.get("claim_id", "")
        status = row.get("lean_status", "")
        if status not in ALLOWED_STATUSES:
            failures.append(f"{claim}: bad lean_status {status!r}")
        if not row.get("lean_module") or not row.get("lean_theorem"):
            failures.append(f"{claim}: missing Lean module/theorem")

        uses_bridge = row.get("uses_bridge_assumptions", "").lower() == "true"
        assumption_ids = split_ids(row.get("assumption_ids", ""))
        if uses_bridge and not assumption_ids:
            failures.append(f"{claim}: bridge claim missing assumption_ids")
        if not uses_bridge and assumption_ids:
            failures.append(f"{claim}: assumption_ids present but uses_bridge_assumptions is false")
        for aid in assumption_ids:
            if aid not in assumptions:
                failures.append(f"{claim}: missing assumption ledger row {aid}")

        release_status = row.get("release_status", "")
        if release_status in CORE_STATUSES and status != "LEAN_PROVED":
            failures.append(f"{claim}: core release status must be LEAN_PROVED")
        if uses_bridge and status not in {"LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS", "PYTHON_CERTIFIED"}:
            failures.append(f"{claim}: bridge claim must be LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS or PYTHON_CERTIFIED")

    if failures:
        print("FAIL")
        for failure in failures:
            print(failure)
        return 1

    print("PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
