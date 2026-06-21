#!/usr/bin/env python3
"""vp_five_primitive_no_fitted_cmb_window - Lane H: no fitted CMB window (no Planck/pivot/width).
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no forced smoothing window; any window would need Planck/pivot/width (forbidden).')
    bad=affirm(books(),["planck n_s pivot chosen","chosen diffusion scale u","gaussian width chosen for smoothing"])
    assert not bad, f"fitted window: {bad}"
    print("PASS_NO_FITTED_WINDOW  no Planck/pivot/width CMB window in books.")
    assert affirm("the gaussian width chosen for smoothing",["gaussian width chosen for smoothing"])
    print("FAIL_FITTED_WINDOW_CAUGHT  a planted fitted-window claim is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_FITTED_CMB_WINDOW')
    return 0

if __name__ == "__main__": raise SystemExit(main())
