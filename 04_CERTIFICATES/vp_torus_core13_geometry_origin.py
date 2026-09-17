#!/usr/bin/env python3
"""D0 memory-torus Core-13 geometry origin certificate.

This is a core-geometry algebra certificate, not a PDG passport.  It instantiates
the Lean algebraic parameter with a = phi^5 only to verify the intended frozen
dimensionless torus geometry.
"""

from __future__ import annotations

import math
from itertools import permutations

import numpy as np


TOL = 1.0e-10


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
    print("--- D0 TORUS CORE-13 GEOMETRY ORIGIN CERTIFICATE ---")

    phi = (1.0 + math.sqrt(5.0)) / 2.0
    a = phi**5
    xi5 = phi ** -5

    inner = 1.0
    core = (a + 1.0) / 2.0
    outer = a
    major = core
    minor = (a - 1.0) / 2.0

    assert a > 1.0
    assert np.isclose(outer / inner, a)
    assert np.isclose(major / minor, (a + 1.0) / (a - 1.0))
    assert np.isclose(major / minor, (1.0 + xi5) / (1.0 - xi5))
    assert np.isclose((major + minor) / (major - minor), a)

    print("[1] phi^5 torus invariant and radius ratios: PASS")

    shell_radii = np.array([inner, core, outer])
    assert len(shell_radii) == 3

    radial = np.array(
        [
            [0.0, 1.0, 0.0],
            [1.0, 0.0, 1.0],
            [0.0, 1.0, 0.0],
        ]
    )
    phase = np.diag(shell_radii)
    comm = radial @ phase - phase @ radial

    assert np.isclose(comm[0, 1], minor)
    assert abs(comm[0, 1]) > TOL

    print("[2] three shell carrier and radial adjacency: PASS")
    print("[3] [A_radial,D_phase][0,1] = minor radius != 0: PASS")

    _, u_phase = np.linalg.eigh(phase)
    _, u_mixed = np.linalg.eigh(phase + radial)
    amplitude = u_phase.conj().T @ u_mixed
    overlap = np.abs(amplitude) ** 2

    assert np.all(overlap >= -TOL)
    assert np.allclose(overlap.sum(axis=1), 1.0, atol=TOL, rtol=0.0)
    assert np.allclose(overlap.sum(axis=0), 1.0, atol=TOL, rtol=0.0)
    assert not is_permutation_matrix(overlap)

    flavour_defect = np.eye(3) - overlap
    response = flavour_defect.T @ flavour_defect
    eigs = np.linalg.eigvalsh(response)
    assert np.all(eigs >= -TOL)

    print("[4] shell-induced Born overlap is non-permutation unistochastic: PASS")
    print("[5] F_fl = I - O gives PSD response F^T F: PASS")
    print("\n[CERT-CLOSED] PASS_TORUS_CORE13_GEOMETRY_ORIGIN")


if __name__ == "__main__":
    run_certificate()
