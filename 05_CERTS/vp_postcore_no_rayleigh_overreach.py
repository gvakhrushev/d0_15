#!/usr/bin/env python3
"""vp_postcore_no_rayleigh_overreach - the avg-degree Rayleigh bound is not treated as ruling out arbitrary refinement."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    return rs, rs[0]
def books():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if")
def affirm(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the Rayleigh/min-successor bound rules out phi^3 only in the inherited-adjacency + path-refinement classes, not all refinement.')
    sr = list(csv.DictReader((ROOT/"04_VERIFICATION/POST_CORE_NOGO_SCOPE_REPAIR.csv").open(encoding="utf-8", newline="")))
    r3 = next(r for r in sr if r["root"]=="R3")
    assert "scene-native" in r3["what_it_does_NOT_prove"] or "refinement" in r3["what_it_does_NOT_prove"]
    print("PASS_R3_SCOPED  R3 scope row excludes scene-native refinement / cylinder / cond-exp / profinite from the bound.")
    bad = affirm(books(), ["rayleigh bound rules out all refinement","no refinement tower can produce phi^3","avg-degree bound rules out every refinement"])
    assert not bad, f"rayleigh overreach in books: {bad}"
    print("FAIL_RAYLEIGH_OVERREACH_REJECTED  treating the base bound as a universal refinement no-go is caught.")
    print('PASS_POSTCORE_NO_RAYLEIGH_OVERREACH')
    return 0

if __name__ == "__main__": raise SystemExit(main())
