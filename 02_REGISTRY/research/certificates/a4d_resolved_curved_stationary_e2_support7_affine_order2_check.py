#!/usr/bin/env python3
"""Exact affine-residual jet on the selected all-face-active seven-support.

The Lorentz path is the rational Cayley path already owned by
a4d_resolved_curved_stationary_e2_support7_order1_check.py.  This certificate
uses a homogeneous matched translation b_r for each link direction, with the
same b_r on all 16 sites of the L=2 torus.  It computes the full order-two
joint-residual jet as a linear map in all 16 translation components and the
leading order-four forms of all four existing channels.

It does not solve the affine Euler equation R=R_*(C), and it does not claim a
stationary branch or finite vacuum.
"""
from __future__ import annotations

import hashlib
from pathlib import Path
from collections import Counter
from itertools import combinations, permutations

import sympy as sp
from sympy import Matrix, Rational, eye, zeros


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


ETA = sp.diag(1, -1, -1, -1)
I4 = eye(4)
PAIRS = list(combinations(range(4), 2))


def gen_boost(i: int) -> Matrix:
    a = zeros(4)
    a[0, i] = a[i, 0] = 1
    return a


def gen_rot(i: int, j: int) -> Matrix:
    a = zeros(4)
    a[i, j] = -1
    a[j, i] = 1
    return a


K1 = gen_boost(1)
N2 = gen_boost(2) + gen_rot(1, 2)
N3 = gen_boost(3) + gen_rot(1, 3)
M2 = gen_boost(2) - gen_rot(1, 2)
M3 = gen_boost(3) - gen_rot(1, 3)
J23 = gen_rot(2, 3)

# The unique size-seven support with both first-order cofactor-active columns.
# Generator order is (K1_0, K1_2, N2_2, N3_0, N3_1, N3_2, N3_3).
BASE = [-2 * J23, -2 * J23, M3, M2]
H = [
    Rational(-346, 13) * K1 + Rational(58, 13) * N3,
    Rational(311, 13) * N3,
    Rational(-22, 13) * K1 + Rational(-609, 26) * N2
    + Rational(-24, 13) * N3,
    Rational(-11, 26) * N3,
]
SUPPORT = ("K1_0", "K1_2", "N2_2", "N3_0", "N3_1", "N3_2", "N3_3")
check("SELECTED_SUPPORT_LABELS", SUPPORT == (
    "K1_0", "K1_2", "N2_2", "N3_0", "N3_1", "N3_2", "N3_3"
))
check("BASE_AND_PATH_DIRECTIONS_LIE_ALGEBRA", all(
    (a.T * ETA + ETA * a) == zeros(4) for a in BASE + H
))


def jet_add(a, b):
    return [a[k] + b[k] for k in range(3)]


def jet_neg(a):
    return [-x for x in a]


def jet_mul(a, b):
    return [
        sum((a[i] * b[k - i] for i in range(k + 1)), zeros(a[0].rows, b[0].cols))
        for k in range(3)
    ]


def jet_inv(a):
    x0 = a[0].inv()
    x1 = -x0 * a[1] * x0
    x2 = x0 * a[1] * x0 * a[1] * x0 - x0 * a[2] * x0
    return [x0, x1, x2]


def scalar_jet_mul(a, b):
    return [
        sum((a[i] * b[k - i] for i in range(k + 1)), zeros(b[0].rows, b[0].cols))
        for k in range(3)
    ]


def det_jet(a):
    size = a[0].rows
    out = [sp.S.Zero, sp.S.Zero, sp.S.Zero]
    for perm in permutations(range(size)):
        inversions = sum(
            perm[i] > perm[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        prod = [sp.S.One, sp.S.Zero, sp.S.Zero]
        for row, col in enumerate(perm):
            entry = [a[k][row, col] for k in range(3)]
            prod = [
                sum(prod[i] * entry[k - i] for i in range(k + 1))
                for k in range(3)
            ]
        sign = -1 if inversions % 2 else 1
        out = [out[k] + sign * prod[k] for k in range(3)]
    return out


def adj_jet(a):
    size = a[0].rows
    out = [zeros(size) for _ in range(3)]
    for i in range(size):
        for j in range(size):
            rows = [r for r in range(size) if r != j]
            cols = [c for c in range(size) if c != i]
            minor = [
                Matrix([[a[k][r, c] for c in cols] for r in rows])
                for k in range(3)
            ]
            cof = det_jet(minor)
            sign = -1 if (i + j) % 2 else 1
            for k in range(3):
                out[k][i, j] = sign * cof[k]
    return out


def constant_jet(a):
    a = Matrix(a)
    return [a, zeros(*a.shape), zeros(*a.shape)]


def cayley_jet(a, h):
    numerator = [I4 + a / 2, h / 2, zeros(4)]
    denominator = [I4 - a / 2, -h / 2, zeros(4)]
    return jet_mul(numerator, jet_inv(denominator))


U = [cayley_jet(a, h) for a, h in zip(BASE, H)]
Uinv = [jet_inv(u) for u in U]
check("CAYLEY_CHART_OPEN_AT_BASE", all(
    (I4 - a / 2).det() != 0 for a in BASE
))
check("BASE_LINKS_LORENTZ", all(u[0].T * ETA * u[0] == ETA for u in U))

faces = list(combinations(range(4), 2))
face_data = {}
for r, s in faces:
    p = jet_mul(jet_mul(jet_mul(U[r], U[s]), Uinv[r]), Uinv[s])
    m = jet_add(constant_jet(I4), jet_neg(p))
    d = det_jet(m)
    a = adj_jet(m)
    face_data[(r, s)] = (p, m, d, a)
    check(f"FACE_{r}_{s}_DET0_AND_DET1_ZERO", d[0] == 0 and d[1] == 0)
    check(f"FACE_{r}_{s}_ADJ0_ZERO", a[0] == zeros(4))
    print(
        f"FACE_{r}_{s}_JET",
        "det", [str(x) for x in d],
        "adj coefficient ranks", [a[k].rank() for k in range(3)],
    )

expected_det2 = {
    (0, 1): 0,
    (0, 2): Rational(-1483524, 169),
    (0, 3): Rational(-484, 169),
    (1, 2): Rational(-1483524, 169),
    (1, 3): Rational(-484, 169),
    (2, 3): 0,
}
check("EXACT_DET_SECOND_COEFFICIENTS", all(
    face_data[f][2][2] == expected_det2[f] for f in faces
))
for f in ((0, 2), (0, 3), (1, 2), (1, 3)):
    check(f"CURVED_FACE_{f[0]}_{f[1]}_ADJ_FIRST_ORDER_RANK_2",
          face_data[f][3][1].rank() == 2)


def translation_jet(face, b):
    r, s = face
    first = jet_add(constant_jet(b[r]), jet_mul(U[r], constant_jet(b[s])))
    second = jet_add(constant_jet(b[s]), jet_mul(U[s], constant_jet(b[r])))
    return jet_add(first, jet_neg(jet_mul(face_data[face][0], second)))


def joint_residual_jet(face1, face2, b):
    _, m1, det1, adj1 = face_data[face1]
    _, m2, _, _ = face_data[face2]
    t1 = translation_jet(face1, b)
    t2 = translation_jet(face2, b)
    return jet_add(
        scalar_jet_mul(det1, t2),
        jet_neg(jet_mul(jet_mul(m2, adj1), t1)),
    )


# One homogeneous b_r per role/direction, four components each.
translation_basis = []
for r in range(4):
    for k in range(4):
        b = [zeros(4, 1) for _ in range(4)]
        b[r][k] = 1
        translation_basis.append(b)


def face_class(f1, f2):
    return "adj" if len(set(f1) & set(f2)) == 1 else "opp"


Q_N = Matrix([1, 1, 0, 0]) * Matrix([1, 1, 0, 0]).T
quadratic_forms = {
    (kind, cls): zeros(16)
    for kind in ("eta", "n")
    for cls in ("adj", "opp")
}
rank_distribution = Counter()
active_pairs = 0

for f1 in faces:
    for f2 in faces:
        if f1 == f2:
            continue
        columns = [joint_residual_jet(f1, f2, b) for b in translation_basis]
        check(f"PAIR_{f1}_{f2}_R0_R1_ZERO_FOR_ALL_MATCHED_B", all(
            col[0] == zeros(4, 1) and col[1] == zeros(4, 1)
            for col in columns
        ))
        L2 = Matrix.hstack(*[col[2] for col in columns])
        rank_distribution[L2.rank()] += 1
        if L2 != zeros(4, 16):
            active_pairs += 1
        cls = face_class(f1, f2)
        for kind, q in (("eta", ETA), ("n", Q_N)):
            quadratic_forms[(kind, cls)] += 16 * L2.T * q * L2

check("RESIDUAL_ORDER2_RANK_DISTRIBUTION",
      rank_distribution == Counter({0: 10, 2: 8, 3: 12}))
check("TWENTY_ORDERED_FACE_PAIRS_ACTIVATE_R_AT_ORDER2",
      active_pairs == 20)

expected_channel_ranks = {
    ("eta", "adj"): 7,
    ("eta", "opp"): 3,
    ("n", "adj"): 8,
    ("n", "opp"): 4,
}
for key, expected_rank in expected_channel_ranks.items():
    form = quadratic_forms[key]
    check(f"CHANNEL_{key[0]}_{key[1]}_STARTS_AT_EPSILON4",
          form != zeros(16) and form.rank() == expected_rank)
    print("CHANNEL_ORDER_4_FORM", key, "rank", form.rank())

print("RESULT: for arbitrary homogeneous matched b, every pair residual has")
print("R(epsilon)=epsilon^2*R2(b)+O(epsilon^3); the epsilon coefficient vanishes.")
print("All four existing channel forms have nonzero epsilon^4 coefficient.")
print("This is residual activation only; no R=R_*(C), Euler solution, or branch is claimed.")
print("CERT_SHA256", hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
