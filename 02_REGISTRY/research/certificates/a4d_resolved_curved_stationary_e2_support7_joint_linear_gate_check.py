#!/usr/bin/env python3
"""Joint linear gate and exact absolute-solder obstruction at one frozen link.

Base link: the homogeneous E(2) point (j, gamma, delta) = (2, 0, 1), with the
Cayley convention and the selected seven-amplitude support owned by
a4d_resolved_curved_stationary_e2_support7_order1_check.py. Solder means one
absolute 4x4 coframe, copied at every site. This is not a sitewise solder
search and not a no-go for finite deformations of the seven amplitudes.

Two exact statements are checked.

1. Every solution of the joint linearized star system (24 Lorentz link Euler
   equations and 16 absolute-solder Euler equations) has all seven amplitudes
   equal to zero. Its solder part lies in the 10-dimensional kernel of the
   solder Hessian. The two adjugate-active amplitudes N2 on role 2 and N3 on
   role 3 are therefore zero, so every such solution has vanishing first
   adjugate variation on all four curved faces.

2. At this same frozen link the absolute-solder gradient is exactly linear.
   On its 10-dimensional zero set the link Euler is quadratic, and every
   common zero has determinant zero. The base solder eta is a nondegenerate
   critical point whose link Euler is the known nonzero defect, so criticality
   alone does not force degeneracy.

Every face holonomy satisfies det(I-P) = adj(I-P) = 0 while at least one
curvature bivector is nonzero. The owned joint residual therefore vanishes
for every translation, and the four channel integrands contribute nothing to
the first link or translation derivative at this link. No active-residual
witness is obtained.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path

import sympy as sp


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name)


OWNER_PATH = Path(__file__).with_name(
    "a4d_resolved_curved_stationary_e2_support7_order1_check.py"
)
spec = importlib.util.spec_from_file_location("support7_order1_owner", OWNER_PATH)
owner = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(owner)


def solder_gradient_value(theta: sp.Matrix) -> sp.Matrix:
    out = sp.zeros(16, 1)
    for face in owner.PAIRS:
        r, s = face
        link_r = owner.role0[r]
        link_s = owner.role0[s]
        p = link_r * link_s * link_r.inv() * link_s.inv()
        curvature = (p - p.inv()) / 2
        response = owner.G2 * owner.STAR * owner.bivector_of_tangent(curvature)
        u, v = [i for i in range(4) if i not in face]
        for a in range(4):
            axis = sp.eye(4)[:, a]
            for b in range(4):
                leg = sp.zeros(6, 1)
                if b == u:
                    leg += owner.wedge(axis, theta[:, v])
                if b == v:
                    leg += owner.wedge(theta[:, u], axis)
                out[4 * a + b] += 16 * owner.orientation(face) * (leg.T * response)[0]
    return out


def solder_gradient_jet(role, theta: sp.Matrix):
    out = [owner.MJet(sp.zeros(1, 1)) for _ in range(16)]
    for face in owner.PAIRS:
        r, s = face
        p = role[r] * role[s] * role[r].inv() * role[s].inv()
        curvature = (p - p.inv()) / 2
        response = owner.constant_jet(owner.G2 * owner.STAR) * owner.bivector_of_tangent_jet(
            curvature
        )
        u, v = [i for i in range(4) if i not in face]
        for a in range(4):
            axis = sp.eye(4)[:, a]
            for b in range(4):
                leg = sp.zeros(6, 1)
                if b == u:
                    leg += owner.wedge(axis, theta[:, v])
                if b == v:
                    leg += owner.wedge(theta[:, u], axis)
                out[4 * a + b] += (
                    16 * owner.orientation(face) * owner.constant_jet(leg.T) * response
                )
    return out


def curvature_responses(role_index: int, generator: sp.Matrix):
    increment = owner.cayley_diff(owner.generators0[role_index], generator)
    responses = {}
    for r, s in owner.PAIRS:
        link_r, link_s = owner.role0[r], owner.role0[s]
        inverse_r, inverse_s = link_r.inv(), link_s.inv()
        d_r = increment if r == role_index else sp.zeros(4)
        d_s = increment if s == role_index else sp.zeros(4)
        d_inverse_r = (
            -inverse_r * d_r * inverse_r if r == role_index else sp.zeros(4)
        )
        d_inverse_s = (
            -inverse_s * d_s * inverse_s if s == role_index else sp.zeros(4)
        )
        p = link_r * link_s * inverse_r * inverse_s
        dp = (
            d_r * link_s * inverse_r * inverse_s
            + link_r * d_s * inverse_r * inverse_s
            + link_r * link_s * d_inverse_r * inverse_s
            + link_r * link_s * inverse_r * d_inverse_s
        )
        responses[(r, s)] = owner.G2 * owner.STAR * owner.bivector_of_tangent(
            owner.d_curvature(p, dp)
        )
    return responses


def link_euler_at(theta: sp.Matrix, responses_by_test) -> sp.Matrix:
    values = []
    for responses in responses_by_test:
        total = sp.Integer(0)
        for face, response in responses.items():
            u, v = [i for i in range(4) if i not in face]
            total += 16 * owner.orientation(face) * (
                owner.wedge(theta[:, u], theta[:, v]).T * response
            )[0]
        values.append(sp.expand(total))
    return sp.Matrix(values)


def solder_derivative_row(responses) -> sp.Matrix:
    row = sp.zeros(1, 16)
    for face, response in responses.items():
        u, v = [i for i in range(4) if i not in face]
        for a in range(4):
            axis = sp.eye(4)[:, a]
            for b in range(4):
                leg = sp.zeros(6, 1)
                if b == u:
                    leg += owner.wedge(axis, owner.ETA[:, v])
                if b == v:
                    leg += owner.wedge(owner.ETA[:, u], axis)
                row[0, 4 * a + b] += 16 * owner.orientation(face) * (leg.T * response)[0]
    return row


TESTS = [(r, generator) for r in range(4) for _, generator in owner.ALL_TESTS]
RESPONSES = [curvature_responses(r, generator) for r, generator in TESTS]
E0 = link_euler_at(owner.ETA, RESPONSES)
EXPECTED_E0 = sp.Matrix(
    [0, 0, 0, 0, -16, 0]
    + [0, 0, 0, 0, 16, 0]
    + [0, 0, 0, 0, -32, 64]
    + [0, 0, 0, 0, 0, -32]
)
check("BASE_LINK_EULER_REPRODUCED", E0 == EXPECTED_E0)
check("BASE_LINK_EULER_NONZERO", E0 != sp.zeros(24, 1))

generator_stack = sp.Matrix.hstack(*[
    sp.Matrix(list(generator)) for _, generator in owner.ALL_TESTS
])
check("SIX_LORENTZ_TESTS_ARE_A_BASIS", generator_stack.rank() == 6)

link_columns = []
for _, role_index, generator in owner.SELECTED_SPECS:
    generators_j = [
        owner.MJet(base, generator if r == role_index else sp.zeros(4))
        for r, base in enumerate(owner.generators0)
    ]
    role_j = [owner.cayley_jet(a) for a in generators_j]
    link_columns.append(sp.Matrix([
        owner.d_star_jet(role_j, generators_j, r, test)[1] for r, test in TESTS
    ]))
j_link = sp.Matrix.hstack(*link_columns)
missing_rows = [6 * r + offset for r in range(4) for offset in (4, 5)]
check("MISSING_BLOCK_AGREES_WITH_ORDER1_OWNER", j_link[missing_rows, :] == owner.J_missing)

m_solder = sp.Matrix.vstack(*[solder_derivative_row(responses) for responses in RESPONSES])
vec_eta = sp.Matrix(list(owner.ETA))
check("SOLDER_SCALE_DERIVATIVE_IS_TWICE_BASE_DEFECT", m_solder * vec_eta == 2 * E0)

hessian_columns = []
for i in range(4):
    for j in range(4):
        basis = sp.zeros(4)
        basis[i, j] = 1
        hessian_columns.append(solder_gradient_value(basis))
hessian = sp.Matrix.hstack(*hessian_columns)
check("SOLDER_HESSIAN_SYMMETRIC_RANK_6", hessian == hessian.T and hessian.rank() == 6)
check("ETA_IS_SOLDER_CRITICAL", hessian * vec_eta == sp.zeros(16, 1))

symbols = sp.symbols("t0:16")
symbolic_theta = sp.Matrix(4, 4, lambda i, j: symbols[4 * i + j])
# The next identity is the bilinear leg structure of the star density. It cannot
# fail while that density is unchanged. The load-bearing controls are the
# nonzero base defect, the nondegenerate critical witness, and the wall below.
check(
    "SOLDER_GRADIENT_IS_EXACTLY_LINEAR",
    sp.expand(solder_gradient_value(symbolic_theta) - hessian * sp.Matrix(symbols))
    == sp.zeros(16, 1),
)

mixed_columns = []
for _, role_index, generator in owner.SELECTED_SPECS:
    generators_j = [
        owner.MJet(base, generator if r == role_index else sp.zeros(4))
        for r, base in enumerate(owner.generators0)
    ]
    role_j = [owner.cayley_jet(a) for a in generators_j]
    mixed_columns.append(sp.Matrix([
        component.d[0] for component in solder_gradient_jet(role_j, owner.ETA)
    ]))
j_solder = sp.Matrix.hstack(*mixed_columns)
clairaut = True
for column, (_, role_index, generator) in enumerate(owner.SELECTED_SPECS):
    offset = next(
        index for index, (_, test) in enumerate(owner.ALL_TESTS) if test == generator
    )
    if sp.expand(m_solder[6 * role_index + offset, :].T - j_solder[:, column]) != sp.zeros(16, 1):
        clairaut = False
check("MIXED_PARTIALS_AGREE_ON_THE_SEVEN_SUPPORT", clairaut)

joint = sp.BlockMatrix([
    [j_link, m_solder],
    [j_solder, hessian],
]).as_explicit()
rhs = sp.Matrix.vstack(-E0, sp.zeros(16, 1))
check("JOINT_LINEAR_SYSTEM_RANK_19", joint.rank() == 19)
check("JOINT_LINEAR_SYSTEM_CONSISTENT", joint.row_join(rhs).rank() == 19)
particular = sp.zeros(23, 1)
particular[7:, 0] = -sp.Rational(1, 2) * vec_eta
check("PURE_SOLDER_SCALE_IS_A_PARTICULAR_SOLUTION", joint * particular == rhs)
kernel = joint.nullspace()
check("JOINT_HOMOGENEOUS_KERNEL_DIMENSION_4", len(kernel) == 4)
amplitude_kernel = sp.Matrix.hstack(*[vector[:7, :] for vector in kernel])
check("EVERY_JOINT_SOLUTION_HAS_ZERO_AMPLITUDES", amplitude_kernel == sp.zeros(7, len(kernel)))

kernel_matrices = [
    sp.Matrix([[1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]),
    sp.Matrix([[0, 0, 2, 1], [0, 0, 2, 1], [1, 1, 0, 0], [0, 0, 0, 0]]),
    sp.Matrix([[0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0], [1, 1, 0, 0]]),
    sp.Matrix([[0, -1, -3, -1], [1, 0, -3, -1], [0, 0, 1, 0], [0, 0, 0, 1]]),
]
kernel_vectors = sp.Matrix.hstack(*[sp.Matrix(list(matrix)) for matrix in kernel_matrices])
check("HOMOGENEOUS_SOLDER_KERNEL_BASIS_RANK_4", kernel_vectors.rank() == 4)
check(
    "HOMOGENEOUS_SOLDER_KERNEL_KILLS_HESSIAN_AND_LINK_DERIVATIVE",
    hessian * kernel_vectors == sp.zeros(16, 4) and m_solder * kernel_vectors == sp.zeros(24, 4),
)
check(
    "HOMOGENEOUS_SOLDER_KERNEL_SPANS_THE_POLAR",
    sp.Matrix.vstack(hessian, m_solder).rank() == 12,
)
check("ETA_IS_NOT_IN_THE_POLAR_KERNEL", sp.Matrix.hstack(kernel_vectors, vec_eta).rank() == 5)

curved_faces = ((0, 2), (0, 3), (1, 2), (1, 3))
expected_adj_ranks = {
    "K1_0": (0, 0, 0, 0),
    "K1_2": (0, 0, 0, 0),
    "N2_2": (2, 0, 2, 0),
    "N3_0": (0, 0, 0, 0),
    "N3_1": (0, 0, 0, 0),
    "N3_2": (0, 0, 0, 0),
    "N3_3": (0, 2, 0, 2),
}
one = owner.constant_jet(owner.I4)
for name, role_index, generator in owner.SELECTED_SPECS:
    generators_j = [
        owner.MJet(base, generator if r == role_index else sp.zeros(4))
        for r, base in enumerate(owner.generators0)
    ]
    role_j = [owner.cayley_jet(a) for a in generators_j]
    det_derivatives = []
    adj_ranks = []
    for a, b in curved_faces:
        holonomy = role_j[a] * role_j[b] * role_j[a].inv() * role_j[b].inv()
        factor = one - holonomy
        det_derivatives.append(owner.det_direction(factor.v, factor.d))
        adj_ranks.append(owner.adj_direction(factor.v, factor.d).rank())
    check(f"{name}_DETERMINANT_DERIVATIVE_ZERO", all(value == 0 for value in det_derivatives))
    check(f"{name}_ADJUGATE_RANKS", tuple(adj_ranks) == expected_adj_ranks[name])

curvature_nonzero = 0
for a, b in owner.PAIRS:
    link_a, link_b = owner.role0[a], owner.role0[b]
    holonomy = link_a * link_b * link_a.inv() * link_b.inv()
    factor = owner.I4 - holonomy
    check(f"FACE_{a}_{b}_DET_AND_ADJUGATE_ZERO", factor.det() == 0 and factor.adjugate() == sp.zeros(4))
    curvature = owner.bivector_of_tangent((holonomy - holonomy.inv()) / 2)
    if curvature != sp.zeros(6, 1):
        curvature_nonzero += 1
check("FROZEN_LINK_HAS_NONZERO_CURVATURE", curvature_nonzero == 4)
print("CURVED_FACE_COUNT", curvature_nonzero)

# Exact absolute-solder zero set at the frozen link.
z_names = sp.symbols("z0:10")
z_vector = sp.Matrix(z_names)
theta = sp.Matrix([
    [z_names[0] + z_names[1] - z_names[2], z_names[0], z_names[3], z_names[4]],
    [z_names[1], z_names[2], z_names[3], z_names[4]],
    [z_names[5], z_names[5], z_names[6] + z_names[8] + z_names[9], z_names[6]],
    [z_names[7], z_names[7], z_names[8], z_names[9]],
])
coordinate_basis = sp.Matrix.hstack(*[
    sp.Matrix(list(theta.subs({name: int(index == column) for index, name in enumerate(z_names)})))
    for column in range(10)
])
check("CRITICAL_COORDINATES_ARE_A_KERNEL_BASIS", coordinate_basis.rank() == 10)
check("CRITICAL_COORDINATES_ARE_HESSIAN_NULL", hessian * coordinate_basis == sp.zeros(16, 10))

euler_polynomials = list(link_euler_at(theta, RESPONSES))
check(
    "CRITICAL_LINK_EULER_IS_QUADRATIC_OR_ZERO",
    all(polynomial == 0 or sp.total_degree(polynomial) == 2 for polynomial in euler_polynomials),
)
eta_coordinates = {z_names[2]: -1, z_names[9]: -1}
for name in z_names:
    eta_coordinates.setdefault(name, 0)
check(
    "CRITICAL_POLYNOMIALS_REPRODUCE_BASE_DEFECT",
    sp.Matrix([polynomial.subs(eta_coordinates) for polynomial in euler_polynomials]) == E0,
)
# Quadratic homogeneity on the scale line is the same bilinear structure.
# Comparing eta/2 with E0/4 is load-bearing only because E0 is nonzero.
scale = sp.symbols("t")
scaled = [polynomial.subs({name: scale * eta_coordinates[name] for name in z_names}) for polynomial in euler_polynomials]
check(
    "SCALE_LINE_EULER_IS_QUADRATIC",
    sp.Matrix([sp.expand(value - scale**2 * defect) for value, defect in zip(scaled, E0)])
    == sp.zeros(24, 1),
)
half_eta = owner.ETA / 2
check("HALF_ETA_REMAINS_SOLDER_CRITICAL", hessian * sp.Matrix(list(half_eta)) == sp.zeros(16, 1))
check("HALF_ETA_EXACT_EULER_IS_ONE_QUARTER_DEFECT", link_euler_at(half_eta, RESPONSES) == E0 / 4)
check("HALF_ETA_IS_NONDEGENERATE", half_eta.det() == -sp.Rational(1, 16))

determinant = sp.factor(theta.det())
wall = (z_names[0] - z_names[2]) * (z_names[1] - z_names[2])
complement = z_names[6] * z_names[8] - z_names[6] * z_names[9] - z_names[8] * z_names[9] - z_names[9]**2
check("DETERMINANT_FACTORS_THROUGH_THE_EULER_WALL", sp.expand(determinant - wall * complement) == 0)

monomials = set()
for polynomial in euler_polynomials:
    monomials.update(sp.Poly(sp.expand(polynomial), *z_names).terms())
target = sp.Poly(sp.expand(wall), *z_names)
monomials.update(target.terms())
ordered = sorted({monomial for monomial, _ in monomials})
rows = []
for polynomial in euler_polynomials:
    coefficient = sp.Poly(sp.expand(polynomial), *z_names)
    rows.append([coefficient.coeff_monomial(monomial) for monomial in ordered])
system = sp.Matrix(rows).T
target_column = sp.Matrix([target.coeff_monomial(monomial) for monomial in ordered])
wall_coefficients, free_parameters = system.gauss_jordan_solve(target_column)
wall_coefficients = wall_coefficients.subs({parameter: 0 for parameter in free_parameters})
check(
    "EULER_WALL_IS_AN_EXPLICIT_LINEAR_COMBINATION",
    sp.expand(sum(wall_coefficients[i] * euler_polynomials[i] for i in range(24)) - wall) == 0,
)
check(
    "EULER_WALL_IS_ROLE2_N3_PLUS_ROLE3_N2_OVER_64",
    sp.expand((euler_polynomials[17] + euler_polynomials[22]) / 64 - wall) == 0,
)
print(
    "EULER_WALL_COMBINATION",
    [(i, str(wall_coefficients[i])) for i in range(24) if wall_coefficients[i] != 0],
)

witness_values = {
    z_names[0]: 1,
    z_names[1]: 1,
    z_names[6]: 1,
    z_names[8]: 1,
}
for name in z_names:
    witness_values.setdefault(name, 0)
witness = theta.subs(witness_values)
check("NONDEGENERATE_CRITICAL_SOLDER_EXISTS", witness.det() == 1)
check(
    "NONDEGENERATE_CRITICAL_SOLDER_IS_NOT_LINK_STATIONARY",
    link_euler_at(witness, RESPONSES) != sp.zeros(24, 1),
)
check("DEGENERATE_ORIGIN_IS_LINK_STATIONARY", link_euler_at(sp.zeros(4), RESPONSES) == sp.zeros(24, 1))

print("JOINT_SOLUTION_AMPLITUDES", "identically zero")
print("ADJUGATE_ACTIVE_AMPLITUDES_IN_EVERY_JOINT_SOLUTION", "N2_2=0", "N3_3=0")
print("OPEN_ABSOLUTE_SOLDER_AT_FROZEN_LINK", "empty")
print("STATUS: no active-residual L=2 witness; finite seven-amplitude deformations away from this link remain open")
