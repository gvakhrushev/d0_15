#!/usr/bin/env python3
"""vp_dual_frontier_no_overclaim - guard the lepton-indirect + phason-w(z) fronts against over-claim.

Fails if the books assert any dual-frontier closure phrase whose owner is not actually
registered-closed (reads the registry + the books, not only prose).
"""
import csv
import pathlib
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = pathlib.Path(__file__).resolve().parents[1]
CSV = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
CLOSED = {"CERT-CLOSED", "CORE-FORMALIZED", "NO-GO", "NO_GO_PROVED", "PASSPORT-CLOSED", "THE"}
UNCONDITIONAL = [
    "DESI confirms D0",
    "D0 predicts DESI w(z)",
    "30-dimensional kernel proves w(z)",
    "charged-lepton decimals are CORE-THE",
    "PDG validates lepton coefficients",
]
CONDITIONAL = {
    "lepton indirect coefficient owner closed": "D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001",
    "phason w(z) derived": "D0-PHASON-WZ-TRANSFER-OWNER-001",
}


def main() -> int:
    print("=== vp_dual_frontier_no_overclaim  guard the lepton-indirect + phason-w(z) fronts ===")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [p for p in UNCONDITIONAL if p in prose]
    assert not hits, f"forbidden dual-frontier over-claim(s) present: {hits}"
    print(f"PASS_NO_UNCONDITIONAL_OVERCLAIM  none of the {len(UNCONDITIONAL)} dual-frontier over-claims appear in the books")
    for phrase, cid in CONDITIONAL.items():
        if phrase in prose:
            assert rows.get(cid, {}).get("release_status") in CLOSED, f"'{phrase}' but {cid} not registered-closed"
    print("PASS_CONDITIONAL_OWNERS  any 'owner closed' / 'w(z) derived' phrase is backed by a registered-closed owner")
    assert any(p in "x DESI confirms D0 x" for p in UNCONDITIONAL), "control: detector reachable"
    print("FAIL_PLANTED_DUAL_OVERCLAIM_CAUGHT  the detector is reachable")
    print("PASS_DUAL_FRONTIER_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
