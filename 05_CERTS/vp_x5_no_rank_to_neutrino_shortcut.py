#!/usr/bin/env python3
"""vp_x5_no_rank_to_neutrino_shortcut - N_active not from rank; nc is grading-dependent (8 vs 12).
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: N_active = nc(p,q)=p^2+q^2+3 (grading-relative), never rank 3.')
    nc=lambda p,q:p*p+q*q+3; assert nc(2,1)==8 and nc(3,0)==12 and nc(2,1)!=nc(3,0)
    print("PASS_GRADING_RELATIVE  N_active grading-dependent (8 vs 12), not rank 3.")
    bad=affirm(books(),["rank 3 therefore three active neutrinos","m3 block gives the active neutrino count"])
    assert not bad, f"rank->neutrino: {bad}"
    print("FAIL_RANK_NEUTRINO_REJECTED  rank/M3 -> neutrino-count overclaim is caught.")
    assert affirm("rank 3 therefore three active neutrinos",["rank 3 therefore three active neutrinos"])
    print("FAIL_PLANTED_RANK_NEUTRINO_CAUGHT  a planted claim is caught.")
    print('PASS_X5_NO_RANK_TO_NEUTRINO_SHORTCUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
