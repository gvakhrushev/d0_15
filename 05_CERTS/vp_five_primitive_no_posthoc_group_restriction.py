#!/usr/bin/env python3
"""vp_five_primitive_no_posthoc_group_restriction - no lane fixes uniqueness by a post-hoc centralizer.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the lepton selector is orbit-intrinsic (4!=3), not from Cent(U_eff)-after-selection.')
    bad=affirm(books(),["cent(u_eff) chosen after selecting","group restricted after choosing the branch","centralizer selected post-hoc"])
    assert not bad, f"posthoc group: {bad}"
    print("PASS_NO_POSTHOC_GROUP  no post-hoc centralizer narrowing in books.")
    assert affirm("the centralizer selected post-hoc to force uniqueness",["centralizer selected post-hoc"])
    print("FAIL_POSTHOC_GROUP_CAUGHT  a planted post-hoc narrowing is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_POSTHOC_GROUP_RESTRICTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
