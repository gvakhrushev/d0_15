#!/usr/bin/env python3
"""CAR Dirac square certificate.

Verifies the central theorem of Package II:
  D_L² = Δ_L^(4) ⊗ I_16.

Includes reachable negative control: altering one fermionic anticommutation sign
causes cross-terms to survive, proving D_mutated² != Δ ⊗ I.
"""

from __future__ import annotations

import cmath
import itertools
import json
import math
import sys
from pathlib import Path

ROLES = [0, 1, 2, 3]
FOCK_DIM = 16


def jw_phase(state: int, role: int) -> int:
    mask = (1 << role) - 1
    occupied_before = bin(state & mask).count("1")
    return -1 if occupied_before % 2 == 1 else 1


def construct_annihilation_matrix(role: int, mutate: bool = False) -> list[list[int]]:
    mat = [[0] * FOCK_DIM for _ in range(FOCK_DIM)]
    for ket in range(FOCK_DIM):
        if (ket >> role) & 1:
            bra = ket ^ (1 << role)
            phase = jw_phase(ket, role)
            if mutate and role == 2 and (ket & 1):
                phase = -phase  # breaks cross-anticommutator with role 0
            mat[bra][ket] = phase
    return mat


def transpose(mat: list[list[int]]) -> list[list[int]]:
    dim = len(mat)
    return [[mat[j][i] for j in range(dim)] for i in range(dim)]


def verify_dirac_square(side: int = 3, mutate: bool = False) -> bool:
    c = [construct_annihilation_matrix(r, mutate=mutate) for r in ROLES]
    c_dag = [transpose(c[r]) for r in ROLES]

    scale = float(side * side)
    # Check on representative Fourier modes
    test_modes = [(0, 0, 0, 0), (1, 0, 0, 0), (1, 2, 0, 1), (2, 2, 2, 2)]

    for k in test_modes:
        # Expected scalar Laplacian eigenvalue
        expected_lam = sum(4.0 * scale * (math.sin(math.pi * ki / side) ** 2) for ki in k)

        # Matrix of D(k) on 16-dimensional Fock space:
        # D(k) = sum_r [ nabla_r(k) (x) c_r† + nabla_r*(k) (x) c_r ]
        # where nabla_r(k) = side * (exp(2pi i k_r / side) - 1)
        # Note: |nabla_r(k)|^2 = 4 side^2 sin^2(pi k_r / side)
        D_k = [[0.0 + 0.0j] * FOCK_DIM for _ in range(FOCK_DIM)]
        for r in ROLES:
            kr = k[r]
            phase = 2.0 * math.pi * kr / side
            grad_r = float(side) * (cmath.exp(1j * phase) - 1.0)
            grad_r_adj = float(side) * (cmath.exp(-1j * phase) - 1.0)  # adjoint = backward diff

            for i in range(FOCK_DIM):
                for j in range(FOCK_DIM):
                    if c_dag[r][i][j] != 0:
                        D_k[i][j] += grad_r * c_dag[r][i][j]
                    if c[r][i][j] != 0:
                        D_k[i][j] += grad_r_adj * c[r][i][j]

        # Compute D(k)^2 = D_k @ D_k
        D2_k = [[0.0 + 0.0j] * FOCK_DIM for _ in range(FOCK_DIM)]
        for i in range(FOCK_DIM):
            for m in range(FOCK_DIM):
                if D_k[i][m] != 0:
                    for j in range(FOCK_DIM):
                        D2_k[i][j] += D_k[i][m] * D_k[m][j]

        # Check whether D2_k == expected_lam * I_16
        for i in range(FOCK_DIM):
            for j in range(FOCK_DIM):
                expected = (expected_lam + 0.0j) if i == j else 0.0j
                diff = abs(D2_k[i][j] - expected)
                if diff > 1e-9:
                    return False

    return True


def main() -> int:
    canonical_square_holds = verify_dirac_square(side=3, mutate=False)
    mutated_square_holds = verify_dirac_square(side=3, mutate=True)

    checks = {
        "fock_dimension_16": FOCK_DIM == 16,
        "canonical_car_dirac_square_matches_laplacian": canonical_square_holds,
        "negative_mutated_sign_cross_terms_survive": not mutated_square_holds,
    }

    status = "PASS_CANONICAL_CAR_SQUARE" if all(checks.values()) else "FAIL_CANONICAL_CAR_SQUARE"

    payload = {
        "status": status,
        "carrier_source": "D0.Geometry.ArchiveCARFockCarrier.ArchiveFockState",
        "operator_source": "D0.Geometry.ArchiveCARDirac.archiveCARDirac",
        "laplacian_source": "D0.Geometry.ArchiveRoleProductLaplacian.archiveMetricProductLaplacian",
        "checks": checks,
    }

    print("operator_source: D0.Geometry.ArchiveCARDirac")
    print("laplacian_source: D0.Geometry.ArchiveRoleProductLaplacian")
    print(status)
    print(json.dumps(payload, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
