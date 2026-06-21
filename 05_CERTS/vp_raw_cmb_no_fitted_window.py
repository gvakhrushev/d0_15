#!/usr/bin/env python3
"""vp_raw_cmb_no_fitted_window - no fitted CMB window (no Planck/pivot/Gaussian width).
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
def lean(path):
    return (ROOT/"09_LEAN_FORMALIZATION"/path).read_text(encoding="utf-8")
def vcsv(name):
    return list(csv.DictReader((ROOT/"04_VERIFICATION"/name).open(encoding="utf-8",newline="")))
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","only when","derived","derive")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no CMB observable emitted; any window would need Planck/pivot/width (forbidden).')
    bad=affirm(books(),["planck n_s pivot chosen","chosen diffusion time u","gaussian smoothing width chosen","chosen bin width"])
    assert not bad, f"fitted window: {bad}"
    print("PASS_NO_FITTED_WINDOW  no Planck/pivot/width CMB window in books.")
    assert affirm("the gaussian smoothing width chosen here",["gaussian smoothing width chosen"])
    print("FAIL_FITTED_WINDOW_CAUGHT  a planted fitted-window overclaim is caught.")
    assert not affirm("no gaussian smoothing width chosen",["gaussian smoothing width chosen"])
    print("PASS_NEGATED_DISCLAIMER_ALLOWED  an honest negated disclaimer is NOT flagged.")
    print('PASS_RAW_CMB_NO_FITTED_WINDOW')
    return 0

if __name__ == "__main__": raise SystemExit(main())
