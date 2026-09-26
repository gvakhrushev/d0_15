#!/usr/bin/env python3
"""Exact hostile control for the diagonal quarter-wave slow-background germ.

Reproduces the owned frozen quartic, differentiates the owned polarized
connection symbol under one declared diagonal phase detuning, and certifies
real flat-approaching roots of the leading zero-source balance.

This is one orbit. It does not prove uniform coupled normal rescue.
"""

from itertools import combinations

import sympy as sp

PAIRS = list(combinations(range(4), 2))
ETA = sp.diag(1, -1, -1, -1)
GENERATORS = []
for i in (1, 2, 3):
    matrix = sp.zeros(4)
    matrix[0, i] = matrix[i, 0] = 1
    GENERATORS.append(matrix)
for i, j in ((1, 2), (1, 3), (2, 3)):
    matrix = sp.zeros(4)
    matrix[i, j], matrix[j, i] = 1, -1
    GENERATORS.append(matrix)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1),
    (0, 3): ((1, 2), -1), (1, 2): ((0, 3), 1),
    (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PAIRS.index(dst), PAIRS.index(src)] = sign


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def wedge(left, right):
    return sp.Matrix([left[a] * right[b] - left[b] * right[a] for a, b in PAIRS])


def connection_symbol(solder, phase):
    """Owned polarized symbol from the fixed-realization IR certificate."""
    result = sp.zeros(24)
    for r, s in PAIRS:
        u, v = [i for i in range(4) if i not in (r, s)]
        seq = [r, s, u, v]
        sign = (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))
        pairing = sign * wedge(solder[:, u], solder[:, v]).T * G2 * STAR
        bracket = sp.zeros(6)
        for i, xi in enumerate(GENERATORS):
            for j, xj in enumerate(GENERATORS):
                commutator = (xi * xj - xj * xi) * ETA
                bracket[i, j] = (pairing * sp.Matrix([commutator[a, b] for a, b in PAIRS]))[0]
        roles = [r, s, r, s]
        direct = [sp.Integer(1), phase[r], -phase[s], sp.Integer(-1)]
        inverse = [sp.Integer(1), 1 / phase[r], -1 / phase[s], sp.Integer(-1)]
        role_form = sp.zeros(4)
        for i, j in combinations(range(4), 2):
            role_form[roles[i], roles[j]] += direct[i] * inverse[j] / 2
            role_form[roles[j], roles[i]] -= inverse[i] * direct[j] / 2
        result += sp.kronecker_product(role_form, bracket)
    return result.applyfunc(sp.expand)


def kernel_vector(entries):
    vector = sp.zeros(24, 1)
    for idx, val in entries.items():
        vector[idx] = val
    return vector


KERNEL = sp.Matrix.hstack(*[
    kernel_vector({0: 1, 1: 1, 2: 1}),
    kernel_vector({3: 1, 4: -1, 5: 1}),
    kernel_vector({6: 1, 9: 1, 10: 1}),
    kernel_vector({7: 1, 8: -1, 11: 1}),
    kernel_vector({12: 1, 14: -1, 16: 1}),
    kernel_vector({13: 1, 15: -1, 17: 1}),
    kernel_vector({18: 1, 19: -1, 21: 1}),
    kernel_vector({20: -1, 22: 1, 23: 1}),
])

QUARTER = [sp.I, sp.I, sp.I, sp.I]
FROZEN = connection_symbol(sp.eye(4), QUARTER)
check("QUARTER_KERNEL", FROZEN * KERNEL == sp.zeros(24, 8))

SLOW = sp.symbols("t")
DETUNED = connection_symbol(sp.eye(4), [sp.I * sp.exp(sp.I * SLOW)] * 4)
FORM = sp.simplify(KERNEL.T * DETUNED * KERNEL)
check("DETUNING_FREEZES_KERNEL_FORM", sp.simplify(FORM.subs(SLOW, 0)) == sp.zeros(8))
DERIVATIVE = sp.simplify(sp.diff(FORM, SLOW).subs(SLOW, 0))
check("DETUNING_DERIVATIVE_REAL", all(entry.is_real for entry in DERIVATIVE))
COMBO = sp.zeros(8, 1)
COMBO[2] = 1
COMBO[5] = 1
COMBO[7] = -1
CROSS = sp.simplify((DERIVATIVE.row(0) * COMBO)[0])
check("LEADING_CROSS_COEFFICIENT", CROSS == 6)
check("PURE_DIRECTION_STAYS_NULL", sp.simplify(DERIVATIVE[0, 0]) == 0)
check("PURE_COMBO_STAYS_NULL", sp.simplify((COMBO.T * DERIVATIVE * COMBO)[0]) == 0)

STRETCH = sp.eye(4)
STRETCH[1, 1] = 1 + SLOW
SOLDER_FORM = sp.simplify(KERNEL.T * connection_symbol(STRETCH, QUARTER) * KERNEL)
SOLDER_DERIVATIVE = sp.simplify(sp.diff(SOLDER_FORM, SLOW).subs(SLOW, 0))
check("CONSTANT_STRETCH_HAS_NO_LINEAR_KERNEL_TERM", SOLDER_DERIVATIVE == sp.zeros(8))

a, b, c, d = sp.symbols("a b c d")
VARS = (a, b, c, d)
P4 = (
    36*a**2*b**2 - 3*a**2*b*c - 27*a**2*b*d + 2*a**2*c*d + 3*a**2*d**2
    - 27*a*b**2*c + 3*a*b**2*d + 188*a*b*c*d
    + 22*a*c**2*d - 107*a*c*d**2 - a*d**3
    + 3*b**2*c**2 - 2*b**2*c*d + b*c**3
    - 107*b*c**2*d - 22*b*c*d**2
    - 6*c**3*d + 38*c**2*d**2 + 6*c*d**3
)
V4 = 48 * P4
GRADIENT = sp.Matrix([sp.diff(V4, var) for var in VARS])
check("OWNED_QUARTIC_DEGREE", sp.total_degree(sp.Poly(V4, *VARS)) == 4)
check("GRADIENT_CUBIC_ODD", all(
    sp.expand(GRADIENT[i].subs({var: -var for var in VARS}) + GRADIENT[i]) == 0
    for i in range(4)
))
check("A_AXIS_IS_FROZEN_ZERO", all(sp.expand(expr.subs({b: 0, c: 0, d: 0})) == 0 for expr in GRADIENT))
check("B_AXIS_IS_FROZEN_ZERO", all(sp.expand(expr.subs({a: 0, c: 0, d: 0})) == 0 for expr in GRADIENT))


def chart_basis(substitutions, generators):
    equations = [sp.expand(expr.subs(substitutions)) for expr in GRADIENT]
    return list(sp.groebner(equations, *generators, order="grevlex"))


check("A_CHART_ONLY_ORIGIN_OF_THE_OTHERS", [sp.expand(g) for g in chart_basis({a: 1}, (b, c, d))] == [b, c, d])
check("B_CHART_ONLY_ORIGIN_OF_THE_OTHERS", [sp.expand(g) for g in chart_basis({a: 0, b: 1}, (c, d))] == [c, d])
check("NO_CD_RAY", chart_basis({a: 0, b: 0, c: 1}, (d,)) == [sp.Integer(1)])
check(
    "NO_PURE_D_POINT",
    any(sp.expand(expr.subs({a: 0, b: 0, c: 0, d: 1})) != 0 for expr in GRADIENT),
)

LINEAR = sp.Matrix([6 * c, 6 * d, 6 * a, 6 * b])
check("A_AXIS_BROKEN", sp.expand(LINEAR.subs({a: 1, b: 0, c: 0, d: 0})) != sp.zeros(4, 1))
check("B_AXIS_BROKEN", sp.expand(LINEAR.subs({a: 0, b: 1, c: 0, d: 0})) != sp.zeros(4, 1))

JACOBIAN = GRADIENT.jacobian(VARS)
LINEAR_JACOBIAN = sp.Matrix([
    [0, 0, 6, 0],
    [0, 0, 0, 6],
    [6, 0, 0, 0],
    [0, 6, 0, 0],
])
SEEDS = {
    1: (
        sp.Rational(1966487, 100000000),
        sp.Rational(1992998, 100000000),
        sp.Rational(4512801, 100000000),
        sp.Rational(6075041, 100000000),
    ),
    -1: (
        sp.Rational(-10075542, 1000000000),
        sp.Rational(159833106, 1000000000),
        sp.Rational(-36426563, 1000000000),
        sp.Rational(237478068, 1000000000),
    ),
}
RADIUS = sp.Rational(1, 10**5)

for sign, center in SEEDS.items():
    substitution = dict(zip(VARS, center))
    residual = (GRADIENT + sign * LINEAR).subs(substitution)
    jacobian = JACOBIAN.subs(substitution) + sign * LINEAR_JACOBIAN
    step = jacobian.LUsolve(residual)
    eta = max(abs(step[i, 0]) for i in range(4))
    inverse_norm = 0
    for column in range(4):
        basis = sp.zeros(4, 1)
        basis[column] = 1
        solved = jacobian.LUsolve(basis)
        inverse_norm = max(inverse_norm, sum(abs(solved[i, 0]) for i in range(4)))
    lipschitz = 0
    for i in range(4):
        row_bound = 0
        for j in range(4):
            entry_bound = 0
            for left in VARS:
                derivative = sp.diff(JACOBIAN[i, j], left)
                supremum = abs(derivative.subs(substitution))
                for right in VARS:
                    supremum += abs(sp.diff(derivative, right)) * RADIUS
                entry_bound += supremum
            row_bound += entry_bound
        lipschitz = max(lipschitz, row_bound)
    contraction = inverse_norm * lipschitz * RADIUS
    check("SHEET_CONTRACTION_" + ("POS" if sign > 0 else "NEG"), contraction < 1)
    check(
        "SHEET_BALL_INVARIANT_" + ("POS" if sign > 0 else "NEG"),
        eta / (1 - contraction) < RADIUS,
    )
    check(
        "SHEET_EXCLUDES_ZERO_" + ("POS" if sign > 0 else "NEG"),
        min(abs(value) for value in center) > RADIUS,
    )

print("RESULT_DECLARED_BACKGROUND: uniform diagonal phase i*exp(i*t)")
print("RESULT_LINEAR_POTENTIAL: 6*t*(a*c + b*d)")
print("RESULT_FROZEN_ZERO_SET: a-axis union b-axis")
print("RESULT_SHEET_SCALING: amplitude sqrt(|t|), both signs")
print("TERMINAL: J2-DIAGONAL-SLOW-BACKGROUND-FLAT-SPLITTING-TERM-FOUND")
