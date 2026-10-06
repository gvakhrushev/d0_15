#!/usr/bin/env python3
"""F4 Track B -- gauge-canonical packing replacing provisional FIXED_13.

Research-only. Exact rational / symbolic arithmetic. Minutes-scale.

Context: two D/U specializations under provisional FIXED_13 packing
(slots [0,1,2,3,4,5,6,12..17] with memo-§5 rationals, including nonzero
values in the six strict-L slots) both force open-chart free-internal empty
via GB {j_r2+j_r3, j_r3^2+4}. Strong signal that packing / all-D/U fixing is
the wrong normal form for open-chart roots.

This certificate:

  * documents the QR-blocker: numerical E(2) scout Jacobian dump was never
    persisted, so rank-revealing QR pivot indices cannot be recovered from
    repo artifacts;
  * records the exact recompute formula for that missing artifact;
  * defines a gauge-canonical exact normal form replacing provisional
    FIXED_13: keep the same geometric free/fixed partition of the 27-chart,
    but set all six strict-L coordinates to 0 (Iwasawa / LDU solder gauge)
    and retain the seven E(2) NF rationals on roles 0–1 + role2.n2 from
    memo §5; free slots remain role2 {n3,j} + role3 E(2) + D + U (14), so
    D and U stay free (not specialized here);
  * certifies slots / free-fixed partition / L≡0 / open-chart probe;
  * samples exact rational FD Jacobians: internal 14×14 rank 14, transverse
    6×14 rank 6, selected 8+6 subsystem rank 14.

Does NOT recover float QR pivots (artifact missing).
Does NOT claim an exact curved stationary root.
Does NOT run Groebner / eliminate / specialize all D/U.
Does NOT open Holst/phi/new I-channels.
Does NOT assert global F4 no-go / continuum Einstein.
"""
from __future__ import annotations

import hashlib
import time
from itertools import combinations

import sympy as sp
from sympy import Matrix, Rational, eye, zeros

t_wall0 = time.time()
WALL_SEC = 480


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def elapsed():
    return time.time() - t_wall0


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
print("SECTION_QR_BLOCKER_MISSING_ARTIFACT")
# Honest blocker: memo §§5–7 records that rank-revealing QR on the numerical
# full Euler+scale Jacobian at the E(2) float root selected 14 pivot columns
# (nullity 13), but the Jac matrix / pivot permutation was never committed.
MISSING_ARTIFACT = (
    "numerical E(2)+LDU chart Jacobian dump at the float curved root: "
    "array J of shape (m, 27) with m>=40 (full Euler+scale residual wrt "
    "the 27-chart), plus the column-pivoted QR permutation (or explicit "
    "FREE_IDX / FIXED_IDX). Absent from repo tip, scout json "
    "(a4d_curved_stationary_cayley_scout_candidate.json has only link/LDU "
    "floats), and memo §§5–7 (values of FIXED_13 recorded; pivot slots not)."
)
RECOMPUTE_FORMULA = (
    "At float chart point x* in R^27 (memo §4.1 E(2) links + det-one LDU "
    "solder at the E(2) root), form residual F(x)=EL_full+scale in R^m, "
    "J = DF/Dx |_{x*} in R^{m x 27}; then Q,R,piv = "
    "scipy.linalg.qr(J, mode='economic', pivoting=True); "
    "FREE_IDX = list(piv[:14]); FIXED_IDX = list(piv[14:]); "
    "persist J (or at least piv) alongside FIXED_13 values."
)
print("QR_MISSING_ARTIFACT", MISSING_ARTIFACT)
print("QR_RECOMPUTE_FORMULA", RECOMPUTE_FORMULA)
check("QR_PIVOTS_UNRECOVERED_DOCUMENTED", True)
check("QR_RECOMPUTE_FORMULA_DOCUMENTED", "pivoting=True" in RECOMPUTE_FORMULA)

# ---------------------------------------------------------------------------
print("SECTION_GAUGE_CANONICAL_PACKING")
CHART_NAMES = (
    [f"e2_r{r}_{c}" for r in range(4) for c in ("n2", "n3", "j")]
    + [f"L_{k}" for k in range(6)]
    + [f"D_{k}" for k in range(3)]
    + [f"U_{k}" for k in range(6)]
)
# Same geometric slots as provisional packing, but L-values = 0 (gauge).
FIXED_IDX = [0, 1, 2, 3, 4, 5, 6, 12, 13, 14, 15, 16, 17]
FREE_IDX = [i for i in range(27) if i not in FIXED_IDX]
# Memo §5 first seven rationals on E(2) NF slots; last six = L ≡ 0.
GAUGE_FIXED_13 = [
    Rational(-1, 3),  # e2_r0_n2
    Rational(0, 1),   # e2_r0_n3
    Rational(-1, 3),  # e2_r0_j
    Rational(1, 2),   # e2_r1_n2
    Rational(1, 2),   # e2_r1_n3
    Rational(-1, 2),  # e2_r1_j
    Rational(-1, 2),  # e2_r2_n2
    Rational(0, 1),   # L_0
    Rational(0, 1),   # L_1
    Rational(0, 1),   # L_2
    Rational(0, 1),   # L_3
    Rational(0, 1),   # L_4
    Rational(0, 1),   # L_5
]
# Provisional packing put these nonzero memo-§5 tail values into L slots:
PROVISIONAL_L_VALUES = [
    Rational(4, 3),
    Rational(3, 2),
    Rational(1, 2),
    Rational(2, 3),
    Rational(-1, 3),
    Rational(-1, 1),
]

check("PACK_FIXED_COUNT_13", len(FIXED_IDX) == 13)
check("PACK_FREE_COUNT_14", len(FREE_IDX) == 14)
check("PACK_IDX_PARTITION", sorted(FIXED_IDX + FREE_IDX) == list(range(27)))
check(
    "PACK_FIXED13_ALL_RATIONAL",
    all(isinstance(x, sp.Rational) for x in GAUGE_FIXED_13),
)
check("PACK_L_SLOTS_ARE_12_TO_17", FIXED_IDX[7:] == [12, 13, 14, 15, 16, 17])
check(
    "PACK_L_ALL_ZERO_GAUGE",
    all(GAUGE_FIXED_13[k] == 0 for k in range(7, 13)),
)
check(
    "PACK_DIFFERS_FROM_PROVISIONAL_L",
    GAUGE_FIXED_13[7:] != PROVISIONAL_L_VALUES,
)
check(
    "PACK_FREE_CONTAINS_ALL_D",
    all(CHART_NAMES[i].startswith("D_") for i in FREE_IDX[5:8]),
)
check(
    "PACK_FREE_CONTAINS_ALL_U",
    all(CHART_NAMES[i].startswith("U_") for i in FREE_IDX[8:14]),
)
check("PACK_D_AND_U_STAY_FREE", len(FREE_IDX[5:14]) == 9)

print("PACK_FIXED_IDX", FIXED_IDX)
print("PACK_FREE_IDX", FREE_IDX)
print("PACK_FIXED_NAMES", [CHART_NAMES[i] for i in FIXED_IDX])
print("PACK_FREE_NAMES", [CHART_NAMES[i] for i in FREE_IDX])
print("PACK_GAUGE_FIXED_13", [str(x) for x in GAUGE_FIXED_13])
print(
    "RESULT_PACK: gauge-canonical packing declared; L≡0 (Iwasawa solder "
    "gauge); E(2) NF on roles 0–1 + role2.n2 from memo §5; free = "
    "e2_r2_{n3,j} + e2_r3_* + D_* + U_* (14). Replaces provisional FIXED_13 "
    "nonzero L-slot assignment. QR pivots still unrecovered."
)

# ---------------------------------------------------------------------------
print("SECTION_PROBE_JAC_RANKS_8P6")
PROBE = [Rational(1, 7) + Rational(i, 11) for i in range(14)]
h = Rational(1, 50)

# Chart-open at probe: j2=free[1], j3=free[4], D=free[5:8].
j2v, j3v = PROBE[1], PROBE[4]
d0v, d1v, d2v = PROBE[5], PROBE[6], PROBE[7]
check("PROBE_J2SQ4_NONZERO", j2v**2 + 4 != 0)
check("PROBE_J3SQ4_NONZERO", j3v**2 + 4 != 0)
check("PROBE_D_NONZERO", d0v != 0 and d1v != 0 and d2v != 0)


def chart_at(free_vals):
    ch = [None] * 27
    for k, i in enumerate(FIXED_IDX):
        ch[i] = GAUGE_FIXED_13[k]
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
    for r0, H in (
        (0, K1),
        (0, M2),
        (0, M3),
        (1, K1),
        (1, M2),
        (1, M3),
    ):
        out.append(sp.simplify(dS_transverse(role_r, As_r, Th, r0, H)))
    return Matrix(out)


t1 = time.time()
g0 = grad_S_at(PROBE)
check("INTERNAL_GRAD_ALL_NONZERO_AT_PROBE", all(g0[i] != 0 for i in range(14)))
Jac_rows = []
for j in range(14):
    fv = list(PROBE)
    fv[j] = PROBE[j] + h
    gj = grad_S_at(fv)
    Jac_rows.append([sp.simplify((gj[i] - g0[i]) / h) for i in range(14)])
Jac_int = Matrix(Jac_rows).T
rank_int = Jac_int.rank()
print("INTERNAL_PROBE_JAC_RANK", rank_int)
check("INTERNAL_PROBE_JAC_FULL_RANK_14", rank_int == 14)
print("TIMING_INTERNAL_JAC_SEC", round(time.time() - t1, 3))

t2 = time.time()
tr0 = trans_vec_at(PROBE)
check("TRANSVERSE_ALL_NONZERO_AT_PROBE", all(tr0[i] != 0 for i in range(6)))
Jac_tr_rows = []
for j in range(14):
    fv = list(PROBE)
    fv[j] = PROBE[j] + h
    trj = trans_vec_at(fv)
    Jac_tr_rows.append([sp.simplify((trj[i] - tr0[i]) / h) for i in range(6)])
Jac_tr = Matrix(Jac_tr_rows).T
rank_tr = Jac_tr.rank()
print("TRANSVERSE_PROBE_JAC_RANK", rank_tr)
check("TRANSVERSE_PROBE_JAC_FULL_RANK_6", rank_tr == 6)
print("TIMING_TRANSVERSE_JAC_SEC", round(time.time() - t2, 3))

# Greedy internal pivots for 8+6 subsystem (same recipe as polys/deg-reduce).
selected_internal = []
span_rows = []
for i in range(14):
    trial = span_rows + [Jac_int.row(i)]
    if Matrix.vstack(*trial).rank() == len(trial):
        span_rows = trial
        selected_internal.append(i)
        if len(selected_internal) == 8:
            break
check("SELECTED_INTERNAL_COUNT_8", len(selected_internal) == 8)
print("SELECTED_INTERNAL_ROWS", selected_internal)

Jac_sub = Matrix.vstack(Jac_int[selected_internal, :], Jac_tr)
rank_sub = Jac_sub.rank()
print("SUBSYSTEM_8P6_PROBE_JAC_RANK", rank_sub)
check("SUBSYSTEM_8P6_PROBE_JAC_FULL_RANK_14", rank_sub == 14)

# Complement basis sanity (unchanged from prior E2 certs).
def _vec(A):
    return Matrix(16, 1, lambda i, _j: A[i // 4, i % 4])


_basis6 = Matrix.hstack(*[_vec(G) for G in (N2, N3, J23, K1, M2, M3)])
check("SO13_E2_PLUS_COMPL_BASIS_RANK_6", _basis6.rank() == 6)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_12_MIN", wall < 720)

# Hash of this certificate source for audit trail.
_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_GAUGE_CANONICAL_PACKING: QR pivot recovery blocked (missing "
    "numerical Jac dump; recompute formula recorded). Replaced provisional "
    "FIXED_13 by gauge-canonical packing with L≡0 on slots [12..17] and memo "
    "§5 E(2) NF on slots [0..6]; free = e2_r2_{n3,j}+e2_r3_*+D+U (14). Exact "
    f"rational FD sample: internal Jac rank {rank_int}, transverse rank "
    f"{rank_tr}, selected 8+6 subsystem rank {rank_sub}."
)
print(
    "SCOPE: packing + sample Jac ranks only; no exact root; no Groebner; "
    "no D/U specialization this turn; QR pivots still unrecovered; not a "
    "global E2/F4 no-go; no continuum Einstein claim; A4 ambient FD not "
    "restarted."
)
print(
    "NEXT: under this gauge-canonical packing, keep D free with scout-near U "
    "(or selected U free with scout-near D) on degree-reduced gens; or "
    "recompute/persist the missing Jac dump and replace FREE/FIXED by true "
    "QR pivots; still avoid blind 14-var / deg-33 Groebner; filter by "
    "four-channel R=R_*(C)."
)
