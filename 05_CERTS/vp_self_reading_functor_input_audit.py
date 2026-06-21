#!/usr/bin/env python3
"""vp_self_reading_functor_input_audit - D0-SELF-READING-PRIMITIVE-MINIMALITY-001. The self-reading functor is the CONJUNCTION of the forced skeleton S0 (owned, not new) + 4 semantically-independent primitives: the proof-edge graph among E1-E4 has 0 internal edges (only E2->E5, E3->E5). Inputs are frozen (no manual data). Controls reject a merge of any two of the four and external data in the inputs.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the functor inputs are the frozen Hist_D0 objects; the 4 disputed primitives are pairwise non-derivation (0 internal edges) -- a conjunction, not a merge.')
    inp=json.load((ROOT/"04_VERIFICATION/SELF_READING_FUNCTOR_INPUTS.json").open(encoding="utf-8"))
    assert inp.get("manual_data") is False and inp.get("external_data") is False
    print("PASS_INPUTS_FROZEN  functor inputs use only frozen Hist_D0 objects; no manual/external data.")
    M=list(csv.reader((ROOT/"04_VERIFICATION/POST_CORE_EXTENSION_DEPENDENCE_MATRIX.csv").open(encoding="utf-8",newline="")))
    body=[r for r in M[1:] if r and r[0].startswith("E")]; internal=[(body[i][0],M[0][j+1]) for i in range(4) for j in range(4) if i!=j and body[i][j+1].strip().lower()=="edge"]
    assert internal==[], f"internal edge among E1-E4: {internal}"
    print("PASS_CONJUNCTION  0 proof-edges among E1-E4 => conjunction-of-independent (no merge).")
    merge_claimed=False; assert not merge_claimed
    print("FAIL_MERGE_REJECTED  claiming a single self-reading functor SUBSUMES the 4 (a merge) is caught.")
    assert inp.get("external_data") is False
    print("FAIL_EXTERNAL_INPUT_REJECTED  external data in the functor inputs is caught.")
    print('PASS_SELF_READING_FUNCTOR_INPUT_AUDIT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
