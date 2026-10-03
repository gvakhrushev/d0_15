#!/usr/bin/env python3
"""Exact Bloch-Lyapunov-Schmidt response at the curved #232 Y vacuum.

At z=1 this computes the low-color metric Hessian after eliminating the full
96-variable connection cell for a Bloch wave along role 0.  The singular
zero-momentum connection Hessian is split into its exact center and range;
the two-dimensional center is solved at quadratic order.  A flat z=0 control
reproduces the owned -1/2 Einstein symbol, while the curved TT coefficient
does not.

All arithmetic is rational.  This is a finite-cell Hessian response result,
not a nonlinear continuation or a global homogenization theorem.
"""
from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix


ROOT = Path(__file__).resolve().parents[3]
RESULT_PATH = ROOT / "02_REGISTRY/research/certificates/a4d_y_curved_response_quotient_results.json"
FLAT_OWNER_PATH = ROOT / "02_REGISTRY/research/certificates/a4d_y_slow_joint_cross_matrices.json"
PRIME = 1_000_003
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
PAIRS = list(combinations(range(4), 2))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
GEN = []
for j in (1, 2, 3):
    X = sp.zeros(4)
    X[0, j] = X[j, 0] = 1
    GEN.append(X)
for a, b in ((1, 2), (1, 3), (2, 3)):
    X = sp.zeros(4)
    X[a, b], X[b, a] = 1, -1
    GEN.append(X)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for col, (row, sign) in enumerate(((5, -1), (4, 1), (3, -1), (2, 1), (1, -1), (0, 1))):
    STAR[row, col] = sign


def check(name: str, condition: bool, detail: str = "") -> None:
    if not condition:
        raise AssertionError(name + (": " + detail if detail else ""))
    print("PASS_" + name)


def linv(M: sp.Matrix) -> sp.Matrix:
    return ETA * M.T * ETA


def wedge(u: sp.Matrix, v: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def biv(M: sp.Matrix) -> sp.Matrix:
    X = M * ETA
    return sp.Matrix([X[a, b] for a, b in PAIRS])


def orientation(a: int, b: int) -> int:
    seq = [a, b] + [j for j in range(4) if j not in (a, b)]
    inversions = sum(seq[i] > seq[j] for i in range(4) for j in range(i + 1, 4))
    return -1 if inversions % 2 else 1


def symxy(X: sp.Matrix, Y: sp.Matrix) -> sp.Matrix:
    return (X * Y + Y * X) / 2


def cayley_Y(z: sp.Expr) -> sp.Matrix:
    Y = GEN[3] - GEN[4] + GEN[5]
    return sp.cancel((I4 - z * Y / 2).inv() * (I4 + z * Y / 2))


def action_connection_hessian(z: sp.Expr):
    """Return the exact 96x96 connection Hessian and per-face local jets."""
    U = cayley_Y(z)
    W = [U, I4, linv(U), I4]
    labels = [(p, r, g) for p in range(4) for r in range(4) for g in range(6)]
    label_index = {label: i for i, label in enumerate(labels)}
    basis = [I4[:, j] for j in range(4)]
    H = sp.zeros(96)
    face_data = []

    for phase in range(4):
        for a, b in PAIRS:
            # The four oriented plaquette factors and their cell offsets.
            locs = [
                (phase, a, False),
                ((phase + 1) % 4, b, False),
                ((phase + 1) % 4, a, True),
                (phase, b, True),
            ]
            factors = []
            first = []
            for q, role, inverse in locs:
                K = W[q] if role == 0 else I4
                F = linv(K) if inverse else K
                factors.append(F)
                first.append([(-X * F if inverse else F * X) for X in GEN])

            local = []
            for pos, (q, role, _inverse) in enumerate(locs):
                for g in range(6):
                    local.append((pos, g, label_index[(q, role, g)]))

            u, v = [j for j in range(4) if j not in (a, b)]
            area = wedge(basis[u], basis[v])
            Hloc = sp.zeros(24)
            for i, (pi, gi, _global_i) in enumerate(local):
                for j in range(i, 24):
                    pj, gj, _global_j = local[j]
                    if pi == pj:
                        Q = symxy(GEN[gi], GEN[gj])
                        Q = Q * factors[pi] if locs[pi][2] else factors[pi] * Q
                        d2P = I4
                        for n, F in enumerate(factors):
                            d2P = d2P * (Q if n == pi else F)
                    else:
                        d2P = I4
                        for n, F in enumerate(factors):
                            if n == pi:
                                item = first[n][gi]
                            elif n == pj:
                                item = first[n][gj]
                            else:
                                item = F
                            d2P = d2P * item
                    d2F = (d2P - linv(d2P)) / 2
                    value = sp.cancel(orientation(a, b) * (area.T * G2 * STAR * biv(d2F))[0])
                    Hloc[i, j] = value
                    Hloc[j, i] = value

            for i, (_pi, _gi, global_i) in enumerate(local):
                for j, (_pj, _gj, global_j) in enumerate(local):
                    H[global_i, global_j] += Hloc[i, j]
            face_data.append((a, b, locs, local, Hloc, factors))

    return H.applyfunc(sp.cancel), labels, face_data


def clear_denominator_rank_and_kernel(M: sp.Matrix, prime: int):
    den = sp.ilcm(*[x.q for x in M if x != 0])
    check("MODULUS_DOES_NOT_DIVIDE_CLEARING_DENOMINATOR", den % prime != 0, str(den))
    A = [[int(x * den) % prime for x in row] for row in M.tolist()]
    rows, cols = M.shape
    pivots = []
    row = 0
    for col in range(cols):
        pivot = next((i for i in range(row, rows) if A[i][col]), None)
        if pivot is None:
            continue
        A[row], A[pivot] = A[pivot], A[row]
        inv = pow(A[row][col], prime - 2, prime)
        A[row] = [(x * inv) % prime for x in A[row]]
        for i in range(rows):
            if i != row and A[i][col]:
                q = A[i][col]
                A[i] = [(x - q * y) % prime for x, y in zip(A[i], A[row])]
        pivots.append(col)
        row += 1
        if row == rows:
            break
    free = [j for j in range(cols) if j not in pivots]
    null = []
    for f in free:
        v = [0] * cols
        v[f] = 1
        for r, c in enumerate(pivots):
            v[c] = (-A[r][f]) % prime
        null.append([x if x <= prime // 2 else x - prime for x in v])
    return den, row, null


def bordered_solve(H: sp.Matrix, N: sp.Matrix, rhs: sp.Matrix) -> sp.Matrix:
    n, c = N.shape
    bordered = H.row_join(N).col_join(N.T.row_join(sp.zeros(c)))
    full_rhs = rhs.col_join(sp.zeros(c, rhs.cols))
    solved = DomainMatrix.from_Matrix(bordered).convert_to(QQ).lu_solve(
        DomainMatrix.from_Matrix(full_rhs).convert_to(QQ)
    ).to_Matrix()
    return solved[:n, :]


def metric_lift(a: int, b: int) -> sp.Matrix:
    q = sp.zeros(4)
    q[a, b] = q[b, a] = 1
    return ETA * q / 2


def lowcolor_coefficients(axis: int, H: sp.Matrix, face_data, labels, z: int):
    """Build A_1,A_2, B_0,B_1,B_2 and D_0 for lambda=exp(t)."""
    index = {label: i for i, label in enumerate(labels)}
    A1, A2 = sp.zeros(96), sp.zeros(96)
    B0, B1, B2 = sp.zeros(96, 10), sp.zeros(96, 10), sp.zeros(96, 10)
    D0 = sp.zeros(10)
    U = cayley_Y(sp.Integer(z))
    W = [U, I4, linv(U), I4]
    unit = [I4[:, j] for j in range(4)]

    for a, b, locs, local, Hloc, factors in face_data:
        offsets = []
        for pos in range(4):
            shift = (axis == a) if pos == 1 else ((axis == b) if pos == 2 else False)
            offsets.extend([int(shift)] * 6)
        for i, (_pi, _gi, gi) in enumerate(local):
            for j, (_pj, _gj, gj) in enumerate(local):
                delta = offsets[j] - offsets[i]
                A1[gi, gj] += Hloc[i, j] * delta
                A2[gi, gj] += Hloc[i, j] * sp.Rational(delta * delta, 2)

        u, v = [j for j in range(4) if j not in (a, b)]
        darea = []
        for qa, qb in SYM:
            dS = metric_lift(qa, qb)
            darea.append(wedge(dS[:, u], unit[v]) + wedge(unit[u], dS[:, v]))

        for pos, (q, role, inverse) in enumerate(locs):
            for g, X in enumerate(GEN):
                dFfactor = -X * factors[pos] if inverse else factors[pos] * X
                dP = I4
                for n, F in enumerate(factors):
                    dP = dP * (dFfactor if n == pos else F)
                dF = (dP - linv(dP)) / 2
                dFb = biv(dF)
                global_i = index[(q, role, g)]
                offset = offsets[6 * pos]
                for metric_i, area_i in enumerate(darea):
                    value = sp.cancel(orientation(a, b) * (area_i.T * G2 * STAR * dFb)[0])
                    B0[global_i, metric_i] += value
                    B1[global_i, metric_i] += offset * value
                    B2[global_i, metric_i] += sp.Rational(offset * offset, 2) * value

        P = factors[0] * factors[1] * factors[2] * factors[3]
        F = (P - linv(P)) / 2
        Fb = biv(F)
        dSlist = [metric_lift(qa, qb) for qa, qb in SYM]
        for i, X in enumerate(dSlist):
            for j in range(i, 10):
                Y = dSlist[j]
                d2area = wedge(X[:, u], Y[:, v]) + wedge(Y[:, u], X[:, v])
                value = sp.cancel(orientation(a, b) * (d2area.T * G2 * STAR * Fb)[0])
                D0[i, j] += value
                if i != j:
                    D0[j, i] += value

    return tuple(M.applyfunc(sp.cancel) for M in (A1, A2, B0, B1, B2, D0))


def einstein_symbol(axis: int) -> sp.Matrix:
    """Direct standard G^(1) symbol in the repository's ten q coordinates."""
    eta = [1, -1, -1, -1]
    k = [0, 0, 0, 0]
    k[axis] = 1
    kup = [eta[i] * k[i] for i in range(4)]
    k2 = sum(k[i] * kup[i] for i in range(4))
    result = sp.zeros(10)
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
            result[row, col] = Gup[i, j] * (1 if i == j else 2)
    return result


def matrix_json(M: sp.Matrix):
    return [[str(sp.factor(M[i, j])) for j in range(M.cols)] for i in range(M.rows)]


def direct_schur_at_lambda(lam: sp.Rational, H: sp.Matrix, B0: sp.Matrix,
                           B1: sp.Matrix, D0: sp.Matrix, face_data, labels,
                           wrong_metric_phase: bool = False) -> sp.Matrix:
    """Independent exact evaluation at a nonzero Bloch detuning."""
    A = sp.zeros(96)
    for _a, _b, _locs, local, Hloc, _factors in face_data:
        a, b, locs = _a, _b, _locs
        offsets = []
        for pos in range(4):
            shift = (0 == a) if pos == 1 else ((0 == b) if pos == 2 else False)
            offsets.extend([int(shift)] * 6)
        for i, (_pi, _gi, gi) in enumerate(local):
            for j, (_pj, _gj, gj) in enumerate(local):
                A[gi, gj] += Hloc[i, j] * lam ** (offsets[j] - offsets[i])
    Bplus = B0 + (lam - 1) * B1
    Bminus = B0 + (1 / lam - 1) * B1
    connection = DomainMatrix.from_Matrix(A).convert_to(QQ).lu_solve(
        DomainMatrix.from_Matrix(-Bplus).convert_to(QQ)
    ).to_Matrix()
    # Hostile control deliberately uses the connection-side Bloch phase in
    # the metric transpose. The Euler pairing requires the inverse phase.
    metric_side = Bplus if wrong_metric_phase else Bminus
    return (D0 + metric_side.T * connection).applyfunc(sp.cancel)


def run(write: bool = False):
    # Flat control: the independently reconstructed connection Hessian must
    # equal the frozen #275 owner matrix L2/2 entry by entry.
    Hflat, labels, flat_faces = action_connection_hessian(sp.Integer(0))
    owner = json.loads(FLAT_OWNER_PATH.read_text())
    L2 = sp.Matrix(owner["L2"])
    check("FLAT_HESSIAN_MATCHES_OWNED_L0", Hflat == L2 / 2)
    den0, rank0, flat_null_mod = clear_denominator_rank_and_kernel(Hflat, PRIME)
    Nflat = sp.Matrix([
        [flat_null_mod[j][i] for j in range(len(flat_null_mod))]
        for i in range(96)
    ])
    check("FLAT_EXACT_RANK80", rank0 == 80 and len(flat_null_mod) == 16)
    check("FLAT_EXACT_KERNEL_BASIS16", Hflat * Nflat == sp.zeros(96, 16) and Nflat.rank() == 16)

    A1f, A2f, B0f, B1f, B2f, D0f = lowcolor_coefficients(0, Hflat, flat_faces, labels, 0)
    check("FLAT_LOW_COLOR_B0_ZERO", B0f == sp.zeros(96, 10))
    check("FLAT_CENTER_COMPATIBILITY", Nflat.T * B1f == sp.zeros(16, 10))
    af1 = bordered_solve(Hflat, Nflat, -B1f)
    flat_t2 = (-B1f.T * af1).applyfunc(sp.factor)
    KG = einstein_symbol(0)
    check("FLAT_LOW_COLOR_CONTROL_IS_HALF_EINSTEIN", flat_t2 / 4 == KG / 2)

    # Curved exact #232 branch, z=1. The range Hessian is singular at zero
    # momentum, but the two exact center vectors exhaust its nullspace.
    z = 1
    H, labels, faces = action_connection_hessian(sp.Integer(z))
    check("CURVED_HESSIAN_SYMMETRIC", H == H.T)
    Y = GEN[3] - GEN[4] + GEN[5]
    tangent_scale = sp.Rational(4, 4 + 3 * z * z)
    index = {label: i for i, label in enumerate(labels)}
    ny = sp.zeros(96, 1)
    nd = sp.zeros(96, 1)
    for phase, sign in ((0, 1), (2, -1)):
        for g, coeff in ((3, 1), (4, -1), (5, 1)):
            ny[index[(phase, 0, g)], 0] = sign * tangent_scale * coeff
    for phase, sign in ((0, -1), (2, 1)):
        for g in (0, 1, 2):
            nd[index[(phase, 0, g)], 0] = sign
    N = sp.Matrix.hstack(ny, nd)
    check("CURVED_Y_AND_DUAL_ARE_EXACT_CENTERS", H * N == sp.zeros(96, 2))
    check("CURVED_CENTER_BASIS_INDEPENDENT", N.rank() == 2 and N.T * H == sp.zeros(2, 96))
    den1, rank1, _null1 = clear_denominator_rank_and_kernel(H, PRIME)
    check("CURVED_EXACT_CENTER_DIMENSION2", rank1 == 94)

    A1, A2, B0, B1, B2, D0 = lowcolor_coefficients(0, H, faces, labels, z)
    check("CURVED_LOW_COLOR_CENTER_COMPATIBILITY", N.T * B0 == sp.zeros(2, 10)
          and N.T * B1 == sp.zeros(2, 10))
    y1 = bordered_solve(H, N, -A1 * N)
    center_t2 = (N.T * (A2 * N + A1 * y1)).applyfunc(sp.factor)
    check("CURVED_REDUCED_CENTER_NONDEGENERATE", center_t2.det() != 0)
    a0_range = bordered_solve(H, N, -B0)
    compatibility1 = N.T * (A1 * a0_range + B1)
    check("CURVED_ORDER1_FREDHOLM_COMPATIBILITY", compatibility1 == sp.zeros(2, 10))
    a1_range = bordered_solve(H, N, -(A1 * a0_range + B1))
    center_coeff = -center_t2.inv() * N.T * (A1 * a1_range + A2 * a0_range + B2)
    a0 = a0_range + N * center_coeff
    a1 = a1_range + y1 * center_coeff
    check("CURVED_RANGE_AND_CENTER_SOLVES_EXACT",
          H * a0_range + B0 == sp.zeros(96, 10)
          and N.T * a0_range == sp.zeros(2, 10)
          and H * a1_range + A1 * a0_range + B1 == sp.zeros(96, 10)
          and N.T * a1_range == sp.zeros(2, 10)
          and center_t2 * center_coeff
              + N.T * (A1 * a1_range + A2 * a0_range + B2) == sp.zeros(2, 10))
    response0 = D0 + B0.T * a0_range
    response1 = B0.T * a1 - B1.T * a0
    check("CURVED_RESPONSE_CONSTANT_AND_LINEAR_TERMS_VANISH",
          response0 == sp.zeros(10) and response1 == sp.zeros(10))

    curved_t2 = sp.zeros(10)
    for i in range(10):
        for j in range(10):
            ai, aj = a0[:, i], a0[:, j]
            bi, bj = a1[:, i], a1[:, j]
            curved_t2[i, j] = sp.factor((
                (ai.T * A1 * bj + aj.T * A1 * bi) / 2
                + ai.T * A2 * aj
                + ai.T * B2[:, j]
                + aj.T * B2[:, i]
                - (B1[:, i].T * bj + B1[:, j].T * bi) / 2
            )[0])
    check("CURVED_RESPONSE_T2_SYMMETRIC", curved_t2 == curved_t2.T)

    # The TT coordinate q_12 is transverse and traceless for k=e_0, so this
    # mismatch survives the linearized diffeomorphism quotient.
    tt_index = SYM.index((1, 2))
    tt_curved_t2 = sp.factor(curved_t2[tt_index, tt_index] / 4)
    tt_flat_t2 = sp.factor(KG[tt_index, tt_index] / 2)
    tt_defect_t2 = sp.factor(tt_curved_t2 - tt_flat_t2)
    tt_indices = [SYM.index((1, 2)), SYM.index((1, 3))]
    tt_curved_block = (curved_t2.extract(tt_indices, tt_indices) / 4).applyfunc(sp.factor)
    tt_flat_block = (KG.extract(tt_indices, tt_indices) / 2).applyfunc(sp.factor)
    tt_defect_block = (tt_curved_block - tt_flat_block).applyfunc(sp.factor)
    check("TT_MODES_ARE_TRANSVERSE_TRACELESS",
          all(a != 0 and b != 0 for a, b in ((1, 2), (1, 3)))
          and all((a, b) in SYM for a, b in ((1, 2), (1, 3))))
    check("CURVED_TT_RESPONSE_DIFFERS_FROM_EINSTEIN",
          tt_defect_t2 != 0 and tt_defect_block.det() != 0)

    # Direct exact Schur evaluations at two nearby rational Bloch multipliers
    # independently confirm the computed quadratic coefficient.
    direct_differences = []
    for x in (sp.Rational(1, 20), sp.Rational(1, 100)):
        direct = direct_schur_at_lambda(1 + x, H, B0, B1, D0, faces, labels)
        ratio = sp.factor(direct[tt_index, tt_index] / (x * x))
        direct_differences.append(abs(ratio - curved_t2[tt_index, tt_index]))
    check("DIRECT_LAMBDA_SCHUR_CONVERGES_TO_T2", direct_differences[1] < direct_differences[0])
    hostile_lam = sp.Rational(21, 20)
    hostile = direct_schur_at_lambda(hostile_lam, H, B0, B1, D0, faces, labels,
                                     wrong_metric_phase=True)
    correct = direct_schur_at_lambda(hostile_lam, H, B0, B1, D0, faces, labels)
    check("HOSTILE_WRONG_METRIC_PHASE_TRANSPOSE_FAILS",
          hostile[tt_index, tt_index] != correct[tt_index, tt_index])

    result = {
        "schema": "a4d-y-curved-response-quotient-v1",
        "terminal": "A4D-Y-CURVED-RESPONSE-QUOTIENT-OBSTRUCTED-AT-Z1-TT",
        "source": "#232 exact period-4 Y joint vacuum; z=1; standard solder",
        "bloch": {"direction": "e0", "parameter": "lambda=exp(t), t=i*k0", "low_color": "same q on all four phases"},
        "connection_hessian": {
            "flat_rank": rank0, "flat_kernel_dimension": 96 - rank0,
            "curved_rank_at_z1": rank1, "curved_kernel_dimension_at_z1": 96 - rank1,
            "curved_center_basis": ["right-log Y tangent", "phase-0/2 boost dual"],
            "curved_right_kernel_columns": matrix_json(N),
            "curved_left_cokernel_rows": matrix_json(N.T),
            "clearing_denominators": {"flat": str(den0), "curved_z1": str(den1), "modulus": PRIME},
        },
        "range_solution_witness_q12": {
            "metric_coordinate": "q12",
            "connection_t0": [str(x) for x in a0[:, tt_index]],
            "connection_t1": [str(x) for x in a1[:, tt_index]],
            "center_amplitudes": [str(x) for x in center_coeff[:, tt_index]],
            "exact_range_and_center_equations": True,
        },
        "center_reduced_t2": matrix_json(center_t2),
        "metric_coordinate_order": [f"q{a}{b}" for a, b in SYM],
        "flat_t2_symbol_per_site": matrix_json(flat_t2 / 4),
        "einstein_half_G_t2": matrix_json(KG / 2),
        "curved_t2_symbol_total_cell": matrix_json(curved_t2),
        "curved_t2_symbol_per_site": matrix_json(curved_t2 / 4),
        "tt_witness": {
            "metric_coordinate": "q12", "momentum": "e0", "physical_sector": "transverse-traceless",
            "curved_t2_per_site": str(tt_curved_t2),
            "flat_einstein_t2_per_site": str(tt_flat_t2),
            "t2_defect": str(tt_defect_t2),
            "physical_k2_defect": str(-tt_defect_t2),
            "tt_mode_coordinates": ["q12", "q13"],
            "curved_tt_block_per_site": matrix_json(tt_curved_block),
            "flat_einstein_tt_block_per_site": matrix_json(tt_flat_block),
            "tt_defect_block_per_site": matrix_json(tt_defect_block),
            "tt_defect_block_determinant": str(sp.factor(tt_defect_block.det())),
        },
        "direct_lambda_checks": {
            "x_values": ["1/20", "1/100"],
            "absolute_tt_ratio_errors": [str(x) for x in direct_differences],
        },
        "hostile_wrong_metric_phase_control": {
            "lambda": str(hostile_lam),
            "correct_tt_response": str(correct[tt_index, tt_index]),
            "wrong_phase_transpose_tt_response": str(hostile[tt_index, tt_index]),
        },
        "scope": "finite exact Hessian/Schur response at one curved vacuum; not nonlinear continuation or global #240 homogenization",
    }

    if write:
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", RESULT_PATH)
    else:
        expected = json.loads(RESULT_PATH.read_text())
        check("RESULTS_MATCH_PINNED_JSON", result == expected)
    print("FLAT_TT_T2", tt_flat_t2)
    print("CURVED_TT_T2_PER_SITE", tt_curved_t2)
    print("TT_DEFECT_T2", tt_defect_t2)
    print("TERMINAL", result["terminal"])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true", help="explicitly regenerate the frozen JSON result")
    args = parser.parse_args()
    run(write=args.write)
