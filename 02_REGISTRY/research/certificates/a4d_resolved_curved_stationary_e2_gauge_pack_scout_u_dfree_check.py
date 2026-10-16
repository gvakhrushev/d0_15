#!/usr/bin/env python3
"""F4 Track B -- gauge-canonical L≡0 packing + scout-near U, D free.

Research-only. Exact rational / symbolic arithmetic. Minutes-scale.

Under the gauge-canonical packing of
`a4d_resolved_curved_stationary_e2_gauge_canonical_packing_check.py`
(L≡0 Iwasawa solder gauge; memo-§5 E(2) NF on slots [0..6]; free =
e2_r2_{n3,j}+e2_r3_*+D+U), specialize the six U slots to the scout-near
rationals from
`a4d_resolved_curved_stationary_e2_stationarity_specialize_scout_du_check.py`:

    U=(1/6, 5/4, -1/10, -3/5, 0, -1/5)

and KEEP the three D slots free. Remaining free coordinates (8):

    (e2_r2_n3, e2_r2_j, e2_r3_n2, e2_r3_n3, e2_r3_j, D0, D1, D2).

Certifies (hard wall ~8–12 min):

  * packing is the gauge-canonical one (L≡0; U scout-near; D free);
  * the eight free-internal cleared stationarity generators, chart-denom /
    content stripped (j2^2+4, j3^2+4, d0, d1, d2), have finite reduced
    degree on the open chart;
  * the three n-direction generators project under lex GB / resultant to a
    clear open-chart obstruction, candidate, or documented stall with an
    exact next command.

Does NOT redo FIXED_13 fully-fixed D/U slices.
Does NOT run blind 14-var / deg-33 Groebner.
Does NOT claim a curved stationary root unless an exact open-chart witness
is reconstructed.
Does NOT open Holst/phi/new I-channels.
Does NOT assert global F4 no-go / continuum Einstein.
"""
from __future__ import annotations

import hashlib
import time
from itertools import combinations

import sympy as sp
from sympy import Matrix, Poly, Rational, eye, zeros, symbols

t_wall0 = time.time()
WALL_SEC = 540  # hard abort budget (~9 min; report under 12)


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def elapsed():
    return time.time() - t_wall0


def abort_if(msg):
    if elapsed() > WALL_SEC - 30:
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
print("SECTION_GAUGE_PACK_SCOUT_U_DFREE")
# Gauge-canonical FIXED_13: E(2) NF + L≡0 (not provisional nonzero L).
GAUGE_FIXED_13 = [
    Rational(-1, 3),  # e2_r0_n2
    Rational(0, 1),  # e2_r0_n3
    Rational(-1, 3),  # e2_r0_j
    Rational(1, 2),  # e2_r1_n2
    Rational(1, 2),  # e2_r1_n3
    Rational(-1, 2),  # e2_r1_j
    Rational(-1, 2),  # e2_r2_n2
    Rational(0, 1),  # L_0
    Rational(0, 1),  # L_1
    Rational(0, 1),  # L_2
    Rational(0, 1),  # L_3
    Rational(0, 1),  # L_4
    Rational(0, 1),  # L_5
]
FIXED_IDX = [0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 17]
FREE_IDX = [i for i in range(27) if i not in FIXED_IDX]
CHART_NAMES = (
    [f"e2_r{r}_{c}" for r in range(4) for c in ("n2", "n3", "j")]
    + [f"L_{k}" for k in range(6)]
    + [f"D_{k}" for k in range(3)]
    + [f"U_{k}" for k in range(6)]
)
# Free-local 0..13 under packing: e2_r2_n3, e2_r2_j, e2_r3_n2, e2_r3_n3,
# e2_r3_j, D0, D1, D2, U0..U5. Specialize U only; keep D free.
SPEC_U_LOCAL = {
    8: Rational(1, 6),
    9: Rational(5, 4),
    10: Rational(-1, 10),
    11: Rational(-3, 5),
    12: Rational(0),
    13: Rational(-1, 5),
}
SPEC_U = tuple(SPEC_U_LOCAL[i] for i in range(8, 14))
REM_LOCAL = [i for i in range(14) if i not in SPEC_U_LOCAL]
# Rem: 0..4 E(2) free + 5,6,7 = D0,D1,D2.
check("PACK_FIXED_COUNT_13", len(FIXED_IDX) == 13)
check("PACK_FREE_COUNT_14", len(FREE_IDX) == 14)
check("PACK_L_ALL_ZERO_GAUGE", all(GAUGE_FIXED_13[k] == 0 for k in range(7, 13)))
check("SPEC_U_COUNT_6", len(SPEC_U_LOCAL) == 6)
check("REM_COUNT_8", len(REM_LOCAL) == 8)
check("REM_ARE_E2_PLUS_D", REM_LOCAL == [0, 1, 2, 3, 4, 5, 6, 7])
check(
    "SPEC_U_NEAR_SCOUT",
    SPEC_U
    == (
        Rational(1, 6),
        Rational(5, 4),
        Rational(-1, 10),
        Rational(-3, 5),
        Rational(0),
        Rational(-1, 5),
    ),
)
check("D_STAYS_FREE", 5 in REM_LOCAL and 6 in REM_LOCAL and 7 in REM_LOCAL)
print(
    "SPEC_DECLARED: U=",
    [str(x) for x in SPEC_U],
    "; D free; remaining free =",
    [CHART_NAMES[FREE_IDX[i]] for i in REM_LOCAL],
)

gens = symbols("g0:8")
n3_r2, j_r2, n2_r3, n3_r3, j_r3, d0, d1, d2 = gens
CHART_FACTORS = [
    ("j2sq4", j_r2**2 + 4),
    ("j3sq4", j_r3**2 + 4),
    ("d0", d0),
    ("d1", d1),
    ("d2", d2),
]

chart = [None] * 27
for k, i in enumerate(FIXED_IDX):
    chart[i] = GAUGE_FIXED_13[k]
gi = 0
for k, i in enumerate(FREE_IDX):
    if k in SPEC_U_LOCAL:
        chart[i] = SPEC_U_LOCAL[k]
    else:
        chart[i] = gens[gi]
        gi += 1
check("CHART_FILL_COMPLETE", all(c is not None for c in chart))
check(
    "CHART_L_ZERO",
    all(chart[i] == 0 for i in range(12, 18)),
)
check(
    "CHART_U_SPECIALIZED_SCOUT",
    chart[21:]
    == [
        Rational(1, 6),
        Rational(5, 4),
        Rational(-1, 10),
        Rational(-3, 5),
        Rational(0),
        Rational(-1, 5),
    ],
)
check(
    "CHART_D_SYMBOLIC",
    chart[18] == d0 and chart[19] == d1 and chart[20] == d2,
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
print("SECTION_FREE_INTERNAL_DEG_REDUCE")
FREE_NAMES = [
    "n3_r2",
    "j_r2",
    "n2_r3",
    "n3_r3",
    "j_r3",
    "d0",
    "d1",
    "d2",
]
internal = []
t2 = time.time()
for i, g in enumerate(gens):
    cleared = S_den * sp.diff(S_num, g) - S_num * sp.diff(S_den, g)
    internal.append(strip_chart_content(cleared, f"INT_{FREE_NAMES[i]}"))
print("TIMING_INTERNAL_SEC", round(time.time() - t2, 3))

check("INTERNAL_COUNT_8", len(internal) == 8)
red_degs = [r["red_deg"] for r in internal]
print("INTERNAL_RED_DEGS", red_degs)
check("INTERNAL_RED_ALL_FINITE", all(d >= 0 for d in red_degs))
check(
    "INTERNAL_RED_DEGS_STRICTLY_LOWER",
    all(r["red_deg"] < r["raw_deg"] for r in internal),
)

# n-direction gens: n3_r2, n2_r3, n3_r3
n_idx = [0, 2, 3]
n_syms = set()
for i in n_idx:
    fs = set(internal[i]["red"].free_symbols)
    n_syms |= fs
    print(f"INT_{FREE_NAMES[i]}_FREE_SYMS", sorted(str(s) for s in fs))
print("N_DIR_UNION_SYMS", sorted(str(s) for s in n_syms))

# ---------------------------------------------------------------------------
print("SECTION_N_DIRECTION_ELIMINATE")
abort_if("before n-dir GB")
n_gens = [internal[i]["red"] for i in n_idx]
outcome = "UNKNOWN"
gb_list = None
gb_norm = None
t3 = time.time()

# Prefer smallest projection: if n-gens live in a small var set, GB there.
if n_syms <= {j_r2, j_r3}:
    gb = sp.groebner(n_gens, j_r2, j_r3, domain="QQ", order="lex")
    gb_list = list(gb)
    print("TIMING_GB_N_JONLY_SEC", round(time.time() - t3, 3))
    print("GB_N_DIRECTION_JONLY", gb_list)
elif n_syms <= {j_r2, j_r3, d0, d1, d2}:
    # Eliminate D first: lex with d0 > d1 > d2 > j_r2 > j_r3
    order_vars = [v for v in (d0, d1, d2, j_r2, j_r3) if v in n_syms]
    # Prefer eliminating D onto (j_r2, j_r3): put D highest.
    order_vars = [v for v in (d0, d1, d2) if v in n_syms] + [
        v for v in (j_r2, j_r3) if v in n_syms
    ]
    try:
        gb = sp.groebner(n_gens, *order_vars, domain="QQ", order="lex")
        gb_list = list(gb)
        print("TIMING_GB_N_WITH_D_SEC", round(time.time() - t3, 3))
        print("GB_N_DIRECTION_WITH_D", gb_list)
        print("GB_ORDER_VARS", [str(v) for v in order_vars])
    except Exception as exc:  # pragma: no cover - defensive
        print("GB_N_WITH_D_FAILED", type(exc).__name__, str(exc)[:200])
        gb_list = None
else:
    # Broader support: try n-gens alone in their symbol order (n's + j's + D).
    order_vars = [v for v in gens if v in n_syms]
    # Put n's highest to eliminate onto (j, D).
    try:
        gb = sp.groebner(n_gens, *order_vars, domain="QQ", order="lex")
        gb_list = list(gb)
        print("TIMING_GB_N_BROAD_SEC", round(time.time() - t3, 3))
        print("GB_N_DIRECTION_BROAD", gb_list)
    except Exception as exc:  # pragma: no cover
        print("GB_N_BROAD_FAILED", type(exc).__name__, str(exc)[:200])
        gb_list = None

print("TIMING_GB_N_SEC", round(time.time() - t3, 3))

j3sq4_in_ideal = False
j2_plus_j3_in = False
open_units = {d0, d1, d2}


def forces_j3sq4_on_open_chart(expr):
    """True if expr = (QQ-unit) * (product of open D-units)^* * (j3^2+4)^+
    optionally times other factors that are themselves open units or 1.
    Equivalently: after stripping content and open-chart D-powers, the
    remaining polynomial is a positive power of (j_r3^2+4) (possibly times
    a QQ unit), with no other essential factors.
    """
    e = sp.expand(expr)
    if e == 0:
        return False
    fs = sorted(e.free_symbols, key=str)
    if not fs:
        return False
    P = Poly(e, *fs, domain="QQ")
    cont = P.content()
    if cont not in (0, 1, -1):
        P = Poly(P.as_expr() / cont, *fs, domain="QQ")
    # Strip open-chart D-powers.
    for u in (d0, d1, d2):
        if u not in P.gens:
            continue
        Fu = Poly(u, *P.gens, domain="QQ")
        while True:
            q, r = P.div(Fu)
            if r == 0 and q != 0:
                P = q
            else:
                break
    rem = sp.expand(P.as_expr())
    if rem == 0:
        return False
    # Accept rem == c*(j3^2+4)^k for k>=1, c in QQ^*.
    rem_fs = sorted(rem.free_symbols, key=str)
    if set(rem_fs) <= {j_r3} or set(rem_fs) <= {j_r2, j_r3}:
        Pr = Poly(rem, *([j_r2, j_r3] if j_r2 in rem.free_symbols else [j_r3]), domain="QQ")
        Fj = Poly(j_r3**2 + 4, *Pr.gens, domain="QQ")
        k = 0
        cur = Pr
        while True:
            q, r = cur.div(Fj)
            if r == 0 and q != 0:
                cur = q
                k += 1
            else:
                break
        if k >= 1 and cur.as_expr().free_symbols == set() and cur.as_expr() != 0:
            return True
    # Also: rem factors and every non-unit factor is (j3^2+4).
    fac = sp.factor(rem)
    print("OPEN_CHART_FACTOR_PROBE", fac)
    # Divide out (j3^2+4) maximally; leftover should be QQ * D-units only.
    leftover = rem
    k = 0
    while True:
        q, r = sp.div(leftover, j_r3**2 + 4, domain="QQ")
        # sp.div may need Poly form
        try:
            Pl = Poly(leftover, *sorted(leftover.free_symbols, key=str), domain="QQ") if leftover.free_symbols else None
        except Exception:
            Pl = None
        if Pl is None:
            break
        Fj = Poly(j_r3**2 + 4, *Pl.gens, domain="QQ")
        q2, r2 = Pl.div(Fj)
        if r2 == 0 and q2 != 0:
            leftover = q2.as_expr()
            k += 1
        else:
            break
    if k >= 1:
        lf_fs = set(sp.sympify(leftover).free_symbols)
        if lf_fs <= open_units or lf_fs == set():
            if leftover != 0:
                return True
    return False


if gb_list is not None:
    check("GB_N_NONEMPTY", len(gb_list) >= 1)
    gb_norm = []
    for g in gb_list:
        fs = sorted(g.free_symbols, key=lambda s: str(s))
        if not fs:
            gb_norm.append(sp.Integer(1) if g != 0 else sp.Integer(0))
            continue
        Pg2 = Poly(g, *fs, domain="QQ")
        ng = sp.expand(g / Pg2.LC())
        gb_norm.append(ng)
        if sp.expand(ng - (j_r3**2 + 4)) == 0:
            j3sq4_in_ideal = True
        if sp.expand(ng - (j_r2 + j_r3)) == 0:
            j2_plus_j3_in = True
        if forces_j3sq4_on_open_chart(ng) or forces_j3sq4_on_open_chart(g):
            j3sq4_in_ideal = True
    print("GB_N_NORMALIZED", gb_norm)
    print("J3SQ4_IN_N_IDEAL", j3sq4_in_ideal)
    print("J2_PLUS_J3_IN_N_IDEAL", j2_plus_j3_in)

    # Explicit witness from the observed GB shape d*(j3^2+4).
    for g in gb_list:
        ge = sp.factor(sp.expand(g))
        print("GB_N_FACTORED", ge)
        if forces_j3sq4_on_open_chart(g):
            j3sq4_in_ideal = True

    if j3sq4_in_ideal:
        outcome = "CHART_CLOSED_EMPTY"
        check("J3SQ4_IN_FREE_INTERNAL_N_IDEAL", True)
        check("OPEN_CHART_EMPTY_N_PROJECTION", True)
        # On open chart di!=0, j3^2+4 lies in the saturated n-ideal.
        check("OPEN_CHART_SATURATES_TO_J3SQ4", True)
    else:
        consts = [g for g in gb_norm if g.free_symbols == set()]
        if any(c != 0 for c in consts):
            outcome = "STRUCTURAL_EMPTY"
            check("N_PROJECTION_HAS_NONZERO_CONSTANT", True)
        else:
            j_only = [
                g
                for g in gb_norm
                if g.free_symbols and g.free_symbols <= {j_r2, j_r3}
            ]
            print("GB_N_JONLY_ELEMS", j_only)
            if j_only:
                for g in j_only:
                    if forces_j3sq4_on_open_chart(g):
                        j3sq4_in_ideal = True
                if j3sq4_in_ideal:
                    outcome = "CHART_CLOSED_EMPTY"
                    check("J3SQ4_DIVIDES_N_JONLY_GB", True)
                    check("OPEN_CHART_EMPTY_N_PROJECTION", True)
                else:
                    outcome = "J_LOCUS_OPEN_CANDIDATE"
                    check("N_PROJECTION_OPEN_J_LOCUS", True)
            else:
                outcome = "N_GB_NO_PURE_J"
                check("N_GB_COMPUTED_NO_PURE_J_YET", True)
else:
    outcome = "N_GB_STALL"
    check("N_GB_STALL_DOCUMENTED", True)

# If still unsettled: expression-level resultant onto (j_r2, j_r3), then
# optional full-8 GB under remaining wall.
if outcome in ("N_GB_NO_PURE_J", "J_LOCUS_OPEN_CANDIDATE", "N_GB_STALL", "UNKNOWN"):
    abort_if("before resultant / full8")
    if n_syms <= {j_r2, j_r3, d0, d1, d2} and len(n_syms) >= 3:
        t4 = time.time()
        elim = list(n_gens)
        for var in (d0, d1, d2):
            if var not in n_syms:
                continue
            abort_if(f"resultant_{var}")
            if len(elim) < 2:
                break
            new_elim = []
            for a, b in zip(elim, elim[1:]):
                # Expression resultant; coeffs may involve other symbols.
                r = sp.resultant(sp.Poly(a, var), sp.Poly(b, var), var)
                r = sp.expand(r)
                if r != 0:
                    new_elim.append(r)
            print(f"RESULTANT_{var}_COUNT", len(new_elim))
            if new_elim:
                elim = new_elim
            else:
                break
        print("TIMING_RESULTANT_SEC", round(time.time() - t4, 3))
        print("RESULTANT_FINAL", elim)
        for r in elim:
            if forces_j3sq4_on_open_chart(r):
                j3sq4_in_ideal = True
                outcome = "CHART_CLOSED_EMPTY"
                check("J3SQ4_VIA_RESULTANT", True)
                check("OPEN_CHART_EMPTY_N_PROJECTION", True)
                break

if outcome in ("N_GB_NO_PURE_J", "J_LOCUS_OPEN_CANDIDATE", "UNKNOWN") and elapsed() < WALL_SEC - 120:
    abort_if("before full8 GB")
    t5 = time.time()
    try:
        order8 = [n3_r2, n2_r3, n3_r3, j_r2, j_r3, d0, d1, d2]
        gb8 = sp.groebner(
            [r["red"] for r in internal], *order8, domain="QQ", order="lex"
        )
        gb8_list = list(gb8)
        print("TIMING_GB8_SEC", round(time.time() - t5, 3))
        print("GB_ALL_EIGHT_FREE_INTERNAL", gb8_list)
        check("GB8_COMPUTED", len(gb8_list) >= 1)
        for g in gb8_list:
            if forces_j3sq4_on_open_chart(g):
                j3sq4_in_ideal = True
                outcome = "CHART_CLOSED_EMPTY"
                check("J3SQ4_IN_FULL8_IDEAL", True)
                check("OPEN_CHART_EMPTY_SPECIALIZED_FREE_INTERNAL", True)
                break
            if g.free_symbols == set() and g != 0:
                outcome = "STRUCTURAL_EMPTY"
                check("FULL8_NONZERO_CONSTANT", True)
                break
    except Exception as exc:
        print("GB8_FAILED_OR_HEAVY", type(exc).__name__, str(exc)[:200])
        check("GB8_STALL_DOCUMENTED", True)
        if outcome == "UNKNOWN":
            outcome = "FULL8_STALL"

print("OUTCOME", outcome)

# Always certify the packing / specialization contract regardless of GB path.
check("GAUGE_PACK_SCOUT_U_DFREE_DECLARED", True)
if outcome == "CHART_CLOSED_EMPTY":
    check("SLICE_OPEN_CHART_EMPTY", True)
elif outcome == "STRUCTURAL_EMPTY":
    check("SLICE_STRUCTURALLY_EMPTY", True)
elif outcome == "J_LOCUS_OPEN_CANDIDATE":
    check("SLICE_OPEN_J_LOCUS_RECORDED", True)
else:
    check("SLICE_PARTIAL_ADVANCE_RECORDED", True)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_12_MIN", wall < 720)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_GAUGE_PACK_SCOUT_U_DFREE: under gauge-canonical L≡0 packing "
    f"and scout-near U=({','.join(str(x) for x in SPEC_U)}) with D free, "
    f"the eight free-internal reduced gens have degrees {red_degs}; "
    f"n-dir union symbols={sorted(str(s) for s in n_syms)}; "
    f"outcome={outcome}; j3sq4_in_ideal={j3sq4_in_ideal}."
)
print(
    "SCOPE: slice under gauge-canonical packing with U scout-near / D free; "
    "not a global E2/F4 no-go; does not redo FIXED_13 fully-fixed D/U; "
    "transverse Lorentz eqs not required for n-projection emptiness when "
    "j3^2+4 lies in the free-internal n-ideal; QR pivots still unrecovered; "
    "no continuum Einstein claim; A4 ambient FD not restarted."
)
if outcome == "CHART_CLOSED_EMPTY":
    print(
        "NEXT: try the symmetric slice (U free + scout-near D) under the same "
        "L≡0 packing; or recompute/persist missing Jac dump for true QR pivots; "
        "or keep a different U rational near scout; still avoid blind 14-var / "
        "deg-33 Groebner; filter by four-channel R=R_*(C)."
    )
elif outcome == "J_LOCUS_OPEN_CANDIDATE":
    print(
        "NEXT: reconstruct exact open-chart coordinates on the recorded j-locus "
        "by back-substituting into the remaining free-internal / D / transverse "
        "gens; still minutes-scale; avoid blind 14-var GB."
    )
else:
    print(
        "NEXT: smaller projection (n-dir only already attempted) or memo the "
        "exact stalled command; try U-free + scout-near D; or persist Jac dump "
        "for QR pivots; still avoid blind 14-var / deg-33 Groebner."
    )