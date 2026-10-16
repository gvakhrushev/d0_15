#!/usr/bin/env python3
"""Classify the support-7 fixed-solder main branch.

The three polynomials F0,F2,F3 of degrees 19,25,24 are the exact
denominator-cleared images of the column-2 solder subsystem after x0=-b/a.
Their common zero set meets the open Cayley chart in the empty set:
every eliminant component forces x6^2=4, x0^2=4, or a=0.
"""
from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


data = json.loads(Path(__file__).with_name(
    "a4d_resolved_curved_stationary_e2_support7_solder_reduced4.json"
).read_text())
x0, x3, x4, x6 = sp.symbols("x0 x3 x4 x6")
integer_polys = [
    sp.Poly(sp.sympify(eq["numerator"]), x0, x3, x4, x6).clear_denoms()[1].as_expr()
    for eq in data["equations"]
]
a = sp.expand(sp.diff(integer_polys[1], x0))
b = sp.expand(integer_polys[1].subs(x0, 0))
check("BRANCH_WALL_IDENTITY", sp.expand(b - 2 * a - 2 * x4 * (x6**2 - 4) ** 2) == 0)
check("A_AT_X4_ZERO", sp.expand(a.subs(x4, 0) - 32 * x6**2) == 0)

polynomials = []
for index in (0, 2, 3):
    univariate = sp.Poly(integer_polys[index], x0)
    degree = univariate.degree()
    substituted = sum(
        coefficient * (-b) ** power * a ** (degree - power)
        for (power,), coefficient in univariate.terms()
    )
    polynomials.append(sp.Poly(sp.expand(substituted), x3, x4, x6, domain=sp.ZZ))
check("MAIN_BRANCH_DEGREES", [poly.total_degree() for poly in polynomials] == [19, 25, 24])

Q1 = sp.Poly(
    2 * x4**3 * x6 - 4 * x4**3 + 8 * x4**2 * x6 - x4 * x6**4 + 2 * x4 * x6**3
    + 12 * x4 * x6**2 + 8 * x4 * x6 + 32 * x6**2,
    x4, x6, domain=sp.ZZ,
)
Q2 = sp.Poly(
    4 * x4**3 * x6 - 8 * x4**3 + 16 * x4**2 * x6 - x4 * x6**4 + 4 * x4 * x6**3
    + 16 * x4 * x6**2 + 16 * x4 * x6 + 16 * x4 + 64 * x6**2,
    x4, x6, domain=sp.ZZ,
)
resultant_02 = sp.Poly(sp.expand(sp.resultant(polynomials[0], polynomials[1], x3)), x4, x6)
resultant_03 = sp.Poly(sp.expand(sp.resultant(polynomials[0], polynomials[2], x3)), x4, x6)
eliminant = sp.gcd(resultant_02, resultant_03)
_, factors = sp.factor_list(eliminant.as_expr())
found = {sp.Poly(sp.expand(factor), x4, x6).primitive()[1].as_expr() for factor, _ in factors}
expected = {
    x4,
    x6 - 2,
    x6 + 2,
    Q1.as_expr(),
    Q2.as_expr(),
}
check("ELIMINANT_RADICAL", found == expected)

system = [poly.as_expr() for poly in polynomials]
ideal_q1 = sp.groebner(system + [Q1.as_expr()], x3, x4, x6, order="lex", domain=sp.QQ)
check("Q1_FORCES_CHART_OR_X6_ZERO",
      ideal_q1.reduce(x6**5 * (x6 - 2)**6 * (x6 + 2)**6)[1] == 0)
check("Q1_AT_X6_ZERO_IS_X4_CUBE", sp.factor(Q1.as_expr().subs(x6, 0)) == -4 * x4**3)

ideal_q2 = sp.groebner(system + [Q2.as_expr()], x3, x4, x6, order="lex", domain=sp.QQ)
check("Q2_FORCES_THREE_COMPONENTS",
      ideal_q2.reduce(x6**8 * (x3**2 - 8 * x6) * (x6 - 2)**8 * (x6 + 2)**8)[1] == 0)
check("Q2_AT_X6_ZERO", sp.factor(Q2.as_expr().subs(x6, 0)) == -8 * x4 * (x4**2 - 2))
for sign in (1, -1):
    value = {x3: 0, x6: 0, x4: sign * sp.sqrt(2)}
    ratio = sp.simplify(-b.subs(value) / a.subs(value))
    check(f"X4_SQ2_X6_ZERO_SIGN_{sign}_HITS_X0_TWO", ratio == 2)

curve = sp.Poly(
    x3**8 * x4 - 32 * x3**6 * x4 - 1024 * x3**4 * x4 - 4096 * x3**4
    - 2048 * x3**2 * x4**3 - 8192 * x3**2 * x4**2 - 8192 * x3**2 * x4
    + 32768 * x4**3 - 65536 * x4,
    x3, x4, domain=sp.ZZ,
)
scale = 8**12
numerator_a = sp.expand(a.subs(x6, x3**2 / 8) * scale)
numerator_b = sp.expand(b.subs(x6, x3**2 / 8) * scale)
remainder = sp.reduced(
    sp.expand(numerator_b**2 - 4 * numerator_a**2),
    [curve.as_expr()], x3, x4, domain=sp.QQ,
)[1]
check("CURVE_X3_SQ_EQ_8_X6_HITS_X0_WALL", sp.expand(remainder) == 0)
check("CURVE_DOES_NOT_FORCE_A_ZERO",
      sp.expand(sp.reduced(numerator_a, [curve.as_expr()], x3, x4, domain=sp.QQ)[1]) != 0)

print("MAIN_BRANCH_OPEN_CHART", "empty")
print("ONLY_FIXED_ETA_CHART_SOLUTION", "exceptional origin, already obstructed by the Lorentz defect")
print("STATUS: fixed-solder seven-support gate closed; free solder, full link Euler, and R=R_*(C) remain open")
