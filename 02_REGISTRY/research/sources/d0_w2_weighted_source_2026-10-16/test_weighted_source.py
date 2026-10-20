#!/usr/bin/env python3
"""Decisive checks for the supplied site-weight transport.

Positive controls: both endpoint factors, the counting adjoint, unitary
transport in the weighted Gram, and invariance of the scalar price under a
simultaneous frame change. Negative controls: a one-sided frozen weight and
a unitary claim in the unweighted counting space.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

import weighted_source as w

FAILURES: list[str] = []


def check(name: str, cond: bool) -> None:
    print(("PASS " if cond else "FAIL ") + name)
    if not cond:
        FAILURES.append(name)


def e(index: int) -> np.ndarray:
    vector = np.zeros(4)
    vector[index] = 1.0
    return vector


def eye_links(count: int) -> list[np.ndarray]:
    return [np.eye(4) for _ in range(count)]


def near(matrix: np.ndarray, bound: float) -> bool:
    return w.max_abs(matrix) <= bound


def exact_blocks(blocks: list[np.ndarray], expected: list[float]) -> bool:
    identity = np.eye(w.FIBER)
    for block, factor in zip(blocks, expected):
        if w.max_abs(block - factor * identity) > 1e-12:
            return False
    return True


def reject_nonpositive_weight() -> None:
    raised = False
    try:
        w.endpoint_factor(1.0, 0.0)
    except ValueError:
        raised = True
    check("nonpositive_weight_rejected", raised)


def exterior_and_gamma() -> None:
    root = np.diag([2.0, 3.0, 1.0, 5.0])
    lifted = w.exterior_lift(root)
    for mask in range(w.FIBER):
        factor = 1.0
        for role in range(4):
            if mask & (1 << role):
                factor *= root[role, role]
        if abs(lifted[mask, mask] - factor) > 1e-12:
            check("exterior_diagonal_minors", False)
            return
        if np.max(np.abs(lifted[mask, :])) > abs(factor) + 1e-12 and mask != 0:
            off = lifted[mask].copy()
            off[mask] = 0.0
            if w.max_abs(off) > 1e-12:
                check("exterior_diagonal_minors", False)
                return
    check("exterior_diagonal_minors", True)
    generator = np.diag([0.5, -1.0, 2.0, 0.0])
    gamma = w.gamma_action(generator)
    for mask in range(w.FIBER):
        weight = sum(generator[role, role] for role in range(4) if mask & (1 << role))
        column = np.zeros(w.FIBER)
        column[mask] = weight
        if w.max_abs(gamma[:, mask] - column) > 1e-12:
            check("gamma_diagonal_weights", False)
            return
    check("gamma_diagonal_weights", True)
    shear = np.array(
        [[0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 0.0]]
    )
    step = 1e-7
    difference = (w.exterior_lift(np.eye(4) + step * shear) - np.eye(w.FIBER)) / step
    check("gamma_matches_exterior_derivative", near(difference - w.gamma_action(shear), 1e-6))
    phase = w.acdb_phase()
    check("acdb_phase_is_involutory", near(phase @ phase - np.eye(w.FIBER), 0.0))
    vector = np.array([0.5, -0.25, 1.0, 2.0])
    root = np.diag([2.0, 1.0, 4.0, 0.5])
    lifted_root = w.exterior_lift(root)
    conjugated = lifted_root @ w.creation(vector) @ np.linalg.inv(lifted_root)
    check("creation_intertwines_square_root", near(conjugated - w.creation(root @ vector), 1e-10))
    metric = root.T @ root
    lowered = np.linalg.inv(lifted_root) @ w.contraction(root @ vector) @ lifted_root
    check("contraction_intertwines_metric_leg", near(lowered - w.contraction(metric @ vector), 1e-10))


def two_node_endpoint_and_adjoint() -> None:
    omega = [4.0, 1.0]
    links = eye_links(2)
    blocks = w.endpoint_blocks(omega, links)
    check("two_node_both_endpoint_factors", exact_blocks(blocks, [2.0, 0.5]))
    shift = w.cycle_transport(blocks)
    inverse = w.cycle_inverse(blocks)
    adjoint = w.cycle_adjoint(blocks)
    check("two_node_shift_inverse_matches_matrix_inverse", near(inverse - np.linalg.inv(shift), 1e-12))
    check("two_node_shift_adjoint_matches_transpose", near(adjoint - shift.T, 1e-12))
    # On this 2-cycle the product of the factors is 1, so S^{-1} = S, while S* swaps the factors.
    check("two_node_inverse_is_not_the_adjoint", not near(adjoint - inverse, 1e-8))
    ratio = omega[0] / omega[1]
    # (S* psi)(source) = (omega_arrival/omega_source) (S^{-1} psi)(source) for orthogonal O.
    scaled = np.zeros_like(inverse)
    scaled[w.FIBER :, : w.FIBER] = ratio * inverse[w.FIBER :, : w.FIBER]
    scaled[: w.FIBER, w.FIBER :] = (1.0 / ratio) * inverse[: w.FIBER, w.FIBER :]
    check("two_node_adjoint_is_weight_ratio_times_inverse", near(adjoint - scaled, 1e-12))
    check("false_unweighted_unitary_on_inhomogeneous_shift", not w.counting_unitary(shift))
    frozen_source = w.frozen_endpoint_blocks(omega, links, "freeze_source")
    frozen_arrival = w.frozen_endpoint_blocks(omega, links, "freeze_arrival")
    absolute = w.frozen_endpoint_blocks(omega, links, "absolute_arrival_only")
    check("one_sided_freeze_source_differs", not exact_blocks(frozen_source, [2.0, 0.5]))
    check("one_sided_freeze_arrival_differs", not exact_blocks(frozen_arrival, [2.0, 0.5]))
    check("absolute_arrival_factor_differs", not exact_blocks(absolute, [2.0, 0.5]))
    check("frozen_source_is_unweighted_shift", exact_blocks(frozen_source, [1.0, 1.0]))
    phase = w.acdb_phase()
    bridged = [phase @ block @ phase for block in blocks]
    check("site_independent_bridge_keeps_endpoint_factors", exact_blocks(bridged, [2.0, 0.5]))


def three_node_adjoint_not_inverse() -> None:
    omega = [4.0, 1.0, 1.0]
    blocks = w.endpoint_blocks(omega, eye_links(3))
    check("three_node_endpoint_factors", exact_blocks(blocks, [2.0, 1.0, 0.5]))
    shift = w.cycle_transport(blocks)
    inverse = np.linalg.inv(shift)
    check("three_node_inverse_differs_from_shift", not near(inverse - shift, 1e-8))
    check("three_node_adjoint_matches_transpose", near(w.cycle_adjoint(blocks) - shift.T, 1e-12))
    check("three_node_adjoint_differs_from_inverse", not near(shift.T - inverse, 1e-8))
    check("false_unweighted_unitary_on_three_node", not w.counting_unitary(shift))


def self_adjoint_law_controls() -> None:
    omega = [4.0, 1.0]
    orthogonal = eye_links(2)
    equal_legs = [e(0), e(0)]
    weighted_legs = [e(0), 4.0 * e(0)]
    for arrival, linear in enumerate(orthogonal):
        source = (arrival + 1) % 2
        law = w.edge_self_adjoint_law(
            linear, equal_legs[arrival], equal_legs[source], omega[arrival], omega[source]
        )
        check(f"equal_legs_fail_inhomogeneous_law_{arrival}", law["holds"] is False)
        good = w.edge_self_adjoint_law(
            linear, weighted_legs[arrival], weighted_legs[source], omega[arrival], omega[source]
        )
        check(f"weighted_legs_satisfy_law_{arrival}", good["holds"] is True and abs(good["kappa"] - 1.0) < 1e-12)
    equal_dirac = w.whitened_literal_dirac(equal_legs, w.endpoint_blocks(omega, orthogonal), 1.0)
    weighted_dirac = w.whitened_literal_dirac(
        weighted_legs, w.endpoint_blocks(omega, orthogonal), 1.0
    )
    check("literal_equal_legs_not_weighted_symmetric", not near(equal_dirac - equal_dirac.T, 1e-8))
    check("weighted_leg_literal_is_symmetric", near(weighted_dirac - weighted_dirac.T, 1e-10))
    habit = w.forced_adjoint_completion(equal_legs, w.endpoint_blocks(omega, orthogonal), 1.0)
    check("habit_d_plus_d_dagger_changes_literal_operator", not near(habit - equal_dirac, 1e-8))
    naive = w.naive_inverse_swap(weighted_legs, w.endpoint_blocks(omega, orthogonal), 1.0)
    check("symmetric_literal_is_not_the_naive_inverse_swap", not near(naive - weighted_dirac, 1e-8))
    constant = w.whitened_literal_dirac(equal_legs, w.endpoint_blocks([3.0, 3.0], orthogonal), 1.0)
    check("constant_weight_restores_unweighted_legs", near(constant - constant.T, 1e-10))
    check("constant_weight_shift_is_counting_unitary", w.counting_unitary(w.cycle_transport(w.endpoint_blocks([3.0, 3.0], orthogonal))))
    # kappa != 1. O = diag(2,1,1,1) on 0←1 and its inverse on 1←0.
    stretched = np.diag([2.0, 1.0, 1.0, 1.0])
    inverse = np.diag([0.5, 1.0, 1.0, 1.0])
    linears = [stretched, inverse]
    legs = [e(0), 8.0 * e(0)]
    for arrival, linear in enumerate(linears):
        source = (arrival + 1) % 2
        law = w.edge_self_adjoint_law(linear, legs[arrival], legs[source], omega[arrival], omega[source])
        check(f"kappa_exception_holds_{arrival}", law["holds"] is True)
    check("kappa_at_arrival_is_four", abs(w.edge_self_adjoint_law(stretched, legs[0], legs[1], 4.0, 1.0)["kappa"] - 4.0) < 1e-12)
    kappa_dirac = w.whitened_literal_dirac(legs, w.endpoint_blocks(omega, linears), 8.0)
    check("kappa_exception_literal_is_symmetric", near(kappa_dirac - kappa_dirac.T, 1e-9))
    bad_legs = [e(0), 8.0 * e(0) + e(1)]
    bad = w.whitened_literal_dirac(bad_legs, w.endpoint_blocks(omega, linears), 8.0)
    check("leaving_the_kappa_axis_breaks_symmetry", not near(bad - bad.T, 1e-8))
    identity = w.fibre_adjoint_identity(stretched, legs[0], legs[1], 4.0, 1.0)
    check("fibre_identity_holds_on_all_degrees", near(identity, 1e-10))
    broken = w.fibre_adjoint_identity(stretched, equal_legs[0], equal_legs[1], 4.0, 1.0)
    check("fibre_identity_fails_without_weight_ratio", not near(broken, 1e-8))
    frozen = w.whitened_literal_dirac(legs, w.frozen_endpoint_blocks(omega, linears, "freeze_source"), 8.0)
    check("one_sided_freeze_breaks_actual_adjoint", not near(frozen - frozen.T, 1e-8))


def raw_matches_conjugate() -> None:
    # Nontrivial square roots, orthogonal whitened O, inhomogeneous omega.
    root_0 = np.diag([2.0, 1.0, 1.0, 1.0])
    root_1 = np.eye(4)
    metric_0 = root_0.T @ root_0
    metric_1 = np.eye(4)
    link_01 = np.diag([0.5, 1.0, 1.0, 1.0])
    link_10 = root_0.copy()
    omega = [4.0, 1.0]
    raw_legs = [0.5 * e(0), e(0)]
    raw = w.raw_stored_dirac(raw_legs, [link_01, link_10], [metric_0, metric_1], inv_ell=8.0)
    whitening = w.block_diag(w.whitening_blocks(omega, [root_0, root_1]))
    conjugated = whitening @ raw @ np.linalg.inv(whitening)
    o_01 = root_0 @ link_01 @ np.linalg.inv(root_1)
    o_10 = root_1 @ link_10 @ np.linalg.inv(root_0)
    check("whitened_links_are_orthogonal", near(o_01 - np.eye(4), 1e-12) and near(o_10 - np.eye(4), 1e-12))
    u_legs = [root_0 @ raw_legs[0], root_1 @ raw_legs[1]]
    direct = w.whitened_literal_dirac(u_legs, w.endpoint_blocks(omega, [o_01, o_10]), 8.0)
    check("raw_literal_conjugates_to_both_endpoint_shift", near(conjugated - direct, 1e-9))
    check("this_raw_literal_is_not_weighted_symmetric", not near(conjugated - conjugated.T, 1e-8))
    weighted_raw_legs = [0.5 * e(0), 4.0 * e(0)]
    weighted_raw = w.raw_stored_dirac(
        weighted_raw_legs, [link_01, link_10], [metric_0, metric_1], inv_ell=8.0
    )
    weighted_conjugated = whitening @ weighted_raw @ np.linalg.inv(whitening)
    check("weight_matched_raw_legs_conjugate_to_symmetric", near(weighted_conjugated - weighted_conjugated.T, 1e-8))
    delta_1 = raw @ raw
    delta_2 = (2.0 * raw) @ (2.0 * raw)
    singular_1 = np.linalg.svd(delta_1, compute_uv=False)
    singular_2 = np.linalg.svd(delta_2, compute_uv=False)
    ratio = float(singular_2[0] / singular_1[0])
    check("mesh_factor_scales_delta_by_inv_ell_squared", abs(ratio - 4.0) < 1e-8)


def unitary_transport_and_false_return() -> None:
    root_0 = np.diag([2.0, 1.0, 1.0, 1.0])
    root_1 = np.eye(4)
    link_01 = np.diag([0.5, 1.0, 1.0, 1.0])
    link_10 = root_0.copy()
    omega = [4.0, 1.0]
    grams = w.weighted_gram_blocks(omega, [root_0, root_1])
    corrected = w.corrected_unitary_blocks(omega, [link_01, link_10])
    transport = w.cycle_transport(corrected)
    rng = np.random.default_rng(7)
    left = rng.normal(size=2 * w.FIBER)
    right = rng.normal(size=2 * w.FIBER)
    inner = w.weighted_inner(left, right, grams)
    moved = w.weighted_inner(transport @ left, transport @ right, grams)
    check("corrected_transport_is_unitary_on_weighted_gram", abs(inner - moved) < 1e-9)
    whitening = w.block_diag(w.whitening_blocks(omega, [root_0, root_1]))
    pure = whitening @ transport @ np.linalg.inv(whitening)
    pure_shift = w.cycle_transport([np.eye(w.FIBER), np.eye(w.FIBER)])
    check("corrected_transport_conjugates_to_orthogonal_shift", near(pure - pure_shift, 1e-8))
    check("corrected_transport_returns_to_counting_unitary_shift", w.counting_unitary(pure))
    raw_shift = w.cycle_transport([w.exterior_lift(link_01), w.exterior_lift(link_10)])
    stored_conjugate = whitening @ raw_shift @ np.linalg.inv(whitening)
    weighted_shift = w.cycle_transport(w.endpoint_blocks(omega, [np.eye(4), np.eye(4)]))
    check("raw_shift_conjugates_to_endpoint_weighted_shift", near(stored_conjugate - weighted_shift, 1e-8))
    check("stored_conjugate_is_not_the_gram_unitary_transport", not near(stored_conjugate - pure, 1e-8))
    check("stored_shift_is_not_counting_unitary", not w.counting_unitary(stored_conjugate))
    vector = rng.normal(size=2 * w.FIBER)
    counting_out = np.linalg.norm(np.linalg.inv(whitening) @ vector)
    counting_in = np.linalg.norm(vector)
    check("false_unweighted_unitary_return", abs(counting_out - counting_in) > 1e-6)
    weighted_out = w.weighted_inner(np.linalg.inv(whitening) @ vector, np.linalg.inv(whitening) @ vector, grams)
    check("return_is_unitary_between_gram_spaces", abs(weighted_out - float(vector @ vector)) < 1e-8)
    identity_norm = float(vector @ vector)
    weighted_norm = w.weighted_inner(vector, vector, grams)
    check("weighted_norm_is_not_the_counting_norm", abs(weighted_norm - identity_norm) > 1e-6)


def observer_commutator() -> None:
    dlog = 2.0
    root = np.eye(4)
    velocity = np.diag([1.0, 0.0, 0.0, 0.0])
    generator = w.observer_generator(dlog, root, velocity)
    expected = 0.5 * dlog * np.eye(w.FIBER) + w.gamma_action(velocity)
    check("observer_generator_adds_dlog_and_gamma", near(generator - expected, 1e-12))
    step = 1e-6
    moved = math.sqrt(4.0) * w.exterior_lift(root + step * velocity)
    base = math.sqrt(4.0) * w.exterior_lift(root)
    # omega fixed in this difference; dlog part is checked separately below.
    metric_only = w.observer_generator(0.0, root, velocity)
    difference = (math.sqrt(4.0) * w.exterior_lift(root + step * velocity) - base) / step
    check("square_root_velocity_matches_gamma", near(difference - math.sqrt(4.0) * metric_only, 1e-5))
    # omega(t) = 4*(1+t)^2, d/dt log omega at 0 is 2. L fixed.
    def whitening_at(t: float) -> np.ndarray:
        weight = 4.0 * (1.0 + t) ** 2
        return math.sqrt(weight) * np.eye(w.FIBER)

    derivative = (whitening_at(step) - whitening_at(-step)) / (2.0 * step)
    weight_generator = w.observer_generator(2.0, root, np.zeros((4, 4)))
    check("dlog_omega_matches_whitening_derivative", near(derivative - weight_generator @ whitening_at(0.0), 1e-6))
    omega = [4.0, 1.0]
    blocks = w.endpoint_blocks(omega, eye_links(2))
    shift = w.cycle_transport(blocks)
    log_gradient = [2.0, 0.0]
    generator_blocks = [
        w.observer_generator(log_gradient[index], np.eye(4), np.zeros((4, 4))) for index in range(2)
    ]
    full = w.block_diag(generator_blocks)
    bracket = w.commutator(full, shift)
    edge_0 = w.edge_log_derivative(2.0, 0.0)
    edge_1 = w.edge_log_derivative(0.0, 2.0)
    expected_bracket = shift.copy()
    expected_bracket[: w.FIBER, w.FIBER :] *= edge_0
    expected_bracket[w.FIBER :, : w.FIBER] *= edge_1
    check("edge_dlog_commutator", near(bracket - expected_bracket, 1e-12))
    check("edge_jets_are_opposite", abs(edge_0 - 1.0) < 1e-12 and abs(edge_1 + 1.0) < 1e-12)


def price_frame_and_physical_law() -> None:
    omega = [4.0, 1.0]
    legs = [e(0), 4.0 * e(0)]
    operator = w.whitened_literal_dirac(legs, w.endpoint_blocks(omega, eye_links(2)), inv_ell=1.0)
    check("price_carrier_is_symmetric", near(operator - operator.T, 1e-10))
    delta_norm = float(np.linalg.norm(operator @ operator, ord=2))
    alpha = 0.2 / max(delta_norm, 1.0)
    m = 2
    z = 0.25
    C = 11.0
    M = 128.0
    size = operator.shape[0]
    rho = np.eye(size) / size
    base = w.scalar_price(operator, rho, alpha=alpha, m=m, z=z, C=C, M=M)
    check("sigma_trace_is_one", abs(base["sigma_trace"] - 1.0) < 1e-10)
    check("C_and_M_stay_external", base["C"] == C and base["M"] == M)
    kernel_trace = base["Z_raw"]
    weight_sum = float(sum(omega))
    check("raw_trace_is_not_the_weight_sum", abs(kernel_trace - weight_sum) > 1e-6)
    check("raw_trace_is_not_weight_times_fibre", abs(kernel_trace - weight_sum * w.FIBER) > 1e-6)
    # Build K explicitly to read site masses of the normalized survival state.
    survival = np.eye(size) - alpha * (operator @ operator)
    kernel = np.linalg.matrix_power(survival, m)
    sigma = kernel / np.trace(kernel)
    masses = w.site_masses(sigma, 2)
    probabilities = np.asarray(omega, dtype=float)
    probabilities /= probabilities.sum()
    check("normalized_sigma_is_not_the_site_weight_probability", float(np.linalg.norm(masses - probabilities)) > 1e-6)
    check("site_masses_still_sum_to_one", abs(float(masses.sum()) - 1.0) < 1e-10)
    mutated_C = w.scalar_price(operator, rho, alpha=alpha, m=m, z=z, C=C * weight_sum, M=M)
    mutated_M = w.scalar_price(operator, rho, alpha=alpha, m=m, z=z, C=C, M=M * weight_sum)
    check("folding_weight_sum_into_C_changes_price", abs(mutated_C["S"] - base["S"]) > 1e-8)
    check("folding_weight_sum_into_M_changes_price", abs(mutated_M["S"] - base["S"]) > 1e-8)
    shear = np.eye(4)
    shear[0, 1] = 1.0
    frame = w.block_diag([w.exterior_lift(shear), w.exterior_lift(shear)])
    moved = frame @ operator @ np.linalg.inv(frame)
    moved_rho = frame @ rho @ np.linalg.inv(frame)
    # The shear is not orthogonal, so the similar matrix is not symmetric.
    # Price invariance is the cyclic trace of that similar family. The orthogonal
    # ACDB bridge is the case where the representative stays symmetric.
    phase = w.block_diag([w.acdb_phase(), w.acdb_phase()])
    bridged = phase @ operator @ phase
    bridged_price = w.scalar_price(bridged, phase @ rho @ phase, alpha=alpha, m=m, z=z, C=C, M=M)
    check("acdb_frame_preserves_scalar_price", abs(bridged_price["S"] - base["S"]) < 1e-9)
    weight_frame = w.block_diag([2.0 * np.eye(w.FIBER), 0.5 * np.eye(w.FIBER)])
    # Diagonal positive frame: similar image of a symmetric matrix need not be symmetric.
    # Reconstruct the price from the similar matrices by the cyclic identities directly.
    similar = weight_frame @ operator @ np.linalg.inv(weight_frame)
    similar_rho = weight_frame @ rho @ np.linalg.inv(weight_frame)
    similar_delta = similar @ similar
    base_delta = operator @ operator
    check(
        "weight_frame_preserves_matter_trace",
        abs(float(np.trace(similar_rho @ similar_delta)) - float(np.trace(rho @ base_delta))) < 1e-8,
    )
    base_survival = np.eye(size) - alpha * base_delta
    similar_survival = np.eye(size) - alpha * similar_delta
    base_kernel = np.linalg.matrix_power(base_survival, m)
    similar_kernel = weight_frame @ base_kernel @ np.linalg.inv(weight_frame)
    check("similarity_preserves_raw_trace", abs(float(np.trace(similar_kernel)) - float(np.trace(base_kernel))) < 1e-8)
    check(
        "similar_survival_matches_conjugated_kernel",
        near(np.linalg.matrix_power(similar_survival, m) - similar_kernel, 1e-7),
    )
    base_feedback = (1.0 - z) * np.eye(size) + z * base_kernel
    similar_feedback = weight_frame @ base_feedback @ np.linalg.inv(weight_frame)
    base_log = float(np.sum(np.log(np.linalg.eigvalsh(base_feedback))))
    similar_log = float(np.sum(np.log(np.linalg.eigvals(similar_feedback).real)))
    check("weight_frame_preserves_feedback_trace", abs(base_log - similar_log) < 1e-8)
    # The shear frame is invertible and site-independent. Its price identity is the same cyclic trace.
    shear_delta = moved @ moved
    check(
        "shear_frame_preserves_matter_trace",
        abs(float(np.trace(moved_rho @ shear_delta)) - base["R"]) < 1e-8,
    )
    # Physical weight law: legs and endpoint factors track omega. Not a similarity.
    def family(t: float) -> np.ndarray:
        weight_0 = 4.0 * (1.0 + t) ** 2
        weights = [weight_0, 1.0]
        tracked = [e(0), (weight_0 / 1.0) * e(0)]
        return w.whitened_literal_dirac(tracked, w.endpoint_blocks(weights, eye_links(2)), inv_ell=1.0)

    plus = family(1e-4)
    minus = family(-1e-4)
    finite = (plus - minus) / (2e-4)
    # Exact derivative at t=0: u1 = 4(1+t)^2 e0, alpha0 = 2(1+t), alpha1 = 1/alpha0.
    d_legs = [np.zeros(4), 8.0 * e(0)]
    d_alpha = [2.0, -0.5]
    shift_blocks = w.endpoint_blocks(omega, eye_links(2))
    d_blocks = [d_alpha[index] * np.eye(w.FIBER) for index in range(2)]
    shift = w.cycle_transport(shift_blocks)
    d_shift = w.cycle_transport(d_blocks)
    backward = w.cycle_inverse(shift_blocks)
    d_backward = -backward @ d_shift @ backward
    identity = np.eye(size)
    creators = w.local_creation(legs)
    d_creators = w.local_creation(d_legs)
    contractions = w.local_contraction(legs)
    d_contractions = w.local_contraction(d_legs)
    exact = (
        d_creators @ (shift - identity)
        + creators @ d_shift
        + d_contractions @ (backward - identity)
        + contractions @ d_backward
    )
    check("physical_weight_derivative_matches_product_rule", near(finite - exact, 1e-5))
    one_form = w.source_one_form(operator, rho, exact, np.zeros_like(rho), alpha=alpha, m=m, z=z, M=M)
    price_plus = w.scalar_price(plus, rho, alpha=alpha, m=m, z=z, C=C, M=M)["S"]
    price_minus = w.scalar_price(minus, rho, alpha=alpha, m=m, z=z, C=C, M=M)["S"]
    price_derivative = (price_plus - price_minus) / (2e-4)
    check("physical_weight_source_matches_price_derivative", abs(one_form - price_derivative) < 1e-4)
    check("physical_weight_source_is_not_zero", abs(one_form) > 1e-6)
    # Representation change: raw operator fixed, only the whitening moves.
    raw_legs = [e(0), e(0)]
    raw = w.raw_stored_dirac(raw_legs, eye_links(2), [np.eye(4), np.eye(4)], inv_ell=1.0)

    def represented(t: float) -> np.ndarray:
        weights = [4.0 * (1.0 + t) ** 2, 1.0]
        frame_t = w.block_diag(w.whitening_blocks(weights, [np.eye(4), np.eye(4)]))
        return frame_t @ raw @ np.linalg.inv(frame_t)

    represented_0 = represented(0.0)
    represented_plus = represented(1e-4)
    represented_minus = represented(-1e-4)
    represented_finite = (represented_plus - represented_minus) / (2e-4)
    generator = w.block_diag(
        [
            w.observer_generator(2.0, np.eye(4), np.zeros((4, 4))),
            w.observer_generator(0.0, np.eye(4), np.zeros((4, 4))),
        ]
    )
    check(
        "representation_derivative_is_only_the_commutator",
        near(represented_finite - w.commutator(generator, represented_0), 1e-5),
    )
    mixed = np.zeros(size)
    mixed[0] = 1.0
    mixed[w.FIBER + 3] = 2.0
    mixed /= np.linalg.norm(mixed)
    density = np.outer(mixed, mixed)
    representation_form = w.source_one_form(
        represented_0,
        density,
        w.commutator(generator, represented_0),
        w.commutator(generator, density),
        alpha=alpha,
        m=m,
        z=z,
        M=M,
    )
    check("representation_source_cancels", abs(representation_form) < 1e-7)
    eigenvalues_0 = np.linalg.eigvals(represented_0 @ represented_0)
    eigenvalues_t = np.linalg.eigvals(represented(0.05) @ represented(0.05))
    check(
        "representation_keeps_the_spectrum",
        np.allclose(np.sort(eigenvalues_0.real), np.sort(eigenvalues_t.real), atol=1e-8),
    )
    physical_0 = np.linalg.eigvalsh(operator @ operator)
    physical_t = np.linalg.eigvalsh(family(0.05) @ family(0.05))
    check(
        "physical_weight_law_moves_the_spectrum",
        float(np.linalg.norm(np.sort(physical_0) - np.sort(physical_t))) > 1e-6,
    )
    # One-sided freeze of the self-adjoint family changes the symmetric completion's price.
    frozen_blocks = w.frozen_endpoint_blocks(omega, eye_links(2), "freeze_source")
    frozen_completion = w.forced_adjoint_completion(legs, frozen_blocks, inv_ell=1.0)
    frozen_scale = float(np.linalg.norm(frozen_completion @ frozen_completion, ord=2))
    frozen_alpha = 0.2 / max(frozen_scale, 1.0)
    frozen_price = w.scalar_price(
        frozen_completion, rho, alpha=frozen_alpha, m=m, z=z, C=C, M=M
    )
    honest = w.scalar_price(operator, rho, alpha=frozen_alpha, m=m, z=z, C=C, M=M)
    check("one_sided_freeze_changes_scalar_price", abs(frozen_price["S"] - honest["S"]) > 1e-6)
    print("EXTRA_SOURCE " + w.EXTRA_SOURCE_NOT_TO_DROP)
    print(f"PHYSICAL_SOURCE {one_form:.12e}")
    print(f"PRICE {base['S']:.12e}")
    print(f"Z_RAW {base['Z_raw']:.12e}")
    print(f"SITE_MASSES {masses[0]:.12e} {masses[1]:.12e}")


def main() -> int:
    reject_nonpositive_weight()
    exterior_and_gamma()
    two_node_endpoint_and_adjoint()
    three_node_adjoint_not_inverse()
    self_adjoint_law_controls()
    raw_matches_conjugate()
    unitary_transport_and_false_return()
    observer_commutator()
    price_frame_and_physical_law()
    print(f"status = {'FAIL' if FAILURES else 'PASS'} checks_failed = {len(FAILURES)}")
    if FAILURES:
        print("failed: " + ", ".join(FAILURES))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
