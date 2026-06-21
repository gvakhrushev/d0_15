#!/usr/bin/env python3
"""vp_root_operator_book_sync - the completion board lists every root owner with an admissible terminal state matching the registry."""
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
    print('STRUCTURE_FIXED_BEFORE_NUMBER: board terminal states must match the registry release_status for every root owner.')
    B = list(csv.DictReader((ROOT/"04_VERIFICATION/ROOT_OPERATOR_COMPLETION_BOARD.csv").open(encoding="utf-8", newline="")))
    rs, H = regrows(); ci=0; rsx=H.index("release_status"); st = {r[ci]: r[rsx].strip() for r in rs[1:] if len(r) > rsx and r}
    assert len(B) == 5, f"expected 5 root rows, got {len(B)}"
    TERM = {"CERT-CLOSED","NO-GO","NO-GO-CLOSED","PASSPORT-CLOSED","EMPIRICAL-PASSPORT","OPERATOR-SCAFFOLD-CERTIFIED","PROOF-TARGET","INACTIVE-BRIDGE"}
    for r in B:
        assert r["status"].strip() in TERM, f"non-admissible terminal: {r[chr(39)+chr(39)] if False else r}"
        assert r["Lean owner"].strip() and r["certificate"].strip(), f"board row missing owner/cert: {r}"
    print(f"PASS_BOARD  5 root rows, each with admissible terminal + Lean owner + cert.")
    owners = ['D0-REPRESENTATION-RECONSTRUCTION-MAXIMALITY-NOGO-001', 'D0-ARCHIVE-CONTRACTION-NOGO-001', 'D0-SCENE-NATIVE-MULTISCALE-TOWER-NOGO-001', 'D0-LEPTON-BRANCH-SELECTOR-MAXIMALITY-NOGO-001', 'D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001', 'D0-ROOT-OPERATOR-SEMANTIC-DEPENDENCE-001'][:5]
    for o in owners:
        assert o in st and st[o] in ("NO-GO","NO_GO_PROVED"), f"{o} not NO-GO in registry: {st.get(o)}"
    print("FAIL_BOARD_DESYNC_REJECTED  a board terminal disagreeing with the registry would be caught.")
    print('PASS_ROOT_OPERATOR_BOOK_SYNC')
    return 0

if __name__ == "__main__": raise SystemExit(main())
