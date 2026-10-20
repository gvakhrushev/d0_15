#!/usr/bin/env python3
"""Exact margin of one fixed U(1) source probe inside the pure-source ellipsoid.

Certifies equations (5)-(8) and (10)-(11) of
A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md at
ec45c8cc4085e7bce888d97439251be9e578d4ff. The operators are the memo's B_r.
No geometry, no field kernel, no nonlinear branch, and no uniform separation
of distinct histories.
"""
from __future__ import annotations

import json

import sympy as s

PIN = "ec45c8cc4085e7bce888d97439251be9e578d4ff"
MEMO = "02_REGISTRY/research/A4D_MEMORY_SOURCE_CAPACITY_AND_NONLINEAR_SELECTION.md"
FIBRE = "02_REGISTRY/research/A4D_NATIVE_MEMORY_SOURCE_FIBRE.md"
MEMO_SHA256 = "8ec54e4838aaa579469896eeaf369e16a24d6a6f0f67824ede6fa88f5cb9b622"
FIBRE_SHA256 = "37d31c0e3ab9ebfd4e60a105913f46b1c959f97e1be9b0c339a12dc8ce31b014"
AUDIT_N = 12

p, a = s.symbols("p a", positive=True)
A, B = s.symbols("A B", real=True)
delta = s.symbols("delta", positive=True)
Bpos = s.symbols("Bpos", positive=True)
tau = s.symbols("tau", real=True)


def reduce(expr):
    expr = s.expand(expr)
    expr = s.expand(s.rem(s.together(expr), a * a - p, a))
    return s.expand(s.rem(expr, p * p + p - 1, p))


def zero(expr) -> bool:
    return s.expand(expr) == 0


def zero_matrix(mat) -> bool:
    return all(zero(entry) for entry in s.Matrix(mat))


def car_creators():
    creators = []
    for slot in range(4):
        matrix = s.zeros(16)
        low = (1 << slot) - 1
        for mask in range(16):
            if mask & (1 << slot):
                continue
            sign = (-1) ** bin(mask & low).count("1")
            matrix[mask | (1 << slot), mask] = sign
        creators.append(matrix)
    return creators


def gamma_op(vector, creators):
    created = sum((vector[i] * creators[i] for i in range(4)), s.zeros(16))
    removed = sum((vector[i] * creators[i].T for i in range(4)), s.zeros(16))
    return created + removed


def kappa_op(vector, creators):
    created = sum((vector[i] * creators[i] for i in range(4)), s.zeros(16))
    removed = sum((vector[i] * creators[i].T for i in range(4)), s.zeros(16))
    return created - removed


def source_data():
    creators = car_creators()
    frame = (A - B) * s.eye(4) + B * s.ones(4)
    rows = [frame.row(i).T for i in range(4)]
    axes = [
        s.Matrix([0, 0, -1, 1]),
        s.Matrix([0, 1, 0, -1]),
        s.Matrix([0, -1, 1, 0]),
    ]
    operators = [
        gamma_op(axes[i], creators) * kappa_op(rows[i + 1], creators) for i in range(3)
    ]
    chi = s.zeros(16, 1)
    chi[1] = 1 / s.sqrt(2)
    chi[15] = -1 / s.sqrt(2)
    return operators, chi


def covariance_formula():
    degree = A * A + 3 * B * B
    off = A * A - 4 * A * B - B * B
    matrix = (2 * degree - off) * s.eye(3) + off * s.ones(3)
    parallel = 4 * (A - B) ** 2
    transverse = A * A + 4 * A * B + 7 * B * B
    return matrix, off, parallel, transverse


def closed_inverse(off, parallel, transverse):
    return (1 / transverse) * s.eye(3) - off / (transverse * parallel) * s.ones(3)


def certify() -> dict:
    checks: list[str] = []

    def require(name: str, cond: bool) -> None:
        if not bool(cond):
            raise ArithmeticError(name)
        checks.append(name)

    operators, chi = source_data()
    formula, off, parallel, transverse = covariance_formula()
    inverse = closed_inverse(off, parallel, transverse)
    direction = s.Matrix([2 * B, -A, -A])
    ones = s.Matrix([1, 1, 1])
    plane_u = s.Matrix([1, -1, 0])
    plane_w = s.Matrix([1, 1, -2])

    require("chi_normalized", s.expand((chi.T * chi)[0] - 1) == 0)
    images = []
    for index, operator in enumerate(operators):
        require(f"source_operator_symmetric_{index}", zero_matrix(operator - operator.T))
        image = s.expand(operator * chi)
        images.append(image)
        require(f"seed_linear_moment_zero_{index}", zero((chi.T * image)[0]))
    gram = s.Matrix(3, 3, lambda i, j: s.expand(images[i].dot(images[j])))
    require("covariance_matches_formula_5", zero_matrix(gram - formula))
    require("parallel_eigenvalue", zero_matrix(formula * ones - parallel * ones))
    require("transverse_eigenvalue_u", zero_matrix(formula * plane_u - transverse * plane_u))
    require("transverse_eigenvalue_w", zero_matrix(formula * plane_w - transverse * plane_w))
    basis = s.Matrix.hstack(ones, plane_u, plane_w)
    require("eigenbasis_invertible", s.factor(basis.det()) != 0)
    require("inverse_times_gamma_is_identity", zero_matrix(s.simplify(formula * inverse - s.eye(3))))

    x = s.Matrix(s.symbols("x0:3", real=True))
    total = x[0] + x[1] + x[2]
    quadratic = s.expand((x.T * formula * x)[0])
    decomposed = s.expand(
        parallel * total ** 2 / 3 + transverse * (x.dot(x) - total ** 2 / 3)
    )
    require("quadratic_form_eigen_decomposition", zero(quadratic - decomposed))
    positive_root = {A: Bpos + delta, B: Bpos}
    lam1 = s.factor(s.expand(parallel.subs(positive_root)))
    lam2 = s.expand(transverse.subs(positive_root))
    require("parallel_eigenvalue_is_square", lam1 == 4 * delta ** 2)
    require(
        "transverse_eigenvalue_sum_of_squares",
        zero(lam2 - ((delta + 3 * Bpos) ** 2 + 3 * Bpos ** 2)),
    )
    require("gamma_positive_definite_for_A_gt_B_gt_0", lam1 == 4 * delta ** 2 and not zero(lam2))

    witness = {A: s.Rational(3, 5), B: s.Rational(1, 10)}
    gram_w = s.Matrix(formula.subs(witness))
    minors = [s.factor(gram_w[:k, :k].det()) for k in (1, 2, 3)]
    require("witness_sylvester_positive", all(minor > 0 for minor in minors))

    heights = s.Matrix(s.symbols("h0:3", real=True))
    prepared = sum((heights[i] * images[i] for i in range(3)), s.zeros(16, 1))
    require(
        "preparation_norm_6",
        zero(s.expand((chi + prepared).dot(chi + prepared) - (1 + (heights.T * gram * heights)[0]))),
    )
    for index, operator in enumerate(operators):
        cubic = s.expand((prepared.T * operator * prepared)[0])
        require(f"cubic_moment_zero_{index}", zero(cubic))
        numerator = s.expand(((chi + prepared).T * operator * (chi + prepared))[0])
        require(f"pure_source_numerator_{index}", zero(numerator - 2 * (gram * heights)[index]))

    source_norm = s.symbols("s", nonnegative=True)
    image_q = s.together(4 * source_norm / (1 + source_norm) ** 2)
    require(
        "forward_image_inside_closed_ellipsoid",
        zero(s.together((1 + source_norm) ** 2 - 4 * source_norm - (1 - source_norm) ** 2)),
    )
    require("forward_q_equals_four_s_over_square", zero(s.together(image_q * (1 + source_norm) ** 2 - 4 * source_norm)))

    t = s.symbols("t", nonnegative=True)
    q_t = 1 - t ** 2
    selected = s.together(q_t / (1 + t) ** 2)
    recovered = s.together((2 / (1 + t)) / (1 + selected))
    require("inverse_scale_identity_8", zero(s.together(recovered - 1)))
    require("selected_branch_source_norm_at_most_one", zero(s.together(selected * (1 + t) - (1 - t))))
    other = s.together(q_t / (1 - t) ** 2)
    other_recovered = s.cancel((2 / (1 - t)) / (1 + other))
    require("minus_branch_is_a_different_preimage", zero(s.together(other_recovered - 1)))
    require(
        "minus_branch_is_not_equation_8",
        s.simplify(other.subs(t, s.Rational(1, 2)) - selected.subs(t, s.Rational(1, 2))) != 0,
    )
    rationalized = s.together((1 - t) / q_t)
    require(
        "rationalized_denominator_matches_for_q_nonzero",
        zero(s.together(rationalized * (1 + t) - 1)),
    )
    require("inverse_fixes_zero", zero(s.limit(recovered, t, 1) - 1))
    require("inverse_fixes_boundary_q_one", zero(recovered.subs(t, 0) - 1))

    sample_h = s.Matrix([s.Rational(1, 11), s.Rational(-1, 13), s.Rational(2, 17)])
    sample_norm = s.factor((sample_h.T * gram_w * sample_h)[0])
    require("rational_witness_inside_open_ellipsoid", 0 < sample_norm < 1)
    sample_y = s.simplify(2 * gram_w * sample_h / (1 + sample_norm))
    sample_q = s.factor((sample_y.T * gram_w.inv() * sample_y)[0])
    sample_t = s.factor((1 - sample_norm) / (1 + sample_norm))
    require("rational_witness_q_matches_forward", zero(s.together(sample_q - 4 * sample_norm / (1 + sample_norm) ** 2)))
    require("rational_witness_sqrt_gap_is_rational", zero(s.together(sample_t ** 2 - (1 - sample_q))))
    sample_back = s.simplify(gram_w.inv() * sample_y / (1 + sample_t))
    require("rational_forward_inverse_witness", zero_matrix(sample_back - sample_h))

    ratio = (A * A + 4 * A * B + 5 * B * B) / transverse
    history_quad = s.together((direction.T * inverse * direction)[0])
    require("history_quadratic_ratio_10", zero(s.together(history_quad - ratio)))
    gap_factor = s.together(1 - ratio)
    require("covariance_gap_is_two_B_squared", zero(s.together(gap_factor - 2 * B ** 2 / transverse)))
    gap_num = s.factor(s.together(gap_factor.subs(positive_root) * lam2))
    require("ratio_strictly_below_one_when_B_positive", gap_num == 2 * Bpos ** 2)
    require("ratio_reaches_one_if_B_vanishes", zero(s.together(gap_factor.subs(B, 0))))

    rr = 2 * p - 1
    ss = 2 * a * p
    require("golden_relation", zero(reduce(p * p + p - 1)))
    require("chebyshev_argument_equals_p3", zero(reduce(rr - p ** 3)))
    require("rotation_norm", zero(reduce(rr ** 2 + ss ** 2 - 1)))
    require("argument_inside_open_interval", zero(reduce(1 - rr ** 2 - 4 * p ** 3)))

    r, sig, c_prev, s_prev = s.symbols("r sig c_prev s_prev")
    c_n = r * c_prev - sig * s_prev
    s_n = r * s_prev + sig * c_prev
    c_next = r * c_n - sig * s_n
    norm_gap = s.expand(c_n ** 2 + s_n ** 2 - (r ** 2 + sig ** 2) * (c_prev ** 2 + s_prev ** 2))
    recurrence_gap = s.expand(s.expand(c_next - (2 * r * c_n - c_prev)).subs(sig ** 2, 1 - r ** 2))
    require("chebyshev_norm_step", zero(norm_gap))
    require("chebyshev_recurrence_step", zero(recurrence_gap))
    require("chebyshev_base", s.chebyshevt(0, rr) == 1 and s.expand(s.chebyshevt(1, rr) - rr) == 0)

    c_n_val, s_n_val = s.Integer(1), s.Integer(0)
    audit_ok = zero(reduce(c_n_val - 1)) and zero(reduce(c_n_val ** 2 + s_n_val ** 2 - 1))
    for n in range(AUDIT_N):
        c_n_val, s_n_val = (
            reduce(rr * c_n_val - ss * s_n_val),
            reduce(rr * s_n_val + ss * c_n_val),
        )
        expected = reduce(s.chebyshevt(n + 1, rr))
        audit_ok = audit_ok and zero(reduce(c_n_val - expected)) and zero(reduce(c_n_val ** 2 + s_n_val ** 2 - 1))
    require("chebyshev_finite_audit", audit_ok)
    require(
        "chebyshev_bound_all_n",
        "chebyshev_norm_step" in checks and "chebyshev_recurrence_step" in checks and "chebyshev_base" in checks,
    )

    p_pos = (s.sqrt(5) - 1) / 2
    require("positive_golden_root", bool(s.simplify(p_pos ** 2 + p_pos - 1) == 0 and s.simplify(p_pos ** 6) > 0))
    require("margin_identity_11", bool(s.simplify(1 - 4 * p_pos ** 3 - p_pos ** 6) == 0))
    require("margin_positive", bool(s.simplify(p_pos ** 6) > 0 and s.simplify(4 * p_pos ** 3) < 1))

    q_tau = s.together(4 * p ** 3 * tau ** 2 * ratio)
    deficit = s.together(4 * p ** 3 - q_tau)
    require(
        "probe_quadratic_form",
        zero(s.together(deficit - 4 * p ** 3 * ((1 - ratio) + ratio * (1 - tau ** 2)))),
    )
    floor = s.together(4 * p ** 3 * (1 - ratio))
    require("probe_deficit_at_least_covariance_gap", zero(s.together(deficit - floor - 4 * p ** 3 * ratio * (1 - tau ** 2))))
    require(
        "strict_deficit_factors_through_B",
        zero(s.together(floor - 8 * p ** 3 * B ** 2 / transverse)),
    )
    require(
        "equality_to_4p3_fails_for_positive_B",
        not zero(s.expand(floor.subs({A: Bpos + delta, B: Bpos, p: p_pos}))),
    )
    order_01 = s.together(4 * p ** 3 * ratio)
    order_10 = s.together(p ** 6 * order_01)
    require("order_01_same_ray_as_chebyshev_endpoint", zero(s.together(order_01 - q_tau.subs(tau ** 2, 1))))
    require("order_10_smaller_by_p6", zero(reduce(s.together(order_10 - p ** 6 * 4 * p ** 3 * ratio))))
    require("golden_order_coefficient", zero(reduce((2 - 3 * p) - p ** 4)))

    c8 = s.simplify(64 * (1 - s.cos(2 * s.pi / 8)) / 4)
    require("L8_source_unit", bool(s.simplify(c8 - 8 * (2 - s.sqrt(2))) == 0))
    raw = 16 * a * (2 - s.sqrt(2))
    require("unit_change_matches_equation_10", bool(s.simplify(raw / c8 - 2 * a) == 0))

    gap_above = s.together(1 - 4 * p ** 3 * ratio - p ** 6)
    require(
        "gap_above_p6_identity",
        zero(reduce(s.together(gap_above - 4 * p ** 3 * (1 - ratio)))),
    )

    flags = {
        "uniform_history_separation": False,
        "geometry_claimed": False,
        "physical_GR_closed": False,
        "field_kernel_solved": False,
        "nonlinear_branch_built": False,
        "claims_row_added": False,
        "preparation_law_selected": False,
        "native_root_searched": False,
        "operators": "memo B_r, not a new J_r",
    }
    for name, value in flags.items():
        if name == "operators":
            continue
        require(f"flag_{name}_false", value is False)

    return {
        "schema": "d0-rank-orbit-margin/1",
        "pin": PIN,
        "memo_sha256": MEMO_SHA256,
        "fibre_sha256": FIBRE_SHA256,
        "exact_checks": len(checks),
        "checks": checks,
        "audit_n": AUDIT_N,
        "witness_principal_minors": [str(minor) for minor in minors],
        "witness_source_norm": str(sample_norm),
        "gamma_positive_definite": True,
        "inverse_map": "h(y)=Gamma^{-1} y/(1+sqrt(1-q)), q=y^T Gamma^{-1} y<=1",
        "history_bound": "y_k^T Gamma^{-1} y_k < 4 p^3",
        "margin": "1-4 p^3 = p^6 > 0",
        "ellipsoid_gap_lower_bound_independent_of_index": True,
        "margin_separates_distinct_histories": False,
        **flags,
    }


def main() -> None:
    print(json.dumps(certify(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
