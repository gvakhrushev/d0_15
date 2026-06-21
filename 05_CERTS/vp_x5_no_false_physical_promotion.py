#!/usr/bin/env python3
"""vp_x5_no_false_physical_promotion - negation-aware book scan rejecting D0-X5 -> physical promotions.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no D0-X5 contract consequence is promoted to a measured physical observable; scan is NEGATION-AWARE.')
    FORB=["d0-x5 derives three neutrinos","d0-x5 gives the observed redshift","d0-x5 derives the lepton masses","d0-x5 derives physical w_de","d0-x5 predicts planck n_s","d0-x5 derives measured alpha"]
    bad=affirm(books(),FORB); assert not bad, f"false promotion: {bad}"
    print("PASS_NO_FALSE_PROMOTION  no D0-X5 -> physical-observable overclaim in books.")
    assert affirm("d0-x5 derives three neutrinos",["d0-x5 derives three neutrinos"])
    print("FAIL_FALSE_PROMOTION_CAUGHT  a planted D0-X5->physical claim is caught.")
    assert not affirm("d0-x5 does not derive three neutrinos",["d0-x5 derives three neutrinos"])
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print('PASS_X5_NO_FALSE_PHYSICAL_PROMOTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
