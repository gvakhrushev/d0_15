
#!/usr/bin/env python3
"""Connection-stationary slow lift of the #232 microstructure (reconstructed)."""
from __future__ import annotations
from itertools import combinations
import sympy as sp

def check(name, condition):
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
            check("FLAT_EK_%d_%d_%d" % (p, role, gi), c0 == 0)
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
    check("PHASE_%d_ORDER_H_CANCELLED" % p, all(term == 0 for term in low))
    expected = [
        0,
        -sign * h**2 * z**2 * (z - 2) / (2 * D**2),
        sign * h**2 * z**2 * (z - 2) / (2 * D**2),
        0, 0,
        -sign * h**2 * x0 * z / D,
        sign * h**2 * x0 * z / D,
        -sign * h**2 * x0 * z / D,
        0,
        sign * h**2 * x0 * z / D,
    ]
    check("PHASE_%d_ORDER_H2" % p, all(
        sp.simplify(sp.together(sp.sympify(got).coeff(h, 2) - sp.sympify(want).coeff(h, 2))) == 0
        for got, want in zip(comps, expected)))

for scaling in (h, h**2):
    normalized = sp.series((-h**2 * z**2 * (z - 2) / (2 * D**2)).subs(z, scaling) / h**2, h, 0, 2).removeO()
    slope = sp.series((h**2 * x0 * z / D).subs(z, scaling) / h**2, h, 0, 1).removeO()
    check("NORMALIZED_LIMIT_%s" % scaling, normalized == 0 and slope == 0)

for p in range(4):
    site = (p, 0, 0, 0)
    for role in range(4):
        for gi, gen in enumerate(GENERATORS):
            value = edge_euler(site, role, gen, [I4, I4, I4, I4], solder.subs(z, 0))
            check("FLAT_LIMIT_EK_%d_%d_%d" % (p, role, gi), sp.series(sp.expand(value), h, 0, 3).removeO() == 0)

print("LIFT", [str(sp.factor(s)) for s in solution])
print("TERMINAL J2-DIAGONAL-MICROSTRUCTURE-CONNECTION-STATIONARY-RESPONSE-CANCELS")
