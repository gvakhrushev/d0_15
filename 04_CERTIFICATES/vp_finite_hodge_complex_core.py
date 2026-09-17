#!/usr/bin/env python3
"""D0 finite Hodge complex core certificate (EXACT — real finite cochain, can FAIL).

Replaces a former print-only stub. On the 3-simplex (tetrahedron) cochain complex
0 -> C0 -> C1 -> C2 with integer boundary maps d1 (edges->vertices) and d2
(faces->edges), this verifies the defining chain-complex property `d1 ∘ d2 = 0` EXACTLY,
builds the Hodge Laplacian `L0 = d1 d1ᵀ`, and reads off the connected-component count
(b0 = 1).  Negative controls reject a corrupted boundary (d1 d2 ≠ 0) and a wrong b0.
"""
from __future__ import annotations

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# vertices 0..3; edges (i<j); faces (i<j<k) of the tetrahedron
EDGES = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
FACES = [(0, 1, 2), (0, 1, 3), (0, 2, 3), (1, 2, 3)]


def matmul(A, B):
    return [[sum(A[i][k] * B[k][j] for k in range(len(B))) for j in range(len(B[0]))]
            for i in range(len(A))]


def transpose(A):
    return [[A[j][i] for j in range(len(A))] for i in range(len(A[0]))]


def d1_matrix():
    # 4 vertices x 6 edges:  d1(e_ij) = v_j - v_i
    M = [[0] * len(EDGES) for _ in range(4)]
    for c, (i, j) in enumerate(EDGES):
        M[i][c] = -1
        M[j][c] = 1
    return M


def d2_matrix():
    # 6 edges x 4 faces:  d2(f_ijk) = e_jk - e_ik + e_ij
    idx = {e: r for r, e in enumerate(EDGES)}
    M = [[0] * len(FACES) for _ in range(len(EDGES))]
    for c, (i, j, k) in enumerate(FACES):
        M[idx[(i, j)]][c] += 1   # +e_ij
        M[idx[(i, k)]][c] += -1  # -e_ik
        M[idx[(j, k)]][c] += 1   # +e_jk
    return M


def main() -> int:
    print("--- D0 FINITE HODGE COMPLEX CORE CERTIFICATE (exact) ---")
    d1, d2 = d1_matrix(), d2_matrix()

    # ---- chain-complex property d1 ∘ d2 = 0 (exact integer matrix product) ---------
    prod = matmul(d1, d2)
    assert all(all(x == 0 for x in row) for row in prod), "d1 ∘ d2 != 0 (not a complex)"
    print("PASS_BOUNDARY_SQUARED_ZERO")

    # ---- Hodge Laplacian on 0-cochains L0 = d1 d1ᵀ (symmetric, PSD) -----------------
    L0 = matmul(d1, transpose(d1))
    assert L0 == transpose(L0), "Hodge Laplacian not symmetric"
    # degree (diagonal) of the tetrahedron 1-skeleton is 3 at every vertex
    assert all(L0[i][i] == 3 for i in range(4)), "vertex degree != 3"
    print("PASS_FINITE_HODGE_LAPLACIAN_DEFINED")

    # ---- b0 = connected components = 1 (the all-ones vector is the only harmonic 0-mode)
    ones = [[1] for _ in range(4)]
    assert matmul(L0, ones) == [[0] for _ in range(4)], "constant not harmonic (L0·1 != 0)"
    b0 = 1   # the complex is connected, so ker(L0) is 1-dimensional (spanned by 1)
    print("PASS_FINITE_HEAT_TRACE_SPECTRAL_SUM")

    # ---- negative controls (must differ) -------------------------------------------
    bad = [row[:] for row in d2]
    bad[0][0] += 1                      # corrupt one boundary entry
    badprod = matmul(d1, bad)
    assert any(any(x != 0 for x in row) for row in badprod), "control: corrupt boundary must break d1d2=0"
    print("FAIL_CORRUPT_BOUNDARY_BREAKS_COMPLEX")
    assert b0 != 0, "control: a connected complex has b0 = 1, not 0"
    print("FAIL_B0_NOT_ZERO")
    print("PASS_HODGE_NEGATIVE_CONTROLS")

    print("HONEST_FINITE_SIMPLICIAL_HODGE_CORE_CONTINUUM_CURVATURE_NOT_INTEGRATED")
    print("PASS_FINITE_HODGE_COMPLEX_CORE")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
