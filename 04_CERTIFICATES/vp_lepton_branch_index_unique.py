#!/usr/bin/env python3
# vp_lepton_branch_index_unique.py
# Cert for D0-LEPTON-CYCLIC-GENERATOR-001 (branch-index uniqueness clause, status THE for the INDEX).
#
# Claim: C_n (char poly z^n - 1) has SIMPLE spectrum (n distinct n-th roots of unity), hence is
# non-derogatory, hence any matrix with this char poly is similar to C_n; the Puiseux branch index
# 1/n is similarity-invariant, so it is uniquely determined. The generic isospectral/derogatory
# obstruction (non-similar matrices sharing a char poly) requires REPEATED roots and does NOT apply.
# External owners: Newton-Puiseux (1671/1850; Duval 1989); Kato perturbation theory (1966).
# SCOPE: fixes the INDEX 1/n only, NOT the branch->generation row map (= v16 NO-GO
# D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001); decimals stay external (ASSUMP-LEPTON-EFT-DECIMALS).
import numpy as np


def cycle(n):
    return np.roll(np.eye(n), 1, axis=0)


def distinct_spectrum(M):
    ev = np.round(np.linalg.eigvals(M), 8)
    return len(set(ev.tolist())) == M.shape[0]


def main():
    for n in (3, 4):
        C = cycle(n)
        assert distinct_spectrum(C), f"C_{n} must have simple spectrum (distinct n-th roots of 1)"
        rng = np.random.default_rng(n)
        U = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
        while abs(np.linalg.det(U)) < 1e-6:
            U = rng.standard_normal((n, n)) + 1j * rng.standard_normal((n, n))
        M = U @ C.astype(complex) @ np.linalg.inv(U)
        assert np.allclose(sorted(np.linalg.eigvals(M).round(6), key=lambda z: (z.real, z.imag)),
                           sorted(np.linalg.eigvals(C).round(6), key=lambda z: (z.real, z.imag))), \
            "conjugate must share spectrum"
        z = 0.3 + 0.1j
        assert np.isclose(np.linalg.det(np.eye(n) - z * C), 1 - z ** n), "det(I-zC_n)=1-z^n"
        print(f"  n={n}: simple spectrum, non-derogatory, branch index 1/{n} similarity-invariant => unique")

    # CONTROL (must exhibit the obstruction): repeated-root char poly admits NON-similar isospectral matrices.
    A = np.array([[1, 0], [0, 1]], float)        # diagonalizable, eigenvalue 1 (mult 2)
    B = np.array([[1, 1], [0, 1]], float)        # Jordan block, same char poly (z-1)^2, NOT similar
    same_charpoly = np.allclose(np.poly(A), np.poly(B))
    similar = (np.linalg.matrix_rank(A - np.eye(2)) == np.linalg.matrix_rank(B - np.eye(2)))
    assert same_charpoly and not similar, \
        "CONTROL: repeated-root (z-1)^2 must admit non-similar isospectral matrices (obstruction bites)"
    print("  CONTROL ok: (z-1)^2 -> diag vs Jordan isospectral but NOT similar; z^n-1 (distinct roots) immune.")
    print("PASS  D0-LEPTON-CYCLIC-GENERATOR-001 (branch-index uniqueness; INDEX only, row map stays v16 NO-GO)")


if __name__ == "__main__":
    main()
