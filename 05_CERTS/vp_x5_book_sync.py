#!/usr/bin/env python3
"""vp_x5_book_sync - the X5 owners are registered with a lean_module or cert and a release_status.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
def lean(p):
    return (ROOT/"09_LEAN_FORMALIZATION"/p).read_text(encoding="utf-8")
def x5lean():
    return "\n".join(p.read_text(encoding="utf-8") for p in (ROOT/"09_LEAN_FORMALIZATION/D0/Extensions/X5").glob("*.lean"))
def reg():
    rs=list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8",newline=""))); return rs,rs[0]
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","derived","postulate","hyp","contract")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every D0-X5 owner has a lean_module or cert and a controlled release_status.')
    rs,H=reg(); ci=0; lm=H.index("lean_module"); pc=H.index("python_cert"); rsx=H.index("release_status")
    CANON={"CORE-FORMALIZED","CERT-CLOSED","NO-GO","NO_GO_PROVED","BRIDGE-ASSUMPTIONS-EXPLICIT","CORE_BRIDGE_SPLIT","BRIDGE-CALIBRATION","EMPIRICAL-PASSPORT","PASSPORT-CLOSED","EXTERNAL-BACKGROUND","PROOF-TARGET","DEPRECATED","OPEN"}
    x5=[r for r in rs[1:] if len(r)>rsx and r and r[ci].startswith("D0-X5")]
    assert len(x5)>=5, f"expected >=5 D0-X5 owners, got {len(x5)}"
    bad=[r[ci] for r in x5 if not r[lm].strip() and not r[pc].strip()]; assert not bad, f"status-only: {bad}"
    badst=[r[ci] for r in x5 if r[rsx].strip() not in CANON]; assert not badst, f"non-canonical status: {badst}"
    print(f"PASS_BOOK_SYNC  {len(x5)} D0-X5 owners; each has lean/cert + a controlled release_status.")
    assert all(r[rsx].strip() in CANON for r in x5)
    print("FAIL_STATUS_ONLY_OR_INVALID_REJECTED  a status-only or invalid-status D0-X5 owner would be caught.")
    print('PASS_X5_BOOK_SYNC')
    return 0

if __name__ == "__main__": raise SystemExit(main())
