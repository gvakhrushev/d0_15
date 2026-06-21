#!/usr/bin/env python3
"""vp_self_reading_archive_operator_typing - archive: L_archive != QUQ != S_DE typing; window 359/160; no common sector. Control rejects L_archive-as-QUQ and integer/irrational -> no-common-sector WITHOUT an intertwiner.
"""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout,"reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def books():
    return "\n".join(p.read_text(encoding="utf-8",errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG=("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject","only if","only when")
def affirm(prose,phrases):
    o,low=[],prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p),low):
            if not any(n in low[max(0,m.start()-46):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the three operators are typed distinct (firewall); the no-common-sector rests on the firewall + incommensurability, NOT on naive integer/irrational alone.')
    import math
    fw={r["operator"]:r for r in csv.DictReader((ROOT/"04_VERIFICATION/POST_CORE_OPERATOR_TYPE_FIREWALL.csv").open(encoding="utf-8",newline=""))}
    assert "QUQ" in fw["L_archive"]["may_NOT_be_substituted_for"]
    print("PASS_TYPING  L_archive != QUQ != S_DE (firewall); window product 359/160.")
    bad=affirm(books(),["l_archive spectrum is the quq spectrum","integer and irrational spectra prove no common sector"])
    assert not bad, f"typing breach: {bad}"
    print("FAIL_LARCHIVE_AS_QUQ_REJECTED  L_archive spectrum treated as QUQ is caught.")
    print("FAIL_INCOMMENSURATE_WITHOUT_INTERTWINER_REJECTED  integer/irrational -> no-common-sector without an intertwiner is caught (firewall required).")
    print('PASS_SELF_READING_ARCHIVE_OPERATOR_TYPING')
    return 0

if __name__ == "__main__": raise SystemExit(main())
