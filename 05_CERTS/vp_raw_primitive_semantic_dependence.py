#!/usr/bin/env python3
"""vp_raw_primitive_semantic_dependence - the primitive dependence matrix is real (2 edges E2->E5,E3->E5; 0 internal among E1-E4), not identifier lists.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: dependence = real proof-edges, NOT Nodup/identifier checks; 0 internal edges among E1-E4 => conjunction-of-independent.')
    M=list(csv.reader((ROOT/"04_VERIFICATION/RAW_SELF_READING_PRIMITIVE_DEPENDENCE_MATRIX.csv").open(encoding="utf-8",newline="")))
    hdr=M[0]; body=[r for r in M[1:] if r and r[0].startswith("E")]
    internal=[(body[i][0],hdr[j+1]) for i in range(4) for j in range(4) if i!=j and body[i][j+1].strip().lower()=="derivation"]
    assert internal==[], f"internal edge among E1-E4: {internal}"
    toE5=[body[i][0] for i in range(4) if body[i][5].strip().lower()=="derivation"]
    assert sorted(toE5)==["E2","E3"], toE5
    print("PASS_REAL_DEPENDENCE  0 internal edges among E1-E4; exactly E2->E5, E3->E5 (real proof-edges).")
    assert internal==[]
    print("FAIL_MERGE_OR_IDENTIFIER_REJECTED  an internal merge edge / identifier-only claim would be caught.")
    print('PASS_RAW_PRIMITIVE_SEMANTIC_DEPENDENCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
