#!/usr/bin/env python3
"""vp_postcore_no_branch_swap_overreach - the block swap is not treated as a universal impossibility."""
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the swap witness proves no canonical assignment only if the admissible group CONTAINS the swap.')
    sr = list(csv.DictReader((ROOT/"04_VERIFICATION/POST_CORE_NOGO_SCOPE_REPAIR.csv").open(encoding="utf-8", newline="")))
    r4 = next(r for r in sr if r["root"]=="R4")
    assert "EXCLUDES" in r4["what_it_does_NOT_prove"] or "exclude" in r4["what_it_does_NOT_prove"].lower()
    print("PASS_R4_SCOPED  R4 scope row makes the no-go conditional on the group CONTAINING the swap.")
    bad = affirm(books(), ["block swap proves no selector can ever exist","swap proves universal impossibility"])
    assert not bad, f"branch-swap overreach in books: {bad}"
    print("FAIL_BRANCH_SWAP_OVERREACH_REJECTED  treating the swap as universal impossibility is caught.")
    print('PASS_POSTCORE_NO_BRANCH_SWAP_OVERREACH')
    return 0

if __name__ == "__main__": raise SystemExit(main())
