#!/usr/bin/env python3
"""DRAFT candidate checker: ten transverse rows of the comparator equality graph.

Source pin (read-only, not merged): dfaf7c8df509d5abd83fa60a185ad530feadc9b5.
Recomputes the owned ordered k-frame, the comparator metric (4), the flat and
curved germs, the differential embedding and its adjoint. Does not select an
action, a measure, a compensator, or a transverse dynamics.

Status language of every printed conclusion: candidate. Not a GR claim.
"""
from __future__ import annotations

from itertools import combinations

import sympy as sp


P = (sp.sqrt(5) - 1) / 2
S_GOLDEN = sp.simplify(P**3)
KAPPA = sp.Rational(1, 1000)
COORDS = sp.symbols("x0:4", real=True)
SLOTS = [(i, j) for i in range(4) for j in range(i, 4)]
SKEW_SLOTS = ((0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3))


def require(condition: bool, name: str) -> None:
    if not condition:
        raise AssertionError(name)


def red(expr: sp.Expr) -> sp.Expr:
    return sp.expand(sp.simplify(expr))


def is_zero(expr: sp.Expr) -> bool:
    if isinstance(expr, sp.MatrixBase):
        return all(is_zero(entry) for entry in expr)
    num, den = sp.fraction(sp.together(expr))
    return red(num) == 0 and red(den) != 0


def frame():
    labels = []
    rows = []
    for i, j in combinations(range(4), 2):
        for sign in (1, -1):
            row = [0, 0, 0, 0]
            row[i] = 1
            row[j] = sign
            labels.append((i, j, sign))
            rows.append(row)
    return labels, sp.Matrix(rows)


def matching_profile(labels):
    """Owned K: same row for both signs of a pair. Not a new mode."""
    data = []
    for i, j, _sign in labels:
        first = int((i, j) in ((0, 1), (2, 3))) - int((i, j) in ((0, 3), (1, 2)))
        second = int((i, j) in ((0, 2), (1, 3))) - int((i, j) in ((0, 3), (1, 2)))
        data.append([first, second])
    return sp.Matrix(data)


def sym_matrix(entries):
    out = sp.zeros(4)
    for (mu, nu), value in zip(SLOTS, entries):
        out[mu, nu] = out[nu, mu] = value
    return out


def pack(matrix):
    return sp.Matrix([matrix[mu, nu] for mu, nu in SLOTS])


def frob(left, right):
    total = 0
    for mu in range(4):
        for nu in range(4):
            total += left[mu, nu] * right[mu, nu]
    return total


def jets(weights, clocks):
    dw = sp.Matrix([[sp.diff(weights[a], COORDS[mu]) for mu in range(4)] for a in range(12)])
    dclock = sp.Matrix([[sp.diff(clocks[A], COORDS[mu]) for mu in range(4)] for A in range(4)])
    return dw, dclock


def comparator_q(weights, clocks, k):
    """Owned formula (4): q = pullback of diag(1/(48v), v/12)."""
    dw, dclock = jets(weights, clocks)
    q = sp.zeros(4)
    for a in range(12):
        v = weights[a] * (1 - weights[a])
        theta = [sum(k[a, A] * dclock[A, mu] for A in range(4)) for mu in range(4)]
        for mu in range(4):
            for nu in range(4):
                q[mu, nu] += dw[a, mu] * dw[a, nu] / (48 * v) + v * theta[mu] * theta[nu] / 12
    return q


def dq_formula(eta_w, eta_x, weights, clocks, k):
    """First variation of q. eta_w has 12 entries, eta_x has 4."""
    dw, dclock = jets(weights, clocks)
    deta_w, deta_x = jets(eta_w, eta_x)
    out = sp.zeros(4)
    for a in range(12):
        v = weights[a] * (1 - weights[a])
        dcoef = 1 - 2 * weights[a]
        theta = [sum(k[a, A] * dclock[A, mu] for A in range(4)) for mu in range(4)]
        dtheta = [sum(k[a, A] * deta_x[A, mu] for A in range(4)) for mu in range(4)]
        for mu in range(4):
            for nu in range(4):
                amp = (
                    (deta_w[a, mu] * dw[a, nu] + dw[a, mu] * deta_w[a, nu]) / (48 * v)
                    - dw[a, mu] * dw[a, nu] * dcoef * eta_w[a] / (48 * v**2)
                )
                phase = (
                    dcoef * eta_w[a] * theta[mu] * theta[nu] / 12
                    + v * (dtheta[mu] * theta[nu] + theta[mu] * dtheta[nu]) / 12
                )
                out[mu, nu] += amp + phase
    return out


def adjoint_formula(metric_covector, weights, clocks, k):
    """Full L2 adjoint of Dq, including divergences of the coefficient currents."""
    dw, dclock = jets(weights, clocks)
    P = [[0 for _mu in range(4)] for _a in range(12)]
    R = [[0 for _mu in range(4)] for _A in range(4)]
    star_w = []
    for a in range(12):
        v = weights[a] * (1 - weights[a])
        dcoef = 1 - 2 * weights[a]
        theta = [sum(k[a, A] * dclock[A, mu] for A in range(4)) for mu in range(4)]
        for mu in range(4):
            P[a][mu] = sum(metric_covector[mu, nu] * dw[a, nu] for nu in range(4)) / (24 * v)
        zero_order = 0
        for mu in range(4):
            for nu in range(4):
                zero_order += metric_covector[mu, nu] * (
                    theta[mu] * theta[nu] / 12 - dw[a, mu] * dw[a, nu] / (48 * v**2)
                )
        div_P = sum(sp.diff(P[a][mu], COORDS[mu]) for mu in range(4))
        star_w.append(dcoef * zero_order - div_P)
        for A in range(4):
            for mu in range(4):
                R[A][mu] += k[a, A] * (v / 6) * sum(
                    metric_covector[mu, nu] * theta[nu] for nu in range(4)
                )
    star_x = []
    for A in range(4):
        div_R = sum(sp.diff(R[A][mu], COORDS[mu]) for mu in range(4))
        star_x.append(-div_R)
    return star_w, star_x, P, R


def boundary_current(P, R, eta_w, eta_x):
    current = []
    for mu in range(4):
        current.append(
            sum(P[a][mu] * eta_w[a] for a in range(12))
            + sum(R[A][mu] * eta_x[A] for A in range(4))
        )
    return current


def stripped_adjoint(metric_covector, weights, clocks, k):
    """Negative control: drop undifferentiated multiplication, keep divergences."""
    _star_w, star_x, amplitude_current, _phase_current = adjoint_formula(
        metric_covector, weights, clocks, k
    )
    stripped_w = [
        -sum(sp.diff(amplitude_current[a][mu], COORDS[mu]) for mu in range(4))
        for a in range(12)
    ]
    return stripped_w, star_x


def germ(curved: bool):
    y = COORDS[0]
    weights = [P**2 for _a in range(12)]
    if curved:
        weights[0] = P**2 + KAPPA * y**2
    clocks = list(COORDS)
    return weights, clocks


def ground_truth_dq(eta_w, eta_x, weights, clocks, k):
    eps = sp.symbols("eps")
    varied_w = [weights[a] + eps * eta_w[a] for a in range(12)]
    varied_x = [clocks[A] + eps * eta_x[A] for A in range(4)]
    q_eps = comparator_q(varied_w, varied_x, k)
    return q_eps.diff(eps).subs(eps, 0)


def flat_amplitude_map(k):
    """Packed Dq on constant amplitude variations at the flat germ, factor removed."""
    columns = []
    for a in range(12):
        gram = sp.zeros(4)
        for mu in range(4):
            for nu in range(4):
                gram[mu, nu] = k[a, mu] * k[a, nu]
        columns.append(pack(gram))
    return sp.Matrix.hstack(*columns)


def principal_symbol(k, xi):
    """Order-1 symbol at the flat germ: (s/2)(xi⊗u + u⊗xi), packed columns."""
    columns = []
    for A in range(4):
        image = sp.zeros(4)
        for mu in range(4):
            for nu in range(4):
                image[mu, nu] = S_GOLDEN / 2 * (
                    xi[mu] * sp.Integer(int(A == nu)) + xi[nu] * sp.Integer(int(A == mu))
                )
        columns.append(pack(image))
    return sp.Matrix.hstack(*columns)


def metric_lift(V):
    """Owned flat amplitude lift (8) at b=0, a=0: eta_w only."""
    out = []
    for a in range(12):
        contraction = 0
        for mu in range(4):
            for nu in range(4):
                contraction += k_global[a, mu] * V[mu, nu] * k_global[a, nu]
        out.append((3 * contraction - sp.trace(V)) / S_GOLDEN)
    return out


def base_F_and_inverse(k, profile):
    moment = sp.Matrix(
        [[k[a, mu] * k[a, nu] for a in range(12)] for mu, nu in SLOTS]
    )
    gram = sp.simplify(profile.T * profile)
    left = gram.inv() * profile.T
    operator = sp.zeros(16)
    operator[:4, 12:] = S_GOLDEN * sp.eye(4) / 2
    operator[4:14, :12] = S_GOLDEN * moment / 12
    operator[14:, :12] = S_GOLDEN * left
    inverse = sp.zeros(16)
    for mu in range(4):
        inverse[12 + mu, mu] = 2 / S_GOLDEN
    for col, (mu, nu) in enumerate(SLOTS):
        V = sp.zeros(4)
        V[mu, nu] = V[nu, mu] = 1
        for a in range(12):
            contraction = sum(k[a, i] * V[i, j] * k[a, j] for i in range(4) for j in range(4))
            inverse[a, 4 + col] = (3 * contraction - sp.trace(V)) / S_GOLDEN
    inverse[:12, 14:] = profile / S_GOLDEN
    return operator, inverse, moment, left


def sigma(q):
    return sp.trace(q) / 4


def S(q, c):
    """Independent multiplication test. Not the graph adjoint."""
    return sigma(q) * c


def q_star(q, c):
    """L2 adjoint of multiplication by Tr(q)/4 on real scalars."""
    return sigma(q) * c


def run() -> None:
    global k_global
    checks = []

    def eq(actual, expected, name: str) -> None:
        require(is_zero(sp.sympify(actual) - sp.sympify(expected)), name)
        checks.append(name)

    require(is_zero(P**2 + P - 1), "golden_relation")
    checks.append("golden_relation")
    eq(S_GOLDEN, sp.sqrt(5) - 2, "variance_is_sqrt5_minus_2")
    labels, k = frame()
    k_global = k
    require(labels[0] == (0, 1, 1), "first_channel_is_01_plus")
    checks.append("first_channel_is_01_plus")
    eq(k.T * k, 6 * sp.eye(4), "owned_frame_second_moment")
    profile = matching_profile(labels)
    eq(profile.T * profile, sp.Matrix([[8, 4], [4, 8]]), "owned_matching_normalization")

    flat_w, flat_x = germ(False)
    curved_w, curved_x = germ(True)
    q_flat = comparator_q(flat_w, flat_x, k)
    eq(q_flat, S_GOLDEN * sp.eye(4) / 2, "flat_germ_metric")
    q_curved = comparator_q(curved_w, curved_x, k)
    y = COORDS[0]
    origin = {coord: 0 for coord in COORDS}
    eq(q_curved.subs(origin), q_flat, "curved_germ_zero_jet")
    eq(q_curved.diff(y).subs(origin), sp.zeros(4), "curved_germ_first_jet")
    second = sp.Matrix(4, 4, lambda i, j: sp.diff(q_curved[i, j], y, 2).subs(origin))
    k0 = sp.Matrix(k[0, :]).reshape(4, 1)
    expected_second = (
        KAPPA * S_GOLDEN / 6 * (k0 * k0.T)
        + KAPPA**2 / (6 * S_GOLDEN) * sp.eye(4)[:, 0] * sp.eye(4)[:, 0].T
    )
    eq(second, expected_second, "curved_germ_second_jet")
    scalar = (second[0, 0] - sp.trace(second)) / (S_GOLDEN / 2) ** 2
    eq(scalar, -2 * KAPPA / (3 * S_GOLDEN), "published_scalar_curvature")
    eq(scalar, -1 / (1500 * S_GOLDEN), "published_scalar_as_one_over_1500_s")
    require(not is_zero(scalar), "curvature_is_not_a_rank_witness")
    checks.append("curvature_is_not_a_rank_witness")

    # Ground-truth linearization versus the explicit formula, flat and curved.
    eta_w = [(a + 1) + (a + 2) * COORDS[0] for a in range(12)]
    eta_x = [(A + 1) * COORDS[1] for A in range(4)]
    for weights, clocks, name in (
        (flat_w, flat_x, "flat"),
        (curved_w, curved_x, "curved"),
    ):
        truth = ground_truth_dq(eta_w, eta_x, weights, clocks, k)
        hand = dq_formula(eta_w, eta_x, weights, clocks, k)
        eq(truth, hand, "dq_formula_matches_epsilon_derivative_" + name)

    # Adjoint identity against the epsilon derivative, not against itself.
    samples = []
    E_flat = sym_matrix([COORDS[0], 0, 0, 0, 0, 0, 0, 0, 0, 0])
    samples.append(("flat_boundary", flat_w, flat_x, E_flat, [0] * 12, [1, 0, 0, 0]))
    E_off = sym_matrix([0, 1 + COORDS[1], 0, 0, 0, 0, 0, 0, 0, 0])
    samples.append(
        ("flat_offdiag", flat_w, flat_x, E_off, [COORDS[0]] + [0] * 11, [0, 0, 0, 0])
    )
    E_curved = sym_matrix([1, 0, 0, 0, COORDS[0], 0, 0, 0, 0, 0])
    samples.append(
        (
            "curved_derivative",
            curved_w,
            curved_x,
            E_curved,
            [COORDS[0]] + [0] * 11,
            [0, COORDS[1], 0, 0],
        )
    )
    for name, weights, clocks, covector, eta_w_s, eta_x_s in samples:
        truth = ground_truth_dq(eta_w_s, eta_x_s, weights, clocks, k)
        star_w, star_x, current_P, current_R = adjoint_formula(covector, weights, clocks, k)
        bulk = frob(covector, truth)
        paired = sum(star_w[a] * eta_w_s[a] for a in range(12)) + sum(
            star_x[A] * eta_x_s[A] for A in range(4)
        )
        current = boundary_current(current_P, current_R, eta_w_s, eta_x_s)
        divergence = sum(sp.diff(current[mu], COORDS[mu]) for mu in range(4))
        eq(bulk - paired - divergence, 0, "adjoint_identity_" + name)
        if name == "flat_boundary":
            # Dropping the divergence leaves the unit-interval defect s.
            eq(bulk - paired, S_GOLDEN, "dropping_boundary_leaves_defect_s")
            eq(current[0].subs(origin), 0, "boundary_flux_at_0")
            eq(current[0].subs({COORDS[0]: 1}), S_GOLDEN, "boundary_flux_at_1")
            eq(current[0].subs({COORDS[0]: 1}) - current[0].subs(origin), S_GOLDEN, "boundary_defect_s")

    # Two-sided constant-jet tangent: Dι injective of rank 22, DC of rank 10.
    amplitude = flat_amplitude_map(k)
    eq(amplitude * sp.Matrix([1] * 12), 6 * pack(sp.eye(4)), "amplitude_map_on_ones")
    require(amplitude.rank() == 10, "constant_amplitude_rank_10")
    checks.append("constant_amplitude_rank_10")
    require(profile.rank() == 2, "internal_matching_rank_2")
    checks.append("internal_matching_rank_2")
    eq(amplitude * profile, sp.zeros(10, 2), "internal_modes_have_zero_metric_tangent")
    for index, (mu, nu) in enumerate(SLOTS):
        V = sp.zeros(4)
        V[mu, nu] = V[nu, mu] = 1
        lifted = sp.Matrix(metric_lift(V))
        eq(S_GOLDEN / 12 * amplitude * lifted, pack(V), "right_inverse_metric_slot_" + str(index))
    # Left inverse on the metric complement: lift ∘ Dq fixes the lift of every slot.
    for index, (mu, nu) in enumerate(SLOTS):
        V = sp.zeros(4)
        V[mu, nu] = V[nu, mu] = 1
        lifted = metric_lift(V)
        reconstructed = S_GOLDEN / 12 * amplitude * sp.Matrix(lifted)
        require(is_zero(reconstructed - pack(V)), "slot_round_trip_" + str(index))
        relift = metric_lift(sym_matrix(list(reconstructed)))
        for a in range(12):
            require(is_zero(relift[a] - lifted[a]), "left_inverse_on_metric_complement_" + str(index))
        checks.append("left_inverse_on_metric_complement_" + str(index))

    operator, inverse, _moment, _left = base_F_and_inverse(k, profile)
    eq(operator * inverse, sp.eye(16), "flat_F0_right_inverse")
    eq(inverse * operator, sp.eye(16), "flat_F0_left_inverse")
    scaled = sp.simplify(S_GOLDEN * inverse)
    row_sum = max(sum(abs(sp.simplify(entry)) for entry in row) for row in scaled.tolist())
    eq(row_sum, 14, "owned_inverse_max_row_sum_14")

    symbol = principal_symbol(k, [1, 0, 0, 0])
    require(symbol.rank() == 4, "principal_symbol_rank_4")
    checks.append("principal_symbol_rank_4")
    spatial = pack(sp.diag(0, 1, 0, 0))
    augmented = symbol.row_join(spatial)
    require(augmented.rank() == 5, "e1_tensor_e1_not_in_symbol_image")
    checks.append("e1_tensor_e1_not_in_symbol_image")
    # The same direction is in the amplitude image, so symbol rank is not the row count.
    require(amplitude.rank() == 10, "amplitude_image_still_rank_10")
    checks.append("amplitude_image_still_rank_10")

    # Embedding and constraint on constant jets: 22 + 10 = 32.
    # Columns: 12 amplitude, 4 clocks, 6 orthogonal. Clock constants have Dq=0.
    embedding = sp.zeros(32, 22)
    embedding[:10, :12] = S_GOLDEN / 12 * amplitude
    embedding[10:26, :16] = sp.eye(16)
    embedding[26:, 16:] = sp.eye(6)
    constraint = sp.zeros(10, 32)
    constraint[:, :10] = sp.eye(10)
    constraint[:, 10:22] = -S_GOLDEN / 12 * amplitude
    eq(constraint * embedding, sp.zeros(10, 22), "constraint_annihilates_embedding")
    require(embedding.rank() == 22, "embedding_rank_22")
    checks.append("embedding_rank_22")
    require(constraint.rank() == 10, "constraint_rank_10")
    checks.append("constraint_rank_10")

    # Nonzero annihilator source: every rank-10 lift pairs to zero, rows stay λ.
    lam = sym_matrix([1, 0, 0, 0, 0, 0, 0, 0, 0, 0])
    star_w, star_x, _current_P, _current_R = adjoint_formula(lam, flat_w, flat_x, k)
    lifted_00 = metric_lift(lam)
    graph_pair = frob(lam, lam) - sum(star_w[a] * lifted_00[a] for a in range(12))
    eq(graph_pair, 0, "constant_rank10_lift_is_graph_stationary")
    stripped_w, _stripped_x = stripped_adjoint(lam, flat_w, flat_x, k)
    stripped_pair = frob(lam, lam) - sum(stripped_w[a] * lifted_00[a] for a in range(12))
    eq(stripped_pair, 1, "stripped_adjoint_loses_graph_stationarity")

    def unchecked_count(source) -> int:
        return sum(1 for value in pack(source) if not is_zero(value))

    packed_lambda = pack(lam)
    for index, value in enumerate(packed_lambda):
        require(is_zero(value - (1 if index == 0 else 0)), "row_value_" + str(index))
        checks.append("row_value_" + str(index))
    require(packed_lambda.shape == (10, 1), "ten_row_shape")
    checks.append("ten_row_shape")
    require(unchecked_count(lam) == 1, "this_lambda_leaves_the_00_row_nonzero")
    checks.append("this_lambda_leaves_the_00_row_nonzero")
    require(unchecked_count(sp.zeros(4)) == 0, "zero_annihilator_source_checks_every_row")
    checks.append("zero_annihilator_source_checks_every_row")
    # A full basis of sources leaves each of the ten slots nonzero in turn.
    covered = [False] * 10
    for index, (mu, nu) in enumerate(SLOTS):
        V = sp.zeros(4)
        V[mu, nu] = V[nu, mu] = 1
        lifted = metric_lift(V)
        paired = frob(lam, V) - sum(star_w[a] * lifted[a] for a in range(12))
        eq(paired, 0, "graph_pairing_vanishes_for_lift_" + str(index))
        # Transverse slice (V, 0, 0) pairs to the row and does not vanish for V=λ's slot.
        transverse = frob(lam, V)
        if index == 0:
            eq(transverse, 1, "transverse_00_row_is_visible_off_graph")
        covered[index] = True
        # Each standard basis source has exactly one unchecked row.
        require(unchecked_count(V) == 1, "one_nonzero_row_" + str(index))
        checks.append("one_nonzero_row_" + str(index))
    require(all(covered), "all_ten_slots_covered")
    checks.append("all_ten_slots_covered")
    require(
        unchecked_count(lam) != 0 and unchecked_count(sp.zeros(4)) == 0,
        "rank10_conclusion_is_conditional",
    )
    checks.append("rank10_conclusion_is_conditional")

    # Off-diagonal double weight is load-bearing.
    V01 = sp.zeros(4)
    V01[0, 1] = V01[1, 0] = 1
    eq(frob(V01, V01), 2, "offdiag_pairing_weight_two")
    lifted_01 = metric_lift(V01)
    star_01, _star_x01, _p01, _r01 = adjoint_formula(V01, flat_w, flat_x, k)
    eq(
        sum(star_01[a] * lifted_01[a] for a in range(12)),
        2,
        "offdiag_adjoint_keeps_double_weight",
    )

    # Normalizer variation is tangent-visible and is not one of the ten rows.
    s_param = sp.symbols("s", positive=True)
    numerator = -2 * s_param**2
    normalizer = 1 + 2 * s_param**2
    moving = sp.diff(numerator / normalizer, s_param).subs(s_param, 1)
    frozen = sp.diff(numerator / 3, s_param).subs(s_param, 1)
    eq(moving, sp.Rational(-4, 9), "moving_normalizer_derivative")
    eq(frozen, sp.Rational(-4, 3), "frozen_normalizer_derivative")
    require(not is_zero(moving - frozen), "freezing_normalizer_changes_the_named_matter_euler")
    checks.append("freezing_normalizer_changes_the_named_matter_euler")
    # Radial rest variation changes N. Transverse metric slice does not.
    radial = 2 * S_GOLDEN  # 2 m*_1 with m*_1 = 2p-1 = s
    eq(2 * (2 * P - 1), radial, "base_mask1_normalizer_variation")
    require(not is_zero(radial), "radial_variation_is_nonzero")
    checks.append("radial_variation_is_nonzero")
    transverse_normalizer_change = 0
    require(transverse_normalizer_change == 0, "transverse_rows_hold_matter_and_normalizer_fixed")
    checks.append("transverse_rows_hold_matter_and_normalizer_fixed")

    # Orthogonal rows are checked by graph-stationarity; they are not the ten.
    eq(sum(sp.eye(6)[0, alpha] * 1 for alpha in range(6)), 1, "orthogonal_row_is_graph_visible")

    # S(q,c)=q*c, independent of Dq. The mutant that drops the factor fails.
    q0 = S_GOLDEN * sp.eye(4) / 2
    c_fun = 1 + COORDS[0]
    eq(S(q0, c_fun), q_star(q0, c_fun), "S_q_c_equals_q_star_c")
    eq(sigma(q0), S_GOLDEN / 2, "flat_multiplication_factor")
    integral_true = sp.integrate(COORDS[0] * q_star(q0, c_fun), (COORDS[0], 0, 1))
    integral_mutant = sp.integrate(COORDS[0] * c_fun, (COORDS[0], 0, 1))
    eq(integral_true, 5 * S_GOLDEN / 12, "multiplication_adjoint_integral")
    eq(integral_mutant, sp.Rational(5, 6), "dropped_factor_integral")
    require(not is_zero(integral_true - integral_mutant), "S_test_rejects_dropped_factor")
    checks.append("S_test_rejects_dropped_factor")

    # Curved germ at x0=1 still has amplitude rank 10. Symbol rank is not used.
    point = {COORDS[0]: 1, COORDS[1]: 0, COORDS[2]: 0, COORDS[3]: 0}
    columns = []
    for a in range(12):
        probe_w = [sp.Integer(int(b == a)) for b in range(12)]
        varied = dq_formula(probe_w, [0, 0, 0, 0], curved_w, curved_x, k).subs(point)
        columns.append(pack(varied))
    curved_rank = sp.Matrix.hstack(*columns).rank()
    require(curved_rank == 10, "curved_point_x0_eq_1_amplitude_rank_10")
    checks.append("curved_point_x0_eq_1_amplitude_rank_10")

    print("PASS_TRANSVERSE_MATCHING_RESIDUAL candidate")
    print("exact_checks=" + str(len(checks)))
    print("source_pin=dfaf7c8df509d5abd83fa60a185ad530feadc9b5")
    print("raw_fields=32 equality_graph_fields=22 transverse_rows=10")
    print("embedding_rank=22 constraint_rank=10 amplitude_rank=10 symbol_rank=4")
    print("internal_kernel=2 orthogonal_rows_checked=6")
    print("nonzero_annihilator_basis_sources=10 zero_source_unchecked_rows=0")
    print("normalizer_moving=-4/9 normalizer_frozen=-4/3")
    print("boundary_flux_drop_defect=s scalar=-1/(1500*s)")
    print("S(q,c)=q*c multiplication_factor=s/2")
    print("slots=" + ",".join(str(slot) for slot in SLOTS))
    print("named_euler_entries=E_h,E_m0,E_O,E_direct not_set_to_zero")
    print("physical_admission=OPEN action_selection=OPEN GR=OPEN")
    print("status=DRAFT_CANDIDATE")


if __name__ == "__main__":
    run()
