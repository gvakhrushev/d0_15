#!/usr/bin/env python3
"""Exact cubic compatibility test on the original six-plaquette action.

The baseline is the fixed-coframe orthogonal crossed-null chart H=a*x, J=b*y
with the published mixed a*b Cartan repair. At order a^2*b, allow all 24
proper-Lorentz link corrections and all 16 coframe corrections to be arbitrary
quadratic polynomials in the transverse lattice coordinates. Site coordinates
are substituted separately for every shifted link/coframe evaluation.

The resulting 240 exact rational equations have rank 154, while the augmented
system has rank 155. This excludes this polynomial correction chart only; it
does not exclude arbitrary functions on the lattice or an exact nonpolynomial
root.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / "d0_double_null_cubic_uniform_control_2026-10-19" / "check_cubic_uniform_control.py"
spec = importlib.util.spec_from_file_location("cubic_baseline", BASELINE)
assert spec is not None and spec.loader is not None
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

x, y = s.symbols("x y")
monomials = ((0, 0), (1, 0), (0, 1), (2, 0), (1, 1), (0, 2))
link_variables = []
link_polynomials = []
for axis in range(4):
    matrix = s.zeros(4)
    for generator, G in enumerate(m.G):
        for ix, iy in monomials:
            coefficient = s.symbols(f"w_{axis}_{generator}_{ix}_{iy}")
            link_variables.append(coefficient)
            matrix += coefficient * x**ix * y**iy * G
    link_polynomials.append(matrix)

coframe_variables = []
coframe_polynomial = s.zeros(4)
for internal in range(4):
    for coordinate in range(4):
        for ix, iy in monomials:
            coefficient = s.symbols(f"e_{internal}_{coordinate}_{ix}_{iy}")
            coframe_variables.append(coefficient)
            coframe_polynomial[internal, coordinate] += coefficient * x**ix * y**iy

variables = link_variables + coframe_variables
base_link = m.link
base_coframe = m.coframe
baseline_high_corrections = [dict(entries) for entries in m.CORR_HIGH]


def at_site(expression, site):
    return expression.subs({x: site[2], y: site[3]}, simultaneous=True)


def site_link(site, axis, back=False):
    previous = m.CORR_HIGH
    m.CORR_HIGH = [dict(entries) for entries in baseline_high_corrections]
    for direction in range(4):
        m.CORR_HIGH[direction][(2, 1)] = at_site(link_polynomials[direction], site)
    try:
        return base_link(site, axis, back)
    finally:
        m.CORR_HIGH = previous


def site_coframe(site):
    return base_coframe(site) + m.Jet.co(2, 1, at_site(coframe_polynomial, site))


m.link = site_link
m.coframe = site_coframe
z = (0, 0, x, y)
rows = m.link_rows(z) + m.solder_rows(z)
equations = []
for row in rows:
    polynomial = s.Poly(s.expand(row.coeff(2, 1)), x, y)
    assert polynomial.total_degree() <= 2
    equations.extend(polynomial.coeff_monomial(x**ix * y**iy)
                     for ix, iy in monomials)

matrix, rhs = s.linear_eq_to_matrix(equations, variables)
rank = matrix.rank()
augmented_rank = matrix.row_join(rhs).rank()
assert len(rows) == 40
assert len(equations) == 240
assert matrix.shape == (240, 240)
assert (rank, augmented_rank) == (154, 155)

print("PASS exact original six-plaquette [a^2 b] Euler expansion: 24 link + 16 coframe rows")
print("PASS site-dependent quadratic polynomial corrections: 240 rational equations")
print(f"INCONSISTENT chart: coefficient rank={rank}, augmented rank={augmented_rank}")
print("SCOPE: excludes only this degree<=2 polynomial correction chart at h=1 for H=a*x, J=b*y.")
print("SCOPE: arbitrary spatial lattice modes, higher-order/nonpolynomial corrections, other coframe branches, and native D0 price remain open.")
