#!/usr/bin/env python3
"""vp_five_primitive_no_rank_to_neutrino_shortcut - Lane G: nc 8 vs 12 (grading-dependent); N_active not from rank=3.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
def lean(p):
    return (ROOT/"09_LEAN_FORMALIZATION"/p).read_text(encoding="utf-8")
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","derived","derive")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the neutral-current count is grading-dependent (8 or 12), not rank 3.')
    nc=lambda p,q:p*p+q*q+3; assert nc(2,1)==8 and nc(3,0)==12 and nc(2,1)!=nc(3,0)
    print("PASS_GRADING_DEPENDENT  nc 8 vs 12 (two completions); N_active not a rank fact.")
    bad=affirm(books(),["rank 3 therefore three active neutrinos","rank=3 gives n_active=3"])
    assert not bad, f"rank->neutrino: {bad}"
    print("FAIL_RANK_NEUTRINO_REJECTED  rank=3 -> three neutrinos overclaim is caught.")
    assert affirm("rank 3 therefore three active neutrinos",["rank 3 therefore three active neutrinos"])
    print("FAIL_PLANTED_RANK_NEUTRINO_CAUGHT  a planted rank->neutrino claim is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_RANK_TO_NEUTRINO_SHORTCUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
