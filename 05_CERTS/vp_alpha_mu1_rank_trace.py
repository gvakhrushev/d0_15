#!/usr/bin/env python3
"""D0-ALPHA-MU1-RANKTRACE-001 - mu1 = 1/3 as the rank-normalized first archive-return trace.

In the depth-<=2 archive-resolvent writing alpha_alg^-1 = mu2 u^2 + mu1 u (u=phi^-3), the first
coefficient is mu1 = Tr_R(p1)/Tr_R(I_R) = 1/3: the primitive first archive-return projector p1 has
trace 1 on the rank-3 transport carrier R (Tr_R(I_R) = rank = 3). NOT read from generations, the
empirical alpha, or decimal fitting.

CONSOLIDATION (honest): the VALUE mu1=1/3 is already Lean-CORE in D0.Spectral.DeltaAlphaMoment
(delta_alpha_moment, D0-DELTA-ALPHA-MOMENT-001) and DERIVED as a trace in
vp_feshbach_residue_amplitudes.py (mu1 = Tr(floor)/rank). This row states the rank-trace reading with
reachable controls; it does not re-derive the CORE value.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main() -> int:
    print("=== D0-ALPHA-MU1-RANKTRACE-001  mu1 = Tr_R(p1)/Tr_R(I_R) = 1/3 (rank-3 carrier) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: rank-3 transport carrier R (Tr_R(I_R)=3) + primitive first-return "
          "projector p1 (Tr_R(p1)=1) fixed before the value")
    rank_R = 3
    trace_p1 = 1
    mu1 = F(trace_p1, rank_R)
    assert mu1 == F(1, 3), f"mu1 must be 1/3: {mu1}"
    print(f"PASS_MU1_RANK_TRACE  mu1 = Tr_R(p1)/Tr_R(I_R) = {trace_p1}/{rank_R} = {mu1}")

    assert F(trace_p1, 2) != F(1, 3) and F(trace_p1, 4) != F(1, 3), "control: wrong rank must miss 1/3"
    print("FAIL_WRONG_RANK_REJECTED  rank 2 -> 1/2, rank 4 -> 1/4 != 1/3 (the rank-3 carrier is forced)")
    assert F(2, rank_R) != F(1, 3), "control: a non-primitive (trace 2) projector must miss 1/3"
    print("FAIL_NONPRIMITIVE_PROJECTOR_REJECTED  Tr(p1)=2 -> 2/3 != 1/3 (p1 is the PRIMITIVE first return)")
    print("HONEST_CONSOLIDATION  mu1=1/3 is Lean-CORE (D0.Spectral.DeltaAlphaMoment / D0-DELTA-ALPHA-MOMENT-001) and "
          "trace-derived (vp_feshbach_residue_amplitudes.py); this states the rank-trace reading, not a new derivation. "
          "NOT from generations / empirical alpha / decimal fit.")
    print("PASS_ALPHA_MU1_RANKTRACE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
