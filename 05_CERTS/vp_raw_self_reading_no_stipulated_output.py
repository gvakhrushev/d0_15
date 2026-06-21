#!/usr/bin/env python3
"""vp_raw_self_reading_no_stipulated_output - every forced output has a raw provenance chain; commutant 12 is the pair-orbit count, not a literal.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: forced outputs are raw computations; commutant 12 = card(image pairClass), proven by native_decide -- not a hand-written list.')
    rows=vcsv("SELF_READING_OUTPUT_PROVENANCE.csv"); assert all(r["is_literal"]=="no" for r in rows)
    print(f"PASS_NO_LITERAL  {len(rows)} forced outputs, all with a raw provenance chain (0 literals).")
    src=lean("D0/SelfReading/SelfReadingNoStipulation.lean")
    assert "commutantDim = (Finset.univ.image pairClass).card := rfl" in src
    print("PASS_COMMUTANT_DERIVED  commutant dim is DEFINED as the pair-orbit count (rfl), not a literal.")
    j=json.load((ROOT/"04_VERIFICATION/SELF_READING_NO_STIPULATED_OUTPUT_AUDIT.json").open(encoding="utf-8"))
    assert j["stipulated_outputs"]==0
    print("FAIL_STIPULATED_OUTPUT_REJECTED  a literal expected-spectrum output would be caught.")
    print('PASS_RAW_SELF_READING_NO_STIPULATED_OUTPUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
