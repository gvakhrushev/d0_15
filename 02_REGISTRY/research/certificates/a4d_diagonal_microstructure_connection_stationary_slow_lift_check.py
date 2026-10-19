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

# The next mixed slow coefficient is a joint connection/metric compatibility
# problem, not merely a connection range solve.  Keep the complete 96-link
# carrier and all ten symmetric metric probes.  The amplitude variable z is
# linearized at z=0, so this is the exact coefficient of the original Cayley
# family, not a finite-z approximation.
def metric_euler_full(site, row, col, waves, solder):
    direction = sp.zeros(4)
    direction[row, col] = direction[col, row] = 1
    variation = direction * ETA / 2
    result = 0
    for a, b in PAIRS:
        places = [
            (site, a, False),
            (shift(site, a), b, False),
            (shift(site, b), a, True),
            (site, b, True),
        ]
        factors = []
        for loc, rel, inverted in places:
            link = waves[rel][phase(loc)]
            factors.append(lorentz_inverse(link) if inverted else link)
        holonomy = factors[0] * factors[1] * factors[2] * factors[3]
        curvature = (holonomy - lorentz_inverse(holonomy)) / 2
        u, v = [j for j in range(4) if j not in (a, b)]
        dw = wedge(variation[u, :].T, solder[:, v]) + wedge(
            solder[:, u], variation[v, :].T
        )
        result += orientation(a, b) * (
            dw.T * G2 * STAR * bivector(curvature)
        )[0]
    return sp.expand(result)


def metric_euler_z1(site, row, col, tangents, solder):
    """Exact first-amplitude coefficient, evaluated without higher powers."""
    direction = sp.zeros(4)
    direction[row, col] = direction[col, row] = 1
    variation = direction * ETA / 2
    result = 0
    for a, b in PAIRS:
        places = [
            (site, a, False),
            (shift(site, a), b, False),
            (shift(site, b), a, True),
            (site, b, True),
        ]
        p1 = sp.zeros(4)
        for loc, rel, inverted in places:
            tangent = tangents[rel][phase(loc)]
            p1 += lorentz_inverse(tangent) if inverted else tangent
        curvature1 = (p1 - lorentz_inverse(p1)) / 2
        u, v = [j for j in range(4) if j not in (a, b)]
        dw = wedge(variation[u, :].T, solder[:, v]) + wedge(
            solder[:, u], variation[v, :].T
        )
        result += orientation(a, b) * (
            dw.T * G2 * STAR * bivector(curvature1)
        )[0]
    return sp.expand(result)


def connection_euler_z1(site, role, generator, tangents, solder):
    """Exact first-amplitude coefficient of the original link Euler rows."""
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
            d_factors = []
            for loc, rel, inverted in places:
                tangent = tangents[rel][phase(loc)]
                d_factors.append(lorentz_inverse(tangent) if inverted else tangent)
            p1 = sum(d_factors, sp.zeros(4))
            dp0 = generator if corner < 2 else -generator
            dp1 = sp.zeros(4)
            for j, derivative in enumerate(d_factors):
                if j == corner:
                    derivative = (
                        derivative * generator
                        if corner < 2
                        else -generator * derivative
                    )
                    dp1 += derivative
                elif j < corner:
                    dp1 += derivative * dp0
                else:
                    dp1 += dp0 * derivative
            pinv1 = lorentz_inverse(p1)
            dc1 = dp1 + (pinv1 * dp0 + dp0 * pinv1) / 2
            u, v = [j for j in range(4) if j not in (a, b)]
            result += orientation(a, b) * (
                wedge(solder[:, u], solder[:, v]).T
                * G2 * STAR * bivector(dc1)
            )[0]
    return sp.expand(result)


first_lift_probe = [I4 for _ in range(4)]
first_lift_probe[0] = I4 + z * Y - h * z * GENERATORS[3] / 2
first_lift_probe[2] = I4 - z * Y + h * z * GENERATORS[3] / 2
probe_waves = [
    [first_lift_probe[p] if role == 0 else I4 for p in range(4)]
    for role in range(4)
]
probe_solder = (
    I4
    + h * (alpha * ETA / 2).T
    + h**2 * x0 * (beta * ETA / 2).T
)
probe_tangents = [
    [
        sp.diff(first_lift_probe[p], z).subs(z, 0) if role == 0 else sp.zeros(4)
        for p in range(4)
    ]
    for role in range(4)
]

metric_base_full = sp.Matrix([
    sp.Poly(
        metric_euler_full((p, 0, 0, 0), row, col, probe_waves, probe_solder),
        h, z, x0,
    ).coeff_monomial(h**2 * z * x0)
    for p in range(4)
    for row, col in SYM
])
metric_base = sp.Matrix([
    sp.Poly(
        metric_euler_z1((p, 0, 0, 0), row, col, probe_tangents, probe_solder),
        h, x0,
    ).coeff_monomial(h**2 * x0)
    for p in range(4)
    for row, col in SYM
])
check("ALL_40_METRIC_Z1_FORMULAS_MATCH_FULL_PLAQUETTE", metric_base == metric_base_full)
connection_base_check = sp.Matrix([
    sp.Poly(
        connection_euler_z1((p, 0, 0, 0), role, GENERATORS[gi], probe_tangents, probe_solder),
        h, x0,
    ).coeff_monomial(h**2 * x0)
    for p, role, gi in full_rows
])
check("ALL_96_CONNECTION_Z1_FORMULAS_MATCH_FULL_PLAQUETTE", connection_base_check == slope_source)

# Metric response to an arbitrary h^2*z*x0 link correction at the flat point.
# Variables use exactly the phase-role-generator order of full_jacobian.
b_symbols = sp.symbols("b0:96")
row_index = {key: i for i, key in enumerate(full_rows)}
metric_probe_tangents = []
for role in range(4):
    tangent_row = []
    for p in range(4):
        tangent = sum(
            (
                b_symbols[row_index[(p, role, gi)]] * GENERATORS[gi]
                for gi in range(6)
            ),
            sp.zeros(4),
        )
        tangent_row.append(tangent)
    metric_probe_tangents.append(tangent_row)

metric_link_rows = []
for p in range(4):
    for row, col in SYM:
        response = metric_euler_z1((p, 0, 0, 0), row, col, metric_probe_tangents, I4)
        response_poly = sp.Poly(response, *b_symbols)
        metric_link_rows.append([
            response_poly.coeff_monomial(symbol) for symbol in b_symbols
        ])
metric_link_map = sp.Matrix(metric_link_rows)

# Upgrade the already solved curvature-only h^2*z^2 connection correction to
# the full joint coefficient.  The coframe metric_solder is constant across
# the cell, and the identity-link flat control has zero metric Euler on every
# row.  This calculation does not identify that control with the designated
# discrete #216 comparator.  Keep every phase, role and Lorentz-link direction
# available to the correction solve.
identity_links = [[I4 for _ in range(4)] for _ in range(4)]
check(
    "CONSTANT_SOLDER_IDENTITY_COMPARATOR_METRIC_ZERO",
    all(
        metric_euler_full((p, 0, 0, 0), row, col, identity_links, metric_solder) == 0
        for p in range(4)
        for row, col in SYM
    ),
)
curvature_metric_source = sp.Matrix([
    coefficient_h2_z2(metric_euler_full(
        (p, 0, 0, 0), row, col, full_order_h_links, metric_solder,
    ))
    for p in range(4)
    for row, col in SYM
])
joint_curvature_matrix = full_jacobian.col_join(metric_link_map)
joint_curvature_rhs = (-curvature_source).col_join(-curvature_metric_source)
joint_curvature_rank = sp.polys.matrices.DomainMatrix.from_Matrix(
    joint_curvature_matrix
).rank()
joint_curvature_augmented_rank = sp.polys.matrices.DomainMatrix.from_Matrix(
    joint_curvature_matrix.row_join(joint_curvature_rhs)
).rank()
print(
    "JOINT_H2_Z2_CONNECTION_METRIC_RANKS",
    joint_curvature_rank,
    joint_curvature_augmented_rank,
)
check(
    "JOINT_H2_Z2_CONNECTION_METRIC_COMPATIBLE",
    joint_curvature_rank == joint_curvature_augmented_rank,
)
joint_curvature_solution, joint_curvature_parameters = (
    joint_curvature_matrix.gauss_jordan_solve(joint_curvature_rhs)
)
joint_curvature_solution = joint_curvature_solution.subs(
    {parameter: 0 for parameter in joint_curvature_parameters}
)
check(
    "JOINT_H2_Z2_CONNECTION_RESIDUAL_ZERO",
    full_jacobian * joint_curvature_solution + curvature_source
    == sp.zeros(96, 1),
)
check(
    "JOINT_H2_Z2_ALL_40_METRIC_ROWS_ZERO",
    metric_link_map * joint_curvature_solution + curvature_metric_source
    == sp.zeros(40, 1),
)
joint_curvature_corrected_links = [list(row) for row in full_order_h_links]
for (p, role, gi), coefficient in zip(full_rows, joint_curvature_solution):
    joint_curvature_corrected_links[role][p] += (
        h**2 * z**2 * coefficient * GENERATORS[gi]
    )
check(
    "JOINT_H2_Z2_ALL_96_FINITE_CONNECTION_ROWS_ZERO",
    all(
        coefficient_h2_z2(edge_euler_full(
            (p, 0, 0, 0), role, GENERATORS[gi],
            joint_curvature_corrected_links, metric_solder,
        )) == 0
        for p, role, gi in full_rows
    ),
)
check(
    "JOINT_H2_Z2_ALL_40_FINITE_METRIC_ROWS_ZERO",
    all(
        coefficient_h2_z2(metric_euler_full(
            (p, 0, 0, 0), row, col,
            joint_curvature_corrected_links, metric_solder,
        )) == 0
        for p in range(4)
        for row, col in SYM
    ),
)
print(
    "JOINT_H2_Z2_LINK_SUPPORT",
    [(full_rows[i], str(value)) for i, value in enumerate(joint_curvature_solution) if value],
)

phase_difference_map = sp.zeros(30, 96)
phase_difference_base = sp.zeros(30, 1)
for p in (1, 2, 3):
    for k in range(10):
        out = (p - 1) * 10 + k
        phase_difference_map[out, :] = (
            metric_link_map[p * 10 + k, :] - metric_link_map[k, :]
        )
        phase_difference_base[out] = metric_base[p * 10 + k] - metric_base[k]

# Independently test the original connection-only representative against all
# 40 metric rows; the joint solve above also verifies its own finite root.
curvature_metric_on_connection_lift = sp.Matrix([
    coefficient_h2_z2(metric_euler_full(
        (p, 0, 0, 0), row, col, curvature_corrected_links, metric_solder,
    ))
    for p in range(4)
    for row, col in SYM
])
check("H2_Z2_METRIC_ROWS_ZERO_ON_CONNECTION_ONLY_CORRECTION",
      curvature_metric_on_connection_lift == sp.zeros(40, 1))

joint_slope_matrix = full_jacobian.col_join(phase_difference_map)
joint_slope_rhs = (-slope_source).col_join(-phase_difference_base)
joint_slope_rank = sp.polys.matrices.DomainMatrix.from_Matrix(
    joint_slope_matrix
).rank()
joint_slope_augmented_rank = sp.polys.matrices.DomainMatrix.from_Matrix(
    joint_slope_matrix.row_join(joint_slope_rhs)
).rank()
check(
    "FULL_96_CONNECTION_AND_30_METRIC_DIFFERENCES_COMPATIBLE",
    joint_slope_rank == 88 and joint_slope_augmented_rank == 88,
)
joint_slope_solution, joint_slope_parameters = joint_slope_matrix.gauss_jordan_solve(
    joint_slope_rhs
)
joint_slope_solution = joint_slope_solution.subs(
    {parameter: 0 for parameter in joint_slope_parameters}
)
expected_joint_slope = sp.zeros(96, 1)
for key, value in {
    (0, 0, 1): sp.Rational(1, 2),
    (0, 0, 2): -sp.Rational(1, 2),
    (2, 0, 1): -sp.Rational(1, 2),
    (2, 0, 2): sp.Rational(1, 2),
}.items():
    expected_joint_slope[full_rows.index(key)] = value
check(
    "EXPLICIT_PHASE_COMMON_H2_Z_SLOPE_LIFT",
    joint_slope_solution == expected_joint_slope,
)
check(
    "JOINT_SLOPE_CONNECTION_RESIDUAL_ZERO",
    full_jacobian * joint_slope_solution + slope_source == sp.zeros(96, 1),
)
joint_metric_coefficient = metric_base + metric_link_map * joint_slope_solution
check(
    "ALL_TEN_PHASE_COMMON_H2_Z_SLOPE_METRIC_ROWS_ZERO",
    joint_metric_coefficient == sp.zeros(40, 1),
)
check(
    "JOINT_SLOPE_PHASE_DIFFERENCES_ZERO",
    phase_difference_map * joint_slope_solution + phase_difference_base
    == sp.zeros(30, 1),
)
print("JOINT_SLOPE_RANKS", joint_slope_rank, joint_slope_augmented_rank)
print(
    "JOINT_SLOPE_LINK_COEFFICIENTS",
    [(full_rows[i], str(value)) for i, value in enumerate(joint_slope_solution) if value],
)

# Continue the first-amplitude slow jet through h^3*z*x0 without fixing any
# first- or second-order joint-kernel representative.  The exact z-linear
# formulas above keep this 388 x 288 system small and retain all 96 link modes
# independently at each of the three h-orders.
a3_symbols = sp.symbols("a3_0:96")
b3_symbols = sp.symbols("b3_0:96")
c3_symbols = sp.symbols("c3_0:96")
jet_variables = a3_symbols + b3_symbols + c3_symbols
jet_tangents = []
for role in range(4):
    tangent_row = []
    for p in range(4):
        base_tangent = Y if (role, p) == (0, 0) else -Y if (role, p) == (0, 2) else sp.zeros(4)
        tangent_row.append(
            base_tangent
            + h * sum(
                (a3_symbols[row_index[(p, role, gi)]] * GENERATORS[gi] for gi in range(6)),
                sp.zeros(4),
            )
            + h**2 * x0 * sum(
                (b3_symbols[row_index[(p, role, gi)]] * GENERATORS[gi] for gi in range(6)),
                sp.zeros(4),
            )
            + h**3 * x0 * sum(
                (c3_symbols[row_index[(p, role, gi)]] * GENERATORS[gi] for gi in range(6)),
                sp.zeros(4),
            )
        )
    jet_tangents.append(tangent_row)

jet_equations = []
for p, role, gi in full_rows:
    response = connection_euler_z1(
        (p, 0, 0, 0), role, GENERATORS[gi], jet_tangents, probe_solder
    )
    response_poly = sp.Poly(sp.expand(response), h, x0)
    jet_equations.extend([
        response_poly.coeff_monomial(h),
        response_poly.coeff_monomial(h**2 * x0),
        response_poly.coeff_monomial(h**3 * x0),
    ])

jet_metric_coefficients = []
for p in range(4):
    phase_rows = []
    for row, col in SYM:
        response = metric_euler_z1(
            (p, 0, 0, 0), row, col, jet_tangents, probe_solder
        )
        response_poly = sp.Poly(sp.expand(response), h, x0)
        coefficients = (
            response_poly.coeff_monomial(h),
            response_poly.coeff_monomial(h**2 * x0),
            response_poly.coeff_monomial(h**3 * x0),
        )
        phase_rows.append(coefficients)
        jet_equations.append(coefficients[0])
    jet_metric_coefficients.append(phase_rows)

for p in (1, 2, 3):
    for k in range(10):
        jet_equations.append(
            jet_metric_coefficients[p][k][1] - jet_metric_coefficients[0][k][1]
        )
        jet_equations.append(
            jet_metric_coefficients[p][k][2] - jet_metric_coefficients[0][k][2]
        )

check("H3_SLOPE_JET_SYSTEM_SHAPE", len(jet_equations) == 388 and len(jet_variables) == 288)
jet_matrix, jet_rhs = sp.linear_eq_to_matrix(jet_equations, jet_variables)
jet_rank = sp.polys.matrices.DomainMatrix.from_Matrix(jet_matrix).rank()
jet_augmented_rank = sp.polys.matrices.DomainMatrix.from_Matrix(
    jet_matrix.row_join(jet_rhs)
).rank()
print("H3_SLOPE_JET_RANKS", jet_rank, jet_augmented_rank, "FREE", 288 - jet_rank)
if jet_rank == jet_augmented_rank:
    jet_solution, jet_parameters = jet_matrix.gauss_jordan_solve(jet_rhs)
    check("H3_JET_FREE_DIMENSION_24", len(jet_parameters) == 24)
    jet_parametric_substitution = dict(zip(jet_variables, jet_solution))
    jet_solution = jet_solution.subs({parameter: 0 for parameter in jet_parameters})
    check(
        "H3_SLOPE_JET_EXACT_SOLUTION",
        jet_matrix * jet_solution - jet_rhs == sp.zeros(jet_matrix.rows, 1),
    )
    jet_substitution = dict(zip(jet_variables, jet_solution))
    common_metric_h2x = [
        sp.factor(jet_metric_coefficients[0][k][1].subs(jet_parametric_substitution))
        for k in range(10)
    ]
    common_metric_h3x = [
        sp.factor(jet_metric_coefficients[0][k][2].subs(jet_parametric_substitution))
        for k in range(10)
    ]
    check(
        "H3_JET_NATIVE_METRIC_H2_X0_ZERO_FOR_ALL_24_DIRECTIONS",
        all(sp.simplify(value) == 0 for value in common_metric_h2x),
    )
    check(
        "H3_JET_NATIVE_METRIC_H3_X0_ZERO_FOR_ALL_24_DIRECTIONS",
        all(sp.simplify(value) == 0 for value in common_metric_h3x),
    )
    check(
        "H3_JET_PHASE_COMMON_METRIC_FOR_ALL_24_FREE_DIRECTIONS",
        all(
            sp.simplify(
                jet_metric_coefficients[p][k][j].subs(jet_parametric_substitution)
                - jet_metric_coefficients[0][k][j].subs(jet_parametric_substitution)
            ) == 0
            for p in range(1, 4)
            for k in range(10)
            for j in (1, 2)
        ),
    )
    print("H3_PARAMETRIC_COMMON_METRIC_H2_X0", [str(value) for value in common_metric_h2x])
    print("H3_PARAMETRIC_COMMON_METRIC_H3_X0", [str(value) for value in common_metric_h3x])
    print("H3_COMMON_METRIC_H2_X0", [str(value) for value in common_metric_h2x])
    print("H3_COMMON_METRIC_H3_X0", [str(value) for value in common_metric_h3x])
    print(
        "H3_JOINT_LIFT_SUPPORT",
        {
            "A": [(full_rows[i], str(sp.factor(jet_solution[i]))) for i in range(96) if jet_solution[i]],
            "B": [(full_rows[i], str(sp.factor(jet_solution[96 + i]))) for i in range(96) if jet_solution[96 + i]],
            "C": [(full_rows[i], str(sp.factor(jet_solution[192 + i]))) for i in range(96) if jet_solution[192 + i]],
        },
    )
else:
    check("H3_SLOPE_JET_EXACT_OBSTRUCTION", jet_augmented_rank > jet_rank)
print("TERMINAL", "J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-CANCELS")
