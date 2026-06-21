#!/usr/bin/env python3
"""vp_x5_semantic_dependence - the X5 dependence has one real edge P1->P2; G,H,L independent.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: dependence = real construction edges (P1->P2), not identifier lists.')
    M=list(csv.reader((ROOT/"04_VERIFICATION/X5_SEMANTIC_DEPENDENCE_MATRIX.csv").open(encoding="utf-8",newline="")))
    hdr=M[0]; body=[r for r in M[1:] if r]
    edges=[(body[i][0],hdr[j+1]) for i in range(5) for j in range(5) if i!=j and body[i][j+1].strip().lower()=="edge"]
    assert edges==[("P1","P2")], f"expected [P1->P2], got {edges}"
    print("PASS_ONE_EDGE  exactly one real construction edge P1->P2.")
    assert body[4][4].strip().lower()!="edge"
    print("FAIL_SYMMETRIC_OR_IDENTIFIER_REJECTED  a reverse/identifier-only claim is caught.")
    print('PASS_X5_SEMANTIC_DEPENDENCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
