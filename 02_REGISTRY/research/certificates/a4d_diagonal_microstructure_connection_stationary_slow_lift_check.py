#!/usr/bin/env python3
"""Connection-stationary slow lift of the #232 microstructure.

The order-h connection Euler on the #241 valued solder is a four-component
forcing. It is solved by a phase-uniform rotation correction on the curved
role-0 edges. After that substitution every order-h metric component vanishes
pointwise. The full link carrier also cancels the next h^2*z*x0 and h^2*z^2
connection coefficients. The substituted metric jet through h^2 is
divisible by z, so both declared scalings z=h and z=h^2 have vanishing
normalized limit.
"""
from __future__ import annotations

from itertools import combinations

import sympy as sp


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
GENERATORS = []
for j in (1, 2, 3):
    matrix = sp.zeros(4)
    matrix[0, j] = matrix[j, 0] = 1
    GENERATORS.append(matrix)
for a, b in ((1, 2), (1, 3), (2, 3)):
    matrix = sp.zeros(4)
    matrix[a, b], matrix[b, a] = 1, -1
    GENERATORS.append(matrix)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for col, (row, sign) in enumerate([(5, -1), (4, 1), (3, -1), (2, 1), (1, -1), (0, 1)]):
    STAR[row, col] = sign
Y = sp.zeros(4)
Y[1, 2], Y[2, 1] = 1, -1
Y[1, 3], Y[3, 1] = -1, 1
Y[2, 3], Y[3, 2] = 1, -1
check("Y_CUBIC", sp.expand(Y**3 + 3 * Y) == sp.zeros(4))
check("STAR_SQUARE_MINUS_ID", STAR * STAR == -sp.eye(6))

z, h, x0, eps = sp.symbols("z h x0 eps")
D = 3 * z**2 + 4
U = sp.simplify((I4 - z * Y / 2).inv() * (I4 + z * Y / 2))
Ui = sp.simplify(ETA * U.T * ETA)
c = sp.together(4 * z / (4 + 3 * z**2))
check("ODD_CURVATURE", sp.simplify((U - Ui) / 2 - c * Y) == sp.zeros(4))
BASE_WAVE = [U, I4, Ui, I4]


def lorentz_inverse(matrix):
    return ETA * matrix.T * ETA


def wedge(left, right):
    return sp.Matrix([left[i] * right[j] - left[j] * right[i] for i, j in PAIRS])


def bivector(matrix):
    dressed = matrix * ETA
    return sp.Matrix([dressed[a, b] for a, b in PAIRS])


def orientation(a, b):
    rest = [j for j in range(4) if j not in (a, b)]
    seq = [a, b] + rest
    return (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))


def shift(site, role, step=1):
    out = list(site)
    out[role] = (out[role] + step) % 4
    return tuple(out)


def phase(site):
    return sum(site) % 4


def edge_euler(site, role, generator, wave, solder):
    result = 0
    for a, b in PAIRS:
        if role == a:
            corners = [(site, 0), (shift(site, b, -1), 2)]
        elif role == b:
            corners = [(shift(site, a, -1), 1), (site, 3)]
        else:
            continue
        for base, corner in corners:
            places = [
                (base, a, False),
                (shift(base, a), b, False),
                (shift(base, b), a, True),
                (base, b, True),
            ]
            factors = []
            for loc, rel, inverted in places:
                link = wave[phase(loc)] if rel == 0 else I4
                factors.append(lorentz_inverse(link) if inverted else link)
            plaquette = factors[0] * factors[1] * factors[2] * factors[3]
            pinv = lorentz_inverse(plaquette)
            varied = list(factors)
            if corner < 2:
                varied[corner] = factors[corner] * generator
            else:
                varied[corner] = -generator * factors[corner]
            dp = varied[0] * varied[1] * varied[2] * varied[3]
            dc = (dp + pinv * dp * pinv) / 2
            u, v = [j for j in range(4) if j not in (a, b)]
            result += orientation(a, b) * (
                wedge(solder[:, u], solder[:, v]).T * G2 * STAR * bivector(dc)
            )[0]
    return result


def edge_euler_full(site, role, generator, waves, solder):
    """Same Euler row with an independent phase/role link on every edge."""
    result = 0
    for a, b in PAIRS:
        if role == a:
            corners = [(site, 0), (shift(site, b, -1), 2)]
        elif role == b:
            corners = [(shift(site, a, -1), 1), (site, 3)]
        else:
            continue
        for base, corner in corners:
            places = [
                (base, a, False),
                (shift(base, a), b, False),
                (shift(base, b), a, True),
                (base, b, True),
            ]
            factors = []
            for loc, rel, inverted in places:
                link = waves[rel][phase(loc)]
                factors.append(lorentz_inverse(link) if inverted else link)
            plaquette = factors[0] * factors[1] * factors[2] * factors[3]
            pinv = lorentz_inverse(plaquette)
            varied = list(factors)
            if corner < 2:
                varied[corner] = factors[corner] * generator
            else:
                varied[corner] = -generator * factors[corner]
            dp = varied[0] * varied[1] * varied[2] * varied[3]
            dc = (dp + pinv * dp * pinv) / 2
            u, v = [j for j in range(4) if j not in (a, b)]
            result += orientation(a, b) * (
                wedge(solder[:, u], solder[:, v]).T * G2 * STAR * bivector(dc)
            )[0]
    return sp.expand(result)


alpha = sp.zeros(4)
alpha[1, 2] = alpha[2, 1] = 1
beta = sp.zeros(4)
beta[0, 1] = beta[1, 0] = 1
solder_h = I4 + h * (alpha * ETA / 2).T
forcing = {}
for p in range(4):
    site = (p, 0, 0, 0)
    for role in range(4):
        for gi, gen in enumerate(GENERATORS):
            value = edge_euler(site, role, gen, BASE_WAVE, solder_h)
            c0 = sp.factor(value.subs(h, 0))
            c1 = sp.factor(sp.diff(value, h).subs(h, 0))
            check(f"FLAT_EK_{p}_{role}_{gi}", c0 == 0)
            if c1 != 0:
                forcing[(p, role, gi)] = c1
expected_forcing = {
    (1, 0, 0): 2 * z / D,
    (1, 0, 1): -2 * z / D,
    (3, 0, 0): -2 * z / D,
    (3, 0, 1): 2 * z / D,
}
check("ORDER_H_FORCING_SUPPORT", forcing == expected_forcing)


def jacobian_column(vary_phase, vary_gen):
    wave = list(BASE_WAVE)
    wave[vary_phase] = sp.simplify(BASE_WAVE[vary_phase] * (I4 + eps * GENERATORS[vary_gen]))
    column = []
    for p in range(4):
        site = (p, 0, 0, 0)
        for role in range(4):
            for gen in GENERATORS:
                value = edge_euler(site, role, gen, wave, I4)
                column.append(sp.factor(sp.diff(value, eps).subs(eps, 0)))
    return column


modes = [(0, 3), (0, 5), (2, 3), (2, 4)]
columns = [jacobian_column(phase_index, gen_index) for phase_index, gen_index in modes]
operator = sp.Matrix(columns).T
rhs = sp.zeros(96, 1)
labels = [(p, r, g) for p in range(4) for r in range(4) for g in range(6)]
for key, value in expected_forcing.items():
    rhs[labels.index(key)] = value
solution, parameters = operator.gauss_jordan_solve(-rhs)
solution = solution.subs({parameter: 0 for parameter in parameters})
expected_solution = sp.Matrix([
    -z * (z + 2) / D,
    -2 * z**2 / D,
    z * (z + 2) / D,
    -2 * z**2 / D,
])
check("LIFT_SOLUTION", sp.simplify(solution - expected_solution) == sp.zeros(4, 1))
check("LIFT_RESIDUAL", sp.simplify(operator * solution + rhs) == sp.zeros(96, 1))

# Corrected links through the quadratic exponential, and the full slow solder.
corr0 = solution[0] * GENERATORS[3] + solution[1] * GENERATORS[5]
corr2 = solution[2] * GENERATORS[3] + solution[3] * GENERATORS[4]


def corrected(link, correction):
    return sp.simplify(link * (I4 + h * correction + h**2 * (correction * correction) / 2))


wave = [corrected(U, corr0), I4, corrected(Ui, corr2), I4]
solder = I4 + h * (alpha * ETA / 2).T + h**2 * x0 * (beta * ETA / 2).T
SIGMA = (1, 1, -1, -1)


def metric_series(site):
    series_values = []
    for row, col in SYM:
        direction = sp.zeros(4)
        direction[row, col] = direction[col, row] = 1
        variation = direction * ETA / 2
        total = 0
        for a, b in PAIRS:
            places = [
                (site, a, False),
                (shift(site, a), b, False),
                (shift(site, b), a, True),
                (site, b, True),
            ]
            factors = []
            for loc, rel, inverted in places:
                link = wave[phase(loc)] if rel == 0 else I4
                factors.append(lorentz_inverse(link) if inverted else link)
            holonomy = factors[0] * factors[1] * factors[2] * factors[3]
            curvature = (holonomy - lorentz_inverse(holonomy)) / 2
            u, v = [j for j in range(4) if j not in (a, b)]
            dw = wedge(variation[u, :].T, solder[:, v]) + wedge(solder[:, u], variation[v, :].T)
            total += orientation(a, b) * (dw.T * G2 * STAR * bivector(curvature))[0]
        series_values.append(sp.series(sp.together(total), h, 0, 3).removeO())
    return series_values


for p, sign in enumerate(SIGMA):
    comps = metric_series((p, 0, 0, 0))
    low = [sp.simplify(sp.together(sp.series(comp, h, 0, 2).removeO())) for comp in comps]
    check(f"PHASE_{p}_ORDER_H_CANCELLED", all(term == 0 for term in low))
    expected = [
        0,
        -sign * h**2 * z**2 * (z - 2) / (2 * D**2),
        sign * h**2 * z**2 * (z - 2) / (2 * D**2),
        0,
        0,
        -sign * h**2 * x0 * z / D,
        sign * h**2 * x0 * z / D,
        -sign * h**2 * x0 * z / D,
        0,
        sign * h**2 * x0 * z / D,
    ]
    check(
        f"PHASE_{p}_ORDER_H2",
        all(
            sp.simplify(sp.together(
                sp.sympify(got).coeff(h, 2) - sp.sympify(want).coeff(h, 2)
            )) == 0
            for got, want in zip(comps, expected)
        ),
    )

for scaling in (h, h**2):
    normalized = sp.series(
        (-h**2 * z**2 * (z - 2) / (2 * D**2)).subs(z, scaling) / h**2,
        h, 0, 2,
    ).removeO()
    slope = sp.series((h**2 * x0 * z / D).subs(z, scaling) / h**2, h, 0, 1).removeO()
    check(f"NORMALIZED_LIMIT_{scaling}", normalized == 0 and slope == 0)

# The remaining h^2*z slope term is not in the four lift modes above.  Solve
# its exact coefficient on the complete 4 phases x 4 roles x 6 Lorentz-link
# carrier, then replay the corrected coefficient in every connection row.
full_rows = [(p, r, gi) for p in range(4) for r in range(4) for gi in range(6)]
epsilon_full = sp.symbols("epsilon_full")
identity_links = [[I4 for _ in range(4)] for _ in range(4)]
full_columns = []
for vp, vr, vg in full_rows:
    links = [list(row) for row in identity_links]
    links[vr][vp] = I4 + epsilon_full * GENERATORS[vg]
    column = []
    for p, r, gi in full_rows:
        value = edge_euler_full(
            (p, 0, 0, 0), r, GENERATORS[gi], links, I4
        )
        column.append(sp.diff(value, epsilon_full).subs(epsilon_full, 0))
    full_columns.append(column)
full_jacobian = sp.Matrix(full_columns).T

alpha_probe = [I4 for _ in range(4)]
alpha_probe[0] = I4 + z * Y - h * z * GENERATORS[3] / 2
alpha_probe[2] = I4 - z * Y + h * z * GENERATORS[3] / 2
beta_slope = sp.zeros(4)
beta_slope[0, 1] = beta_slope[1, 0] = 1
probe_solder = (
    I4
    + h * (alpha * ETA / 2).T
    + h**2 * x0 * (beta_slope * ETA / 2).T
)
slope_source = sp.Matrix([
    sp.Poly(
        edge_euler_full(
            (p, 0, 0, 0), r, GENERATORS[gi],
            [[alpha_probe[phase] if role == 0 else I4 for phase in range(4)]
             for role in range(4)],
            probe_solder,
        ),
        h, z, x0,
    ).coeff_monomial(h**2 * z * x0)
    for p, r, gi in full_rows
])
check(
    "FULL_ORDER_H2_Z_SLOPE_SUPPORT",
    slope_source == sp.Matrix([
        -sp.Rational(1, 2) if row == (1, 0, 3) else
        sp.Rational(1, 2) if row == (1, 0, 4) else
        1 if row == (1, 0, 5) else
        sp.Rational(1, 2) if row == (3, 0, 3) else
        -sp.Rational(1, 2) if row == (3, 0, 4) else
        -1 if row == (3, 0, 5) else 0
        for row in full_rows
    ]),
)

four_mode_jacobian = operator.subs(z, 0)
four_mode_rank = sp.polys.matrices.DomainMatrix.from_Matrix(
    four_mode_jacobian
).rank()
four_mode_augmented_rank = sp.polys.matrices.DomainMatrix.from_Matrix(
    four_mode_jacobian.row_join(-slope_source)
).rank()
check(
    "SLOPE_NEEDS_FULL_LINK_CARRIER",
    four_mode_augmented_rank > four_mode_rank,
)

full_augmented = full_jacobian.row_join(-slope_source)
full_rref, full_pivots = sp.polys.matrices.DomainMatrix.from_Matrix(
    full_augmented
).rref()
check(
    "FULL_96_ROW_SLOPE_COMPATIBILITY",
    len(full_pivots) == 80 and 96 not in full_pivots,
)
full_rref_matrix = full_rref.to_Matrix()
second_order_solution = sp.zeros(96, 1)
for row_index, pivot in enumerate(full_pivots):
    if pivot < 96:
        second_order_solution[pivot] = full_rref_matrix[row_index, 96]
check(
    "FULL_96_ROW_SECOND_ORDER_LINK_CORRECTION",
    sp.simplify(full_jacobian * second_order_solution + slope_source)
    == sp.zeros(96, 1),
)

corrected_links = [[I4 for _ in range(4)] for _ in range(4)]
corrected_links[0] = list(alpha_probe)
for (p, r, gi), coefficient in zip(full_rows, second_order_solution):
    corrected_links[r][p] += h**2 * z * x0 * coefficient * GENERATORS[gi]
all_roles_wave = corrected_links
check(
    "FULL_96_ROW_CORRECTED_H2_Z_SLOPE_ZERO",
    all(
        sp.Poly(
            edge_euler_full(
                (p, 0, 0, 0), r, GENERATORS[gi], all_roles_wave,
                probe_solder,
            ),
            h, z, x0,
        ).coeff_monomial(h**2 * z * x0) == 0
        for p, r, gi in full_rows
    ),
)

# The curvature-only h^2*z^2 coefficient is independent of the x0 slope.
# Reinsert the complete rational first-order lift (not only its O(z) germ),
# then solve this next coefficient on the same full link carrier.
full_order_h_lift = [
    corrected(U, corr0), I4, corrected(Ui, corr2), I4
]
full_order_h_links = [
    [full_order_h_lift[p] if r == 0 else I4 for p in range(4)]
    for r in range(4)
]
metric_solder = I4 + h * (alpha * ETA / 2).T


def coefficient_h2_z2(value):
    h2 = sp.diff(value, h, 2).subs(h, 0) / 2
    return sp.series(sp.cancel(h2), z, 0, 3).removeO().coeff(z, 2)


curvature_source = sp.Matrix([
    coefficient_h2_z2(edge_euler_full(
        (p, 0, 0, 0), r, GENERATORS[gi], full_order_h_links,
        metric_solder,
    ))
    for p, r, gi in full_rows
])
check(
    "FULL_ORDER_H2_Z2_CURVATURE_SOURCE",
    curvature_source == sp.Matrix([
        -sp.Rational(1, 8) if row == (1, 0, 0) else
        sp.Rational(1, 8) if row == (1, 0, 1) else
        sp.Rational(1, 8) if row == (3, 0, 0) else
        -sp.Rational(1, 8) if row == (3, 0, 1) else 0
        for row in full_rows
    ]),
)
curvature_augmented = full_jacobian.row_join(-curvature_source)
curvature_rref, curvature_pivots = sp.polys.matrices.DomainMatrix.from_Matrix(
    curvature_augmented
).rref()
check(
    "FULL_96_ROW_H2_Z2_CURVATURE_COMPATIBILITY",
    len(curvature_pivots) == 80 and 96 not in curvature_pivots,
)
curvature_rref_matrix = curvature_rref.to_Matrix()
curvature_solution = sp.zeros(96, 1)
for row_index, pivot in enumerate(curvature_pivots):
    if pivot < 96:
        curvature_solution[pivot] = curvature_rref_matrix[row_index, 96]
check(
    "FULL_96_ROW_H2_Z2_CURVATURE_LINK_CORRECTION",
    sp.simplify(full_jacobian * curvature_solution + curvature_source)
    == sp.zeros(96, 1),
)
check(
    "H2_Z2_CORRECTION_IS_TWO_PHASE_J12",
    curvature_solution == sp.Matrix([
        sp.Rational(1, 8) if row == (0, 0, 3) else
        -sp.Rational(1, 8) if row == (2, 0, 3) else 0
        for row in full_rows
    ]),
)
curvature_corrected_links = [list(row) for row in full_order_h_links]
for (p, r, gi), coefficient in zip(full_rows, curvature_solution):
    curvature_corrected_links[r][p] += h**2 * z**2 * coefficient * GENERATORS[gi]
check(
    "FULL_96_ROW_CORRECTED_H2_Z2_CURVATURE_ZERO",
    all(
        coefficient_h2_z2(edge_euler_full(
            (p, 0, 0, 0), r, GENERATORS[gi],
            curvature_corrected_links, metric_solder,
        )) == 0
        for p, r, gi in full_rows
    ),
)

# At z=0 the order-h lift vanishes with z, and the identity-link Euler is zero
# through h^2 for every phase, role and generator.
for p in range(4):
    site = (p, 0, 0, 0)
    for role in range(4):
        for gi, gen in enumerate(GENERATORS):
            value = edge_euler(site, role, gen, [I4, I4, I4, I4], solder.subs(z, 0))
            check(
                f"FLAT_LIMIT_EK_{p}_{role}_{gi}",
                sp.series(sp.expand(value), h, 0, 3).removeO() == 0,
            )

print("LIFT", [str(sp.factor(s)) for s in solution])
print("TERMINAL", "J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-CANCELS")
