#!/usr/bin/env python3
"""vp_five_math_stitches_no_overclaim - guard the deep-stitch closure sprint against over-claim.

Reads the books. Fails if any grand-closure phrase appears unless the exact corresponding owner is
registered at a CLOSED status. The stitches are NARROW finite closures / no-gos; none of them licenses
a global or fully-derived claim.
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
BOOKS = ROOT / "01_BOOKS"
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"

# grand-closure phrases that are forbidden outright (no owner can license them)
UNCONDITIONAL = [
    "D0 is complete",
    "all mathematical gaps closed",
    "all mathematical gaps are closed",
    "Bekenstein-Hawking thermodynamics fully derived",
    "all fusion categories classified",
    "CKM fully derived",
    "SI speed of light derived",
    "Weierstrass/Haar time fully proved",
    "Theory of Everything",
    "Open-joints register is empty",
]
# closure phrases allowed only if the named owner is registered-closed
CLOSED = {"CORE-FORMALIZED", "CERT-CLOSED", "OPERATOR-SCAFFOLD-CERTIFIED", "NO-GO", "NO_GO_PROVED",
          "PASSPORT-CLOSED", "BRIDGE-ASSUMPTIONS-EXPLICIT", "DEPRECATED"}
CONDITIONAL = {
    "heat-trace jump closed": "D0-REHEATING-HEAT-TRACE-JUMP-001",
    "Page turning point closed": "D0-PAGE-TURNING-POINT-RANK-THEOREM-001",
    "Ising excluded": "D0-ISING-ANYON-EXCLUSION-001",
    "Fibonacci uniqueness closed": "D0-FIBONACCI-ANYON-UNIQUENESS-001",
    "connectivity spectral gap closed": "D0-CONNECTIVITY-SPECTRAL-GAP-SPEED-001",
    "hypercharge flow lattice closed": "D0-HYPERCHARGE-FLOW-LATTICE-001",
}


def main() -> int:
    print("=== vp_five_math_stitches_no_overclaim  guard the deep-stitch sprint against grand-closure ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the stitches are narrow finite closures / no-gos; no global or "
          "fully-derived claim is licensed; every closure phrase needs a registered-closed owner")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in BOOKS.rglob("*.md"))

    hits = [p for p in UNCONDITIONAL if p in prose]
    assert not hits, f"forbidden grand-closure phrase(s) in books: {hits}"
    print(f"PASS_NO_UNCONDITIONAL_OVERCLAIM  none of the {len(UNCONDITIONAL)} grand-closure phrases appear")

    for phrase, cid in CONDITIONAL.items():
        if phrase in prose:
            st = rows.get(cid, {}).get("release_status")
            assert st in CLOSED, f"book claims '{phrase}' but {cid} is not registered-closed (status={st})"
    print("PASS_CONDITIONAL_OWNERS  any stitch-closure phrase is backed by a registered-closed owner row")

    # the frontier stays non-empty
    pts = [c for c, r in rows.items() if r["release_status"] == "PROOF-TARGET"]
    assert len(pts) > 0, "registry has zero PROOF-TARGET rows -- verify before any closure claim"
    print(f"PASS_FRONTIER_NONEMPTY  {len(pts)} PROOF-TARGET rows remain (open-joints register NOT empty)")

    planted = "intro: this proves the Theory of Everything and all mathematical gaps closed."
    assert any(p in planted for p in UNCONDITIONAL), "control: the over-claim detector must be reachable"
    print("FAIL_PLANTED_STITCH_OVERCLAIM_CAUGHT  the detector catches a planted grand-closure phrase (reachable)")

    print("PASS_FIVE_MATH_STITCHES_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
