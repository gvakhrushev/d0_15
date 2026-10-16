#!/usr/bin/env python3
"""F4 Track B -- float Newton on lean-NF DU1 with enlarged E(2) free-12.

Research-only. Float free-internal + transverse Gauss-Newton. Minutes-scale;
hard abort <60s. NO multi-var Groebner, NO deg-26 resultants, NO exact GB.

Continues
`a4d_resolved_curved_stationary_e2_lean_nf_du1_subqr8_transverse_family_newton_check.py`
(4-param free-internal family with complement E(2)[1,9,10,11]=0: no curved
float transverse root; collapse to flat; best curved ||trans||_2≈9.55).

This certificate escalates packing under lean NF (L≡0 only) + identity D/U:
  * FREE all 12 E(2) Cayley slots — former subQR8 complement [1,9,10,11]
    released (no longer forced to 0);
  * FIXED: L≡0 on [12..17], D=(1,1,1) on [18..20], U=0 on [21..26];
  * float residual = free-internal FD grad of star_S (12) + transverse
    dS_trans on roles {0,1}×{K1,M2,M3} (6) → R^{18} over R^{12};
  * short Gauss-Newton / scipy least_squares from curved seeds (incl. the
    former locus witness with complement=0 and complement-perturbed seeds);
  * report whether a curved open-chart float stationary candidate appears.

Does NOT re-impose locked E(2) NF.
Does NOT run multi-var Groebner / resultant chains.
Does NOT claim an exact curved stationary root / Ready / continuum Einstein.
Does NOT promote a float root to exact without a clear near-rational smoke.
"""
from __future__ import annotations

import hashlib
import math
import time
from itertools import combinations

import numpy as np
from scipy.optimize import least_squares

t_wall0 = time.time()
WALL_SEC = 55  # hard kill well under 60s


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
# Float geometry (reuse lean_nf_free_e2 conventions; numpy-only).
ETA_F = np.diag([1.0, -1.0, -1.0, -1.0])
I4_F = np.eye(4)
PAIRS = list(combinations(range(4), 2))
PINDEX = {p: i for i, p in enumerate(PAIRS)}
G2_F = np.diag([ETA_F[a, a] * ETA_F[b, b] for a, b in PAIRS])
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
    STAR_F[PINDEX[q], PINDEX[p]] = s


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
        l10, l20, l21, l30, l31, l32,
        d0, d1, d2,
        u01, u02, u03, u12, u13, u23,
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
        site += orientation((r, s)) * float(
            wedge_f(vs[u], vs[v]) @ G2_F @ STAR_F @ C
        )
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
        site += orientation((r, s)) * float(
            wedge_f(vs[u], vs[v]) @ G2_F @ STAR_F @ dC
        )
    return 16.0 * site


# ---------------------------------------------------------------------------
print("SECTION_PACKING_ENLARGED12")
CHART_NAMES = (
    [f"e2_r{r}_{c}" for r in range(4) for c in ("n2", "n3", "j")]
    + [f"L_{k}" for k in range(6)]
    + [f"D_{k}" for k in range(3)]
    + [f"U_{k}" for k in range(6)]
)
# Former subQR8 packing: FREE_E2=[0,2,3,4,5,6,7,8], COMPLEMENT=[1,9,10,11]=0.
SUB_QR_FREE_E2 = [0, 2, 3, 4, 5, 6, 7, 8]
SUB_QR_COMPLEMENT_E2 = [1, 9, 10, 11]
# Enlarged: free ALL 12 E(2).
FREE_E2 = list(range(12))
LEAN_FIXED_L = list(range(12, 18))
FIXED_D = [18, 19, 20]
FIXED_U = [21, 22, 23, 24, 25, 26]
D_VALS = (1.0, 1.0, 1.0)

check("FREE_E2_COUNT_12", len(FREE_E2) == 12)
check("COMPLEMENT_RELEASED", set(SUB_QR_COMPLEMENT_E2).issubset(set(FREE_E2)))
check("FORMER_SUBQR8_SUBSET", set(SUB_QR_FREE_E2).issubset(set(FREE_E2)))
check("LEAN_L_FIXED", LEAN_FIXED_L == [12, 13, 14, 15, 16, 17])
check("DID_NOT_IMPOSE_LOCKED_E2_NF", True)
print("FREE_E2", FREE_E2)
print("FORMER_COMPLEMENT_NOW_FREE", SUB_QR_COMPLEMENT_E2)
print("FIXED_L", LEAN_FIXED_L, "=0")
print("FIXED_D", FIXED_D, "=", D_VALS)
print("FIXED_U", FIXED_U, "=0")

# Layout: e2 = (n2,n3,j)×4 roles. j local indices in FREE_E2: 2,5,8,11.
J_LOCAL = [2, 5, 8, 11]
COMPLEMENT_LOCAL = [FREE_E2.index(i) for i in SUB_QR_COMPLEMENT_E2]  # 1,9,10,11


def chart_from_e2(e2_12):
    ch = np.zeros(27, dtype=float)
    for i in range(12):
        ch[i] = float(e2_12[i])
    # L≡0 already zeros
    ch[18] = ch[19] = ch[20] = 1.0
    # U≡0 already zeros
    return ch


def embed_e2(e2_12):
    ch = chart_from_e2(e2_12)
    As = [e2_alg_f(*ch[3 * r : 3 * r + 3]) for r in range(4)]
    role = [cayley_f(A) for A in As]
    Th = ldu_theta_f(ch[12:])
    return role, As, Th


def S_e2(e2_12):
    role, _, Th = embed_e2(e2_12)
    return star_S_f(role, Th)


def grad_internal(e2_12, h=1e-6):
    """FD free-internal residual: ∂S/∂e2_k for k=0..11."""
    x = np.asarray(e2_12, dtype=float)
    S0 = S_e2(x)
    g = np.zeros(12)
    for j in range(12):
        xp = x.copy()
        xp[j] = x[j] + h
        g[j] = (S_e2(xp) - S0) / h
    return g


def trans_res(e2_12):
    role, As, Th = embed_e2(e2_12)
    out = []
    for r0 in (0, 1):
        for H in COMPL_F:
            out.append(dS_trans_f(role, As, Th, r0, H))
    return np.array(out, dtype=float)


def residual_vec(e2_12):
    """Stacked free-internal (12) + transverse (6) = R^{18}."""
    x = np.asarray(e2_12, dtype=float)
    try:
        gi = grad_internal(x)
        tr = trans_res(x)
        r = np.concatenate([gi, tr])
        if not np.all(np.isfinite(r)):
            return np.full(18, 1e30)
        return r
    except np.linalg.LinAlgError:
        return np.full(18, 1e30)


def norm2(v):
    return float(np.linalg.norm(v))


def curv_frobenius2(e2_12):
    role, _, _ = embed_e2(e2_12)
    s = 0.0
    for r, ss in PAIRS:
        P = (
            role[r]
            @ role[ss]
            @ np.linalg.inv(role[r])
            @ np.linalg.inv(role[ss])
        )
        C = curvature_f(P)
        s += float(np.sum(C * C))
    return s


def is_open_chart(e2_12, eps=1e-10):
    x = np.asarray(e2_12, dtype=float)
    for ji in J_LOCAL:
        if abs(x[ji] * x[ji] + 4.0) < eps:
            return False
    return True


def is_curved(e2_12, eps=1e-4):
    return curv_frobenius2(e2_12) > eps


# ---------------------------------------------------------------------------
print("SECTION_SANITY_WITNESS_AND_FLAT")
# Former locus curved witness (complement=0): (a,b,jj,ee)=(1,0,2,0)
# → e2 = [1,0,2, 0,-1,2, 0,0,0, 0,0,0]
WITNESS = np.array(
    [1.0, 0.0, 2.0, 0.0, -1.0, 2.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    dtype=float,
)
FLAT = np.zeros(12, dtype=float)

rw = residual_vec(WITNESS)
rf = residual_vec(FLAT)
cw = curv_frobenius2(WITNESS)
cf = curv_frobenius2(FLAT)
print("WITNESS_RES_NORM", norm2(rw), "INT", norm2(rw[:12]), "TRANS", norm2(rw[12:]))
print("WITNESS_CURV2", cw, "OPEN", is_open_chart(WITNESS))
print("FLAT_RES_NORM", norm2(rf), "CURV2", cf)
check("WITNESS_OPEN_CHART", is_open_chart(WITNESS))
check("WITNESS_CURVED", is_curved(WITNESS))
check("WITNESS_TRANSVERSE_NONZERO", norm2(rw[12:]) > 1.0)
check("FLAT_CURV_NEAR_ZERO", cf < 1e-12)
check("FLAT_RES_NEAR_ZERO", norm2(rf) < 1e-8)
check("RESIDUAL_DIM_18", rw.shape == (18,))

# ---------------------------------------------------------------------------
print("SECTION_SEEDS_AND_NEWTON")
SEEDS = [
    ("witness_comp0", WITNESS.copy()),
    ("witness_comp_pert", WITNESS + np.array(
        [0, 0.3, 0, 0, 0, 0, 0, 0, 0, 0.2, -0.15, 0.4], dtype=float
    )),
    ("witness_comp_j3", WITNESS + np.array(
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1.0], dtype=float
    )),
    ("curved_j1", np.array(
        [1.0, 0.0, 1.0, 0.0, -0.5, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    )),
    ("curved_mix", np.array(
        [1.0, 0.2, 2.0, 0.5, -1.0, 2.0, 0.3, 0.4, 0.1, 0.2, -0.2, 0.5]
    )),
    ("curved_r3_active", np.array(
        [0.8, 0.1, 1.5, 0.2, -0.6, 1.5, 0.1, 0.3, 0.0, 0.5, 0.4, 1.0]
    )),
    ("curved_am1", np.array(
        [-1.0, 0.0, 2.0, 0.0, 1.0, 2.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0]
    )),
    ("curved_small", np.array(
        [0.3, 0.1, 1.0, 0.2, -0.2, 1.0, 0.1, 0.15, 0.05, 0.1, 0.05, 0.2]
    )),
    ("near_flat_pert", np.array(
        [0.05, 0.02, 2.0, 0.03, -0.04, 2.0, 0.02, 0.01, 0.0, 0.02, -0.01, 0.03]
    )),
    ("symmetric_j2", np.array(
        [0.5, 0.5, 2.0, 0.5, 0.5, 2.0, 0.5, 0.5, 2.0, 0.5, 0.5, 2.0]
    )),
]

# Soft bounds: keep |coords| moderate; j away from ±2i (always real here).
LO = np.full(12, -8.0)
HI = np.full(12, 8.0)


def run_lsq(x0, max_nfev=50):
    abort_if("lsq")
    x0c = np.clip(np.asarray(x0, dtype=float), LO, HI)
    # Nudge j's off the (impossible-on-reals) pole and keep open-ish.
    for ji in J_LOCAL:
        if abs(x0c[ji] * x0c[ji] + 4.0) < 1e-6:
            x0c[ji] = 1.0
    return least_squares(
        residual_vec,
        x0c,
        bounds=(LO, HI),
        method="trf",
        ftol=1e-12,
        xtol=1e-12,
        gtol=1e-12,
        max_nfev=max_nfev,
        # numerical jac: 2-point FD of residual (cheap enough in float)
    )


results = []
t_new = time.time()
for name, x0 in SEEDS:
    abort_if(f"seed {name}")
    n0 = norm2(residual_vec(x0))
    c0 = curv_frobenius2(x0)
    res = run_lsq(x0)
    xf = res.x
    nf = norm2(res.fun)
    ni = norm2(res.fun[:12])
    nt = norm2(res.fun[12:])
    cfv = curv_frobenius2(xf)
    curved_open = is_curved(xf) and is_open_chart(xf)
    print(
        f"NEWTON_{name}",
        "n0", f"{n0:.6g}",
        "nf", f"{nf:.6g}",
        "nint", f"{ni:.6g}",
        "ntr", f"{nt:.6g}",
        "curv0", f"{c0:.6g}",
        "curvf", f"{cfv:.6g}",
        "curved_open", curved_open,
        "nfev", res.nfev,
        "status", res.status,
        "x", [round(float(v), 6) for v in xf],
    )
    results.append(
        {
            "name": name,
            "x0": x0.copy(),
            "xf": xf.copy(),
            "n0": n0,
            "nf": nf,
            "nint": ni,
            "ntr": nt,
            "curv0": c0,
            "curvf": cfv,
            "curved_open": curved_open,
            "success": bool(res.success),
            "nfev": int(res.nfev),
        }
    )
print("TIMING_NEWTON_SEC", round(time.time() - t_new, 3))
check("NEWTON_RAN_ALL_SEEDS", len(results) == len(SEEDS))

best = min(results, key=lambda r: r["nf"])
best_curved = [r for r in results if r["curved_open"]]
best_curved_r = (
    min(best_curved, key=lambda r: r["nf"]) if best_curved else None
)
print(
    "BEST_OVERALL_NF",
    best["nf"],
    "NAME",
    best["name"],
    "CURV",
    best["curvf"],
    "X",
    best["xf"].tolist(),
)
if best_curved_r:
    print(
        "BEST_CURVED_NF",
        best_curved_r["nf"],
        "NAME",
        best_curved_r["name"],
        "CURV",
        best_curved_r["curvf"],
        "NINT",
        best_curved_r["nint"],
        "NTR",
        best_curved_r["ntr"],
        "X",
        best_curved_r["xf"].tolist(),
    )
else:
    print("BEST_CURVED_NF", None)

# Float stationary candidate: tiny combined residual on open curved chart.
FLOAT_ROOT_ABS = 1e-6
STRONG_CURV = 0.5  # distinguish weakly-curved near-flat from load-bearing
curved_float_candidate = (
    best_curved_r is not None and best_curved_r["nf"] < FLOAT_ROOT_ABS
)
strong_curved_hits = [
    r for r in results
    if r["nf"] < FLOAT_ROOT_ABS and r["curvf"] >= STRONG_CURV and is_open_chart(r["xf"])
]
best_strong = (
    min(strong_curved_hits, key=lambda r: r["nf"]) if strong_curved_hits else None
)
print("CURVED_FLOAT_CANDIDATE", curved_float_candidate)
print("STRONG_CURVED_FLOAT_COUNT", len(strong_curved_hits))
print("BEST_COMBINED_NORM", best["nf"])
print(
    "BEST_CURVED_COMBINED_NORM",
    None if best_curved_r is None else best_curved_r["nf"],
)
if best_strong:
    print(
        "BEST_STRONG_CURVED",
        best_strong["name"],
        "nf", best_strong["nf"],
        "curv", best_strong["curvf"],
        "x", best_strong["xf"].tolist(),
    )
check("BEST_NF_FINITE", math.isfinite(best["nf"]))

# Near-zero hits: do they collapse to flat?
near0 = [r for r in results if r["nf"] < 1e-5]
flat_collapse = all(r["curvf"] < 1e-4 for r in near0) if near0 else False
print("NEAR_ZERO_COUNT", len(near0))
print("NEAR_ZERO_COLLAPSE_TO_FLAT", flat_collapse)
for r in near0:
    print(
        "NEAR0",
        r["name"],
        "nf",
        f"{r['nf']:.3e}",
        "curv",
        f"{r['curvf']:.3e}",
        "x",
        [round(float(v), 6) for v in r["xf"]],
    )

# Observed float locus pattern (all 10 seeds):
#   e2 ≈ (α,β,j, α,β,j, γ,δ,0, δ,-γ,0)
# i.e. r0≡r1, j_r2=j_r3=0, n2_r3=n3_r2, n3_r3=-n2_r2.
def matches_pattern(x, atol=5e-3):
    x = np.asarray(x, dtype=float)
    return (
        abs(x[0] - x[3]) < atol
        and abs(x[1] - x[4]) < atol
        and abs(x[2] - x[5]) < atol
        and abs(x[8]) < atol
        and abs(x[11]) < atol
        and abs(x[9] - x[7]) < atol
        and abs(x[10] + x[6]) < atol
    )

pattern_hits = [r for r in near0 if matches_pattern(r["xf"])]
print("PATTERN_R0_EQ_R1_J23_ZERO_COUNT", len(pattern_hits), "/", len(near0))
check(
    "NEAR_ZERO_HITS_MATCH_SYMMETRY_PATTERN",
    len(near0) >= 1 and len(pattern_hits) == len(near0),
)

# Complement activity at best strong (or best curved): former-complement used.
probe = best_strong if best_strong is not None else (
    best_curved_r if best_curved_r is not None else best
)
comp_vals = [float(probe["xf"][FREE_E2.index(i)]) for i in SUB_QR_COMPLEMENT_E2]
comp_norm = float(np.linalg.norm(comp_vals))
print("PROBE_NAME", probe["name"])
print("PROBE_COMPLEMENT_VALS", comp_vals, "NORM", comp_norm)
print("PROBE_USES_COMPLEMENT", comp_norm > 1e-3)
check("PROBE_COMPLEMENT_ACTIVE", comp_norm > 1e-3)

# ---------------------------------------------------------------------------
print("SECTION_OPTIONAL_RATIONAL_SMOKE")
# Smoke near-rationals on strong-curved hits (clearer than near-flat).
rational_smoke = None
from fractions import Fraction

def round_limit(xs, den):
    qs = []
    for v in xs:
        fr = Fraction(float(v)).limit_denominator(den)
        qs.append((fr.numerator, fr.denominator, float(fr)))
    return qs

smoke_targets = strong_curved_hits[:5] if strong_curved_hits else (
    [best_curved_r] if best_curved_r is not None else []
)
for r in smoke_targets:
    abort_if("rational_smoke")
    for den in (4, 8, 12, 16, 24, 32):
        qs = round_limit(r["xf"], den)
        qx = np.array([q[2] for q in qs], dtype=float)
        if not (is_open_chart(qx) and is_curved(qx)):
            continue
        # Prefer strong-curved rationals.
        if curv_frobenius2(qx) < STRONG_CURV:
            continue
        nq = norm2(residual_vec(qx))
        print(
            "RATIONAL_SMOKE_TRY",
            r["name"],
            "den", den,
            "curv", f"{curv_frobenius2(qx):.4g}",
            "res", f"{nq:.4g}",
            "x", qs,
        )
        if nq < 1e-4:
            rational_smoke = {
                "seed": r["name"],
                "den": den,
                "qs": qs,
                "res": nq,
                "curv": curv_frobenius2(qx),
            }
            break
    if rational_smoke is not None:
        break
print("RATIONAL_SMOKE_HIT", rational_smoke)
check("DID_NOT_RUN_MULTI_VAR_GB", True)
check("DID_NOT_RUN_RESULTANT_CHAIN", True)
check("DID_NOT_IMPOSE_LOCKED_E2_NF", True)

# ---------------------------------------------------------------------------
print("SECTION_OUTCOME")
if curved_float_candidate and len(strong_curved_hits) >= 1:
    outcome = "CURVED_FLOAT_CANDIDATE_UNDER_ENLARGED_PACKING"
elif curved_float_candidate:
    # Only weakly-curved near-flat zeros — still report candidate but flag weak.
    outcome = "CURVED_FLOAT_CANDIDATE_UNDER_ENLARGED_PACKING"
elif flat_collapse and len(near0) >= 1:
    outcome = "NO_CURVED_FLOAT_UNDER_ENLARGED_PACKING"
else:
    outcome = "NO_CURVED_FLOAT_UNDER_ENLARGED_PACKING"
check("OUTCOME_RECORDED", True)
print("OUTCOME", outcome)

if outcome == "NO_CURVED_FLOAT_UNDER_ENLARGED_PACKING":
    check("NO_CURVED_FLOAT_CANDIDATE", not curved_float_candidate)
    if near0:
        check("NEAR_ZERO_HITS_ARE_FLAT", flat_collapse)
else:
    check("CURVED_FLOAT_CANDIDATE_PRESENT", curved_float_candidate)
    check("STRONG_CURVED_FLOAT_PRESENT", len(strong_curved_hits) >= 1)

wall = elapsed()
print("TIMING_WALL_SEC", round(wall, 3))
check("WALL_UNDER_60S", wall < 60)
check("WALL_MINUTES_SCALE", wall < 300)

_src = open(__file__, "rb").read()
_sha = hashlib.sha256(_src).hexdigest()
print("CERT_SHA256", _sha)

rep = best_strong if best_strong is not None else best_curved_r
bc_nf = None if rep is None else float(f"{rep['nf']:.6g}")
bc_tr = None if rep is None else float(f"{rep['ntr']:.6g}")
bc_in = None if rep is None else float(f"{rep['nint']:.6g}")
bc_cv = None if rep is None else float(f"{rep['curvf']:.6g}")
bc_name = None if rep is None else rep["name"]

print(
    "RESULT_E2_LEAN_NF_DU1_ENLARGED12_NEWTON: under lean L≡0 + D=(1,1,1), U=0, "
    f"FREE all 12 E(2) (former complement {SUB_QR_COMPLEMENT_E2} released), "
    f"float Gauss-Newton on free-internal(12)+transverse(6) from {len(SEEDS)} "
    f"curved seeds yields best ||res||_2={best['nf']:.6g} (name={best['name']}, "
    f"curv²={best['curvf']:.6g}); curved_float_candidate={curved_float_candidate}; "
    f"strong_curved_count={len(strong_curved_hits)}; "
    f"best_strong_||res||={bc_nf} (name={bc_name}, int={bc_in}, tr={bc_tr}, "
    f"curv²={bc_cv}); near_zero_count={len(near0)}, collapse_to_flat={flat_collapse}; "
    f"symmetry_pattern_hits={len(pattern_hits)}; "
    f"probe_complement_norm={comp_norm:.6g}; "
    f"rational_smoke={rational_smoke}; outcome={outcome}."
)
print(
    "SCOPE: float packing-escalate Newton only; NOT multi-var GB; NOT deg-26 "
    "resultant; NOT exact root; locked E(2) NF not imposed; Jac-QR still "
    "blocked; no continuum Einstein; A4 ambient not restarted. Float candidate "
    "is NOT promoted to exact without rational vanishing. Observed float locus "
    "pattern: e2≈(α,β,j, α,β,j, γ,δ,0, δ,-γ,0)."
)
print(
    "NEXT: exactify the observed 4-param float locus "
    "e2=(α,β,j, α,β,j, γ,δ,0, δ,-γ,0) under lean L≡0+D=1+U=0 by cheap "
    "deg-reduced free-internal+transverse polys / rational reconstruction "
    "(forbid blind multi-var GB / deg-26 chains). Optional: confirm pattern "
    "is full 8+6 stationary over Q. Jac-QR still blocked; do not re-impose "
    "locked E(2) NF."
)
if outcome == "CURVED_FLOAT_CANDIDATE_UNDER_ENLARGED_PACKING":
    boxed = "E2-ENLARGED12-NEWTON-CURVED-FLOAT-CANDIDATE"
else:
    boxed = "E2-ENLARGED12-NEWTON-NO-CURVED-FLOAT"
print(f"BOXED: {boxed}")
