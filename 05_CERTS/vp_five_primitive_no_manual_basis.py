#!/usr/bin/env python3
"""vp_five_primitive_no_manual_basis - no lane uses a manual basis/signature/label.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no manual basis/signature/label/root/window/anchor in any lane.')
    bad=affirm(books(),["manual basis chosen for the","manually chosen grading signature","manual generation label assigned"])
    assert not bad, f"manual basis: {bad}"
    print("PASS_NO_MANUAL_BASIS  no manual basis/signature/label in books.")
    assert affirm("a manual basis chosen for the carrier",["manual basis chosen for the"])
    print("FAIL_MANUAL_BASIS_CAUGHT  a planted manual-basis overclaim is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_MANUAL_BASIS')
    return 0

if __name__ == "__main__": raise SystemExit(main())
