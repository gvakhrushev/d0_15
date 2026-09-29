#!/usr/bin/env python3
"""Corrected exact Y normal-jet compatibility at z=1.

The historical response checker is reused only for the literal face Hessian,
Cayley Y vacuum, bordered rational solve, and basic finite-action primitives.
The mixed blocks are rebuilt with the placement signs
D_Q E_K ~ lambda^(-s), D_K E_Q ~ lambda^(+s).

The final constant-order condition is only fast-phase erasure (smooth source);
the Einstein value is compared afterwards and is not imposed.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_response_quotient_check as B

ROOT = Path(__file__).resolve().parents[3]
RESULT_PATH = ROOT / "02_REGISTRY/research/certificates/a4d_y_curved_normaljet_compatibility_results.json"

I4, PAIRS, SYM, GEN = B.I4, B.PAIRS, B.SYM, B.GEN
G2, STAR = B.G2, B.STAR
DIRPAIRS = [(i, j) for i in range(4) for j in range(i, 4)]


def check(name, cond, detail=""):
    if not cond:
        raise AssertionError(name + (": " + detail if detail else ""))
    print("PASS_" + name)


def dm_rank(M):
    return DomainMatrix.from_Matrix(M).convert_to(QQ).rank()


def dm_kernel_columns(M):
    raw = DomainMatrix.from_Matrix(M).convert_to(QQ).nullspace().to_Matrix()
    return raw.T if raw.rows else sp.zeros(M.cols, 0)


def matrix_json(M):
    return [[str(sp.factor(M[i, j])) for j in range(M.cols)] for i in range(M.rows)]


def centers(H, labels, z):
    tangent_scale = sp.Rational(4, 1) / (4 + 3 * z * z)
    index = {label: i for i, label in enumerate(labels)}
    ny, nd = sp.zeros(96, 1), sp.zeros(96, 1)
    for phase, sign in ((0, 1), (2, -1)):
        for g, coeff in ((3, 1), (4, -1), (5, 1)):
            ny[index[(phase, 0, g)], 0] = sign * tangent_scale * coeff
    for phase, sign in ((0, -1), (2, 1)):
        for g in (0, 1, 2):
            nd[index[(phase, 0, g)], 0] = sign
    N = sp.Matrix.hstack(ny, nd)
    check("CURVED_EXACT_CENTER", H * N == sp.zeros(96, 2) and N.T * H == sp.zeros(2, 96))
    return N


def with_base_phases(faces0):
    faces = []
    k = 0
    for phase in range(4):
        for _ in PAIRS:
            a, b, locs, local, Hloc, factors = faces0[k]
            faces.append((phase, a, b, locs, local, Hloc, factors))
            k += 1
    return faces


def blocks_all(H, face_data, labels):
    idx = {x: i for i, x in enumerate(labels)}
    A1 = [sp.zeros(96) for _ in range(4)]
    A2 = {ij: sp.zeros(96) for ij in DIRPAIRS}
    M0 = sp.zeros(96, 10)
    M1 = [sp.zeros(96, 10) for _ in range(4)]
    M2 = {ij: sp.zeros(96, 10) for ij in DIRPAIRS}
    C0 = sp.zeros(40, 96)
    C1 = [sp.zeros(40, 96) for _ in range(4)]
    C2 = {ij: sp.zeros(40, 96) for ij in DIRPAIRS}
    Dphase = sp.zeros(40, 40)
    unit = [I4[:, j] for j in range(4)]

    for phase, a, b, locs, local, Hloc, factors in face_data:
        shifts = [
            (0, 0, 0, 0),
            tuple(1 if r == a else 0 for r in range(4)),
            tuple(1 if r == b else 0 for r in range(4)),
            (0, 0, 0, 0),
        ]
        slot_shifts = []
        for pos in range(4):
            slot_shifts += [shifts[pos]] * 6

        for ii, (_pi, _gi, gi) in enumerate(local):
            for jj, (_pj, _gj, gj) in enumerate(local):
                d = [slot_shifts[jj][r] - slot_shifts[ii][r] for r in range(4)]
                h = Hloc[ii, jj]
                for r in range(4):
                    A1[r][gi, gj] += h * d[r]
                for r, s in DIRPAIRS:
                    coef = sp.Rational(d[r] * d[s], 2) if r == s else d[r] * d[s]
                    A2[(r, s)][gi, gj] += h * coef

        u, v = [j for j in range(4) if j not in (a, b)]
        darea = []
        for qa, qb in SYM:
            dS = B.metric_lift(qa, qb)
            darea.append(B.wedge(dS[:, u], unit[v]) + B.wedge(unit[u], dS[:, v]))

        for pos, (q, role, inverse) in enumerate(locs):
            sh = shifts[pos]
            for g, X in enumerate(GEN):
                dFfactor = -X * factors[pos] if inverse else factors[pos] * X
                dP = I4
                for n, F in enumerate(factors):
                    dP = dP * (dFfactor if n == pos else F)
                dF = (dP - B.linv(dP)) / 2
                dFb = B.biv(dF)
                gi = idx[(q, role, g)]
                for mi, area_i in enumerate(darea):
                    val = sp.cancel(B.orientation(a, b) * (area_i.T * G2 * STAR * dFb)[0])
                    M0[gi, mi] += val
                    C0[10 * phase + mi, gi] += val
                    for r in range(4):
                        M1[r][gi, mi] += sh[r] * val
                        C1[r][10 * phase + mi, gi] += sh[r] * val
                    for r, s in DIRPAIRS:
                        coef = sp.Rational(sh[r] * sh[s], 2) if r == s else sh[r] * sh[s]
                        M2[(r, s)][gi, mi] += coef * val
                        C2[(r, s)][10 * phase + mi, gi] += coef * val

        P = factors[0] * factors[1] * factors[2] * factors[3]
        F = (P - B.linv(P)) / 2
        Fb = B.biv(F)
        dSlist = [B.metric_lift(qa, qb) for qa, qb in SYM]
        for i, X in enumerate(dSlist):
            for j in range(i, 10):
                Y = dSlist[j]
                d2area = B.wedge(X[:, u], Y[:, v]) + B.wedge(Y[:, u], X[:, v])
                val = sp.cancel(B.orientation(a, b) * (d2area.T * G2 * STAR * Fb)[0])
                ri, rj = 10 * phase + i, 10 * phase + j
                Dphase[ri, rj] += val
                if i != j:
                    Dphase[rj, ri] += val
    return A1, A2, M0, M1, M2, C0, C1, C2, Dphase


def riemann_basis():
    coords = [(i, j) for i in range(6) for j in range(i, 6)]

    def R_of(vec, a, b, c, d):
        if a == b or c == d:
            return sp.Integer(0)
        s1, p1 = (1, (a, b)) if a < b else (-1, (b, a))
        s2, p2 = (1, (c, d)) if c < d else (-1, (d, c))
        i, j = PAIRS.index(p1), PAIRS.index(p2)
        if i > j:
            i, j = j, i
        return s1 * s2 * vec[coords.index((i, j))]

    bianchi = []
    for k in range(21):
        e = [sp.Integer(0)] * 21
        e[k] = 1
        bianchi.append(R_of(e, 0, 1, 2, 3) + R_of(e, 0, 2, 3, 1) + R_of(e, 0, 3, 1, 2))
    basis = sp.Matrix([bianchi]).nullspace()
    check("RIEMANN_DIMENSION_20", len(basis) == 20)

    J = {ij: sp.zeros(10, 20) for ij in DIRPAIRS}
    for alpha, vec in enumerate(basis):
        vv = list(vec)
        for mi, (a, b) in enumerate(SYM):
            for c, d in DIRPAIRS:
                J[(c, d)][mi, alpha] = sp.factor(
                    -sp.Rational(1, 3) * (R_of(vv, a, c, b, d) + R_of(vv, a, d, b, c))
                )
    return J, basis, coords


def einstein_k(k):
    eta = [1, -1, -1, -1]
    kup = [eta[i] * k[i] for i in range(4)]
    k2 = sum(k[i] * kup[i] for i in range(4))
    R = sp.zeros(10)
    for col, (a, b) in enumerate(SYM):
        h = sp.zeros(4)
        h[a, b] = h[b, a] = 1
        trace = sum(eta[i] * h[i, i] for i in range(4))
        kkh = sum(kup[i] * kup[j] * h[i, j] for i in range(4) for j in range(4))
        G = sp.zeros(4)
        for mu in range(4):
            for nu in range(4):
                value = sum(
                    k[mu] * kup[r] * h[nu, r] + k[nu] * kup[r] * h[mu, r]
                    for r in range(4)
                )
                value -= k2 * h[mu, nu] + k[mu] * k[nu] * trace
                value -= eta[mu] * int(mu == nu) * (kkh - k2 * trace)
                G[mu, nu] = sp.Rational(value, 2)
        Gup = sp.diag(*eta) * G * sp.diag(*eta)
        for row, (i, j) in enumerate(SYM):
            R[row, col] = Gup[i, j] * (1 if i == j else 2)
    return R


def run(write=False):
    Hflat, labels, flat_faces = B.action_connection_hessian(sp.Integer(0))
    check("FLAT_OWNER_HESSIAN", Hflat == sp.Matrix(json.loads(B.FLAT_OWNER_PATH.read_text())["L2"]) / 2)
    A1f, A2f, B0f, B1f, B2f, D0f = B.lowcolor_coefficients(0, Hflat, flat_faces, labels, 0)
    Nflat = dm_kernel_columns(Hflat)
    check("FLAT_RANK80_KERNEL16", dm_rank(Hflat) == 80 and Nflat.cols == 16)
    check("FLAT_B0_ZERO", B0f == sp.zeros(96, 10))
    check("FLAT_CENTER_COMPATIBILITY", Nflat.T * B1f == sp.zeros(16, 10))
    af1 = B.bordered_solve(Hflat, Nflat, -B1f)
    flat_t2 = (-B1f.T * af1).applyfunc(sp.factor)
    check("FLAT_HALF_EINSTEIN_CONTROL", flat_t2 / 4 == einstein_k([1, 0, 0, 0]) / 2)

    z = sp.Integer(1)
    H, labels, faces0 = B.action_connection_hessian(z)
    faces = with_base_phases(faces0)
    N = centers(H, labels, z)
    check("CURVED_RANK94_CENTER2", dm_rank(H) == 94 and N.rank() == 2)

    # One-axis corrected regression. Raw M1 is the +shift metric-side coefficient.
    A1x, A2x, M0x, M1x, M2x, D0x = B.lowcolor_coefficients(0, H, faces0, labels, 1)
    B0x, B1x, B2x = M0x, -M1x, M2x
    C0x, C1x, C2x = M0x.T, M1x.T, M2x.T
    a0r = B.bordered_solve(H, N, -B0x)
    check("CORRECTED_ORDER1_FREDHOLM", N.T * (A1x * a0r + B1x) == sp.zeros(2, 10))
    a1r = B.bordered_solve(H, N, -(A1x * a0r + B1x))
    y1 = B.bordered_solve(H, N, -A1x * N)
    center2 = (N.T * (A2x * N + A1x * y1)).applyfunc(sp.factor)
    c0 = -center2.inv() * N.T * (A1x * a1r + A2x * a0r + B2x)
    a0 = a0r + N * c0
    a1 = a1r + y1 * c0
    check("CORRECTED_ORDER2_FREDHOLM", N.T * (A1x * a1 + A2x * a0 + B2x) == sp.zeros(2, 10))
    a2r = B.bordered_solve(H, N, -(A1x * a1 + A2x * a0 + B2x))
    S0 = (D0x + C0x * a0).applyfunc(sp.factor)
    S1 = (C0x * a1 + C1x * a0).applyfunc(sp.factor)
    S2 = (C0x * a2r + C1x * a1 + C2x * a0).applyfunc(sp.factor)
    check("CORRECTED_AVERAGED_CONSTANT_LINEAR_ZERO", S0 == sp.zeros(10) and S1 == sp.zeros(10))
    q12 = SYM.index((1, 2))
    q12_per_site = sp.factor(S2[q12, q12] / 4)
    q12_defect = sp.factor(q12_per_site + sp.Rational(1, 2))
    check("CORRECTED_Q12_REGRESSION", q12_per_site == -sp.Rational(186451, 236250))
    check("CORRECTED_Q12_DEFECT_REGRESSION", q12_defect == -sp.Rational(34163, 118125))

    A1, A2, M0, M1, M2, C0, C1, C2, Dphase = blocks_all(H, faces, labels)
    R0 = B.bordered_solve(H, N, -M0)
    J, rbasis, rcoords = riemann_basis()

    P = sp.zeros(40, 10)
    for ph in range(4):
        P[10 * ph:10 * (ph + 1), :] = sp.eye(10)
    Dlow_phase = Dphase * P

    A2map, Jmap = {}, {}
    E2 = sp.zeros(400, 40)
    for pp, ij in enumerate(DIRPAIRS):
        T = sp.zeros(96, 40)
        T[:, :20] = R0 * J[ij]
        T[:, 20 + 2 * pp:20 + 2 * pp + 2] = N
        A2map[ij] = T
        U = sp.zeros(10, 40)
        U[:, :20] = J[ij]
        Jmap[ij] = U
        E2[40 * pp:40 * (pp + 1), :] = Dlow_phase * Jmap[ij] + C0 * A2map[ij]
    E2rank = dm_rank(E2)
    E2ker = dm_kernel_columns(E2)
    check("DEGREE2_PHASE_SYSTEM_RANK10", E2rank == 10 and E2ker.cols == 30)
    check("DEGREE2_CURVATURE_UNRESTRICTED", E2ker[:20, :].rank() == 20)

    # Corrected connection side: metric input at base, connection test at +shift.
    B1 = [-M1[r] for r in range(4)]
    F1, G1 = [], []
    for m in range(4):
        T = sp.zeros(96, 40)
        for i in range(4):
            ij = (i, m) if i <= m else (m, i)
            T += A1[i] * A2map[ij] + B1[i] * Jmap[ij]
        F1.append(T)
        G1.append(N.T * T)
    Pcat = B.bordered_solve(H, N, sp.Matrix.hstack(*[-T for T in F1]))
    P1 = [Pcat[:, 40 * m:40 * (m + 1)] for m in range(4)]

    E2ext = E2.row_join(sp.zeros(E2.rows, 8))
    G1stack = sp.zeros(8, 48)
    Y1stack = sp.zeros(160, 48)
    for m in range(4):
        G1stack[2 * m:2 * m + 2, :40] = G1[m]
        Y = sp.zeros(40, 48)
        for i in range(4):
            ij = (i, m) if i <= m else (m, i)
            Y[:, :40] += C1[i] * A2map[ij]
        Y[:, :40] += C0 * P1[m]
        Y[:, 40 + 2 * m:40 + 2 * m + 2] = C0 * N
        Y1stack[40 * m:40 * (m + 1), :] = Y
    SYS1 = E2ext.col_join(G1stack).col_join(Y1stack)
    SYS1rank = dm_rank(SYS1)
    K1 = dm_kernel_columns(SYS1)
    check("FULL_FIRST_SLOW_SYSTEM_RANK43", SYS1rank == 43 and K1.cols == 5)
    check("CURVATURE_20_TO_1", K1[:20, :].rank() == 1)

    A1map = []
    for m in range(4):
        T = sp.zeros(96, 48)
        T[:, :40] = P1[m]
        T[:, 40 + 2 * m:40 + 2 * m + 2] = N
        A1map.append(T)
    A2map48, Jmap48 = {}, {}
    for ij in DIRPAIRS:
        T = sp.zeros(96, 48)
        T[:, :40] = A2map[ij]
        A2map48[ij] = T
        U = sp.zeros(10, 48)
        U[:, :40] = Jmap[ij]
        Jmap48[ij] = U

    F0 = sp.zeros(96, 48)
    for i in range(4):
        F0 += A1[i] * A1map[i]
    for ij in DIRPAIRS:
        F0 += A2[ij] * A2map48[ij] + M2[ij] * Jmap48[ij]
    G0K = (N.T * F0 * K1).applyfunc(sp.factor)
    check("CONSTANT_CONNECTION_FREDHOLM_AUTOMATIC", G0K == sp.zeros(2, 5))
    P0K = B.bordered_solve(H, N, -F0 * K1)

    Y0K = C0 * P0K
    for i in range(4):
        Y0K += C1[i] * A1map[i] * K1
    for ij in DIRPAIRS:
        Y0K += C2[ij] * A2map48[ij] * K1
    Y0K = Y0K.applyfunc(sp.factor)

    # Non-tautological source condition: erase fast-phase dependence only.
    PhaseDiff = sp.zeros(30, 40)
    for ph in range(1, 4):
        PhaseDiff[10 * (ph - 1):10 * ph, 0:10] = -sp.eye(10)
        PhaseDiff[10 * (ph - 1):10 * ph, 10 * ph:10 * (ph + 1)] = sp.eye(10)
    SMOOTH = sp.zeros(32, 7)
    SMOOTH[:2, :5] = G0K
    SMOOTH[2:, :5] = PhaseDiff * Y0K
    SMOOTH[2:, 5:] = PhaseDiff * C0 * N
    smooth_rank = dm_rank(SMOOTH)
    Ks = dm_kernel_columns(SMOOTH)
    CurvSmooth = K1[:20, :] * Ks[:5, :]
    check("SMOOTH_SOURCE_SYSTEM_RANK5", smooth_rank == 5 and Ks.cols == 2)
    check("SMOOTH_SOURCE_CURVATURE_RANK1", CurvSmooth.rank() == 1)

    # Compare the emergent common response with Einstein only after phase erasure.
    zero = [sp.Integer(0)] * 4
    Ecoef = {}
    for i, j in DIRPAIRS:
        if i == j:
            k = zero.copy()
            k[i] = 1
            Ecoef[(i, j)] = einstein_k(k) / 2
        else:
            k = zero.copy()
            k[i] = k[j] = 1
            ki, kj = zero.copy(), zero.copy()
            ki[i], kj[j] = 1, 1
            Ecoef[(i, j)] = (einstein_k(k) - einstein_k(ki) - einstein_k(kj)) / 2
    E10map = sp.zeros(10, 48)
    for ij in DIRPAIRS:
        E10map += Ecoef[ij] * Jmap48[ij]

    emergent = (Y0K * Ks[:5, :] + C0 * N * Ks[5:, :])[:10, :]
    expected = E10map * K1 * Ks[:5, :]
    diff = (emergent - expected).applyfunc(sp.factor)
    check("SMOOTH_SOURCE_EMERGENT_RESPONSE_IS_EINSTEIN", diff == sp.zeros(10, Ks.cols))

    phys_col = next(j for j in range(Ks.cols) if CurvSmooth[:, j] != sp.zeros(20, 1))
    rv = CurvSmooth[:, phys_col]
    v21 = sum((rbasis[i] * rv[i] for i in range(20)), sp.zeros(21, 1))
    lookup = {c: n for n, c in enumerate(rcoords)}
    spatial = sp.zeros(3)
    for i in range(3, 6):
        for j in range(3, 6):
            ii, jj = (i, j) if i <= j else (j, i)
            spatial[i - 3, j - 3] = v21[lookup[(ii, jj)]]
    scale = -1 / spatial[0, 0]
    spatial_norm = (scale * spatial).applyfunc(sp.factor)
    YYminus = sp.Matrix([[-1, 1, -1], [1, -1, 1], [-1, 1, -1]])
    check("SURVIVING_CURVATURE_IS_MINUS_Y_TENSOR_Y", spatial_norm == YYminus)

    rvn = scale * rv
    Jnorm = {ij: (J[ij] * rvn).applyfunc(sp.factor) for ij in DIRPAIRS}
    resp_norm = (scale * emergent[:, phys_col]).applyfunc(sp.factor)
    expected_resp_norm = (scale * expected[:, phys_col]).applyfunc(sp.factor)
    check("NORMALIZED_RESPONSE_MATCH", resp_norm == expected_resp_norm)

    result = {
        "schema": "a4d-y-curved-normaljet-compatibility-v1",
        "terminal": "A4D-Y-CURVED-NORMAL-JET-RESPONSE-COMPATIBLE",
        "scope": "exact finite linear normal-jet compatibility at z=1; nonlinear continuation and h-uniform remainder remain open",
        "mixed_phase_convention": {
            "D_Q_E_K": "lambda^(-s)",
            "D_K_E_Q": "lambda^(+s)",
            "reason": "metric input/test is at face base while connection test/input is at shifted factor",
        },
        "flat_control": {"rank": 80, "kernel_dimension": 16, "per_site_symbol": "1/2 * repository Einstein t-symbol"},
        "curved_connection": {
            "z": "1", "rank": 94, "center_dimension": 2,
            "reduced_center_t2": matrix_json(center2),
        },
        "corrected_one_axis_regression": {
            "metric_coordinate": "q12", "axis": "e0",
            "per_site_t2": str(q12_per_site),
            "difference_from_flat_minus_one_half": str(q12_defect),
        },
        "normal_jet": {
            "riemann_dimension": 20,
            "degree2_phase_system_rank": E2rank,
            "degree2_kernel_dimension": E2ker.cols,
            "degree2_curvature_projection_rank": E2ker[:20, :].rank(),
            "first_slow_system_rank": SYS1rank,
            "first_slow_kernel_dimension": K1.cols,
            "first_slow_curvature_projection_rank": K1[:20, :].rank(),
            "constant_connection_fredholm_rank_on_kernel": dm_rank(G0K),
            "smooth_source_system_rank": smooth_rank,
            "smooth_source_kernel_dimension": Ks.cols,
            "smooth_source_curvature_projection_rank": CurvSmooth.rank(),
            "emergent_minus_einstein_rank": dm_rank(diff),
        },
        "normalized_surviving_curvature": {
            "spatial_bivector_basis": ["12", "13", "23"],
            "minus_R_operator_normalized_as_YY": matrix_json(spatial_norm),
            "normal_metric_hessian_nonzero": {
                f"d{c}d{d}": [str(x) for x in Jnorm[(c, d)]]
                for c, d in DIRPAIRS if Jnorm[(c, d)] != sp.zeros(10, 1)
            },
            "metric_coordinate_order": [f"q{a}{b}" for a, b in SYM],
            "emergent_common_response": [str(x) for x in resp_norm],
            "flat_einstein_control": [str(x) for x in expected_resp_norm],
        },
        "nonclaims": [
            "no nonlinear curved-background exact branch is proved here",
            "no refinement-uniform o(h^2) response remainder is proved here",
            "no global selector/no-go conclusion is made",
        ],
    }

    if write:
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", RESULT_PATH)
    else:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(RESULT_PATH.read_text()))

    print("CORRECTED_Q12_PER_SITE", q12_per_site)
    print("FIRST_SLOW_CURVATURE_RANK", K1[:20, :].rank())
    print("SMOOTH_SOURCE_CURVATURE_RANK", CurvSmooth.rank())
    print("EMERGENT_MINUS_EINSTEIN_RANK", dm_rank(diff))
    print("TERMINAL", result["terminal"])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    run(write=args.write)
