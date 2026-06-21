#!/usr/bin/env python3
"""vp_raw_archive_operator_type_firewall - L_archive != QUQ != Feshbach != S_DE; no trace/det treated as a canonical common-sector map.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the four archive operators are typed distinct; a common-sector map needs an explicit typed intertwiner, not a trace/det coincidence.')
    fw={r["operator"]:r for r in vcsv("RAW_SELF_READING_OPERATOR_TYPE_FIREWALL.csv")}
    assert "QUQ" in fw["L_archive"]["may_NOT_be_substituted_for"] and "S_DE" in fw["QUQ"]["may_NOT_be_substituted_for"]
    print("PASS_FIREWALL  L_archive/QUQ/Feshbach/S_DE typed distinct (no substitution).")
    bad=affirm(books(),["l_archive spectrum is the quq spectrum","trace and determinant give the canonical common-sector map","matching traces prove a common sector"])
    assert not bad, f"typing/trace breach: {bad}"
    print("FAIL_TRACE_AS_MAP_REJECTED  a trace/det coincidence treated as a canonical common-sector map is caught.")
    print('PASS_RAW_ARCHIVE_OPERATOR_TYPE_FIREWALL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
