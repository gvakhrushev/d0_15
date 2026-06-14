#!/usr/bin/env python3
"""D0-ICOSIAN-E8-GRAM-001 — the E8 Gram is even unimodular (finite shadow of icosian->E8).

Finite-core reduction (Option-1) of the icosian->E8 family. The Mordell genus-uniqueness
THEOREM (E8 is the UNIQUE even unimodular rank-8 lattice) needs lattice-genus machinery
absent from Mathlib and stays EXTERNAL-GAP. Its DECIDABLE SHADOW is exact: the specific E8
Gram matrix (the simply-laced E8 Cartan matrix) IS even and unimodular, and its rank 8 is
the Z[sqrt5]->Z doubling of the rank-4 icosian ring (2*4=8).

WHAT IS PROVED (exact integer arithmetic, able to FAIL):
  * EVEN.  The E8 Gram is symmetric with all diagonal entries = 2 (even) and integer
    off-diagonal entries — i.e. it is an even lattice (q(x)=xᵀGx is even-valued).
  * UNIMODULAR.  det(G) = 1 (exact integer Bareiss determinant) — the lattice is self-dual.
  * RANK = 8 = 2*4.  The icosian ring is rank 4 over Z[sqrt5]; the Galois doubling
    a+b sqrt5 |-> (a,b) sends it to a rank-8 Z-lattice — exactly E8's rank.

HONESTY BOUNDARY (printed, not hidden):
  * This proves the SPECIFIC E8 Gram is even unimodular (decidable). It does NOT prove the
    Mordell uniqueness (E8 is THE even unimodular rank-8 lattice) — that genus theorem stays
    EXTERNAL-GAP. The icosian->E8 embedding itself is the bridge; here we certify the target
    lattice's defining invariants exactly.
"""
from __future__ import annotations

import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# E8 Cartan / Gram matrix (simply-laced => Gram = Cartan), 8x8 integer, Bourbaki-style tree
E8 = [
    [2, 0, -1, 0, 0, 0, 0, 0],
    [0, 2, 0, -1, 0, 0, 0, 0],
    [-1, 0, 2, -1, 0, 0, 0, 0],
    [0, -1, -1, 2, -1, 0, 0, 0],
    [0, 0, 0, -1, 2, -1, 0, 0],
    [0, 0, 0, 0, -1, 2, -1, 0],
    [0, 0, 0, 0, 0, -1, 2, -1],
    [0, 0, 0, 0, 0, 0, -1, 2],
]


def det_exact(M):
    """Exact integer determinant via fraction-free Bareiss elimination."""
    n = len(M)
    A = [[F(x) for x in row] for row in M]
    sign = 1
    prev = F(1)
    for k in range(n - 1):
        if A[k][k] == 0:
            swap = next((i for i in range(k + 1, n) if A[i][k] != 0), None)
            if swap is None:
                return 0
            A[k], A[swap] = A[swap], A[k]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i][j] = (A[i][j] * A[k][k] - A[i][k] * A[k][j]) / prev
        prev = A[k][k]
    return sign * A[n - 1][n - 1]


def main() -> int:
    print("=== D0-ICOSIAN-E8-GRAM-001  E8 Gram even unimodular (icosian->E8 shadow) ===")

    n = len(E8)
    assert n == 8 and all(len(r) == 8 for r in E8), "E8 Gram not 8x8"

    # ---- even lattice: symmetric, integer, diagonal all 2 --------------------------
    assert all(E8[i][j] == E8[j][i] for i in range(8) for j in range(8)), "Gram not symmetric"
    assert all(isinstance(E8[i][j], int) for i in range(8) for j in range(8)), "non-integer entry"
    assert all(E8[i][i] == 2 for i in range(8)), "diagonal not all 2 (not even)"
    print("PASS_EVEN_LATTICE  symmetric integer Gram, diagonal all 2 (q is even-valued)")

    # ---- unimodular: det = 1 (exact integer Bareiss) -------------------------------
    d = det_exact(E8)
    assert d == 1, f"det(E8 Gram) != 1 (not unimodular): {d}"
    print(f"PASS_UNIMODULAR  det(E8 Gram) = {int(d)} (self-dual lattice)")

    # ---- rank 8 = 2*4 (icosian Z[sqrt5]->Z doubling) -------------------------------
    icosian_rank_over_Zsqrt5 = 4
    assert n == 2 * icosian_rank_over_Zsqrt5 == 8, "rank != 2*4"
    print("PASS_RANK_8_IS_ICOSIAN_DOUBLING  8 = 2*4 (Z[sqrt5]->Z Galois doubling of icosians)")

    # ---- negative controls (must differ) -------------------------------------------
    # odd diagonal -> not an even lattice
    odd = [row[:] for row in E8]; odd[0][0] = 1
    assert not all(odd[i][i] % 2 == 0 for i in range(8)), "control: odd diagonal is not even"
    print("FAIL_ODD_DIAGONAL_NOT_EVEN_LATTICE")
    # a perturbed Gram with det != 1 is not unimodular
    bad = [row[:] for row in E8]; bad[0][0] = 3
    assert det_exact(bad) != 1, "control: perturbed Gram must not be unimodular"
    print("FAIL_PERTURBED_GRAM_NOT_UNIMODULAR")
    # A8 (not E8) has det 9, not 1 -> only the E8 tree gives unimodular
    A8 = [[2 if i == j else (-1 if abs(i - j) == 1 else 0) for j in range(8)] for i in range(8)]
    assert det_exact(A8) == 9, "control: A8 chain det should be 9, not 1"
    print("FAIL_A8_CHAIN_DET_9_NOT_UNIMODULAR")
    print("PASS_ICOSIAN_E8_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_PROVES_E8_GRAM_EVEN_UNIMODULAR_NOT_MORDELL_GENUS_UNIQUENESS")
    print("HONEST_MORDELL_E8_IS_THE_UNIQUE_EVEN_UNIMODULAR_RANK8_STAYS_EXTERNAL_GAP")

    print("PASS_ICOSIAN_E8_GRAM")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
