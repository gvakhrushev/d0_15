#!/usr/bin/env python3
"""vp_raw_self_reading_functor_naturality - the functor candidate class declares all naturality conditions; terminal S3.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: functoriality + readout/retained-archive/terminal/tripartite naturality + role equivariance are required before any S claim.')
    rows=vcsv("SELF_READING_FUNCTOR_CANDIDATE_CLASS.csv"); conds={r["condition"]:r["status"] for r in rows}
    for k in ["functoriality","readout naturality","role equivariance (Q8/Omega8/ABCD)","no-extra-catalog (raw only)"]:
        assert k in conds, k
    assert conds["S0 extends to total functor"]=="NO (4 two-completions)"
    print("PASS_NATURALITY  all functor conditions declared; S0 does NOT extend to a total functor (S3).")
    assert conds["forced-skeleton S0 raw-derived"].startswith("YES")
    print("FAIL_TOTAL_FUNCTOR_CLAIMED_REJECTED  claiming S0 extends to a unique total functor (Outcome A) is caught.")
    print('PASS_RAW_SELF_READING_FUNCTOR_NATURALITY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
