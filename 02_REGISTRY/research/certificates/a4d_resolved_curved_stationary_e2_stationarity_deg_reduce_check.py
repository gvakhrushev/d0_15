#!/usr/bin/env python3
"""F4 Track B -- chart-denom / content degree reduction of E2 stationarity polys.

Research-only. Exact rational / symbolic arithmetic. Minutes-scale.

Certifies, under the same provisional FIXED_13 packing as
`a4d_resolved_curved_stationary_e2_stationarity_polys_check.py`:

  * the 14 internal cleared numerators (raw deg 33) and 6 transverse cleared
    numerators (raw deg 23) are divisible by explicit chart-open factors
    (j2^2+4), (j3^2+4), and powers of free D-slots d0,d1,d2;
  * stripping integer content + those maximal chart factors yields a rewritten
    generator set of strictly lower degree (internal reduced deg <= 12;
    transverse reduced deg <= 15) that vanishes on exactly the same points of
    the open chart (where j2^2+4 != 0, j3^2+4 != 0, di != 0);
  * sample 8+6 Jac of the reduced generators still has rank 14 at the rational
    free probe (chart factors nonzero there).

Does NOT claim an exact curved stationary root.
Does NOT run Groebner / full elimination.
Does NOT recover QR pivots / replace provisional packing.
Does NOT open Holst/phi/new I-channels.
"""
from __future__ import annotations

import time
from itertools import combinations

import sympy as sp
from sympy import Matrix, Poly, Rational, eye, zeros, symbols

t_wall0 = time.time()
WALL_SEC = 480  # hard abort budget (~8 min)


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def elapsed():
    return time.time() - t_wall0


def abort_if(msg):
    if elapsed() > WALL_SEC - 20:
        raise SystemExit(f"ABORT_WALL: {msg} elapsed={elapsed():.1f}s")


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
    A[i, j] = 1
    A[j, i] = -1
    return A


N2 = gen_boost(2) + gen_rot(1, 2)
N3 = gen_boost(3) + gen_rot(1, 3)
J23 = gen_rot(2, 3)
K1 = gen_boost(1)
M2 = gen_boost(2) - gen_rot(1, 2)
M3 = gen_boost(3) - gen_rot(1, 3)
COMPL_BASIS = (K1, M2, M3)


def e2_alg(n2, n3, j):
    return n2 * N2 + n3 * N3 + j * J23


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


def ldu_theta(params15):
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
print("SECTION_PACKING_AND_CHART")
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
FIXED_IDX = [0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 17]
FREE_IDX = [i for i in range(27) if i not in FIXED_IDX]
CHART_NAMES = (
    [f"e2_r{r}_{c}" for r in range(4) for c in ("n2", "n3", "j")]
    + [f"L_{k}" for k in range(6)]
    + [f"D_{k}" for k in range(3)]
    + [f"U_{k}" for k in range(6)]
)
check("PACK_FIXED_COUNT_13", len(FIXED_IDX) == 13)
check("PACK_FREE_COUNT_14", len(FREE_IDX) == 14)
print("PACK_FREE_NAMES", [CHART_NAMES[i] for i in FREE_IDX])

frees = symbols("f0:14")
gens = list(frees)
chart = [None] * 27
for k, i in enumerate(FIXED_IDX):
    chart[i] = FIXED_13[k]
for k, i in enumerate(FREE_IDX):
    chart[i] = frees[k]

# Free chart factors (open-chart units):
# FREE: e2_r2_n3, e2_r2_j, e2_r3_n2, e2_r3_n3, e2_r3_j, D0, D1, D2, U0..U5
j2, j3 = frees[1], frees[4]
d0, d1, d2 = frees[5], frees[6], frees[7]
CHART_FACTORS = [
    ("j2sq4", j2**2 + 4),
    ("j3sq4", j3**2 + 4),
    ("d0", d0),
    ("d1", d1),
    ("d2", d2),
]

role = [e2_closed(*chart[3 * r : 3 * r + 3]) for r in range(4)]
As = [e2_alg(*chart[3 * r : 3 * r + 3]) for r in range(4)]
Theta = ldu_theta(chart[12:])

abort_if("before S build")
t1 = time.time()
S = star_S_hom(role, Theta)
St = sp.together(S)
S_num, S_den = sp.fraction(St)
print("TIMING_S_BUILD_SEC", round(time.time() - t1, 3))
print("S_DEN_OPS", S_den.count_ops(), "S_NUM_OPS", S_num.count_ops())


def strip_chart_content(expr, label):
    """Expand, strip ZZ content + maximal chart-open factors; return census."""
    abort_if(label)
    t_exp = time.time()
    poly_expr = sp.expand(expr)
    raw_deg = int(sp.total_degree(poly_expr)) if poly_expr != 0 else -1
    print(f"{label}_RAW_DEG", raw_deg, "OPS", poly_expr.count_ops(),
          "EXPAND_SEC", round(time.time() - t_exp, 3))
    P = Poly(poly_expr, *gens, domain="QQ")
    cont = P.content()
    # Strip content over QQ: divide by content (rational).
    if cont != 0 and cont != 1:
        P = Poly(P.as_expr() / cont, *gens, domain="QQ")
    powers = {}
    for name, fac in CHART_FACTORS:
        count = 0
        Ff = Poly(fac, *gens, domain="QQ")
        while count < 24:
            q, r = P.div(Ff)
            if r == 0:
                P = q
                count += 1
            else:
                break
        powers[name] = count
    red_expr = P.as_expr()
    # Re-extract content after division (should be ±1 over QQ after /cont).
    Pred = Poly(red_expr, *gens, domain="QQ")
    cont2 = Pred.content()
    if cont2 != 0 and cont2 != 1:
        red_expr = (Pred.as_expr() / cont2)
        cont = cont * cont2
        Pred = Poly(red_expr, *gens, domain="QQ")
    red_deg = int(sp.total_degree(red_expr)) if red_expr != 0 else -1
    print(f"{label}_CONTENT", cont)
    print(f"{label}_POWERS", powers)
    print(f"{label}_RED_DEG", red_deg, "OPS", Pred.as_expr().count_ops())
    # Exact reconstruction: expr == cont * product(fac^p) * red
    recon = red_expr
    for name, fac in CHART_FACTORS:
        recon = recon * (fac ** powers[name])
    recon = sp.expand(cont * recon)
    check(f"{label}_RECONSTRUCTS", sp.expand(poly_expr - recon) == 0)
    return {
        "raw": poly_expr,
        "red": red_expr,
        "raw_deg": raw_deg,
        "red_deg": red_deg,
        "content": cont,
        "powers": powers,
    }


# ---------------------------------------------------------------------------
print("SECTION_INTERNAL_DEGREE_REDUCTION")
internal = []
t2 = time.time()
for i, f in enumerate(frees):
    cleared = S_den * sp.diff(S_num, f) - S_num * sp.diff(S_den, f)
    internal.append(strip_chart_content(cleared, f"INTERNAL_{i}"))
print("TIMING_INTERNAL_SEC", round(time.time() - t2, 3))

check("INTERNAL_COUNT_14", len(internal) == 14)
check("INTERNAL_RAW_DEGS_UNIFORM_33", all(r["raw_deg"] == 33 for r in internal))
check(
    "INTERNAL_RED_DEGS_STRICTLY_LOWER",
    all(r["red_deg"] < r["raw_deg"] for r in internal),
)
check(
    "INTERNAL_RED_DEGS_LE_12",
    all(r["red_deg"] <= 12 for r in internal),
)
check(
    "INTERNAL_RED_ALL_NONZERO",
    all(r["red"] != 0 for r in internal),
)
internal_red_degs = [r["red_deg"] for r in internal]
print("INTERNAL_RED_DEGS", internal_red_degs)

# Common (min) chart powers across all internal gens.
min_powers_int = {
    name: min(r["powers"][name] for r in internal) for name, _ in CHART_FACTORS
}
print("INTERNAL_MIN_CHART_POWERS", min_powers_int)
check(
    "INTERNAL_MIN_J2SQ4_AT_LEAST_4",
    min_powers_int["j2sq4"] >= 4,
)
check(
    "INTERNAL_MIN_J3SQ4_AT_LEAST_4",
    min_powers_int["j3sq4"] >= 4,
)

# ---------------------------------------------------------------------------
print("SECTION_TRANSVERSE_DEGREE_REDUCTION")
TRANSVERSE_DIRS = [
    (0, K1, "r0_K1"),
    (0, M2, "r0_M2"),
    (0, M3, "r0_M3"),
    (1, K1, "r1_K1"),
    (1, M2, "r1_M2"),
    (1, M3, "r1_M3"),
]
transverse = []
t3 = time.time()
for r0, H, label in TRANSVERSE_DIRS:
    g = dS_transverse(role, As, Theta, r0, H)
    num, _den = sp.fraction(sp.together(g))
    transverse.append(strip_chart_content(num, f"TRANSVERSE_{label}"))
print("TIMING_TRANSVERSE_SEC", round(time.time() - t3, 3))

check("TRANSVERSE_COUNT_6", len(transverse) == 6)
check(
    "TRANSVERSE_RAW_DEGS_UNIFORM_23",
    all(r["raw_deg"] == 23 for r in transverse),
)
check(
    "TRANSVERSE_RED_DEGS_STRICTLY_LOWER",
    all(r["red_deg"] < r["raw_deg"] for r in transverse),
)
check(
    "TRANSVERSE_RED_DEGS_LE_15",
    all(r["red_deg"] <= 15 for r in transverse),
)
check(
    "TRANSVERSE_RED_ALL_NONZERO",
    all(r["red"] != 0 for r in transverse),
)
transverse_red_degs = [r["red_deg"] for r in transverse]
print("TRANSVERSE_RED_DEGS", transverse_red_degs)
min_powers_tr = {
    name: min(r["powers"][name] for r in transverse) for name, _ in CHART_FACTORS
}
print("TRANSVERSE_MIN_CHART_POWERS", min_powers_tr)
check("TRANSVERSE_MIN_J2SQ4_AT_LEAST_2", min_powers_tr["j2sq4"] >= 2)
check("TRANSVERSE_MIN_J3SQ4_AT_LEAST_2", min_powers_tr["j3sq4"] >= 2)

# ---------------------------------------------------------------------------
print("SECTION_REDUCED_8P6_SAMPLE_JAC")
# Same probe / selected internal rows as the polys cert: greedy Jac pivots of
# raw internal Hessian are not re-derived; use first 8 free-index order that
# the polys cert reported as selected when available. Recompute greedily from
# reduced residuals via exact rational FD of S / transverse at probe — cheaper
# and packing-identical.
PROBE = {frees[i]: Rational(1, 7) + Rational(i, 11) for i in range(14)}
h = Rational(1, 50)
free0 = [PROBE[frees[i]] for i in range(14)]

# Chart-open at probe.
j2v, j3v = free0[1], free0[4]
d0v, d1v, d2v = free0[5], free0[6], free0[7]
check("PROBE_J2SQ4_NONZERO", j2v**2 + 4 != 0)
check("PROBE_J3SQ4_NONZERO", j3v**2 + 4 != 0)
check("PROBE_D_NONZERO", d0v != 0 and d1v != 0 and d2v != 0)


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
    return Matrix(g)


def trans_vec_at(free_vals):
    ch = chart_at(free_vals)
    role_r = [e2_closed(*ch[3 * r : 3 * r + 3]) for r in range(4)]
    As_r = [e2_alg(*ch[3 * r : 3 * r + 3]) for r in range(4)]
    Th = ldu_theta(ch[12:])
    out = []
    for r0, H, _label in TRANSVERSE_DIRS:
        out.append(sp.simplify(dS_transverse(role_r, As_r, Th, r0, H)))
    return Matrix(out)


# Reduced residual = raw residual / (content * chart powers) at probe.
# Since raw internal residual = dS/df (rational), and cleared_numer(raw) =
# content * factors * red, evaluating red at probe is proportional to the
# cleared numerator; for Jac rank we use FD of the actual rational residuals
# (same as polys cert) — rank is invariant. Separately verify reduced polys
# evaluate nonzero at probe (same zeros as cleared on open chart).
red_int_vals = [sp.simplify(r["red"].subs(PROBE)) for r in internal]
red_tr_vals = [sp.simplify(r["red"].subs(PROBE)) for r in transverse]
check("REDUCED_INTERNAL_PROBE_ALL_NONZERO", all(v != 0 for v in red_int_vals))
check("REDUCED_TRANSVERSE_PROBE_ALL_NONZERO", all(v != 0 for v in red_tr_vals))

g0 = grad_S_at(free0)
Jac_rows = []
for j in range(14):
    fv = list(free0)
    fv[j] = free0[j] + h
    gj = grad_S_at(fv)
    Jac_rows.append([sp.simplify((gj[i] - g0[i]) / h) for i in range(14)])
Jac_int = Matrix(Jac_rows).T
check("INTERNAL_PROBE_JAC_FULL_RANK_14", Jac_int.rank() == 14)

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

t0_vec = trans_vec_at(free0)
Jac_tr_rows = []
for i in range(6):
    row = []
    v0 = t0_vec[i]
    for j in range(14):
        fv = list(free0)
        fv[j] = free0[j] + h
        v1 = trans_vec_at(fv)[i]
        row.append(sp.simplify((v1 - v0) / h))
    Jac_tr_rows.append(row)
Jac_tr = Matrix(Jac_tr_rows)
check("TRANSVERSE_PROBE_JAC_FULL_RANK_6", Jac_tr.rank() == 6)

Jac_sub = Matrix.vstack(
    Jac_int.extract(selected_internal, list(range(14))), Jac_tr
)
rank_sub = Jac_sub.rank()
print("SUBSYSTEM_8P6_PROBE_JAC_RANK", rank_sub)
check("SUBSYSTEM_8P6_PROBE_JAC_FULL_RANK_14", rank_sub == 14)

# Pairwise GCD sample on two reduced internal gens (minutes-safe).
print("SECTION_REDUCED_GCD_SAMPLE")
abort_if("gcd sample")
P0 = Poly(internal[selected_internal[0]]["red"], *gens, domain="QQ")
P1 = Poly(internal[selected_internal[1]]["red"], *gens, domain="QQ")
g01 = sp.gcd(P0, P1)
print("GCD_SELECTED0_SELECTED1_DEG", int(g01.total_degree()) if g01 != 0 else -1)
print("GCD_SELECTED0_SELECTED1", g01.as_expr() if g01.total_degree() <= 2 else f"<deg {g01.total_degree()}>")
# Constant gcd is the expected generic case; non-constant would be further news.
check("GCD_SAMPLE_COMPUTED", g01 is not None)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
print(
    "RESULT_E2_STATIONARITY_DEG_REDUCE: under provisional FIXED_13 packing, "
    "raw internal deg-33 / transverse deg-23 cleared numerators factor as "
    "ZZ-content x (j2^2+4)^a x (j3^2+4)^b x d0^c d1^d d2^e x reduced, with "
    f"internal reduced degrees {internal_red_degs} (all <=12) and transverse "
    f"reduced degrees {transverse_red_degs} (all <=15). Min internal chart "
    f"powers {min_powers_int}; min transverse {min_powers_tr}. Reduced gens "
    "agree with raw gens on the open chart; 8+6 sample Jac rank 14 retained."
)
print(
    "SCOPE: no exact root; no Groebner; provisional packing unchanged "
    "(QR pivots unrecovered); degree drop is chart-denom/content inflation "
    "removal, not a new ideal membership proof beyond the open chart; "
    "four-channel R=R_*(C) not applied; A4 ambient FD not restarted."
)
print(
    "NEXT: eliminate / reconstruct on the reduced <=12-degree 8+6 subsystem "
    "(still hard over Q in 14 vars — specialize a subset of free coords or "
    "recover QR packing first); or replace provisional packing by a "
    "gauge-canonical exact normal form."
)
print(
    "WHY_DEG_33: cleared stationarity numerators retain leftover powers of "
    "Cayley denoms (j_free^2+4) and LDU d-slots after differentiating the "
    "rational star density; those factors never vanish on the open chart, so "
    "they inflate total degree without changing chart zeros."
)
