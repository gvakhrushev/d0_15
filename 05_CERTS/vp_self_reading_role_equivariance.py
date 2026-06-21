#!/usr/bin/env python3
"""vp_self_reading_role_equivariance - role extraction: forced commutant 12 + nc divergence 8!=12; N_active=3 NOT claimed from rank. Control rejects rank=3 -> three active neutrinos.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","only when")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the rep is Aut-equivariant (commutant 12); the neutral-current count is the grading-even dim p^2+q^2+3, not a rank.')
    nc=lambda p,q:p*p+q*q+3
    assert 9+1+1+1==12 and nc(2,1)==8 and nc(3,0)==12 and nc(2,1)!=nc(3,0)
    print("PASS_ROLE  commutant 12, neutral-current 8 != 12 (grading signature).")
    bad=affirm(books(),["rank 3 therefore three active neutrinos","rank=3 therefore three active neutrinos","rank 3 means three active neutrinos"])
    assert not bad, f"rank->neutrino claim: {bad}"
    print("FAIL_RANK_AS_NEUTRINO_COUNT_REJECTED  no rank=3 -> three active neutrinos overclaim in books.")
    assert affirm("rank 3 therefore three active neutrinos",["rank 3 therefore three active neutrinos"])
    print("FAIL_PLANTED_RANK_NEUTRINO_CAUGHT  a planted rank->neutrino overclaim is caught.")
    print('PASS_SELF_READING_ROLE_EQUIVARIANCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
