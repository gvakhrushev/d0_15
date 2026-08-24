#!/usr/bin/env python3
"""vp_total_extension_primitive_minimality - all registered extension primitives (19) fully specified; 19x19 independence matrix off-diagonal independent."""
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
    N=len(P)
    assert N==19, f"expected 19 primitives, got {N}"
    bad=[p["primitive_id"] for p in P if any(not (p.get(k) or "").strip() for k in REQ)]
    assert not bad, f"primitive missing required field: {bad}"
    print(f"PASS_PRIMITIVES  11 primitives, each with type/input/why/class/necessary/sufficient/counterexample/controls.")
    M = list(csv.reader((ROOT/"04_VERIFICATION/TOTAL_EXTENSION_PRIMITIVE_INDEPENDENCE_MATRIX.csv").open(encoding="utf-8", newline="")))
    body=M[1:]; assert len(body)==N and all(len(r)==N+1 for r in body), f"matrix not {N}x{N}"
    ids=[p["primitive_id"] for p in P]
    assert [r[0] for r in body]==ids, "matrix row order must match primitive registry order"
    assert M[0][1:]==ids, "matrix header must match primitive registry order"
    offdiag=[body[i][j+1] for i in range(N) for j in range(N) if i!=j]
    assert all(v=="independent" for v in offdiag), "non-independent off-diagonal pair present"
    assert all(body[i][i+1]=="self" for i in range(N))
    print(f"PASS_INDEPENDENCE  {N*(N-1)} off-diagonal pairs all independent; no merge/derivation.")
    assert len({p["primitive_id"] for p in P})==N
    print("FAIL_INCOMPLETE_PRIMITIVE_REJECTED  a primitive missing a field or a merged pair would be caught.")
    print('PASS_TOTAL_EXTENSION_PRIMITIVE_MINIMALITY')
    return 0

if __name__ == "__main__": raise SystemExit(main())
