#!/usr/bin/env python3
"""Exact identity-link harmonic forcing of the A4D metric-null ray.

CONTROL: CTRL-A4D-RESOLVED-AFFINE-PROGRAM-WAVE, PR #296.
Terminal: A4D-Q0-HARMONIC-LIFT-SECOND-JET-EXACT

Consumes #270 only through its polynomial C(d), before its rank cover.
Independently reconstructs the edge Euler from the four oriented incidences
of a based plaquette. No floating arithmetic, stationary-link solve, Einstein
comparison, full-action change, or global stationary-sheet claim is used.
"""
from __future__ import annotations

from itertools import combinations
from pathlib import Path

import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def zero(matrix):
    return all(sp.expand(x) == 0 for x in matrix)


OWNER = Path(__file__).with_name("a4d_metric_null_hessian_complex_check.py")
source = OWNER.read_text(encoding="utf-8")
cut = source.index("# Exact projective cover of d != 0.")
owner = {"__name__": "_q0_harmonic_owner", "__file__": str(OWNER)}
exec(compile(source[:cut], str(OWNER), "exec"), owner)
C = owner["C"]
d = sp.Matrix(owner["d"])
ETA = sp.diag(1, -1, -1, -1)
PAIRS = list(combinations(range(4), 2))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
I4 = sp.eye(4)


def sym_vec(matrix):
    return sp.Matrix([matrix[a, b] for a, b in SYM])


def wedge(u, v):
    return sp.Matrix([sp.expand(u[a] * v[b] - u[b] * v[a]) for a, b in PAIRS])


def orientation(face):
    complement = [i for i in range(4) if i not in face]
    order = list(face) + complement
    return (-1) ** sum(order[i] > order[j] for i in range(4) for j in range(i + 1, 4))


# Reconstruct the six literal Lorentz edge variations and density pairing.
GENERATORS = []
for i in (1, 2, 3):
    generator = sp.zeros(4)
    generator[0, i] = generator[i, 0] = 1
    GENERATORS.append(generator)
for i, j in ((1, 2), (1, 3), (2, 3)):
    generator = sp.zeros(4)
    generator[i, j], generator[j, i] = 1, -1
    GENERATORS.append(generator)
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = sp.zeros(6)
for column, ((a, b), (c, e), sign) in enumerate((
    ((0, 1), (2, 3), -1), ((0, 2), (1, 3), 1),
    ((0, 3), (1, 2), -1), ((1, 2), (0, 3), 1),
    ((1, 3), (0, 2), -1), ((2, 3), (0, 1), 1),
)):
    assert PAIRS[column] == (a, b)
    STAR[PAIRS.index((c, e)), column] = sign
PAIRING = [G2 * STAR * sp.Matrix([(g * ETA)[a, b] for a, b in PAIRS]) for g in GENERATORS]
check("LITERAL_STAR_SQUARE", STAR * STAR == -sp.eye(6))


def face_covectors(area, face):
    return sp.Matrix([sp.expand(orientation(face) * (area.T * pairing)[0]) for pairing in PAIRING])


def incidence_symbol(areas, difference):
    """Edge Euler, directly from (+r at x,+s at x+r,-r at x+s,-s at x).

    For an area character w, the Role-r coefficient is 1-w_s^-1,
    and the Role-s coefficient is w_r^-1-1. The input is w^-1-1.
    """
    result = sp.zeros(24, 1)
    for r, s in PAIRS:
        covector = face_covectors(areas[(r, s)], (r, s))
        for g in range(6):
            result[6 * r + g] -= difference[s] * covector[g]
            result[6 * s + g] += difference[r] * covector[g]
    return result.applyfunc(sp.expand)


def area_linear(polarization):
    lift = polarization * ETA / 2
    return {
        face: wedge(lift.row(u).T, I4[:, v]) + wedge(I4[:, u], lift.row(v).T)
        for face in PAIRS
        for u, v in [[i for i in range(4) if i not in face]]
    }


w = sp.Matrix(sp.symbols("w0:4"))
Cw = C.subs(dict(zip(d, w)), simultaneous=True)
q = d * d.T
qvec = sym_vec(q)
sigma = (d.T * ETA * d)[0]
R = q * ETA
check("RANK_ONE_SQUARE", zero(R * R - sigma * R))
check("RANK_ONE_METRIC_NULL_OWNER", zero(C * qvec))
check("INDEPENDENT_INCIDENCE_MATCHES_C", zero(incidence_symbol(area_linear(q), w) - Cw * qvec))

a, t = sp.symbols("a t")
theta = I4 + a * R
gram_remainder = theta * ETA * theta.T - ETA - t * q
check("EXACT_GRAM_RELATION", zero(gram_remainder - (2 * a + sigma * a**2 - t) * q))
check("EXACT_FRAME_DETERMINANT", sp.expand(theta.det() - 1 - a * sigma) == 0)
s = sp.symbols("s")
scalar_lift = t / (1 + sp.sqrt(1 + s * t))
check("EXACT_SCALAR_ROOT", sp.simplify(2 * scalar_lift + s * scalar_lift**2 - t) == 0)
check("NULL_SCALAR_LIFT_IS_LINEAR", scalar_lift.subs(s, 0) == t / 2)
# Verify every coefficient through degree two.
jet_gram = sp.expand((I4 + t * R / 2 - sigma * t**2 * R / 8) * ETA * (I4 + t * R / 2 - sigma * t**2 * R / 8).T - ETA - t * q)
check("ALL_GRAM_COEFFICIENTS_THROUGH_TWO", all(sp.expand(x).coeff(t, n) == 0 for x in jet_gram for n in range(3)))

areas = {}
for face in PAIRS:
    u, v = [i for i in range(4) if i not in face]
    areas[face] = wedge(theta.row(u).T, theta.row(v).T) - wedge(I4[:, u], I4[:, v])
    check("AREA_LINEAR_%d%d" % face, zero(areas[face] - 2 * a * area_linear(q)[face]))
check("EXACT_EULER_LINEAR_IN_FRAME_SCALAR", zero(incidence_symbol(areas, w) - 2 * a * Cw * qvec))

d_squared = d.applyfunc(lambda x: x**2)
d2 = 2 * d + d_squared
C2 = C.subs(dict(zip(d, d2)), simultaneous=True)
F2 = (-sigma * C2 * qvec / 4).applyfunc(sp.expand)
degree_six = (-sigma * C.subs(dict(zip(d, d_squared)), simultaneous=True) * qvec / 4).applyfunc(sp.expand)
check("SECOND_HARMONIC_DEGREE_SIX_IDENTITY", zero(F2 - degree_six))
check("SECOND_HARMONIC_HOMOGENEOUS_DEGREE_SIX", all(sp.Poly(x, *d).total_degree() == 6 for x in F2 if x != 0))
check("SECOND_HARMONIC_NOT_ZERO_POLYNOMIAL", not zero(F2))
for i, j in PAIRS:
    check("PARALLELISM_MINOR_%d%d" % (i, j), sp.expand(d[i] * d2[j] - d[j] * d2[i] - d[i] * d[j] * (d[j] - d[i])) == 0)

# All-order criterion uses exact algebra, not a finite Taylor test.
# On each nonempty active support d=c*v, d(z^n)=((1+c)^n-1)*v.
# C is linear, so C(d(z^n)) q(d)=0 for every n by the consumed null identity.
c, harmonic_scalar = sp.symbols("c harmonic_scalar")
for mask in range(1, 16):
    support = sp.Matrix([(mask >> r) & 1 for r in range(4)])
    q_support = c**2 * support * support.T
    harmonic_C = C.subs(dict(zip(d, harmonic_scalar * support)), simultaneous=True)
    check("COMMON_CHARACTER_ALL_ORDER_SUPPORT_%02d" % mask, zero(harmonic_C * sym_vec(q_support)))


def real_frame_areas(z, order):
    """Literal real metric path q*chi+conjugate(q*chi), symmetric Gram 2-jet."""
    dv = sp.Matrix([1 / x - 1 for x in z])
    qq = dv * dv.T
    areas_by_phase = {}
    for phase in range(order):
        chi = sp.I**phase if order == 4 else sp.Integer((-1)**phase)
        metric_amplitude = (qq * chi + sp.conjugate(qq * chi)).applyfunc(sp.expand)
        H = metric_amplitude * ETA / 2
        S = -(metric_amplitude * ETA)**2 / 8
        for face in PAIRS:
            u, v = [i for i in range(4) if i not in face]
            areas_by_phase[(phase, face, 1)] = wedge(H.row(u).T, I4[:, v]) + wedge(I4[:, u], H.row(v).T)
            areas_by_phase[(phase, face, 2)] = wedge(S.row(u).T, I4[:, v]) + wedge(I4[:, u], S.row(v).T) + wedge(H.row(u).T, H.row(v).T)
        check("REAL_GRAM_JET_%d_%d" % (order, phase), zero(S * ETA + ETA * S.T + H * ETA * H.T))
    return areas_by_phase


def phase_edge_euler(areas_by_phase, phase, increments, order, degree):
    """Position-space Euler at a site, with all incident base sites retained."""
    result = sp.zeros(24, 1)
    for r, s in PAIRS:
        here = face_covectors(areas_by_phase[(phase, (r, s), degree)], (r, s))
        previous_s = face_covectors(areas_by_phase[((phase - increments[s]) % order, (r, s), degree)], (r, s))
        previous_r = face_covectors(areas_by_phase[((phase - increments[r]) % order, (r, s), degree)], (r, s))
        for g in range(6):
            result[6 * r + g] += here[g] - previous_s[g]
            result[6 * s + g] += previous_r[g] - here[g]
    return result.applyfunc(sp.expand)


ZA = (sp.I, sp.I, -sp.I, -sp.I)
da = sp.Matrix([1 / x - 1 for x in ZA])
qa = da * da.T
sigma_a = sp.expand((da.T * ETA * da)[0])
ca2 = C.subs(dict(zip(d, [-2] * 4)))
fa = (-sigma_a * ca2 * sym_vec(qa) / 4).applyfunc(sp.expand)
real_fa = (fa + sp.conjugate(fa)).applyfunc(sp.expand)
check("QUARTER_WAVE_SIGMA_4I", sigma_a == 4 * sp.I)
check("REAL_QUARTER_WAVE_SECOND_FORCING_NONZERO", not zero(real_fa))
check("REAL_QUARTER_WAVE_POLARIZATION_RANK_TWO", (sigma_a * qa + sp.conjugate(sigma_a * qa)).rank() == 2)
areas_a = real_frame_areas(ZA, 4)
for phase in range(4):
    check("REAL_QUARTER_WAVE_LINEAR_ZERO_%d" % phase, zero(phase_edge_euler(areas_a, phase, (1, 1, -1, -1), 4, 1)))
    direct = phase_edge_euler(areas_a, phase, (1, 1, -1, -1), 4, 2)
    check("REAL_QUARTER_WAVE_SECOND_FORMULA_%d" % phase, zero(direct - (-1)**phase * real_fa))
wrong_frozen = (-sigma_a * C.subs(dict(zip(d, da))) * sym_vec(qa) / 4)
check("HOSTILE_FROZEN_CHARACTER_FAILS", zero(wrong_frozen) and not zero(real_fa))
check("HOSTILE_WRONG_SECOND_ORDER_SIGN_FAILS", not zero(real_fa + phase_edge_euler(areas_a, 0, (1, 1, -1, -1), 4, 2)))

# The conjugate-product terms are constant in phase and have zero flat-link
# edge Euler because the literal incidences telescope at character one.
arbitrary_area = sp.Matrix(sp.symbols("b0:6"))
check("CONSTANT_MIXED_AREA_TELESCOPES", zero(incidence_symbol({face: arbitrary_area for face in PAIRS}, sp.zeros(4, 1))))

# Physical null example, including the factor two from q*chi+conjugate.
ZB = (-1, 1, -1, 1)
db = sp.Matrix([sp.Integer(1) / x - 1 for x in ZB])
qb = db * db.T
check("REAL_NULL_SIGMA_ZERO", (db.T * ETA * db)[0] == 0)
eps = sp.symbols("eps", real=True)
for sign in (1, -1):
    exact_frame = I4 + eps * sign * qb * ETA
    check("REAL_NULL_EXACT_GRAM_%d" % sign, zero(exact_frame * ETA * exact_frame.T - ETA - 2 * eps * sign * qb))
    check("REAL_NULL_EXACT_DETERMINANT_%d" % sign, sp.expand(exact_frame.det()) == 1)
areas_b = real_frame_areas(ZB, 2)
for phase in range(2):
    for degree in (1, 2):
        check("REAL_NULL_EULER_%d_%d" % (phase, degree), zero(phase_edge_euler(areas_b, phase, (1, 0, 1, 0), 2, degree)))
# Exact frame is linear in eps and the area is quadratic; those two zero
# coefficients exhaust the full connection Euler, not merely a Taylor jet.

# Complex-null alone is not permission to assume that a real conjugate pair
# remains rank one. This is a carrier guard, not an all-order failure claim.
zc = (sp.I, sp.I, sp.I, -sp.I)
dc = sp.Matrix([1 / x - 1 for x in zc])
qc = dc * dc.T
check("COMPLEX_NULL_REAL_PAIR_GUARD", sp.expand((dc.T * ETA * dc)[0]) == 0 and (qc + sp.conjugate(qc)).rank() == 2)

print("A4D-Q0-HARMONIC-LIFT-SECOND-JET-EXACT")
print("SCOPE: identity-link forcing and exact restricted ray continuation; no stationary-link repair or general metric-stress theorem")
