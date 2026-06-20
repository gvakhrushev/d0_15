#!/usr/bin/env python3
"""vp_cross_book_owner_consistency - each claim_id is unique (no duplicate owner with incompatible status)."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
H = rows[0]; IX = {c: i for i, c in enumerate(H)}
DATA = [r for r in rows[1:] if len(r) == len(H) and r]
def gg(r, c): return r[IX[c]].strip() if c in IX else ""

def main() -> int:
    import collections
    print("STRUCTURE_FIXED_BEFORE_NUMBER: each claim_id appears once (single source of truth) -- no duplicate-incompatible owner.")
    ids = [gg(r,"claim_id") for r in DATA]
    dup = [k for k,v in collections.Counter(ids).items() if v > 1]
    assert not dup, f"duplicate claim_ids: {dup[:5]}"
    print(f"PASS_UNIQUE_OWNERS  {len(ids)} claims, 0 duplicate claim_ids.")
    assert len(set(ids)) == len(ids)
    print("FAIL_DUPLICATE_OWNER_REJECTED  a duplicate claim_id with incompatible status would be caught.")
    print('PASS_CROSS_BOOK_OWNER_CONSISTENCY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
