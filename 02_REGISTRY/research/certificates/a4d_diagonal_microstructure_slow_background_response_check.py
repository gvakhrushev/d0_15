#!/usr/bin/env python3
"""Slow-background metric partial of the period-4 diagonal Y-microstructure.

The connection is the #232 family. The metric partial is the owned #201 lift:
rows of H(q) = q eta / 2 are the solder-leg variations, and
DQ_flat[H(q)] = q. Curvature is placed only on the faces (0, s). Spatial
plaquettes of this family are flat.

Two slow profiles are expanded through h^2. The constant piece of a slow
field is not the whole test: every profile below changes between x0 and
x0+1. The identity connection is the comparator, so Delta E_Q = E_Q(Q_h, K).
"""
from __future__ import annotations

from itertools import combinations

import sympy as sp


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


PAIRS = list(combinations(range(4), 2))
PINDEX = {pair: index for index, pair in enumerate(PAIRS)}
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
SYM = [(a, b) for a in range(4) for b in range(a, 4)]


def rot(i: int, j: int) -> sp.Matrix:
    matrix = sp.zeros(4)
    matrix[i, j] = 1
    matrix[j, i] = -1
    return matrix


def orient(i: int, j: int) -> int:
    rest = [k for k in range(4) if k not in (i, j)]
    seq = [i, j] + rest
    inversions = sum(seq[p] > seq[q] for p, q in combinations(range(4), 2))
    return -1 if inversions % 2 else 1


def wedge(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([left[a] * right[b] - left[b] * right[a] for a, b in PAIRS])


def bivector(tangent: sp.Matrix) -> sp.Matrix:
    dressed = tangent * ETA
    return sp.Matrix([dressed[a, b] for a, b in PAIRS])


Y = rot(1, 2) - rot(1, 3) + rot(2, 3)
check("Y_CUBIC", sp.expand(Y**3 + 3 * Y) == sp.zeros(4))
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = sp.zeros(6)
for src, (dst, sign) in {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}.items():
    STAR[PINDEX[dst], PINDEX[src]] = sign
check("STAR_SQUARE_MINUS_ID", STAR * STAR == -sp.eye(6))

z = sp.symbols("z")
U = sp.simplify((I4 - z * Y / 2).inv() * (I4 + z * Y / 2))
Ui = sp.simplify(U.subs(z, -z))
c = sp.together(4 * z / (4 + 3 * z**2))
check("ODD_CURVATURE", sp.simplify((U - Ui) / 2 - c * Y) == sp.zeros(4))
W = [U, I4, Ui, I4]
Winv = [Ui, I4, U, I4]
phase_curvature = []
for phase in range(4):
    plaquette = sp.simplify(W[phase] * Winv[(phase + 1) % 4])
    phase_curvature.append(sp.simplify((plaquette - plaquette.inv()) / 2))
expected_signs = (1, 1, -1, -1)
for phase, sign in enumerate(expected_signs):
    check(
        f"PHASE_{phase}_CURVATURE",
        sp.simplify(phase_curvature[phase] - sign * c * Y) == sp.zeros(4),
    )


def gram_lift(q: sp.Matrix) -> sp.Matrix:
    return q * ETA / 2


def metric_partial(legs, curvature_scale):
    response = G2 * STAR * bivector(curvature_scale * Y)
    values = []
    for qa, qb in SYM:
        direction = sp.zeros(4)
        direction[qa, qb] = direction[qb, qa] = 1
        variation = gram_lift(direction)
        total = 0
        for a, b in PAIRS:
            if 0 not in (a, b):
                continue
            u, v = [j for j in range(4) if j not in (a, b)]
            dw = wedge(variation[u, :].T, legs[v]) + wedge(legs[u], variation[v, :].T)
            total += orient(a, b) * (dw.T * response)[0]
        values.append(sp.expand(total))
    return sp.Matrix(values)


flat_legs = [I4[:, i] for i in range(4)]
check("FLAT_CONTROL_TEN", metric_partial(flat_legs, 1) == sp.zeros(10, 1))
check(
    "GRAM_LIFT_REPRODUCES_Q",
    all(
        sp.expand(gram_lift(direction) * ETA + ETA * gram_lift(direction).T - direction)
        == sp.zeros(4)
        for direction in (
            sp.eye(4),
            sp.Matrix([[0, 1, 0, 0], [1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
        )
    ),
)

h, x0 = sp.symbols("h x0")
alpha = sp.zeros(4)
alpha[1, 2] = alpha[2, 1] = 1
beta = sp.zeros(4)
beta[0, 1] = beta[1, 0] = 1
# Q = eta + h (alpha + h x0 beta). Neighbors differ by h^2 beta.
shift_value = [gram_lift(alpha)[i, :].T for i in range(4)]
shift_slope = [gram_lift(beta)[i, :].T for i in range(4)]
legs_valued = [
    flat_legs[i] + h * shift_value[i] + (h**2) * x0 * shift_slope[i] for i in range(4)
]
unit = metric_partial(legs_valued, 1)
check("VALUED_PROFILE_NO_H0", all(component.coeff(h, 0) == 0 for component in unit))
h1 = sp.Matrix([sp.factor(component.coeff(h, 1)) for component in unit])
h2 = sp.Matrix([sp.factor(component.coeff(h, 2)) for component in unit])
check("VALUED_PROFILE_H1", h1 == sp.Matrix([0, -sp.Rational(1, 4), sp.Rational(1, 4), 0, 0, 0, 0, 0, 0, 0]))
check(
    "VALUED_PROFILE_H2_SEES_NEIGHBOR_SLOPE",
    h2 == x0 * sp.Matrix([0, 0, 0, 0, 0, -sp.Rational(1, 4), sp.Rational(1, 4), -sp.Rational(1, 4), 0, sp.Rational(1, 4)]),
)

# Pure slow gradient: no constant value. Q = eta + h^2 x0 beta.
legs_gradient = [flat_legs[i] + (h**2) * x0 * shift_slope[i] for i in range(4)]
gradient_unit = metric_partial(legs_gradient, 1)
check("PURE_GRADIENT_NO_H1", all(component.coeff(h, 1) == 0 for component in gradient_unit))
check(
    "PURE_GRADIENT_H2",
    sp.Matrix([sp.factor(component.coeff(h, 2)) for component in gradient_unit])
    == x0 * sp.Matrix([0, 0, 0, 0, 0, -sp.Rational(1, 4), sp.Rational(1, 4), -sp.Rational(1, 4), 0, sp.Rational(1, 4)]),
)

def component(index: int, sign: int, scale) -> sp.Expr:
    return sp.factor(sign * c.subs(z, scale) * unit[index])


# Pointwise leading component (0,1), valued slow profile.
leading = sp.Matrix([
    sp.factor(sign * c * h1[1]) for sign in expected_signs
])
check(
    "POINTWISE_H1_Z_COEFFICIENT",
    leading == sp.Matrix([
        -sign * z / (4 + 3 * z**2) for sign in expected_signs
    ]),
)
check("PHASE_AVERAGE_OF_H1_IS_ZERO", sp.factor(sum(leading)) == 0)
check("IDENTITY_CONNECTION_PARTIAL_ZERO", metric_partial(legs_valued, 0) == sp.zeros(10, 1))

for scaling, name in ((h, "Z_EQ_H"), (h**2, "Z_EQ_H2")):
    raw = sp.factor(component(1, 1, scaling))
    normalized = sp.factor(raw / h**2)
    limit = sp.limit(normalized, h, 0)
    print(f"SCALING_{name}_PHASE0_COMPONENT_01_RAW", raw)
    print(f"SCALING_{name}_PHASE0_COMPONENT_01_NORMALIZED_LIMIT", limit)
    if name == "Z_EQ_H":
        check("Z_EQ_H_NORMALIZED_LIMIT", limit == -sp.Rational(1, 4))
    else:
        check("Z_EQ_H2_NORMALIZED_LIMIT", limit == 0)

gradient_raw = sp.factor(c * gradient_unit[5])
for scaling, name, expected in (
    (h, "GRADIENT_Z_EQ_H", 0),
    (h**2, "GRADIENT_Z_EQ_H2", 0),
):
    normalized = sp.factor(gradient_raw.subs(z, scaling) / h**2)
    check(f"{name}_NORMALIZED_LIMIT", sp.limit(normalized, h, 0) == expected)

print("LEADING_MONOMIAL", "h^1 z^1")
print("COMPONENT_01_COEFFICIENT", "-sigma(p) / (4 + 3 z^2) * z, exact before scaling")
print("TERMINAL", "J2-DIAGONAL-MICROSTRUCTURE-EINSTEIN-RESPONSE-OBSTRUCTION-FOUND")
