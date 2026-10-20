#!/usr/bin/env python3
"""Decisive checks for the owned off-shell matter response.

No assert: python -O must keep every scientific check. The native
complement of 16,744,448 real coordinates is never allocated. The
row-wave repair and the nonscalar conformal obstruction are different
scopes. The old 8192-edge price sum is not rerun.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import sympy as s

import matter_response as mr


CHECKS = []


def require(condition, label):
    if not bool(condition):
        raise AssertionError(label)
    CHECKS.append(label)


def zero(value):
    return mr.is_zero(value)


def git_text(sha, path):
    repo = Path(__file__).resolve().parents[4]
    return subprocess.check_output(
        ["git", "show", "%s:%s" % (sha, path)],
        cwd=repo, text=True,
    )


def fixture_isometries():
    U = s.Matrix([[0, 0], [1, 0], [0, 1], [0, 0]])
    W = s.Matrix([[1, 0], [0, 0], [0, 0], [0, 1]])
    return U, W


def check_provenance():
    wave = git_text(
        mr.HISTORICAL_SHA,
        "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py",
    )
    heat = git_text(
        mr.HISTORICAL_SHA,
        "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/record_heat_continuation.py",
    )
    owner = git_text(
        mr.OWNER_SHA,
        "02_REGISTRY/research/A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md",
    )
    require(
        "return lambda1*rotated_norm_squared*(1+B/(B+256*o))/2" in wave,
        "pinned_row_wave_gamma",
    )
    require(
        "return -64*(d+3*o)*polynomial/((d+o)*((7+5*rt2)*d+(11+8*rt2)*o))" in heat,
        "pinned_conformal_trace_contrast",
    )
    require("8*sqrt(2)*(d-o)>0" in heat, "pinned_nonscalar_defect_statement")
    require("16 744 448" in owner, "pinned_excluded_real_count")
    require(mr.EXCLUDED_REAL_Q_COORDINATES == 16744448, "excluded_count_is_16744448")
    require(mr.CARRIER_DIM == 65536 and mr.SHELL_RANK == 128, "carrier_and_shell128")
    require(len(mr.SHELL_MOMENTA) == 8, "eight_shell_momenta")
    require(all(mr.is_shell_momentum(mode) for mode in mr.SHELL_MOMENTA), "shell_mask_accepts_owned_shell")
    require(not mr.is_shell_momentum((0, 0, 0, 0)), "zero_mode_stays_off_shell")
    require(not mr.is_shell_momentum((3, 3, 0, 0)), "row_wave_momentum_is_not_a_shell_mode")


def check_rectangle_and_bound():
    rectangle = mr.certified_root_rectangle()
    require(rectangle["d_above_o"], "receipt_rectangle_has_d_above_o")
    require(rectangle["d_above_one_sixteenth"], "receipt_rectangle_has_d_above_1_16")
    require(rectangle["epsilon0_above_2"], "zero_mode_does_not_spoil_the_certified_gap")
    require(rectangle["field_inverse_estimated"] is False, "rectangle_does_not_estimate_field_inverse")
    inside = mr.uniform_shell_complement_bound(
        s.Rational(1, 9), s.Rational(1, 9), gap_exceeds_certified=True,
    )
    require(inside["gq_strict_upper"] == 4, "gq_bound_4_inside_open_window")
    require(inside["rq_norm_upper"] == 2, "rq_bound_2_from_certified_gap")
    require(inside["field_inverse_estimated"] is False, "bound_is_not_a_field_inverse")
    boundary = mr.uniform_shell_complement_bound(
        s.Rational(1, 8), s.Rational(1, 9), gap_exceeds_certified=True,
    )
    require(boundary["gq_strict_upper"] is None, "gq_bound_refused_on_closed_window")
    require(boundary["rq_norm_upper"] == 2, "root_resolvent_bound_survives_outside_the_window")
    missing = mr.uniform_shell_complement_bound(
        s.Rational(1, 100), 0, gap_exceeds_certified=False,
    )
    require(missing["gq_strict_upper"] is None and missing["rq_norm_upper"] is None,
            "no_substitute_bound_without_the_certified_gap")
    # A numerically smaller resolvent is not allowed to replace the constant 4.
    require(inside["gq_strict_upper"] != s.Rational(10, 11), "certified_4_is_not_a_fitted_norm")


def check_neumann():
    tail = mr.neumann_tail_bound(3, s.Rational(1, 3), 2)
    require(tail["exact_tail"] == s.Rational(1, 27) and tail["strict"], "neumann_tail_strictly_under_4_over_16")
    try:
        mr.neumann_tail_bound(1, s.Rational(1, 2), 2)
    except mr.MatterResponseError:
        require(True, "neumann_tail_refuses_contraction_one_half")
    else:
        require(False, "neumann_tail_refuses_contraction_one_half")
    offsets = (s.Integer(1), s.Integer(-2))
    shifts = (s.Rational(1, 10), s.Rational(-1, 10))
    applied = mr.matrix_free_neumann(offsets, shifts, 6)
    expected = (s.Rational(10, 11), s.Rational(-10, 21))
    require(all(zero(got - want) for got, want in zip(applied["exact"], expected)),
            "modewise_resolvent_matches_the_scalar_inverse")
    require(applied["workspace_length"] == 2, "neumann_workspace_is_the_mode_count")
    require(applied["excluded_coordinates_materialized"] == 0, "neumann_allocates_no_excluded_vector")
    require(applied["matrix_free"] is True, "neumann_apply_is_matrix_free")
    errors = [
        s.Abs(s.simplify(partial - exact))
        for partial, exact in zip(applied["partial"], applied["exact"])
    ]
    # ||R0 V|| = 1/10, ||R0|| = 1, tail = 1 * (1/10)^7 / (1-1/10).
    limit = mr.neumann_tail_bound(6, s.Rational(1, 10), 1)["exact_tail"]
    require(all(error <= limit for error in errors), "partial_sum_respects_the_owned_tail")
    try:
        mr.refuse_native_dense_materialization(mr.CARRIER_DIM, mr.SHELL_RANK, mr.REFERENCE_RANK)
    except mr.MatterResponseError:
        require(True, "native_dense_Q_amplitudes_refused")
    else:
        require(False, "native_dense_Q_amplitudes_refused")
    try:
        mr.solve_matter_response(
            {"scope": "native_dense"}, {"scope": "native_dense"}, {"carrier": "native_dense"},
        )
    except mr.MatterResponseError:
        require(True, "solve_refuses_native_dense_carrier")
    else:
        require(False, "solve_refuses_native_dense_carrier")


def check_elimination_and_jets():
    U, W = fixture_isometries()
    t = s.symbols("t", real=True)
    delta0 = s.diag(1, 2, 2, 4)
    coupling_jet = s.zeros(4)
    coupling_jet[0, 1] = coupling_jet[1, 0] = 1
    diagonal_jet = s.zeros(4)
    diagonal_jet[0, 0] = 1
    delta = delta0 + t * coupling_jet + (t ** 2) / 2 * diagonal_jet
    epsilon = 2 + t * s.Rational(1, 3) + (t ** 2) * s.Rational(1, 5)
    factors = mr.off_shell_factors(delta, epsilon, U, W)
    identity = mr.dE_formula(
        factors["J_Q"], factors["gram"], U, W, s.diff(delta, t), s.diff(epsilon, t),
    )
    require(zero(s.diff(factors["E"], t) - identity), "dE_identity_along_the_curve")
    require(not zero(factors["E"].subs(t, s.Rational(1, 7))), "curve_is_off_shell_at_one_seventh")
    require(
        zero((s.diff(factors["E"], t) - identity).subs(t, s.Rational(1, 7))),
        "dE_identity_holds_off_E0",
    )
    require(zero(factors["E"].subs(t, 0)), "curve_starts_on_the_shell")
    require(
        zero((U.H * (U + W * factors["J_Q"]) - s.eye(2)).subs(t, 0)),
        "J_splits_the_shell_at_the_root",
    )
    anti = s.zeros(2)
    anti[0, 1] = s.I
    anti[1, 0] = s.I
    # anti is Hermitian, not anti-Hermitian. Use a real skew reference velocity.
    reference_velocity = s.Matrix([[0, 1], [-1, 0]])
    tau = s.eye(2) / 2
    V = s.eye(2) + t * reference_velocity + (t ** 2) / 2 * (reference_velocity ** 2)
    jets = mr.response_curve_jets(delta, epsilon, tau, V, U, W, t)
    require(zero(jets["E"]["first"] - jets["dE_identity"]["value"]), "first_jet_matches_proved_dE")
    require(zero(jets["E"]["second"] - jets["dE_identity"]["first"]), "second_jet_matches_derivative_of_dE")
    require(zero(jets["normalization"]["first"]), "normalization_first_jet_holds_at_the_root_gram")
    require(not zero(jets["normalization"]["second"]), "frozen_tau_misses_the_second_normalization_jet")
    require(not zero(jets["frozen_trace"]["second"] - jets["normalization"]["second"]),
            "moving_gram_second_jet_is_not_the_frozen_trace")
    require(not zero(jets["Q_factor"]["first"]), "field_first_jet_reaches_the_normal_Q_response")
    require(not zero(jets["shell_factor"]["first"]), "reference_velocity_stays_in_the_shell_fiber")
    require(jets["declared_gauge"] is False, "curve_does_not_declare_V_gauge")
    gram = factors["gram"]
    rest = mr.normalization_restoring_tau_jet(
        tau, gram.subs(t, 0), s.diff(gram, t).subs(t, 0), s.diff(gram, t, 2).subs(t, 0),
    )
    require(not zero(rest["frozen_second_residual"]), "frozen_normalization_residual_is_nonzero")
    require(rest["declared_gauge"] is False, "trace_correction_does_not_gauge_fix_tau")
    corrected = tau + rest["trace_correction_first"] * t * s.eye(2)
    corrected += rest["trace_correction_second"] * (t ** 2) / 2 * s.eye(2)
    held = s.trace(corrected * gram)
    require(zero(s.diff(held, t).subs(t, 0)), "restoring_tau_kills_the_first_residual")
    require(zero(s.diff(held, t, 2).subs(t, 0)), "restoring_tau_kills_the_second_residual")

    # Owned nonlinear block with a moving Gram, transcribed as a fixture.
    coupling = s.Matrix([
        [s.Rational(1, 7), s.I / 11],
        [(1 + s.I) / 13, s.Rational(1, 17)],
    ])
    q_shift = s.diag(-1, 2)
    shell = s.simplify(coupling.H * q_shift.inv() * coupling)
    base = (
        2 * s.eye(4)
        + W * q_shift * W.H
        + W * coupling * U.H
        + U * coupling.H * W.H
        + U * shell * U.H
    )
    moved = mr.off_shell_factors(base, 2, U, W)
    require(zero(moved["E"]), "nonlinear_fixture_sits_at_E0")
    require(not zero(moved["gram"] - s.eye(2)), "nonlinear_fixture_gram_moves")
    tau_moving = s.eye(2) / s.trace(moved["gram"])
    moving = mr.normalization_value(tau_moving, moved["gram"])
    frozen = mr.normalization_value(s.eye(2) / 2, moved["gram"])
    require(moving["normalized"] is True, "moving_gram_normalization_holds")
    require(frozen["normalized"] is False, "frozen_trace_one_is_rejected")
    require(moving["frozen_reading_accepted"] is False, "frozen_reading_flag_stays_off")
    probe = s.zeros(4)
    probe[0, 0] = s.Rational(1, 3)
    probe[0, 1] = probe[1, 0] = 1
    probe[2, 3] = s.I
    probe[3, 2] = -s.I
    line = mr.off_shell_factors(base + t * probe, 2 + t * s.Rational(2, 7), U, W)
    line_identity = mr.dE_formula(
        line["J_Q"], line["gram"], U, W, probe, s.Rational(2, 7),
    )
    require(zero(s.diff(line["E"], t) - line_identity), "dE_identity_on_the_moving_gram_fixture")
    frozen_dE = mr.dE_formula(line["J_Q"], s.eye(2), U, W, probe, s.Rational(2, 7))
    require(not zero((line_identity - frozen_dE).subs(t, 0)), "frozen_gram_in_dE_disagrees")


def check_schmidt_and_pure16():
    U, W = fixture_isometries()
    delta = s.diag(1, 0, 5, 4)
    prime = s.zeros(4)
    prime[1, 1] = 1
    prime[2, 2] = 3
    rank_one = mr.solve_matter_response(prime, s.zeros(4), {
        "carrier": "block_fixture",
        "delta": delta,
        "epsilon": 0,
        "U": U,
        "W": W,
        "tau": s.diag(1, 0),
        "V": s.eye(2),
        "schmidt_rank": 1,
        "delta_op_norm": 1,
        "epsilon_shift": 1,
        "gap_exceeds_certified": False,
    })
    require(rank_one["projected_compatibility"]["operator_equality_proved"] is False,
            "rank_one_does_not_inherit_operator_equality")
    require(rank_one["extra"]["compatibility"]["support_zero"] is True,
            "rank_one_support_condition_can_hold")
    require(rank_one["extra"]["compatibility"]["compatible"] is True,
            "rank_one_compatibility_is_the_support_condition")
    require(rank_one["extra"]["bound"]["gq_strict_upper"] is None,
            "fixture_does_not_inherit_the_native_GQ_bound")
    require(rank_one["field_shell_kernel_solved"] is False, "fixture_does_not_solve_the_saddle")
    require(rank_one["declared_gauge"] is False, "rank_one_reference_is_not_gauge")
    require(rank_one["lower_saddle_block_inverted"] is False, "zero_lower_block_is_not_inverted")
    full = mr.projected_compatibility(
        s.diag(0, 5), s.eye(2), schmidt_rank=2, shell_rank=2,
    )
    require(full["operator_equality_proved"] is True and full["compatible"] is False,
            "full_schmidt_keeps_the_operator_equation_and_rejects_this_E")
    split = mr.linear_shell_split(s.diag(1, 3), full_schmidt=False)
    require(split["operator_equality_proved"] is False and split["operator_compatible"] is None,
            "linear_operator_equality_is_not_imposed_below_full_rank")
    scalar = mr.linear_shell_split(s.eye(2), full_schmidt=True)
    require(scalar["operator_compatible"] is True and zero(scalar["epsilon_prime"] - 1),
            "full_schmidt_scalar_block_is_epsilon_prime_P")
    try:
        mr.pure16_native_reduction(16, 128)
    except mr.MatterResponseError:
        require(True, "pure16_shell_rejected")
    else:
        require(False, "pure16_shell_rejected")
    try:
        mr.pure16_native_reduction(128, 16)
    except mr.MatterResponseError:
        require(True, "pure16_reference_rejected")
    else:
        require(False, "pure16_reference_rejected")
    kept = mr.pure16_native_reduction(128, 128)
    require(kept["accepted"] is True, "shell128_reference128_accepted")
    try:
        mr.solve_matter_response(prime, None, {"carrier": "block_fixture"})
    except mr.MatterResponseError:
        require(True, "missing_second_jet_is_not_treated_as_zero")
    else:
        require(False, "missing_second_jet_is_not_treated_as_zero")


def check_auxiliary_and_thermal():
    aux = mr.auxiliary_unfolding(s.diag(1, 3), s.diag(2, 4))
    require(aux["is_physical_matter"] is False and aux["is_reference_frame"] is False,
            "auxiliary_sigma_and_X_are_not_matter")
    require(zero(aux["sigma_aux"] - s.diag(s.Rational(1, 4), s.Rational(3, 4))),
            "sigma_aux_is_K_over_trace")
    require(zero(aux["X_aux"] - s.diag(s.Rational(1, 2), s.Rational(1, 4))),
            "X_aux_is_A_inverse")
    alpha = s.Rational(1, 8)
    exponent = 2
    beta = s.Rational(1, 4)
    fugacity = s.Rational(1, 5)
    feedback = 5
    reference_rank = 2
    eigenvalues = [s.Integer(1), s.Integer(2), s.Integer(2), s.Integer(4)]
    B = [1 - alpha * value for value in eigenvalues]
    Z = sum(value ** exponent for value in B)
    calibrations = {
        "alpha": alpha,
        "exponent": exponent,
        "beta": beta,
        "fugacity": fugacity,
        "feedback_multiplicity": feedback,
        "reference_rank": reference_rank,
        "Z": Z,
        "multiplicities": [1, 1, 1, 1],
    }
    outside = [1, 0, 0, 0]
    shell_mask = [False, True, True, False]
    kept = mr.thermal_feedback_source(
        eigenvalues, outside, [], calibrations, shell_mask=shell_mask,
    )
    dropped = mr.thermal_feedback_source(
        eigenvalues, outside, [], calibrations, shell_mask=shell_mask, drop_outside_shell=True,
    )
    omitted = mr.thermal_feedback_source(
        eigenvalues, outside, [], calibrations, shell_mask=shell_mask, omit_normalizer=True,
    )
    require(not zero(kept["outside_shell_diagonal_contribution"]),
            "outside_shell_diagonal_jet_is_visible_in_the_thermal_source")
    require(zero(dropped["first_source"]) and not zero(kept["first_source"]),
            "shell_truncation_drops_the_outside_jet")
    require(not zero(kept["normalizer_visible_on_shell"]),
            "outside_jet_moves_the_shell_feedback_through_Z")
    require(zero(omitted["normalizer_visible_on_shell"]),
            "dropping_the_normalizer_hides_that_shell_feedback")
    mixed = mr.thermal_feedback_source(
        eigenvalues, [0, 0, 0, 0], [(0, 1, s.Integer(1))], calibrations, shell_mask=shell_mask,
    )
    bare = mr.thermal_feedback_source(
        eigenvalues, [0, 0, 0, 0], [], calibrations, shell_mask=shell_mask,
    )
    require(not zero(mixed["second_contraction"] - bare["second_contraction"]),
            "shell_to_outside_coherence_survives_in_the_second_source")
    swapped = dict(calibrations)
    swapped["feedback_multiplicity"] = reference_rank
    other = mr.thermal_feedback_source(
        eigenvalues, outside, [], swapped, shell_mask=shell_mask,
    )
    require(not zero(kept["first_source"] - other["first_source"]),
            "feedback_multiplicity_is_not_replaced_by_reference_rank")
    require(kept["reference_rank_not_substituted"] is True, "thermal_carrier_keeps_the_two_roles")


def check_scopes():
    d, o, w = s.symbols("d o w", positive=True)
    require(zero(mr.gamma_second(d, o, w) - mr.gamma_memo_form(d, o, w)),
            "row_wave_gamma_matches_the_transport_note")
    defect = mr.occupied_vacuum_defect(d, o)
    require(zero(defect - 8 * s.sqrt(2) * (d - o)), "vacuum_defect_is_8_sqrt2_times_d_minus_o")
    contrast = mr.occupied_second_trace(d, o, (1, 0, 0, 0)) - mr.occupied_second_trace(d, o, (0, 0, 1, 0))
    require(zero(contrast - mr.occupied_trace_contrast(d, o)),
            "trace_contrast_matches_the_closed_form")
    sample_defect = s.simplify(defect.subs({d: 1, o: s.Rational(1, 2)}))
    sample_contrast = s.simplify(mr.occupied_trace_contrast(1, s.Rational(1, 2)))
    require(sample_defect > 0 and sample_contrast < 0, "defect_positive_and_contrast_negative")
    old_entry, old_trace, shift = s.symbols("old_entry old_trace shift")
    before = old_entry - old_trace / 16
    after = (old_entry + shift) - (old_trace + 16 * shift) / 16
    require(zero(before - after), "scalar_matrix_does_not_change_vacuum_minus_mean")
    row_scope = {"scope": "stored_rotational_row_wave"}
    row = mr.solve_matter_response(row_scope, row_scope, {
        "carrier": "row_wave", "a": s.Rational(1, 4), "b": s.Rational(1, 125),
    })
    conf_scope = {"scope": "nonscalar_conformal_obstruction"}
    conformal = mr.solve_matter_response(conf_scope, conf_scope, {
        "carrier": "conformal", "d": s.Rational(1, 2), "o": s.Rational(1, 5),
    })
    require(row["scope"] != conformal["scope"], "row_wave_and_conformal_are_different_scopes")
    require(row["extra"]["stored_adjoint_admissible"] is True, "row_wave_is_stored_adjoint_admissible")
    require(conformal["extra"]["stored_adjoint_admissible"] is False, "conformal_violates_diagonal_invariance")
    require(not zero(conformal["extra"]["diagonal_invariance_residual"]),
            "conformal_phi_shift_along_role_0_is_nonzero")
    require(zero(row["extra"]["leg_second_jet_identity"]), "row_wave_length_and_rotation_jets_match")
    require(row["extra"]["shell_second_rows_repaired"] is True, "length_acceleration_repairs_all_shell_rows")
    require(conformal["extra"]["shell_second_rows_repaired"] is False, "conformal_shell_rows_stay_obstructed")
    require(conformal["extra"]["scalar_repair_clears_defect"] is False, "scalar_repair_does_not_clear_conformal")
    require(zero(row["second_source"]["matter_eliminated_term"] + row["extra"]["gamma"] / 4),
            "row_wave_matter_term_is_minus_gamma_over_4")
    require(row["second_source"]["thermal_feedback_term"] == "not_recomputed_full_carrier_retained",
            "row_wave_does_not_replace_the_full_thermal_carrier")
    require(row["normal_response_nonzero"] is True, "row_wave_normal_response_is_nonzero")
    require(row["field_shell_kernel_solved"] is False and conformal["field_shell_kernel_solved"] is False,
            "neither_scope_solves_the_remaining_kernel")
    require(row["remaining_kernel_coordinates"]["declared_gauge"] is False, "kernel_fiber_is_not_gauge")
    require(row["remaining_kernel_coordinates"]["antihermitian_reference_real_dimension"] == 128 ** 2,
            "reference_fiber_keeps_16384_real_directions")
    require(row["remaining_kernel_coordinates"]["coordinates_materialized"] is False,
            "kernel_coordinates_are_not_materialized")
    require(row["shell_equations_satisfied"] is True, "repaired_row_wave_holds_the_shell_equations")
    require(conformal["shell_equations_satisfied"] is False, "conformal_shell_equations_remain_open")
    require(row["shell_equations_retained"] is True and conformal["shell_equations_retained"] is True,
            "both_scopes_retain_the_shell_equations")
    require(row["physical_admission"] is False and conformal["gr_derived"] is False,
            "no_physical_admission_and_no_GR")
    require(row["engine_narrower_than_full_hermitian_sphere"] is True,
            "stored_adjoint_restriction_is_separate_from_the_full_sphere")
    x0, x1, x2 = s.symbols("x0 x1 x2", real=True)
    phi = s.cos(2 * s.pi * (3 * x0 + 3 * x1) / 8)
    require(zero(s.diff(phi, x2)), "row_wave_phase_is_independent_of_x2")


def main():
    check_provenance()
    check_rectangle_and_bound()
    check_neumann()
    check_elimination_and_jets()
    check_schmidt_and_pure16()
    check_auxiliary_and_thermal()
    check_scopes()
    payload = {
        "status": "PASS",
        "checks": len(CHECKS),
        "check_names": CHECKS,
        "interface": "solve_matter_response",
        "import_path": "02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/matter_response.py",
        "matrix_free_operations": list(mr.MATRIX_FREE_OPERATIONS),
        "excluded_real_coordinates_materialized": 0,
        "field_shell_kernel_solved": False,
        "physical_admission": False,
        "gr_derived": False,
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    main()
