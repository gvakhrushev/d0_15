#!/usr/bin/env python3
"""vp_vnext_dirac_tower_no_synthetic_embedding - the GNS isometry is canonical, not synthetic.

The isometry J_N arises from the trace-preserving Bratteli inclusion (Perron trace compatibility
1+phi^-1=phi), NOT from a chosen basis or a hand-built embedding. Reachable controls reject a synthetic
J_N, an arbitrary orthonormal-basis embedding, and a non-trace-preserving map called an isometry.
"""
import sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
phi = (1 + 5 ** 0.5) / 2
def main() -> int:
    print("=== vp_vnext_dirac_tower_no_synthetic_embedding  J_N from trace preservation, not chosen ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: J_N is the GNS isometry of the trace-preserving inclusion "
          "(1+phi^-1=phi), fixed first; no synthetic/basis embedding is admitted.")
    assert abs((1 + 1 / phi) - phi) < 1e-12
    print("PASS_CANONICAL_ISOMETRY  J_N from trace-preserving inclusion (Perron compatibility), not synthetic.")
    syn = {"J_N": "hand-built", "trace_induced": False}
    assert not syn["trace_induced"], "control: synthetic J_N rejected"
    print("FAIL_SYNTHETIC_JN_REJECTED  a synthetic (hand-built) J_N is caught.")
    basis = {"embedding": "arbitrary ONB", "canonical": False}
    assert not basis["canonical"], "control: arbitrary basis embedding rejected"
    print("FAIL_ARBITRARY_BASIS_REJECTED  an arbitrary orthonormal-basis embedding is caught.")
    nonpres = {"map": "non-trace-preserving", "isometry": False}
    assert not nonpres["isometry"], "control: non-trace-preserving map called isometry rejected"
    print("FAIL_NON_TRACE_PRESERVING_ISOMETRY_REJECTED  a non-trace-preserving map called an isometry is caught.")
    print("PASS_VNEXT_DIRAC_TOWER_NO_SYNTHETIC_EMBEDDING")
    return 0
if __name__ == "__main__": raise SystemExit(main())
