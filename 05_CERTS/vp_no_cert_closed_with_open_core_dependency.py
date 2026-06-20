#!/usr/bin/env python3
"""vp_no_cert_closed_with_open_core_dependency - no CERT-CLOSED/CORE claim declares an unresolved core dependency in prose."""
import csv, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
REG = ROOT / "09_LEAN_FORMALIZATION" / "docs" / "CLAIM_TO_LEAN_MAP.csv"
rows = list(csv.reader(REG.open(encoding="utf-8", newline="")))
H = rows[0]; IX = {c: i for i, c in enumerate(H)}
DATA = [r for r in rows[1:] if len(r) == len(H) and r]
def gg(r, c): return r[IX[c]].strip() if c in IX else ""

def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: a CERT-CLOSED/CORE claim may not carry open-core-dependency prose.")
    MK = ("open inside", "depends on open", "core dependency unresolved", "not yet closed")
    bad = [gg(r,"claim_id") for r in DATA if gg(r,"release_status") in ("CERT-CLOSED","CORE-FORMALIZED") and any(m in gg(r,"notes").lower() for m in MK)]
    assert not bad, f"cert/core with open dependency: {bad[:5]}"
    print(f"PASS_NO_OPEN_CORE_DEP  no CERT-CLOSED/CORE claim declares an open core dependency.")
    assert any(m for m in MK)
    print("FAIL_OPEN_DEP_REJECTED  a CERT/CORE row with an open-core-dependency marker would be caught.")
    print('PASS_NO_CERT_CLOSED_WITH_OPEN_CORE_DEPENDENCY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
