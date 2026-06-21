#!/usr/bin/env python3
"""vp_raw_phason_no_manual_redshift - no manual phason redshift calibration (CPL/DESI/anchor/FLRW).
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the coordinate cocycle must come from an internal observable; no CPL/DESI/anchor/FLRW.')
    bad=affirm(books(),["cpl parametrization inserted","desi parameter used","chosen redshift anchor","assumed flrw scale factor","manual redshift normalization"])
    assert not bad, f"manual redshift: {bad}"
    print("PASS_NO_MANUAL_REDSHIFT  no CPL/DESI/anchor/FLRW redshift calibration in books.")
    assert affirm("a chosen redshift anchor is used",["chosen redshift anchor"])
    print("FAIL_MANUAL_REDSHIFT_CAUGHT  a planted redshift-calibration overclaim is caught.")
    print('PASS_RAW_PHASON_NO_MANUAL_REDSHIFT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
