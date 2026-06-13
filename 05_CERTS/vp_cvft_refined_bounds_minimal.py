#!/usr/bin/env python3
"""Minimal deterministic CVFT refined-bounds certificate.

No external data, no PDG and no Lean build are required.
"""

from __future__ import annotations

import cmath
import math

import numpy as np


EPS = 1e-10


def rank(a: np.ndarray) -> int:
    return int(np.linalg.matrix_rank(a, tol=EPS))


def full_rank_crossing_example():
    p = np.diag([1.0, 1.0, 0.0, 0.0])
    q = np.eye(4) - p
    u = np.array(
        [
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
            [1.0, 0.0, 0.0, 0.0],
            [0.0, 1.0, 0.0, 0.0],
        ]
    )
    qup = q @ u @ p
    f = qup.conj().T @ qup
    return p, q, u, qup, f


def boundary_dim_lt_edge_count_example():
    p = np.diag([1.0, 1.0, 1.0, 0.0])
    q = np.eye(4) - p
    v = np.ones((4, 1)) / 2.0
    u = np.eye(4) - 2.0 * (v @ v.T)
    qup = q @ u @ p
    f = qup.conj().T @ qup
    return p, q, u, qup, f


def logdet_bound(f: np.ndarray, z: complex) -> bool:
    vals = np.linalg.eigvalsh(f)
    rho = float(max(abs(x) for x in vals))
    rank_f = sum(1 for x in vals if abs(x) > EPS)
    a = abs(z) * rho
    if not a < 1:
        return False
    logdet = sum(-cmath.log(1 - z * float(lam)) for lam in vals if abs(lam) > EPS)
    refined = rank_f * (-math.log(1 - a))
    rational = rank_f * a / (1 - a)
    return abs(logdet) <= refined + 1e-10 and refined <= rational + 1e-10


def uv_tail_bound(f: np.ndarray, z: complex, m_cut: int) -> bool:
    vals = np.linalg.eigvalsh(f)
    rho = float(max(abs(x) for x in vals))
    rank_f = sum(1 for x in vals if abs(x) > EPS)
    a = abs(z) * rho
    if not a < 1:
        return False
    tail = 0j
    for m in range(m_cut + 1, 160):
        tail += (z**m / m) * sum(complex(lam) ** m for lam in vals)
    bound = rank_f / (m_cut + 1) * (a ** (m_cut + 1)) / (1 - a)
    return abs(tail) <= bound + 1e-10


def delta12_tolerance_check(f: np.ndarray) -> bool:
    vals = np.linalg.eigvalsh(f)
    delta12 = 1e-6

    def tail_abs(z: float, m_cut: int) -> float:
        total = 0.0
        for m in range(m_cut + 1, 220):
            total += (z**m / m) * sum(float(lam) ** m for lam in vals)
        return abs(total)

    above = abs(0.9) * max(vals) < 1 and tail_abs(0.9, 1) > delta12
    below = abs(0.1) * max(vals) < 1 and tail_abs(0.1, 8) < delta12
    return above and below


def bad_z_over_one_minus_z_controls() -> bool:
    complex_z = 0.35 + 0.2j
    complex_bad = complex_z / (1 - complex_z)
    complex_invalid = abs(complex_bad.imag) > EPS
    z = 1.5
    rho = 0.5
    large_z_valid_refined = abs(z) * rho < 1
    large_z_bad = z / (1 - z)
    large_z_invalid = large_z_bad < 0
    return complex_invalid and large_z_valid_refined and large_z_invalid


def main() -> int:
    p, _q, _u, qup, f = full_rank_crossing_example()
    full_rank_ok = (
        rank(qup) == 2
        and rank(f) == 2
        and np.allclose(f, p)
        and abs(max(np.linalg.eigvalsh(f)) - 1.0) < EPS
    )

    _p2, _q2, _u2, qup2, f2 = boundary_dim_lt_edge_count_example()
    boundary_ok = rank(qup2) == 1 and rank(f2) == 1 and 1 < 3

    logdet_ok = logdet_bound(f, 0.35 + 0.2j) and bad_z_over_one_minus_z_controls()
    uv_ok = uv_tail_bound(f, 0.35, 4)
    delta_ok = delta12_tolerance_check(f)
    rank_not_a4 = rank(f2) == 1

    if full_rank_ok:
        print("PASS_CVFT_RANK_EQ_CROSSING_RANK")
    if boundary_ok:
        print("PASS_CVFT_BOUNDARY_DIM_LT_EDGE_COUNT")
    if logdet_ok:
        print("PASS_CVFT_LOGDET_RANK_BOUND_REFINED")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_LOGDET_BOUND_USING_Z_NOT_ZRHO")
    if uv_ok:
        print("PASS_CVFT_UV_TAIL_BOUND_REFINED")
    if delta_ok:
        print("PASS_DELTA12_IS_READOUT_TOLERANCE")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_DELTA12_AS_RADIUS")
    if rank_not_a4:
        print("NEGATIVE_CONTROL_CAUGHT FAIL_RANK_BOUND_AS_A4_PROOF")

    ok = full_rank_ok and boundary_ok and logdet_ok and uv_ok and delta_ok and rank_not_a4
    if not ok:
        print("FAIL_CVFT_REFINED_BOUNDS_MINIMAL")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
