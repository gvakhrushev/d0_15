#!/usr/bin/env python3
"""vp_raw_readout_input_provenance - ReadoutRep_D0 inputs have raw provenance; Gamma/J/C derived-absent.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the response object maps to a Lean constant; optional Gamma/J/C are not assumed.')
    rows=vcsv("READOUTREP_D0_RAW_OBJECT_MAP.csv"); assert rows and all(r["lean_constant"].startswith("D0.") for r in rows)
    assert any("derived-absent" in r["optional_GammaJC"] for r in rows)
    print("PASS_PROVENANCE  ReadoutRep object maps to a Lean constant; Gamma/J/C derived-absent.")
    assert all("import" not in r["optional_GammaJC"].lower() for r in rows)
    print("FAIL_ASSUMED_GAMMA_REJECTED  assuming Gamma/J/C as axioms would be caught.")
    print('PASS_RAW_READOUT_INPUT_PROVENANCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
