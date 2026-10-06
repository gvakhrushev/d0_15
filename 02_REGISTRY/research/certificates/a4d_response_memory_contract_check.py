#!/usr/bin/env python3
"""Exact contract controls, not a D0 field-equation or continuum certificate.

The general identities are proved in CONTROL_RESPONSE_MEMORY_CONSOLIDATION.md.
These finite rational fixtures reject the previously proposed invalid terminals.
No source is inferred from an unknown field and no expected ledger is rewritten.
"""
from fractions import Fraction as F
from itertools import product


def l1(values):
    return sum((abs(value) for value in values), F(0))


def source_response(h, tau):
    if h <= 0:
        raise ValueError("positive mesh spacing required")
    return tuple(h * h * value for value in tau)


def source_residual(h, tau, xi):
    if len(tau) != len(xi):
        raise ValueError("source and response must have the same slots")
    return tuple(a - b for a, b in zip(xi, source_response(h, tau)))


def main():
    checks = 0
    # The two exact source rows cannot simultaneously hold with distinct Xi.
    for h, tau in product((F(1, 4), F(1, 8), F(1, 12)),
                          ((F(0),), (F(2, 3), F(-5, 7), F(0)))):
        xi1 = source_response(h, tau)
        xi2 = source_response(h, tau)
        assert l1(a-b for a, b in zip(xi1, xi2)) == 0
        wrong = (xi2[0] + F(1, 11),) + xi2[1:]
        assert l1(source_residual(h, tau, wrong)) > 0
        checks += 1
    # The designated comparator need not be an exact root of this source.
    h = F(1, 8)
    tau = (F(2, 3), F(-5, 7), F(0))
    rho_sm = (F(1, 2), F(-2, 7), F(1, 13))
    xi, xi_sm = source_response(h, tau), source_response(h, rho_sm)
    assert l1(a-b for a, b in zip(xi, xi_sm)) / h**2 == l1(a-b for a, b in zip(tau, rho_sm))
    assert l1(source_residual(h, tau, xi_sm)) > 0
    checks += 1
    # Reproduce only the norm arithmetic of the historical mesh-dependent
    # source fixture; this is NOT its physical Euler/existence verification.
    for L in (4, 8, 12):
        h = F(1, L)
        assert L**4 * 6 * h**6 / h**2 == 6
        assert h**4 * (L**4 * 6 * h**6 / h**2) == 6 * h**4
        # O(h^2) locally is not enough for h^-2 times an unweighted 4D sum.
        assert L**4 * h**2 / h**2 == L**4
        assert L**4 * h**6 / h**2 == 1
        checks += 1
    # Telescoping signed sums do not control the unweighted absolute norm.
    for L in (4, 8, 12):
        values = tuple(F((-1)**i) for i in range(L))
        divergence = tuple(values[i] - values[(i-1) % L] for i in range(L))
        assert sum(divergence) == 0 and l1(divergence) == 2 * L
        checks += 1
    # A stencil of radius zero can retain N independent response coordinates:
    # its derivative is I_N. This is a generic countermodel to the inference
    # 'finite stencil => uniformly finite response rank', not a D0 no-go.
    for N in (1, 2, 4, 8, 16):
        basis = [tuple(F(i == j) for i in range(N)) for j in range(N)]
        assert len(set(basis)) == N
        for j in range(N):
            assert tuple(v[j] for v in basis) == basis[j]
        checks += 1
    # Canonical Y harmonic-memory formula from SOURCE_IMAGE_COLLAPSE §9.2:
    # its nonzero value is compatible with the owner's Xi=0. Here only the
    # rational coefficient/nonconstancy is checked, not the Y Euler equations.
    assert F(1, 5)**2 / (4 + 3*F(1, 5)**2) == F(1, 103)
    assert F(1, 4)**2 / (4 + 3*F(1, 4)**2) == F(1, 67)
    checks += 1
    print(f"PASS {checks} exact source/comparator and memory-contract controls")
    print("SCOPE: contract regression only; original D0 response terminal remains OPEN")


if __name__ == '__main__':
    main()
