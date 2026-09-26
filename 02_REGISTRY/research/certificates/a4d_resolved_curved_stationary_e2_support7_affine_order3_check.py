#!/usr/bin/env python3
"""Exact third-order affine-residual jet on the shared order-two blind space.

This extends the selected rational Cayley path and homogeneous matched-b family
owned by a4d_resolved_curved_stationary_e2_support7_affine_order2_check.py.
It proves that the common order-two residual/channel kernel is detected by R3,
and computes the four channel forms at their next order on that subspace.
It does not solve the finite affine equation, an Euler system, or a branch.
"""
from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
from itertools import combinations, permutations
from pathlib import Path

import sympy as sp
from sympy import Matrix, eye, zeros


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


ORDER = 4  # coefficients through epsilon^3
HERE = Path(__file__).resolve().parent
BASE_PATH = HERE / "a4d_resolved_curved_stationary_e2_support7_affine_order2_check.py"
spec = importlib.util.spec_from_file_location("a4d_order2_certificate", BASE_PATH)
base = importlib.util.module_from_spec(spec)
assert spec.loader is not None
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(base)

I4 = eye(4)
Z4 = zeros(4)
Z41 = zeros(4, 1)


def jet_add(a, b):
    return [a[k] + b[k] for k in range(ORDER)]


def jet_neg(a):
    return [-x for x in a]


def jet_mul(a, b):
    return [
        sum((a[i] * b[k - i] for i in range(k + 1)), zeros(a[0].rows, b[0].cols))
        for k in range(ORDER)
    ]


def jet_inv(a):
    out = [a[0].inv()]
    for k in range(1, ORDER):
        correction = sum(
            (a[i] * out[k - i] for i in range(1, k + 1)),
            zeros(a[0].rows, a[0].cols),
        )
        out.append(-out[0] * correction)
    return out


def scalar_jet_mul(a, b):
    return [
        sum((a[i] * b[k - i] for i in range(k + 1)), sp.S.Zero)
        for k in range(ORDER)
    ]


def det_jet(a):
    size = a[0].rows
    out = [sp.S.Zero] * ORDER
    for perm in permutations(range(size)):
        inversions = sum(
            perm[i] > perm[j]
            for i in range(size)
            for j in range(i + 1, size)
        )
        prod = [sp.S.One] + [sp.S.Zero] * (ORDER - 1)
        for row, col in enumerate(perm):
            entry = [a[k][row, col] for k in range(ORDER)]
            prod = scalar_jet_mul(prod, entry)
        sign = -1 if inversions % 2 else 1
        out = [out[k] + sign * prod[k] for k in range(ORDER)]
    return out


def adj_jet(a):
    size = a[0].rows
    out = [zeros(size) for _ in range(ORDER)]
    for i in range(size):
        for j in range(size):
            rows = [r for r in range(size) if r != j]
            cols = [c for c in range(size) if c != i]
            minor = [
                Matrix([[a[k][r, c] for c in cols] for r in rows])
                for k in range(ORDER)
            ]
            cofactor = det_jet(minor)
            sign = -1 if (i + j) % 2 else 1
            for k in range(ORDER):
                out[k][i, j] = sign * cofactor[k]
    return out


def scalar_matrix_jet_mul(a, b):
    return [
        sum((a[i] * b[k - i] for i in range(k + 1)), zeros(b[0].rows, b[0].cols))
        for k in range(ORDER)
    ]


def cayley_jet(a, h):
    numerator = [I4 + a / 2, h / 2, Z4, Z4]
    denominator = [I4 - a / 2, -h / 2, Z4, Z4]
    return jet_mul(numerator, jet_inv(denominator))


U = [cayley_jet(a, h) for a, h in zip(base.BASE, base.H)]
Uinv = [jet_inv(u) for u in U]
check("CAYLEY_TWO_JET_MATCHES_ORDER2_OWNER", all(
    U[r][k] == base.U[r][k]
    and Uinv[r][k] == base.Uinv[r][k]
    for r in range(4)
    for k in range(3)
))

faces = list(combinations(range(4), 2))
face_data = {}
for r, s in faces:
    p = jet_mul(jet_mul(jet_mul(U[r], U[s]), Uinv[r]), Uinv[s])
    m = jet_add([I4, Z4, Z4, Z4], jet_neg(p))
    d = det_jet(m)
    a = adj_jet(m)
    face_data[(r, s)] = (p, m, d, a)
    check(f"FACE_{r}_{s}_DETERMINANT_ORDERS_0_1_ZERO", d[0] == 0 and d[1] == 0)
    check(f"FACE_{r}_{s}_ADJUGATE_ORDER0_ZERO", a[0] == Z4)


def translation_jet(face, b):
    r, s = face
    br = [b[r], Z41, Z41, Z41]
    bs = [b[s], Z41, Z41, Z41]
    first = jet_add(br, jet_mul(U[r], bs))
    second = jet_add(bs, jet_mul(U[s], br))
    return jet_add(first, jet_neg(jet_mul(face_data[face][0], second)))


def joint_residual_jet(face1, face2, b):
    _, m1, det1, adj1 = face_data[face1]
    _, m2, _, _ = face_data[face2]
    t1 = translation_jet(face1, b)
    t2 = translation_jet(face2, b)
    return jet_add(
        scalar_matrix_jet_mul(det1, t2),
        jet_neg(jet_mul(jet_mul(m2, adj1), t1)),
    )


r2_blocks = []
r3_blocks = []
channel_order6 = {
    (kind, cls): zeros(8)
    for kind in ("eta", "n")
    for cls in ("adj", "opp")
}
for f1 in faces:
    for f2 in faces:
        if f1 == f2:
            continue
        columns = [joint_residual_jet(f1, f2, b) for b in base.translation_basis]
        r2 = Matrix.hstack(*[column[2] for column in columns])
        r3 = Matrix.hstack(*[column[3] for column in columns])
        old_r2 = Matrix.hstack(*[
            base.joint_residual_jet(f1, f2, b)[2]
            for b in base.translation_basis
        ])
        check(f"PAIR_{f1}_{f2}_R2_MATCHES_ORDER2_OWNER", r2 == old_r2)
        r2_blocks.append(r2)
        r3_blocks.append((f1, f2, r3))

R2 = Matrix.vstack(*r2_blocks)
R3 = Matrix.vstack(*[block[2] for block in r3_blocks])
n_sum = base.quadratic_forms[("n", "adj")] + base.quadratic_forms[("n", "opp")]
W = Matrix.hstack(*n_sum.nullspace())
check("ORDER2_COMMON_BLIND_SPACE_DIMENSION_8",
      n_sum.is_positive_semidefinite and n_sum.rank() == 8 and W.shape == (16, 8))
check("ORDER2_RESIDUAL_HAS_SAME_KERNEL_AS_CHANNELS",
      R2.rank() == 8 and R2 * W == zeros(120, 8)
      and Matrix.vstack(R2, n_sum).rank() == 8)
check("ORDER3_RESIDUAL_INJECTIVE_ON_ORDER2_BLIND_SPACE",
      R3.shape == (120, 16) and R3.rank() == 16 and (R3 * W).rank() == 8)

for f1, f2, r3 in r3_blocks:
    cls = "adj" if len(set(f1) & set(f2)) == 1 else "opp"
    restricted = r3 * W
    for kind, q in (("eta", base.ETA), ("n", base.Q_N)):
        channel_order6[(kind, cls)] += 16 * restricted.T * q * restricted

expected_order6_ranks = {
    ("eta", "adj"): 8,
    ("eta", "opp"): 4,
    ("n", "adj"): 8,
    ("n", "opp"): 4,
}
for key, expected_rank in expected_order6_ranks.items():
    form = channel_order6[key]
    check(f"CHANNEL_{key[0]}_{key[1]}_ORDER6_RANK_{expected_rank}",
          form != zeros(8) and form.rank() == expected_rank)

n_order6_sum = channel_order6[("n", "adj")] + channel_order6[("n", "opp")]
check("N_CHANNEL_ORDER6_FORM_POSITIVE_DEFINITE_ON_W",
      n_order6_sum.is_positive_definite and n_order6_sum.rank() == 8)

print("RESULT: on the 8-dimensional shared order-two blind space, the stacked")
print("order-three residual map is injective and the order-six n-channel sum")
print("is positive definite. This rejects nonzero 2-jet blind directions only;")
print("it does not solve finite equations or establish a stationary branch.")
print("CERT_SHA256", hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
