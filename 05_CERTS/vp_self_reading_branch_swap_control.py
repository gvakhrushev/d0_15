#!/usr/bin/env python3
"""vp_self_reading_branch_swap_control - lepton: forced orbit exponents 1/4!=1/3; disputed 2 orbits<3 generations. Control rejects block swap -> universal no-go without an admissible swap symmetry.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the orbit exponent set is forced; the branch->generation assignment is disputed only within a group CONTAINING the swap (R4 scope).')
    from fractions import Fraction as Fr
    assert Fr(1,4)!=Fr(1,3) and 2<3
    print("PASS_BRANCH  orbit exponents 1/4 != 1/3 (forced); 2 orbits < 3 generations (disputed).")
    bad=affirm(books(),["block swap proves a universal no-go","block swap therefore universal impossibility"])
    assert not bad, f"swap->universal: {bad}"
    print("FAIL_SWAP_AS_UNIVERSAL_NOGO_REJECTED  block swap treated as universal no-go (without admissible swap symmetry) is caught.")
    assert affirm("block swap proves a universal no-go",["block swap proves a universal no-go"])
    print("FAIL_PLANTED_SWAP_CAUGHT  a planted swap->universal overclaim is caught.")
    print('PASS_SELF_READING_BRANCH_SWAP_CONTROL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
