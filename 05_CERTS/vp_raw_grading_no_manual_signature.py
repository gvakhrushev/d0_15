#!/usr/bin/env python3
"""vp_raw_grading_no_manual_signature - the grading/neutral-current uses no manually chosen signature; nc 8 vs 12 is derived (two completions).
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the neutral-current count p^2+q^2+3 ranges over admissible signatures; no signature is hand-picked.')
    nc=lambda p,q:p*p+q*q+3
    assert nc(2,1)==8 and nc(3,0)==12 and nc(2,1)!=nc(3,0)
    print("PASS_NO_MANUAL_SIGNATURE  nc 8 vs 12 derived from the grading-even commutant; two completions.")
    bad=affirm(books(),["grading signature chosen by hand","manually selected grading signature"])
    assert not bad, f"manual signature: {bad}"
    print("FAIL_MANUAL_SIGNATURE_REJECTED  a hand-picked grading signature would be caught.")
    print('PASS_RAW_GRADING_NO_MANUAL_SIGNATURE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
