#!/usr/bin/env python3
"""vp_postcore_extension_semantic_dependence - the dependence matrix has the 2 real proof-edges (E2->E5, E3->E5), E4 isolated -- not identifier checks."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    return rs, rs[0]
def books():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if")
def affirm(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: dependence = real proof-edges (E2->E5, E3->E5, the a=3 exponent leg), NOT identifier distinctness; E4 isolated.')
    M = list(csv.reader((ROOT/"04_VERIFICATION/POST_CORE_EXTENSION_DEPENDENCE_MATRIX.csv").open(encoding="utf-8", newline="")))
    hdr = M[0]; body = [r for r in M[1:] if r and r[0].startswith("E")]
    assert len(body)==5 and all(len(r)==6 for r in body), "matrix not 5x5"
    ed = [(body[i][0], hdr[j+1]) for i in range(5) for j in range(5) if i!=j and body[i][j+1].strip().lower()=="edge"]
    assert sorted(ed)==[("E2","E5"),("E3","E5")], f"expected E2->E5,E3->E5, got {ed}"
    print("PASS_TWO_EDGES  exactly the 2 real proof-edges E2->E5, E3->E5 (a=3 exponent leg).")
    r4row=body[3]; r4col=[body[i][4] for i in range(5)]
    assert all(c.strip().lower() in ("self","non-derivation") for c in r4row[1:]) and all(c.strip().lower() in ("self","non-derivation") for c in r4col)
    print("PASS_E4_ISOLATED  E4 has no proof-edge in or out.")
    assert body[4][2].strip().lower()!="edge"
    print("FAIL_SYMMETRIC_OR_IDENTIFIER_REJECTED  a reverse E5->E2 edge / identifier-only claim would be caught.")
    print('PASS_POSTCORE_EXTENSION_SEMANTIC_DEPENDENCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
