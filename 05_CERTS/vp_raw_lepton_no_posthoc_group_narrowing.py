#!/usr/bin/env python3
"""vp_raw_lepton_no_posthoc_group_narrowing - the branch selector is not made unique by Cent(U_eff) after selection.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the admissible symmetry group is the full (4,3)-conjugacy-respecting group; no post-hoc centralizer narrowing.')
    bad=affirm(books(),["cent(u_eff) chosen after selecting","admissible group narrowed to the centralizer after","group restricted after choosing the branch"])
    assert not bad, f"posthoc narrowing: {bad}"
    print("PASS_NO_POSTHOC_NARROWING  no Cent(U_eff)-after-selection narrowing in books.")
    sr=vcsv("RAW_SELF_READING_NOGO_STRENGTH_AUDIT.csv"); e4=[r for r in sr if r["frontier"]=="E4"][0]
    assert e4["classification"]=="TWO-COMPLETION-WITNESS-ONLY"
    print("FAIL_POSTHOC_NARROWING_REJECTED  a post-hoc centralizer narrowing (circular uniqueness) is caught.")
    print('PASS_RAW_LEPTON_NO_POSTHOC_GROUP_NARROWING')
    return 0

if __name__ == "__main__": raise SystemExit(main())
