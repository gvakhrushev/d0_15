from __future__ import annotations

import numpy as np
from typing import Tuple, List


def complete_tripartite_sizes() -> Tuple[int, int, int]:
    return (9, 11, 13)


def laplacian_complete_tripartite(a: int, b: int, c: int) -> np.ndarray:
    """
    Laplacian of complete tripartite graph K(a,b,c):
    - blocks on diagonal: degree_i on diag (degree depends on part)
    - off-diagonal: -1 between different parts, 0 within part
    """
    n = a + b + c
    L = np.zeros((n, n), dtype=float)
    parts: List[Tuple[int, int, int]] = []
    parts.append((0, a, b + c))
    parts.append((a, a + b, a + c))
    parts.append((a + b, n, a + b))

    for s, e, d in parts:
        np.fill_diagonal(L[s:e, s:e], d)

    for i, (s1, e1, _) in enumerate(parts):
        for j, (s2, e2, _) in enumerate(parts):
            if i == j:
                continue
            L[s1:e1, s2:e2] = -1.0
    return L


def ranks_nullity(A: np.ndarray, tol: float = 1e-12) -> Tuple[int, int]:
    s = np.linalg.svd(A, compute_uv=False)
    rank = int((s > tol).sum())
    null = A.shape[1] - rank
    return rank, null
