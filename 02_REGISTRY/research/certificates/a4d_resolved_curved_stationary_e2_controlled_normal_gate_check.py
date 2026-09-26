#!/usr/bin/env python3
"""Exact first-order gates for controlled deformations of the E(2) witness.

At (j,gamma,delta)=(2,0,1), compute the Jacobian of the eight missing
{N2,N3}-Euler components under each role-local {K1,N2,N3} generator
deformation.  Independently differentiate adj(I-P) on the four curved faces
using exact cofactors.  This is a rank gate and linearized correction only;
it does not certify a finite stationary point.
"""
from __future__ import annotations

import time
from itertools import combinations

import sympy as sp
from sympy import Matrix, Rational, eye, zeros

T0 = time.time()
WALL_SEC = 240


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


def abort_if(name: str) -> None:
    if time.time() - T0 > WALL_SEC:
        raise SystemExit(f"ABORT_WALL: {name}")


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
for p, (q, sign) in STAR_MAP.items():
    STAR[PINDEX[q], PINDEX[p]] = sign


def gen_boost(i: int) -> Matrix:
    A = zeros(4)
    A[0, i] = A[i, 0] = 1
    return A


def gen_rot(i: int, j: int) -> Matrix:
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
INTERNAL = (M2, M3, -J23)
COMPLEMENT = (K1, N2, N3)


def e2_alg(n2, n3, j):
    return n2 * M2 + n3 * M3 - j * J23


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


def cayley(A: Matrix) -> Matrix:
    return (I4 + A / 2) * (I4 - A / 2).inv()


def cayley_diff(A: Matrix, H: Matrix) -> Matrix:
    B_inv = (I4 - A / 2).inv()
    U = (I4 + A / 2) * B_inv
    return H / 2 * B_inv + U * H / 2 * B_inv


def orientation(face) -> int:
    comp = [i for i in range(4) if i not in face]
    seq = list(face) + comp
    inversions = sum(
        seq[i] > seq[j]
        for i in range(4)
        for j in range(i + 1, 4)
    )
    return -1 if inversions % 2 else 1


def wedge(u: Matrix, v: Matrix) -> Matrix:
    return Matrix([u[a] * v[b] - u[b] * v[a] for a, b in PAIRS])


def bivector_of_tangent(X: Matrix) -> Matrix:
    Y = X * ETA
    return Matrix([Y[a, b] for a, b in PAIRS])


def d_curvature(P: Matrix, dP: Matrix) -> Matrix:
    P_inv = P.inv()
    return (dP + P_inv * dP * P_inv) / 2


def d_star(role, As, role_index: int, H: Matrix):
    dU = cayley_diff(As[role_index], H)
    coframe = [ETA[:, r] for r in range(4)]
    site = 0
    for r, s in PAIRS:
        Ur, Us = role[r], role[s]
        Uri, Usi = Ur.inv(), Us.inv()
        dUr = dU if r == role_index else zeros(4)
        dUs = dU if s == role_index else zeros(4)
        dUri = -Uri * dUr * Uri if r == role_index else zeros(4)
        dUsi = -Usi * dUs * Usi if s == role_index else zeros(4)
        P = Ur * Us * Uri * Usi
        dP = (
            dUr * Us * Uri * Usi
            + Ur * dUs * Uri * Usi
            + Ur * Us * dUri * Usi
            + Ur * Us * Uri * dUsi
        )
        dC = bivector_of_tangent(d_curvature(P, dP))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * (
            wedge(coframe[u], coframe[v]).T * G2 * STAR * dC
        )[0]
    return 16 * site


def det_direction(M: Matrix, dM: Matrix):
    return sp.factor(sum(
        M.cofactor(i, j) * dM[i, j]
        for i in range(M.rows)
        for j in range(M.cols)
    ))


def adj_direction(M: Matrix, dM: Matrix) -> Matrix:
    """Directional derivative of adj(M), by its exact 3x3 cofactors."""
    out = zeros(M.rows)
    for i in range(M.rows):
        for j in range(M.cols):
            # adj(M)[i,j] is the signed minor deleting row j, column i.
            minor = M.minor_submatrix(j, i)
            dminor = dM.minor_submatrix(j, i)
            out[i, j] = (-1) ** (i + j) * sum(
                minor.cofactor(a, b) * dminor[a, b]
                for a in range(minor.rows)
                for b in range(minor.cols)
            )
    return out


# This is the actual matrix-defined E(2) witness: links 0,1 use -j J23;
# links 2,3 use M3,M2.  All arithmetic remains rational.
As0 = [
    e2_alg(Rational(0), Rational(0), Rational(2)),
    e2_alg(Rational(0), Rational(0), Rational(2)),
    e2_alg(Rational(0), Rational(1), Rational(0)),
    e2_alg(Rational(1), Rational(0), Rational(0)),
]
role0 = [
    e2_closed(Rational(0), Rational(0), Rational(2)),
    e2_closed(Rational(0), Rational(0), Rational(2)),
    e2_closed(Rational(0), Rational(1), Rational(0)),
    e2_closed(Rational(1), Rational(0), Rational(0)),
]
for r in range(4):
    check(f"ROLE_{r}_STORED_MATRIX_MATCHES_CAYLEY_BASE", cayley(As0[r]) == role0[r])
faces = ((0, 2), (0, 3), (1, 2), (1, 3))
for face in faces:
    a, b = face
    M = I4 - role0[a] * role0[b] * role0[a].inv() * role0[b].inv()
    check(f"BASE_FACE_{a}_{b}_RANK_2", M.rank() == 2)

EL_BASE = Matrix([
    sp.factor(d_star(role0, As0, r, H))
    for r in range(4)
    for H in (N2, N3)
])
print("BASE_MISSING_EL_N2_N3", [str(x) for x in EL_BASE])
check("BASE_MISSING_EL_REPRODUCES_CORRECTED_WITNESS", list(EL_BASE) == [
    Rational(-16), 0, 16, 0, -32, 64, 0, -32
])

# Exact Euler Jacobian: one generator deformation in one role at a time.
candidate_names = []
euler_columns = []
residual_active = []
specs = (("K1", K1), ("N2", N2), ("N3", N3))
for label, H_def in specs:
    for q in range(4):
        abort_if(f"before Euler direction {label}{q}")
        lam = sp.Symbol(f"lambda_{label}_{q}")
        As = [
            A + (lam * H_def if r == q else zeros(4))
            for r, A in enumerate(As0)
        ]
        role = [cayley(A) for A in As]
        column = []
        for r in range(4):
            for H_test in (N2, N3):
                value = d_star(role, As, r, H_test)
                derivative = sp.diff(value, lam).subs(lam, 0)
                column.append(sp.factor(sp.cancel(sp.together(derivative))))
        name = f"{label}{q}"
        candidate_names.append(name)
        euler_columns.append(column)
        print("EULER_JAC_COLUMN", name, [str(x) for x in column])

        # Independently differentiate adj(I-P) and det(I-P) on each curved face.
        dU = cayley_diff(As0[q], H_def)
        face_data = []
        for a, b in faces:
            U, V = role0[a], role0[b]
            U_inv, V_inv = U.inv(), V.inv()
            P = U * V * U_inv * V_inv
            dU_a = dU if a == q else zeros(4)
            dU_b = dU if b == q else zeros(4)
            dU_inv = -U_inv * dU_a * U_inv if a == q else zeros(4)
            dV_inv = -V_inv * dU_b * V_inv if b == q else zeros(4)
            dP = (
                dU_a * V * U_inv * V_inv
                + U * dU_b * U_inv * V_inv
                + U * V * dU_inv * V_inv
                + U * V * U_inv * dV_inv
            )
            M, dM = I4 - P, -dP
            ddet = det_direction(M, dM)
            dadj = adj_direction(M, dM)
            face_data.append((a, b, ddet, dadj.rank(), sum(x != 0 for x in dadj)))
        active = any(nonzero for _, _, _, _, nonzero in face_data)
        if active:
            residual_active.append(len(candidate_names) - 1)
        print("RESIDUAL_DIRECTION", name, [
            (a, b, str(ddet), rank, nonzero)
            for a, b, ddet, rank, nonzero in face_data
        ])

EL_JAC = Matrix(8, len(euler_columns), lambda i, j: euler_columns[j][i])
check("K1_SIM_DILATIONS_DO_NOT_ACTIVATE_ADJUGATE", all(
    i not in residual_active for i in range(4)
))
check("ONLY_ROLE2_N2_AND_ROLE3_N3_ACTIVATE_ADJUGATE", [
    candidate_names[i] for i in residual_active
] == ["N22", "N33"])
check("K1_SIM_DILATIONS_CANNOT_REPAIR_FULL_MISSING_EL_AT_FIRST_ORDER", Matrix.hstack(
    *[EL_JAC[:, i] for i in range(4)]
).rank() < Matrix.hstack(*[EL_JAC[:, i] for i in range(4)]).row_join(EL_BASE).rank())
check("FULL_12_DIRECTION_EULER_JACOBIAN_RANK_8", EL_JAC.rank() == 8)
check("FULL_12_DIRECTION_JACOBIAN_SPANS_BASE_DEFECT", EL_JAC.rank() == EL_JAC.row_join(EL_BASE).rank())
print("EULER_JAC_RANK", EL_JAC.rank(), "AUGMENTED_RANK", EL_JAC.row_join(EL_BASE).rank())

# Find the smallest set containing a residual-active column that spans -EL_BASE.
minimum_sets = []
for size in range(1, len(candidate_names) + 1):
    for subset in combinations(range(len(candidate_names)), size):
        if not set(subset).intersection(residual_active):
            continue
        sub = EL_JAC[:, subset]
        if sub.rank() == sub.row_join(EL_BASE).rank():
            minimum_sets.append(subset)
    if minimum_sets:
        break
check("MINIMUM_RESIDUAL_ACTIVE_LINEARIZED_SUPPORT_HAS_SIZE_7", len(minimum_sets) > 0 and len(minimum_sets[0]) == 7)
print("MINIMUM_SUPPORT_COUNT", len(minimum_sets))
selected = minimum_sets[0]
selected_names = [candidate_names[i] for i in selected]
selected_matrix = EL_JAC[:, selected]
linear_correction = next(iter(sp.linsolve((selected_matrix, -EL_BASE))))
check("MINIMUM_SUPPORT_EXACT_RATIONAL_LINEAR_CORRECTION", all(
    x.is_Rational for x in linear_correction
) and selected_matrix * Matrix(linear_correction) == -EL_BASE)
print("MINIMUM_SUPPORT_NAMES", selected_names)
print("MINIMUM_SUPPORT_CORRECTION", [str(x) for x in linear_correction])
print("STATUS_LINEARIZED_GATE_ONLY_NONLINEAR_STATIONARITY_OPEN")
