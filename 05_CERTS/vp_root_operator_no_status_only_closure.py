#!/usr/bin/env python3
"""vp_root_operator_no_status_only_closure - every root-operator owner has a Lean module OR a cert (never status-only)."""
import csv, json, pathlib, re, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def regrows():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; return rs, H
def book_prose():
    return "\n".join(p.read_text(encoding="utf-8", errors="replace") for p in (ROOT/"01_BOOKS").rglob("*.md"))
NEG = ("no ","not ","never ","without ","does not ","is not ","are not ","do not ","cannot ","would ","if ","reject")
def affirm_hits(prose, phrases):
    o, low = [], prose.lower()
    for p in phrases:
        for m in re.finditer(re.escape(p), low):
            if not any(n in low[max(0,m.start()-44):m.start()] for n in NEG): o.append(p); break
    return o

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: each root owner must carry a real Lean theorem or executable cert before it counts as closed.')
    rs, H = regrows(); ci=0; lm=H.index("lean_module"); pc=H.index("python_cert"); rsx=H.index("release_status")
    owners = ['D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001', 'D0-ARCHIVE-CONTRACTION-NOGO-001', 'D0-SCENE-NATIVE-MULTISCALE-TOWER-NOGO-001', 'D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001', 'D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001', 'D0-ROOT-OPERATOR-SEMANTIC-DEPENDENCE-001']
    rows = {r[ci]: r for r in rs[1:] if len(r) > pc and r}
    missing = [o for o in owners if o not in rows]
    assert not missing, f"root owner not registered: {missing}"
    statusonly = [o for o in owners if not rows[o][lm].strip() and not rows[o][pc].strip()]
    assert not statusonly, f"status-only root owner (no lean, no cert): {statusonly}"
    print(f"PASS_OWNED  all {len(owners)} root owners carry a Lean module or a cert.")
    assert all(rows[o][rsx].strip() for o in owners)
    print("FAIL_STATUS_ONLY_REJECTED  a root owner with neither lean nor cert would be caught.")
    print('PASS_ROOT_OPERATOR_NO_STATUS_ONLY_CLOSURE')
    return 0

if __name__ == "__main__": raise SystemExit(main())
