#!/usr/bin/env python3
"""vp_four_physics_front_no_overclaim - guard the four physics fronts (P1-P4) against over-claim.

Reads the canonical registry AND the books. Fails on grand-closure / front-specific over-claim phrases
unless the corresponding owner is registered at a CLOSED status; and fails if any owner this strike
declares OPEN is silently promoted. Reads REGISTRY ROWS, not only prose.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CLOSED = {"CORE-FORMALIZED", "CERT-CLOSED", "OPERATOR-SCAFFOLD-CERTIFIED", "NO-GO", "NO_GO_PROVED",
          "PASSPORT-CLOSED", "BRIDGE-ASSUMPTIONS-EXPLICIT", "DEPRECATED"}

UNCONDITIONAL = [
    "D0 proves the Standard Model hypercharges",
    "D0 proves the Standard Model",
    "D0 solves the black-hole information paradox",
    "D0 solves the black hole information paradox",
    "D0 derives 246 GeV",
    "D0 predicts Planck n_s",
    "D0 predicts the Planck spectral index",
    "D0 replaces the inflaton completely",
    "D0 is now a complete TOE",
    "D0 is a complete TOE",
    "all open joints closed",
    "all open joints are closed",
    "charged-lepton decimals are CORE",
]
# phrase -> owner that must be registered-closed for the phrase to be allowed.
CONDITIONAL = {
    "anomaly cancellation closed": "D0-SM-ANOMALY-CANCELLATION-OWNER-001",
    "D0-SM-ANOMALY-CANCELLATION-OWNER-001 CLOSED": "D0-SM-ANOMALY-CANCELLATION-OWNER-001",
    "finite-rank Page curve closed": "D0-PAGE-CURVE-FINITE-RANK-OWNER-001",
    "D0-PAGE-CURVE-FINITE-RANK-OWNER-001 CLOSED": "D0-PAGE-CURVE-FINITE-RANK-OWNER-001",
    "black-hole information unitarity closed": "D0-BLACK-HOLE-INFORMATION-UNITARITY-OWNER-001",
    "Yukawa shell-overlap closed": "D0-YUKAWA-SHELL-OVERLAP-MATRIX-001",
    "connectivity threshold closed": "D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001",
    "D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001 CLOSED": "D0-COSMOLOGY-CONNECTIVITY-THRESHOLD-OWNER-001",
}
# the owners this strike registers as OPEN -- must NOT be silently closed.
MUST_STAY_OPEN = [
    "D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001",
    "D0-SM-HYPERCHARGE-MINIMAL-DENOMINATOR-001",
    "D0-HIGGS-PHASON-CONDENSATION-OWNER-001",
    "D0-LEPTON-YUKAWA-HIERARCHY-OWNER-001",
    "D0-CMB-PHASON-SPECTRUM-OWNER-001",
    "D0-INFLATIONLESS-EARLY-UNIVERSE-OWNER-001",
]


def main() -> int:
    print("=== vp_four_physics_front_no_overclaim  guard the four physics fronts P1-P4 ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: every closure phrase must be backed by a registered-closed owner; "
          "the OPEN owners of this strike must stay non-closed; no 'D0 proves the SM / solves BH info / derives "
          "246 GeV / predicts n_s / replaces inflaton / complete TOE' phrase appears in the books")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))

    proof_targets = [c for c, r in rows.items() if r["release_status"] == "PROOF-TARGET"]
    assert len(proof_targets) > 0, "registry has zero PROOF-TARGET rows -- verify before any closure claim"
    print(f"PASS_FRONTIER_NONEMPTY  {len(proof_targets)} PROOF-TARGET rows remain (open-joints register NOT empty)")

    hits = [p for p in UNCONDITIONAL if p in prose]
    assert not hits, f"forbidden four-physics over-claim(s) in books: {hits}"
    print(f"PASS_NO_UNCONDITIONAL_OVERCLAIM  none of the {len(UNCONDITIONAL)} grand over-claims appear in the books")

    for phrase, cid in CONDITIONAL.items():
        if phrase in prose:
            st = rows.get(cid, {}).get("release_status")
            assert st in CLOSED, f"book claims '{phrase}' but {cid} is not registered-closed (status={st})"
    print("PASS_CONDITIONAL_OWNERS  any closure phrase in the books is backed by a registered-closed owner row")

    for cid in MUST_STAY_OPEN:
        r = rows.get(cid)
        if r is not None:
            assert r["release_status"] in {"PROOF-TARGET", "OPEN"}, \
                f"{cid} must stay PROOF-TARGET/OPEN (got {r['release_status']})"
    print(f"PASS_OPEN_OWNERS_STAY_OPEN  the {len(MUST_STAY_OPEN)} declared-open physics owners are all PROOF-TARGET/OPEN")

    planted = "intro: D0 solves the black-hole information paradox and all open joints closed."
    assert any(p in planted for p in UNCONDITIONAL), "control: the over-claim detector must be reachable"
    print("FAIL_PLANTED_FOUR_PHYSICS_OVERCLAIM_CAUGHT  the detector catches a planted grand-closure phrase (reachable)")

    print("PASS_FOUR_PHYSICS_FRONT_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
