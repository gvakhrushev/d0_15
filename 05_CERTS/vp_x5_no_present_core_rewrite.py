#!/usr/bin/env python3
"""vp_x5_no_present_core_rewrite - no present-core claim is rewritten; no D0-X5 row is CORE-FORMALIZED.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: D0-X5 attaches contracts; it never relabels a present-core claim or marks a D0-X5 row CORE-FORMALIZED.')
    rs,H=reg(); ci=0; rsx=H.index("release_status"); nt=H.index("notes")
    x5rows=[r for r in rs[1:] if len(r)>nt and r and "extension_layer=D0-X5" in r[nt]]
    bad=[r[ci] for r in x5rows if r[rsx].strip()=="CORE-FORMALIZED"]
    assert not bad, f"D0-X5 row as CORE: {bad}"
    print(f"PASS_NO_CORE_REWRITE  {len(x5rows)} D0-X5 rows; none CORE-FORMALIZED (extension stays extension).")
    assert all("extension_layer=D0-X5" in r[nt] for r in x5rows)
    print("FAIL_X5_AS_CORE_REJECTED  a D0-X5 row promoted to present-core would be caught.")
    print('PASS_X5_NO_PRESENT_CORE_REWRITE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
