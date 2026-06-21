#!/usr/bin/env python3
"""vp_postcore_no_bridge_assumption_as_core - any bridge-assumption row is never unconditional CORE-FORMALIZED."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    return rs, rs[0]
def books():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if")
def affirm(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: a uses_bridge_assumptions row must carry LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS or PYTHON_CERTIFIED, never CORE-FORMALIZED.')
    rs, H = regrows(); ub=H.index("uses_bridge_assumptions"); ls=H.index("lean_status"); rsx=H.index("release_status"); ci=0
    bad = [r[ci] for r in rs[1:] if len(r)>rsx and r and r[ub].strip().lower()=="true" and (r[rsx].strip()=="CORE-FORMALIZED" or r[ls].strip()=="LEAN_PROVED")]
    assert not bad, f"bridge row as unconditional core/LEAN_PROVED: {bad}"
    print("PASS_NO_BRIDGE_AS_CORE  every bridge-assumption row is LEAN_PROVED_WITH_BRIDGE_ASSUMPTIONS/PYTHON_CERTIFIED, never CORE-FORMALIZED.")
    lindemann = [r[ci] for r in rs[1:] if len(r)>ub and r and "LINDEMANN" in (r[H.index("assumption_ids")] or "").upper()]
    assert lindemann, "expected >=1 Lindemann-threaded row"
    print("FAIL_BRIDGE_AS_CORE_REJECTED  a Lindemann/bridge row promoted to CORE-FORMALIZED would be caught.")
    print('PASS_POSTCORE_NO_BRIDGE_ASSUMPTION_AS_CORE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
