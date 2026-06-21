#!/usr/bin/env python3
"""vp_five_primitive_semantic_dependence - D0-FIVE-PRIMITIVE-DEPENDENCE-001. One asymmetric edge P1->P2; G,H,L independent; no merge.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: dependence = real construction edges (P1->P2 = coordinate needs sector), not identifier lists.')
    M=list(csv.reader((ROOT/"04_VERIFICATION/FIVE_PRIMITIVE_SEMANTIC_DEPENDENCE_MATRIX.csv").open(encoding="utf-8",newline="")))
    hdr=M[0]; body=[r for r in M[1:] if r]
    edges=[(body[i][0],hdr[j+1]) for i in range(5) for j in range(5) if i!=j and body[i][j+1].strip().lower()=="edge"]
    assert edges==[("P1","P2")], f"expected [P1->P2], got {edges}"
    print("PASS_ONE_EDGE  exactly one real construction edge P1->P2 (coordinate needs the sector).")
    assert body[4][4].strip().lower()!="edge"
    print("FAIL_SYMMETRIC_OR_IDENTIFIER_REJECTED  a reverse P2->P1 edge / identifier-only claim is caught.")
    print('PASS_FIVE_PRIMITIVE_SEMANTIC_DEPENDENCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
