#!/usr/bin/env python3
"""vp_x5_no_grading_dim_shortcut - commutant dimension does not by itself give a grading signature.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the grading signature is a postulated D0-X5 contract choice, not read off dim 12.')
    bad=affirm(books(),["commutant dimension gives the grading signature","dim 12 fixes the grading signature"])
    assert not bad, f"dim->signature: {bad}"
    print("PASS_NO_DIM_SHORTCUT  no commutant-dim -> grading-signature claim in books.")
    assert affirm("the commutant dimension gives the grading signature",["commutant dimension gives the grading signature"])
    print("FAIL_DIM_SHORTCUT_CAUGHT  a planted dim->signature claim is caught.")
    print('PASS_X5_NO_GRADING_DIM_SHORTCUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
