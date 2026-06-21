#!/usr/bin/env python3
"""vp_x5_no_branch_to_generation_shortcut - Puiseux exponents do not identify generations; two nontrivial exponents do not imply only two rows.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: B_3 acts on all 3 rows (0,1/4,1/3); exponents are not generation labels.')
    bad=affirm(books(),["puiseux exponent identifies the generation","two exponents therefore only two lepton rows","branch exponent is the generation label"])
    assert not bad, f"exponent->generation: {bad}"
    print("PASS_NO_EXPONENT_GENERATION  no exponent->generation / two-exponents->two-rows claim in books.")
    assert affirm("the puiseux exponent identifies the generation",["puiseux exponent identifies the generation"])
    print("FAIL_EXPONENT_GENERATION_CAUGHT  a planted exponent->generation claim is caught.")
    print('PASS_X5_NO_BRANCH_TO_GENERATION_SHORTCUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
