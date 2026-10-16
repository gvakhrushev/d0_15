#!/usr/bin/env python3
"""Independent checks for the fixed-probe source margin. No bare asserts."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import sympy as s

import orbit_margin as om

FAILURES: list[str] = []

CRITICAL = (
    "covariance_matches_formula_5",
    "gamma_positive_definite_for_A_gt_B_gt_0",
    "cubic_moment_zero_0",
    "pure_source_numerator_0",
    "inverse_scale_identity_8",
    "rational_forward_inverse_witness",
    "history_quadratic_ratio_10",
    "chebyshev_norm_step",
    "chebyshev_recurrence_step",
    "chebyshev_finite_audit",
    "margin_identity_11",
    "probe_quadratic_form",
    "gap_above_p6_identity",
    "unit_change_matches_equation_10",
    "equality_to_4p3_fails_for_positive_B",
    "minus_branch_is_not_equation_8",
    "flag_uniform_history_separation_false",
    "flag_geometry_claimed_false",
    "flag_physical_GR_closed_false",
)


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILURES.append(name)


def independent_algebra() -> None:
    p_pos = (s.sqrt(5) - 1) / 2
    check("independent_golden_minimal_polynomial", s.simplify(p_pos ** 2 + p_pos - 1) == 0)
    check("independent_margin_identity", s.simplify(1 - 4 * p_pos ** 3 - p_pos ** 6) == 0)
    check("independent_margin_positive", bool(s.simplify(p_pos ** 6) > 0))
    check("independent_four_p3_not_one", bool(s.simplify(1 - 4 * p_pos ** 3) != 0))

    argument = 2 * p_pos - 1
    # Polynomial identity on this one argument: T_n^2 + (1-x^2) U_{n-1}^2 = 1.
    for n in range(0, 9):
        value = s.chebyshevt(n, argument)
        if n == 0:
            gap = s.simplify(value ** 2 - 1)
        else:
            second = s.chebyshevu(n - 1, argument)
            gap = s.simplify(value ** 2 + (1 - argument ** 2) * second ** 2 - 1)
        check(f"independent_chebyshev_identity_{n}", gap == 0)
        check(f"independent_chebyshev_inside_{n}", bool(s.simplify(1 - value ** 2) >= 0))

    a_val, b_val = s.Rational(3, 5), s.Rational(1, 10)
    transverse = a_val ** 2 + 4 * a_val * b_val + 7 * b_val ** 2
    off = a_val ** 2 - 4 * a_val * b_val - b_val ** 2
    gram = transverse * s.eye(3) + off * s.ones(3)
    minors = [gram[:k, :k].det() for k in (1, 2, 3)]
    check("independent_witness_pd", all(minor > 0 for minor in minors))
    direction = s.Matrix([2 * b_val, -a_val, -a_val])
    quad = s.together((direction.T * gram.inv() * direction)[0])
    ratio = (a_val ** 2 + 4 * a_val * b_val + 5 * b_val ** 2) / transverse
    check("independent_history_ratio", s.simplify(quad - ratio) == 0)
    check("independent_ratio_strict", bool(s.simplify(ratio) < 1))
    endpoint = s.simplify(4 * p_pos ** 3 * ratio)
    check("independent_endpoint_below_4p3", bool(endpoint < 4 * p_pos ** 3))
    check("independent_gap_above_p6", bool(s.simplify(1 - endpoint - p_pos ** 6) > 0))

    sample_h = s.Matrix([s.Rational(1, 11), s.Rational(-1, 13), s.Rational(2, 17)])
    source_norm = s.together((sample_h.T * gram * sample_h)[0])
    sample_y = s.simplify(2 * gram * sample_h / (1 + source_norm))
    sample_t = s.together((1 - source_norm) / (1 + source_norm))
    recovered = s.simplify(gram.inv() * sample_y / (1 + sample_t))
    other = s.simplify(gram.inv() * sample_y / (1 - sample_t))
    check("independent_plus_branch", s.simplify(recovered - sample_h) == s.zeros(3, 1))
    check("independent_minus_branch_differs", s.simplify(other - sample_h) != s.zeros(3, 1))
    # |T|<=1 admits coefficients closer than p^6, so p^6 is not a history separation.
    near = 1 - s.Rational(1, 1000)
    check("admissible_coefficients_squared", bool(near ** 2 <= 1))
    check(
        "p6_is_not_a_coefficient_separation",
        bool(s.simplify(s.Abs(1 - near) - p_pos ** 6) < 0),
    )


def main() -> int:
    result = om.certify()
    check("exact_check_count", result["exact_checks"] == 72 and len(result["checks"]) == 72)
    check("checks_unique", len(set(result["checks"])) == 72)
    for name in CRITICAL:
        check("present_" + name, name in result["checks"])
    check("gamma_positive", result["gamma_positive_definite"] is True)
    check("no_uniform_separation", result["uniform_history_separation"] is False)
    check("no_history_separation_flag", result["margin_separates_distinct_histories"] is False)
    check("gap_bound_not_a_distance", result["ellipsoid_gap_lower_bound_independent_of_index"] is True)
    check("no_geometry", result["geometry_claimed"] is False)
    check("gr_not_closed", result["physical_GR_closed"] is False)
    check("no_field_kernel", result["field_kernel_solved"] is False)
    check("no_nonlinear_branch", result["nonlinear_branch_built"] is False)
    check("no_claims_row", result["claims_row_added"] is False)
    check("no_preparation_law", result["preparation_law_selected"] is False)
    check("no_root_search", result["native_root_searched"] is False)
    check("operators_are_memo_B", result["operators"] == "memo B_r, not a new J_r")
    independent_algebra()
    if FAILURES:
        print("status = FAIL")
        print("FAILED " + ", ".join(FAILURES))
        return 1
    print("status = PASS")
    print("exact_checks =", result["exact_checks"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
