#!/usr/bin/env python3
"""Exact first full-Euler jet on the uniquely all-face-active 7-support.

The input is the exact E(2) witness (j,gamma,delta)=(2,0,1) and the Cayley
generator convention owned by the corrected full-transverse certificate.
The support is selected from the eight rank-7, residual-active solutions of
the controlled-normal gate: it contains both cofactor-active directions
N2@Role2 and N3@Role3, hence activates all four curved-face adjugates at
first order.  This file then checks all 24 Lorentz link Euler components on
the exact nonlinear Cayley path A_r(eps)=A_r(0)+eps*sum_i v_i X_{r,i}.

The base witness is not stationary.  Thus the displayed ``J v = -E_0`` is a
linear Newton correction, not the tangent equation for a small stationary
germ ``x(eps)=eps*v+...``.  The script keeps the Taylor orders separate and
does not promote this computation to a branch obstruction or finite witness.
"""
from __future__ import annotations

from itertools import combinations

import sympy as sp
from sympy import Matrix, Rational, eye, zeros


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


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


class MJet:
    """A matrix first jet (value, exact directional derivative)."""

    def __init__(self, value: Matrix, deriv: Matrix | None = None):
        self.v = Matrix(value)
        self.d = zeros(*self.v.shape) if deriv is None else Matrix(deriv)

    def __add__(self, other):
        if isinstance(other, MJet):
            return MJet(self.v + other.v, self.d + other.d)
        return MJet(self.v + other, self.d)

    __radd__ = __add__

    def __neg__(self):
        return MJet(-self.v, -self.d)

    def __sub__(self, other):
        return self + (-other if isinstance(other, MJet) else -other)

    def __rsub__(self, other):
        return (-self) + other

    def __mul__(self, other):
        if isinstance(other, MJet):
            return MJet(self.v * other.v, self.d * other.v + self.v * other.d)
        if isinstance(other, sp.MatrixBase):
            return MJet(self.v * other, self.d * other)
        return MJet(self.v * other, self.d * other)

    def __rmul__(self, other):
        if isinstance(other, sp.MatrixBase):
            return MJet(other * self.v, other * self.d)
        return MJet(other * self.v, other * self.d)

    def __truediv__(self, scalar):
        return MJet(self.v / scalar, self.d / scalar)

    def inv(self):
        vi = self.v.inv()
        return MJet(vi, -vi * self.d * vi)


def constant_jet(m: Matrix) -> MJet:
    return MJet(m, zeros(*m.shape))


def cayley_jet(a: MJet) -> MJet:
    one = constant_jet(I4)
    return (one + a / 2) * (one - a / 2).inv()


def cayley_diff_jet(a: MJet, h: Matrix) -> MJet:
    one = constant_jet(I4)
    hj = constant_jet(h)
    b_inv = (one - a / 2).inv()
    u = (one + a / 2) * b_inv
    return hj / 2 * b_inv + u * hj / 2 * b_inv


def d_curvature_jet(p: MJet, dp: MJet) -> MJet:
    pi = p.inv()
    return (dp + pi * dp * pi) / 2


def bivector_of_tangent_jet(x: MJet) -> MJet:
    y = x * constant_jet(ETA)
    return MJet(
        Matrix([y.v[a, b] for a, b in PAIRS]),
        Matrix([y.d[a, b] for a, b in PAIRS]),
    )


def d_star_jet(role, generators, role_index: int, h: Matrix):
    du = cayley_diff_jet(generators[role_index], h)
    coframe = [ETA[:, r] for r in range(4)]
    site_value, site_deriv = sp.S.Zero, sp.S.Zero
    for r, s in PAIRS:
        ur, us = role[r], role[s]
        uri, usi = ur.inv(), us.inv()
        dur = du if r == role_index else constant_jet(zeros(4))
        dus = du if s == role_index else constant_jet(zeros(4))
        duri = -uri * dur * uri if r == role_index else constant_jet(zeros(4))
        dusi = -usi * dus * usi if s == role_index else constant_jet(zeros(4))
        p = ur * us * uri * usi
        dp = (
            dur * us * uri * usi
            + ur * dus * uri * usi
            + ur * us * duri * usi
            + ur * us * uri * dusi
        )
        dc = bivector_of_tangent_jet(d_curvature_jet(p, dp))
        u, v = [i for i in range(4) if i not in (r, s)]
        pairing = (
            constant_jet(wedge(coframe[u], coframe[v]).T)
            * constant_jet(G2)
            * constant_jet(STAR)
            * dc
        )
        site_value += orientation((r, s)) * pairing.v[0]
        site_deriv += orientation((r, s)) * pairing.d[0]
    return 16 * site_value, 16 * site_deriv


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
INTERNAL = (("M2", M2), ("M3", M3), ("-J23", -J23))
COMPLEMENT = (("K1", K1), ("N2", N2), ("N3", N3))
ALL_TESTS = INTERNAL + COMPLEMENT


def e2_alg(n2, n3, j):
    return n2 * M2 + n3 * M3 - j * J23


def cayley(a: Matrix) -> Matrix:
    return (I4 + a / 2) * (I4 - a / 2).inv()


def cayley_diff(a: Matrix, h: Matrix) -> Matrix:
    b_inv = (I4 - a / 2).inv()
    u = (I4 + a / 2) * b_inv
    return h / 2 * b_inv + u * h / 2 * b_inv


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


def bivector_of_tangent(x: Matrix) -> Matrix:
    y = x * ETA
    return Matrix([y[a, b] for a, b in PAIRS])


def d_curvature(p: Matrix, dp: Matrix) -> Matrix:
    pinv = p.inv()
    return (dp + pinv * dp * pinv) / 2


def d_star(role, generators, role_index: int, h: Matrix):
    du = cayley_diff(generators[role_index], h)
    coframe = [ETA[:, r] for r in range(4)]
    site = 0
    for r, s in PAIRS:
        ur, us = role[r], role[s]
        uri, usi = ur.inv(), us.inv()
        dur = du if r == role_index else zeros(4)
        dus = du if s == role_index else zeros(4)
        duri = -uri * dur * uri if r == role_index else zeros(4)
        dusi = -usi * dus * usi if s == role_index else zeros(4)
        p = ur * us * uri * usi
        dp = (
            dur * us * uri * usi
            + ur * dus * uri * usi
            + ur * us * duri * usi
            + ur * us * uri * dusi
        )
        dc = bivector_of_tangent(d_curvature(p, dp))
        u, v = [i for i in range(4) if i not in (r, s)]
        site += orientation((r, s)) * (
            wedge(coframe[u], coframe[v]).T * G2 * STAR * dc
        )[0]
    return 16 * site


def det_direction(m: Matrix, dm: Matrix):
    return sp.factor(sum(
        m.cofactor(i, j) * dm[i, j]
        for i in range(m.rows)
        for j in range(m.cols)
    ))


def adj_direction(m: Matrix, dm: Matrix) -> Matrix:
    out = zeros(m.rows)
    for i in range(m.rows):
        for j in range(m.cols):
            minor = m.minor_submatrix(j, i)
            dminor = dm.minor_submatrix(j, i)
            out[i, j] = (-1) ** (i + j) * sum(
                minor.cofactor(a, b) * dminor[a, b]
                for a in range(minor.rows)
                for b in range(minor.cols)
            )
    return out


# The eight exact minimum supports reported by the controlled-normal gate.
MINIMUM_SUPPORTS = (
    ("K1_0", "K1_1", "N2_0", "N2_2", "N2_3", "N3_0", "N3_1"),
    ("K1_0", "K1_1", "N2_0", "N2_2", "N2_3", "N3_0", "N3_2"),
    ("K1_0", "K1_1", "N2_0", "N2_2", "N2_3", "N3_1", "N3_2"),
    ("K1_0", "K1_1", "N2_0", "N2_2", "N3_0", "N3_1", "N3_2"),
    ("K1_0", "K1_1", "N2_2", "N2_3", "N3_0", "N3_1", "N3_2"),
    ("K1_0", "K1_2", "N2_2", "N3_0", "N3_1", "N3_2", "N3_3"),
    ("K1_0", "N2_0", "N2_2", "N2_3", "N3_0", "N3_1", "N3_2"),
    ("K1_1", "N2_0", "N2_2", "N2_3", "N3_0", "N3_1", "N3_2"),
)
SELECTED_NAMES = MINIMUM_SUPPORTS[5]
SELECTED_SPECS = (
    ("K1_0", 0, K1),
    ("K1_2", 2, K1),
    ("N2_2", 2, N2),
    ("N3_0", 0, N3),
    ("N3_1", 1, N3),
    ("N3_2", 2, N3),
    ("N3_3", 3, N3),
)
EXPECTED_V = (
    Rational(-346, 13), Rational(-22, 13), Rational(-609, 26),
    Rational(58, 13), Rational(311, 13), Rational(-24, 13),
    Rational(-11, 26),
)

active_names = {"N2_2", "N3_3"}
check("EIGHT_MINIMUM_SUPPORTS", len(MINIMUM_SUPPORTS) == 8)
check("SELECTED_IS_UNIQUE_SUPPORT_WITH_BOTH_ACTIVE_COLUMNS", [
    s for s in MINIMUM_SUPPORTS if active_names.issubset(s)
] == [SELECTED_NAMES])
print("SELECTED_SUPPORT", SELECTED_NAMES)

# Exact base generators for (j,gamma,delta)=(2,0,1).
generators0 = [
    e2_alg(Rational(0), Rational(0), Rational(2)),
    e2_alg(Rational(0), Rational(0), Rational(2)),
    e2_alg(Rational(0), Rational(1), Rational(0)),
    e2_alg(Rational(1), Rational(0), Rational(0)),
]
generators0j = [constant_jet(a) for a in generators0]
role0j = [cayley_jet(a) for a in generators0j]
role0 = [a.v for a in role0j]
for r, a in enumerate(generators0):
    check(f"ROLE_{r}_CAYLEY_CHART_OPEN", (I4 - a / 2).det() != 0)
    check(f"ROLE_{r}_LORENTZ", role0[r].T * ETA * role0[r] == ETA)

faces = ((0, 2), (0, 3), (1, 2), (1, 3))
base_missing = Matrix([
    d_star_jet(role0j, generators0j, r, h)[0]
    for r in range(4)
    for h in (N2, N3)
])
check("BASE_MISSING_VECTOR_REPRODUCED", list(base_missing) == [
    -16, 0, 16, 0, -32, 64, 0, -32
])

# Recompute the selected 8x7 missing-Euler Jacobian exactly by first jets.
column_by_name = {}
for name, q, h_def in SELECTED_SPECS:
    generators_j = [
        MJet(a, h_def if r == q else zeros(4))
        for r, a in enumerate(generators0)
    ]
    role_j = [cayley_jet(a) for a in generators_j]
    column_by_name[name] = [
        d_star_jet(role_j, generators_j, r, h_test)[1]
        for r in range(4)
        for h_test in (N2, N3)
    ]
J_missing = Matrix(8, 7, lambda i, j: column_by_name[SELECTED_NAMES[j]][i])
check("SELECTED_MISSING_EULER_JACOBIAN_RANK_7", J_missing.rank() == 7)
solutions = list(sp.linsolve((J_missing, -base_missing)))
check("SELECTED_CORRECTION_UNIQUE", len(solutions) == 1)
v = tuple(solutions[0])
check("SELECTED_CORRECTION_MATCHES_EXACT_GATE", v == EXPECTED_V)
check("LINEAR_NEWTON_STEP_SOLVES_MISSING_DEFECT", J_missing * Matrix(v) == -base_missing)
print("FIRST_ORDER_CORRECTION", [str(x) for x in v])

# The path itself is the exact nonlinear group ansatz; jets only extract its
# first derivative.  Each Cayley denominator is nonzero at epsilon=0.
H_by_role = [zeros(4) for _ in range(4)]
for coeff, (_, q, h_def) in zip(v, SELECTED_SPECS):
    H_by_role[q] += coeff * h_def
generators_path = [
    MJet(a, h) for a, h in zip(generators0, H_by_role)
]
role_path = [cayley_jet(a) for a in generators_path]

# Check all 24 Lorentz link Euler components through order epsilon.
base_full, first_full = [], []
labels = [name for name, _ in ALL_TESTS]
for r in range(4):
    for _, h_test in ALL_TESTS:
        e0, _ = d_star_jet(role0j, generators0j, r, h_test)
        _, e1 = d_star_jet(role_path, generators_path, r, h_test)
        base_full.append(e0)
        first_full.append(e1)

check("BASE_INTERNAL_AND_K1_EULER_ZERO", all(
    base_full[r * 6 + i] == 0
    for r in range(4)
    for i in range(4)
))
check("LINEAR_NEWTON_CORRECTION_SOLVES_MISSING_EQUATIONS", all(
    base_full[r * 6 + i] + first_full[r * 6 + i] == 0
    for r in range(4)
    for i in (4, 5)
))
check("BASEPOINT_HAS_NONZERO_ORDER_ZERO_EULER_DEFECT", any(base_full))
base_rows = [
    tuple(str(base_full[r * 6 + i]) for i in range(6))
    for r in range(4)
]
first_rows = [
    tuple(str(first_full[r * 6 + i]) for i in range(6))
    for r in range(4)
]
print("EULER_TAYLOR_CONSTANT_TERM_ROWS_M2_M3_NEGJ23_K1_N2_N3", base_rows)
print("EULER_TAYLOR_EPSILON_COEFFICIENT_ROWS_M2_M3_NEGJ23_K1_N2_N3", first_rows)
print("ORDERING_NOTE", "E(epsilon)=E0+epsilon*Jv+O(epsilon^2); E0!=0")
print("INTERPRETATION", "Jv=-E0 is the unit Newton correction equation, not small-germ solvability")

# Inspect the exact finite point obtained by taking the Newton displacement
# with unit amplitude.  This is one candidate point only, not a support no-go.
generators_unit = [a + h for a, h in zip(generators0, H_by_role)]
role_unit = [cayley(a) for a in generators_unit]
check("UNIT_NEWTON_POINT_CHART_OPEN", all(
    (I4 - a / 2).det() != 0 for a in generators_unit
))
unit_euler = [
    sp.factor(sp.cancel(sp.together(d_star(role_unit, generators_unit, r, h_test))))
    for r in range(4)
    for _, h_test in ALL_TESTS
]
unit_nonzero = sum(x != 0 for x in unit_euler)
check("UNIT_NEWTON_POINT_NOT_STAR_STATIONARY_AT_B_ZERO", unit_nonzero == 24)
print("UNIT_NEWTON_POINT_ROLE0_M2_EULER", str(unit_euler[0]))
print("UNIT_NEWTON_POINT_NONZERO_STAR_EULER_COUNT", unit_nonzero)

# First cofactor activation along the same exact path on all four curved faces.
one = constant_jet(I4)
for a, b in faces:
    p = role_path[a] * role_path[b] * role_path[a].inv() * role_path[b].inv()
    m = one - p
    ddet = det_direction(m.v, m.d)
    dadj = adj_direction(m.v, m.d)
    check(f"FACE_{a}_{b}_BASE_ADJUGATE_ZERO", m.v.adjugate() == zeros(4))
    check(f"FACE_{a}_{b}_DETERMINANT_FIRST_JET_ZERO", ddet == 0)
    check(f"FACE_{a}_{b}_ADJUGATE_FIRST_JET_RANK_2", dadj.rank() == 2)
    print(f"FACE_{a}_{b}_RESIDUAL_JET", "det: O(epsilon^2)", "adj: epsilon^1 rank", dadj.rank())

print("NOTE_ACTUAL_R_REQUIRES_AFFINE_TRANSLATION_JET; THIS_CERTIFICATE_ONLY_OWNS_ADJUGATE_ACTIVATION")
print("STATUS_SMALL_BRANCH_QUESTION_NOT_DECIDED_FROM_THIS_NONSTATIONARY_BASEPOINT")
