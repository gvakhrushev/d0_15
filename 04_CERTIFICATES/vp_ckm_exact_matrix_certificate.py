#!/usr/bin/env python3
"""Exact finite CKM-origin matrix certificate for the concrete orientation witness."""
from __future__ import annotations

# Up orientation is canonical: up basis vectors are 0,1,2.
up = [0, 1, 2]
# Down orientation is cyclicShift: down basis vectors are 1,2,0.
down = [1, 2, 0]
M = [[1 if up_i == down_j else 0 for down_j in down] for up_i in up]
expected = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]
assert M == expected, M
assert all(sum(row) == 1 for row in M)
assert all(sum(M[i][j] for i in range(3)) == 1 for j in range(3))
print("CKM_EXACT_MATRIX")
for row in M:
    print(row)
print("PASS_CKM_EXACT_MATRIX_CERTIFICATE")
