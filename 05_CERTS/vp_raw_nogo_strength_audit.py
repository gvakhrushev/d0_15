#!/usr/bin/env python3
"""vp_raw_nogo_strength_audit - E1-E5 reclassification under the 5-item standard; none FULL-MAXIMALITY, none INVALID.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the strengths are fixed by the audit; downgrade-only.')
    sr={r["frontier"]:r["classification"] for r in vcsv("RAW_SELF_READING_NOGO_STRENGTH_AUDIT.csv")}
    exp={"E1":"CLASS-SCOPED-NOGO","E2":"TWO-COMPLETION-WITNESS-ONLY","E3":"CLASS-SCOPED-NOGO","E4":"TWO-COMPLETION-WITNESS-ONLY","E5":"CLASS-SCOPED-NOGO"}
    for k,v in exp.items(): assert sr[k]==v, (k,sr[k])
    print("PASS_RECLASSIFIED  E1/E3/E5 CLASS-SCOPED, E2/E4 WITNESS-ONLY.")
    assert all(v!="FULL-MAXIMALITY-NOGO" for v in sr.values())
    print("FAIL_FULL_MAXIMALITY_REJECTED  no frontier is FULL-MAXIMALITY (no whole-class exhaustion).")
    print('PASS_RAW_NOGO_STRENGTH_AUDIT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
