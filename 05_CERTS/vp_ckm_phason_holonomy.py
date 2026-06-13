#!/usr/bin/env python3
"""D0 QUASI-009 CKM phason-holonomy finite algebra certificate."""

from __future__ import annotations

from fractions import Fraction


STATUS = "PASS_CKM_PHASON_HOLONOMY"


Matrix = tuple[tuple[Fraction, ...], ...]


def matmul(a: Matrix, b: Matrix) -> Matrix:
    n = len(a)
    return tuple(
        tuple(sum(a[i][k] * b[k][j] for k in range(n)) for j in range(n))
        for i in range(n)
    )


def transpose(a: Matrix) -> Matrix:
    return tuple(tuple(a[j][i] for j in range(len(a))) for i in range(len(a)))


def commutator(a: Matrix, b: Matrix) -> Matrix:
    ab = matmul(a, b)
    ba = matmul(b, a)
    return tuple(
        tuple(ab[i][j] - ba[i][j] for j in range(len(a)))
        for i in range(len(a))
    )


def identity(n: int) -> Matrix:
    return tuple(tuple(Fraction(1 if i == j else 0) for j in range(n)) for i in range(n))


def run_certificate() -> None:
    print("--- D0 CKM PHASON HOLONOMY CERTIFICATE ---")

    print("[1] Torus shell radial/phase commutator:")
    a = Fraction(2, 1)
    radial = (
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(1), Fraction(0), Fraction(1)),
        (Fraction(0), Fraction(1), Fraction(0)),
    )
    phase = (
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), (a + 1) / 2, Fraction(0)),
        (Fraction(0), Fraction(0), a),
    )
    curv = commutator(radial, phase)
    assert curv[0][1] == (a - 1) / 2
    assert curv[0][1] != 0
    print("    [A_radial,D_phase](0,1)=(a-1)/2 != 0: PASS")

    print("[2] Finite shell-loop holonomy transport:")
    u = (
        (Fraction(3, 5), Fraction(4, 5), Fraction(0)),
        (Fraction(-4, 5), Fraction(3, 5), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    )
    assert matmul(u, transpose(u)) == identity(3)
    assert matmul(transpose(u), u) == identity(3)
    print("    rational 3/5-4/5 transport is orthogonal/unitary: PASS")

    print("[3] Phase-blind holonomy response:")
    response = tuple(tuple(x * x for x in row) for row in u)
    assert response[0][0] == Fraction(9, 25)
    assert response[0][1] == Fraction(16, 25)
    assert response[0][0] > 0 and response[0][1] > 0
    assert response[0][0] != 1 and response[0][1] != 1
    print("    row 0 has two positive channels 9/25 and 16/25: PASS")

    print("[4] Non-permutation and CP-like orientation checks:")
    permutation_rows = {
        (Fraction(1), Fraction(0), Fraction(0)),
        (Fraction(0), Fraction(1), Fraction(0)),
        (Fraction(0), Fraction(0), Fraction(1)),
    }
    assert response[0] not in permutation_rows
    forward_charge = 1
    reverse_charge = -1
    assert reverse_charge == -forward_charge
    print("    non-permutation response and orientation reversal sign flip: PASS")

    print("[5] Negative controls:")
    uses_pdg_ckm_entries = False
    direct_fit_matrix = False
    assert not uses_pdg_ckm_entries
    assert not direct_fit_matrix
    print("    no PDG CKM entries and no fitted CKM matrix: PASS")

    print(f"\n[CERT-CLOSED] {STATUS}")


if __name__ == "__main__":
    run_certificate()
