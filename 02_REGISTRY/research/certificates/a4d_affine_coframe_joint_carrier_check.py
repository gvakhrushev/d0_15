#!/usr/bin/env python3
"""Exact flat forward-coframe image in the J2 (q,connection) carrier.

Can-fail certificate for EXP-A4D-AFFINE-COFRAME-PERIOD-DESCENT.

It rebuilds the accepted polarized HAB/HAQ symbols from the merged census,
constructs the quotient-coordinate image of one forward-coframe Fourier
amplitude, validates the convention against the already-owned L=2 Hessian-null
statement, and then tests all nine singular L=4 orbit representatives.

No nonlinear affine gauge symmetry is claimed.
"""
from __future__ import annotations

import os
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "a4d_joint_resonance_linear_kernel_check.py")

text = open(SRC, encoding="utf-8").read()
cut = text.index("# ---------------------------------------------------------------------------\n# 2. Reproduce the nine owned singular orbit types")
ns = {"__name__": "_symbol_builder", "__file__": SRC}
exec(compile(text[:cut], SRC, "exec"), ns)

HAB = ns["HAB"]
HAQ = ns["HAQ"]
z = ns["z"]
ETA = ns["ETA"]
LORENTZ = ns["LORENTZ"]
SYM = ns["SYM"]

ROOT = [sp.Integer(1), sp.I, sp.Integer(-1), -sp.I]
L4_IDS = [
    (0, 0, 1, 1),
    (0, 0, 1, 3),
    (0, 1, 1, 2),
    (1, 0, 1, 2),
    (1, 1, 1, 1),
    (1, 1, 3, 3),
    (2, 0, 1, 1),
    (2, 1, 1, 2),
    (2, 1, 2, 3),
]

FAIL = []


def check(name, cond, detail=""):
    if cond:
        print("PASS_" + name)
    else:
        FAIL.append(name)
        print("FAIL_" + name + (" :: " + detail if detail else ""))


def is_zero(M):
    return all(sp.simplify(M[i, j]) == 0
               for i in range(M.rows) for j in range(M.cols))


def lorentz_coeffs(X):
    """Coordinates in the accepted [K1,K2,K3,J12,J13,J23] basis."""
    out = sp.Matrix([
        X[0, 1], X[0, 2], X[0, 3],
        X[1, 2], X[1, 3], X[2, 3],
    ])
    rebuilt = sp.zeros(4)
    for j, g in enumerate(LORENTZ):
        rebuilt += out[j] * g
    check("LORENTZ_COORD_REBUILD", is_zero(sp.expand(rebuilt - X)))
    return out


def coframe_to_joint(phase):
    """Return the complex 34x4 map xi -> (q,x) in one table-character sector.

    The physical real carrier pairs this sector with its conjugate. Start with
    H_raw[r,:] = (phase_r - 1) xi^T and raw connection zero, then move to the
    #208 metric section H(q)=1/2 q eta by the compensating local Lorentz
    vertical.
    """
    phase = list(phase)
    G = sp.zeros(34, 4)
    for col in range(4):
        xi = sp.eye(4)[:, col]
        Hraw = sp.zeros(4)
        for r in range(4):
            for a in range(4):
                Hraw[r, a] = (phase[r] - 1) * xi[a]

        q = sp.expand(Hraw * ETA + ETA * Hraw.T)
        Hsec = sp.expand(sp.Rational(1, 2) * q * ETA)
        Delta = sp.expand(Hraw - Hsec)
        lam = sp.expand(Delta.T)

        check("SECTION_DIFFERENCE_IN_DQ_KERNEL",
              is_zero(sp.expand(Delta * ETA + ETA * Delta.T)))
        check("COMPENSATOR_IS_LORENTZ",
              is_zero(sp.expand(lam.T * ETA + ETA * lam)))

        for j, (a, b) in enumerate(SYM):
            G[j, col] = q[a, b]

        for r in range(4):
            Xr = sp.expand((phase[r] - 1) * lam)
            coeff = lorentz_coeffs(Xr)
            for j in range(6):
                G[10 + 6 * r + j, col] = coeff[j]

    return G


def joint_residual(zeta):
    sub = {z[j]: zeta[j] for j in range(4)}
    H = HAB.subs(sub)
    S = HAQ.subs(sub)
    G = coframe_to_joint(zeta)
    qG = G[:10, :]
    xG = G[10:, :]

    # Complex polarized stationarity system whose realification is #262.
    top = sp.expand(S.T * xG)
    bottom = sp.expand(S * qG + H * xG)
    return G, top, bottom


# Hostile convention test: #175 owns every nonzero L=2 forward-coframe tangent
# as a flat Hessian null. The same map must reproduce that fact before L4 use.
L2 = [sp.Integer(1), sp.Integer(-1)]
l2_nonzero = 0
for a in L2:
    for b in L2:
        for c in L2:
            for d in L2:
                zz = (a, b, c, d)
                if zz == (1, 1, 1, 1):
                    continue
                l2_nonzero += 1
                sub = {z[j]: zz[j] for j in range(4)}
                H = HAB.subs(sub)
                S = HAQ.subs(sub)
                G = coframe_to_joint(zz)
                qG = G[:10, :]
                xG = G[10:, :]
                check("L2_GAUGE_MAP_RANK4", G.rank() == 4, str(zz))
                check(
                    "L2_FORWARD_COFRAME_JOINT_NULL",
                    is_zero(S.T * xG) and is_zero(S * qG + H * xG),
                    str(zz),
                )
check("L2_ALL_15_NONZERO_CHECKED", l2_nonzero == 15)


def real_pair(M):
    R = sp.re(M)
    I = sp.im(M)
    return sp.Matrix.vstack(
        sp.Matrix.hstack(R, -I),
        sp.Matrix.hstack(I, R),
    )


def realify_joint_map(G):
    # #262 ordering is [Re q, Im q, Re x, Im x], not global realification.
    return sp.Matrix.vstack(real_pair(G[:10, :]), real_pair(G[10:, :]))


EXPECTED_RESIDUAL_RANK = [6, 6, 8, 8, 6, 8, 8, 8, 6]
EXPECTED_INTERSECTION = {
    0: (2, 2, 0, "metric-only"),
    1: (2, 2, 2, "mixed"),
    4: (2, 2, 0, "metric-only"),
    8: (2, 2, 2, "mixed"),
}

print()
print("L4 singular orbit forward-coframe image in the physical real carrier:")
rows = []
for n, ids in enumerate(L4_IDS):
    zeta = tuple(ROOT[i] for i in ids)
    sub = {z[j]: zeta[j] for j in range(4)}
    H = HAB.subs(sub)
    S = HAQ.subs(sub)

    Ar = real_pair(H)
    Cr = real_pair(S)
    HJr = sp.Matrix.vstack(
        sp.Matrix.hstack(sp.zeros(20, 20), Cr.T),
        sp.Matrix.hstack(Cr, Ar),
    )

    G = coframe_to_joint(zeta)
    Gc = coframe_to_joint(tuple(sp.conjugate(v) for v in zeta))
    check("ORBIT_%d_MAP_CONJUGATION" % n, Gc == sp.conjugate(G))
    Gr = realify_joint_map(G)
    residual = sp.simplify(HJr * Gr)

    check("ORBIT_%d_REAL_IMAGE_RANK8" % n, Gr.rank() == 8)
    check("ORBIT_%d_METRIC_EULER_ZERO" % n, residual[:20, :].rank() == 0)
    check(
        "ORBIT_%d_CONNECTION_RESIDUAL_RANK" % n,
        residual[20:, :].rank() == EXPECTED_RESIDUAL_RANK[n],
        "got %d expected %d"
        % (residual[20:, :].rank(), EXPECTED_RESIDUAL_RANK[n]),
    )

    ker = residual.nullspace()
    K = sp.Matrix.hstack(*ker) if ker else sp.zeros(8, 0)
    inter = sp.simplify(Gr * K)
    qproj = inter[:20, :]
    xproj = inter[20:, :]
    dim_inter = inter.rank()

    if n in EXPECTED_INTERSECTION:
        exp_dim, exp_q, exp_x, kind = EXPECTED_INTERSECTION[n]
        check("ORBIT_%d_INTERSECTION_DIM" % n, dim_inter == exp_dim)
        check("ORBIT_%d_INTERSECTION_Q_RANK" % n, qproj.rank() == exp_q)
        check("ORBIT_%d_INTERSECTION_X_RANK" % n, xproj.rank() == exp_x)

        if kind == "metric-only":
            # The full #262 metric-only block has dim ker(C_real)=2.
            metric_kernel = Cr.nullspace()
            MK = sp.Matrix.hstack(*metric_kernel)
            check("ORBIT_%d_METRIC_KERNEL_DIM2" % n, MK.rank() == 2)
            check(
                "ORBIT_%d_AFFINE_INTERSECTION_EQUALS_METRIC_ONLY" % n,
                xproj.rank() == 0
                and qproj.rank() == 2
                and sp.Matrix.hstack(MK, qproj).rank() == 2,
            )
        else:
            # Both projections inject on the 2D intersection: no nonzero pure leg.
            check(
                "ORBIT_%d_INTERSECTION_GENUINELY_MIXED" % n,
                dim_inter == 2 and qproj.rank() == 2 and xproj.rank() == 2,
            )
    else:
        check("ORBIT_%d_INTERSECTION_ZERO" % n, dim_inter == 0)

    rows.append(
        (
            n,
            ids,
            Gr.rank(),
            residual[20:, :].rank(),
            dim_inter,
            qproj.rank(),
            xproj.rank(),
        )
    )
    print(
        "ORBIT",
        n,
        ids,
        "image_rank",
        Gr.rank(),
        "connection_residual_rank",
        residual[20:, :].rank(),
        "intersection",
        dim_inter,
        "q_rank",
        qproj.rank(),
        "x_rank",
        xproj.rank(),
    )

check(
    "NO_L4_ORBIT_HAS_FULL_AFFINE_IMAGE_IN_JOINT_KERNEL",
    all(row[4] < row[2] for row in rows),
)
check(
    "NONZERO_INTERSECTION_ORBITS_0_1_4_8",
    [row[0] for row in rows if row[4] > 0] == [0, 1, 4, 8],
)

if FAIL:
    print("RESULT: FAIL", len(FAIL))
    for name in FAIL:
        print(" -", name)
    raise SystemExit(1)

print("RESULT: PASS")
print("L2_CONTROL: all 15 nontrivial forward-coframe images are exact joint Hessian nulls.")
print("L4_RESULT: the real affine/coframe image has rank 8 on every singular orbit and is never wholly joint-null.")
print("L4_INTERSECTIONS: orbit 0 metric-only dim2; orbit 1 mixed dim2; orbit 4 metric-only dim2; orbit 8 mixed dim2; all other singular orbits zero.")
print("L4_METRIC_ONLY: on orbits 0 and 4 the affine/coframe null intersection equals the complete #262 metric-only 2-plane.")
print("SCOPE: exact flat linear descent only; no nonlinear affine gauge symmetry or quotient.")
