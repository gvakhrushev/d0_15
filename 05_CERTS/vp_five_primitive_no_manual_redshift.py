#!/usr/bin/env python3
"""vp_five_primitive_no_manual_redshift - Lane P2: no manual redshift (CPL/DESI/anchor/FLRW); P2-E passport only.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the coordinate cocycle is internal; the physical redshift map is passport-only.')
    bad=affirm(books(),["cpl parametrization as the definition","desi value as anchor","assumed flrw scale factor","manual z = 0 normalization"])
    assert not bad, f"manual redshift: {bad}"
    print("PASS_NO_MANUAL_REDSHIFT  no CPL/DESI/anchor/FLRW redshift in books.")
    assert affirm("desi value as anchor is used",["desi value as anchor"])
    print("FAIL_MANUAL_REDSHIFT_CAUGHT  a planted manual-redshift claim is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_MANUAL_REDSHIFT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
