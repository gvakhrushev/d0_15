#!/usr/bin/env python3
"""vp_no_false_grand_closure - guard against premature 'Grand Closure' / empty-register over-claims.

Reads the claim registry AND the books. FAILS if any book asserts a global-closure phrase whose owner
is not actually registered-as-closed, or that is forbidden while the frontier is non-empty.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CLOSED = {"CERT-CLOSED", "CORE-FORMALIZED", "OPERATOR-SCAFFOLD-CERTIFIED", "NO-GO", "NO_GO_PROVED",
          "PASSPORT-CLOSED", "BRIDGE-ASSUMPTIONS-EXPLICIT", "DEPRECATED"}

# phrases that are over-claims whenever any PROOF-TARGET remains (the frontier is non-empty)
UNCONDITIONAL = [
    "Open-joints register is formally EMPTY",
    "Open-joints register empty",
    "zero analytical theorem debt",
    "D0 framework now carries zero analytical theorem debt",
    "D0-BARYON-ASYMMETRY-DELTA0-001 CORE-THE",
]
# phrase -> claim_id that must be registered at a CLOSED status for the phrase to be allowed
CONDITIONAL = {
    "D0-BARYON-ASYMMETRY-DELTA0-001 CLOSED": "D0-BARYON-ASYMMETRY-DELTA0-001",
    "D0-BARE-GRAPH-DECIMAL-NOGO-001 CLOSED": "D0-BARE-GRAPH-DECIMAL-NOGO-001",
    "lepton indirect coefficient owner closed": "D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001",
    "phason w(z) derived": "D0-PHASON-WZ-TRANSFER-OWNER-001",
    "D0-PHASON-WZ-TRANSFER-OWNER-001 CLOSED": "D0-PHASON-WZ-TRANSFER-OWNER-001",
    "D0-PHASON-WZ-EXPLICIT-FUNCTION-001 CLOSED": "D0-PHASON-WZ-EXPLICIT-FUNCTION-001",
    "explicit phason w(z) function closed": "D0-PHASON-WZ-EXPLICIT-FUNCTION-001",
    "D0-LEPTON-INDIRECT-GREEN-PUISEUX-SCOUT-001 CLOSED": "D0-LEPTON-INDIRECT-GREEN-PUISEUX-SCOUT-001",
    "D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001 CLOSED": "D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001",
    "D0-NEUTRINO-DELTA-ALPHA-NORM-SQUARE-001 CLOSED": "D0-NEUTRINO-DELTA-ALPHA-NORM-SQUARE-001",
    "D0-LEPTON-GREEN-PUISEUX-OPERATOR-001 CLOSED": "D0-LEPTON-GREEN-PUISEUX-OPERATOR-001",
    "D0-LUCAS-VORONOI-MARKOV-PARTITION-001 CLOSED": "D0-LUCAS-VORONOI-MARKOV-PARTITION-001",
    "D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001 CLOSED": "D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001",
    "D0-PHASON-WZ-CPL-PASSPORT-001 CLOSED": "D0-PHASON-WZ-CPL-PASSPORT-001",
    "D0-CONNES-GRAPH-DISTANCE-OWNER-001 CLOSED": "D0-CONNES-GRAPH-DISTANCE-OWNER-001",
    "D0-GHP-GOLDEN-CAUCHY-BOUND-001 CLOSED": "D0-GHP-GOLDEN-CAUCHY-BOUND-001",
}


def main() -> int:
    print("=== vp_no_false_grand_closure  guard against premature Grand-Closure / empty-register over-claims ===")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))

    # the frontier is non-empty: PROOF-TARGET rows still exist
    proof_targets = [c for c, r in rows.items() if r["release_status"] == "PROOF-TARGET"]
    assert len(proof_targets) > 0, "registry has zero PROOF-TARGET rows -- verify before any 'register empty' claim"
    print(f"PASS_FRONTIER_NONEMPTY  {len(proof_targets)} PROOF-TARGET rows remain (the open-joints register is NOT empty)")

    # unconditional over-claims must be absent from the books
    hits = [p for p in UNCONDITIONAL if p in prose]
    assert not hits, f"forbidden grand-closure / empty-register phrase(s) present in books: {hits}"
    print(f"PASS_NO_UNCONDITIONAL_OVERCLAIM  none of the {len(UNCONDITIONAL)} grand-closure/empty-register phrases appear in the books")

    # conditional closure phrases allowed only if the owner is registered-as-closed
    for phrase, cid in CONDITIONAL.items():
        if phrase in prose:
            st = rows.get(cid, {}).get("release_status")
            assert st in CLOSED, f"book claims '{phrase}' but {cid} is not registered-closed (status={st})"
    print(f"PASS_CONDITIONAL_OWNERS_PRESENT  any '<claim> CLOSED' phrase in the books is backed by a registered-closed owner")

    # negative control: the guard is reachable (a planted empty-register claim would be caught)
    planted = "intro: the Open-joints register is formally EMPTY now."
    assert any(p in planted for p in UNCONDITIONAL), "control: the over-claim detector must be reachable"
    print("FAIL_PLANTED_GRAND_CLOSURE_CAUGHT  the detector catches a planted 'register empty' over-claim (reachable)")

    print("PASS_NO_FALSE_GRAND_CLOSURE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
