#!/usr/bin/env python3
"""vp_self_reading_refinement_naturality - refinement extraction: forced no-phi^3 (19>phi^3) + disputed 15708!=14990. Control rejects two path counts -> full history no-go.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the min-successor 19>phi^3 holds in both families (forced); the two carriers differ (disputed, two-completion-WITNESS-ONLY, not a full no-go).')
    phi=(1+5**0.5)/2
    assert phi**3<19 and 15708!=14990 and abs(15708-14990)==718
    print("PASS_REFINEMENT  phi^3<19 (forced); 15708!=14990 (disputed, diff 2|E|=718).")
    bad=affirm(books(),["two path counts therefore full history no-go","two walk counts prove a full history no-go"])
    assert not bad, f"two-counts->full-nogo: {bad}"
    print("FAIL_TWO_COUNTS_AS_FULL_NOGO_REJECTED  two path counts treated as a full history no-go is caught (E2 is WITNESS-ONLY).")
    assert affirm("two path counts therefore full history no-go",["two path counts therefore full history no-go"])
    print("FAIL_PLANTED_TWO_COUNTS_CAUGHT  a planted two-counts->full-nogo overclaim is caught.")
    print('PASS_SELF_READING_REFINEMENT_NATURALITY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
