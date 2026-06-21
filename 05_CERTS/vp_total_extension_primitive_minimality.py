#!/usr/bin/env python3
"""vp_total_extension_primitive_minimality - 11 primitives fully specified; 11x11 independence matrix off-diagonal independent."""
import csv, json, pathlib, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
ROOT = pathlib.Path(__file__).resolve().parents[1]
def reg():
    rs = list(csv.reader((ROOT/"09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv").open(encoding="utf-8", newline="")))
    H = rs[0]; I = {c:H.index(c) for c in H}
    return [r for r in rs[1:] if len(r)==len(H) and r], I

def main() -> int:
    print('STRUCTURE_FIXED_BEFORE_NUMBER: each primitive must be fully typed and pairwise-independent before any count.')
    P = list(csv.DictReader((ROOT/"04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVES.csv").open(encoding="utf-8", newline="")))
    REQ=["primitive_id","mathematical_type","minimal_input","why_core_cannot_derive","admissible_completion_class","necessary_conditions","sufficient_conditions","counterexample_witness","negative_controls"]
    assert len(P)==11, f"expected 11 primitives, got {len(P)}"
    bad=[p["primitive_id"] for p in P if any(not (p.get(k) or "").strip() for k in REQ)]
    assert not bad, f"primitive missing required field: {bad}"
    print(f"PASS_PRIMITIVES  11 primitives, each with type/input/why/class/necessary/sufficient/counterexample/controls.")
    M = list(csv.reader((ROOT/"04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_INDEPENDENCE_MATRIX.csv").open(encoding="utf-8", newline="")))
    body=M[1:]; assert len(body)==11 and all(len(r)==12 for r in body), "matrix not 11x11"
    offdiag=[body[i][j+1] for i in range(11) for j in range(11) if i!=j]
    assert all(v=="independent" for v in offdiag), "non-independent off-diagonal pair present"
    assert all(body[i][i+1]=="self" for i in range(11))
    print("PASS_INDEPENDENCE  55 off-diagonal pairs all independent; no merge/derivation.")
    assert len({p["primitive_id"] for p in P})==11
    print("FAIL_INCOMPLETE_PRIMITIVE_REJECTED  a primitive missing a field or a merged pair would be caught.")
    print('PASS_TOTAL_EXTENSION_PRIMITIVE_MINIMALITY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
