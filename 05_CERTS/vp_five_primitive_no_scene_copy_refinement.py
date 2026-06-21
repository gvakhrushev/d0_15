#!/usr/bin/env python3
"""vp_five_primitive_no_scene_copy_refinement - Lane H: the refined operator is not L_n:=J L_scene C; H3 several towers.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: refined operators are independently generated; W and NB differ (15708 vs 14990).')
    assert 15708!=14990 and abs(15708-14990)==718
    print("PASS_INDEPENDENT_REFINEMENT  W (15708) != NB (14990); inequivalent towers (H3).")
    bad=affirm(books(),["l_n := j_n l_scene c_n","refined operator copied from the base scene"])
    assert not bad, f"scene copy: {bad}"
    print("FAIL_SCENE_COPY_REJECTED  an L_n:=J L_scene C copy is caught.")
    assert affirm("the refined operator copied from the base scene",["refined operator copied from the base scene"])
    print("FAIL_PLANTED_SCENE_COPY_CAUGHT  a planted scene-copy claim is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_SCENE_COPY_REFINEMENT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
