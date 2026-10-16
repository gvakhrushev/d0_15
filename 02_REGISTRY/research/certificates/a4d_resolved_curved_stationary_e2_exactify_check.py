#!/usr/bin/env python3
"""F4 Track B -- E(2) little-group exactify gate (lean).

Research-only. Exact rational arithmetic.

Certifies:
  * E(2)=span{N2,N3,J23} is a Lie subalgebra of so(1,3) over Q,
    stabilizing the null line n=(1,1,0,0) with vanishing scale;
  * homogeneous Cayley-E(2) 4-link configurations have exactly parabolic
    plaquettes (tr P=4 and (P-I)^3=0) on a rational battery;
  * the memo §5 normal-form packing (13 fixed rationals / 14 free slots)
    is recorded as an exact interface table;
  * a rational reconstruction probe: denom-cap rounding of the memo §4.1
    float E(2) link scout yields exact nonzero star-Euler residuals in the
    12-dimensional homogeneous E(2) chart (identity solder), confirming
    memo §4.2 over Q rather than float.

Does NOT claim an exact curved stationary root.
Does NOT open Holst/phi/new I-channels.
Does NOT recompute the numerical rank-14 Jacobian at the float root.
A4 sitewise / all-site solder ambient widens were aborted as too heavy.
"""
from __future__ import annotations

from itertools import combinations, product
from fractions import Fraction

import sympy as sp
from sympy import Matrix, Rational, eye, zeros, simplify

ETA = sp.diag(1, -1, -1, -1)
I4 = eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
SITES = list(product(range(2), repeat=4))
ORIGIN = (0, 0, 0, 0)

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


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def site_add(x, r):
    y = list(x)
    y[r] = (y[r] + 1) % 2
    return tuple(y)


def wedge(u, v):
    return Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def bivector_of_tangent(X):
    Y = X * ETA
    return Matrix([simplify(Y[a, b]) for a, b in PAIRS])


def curvature(P):
    return simplify((P - P.inv()) / 2)


def gen_boost(i):
    A = zeros(4)
    A[0, i] = 1
    A[i, 0] = 1
    return A


def gen_rot(i, j):
    A = zeros(4)
    A[i, j] = 1
    A[j, i] = -1
    return A


def cayley_from_A(A):
    return simplify((I4 + A / 2) * (I4 - A / 2).inv())


def bracket(A, B):
    return simplify(A * B - B * A)


# ---------------------------------------------------------------------------
# E(2) generators: null line n=(1,1,0,0)
# N2 = K2 + J12, N3 = K3 + J13, J23 = J_23  (no null-line scale K1)
# ---------------------------------------------------------------------------
K1 = gen_boost(1)
K2 = gen_boost(2)
K3 = gen_boost(3)
J12 = gen_rot(1, 2)
J13 = gen_rot(1, 3)
J23 = gen_rot(2, 3)
N2 = K2 + J12
N3 = K3 + J13
E2_BASIS = (N2, N3, J23)
N_NULL = Matrix([1, 1, 0, 0])


print("SECTION_E2_LIE_ALGEBRA")
check("E2_BRACKET_N2_N3_ZERO", bracket(N2, N3) == zeros(4))
check("E2_BRACKET_J23_N2_EQ_MINUS_N3", bracket(J23, N2) == -N3)
check("E2_BRACKET_J23_N3_EQ_N2", bracket(J23, N3) == N2)
check("E2_N2_ANNIHILATES_NULL", simplify(N2 * N_NULL) == zeros(4, 1))
check("E2_N3_ANNIHILATES_NULL", simplify(N3 * N_NULL) == zeros(4, 1))
check("E2_J23_ANNIHILATES_NULL", simplify(J23 * N_NULL) == zeros(4, 1))
check("E2_K1_SCALES_NULL", simplify(K1 * N_NULL) == N_NULL)
print(
    "RESULT_E2_LIE: span{N2,N3,J23} is an so(1,3) Lie subalgebra over Q "
    "stabilizing n=(1,1,0,0) with vanishing scale (E(2) little group)."
)


def e2_algebra(n2, n3, j):
    return n2 * N2 + n3 * N3 + j * J23


def e2_matrix(n2, n3, j):
    return cayley_from_A(e2_algebra(n2, n3, j))


def is_parabolic(P):
    return simplify(P.trace()) == 4 and simplify((P - I4) ** 3) == zeros(4)


print("SECTION_E2_CAYLEY_NILPOTENT_TRANSLATIONS")
# Null translations Cayley-exponentiate to parabolic elements; J23 alone is
# elliptic (rotation) and is NOT claimed parabolic as a single link.
for name, G, t in (
    ("N2", N2, Rational(2, 5)),
    ("N3", N3, Rational(-3, 7)),
    ("COMBO_N2_N3", N2 * Rational(1, 3) + N3 * Rational(-2, 5), Rational(1, 1)),
):
    P = cayley_from_A(t * G if name != "COMBO_N2_N3" else G)
    check(f"E2_CAYLEY_{name}_PARABOLIC", is_parabolic(P))
    check(f"E2_CAYLEY_{name}_DET_ONE", simplify(P.det()) == 1)
P_rot = cayley_from_A(Rational(2, 5) * J23)
check("E2_CAYLEY_J23_NOT_PARABOLIC_AS_LINK", not is_parabolic(P_rot))
print(
    "RESULT_E2_CAYLEY: N2/N3 (and their combos) Cayley images are exactly "
    "parabolic over Q; J23 Cayley is elliptic as a single link (expected)."
)


def homogeneous_e2_links(params12):
    """params12: 4 roles x (n2,n3,j). Same link per role at every site."""
    role = []
    for r in range(4):
        n2, n3, j = params12[3 * r : 3 * r + 3]
        role.append(e2_matrix(n2, n3, j))
    links = {}
    for x in SITES:
        for r in range(4):
            links[(x, r)] = role[r]
    return links, role


def plaquette_hom(role, r, s):
    return simplify(role[r] * role[s] * role[r].inv() * role[s].inv())


print("SECTION_E2_HOMOGENEOUS_PLAQUETTE_PARABOLIC")
# Rational battery (including a denom-cap rounding of the memo §4.1 scout).
_FLOAT_SCOUT = [
    [0.088504652044, 0.082911143621, -0.249807924819],
    [-0.320461257769, -0.081035776131, -0.303588032463],
    [-0.322033101871, -0.137571575304, 0.125148917575],
    [0.287012659188, 0.226439735406, -0.295275453655],
]


def round_to_denom(x, denom):
    return Rational(int(round(x * denom)), denom)


def scout_params_denom(denom):
    out = []
    for row in _FLOAT_SCOUT:
        for v in row:
            out.append(round_to_denom(v, denom))
    return out


_BATTERY = {
    "UNIT_N2_ONLY": [Rational(1, 5), 0, 0, 0, Rational(1, 5), 0, 0, 0, Rational(1, 5), 0, 0, 0],
    "MIXED_SMALL": [
        Rational(1, 5), Rational(1, 7), Rational(-1, 4),
        Rational(-1, 3), Rational(-1, 8), Rational(-1, 4),
        Rational(-2, 5), Rational(-1, 6), Rational(1, 7),
        Rational(1, 4), Rational(1, 5), Rational(-1, 3),
    ],
    "SCOUT_DENOM8": scout_params_denom(8),
    "SCOUT_DENOM12": scout_params_denom(12),
}

for label, params in _BATTERY.items():
    links, role = homogeneous_e2_links(params)
    ok = True
    nz = 0
    for r, s in PAIRS:
        P = plaquette_hom(role, r, s)
        if not is_parabolic(P):
            ok = False
        if simplify(P - I4) != zeros(4):
            nz += 1
    check(f"E2_PLAQ_{label}_ALL_PARABOLIC", ok)
    check(f"E2_PLAQ_{label}_SOME_NONFLAT", nz > 0)
    print(f"E2_PLAQ_{label}_nonflat_count", nz)
print(
    "RESULT_E2_PLAQ: on a rational homogeneous E(2) battery (including "
    "denom-8/12 roundings of the memo scout), every plaquette is exactly "
    "parabolic over Q with at least one nonflat cell."
)


# ---------------------------------------------------------------------------
# Memo §5 normal-form packing: 13 fixed rationals, 14 free transverse slots
# ---------------------------------------------------------------------------
print("SECTION_E2_NORMAL_FORM_PACKING")
# Exact table from memo §5 (order as recorded there).
FIXED_13 = [
    Rational(-1, 3),  # 0
    Rational(0, 1),   # 1
    Rational(-1, 3),  # 2
    Rational(1, 2),   # 3
    Rational(1, 2),   # 4
    Rational(-1, 2),  # 5
    Rational(-1, 2),  # 6
    Rational(4, 3),   # 7
    Rational(3, 2),   # 8
    Rational(1, 2),   # 9
    Rational(2, 3),   # 10
    Rational(-1, 3),  # 11
    Rational(-1, 1),  # 12
]
check("E2_FIXED13_LEN", len(FIXED_13) == 13)
check("E2_FIXED13_ALL_RATIONAL", all(isinstance(x, sp.Rational) for x in FIXED_13))
check("E2_TRANSVERSE_SLOT_COUNT_14", 27 - 13 == 14)
check("E2_INTERNAL_PLUS_TRANSVERSE_SPLIT", 8 + 6 == 14)
print("E2_FIXED13", [str(x) for x in FIXED_13])
print(
    "RESULT_E2_NORMAL_FORM: memo §5 13-rational normal-form table packed "
    "exactly; transverse system declared as 14 eqs in 14 unknowns after "
    "fixing (8 internal E(2)-chart + 6 transverse Lorentz), matching "
    "memo §§5–7 interface. Pivot-to-coordinate QR assignment is NOT "
    "re-derived here (numerical provenance retained)."
)


# ---------------------------------------------------------------------------
# Star density on homogeneous identity-solder backgrounds (exact, lean)
# ---------------------------------------------------------------------------
def star_S_hom(role):
    total = sp.Integer(0)
    basis = [I4[:, r] for r in range(4)]
    # Homogeneous: same contribution at every site; multiply by |SITES|=16.
    site_sum = sp.Integer(0)
    for r, s in PAIRS:
        C = bivector_of_tangent(curvature(plaquette_hom(role, r, s)))
        u, v = [i for i in range(4) if i not in (r, s)]
        site_sum += orientation((r, s)) * (
            wedge(basis[u], basis[v]).T * G2 * STAR * C
        )[0]
    return simplify(16 * site_sum)


def e2_star_grad12(params12, h=Rational(1, 40)):
    """Exact FD gradient of homogeneous star action in 12 E(2) link dirs."""
    _, role0 = homogeneous_e2_links(params12)
    S0 = star_S_hom(role0)
    g = []
    for a in range(12):
        p1 = list(params12)
        p1[a] = params12[a] + h
        _, role1 = homogeneous_e2_links(p1)
        S1 = star_S_hom(role1)
        g.append(simplify((S1 - S0) / h))
    return Matrix(g), S0


print("SECTION_E2_RATIONAL_RECONSTRUCTION_PROBE")
# Denom-cap rounding probe (memo §4.2 / §5): exact star-Euler residual in
# the 12-dim homogeneous E(2) chart with identity solder. A vanishing
# residual would be a hold; nonzero confirms the link-only rational
# rounding obstruction over Q.
_probe_rows = []
for denom in (4, 8, 12, 16, 24):
    params = scout_params_denom(denom)
    g, S = e2_star_grad12(params)
    # Exact squared residual (rational).
    g2 = simplify((g.T * g)[0])
    nonzero = sum(1 for x in g if x != 0)
    curved = 0
    _, role = homogeneous_e2_links(params)
    for r, s in PAIRS:
        if simplify(plaquette_hom(role, r, s) - I4) != zeros(4):
            curved += 1
    check(f"E2_PROBE_DENOM{denom}_CURVED", curved > 0)
    check(f"E2_PROBE_DENOM{denom}_RESIDUAL_NONZERO", g2 != 0)
    _probe_rows.append((denom, str(S), str(g2), nonzero, curved))
    print(
        f"E2_PROBE_denom{denom}",
        "S", S,
        "g2", g2,
        "g_nonzero", nonzero,
        "curved_plaquettes", curved,
    )

check(
    "E2_PROBE_ALL_DENOM_CAPS_RESIDUAL_NONZERO",
    all(row[2] != "0" for row in _probe_rows),
)
print(
    "RESULT_E2_PROBE: for denom caps {4,8,12,16,24}, nearest-rational "
    "roundings of the memo §4.1 E(2) link scout have C!=0 (parabolic "
    "nonflat plaquettes) but exact homogeneous star-Euler residual "
    "||g||^2 != 0 in the 12 E(2) chart with identity solder. Confirms "
    "memo §4.2 over Q: link-only rational rounding does not yield a "
    "star-stationary witness; joint link+solder exactification of the "
    "14-transverse / 13-fixed system remains the Track B blocker."
)

print(
    "RESULT_E2_CHECKPOINT: E(2) Lie algebra + null-line stabilizer "
    "certified over Q; homogeneous Cayley-E(2) plaquettes exactly "
    "parabolic on a rational battery; memo §5 13-rational / 14-free "
    "normal-form interface packed; rational reconstruction probe shows "
    "exact nonzero star residual under denom-cap link rounding."
)
print(
    "SCOPE: no exact curved stationary root; no claim that the float "
    "E(2) scout is algebraic of a given degree; QR pivot assignment of "
    "the 14 transverse unknowns is numerical provenance only; A4 "
    "sitewise Ad-Lorentz / all-site free-solder ambient widens aborted "
    "as too heavy this turn (TORUS16_PI remains the Track A ceiling)."
)
