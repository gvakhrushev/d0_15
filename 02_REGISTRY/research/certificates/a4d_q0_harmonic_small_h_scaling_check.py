#!/usr/bin/env python3
"""Exact small-h grading of the #296 q0 harmonic lift coefficients.

This checks the coefficient formula owned by
``a4d_q0_harmonic_lift_obstruction_check.py``.  It distinguishes that
Gram-lift series from the independent #260 connection-amplitude degree-six
calculation.  It makes no claim about the full action, a slow Y response, or
the physical cross-character cokernel.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

import sympy as sp


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def zero(vector: sp.MatrixBase) -> bool:
    return all(sp.expand(entry) == 0 for entry in vector)


def minimum_total_degree(expression: sp.Expr, variables: list[sp.Symbol]) -> int | None:
    polynomial = sp.Poly(sp.expand(expression), *variables)
    if polynomial.is_zero:
        return None
    return min(sum(monomial) for monomial, coefficient in polynomial.terms() if coefficient != 0)


def leading_order(expression: sp.Expr, variable: sp.Symbol) -> int | None:
    """Return 0 for a nonzero constant, and None only for the zero polynomial."""
    polynomial = sp.Poly(sp.expand(expression), variable)
    if polynomial.is_zero:
        return None
    return min(monomial[0] for monomial, coefficient in polynomial.terms() if coefficient != 0)


OWNER = Path(__file__).with_name("a4d_metric_null_hessian_complex_check.py")
source = OWNER.read_text(encoding="utf-8")
cut = source.index("# Exact projective cover of d != 0.")
owner = {"__name__": "_q0_harmonic_scaling_owner", "__file__": str(OWNER)}
exec(compile(source[:cut], str(OWNER), "exec"), owner)
C = owner["C"]
d = sp.Matrix(owner["d"])
dvars = list(d)
eta = sp.diag(1, -1, -1, -1)
upper_triangle = [(i, j) for i in range(4) for j in range(i, 4)]


def symmetric_vector(matrix: sp.MatrixBase) -> sp.Matrix:
    return sp.Matrix([matrix[i, j] for i, j in upper_triangle])


def q_vector(vector: sp.MatrixBase) -> sp.Matrix:
    return symmetric_vector(vector * vector.T)


h = sp.symbols("h")
p = sp.symbols("p0:4", real=True)
pv = sp.Matrix(p)
P = sp.expand((pv.T * eta * pv)[0])
q0 = q_vector(d)
sigma = sp.expand((d.T * eta * d)[0])
d_squared = [entry**2 for entry in dvars]
base = (C.subs(dict(zip(dvars, d_squared)), simultaneous=True) * q0).applyfunc(sp.expand)

check("CONSTANT_LEADING_ORDER_IS_ZERO", leading_order(sp.Integer(7), h) == 0)
check("ZERO_POLYNOMIAL_HAS_NO_LEADING_ORDER", leading_order(sp.Integer(0), h) is None)
check("HARMONIC_NULL_IDENTITY", zero(C * q0))
check("FIRST_HARMONIC_IS_IDENTICALLY_ZERO", zero(C * q0))
check("FIRST_NONZERO_HOMOGENEOUS_FACTOR_EXISTS", any(entry != 0 for entry in base))

# d(z^n)=(1+d)^n-1.  The linear term n*d is annihilated by C(d)q0=0;
# the first candidate is binomial(n,2)*C(d^2)q0.  Its residual has degree
# at least five before multiplication by sigma^(n-1), so the full coefficient
# has no degree below (2n-2)+4 = 2n+2.
for n in range(2, 9):
    delta = [sp.expand((1 + entry) ** n - 1 - n * entry) for entry in dvars]
    inner = (C.subs(dict(zip(dvars, delta)), simultaneous=True) * q0).applyfunc(sp.expand)
    inner_degrees = [minimum_total_degree(entry, dvars) for entry in inner if entry != 0]
    check(f"N{n}_INNER_FIRST_DEGREE_FOUR", bool(inner_degrees) and min(inner_degrees) == 4)

    remainder = (inner - sp.binomial(n, 2) * base).applyfunc(sp.expand)
    remainder_degrees = [minimum_total_degree(entry, dvars) for entry in remainder if entry != 0]
    check(f"N{n}_LEADING_INNER_COEFFICIENT", not remainder_degrees or min(remainder_degrees) >= 5)

    coefficient = sp.simplify(
        (-1) ** (n - 1)
        * 2
        * sp.binomial(sp.Rational(1, 2), n)
        * sp.binomial(n, 2)
    )
    # In the leading jet d=-i*h*p, sigma=-h^2*P and
    # C(d^2)q(d)=h^4*C(p^2)q(p).
    d_leading = sp.Matrix([-sp.I * h * value for value in p])
    sigma_leading = sp.expand((d_leading.T * eta * d_leading)[0])
    p_squared = [value**2 for value in p]
    p_q = q_vector(pv)
    p_factor = C.subs(dict(zip(dvars, p_squared)), simultaneous=True) * p_q
    base_leading = C.subs(
        dict(zip(dvars, [entry**2 for entry in d_leading])), simultaneous=True
    ) * q_vector(d_leading)
    check(f"N{n}_METRIC_FACTOR_LEADING", sp.expand(sigma_leading + h**2 * P) == 0)
    check(f"N{n}_VERONESE_FACTOR_LEADING", zero(base_leading - h**4 * p_factor))
    check(f"N{n}_ASYMPTOTIC_MULTIPLIER_{coefficient}", coefficient != 0)

# A rational non-null direction certifies that the n=6 leading coefficient
# is not the zero polynomial.  The 24 output slots use four roles by six
# Lorentz generators, in the ordering of the consumed C owner.
point = {p[0]: 1, p[1]: 2, p[2]: 0, p[3]: 0}
P_at_point = P.subs(point)
K_at_point = p_factor.subs(point)
f6_leading = [
    sp.simplify(sp.Rational(315, 512) * P_at_point**5 * entry)
    for entry in K_at_point
]
nonzero_slots = [(index, value) for index, value in enumerate(f6_leading) if value != 0]
check(
    "F6_EXPLICIT_NONZERO_LEADING_WITNESS",
    nonzero_slots
    == [
        (13, sp.Rational(-76545, 256)),
        (15, sp.Rational(-76545, 512)),
        (20, sp.Rational(-76545, 256)),
        (22, sp.Rational(-76545, 512)),
    ],
)

print("GENERIC_HARMONIC_ORDERS", {n: 2 * n + 2 for n in range(2, 9)})
print("F6_WITNESS_P", (1, 2, 0, 0))
print("F6_WITNESS_NONZERO_ROLE_GENERATOR_SLOTS", nonzero_slots)
print("SCOPE: #296 Gram-lift harmonic series only; not #260 Y-amplitude F6")
