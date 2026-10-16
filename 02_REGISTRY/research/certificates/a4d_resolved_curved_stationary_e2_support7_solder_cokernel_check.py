#!/usr/bin/env python3
"""Exact solder range gate for the eight supplied missing-Euler corrections.

Reuse the matrix-defined E(2) base, Cayley convention and support enumeration.
The four owned residual channels are independent of the free absolute solder
(f4 owner, star_action and four_channel_I); hence its Euler equations are a
necessary sector of every selected four-channel full stationary system.

This certificate does NOT identify a star-only missing-equation Newton vector
with the Newton vector of the coupled system with free solder/translations.
It tests each supplied vector against the free-solder first-order range, and
records the smaller allowed amplitude space. The base Lorentz defect is
nonzero already at order zero. No finite support no-go is inferred.
"""
from __future__ import annotations

import contextlib
import importlib.util
import io
from pathlib import Path

import sympy as sp


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print('PASS_' + name)


owner_path = Path(__file__).with_name(
    'a4d_resolved_curved_stationary_e2_support7_order1_check.py')
spec = importlib.util.spec_from_file_location('support7_order1_owner', owner_path)
owner = importlib.util.module_from_spec(spec)
with contextlib.redirect_stdout(io.StringIO()):
    spec.loader.exec_module(owner)


def solder_gradient_jet(role, theta):
    """16 homogeneous solder Euler entries, in row-major matrix order.

    The factor 16 sums the identical L=2 site equations; it has no effect on
    their zero set. Curvature is (P-P^{-1})/2, and the base coframe is ETA.
    """
    out = [owner.MJet(sp.zeros(1, 1)) for _ in range(16)]
    for face in owner.PAIRS:
        r, s = face
        p = role[r] * role[s] * role[r].inv() * role[s].inv()
        c = (p - p.inv()) / 2
        response = (owner.constant_jet(owner.G2 * owner.STAR)
                    * owner.bivector_of_tangent_jet(c))
        u, v = [i for i in range(4) if i not in face]
        for a in range(4):
            ea = sp.eye(4)[:, a]
            for b in range(4):
                dw = sp.zeros(6, 1)
                if b == u:
                    dw += owner.wedge(ea, theta[:, v])
                if b == v:
                    dw += owner.wedge(theta[:, u], ea)
                out[4*a+b] += (16 * owner.orientation(face)
                               * owner.constant_jet(dw.T) * response)
    return out


def vec(theta):
    return sp.Matrix(list(theta))


base_solder = sp.Matrix([g.v[0] for g in
                         solder_gradient_jet(owner.role0j, owner.ETA)])
check('BASE_SOLDER_EULER_ZERO', base_solder == sp.zeros(16, 1))
check('BASE_SOLDER_NONDEGENERATE', owner.ETA.det() == -1)
check('BASE_FULL_EULER_HAS_ORDER_ZERO_DEFECT', owner.base_missing != sp.zeros(8, 1))

hessian_columns = []
for i in range(4):
    for j in range(4):
        theta = sp.zeros(4)
        theta[i, j] = 1
        hessian_columns.append(sp.Matrix([
            g.v[0] for g in solder_gradient_jet(owner.role0j, theta)]))
Htheta = sp.Matrix.hstack(*hessian_columns)
vec_theta0 = vec(owner.ETA)
check('SOLDER_HESSIAN_SYMMETRIC', Htheta == Htheta.T)
check('SOLDER_HESSIAN_RANK_6_NULLITY_10', Htheta.rank() == 6)
check('BASE_SOLDER_IS_LEFT_AND_RIGHT_HESSIAN_NULL',
      Htheta * vec_theta0 == sp.zeros(16, 1)
      and vec_theta0.T * Htheta == sp.zeros(1, 16))
L = sp.Matrix.vstack(*[v.T for v in Htheta.T.nullspace()])
check('EXACT_COKERNEL_DIMENSION_10', L.shape == (10, 16) and L * Htheta == sp.zeros(10, 16))

columns, missing_columns, base_directional_euler = {}, {}, {}
for label, direction in [('K1', owner.K1), ('N2', owner.N2), ('N3', owner.N3)]:
    for q in range(4):
        name = f'{label}_{q}'
        gens = [owner.MJet(a, direction if r == q else sp.zeros(4))
                for r, a in enumerate(owner.generators0)]
        links = [owner.cayley_jet(a) for a in gens]
        columns[name] = sp.Matrix([
            g.d[0] for g in solder_gradient_jet(links, owner.ETA)])
        missing_columns[name] = sp.Matrix([
            owner.d_star_jet(links, gens, r, test)[1]
            for r in range(4) for test in (owner.N2, owner.N3)])
        base_directional_euler[name] = owner.d_star_jet(
            owner.role0j, owner.generators0j, q, direction)[0]

Jall = sp.Matrix.hstack(*columns.values())
check('TWELVE_NORMAL_SOLDER_MIXED_RANK_11', Jall.rank() == 11)
check('TWELVE_NORMAL_SOLDER_COKERNEL_RANK_6', (L * Jall).rank() == 6)
expected_solder_ranks = (6, 6, 6, 6, 6, 7, 7, 7)
expected_projected_ranks = (5, 6, 6, 5, 5, 4, 6, 6)
expected_obstructions = (
    -sp.Rational(4992, 67), sp.Rational(4992, 1055),
    -sp.Rational(14976, 47), sp.Rational(7296, 7), sp.Integer(1872),
    sp.Rational(16768, 13), sp.Rational(49920, 67),
    -sp.Rational(99840, 427))

for index, support in enumerate(owner.MINIMUM_SUPPORTS):
    JM = sp.Matrix.hstack(*[missing_columns[k] for k in support])
    JS = sp.Matrix.hstack(*[columns[k] for k in support])
    check(f'SUPPORT_{index}_MISSING_JACOBIAN_RANK_7', JM.rank() == 7)
    solutions = list(sp.linsolve((JM, -owner.base_missing)))
    check(f'SUPPORT_{index}_STAR_MISSING_NEWTON_VECTOR_UNIQUE', len(solutions) == 1)
    correction = sp.Matrix(solutions[0])
    check(f'SUPPORT_{index}_NEWTON_EQUATION', JM * correction == -owner.base_missing)
    scale_obstruction = (vec_theta0.T * JS * correction)[0]
    action_first = sum(base_directional_euler[k] * correction[j]
                       for j, k in enumerate(support))
    check(f'SUPPORT_{index}_QUADRATIC_SOLDER_HOMOGENEITY',
          scale_obstruction == 2 * action_first)
    check(f'SUPPORT_{index}_EXACT_SCALE_COKERNEL_OBSTRUCTION',
          scale_obstruction == expected_obstructions[index] != 0)
    check(f'SUPPORT_{index}_NO_FIRST_SOLDER_LIFT_FOR_THIS_VECTOR',
          sp.Matrix.hstack(Htheta, JS * correction).rank() == 7)
    check(f'SUPPORT_{index}_SOLDER_MIXED_RANK',
          JS.rank() == expected_solder_ranks[index])
    check(f'SUPPORT_{index}_SOLDER_COKERNEL_RANK',
          (L * JS).rank() == expected_projected_ranks[index])
    print('SUPPORT', index, support, 'SCALE_OBSTRUCTION', str(scale_obstruction),
          'PROJECTED_RANK', (L * JS).rank())
    if index == 5:
        check('SELECTED_VECTOR_AGREES_WITH_OWNER',
              correction == sp.Matrix(owner.EXPECTED_V))
        selected_JS = JS

# Exact reduction of the selected seven amplitudes at the solder tangent gate.
# x = (-4*z3, z1, -z3, z2, z2, 0, z3) is necessary and sufficient for a
# first-order solder lift. It does not solve link/affine stationarity.
Kreduced = sp.Matrix([
    [0, 0, -4], [1, 0, 0], [0, 0, -1], [0, 1, 0],
    [0, 1, 0], [0, 0, 0], [0, 0, 1]])
reduced_equations = sp.Matrix([
    [1, 0, 0, 0, 0, 0, 4], [0, 0, 1, 0, 0, 0, 1],
    [0, 0, 0, 1, -1, 0, 0], [0, 0, 0, 0, 0, 1, 0]])
projected = L * selected_JS
check('SELECTED_SOLDER_PROJECTED_RANK_4_KERNEL_3', projected.rank() == 4)
check('REDUCED_EQUATIONS_HAVE_IDENTICAL_ROWSPACE',
      sp.Matrix.vstack(projected, reduced_equations).rank() == 4
      and reduced_equations.rank() == 4)
check('THREE_PARAMETER_KERNEL_IS_COMPLETE',
      Kreduced.rank() == 3 and projected * Kreduced == sp.zeros(10, 3))
lift, parameters = Htheta.gauss_jordan_solve(-selected_JS * Kreduced)
lift = lift.subs({p: 0 for p in parameters})
check('EXACT_FREE_SOLDER_LIFT_OF_REDUCED_KERNEL',
      Htheta * lift + selected_JS * Kreduced == sp.zeros(16, 3))
print('REDUCED_AMPLITUDE_EQUATIONS', 'x0+4*x6=0; x2+x6=0; x3-x4=0; x5=0')
print('REDUCED_AMPLITUDE_PARAMETERIZATION', '(-4*z3,z1,-z3,z2,z2,0,z3)')
print('SOLDER_LIFT_MATRIX_ROW_MAJOR', lift.tolist())
print('SELECTED_NEWTON_REDUCED_DEFECT',
      [str(x) for x in reduced_equations * sp.Matrix(owner.EXPECTED_V)])
print('SCOPE: eight supplied star-only missing-Euler Newton vectors, not all finite support points')
print('STATUS: full finite active-residual stationary closure remains IN_PROGRESS')
