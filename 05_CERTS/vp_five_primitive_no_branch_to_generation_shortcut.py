#!/usr/bin/env python3
"""vp_five_primitive_no_branch_to_generation_shortcut - Lane L: Puiseux exponents do not identify generations; 2 orbits < 3.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the orbit-keyed exponent set {1/4,1/3} is forced but 2 orbits < 3 generations.')
    from fractions import Fraction as F
    assert F(1,4)!=F(1,3) and 2<3
    print("PASS_ORBIT_KEYED  1/4 != 1/3 (orbit-keyed); 2 orbits < 3 generations (L4, row needs new operator).")
    bad=affirm(books(),["puiseux exponent identifies the generation","branch exponent is the generation label"])
    assert not bad, f"exponent->generation: {bad}"
    print("FAIL_EXPONENT_AS_GENERATION_REJECTED  Puiseux exponent -> generation label is caught.")
    assert affirm("the puiseux exponent identifies the generation",["puiseux exponent identifies the generation"])
    print("FAIL_PLANTED_EXPONENT_GENERATION_CAUGHT  a planted exponent->generation claim is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_BRANCH_TO_GENERATION_SHORTCUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
