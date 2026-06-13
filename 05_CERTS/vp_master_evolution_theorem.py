#!/usr/bin/env python3
"""D0 master finite-evolution theorem certificate."""

from __future__ import annotations

from math import gcd


STATUS = "PASS_MASTER_EVOLUTION_THEOREM"

Mat2 = tuple[tuple[int, int], tuple[int, int]]
Vec2 = tuple[int, int]


def mat_add(A: Mat2, B: Mat2) -> Mat2:
    return (
        (A[0][0] + B[0][0], A[0][1] + B[0][1]),
        (A[1][0] + B[1][0], A[1][1] + B[1][1]),
    )


def mat_sub(A: Mat2, B: Mat2) -> Mat2:
    return (
        (A[0][0] - B[0][0], A[0][1] - B[0][1]),
        (A[1][0] - B[1][0], A[1][1] - B[1][1]),
    )


def mat_mul(A: Mat2, B: Mat2) -> Mat2:
    return (
        (
            A[0][0] * B[0][0] + A[0][1] * B[1][0],
            A[0][0] * B[0][1] + A[0][1] * B[1][1],
        ),
        (
            A[1][0] * B[0][0] + A[1][1] * B[1][0],
            A[1][0] * B[0][1] + A[1][1] * B[1][1],
        ),
    )


def mat_pow(A: Mat2, n: int) -> Mat2:
    out: Mat2 = ((1, 0), (0, 1))
    for _ in range(n):
        out = mat_mul(out, A)
    return out


def mat_add_identity(A: Mat2) -> Mat2:
    return mat_add(A, ((1, 0), (0, 1)))


def trace(A: Mat2) -> int:
    return A[0][0] + A[1][1]


def det(A: Mat2) -> int:
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def mat_vec(A: Mat2, v: Vec2) -> Vec2:
    return (
        A[0][0] * v[0] + A[0][1] * v[1],
        A[1][0] * v[0] + A[1][1] * v[1],
    )


def detector_response(weights: Vec2, state: Vec2) -> int:
    return weights[0] * state[0] * state[0] + weights[1] * state[1] * state[1]


def lucas(n: int) -> int:
    if n == 0:
        return 2
    if n == 1:
        return 1
    a, b = 2, 1
    for _ in range(n - 1):
        a, b = b, a + b
    return b


def euler_phi(n: int) -> int:
    return sum(1 for k in range(1, n + 1) if gcd(k, n) == 1)


def run_certificate() -> None:
    print("--- D0 MASTER FINITE-EVOLUTION THEOREM CERTIFICATE ---")

    T: Mat2 = ((0, 1), (1, -1))
    I: Mat2 = ((1, 0), (0, 1))
    Z: Mat2 = ((0, 0), (0, 0))

    print("[1] Time operator quadratic identity:")
    assert mat_sub(mat_add(mat_pow(T, 2), T), I) == Z
    assert det(T) == -1
    print("    T^2 + T - I = 0 and det(T)=-1: PASS")

    print("[2] Signed Lucas trace layers:")
    for n in range(0, 21):
        tr = trace(mat_pow(T, n))
        assert tr == ((-1) ** n) * lucas(n)
    print("    Tr(T^n)=(-1)^n L_n for n=0..20: PASS")

    print("[3] Anti-periodic Lefschetz scene spectrum:")
    counts = {n: abs(det(mat_add_identity(mat_pow(T, n)))) for n in range(3, 7)}
    assert counts[3] == 4
    assert counts[4] == 9
    assert counts[5] == 11
    assert counts[3] + counts[4] == 13
    assert counts[6] == 20
    print("    4, 9, 11, 13, 20 scene counts: PASS")

    print("[4] Determinant-square volume balance:")
    for n in range(0, 21):
        d = det(mat_pow(T, n))
        assert d * d == 1
    print("    det(T^n)^2=1 for n=0..20: PASS")

    print("[5] Dark/archive even-window cancellation:")
    for N in range(1, 21):
        assert sum(((-1) ** k) for k in range(2 * N)) == 0
    print("    alternating archive window sum is zero: PASS")

    print("[6] Heat moments of Delta_T=T^2:")
    Delta_T = mat_pow(T, 2)
    for m in range(0, 11):
        assert trace(mat_pow(Delta_T, m)) == trace(mat_pow(T, 2 * m))
        assert trace(mat_pow(Delta_T, m)) == lucas(2 * m)
    print("    Tr((T^2)^m)=L_{2m} for m=0..10: PASS")

    print("[7] Fixed detector time ladder:")
    detector_weights: Vec2 = (2, 3)
    psi0: Vec2 = (1, 2)
    readouts: list[int] = []
    for n in range(0, 8):
        assert detector_weights == (2, 3)
        readouts.append(detector_response(detector_weights, mat_vec(mat_pow(T, n), psi0)))
    assert len(set(readouts)) > 1
    print("    detector fixed; readout changes through T^n state: PASS")

    print("[8] Finite return quotients used by the quasicrystal support:")
    assert euler_phi(44) == 20
    assert euler_phi(710) == 280
    print("    phi_Euler(44)=20 and phi_Euler(710)=280: PASS")

    print(f"\n[CERT-CLOSED] {STATUS}")


if __name__ == "__main__":
    run_certificate()
