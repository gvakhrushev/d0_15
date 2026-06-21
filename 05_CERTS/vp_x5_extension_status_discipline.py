#!/usr/bin/env python3
"""vp_x5_extension_status_discipline - every D0-X5 contract row carries extension_layer=D0-X5 in notes and is never CORE-FORMALIZED.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every D0-X5 owner declares extension_layer=D0-X5 (the visible field) and stays an extension, never present-core.')
    rs,H=reg(); ci=0; rsx=H.index("release_status"); nt=H.index("notes")
    x5=[r for r in rs[1:] if len(r)>nt and r and r[ci].startswith("D0-X5")]
    assert x5, "expected D0-X5 rows"
    nolayer=[r[ci] for r in x5 if "extension_layer=D0-X5" not in r[nt]]
    assert not nolayer, f"D0-X5 row missing extension_layer tag: {nolayer}"
    core=[r[ci] for r in x5 if r[rsx].strip()=="CORE-FORMALIZED"]
    assert not core, f"D0-X5 row as CORE: {core}"
    print(f"PASS_X5_DISCIPLINE  {len(x5)} D0-X5 rows: all tagged extension_layer=D0-X5; none CORE-FORMALIZED.")
    assert all("extension_layer=D0-X5" in r[nt] for r in x5)
    print("FAIL_X5_UNTAGGED_OR_CORE_REJECTED  a D0-X5 row missing the tag or marked CORE would be caught.")
    print('PASS_X5_EXTENSION_STATUS_DISCIPLINE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
