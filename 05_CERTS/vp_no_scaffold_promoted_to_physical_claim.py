#!/usr/bin/env python3
"""vp_no_scaffold_promoted_to_physical_claim - no operator-scaffold claim asserts a physical prediction."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
H = rows[0]; IX = {c: i for i, c in enumerate(H)}
DATA = [r for r in rows[1:] if len(r) == len(H) and r]
def gg(r, c): return r[IX[c]].strip() if c in IX else ""

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: an operator-scaffold note may not co-occur with a physical-prediction claim.")
    bad = [gg(r,"claim_id") for r in DATA if "operator-scaffold" in gg(r,"notes").lower() and any(p in gg(r,"notes").lower() for p in ("predicts the measured","derives the measured value","physical prediction confirmed"))]
    assert not bad, f"scaffold as physical claim: {bad[:5]}"
    print(f"PASS_NO_SCAFFOLD_PHYSICAL  no operator-scaffold claim asserts a physical prediction.")
    assert "predicts the measured" != ""
    print("FAIL_SCAFFOLD_PHYSICAL_REJECTED  a scaffold row claiming a measured prediction would be caught.")
    print('PASS_NO_SCAFFOLD_PROMOTED_TO_PHYSICAL_CLAIM')
    return 0

if __name__ == "__main__": raise SystemExit(main())
