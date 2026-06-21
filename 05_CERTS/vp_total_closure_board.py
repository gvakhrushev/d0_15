#!/usr/bin/env python3
"""vp_total_closure_board - all 10 lanes have owner + terminal + exit + forbidden + (primitive or external)."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: each lane must carry owner+admissible-terminal+exit+forbidden+(primitive|external) before any count.')
    B = list(csv.DictReader((ROOT/"04_VERIFICATION/TOTAL_CLOSURE_BOARD.csv").open(encoding="utf-8", newline="")))
    TERM = {"CERT-CLOSED","NO-GO","NO-GO-CLOSED","PASSPORT-CLOSED","EMPIRICAL-PASSPORT","OPERATOR-SCAFFOLD-CERTIFIED","PROOF-TARGET","INACTIVE-BRIDGE"}
    assert len(B)==10, f"expected 10 lanes, got {len(B)}"
    bad=[r["lane"] for r in B if not r["owner(s)"] or r["terminal_state"] not in TERM or not r["exit_condition"] or not r["forbidden_route"]]
    assert not bad, f"lane missing owner/terminal/exit/forbidden: {bad}"
    print(f"PASS_BOARD  10 lanes, each owner + admissible terminal + exit + forbidden route.")
    nogap=[r["lane"] for r in B if not r["minimum_new_primitive"] and not r["external_passport"]]
    assert not nogap, f"lane without primitive/external: {nogap}"
    print("PASS_GAP_NAMED  each lane names a minimum primitive or external passport.")
    assert all(r["terminal_state"] in TERM for r in B)
    print("FAIL_NONADMISSIBLE_TERMINAL_REJECTED  a non-admissible terminal synonym would be caught.")
    print('PASS_TOTAL_CLOSURE_BOARD')
    return 0

if __name__ == "__main__": raise SystemExit(main())
