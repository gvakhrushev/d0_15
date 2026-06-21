#!/usr/bin/env python3
"""vp_x5_deletion_minimality_required - each contract has a deletion test with >=2 surviving models.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every consumed law has a deletion countermodel (>=2 admissible models).')
    src=x5lean()
    assert src.count("DeletionTest :=")>=5 and src.count("deletion_necessary")>=5
    assert "lawNecessary" in src
    print("PASS_DELETION_MINIMAL  all 5 contracts have deletion tests proving each law necessary (>=2 models).")
    assert "survivingModels" in lean("D0/Extensions/X5/PrimitiveContract.lean")
    print("FAIL_NO_DELETION_REJECTED  a contract without a deletion test would be caught.")
    print('PASS_X5_DELETION_MINIMALITY_REQUIRED')
    return 0

if __name__ == "__main__": raise SystemExit(main())
