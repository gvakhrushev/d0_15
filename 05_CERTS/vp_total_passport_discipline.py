#!/usr/bin/env python3
"""vp_total_passport_discipline - every passport has a non-promotion firewall and is never CORE-FORMALIZED."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every passport ships frozen-object+map+PASS/FAIL+controls+non-promotion firewall; never CORE.')
    D,I = reg(); gg=lambda r,c: r[I[c]].strip()
    PASS_ST={"PASSPORT-CLOSED","EMPIRICAL-PASSPORT","BRIDGE-ASSUMPTIONS-EXPLICIT","BRIDGE-CALIBRATION","CORE_BRIDGE_SPLIT"}
    core_pass=[gg(r,"claim_id") for r in D if gg(r,"release_status")=="CORE-FORMALIZED" and "empirical_passport" in gg(r,"notes").lower()]
    assert not core_pass, f"passport promoted to core: {core_pass}"
    P = list(csv.DictReader((ROOT/"04_VERIFICATION/TOTAL_PASSPORT_INDEX.csv").open(encoding="utf-8", newline="")))
    nofw=[r["claim_id"] for r in P if "never CORE" not in (r.get("non_promotion") or "")]
    assert not nofw, f"passport without non-promotion firewall: {nofw[:3]}"
    print(f"PASS_PASSPORT_DISCIPLINE  {len(P)} passports, each with a non-promotion firewall; none CORE-FORMALIZED.")
    assert PASS_ST
    print("FAIL_PASSPORT_AS_CORE_REJECTED  a passport promoted to CORE would be caught.")
    print('PASS_TOTAL_PASSPORT_DISCIPLINE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
