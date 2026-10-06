#!/usr/bin/env python3
"""Exact full Lorentz-link transverse audit of the enlarged parabolic family.

Derives all 12 analytic Lorentz-complement directions {K1,N2,N3} x Roles 0..3
for the subgroup actually represented by e2_closed, namely span{M2,M3,-J23},
on e2=(0,0,j,0,0,j,gamma,delta,0,delta,-gamma,0). Exact SymPy rational
algebra; only Cayley chart units are removed. No finite differences or float roots.
"""
from __future__ import annotations

import hashlib
import time
from pathlib import Path
from itertools import combinations

import sympy as sp
from sympy import Matrix, Rational, eye, zeros, together, simplify

t_wall0 = time.time()
WALL_SEC = 240


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def elapsed():
    return time.time() - t_wall0


def abort_if(msg):
    if elapsed() > WALL_SEC:
        raise SystemExit(f"ABORT_WALL: {msg} elapsed={elapsed():.1f}s")


# ---------------------------------------------------------------------------
ETA = sp.diag(1, -1, -1, -1)
I4 = eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
STAR = zeros(6)
STAR_MAP = {
    (0, 1): ((2, 3), -1),
    (0, 2): ((1, 3), +1),
    (0, 3): ((1, 2), -1),
    (1, 2): ((0, 3), +1),
    (1, 3): ((0, 2), -1),
    (2, 3): ((0, 1), +1),
}
for p, (q, s) in STAR_MAP.items():
    STAR[PINDEX[q], PINDEX[p]] = s


def gen_boost(i):
    A = zeros(4)
    A[0, i] = 1
    A[i, 0] = 1
    return A


def gen_rot(i, j):
    A = zeros(4)
    A[i, j] = -1
    A[j, i] = 1
    return A


N2 = gen_boost(2) + gen_rot(1, 2)
N3 = gen_boost(3) + gen_rot(1, 3)
J23 = gen_rot(2, 3)
K1 = gen_boost(1)
M2 = gen_boost(2) - gen_rot(1, 2)
M3 = gen_boost(3) - gen_rot(1, 3)
COMPL = (K1, N2, N3)
INTERNAL = (M2, M3, -J23)
TRANS_LABELS = ["r0_K1", "r0_N2", "r0_N3", "r1_K1", "r1_N2", "r1_N3"]
LIE_BASIS = (K1, N2, N3, M2, M3, -J23)
LIE_BASIS_MATRIX = Matrix.hstack(*[H.reshape(16, 1) for H in LIE_BASIS])
check("LIE_COMPLEMENT_AND_SUBGROUP_BASIS_RANK_6", LIE_BASIS_MATRIX.rank() == 6)


def e2_alg(n2, n3, j):
    return n2 * M2 + n3 * M3 - j * J23


def e2_closed(n2, n3, j):
    d = j * j + 4
    return Matrix(
        [
            [
                (j * j + 2 * n2 * n2 + 2 * n3 * n3 + 4) / d,
                2 * (-n2 * n2 - n3 * n3) / d,
                2 * (-j * n3 + 2 * n2) / d,
                2 * (j * n2 + 2 * n3) / d,
            ],
            [
                2 * (n2 * n2 + n3 * n3) / d,
                (j * j - 2 * n2 * n2 - 2 * n3 * n3 + 4) / d,
                2 * (-j * n3 + 2 * n2) / d,
                2 * (j * n2 + 2 * n3) / d,
            ],
            [
                2 * (j * n3 + 2 * n2) / d,
                2 * (-j * n3 - 2 * n2) / d,
                (4 - j * j) / d,
                4 * j / d,
            ],
            [
                2 * (-j * n2 + 2 * n3) / d,
                2 * (j * n2 - 2 * n3) / d,
                -4 * j / d,
                (4 - j * j) / d,
            ],
        ]
    )


def cayley_diff(A, H):
    B = I4 - A / 2
    Binv = B.inv()
    P = (I4 + A / 2) * Binv
    halfH = H / 2
    return halfH * Binv + P * halfH * Binv


def orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def wedge(u, v):
    return Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def bivector_of_tangent(X):
    Y = X * ETA
    return Matrix([Y[a, b] for a, b in PAIRS])


def curvature(P):
    return (P - P.inv()) / 2


def d_curvature(P, dP):
    Pinv = P.inv()
    return (dP + Pinv * dP * Pinv) / 2


def star_S_hom(role, Theta):
    vs = [Theta[:, r] for r in range(4)]
    site = 0
    for r, s in PAIRS:
        P = role[r] * role[s] * role[r].inv() * role[s].inv()
        C = bivector_of_tangent(curvature(P))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * (
            wedge(vs[u], vs[v]).T * G2 * STAR * C
        )[0]
    return 16 * site


def dS_transverse(role, As, Theta, r0, H):
    dP0 = cayley_diff(As[r0], H)
    vs = [Theta[:, r] for r in range(4)]
    site = 0
    for r, s in PAIRS:
        Ur, Us = role[r], role[s]
        Uri, Usi = Ur.inv(), Us.inv()
        dUr = dP0 if r == r0 else zeros(4)
        dUs = dP0 if s == r0 else zeros(4)
        dUri = (-Uri * dUr * Uri) if r == r0 else zeros(4)
        dUsi = (-Usi * dUs * Usi) if s == r0 else zeros(4)
        dP = (
            dUr * Us * Uri * Usi
            + Ur * dUs * Uri * Usi
            + Ur * Us * dUri * Usi
            + Ur * Us * Uri * dUsi
        )
        P = Ur * Us * Uri * Usi
        dC = bivector_of_tangent(d_curvature(P, dP))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * (
            wedge(vs[u], vs[v]).T * G2 * STAR * dC
        )[0]
    return 16 * site



# ---------------------------------------------------------------------------
def family_e2(j, gamma, delta):
    z = Rational(0)
    return [z, z, j, z, z, j, gamma, delta, z, delta, -gamma, z]


def embed_e2(e2_12):
    role = [e2_closed(*e2_12[3 * r : 3 * r + 3]) for r in range(4)]
    As = [e2_alg(*e2_12[3 * r : 3 * r + 3]) for r in range(4)]
    return role, As, ETA

print("SECTION_FULL_TRANSVERSE_SYMBOLIC")
j, gamma, delta = sp.symbols("j gamma delta", real=True)
e2_sym = family_e2(j, gamma, delta)
role_sym, As_sym, Theta = embed_e2(e2_sym)
labels = ("K1", "N2", "N3")
print("SECTION_CAYLEY_CONVENTION_AUDIT")
for r0 in range(4):
    A = As_sym[r0]
    P_from_A = (I4 + A/2) * (I4 - A/2).inv()
    check(f"ROLE_{r0}_CLOSED_FORM_MATCHES_CAYLEY_ALGEBRA", all(
        sp.factor(x) == 0 for x in (P_from_A - role_sym[r0])
    ))
wrong_alg = [e2_sym[3*r] * N2 + e2_sym[3*r+1] * N3 + e2_sym[3*r+2] * J23 for r in range(4)]
wrong_P_role2 = (I4 + wrong_alg[2]/2) * (I4 - wrong_alg[2]/2).inv()
check("LEGACY_N_BASIS_DOES_NOT_REPRESENT_ROLE_2_MATRIX", any(
    sp.factor(x) != 0 for x in (wrong_P_role2 - role_sym[2])
))
print("REPRESENTED_SUBGROUP", "span{M2,M3,-J23}; complement={K1,N2,N3}")
legacy_expected = [(-32, -16, 32), (32, 0, -16)]
legacy_rows = []
for r0 in (2, 3):
    vals = [sp.factor(dS_transverse(role_sym, wrong_alg, Theta, r0, H).subs({j: 2, gamma: 0, delta: 1})) for H in (K1, M2, M3)]
    legacy_rows.append(tuple(vals))
    print(f"LEGACY_MISMATCHED_BASE_ROLE_{r0}_K1_M2_M3", [str(v) for v in vals], "INVALID_AS_EULER")
check("REQUESTED_LEGACY_ROWS_REPRODUCED_ONLY_WITH_MISMATCHED_BASE", legacy_rows == legacy_expected)
transverse = {}
for r0 in range(4):
    for H, lab in zip(COMPL, labels):
        abort_if(f"symbolic role={r0} {lab}")
        value = sp.factor(sp.cancel(together(dS_transverse(role_sym, As_sym, Theta, r0, H))))
        numerator, denominator = sp.fraction(value)
        numerator, denominator = sp.factor(numerator), sp.factor(denominator)
        transverse[(r0, lab)] = (value, numerator, denominator)
        print(f"TRANSVERSE_ROLE_{r0}_{lab}_DENOM_UNIT", denominator)
        print(f"TRANSVERSE_ROLE_{r0}_{lab}_NUM", numerator)
        if lab == "K1":
            check(f"ROLE_{r0}_{lab}_K1_ZERO", numerator == 0)
        else:
            check(f"ROLE_{r0}_{lab}_{lab}_NONZERO_POLYNOMIAL", numerator != 0)

print("SECTION_INTERNAL_E2_SYMBOLIC")
internal = {}
internal_labels = ("M2", "M3", "-J23")
for r0 in range(4):
    for H, lab in zip(INTERNAL, internal_labels):
        abort_if(f"internal role={r0} {lab}")
        value = sp.factor(sp.cancel(together(dS_transverse(role_sym, As_sym, Theta, r0, H))))
        internal[(r0, lab)] = value
        print(f"INTERNAL_ROLE_{r0}_{lab}", value)
        check(f"INTERNAL_ROLE_{r0}_{lab}_ZERO", value == 0)

# The old six checks used M2/M3, which are tangent to this represented
# subgroup.  We do not relabel them as transverse; the actual complement is N2/N3.
check("ACTUAL_SUBGROUP_INTERNAL_DERIVATIVES_ZERO", all(v == 0 for v in internal.values()))

print("SECTION_EXACT_WITNESS")
witness = {j: Rational(2), gamma: Rational(0), delta: Rational(1)}
for r0 in range(4):
    values = [sp.factor(transverse[(r0, h)][0].subs(witness)) for h in labels]
    print(f"WITNESS_ROLE_{r0}_K1_N2_N3", [str(v) for v in values])
    expected = [(0,-16,0), (0,16,0), (0,-32,64), (0,0,-32)][r0]
    check(f"WITNESS_ROLE_{r0}_EXACT", values == list(expected))

print("SECTION_MISSING_NUMERATORS_AND_ELIMINATION")
missing = [transverse[(r, h)][1] for r in range(4) for h in labels]
# Remove only nonzero rational constants and positive Cayley chart units j^2+4.
# Here each denominator must factor over Q as a rational constant times a power
# of (j^2+4); no gamma/delta factor is cancelled.
for r in range(4):
    for h in labels:
        den = transverse[(r,h)][2]
        den_q = sp.factor(den / (j*j + 4)) if den.has(j) else den
        print(f"DENOM_CHECK_ROLE_{r}_{h}", den, "reduced_constant", den_q)
        check(f"CHART_UNIT_ONLY_ROLE_{r}_{h}", den_q == 1)

# Four exact role-2/3 numerator equations already force the only full-star
# stationary point on the family.  The denominator D=j^2+4 is a positive
# Cayley chart unit over the reals and is never cancelled with gamma/delta.
D = j*j + 4
f_gamma_2 = sp.factor(transverse[(2, "N2")][1] / 32)
f_gamma_3 = sp.factor(-transverse[(3, "N3")][1] / 32)
f_delta_2 = sp.factor(transverse[(2, "N3")][1] / 32)
f_delta_3 = sp.factor(transverse[(3, "N2")][1] / 32)
print("CORE_ROLE23_EQUATIONS", [str(x) for x in (f_gamma_2, f_gamma_3, f_delta_2, f_delta_3)])
check("CORE_GAMMA_EQUATIONS_EXACT", sp.factor(f_gamma_2 - (gamma*D - 2*j*j)) == 0 and sp.factor(f_gamma_3 - (gamma*D + 2*j*j)) == 0)
check("CORE_DELTA_EQUATIONS_EXACT", sp.factor(f_delta_2 - (delta*D + 4*j)) == 0 and sp.factor(f_delta_3 - (delta*D - 4*j)) == 0)
combos = [sp.factor(f_gamma_2 + f_gamma_3), sp.factor(f_gamma_2 - f_gamma_3),
          sp.factor(f_delta_2 + f_delta_3), sp.factor(f_delta_2 - f_delta_3)]
print("CORE_EQUATION_COMBINATIONS", [str(x) for x in combos])
check("CORE_COMBOS_FORCE_ORIGIN", all(sp.factor(a-b) == 0 for a,b in zip(combos, [2*gamma*D, -4*j*j, 2*delta*D, 8*j])))
print("FULL_STAR_ZERO_SET_ON_FAMILY", "role-2/3 transverse equations imply j=0, gamma=0, delta=0 over R")
print("J_ZERO_CORE_EQUATIONS", [str(sp.factor(x.subs(j, 0))) for x in (f_gamma_2, f_gamma_3, f_delta_2, f_delta_3)])

print("SECTION_FLAT_ACTION_AND_CURVATURE")
S = sp.factor(sp.cancel(together(star_S_hom(role_sym, Theta))))
print("STAR_ACTION_ON_FAMILY", S)
check("STAR_ACTION_ZERO_ON_FAMILY", S == 0)
curv2 = 0
for r,s in PAIRS:
    P = role_sym[r] * role_sym[s] * role_sym[r].inv() * role_sym[s].inv()
    C = curvature(P)
    curv2 += sum(C[a,b]**2 for a in range(4) for b in range(4))
curv2 = sp.factor(sp.cancel(together(curv2)))
expected_curv2 = 64*j**2*(gamma**2+delta**2)/(j**2+4)
print("CURVATURE2_ON_FAMILY", curv2)
check("CURVATURE2_EXACT_FORMULA", sp.factor(curv2-expected_curv2) == 0)
check("J_ZERO_CURVATURE_IDENTICALLY_ZERO", sp.factor(curv2.subs(j, 0)) == 0)
flat_line_N2 = sp.factor(transverse[(2, "N3")][0].subs({gamma: 0, delta: 0}))
print("FLAT_CONFIG_LINE_ROLE2_N3_EULER", flat_line_N2)
check("FLAT_J_LINE_NOT_CRITICAL_EXCEPT_ORIGIN", sp.factor(flat_line_N2 - 128*j/(j*j+4)) == 0)
origin = {j: 0, gamma: 0, delta: 0}
check("ALL_24_LINK_DERIVATIVES_ZERO_AT_ORIGIN",
      all(v.subs(origin) == 0 for v in internal.values()) and
      all(v.subs(origin) == 0 for v, _, _ in transverse.values()))
print("BOXED: E2-ENLARGED-PARABOLIC-FAMILY-FULL-TRANSVERSE-CURVED-NOGO")
print("TIMING_WALL_SEC", round(elapsed(), 3))
check("WALL_UNDER_240S", elapsed() < WALL_SEC)
print("CERT_SHA256", hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
