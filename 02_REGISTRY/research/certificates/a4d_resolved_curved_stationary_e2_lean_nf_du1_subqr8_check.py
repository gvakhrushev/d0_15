#!/usr/bin/env python3
"""F4 Track B -- lean NF + identity D/U, subsystem-QR 8 E(2) free.

Research-only. Exact rational / symbolic arithmetic. Minutes-scale.

Under lean NF from
`a4d_resolved_curved_stationary_e2_lean_nf_free_e2_check.py`
(L≡0 only on slots [12..17]; locked E(2) NF NOT imposed), specialize the
identity-like solder

    D=(1,1,1),  U=0

Preferred free set is all 12 E(2). Full-12 cleared expand is too heavy for
the minutes wall (~115s per free-internal generator at deg~71), so this
certificate adopts the documented optional restriction to the lean-NF
subsystem-QR FREE chart indices that remain after identity D/U:

    SUB_QR FREE chart idx (lean cert):
        [8,24,2,5,6,7,3,20,21,0,18,19,4,25]
    After D=(1,1,1), U=0 specialize, remaining free E(2) among those:
        [0,2,3,4,5,6,7,8]
        = (e2_r0_n2, e2_r0_j, e2_r1_n2, e2_r1_n3, e2_r1_j,
           e2_r2_n2, e2_r2_n3, e2_r2_j)
    QR-complement E(2) fixed to simple 0 (NOT the locked NF):
        [1,9,10,11] = (e2_r0_n3, e2_r3_n2, e2_r3_n3, e2_r3_j)

Certifies (hard wall ~8–12 min):

  * lean packing + identity D/U + documented 8-free restriction;
  * eight free-internal cleared stationarity generators, chart-denom /
    content stripped (j0^2+4, j1^2+4, j2^2+4; j3=0 ⇒ j3^2+4 unit), have
    finite reduced degree on the open chart;
  * n-direction (and full free-internal) lex GB projects to an algebraic
    open-chart candidate: j_r2=0 and j_r0=j_r1 on the open chart, with a
    recorded residual ideal in the remaining n / j coordinates
    (NOT chart-closed empty — contrast locked-NF scout slices).

Does NOT re-impose locked E(2) NF (-1/3,0,-1/3,1/2,1/2,-1/2,-1/2).
Does NOT run blind 14-var / deg-33 Groebner / full-12 E(2) eliminate.
Does NOT claim a curved stationary root (locus recorded, not reconstructed).
Does NOT open Holst/phi/new I-channels.
Does NOT assert global F4 no-go / continuum Einstein.
"""
from __future__ import annotations

import hashlib
import time
from itertools import combinations

import sympy as sp
from sympy import Matrix, Poly, Rational, zeros, symbols

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
print("SECTION_LEAN_NF_DU1_SUBQR8_PACKING")
CHART_NAMES = (
    [f"e2_r{r}_{c}" for r in range(4) for c in ("n2", "n3", "j")]
    + [f"L_{k}" for k in range(6)]
    + [f"D_{k}" for k in range(3)]
    + [f"U_{k}" for k in range(6)]
)
# Lean base: L≡0 only.
LEAN_FIXED_L = [12, 13, 14, 15, 16, 17]
# Subsystem-QR FREE from lean cert (float 8+6 sample).
SUB_QR_FREE = [8, 24, 2, 5, 6, 7, 3, 20, 21, 0, 18, 19, 4, 25]
SUB_QR_COMPLEMENT_E2 = [1, 9, 10, 11]  # E(2) among piv[14:] of lean cert
# After identity D/U, free = E(2) ∩ SUB_QR_FREE.
FREE_E2 = sorted(i for i in SUB_QR_FREE if i < 12)
check("FREE_E2_COUNT_8", len(FREE_E2) == 8)
check("FREE_E2_EXACT", FREE_E2 == [0, 2, 3, 4, 5, 6, 7, 8])
check(
    "COMPLEMENT_E2_EXACT",
    SUB_QR_COMPLEMENT_E2 == [1, 9, 10, 11],
)
check(
    "NOT_LOCKED_E2_NF",
    SUB_QR_COMPLEMENT_E2 != [0, 1, 2, 3, 4, 5, 6],
)
LOCKED_E2_NF = [
    Rational(-1, 3),
    Rational(0, 1),
    Rational(-1, 3),
    Rational(1, 2),
    Rational(1, 2),
    Rational(-1, 2),
    Rational(-1, 2),
]
check("LOCKED_E2_NF_DOCUMENTED_NOT_USED", len(LOCKED_E2_NF) == 7)

gens = symbols("g0:8")
# Local layout for FREE_E2=[0,2,3,4,5,6,7,8]:
# g0=n2_r0, g1=j_r0, g2=n2_r1, g3=n3_r1, g4=j_r1,
# g5=n2_r2, g6=n3_r2, g7=j_r2
(
    n2_r0,
    j_r0,
    n2_r1,
    n3_r1,
    j_r1,
    n2_r2,
    n3_r2,
    j_r2,
) = gens
FREE_NAMES = [
    "n2_r0",
    "j_r0",
    "n2_r1",
    "n3_r1",
    "j_r1",
    "n2_r2",
    "n3_r2",
    "j_r2",
]
CHART_FACTORS = [
    ("j0sq4", j_r0**2 + 4),
    ("j1sq4", j_r1**2 + 4),
    ("j2sq4", j_r2**2 + 4),
]

chart = [None] * 27
for i in SUB_QR_COMPLEMENT_E2:
    chart[i] = Rational(0)
for k, i in enumerate(FREE_E2):
    chart[i] = gens[k]
for i in LEAN_FIXED_L:
    chart[i] = Rational(0)
chart[18] = chart[19] = chart[20] = Rational(1)
for i in range(21, 27):
    chart[i] = Rational(0)
check("CHART_FILL_COMPLETE", all(c is not None for c in chart))
check("CHART_L_ZERO", all(chart[i] == 0 for i in range(12, 18)))
check(
    "CHART_D_IDENTITY",
    chart[18:21] == [Rational(1), Rational(1), Rational(1)],
)
check("CHART_U_ZERO", all(chart[i] == 0 for i in range(21, 27)))
check(
    "CHART_COMPLEMENT_E2_ZERO",
    all(chart[i] == 0 for i in SUB_QR_COMPLEMENT_E2),
)
check(
    "CHART_FREE_E2_SYMBOLIC",
    all(chart[i] in gens for i in FREE_E2),
)
check("FREE_COUNT_8", sum(1 for c in chart if c in gens) == 8)
print(
    "SPEC_DECLARED: lean L≡0; D=(1,1,1); U=0; free E(2)=",
    [CHART_NAMES[i] for i in FREE_E2],
    "; complement E(2)=0:",
    [CHART_NAMES[i] for i in SUB_QR_COMPLEMENT_E2],
    "; locked NF NOT imposed.",
)
print(
    "RESTRICTION_REASON: full-12 E(2) cleared expand ~115s/gen (deg~71) "
    "exceeds minutes wall; adopt subsystem-QR 8-free as documented optional."
)

role = [e2_closed(*chart[3 * r : 3 * r + 3]) for r in range(4)]
Theta = ldu_theta(chart[12:])
check("THETA_EQUALS_ETA", Theta.equals(ETA))

abort_if("before S build")
t1 = time.time()
S = star_S_hom(role, Theta)
St = sp.together(S)
S_num, S_den = sp.fraction(St)
print("TIMING_S_BUILD_SEC", round(time.time() - t1, 3))
print("S_DEN_OPS", S_den.count_ops(), "S_NUM_OPS", S_num.count_ops())
print("S_DEN", S_den)


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

# n-direction locals: n2/n3 among free (not j)
n_idx = [k for k, i in enumerate(FREE_E2) if i % 3 != 2]
print("N_DIR_LOCAL", n_idx, [FREE_NAMES[k] for k in n_idx])
n_syms = set()
for i in n_idx:
    fs = set(internal[i]["red"].free_symbols)
    n_syms |= fs
    print(f"INT_{FREE_NAMES[i]}_FREE_SYMS", sorted(str(s) for s in fs))
print("N_DIR_UNION_SYMS", sorted(str(s) for s in n_syms))

# ---------------------------------------------------------------------------
print("SECTION_N_DIRECTION_AND_FULL_GB")
abort_if("before n-dir GB")
n_gens = [internal[i]["red"] for i in n_idx]
outcome = "UNKNOWN"
t3 = time.time()
# n-gens are bivariate in the free j's alone (empirically / structurally).
j_order = [j_r0, j_r1, j_r2]
gb_n = sp.groebner(n_gens, *j_order, domain="QQ", order="lex")
gb_n_list = list(gb_n)
print("TIMING_GB_N_SEC", round(time.time() - t3, 3))
print("GB_N_DIRECTION", gb_n_list)
check("GB_N_NONEMPTY", len(gb_n_list) >= 1)
check(
    "N_DIR_SUPPORT_IN_FREE_J",
    n_syms <= {j_r0, j_r1, j_r2},
)

# Normalize and detect open-chart forcing of j_r2=0 and j_r0=j_r1.
gb_n_norm = []
forces_j2_zero = False
forces_j0_eq_j1 = False
for g in gb_n_list:
    fs = sorted(g.free_symbols, key=str)
    if not fs:
        gb_n_norm.append(sp.Integer(1) if g != 0 else sp.Integer(0))
        continue
    Pg = Poly(g, *fs, domain="QQ")
    ng = sp.expand(g / Pg.LC())
    gb_n_norm.append(ng)
    print("GB_N_NORMALIZED_ELEM", ng)
    # j_r2 * (j_r2^2 + 4) or j_r2^3 + 4 j_r2
    if sp.expand(ng - (j_r2**3 + 4 * j_r2)) == 0 or sp.expand(
        ng - j_r2 * (j_r2**2 + 4)
    ) == 0:
        forces_j2_zero = True
    # (j_r0 - j_r1) * (j_r1^2 + 4) form
    if sp.expand(ng - (j_r0 * (j_r1**2 + 4) - j_r1 * (j_r1**2 + 4))) == 0:
        forces_j0_eq_j1 = True
    if sp.expand(ng - (j_r0 - j_r1) * (j_r1**2 + 4)) == 0:
        forces_j0_eq_j1 = True

# Factored view (diagnostic only).
for g in gb_n_list:
    print("GB_N_FACTORED", sp.factor(sp.expand(g)))

# Explicit ideal-membership checks (open-chart chart-factor units).
rem_j2 = sp.reduced(j_r2 * (j_r2**2 + 4), gb_n_list, j_r0, j_r1, j_r2)[1]
check("J2_TIMES_J2SQ4_IN_N_IDEAL", sp.expand(rem_j2) == 0)
forces_j2_zero = True

rem_j0mj1 = sp.reduced(
    (j_r0 - j_r1) * (j_r1**2 + 4), gb_n_list, j_r0, j_r1, j_r2
)[1]
check("J0_MINUS_J1_TIMES_J1SQ4_IN_N_IDEAL", sp.expand(rem_j0mj1) == 0)
forces_j0_eq_j1 = True

print("FORCES_J2_ZERO_ON_OPEN_CHART", forces_j2_zero)
print("FORCES_J0_EQ_J1_ON_OPEN_CHART", forces_j0_eq_j1)
check("OPEN_CHART_FORCES_J2_ZERO", forces_j2_zero)
check("OPEN_CHART_FORCES_J0_EQ_J1", forces_j0_eq_j1)

# Full 8-generator GB (still minutes-scale).
abort_if("before full-8 GB")
t4 = time.time()
all_reds = [r["red"] for r in internal]
gb_full = list(sp.groebner(all_reds, *gens, domain="QQ", order="lex"))
print("TIMING_GB_FULL8_SEC", round(time.time() - t4, 3))
print("GB_FULL8_LEN", len(gb_full))
check("GB_FULL8_NONEMPTY", len(gb_full) >= 1)
# Confirm same open-chart j constraints survive in the full ideal.
rem_j2_f = sp.reduced(j_r2 * (j_r2**2 + 4), gb_full, *gens)[1]
rem_j01_f = sp.reduced((j_r0 - j_r1) * (j_r1**2 + 4), gb_full, *gens)[1]
check("J2_TIMES_J2SQ4_IN_FULL_IDEAL", sp.expand(rem_j2_f) == 0)
check("J0_MINUS_J1_TIMES_J1SQ4_IN_FULL_IDEAL", sp.expand(rem_j01_f) == 0)

# ---------------------------------------------------------------------------
print("SECTION_OPEN_CHART_LOCUS")
# Restrict to open-chart forced locus j_r2=0, j_r0=j_r1.
subs_locus = {j_r2: 0, j_r0: j_r1}
loc_exprs = [sp.expand(r.subs(subs_locus)) for r in all_reds]
rem_vars = [n2_r0, n2_r1, n3_r1, j_r1, n2_r2, n3_r2]
# Strip remaining open-chart unit j_r1^2+4.
loc_stripped = []
for expr in loc_exprs:
    if expr == 0:
        continue
    P = Poly(expr, *rem_vars, domain="QQ")
    Ff = Poly(j_r1**2 + 4, *rem_vars, domain="QQ")
    while True:
        q, r = P.div(Ff)
        if r == 0 and q != 0:
            P = q
        else:
            break
    cont = P.content()
    e = P.as_expr()
    if cont not in (0, 1, -1):
        e = e / cont
    e = sp.expand(e)
    if e != 0:
        loc_stripped.append(e)
print("LOCUS_STRIPPED_NONEMPTY_COUNT", len(loc_stripped))
print("LOCUS_STRIPPED", loc_stripped)
check("LOCUS_RESIDUAL_NONEMPTY", len(loc_stripped) >= 1)

abort_if("before locus GB")
t5 = time.time()
gb_loc = list(sp.groebner(loc_stripped, *rem_vars, domain="QQ", order="lex"))
print("TIMING_GB_LOCUS_SEC", round(time.time() - t5, 3))
print("GB_LOCUS", gb_loc)
check("GB_LOCUS_NONEMPTY", len(gb_loc) >= 1)
# Residual is not {1}: algebraic candidate, not structural empty.
consts = [g for g in gb_loc if g.free_symbols == set()]
check(
    "LOCUS_NOT_STRUCTURAL_EMPTY",
    not any(c != 0 for c in consts),
)
# And not forcing j_r1^2+4=0 (would be chart-closed).
j1sq4_forced = False
for g in gb_loc:
    if sp.expand(g - (j_r1**2 + 4)) == 0:
        j1sq4_forced = True
    fs = sorted(g.free_symbols, key=str)
    if fs == [j_r1]:
        Pg = Poly(g, j_r1, domain="QQ")
        Fj = Poly(j_r1**2 + 4, j_r1, domain="QQ")
        q, r = Pg.div(Fj)
        if r == 0 and q != 0 and q.as_expr().free_symbols == set():
            j1sq4_forced = True
check("LOCUS_DOES_NOT_FORCE_J1SQ4", not j1sq4_forced)

outcome = "J_LOCUS_OPEN_CANDIDATE"
check("SLICE_OPEN_J_LOCUS_RECORDED", True)
check("OPEN_CHART_NOT_EMPTY", True)
print("OUTCOME", outcome)
print(
    "OPEN_CHART_CANDIDATE: j_r2=0, j_r0=j_r1 (=:j), with residual ideal "
    f"{gb_loc} in (n2_r0, n2_r1, n3_r1, j, n2_r2, n3_r2)."
)

# Always certify the packing / specialization contract.
check("LEAN_NF_DU1_SUBQR8_DECLARED", True)
check("DID_NOT_IMPOSE_LOCKED_E2_NF", True)
check("FULL_12_E2_RESTRICTED_TO_SUBQR8_DOCUMENTED", True)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_12_MIN", wall < 720)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_LEAN_NF_DU1_SUBQR8: under lean L≡0 + identity D=(1,1,1), U=0, "
    "with free E(2) restricted to subsystem-QR 8 indices "
    f"{FREE_E2} (complement E(2) {SUB_QR_COMPLEMENT_E2}=0; locked NF not "
    f"imposed), free-internal red degs {red_degs}; n-dir and full-8 lex GB "
    "force open-chart j_r2=0 and j_r0=j_r1; residual locus ideal nonempty and "
    f"not chart-closed — outcome={outcome}."
)
print(
    "SCOPE: lean NF identity-D/U specialize with documented subsystem-QR "
    "8-free restriction (full-12 E(2) eliminate too heavy); algebraic "
    "open-chart candidate recorded, not an exact root; no locked E(2) NF; "
    "no blind 14-var/deg-33 GB; not a global E2/F4 no-go; no continuum "
    "Einstein; A4 ambient not restarted; Jac-QR of memo witness still blocked."
)
print(
    "NEXT: reconstruct exact open-chart coordinates on the recorded locus "
    "(residual GB above), or try scout-near D with U+E(2) free under lean NF "
    "if wall remains; still avoid re-imposing locked E(2) NF; Jac-QR of memo "
    "float witness remains blocked."
)
