#!/usr/bin/env python3
"""Checks for the matrix-free v8 Hessian action.

No assert: python -O must keep every scientific check. The dense
workspace 128^8192 is not allocated. The zero shell block is not inverted.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import sympy as s

import hessian_apply as hz


CHECKS = []


def require(condition, label):
    if not bool(condition):
        raise AssertionError(label)
    CHECKS.append(label)


def zero(value):
    if isinstance(value, s.MatrixBase):
        return all(zero(entry) for entry in value)
    return s.simplify(s.expand(value)) == 0


def git_bytes(sha, path):
    repo = Path(__file__).resolve().parents[4]
    return subprocess.check_output(["git", "show", "%s:%s" % (sha, path)], cwd=repo)


def fixture_calibrations():
    alpha = s.Rational(1, 10)
    exponent = 4
    return {
        "alpha": alpha,
        "exponent": exponent,
        "beta": exponent * alpha,
        "fugacity": s.Rational(1, 3),
        "feedback_multiplicity": 2,
    }


def spectrum_of(eigenvalues, mask, multiplicities=None):
    count = len(eigenvalues)
    if multiplicities is None:
        multiplicities = (1,) * count
    return SimpleNamespace(
        eigenvalues=tuple(eigenvalues),
        multiplicities=tuple(multiplicities),
        shell_mask=tuple(mask),
    )


def jet(diagonal, off=()):
    return SimpleNamespace(diagonal=tuple(diagonal), off=tuple(off))


def carrier_Z(eigenvalues, calibrations, multiplicities=None):
    multiplicities = multiplicities or (1,) * len(eigenvalues)
    total = 0
    for energy, mult in zip(eigenvalues, multiplicities):
        base = 1 - calibrations["alpha"] * energy
        total += mult * base ** calibrations["exponent"]
    return s.simplify(total)


def check_provenance():
    repo = Path(__file__).resolve().parents[4]
    tangent_path = repo / "02_REGISTRY/research/sources/d0_w2_stored_tangent_2026-10-16/stored_tangent.py"
    matter_path = repo / "02_REGISTRY/research/sources/d0_w2_matter_response_2026-10-16/matter_response.py"
    require(hashlib.sha256(tangent_path.read_bytes()).hexdigest() == hz.N05_SHA256, "n05_on_main_hash")
    require(hashlib.sha256(matter_path.read_bytes()).hexdigest() == hz.N06_SHA256, "n06_on_main_hash")
    historical = {
        "02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md":
            hz.HISTORICAL_SHA256[
                "02_REGISTRY/research/A4D_NATIVE_COMPLETE_FIELD_SOURCE_AND_TRANSPORT.md"
            ],
        "02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md":
            hz.HISTORICAL_SHA256[
                "02_REGISTRY/research/A4D_NATIVE_PRICE_EXACT_VARIATIONAL_UNFOLDING.md"
            ],
        "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py":
            hz.HISTORICAL_SHA256[
                "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py"
            ],
    }
    for path, digest in historical.items():
        require(not (repo / path).exists(), "historical_not_on_main:" + path)
        require(
            hashlib.sha256(git_bytes(hz.HISTORICAL_SHA, path)).hexdigest() == digest,
            "historical_git_show:" + path,
        )
    joint = "02_REGISTRY/research/A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md"
    require(not (repo / joint).exists(), "joint_owner_not_merged")
    require(
        hashlib.sha256(git_bytes(hz.OWNER_SHA, joint)).hexdigest() == hz.JOINT_SHA256,
        "joint_owner_hash",
    )
    wave = git_bytes(
        hz.HISTORICAL_SHA,
        "02_REGISTRY/research/sources/d0_native_field_transport_2026-10-16/stored_rotational_wave.py",
    ).decode()
    require("0.089" in wave and "0.091" in wave, "pinned_wave_enclosure")
    require("full_scalar_edges" in wave, "pinned_feature_groups")


def check_v8_gauges():
    cal = hz.v8_calibrations()
    require(cal["ell"] == s.Rational(1, 8) and cal["ell_is_field"] is False, "ell_fixed_not_a_field")
    require(cal["rounds"] == 8192 and cal["exponent"] == 16384, "v8_exponent")
    require(zero(cal["beta"] - cal["alpha"] * cal["exponent"]), "beta_matches_alpha_exponent")
    require(cal["feedback_multiplicity"] == 128 and cal["fock_multiplicity"] == 16, "multiplicities_explicit")
    require(cal["shell_rank"] == 128 and cal["reference_rank"] == 128, "shell_and_reference_128")
    require(cal["workspaceDim"] == "128^8192" and cal["workspace_materialized"] is False, "workspace_not_built")
    require(cal["af_preparation_second_variation_added"] is False, "af_preparation_not_added")
    try:
        hz.refuse_dense_workspace(128, 8192)
        require(False, "dense_workspace_must_raise")
    except hz.HessianApplyError:
        require(True, "dense_workspace_refused")
    try:
        hz.refuse_shell_schur()
        require(False, "zero_block_must_raise")
    except hz.ZeroBlockError:
        require(True, "zero_shell_block_not_inverted")


def check_chart_gate():
    st = hz.tangent()
    a, b = s.Rational(1, 4), s.Rational(1, 125)
    frame = st.homogeneous_frame(a, b)
    phase = (3, 3, 0, 0)
    angle = hz.chart_gate(frame, phase, {"edge_angle[0]": 1}, 0)
    observer = hz.chart_gate(frame, phase, {"observer_nu[0]": 1}, 0)
    transverse = hz.chart_gate(frame, phase, {"leg_transverse[2][0]": 1}, 2)
    require(angle["c1_nonzero_rows"] == (), "link_angle_is_c1")
    require(observer["c1_nonzero_rows"] == (), "observer_velocity_is_c1")
    require(transverse["c1_nonzero_rows"] == (), "transverse_leg_is_c1")
    require(angle["euler_kernel"] is False, "c1_residual_is_not_an_euler_kernel")
    require(st.is_zero(angle["tangent"].dq), "pure_link_angle_has_vanishing_linear_q")
    require(not st.is_zero(angle["tangent"].dA[0]), "pure_link_angle_moves_A")
    require(not st.is_zero(transverse["first"]["q_x"]), "transverse_coefficient_moves_q")
    require(st.is_zero(angle["recovered"].sin_theta), "edge_inverse_of_edge_value")
    symmetry, mixed = hz.mixed_chart_symmetry(
        frame, 0,
        (phase, {"edge_angle[0]": 1}),
        (phase, {"observer_nu[0]": 1}),
    )
    require(all(symmetry.values()), "link_observer_mixed_jet_is_symmetric")
    require(not st.is_zero(mixed["A"]), "link_observer_cross_moves_A")
    crossed, _ = hz.mixed_chart_symmetry(
        frame, 2,
        (phase, {"leg_transverse[2][0]": 1}),
        (phase, {"observer_nu[0]": 1}),
    )
    require(all(crossed.values()), "coefficient_observer_mixed_jet_is_symmetric")
    curve = st.curve_constraint_jet(st.row_rotation_curve(a, b, (0, 0, 0, 0), 2, c=0), 2, 2)
    require(all(st.is_zero(value) for value in curve.values()), "row_wave_curve_is_c2_on_role_2")


def check_matter_consumer():
    mr = hz.matter()
    a, b = s.Rational(1, 4), s.Rational(1, 125)
    family = mr.row_wave_family(a, b)
    response = hz.rational_matter_term(a, b)
    require(response["scope"] == "stored_rotational_row_wave", "n06_row_wave_scope")
    require(
        zero(response["second_source"]["matter_eliminated_term"] + family["gamma"] / 4),
        "n06_matter_term_is_minus_gamma_over_4",
    )
    require(response["lower_saddle_block_inverted"] is False, "n06_did_not_invert_the_shell_block")
    require(response["field_shell_kernel_solved"] is False, "kernel_not_taken_from_n06")
    require(family["thermal_recomputed"] is False, "n06_did_not_replace_the_thermal_sum")
    d, o, rotated = family["d"], family["o"], family["rotated_norm_squared"]
    cross = s.sqrt((d - o) * (d + 3 * o))
    require(zero((3 * d - o + cross) / 4 - rotated), "rotation_norm_matches_n06_frame")
    tables = hz.fourier_feature_groups()
    require(all(not edge["partner_is_shell"] for edge in tables["shell_edges"]), "row_wave_partners_leave_the_shell")
    require(len(tables["shell_edges"]) == 16, "eight_shell_modes_two_signs")
    try:
        mr.pure16_native_reduction(16, 16)
        require(False, "pure16_must_raise")
    except mr.MatterResponseError:
        require(True, "pure16_reduction_refused")


def check_divided_difference_and_polarization():
    cal = fixture_calibrations()
    lam = s.Rational(1, 5)
    Z = s.Integer(3)
    variable = s.symbols("lam")
    heat, program, heat_prime, program_prime, _short = hz.spectral_weights(variable, cal, Z)
    require(zero(heat_prime - s.diff(heat, variable)), "heat_derivative_is_the_coincident_limit")
    require(zero(program_prime - s.diff(program, variable)), "program_derivative_is_the_coincident_limit")
    left = hz.spectral_weights(lam, cal, Z)
    right = hz.spectral_weights(lam, cal, Z)
    require(
        hz.divided_difference(left[0], right[0], lam, lam, left[2]) == left[2],
        "equal_eigenvalues_return_the_derivative",
    )
    other = s.Rational(2, 5)
    far = hz.spectral_weights(other, cal, Z)
    gap = hz.divided_difference(left[0], far[0], lam, other, left[2])
    require(zero(gap - (left[0] - far[0]) / (lam - other)), "distinct_eigenvalues_use_the_quotient")

    eigenvalues = (lam, other)
    Z_full = carrier_Z(eigenvalues, cal)
    spectrum = spectrum_of(eigenvalues, (False, False))
    rho = (s.Rational(1, 4), s.Rational(3, 4))

    def bilinear(diag_v, diag_w, accel):
        return hz.price_bilinear(
            spectrum,
            jet(diag_v),
            jet(diag_w),
            accel,
            rho,
            cal,
            Z_full,
        )

    v = (s.Rational(1, 7), s.Rational(3, 11))
    w = (s.Rational(1, 5), s.Rational(-1, 4))
    accel = (s.Rational(1, 3), s.Rational(1, 9))
    both = (v[0] + w[0], v[1] + w[1])
    bv = bilinear(v, w, (0, 0))["sum"]
    qv = bilinear(v, v, (0, 0))["sum"]
    qw = bilinear(w, w, (0, 0))["sum"]
    qboth = bilinear(both, both, (0, 0))["sum"]
    require(zero(bv - (qboth - qv - qw) / 2), "bilinear_polarization")
    require(zero(bv - bilinear(w, v, (0, 0))["sum"]), "bilinear_symmetry")
    pieces = bilinear(v, v, accel)
    require(zero(pieces["sum"] - (pieces["H"] + pieces["J_program"] + pieces["R"])), "contributions_add")
    require(not zero(pieces["normalizer"]), "diagonal_jet_sees_the_normalizer")
    frozen = hz.price_bilinear(
        spectrum, jet(v), jet(v), accel, rho, cal, Z_full,
        mutation={"omit_normalizer": True},
    )
    require(not zero(frozen["mutation_discrepancy"]), "frozen_normalizer_is_detected")
    replaced = hz.price_bilinear(
        spectrum, jet(v), jet(v), accel, rho, cal, Z_full,
        mutation={"replace_heat_by_delta": True},
    )
    require(not zero(replaced["mutation_discrepancy"]), "delta_generator_is_not_the_heat_weight")

    # Independent scalar differentiation of the same price, diagonal carrier.
    t = s.symbols("t")
    l1 = lam + t * v[0] + t ** 2 * accel[0] / 2
    l2 = other + t * v[1] + t ** 2 * accel[1] / 2

    def branch(energy):
        base = 1 - cal["alpha"] * energy
        power = base ** cal["exponent"]
        program_den = 1 - cal["fugacity"] + cal["fugacity"] * power
        return power, program_den

    p1, a1 = branch(l1)
    p2, a2 = branch(l2)
    scalar = (
        rho[0] * l1 + rho[1] * l2
        + (1 / cal["beta"]) * s.log(p1 + p2)
        - cal["feedback_multiplicity"] * (s.log(a1) + s.log(a2))
    )
    require(zero(s.diff(scalar, t, 2).subs(t, 0) - pieces["sum"]), "direct_scalar_matches_divided_differences")

    outside = hz.price_bilinear(
        spectrum_of(eigenvalues, (True, False)),
        jet(v), jet(v), accel, rho, cal, Z_full,
        mutation={"drop_off_shell_thermal": True},
    )
    require(not zero(outside["mutation_discrepancy"]), "off_shell_thermal_mode_is_detected")

    # Same contraction through N06's thermal source, one jet, no second-jet Y.
    mr = hz.matter()
    thermal = mr.thermal_feedback_source(
        list(eigenvalues),
        list(v),
        [],
        {
            "alpha": cal["alpha"],
            "exponent": cal["exponent"],
            "beta": cal["beta"],
            "fugacity": cal["fugacity"],
            "feedback_multiplicity": cal["feedback_multiplicity"],
            "Z": Z_full,
            "multiplicities": [1, 1],
        },
        shell_mask=[False, False],
    )
    quadratic = bilinear(v, v, (0, 0))
    require(
        zero(quadratic["H"] + quadratic["J_program"] - thermal["second_contraction"]),
        "n06_second_contraction_matches",
    )
    hidden = mr.thermal_feedback_source(
        list(eigenvalues), list(v), [],
        {
            "alpha": cal["alpha"],
            "exponent": cal["exponent"],
            "beta": cal["beta"],
            "fugacity": cal["fugacity"],
            "feedback_multiplicity": cal["feedback_multiplicity"],
            "Z": Z_full,
        },
        shell_mask=[False, True],
        drop_outside_shell=True,
    )
    require(not zero(hidden["outside_shell_diagonal_contribution"]), "n06_outside_shell_term_is_visible")


def check_dirac_and_curvature():
    cal = fixture_calibrations()
    D = s.diag(1, 2)
    dD = s.Matrix([[0, 1], [1, 0]])
    X, _, Y = hz.dirac_delta_jets(D, dD, dD, s.zeros(2))
    t = s.symbols("t")
    Delta = s.simplify((D + t * dD) ** 2)
    require(zero(s.diff(Delta, t).subs(t, 0) - X), "first_dirac_jet_matches_anticommutator")
    require(zero(s.diff(Delta, t, 2).subs(t, 0) - Y), "second_dirac_jet_matches_anticommutator")
    rho = s.diag(s.Rational(1, 4), s.Rational(3, 4))
    Z = carrier_Z((1, 4), cal)
    action = hz.apply_hessian(
        {
            "kind": "dirac",
            "D": D,
            "dD_v": dD,
            "dD_w": dD,
            "d2D": s.zeros(2),
            "rho": rho,
            "shell_mask": (False, False),
            "Z": Z,
        },
        calibrations=cal,
    )
    Kt = (s.eye(2) - cal["alpha"] * Delta) ** cal["exponent"]
    At = (1 - cal["fugacity"]) * s.eye(2) + cal["fugacity"] * Kt
    scalar = (
        s.trace(rho * Delta)
        + (1 / cal["beta"]) * s.log(s.trace(Kt))
        - cal["feedback_multiplicity"] * s.log(At.det())
    )
    require(zero(s.diff(scalar, t, 2).subs(t, 0) - action["sum"]), "noncommuting_direct_matches_schur_form")
    require(action["lower_block_inverted"] is False, "dirac_path_does_not_invert_shell")
    require(action["kernel_classified"] is False, "dirac_path_does_not_classify_kernel")

    acceleration = s.diag(s.Rational(1, 3), 0)
    curved = hz.apply_hessian(
        {
            "kind": "dirac",
            "D": D,
            "dD_v": dD,
            "dD_w": dD,
            "d2D": acceleration,
            "rho": rho,
            "shell_mask": (False, False),
            "Z": Z,
        },
        calibrations=cal,
    )
    # The coordinate Hessian already contains {dD, dD}. Only {D, d²D} is new.
    Y_acc = hz.dirac_delta_jets(D, s.zeros(2), s.zeros(2), acceleration)[2]
    accel_diagonal = (Y_acc[0, 0], Y_acc[1, 1])
    extra = hz.first_source(
        spectrum_of((1, 4), (False, False)),
        accel_diagonal,
        (rho[0, 0], rho[1, 1]),
        cal,
        Z,
    )
    compared = hz.curve_versus_coordinate(
        action["sum"], accel_diagonal,
        spectrum_of((1, 4), (False, False)),
        (rho[0, 0], rho[1, 1]), cal, Z,
    )
    require(not zero(extra), "acceleration_term_survives_off_criticality")
    require(zero(curved["sum"] - action["sum"] - extra), "curve_second_keeps_the_acceleration")
    require(compared["acceleration_vanishes_automatically"] is False, "acceleration_is_not_discarded")


def check_auxiliary_and_matter_schur():
    cal = fixture_calibrations()
    lam1, lam2 = s.Rational(1, 5), s.Rational(2, 5)
    v1, v2 = s.Rational(1, 7), s.Rational(3, 11)
    a1, a2 = s.Rational(1, 3), s.Rational(1, 9)
    t = s.symbols("t")
    l1 = lam1 + t * v1 + t ** 2 * a1 / 2
    l2 = lam2 + t * v2 + t ** 2 * a2 / 2

    def K_of(energy):
        return (1 - cal["alpha"] * energy) ** cal["exponent"]

    def A_of(energy):
        return 1 - cal["fugacity"] + cal["fugacity"] * K_of(energy)

    heat = hz.auxiliary_sigma_schur({
        "beta": cal["beta"],
        "K1": K_of(lam1), "K2": K_of(lam2),
        "dK1": s.diff(K_of(l1), t).subs(t, 0),
        "dK2": s.diff(K_of(l2), t).subs(t, 0),
        "d2K1": s.diff(K_of(l1), t, 2).subs(t, 0),
        "d2K2": s.diff(K_of(l2), t, 2).subs(t, 0),
    })
    require(heat["block_invertible"] is True, "heat_block_is_invertible")
    require(zero(heat["direct"] - heat["frozen_plus_correction"]), "heat_direct_matches_correction")
    require(zero(heat["direct"] - heat["schur_complement"]), "heat_direct_matches_block_inverse")
    program = hz.auxiliary_program_schur({
        "M": cal["feedback_multiplicity"],
        "A1": A_of(lam1), "A2": A_of(lam2),
        "dA1": s.diff(A_of(l1), t).subs(t, 0),
        "dA2": s.diff(A_of(l2), t).subs(t, 0),
        "d2A1": s.diff(A_of(l1), t, 2).subs(t, 0),
        "d2A2": s.diff(A_of(l2), t, 2).subs(t, 0),
    })
    require(program["block_invertible"] is True, "program_block_is_invertible")
    require(zero(program["direct"] - program["schur_complement"]), "program_direct_matches_block_inverse")
    require(heat["lower_shell_block_inverted"] is False, "auxiliary_schur_is_not_the_shell_block")

    # Indefinite resolvent: shell energy 2, Q energies 0 and 5.
    eigenvalues = (0, 2, 5)
    mask = (False, True, False)
    X = s.zeros(3)
    X[0, 1] = X[1, 0] = 1
    X[1, 2] = X[2, 1] = 1
    Y = s.diag(s.Rational(1, 5), s.Rational(1, 7), s.Rational(1, 11))
    symbol = hz._as_symbol(X)
    spectrum = spectrum_of(eigenvalues, mask)
    Z = carrier_Z(eigenvalues, cal)
    rho = (0, 1, 0)
    price = hz.price_bilinear(
        spectrum, symbol, symbol, tuple(Y[i, i] for i in range(3)), rho, cal, Z,
        epsilon=2, shell_rank=1,
    )
    v0 = s.Matrix([0, 1, 0])
    resolvent = s.diag(-2, 0, 3)
    image = -(X * v0)
    v1 = s.Matrix([image[0] / resolvent[0, 0], 0, image[2] / resolvent[2, 2]])
    perturbation = (v0.T * Y * v0)[0] + 2 * (v0.T * X * v1)[0]
    require(zero(price["R"] - perturbation), "matter_schur_matches_direct_perturbation")
    require(s.simplify(price["resolvent_R"]) > 0, "indefinite_sides_do_not_cancel")
    dropped = hz.price_bilinear(
        spectrum, symbol, symbol, tuple(Y[i, i] for i in range(3)), rho, cal, Z,
        epsilon=2, shell_rank=1, mutation={"drop_negative_resolvent": True},
    )
    require(not zero(dropped["mutation_discrepancy"]), "negative_resolvent_mode_is_detected")
    v1_drop = s.Matrix([0, 0, image[2] / resolvent[2, 2]])
    dropped_perturbation = (v0.T * Y * v0)[0] + 2 * (v0.T * X * v1_drop)[0]
    require(not zero(perturbation - dropped_perturbation), "direct_perturbation_sees_the_negative_mode")

    # Preparation couples only through T*. A traceless shell value on this
    # single shell mode cannot be nonzero, so use two shell slots.
    shell_eigen = (s.Rational(1, 2), s.Rational(1, 2), s.Integer(3))
    shell_mask = (True, True, False)
    shell_spectrum = spectrum_of(shell_eigen, shell_mask)
    shell_Z = carrier_Z(shell_eigen, cal)
    diag = (s.Rational(1, 2), s.Rational(-1, 6), 0)
    coupling = ((2, 0, s.Rational(1, 4)), (0, 2, s.Rational(1, 4)))
    base = hz.price_bilinear(
        shell_spectrum, jet(diag, coupling), jet(diag, coupling),
        (0, 0, 0), (s.Rational(1, 2), s.Rational(1, 2), 0), cal, shell_Z,
        epsilon=s.Rational(1, 2), shell_rank=2,
    )
    shell = (1, -1)
    linear = hz.saddle_bilinear(base, shell, (0, 0), jet(diag, coupling), jet(diag, coupling), shell_spectrum)
    bare = hz.saddle_bilinear(base, (0, 0), (0, 0), jet(diag, coupling), jet(diag, coupling), shell_spectrum)
    require(not zero(linear["linear_action"] - bare["linear_action"]), "preparation_cross_term")
    doubled = hz.saddle_bilinear(base, (2, -2), (0, 0), jet(diag, coupling), jet(diag, coupling), shell_spectrum)
    require(zero(doubled["shell_cross"] - 2 * linear["shell_cross"]), "shell_response_is_linear")
    quadratic = hz.saddle_bilinear(base, shell, shell, jet(diag), jet(diag), shell_spectrum)
    left = hz.saddle_bilinear(base, shell, (0, 0), jet(diag), jet(diag), shell_spectrum)
    right = hz.saddle_bilinear(base, (0, 0), shell, jet(diag), jet(diag), shell_spectrum)
    origin = hz.saddle_bilinear(base, (0, 0), (0, 0), jet(diag), jet(diag), shell_spectrum)
    require(
        zero(quadratic["linear_action"] - left["linear_action"] - right["linear_action"] + origin["linear_action"]),
        "no_quadratic_lower_block",
    )
    swapped_diag = (s.Rational(-1, 6), s.Rational(1, 2), 0)
    other_shell = (s.Rational(1, 2), s.Rational(-1, 2))
    forward_price = hz.price_bilinear(
        shell_spectrum, jet(diag, coupling), jet(swapped_diag, coupling),
        (0, 0, 0), (s.Rational(1, 2), s.Rational(1, 2), 0),
        cal, shell_Z, epsilon=s.Rational(1, 2), shell_rank=2,
    )
    backward_price = hz.price_bilinear(
        shell_spectrum, jet(swapped_diag, coupling), jet(diag, coupling),
        (0, 0, 0), (s.Rational(1, 2), s.Rational(1, 2), 0),
        cal, shell_Z, epsilon=s.Rational(1, 2), shell_rank=2,
    )
    forward = hz.saddle_bilinear(
        forward_price, shell, other_shell,
        jet(diag, coupling), jet(swapped_diag, coupling), shell_spectrum,
    )
    backward = hz.saddle_bilinear(
        backward_price, other_shell, shell,
        jet(swapped_diag, coupling), jet(diag, coupling), shell_spectrum,
    )
    require(zero(forward["linear_action"] - backward["linear_action"]), "real_pairing_adjoint")
    try:
        hz.shell_pairing((1, 0), diag, shell_mask, (1, 1, 1))
        require(False, "traceful_shell_must_raise")
    except hz.HessianApplyError:
        require(True, "traceful_shell_multiplier_rejected")

    # Complex Fourier pair: the declared pairing is the real part.
    imag = s.I
    left_off = ((0, 1, 1 + imag), (1, 0, 1 - imag))
    right_off = ((0, 1, 2), (1, 0, 2))
    complex_spectrum = spectrum_of((s.Rational(1, 5), s.Rational(2, 5)), (False, False))
    complex_Z = carrier_Z(complex_spectrum.eigenvalues, cal)
    cross = hz.price_bilinear(
        complex_spectrum, jet((0, 0), left_off), jet((0, 0), right_off),
        (0, 0), (0, 0), cal, complex_Z,
    )
    cross_back = hz.price_bilinear(
        complex_spectrum, jet((0, 0), right_off), jet((0, 0), left_off),
        (0, 0), (0, 0), cal, complex_Z,
    )
    require(zero(cross["sum"] - cross_back["sum"]), "complex_fourier_pairing_is_real_symmetric")
    require(cross["sum"].is_real, "complex_pairing_lands_in_the_real_chart")


def check_interval_and_apply():
    import mpmath as mp

    result = hz.apply_hessian({"kind": "row_wave", "digits": 25})
    require(result["root_solved"] is False, "no_new_root_solve")
    require(result["midpoint_used_as_root"] is False, "midpoint_is_not_a_root")
    require(result["thermal_modes"] == 4096, "all_4096_modes")
    require(result["directed_edges"] == 8192, "all_8192_directed_edges")
    require(result["scalar_groups"] == 1061, "feature_group_count")
    require(result["equal_energy_edges"] == 1248, "exact_equal_energy_edges")
    require(result["nonzero_gap_edges"] == 6944, "exact_nonzero_gap_edges")
    require(result["fock_multiplicity"] == 16 and result["feedback_multiplicity"] == 128, "interval_multiplicities")
    total = result["sum"]
    require(total.a > mp.mpf("0.089") and total.b < mp.mpf("0.091"), "positive_directional_bound")
    require(result["H"].a > 0 and result["J_program"].b < 0 and result["R"].b < 0, "signed_H_J_R_split")
    require(mp.mpf(result["rectangle"]["d"][0]) < mp.mpf(result["rectangle"]["d"][1]), "rectangle_has_width")
    mutated = hz.apply_hessian(
        {"kind": "row_wave", "digits": 25},
        mutation={"drop_off_shell_thermal": True},
    )
    require(not (mutated["mutation_discrepancy"].a <= 0 <= mutated["mutation_discrepancy"].b),
            "row_wave_off_shell_thermal_mutation_detected")
    require(result["lower_block_inverted"] is False, "row_wave_shell_block_not_inverted")
    require(result["kernel_classified"] is False, "row_wave_kernel_not_classified")
    require(result["gr_derived"] is False and result["physical_admission"] is False, "no_physical_claim")
    require(result["af_preparation_second_variation_added"] is False, "row_wave_omits_af_preparation")
    require(result["preparation_couples_this_wave"] is False, "this_wave_has_vanishing_shell_residual")
    # Endpoint objects are intervals. Compare them in a high fixed context,
    # not at the default 15-digit mpf precision.
    mp.mp.dps = 50
    lower = mp.mpf(total.a)
    upper = mp.mpf(total.b)
    require(
        lower > mp.mpf("0.08996033839979331495")
        and upper < mp.mpf("0.08996033878441452448"),
        "interval_inside_published_printed_enclosure",
    )
    def ends(interval):
        return [
            mp.nstr(mp.mpf(interval.a), 25, strip_zeros=False),
            mp.nstr(mp.mpf(interval.b), 25, strip_zeros=False),
        ]

    return {
        "sum": ends(total),
        "H": ends(result["H"]),
        "J_program": ends(result["J_program"]),
        "R": ends(result["R"]),
    }


def main():
    check_provenance()
    check_v8_gauges()
    check_chart_gate()
    check_matter_consumer()
    check_divided_difference_and_polarization()
    check_dirac_and_curvature()
    check_auxiliary_and_matter_schur()
    interval = check_interval_and_apply()
    payload = {
        "status": "PASS",
        "exact_checks": len(CHECKS),
        "real_chart": hz.REAL_CHART,
        "callable": "apply_hessian",
        "interval": interval,
        "kernel_classified": False,
        "lower_block_inverted": False,
        "gr_derived": False,
    }
    json.dump(payload, sys.stdout, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as exc:
        sys.stderr.write("FAIL %s\n" % exc)
        raise SystemExit(1)
