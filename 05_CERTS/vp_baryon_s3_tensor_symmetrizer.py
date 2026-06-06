#!/usr/bin/env python3
"""Finite S3 tensor symmetrizer certificate for the baryon decuplet carrier."""
from __future__ import annotations

from itertools import permutations, product

import numpy as np


ROLES = range(3)
TRIPLES = [(a, b, c) for a in ROLES for b in ROLES for c in ROLES]
INDEX = {triple: i for i, triple in enumerate(TRIPLES)}
S3 = list(permutations(range(3)))


def inverse_perm(p: tuple[int, int, int]) -> tuple[int, int, int]:
    inv = [0, 0, 0]
    for i, image in enumerate(p):
        inv[image] = i
    return tuple(inv)


def act(p: tuple[int, int, int], t: tuple[int, int, int]) -> tuple[int, int, int]:
    inv = inverse_perm(p)
    return tuple(t[inv[i]] for i in range(3))


def permutation_matrix(p: tuple[int, int, int]) -> np.ndarray:
    mat = np.zeros((len(TRIPLES), len(TRIPLES)), dtype=float)
    for col, triple in enumerate(TRIPLES):
        row = INDEX[act(p, triple)]
        mat[row, col] = 1.0
    return mat


rho = {p: permutation_matrix(p) for p in S3}
pi_sym = sum(rho.values()) / len(S3)

carrier_dim = len(TRIPLES)
s3_order = len(S3)
rank_sym = int(np.linalg.matrix_rank(pi_sym, tol=1e-10))
idempotent = np.allclose(pi_sym @ pi_sym, pi_sym)
left_invariance = all(np.allclose(rho[p] @ pi_sym, pi_sym) for p in S3)
right_invariance = all(np.allclose(pi_sym @ rho[p], pi_sym) for p in S3)

sorted_representatives = sorted({tuple(sorted(t)) for t in TRIPLES})
assert carrier_dim == 27
assert s3_order == 6
assert len(sorted_representatives) == 10
assert rank_sym == 10
assert idempotent
assert left_invariance
assert right_invariance

# A deterministic antisymmetric line witness under the first-position swap.
line = np.zeros(carrier_dim)
line[INDEX[(0, 1, 0)]] = 1.0
line[INDEX[(1, 0, 0)]] = -1.0
antisymmetric_line_projection = pi_sym @ line
antisymmetric_line_overlap = float(np.linalg.norm(antisymmetric_line_projection))
assert np.allclose(antisymmetric_line_projection, 0.0)

print("PASS_BARYON_S3_TENSOR_SYMMETRIZER")
print(f"carrier_dim = {carrier_dim}")
print(f"s3_order = {s3_order}")
print(f"rank_sym = {rank_sym}")
print("idempotent = PASS")
print("left_invariance = PASS")
print("right_invariance = PASS")
print(f"antisymmetric_line_overlap = {antisymmetric_line_overlap:.1f}")
