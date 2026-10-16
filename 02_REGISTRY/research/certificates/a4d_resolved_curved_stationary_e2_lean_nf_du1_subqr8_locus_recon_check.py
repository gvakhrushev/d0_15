#!/usr/bin/env python3
"""F4 Track B -- reconstruct on lean-NF DU1/subQR8 open-chart j-locus.

Research-only. Exact rational / symbolic arithmetic. Minutes-scale.

Continues
`a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_check.py`
(L≡0; D=(1,1,1); U=0; subsystem-QR 8-free E(2) [0,2,3,4,5,6,7,8];
complement E(2) [1,9,10,11]=0; locked E(2) NF NOT imposed), which forced
open-chart

    j_r2 = 0,   j_r0 = j_r1

and recorded residual locus ideal (3 gens, not chart-closed):

    g1  = j*n2_r0 - j*n2_r1 + 2*n3_r1
    g2z = j*n3_r1*n3_r2 + 2*n2_r0*n3_r2 - 2*n2_r1*n3_r2 + 4*n2_r2*n3_r1
    g3  = j^2*n3_r2 + 4*j*n2_r2 - 4*n3_r2

This certificate RECONSTRUCTS that locus over Q:

  * solve residual ideal → open j≠0 parametric form
      n3_r1 = j*(n2_r1 - n2_r0)/2
      n2_r2 = n3_r2*(4 - j^2)/(4*j)
    with free (n2_r0, n2_r1, j, n3_r2);
  * free-internal of the reduced 4-param packing vanish identically;
  * exact rational CURVED open-chart witness
      (n2_r0,n2_r1,n3_r1,j,n2_r2,n3_r2)=(1,0,-1,2,0,0)
    with certified vanishing of all 8 ambient free-internal gens
    (1-symbol sweeps under the parent packing);
  * exact transverse (roles {0,1}×{K1,M2,M3}) at the curved witness
    recorded nonzero — not a full 8+6 root.

Does NOT re-impose locked E(2) NF.
Does NOT run blind 14-var / deg-33 Groebner / full-12 E(2) eliminate.
Does NOT claim a curved stationary root (free-internal family only).
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
WALL_SEC = 540


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
    A[i, j] = -1
    A[j, i] = 1
    return A


N2 = gen_boost(2) + gen_rot(1, 2)
N3 = gen_boost(3) + gen_rot(1, 3)
J23 = gen_rot(2, 3)
K1 = gen_boost(1)
M2 = gen_boost(2) - gen_rot(1, 2)
M3 = gen_boost(3) - gen_rot(1, 3)


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


def fill_chart_e2(e2_12):
    """Lean DU1/subQR8 packing from a length-12 E(2) tuple."""
    chart = [None] * 27
    for i in range(12):
        chart[i] = e2_12[i]
    for i in range(12, 18):
        chart[i] = Rational(0)
    chart[18] = chart[19] = chart[20] = Rational(1)
    for i in range(21, 27):
        chart[i] = Rational(0)
    return chart


# ---------------------------------------------------------------------------
print("SECTION_PACKING_AND_RESIDUAL_IDEAL")
SUB_QR_COMPLEMENT_E2 = [1, 9, 10, 11]
FREE_E2 = [0, 2, 3, 4, 5, 6, 7, 8]
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
check("FREE_E2_EXACT", FREE_E2 == [0, 2, 3, 4, 5, 6, 7, 8])
check("COMPLEMENT_E2_EXACT", SUB_QR_COMPLEMENT_E2 == [1, 9, 10, 11])
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
check("DID_NOT_IMPOSE_LOCKED_E2_NF", True)

n2_r0, n2_r1, n3_r1, j, n2_r2, n3_r2 = symbols(
    "n2_r0 n2_r1 n3_r1 j n2_r2 n3_r2"
)
# Parent-recorded residual gens (ZZ-friendly g2).
g1 = sp.expand(j * n2_r0 - j * n2_r1 + 2 * n3_r1)
g2z = sp.expand(
    j * n3_r1 * n3_r2
    + 2 * n2_r0 * n3_r2
    - 2 * n2_r1 * n3_r2
    + 4 * n2_r2 * n3_r1
)
g3 = sp.expand(j**2 * n3_r2 + 4 * j * n2_r2 - 4 * n3_r2)
print("RESIDUAL_G1", g1)
print("RESIDUAL_G2Z", g2z)
print("RESIDUAL_G3", g3)

rem_vars = [n2_r0, n2_r1, n3_r1, j, n2_r2, n3_r2]
gb = list(sp.groebner([g1, g2z, g3], *rem_vars, domain="QQ", order="lex"))
print("GB_RESIDUAL_LEN", len(gb))
for i, g in enumerate(gb):
    print(f"GB_RESIDUAL[{i}]", sp.factor(sp.expand(g)))
check("GB_RESIDUAL_NONEMPTY", len(gb) >= 1)
consts = [g for g in gb if g.free_symbols == set()]
check(
    "RESIDUAL_NOT_STRUCTURAL_EMPTY",
    not any(c != 0 for c in consts),
)
# Open-chart: does not force j^2+4=0.
jsq4_forced = False
for g in gb:
    if sp.expand(g - (j**2 + 4)) == 0:
        jsq4_forced = True
    fs = sorted(g.free_symbols, key=str)
    if fs == [j]:
        Pg = Poly(g, j, domain="QQ")
        Fj = Poly(j**2 + 4, j, domain="QQ")
        q, r = Pg.div(Fj)
        if r == 0 and q != 0 and q.as_expr().free_symbols == set():
            jsq4_forced = True
check("RESIDUAL_DOES_NOT_FORCE_JSQ4", not jsq4_forced)

sols = sp.solve([g1, g2z, g3], rem_vars, dict=True)
print("SOLVE_NSOLS", len(sols) if sols else 0)
check("SOLVE_NONEMPTY", bool(sols) and len(sols) >= 1)
sol0 = sols[0]
print("SOLVE_PRIMARY", sol0)
check(
    "OPEN_BRANCH_N3R1",
    n3_r1 in sol0
    and sp.expand(sol0[n3_r1] - j * (n2_r1 - n2_r0) / 2) == 0,
)
check(
    "OPEN_BRANCH_N2R2",
    n2_r2 in sol0
    and sp.expand(sol0[n2_r2] - n3_r2 * (4 - j * j) / (4 * j)) == 0,
)
print(
    "PARAMETRIC_OPEN_J_NEQ_0: n3_r1=j*(n2_r1-n2_r0)/2; "
    "n2_r2=n3_r2*(4-j^2)/(4*j); free=(n2_r0,n2_r1,j,n3_r2)."
)

# ---------------------------------------------------------------------------
print("SECTION_PARAMETRIC_FREE_INTERNAL_IDENTITY")
abort_if("before parametric S")
a, b, jj, ee = symbols("a b jj ee")
n3_r1_p = jj * (b - a) / 2
n2_r2_p = ee * (4 - jj * jj) / (4 * jj)
# E(2) 12-tuple under lean complement=0 + locus j_r2=0, j_r0=j_r1=jj.
e2_p = [
    a,
    Rational(0),
    jj,
    b,
    n3_r1_p,
    jj,
    n2_r2_p,
    ee,
    Rational(0),
    Rational(0),
    Rational(0),
    Rational(0),
]
chart_p = fill_chart_e2(e2_p)
check(
    "CHART_P_COMPLEMENT_ZERO",
    all(chart_p[i] == 0 for i in SUB_QR_COMPLEMENT_E2),
)
check("CHART_P_LOCUS_J2_ZERO", chart_p[8] == 0)
check("CHART_P_LOCUS_J0_EQ_J1", chart_p[2] == chart_p[5])

t1 = time.time()
role_p = [e2_closed(*chart_p[3 * r : 3 * r + 3]) for r in range(4)]
Theta_p = ldu_theta(chart_p[12:])
check("THETA_P_EQUALS_ETA", Theta_p.equals(ETA))
S_p = star_S_hom(role_p, Theta_p)
St_p = sp.together(S_p)
Sn_p, Sd_p = sp.fraction(St_p)
print("TIMING_S_PARAM_SEC", round(time.time() - t1, 3))
print("S_PARAM_DEN", Sd_p)

param_free = [a, b, jj, ee]
param_names = ["a_n2_r0", "b_n2_r1", "jj", "ee_n3_r2"]
t2 = time.time()
for g, name in zip(param_free, param_names):
    abort_if(f"param {name}")
    cleared = Sd_p * sp.diff(Sn_p, g) - Sn_p * sp.diff(Sd_p, g)
    poly_expr = sp.expand(cleared)
    print(
        f"PARAM_{name}_RAW_DEG",
        int(sp.total_degree(poly_expr)) if poly_expr != 0 else -1,
        "OPS",
        poly_expr.count_ops(),
    )
    check(f"PARAM_{name}_VANISHES", poly_expr == 0)
print("TIMING_PARAM_INTERNAL_SEC", round(time.time() - t2, 3))
check("PARAMETRIC_FREE_INTERNAL_IDENTICALLY_ZERO", True)

# ---------------------------------------------------------------------------
print("SECTION_EXACT_CURVED_WITNESS_AMBIENT_8")
# Witness on residual: (n2_r0,n2_r1,n3_r1,j,n2_r2,n3_r2)=(1,0,-1,2,0,0)
W_rem = {
    n2_r0: Rational(1),
    n2_r1: Rational(0),
    n3_r1: Rational(-1),
    j: Rational(2),
    n2_r2: Rational(0),
    n3_r2: Rational(0),
}
for label, cand in (("G1", g1), ("G2Z", g2z), ("G3", g3)):
    check(f"WITNESS_ON_{label}", sp.expand(cand.subs(W_rem)) == 0)
check("WITNESS_OPEN_JSQ4", sp.expand(W_rem[j] ** 2 + 4) != 0)
check("WITNESS_J_NONZERO", W_rem[j] != 0)

# Full E(2) 12-tuple at witness (complement slots 1,9,10,11 already 0).
e2_w = [
    Rational(1),
    Rational(0),
    Rational(2),  # r0
    Rational(0),
    Rational(-1),
    Rational(2),  # r1
    Rational(0),
    Rational(0),
    Rational(0),  # r2
    Rational(0),
    Rational(0),
    Rational(0),  # r3
]
check("WITNESS_COMPLEMENT_ZERO", all(e2_w[i] == 0 for i in SUB_QR_COMPLEMENT_E2))
check("WITNESS_LOCUS_J2_ZERO", e2_w[8] == 0)
check("WITNESS_LOCUS_J0_EQ_J1", e2_w[2] == e2_w[5])

chart_w = fill_chart_e2(e2_w)
role_w = [e2_closed(*chart_w[3 * r : 3 * r + 3]) for r in range(4)]
As_w = [e2_alg(*chart_w[3 * r : 3 * r + 3]) for r in range(4)]
Theta_w = ldu_theta(chart_w[12:])
check("WITNESS_THETA_ETA", Theta_w.equals(ETA))

curved_count = 0
for r, s in PAIRS:
    P = role_w[r] * role_w[s] * role_w[r].inv() * role_w[s].inv()
    C = curvature(P)
    nrm = sp.simplify(sum(C[i, j] ** 2 for i in range(4) for j in range(4)))
    if nrm != 0:
        curved_count += 1
        print(f"WITNESS_CURV_{r}{s}_SQNORM", nrm)
check("WITNESS_CURVED", curved_count >= 1)

# Ambient 8 free-internal via 1-symbol sweeps (parent FREE_E2 indices).
t3 = time.time()
for idx, name in zip(FREE_E2, FREE_NAMES):
    abort_if(f"ambient {name}")
    t = symbols("t")
    e2 = list(e2_w)
    e2[idx] = t
    chart = fill_chart_e2(e2)
    role = [e2_closed(*chart[3 * r : 3 * r + 3]) for r in range(4)]
    Theta = ldu_theta(chart[12:])
    S = star_S_hom(role, Theta)
    St = sp.together(S)
    Sn, Sd = sp.fraction(St)
    cleared = sp.expand(Sd * sp.diff(Sn, t) - Sn * sp.diff(Sd, t))
    val = sp.expand(cleared.subs(t, e2_w[idx]))
    print(f"WITNESS_AMB_{name}", val)
    check(f"WITNESS_AMB_{name}_ZERO", val == 0)
print("TIMING_AMBIENT_8_SEC", round(time.time() - t3, 3))
check("WITNESS_ALL_8_AMBIENT_FREE_INTERNAL_ZERO", True)

# Off-residual control: same locus but n3_r1=0 (should break residual).
e2_off = list(e2_w)
e2_off[4] = Rational(0)  # n3_r1
off_nonzero = False
t = symbols("t")
# Probe j_r2 direction (empirically sensitive off residual).
e2 = list(e2_off)
e2[8] = t
chart = fill_chart_e2(e2)
role = [e2_closed(*chart[3 * r : 3 * r + 3]) for r in range(4)]
Theta = ldu_theta(chart[12:])
S = star_S_hom(role, Theta)
St = sp.together(S)
Sn, Sd = sp.fraction(St)
cleared = sp.expand(Sd * sp.diff(Sn, t) - Sn * sp.diff(Sd, t))
val_off = sp.expand(cleared.subs(t, e2_off[8]))
print("OFF_RESIDUAL_AMB_j_r2", val_off)
check("OFF_RESIDUAL_AMB_j_r2_NONZERO", val_off != 0)

# Exact transverse at curved witness.
TRANSVERSE_DIRS = [
    (0, K1, "r0_K1"),
    (0, M2, "r0_M2"),
    (0, M3, "r0_M3"),
    (1, K1, "r1_K1"),
    (1, M2, "r1_M2"),
    (1, M3, "r1_M3"),
]
t4 = time.time()
trans_vals = []
for r0, H, label in TRANSVERSE_DIRS:
    g = sp.simplify(dS_transverse(role_w, As_w, Theta_w, r0, H))
    trans_vals.append(g)
    print(f"WITNESS_TRANS_{label}", g)
print("TIMING_TRANSVERSE_WITNESS_SEC", round(time.time() - t4, 3))
trans_all_zero = all(v == 0 for v in trans_vals)
print("WITNESS_TRANSVERSE_ALL_ZERO", trans_all_zero)
check("WITNESS_TRANSVERSE_RECORDED_NONZERO", not trans_all_zero)
check("WITNESS_NOT_FULL_8P6_ROOT", not trans_all_zero)

# ---------------------------------------------------------------------------
outcome = "LOCUS_RECON_FREE_INTERNAL_FAMILY"
check("LOCUS_RECONSTRUCTED_PARAMETRIC", True)
check("OPEN_CHART_CURVED_WITNESS_FREE_INTERNAL", True)
print("OUTCOME", outcome)
print(
    "RECONSTRUCTION: open j≠0 branch "
    "n3_r1=j*(n2_r1-n2_r0)/2, n2_r2=n3_r2*(4-j^2)/(4*j); "
    "reduced free-internal vanish identically on this 4-param family; "
    "exact curved witness (1,0,-1,2,0,0) has all 8 ambient free-internal=0 "
    "and transverse nonzero."
)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_12_MIN", wall < 720)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_LEAN_NF_DU1_SUBQR8_LOCUS_RECON: under lean L≡0 + D=(1,1,1), "
    "U=0, subsystem-QR 8-free packing, open-chart locus j_r2=0, j_r0=j_r1 "
    "residual ideal solved over Q to a 4-param open j≠0 family with "
    "free-internal identically zero; exact curved witness (1,0,-1,2,0,0) "
    "certifies all 8 ambient free-internal vanish; transverse at witness "
    f"nonzero — outcome={outcome}."
)
print(
    "SCOPE: free-internal reconstruction on recorded open-chart j-locus; "
    "4-param algebraic family, not a unique root; curved witness is "
    "free-internal-stationary but NOT transverse-stationary (not a full "
    "8+6 / Ready claim); locked E(2) NF not imposed; no blind 14-var/"
    "deg-33 GB; no continuum Einstein; Jac-QR still blocked; A4 ambient "
    "not restarted."
)
print(
    "NEXT: solve exact transverse on the 4-param free-internal family "
    "(or prove open-chart curved transverse-empty); cheap slice "
    "n2_r1=n3_r2=0 already forces n2_r0=0 (flat only) under transverse GB; "
    "still avoid locked E(2) NF / blind 14-var GB; filter R=R_*(C) if a "
    "full 8+6 point appears."
)
