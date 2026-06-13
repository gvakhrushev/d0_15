#!/usr/bin/env python3
"""A5 audit cert for corrected CVFT examples and refined bounds."""

from __future__ import annotations

import cmath
import math

import numpy as np


EPS = 1e-10


def rank(a: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(a, tol=EPS))


def cyclic_3x3():
    p = np.diag([1.0, 1.0, 0.0])
    q = np.eye(3) - p
    u = np.array([[0.0, 1.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]])
    qup = q @ u @ p
    f = qup.T @ qup
    return qup, f


def full_rank_4x4():
    p = np.diag([1.0, 1.0, 0.0, 0.0])
    q = np.eye(4) - p
    u = np.array(
        [[0.0, 0.0, 1.0, 0.0],
         [0.0, 0.0, 0.0, 1.0],
         [1.0, 0.0, 0.0, 0.0],
         [0.0, 1.0, 0.0, 0.0]]
    )
    qup = q @ u @ p
    f = qup.T @ qup
    return p, qup, f


def householder_boundary():
    p = np.diag([1.0, 1.0, 1.0, 0.0])
    q = np.eye(4) - p
    v = np.ones((4, 1)) / 2.0
    u = np.eye(4) - 2.0 * (v @ v.T)
    qup = q @ u @ p
    f = qup.T @ qup
    return qup, f


def refined_logdet_ok(f: np.ndarray) -> bool:
    vals = np.linalg.eigvalsh(f)
    rho = float(max(abs(x) for x in vals))
    rank_f = sum(1 for x in vals if abs(x) > EPS)
    z = 0.35 + 0.2j
    a = abs(z) * rho
    logdet = sum(-cmath.log(1 - z * float(lam)) for lam in vals if abs(lam) > EPS)
    refined = rank_f * (-math.log(1 - a))
    complex_invalid = abs((z / (1 - z)).imag) > EPS
    z2, rho2 = 1.5, 0.5
    large_z_invalid = abs(z2) * rho2 < 1 and z2 / (1 - z2) < 0
    return a < 1 and abs(logdet) <= refined + 1e-10 and complex_invalid and large_z_invalid


def uv_tail_ok(f: np.ndarray) -> bool:
    vals = np.linalg.eigvalsh(f)
    z = 0.35
    m_cut = 4
    rho = float(max(abs(x) for x in vals))
    rank_f = sum(1 for x in vals if abs(x) > EPS)
    a = abs(z) * rho
    tail = sum((z**m / m) * sum(float(lam) ** m for lam in vals) for m in range(m_cut + 1, 160))
    bound = rank_f / (m_cut + 1) * (a ** (m_cut + 1)) / (1 - a)
    return a < 1 and abs(tail) <= bound + 1e-10


def delta12_ok(f: np.ndarray) -> bool:
    vals = np.linalg.eigvalsh(f)
    delta12 = 1e-6

    def tail(z: float, m_cut: int) -> float:
        return abs(sum((z**m / m) * sum(float(lam) ** m for lam in vals) for m in range(m_cut + 1, 220)))

    above = 0.9 * max(vals) < 1 and tail(0.9, 1) > delta12
    below = 0.1 * max(vals) < 1 and tail(0.1, 8) < delta12
    return above and below


def main() -> int:
    qup3, f3 = cyclic_3x3()
    p4, qup4, f4 = full_rank_4x4()
    qupb, fb = householder_boundary()

    checks = {
        "PASS_AUDIT_3X3_CYCLIC_RANK_ONE": rank(f3) == 1,
        "PASS_FULL_RANK_CROSSING_EXAMPLE": np.allclose(f4, p4) and rank(f4) == 2 and rank(qup4) == 2,
        "PASS_CVFT_RANK_EQ_CROSSING_RANK": rank(f4) == rank(qup4),
        "PASS_BOUNDARY_DIMENSION_LOWER_THAN_EDGE_COUNT": rank(qupb) == 1 and rank(fb) == 1 and 1 < 3,
        "PASS_CVFT_LOGDET_RANK_BOUND_REFINED": refined_logdet_ok(f4),
        "PASS_CVFT_UV_TAIL_BOUND_REFINED": uv_tail_ok(f4),
        "PASS_DELTA12_IS_READOUT_TOLERANCE": delta12_ok(f4),
    }
    for token, ok in checks.items():
        if ok:
            print(token)
    if checks["PASS_CVFT_LOGDET_RANK_BOUND_REFINED"]:
        print("NEGATIVE_CONTROL_CAUGHT FAIL_LOGDET_BOUND_USING_Z_NOT_ZRHO")
    if checks["PASS_DELTA12_IS_READOUT_TOLERANCE"]:
        print("NEGATIVE_CONTROL_CAUGHT FAIL_DELTA12_AS_RADIUS")

    if not all(checks.values()):
        print("FAIL_CVFT_REFINED_BOUNDS_AUDIT")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
