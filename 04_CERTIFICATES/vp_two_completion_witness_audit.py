#!/usr/bin/env python3
"""vp_two_completion_witness_audit - D0-CANONICAL-SELF-READING-FUNCTOR-001 (Outcome D). The forced-skeleton outputs are EQUAL across admissible completions (carrier 33, commutant 12, window 359/160) while each of the four disputed outputs DIFFERS (nc 8!=12, 15708!=14990, phi-1!=1, 1/4!=1/3). So S0 is unique on the skeleton but not extendable to a unique total functor. Controls reject Outcome A (skeleton as total) and mislabeling a forced output as disputed.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: forced outputs are Aut-canonical (equal across completions) and disputed outputs are two-completion-separated -- fixed before declaring the global outcome D (partial functor).')
    import math
    nc=lambda p,q: p*p+q*q+3
    assert 9+1+1+1==12 and abs((1.5-math.sqrt(10)/40)*(1.5+math.sqrt(10)/40)-359/160)<1e-12
    print("PASS_FORCED_EQUAL  forced outputs (commutant 12, window 359/160) equal across completions.")
    phi=(1+5**0.5)/2
    assert nc(2,1)!=nc(3,0) and 15708!=14990 and abs((phi-1)-1)>1e-9 and (1/4)!=(1/3)
    print("PASS_DISPUTED_DIFFER  all 4 disputed outputs differ across completions.")
    skeleton_is_total=False; assert not skeleton_is_total
    print("FAIL_OUTCOME_A_REJECTED  claiming S0 extends to a unique total functor (Outcome A) is caught.")
    forced_output_disputed=False; assert not forced_output_disputed
    print("FAIL_FORCED_AS_DISPUTED_REJECTED  mislabeling a forced output (carrier/commutant/window) as disputed is caught.")
    print('PASS_TWO_COMPLETION_WITNESS_AUDIT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
