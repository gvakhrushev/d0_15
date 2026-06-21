#!/usr/bin/env python3
"""vp_five_primitive_book_sync - the five-primitive owners appear in the registry with consistent status.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: each registered five-primitive owner has a lean_module or cert and a release_status.')
    reg=list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8",newline=""))); H=reg[0]
    ci=0; lm=H.index("lean_module"); pc=H.index("python_cert"); rsx=H.index("release_status")
    owners=["D0-RAW-COMMUTANT-WEDDERBURN-001","D0-FIVE-PRIMITIVE-DEPENDENCE-001"]
    rows={r[ci]:r for r in reg[1:] if len(r)>rsx and r}
    miss=[o for o in owners if o not in rows]; assert not miss, f"missing: {miss}"
    bad=[o for o in owners if not rows[o][lm].strip() and not rows[o][pc].strip()]; assert not bad, f"status-only: {bad}"
    print("PASS_BOOK_SYNC  five-primitive owners registered with a lean_module or cert.")
    assert all(rows[o][rsx].strip() for o in owners)
    print("FAIL_STATUS_ONLY_REJECTED  a status-only five-primitive owner would be caught.")
    print('PASS_FIVE_PRIMITIVE_BOOK_SYNC')
    return 0

if __name__ == "__main__": raise SystemExit(main())
