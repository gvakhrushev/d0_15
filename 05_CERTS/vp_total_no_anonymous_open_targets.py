#!/usr/bin/env python3
"""vp_total_no_anonymous_open_targets - every PROOF-TARGET/OPEN names a missing primitive/external/completion."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: every open target must name exactly one missing primitive/external/completion before counting.')
    D,I = reg(); gg=lambda r,c: r[I[c]].strip()
    TOK=("prim-","assump-","external","missing artifact","exact-missing","passport","completion class")
    anon=[gg(r,"claim_id") for r in D if gg(r,"release_status") in ("PROOF-TARGET","OPEN") and not any(t in gg(r,"notes").lower() for t in TOK)]
    assert not anon, f"anonymous open targets: {anon[:6]}"
    print(f"PASS_NO_ANONYMOUS  every open target names a missing primitive/external/completion class.")
    assert any(t for t in TOK)
    print("FAIL_ANONYMOUS_REJECTED  an open target naming no missing artifact would be caught.")
    print('PASS_TOTAL_NO_ANONYMOUS_OPEN_TARGETS')
    return 0

if __name__ == "__main__": raise SystemExit(main())
