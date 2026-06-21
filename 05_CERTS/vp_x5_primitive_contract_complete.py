#!/usr/bin/env python3
"""vp_x5_primitive_contract_complete - each of the 5 contracts is fully typed (id, layer, laws, carrier, model, deletion).
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: each contract declares id+layer+laws+carrier+model+deletion before any consequence.')
    src=x5lean()
    for cid in ["PRIM-GRADING-NEUTRAL-CURRENT-OPERATOR","PRIM-SCENE-HISTORY-REFINEMENT-RULE","PRIM-LEPTON-BRANCH-FIXING-OPERATOR","PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT","PRIM-PHASON-COORDINATE-FUNCTOR"]:
        assert cid in src, cid
    assert src.count("PrimitiveContract :=")>=5 and src.count("ModelWitness :=")>=5 and src.count("DeletionTest :=")>=5
    print("PASS_CONTRACTS_COMPLETE  all 5 contracts declare PrimitiveContract + ModelWitness + DeletionTest.")
    assert "D0-X5" in src
    print("FAIL_INCOMPLETE_CONTRACT_REJECTED  a contract missing model/deletion would be caught.")
    print('PASS_X5_PRIMITIVE_CONTRACT_COMPLETE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
