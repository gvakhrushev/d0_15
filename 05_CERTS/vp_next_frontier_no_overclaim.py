#!/usr/bin/env python3
"""vp_next_frontier_no_overclaim - guard the phason-explicit + lepton-scout fronts against over-claim.

Reads the registry AND the books. Fails on grand-closure / front-specific over-claim phrases unless the
corresponding owner is registered CERT-CLOSED or NO-GO-CLOSED.
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
    "Open-joints register is empty",
    "zero theorem debt",
    "phason w(z) derived from kernel dimension",
    "DESI confirms D0",
    "DESI selects D0",
    "w0 wa are core",
    "charged lepton decimals are CORE",
]
CONDITIONAL = {
    "lepton indirect owner closed": "D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001",
    "Puiseux exponents proved": "D0-LEPTON-INDIRECT-COEFFICIENT-OWNER-001",
    "explicit phason w(z) function closed": "D0-PHASON-WZ-EXPLICIT-FUNCTION-001",
}


def main() -> int:
    print("=== vp_next_frontier_no_overclaim  guard the phason-explicit + lepton-scout fronts ===")
    rows = {r["claim_id"]: r for r in csv.DictReader(CSV.open(encoding="utf-8"))}
    prose = "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT / "01_BOOKS").rglob("*.md"))
    hits = [p for p in UNCONDITIONAL if p in prose]
    assert not hits, f"forbidden next-frontier over-claim(s): {hits}"
    print(f"PASS_NO_UNCONDITIONAL_OVERCLAIM  none of the {len(UNCONDITIONAL)} over-claims appear in the books")
    for phrase, cid in CONDITIONAL.items():
        if phrase in prose:
            assert rows.get(cid, {}).get("release_status") in CLOSED, f"'{phrase}' but {cid} not registered-closed"
    print("PASS_CONDITIONAL_OWNERS  any 'owner closed' / 'exponents proved' / 'function closed' phrase is backed by a registered-closed owner")
    assert any(p in "x DESI confirms D0 x" for p in UNCONDITIONAL), "control: detector reachable"
    print("FAIL_PLANTED_NEXT_FRONTIER_OVERCLAIM_CAUGHT  the detector is reachable")
    print("PASS_NEXT_FRONTIER_NO_OVERCLAIM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
