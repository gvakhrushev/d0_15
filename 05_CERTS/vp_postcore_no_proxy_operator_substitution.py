#!/usr/bin/env python3
"""vp_postcore_no_proxy_operator_substitution - the operator-type firewall (L_archive/QUQ/S_DE distinct) is recorded and respected."""
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: L_archive, QUQ, S_DE are distinct operators; none may be substituted for another.')
    fw = list(csv.DictReader((ROOT/"04_VERIFICATION/POST_CORE_OPERATOR_TYPE_FIREWALL.csv").open(encoding="utf-8", newline="")))
    ops = {r["operator"] for r in fw}
    assert {"L_archive","QUQ","S_DE"} <= ops, f"firewall missing operators: {ops}"
    larch = next(r for r in fw if r["operator"]=="L_archive")
    assert "QUQ" in larch["may_NOT_be_substituted_for"]
    print("PASS_FIREWALL  L_archive/QUQ/S_DE recorded distinct; L_archive may NOT be substituted for QUQ.")
    bad = affirm(books(), ["l_archive spectrum is the quq spectrum","quq spectrum is {24,22,20}"])
    assert not bad, f"proxy substitution in books: {bad}"
    print("FAIL_PROXY_SUBSTITUTION_REJECTED  treating one operator spectrum as another would be caught.")
    print('PASS_POSTCORE_NO_PROXY_OPERATOR_SUBSTITUTION')
    return 0

if __name__ == "__main__": raise SystemExit(main())
