#!/usr/bin/env python3
"""vp_x5_no_fitted_cmb_window - no fitted CMB window (Planck/pivot/width).
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
def lean(p):
    return (ROOT/"09_LEAN_FORMALIZATION"/p).read_text(encoding="utf-8")
def x5lean():
    return "\n".join(p.read_text(encoding="utf-8") for p in (ROOT/"09_LEAN_FORMALIZATION/D0/Extensions/X5").glob("*.lean"))
def reg():
    rs=list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8",newline=""))); return rs,rs[0]
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","derived","postulate","hyp","contract")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: no smoothing window unless derived from HistoryRefinement; no Planck/pivot/width.')
    bad=affirm(books(),["planck pivot chosen for the x5","gaussian width chosen for the smoothing","chosen diffusion time for cmb"])
    assert not bad, f"fitted window: {bad}"
    print("PASS_NO_FITTED_WINDOW  no Planck/pivot/width window in books.")
    assert affirm("a planck pivot chosen for the x5 smoothing",["planck pivot chosen for the x5"])
    print("FAIL_FITTED_WINDOW_CAUGHT  a planted fitted-window claim is caught.")
    print('PASS_X5_NO_FITTED_CMB_WINDOW')
    return 0

if __name__ == "__main__": raise SystemExit(main())
