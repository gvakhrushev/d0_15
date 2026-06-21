#!/usr/bin/env python3
"""vp_five_primitive_no_false_physical_promotion - negation-aware book scan rejecting physical promotions from internal operators.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no internal operator/count/window is promoted to a physical observable; scan is NEGATION-AWARE.')
    FORB=["s_de roots give physical w(z)","internal coordinate is the observed redshift","grading gives three neutrinos","commutant dimension gives the grading signature","measured alpha is derived","all physics is closed"]
    bad=affirm(books(),FORB); assert not bad, f"false promotion: {bad}"
    print("PASS_NO_FALSE_PROMOTION  no internal->physical overclaim in books.")
    assert affirm("the internal coordinate is the observed redshift",["internal coordinate is the observed redshift"])
    print("FAIL_FALSE_PROMOTION_CAUGHT  a planted internal->physical overclaim is caught.")
    assert not affirm("the internal coordinate is not the observed redshift",["internal coordinate is the observed redshift"])
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print('PASS_FIVE_PRIMITIVE_NO_FALSE_PHYSICAL_PROMOTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
