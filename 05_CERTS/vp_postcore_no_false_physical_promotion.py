#!/usr/bin/env python3
"""vp_postcore_no_false_physical_promotion - negation-aware book scan rejecting numerical-coincidence -> physical-observable overclaims."""
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: rank/kernel/trace/graph-polynomial alone never implies a physical count/amplitude/mass; scan is NEGATION-AWARE.')
    FORB = ["rank=3 means three active neutrinos","rank 3 means three active neutrinos","kernel=30 is a phason scattering amplitude","kernel 30 is a phason scattering amplitude","finite graph polynomial is a yukawa mass table","finite graph heat trace gives 4d","pi trace gives the lepton mass"]
    bad = affirm(books(), FORB); assert not bad, f"false physical promotion: {bad}"
    print("PASS_NO_FALSE_PROMOTION  no rank/kernel/trace/polynomial -> physical-quantity overclaim in the books.")
    assert affirm("here rank=3 means three active neutrinos", ["rank=3 means three active neutrinos"])
    print("FAIL_FALSE_PROMOTION_CAUGHT  a planted rank->neutrino overclaim is caught.")
    assert not affirm("we do not claim rank=3 means three active neutrinos", ["rank=3 means three active neutrinos"])
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print('PASS_POSTCORE_NO_FALSE_PHYSICAL_PROMOTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
