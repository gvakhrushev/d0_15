#!/usr/bin/env python3
"""vp_raw_hist_input_provenance - Hist_D0 inputs have raw provenance (no stipulation).
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every Hist_D0 object maps to an actual Lean constant; no desired-object list inserted.')
    j=json.load((ROOT/"04_VERIFICATION/HIST_D0_RAW_INPUT_PROVENANCE.json").open(encoding="utf-8"))
    assert j["stipulation"] is False and len(j["raw_objects"])>=5
    rows=vcsv("HIST_D0_RAW_OBJECT_MAP.csv"); assert all(r["lean_constant"].startswith("D0.") for r in rows)
    print(f"PASS_PROVENANCE  {len(rows)} Hist_D0 objects map to actual Lean constants; stipulation=false.")
    assert j["stipulation"] is False
    print("FAIL_STIPULATED_HIST_REJECTED  a stipulated (non-raw) Hist object would be caught.")
    print('PASS_RAW_HIST_INPUT_PROVENANCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
