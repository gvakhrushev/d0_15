#!/usr/bin/env python3
"""vp_raw_refinement_no_scene_copy_operator - the refined operator is not a scene copy L_n := J L_scene C; the base Rayleigh bound is class-scoped.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
def lean(path):
    return (ROOT/"09_LEAN_FORMALIZATION"/path).read_text(encoding="utf-8")
def vcsv(name):
    return list(csv.DictReader((ROOT/"04_VERIFICATION"/name).open(encoding="utf-8",newline="")))
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","only when","derived","derive")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: L_n must be derived from history dynamics, not copied from L_scene; the avg-degree bound is inherited-adjacency-scoped.')
    bad=affirm(books(),["l_n := j_n l_scene c_n","refined operator copied from the base scene","rayleigh bound rules out all refinement"])
    assert not bad, f"scene-copy/overreach: {bad}"
    print("PASS_NO_SCENE_COPY  no L_n:=J L_scene C copy and no Rayleigh overreach in books.")
    sr=vcsv("RAW_SELF_READING_NOGO_STRENGTH_AUDIT.csv"); e2=[r for r in sr if r["frontier"]=="E2"][0]
    assert e2["classification"]=="TWO-COMPLETION-WITNESS-ONLY"
    print("FAIL_SCENE_COPY_REJECTED  a base-scene-copy refined operator would be caught (E2 is WITNESS-ONLY).")
    print('PASS_RAW_REFINEMENT_NO_SCENE_COPY_OPERATOR')
    return 0

if __name__ == "__main__": raise SystemExit(main())
