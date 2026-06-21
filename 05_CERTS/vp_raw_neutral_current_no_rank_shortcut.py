#!/usr/bin/env python3
"""vp_raw_neutral_current_no_rank_shortcut - N_active=3 is not asserted from rank; book scan rejects rank->3-neutrinos.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the neutral count needs three orthogonal light channels with nonzero response, not a rank.')
    bad=affirm(books(),["rank 3 therefore three active neutrinos","rank 3 means three active neutrinos","rank=3 gives three active neutrinos"])
    assert not bad, f"rank->neutrino: {bad}"
    print("PASS_NO_RANK_SHORTCUT  no rank=3 -> three active neutrinos overclaim in books.")
    assert affirm("rank 3 therefore three active neutrinos",["rank 3 therefore three active neutrinos"])
    print("FAIL_RANK_SHORTCUT_CAUGHT  a planted rank->neutrino overclaim is caught.")
    print('PASS_RAW_NEUTRAL_CURRENT_NO_RANK_SHORTCUT')
    return 0

if __name__ == "__main__": raise SystemExit(main())
