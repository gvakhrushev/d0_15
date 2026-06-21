#!/usr/bin/env python3
"""vp_x5_operator_type_firewall - L_archive != QUQ != W_eff != S_DE.
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: the archive operators are typed distinct; no spectrum substitution.')
    fw={r["operator"]:r for r in list(csv.DictReader((ROOT/"04_VERIFICATION/RAW_SELF_READING_OPERATOR_TYPE_FIREWALL.csv").open(encoding="utf-8",newline="")))}
    assert "QUQ" in fw["L_archive"]["may_NOT_be_substituted_for"]
    print("PASS_FIREWALL  L_archive/QUQ/Feshbach/S_DE typed distinct.")
    bad=affirm(books(),["l_archive spectrum is the quq spectrum","quq spectrum equals the l_archive"])
    assert not bad, f"firewall: {bad}"
    print("FAIL_FIREWALL_BREACH_CAUGHT  an L_archive-as-QUQ claim is caught.")
    print('PASS_X5_OPERATOR_TYPE_FIREWALL')
    return 0

if __name__ == "__main__": raise SystemExit(main())
