#!/usr/bin/env python3
"""Exact finite controls for the fixed-realization J2 theorem memo.

Owns: the full polarized 24x24 zero-phase Gram spectrum, Laurent derivative
bounds at the canonical solder, and a polynomial congruence for arbitrary
constant solder. Hostile examples check two invalid inference rules.
Does not certify a nonlinear stationary branch of the full lattice, a uniform
UV inverse, or the continuum Einstein operator.
"""
from itertools import combinations
import sympy as sp

PAIRS = list(combinations(range(4), 2))
ETA = sp.diag(1, -1, -1, -1)
GENERATORS = []
for i in (1, 2, 3):
    x = sp.zeros(4)
    x[0, i] = x[i, 0] = 1
    GENERATORS.append(x)
for i, j in ((1, 2), (1, 3), (2, 3)):
    x = sp.zeros(4)
    x[i, j], x[j, i] = 1, -1
    GENERATORS.append(x)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for p, (q, sign) in {
    (0, 1): ((2, 3), -1), (0, 2): ((1, 3), 1),
    (0, 3): ((1, 2), -1), (1, 2): ((0, 3), 1),
    (1, 3): ((0, 2), -1), (2, 3): ((0, 1), 1),
}.items():
    STAR[PAIRS.index(q), PAIRS.index(p)] = sign


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def wedge(u, v):
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def connection_symbol(solder, phase):
    """BCH mixed jet of (P-P^-1)/2, polarized as z and z^-1.

    Each plaquette has four exponential factors. Its mixed curvature is
    1/2 sum_{i<j} ([X_i,Y_j]+[Y_i,X_j]). The two independent amplitudes
    carry inverse phases, as in the merged #208 certificate.
    solder[:,r] is the internal vector v_r; no numerical arithmetic is used.
    """
    result = sp.zeros(24)
    for r, s in PAIRS:
        u, v = [i for i in range(4) if i not in (r, s)]
        seq = [r, s, u, v]
        sign = (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))
        pairing = sign * wedge(solder[:, u], solder[:, v]).T * G2 * STAR
        bracket_form = sp.zeros(6)
        for i, xi in enumerate(GENERATORS):
            for j, xj in enumerate(GENERATORS):
                y = (xi * xj - xj * xi) * ETA
                bracket_form[i, j] = (pairing * sp.Matrix([y[a, b] for a, b in PAIRS]))[0]
        roles = [r, s, r, s]
        direct = [sp.Integer(1), phase[r], -phase[s], sp.Integer(-1)]
        inverse = [sp.Integer(1), 1 / phase[r], -1 / phase[s], sp.Integer(-1)]
        role_form = sp.zeros(4)
        for i, j in combinations(range(4), 2):
            role_form[roles[i], roles[j]] += direct[i] * inverse[j] / 2
            role_form[roles[j], roles[i]] -= inverse[i] * direct[j] / 2
        result += sp.kronecker_product(role_form, bracket_form)
    return result.applyfunc(sp.expand)


check("LORENTZ_GENERATORS", all(x.T * ETA + ETA * x == sp.zeros(4) for x in GENERATORS))
check("STAR_SQUARE", STAR * STAR == -sp.eye(6))
one = [sp.Integer(1)] * 4
h0 = connection_symbol(sp.eye(4), one)
check("ZERO_PHASE_SYMMETRIC", h0 == h0.T)
check("ZERO_PHASE_DETERMINANT_256", h0.det() == 256)
check("ZERO_PHASE_GRAM_SPECTRUM", (h0.T * h0).eigenvals() == {sp.Integer(1): 16, sp.Integer(4): 8})

z = sp.symbols("z0:4", nonzero=True)
hz = connection_symbol(sp.eye(4), z)
check("LAURENT_ZERO_PHASE_MATCH", hz.subs(dict(zip(z, one))) == h0)
for j in range(4):
    bounds = []
    for entry in hz:
        bound = 0
        for term in sp.Add.make_args(entry):
            powers = term.as_powers_dict()
            coefficient = term
            for zi in z:
                coefficient /= zi ** powers.get(zi, 0)
            check_rational = coefficient.is_Rational
            if not check_rational:
                raise AssertionError("nonrational Laurent coefficient")
            bound += abs(coefficient) * abs(powers.get(z[j], 0))
        bounds.append(bound)
    check("PHASE_DERIVATIVE_FROBENIUS_SQUARED_" + str(j), sum(b * b for b in bounds) == 36)
# For real phases: ||H(theta)-H(0)||_2 <= 6 ||theta||_1.
# sigma_min >= 1/2 whenever ||theta||_1 <= 1/12.
check("CANONICAL_GAP_BOUND", 1 - 6 * sp.Rational(1, 12) == sp.Rational(1, 2))

# Generic polynomial identity, not a finite battery of solder samples.
e = sp.symbols("e0:16")
E = sp.Matrix(4, 4, e)
role_change = sp.kronecker_product(E.T, sp.eye(6))
identity = role_change.T * connection_symbol(E, one) * role_change - E.det() * h0
check("ALL_CONSTANT_SOLDERS_POLYNOMIAL_CONGRUENCE", all(sp.expand(c) == 0 for c in identity))
# If E is invertible, P=E^-T tensor I gives H_E(0)=det(E) P^T H_I(0) P.
# Thus sigma_min(H_E(0)) >= |det E| / ||E||_2^2.

u, t = sp.symbols("u t", real=True)
# Isolated zero does not imply surjectivity: u^2 never takes negative values.
check("ISOLATION_WITHOUT_SURJECTIVITY", sp.solveset(u ** 2 + 1, u, domain=sp.S.Reals) == sp.S.EmptySet)
# Odd degree at an unperturbed zero does not exclude new flat-approaching
# sheets under a small slow-background perturbation h=t^2.
f = u ** 3 - t ** 2 * u
check("SLOW_PERTURBATION_PLUS_SHEET", sp.expand(f.subs(u, t)) == 0)
check("SLOW_PERTURBATION_MINUS_SHEET", sp.expand(f.subs(u, -t)) == 0)
check("SLOW_PERTURBATION_FLAT_SHEET", f.subs(u, 0) == 0)
check("UNPERTURBED_CUBIC", f.subs(t, 0) == u ** 3)
print("RESULT: canonical IR gap and arbitrary constant-solder congruence are exact.")
print("BOUNDARY: no full-lattice UV stability or Einstein-limit closure is certified.")
