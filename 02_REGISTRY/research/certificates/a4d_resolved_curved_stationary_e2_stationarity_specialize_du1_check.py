#!/usr/bin/env python3
"""F4 Track B -- rational specialization D=(1,1,1), U=0 of reduced E2 stationarity.

Research-only. Exact rational / symbolic arithmetic. Minutes-scale.

Under the same provisional FIXED_13 packing as
`a4d_resolved_curved_stationary_e2_stationarity_deg_reduce_check.py`, specialize
the nine free solder slots

    D0=D1=D2=1,   U01=U02=U03=U12=U13=U23=0

and retain the five free E(2) coordinates

    (e2_r2_n3, e2_r2_j, e2_r3_n2, e2_r3_n3, e2_r3_j).

Certifies:

  * the five free-internal cleared/reduced stationarity generators (chart-denom
    content stripped as in the deg-reduce cert) have degrees <=5;
  * the three n-direction generators (dS/d n3_r2, dS/d n2_r3, dS/d n3_r3) are
    bivariate in (j_r2, j_r3) alone;
  * their lex Groebner basis over Q is exactly {j_r2 + j_r3, j_r3^2 + 4};
  * hence j_r3^2 + 4 lies in the free-internal ideal, so every common zero of
    the specialized free-internal system lies on the Cayley chart-closed locus
    j_r3^2 + 4 = 0 (and j_r2 = -j_r3);
  * on the open chart (j_r2^2+4 != 0 and j_r3^2+4 != 0) the specialized
    free-internal system has no solutions (over C).

Does NOT claim a curved stationary root.
Does NOT run 14-var Groebner / blind deg-33 elimination.
Does NOT recover QR pivots / replace provisional packing.
Does NOT open Holst/phi/new I-channels.
Does NOT assert emptiness of other specializations or of the unspecialized ideal.
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


# ---------------------------------------------------------------------------
print("SECTION_PACKING_AND_SPECIALIZATION")
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
# Free-local indices 0..13: e2_r2_n3, e2_r2_j, e2_r3_n2, e2_r3_n3, e2_r3_j,
# D0, D1, D2, U0..U5. Specialize D and U; retain five E(2) frees.
SPEC_LOCAL = {
    5: Rational(1),
    6: Rational(1),
    7: Rational(1),
    8: Rational(0),
    9: Rational(0),
    10: Rational(0),
    11: Rational(0),
    12: Rational(0),
    13: Rational(0),
}
REM_LOCAL = [i for i in range(14) if i not in SPEC_LOCAL]
check("PACK_FIXED_COUNT_13", len(FIXED_IDX) == 13)
check("PACK_FREE_COUNT_14", len(FREE_IDX) == 14)
check("SPEC_COUNT_9", len(SPEC_LOCAL) == 9)
check("REM_COUNT_5", len(REM_LOCAL) == 5)
check("REM_ARE_E2_ONLY", REM_LOCAL == [0, 1, 2, 3, 4])
print(
    "SPEC_DECLARED: D0=D1=D2=1, U0..U5=0; remaining free =",
    [CHART_NAMES[FREE_IDX[i]] for i in REM_LOCAL],
)

gens = symbols("g0:5")
n3_r2, j_r2, n2_r3, n3_r3, j_r3 = gens
CHART_FACTORS = [
    ("j2sq4", j_r2**2 + 4),
    ("j3sq4", j_r3**2 + 4),
]

chart = [None] * 27
for k, i in enumerate(FIXED_IDX):
    chart[i] = FIXED_13[k]
gi = 0
for k, i in enumerate(FREE_IDX):
    if k in SPEC_LOCAL:
        chart[i] = SPEC_LOCAL[k]
    else:
        chart[i] = gens[gi]
        gi += 1
check("CHART_FILL_COMPLETE", all(c is not None for c in chart))
check("CHART_D_SPECIALIZED_TO_ONE", chart[18] == 1 and chart[19] == 1 and chart[20] == 1)
check(
    "CHART_U_SPECIALIZED_TO_ZERO",
    all(chart[i] == 0 for i in range(21, 27)),
)

role = [e2_closed(*chart[3 * r : 3 * r + 3]) for r in range(4)]
Theta = ldu_theta(chart[12:])

abort_if("before S build")
t1 = time.time()
S = star_S_hom(role, Theta)
St = sp.together(S)
S_num, S_den = sp.fraction(St)
print("TIMING_S_BUILD_SEC", round(time.time() - t1, 3))
print("S_DEN_OPS", S_den.count_ops(), "S_NUM_OPS", S_num.count_ops())


def strip_chart_content(expr, label):
    """Expand, strip ZZ content + maximal open-chart factors; return red expr."""
    abort_if(label)
    t_exp = time.time()
    poly_expr = sp.expand(expr)
    raw_deg = int(sp.total_degree(poly_expr)) if poly_expr != 0 else -1
    print(
        f"{label}_RAW_DEG",
        raw_deg,
        "OPS",
        poly_expr.count_ops(),
        "EXPAND_SEC",
        round(time.time() - t_exp, 3),
    )
    check(f"{label}_NONZERO_RAW", poly_expr != 0)
    P = Poly(poly_expr, *gens, domain="QQ")
    cont = P.content()
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
    Pred = Poly(red_expr, *gens, domain="QQ")
    cont2 = Pred.content()
    if cont2 != 0 and cont2 != 1:
        red_expr = Pred.as_expr() / cont2
        cont = cont * cont2
        Pred = Poly(red_expr, *gens, domain="QQ")
    red_deg = int(sp.total_degree(red_expr)) if red_expr != 0 else -1
    print(f"{label}_CONTENT", cont)
    print(f"{label}_POWERS", powers)
    print(f"{label}_RED_DEG", red_deg, "OPS", Pred.as_expr().count_ops())
    recon = red_expr
    for name, fac in CHART_FACTORS:
        recon = recon * (fac ** powers[name])
    recon = sp.expand(cont * recon)
    check(f"{label}_RECONSTRUCTS", sp.expand(poly_expr - recon) == 0)
    check(f"{label}_RED_NONZERO", red_expr != 0)
    return {
        "red": sp.expand(red_expr),
        "raw_deg": raw_deg,
        "red_deg": red_deg,
        "content": cont,
        "powers": powers,
    }


# ---------------------------------------------------------------------------
print("SECTION_SPECIALIZED_FREE_INTERNAL")
FREE_NAMES = ["n3_r2", "j_r2", "n2_r3", "n3_r3", "j_r3"]
internal = []
t2 = time.time()
for i, g in enumerate(gens):
    cleared = S_den * sp.diff(S_num, g) - S_num * sp.diff(S_den, g)
    internal.append(strip_chart_content(cleared, f"INT_{FREE_NAMES[i]}"))
print("TIMING_INTERNAL_SEC", round(time.time() - t2, 3))

check("INTERNAL_COUNT_5", len(internal) == 5)
check(
    "INTERNAL_RED_DEGS_LE_5",
    all(r["red_deg"] <= 5 for r in internal),
)
red_degs = [r["red_deg"] for r in internal]
print("INTERNAL_RED_DEGS", red_degs)

# n-direction gens are bivariate in (j_r2, j_r3) only.
n_idx = [0, 2, 3]  # n3_r2, n2_r3, n3_r3
for i in n_idx:
    fs = internal[i]["red"].free_symbols
    check(
        f"INT_{FREE_NAMES[i]}_BIVARIATE_IN_J_ONLY",
        fs <= {j_r2, j_r3},
    )
    check(
        f"INT_{FREE_NAMES[i]}_RED_DEG_LE_3",
        internal[i]["red_deg"] <= 3,
    )

# ---------------------------------------------------------------------------
print("SECTION_GROEBNER_N_DIRECTION")
abort_if("before GB")
n_gens = [internal[i]["red"] for i in n_idx]
t3 = time.time()
gb = sp.groebner(n_gens, j_r2, j_r3, domain="QQ", order="lex")
print("TIMING_GB_SEC", round(time.time() - t3, 3))
gb_list = list(gb)
print("GB_N_DIRECTION", gb_list)
check("GB_LEN_2", len(gb_list) == 2)
# Exact expected basis (up to QQ units): {j_r2 + j_r3, j_r3^2 + 4}.
g0, g1 = gb_list[0], gb_list[1]
# Normalize leading coeffs to 1.
P0 = Poly(g0, j_r2, j_r3, domain="QQ")
P1 = Poly(g1, j_r2, j_r3, domain="QQ")
n0 = sp.expand(g0 / P0.LC())
n1 = sp.expand(g1 / P1.LC())
check("GB_ELEM0_IS_J2_PLUS_J3", sp.expand(n0 - (j_r2 + j_r3)) == 0)
check("GB_ELEM1_IS_J3SQ_PLUS_4", sp.expand(n1 - (j_r3**2 + 4)) == 0)

# Ideal membership: j_r3^2 + 4 is (up to unit) a GB element.
check(
    "J3SQ4_IN_FREE_INTERNAL_IDEAL",
    sp.expand(n1 - (j_r3**2 + 4)) == 0,
)

# Full five-generator GB agrees (same chart-closed conclusion).
abort_if("before full5 GB")
t4 = time.time()
gb5 = sp.groebner([r["red"] for r in internal], *gens, domain="QQ", order="lex")
print("TIMING_GB5_SEC", round(time.time() - t4, 3))
gb5_list = list(gb5)
print("GB_ALL_FIVE_FREE_INTERNAL", gb5_list)
check("GB5_LEN_2", len(gb5_list) == 2)
Q0 = Poly(gb5_list[0], *gens, domain="QQ")
Q1 = Poly(gb5_list[1], *gens, domain="QQ")
m0 = sp.expand(gb5_list[0] / Q0.LC())
m1 = sp.expand(gb5_list[1] / Q1.LC())
check("GB5_ELEM0_IS_J2_PLUS_J3", sp.expand(m0 - (j_r2 + j_r3)) == 0)
check("GB5_ELEM1_IS_J3SQ_PLUS_4", sp.expand(m1 - (j_r3**2 + 4)) == 0)

# Open-chart emptiness: any common zero satisfies j_r3^2+4=0, hence is not
# chart-open. Equivalently, the open-chart locus of the specialized
# free-internal system is empty over C.
check(
    "OPEN_CHART_EMPTY_SPECIALIZED_FREE_INTERNAL",
    True,  # logical consequence of J3SQ4_IN_FREE_INTERNAL_IDEAL
)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
print(
    "RESULT_E2_STATIONARITY_SPECIALIZE_DU1: under provisional FIXED_13 packing "
    "and rational specialization D=(1,1,1), U=0, the five free-internal reduced "
    f"stationarity gens have degrees {red_degs}; the three n-direction gens "
    "are bivariate in (j_r2, j_r3) and have lex GB {{j_r2+j_r3, j_r3^2+4}} over "
    "Q; thus j_r3^2+4 lies in the free-internal ideal and every common zero is "
    "chart-closed. Open-chart specialized free-internal system: empty."
)
print(
    "SCOPE: slice-only no-go (this D/U specialization under provisional "
    "packing); not a global E2/F4 no-go; specialized-dir residuals "
    "(dS/dD, dS/dU) and transverse Lorentz eqs not required for emptiness "
    "(free-internal alone already forces chart-closed); QR pivots still "
    "unrecovered; no exact curved root; no continuum Einstein claim; "
    "A4 ambient FD not restarted."
)
print(
    "NEXT: try a denser rational specialization nearer the numerical E2 scout "
    "(or recover QR pivot map / gauge-canonical packing replacing FIXED_13); "
    "or specialize a different free subset (e.g. keep D free, set selected U); "
    "still avoid blind 14-var / deg-33 Groebner."
)
