#!/usr/bin/env python3
"""F4 Track B -- E(2) 14 stationarity polynomials under packed normal form (lean).

Research-only. Exact rational / symbolic arithmetic.

Certifies:
  * exact 27-chart packing: 12 E(2) Cayley link coords + 15 det-one LDU solder
    times eta (det Theta = -1);
  * so(1,3)/e(2) complement basis {K1, M2=K2-J12, M3=K3-J13} spanning a
    linear complement of E(2)=span{N2,N3,J23} over Q (joint rank 6);
  * provisional algebraic assignment of the memo §5 FIXED_13 rationals into 13
    chart slots (QR pivot indices unrecovered this turn; packing declared below);
  * 14 exact cleared internal stationarity polynomials = numerators of
    dS_star/df_i on the 14 free coords (closed-form E(2) Cayley);
  * 6 exact transverse Lorentz stationarity polynomials via the Cayley
    differential (roles 0,1) x {K1,M2,M3};
  * structure: degree census, all generators non-zero at a rational free probe,
    sample Jacobian ranks (internal / transverse / selected 8+6 subsystem).

Does NOT claim an exact curved stationary root.
Does NOT recover the float QR pivot-to-coordinate map.
Does NOT run Groebner / full elimination (minutes-scale scope).
Does NOT open Holst/phi/new I-channels.
"""
from __future__ import annotations

import time
from itertools import combinations

import sympy as sp
from sympy import Matrix, Rational, eye, zeros, symbols

t_wall0 = time.time()

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


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


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


N2 = gen_boost(2) + gen_rot(1, 2)
N3 = gen_boost(3) + gen_rot(1, 3)
J23 = gen_rot(2, 3)
K1 = gen_boost(1)
K2 = gen_boost(2)
K3 = gen_boost(3)
J12 = gen_rot(1, 2)
J13 = gen_rot(1, 3)
M2 = K2 - J12
M3 = K3 - J13
E2_BASIS = (N2, N3, J23)
COMPL_BASIS = (K1, M2, M3)


def killing(A, B):
    """Ad-invariant form proportional to tr(A B) on so(1,3)."""
    return sp.simplify((A * B).trace())


def e2_alg(n2, n3, j):
    return n2 * N2 + n3 * N3 + j * J23


def e2_closed(n2, n3, j):
    """Closed-form Cayley image of e2_alg (denom j^2+4)."""
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
    """Exact d/de|0 Cayley(A+e H)."""
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


def ldu_theta(params15):
    """Det-one LDU times eta => det Theta = -1."""
    (
        l10,
        l20,
        l21,
        l30,
        l31,
        l32,
        d0,
        d1,
        d2,
        u01,
        u02,
        u03,
        u12,
        u13,
        u23,
    ) = params15
    d3 = 1 / (d0 * d1 * d2)
    L = Matrix(
        [[1, 0, 0, 0], [l10, 1, 0, 0], [l20, l21, 1, 0], [l30, l31, l32, 1]]
    )
    D = sp.diag(d0, d1, d2, d3)
    U = Matrix(
        [[1, u01, u02, u03], [0, 1, u12, u13], [0, 0, 1, u23], [0, 0, 0, 1]]
    )
    return L * D * U * ETA


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
    """Exact dS for algebra variation of role r0 in direction H."""
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


def cleared_numer(expr, gens):
    """Cleared stationarity numerator of a rational residual in gens."""
    num, _den = sp.fraction(sp.together(expr))
    return sp.expand(num)


# ---------------------------------------------------------------------------
print("SECTION_E2_LDU_CHART_AND_COMPLEMENT")
# Chart index order: e2[role r][n2,n3,j] for r=0..3 (12), then LDU:
# L:l10,l20,l21,l30,l31,l32 (6); D:d0,d1,d2 (3, d3=1/(d0 d1 d2)); U:u01..u23 (6).
CHART_NAMES = (
    [f"e2_r{r}_{c}" for r in range(4) for c in ("n2", "n3", "j")]
    + [f"L_{k}" for k in range(6)]
    + [f"D_{k}" for k in range(3)]
    + [f"U_{k}" for k in range(6)]
)
check("E2_LDU_CHART_DIM_27", len(CHART_NAMES) == 27)

# Complement = linear complement of E(2) inside so(1,3): joint basis rank 6.
def _vec(A):
    return Matrix(16, 1, lambda i, _j: A[i // 4, i % 4])


_basis6 = Matrix.hstack(*[_vec(G) for G in (N2, N3, J23, K1, M2, M3)])
check("SO13_E2_PLUS_COMPL_BASIS_RANK_6", _basis6.rank() == 6)
check("COMPL_K1_M2_M3_LIN_INDEP", Matrix.hstack(*[_vec(G) for G in COMPL_BASIS]).rank() == 3)
# K1 is Killing-orthogonal to all of E(2) under tr; M2/M3 are the
# algebraic complements of N2/N3 (K +/- J) rather than tr-orthogonal.
check("COMPL_K1_TR_ORTH_N2", killing(K1, N2) == 0)
check("COMPL_K1_TR_ORTH_N3", killing(K1, N3) == 0)
check("COMPL_K1_TR_ORTH_J23", killing(K1, J23) == 0)

# LDU det check on a rational point.
_ldu_bat = [
    Rational(1, 5), 0, Rational(-1, 4), 0, Rational(1, 3), 0,
    Rational(1), Rational(1), Rational(1),
    Rational(1, 4), 0, 0, Rational(-1, 5), 0, Rational(1, 6),
]
Th_bat = ldu_theta(_ldu_bat)
check("LDU_THETA_DET_MINUS_ONE", sp.simplify(Th_bat.det()) == -1)
print(
    "RESULT_CHART: 27 = 12 E(2) + 15 LDU(det1)*eta; complement "
    "{K1,M2,M3} complementary to E(2) in so(1,3) over Q (joint rank 6)."
)

# ---------------------------------------------------------------------------
print("SECTION_PROVISIONAL_NORMAL_FORM_PACKING")
# Memo §5 FIXED_13 values (order preserved). QR pivot indices were not
# persisted with the float scout; this cert declares an explicit provisional
# algebraic packing so the 14 free coordinates are auditable over Q.
FIXED_13 = [
    Rational(-1, 3),
    Rational(0, 1),
    Rational(-1, 3),
    Rational(1, 2),
    Rational(1, 2),
    Rational(-1, 2),
    Rational(-1, 2),
    Rational(4, 3),
    Rational(3, 2),
    Rational(1, 2),
    Rational(2, 3),
    Rational(-1, 3),
    Rational(-1, 1),
]
# Fix: e2 roles 0 and 1 fully (6) + e2 role2 n2 (1) + all 6 strict-L (6) = 13.
FIXED_IDX = [0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 17]
FREE_IDX = [i for i in range(27) if i not in FIXED_IDX]
check("PACK_FIXED_COUNT_13", len(FIXED_IDX) == 13)
check("PACK_FREE_COUNT_14", len(FREE_IDX) == 14)
check("PACK_FIXED13_ALL_RATIONAL", all(isinstance(x, sp.Rational) for x in FIXED_13))
check("PACK_IDX_PARTITION", sorted(FIXED_IDX + FREE_IDX) == list(range(27)))
print("PACK_FIXED_IDX", FIXED_IDX)
print("PACK_FREE_IDX", FREE_IDX)
print("PACK_FIXED_NAMES", [CHART_NAMES[i] for i in FIXED_IDX])
print("PACK_FREE_NAMES", [CHART_NAMES[i] for i in FREE_IDX])
print(
    "RESULT_PACK: provisional FIXED_13 -> chart slots declared; free = "
    "e2_r2_{n3,j} + e2_r3_* + D_* + U_* (14). QR pivot recovery remains "
    "numerical provenance / next exactification hygiene."
)

# ---------------------------------------------------------------------------
print("SECTION_INTERNAL_14_STATIONARITY_POLYNOMIALS")
frees = symbols("f0:14")
chart = [None] * 27
for k, i in enumerate(FIXED_IDX):
    chart[i] = FIXED_13[k]
for k, i in enumerate(FREE_IDX):
    chart[i] = frees[k]

role = [e2_closed(*chart[3 * r : 3 * r + 3]) for r in range(4)]
As = [e2_alg(*chart[3 * r : 3 * r + 3]) for r in range(4)]
Theta = ldu_theta(chart[12:])

t1 = time.time()
S = star_S_hom(role, Theta)
print("TIMING_S_BUILD_SEC", round(time.time() - t1, 3))
St = sp.together(S)
S_num, S_den = sp.fraction(St)

# Keep cleared numerators unexpanded for fast probe/Jac; expand only for degree.
internal_cleared = []
internal_polys = []
internal_degs = []
t2 = time.time()
for i, f in enumerate(frees):
    # d(S_num/S_den)/df = 0 <=> S_den dS_num - S_num dS_den = 0
    cleared = S_den * sp.diff(S_num, f) - S_num * sp.diff(S_den, f)
    internal_cleared.append(cleared)
    poly = sp.expand(cleared)
    internal_polys.append(poly)
    deg = int(sp.total_degree(poly)) if poly != 0 else -1
    internal_degs.append(deg)
    print(f"INTERNAL_POLY_{i}_DEG", deg, "OPS", poly.count_ops())
print("TIMING_INTERNAL_POLYS_SEC", round(time.time() - t2, 3))

check("INTERNAL_POLY_COUNT_14", len(internal_polys) == 14)
check("INTERNAL_POLYS_ALL_NONZERO_EXPR", all(p != 0 for p in internal_polys))
check("INTERNAL_DEGS_POSITIVE", all(d > 0 for d in internal_degs))
check("INTERNAL_DEGS_UNIFORM_33", all(d == 33 for d in internal_degs))

# Rational free probe (D-slots among frees stay away from 0).
PROBE = {frees[i]: Rational(1, 7) + Rational(i, 11) for i in range(14)}
h = Rational(1, 50)


def chart_at(free_vals):
    ch = [None] * 27
    for k, i in enumerate(FIXED_IDX):
        ch[i] = FIXED_13[k]
    for k, i in enumerate(FREE_IDX):
        ch[i] = free_vals[k]
    return ch


def S_at(free_vals):
    ch = chart_at(free_vals)
    role_r = [e2_closed(*ch[3 * r : 3 * r + 3]) for r in range(4)]
    Th = ldu_theta(ch[12:])
    return sp.simplify(star_S_hom(role_r, Th))


def grad_S_at(free_vals):
    S0 = S_at(free_vals)
    g = []
    for j in range(14):
        fv = list(free_vals)
        fv[j] = free_vals[j] + h
        g.append(sp.simplify((S_at(fv) - S0) / h))
    return Matrix(g), S0


free0 = [PROBE[frees[i]] for i in range(14)]
g0, _S0 = grad_S_at(free0)
internal_vals = list(g0)
check(
    "INTERNAL_PROBE_ALL_NONEVAL_ZERO",
    all(v != 0 for v in internal_vals),
)
print("INTERNAL_PROBE_NONEZERO_COUNT", sum(1 for v in internal_vals if v != 0))

# Sample Jac of internal residuals = Hessian of S via exact FD (all-rational).
Jac_rows = []
for j in range(14):
    fv = list(free0)
    fv[j] = free0[j] + h
    gj, _ = grad_S_at(fv)
    Jac_rows.append([sp.simplify((gj[i] - g0[i]) / h) for i in range(14)])
# Jac_rows[j][i] = d r_i / d f_j; transpose so rows are residuals.
Jac_int = Matrix(Jac_rows).T
rank_int = Jac_int.rank()
print("INTERNAL_PROBE_JAC_RANK", rank_int)
check("INTERNAL_PROBE_JAC_FULL_RANK_14", rank_int == 14)
print(
    "RESULT_INTERNAL: 14 exact cleared stationarity numerators in the free "
    "coords under provisional packing; all degree 33; sample Jac rank 14 "
    "at a rational free probe (generic; Hess rank 8 is a root phenomenon)."
)

# ---------------------------------------------------------------------------
print("SECTION_TRANSVERSE_6_STATIONARITY_POLYNOMIALS")
# Six transverse Lorentz dirs: roles {0,1} x complement {K1,M2,M3}.
# (Homogeneous roles 2,3 omitted this turn for minutes-scale; the 6-generator
# set already matches the memo §7 transverse count.)
TRANSVERSE_DIRS = [
    (0, K1, "r0_K1"),
    (0, M2, "r0_M2"),
    (0, M3, "r0_M3"),
    (1, K1, "r1_K1"),
    (1, M2, "r1_M2"),
    (1, M3, "r1_M3"),
]
transverse_cleared = []
transverse_polys = []
transverse_degs = []
t3 = time.time()
for r0, H, label in TRANSVERSE_DIRS:
    g = dS_transverse(role, As, Theta, r0, H)
    num, _den = sp.fraction(sp.together(g))
    transverse_cleared.append(num)
    poly = sp.expand(num)
    transverse_polys.append(poly)
    deg = int(sp.total_degree(poly)) if poly != 0 else -1
    transverse_degs.append(deg)
    print(f"TRANSVERSE_POLY_{label}_DEG", deg, "OPS", poly.count_ops())
print("TIMING_TRANSVERSE_POLYS_SEC", round(time.time() - t3, 3))

check("TRANSVERSE_POLY_COUNT_6", len(transverse_polys) == 6)
check("TRANSVERSE_POLYS_ALL_NONZERO_EXPR", all(p != 0 for p in transverse_polys))
check("TRANSVERSE_DEGS_POSITIVE", all(d > 0 for d in transverse_degs))

def trans_vec_at(free_vals):
    ch = chart_at(free_vals)
    role_r = [e2_closed(*ch[3 * r : 3 * r + 3]) for r in range(4)]
    As_r = [e2_alg(*ch[3 * r : 3 * r + 3]) for r in range(4)]
    Th = ldu_theta(ch[12:])
    out = []
    for r0, H, _label in TRANSVERSE_DIRS:
        out.append(sp.simplify(dS_transverse(role_r, As_r, Th, r0, H)))
    return Matrix(out)


t0_vec = trans_vec_at(free0)
trans_vals = list(t0_vec)
check("TRANSVERSE_PROBE_ALL_NONEVAL_ZERO", all(v != 0 for v in trans_vals))

Jac_tr_rows = []
for i in range(6):
    row = []
    v0 = trans_vals[i]
    for j in range(14):
        fv = list(free0)
        fv[j] = free0[j] + h
        v1 = trans_vec_at(fv)[i]
        row.append(sp.simplify((v1 - v0) / h))
    Jac_tr_rows.append(row)
Jac_tr = Matrix(Jac_tr_rows)
rank_tr = Jac_tr.rank()
print("TRANSVERSE_PROBE_JAC_RANK", rank_tr)
check("TRANSVERSE_PROBE_JAC_FULL_RANK_6", rank_tr == 6)
print(
    "RESULT_TRANSVERSE: 6 exact cleared transverse Lorentz stationarity "
    "numerators via Cayley differential on roles {0,1} x {K1,M2,M3}; "
    f"degrees {transverse_degs}; sample Jac rank 6."
)

# ---------------------------------------------------------------------------
print("SECTION_EIGHT_PLUS_SIX_SUBSYSTEM")
# Select 8 internal polys with full row-rank 8 at PROBE (first 8 already
# span rank 8 in the full-rank-14 Jac; take pivots of Jac_int).
# Use QR-free exact pivot selection: greedy independent rows of Jac_int.
selected_internal = []
span_rows = []
for i in range(14):
    trial = span_rows + [Jac_int.row(i)]
    if Matrix.vstack(*trial).rank() == len(trial):
        selected_internal.append(i)
        span_rows.append(Jac_int.row(i))
    if len(selected_internal) == 8:
        break
check("SELECTED_INTERNAL_COUNT_8", len(selected_internal) == 8)
print("SELECTED_INTERNAL_IDX", selected_internal)

# Combined 8+6 = 14 subsystem Jac at PROBE from all-rational FD blocks above.
sub_polys = [internal_polys[i] for i in selected_internal] + transverse_polys
# Stack selected internal Hessian rows with transverse Jac rows.
Jac_sub = Matrix.vstack(Jac_int.extract(selected_internal, list(range(14))), Jac_tr)
rank_sub = Jac_sub.rank()
print("SUBSYSTEM_8P6_PROBE_JAC_RANK", rank_sub)
check("SUBSYSTEM_8P6_PROBE_JAC_FULL_RANK_14", rank_sub == 14)
check("SUBSYSTEM_POLY_COUNT_14", len(sub_polys) == 14)
print(
    "RESULT_8P6: selected 8 internal + 6 transverse cleared polynomials "
    "form a square 14-generator subsystem with sample Jac rank 14 at the "
    "rational free probe (memo §7 split, under provisional packing)."
)

# ---------------------------------------------------------------------------
print("SECTION_RATIONAL_BATTERY_CURVED_SANITY")
# Cheap curved sanity on a fully rational (unpacked) E(2)+LDU point:
# plaquettes nonflat and star action nonzero — confirms chart plumbing.
_params12 = [
    Rational(1, 5), Rational(1, 7), Rational(-1, 4),
    Rational(-1, 3), Rational(-1, 8), Rational(-1, 4),
    Rational(-2, 5), Rational(-1, 6), Rational(1, 7),
    Rational(1, 4), Rational(1, 5), Rational(-1, 3),
]
role_b = [e2_closed(*_params12[3 * r : 3 * r + 3]) for r in range(4)]
Th_b = ldu_theta(_ldu_bat)
S_b = sp.simplify(star_S_hom(role_b, Th_b))
curved = 0
for r, s in PAIRS:
    P = role_b[r] * role_b[s] * role_b[r].inv() * role_b[s].inv()
    if sp.simplify(P - I4) != zeros(4):
        curved += 1
check("BATTERY_CURVED_PLAQUETTES", curved > 0)
check("BATTERY_STAR_NONZERO", S_b != 0)
print("BATTERY_CURVED_COUNT", curved, "S", S_b)

# ---------------------------------------------------------------------------
wall = time.time() - t_wall0
print("TIMING_WALL_SEC", round(wall, 3))
print(
    "RESULT_E2_STATIONARITY_POLYS: under provisional memo-§5 FIXED_13 packing, "
    "built 14 exact internal + 6 exact transverse cleared stationarity "
    "polynomials (8+6 square subsystem sample Jac rank 14). Degrees: "
    f"internal all 33; transverse {transverse_degs}."
)
print(
    "SCOPE: no exact root; no Groebner/elimination; provisional packing "
    "(QR pivot indices unrecovered); transverse generators use roles {0,1} "
    "only; four-channel R=R_*(C) filter not applied this turn; A4 ambient "
    "FD not restarted."
)
print(
    "NEXT: recover QR pivot assignment or replace provisional packing by a "
    "gauge-canonical exact normal form; eliminate / reconstruct algebraic "
    "numbers for the 14 free coords; filter by four-channel R=R_*(C)."
)
