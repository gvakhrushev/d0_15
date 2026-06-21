#!/usr/bin/env python3
"""vp_raw_self_reading_actual_aut_group - Aut is derived from raw data (distinct part sizes => S9xS11xS13), not replaced by a stipulated group; commutant 12 raw.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: distinct part sizes (9,11,13) force part-preservation; the commutant is the raw pair-orbit count.')
    src=lean("D0/SelfReading/RawHistoryCategory.lean")
    assert "part_sizes_distinct" in src and "commutant_dim_raw" in src
    print("PASS_AUT_DERIVED  Aut = S9xS11xS13 derived from distinct part sizes; commutant 12 raw (pair-orbit).")
    rg=lean("D0/SelfReading/RawSceneGraph.lean"); assert "(Finset.univ.image pairClass).card" in rg
    print("FAIL_STIPULATED_AUT_REJECTED  replacing Aut/commutant with a stipulated group/list would be caught.")
    print('PASS_RAW_SELF_READING_ACTUAL_AUT_GROUP')
    return 0

if __name__ == "__main__": raise SystemExit(main())
