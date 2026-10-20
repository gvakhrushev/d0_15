#!/usr/bin/env python3
"""Decisive check for the rank-8 saddle zero block.

A negative control returns a rejected shape. An exception from arithmetic
is a coding error. ZeroBlockError is the required refusal to invert.
"""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

import sympy as s

sys.path.insert(0, str(Path(__file__).resolve().parent))

import saddle_zero as z

FAILURES: list[str] = []
PASSES = 0


def check(name: str, cond: bool) -> None:
    global PASSES
    print(("PASS " if cond else "FAIL ") + name)
    if cond:
        PASSES += 1
    else:
        FAILURES.append(name)


def _independent_block_shape() -> None:
    """SymPy Hessian of (1/2) v^T H v + s^T T v, not the library scanner."""
    h11, h12, h22 = s.symbols("h11 h12 h22", real=True)
    v1, v2 = s.symbols("v1 v2", real=True)
    shell = s.Matrix(s.symbols("s1:4", real=True))
    velocity = s.Matrix([v1, v2])
    field = s.Matrix([[h11, h12], [h12, h22]])
    coupling = s.Matrix(3, 2, lambda i, j: s.symbols(f"T{i}{j}", real=True))
    lagrangian = (s.Rational(1, 2) * (velocity.T * field * velocity)[0]) + (
        shell.T * coupling * velocity
    )[0]
    variables = [v1, v2, *shell]
    hessian = s.hessian(lagrangian, variables)
    check("independent_upper_block_is_H_rho", hessian[:2, :2] == field)
    check("independent_off_diagonal_is_T_k", hessian[2:, :2] == coupling)
    check("independent_adjoint_is_T_k_star", hessian[:2, 2:] == coupling.T)
    check("independent_lower_block_is_zero", hessian[2:, 2:] == s.zeros(3))
    scale = s.Integer(z.OCCUPIED_RANK)
    polluted = lagrangian + (scale / 2) * (shell.T * shell)[0]
    polluted_hessian = s.hessian(polluted, variables)
    check(
        "independent_thermal_lower_block_is_not_zero",
        polluted_hessian[2:, 2:] == scale * s.eye(3),
    )
    check(
        "independent_polluted_shape_differs",
        polluted_hessian[2:, 2:] != hessian[2:, 2:],
    )


def _scanner_matches_sympy() -> None:
    dimension = 4
    coefficients = s.symbols("c0:4", real=True)
    for scale in (0, z.OCCUPIED_RANK):
        coords = s.Matrix(s.symbols("x0:4", real=True))
        lagrangian = sum(coords[i] * coefficients[i] for i in range(dimension))
        lagrangian += s.Rational(scale, 2) * sum(coords[i] ** 2 for i in range(dimension))
        hessian = s.hessian(lagrangian, list(coords))
        for i in range(dimension):
            got = z.hessian_diagonal(int(coefficients[i].subs(coefficients[i], 3 - i)), scale)
            # Compare the integer scanner at a numeric slice, and the symbolic diagonal.
            check(
                f"sympy_diagonal_scale_{scale}_{i}",
                s.simplify(hessian[i, i] - scale) == 0 and got == scale,
            )
            for j in range(i + 1, dimension):
                off = z.hessian_off(3 - i, 1 - j, scale)
                check(
                    f"sympy_off_scale_{scale}_{i}_{j}",
                    hessian[i, j] == 0 and off == 0,
                )


def _memo_pin() -> None:
    payload = z.memo_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    check("memo_sha256", digest == z.MEMO_SHA256)
    text = payload.decode("utf-8")
    for anchor in z.MEMO_ANCHORS:
        check("memo_anchor_" + anchor[:24].replace(" ", "_"), anchor in text)


def _dimensions() -> None:
    check("rank8_vk_dimension", z.vk_dimension(128, 8) == 1983)
    check("full_rank_vk_is_different", z.vk_dimension(128, 128) == 16383)
    check("rank8_is_not_full_rank_target", 1983 != 16383)
    check(
        "coordinate_count_matches_formula",
        (8 * 8 - 1) + 2 * 8 * (128 - 8) == z.vk_dimension(128, 8),
    )


def _formula_agreement() -> None:
    symbolic = z.symbolic_hermitian(10)
    by_entry = z.t_matrix(symbolic, 8)
    by_projector = z.t_matrix_projectors(symbolic, 8)
    check("symbolic_k8_projector_matches_entries", z.matrices_equal(by_entry, by_projector))
    shell = z.symbolic_vk(8, 2)
    check("symbolic_vk_membership", z.in_vk(shell, 8))
    gap = s.expand(z.frobenius(shell, by_entry) - z.frobenius(shell, symbolic))
    check("symbolic_pairing_gap_vanishes", gap == 0)
    empty_only = z.symbolic_hermitian(4)
    for i in range(4):
        for j in range(4):
            if i < 2 or j < 2:
                empty_only[i][j] = 0
    hidden = z.t_matrix(empty_only, 2)
    check(
        "symbolic_empty_block_is_invisible_to_T_k",
        all(s.expand(hidden[i][j]) == 0 for i in range(4) for j in range(4)),
    )


def _rank8_shell() -> None:
    shell = z.SHELL_RANK
    occupied = z.OCCUPIED_RANK
    matrix = z.hermitian_from_pattern(shell)
    image = z.t_matrix(matrix, occupied)
    mirrored = z.t_matrix_projectors(matrix, occupied)
    check("rank8_projector_matches_entries", z.matrices_equal(image, mirrored))
    other = z.hermitian_from_pattern(shell)
    other[3][3] = other[3][3] + s.Rational(1, 5)
    other[20][21] = other[20][21] + s.I * s.Rational(2, 3)
    other[21][20] = s.conjugate(other[20][21])
    left = z.t_matrix(z.add_matrices(matrix, other), occupied)
    right = z.add_matrices(image, z.t_matrix(other, occupied))
    check("rank8_T_k_linear", z.matrices_equal(left, right))
    check(
        "rank8_T_k_homogeneous",
        z.matrices_equal(z.t_matrix(z.scale_matrix(3, matrix), occupied), z.scale_matrix(3, image)),
    )
    trace = sum(image[i][i] for i in range(shell))
    check("rank8_T_k_trace_zero", s.expand(trace) == 0)
    empty_clear = all(
        image[i][j] == 0 for i in range(occupied, shell) for j in range(occupied, shell)
    )
    check("rank8_T_k_empty_block_zero", empty_clear)
    hermitian = all(
        s.expand(image[j][i] - s.conjugate(image[i][j])) == 0
        for i in range(shell)
        for j in range(i, shell)
    )
    check("rank8_T_k_hermitian", hermitian)
    check(
        "frobenius_matches_trace_product",
        s.expand(z.frobenius(matrix, image) - z.trace_product(matrix, image)) == 0,
    )
    eta = z.occupied_traceless_witness(shell, occupied)
    check("eta_in_vk", z.in_vk(eta, occupied))
    eta_image = z.t_matrix(eta, occupied)
    check("T_k_fixes_traceless_occupied_witness", z.matrices_equal(eta_image, eta))
    pairing = s.expand(z.frobenius(eta, eta_image) - z.frobenius(eta, eta))
    check("pairing_on_eta", pairing == 0)
    rect = z.rectangular_witness(shell, occupied)
    check("rectangular_in_vk", z.in_vk(rect, occupied))
    rect_image = z.t_matrix(rect, occupied)
    check("T_k_fixes_rectangular_witness", z.matrices_equal(rect_image, rect))
    check(
        "pairing_on_rectangular",
        s.expand(z.frobenius(rect, rect_image) - z.frobenius(rect, rect)) == 0,
    )
    outside = z.pure_empty_witness(shell, occupied)
    check("empty_traceless_not_in_vk", z.in_vk(outside, occupied) is False)
    outside_image = z.t_matrix(outside, occupied)
    check(
        "empty_traceless_compressed_to_zero",
        all(value == 0 for row in outside_image for value in row),
    )
    mutated = [row[:] for row in matrix]
    mutated[occupied][occupied] = mutated[occupied][occupied] + s.Integer(9)
    check(
        "changing_empty_entry_does_not_change_T_k",
        z.matrices_equal(image, z.t_matrix(mutated, occupied)),
    )
    fixed = eta
    check(
        "explicit_shell_second_difference_zero",
        s.expand(z.linear_shell_second_difference(eta, rect, fixed)) == 0,
    )


def _positive_controls(zero_scan: dict) -> dict:
    occupied = z.OCCUPIED_RANK
    shell = z.SHELL_RANK
    eta = z.occupied_traceless_witness(shell, occupied)
    true_quadratic = z.linear_shell_second_difference(eta, eta, eta)
    thermal = s.expand(z.thermal_quadratic(eta, occupied))
    entropy = z.entropy_second_variation(occupied)
    check("true_quadratic_on_eta_is_zero", s.expand(true_quadratic) == 0)
    check("thermal_quadratic_on_eta", thermal == 16)
    check("entropy_second_variation_matches_thermal", entropy["second"] == 16)
    check("entropy_equals_k_tr_eta_square", entropy["k_tr_eta_square"] == 16)
    check("thermal_disagrees_with_zero_block", thermal != s.expand(true_quadratic))
    rect = z.rectangular_witness(shell, occupied)
    thermal_rect = s.expand(z.thermal_quadratic(rect, occupied))
    check("thermal_on_rectangular_direction", thermal_rect == 16)
    check(
        "zero_block_on_rectangular_direction",
        s.expand(z.linear_shell_second_difference(rect, rect, rect)) == 0,
    )
    divergence = z.empty_log_divided_difference(occupied)
    check("empty_log_divided_difference_diverges", divergence == s.oo)
    minors = z.diagonal_sum_of_squares_minors(occupied)
    check(
        "traceless_diagonal_form_positive",
        minors == [1 + width for width in range(1, occupied)],
    )
    thermal_operator = z.scale_matrix(occupied, eta)
    thermal_pairing = s.expand(z.frobenius(eta, thermal_operator))
    true_pairing = s.expand(z.frobenius(eta, eta))
    check("thermal_replacement_pairing", thermal_pairing == 16)
    check("true_T_k_pairing_on_same_vector", true_pairing == 2)
    check("thermal_replacement_is_not_T_k", thermal_pairing != true_pairing)
    positive_scan = z.scan_lower_block(z.RANK8_VK, occupied)
    check("scanner_sees_positive_diagonal", positive_scan["nonzero"] == z.RANK8_VK)
    check("scanner_positive_diagonal_value", positive_scan["first_diagonal"] == occupied)
    check("scanner_positive_off_diagonal_stays_zero", positive_scan["first_off"] == 0)
    check("scanner_positive_has_no_off_leak", positive_scan["off_mismatch"] == 0)
    check("zero_scan_has_no_entries", zero_scan["nonzero"] == 0)
    check("positive_scan_is_not_the_zero_block", positive_scan["nonzero"] != zero_scan["nonzero"])
    true_report = {
        "vk_dimension": zero_scan["dimension"],
        "lower_nonzero": zero_scan["nonzero"],
        "lower_quadratic_on_witness": s.expand(true_quadratic),
        "pairing_gap": 0,
        "off_diagonal_is_t_k": True,
        "inverted": False,
        "thermal_matrix_replaced_t_k": False,
    }
    thermal_block_report = {
        "vk_dimension": zero_scan["dimension"],
        "lower_nonzero": 0 if thermal == 0 else 1,
        "lower_quadratic_on_witness": thermal,
        "pairing_gap": 0,
        "off_diagonal_is_t_k": True,
        "inverted": False,
        "thermal_matrix_replaced_t_k": False,
    }
    thermal_coupling_report = {
        "vk_dimension": zero_scan["dimension"],
        "lower_nonzero": zero_scan["nonzero"],
        "lower_quadratic_on_witness": 0,
        "pairing_gap": thermal_pairing - true_pairing,
        "off_diagonal_is_t_k": False,
        "inverted": False,
        "thermal_matrix_replaced_t_k": True,
    }
    check("true_saddle_shape_accepted", z.shape_accepts(true_report))
    check("positive_auxiliary_hessian_fails_check", z.shape_accepts(thermal_block_report) is False)
    check(
        "positive_coordinate_hessian_fails_check",
        z.shape_accepts({**true_report, "lower_nonzero": positive_scan["nonzero"]}) is False,
    )
    check("thermal_matrix_in_place_of_T_k_fails_check", z.shape_accepts(thermal_coupling_report) is False)
    check("full_rank_dimension_fails_check", z.shape_accepts({**true_report, "vk_dimension": 16383}) is False)
    return true_report


def _refusal(true_report: dict) -> None:
    for scale in (0, z.OCCUPIED_RANK):
        refused = False
        try:
            z.invert_lower_block(scale)
        except z.ZeroBlockError:
            refused = True
        check(f"invert_lower_block_refused_scale_{scale}", refused)
    inverted_report = {**true_report, "inverted": True}
    check("inverted_report_fails_shape", z.shape_accepts(inverted_report) is False)
    flags = z.candidate_flags()
    check("flags_candidate", flags["status"] == "candidate")
    check("flags_lower_block_not_inverted", flags["lower_block_inverted"] is False)
    check("flags_no_thermal_substitution", flags["thermal_hessian_substituted"] is False)
    check("flags_T_k_not_replaced", flags["t_k_replaced_by_positive_thermal_matrix"] is False)
    check("flags_field_kernel_open", flags["field_kernel_solved"] is False)
    check("flags_nonlinear_branch_open", flags["nonlinear_branch_built"] is False)
    check("flags_gr_not_derived", flags["gr_derived"] is False)
    check("flags_no_claims_row", flags["claims_csv_row_added"] is False)
    check("flags_no_r01_import", flags["imports_r01"] is False)
    check("flags_no_r02_import", flags["imports_r02"] is False)
    library = Path(z.__file__).read_text(encoding="utf-8")
    for banned in (
        "d0_rank_mv_full",
        "d0_rank_mv_rank8",
        "wrk_r01",
        "wrk_r02",
    ):
        check("library_does_not_name_" + banned, banned not in library)


def main() -> int:
    _memo_pin()
    _dimensions()
    _independent_block_shape()
    _scanner_matches_sympy()
    _formula_agreement()
    _rank8_shell()
    zero_scan = z.scan_lower_block(z.RANK8_VK, 0)
    check("rank8_lower_block_dimension", zero_scan["dimension"] == 1983)
    check("rank8_lower_block_pairs", zero_scan["pairs"] == 1983 * 1984 // 2)
    check("rank8_lower_block_all_zero", zero_scan["nonzero"] == 0)
    check("rank8_lower_diagonal_value", zero_scan["first_diagonal"] == 0)
    check("rank8_lower_off_value", zero_scan["first_off"] == 0)
    check("rank8_lower_diagonal_uniform", zero_scan["diagonal_mismatch"] == 0)
    check("rank8_lower_off_uniform", zero_scan["off_mismatch"] == 0)
    true_report = _positive_controls(zero_scan)
    _refusal(true_report)
    print(f"checks={PASSES + len(FAILURES)}")
    if FAILURES:
        print("FAILED " + ", ".join(FAILURES))
        return 1
    print("status=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
