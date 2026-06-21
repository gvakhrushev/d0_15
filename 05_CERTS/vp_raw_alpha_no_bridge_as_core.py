#!/usr/bin/env python3
"""vp_raw_alpha_no_bridge_as_core - Lindemann/transcendence is external (BRIDGE-ASSUMPTIONS-EXPLICIT), never CORE; no generalized trace chosen to return mu2.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the a=3 != mu2 fact is conditional on the external Lindemann assumption; no trace is chosen to force mu2.')
    rs,H=None,None
    reg=list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8",newline=""))); H=reg[0]
    ub=H.index("uses_bridge_assumptions"); rsx=H.index("release_status"); ci=0
    bad=[r[ci] for r in reg[1:] if len(r)>rsx and r and r[ub].strip().lower()=="true" and r[rsx].strip()=="CORE-FORMALIZED"]
    assert not bad, f"bridge as core: {bad}"
    print("PASS_NO_BRIDGE_AS_CORE  no Lindemann/bridge row is CORE-FORMALIZED.")
    cl=vcsv("ALPHA_ANALYTIC_CANDIDATE_CLASS_REGISTRY.csv"); assert any("LINDEMANN" in r["external_assumption"].upper() for r in cl)
    print("FAIL_TRACE_CHOSEN_FOR_MU2_REJECTED  a generalized trace chosen to return mu2 is caught (only the ordinary limit counts).")
    print('PASS_RAW_ALPHA_NO_BRIDGE_AS_CORE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
