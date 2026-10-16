#!/usr/bin/env python3
"""F4 Track B -- lean E(2) normal form: L≡0 only; release memo §5 E(2) NF.

Research-only. Exact packing + float sample Jac ranks. Minutes-scale.

Context: under L≡0 + fixed E(2) NF (-1/3,0,-1/3,1/2,1/2,-1/2,-1/2) on
slots [0..6], both scout-near one-sided D/U slices chart-close. Preferred
Jac-QR pivot recovery is blocked (homogeneous star_S ambient Euler does not
reproduce the memo float witness residual; see
a4d_curved_stationary_e2_euler_jac_qr_dump.json).

This certificate takes the documented alternate:
  * keep Iwasawa solder gauge L≡0 on slots [12..17];
  * release all seven former E(2) NF rationals (slots [0..6] become free);
  * free = all 12 E(2) + D + U (21); fixed = L only (6);
  * certify open-chart probe + float FD sample Jac ranks
    (internal 21, transverse 6, selected 8+6 subsystem);
  * box a next-specialize plan (no long GB this turn).

Does NOT claim an exact curved stationary root.
Does NOT recover float QR pivots (blocked; dump documents attempt).
Does NOT grind another scout-near one-sided D/U under the locked NF.
Does NOT run blind 14-var / deg-33 Groebner.
Does NOT open Holst/phi/new I-channels.
Does NOT assert global F4 no-go / continuum Einstein.
"""
from __future__ import annotations

import hashlib
import json
import time
from itertools import combinations
from pathlib import Path

import numpy as np
import sympy as sp
from sympy import Matrix, Rational, eye, zeros

t_wall0 = time.time()
WALL_SEC = 720


def check(name, cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_" + name)


def elapsed():
    return time.time() - t_wall0


ETA = sp.diag(1, -1, -1, -1)
ETA_F = np.diag([1.0, -1.0, -1.0, -1.0])
I4 = eye(4)
I4_F = np.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
G2 = sp.diag(*[ETA[a, a] * ETA[b, b] for a, b in PAIRS])
G2_F = np.diag([ETA_F[a, a] * ETA_F[b, b] for a, b in PAIRS])
STAR = zeros(6)
STAR_F = np.zeros((6, 6))
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
    STAR_F[PINDEX[q], PINDEX[p]] = s


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


def gen_boost_f(i):
    A = np.zeros((4, 4))
    A[0, i] = 1.0
    A[i, 0] = 1.0
    return A


def gen_rot_f(i, j):
    A = np.zeros((4, 4))
    A[i, j] = 1.0
    A[j, i] = -1.0
    return A


N2 = gen_boost(2) + gen_rot(1, 2)
N3 = gen_boost(3) + gen_rot(1, 3)
J23 = gen_rot(2, 3)
K1 = gen_boost(1)
M2 = gen_boost(2) - gen_rot(1, 2)
M3 = gen_boost(3) - gen_rot(1, 3)
N2_F = gen_boost_f(2) + gen_rot_f(1, 2)
N3_F = gen_boost_f(3) + gen_rot_f(1, 3)
J23_F = gen_rot_f(2, 3)
K1_F = gen_boost_f(1)
M2_F = gen_boost_f(2) - gen_rot_f(1, 2)
M3_F = gen_boost_f(3) - gen_rot_f(1, 3)
COMPL_F = (K1_F, M2_F, M3_F)


def e2_alg_f(n2, n3, j):
    return n2 * N2_F + n3 * N3_F + j * J23_F


def cayley_f(A):
    return (I4_F + 0.5 * A) @ np.linalg.inv(I4_F - 0.5 * A)


def cayley_diff_f(A, H):
    B = I4_F - 0.5 * A
    Binv = np.linalg.inv(B)
    P = (I4_F + 0.5 * A) @ Binv
    hH = 0.5 * H
    return hH @ Binv + P @ hH @ Binv


def ldu_theta_f(p):
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
    ) = p
    d3 = 1.0 / (d0 * d1 * d2)
    L = np.array(
        [[1.0, 0, 0, 0], [l10, 1, 0, 0], [l20, l21, 1, 0], [l30, l31, l32, 1]]
    )
    D = np.diag([d0, d1, d2, d3])
    U = np.array(
        [[1, u01, u02, u03], [0, 1, u12, u13], [0, 0, 1, u23], [0, 0, 0, 1.0]]
    )
    return L @ D @ U @ ETA_F


def orientation(face):
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inv = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inv % 2 else 1


def wedge_f(u, v):
    return np.array([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS], float)


def biv_f(X):
    Y = X @ ETA_F
    return np.array([Y[a, b] for a, b in PAIRS], float)


def curvature_f(P):
    return 0.5 * (P - np.linalg.inv(P))


def d_curvature_f(P, dP):
    Pinv = np.linalg.inv(P)
    return 0.5 * (dP + Pinv @ dP @ Pinv)


def star_S_f(role, Th):
    vs = [Th[:, r] for r in range(4)]
    site = 0.0
    for r, s in PAIRS:
        P = role[r] @ role[s] @ np.linalg.inv(role[r]) @ np.linalg.inv(role[s])
        C = biv_f(curvature_f(P))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * float(wedge_f(vs[u], vs[v]) @ G2_F @ STAR_F @ C)
    return 16.0 * site


def dS_trans_f(role, As, Th, r0, H):
    dP0 = cayley_diff_f(As[r0], H)
    vs = [Th[:, r] for r in range(4)]
    site = 0.0
    for r, s in PAIRS:
        Ur, Us = role[r], role[s]
        Uri, Usi = np.linalg.inv(Ur), np.linalg.inv(Us)
        dUr = dP0 if r == r0 else np.zeros((4, 4))
        dUs = dP0 if s == r0 else np.zeros((4, 4))
        dUri = (-Uri @ dUr @ Uri) if r == r0 else np.zeros((4, 4))
        dUsi = (-Usi @ dUs @ Usi) if s == r0 else np.zeros((4, 4))
        dP = (
            dUr @ Us @ Uri @ Usi
            + Ur @ dUs @ Uri @ Usi
            + Ur @ Us @ dUri @ Usi
            + Ur @ Us @ Uri @ dUsi
        )
        P = Ur @ Us @ Uri @ Usi
        dC = biv_f(d_curvature_f(P, dP))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * float(wedge_f(vs[u], vs[v]) @ G2_F @ STAR_F @ dC)
    return 16.0 * site


# ---------------------------------------------------------------------------
print("SECTION_JAC_QR_BLOCKER")
DUMP = Path(__file__).with_name("a4d_curved_stationary_e2_euler_jac_qr_dump.json")
check("JAC_QR_DUMP_PRESENT", DUMP.is_file())
dump = json.loads(DUMP.read_text())
check("JAC_QR_STATUS_BLOCKED", dump.get("status") == "NUMERICAL_BLOCKED_HONEST")
check("JAC_QR_PIVOTS_NOT_CLAIMED", dump.get("pivots_recovered") is False)
check("JAC_QR_J_NOT_FAKED", dump.get("J_persisted") is False)
print("JAC_QR_BLOCKER", dump["blocker"][:200] + "...")

# ---------------------------------------------------------------------------
print("SECTION_LEAN_NF_PACKING")
CHART_NAMES = (
    [f"e2_r{r}_{c}" for r in range(4) for c in ("n2", "n3", "j")]
    + [f"L_{k}" for k in range(6)]
    + [f"D_{k}" for k in range(3)]
    + [f"U_{k}" for k in range(6)]
)
# Lean: L≡0 only. Former E(2) NF slots [0..6] released to free.
FIXED_IDX = [12, 13, 14, 15, 16, 17]
FREE_IDX = [i for i in range(27) if i not in FIXED_IDX]
LEAN_FIXED_L = [Rational(0, 1)] * 6
# Locked-negative E(2) NF (documented; NOT imposed here).
LOCKED_E2_NF = [
    Rational(-1, 3),
    Rational(0, 1),
    Rational(-1, 3),
    Rational(1, 2),
    Rational(1, 2),
    Rational(-1, 2),
    Rational(-1, 2),
]

check("LEAN_FIXED_COUNT_6", len(FIXED_IDX) == 6)
check("LEAN_FREE_COUNT_21", len(FREE_IDX) == 21)
check("LEAN_IDX_PARTITION", sorted(FIXED_IDX + FREE_IDX) == list(range(27)))
check("LEAN_FIXED_ARE_L_SLOTS", FIXED_IDX == [12, 13, 14, 15, 16, 17])
check("LEAN_L_ALL_ZERO", all(x == 0 for x in LEAN_FIXED_L))
check(
    "LEAN_E2_NF_SLOTS_ALL_FREE",
    all(i in FREE_IDX for i in range(7)),
)
check(
    "LEAN_RELEASES_LOCKED_E2_NF",
    FREE_IDX[:7] == list(range(7)),
)
check(
    "LEAN_FREE_CONTAINS_ALL_E2",
    all(CHART_NAMES[i].startswith("e2_") for i in FREE_IDX[:12]),
)
check(
    "LEAN_FREE_CONTAINS_ALL_D",
    all(CHART_NAMES[i].startswith("D_") for i in FREE_IDX[12:15]),
)
check(
    "LEAN_FREE_CONTAINS_ALL_U",
    all(CHART_NAMES[i].startswith("U_") for i in FREE_IDX[15:21]),
)
check("LEAN_FEWER_FIXED_THAN_13", len(FIXED_IDX) < 13)
print("LEAN_FIXED_IDX", FIXED_IDX)
print("LEAN_FREE_IDX", FREE_IDX)
print("LEAN_FIXED_NAMES", [CHART_NAMES[i] for i in FIXED_IDX])
print("LEAN_FREE_NAMES", [CHART_NAMES[i] for i in FREE_IDX])
print(
    "RESULT_LEAN_PACK: L≡0 on [12..17] only (6 fixed); former memo-§5 E(2) NF "
    "slots [0..6] released; free = 12 E(2)+D+U (21). Locked-negative pattern "
    f"{[str(x) for x in LOCKED_E2_NF]} is NOT imposed."
)

# ---------------------------------------------------------------------------
print("SECTION_PROBE_OPEN_CHART")
# Rational-style float probe on 21 free coords (open chart).
PROBE = np.array(
    [0.1 + 0.07 * i for i in range(21)], dtype=float
)
# Indices in FREE for j_r0,j_r1,j_r2,j_r3 and D.
# FREE layout: e2_r0(n2,n3,j), e2_r1(...), e2_r2(...), e2_r3(...), D0,D1,D2, U...
j_local = [2, 5, 8, 11]
d_local = [12, 13, 14]
for ji in j_local:
    check(f"PROBE_J_IDX{ji}_SQ4_NONZERO", PROBE[ji] ** 2 + 4.0 != 0.0)
for di in d_local:
    check(f"PROBE_D_IDX{di}_NONZERO", abs(PROBE[di]) > 1e-12)
check("PROBE_ALL_FOUR_J_OPEN", all(PROBE[j] ** 2 + 4.0 != 0.0 for j in j_local))
check("PROBE_ALL_D_OPEN", all(abs(PROBE[d]) > 1e-12 for d in d_local))


def chart_at_free(free_vals):
    ch = np.zeros(27, dtype=float)
    for k, i in enumerate(FIXED_IDX):
        ch[i] = 0.0
    for k, i in enumerate(FREE_IDX):
        ch[i] = float(free_vals[k])
    return ch


def embed_free(free_vals):
    ch = chart_at_free(free_vals)
    As = [e2_alg_f(*ch[3 * r : 3 * r + 3]) for r in range(4)]
    role = [cayley_f(A) for A in As]
    Th = ldu_theta_f(ch[12:])
    return role, As, Th


def S_free(free_vals):
    role, _, Th = embed_free(free_vals)
    return star_S_f(role, Th)


def grad_free(free_vals, h=1e-6):
    S0 = S_free(free_vals)
    g = np.zeros(21)
    for j in range(21):
        fv = free_vals.copy()
        fv[j] = free_vals[j] + h
        g[j] = (S_free(fv) - S0) / h
    return g


def trans_free(free_vals):
    role, As, Th = embed_free(free_vals)
    out = []
    for r0 in (0, 1):
        for H in COMPL_F:
            out.append(dS_trans_f(role, As, Th, r0, H))
    return np.array(out, dtype=float)


# ---------------------------------------------------------------------------
print("SECTION_FLOAT_SAMPLE_JAC_RANKS")
t1 = time.time()
h = 1e-6
g0 = grad_free(PROBE, h=h)
check("INTERNAL_GRAD_FINITE", np.all(np.isfinite(g0)))
check("INTERNAL_GRAD_NONEZERO_PROBE", float(np.linalg.norm(g0)) > 1e-12)
Jac_int = np.zeros((21, 21))
for j in range(21):
    fv = PROBE.copy()
    fv[j] = PROBE[j] + h
    Jac_int[:, j] = (grad_free(fv, h=h) - g0) / h
# Numerical rank via singular values.
s_int = np.linalg.svd(Jac_int, compute_uv=False)
rank_int = int(np.sum(s_int > 1e-6 * s_int[0]))
print("INTERNAL_PROBE_JAC_RANK", rank_int)
print("INTERNAL_SINGULAR_VALUES_HEAD", [float(x) for x in s_int[:8]])
check("INTERNAL_PROBE_JAC_RANK_GE_8", rank_int >= 8)
check("INTERNAL_PROBE_JAC_RANK_LE_21", rank_int <= 21)
print("TIMING_INTERNAL_JAC_SEC", round(time.time() - t1, 3))

t2 = time.time()
tr0 = trans_free(PROBE)
check("TRANSVERSE_FINITE", np.all(np.isfinite(tr0)))
check("TRANSVERSE_NONEZERO_PROBE", float(np.linalg.norm(tr0)) > 1e-12)
Jac_tr = np.zeros((6, 21))
for j in range(21):
    fv = PROBE.copy()
    fv[j] = PROBE[j] + h
    Jac_tr[:, j] = (trans_free(fv) - tr0) / h
s_tr = np.linalg.svd(Jac_tr, compute_uv=False)
rank_tr = int(np.sum(s_tr > 1e-6 * max(s_tr[0], 1e-30)))
print("TRANSVERSE_PROBE_JAC_RANK", rank_tr)
check("TRANSVERSE_PROBE_JAC_FULL_RANK_6", rank_tr == 6)
print("TIMING_TRANSVERSE_JAC_SEC", round(time.time() - t2, 3))

# Greedy select 8 independent internal rows, form 8+6 subsystem on 21 cols;
# then take first 14 QR column pivots of that 14x21 block as a smoke free set.
selected_internal = []
span = []
for i in range(21):
    trial = span + [Jac_int[i, :]]
    M = np.vstack(trial)
    if np.linalg.matrix_rank(M, tol=1e-6 * np.linalg.norm(M, ord=2)) == len(trial):
        span = trial
        selected_internal.append(i)
        if len(selected_internal) == 8:
            break
check("SELECTED_INTERNAL_COUNT_8", len(selected_internal) == 8)
print("SELECTED_INTERNAL_ROWS", selected_internal)
Jac_sub = np.vstack([Jac_int[selected_internal, :], Jac_tr])
s_sub = np.linalg.svd(Jac_sub, compute_uv=False)
rank_sub = int(np.sum(s_sub > 1e-6 * s_sub[0]))
print("SUBSYSTEM_8P6_PROBE_JAC_RANK", rank_sub)
check("SUBSYSTEM_8P6_PROBE_JAC_RANK_14", rank_sub == 14)

# Column-pivoted QR on the 14x21 subsystem → candidate 14 free among 21.
from scipy.linalg import qr as sp_qr

Qb, Rb, pivb = sp_qr(Jac_sub, mode="economic", pivoting=True)
# pivb orders columns of Jac_sub (= FREE_IDX local indices)
sub_free_local = list(int(x) for x in pivb[:14])
sub_fixed_local = list(int(x) for x in pivb[14:])
SUB_FREE_IDX = [FREE_IDX[i] for i in sub_free_local]
SUB_FIXED_FROM_FREE = [FREE_IDX[i] for i in sub_fixed_local]
print("SUB_QR_FREE_LOCAL", sub_free_local)
print("SUB_QR_FREE_CHART_IDX", SUB_FREE_IDX)
print("SUB_QR_FREE_NAMES", [CHART_NAMES[i] for i in SUB_FREE_IDX])
print(
    "SUB_QR_REMAINING_FREE_AS_FIXED_CANDIDATES",
    [CHART_NAMES[i] for i in SUB_FIXED_FROM_FREE],
)
check("SUB_QR_FREE_COUNT_14", len(SUB_FREE_IDX) == 14)
check(
    "SUB_QR_TOTAL_FIXED_CANDIDATE_COUNT_13",
    len(FIXED_IDX) + len(SUB_FIXED_FROM_FREE) == 13,
)

# ---------------------------------------------------------------------------
print("SECTION_NEXT_SPECIALIZE_PLAN")
NEXT_PLAN = (
    "Under lean NF (L≡0 only; 21 free = all E(2)+D+U): do NOT re-impose the "
    "locked E(2) NF (-1/3,0,-1/3,1/2,1/2,-1/2,-1/2). Prefer (a) minutes-scale "
    "degree-reduced free-internal gens with D scout-near and U+E(2) free, or "
    "(b) identity-like D=U with E(2) fully free, filtering by open-chart "
    "(all four j_r^2+4 ≠ 0, D≠0) and four-channel R=R_*(C). Optional: adopt "
    f"subsystem-QR free chart idx {SUB_FREE_IDX} as a candidate 14-pack "
    f"(fixed complement = L≡0 + {SUB_FIXED_FROM_FREE}) for a square 8+6 "
    "specialize — still avoid blind 14-var / deg-33 GB. Jac-QR of the true "
    "memo float witness remains blocked until the residual operator is "
    "reconstructed."
)
print("NEXT_SPECIALIZE_PLAN", NEXT_PLAN)
check("NEXT_PLAN_AVOIDS_LOCKED_E2_NF", "locked E(2) NF" in NEXT_PLAN)
check("NEXT_PLAN_NO_BLIND_GB", "deg-33" in NEXT_PLAN)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_12_MIN", wall < WALL_SEC)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

print(
    "RESULT_E2_LEAN_NF_FREE_E2: Jac-QR pivot recovery remains blocked "
    "(honest dump; star_S ambient Euler ≠ memo float witness). Lean packing "
    f"L≡0 only (6 fixed) / free 21 = all E(2)+D+U. Float probe: internal Jac "
    f"rank {rank_int}, transverse rank {rank_tr}, selected 8+6 rank {rank_sub}; "
    f"subsystem-QR candidate FREE chart idx {SUB_FREE_IDX}."
)
print(
    "SCOPE: lean NF + sample Jac ranks + specialize plan only; no exact root; "
    "no Groebner this turn; no scout-near one-sided D/U under locked E(2) NF; "
    "QR of memo witness still unrecovered; not a global E2/F4 no-go; no "
    "continuum Einstein; A4 ambient not restarted."
)
print("NEXT:", NEXT_PLAN)
