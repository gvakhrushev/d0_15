#!/usr/bin/env python3
"""vp_higgs_return_quotient_action - D0-HIGGS-RETURN-QUOTIENT-ACTION-OWNER-001.

The return modulus q_T = 44 is NOT a toral period. T = [[0,1],[1,-1]] has infinite order in GL(2,Z)
(trace = signed Lucas, grows), so T^44 != I; and on ZMod 44 its order is 30 (T^30 = I, T^44 != I).
Honors the task restriction: do NOT assert T^44 = I. Reachable controls reject asserting T^44=I and a
manual period-44 permutation.
"""
import numpy as np
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
T = np.array([[0, 1], [1, -1]])


def order_mod(m):
    I = np.eye(2, dtype=int) % m; A = T % m; n = 1
    while not np.array_equal(A, I):
        A = (A @ T) % m; n += 1
        if n > 1000: return None
    return n


def main() -> int:
    print("=== vp_higgs_return_quotient_action  q_T=44 is a return MODULUS, not a toral period ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: T=[[0,1],[1,-1]] (charpoly x^2+x-1) and the residue quotient "
          "ZMod 44 are fixed first; the period is the consequence -- T^44=I is NOT assumed.")
    tr = [int(np.trace(np.linalg.matrix_power(T, n))) for n in range(1, 9)]
    assert all(abs(t) != 2 for t in tr[1:]), "trace=2 would allow T^n=I"
    assert abs(tr[-1]) > 2, "Lucas trace grows -> infinite order in GL(2,Z)"
    print(f"PASS_INFINITE_ORDER_GL2Z  Tr(T^n)={tr} (signed Lucas, grows) -> infinite order, T^44 != I in GL(2,Z).")
    o = order_mod(44)
    assert o == 30, f"order of T mod 44 is {o}, expected 30"
    assert not np.array_equal(np.linalg.matrix_power(T, 44) % 44, np.eye(2, dtype=int) % 44), "T^44 != I mod 44"
    print(f"PASS_TORAL_ORDER_30  order of T mod 44 = 30 (T^30=I), and T^44 != I mod 44 (=T^14). 44 is the "
          "modulus, not the period.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert not np.array_equal(np.linalg.matrix_power(T, 44), np.eye(2, dtype=int)), "control: T^44 != I over Z"
    print("FAIL_T_POW_44_EQ_I_REJECTED  the assertion T^44 = I (in GL(2,Z) or mod 44) is caught as false.")
    manual_perm_period = 44  # a hand-invented period-44 permutation, not the toral action
    assert manual_perm_period != o, "control: a manual period-44 permutation differs from the toral order 30"
    print("FAIL_MANUAL_PERIOD44_PERMUTATION_REJECTED  a hand-invented period-44 action != the toral order (30).")
    print("PASS_HIGGS_RETURN_QUOTIENT_ACTION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
