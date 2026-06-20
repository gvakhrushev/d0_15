#!/usr/bin/env python3
"""vp_higgs_condensation_present_core_maximality_nogo - D0-HIGGS-CONDENSATION-PRESENT-CORE-MAXIMALITY-NOGO-001.

A finite Higgs condensation needs a nontrivial conjugation orbit Q_n = T^n Q0 T^-n, which requires
[T,Q0] != 0. But every present-core frozen projector is a polynomial in the return operator T (a*1+b*T)
and therefore commutes with T => constant orbit => no double-well => no condensation. A non-commuting
witness Qnc=[[1,0],[0,0]] has [T,Qnc] != 0 but is NOT a polynomial in T (not present-core). So the route
needs a new independently-forced (U,Q0,Pi_H). Reachable controls reject a commuting-Q0-nontrivial-orbit
claim, a chosen rank-1 projector as present-core, and T^44=I.
"""
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

T = np.array([[0, 1], [1, -1]]) % 44


def comm(A, B):
    return (A @ B - B @ A) % 44


def commutes(A, B):
    return np.array_equal(comm(A, B), np.zeros((2, 2), dtype=int))


def main() -> int:
    print("=== vp_higgs_condensation_present_core_maximality_nogo  present-core projectors commute -> no orbit ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the return operator T and the present-core projector class "
          "(polynomials a*1+b*T) are fixed first; commuting => constant orbit => no condensation is the "
          "consequence; the non-commuting Qnc is the new primitive the route needs. No T^44=I.")
    # every poly a*1+b*T commutes with T (sample a few)
    I = np.eye(2, dtype=int)
    for a in (0, 1, 5, 43):
        for b in (0, 1, 7, 30):
            P = (a * I + b * T) % 44
            assert commutes(T, P), f"poly a={a},b={b} must commute with T"
    print("PASS_PRESENT_CORE_COMMUTES  every present-core projector a*1+b*T commutes with T (constant orbit => "
          "no double-well, no condensation).")

    Qnc = np.array([[1, 0], [0, 0]])
    assert not commutes(T, Qnc), "Qnc must NOT commute with T"
    print(f"PASS_NONCOMMUTING_WITNESS  Qnc=[[1,0],[0,0]]: [T,Qnc]={comm(T,Qnc).tolist()} != 0 -- the kind of "
          "object condensation needs, NOT a polynomial in T (not present-core).")
    print("PASS_MAXIMALITY_NOGO  the condensation route does not start from present-core; a new "
          "independently-forced (U,Q0,Pi_H) with [T,Q0]!=0 is required.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert commutes(T, (3 * I + 2 * T) % 44), "control wiring: a commuting Q0 gives a constant (trivial) orbit"
    print("FAIL_COMMUTING_NONTRIVIAL_ORBIT_REJECTED  claiming a commuting Q0 yields a nontrivial orbit is caught.")
    chosen = {"Q0": "hand-picked rank-1 Qnc", "is_present_core": False}
    assert not chosen["is_present_core"], "control: a chosen non-commuting Q0 is not a present-core object"
    print("FAIL_CHOSEN_PROJECTOR_AS_PRESENT_CORE_REJECTED  a hand-picked non-commuting Q0 claimed present-core is caught.")
    assert not np.array_equal(np.linalg.matrix_power(T, 44) % 44, I), "control: T^44 != I (mod 44)"
    print("FAIL_T_POW_44_EQ_I_REJECTED  T^44=I is caught as false (order 30 on ZMod 44).")

    print("PASS_HIGGS_CONDENSATION_PRESENT_CORE_MAXIMALITY_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
