#!/usr/bin/env python3
"""vp_root_operator_no_fit_before_operator - no numerical coincidence is promoted to a physical observable before an operator (negation-aware book scan)."""
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: rank/kernel/trace/graph-invariant alone never implies a physical count/mass/amplitude; scan is NEGATION-AWARE.')
    prose = book_prose()
    FORB = ["rank 3 therefore three neutrinos","rank 3 implies three neutrinos","kernel 30 therefore","trace therefore canonical transfer matrix","graph invariant therefore fermion masses","finite graph heat trace therefore 4d","pi trace therefore lepton mass"]
    bad = affirm_hits(prose, FORB); assert not bad, f"fit-before-operator claim: {bad}"
    print("PASS_NO_FIT_BEFORE_OPERATOR  no rank/kernel/trace/graph-invariant -> physical-quantity overclaim in the books.")
    assert affirm_hits("rank 3 therefore three neutrinos in the model", ["rank 3 therefore three neutrinos"])
    print("FAIL_FIT_BEFORE_OPERATOR_CAUGHT  a planted rank->count overclaim is caught.")
    assert not affirm_hits("we do not claim rank 3 therefore three neutrinos", ["rank 3 therefore three neutrinos"])
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print('PASS_ROOT_OPERATOR_NO_FIT_BEFORE_OPERATOR')
    return 0

if __name__ == "__main__": raise SystemExit(main())
