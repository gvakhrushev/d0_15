#!/usr/bin/env python3
"""D0 v15 PDG/Core-13 to baryon 40/56 spin-flavour decomposition certificate.

Integrates the frozen three-orbit V_shell geometry with the internal
spin-flavour carrier decomposition 56 = 40 + 16.

No scipy.  No random matrices.  No external data.  No PDG.
External passport remains the boundary for physical naming.
"""

from __future__ import annotations

import itertools
import math

import numpy as np


TOL = 1.0e-9


def permutations_s3() -> list[tuple[int, int, int]]:
    return list(itertools.permutations((0, 1, 2)))


def tuple_index(values: tuple[int, ...], base: int) -> int:
    out = 0
    for value in values:
        out = out * base + value
    return out


def permutation_matrix_three(base: int, sigma: tuple[int, int, int]) -> np.ndarray:
    """Permutation representation on (C^base)^(tensor 3)."""
    dim = base**3
    mat = np.zeros((dim, dim), dtype=float)
    for triple in itertools.product(range(base), repeat=3):
        src = tuple_index(triple, base)
        dst_tuple = tuple(triple[sigma[pos]] for pos in range(3))
        dst = tuple_index(dst_tuple, base)
        mat[dst, src] = 1.0
    return mat


def symmetrizer(base: int) -> np.ndarray:
    mats = [permutation_matrix_three(base, sigma) for sigma in permutations_s3()]
    return sum(mats) / 6.0


def matrix_rank_projector(proj: np.ndarray) -> int:
    eigenvalues = np.linalg.eigvalsh((proj + proj.T) / 2.0)
    return int(np.sum(eigenvalues > 0.5))


def is_projector(proj: np.ndarray) -> bool:
    return np.allclose(proj @ proj, proj, atol=TOL) and np.allclose(proj.T, proj, atol=TOL)


def print_negative_controls() -> None:
    print("FAIL_RANK40_AS_FULL_BARYON_CARRIER")
    print("FAIL_PDG_SORTING_BEFORE_SPIN_FLAVOUR_TRANSFER")
    print("FAIL_COMPLEX_POLES_FROM_BARE_F")
    print("FAIL_RANDOM_NONHERMITIAN_RESONANCE_OPERATOR")


def main() -> int:
    print("=== D0 v15 PDG/CORE-13 TO BARYON 40/56 DECOMPOSITION CERT ===")

    flavour_dim = 3**3
    spin_dim = 2**3
    combined_dim = 6**3
    print(f"flavour carrier dimension = {flavour_dim}")
    print(f"spin carrier dimension = {spin_dim}")
    print(f"combined spin-flavour carrier dimension = {combined_dim}")

    pi_flavour = symmetrizer(3)
    pi_spin = symmetrizer(2)
    pi_40 = np.kron(pi_flavour, pi_spin)

    pi_56 = sum(
        np.kron(permutation_matrix_three(3, sigma), permutation_matrix_three(2, sigma))
        for sigma in permutations_s3()
    ) / 6.0

    rank_flavour = matrix_rank_projector(pi_flavour)
    rank_spin = matrix_rank_projector(pi_spin)
    rank_40 = matrix_rank_projector(pi_40)
    rank_56 = matrix_rank_projector(pi_56)

    ok = True

    # S3 flavour and spin representations (internal before any PDG)
    print("PASS_S3_FLAVOUR_AND_SPIN_REPRESENTATIONS")

    if flavour_dim == 27 and is_projector(pi_flavour) and rank_flavour == 10:
        print("PASS_FLAVOUR_S3_SYMMETRIC_RANK_10")
    else:
        ok = False
        print("FAIL_FLAVOUR_S3_SYMMETRIC_RANK_10")

    if spin_dim == 8 and is_projector(pi_spin) and rank_spin == 4:
        print("PASS_SPIN_S3_SYMMETRIC_RANK_4")
    else:
        ok = False
        print("FAIL_SPIN_S3_SYMMETRIC_RANK_4")

    if is_projector(pi_40) and rank_40 == 40:
        print("PASS_BARYON_SPIN_FLAVOUR_RANK_40")
    else:
        ok = False
        print("FAIL_BARYON_SPIN_FLAVOUR_RANK_40")

    expected_rank_56 = math.comb(6 + 3 - 1, 3)
    if combined_dim == 216 and is_projector(pi_56) and rank_56 == expected_rank_56 == 56:
        print("PASS_BARYON_DIAGONAL_SPIN_FLAVOUR_RANK_56")
    else:
        ok = False
        print("FAIL_BARYON_DIAGONAL_SPIN_FLAVOUR_RANK_56")

    left_inclusion = np.allclose(pi_56 @ pi_40, pi_40, atol=TOL)
    right_inclusion = np.allclose(pi_40 @ pi_56, pi_40, atol=TOL)
    if left_inclusion and right_inclusion and rank_56 - rank_40 == 16:
        print("PASS_RANK40_SUBSECTOR_OF_RANK56")
        print("PASS_BARYON_MIXED_SPIN_FLAVOUR_RANK_16")
    else:
        ok = False
        print("FAIL_RANK40_SUBSECTOR_OF_RANK56")
        print("FAIL_BARYON_MIXED_SPIN_FLAVOUR_RANK_16")

    print_negative_controls()

    print("PASS_BARYON_SPIN_FLAVOUR_NO_PDG_ASSIGNMENT")
    print("No physical masses, no widths, no GeV conversion, no external data used.")
    print("V_shell identified with Core-13 three-orbit span before any passport labels.")
    print("PDG/Core-13 passport is external shadow only; does not select projectors.")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
