#!/usr/bin/env python3
"""vp_root_operator_semantic_independence - the semantic matrix has exactly one directed proof-edge (R3->R5), R4 isolated, asymmetric -- NOT a Nodup distinctness claim."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; return rs, H
def book_prose():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject")
def affirm_hits(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-44):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: semantic dependence = real proof-edges (one: R3->R5), not identifier distinctness; R4 isolated; asymmetric.')
    M = list(csv.reader((ROOT/"04_VERIFICATION/ROOT_OPERATOR_SEMANTIC_DEPENDENCE_MATRIX.csv").open(encoding="utf-8", newline="")))
    hdr = M[0]; body = [r for r in M[1:] if r and r[0].startswith("R")]
    assert len(body) == 5 and all(len(r) == 6 for r in body), "matrix not 5x5"
    edges = [(body[i][0], hdr[j+1]) for i in range(5) for j in range(5) if i != j and body[i][j+1].strip().lower() == "edge"]
    assert edges == [("R3","R5")], f"expected exactly [R3->R5], got {edges}"
    print("PASS_ONE_EDGE  exactly one directed proof-edge R3->R5 (not Nodup).")
    # R4 isolated
    r4row = body[3]; r4col = [body[i][4] for i in range(5)]
    assert all(c.strip().lower() in ("self","-","") for c in r4row[1:]) and all(c.strip().lower() in ("self","-","") for c in r4col)
    print("PASS_R4_ISOLATED  R4 has no proof-edge in or out.")
    # asymmetric
    assert body[4][3].strip().lower() != "edge"
    print("FAIL_SYMMETRIC_OR_NODUP_REJECTED  a symmetric R5->R3 edge / Nodup-only claim would be caught.")
    print('PASS_ROOT_OPERATOR_SEMANTIC_INDEPENDENCE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
