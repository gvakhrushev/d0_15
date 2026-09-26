#!/usr/bin/env python3
"""Exact full-star zero-source germ for the coupled normal-rescue task.

Research-only certificate. Rational symbolic arithmetic; no restricted-gradient
inference. A single edge is varied independently in all six Lorentz directions,
and all six incident plaquettes are differentiated. The resulting 4 phase x
4 Role x 6 generator equations vanish identically in the Cayley parameter.
The analytic memo proves that these local equations apply on every L=4m torus.

Does not prove a joint metric/connection vacuum: the nonzero metric partial is
precisely the branch-response obstruction. Does not edit the #202 witnesses or
repeat the sourced diagonal reduction / slow-background worker.
"""
from itertools import combinations
import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
GENERATORS = []
for j in (1, 2, 3):
    x = sp.zeros(4)
    x[0, j] = x[j, 0] = 1
    GENERATORS.append(x)
for a, b in PAIRS[3:]:
    x = sp.zeros(4)
    x[a, b], x[b, a] = 1, -1
    GENERATORS.append(x)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for col, (row, sign) in enumerate([(5, -1), (4, 1), (3, -1),
                                    (2, 1), (1, -1), (0, 1)]):
    STAR[row, col] = sign

COUNT = 0


def check(name, condition):
    global COUNT
    if not condition:
        raise AssertionError(name)
    COUNT += 1
    print('PASS_' + name, flush=True)


def reduced(matrix):
    return matrix.applyfunc(sp.factor)


def zero(matrix):
    return all(sp.factor(x) == 0 for x in matrix)


def lorentz_inverse(matrix):
    return ETA * matrix.T * ETA


def wedge(a, b):
    return sp.Matrix([a[i] * b[j] - a[j] * b[i] for i, j in PAIRS])


def bivector(matrix):
    y = matrix * ETA
    return sp.Matrix([y[a, b] for a, b in PAIRS])


def orientation(a, b):
    rest = [j for j in range(4) if j not in (a, b)]
    seq = [a, b] + rest
    return (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))


def face_partial(a, b, curvature_partial, solder=I4):
    u, v = [j for j in range(4) if j not in (a, b)]
    return orientation(a, b) * (
        wedge(solder[:, u], solder[:, v]).T * G2 * STAR
        * bivector(curvature_partial))[0]


def shift(site, role, step=1, period=4):
    out = list(site)
    out[role] = (out[role] + step) % period
    return tuple(out)


def phase(site):
    return sum(site) % 4


def link(site, role, wave):
    return wave[phase(site)] if role == 0 else I4


def face_factors(site, a, b, wave):
    return [link(site, a, wave), link(shift(site, a), b, wave),
            lorentz_inverse(link(shift(site, b), a, wave)),
            lorentz_inverse(link(site, b, wave))]


def multiply(factors):
    result = I4
    for factor in factors:
        result = result * factor
    return result


def single_edge_euler(site, role, generator, wave):
    """Derivative of the actual full action for ONE edge L -> L exp(e X).

    No other edge is varied. For each face containing this Role, the edge
    occurs at one positive and one negative corner, i.e. six plaquettes total.
    The period-four choice just evaluates their local coefficients; no sum
    over a constrained ansatz is differentiated.
    """
    result = 0
    incidents = 0
    for a, b in PAIRS:
        if role == a:
            corners = [(site, 0), (shift(site, b, -1), 2)]
        elif role == b:
            corners = [(shift(site, a, -1), 1), (site, 3)]
        else:
            continue
        for base, corner in corners:
            factors = face_factors(base, a, b, wave)
            plaquette = multiply(factors)
            pinv = lorentz_inverse(plaquette)
            varied = factors.copy()
            varied[corner] = (factors[corner] * generator if corner < 2
                              else -generator * factors[corner])
            dp = multiply(varied)
            dc = (dp + pinv * dp * pinv) / 2
            result += face_partial(a, b, dc)
            incidents += 1
    assert incidents == 6
    return sp.factor(result)


def metric_partial(site, wave):
    """Ten local Gram directions with the #201 lift H(q)=q eta/2.

    H rows are the variations of the internal solder vectors. At E_L=0 this
    metric partial agrees with any quotient-section lift, since its vertical
    / connection correction has vanishing contraction with the full E_L.
    """
    result = []
    for qa, qb in SYM:
        q = sp.zeros(4)
        q[qa, qb] = q[qb, qa] = 1
        h = q * ETA / 2
        derivative = 0
        for a, b in PAIRS:
            p = multiply(face_factors(site, a, b, wave))
            c = (p - lorentz_inverse(p)) / 2
            u, v = [j for j in range(4) if j not in (a, b)]
            dw = wedge(h[u, :].T, I4[:, v]) + wedge(I4[:, u], h[v, :].T)
            derivative += orientation(a, b) * (dw.T * G2 * STAR * bivector(c))[0]
        result.append(sp.factor(derivative))
    return sp.Matrix(result)


check('LORENTZ_GENERATORS', all(zero(x.T * ETA + ETA * x) for x in GENERATORS))
check('STAR_SQUARE_MINUS_ID', STAR * STAR == -sp.eye(6))
B = sum(GENERATORS[:3], sp.zeros(4))
t = sp.symbols('t', real=True)
D = 4 - 3 * t ** 2
c = 4 * t / D
U = reduced((I4 - t * B / 2).inv() * (I4 + t * B / 2))
Ui = lorentz_inverse(U)
wave = [U, I4, Ui, I4]
check('B_CUBED_3B', B ** 3 == 3 * B)
check('EXACT_CAYLEY_FORM', zero(U - I4 - c * B - 2 * t ** 2 / D * B ** 2))
check('CAYLEY_LORENTZ', zero(U.T * ETA * U - ETA))
check('CAYLEY_DET_ONE', sp.factor(U.det()) == 1)
check('CAYLEY_INVERSE', zero(U * Ui - I4))
check('CURVATURE_EXACT', zero((U - Ui) / 2 - c * B))
check('PLAQUETTE_TRACE', sp.factor(sp.trace(U) - 4 - 12 * t ** 2 / D) == 0)
check('FLAT_LIMIT', U.subs(t, 0) == I4)

# A separate trace calculation verifies the analytic proof's functional.
coefficients = sp.symbols('v0:6')
Y = sum((a * x for a, x in zip(coefficients, GENERATORS)), sp.zeros(4))
for s in (1, 2, 3):
    check('BOOST_FACE_TRACE_' + str(s),
          sp.expand(face_partial(0, s, Y) - sp.trace(GENERATORS[s - 1] * Y) / 2) == 0)

# Direct independent-edge derivative: 96 identities of rational functions.
for p in range(4):
    site = (p, 0, 0, 0)
    equations = [single_edge_euler(site, r, x, wave)
                 for r in range(4) for x in GENERATORS]
    check('ALL_24_FULL_EDGE_EULERS_PHASE_' + str(p), all(x == 0 for x in equations))

# Independent analytic gradient matrices; no projection is needed here.
for p in range(4):
    w, wp, wn = wave[p], wave[(p - 1) % 4], wave[(p + 1) % 4]
    wi, wpi, wni = map(lorentz_inverse, (w, wp, wn))
    P = w * wni
    Pi = lorentz_inverse(P)
    for s in (1, 2, 3):
        M = GENERATORS[s - 1]
        gs = wi * M * wp + wpi * M * w - M * P - Pi * M
        check('SIDE_ROLE_GRADIENT_MATRIX_' + str(p) + '_' + str(s), zero(gs))
    g0 = wni * B * w + wi * B * wn - wi * B * wp - wpi * B * w
    check('ROLE_ZERO_GRADIENT_MATRIX_' + str(p), zero(g0))

# Metric partial is NONZERO; no joint-vacuum inference is made.
m = sp.Matrix([0, 0, 0, 0, -1, 1, 1, -1, 1, -1])
for p, sign in enumerate((1, 1, -1, -1)):
    check('EXACT_10_METRIC_PARTIALS_PHASE_' + str(p),
          zero(metric_partial((p, 0, 0, 0), wave) - sign * c * m))
check('CURVATURE_FROBENIUS_SQUARED', sp.factor(sp.trace((c * B).T * (c * B)) - 6 * c ** 2) == 0)
q = sp.diag(0, 1, 0, 0)
check('GRAM_LIFT_EXACT', q == (q * ETA / 2) * ETA + ETA * (q * ETA / 2).T)

# The pattern is a function on every periodic L=4m lattice. Role shifts all
# increment its phase, including a wrap at the last site.
for length in (4, 8, 12):
    check('WRAP_COMPATIBILITY_L' + str(length), all(
        phase(shift(site, r, period=length)) == (phase(site) + 1) % 4
        for site in [(length - 1, 0, 0, 0), (0, length - 1, 0, 0),
                     (0, 0, length - 1, 0), (0, 0, 0, length - 1)]
        for r in range(4)))

h = sp.symbols('h', positive=True)
normalized = sp.factor(-c.subs(t, h ** 2) / h ** 2)
check('NORMALIZED_Q11_EXACT', sp.factor(normalized + 4 / (4 - 3 * h ** 4)) == 0)
check('NORMALIZED_Q11_LIMIT_MINUS_ONE', sp.limit(normalized, h, 0) == -1)
check('RAW_RESPONSE_LINEAR_SHARP', sp.limit(c / t, t, 0) == 1)
for length in (4, 8, 12):
    mesh = sp.Rational(1, length)
    check('NONZERO_RESPONSE_REFINEMENT_L' + str(length), normalized.subs(h, mesh) < -1)

# Hostile controls against accidentally certifying just an action-flat ansatz.
wrong_wave = [U, I4, U, I4]
check('WRONG_WAVE_HAS_FULL_EULER_PRESSURE', any(
    single_edge_euler((p, 0, 0, 0), r, x, wrong_wave).subs(t, sp.Rational(1, 5)) != 0
    for p in range(4) for r in range(4) for x in GENERATORS))
wrong_B = GENERATORS[0]
wrong_U = (I4 - t * wrong_B / 2).inv() * (I4 + t * wrong_B / 2)
wrong_axis = [wrong_U, I4, lorentz_inverse(wrong_U), I4]
check('WRONG_AXIS_HAS_ROTATION_EULER_PRESSURE', any(
    single_edge_euler((1, 0, 0, 0), 0, x, wrong_axis).subs(t, sp.Rational(1, 5)) != 0
    for x in GENERATORS[3:]))

u, a = sp.symbols('u a', real=True)
hostile = u ** 3 - a ** 2 * u
check('HOSTILE_FROZEN_CUBIC', hostile.subs(a, 0) == u ** 3)
check('HOSTILE_THREE_ZERO_SOURCE_BRANCHES', all(sp.expand(hostile.subs(u, v)) == 0 for v in (0, a, -a)))
print('CHECKS:', COUNT)
print('RESULT: exact full-star curved connection-stationary germ on every L=4m.')
print('RESULT: r_h=0 at the flat smooth sheet; the curved germ has nonzero normal distance.')
print('RESULT: t=h^2 gives normalized local q11 response -> -1 at the origin.')
print('TERMINAL: NAKED-STAR-J2-COUPLED-NORMAL-RESCUE-NOGO')
