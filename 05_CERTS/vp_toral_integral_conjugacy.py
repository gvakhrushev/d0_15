#!/usr/bin/env python3
"""vp_toral_integral_conjugacy - D0-TORAL-INTEGRAL-CONJUGACY-OWNER-001.

C T C^-1 = -M_phi (integral matrix conjugacy ONLY) with C=[[0,-1],[1,0]] (det 1), T=[[0,1],[1,-1]],
M_phi=[[1,1],[1,0]]. T hyperbolic: tr=-1, det=-1, charpoly x^2+x-1, eigenvalues phi^-1 and -phi, entropy
log phi. -M_phi has a negative entry -> NOT an adjacency matrix -> the integral conjugacy is NOT the
symbolic SSE. Reachable controls reject T^44=I, q_T as a toral period, and -M_phi used as an adjacency.
"""
import math
import sys
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

T = np.array([[0, 1], [1, -1]])
C = np.array([[0, -1], [1, 0]])
Cinv = np.array([[0, 1], [-1, 0]])
Mphi = np.array([[1, 1], [1, 0]])


def main() -> int:
    print("=== vp_toral_integral_conjugacy  C T C^-1 = -M_phi (integral matrix conjugacy only) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: T, C, M_phi fixed first; the conjugacy and entropy are "
          "consequences; this is an integral matrix conjugacy, NOT a symbolic conjugacy (q_T=44 is not a "
          "toral period).")
    assert np.array_equal(C @ Cinv, np.eye(2, dtype=int)), "C unimodular"
    assert np.array_equal(C @ T @ Cinv, -Mphi), "C T C^-1 = -M_phi"
    assert round(np.linalg.det(C)) == 1 and round(np.linalg.det(T)) == -1 and round(np.trace(T)) == -1
    print("PASS_INTEGRAL_CONJUGACY  C T C^-1 = -M_phi; det C=1, det T=-1, tr T=-1 (charpoly x^2+x-1).")

    phi = (1 + 5 ** 0.5) / 2
    ev = sorted(np.linalg.eigvals(T))
    assert abs(ev[0] - (-phi)) < 1e-9 and abs(ev[1] - 1 / phi) < 1e-9, "eigenvalues phi^-1, -phi"
    assert abs(math.log(phi) - 0.4812118) < 1e-6, "entropy log phi"
    print(f"PASS_HYPERBOLIC_ENTROPY  eigenvalues phi^-1={1/phi:.6f}, -phi={-phi:.6f}; entropy=log phi="
          f"{math.log(phi):.6f}.")

    assert (-Mphi)[0, 0] < 0 and not np.array_equal(-Mphi, Mphi), "-M_phi negative entry, != M_phi"
    print("PASS_NOT_SYMBOLIC_SSE  -M_phi has a negative entry and != M_phi -> integral conjugacy is NOT "
          "the symbolic SSE.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    assert not np.array_equal(np.linalg.matrix_power(T, 44), np.eye(2, dtype=int)), "control: T^44 != I"
    print("FAIL_T_POW_44_EQ_I_REJECTED  T^44 = I is caught as false (infinite order in GL(2,Z)).")
    assert not np.array_equal(np.linalg.matrix_power(T, 44) % 44, np.eye(2, dtype=int) % 44), "control"
    print("FAIL_Q_T_AS_TORAL_PERIOD_REJECTED  q_T=44 is a modulus, not a toral period (T^44 != I mod 44).")
    is_adjacency = bool(((-Mphi) >= 0).all())
    assert not is_adjacency, "control: -M_phi is not a nonnegative adjacency matrix"
    print("FAIL_NEG_GOLDEN_AS_ADJACENCY_REJECTED  using -M_phi as an adjacency matrix is caught (neg entry).")

    print("PASS_TORAL_INTEGRAL_CONJUGACY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
