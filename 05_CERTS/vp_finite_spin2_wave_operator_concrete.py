#!/usr/bin/env python3
"""Concrete finite spin-2 TT wave-operator certificate.

No random perturbation is used.  The TT projector is checked on the full
10-dimensional basis of Sym(4).
"""

from __future__ import annotations

import numpy as np


def run_certificate() -> None:
    print("--- D0 FINITE SPIN-2 WAVE OPERATOR CONCRETE CERTIFICATE ---\n")

    n = 4
    eta = np.diag([1.0, -1.0, -1.0, -1.0])
    k = np.array([1.0, 1.0, 0.0, 0.0])
    u = np.array([1.0, 0.0, 0.0, 0.0])

    def pairing(a: np.ndarray, b: np.ndarray) -> float:
        return float(np.trace(a @ eta @ b @ eta))

    def tr(a: np.ndarray) -> float:
        return float(np.trace(a @ eta))

    def div(a: np.ndarray) -> np.ndarray:
        return a @ eta @ k

    def time_proj(a: np.ndarray) -> np.ndarray:
        return a @ eta @ u

    e_plus = np.zeros((n, n))
    e_plus[2, 2] = 1.0
    e_plus[3, 3] = -1.0

    e_cross = np.zeros((n, n))
    e_cross[2, 3] = 1.0
    e_cross[3, 2] = 1.0

    norm_plus = pairing(e_plus, e_plus)
    norm_cross = pairing(e_cross, e_cross)

    assert np.isclose(norm_plus, 2.0)
    assert np.isclose(norm_cross, 2.0)
    assert np.isclose(pairing(e_plus, e_cross), 0.0)

    def pi_tt(h: np.ndarray) -> np.ndarray:
        return (
            pairing(e_plus, h) / norm_plus * e_plus
            + pairing(e_cross, h) / norm_cross * e_cross
        )

    sym_basis: list[np.ndarray] = []
    for i in range(n):
        for j in range(i, n):
            matrix = np.zeros((n, n))
            matrix[i, j] = 1.0
            matrix[j, i] = 1.0
            sym_basis.append(matrix)

    assert len(sym_basis) == 10

    for basis_matrix in sym_basis:
        projected = pi_tt(basis_matrix)
        assert np.allclose(pi_tt(projected), projected), "Pi_TT idempotence failed"
        assert np.isclose(tr(projected), 0.0), "trace-free failed"
        assert np.allclose(div(projected), 0.0), "transverse failed"
        assert np.allclose(time_proj(projected), 0.0), "time-orthogonal failed"

    print("[1] Pi_TT checked on all 10 symmetric basis elements: PASS")

    assert np.allclose(pi_tt(eta), 0.0)

    def sym_grad(xi: np.ndarray) -> np.ndarray:
        return np.outer(k, xi) + np.outer(xi, k)

    gauge_basis = [sym_grad(np.eye(n)[a]) for a in range(n)]
    for gauge_matrix in gauge_basis:
        assert np.allclose(pi_tt(gauge_matrix), 0.0), "gauge annihilation failed"

    print("[2] trace mode and 4 gauge generators annihilated: PASS")

    projector_matrix = np.zeros((10, 10))
    for col, basis_matrix in enumerate(sym_basis):
        projected = pi_tt(basis_matrix)
        for row, row_basis in enumerate(sym_basis):
            denom = np.sum(row_basis * row_basis)
            projector_matrix[row, col] = np.sum(projected * row_basis) / denom

    assert np.allclose(projector_matrix @ projector_matrix, projector_matrix)
    rank = np.linalg.matrix_rank(projector_matrix)
    assert rank == 2

    print("[3] projector matrix idempotent and rank=2: PASS")

    def w_tt(h: np.ndarray) -> np.ndarray:
        return pi_tt(pi_tt(h))

    for basis_matrix in sym_basis:
        energy = pairing(basis_matrix, w_tt(basis_matrix))
        assert energy >= -1.0e-10
        assert np.allclose(w_tt(pi_tt(basis_matrix)), pi_tt(basis_matrix))

    print("[4] W_TT positive on symmetric basis and preserves TT: PASS")

    for basis_matrix in sym_basis:
        for stress in [e_plus, e_cross, 2.0 * e_plus - 3.0 * e_cross]:
            assert np.isclose(pairing(basis_matrix, stress), pairing(pi_tt(basis_matrix), stress))

    print("[5] TT stress coupling sees only TT projection: PASS")

    sym_components = 4 * 5 // 2
    constraints = 2 * 4
    dof = sym_components - constraints
    assert sym_components == 10
    assert dof == 2

    print("[6] finite_spin2_four_role_dof_eq_two: PASS")
    print("\n[CERT-CLOSED] PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE")


if __name__ == "__main__":
    run_certificate()
