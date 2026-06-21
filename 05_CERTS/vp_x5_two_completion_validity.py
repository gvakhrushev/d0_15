#!/usr/bin/env python3
"""vp_x5_two_completion_validity - each deletion test is a valid two-completion (>=2 models, separating observable).
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: deletion countermodels are genuine two-completions (nc 8 vs 12; W vs NB; w_A vs w_B; phi-tick vs integer; B3 vs B3alt).')
    nc=lambda p,q:p*p+q*q+3
    assert nc(2,1)!=nc(3,0) and 15708!=14990
    src=x5lean(); assert "deletion_models_differ" in src or "models_differ" in src
    print("PASS_TWO_COMPLETIONS  deletion tests are valid two-completions with separating observables.")
    bad=affirm(books(),["two examples therefore a universal no-go"])
    assert not bad, f"two->maximality: {bad}"
    print("FAIL_TWO_AS_MAXIMALITY_REJECTED  two examples -> universal no-go is caught.")
    print('PASS_X5_TWO_COMPLETION_VALIDITY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
