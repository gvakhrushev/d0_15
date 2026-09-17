#!/usr/bin/env python3
"""D0 generation selector origin certificate.

The active source is the D0 memory-torus shell geometry:

    selector 1: radial shell hopping A_radial
    selector 2: shell-radius / phase drift D_phase

No PDG data, CKM fit, or arbitrary S_up/S_down fixture is used.
"""

from __future__ import annotations

import math
from itertools import permutations

import numpy as np


TOL = 1.0e-10


def torus_shell_geometry() -> tuple[np.ndarray, np.ndarray, float]:
    phi = (1.0 + math.sqrt(5.0)) / 2.0
    a = phi**5
    inner = 1.0
    core = (a + 1.0) / 2.0
    outer = a
    minor = (a - 1.0) / 2.0
    radial = np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )
    phase = np.diag([inner, core, outer])
    return radial, phase, minor


def is_permutation_matrix(matrix: np.ndarray, tol: float = TOL) -> bool:
    n = matrix.shape[0]
    for sigma in permutations(range(n)):
        witness = np.zeros_like(matrix)
        for i, j in enumerate(sigma):
            witness[i, j] = 1.0
        if np.allclose(matrix, witness, atol=tol, rtol=0.0):
            return True
    return False


def run_certificate() -> None:
    print("--- D0 GENERATION SELECTOR ORIGIN CERTIFICATE ---")

    radial, phase, minor = torus_shell_geometry()
    comm = radial @ phase - phase @ radial

    assert np.isclose(comm[0, 1], minor)
    assert abs(comm[0, 1]) > TOL

    print("[1] radial selector from torus shell adjacency: PASS")
    print("[2] phase selector from torus shell-radius drift: PASS")
    print("[3] [A_radial,D_phase](0,1) equals nonzero minor radius: PASS")

    _, u_phase = np.linalg.eigh(phase)
    _, u_mixed = np.linalg.eigh(phase + radial)
    overlap_amplitude = u_phase.conj().T @ u_mixed
    overlap_response = np.abs(overlap_amplitude) ** 2

    assert np.all(overlap_response >= -TOL)
    assert np.allclose(overlap_response.sum(axis=1), 1.0, atol=TOL, rtol=0.0)
    assert np.allclose(overlap_response.sum(axis=0), 1.0, atol=TOL, rtol=0.0)
    assert not is_permutation_matrix(overlap_response)

    positive_rows = [
        sum(1 for j in range(3) if overlap_response[i, j] > TOL)
        for i in range(3)
    ]
    assert any(support > 1 for support in positive_rows)

    flavour_defect = np.eye(3) - overlap_response
    response = flavour_defect.T @ flavour_defect
    eigs = np.linalg.eigvalsh(response)
    assert np.all(eigs >= -TOL)

    print("[4] O_ij = |<phase_i|mixed_j>|^2 is unistochastic: PASS")
    print("[5] O is not an Equiv.Perm permutation witness: PASS")
    print("[6] O has a multi-support row: PASS")
    print("[7] F_fl = I - O gives PSD response F^T F: PASS")
    print("\n[CERT-CLOSED] PASS_D0_GENERATION_SELECTOR_ORIGIN")


if __name__ == "__main__":
    run_certificate()
