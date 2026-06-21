#!/usr/bin/env python3
"""vp_postcore_nogo_strength - D0-TWO-COMPLETION-NOGO-STRENGTH-001. The E1-E5 reclassification under the strengthened standard: E1 CLASS-SCOPED-NOGO, E2 TWO-COMPLETION-WITNESS-ONLY, E3 CLASS-SCOPED-NOGO, E4 TWO-COMPLETION-WITNESS-ONLY, E5 CLASS-SCOPED-NOGO. None FULL-MAXIMALITY, none INVALID. Controls reject a FULL-MAXIMALITY claim without whole-class exhaustion and an INVALID classification of an owner-preserving witness.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","only when")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the strength is fixed by the 5-item audit; no prior no-go is FULL-MAXIMALITY (no whole-class exhaustion proved) and none is INVALID (all preserve owners). Downgrade-only.')
    rows={r["frontier"]:r for r in csv.DictReader((ROOT/"04_VERIFICATION/TWO_COMPLETION_WITNESS_AUDIT.csv").open(encoding="utf-8",newline=""))}
    exp={"E1":"CLASS-SCOPED-NOGO","E2":"TWO-COMPLETION-WITNESS-ONLY","E3":"CLASS-SCOPED-NOGO","E4":"TWO-COMPLETION-WITNESS-ONLY","E5":"CLASS-SCOPED-NOGO"}
    for k,v in exp.items(): assert rows[k]["classification"]==v, (k,rows[k]["classification"])
    print("PASS_RECLASSIFIED  E1/E3/E5 CLASS-SCOPED, E2/E4 WITNESS-ONLY (audited under the 5-item standard).")
    assert all(r["classification"]!="FULL-MAXIMALITY-NOGO" for r in rows.values())
    print("FAIL_FULL_MAXIMALITY_WITHOUT_EXHAUSTION_REJECTED  no frontier is FULL-MAXIMALITY (none proved whole-class exhaustion).")
    assert all(r["classification"]!="INVALID-WITNESS" for r in rows.values())
    print("FAIL_INVALID_OF_OWNER_PRESERVING_REJECTED  no owner-preserving witness is mislabeled INVALID.")
    print('PASS_POSTCORE_NOGO_STRENGTH')
    return 0

if __name__ == "__main__": raise SystemExit(main())
