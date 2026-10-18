#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=600
"""Rational points on the seed-to-chart Cayley segment.

The segment is the straight line of Cayley generators from the parabolic
seed generators0 to the section 9.37 chart-point generators. It is not the
whole full-affine family. For every rational parameter with all four Cayley
charts open, the homogeneous-link solder Hessian of the original star term
is singular only at the seed. Elsewhere it is invertible, so every
site coframe of that homogeneous link tuple is forced to zero. Channel
coefficients never enter this row: the owned four-channel integrand is a
function of links and translations only.

Status of the result is candidate. Irrational real roots of the degree-70
cofactor are not classified.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path

import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


ROOT = Path(__file__).resolve().parents[4]
OWNER_PATH = ROOT / (
    "02_REGISTRY/research/certificates/"
    "a4d_resolved_curved_stationary_e2_support7_order1_check.py"
)
F4_PATH = ROOT / (
    "02_REGISTRY/research/certificates/"
    "a4d_resolved_curved_stationary_f4_check.py"
)

spec = importlib.util.spec_from_file_location("support7_order1_owner", OWNER_PATH)
owner = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(owner)

R = sp.Rational
s = sp.symbols("s")
rho, t, u = R(1), R(0), R(8, 3)
amp = (R(0), R(0), R(-10, 3), R(-8, 3), R(0), R(4, 9), R(0))
# Published section 9.38 determinant at this chart point. Independent of
# the interpolation below.
EXPECTED_DET_S1 = R(
    40765604576726345069227791532913732955215768490597607321403042878734640884143996245433663881216,
    1043809895872838655329569143133917752420140067322792752999568729,
)

v_roles = [-4 * rho * owner.K1 + t * owner.N3, t * owner.N3, u * owner.K1 - owner.N2, owner.N3]
x_roles = [sp.zeros(4) for _ in range(4)]
for coeff, (_, role, gen) in zip(amp, owner.SELECTED_SPECS):
    x_roles[role] += coeff * gen
A_chart = [sp.Matrix(owner.generators0[r] + v_roles[r] + x_roles[r]) for r in range(4)]
A_seed = [sp.Matrix(a) for a in owner.generators0]
A = [sp.expand(A_seed[r] + s * (A_chart[r] - A_seed[r])) for r in range(4)]

chart_polys = []
for r, a in enumerate(A):
    poly = sp.Poly(sp.expand((owner.I4 - a / 2).det()), s, domain=sp.QQ)
    chart_polys.append(poly)
    print("CHART_POLY", r, sp.factor(poly.as_expr()), flush=True)
check("CHART0_CLOSED_AT_HALF", chart_polys[0].subs(s, R(1, 2)) == 0)
check("CHART3_CLOSED_AT_TWO", chart_polys[3].subs(s, 2) == 0)
check("CHARTS_OPEN_AT_0", all(poly.subs(s, 0) != 0 for poly in chart_polys))
check("CHARTS_OPEN_AT_1", all(poly.subs(s, 1) != 0 for poly in chart_polys))
role2_quad = sp.Poly(233 * s ** 2 + 16 * s - 36, s, domain=sp.ZZ)
role2_disc = sp.discriminant(role2_quad.as_expr(), s)
check("ROLE2_DISCRIMINANT_33808", role2_disc == 33808)
check("ROLE2_DISCRIMINANT_NOT_A_SQUARE", sp.integer_nthroot(int(role2_disc), 2)[1] is False)

f4_text = F4_PATH.read_text()
check(
    "OWNED_CHANNEL_HAS_NO_SOLDER_ARGUMENT",
    "def four_channel_I(links, bfield):" in f4_text
    and "def four_channel_I(links, bfield, theta" not in f4_text,
)
check(
    "OWNED_SOLDER_HESSIAN_IS_PER_SITE",
    "H[vidx(x, u, a), vidx(x, v, b)] += A[a, b]" in f4_text
    and "for x in SITES:" in f4_text,
)


def face_response(roles, r, ss):
    ur, us = roles[r], roles[ss]
    hol = ur * us * ur.inv() * us.inv()
    curv = (hol - hol.inv()) / 2
    qface = owner.orientation((r, ss)) * (
        owner.G2 * owner.STAR * owner.bivector_of_tangent(curv)
    )
    return qface


def assemble_homogeneous(qface, r, ss, homogeneous):
    """Index is 4*component + leg, with the 16-site weight of solder_at."""
    u_ax, v_ax = [i for i in range(4) if i not in (r, ss)]
    for k, (a, b) in enumerate(owner.PAIRS):
        for i, j, value in ((a, b, qface[k]), (b, a, -qface[k])):
            homogeneous[4 * i + u_ax][4 * j + v_ax] += 16 * value
            homogeneous[4 * j + v_ax][4 * i + u_ax] += 16 * value


roles = [sp.together(owner.cayley(a)) for a in A]
H_rows = [[sp.Integer(0) for _ in range(16)] for _ in range(16)]
for r, ss in owner.PAIRS:
    qface = face_response(roles, r, ss)
    assemble_homogeneous(qface, r, ss, H_rows)

reduced = []
den_lcm = sp.Poly(1, s, domain=sp.ZZ)
max_entry_degree = 0
for i in range(16):
    for j in range(i, 16):
        val = sp.together(sp.expand(H_rows[i][j]))
        if val == 0:
            reduced.append((i, j, sp.Poly(0, s, domain=sp.ZZ), sp.Poly(1, s, domain=sp.ZZ)))
            continue
        num, den = sp.fraction(val)
        num_p = sp.Poly(sp.expand(num), s, domain=sp.ZZ)
        den_p = sp.Poly(sp.expand(den), s, domain=sp.ZZ)
        g = sp.gcd(num_p, den_p)
        num_p = sp.div(num_p, g, domain=sp.ZZ)[0]
        den_p = sp.div(den_p, g, domain=sp.ZZ)[0]
        den_lcm = sp.lcm(den_lcm, den_p)
        max_entry_degree = max(max_entry_degree, num_p.degree())
        reduced.append((i, j, num_p, den_p))
check("ENTRY_NUMERATOR_DEGREE_AT_MOST_8", max_entry_degree <= 8)
print("DEN_LCM", sp.factor(den_lcm.as_expr()), flush=True)

M = [[sp.Poly(0, s, domain=sp.ZZ) for _ in range(16)] for _ in range(16)]
max_cleared = 0
den_failures = 0
non_integer = 0
for i, j, num_p, den_p in reduced:
    quot, rem = sp.div(den_lcm, den_p, domain=sp.QQ)
    if rem != 0:
        den_failures += 1
    cleared = sp.Poly(sp.expand(quot.as_expr() * num_p.as_expr()), s, domain=sp.QQ)
    for coeff in cleared.coeffs():
        if sp.fraction(sp.together(coeff))[1] != 1:
            non_integer += 1
    cleared = sp.Poly(sp.expand(cleared.as_expr()), s, domain=sp.ZZ)
    if cleared.degree() >= 0:
        max_cleared = max(max_cleared, cleared.degree())
    M[i][j] = cleared
    M[j][i] = cleared
check("DENOMINATORS_DIVIDE_LCM", den_failures == 0)
check("CLEARED_ENTRIES_ARE_INTEGER", non_integer == 0)
check("CLEARED_DEGREE_AT_MOST_12", max_cleared <= 12)
check("HESSIAN_POLY_SYMMETRIC", all(M[i][j] == M[j][i] for i in range(16) for j in range(16)))


def eval_matrix(poly_rows, value):
    out = sp.zeros(16)
    for i in range(16):
        for j in range(16):
            out[i, j] = poly_rows[i][j].subs(s, value)
    return out


def det_cleared(value):
    return int(eval_matrix(M, value).det())


degree_bound = 16 * max_cleared
nodes = list(range(degree_bound + 1))
values = [det_cleared(n) for n in nodes]
coeff = [sp.Integer(y) for y in values]
for k in range(1, len(nodes)):
    for i in range(len(nodes) - 1, k - 1, -1):
        coeff[i] = (coeff[i] - coeff[i - 1]) / (nodes[i] - nodes[i - k])
det_poly = sp.Integer(0)
for k in range(len(nodes) - 1, -1, -1):
    det_poly = sp.expand(det_poly * (s - nodes[k]) + coeff[k])
det_poly = sp.Poly(det_poly, s, domain=sp.ZZ)
check("DET_DEGREE_WITHIN_BOUND", det_poly.degree() <= degree_bound)
for extra in (-1, 6, 8, degree_bound + 2):
    check(f"DET_INTERPOLATION_{extra}", int(det_poly.subs(s, extra)) == det_cleared(extra))

delta_at_1 = int(den_lcm.subs(s, 1))
det_h_1 = sp.Rational(int(det_poly.subs(s, 1)), delta_at_1 ** 16)
check("CHART_POINT_DETERMINANT_MATCHES_9_38", det_h_1 == EXPECTED_DET_S1)

quad = sp.Poly(233 * s ** 2 + 16 * s - 36, s, domain=sp.ZZ)
base_factors = (
    ("s", sp.Poly(s, s, domain=sp.ZZ)),
    ("s_minus_2", sp.Poly(s - 2, s, domain=sp.ZZ)),
    ("s_plus_2", sp.Poly(s + 2, s, domain=sp.ZZ)),
    ("two_s_minus_1", sp.Poly(2 * s - 1, s, domain=sp.ZZ)),
    ("two_s_plus_1", sp.Poly(2 * s + 1, s, domain=sp.ZZ)),
    ("role2_chart_quad", quad),
)
remaining = det_poly
exponents = {}
for name, factor in base_factors:
    exponent = 0
    while True:
        quot, rem = sp.div(remaining, factor, domain=sp.ZZ)
        if rem != 0:
            break
        remaining = quot
        exponent += 1
    exponents[name] = exponent
    print("VALUATION", name, exponent, flush=True)
q_poly = remaining
check("COFACTOR_DEGREE_70", q_poly.degree() == 70)
q_content = sp.Integer(sp.content(q_poly))
check("COFACTOR_CONTENT_NONZERO", q_content != 0)
q_primitive = sp.Poly(sp.div(q_poly, sp.Poly(q_content, s, domain=sp.ZZ), domain=sp.ZZ)[0].as_expr(), s, domain=sp.ZZ)
check("COFACTOR_CONSTANT_TERM_NONZERO", q_primitive.TC() != 0)
check("S_FACTOR_PRESENT", exponents["s"] > 0)
check("CHART_FACTORS_PRESENT", all(exponents[name] > 0 for name, _ in base_factors if name != "s"))
for name, factor in base_factors:
    if name == "s":
        continue
    check(f"COFACTOR_COPIME_TO_{name}", sp.gcd(q_primitive, factor) == 1)

# A rational root of a primitive polynomial would be a linear factor over
# every prime that does not divide the leading coefficient.
prime = 104729
check("PRIME_DOES_NOT_DIVIDE_COFACTOR_LEADING", int(q_primitive.LC()) % prime != 0)
factored = sp.factor_list(q_primitive, modulus=prime)
degrees = sorted(factor.degree() for factor, mult in factored[1] for _ in range(mult))
print("COFACTOR_DEGREES_MOD", prime, degrees, flush=True)
check("NO_LINEAR_FACTOR_MOD_104729", degrees and min(degrees) > 1)
check("MODULAR_DEGREE_PRESERVED", sum(degrees) == q_primitive.degree())

# Therefore the only rational root of det(M) is s=0, and every chart factor
# is already removed from q. On rational s with open charts, det H = 0
# iff s=0.
open_chart_samples = (R(-3), R(-1), R(1, 3), R(1), R(3, 2), R(3), R(4), R(5))
for value in open_chart_samples:
    charts_open = all(poly.subs(s, value) != 0 for poly in chart_polys)
    check(f"SAMPLE_CHART_OPEN_{value}", charts_open)
    det_h = sp.Rational(int(det_poly.subs(s, value)), int(den_lcm.subs(s, value)) ** 16)
    check(f"SAMPLE_DET_NONZERO_{value}", det_h != 0)


def rational_hessian(value):
    gens = [A_seed[r] + value * (A_chart[r] - A_seed[r]) for r in range(4)]
    roles_v = [owner.cayley(a) for a in gens]
    H = sp.zeros(16)
    for r, ss in owner.PAIRS:
        qface = face_response(roles_v, r, ss)
        u_ax, v_ax = [i for i in range(4) if i not in (r, ss)]
        for k, (a, b) in enumerate(owner.PAIRS):
            for i, j, value_q in ((a, b, qface[k]), (b, a, -qface[k])):
                H[4 * i + u_ax, 4 * j + v_ax] += 16 * value_q
                H[4 * j + v_ax, 4 * i + u_ax] += 16 * value_q
    return sp.Matrix(H), roles_v


def homogeneous_action(theta, roles_v):
    action = 0
    for r, ss in owner.PAIRS:
        ur, us = roles_v[r], roles_v[ss]
        hol = ur * us * ur.inv() * us.inv()
        curv = (hol - hol.inv()) / 2
        response = owner.G2 * owner.STAR * owner.bivector_of_tangent(curv)
        u_ax, v_ax = [i for i in range(4) if i not in (r, ss)]
        sign = owner.orientation((r, ss))
        action += 16 * sign * (owner.wedge(theta[:, u_ax], theta[:, v_ax]).T * response)[0]
    return sp.expand(action)


H_at_1, roles_1 = rational_hessian(R(1))
check("POLY_AGREES_WITH_RATIONAL_HESSIAN_AT_1", H_at_1 == eval_matrix(M, 1) / int(den_lcm.subs(s, 1)))
basis = []
for k in range(16):
    unit = sp.zeros(4)
    unit[k // 4, k % 4] = 1
    basis.append(unit)
polarized = sp.zeros(16)
actions = [homogeneous_action(unit, roles_1) for unit in basis]
for i in range(16):
    polarized[i, i] = sp.expand(2 * actions[i])
    for j in range(i + 1, 16):
        cross = homogeneous_action(basis[i] + basis[j], roles_1) - actions[i] - actions[j]
        polarized[i, j] = polarized[j, i] = sp.expand(cross)
check("HESSIAN_IS_THE_HOMOGENEOUS_ACTION_POLARIZATION", polarized == H_at_1)

H_seed, _ = rational_hessian(R(0))
check("SEED_HESSIAN_RANK_6", H_seed.rank() == 6)
check("SEED_HESSIAN_SINGULAR", H_seed.det() == 0)
flat_roles = [owner.I4 for _ in range(4)]
flat_H = sp.zeros(16)
for r, ss in owner.PAIRS:
    qface = face_response(flat_roles, r, ss)
    u_ax, v_ax = [i for i in range(4) if i not in (r, ss)]
    for k, (a, b) in enumerate(owner.PAIRS):
        for i, j, value_q in ((a, b, qface[k]), (b, a, -qface[k])):
            flat_H[4 * i + u_ax, 4 * j + v_ax] += 16 * value_q
check("FLAT_LINKS_HAVE_ZERO_SOLDER_HESSIAN", flat_H == sp.zeros(16))

def f4_local_block(roles_v):
    """One-site block in the f4 index 4*leg+component."""
    local = sp.zeros(16)
    for r, ss in owner.PAIRS:
        ur, us = roles_v[r], roles_v[ss]
        hol = ur * us * ur.inv() * us.inv()
        curv = (hol - hol.inv()) / 2
        q = owner.orientation((r, ss)) * (
            owner.G2 * owner.STAR * owner.bivector_of_tangent(curv)
        )
        face = sp.zeros(4)
        for value, (a, b) in zip(list(q), owner.PAIRS):
            face[a, b] = value
            face[b, a] = -value
        u_ax, v_ax = [i for i in range(4) if i not in (r, ss)]
        for a in range(4):
            for b in range(4):
                if face[a, b] == 0:
                    continue
                local[4 * u_ax + a, 4 * v_ax + b] += face[a, b]
                local[4 * v_ax + b, 4 * u_ax + a] += face[a, b]
    permuted = sp.zeros(16)
    for p in range(16):
        for q_index in range(16):
            comp_p, leg_p = divmod(p, 4)
            comp_q, leg_q = divmod(q_index, 4)
            permuted[p, q_index] = local[4 * leg_p + comp_p, 4 * leg_q + comp_q]
    return permuted


check("F4_LOCAL_BLOCK_EQUALS_HOMOGENEOUS_OVER_16_AT_1", H_at_1 == 16 * f4_local_block(roles_1))
H_at_3, roles_3 = rational_hessian(R(3))
check("F4_LOCAL_BLOCK_EQUALS_HOMOGENEOUS_OVER_16_AT_3", H_at_3 == 16 * f4_local_block(roles_3))

print("COFACTOR_CONTENT", q_content, flush=True)
print("VALUATION_TUPLE", exponents, flush=True)
print("COFACTOR_DEGREE", q_primitive.degree(), flush=True)
print("DONE", flush=True)
