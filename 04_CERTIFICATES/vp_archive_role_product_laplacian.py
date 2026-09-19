#!/usr/bin/env python3
"""D0-ARCHIVE-ROLE-PRODUCT-LAPLACIAN-001 certificate.

Checks the exact finite matrix owned by ArchiveRoleProductLaplacian:

    B(r,x;y) = L * (delta[y,S_r x] - delta[y,x]),
    Delta = B.T @ B.

The spectrum must be
    sum_r 4 L^2 sin(pi k_r/L)^2
on the four-role product torus.  The L=2 negative control is load-bearing:
boolean simple-cycle adjacency collapses the two oriented incidences and gives a
factor-two smaller nonzero 1D eigenvalue, so it is not the spectral operator.
"""
from __future__ import annotations

from itertools import product
import math
import numpy as np

STATUS = "PASS_ARCHIVE_ROLE_PRODUCT_LAPLACIAN"
ROLE_COUNT = 4
SIDES = (2, 3, 4)
TOL = 2.0e-8


def states(side: int):
    return list(product(range(side), repeat=ROLE_COUNT))


def shift(x: tuple[int, ...], role: int, side: int) -> tuple[int, ...]:
    y = list(x)
    y[role] = (y[role] + 1) % side
    return tuple(y)


def coboundary(side: int, scale: float | None = None) -> np.ndarray:
    xs = states(side)
    where = {x: i for i, x in enumerate(xs)}
    scale = float(side if scale is None else scale)
    B = np.zeros((ROLE_COUNT * len(xs), len(xs)), dtype=float)
    row = 0
    for role in range(ROLE_COUNT):
        for x in xs:
            B[row, where[shift(x, role, side)]] += scale
            B[row, where[x]] -= scale
            row += 1
    return B


def laplacian(side: int, scale: float | None = None) -> np.ndarray:
    B = coboundary(side, scale)
    return B.T @ B


def expected_spectrum(side: int) -> np.ndarray:
    vals = []
    for k in product(range(side), repeat=ROLE_COUNT):
        vals.append(sum(
            4.0 * side * side * math.sin(math.pi * kr / side) ** 2
            for kr in k
        ))
    return np.sort(np.asarray(vals))


def simple_cycle_1d(side: int) -> np.ndarray:
    """Boolean simple-cycle Laplacian, intentionally distinct at side=2."""
    A = np.zeros((side, side), dtype=float)
    for i in range(side):
        A[i, (i + 1) % side] = 1.0
        A[i, (i - 1) % side] = 1.0
    # Boolean adjacency: repeated neighbour at L=2 is still a single edge.
    A[A != 0.0] = 1.0
    degree = np.diag(A.sum(axis=1))
    return side * side * (degree - A)


def kronecker_sum(base: np.ndarray, dimensions: int) -> np.ndarray:
    n = base.shape[0]
    out = np.zeros((n ** dimensions, n ** dimensions), dtype=float)
    I = np.eye(n)
    for role in range(dimensions):
        term = np.array([[1.0]])
        for s in range(dimensions):
            term = np.kron(term, base if s == role else I)
        out += term
    return out


def main() -> int:
    rows = []
    for side in SIDES:
        D = laplacian(side)
        eig = np.sort(np.linalg.eigvalsh(D))
        expected = expected_spectrum(side)
        assert D.shape == (side ** ROLE_COUNT, side ** ROLE_COUNT)
        assert np.allclose(D, D.T, atol=TOL, rtol=0.0)
        assert np.max(np.abs(D.sum(axis=1))) < TOL
        assert eig[0] > -TOL
        assert np.count_nonzero(np.abs(eig) < TOL) == 1
        assert np.allclose(eig, expected, atol=TOL, rtol=0.0)
        rows.append((side, float(eig[-1]), float(np.trace(D))))

    # Load-bearing small-cycle guard.
    metric2 = laplacian(2)
    simple2 = kronecker_sum(simple_cycle_1d(2), ROLE_COUNT)
    metric2_eig = np.sort(np.linalg.eigvalsh(metric2))
    simple2_eig = np.sort(np.linalg.eigvalsh(simple2))
    assert not np.allclose(metric2, simple2, atol=TOL, rtol=0.0)
    assert math.isclose(metric2_eig[-1], 64.0, abs_tol=TOL)
    assert math.isclose(simple2_eig[-1], 32.0, abs_tol=TOL)

    # The metric normalization is L^2. Replacing B's scale L by sqrt(L)
    # gives only L scaling and must fail the exact spectrum.
    wrong = np.sort(np.linalg.eigvalsh(laplacian(4, scale=math.sqrt(4.0))))
    assert not np.allclose(wrong, expected_spectrum(4), atol=TOL, rtol=0.0)

    # Heat trace computed from the matrix agrees with the factorized spectrum.
    side = 4
    eig = np.linalg.eigvalsh(laplacian(side))
    one_d = [
        4.0 * side * side * math.sin(math.pi * k / side) ** 2
        for k in range(side)
    ]
    for u in (0.002, 0.01, 0.05):
        direct = float(np.exp(-u * eig).sum())
        factorized = sum(math.exp(-u * v) for v in one_d) ** ROLE_COUNT
        assert math.isclose(direct, factorized, rel_tol=2e-12, abs_tol=2e-12)

    print("operator_source: ArchiveRolePhasePoint + archiveRoleCoboundary")
    print("operator_identity: Delta = B^T B")
    print("role_count:", ROLE_COUNT)
    print("rows:", rows)
    print("L2_METRIC_MAX_EIG", metric2_eig[-1])
    print("L2_SIMPLE_GRAPH_MAX_EIG", simple2_eig[-1])
    print("PASS_L2_ORIENTED_INCIDENCE_GUARD")
    print("PASS_EXACT_PRODUCT_SPECTRUM")
    print("PASS_HEAT_TRACE_FACTORIZATION")
    print(STATUS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
