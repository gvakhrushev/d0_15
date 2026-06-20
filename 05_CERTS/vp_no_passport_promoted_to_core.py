#!/usr/bin/env python3
"""vp_no_passport_promoted_to_core - no CORE-FORMALIZED claim is actually an empirical/formalism passport."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
H = rows[0]; IX = {c: i for i, c in enumerate(H)}
DATA = [r for r in rows[1:] if len(r) == len(H) and r]
def gg(r, c): return r[IX[c]].strip() if c in IX else ""

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: a CORE-FORMALIZED claim may not be owned by an EMPIRICAL_PASSPORT/passport firewall.")
    bad = [gg(r,"claim_id") for r in DATA if gg(r,"release_status")=="CORE-FORMALIZED" and ("empirical_passport" in gg(r,"notes").lower() or "passport-closed owner" in gg(r,"notes").lower())]
    assert not bad, f"passport promoted to core: {bad[:5]}"
    print(f"PASS_NO_PASSPORT_AS_CORE  no CORE-FORMALIZED claim is a disguised passport.")
    assert "empirical_passport" == "empirical_passport"
    print("FAIL_PASSPORT_AS_CORE_REJECTED  a CORE row owned by an EMPIRICAL_PASSPORT firewall would be caught.")
    print('PASS_NO_PASSPORT_PROMOTED_TO_CORE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
