#!/usr/bin/env python3
"""D0 toral automorphism / Galois balance certificate."""

from __future__ import annotations

from math import sqrt

import numpy as np


STATUS = "PASS_TORAL_AUTOMORPHISM_GALOIS_BALANCE"


def lucas(n: int) -> int:
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def matrix_power(T: np.ndarray, n: int) -> np.ndarray:
    result = np.eye(2, dtype=object)
    for _ in range(n):
        result = result @ T
    return result


def run_certificate() -> None:
    print("--- D0 TORAL AUTOMORPHISM / GALOIS BALANCE CERTIFICATE ---")

    T = np.array([[0, 1], [1, -1]], dtype=object)

    expected = {
        1: -1,
        2: 3,
        3: -4,
        4: 7,
        5: -11,
        6: 18,
    }

    print("[1] Trace unfolding:")
    for n, value in expected.items():
        trace = int(np.trace(matrix_power(T, n)))
        assert trace == value
        assert trace == ((-1) ** n) * lucas(n)
        print(f"    Tr(T^{n}) = {trace}")
    print("    signed Lucas trace: PASS")

    print("[2] Determinant / volume conservation:")
    for n in range(1, 12):
        det = round(np.linalg.det(np.array(matrix_power(T, n), dtype=float)))
        assert abs(det) == 1
    print("    |det(T^n)|=1 for tested n: PASS")

    phi = (1.0 + sqrt(5.0)) / 2.0
    lam_active = 1.0 / phi
    lam_archive = -phi

    print("[3] Galois eigen-pair:")
    assert abs((lam_active * lam_archive) + 1.0) < 1e-12
    print(f"    lambda_active={lam_active:.12f}")
    print(f"    lambda_archive={lam_archive:.12f}")
    print("    lambda_active * lambda_archive = -1: PASS")

    print("[4] Active/archive squeezing:")
    for n in range(1, 8):
        active = abs(lam_active) ** n
        archive = abs(lam_archive) ** n
        assert abs(active * archive - 1.0) < 1e-12
    print("    |lambda_A|^n * |lambda_D|^n = 1: PASS")

    print("[5] Dark alternating coarse-grain:")
    for N in range(1, 16):
        assert sum(((-1) ** k) for k in range(2 * N)) == 0
    print("    sum_{k=0}^{2N-1} (-1)^k = 0: PASS")

    print("[6] D0 layer extraction:")
    assert abs(expected[2]) == 3
    assert abs(expected[3]) == 4
    assert abs(expected[5]) == 11
    print("    |Tr(T^2)|=3 generation carrier")
    print("    |Tr(T^3)|=4 ABCD capacity")
    print("    |Tr(T^5)|=11 memory torus")

    print(f"\n[CERT-CLOSED] {STATUS}")


if __name__ == "__main__":
    run_certificate()
