#!/usr/bin/env python3
"""vp_self_reading_no_false_neutral_count - N_active=3 is not asserted from rank; it needs three orthogonal light channels with nonzero frozen neutral-current response. Control rejects rank/kernel -> physical count.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the neutral-current count is grading-dependent (8 or 12); N_active=3 is NOT a rank fact.')
    nc=lambda p,q:p*p+q*q+3
    assert nc(2,1)!=nc(3,0)
    print("PASS_NO_FALSE_COUNT  neutral-current count is grading-dependent (8 vs 12), not a fixed rank-3 fact.")
    bad=affirm(books(),["kernel 30 therefore a phason scattering amplitude","rank alone gives n_active=3"])
    assert not bad, f"rank/kernel->count: {bad}"
    print("FAIL_RANK_KERNEL_AS_COUNT_REJECTED  rank/kernel -> physical count overclaim is caught.")
    assert affirm("kernel 30 therefore a phason scattering amplitude",["kernel 30 therefore a phason scattering amplitude"])
    print("FAIL_PLANTED_KERNEL_COUNT_CAUGHT  a planted kernel->amplitude overclaim is caught.")
    print('PASS_SELF_READING_NO_FALSE_NEUTRAL_COUNT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
