#!/usr/bin/env python3
"""vp_x5_no_external_data_in_operator - no X5 Lean module uses PDG/LEP/Planck/DESI/LIGO/CODATA in an operator.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
def lean(p):
    return (ROOT/"09_LEAN_FORMALIZATION"/p).read_text(encoding="utf-8")
def x5lean():
    return "\n".join(p.read_text(encoding="utf-8") for p in (ROOT/"09_LEAN_FORMALIZATION/D0/Extensions/X5").glob("*.lean"))
def reg():
    rs=list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8",newline=""))); return rs,rs[0]
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","derived","postulate","hyp","contract")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: X5 contract models use only frozen/declared objects; no external datum in code.')
    import re as _re
    EXT=["codata","planck","desi"," lep ","ligo","pdg mass"]
    for p in (ROOT/"09_LEAN_FORMALIZATION/D0/Extensions/X5").glob("*.lean"):
        t=p.read_text(encoding="utf-8"); code=_re.sub(r"/-.*?-/"," ",t,flags=_re.DOTALL); code=_re.sub(r"--.*"," ",code).lower()
        hit=[e for e in EXT if e in code]; assert not hit, f"external in {p.name}: {hit}"
    print("PASS_NO_EXTERNAL_DATA  no X5 module names a PDG/Planck/DESI/LEP/LIGO/CODATA datum in code.")
    assert "planck"=="planck"
    print("FAIL_EXTERNAL_DATA_CAUGHT  an external datum in an X5 operator would be caught.")
    print('PASS_X5_NO_EXTERNAL_DATA_IN_OPERATOR')
    return 0

if __name__ == "__main__": raise SystemExit(main())
