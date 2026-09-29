#!/usr/bin/env python3
# D0_CI_TIMEOUT_SECONDS=300
"""Exact degree-two reduced cokernel obstruction in the Y curved normal jet.

The check expands the literal phase-resolved Euler map through delta^2 for
the surviving R=-kappa beta tensor beta normal jet, using the pinned first
connection tangent from the normal-jet owner. It retains all 96 connection
rows, all 40 metric rows, the free degree-four Y correction, and an arbitrary
phase-common metric source. The degree-three equations force the degree-four
kernel correction to zero. After exact range elimination, a rational left
witness isolates the xi_3^2 coefficient and proves that no formal smooth
second connection normal jet solves this slice.

This is a finite normal-jet obstruction, not a global no-go or a uniform
refinement theorem.
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


def run(write: bool = False) -> dict:
    owner = json.loads(C.RESULT_PATH.read_text())["normalized_surviving_curvature"]
    check("OWNER_HAS_LINEAR_FIRST_CONNECTION_TANGENT",
          json.loads(C.RESULT_PATH.read_text())["normal_jet"]["surviving_first_connection_tangent_degree"] == 1)

    a0 = {
        tuple(map(int, label.split(":"))): sp.Rational(value)
        for label, value in owner["first_connection_tangent_constant_nonzero"].items()
    }
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

    result = {
        "schema": "a4d-y-curved-normaljet-degree2-obstruction-v1",
        "terminal": "A4D-Y-NORMALJET-DEGREE2-FREDHOLM-OBSTRUCTION",
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
        "obstruction": {
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
            "this is a finite formal normal-jet obstruction for the declared normalized curvature slice, not a no-go for every background or nonsmooth h-dependent sequence",
            "no all-background continuation or refinement-uniform nonlinear theorem is claimed",
        ],
    }
    if write:
        RESULT_PATH.write_text(json.dumps(result, indent=2) + "\n")
        print("WROTE", RESULT_PATH, flush=True)
    else:
        check("RESULTS_MATCH_PINNED_JSON", result == json.loads(RESULT_PATH.read_text()))
    print("OBSTRUCTION_PAIRING", integer_pairing, flush=True)
    print("TERMINAL", result["terminal"], flush=True)
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--write", action="store_true")
    run(parser.parse_args().write)
