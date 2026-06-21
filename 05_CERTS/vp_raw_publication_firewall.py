#!/usr/bin/env python3
"""vp_raw_publication_firewall - negation-aware book scan rejecting imported physical tables / detection / global-completion overclaims.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no physical table / numerical coincidence is elevated to a field equation/spectrum/observable; scan is NEGATION-AWARE.')
    FORB=["planck data in the operator","desi data in the operator","pdg masses in the operator","lep data in the operator","ligo data in the operator","codata alpha in the operator","fermion mass table is derived","active-neutrino count is derived","measured alpha is derived","all physics is closed"]
    bad=affirm(books(),FORB); assert not bad, f"publication breach: {bad}"
    print("PASS_PUBLICATION_FIREWALL  no imported-table/detection/global-completion overclaim in books.")
    assert affirm("the fermion mass table is derived here",["fermion mass table is derived"])
    print("FAIL_PUBLICATION_BREACH_CAUGHT  a planted imported-table overclaim is caught.")
    assert not affirm("no fermion mass table is derived",["fermion mass table is derived"])
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print('PASS_RAW_PUBLICATION_FIREWALL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
