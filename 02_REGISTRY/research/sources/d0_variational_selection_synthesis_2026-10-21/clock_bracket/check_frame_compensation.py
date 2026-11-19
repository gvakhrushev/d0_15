#!/usr/bin/env python3
"""Exact moving-frame compensation at a constant flat CAR16 base.

This is a bounded symbolic coefficient test, not a physical clock compiler.
The existing clock checker/PROOF/RESULT are not changed. No assert statements.
"""
from pathlib import Path
import hashlib
import json
import sys
import sympy as s

ROOT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / 'inputs'
PINS = {
    "02_REGISTRY/research/sources/d0_native_preparation_closure_2026-10-21/inputs/native_input.py":
        "1c501d5609dda3e14a3da95aad0c77ea04ef48bf94921793a403fb058a805fe9",
    "02_REGISTRY/research/sources/d0_paid_moment_field_writer_2026-10-21/moments/EXACT_MOMENT_SOURCE_CONSTRUCTION.md":
        "8c4c3cf03ebf637de6917776f13533d8b9f20cd0e8790025cf64a092915aef15",
    "02_REGISTRY/research/sources/d0_paid_moment_field_writer_2026-10-21/code/PAID_CODE_AND_MOMENT_WRITER.md":
        "e95f0486456c53cf0ce40023bab08ac744fd6189b397d29a8773446c168244a0",
    "02_REGISTRY/research/A4D_DENSITY_DRESSED_CAR_EINSTEIN_METRIC_2026_10_18.md":
        "a33e364caed023d74cc70cfdc38380581bbb4f47af96e1c23ad7d3490e9da169",
}
CHECKS = []


def check(ok, name):
    if not bool(ok):
        raise ArithmeticError(name)
    CHECKS.append(name)


for path, digest in PINS.items():
    check(hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest,
          "source pin " + path)

x, y, z = s.symbols("x y z", real=True)
xs = (x, y, z)
eye = s.eye(16)
zero = s.zeros(16)


def expand(matrix):
    return matrix.applyfunc(s.expand)


def comm(a, b):
    return a * b - b * a


def creators():
    order = (0, 2, 3, 1)
    out = []
    for r in range(4):
        c = s.zeros(16)
        before = order[:order.index(r)]
        for bits in range(16):
            if not ((bits >> r) & 1):
                c[bits | (1 << r), bits] = (-1) ** sum(
                    (bits >> j) & 1 for j in before)
        out.append(c)
    return out


cs = creators()
for i in range(4):
    for j in range(4):
        check(cs[i] * cs[j].T + cs[j].T * cs[i]
              == (eye if i == j else zero), f"full16 CAR {i},{j}")
alpha = [s.I * (cs[i] - cs[i].T) for i in (1, 2, 3)]
for i in range(3):
    check(alpha[i].H == alpha[i], f"Hermitian spatial alpha {i}")
    for j in range(3):
        check(alpha[i] * alpha[j] + alpha[j] * alpha[i]
              == (2 * eye if i == j else zero),
              f"spatial Clifford {i},{j}")

# Arbitrary smooth-function jets, not a polynomial sample. The equality is
# verified as the three principal matrix coefficients and the zero-order
# matrix coefficient of a first-order operator on every CAR16 component.
N = s.Function("N")(*xs)
X = [s.Function(f"X{i}")(*xs) for i in range(3)]
div_x = sum(s.diff(X[i], xs[i]) for i in range(3))
strain = s.Matrix(3, 3, lambda i, j:
                  (s.diff(X[j], xs[i]) + s.diff(X[i], xs[j])) / 2)
spin = sum((comm(alpha[i], alpha[j]) * s.diff(X[j], xs[i]) / 8
            for i in range(3) for j in range(3)), zero)
k = div_x * eye / 2 + spin
delta_alpha = [-sum((alpha[i] * strain[i, j] for i in range(3)), zero)
               for j in range(3)]
XN = sum(X[i] * s.diff(N, xs[i]) for i in range(3))
b = sum((alpha[i] * s.diff(N, xs[i]) / 2 for i in range(3)), zero)

for j in range(3):
    frozen = -s.I * expand(
        XN * alpha[j]
        - sum((N * alpha[i] * s.diff(X[j], xs[i])
               for i in range(3)), zero)
        + N * comm(k, alpha[j]) - XN * alpha[j])
    moving = -s.I * N * delta_alpha[j]
    check(expand(frozen - moving) == zero,
          f"arbitrary-function full16 principal compensation {j}")

frozen_zero = -s.I * expand(
    sum((X[i] * b.diff(xs[i]) - N * alpha[i] * k.diff(xs[i])
         for i in range(3)), zero)
    + comm(k, b)
    - sum((alpha[j] * s.diff(XN, xs[j]) / 2
           for j in range(3)), zero))
moving_zero = -s.I * sum(((N * delta_alpha[j]).diff(xs[j]) / 2
                         for j in range(3)), zero)
check(expand(frozen_zero - moving_zero) == zero,
      "arbitrary-function full16 zero-order half-density compensation")

spin_derivative = sum((alpha[j] * spin.diff(xs[j])
                       for j in range(3)), zero)
spin_reduction = sum((alpha[i] * (
    sum(s.diff(X[i], t, 2) for t in xs) - s.diff(div_x, xs[i])) / 4
    for i in range(3)), zero)
check(expand(spin_derivative - spin_reduction) == zero,
      "Clifford three-form cancels against symmetric second derivatives")

# Explicit hostile controls for each indispensable piece of the identity.
# X=x d_x, N=1: frozen residual = i alpha^x d_x, as is delta H.
correct_dilation_principal = s.I * alpha[0]
check(correct_dilation_principal != zero,
      "frozen dilation has a nonzero strain defect")
check(correct_dilation_principal - s.I * alpha[0] == zero,
      "subtracting field derivative cancels dilation defect")
check(correct_dilation_principal + s.I * alpha[0] != zero,
      "adding field derivative instead doubles dilation defect")
# X=x^2 d_x, N=1: delta alpha^x=-2x alpha^x; zero-order delta H=i alpha^x.
nonlinear_half_density = -s.I * (-2 * x * alpha[0]).diff(x) / 2
check(nonlinear_half_density == s.I * alpha[0]
      and nonlinear_half_density != zero,
      "omitting moving half-density derivative fails for quadratic shift")
# Rotation X=(-y,x,0) has zero strain. Its spin lift cancels rotation of alpha.
rotation = (-y, x, s.Integer(0))
rotation_spin = comm(alpha[0], alpha[1]) / 4
raw_rotation = -sum((alpha[i] * s.diff(rotation[0], xs[i])
                     for i in range(3)), zero)
check(raw_rotation != zero
      and raw_rotation + comm(rotation_spin, alpha[0]) == zero,
      "omitting spin transport fails even for a zero-strain rotation")

# This particular Clifford spin lift is not the old grade-preserving
# exterior Lorentz-link tangent. It acts nontrivially on the scalar vacuum.
vacuum = s.zeros(16, 1)
vacuum[0] = 1
spin_vacuum = rotation_spin * vacuum
grade_two_only = all(spin_vacuum[j] == 0 or j.bit_count() == 2
                     for j in range(16))
exterior_rotation = cs[1] * cs[2].T - cs[2] * cs[1].T
check(spin_vacuum != s.zeros(16, 1) and grade_two_only
      and exterior_rotation * vacuum == s.zeros(16, 1),
      "Clifford spin lift is distinct from old exterior-link tangent")
beta = [cs[i] + cs[i].T for i in (1, 2, 3)]
flavor = beta[0] * beta[1] / 2
check(exterior_rotation == rotation_spin + flavor and flavor != zero,
      "exterior rotation equals Clifford lift plus explicit commutant")
for i in range(3):
    check(comm(flavor, alpha[i]) == zero,
          f"exterior and Clifford lifts induce the same vector rotation {i}")

# The original full16 inverse-coframe moment chart admits the strain
# tangent. A nonscalar rational coframe guards matrix order/transposes.
eta = s.diag(1, -1, -1, -1)
T = s.Matrix([[1, s.Rational(1, 2), 0, 0],
              [1, -s.Rational(1, 2), 0, 0],
              [0, 0, 1, 0], [0, 0, 0, 1]])
E = s.eye(4)
E[1, 0] = s.Rational(1, 14)
E[0, 2] = s.Rational(1, 100)
E[2, 3] = s.Rational(1, 200)
E[3, 1] = s.Rational(1, 150)
u, v, w, a, b0, c0 = s.symbols("u v w a b c", real=True)
B = s.zeros(4)
B[1:4, 1:4] = s.Matrix([[u, a, b0], [a, v, c0], [b0, c0, w]])
D = eta * (T * E).inv().T
delta_D = -D * B.T
delta_E = -E * (delta_D.T * eta * T) * E
check(expand((D.T * eta * T).inv() - E) == s.zeros(4),
      "original inverse-coframe moment map decoded exactly")
check(expand(delta_E - E * B) == s.zeros(4),
      "all six symbolic spatial strains are full-coframe chart tangents")
check(expand(delta_D.T * eta * T + B * E.inv()) == s.zeros(4),
      "inverse-frame variation has the required minus strain sign")

print(json.dumps({
    "scope": "exact formal operator compensation at a constant flat CAR16 base",
    "source_sha256": PINS,
    "checks": CHECKS,
    "passed": len(CHECKS),
    "identity": "[K_X,H_N]-H_(X.N)-delta_alpha H_N[delta_X alpha]=0",
    "generic_symbolic_principal_and_zero_order": True,
    "paid_moment_node_tangent_available": True,
    "physical_field_transport_admission": False,
    "physical_normal_clock_admission": False,
    "full_gravitational_constraint_algebra": False,
    "GR_closed": False,
}, indent=2))
