#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=900
"""Exact degree-two reduced metric phase-readout defect in the Y normal jet.

The check expands the literal phase-resolved Euler map through delta^2 for
the surviving R=-kappa beta tensor beta normal jet, using the pinned first
connection tangent from the normal-jet owner. It retains all 96 connection
rows, all 40 metric rows, the free degree-four Y correction, and an arbitrary
phase-common metric source. The degree-three equations force the degree-four
kernel correction to zero. After exact range elimination, a rational left
witness isolates the xi_3^2 coefficient and proves that no formal smooth
second connection normal jet has an exactly phase-common metric readout on
this slice. The 96 connection equations themselves are solved through the
same degree-four Taylor order.

This is a finite normal-jet result, not a connection no-go or a uniform
refinement theorem. It also extracts the exact zero-momentum connection
cokernel source for a constant-center seed and verifies its cancellation by
the spatially varying center jet in the connection-only solution.
"""
from __future__ import annotations

import argparse
import functools
import itertools
import json
import math
from pathlib import Path

import sympy as sp
from sympy.polys.domains import QQ
from sympy.polys.matrices import DomainMatrix

import a4d_y_curved_normaljet_compatibility_check as C
import a4d_y_curved_response_quotient_check as B

ROOT = Path(__file__).resolve().parents[3]
RESULT_PATH = ROOT / "02_REGISTRY/research/certificates/a4d_y_curved_normaljet_degree2_obstruction_results.json"
XI = sp.symbols("xi0:4")
I4, ETA, G2, STAR, GEN, PAIRS = B.I4, B.ETA, B.G2, B.STAR, B.GEN, B.PAIRS


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def rank_exact(matrix: sp.Matrix) -> int:
    return DomainMatrix.from_Matrix(matrix).convert_to(QQ).rank()


def matrix_json(matrix: sp.Matrix) -> list[list[str]]:
    return [[str(sp.factor(matrix[i, j])) for j in range(matrix.cols)]
            for i in range(matrix.rows)]


def smul(left, right):
    out = []
    for degree in range(3):
        value = sp.zeros(left[0].rows, right[0].cols)
        for k in range(degree + 1):
            value += left[k] * right[degree - k]
        out.append(value.applyfunc(sp.expand))
    return out


def sadd(left, right):
    return [(left[i] + right[i]).applyfunc(sp.expand) for i in range(3)]


def sscale(series, scalar):
    return [(value * scalar).applyfunc(sp.expand) for value in series]


def slinv(series):
    return [ETA * value.T * ETA for value in series]


def shift_expr(expr, offset):
    return sp.expand(expr.subs(
        {XI[i]: XI[i] + offset[i] for i in range(4)}, simultaneous=True
    ))


def wedge(left: sp.Matrix, right: sp.Matrix) -> sp.Matrix:
    return sp.Matrix([
        sp.expand(left[a] * right[b] - left[b] * right[a])
        for a, b in PAIRS
    ])


def bivector(matrix: sp.Matrix) -> sp.Matrix:
    dressed = matrix * ETA
    return sp.Matrix([sp.expand(dressed[a, b]) for a, b in PAIRS])


def pairing_delta2(area, curvature) -> sp.Expr:
    return sp.expand(sum(
        (area[k].T * G2 * STAR * bivector(curvature[2 - k]))[0]
        for k in range(3)
    ))


def run(write: bool = False, first_center_shift=sp.Integer(0), coker_only: bool = False) -> dict:
    owner = json.loads(C.RESULT_PATH.read_text())["normalized_surviving_curvature"]
    check("OWNER_HAS_LINEAR_FIRST_CONNECTION_TANGENT",
          json.loads(C.RESULT_PATH.read_text())["normal_jet"]["surviving_first_connection_tangent_degree"] == 1)

    a0 = {
        tuple(map(int, label.split(":"))): sp.Rational(value)
        for label, value in owner["first_connection_tangent_constant_nonzero"].items()
    }
    # A free order-delta shift along the exact flat Y family is an admissible
    # first tangent.  Keep it explicit when probing the nonlinear cokernel.
    for label, value in {
        (0, 0, 3): sp.Rational(4, 7),
        (0, 0, 4): sp.Rational(-4, 7),
        (0, 0, 5): sp.Rational(4, 7),
        (2, 0, 3): sp.Rational(-4, 7),
        (2, 0, 4): sp.Rational(4, 7),
        (2, 0, 5): sp.Rational(-4, 7),
    }.items():
        a0[label] = a0.get(label, 0) + first_center_shift * value
    linear = {
        direction: {
            tuple(map(int, label.split(":"))): sp.Rational(value)
            for label, value in owner["first_connection_tangent_linear_nonzero"][f"xi{direction}"].items()
        }
        for direction in range(4)
    }

    # Exact geodesic-normal Gram coframe on the normalized surviving product.
    n = sp.ones(3, 1)
    p_perp = sp.eye(3) - n * n.T / 3
    xi_spatial = sp.Matrix([XI[1], XI[2], XI[3]])
    x = p_perp * xi_spatial
    r2 = sp.expand((x.T * x)[0])
    T = (r2 * p_perp - x * x.T).applyfunc(sp.expand)
    U0, V0 = sp.zeros(4), sp.zeros(4)
    U0[1:4, 1:4] = -T / 2
    V0[1:4, 1:4] = 3 * r2 * T / 40
    q1, q2 = sp.zeros(4), sp.zeros(4)
    q1[1:4, 1:4] = T
    q2[1:4, 1:4] = -sp.Rational(2, 5) * r2 * T
    check("NORMAL_GRAM_FIRST_COEFFICIENT",
          U0.T * ETA + ETA * U0 == q1)
    check("NORMAL_GRAM_SECOND_COEFFICIENT",
          all(sp.factor(v) == 0 for v in (V0.T * ETA + ETA * V0 + U0.T * ETA * U0 - q2)))
    owner_hessian = owner["normal_metric_hessian_nonzero"]
    q_from_owner = sp.zeros(4)
    for i in range(4):
        for j in range(i, 4):
            entries = owner_hessian.get(f"d{i}d{j}", ["0"] * 10)
            coefficient = sp.Rational(1, 2) if i == j else sp.Integer(1)
            factor = coefficient * XI[i] * XI[j]
            for metric_index, (qa, qb) in enumerate(B.SYM):
                value = sp.Rational(entries[metric_index]) * factor
                q_from_owner[qa, qb] += value
                if qa != qb:
                    q_from_owner[qb, qa] += value
    check("METRIC_TAYLOR_MATCHES_PINNED_NORMAL_JET",
          all(sp.factor(v) == 0 for v in (q_from_owner - q1)))

    @functools.lru_cache(None)
    def solder_series(offset):
        U = U0.applyfunc(lambda e: shift_expr(e, offset))
        V = V0.applyfunc(lambda e: shift_expr(e, offset))
        return [I4, U, V]

    @functools.lru_cache(None)
    def connection_matrix(phase, role, offset):
        coefficients = dict(a0)
        for direction in range(4):
            for label, value in linear[direction].items():
                coefficients[label] = coefficients.get(label, 0) + value * (XI[direction] + offset[direction])
        result = sp.zeros(4)
        for (p, r, generator), value in coefficients.items():
            if p == phase and r == role and value:
                result += value * GEN[generator]
        return result.applyfunc(sp.expand)

    Y = B.cayley_Y(sp.Integer(1))
    wave = [Y, I4, ETA * Y.T * ETA, I4]

    @functools.lru_cache(None)
    def link_series(phase, role, offset):
        base = wave[phase] if role == 0 else I4
        tangent = connection_matrix(phase, role, offset)
        return [
            base,
            (base * tangent).applyfunc(sp.expand),
            (base * tangent * tangent / 2).applyfunc(sp.expand),
        ]

    def area_series_from_solder(solder, a, b):
        u, v = [j for j in range(4) if j not in (a, b)]
        ca = [sp.Matrix(solder[k][:, u]) for k in range(3)]
        cb = [sp.Matrix(solder[k][:, v]) for k in range(3)]
        out = [sp.zeros(6, 1) for _ in range(3)]
        for degree in range(3):
            for k in range(degree + 1):
                out[degree] += wedge(ca[k], cb[degree - k])
        return out

    @functools.lru_cache(None)
    def face_core(phase, a, b, base_offset):
        shifts = [
            base_offset,
            tuple(base_offset[i] + int(i == a) for i in range(4)),
            tuple(base_offset[i] + int(i == b) for i in range(4)),
            base_offset,
        ]
        locations = [
            (phase, a, False),
            ((phase + 1) % 4, b, False),
            ((phase + 1) % 4, a, True),
            (phase, b, True),
        ]
        factors = []
        for (p, role, inverse), offset in zip(locations, shifts):
            link = link_series(p, role, offset)
            factors.append(slinv(link) if inverse else link)
        plaquette = [I4, sp.zeros(4), sp.zeros(4)]
        for factor in factors:
            plaquette = smul(plaquette, factor)
        inverse = slinv(plaquette)
        curvature = sscale(sadd(plaquette, sscale(inverse, -1)), sp.Rational(1, 2))
        area = area_series_from_solder(solder_series(base_offset), a, b)
        return locations, shifts, factors, plaquette, curvature, area

    @functools.lru_cache(None)
    def curvature_variation(phase, a, b, base_offset, corner, generator):
        _locations, _shifts, factors, plaquette, curvature, area = face_core(
            phase, a, b, base_offset
        )
        varied = (
            sscale(smul([GEN[generator], sp.zeros(4), sp.zeros(4)], factors[corner]), -1)
            if corner in (2, 3)
            else smul(factors[corner], [GEN[generator], sp.zeros(4), sp.zeros(4)])
        )
        dplaquette = [I4, sp.zeros(4), sp.zeros(4)]
        for i, factor in enumerate(factors):
            dplaquette = smul(dplaquette, varied if i == corner else factor)
        pinv = slinv(plaquette)
        dc = sscale(sadd(dplaquette, smul(smul(pinv, dplaquette), pinv)), sp.Rational(1, 2))
        return area, dc

    @functools.lru_cache(None)
    def area_metric_series(a, b, qa, qb):
        solder = solder_series((0, 0, 0, 0))
        dq = sp.zeros(4)
        dq[qa, qb] = dq[qb, qa] = 1
        u0 = dq / 2
        u1 = -(u0 * U0 + U0 * u0) / 2
        u2 = -(u1 * U0 + U0 * u1 + u0 * V0 + V0 * u0) / 2
        ds = [ETA * u0, ETA * u1, ETA * u2]
        u, v = [j for j in range(4) if j not in (a, b)]
        out = [sp.zeros(6, 1) for _ in range(3)]
        for degree in range(3):
            for k in range(degree + 1):
                out[degree] += wedge(ds[k][:, u], solder[degree - k][:, v])
                out[degree] += wedge(solder[k][:, u], ds[degree - k][:, v])
        if ds[0] != B.metric_lift(qa, qb):
            raise AssertionError(f"wrong Gram derivative for q{qa}{qb}")
        return out

    # Full coefficient of delta^2 in all 136 literal Euler rows.
    forcing_connection = [sp.Integer(0)] * 96
    forcing_metric = [sp.Integer(0)] * 40
    zero = (0, 0, 0, 0)
    for phase in range(4):
        for role in range(4):
            for generator in range(6):
                value = 0
                for a, b in PAIRS:
                    if role == a:
                        contexts = [(phase, 0, zero), ((phase - 1) % 4, 2,
                                    tuple(-int(i == b) for i in range(4)))]
                    elif role == b:
                        contexts = [((phase - 1) % 4, 1,
                                    tuple(-int(i == a) for i in range(4))), (phase, 3, zero)]
                    else:
                        continue
                    for base_phase, corner, base_offset in contexts:
                        area, dcurv = curvature_variation(
                            base_phase, a, b, base_offset, corner, generator
                        )
                        value += B.orientation(a, b) * pairing_delta2(area, dcurv)
                forcing_connection[(phase * 4 + role) * 6 + generator] = sp.expand(value)

        for metric_index, (qa, qb) in enumerate(B.SYM):
            value = 0
            for a, b in PAIRS:
                _loc, _shifts, _factors, _plaq, curvature, _area = face_core(
                    phase, a, b, zero
                )
                darea = area_metric_series(a, b, qa, qb)
                value += B.orientation(a, b) * pairing_delta2(darea, curvature)
            forcing_metric[phase * 10 + metric_index] = sp.expand(value)
    print("BUILT_EXACT_DELTA2_EULER_POLYNOMIAL", flush=True)

    forcing_polys = [sp.Poly(value, *XI) for value in forcing_connection + forcing_metric]
    degree4 = [tuple(exponents) for exponents in __import__("itertools").product(range(5), repeat=4)
               if sum(exponents) == 4]
    check("DEGREE_FOUR_FORCE_VANISHES_IDENTICALLY",
          all(poly.coeff_monomial(sp.prod(XI[i] ** exponents[i] for i in range(4))) == 0
              for poly in forcing_polys for exponents in degree4))

    # Frozen joint range and common-source cokernel.
    H, labels, faces0 = B.action_connection_hessian(sp.Integer(1))
    faces = C.with_base_phases(faces0)
    A1, A2, _M0, _M1, _M2, C0, C1, C2, _Dphase = C.blocks_all(H, faces, labels)
    joint = H.col_join(C0)
    common = sp.zeros(136, 10)
    for phase in range(4):
        common[96 + 10 * phase:96 + 10 * (phase + 1), :] = sp.eye(10)
    base = joint.row_join(common)
    left = DomainMatrix.from_Matrix(base.T).convert_to(QQ).nullspace().to_Matrix()
    kernel = DomainMatrix.from_Matrix(base).convert_to(QQ).nullspace().to_Matrix()
    check("FROZEN_CONNECTION_RANK_94", rank_exact(H) == 94)
    check("FROZEN_JOINT_RANK_95", rank_exact(joint) == 95)
    check("COMMON_SOURCE_RANGE_RANK_105", rank_exact(base) == 105)
    check("JOINT_COMMON_SOURCE_COKERNEL_31", left.shape == (31, 136))
    check("JOINT_KERNEL_DIMENSION_ONE", kernel.shape == (1, 106))

    degree4 = [tuple(e) for e in itertools.product(range(5), repeat=4) if sum(e) == 4]
    degree3 = [tuple(e) for e in itertools.product(range(4), repeat=4) if sum(e) == 3]
    degree2 = [tuple(e) for e in itertools.product(range(3), repeat=4) if sum(e) == 2]
    i4 = {e: k for k, e in enumerate(degree4)}
    i3 = {e: k for k, e in enumerate(degree3)}
    u = sp.Matrix(kernel[0, :]).T
    uc = u[:96, :]
    check("FREE_JOINT_KERNEL_IS_PURE_Y", {
        i: uc[i] for i in range(96) if uc[i]
    } == {3: -1, 4: 1, 5: -1, 51: 1, 52: -1, 53: 1})
    check("FREE_JOINT_KERNEL_HAS_NO_COMMON_SOURCE", all(u[96 + i] == 0 for i in range(10)))

    first_moments = [A1[i].col_join(C1[i]) for i in range(4)]
    second_moments = {
        ij: ((2 if ij[0] == ij[1] else 1) * A2[ij]).col_join(
            (2 if ij[0] == ij[1] else 1) * C2[ij]
        ) for ij in C.DIRPAIRS
    }
    monomial = lambda e: sp.prod(XI[i] ** e[i] for i in range(4))

    def force_coeff(exponent):
        expr = monomial(exponent)
        return sp.Matrix([poly.coeff_monomial(expr) for poly in forcing_polys])

    # First answer the physical branch question: can the 96 connection
    # equations themselves be solved through this order, without imposing
    # phase equality on the metric readout?
    jet_monomials = [tuple(e) for e in itertools.product(range(5), repeat=4) if sum(e) <= 4]
    jet_monomials.sort(key=lambda e: (-sum(e), e))
    jet_index = {alpha: i for i, alpha in enumerate(jet_monomials)}
    shift_moments = {nu: sp.zeros(96) for nu in jet_monomials}
    for phase, a, b, locs, local, Hloc, factors in faces:
        shifts = [(0, 0, 0, 0), tuple(int(r == a) for r in range(4)),
                  tuple(int(r == b) for r in range(4)), (0, 0, 0, 0)]
        slot_shifts = []
        for position in range(4):
            slot_shifts += [shifts[position]] * 6
        for ii, (_pi, _gi, gi) in enumerate(local):
            for jj, (_pj, _gj, gj) in enumerate(local):
                difference = [slot_shifts[jj][r] - slot_shifts[ii][r] for r in range(4)]
                for nu in jet_monomials:
                    if not any(nu):
                        continue
                    coefficient = sp.prod(
                        sp.Rational(difference[r] ** nu[r], math.factorial(nu[r]))
                        for r in range(4)
                    )
                    if coefficient:
                        shift_moments[nu][gi, gj] += Hloc[ii, jj] * coefficient
    shift_moments[(0, 0, 0, 0)] = H
    check("CONNECTION_SHIFT_MOMENTS_MATCH_FIRST", all(
        shift_moments[tuple(int(i == r) for i in range(4))] == A1[r]
        for r in range(4)
    ))
    check("CONNECTION_SHIFT_MOMENTS_MATCH_SECOND", all(
        shift_moments[tuple(int(k == i) + int(k == j) for k in range(4))] == A2[(i, j)]
        for i, j in C.DIRPAIRS
    ))

    connection_left = DomainMatrix.from_Matrix(H.T).convert_to(QQ).nullspace().to_Matrix()
    connection_kernel = DomainMatrix.from_Matrix(H).convert_to(QQ).nullspace().to_Matrix().T
    check("CONNECTION_ONLY_KERNEL_AND_COKERNEL_ARE_TWO",
          connection_left.shape == (2, 96) and connection_kernel.shape == (96, 2))
    _, h_columns = H.rref()
    _, h_rows = H.T.rref()
    check("CONNECTION_RANGE_PIVOTS_94", len(h_columns) == len(h_rows) == 94)
    h_inverse = H.extract(list(h_rows), list(h_columns)).inv()
    h_range_inverse = sp.zeros(96)
    for i, column in enumerate(h_columns):
        for j, row in enumerate(h_rows):
            h_range_inverse[column, row] = h_inverse[i, j]
    check("CONNECTION_RANGE_RIGHT_INVERSE", H * h_range_inverse * H == H)

    center_count = connection_kernel.cols * len(jet_monomials)
    center_column = lambda alpha, mode: connection_kernel.cols * jet_index[alpha] + mode
    connection_jets = {}
    cokernel_equations = []
    processed_degree = None
    for gamma in jet_monomials:
        degree = sum(gamma)
        if processed_degree is not None and degree != processed_degree:
            print("BUILT_CONNECTION_JET_COEFFICIENTS_DEGREE", processed_degree, flush=True)
        processed_degree = degree

        rhs = sp.zeros(96, center_count + 1)
        rhs[:, 0] = -sp.Matrix([poly.coeff_monomial(monomial(gamma))
                                for poly in forcing_polys[:96]])
        for nu in jet_monomials:
            if not any(nu):
                continue
            alpha = tuple(gamma[r] + nu[r] for r in range(4))
            if alpha not in connection_jets:
                continue
            derivative_factor = sp.prod(
                math.factorial(alpha[r]) // math.factorial(gamma[r]) for r in range(4)
            )
            rhs -= derivative_factor * shift_moments[nu] * connection_jets[alpha]

        left_equations = connection_left * rhs
        for row in range(connection_left.rows):
            cokernel_equations.append(left_equations[row, :])

        correction = h_range_inverse * rhs
        for mode in range(connection_kernel.cols):
            correction[:, 1 + center_column(gamma, mode)] += connection_kernel[:, mode]
        connection_jets[gamma] = correction
    print("BUILT_CONNECTION_JET_COEFFICIENTS_DEGREE", processed_degree, flush=True)

    connection_equations = sp.Matrix.vstack(*cokernel_equations)
    if coker_only:
        zero_multi = (0, 0, 0, 0)
        zero_row = 2 * jet_index[zero_multi]
        projected_source = sp.Matrix([
            sp.factor(connection_equations[zero_row + row, 0])
            for row in range(connection_left.rows)
        ])
        check("SYMBOLIC_CENTER_SHIFT_C2_IS_AT_MOST_QUADRATIC",
              all(sp.Poly(value, first_center_shift).degree() <= 2
                  for value in projected_source))
        if first_center_shift == sp.Symbol("s"):
            check("FREE_FIRST_ORDER_Y_SHIFT_LEAVES_C2_UNCHANGED",
                  projected_source == sp.Matrix([
                      sp.Rational(351402359, 2108160),
                      sp.Rational(21506403637, 154949760),
                  ]))
        print("FIRST_CENTER_SHIFT", first_center_shift, flush=True)
        print("ZERO_MODE_C2", [sp.factor(value) for value in projected_source], flush=True)
        return {"center_shift": str(first_center_shift),
                "zero_mode_c2": [str(sp.factor(value)) for value in projected_source]}

    connection_matrix = connection_equations[:, 1:]
    connection_rhs = -connection_equations[:, 0]
    connection_rank = rank_exact(connection_matrix)
    connection_augmented_rank = rank_exact(connection_matrix.row_join(connection_rhs))
    check("CONNECTION_ONLY_JET_REDUCED_RANK_30", connection_rank == 30)
    check("CONNECTION_ONLY_JET_AUGMENTED_RANK_30", connection_augmented_rank == 30)
    _, center_columns = connection_matrix.rref()
    _, center_rows = connection_matrix.T.rref()
    center_values = sp.zeros(center_count, 1)
    if connection_rank:
        center_square = connection_matrix.extract(list(center_rows), list(center_columns))
        center_solution = center_square.inv() * connection_rhs[list(center_rows), :]
        for index, column in enumerate(center_columns):
            center_values[column] = center_solution[index]
    check("CONNECTION_ONLY_JET_CENTER_SOLUTION", connection_matrix * center_values == connection_rhs)

    # Isolate the zero-normal-momentum connection cokernel equation.  Its
    # constant-center columns must vanish (a constant kernel shift is still
    # in ker H); any cancellation can only come from spatially varying center
    # coefficients transported into the constant equation by the shift
    # moments.  This is the exact quadratic Lyapunov--Schmidt coefficient on
    # the stationary/constant-center seed for this prescribed normal jet.
    zero_multi = (0, 0, 0, 0)
    zero_block = connection_equations[
        2 * jet_index[zero_multi]:2 * (jet_index[zero_multi] + 1), :
    ]
    zero_source = zero_block[:, 0]
    zero_center_map = zero_block[:, 1:]
    constant_center_columns = [center_column(zero_multi, mode)
                               for mode in range(connection_kernel.cols)]
    check("ZERO_MODE_CONSTANT_CENTER_COLUMNS_VANISH",
          all(zero_center_map[:, column] == sp.zeros(2, 1)
              for column in constant_center_columns))
    zero_center_only = zero_source + sum(
        (zero_center_map[:, column] * center_values[column]
         for column in constant_center_columns), sp.zeros(2, 1)
    )
    check("ZERO_MODE_CONSTANT_SEED_PROJECTED_SOURCE_EXACT",
          zero_center_only == zero_source)
    positive_center_columns = [column for alpha in jet_monomials if sum(alpha) > 0
                               for mode in range(connection_kernel.cols)
                               for column in [center_column(alpha, mode)]]
    zero_mode_transport = zero_center_map[:, positive_center_columns] * \
        center_values[positive_center_columns, :]
    check("ZERO_MODE_TRANSPORT_CANCELLED_BY_FULL_CENTER_JET",
          zero_source + zero_mode_transport == sp.zeros(2, 1))
    print("CONSTANT_CENTER_COKERNEL_SOURCE", list(zero_source), flush=True)
    print("SPATIALLY_VARYING_CENTER_TRANSPORT", list(zero_mode_transport), flush=True)

    nonzero_center_coefficients = []
    for alpha in jet_monomials:
        for mode in range(connection_kernel.cols):
            value = center_values[center_column(alpha, mode)]
            if value:
                nonzero_center_coefficients.append({
                    "monomial": list(alpha), "kernel_basis_index": mode, "coefficient": str(value)
                })

    for gamma in jet_monomials:
        value = connection_jets[gamma][:, 0] + connection_jets[gamma][:, 1:] * center_values
        residual = H * value + sp.Matrix([
            poly.coeff_monomial(monomial(gamma)) for poly in forcing_polys[:96]
        ])
        for nu in jet_monomials:
            if not any(nu):
                continue
            alpha = tuple(gamma[r] + nu[r] for r in range(4))
            if alpha not in connection_jets:
                continue
            derivative_factor = sp.prod(
                math.factorial(alpha[r]) // math.factorial(gamma[r]) for r in range(4)
            )
            shifted_value = connection_jets[alpha][:, 0] + connection_jets[alpha][:, 1:] * center_values
            residual += derivative_factor * shift_moments[nu] * shifted_value
        if residual != sp.zeros(96, 1):
            raise AssertionError(f"connection jet residual at {gamma}")
    check("ALL_96_CONNECTION_ROWS_SOLVED_THROUGH_DEGREE_FOUR", True)

    # The degree-three equations solve for the only free degree-four center jet.
    reduced3 = sp.zeros(31 * len(degree3), len(degree4))
    rhs3 = sp.zeros(31 * len(degree3), 1)
    for block, gamma in enumerate(degree3):
        rhs3[31 * block:31 * (block + 1), :] = left * force_coeff(gamma)
        for direction in range(4):
            alpha = list(gamma)
            alpha[direction] += 1
            alpha = tuple(alpha)
            reduced3[31 * block:31 * (block + 1), i4[alpha]] += (
                alpha[direction] * left * first_moments[direction] * uc
            )
    rank3 = rank_exact(reduced3)
    augmented3 = rank_exact(reduced3.row_join(rhs3))
    check("DEGREE3_REDUCED_RANK_35", rank3 == 35)
    check("DEGREE3_AUGMENTED_RANK_35", augmented3 == 35)
    _, pivot_rows3 = reduced3.T.rref()
    top3 = reduced3.extract(list(pivot_rows3), list(range(len(degree4))))
    degree4_center = top3.inv() * (-rhs3[list(pivot_rows3), :])
    check("DEGREE4_CENTER_CORRECTION_IS_ZERO", degree4_center == sp.zeros(len(degree4), 1))
    check("DEGREE3_EQUATION_SOLVED_EXACTLY", reduced3 * degree4_center == -rhs3)

    # Fix a range representative at degree three. Its arbitrary kernel part
    # remains as 20 free coefficients in the next reduced equation.
    _, pivot_columns = base.rref()
    _, pivot_rows = base.T.rref()
    check("BASE_RANGE_PIVOTS_105", len(pivot_columns) == len(pivot_rows) == 105)
    range_square = base.extract(list(pivot_rows), list(pivot_columns))
    range_inverse = range_square.inv()

    def solve_base(target):
        values = range_inverse * target[list(pivot_rows), :]
        solution = sp.zeros(base.cols, target.cols)
        for index, column in enumerate(pivot_columns):
            solution[column, :] = values[index, :]
        if base * solution != target:
            raise AssertionError("range representative failed exact reconstruction")
        return solution

    degree3_particular = {}
    for gamma in degree3:
        forcing = force_coeff(gamma)
        for direction in range(4):
            alpha = list(gamma)
            alpha[direction] += 1
            alpha = tuple(alpha)
            forcing += alpha[direction] * first_moments[direction] * uc * degree4_center[i4[alpha]]
        degree3_particular[gamma] = solve_base(-forcing)

    # Degree two after range elimination: 20 free degree-three center
    # coefficients try to absorb the effective forcing.
    reduced2 = sp.zeros(31 * len(degree2), len(degree3))
    rhs2 = sp.zeros(31 * len(degree2), 1)
    for block, gamma in enumerate(degree2):
        forcing = force_coeff(gamma)
        for direction in range(4):
            alpha = list(gamma)
            alpha[direction] += 1
            alpha = tuple(alpha)
            forcing += alpha[direction] * first_moments[direction] * degree3_particular[alpha][:96, :]

        for alpha in degree4:
            nu = tuple(alpha[i] - gamma[i] for i in range(4))
            if any(value < 0 for value in nu) or sum(nu) != 2:
                continue
            factor = sp.prod(sp.binomial(alpha[i], gamma[i]) for i in range(4))
            if 2 in nu:
                direction = nu.index(2)
                moment = second_moments[(direction, direction)]
            else:
                directions = [i for i, value in enumerate(nu) if value]
                moment = second_moments[tuple(directions)]
            forcing += factor * moment * uc * degree4_center[i4[alpha]]

        rhs2[31 * block:31 * (block + 1), :] = left * forcing
        for direction in range(4):
            alpha = list(gamma)
            alpha[direction] += 1
            alpha = tuple(alpha)
            reduced2[31 * block:31 * (block + 1), i3[alpha]] += (
                alpha[direction] * left * first_moments[direction] * uc
            )

    rank2 = rank_exact(reduced2)
    augmented2 = rank_exact(reduced2.row_join(rhs2))
    check("DEGREE2_REDUCED_RANK_20", rank2 == 20)
    check("DEGREE2_AUGMENTED_RANK_21", augmented2 == 21)

    # Select a sparse exact left witness for the incompatible reduced RHS.
    reduced2_rref, pivots2 = reduced2.T.rref()
    check("DEGREE2_LEFT_WITNESS_DIMENSION", len(pivots2) == rank2)
    best = None
    for free in (j for j in range(reduced2.rows) if j not in pivots2):
        candidate = sp.zeros(reduced2.rows, 1)
        candidate[free] = 1
        for row, pivot in enumerate(pivots2):
            candidate[pivot] = -reduced2_rref[row, free]
        pairing = sp.cancel((candidate.T * rhs2)[0])
        if pairing:
            support = sum(value != 0 for value in candidate)
            if best is None or support < best[0]:
                best = (support, candidate, pairing)
    if best is None:
        raise AssertionError("rank jump has no exact left witness")
    _, weights, _ = best
    first_nonzero = next(value for value in weights if value)
    if first_nonzero < 0:
        weights = -weights
    denominator = sp.ilcm(*[sp.denom(value) for value in weights if value])
    integer_weights = [int(value * denominator) for value in weights]
    divisor = math.gcd(*[abs(value) for value in integer_weights if value])
    integer_weights = [value // divisor for value in integer_weights]
    weights = sp.Matrix(integer_weights)
    integer_pairing = sp.cancel((weights.T * rhs2)[0])
    check("DEGREE2_WITNESS_ANNIHILATES_FREE_CENTER", reduced2.T * weights == sp.zeros(len(degree3), 1))
    check("DEGREE2_WITNESS_HAS_NONZERO_PAIRING", integer_pairing != 0)

    witness_by_monomial = []
    cokernel_weights = []
    for block, gamma in enumerate(degree2):
        coefficients = weights[31 * block:31 * (block + 1), :]
        witness = coefficients.T * left
        if witness != sp.zeros(1, 136):
            witness_by_monomial.append((gamma, witness))
            cokernel_weights.append({
                "monomial": list(gamma),
                "coefficients": [
                    [index, int(value)] for index, value in enumerate(coefficients) if value
                ],
            })
    check("OBSTRUCTION_IS_SINGLE_XI3_SQUARED", len(witness_by_monomial) == 1 and
          witness_by_monomial[0][0] == (0, 0, 0, 2))
    gamma, witness = witness_by_monomial[0]
    check("LEFT_WITNESS_ANNIHILATES_JOINT_AND_COMMON_RANGE",
          witness * base == sp.zeros(1, base.cols))
    check("LEFT_WITNESS_ANNIHILATES_ALL_FIRST_MOMENTS_OF_FREE_CENTER",
          all((witness * first_moments[i] * uc)[0] == 0 for i in range(4)))

    effective_forcing = force_coeff(gamma)
    for direction in range(4):
        alpha = list(gamma)
        alpha[direction] += 1
        alpha = tuple(alpha)
        effective_forcing += alpha[direction] * first_moments[direction] * degree3_particular[alpha][:96, :]
    check("REDUCED_AND_EULER_WITNESS_PAIRINGS_MATCH",
          (witness * effective_forcing)[0] == integer_pairing)

    # Lift the reduced witness to a primitive integer vector in the 136 Euler rows.
    denominator = sp.ilcm(*[sp.denom(value) for value in witness if value])
    integer_witness = [int(value * denominator) for value in witness]
    divisor = math.gcd(*[abs(value) for value in integer_witness if value])
    integer_witness = [value // divisor for value in integer_witness]
    lifted_witness = sp.Matrix([integer_witness])
    primitive_euler_pairing = (lifted_witness * effective_forcing)[0]
    check("PRIMITIVE_EULER_WITNESS_IS_NONZERO", primitive_euler_pairing != 0)

    # Evaluate the complete order-delta^2 metric response of the connection
    # solution, then separate its phase-common and phase-difference parts.
    metric_shift_moments = {nu: sp.zeros(40, 96) for nu in jet_monomials}
    label_index = {label: index for index, label in enumerate(labels)}
    unit = [I4[:, j] for j in range(4)]
    for phase, a, b, locations, local, Hloc, factors in faces:
        shifts = [(0, 0, 0, 0), tuple(int(r == a) for r in range(4)),
                  tuple(int(r == b) for r in range(4)), (0, 0, 0, 0)]
        ucol, vcol = [j for j in range(4) if j not in (a, b)]
        darea = []
        for qa, qb in B.SYM:
            dS = B.metric_lift(qa, qb)
            darea.append(B.wedge(dS[:, ucol], unit[vcol]) +
                         B.wedge(unit[ucol], dS[:, vcol]))
        for position, (phase_link, role, inverse) in enumerate(locations):
            offset = shifts[position]
            for generator_index, X in enumerate(GEN):
                varied_factor = -X * factors[position] if inverse else factors[position] * X
                dplaquette = I4
                for nfactor, factor in enumerate(factors):
                    dplaquette = dplaquette * (varied_factor if nfactor == position else factor)
                dcurvature = (dplaquette - B.linv(dplaquette)) / 2
                dcurv_biv = B.biv(dcurvature)
                connection_row = label_index[(phase_link, role, generator_index)]
                for metric_index, area_variation in enumerate(darea):
                    value = sp.cancel(B.orientation(a, b) *
                                      (area_variation.T * G2 * STAR * dcurv_biv)[0])
                    row = 10 * phase + metric_index
                    for nu in jet_monomials:
                        coefficient = sp.prod(
                            sp.Rational(offset[r] ** nu[r], math.factorial(nu[r]))
                            for r in range(4)
                        )
                        if coefficient:
                            metric_shift_moments[nu][row, connection_row] += coefficient * value

    check("METRIC_SHIFT_MOMENTS_MATCH_ZERO", metric_shift_moments[(0, 0, 0, 0)] == C0)
    check("METRIC_SHIFT_MOMENTS_MATCH_FIRST", all(
        metric_shift_moments[tuple(int(i == r) for i in range(4))] == C1[r]
        for r in range(4)
    ))
    check("METRIC_SHIFT_MOMENTS_MATCH_SECOND", all(
        metric_shift_moments[tuple(int(k == i) + int(k == j) for k in range(4))] == C2[(i, j)]
        for i, j in C.DIRPAIRS
    ))

    phase_common = sp.zeros(40, 10)
    for phase in range(4):
        phase_common[10 * phase:10 * (phase + 1), :] = sp.eye(10)
    phase_projector = phase_common * phase_common.T / 4
    metric_delta2 = {}
    phase_defect_delta2 = {}
    for gamma in jet_monomials:
        output = sp.Matrix([poly.coeff_monomial(monomial(gamma))
                            for poly in forcing_polys[96:]])
        for nu in jet_monomials:
            alpha = tuple(gamma[r] + nu[r] for r in range(4))
            if alpha not in connection_jets:
                continue
            derivative_factor = sp.prod(
                math.factorial(alpha[r]) // math.factorial(gamma[r]) for r in range(4)
            )
            correction = (connection_jets[alpha][:, 0] +
                         connection_jets[alpha][:, 1:] * center_values)
            output += derivative_factor * metric_shift_moments[nu] * correction
        metric_delta2[gamma] = output
        phase_defect_delta2[gamma] = (sp.eye(40) - phase_projector) * output

    metric_component_bound = max(
        sum(abs(metric_delta2[gamma][row]) for gamma in jet_monomials)
        for row in range(40)
    )
    phase_defect_bound = max(
        sum(abs(phase_defect_delta2[gamma][row]) for gamma in jet_monomials)
        for row in range(40)
    )
    phase_defect_nonzeros = sum(
        value != 0 for gamma in jet_monomials for value in phase_defect_delta2[gamma]
    )
    check("CONNECTION_METRIC_PHASE_DEFECT_IS_NONZERO", phase_defect_nonzeros > 0)
    check("METRIC_PHASE_DEFECT_CELL_BOUND_LT_11000", phase_defect_bound < 11000)
    xi3_squared = (0, 0, 0, 2)
    metric_coefficient_pairing = (
        sp.Matrix([integer_witness[96:]]) * phase_defect_delta2[xi3_squared]
    )[0]
    check("INTEGER_JOINT_WITNESS_DETECTS_CONNECTION_METRIC_DEFECT",
          metric_coefficient_pairing != 0)

    result = {
        "schema": "a4d-y-curved-normaljet-degree2-phase-readout-v1",
        "terminal": "A4D-Y-NORMALJET-DEGREE2-PHASE-READOUT-DEFECT",
        "scope": "normalized surviving Y curvature direction at z=1; exact delta^2 Euler normal jet; arbitrary phase-common metric source retained",
        "normal_jet_source": "a4d_y_curved_normaljet_compatibility_results.json",
        "forcing_degree_counts": {
            "degree4_nonzero_entries": 0,
            "degree3_nonzero_entries": sum(
                poly.coeff_monomial(monomial(e)) != 0 for poly in forcing_polys for e in degree3
            ),
            "degree2_nonzero_entries": sum(
                poly.coeff_monomial(monomial(e)) != 0 for poly in forcing_polys
                for e in itertools.product(range(3), repeat=4) if sum(e) == 2
            ),
            "degree1_nonzero_entries": sum(
                poly.coeff_monomial(monomial(e)) != 0 for poly in forcing_polys
                for e in itertools.product(range(2), repeat=4) if sum(e) == 1
            ),
            "degree0_nonzero_entries": sum(poly.coeff_monomial(1) != 0 for poly in forcing_polys),
        },
        "connection_only_jet": {
            "rows": 96,
            "normal_coordinate_monomials_through_degree_four": len(jet_monomials),
            "center_variables": center_count,
            "reduced_cokernel_matrix_shape": list(connection_matrix.shape),
            "reduced_rank": connection_rank,
            "augmented_rank": connection_augmented_rank,
            "compatible": connection_rank == connection_augmented_rank,
            "primitive_particular_center_coefficients": nonzero_center_coefficients,
            "all_connection_rows_solved_exactly": True,
            "constant_center_cokernel": {
                "left_kernel_basis_rows": matrix_json(connection_left),
                "left_kernel_row_order": "connection row=(phase*4+role)*6+generator",
                "stationary_seed_projected_source": [str(value) for value in zero_center_only],
                "constant_kernel_columns_vanish": True,
                "spatial_center_transport": [str(value) for value in zero_mode_transport],
                "full_center_jet_cancels_zero_mode": True,
                "stationary_seed_definition": "both center amplitudes have zero positive-degree normal-coordinate coefficients",
                "interpretation": "the projected source is nonzero, so the constant-center restriction fails at delta^2; allowing a spatially varying center jet cancels it on this finite normal jet",
            },
        },
        "metric_response_delta2": {
            "phase_difference_nonzero_coefficients": phase_defect_nonzeros,
            "componentwise_l1_bound_on_abs_xi_le_1": str(metric_component_bound),
            "phase_difference_l1_bound_on_abs_xi_le_1": str(phase_defect_bound),
            "verified_simple_phase_difference_bound": "11000",
            "normalization": "delta^2=kappa^2*h^4; bounds are for the coefficient at delta^2",
            "primitive_joint_witness_pairing_on_selected_coefficient": str(metric_coefficient_pairing),
        },
        "joint_dimensions": {
            "connection_hessian_rank": 94,
            "fixed_metric_joint_rank": 95,
            "rows": 136,
            "common_source_augmented_rank": 105,
            "common_source_cokernel_dimension": 31,
            "degree3_reduced_rank": rank3,
            "degree3_augmented_rank": augmented3,
            "degree4_center_kernel_correction": "0",
            "degree2_reduced_rank": rank2,
            "degree2_augmented_rank": augmented2,
        },
        "phase_common_obstruction": {
            "normal_coordinate_monomial": "xi3^2",
            "reduced_basis_primitive_pairing": str(integer_pairing),
            "primitive_euler_witness_pairing": str(primitive_euler_pairing),
            "reduced_left_witness_cokernel_weights": cokernel_weights,
            "primitive_integer_euler_left_witness_nonzero": [
                [row, value] for row, value in enumerate(integer_witness) if value
            ],
            "row_order": {
                "connection": "row=(phase*4+role)*6+generator, 0<=row<96",
                "metric": "row=96+phase*10+metric_index, metric order q00,q01,q02,q03,q11,q12,q13,q22,q23,q33",
            },
            "annihilations": {
                "joint_range": True,
                "common_phase_metric_source": True,
                "all_four_first_moments_of_free_center": True,
            },
        },
        "nonclaims": [
            "the phase-common metric readout condition fails at order delta^2, but this alone is not an obstruction to the 96 connection stationarity equations",
            "this finite normal-jet result does not prove an all-background continuation or a refinement-uniform nonlinear theorem",
        ],
    }
    if write:
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", RESULT_PATH, flush=True)
    else:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(RESULT_PATH.read_text()))
    print("PHASE_READOUT_PAIRING", integer_pairing, flush=True)
    print("TERMINAL", result["terminal"], flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    parser.add_argument("--first-center-shift", default="0",
                        help="exact rational value or 'symbolic' for the free first-order Y-family shift")
    parser.add_argument("--coker-only", action="store_true",
                        help="stop after extracting the exact zero-mode connection-cokernel polynomial")
    args = parser.parse_args()
    shift = sp.Symbol("s") if args.first_center_shift == "symbolic" else sp.Rational(args.first_center_shift)
    run(args.write, shift, args.coker_only)
