#!/usr/bin/env python3
"""vp_five_primitive_no_trace_as_intertwiner - no trace/determinant coincidence is treated as a canonical intertwiner.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: an intertwiner is a typed map, never a trace/det coincidence.')
    bad=affirm(books(),["trace coincidence is an intertwiner","determinant match gives the intertwiner","matching determinants prove a common sector"])
    assert not bad, f"trace-as-intertwiner: {bad}"
    print("PASS_NO_TRACE_INTERTWINER  no trace/det coincidence treated as an intertwiner in books.")
    assert affirm("a trace coincidence is an intertwiner here",["trace coincidence is an intertwiner"])
    print("FAIL_TRACE_INTERTWINER_CAUGHT  a planted trace-as-intertwiner claim is caught.")
    print('PASS_FIVE_PRIMITIVE_NO_TRACE_AS_INTERTWINER')
    return 0

if __name__ == "__main__": raise SystemExit(main())
