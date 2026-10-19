#!/usr/bin/env python3
"""Exact original six-plaquette crossed-null Euler jet through cubic order.

For H=a*x, J=b*y at h=1, start with the published mixed a*b Cartan repair
and continuum Levi-Civita trial. Solve separately for the [a^2*b] and
[a*b^2] corrections, allowing every one of the 24 directed Lorentz-link
components and all 16 coframe components to be site-dependent polynomials of
spatial degree at most three. Then combine both solutions and re-evaluate the
complete 40-row system through total amplitude degree three.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import sympy as s


HERE = Path(__file__).resolve().parent
BASELINE = HERE.parent / "d0_double_null_cubic_uniform_control_2026-10-19" / "check_cubic_uniform_control.py"
MONOMIALS = tuple((ix, degree - ix)
                  for degree in range(4) for ix in range(degree, -1, -1))
LOWER_ORDERS = ((0, 0), (1, 0), (0, 1), (2, 0), (0, 2), (1, 1))
TARGET_ORDERS = ((2, 1), (1, 2))


def load_baseline(name):
    spec = importlib.util.spec_from_file_location(name, BASELINE)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def solve_order(order, name):
    m = load_baseline(name)
    x, y = s.symbols("x y")
    link_variables = []
    link_polynomials = []
    for axis in range(4):
        matrix = s.zeros(4)
        for generator, G in enumerate(m.G):
            for ix, iy in MONOMIALS:
                coefficient = s.symbols(f"w_{order[0]}_{order[1]}_{axis}_{generator}_{ix}_{iy}")
                link_variables.append(coefficient)
                matrix += coefficient * x**ix * y**iy * G
        link_polynomials.append(matrix)

    coframe_variables = []
    coframe_polynomial = s.zeros(4)
    for internal in range(4):
        for coordinate in range(4):
            for ix, iy in MONOMIALS:
                coefficient = s.symbols(f"e_{order[0]}_{order[1]}_{internal}_{coordinate}_{ix}_{iy}")
                coframe_variables.append(coefficient)
                coframe_polynomial[internal, coordinate] += coefficient * x**ix * y**iy

    variables = link_variables + coframe_variables
    base_link, base_coframe = m.link, m.coframe
    baseline_high = [dict(entries) for entries in m.CORR_HIGH]

    def at_site(expression, site):
        return expression.subs({x: site[2], y: site[3]}, simultaneous=True)

    def site_link(site, axis, back=False):
        previous = m.CORR_HIGH
        m.CORR_HIGH = [dict(entries) for entries in baseline_high]
        for direction in range(4):
            m.CORR_HIGH[direction][order] = at_site(link_polynomials[direction], site)
        try:
            return base_link(site, axis, back)
        finally:
            m.CORR_HIGH = previous

    def site_coframe(site):
        return base_coframe(site) + m.Jet.co(*order, at_site(coframe_polynomial, site))

    m.link, m.coframe = site_link, site_coframe
    z = (0, 0, x, y)
    rows = m.link_rows(z) + m.solder_rows(z)
    assert len(rows) == 40

    for lower in LOWER_ORDERS:
        for row in rows:
            assert s.expand(row.coeff(*lower)) == 0, (order, lower)

    equations = []
    for row in rows:
        polynomial = s.Poly(s.expand(row.coeff(*order)), x, y)
        assert polynomial.total_degree() <= 3
        equations.extend(polynomial.coeff_monomial(x**ix * y**iy)
                         for ix, iy in MONOMIALS)

    matrix, rhs = s.linear_eq_to_matrix(equations, variables)
    rank, augmented_rank = matrix.rank(), matrix.row_join(rhs).rank()
    assert matrix.shape == (400, 400)
    assert (rank, augmented_rank) == (266, 266)
    solution, _parameters = matrix.gauss_jordan_solve(rhs)
    free = set().union(*(value.free_symbols for value in solution)) - set(variables)
    solution = [value.subs({parameter: 0 for parameter in free}) for value in solution]
    substitution = dict(zip(variables, solution))
    assert all(s.simplify(eq.subs(substitution)) == 0 for eq in equations)

    correction = {
        "link": [poly.subs(substitution) for poly in link_polynomials],
        "coframe": coframe_polynomial.subs(substitution),
    }
    nonzero = [(str(variable), s.factor(value))
               for variable, value in zip(variables, solution) if value != 0]
    print(f"PASS [{order[0]} {order[1]}] system: 400 exact equations, rank {rank}, augmented rank {augmented_rank}")
    print(f"  free parameters={len(free)}; selected nonzero coefficients={len(nonzero)}")
    for variable, value in nonzero:
        print(f"  {variable} = {value}")
    return correction


solutions = {order: solve_order(order, f"cubic_baseline_{order[0]}_{order[1]}")
             for order in TARGET_ORDERS}

# Rebuild one action state containing both cubic corrections, then check all
# independent field equations simultaneously through total amplitude degree 3.
m = load_baseline("cubic_baseline_combined")
x, y = s.symbols("x y")
base_link, base_coframe = m.link, m.coframe
baseline_high = [dict(entries) for entries in m.CORR_HIGH]


def at_site(expression, site):
    return expression.subs({x: site[2], y: site[3]}, simultaneous=True)


def combined_link(site, axis, back=False):
    previous = m.CORR_HIGH
    m.CORR_HIGH = [dict(entries) for entries in baseline_high]
    for direction in range(4):
        for order in TARGET_ORDERS:
            m.CORR_HIGH[direction][order] = at_site(solutions[order]["link"][direction], site)
    try:
        return base_link(site, axis, back)
    finally:
        m.CORR_HIGH = previous


def combined_coframe(site):
    result = base_coframe(site)
    for order in TARGET_ORDERS:
        result += m.Jet.co(*order, at_site(solutions[order]["coframe"], site))
    return result


m.link, m.coframe = combined_link, combined_coframe
z = (0, 0, x, y)
combined_rows = m.link_rows(z) + m.solder_rows(z)
for order in LOWER_ORDERS + TARGET_ORDERS:
    for index, row in enumerate(combined_rows):
        assert s.expand(row.coeff(*order)) == 0, (order, index, s.factor(row.coeff(*order)))
print("PASS combined corrected state: all 40 original Euler rows vanish identically in x,y through total amplitude degree three")
print("SCOPE: h=1, H=a*x, J=b*y, fixed crossed-null chart. Higher amplitude orders, arbitrary slopes, refinement, boundaries and native D0 price remain open.")
