#!/usr/bin/env python3
"""Exact AF/CAR role-orbit current frame; scoped kinematics, not GR closure."""
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
NOTE = '02_REGISTRY/research/A4D_NATIVE_AF_ROLE_ORBIT_CAR_GEOMETRY_2026-10-16.md'
RESULT = Path(__file__).with_name('a4d_native_af_role_orbit_metric_results.json')
INPUTS = [
    '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_check.py',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_certificate.json',
    '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_certificate.json',
    '02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_check.py',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py',
]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


AF = load('af_role_orbit_af_owner',
          '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py')
F = load('af_role_orbit_fock_owner',
         '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py')
C = load('af_role_orbit_current_owner',
         '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py')
E = load('af_role_orbit_engine_owner',
         '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py')
a, p = C.a, C.p
ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
I16 = sp.eye(16)


def check(condition, label, checks):
    if not bool(condition):
        raise AssertionError(label)
    checks.append(label)


def zero(value):
    if isinstance(value, sp.MatrixBase):
        return all(C.red(entry) == 0 for entry in value)
    return C.red(value) == 0


def active_state(scale):
    m = [E.ZERO] * 16
    m[0] = -2 * E.A * E.P
    m[1] = 2 * E.P - E.ONE
    m[13] = m[14] = E.Golden.integer(scale)
    return E.State(tuple(m))


def engine_vector(state):
    """Read the engine's canonical Z[a] coordinates in the CAR mask basis."""
    return sp.Matrix([
        C.red(sum(sp.Integer(c) * a**degree
                  for degree, c in enumerate(value.coefficients)))
        for value in state.matter
    ])


def engine_gate_matrix(sign):
    """Literal 16-component engine gate, assembled from its owned action."""
    columns = []
    for j in range(16):
        basis = [E.ZERO] * 16
        basis[j] = E.ONE
        output = E.literal_axis_gate(E.State(tuple(basis)), sign)
        columns.append(engine_vector(output))
    return sp.Matrix.hstack(*columns)


def spatial_permutation(mapping):
    S = sp.zeros(4)
    S[0, 0] = 1
    for old, new in mapping.items():
        S[new, old] = 1
    return S


def golden_current_gate():
    T = sp.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                   [0, 1, 0, 1], [0, 1, 0, -1]]) / sp.sqrt(2)
    B = F.record_basis()
    return B * sp.kronecker_product(T.T * AF.record() * T, sp.eye(4)) * B.T


def af_embedding(checks):
    frame = AF.frame(1)
    V, d = frame['V'], frame['old_dimension']
    m2_columns = (list(range(4)) + [d+i for i in range(4)] +
                  [2*d+i for i in range(4)] + [3*d+i for i in range(4)])
    V_m2 = V[:, m2_columns]
    chi = sp.Matrix([[1, 0, 0, 1], [0, 1, -sp.I, 0],
                     [0, 1, sp.I, 0], [1, 0, 0, -1]]) / sp.sqrt(2)
    T = sp.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                   [0, 1, 0, 1], [0, 1, 0, -1]]) / sp.sqrt(2)
    car_basis = F.record_basis()
    Psi = V_m2 * sp.kronecker_product(T, chi) * car_basis.T
    W, P_af, B_af, R = AF.full_operators(V, d)
    U = golden_current_gate()
    P = sp.diag(1, 1, 0, 0)
    B0 = sp.diag(1, 0, 1, 0)
    P_fock = car_basis * sp.kronecker_product(T.T * P * T, sp.eye(4)) * car_basis.T
    B_fock = car_basis * sp.kronecker_product(T.T * B0 * T, sp.eye(4)) * car_basis.T
    check(AF.zero(Psi.conjugate().T * Psi - I16),
          'actual_AF_M2_sector_is_full16_isometry', checks)
    check(AF.zero(W * Psi - Psi * U),
          'actual_AF_record_gate_intertwines_fixed_full_CAR_gate', checks)
    check(AF.zero(P_af * Psi - Psi * P_fock) and
          AF.zero(B_af * Psi - Psi * B_fock),
          'actual_AF_price_and_blank_cuts_intertwine_full16', checks)
    check(AF.zero(W.T * W - sp.eye(W.rows)) and
          AF.zero((sp.eye(W.rows) - R) * W - (sp.eye(W.rows) - R)),
          'whole_AF_gate_is_unitary_and_keeps_ambient_complement', checks)
    return Psi, W, B_fock, U, V, V_m2, d


def metric_frame(scale, gate, rotate_y, rotate_z):
    initial = engine_vector(active_state(scale))
    following = C.mat(gate * initial)
    Jy = C.mat(rotate_y * initial)
    Jz = C.mat(rotate_z * initial)
    currents = [C.current(I4, v) for v in (initial, following, Jy, Jz)]
    frame = sp.Matrix.hstack(*currents)
    gram = C.mat(frame.T * ETA * frame)
    r = sp.Rational(2 * scale * scale, 1 + 2 * scale * scale)
    expected = sp.Matrix([
        [1-r*r, 1+r*r, 1, 1],
        [1+r*r, 1-r*r, 1, 1],
        [1, 1, 1-r*r, 1],
        [1, 1, 1, 1-r*r],
    ])
    return initial, following, currents, frame, gram, expected, r


def build_result():
    checks = []
    U = golden_current_gate()
    e0 = sp.Matrix([1, 0, 0, 0])
    S_y = spatial_permutation({1: 2, 2: 3, 3: 1})
    S_z = spatial_permutation({1: 3, 2: 1, 3: 2})
    P_y, P_z = C.mat(C.C.ext(S_y)), C.mat(C.C.ext(S_z))
    check(S_y.det() == 1 and S_z.det() == 1 and
          S_y[:, 0] == e0 and S_z[:, 0] == e0,
          'two_internal_spatial_C3_maps_are_proper_and_fix_time_role', checks)
    check(zero(U.T * U - I16), 'actual_AF_CAR_gate_is_orthogonal', checks)
    check(zero(U * P_y - P_y * U) and zero(U * P_z - P_z * U),
          'fixed_AF_gate_commutes_with_internal_spatial_C3', checks)

    Psi, W, B_fock, U_embedded, V_af, V_m2, d_af = af_embedding(checks)
    check(zero(U_embedded - U), 'AF_embedding_uses_same_literal_gate', checks)
    _, P_af, _, _ = AF.full_operators(V_af, d_af)
    P_m2_af = V_m2 * V_m2.T
    activation_map = AF.mat(a * V_af[:, :d_af] + p * V_af[:, 3*d_af:])
    check(AF.zero(activation_map - W * V_af[:, :d_af]),
          'AF_activation_map_equals_owned_full_gate_on_every_A1_input', checks)
    check(AF.zero(activation_map.T * activation_map - sp.eye(d_af)),
          'AF_activation_isometry_holds_on_the_complete_A1_input_carrier', checks)
    af_price_pullback = AF.mat(activation_map.T * P_af * activation_map)
    check(AF.zero(af_price_pullback - AF.p * sp.eye(d_af)),
          'complete_A1_activation_p_cut_pulls_back_to_p_times_norm', checks)

    # Start from the actual normalized AF trace vector at A_1. Its M_2
    # component maps to the owned CAR fresh-blank plane; the scalar M_1
    # component stays in the full AF carrier and is not discarded.
    canonical_trace = sp.Matrix([p, 0, 0, p, a*p])
    canonical_native = V_af[:, :d_af] * canonical_trace
    canonical_car_lift = V_m2[:, :4] * canonical_trace[:4, :]
    canonical_car = C.mat(Psi.T * canonical_car_lift)
    check(AF.zero((canonical_trace.T * canonical_trace)[0] - 1),
          'A1_canonical_AF_trace_vector_is_normalized', checks)
    check(AF.zero(Psi * canonical_car - canonical_car_lift),
          'A1_trace_M2_component_has_actual_full16_CAR_lift', checks)
    check(zero(B_fock * canonical_car - canonical_car),
          'A1_trace_M2_component_is_in_owned_fresh_blank_plane', checks)
    canonical_activation = AF.activate(1, canonical_trace)
    check(AF.zero(W * canonical_native - canonical_activation),
          'actual_AF_activate_is_the_owned_full_AF_gate_on_trace_seed', checks)
    activated_car_lift = AF.mat(P_m2_af * canonical_activation)
    activated_car = C.mat(Psi.T * activated_car_lift)
    check(AF.zero(Psi * activated_car - activated_car_lift),
          'activated_A1_trace_M2_component_stays_in_actual_CAR_sector', checks)
    check(zero(activated_car - U * canonical_car),
          'actual_AF_activation_composes_with_same_CAR_gate', checks)

    # Exact cross-owner classification of the inherited AF M2 image against
    # the engine's fresh-blank plane and certified collinear support.
    inherited_m2_to_car = C.mat(Psi.T * V_m2[:, :4])
    activated_A1_to_car = C.mat(Psi.T * P_m2_af * activation_map)
    activated_A1_expected = C.mat(U * inherited_m2_to_car.row_join(sp.zeros(16, 1)))
    engine_guard = (2, 3, 4, 5, 8, 9)
    activated_support_constraints = activated_A1_to_car[list(engine_guard), :]
    activated_support_kernel = activated_support_constraints.nullspace()
    engine_support_constraints = inherited_m2_to_car[list(engine_guard), :]
    engine_support_kernel = engine_support_constraints.nullspace()
    blank_and_engine_constraints = sp.Matrix.vstack(
        (B_fock - I16) * inherited_m2_to_car,
        engine_support_constraints)
    blank_engine_kernel = blank_and_engine_constraints.nullspace()
    canonical_m2_coordinates = canonical_trace[:4, :]
    canonical_engine_blank = E.State(tuple(
        E.P if i in (0, 14) else E.ZERO for i in range(16)))
    check(inherited_m2_to_car.rank() == 4,
          'inherited_AF_M2_to_CAR_map_has_rank_four', checks)
    check(zero(activated_A1_to_car - activated_A1_expected),
          'complete_AF_activation_to_CAR_map_is_owned_gate_after_M2_readout', checks)
    check(activated_A1_to_car.rank() == 4 and
          activated_support_constraints.rank() == 3 and
          len(activated_support_kernel) == 2 and
          activated_support_kernel[0] == sp.Matrix([1, 0, 0, 1, 0]) and
          activated_support_kernel[1] == sp.Matrix([0, 0, 0, 0, 1]),
          'complete_A1_engine_support_kernel_is_M2_trace_plus_scalar_channel', checks)
    af_identity_source = sp.Matrix([1, 0, 0, 1, 0])
    af_scalar_source = sp.Matrix([0, 0, 0, 0, 1])
    activated_identity_car = C.mat(activated_A1_to_car * af_identity_source)
    check(zero(activated_identity_car - sp.Matrix(
        [a, p, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, a, -p])) and
          zero(activated_A1_to_car * af_scalar_source),
          'engine_compatible_A1_family_has_trace_CAR_readout_and_CAR_null_scalar', checks)
    check(zero(C.current(I4, activated_identity_car) - e0) and
          all(C.red(activated_identity_car[i]) == 0 for i in engine_guard),
          'AF_trace_generator_activates_to_valid_engine_state_with_rest_current', checks)
    check(zero(activated_A1_to_car * canonical_trace - activated_car),
          'complete_A1_CAR_map_reproduces_actual_canonical_trace_activation', checks)
    check(engine_support_constraints.rank() == 3 and
          len(engine_support_kernel) == 1 and
          engine_support_kernel[0] == sp.Matrix([1, 0, 0, 1]),
          'entire_AF_inherited_engine_support_is_one_singular_line', checks)
    check(blank_and_engine_constraints.rank() == 3 and
          len(blank_engine_kernel) == 1 and
          blank_engine_kernel[0] == sp.Matrix([1, 0, 0, 1]),
          'AF_inherited_blank_engine_domain_intersection_is_exactly_one_line', checks)
    check(AF.zero(canonical_m2_coordinates - p*blank_engine_kernel[0]) and
          zero(engine_vector(canonical_engine_blank) - canonical_car),
          'canonical_AF_trace_is_the_unique_intersection_line', checks)
    check(not canonical_engine_blank.matter[1] and
          all(not canonical_engine_blank.matter[i] for i in engine_guard),
          'canonical_AF_blank_line_meets_engine_support_but_has_zero_pairing', checks)
    try:
        E.step(canonical_engine_blank)
    except ValueError as error:
        check(str(error) == 'FIRST_GRADE_PAIRING_SINGULARITY',
              'canonical_AF_blank_line_is_rejected_by_owned_engine_pairing', checks)
    else:
        raise AssertionError('CANONICAL_AF_BLANK_LINE_UNEXPECTEDLY_PASSED_ENGINE_GATE')

    owned_engine_blank = E.seed()
    owned_engine_blank_car = engine_vector(owned_engine_blank)
    check(zero(B_fock * owned_engine_blank_car - owned_engine_blank_car) and
          all(not owned_engine_blank.matter[i] for i in engine_guard) and
          owned_engine_blank.matter[1].sign() != 0,
          'engine_seed_is_blank_and_inside_its_certified_transition_domain', checks)
    check(zero(C.current(I4, owned_engine_blank_car) - e0) and
          E.step(owned_engine_blank) is not None,
          'engine_blank_seed_has_rest_current_and_a_real_owned_step', checks)
    check(sp.Matrix.hstack(inherited_m2_to_car, owned_engine_blank_car).rank() == 5,
          'engine_blank_seed_is_outside_the_inherited_AF_M2_image', checks)

    # The actual AF activation of its complete trace vector does enter the
    # engine domain. Compare both owned transitions on the same full state;
    # their agreement lasts four transitions and then ends at the fifth.
    activated_engine = E.State(tuple(
        E.Golden((0, 0, 0, 1)) if i in (0, 14) else
        E.Golden((1, 0, -1, 0)) if i == 1 else
        E.Golden((-1, 0, 1, 0)) if i == 15 else E.ZERO
        for i in range(16)))
    check(zero(engine_vector(activated_engine) - activated_car) and
          not zero(B_fock * activated_car - activated_car),
          'AF_activation_has_exact_full16_engine_state_outside_blank_plane', checks)
    check(all(not activated_engine.matter[i] for i in engine_guard) and
          activated_engine.matter[1].sign() != 0,
          'AF_activated_trace_state_is_admissible_to_owned_engine', checks)
    fixed_trace_state = activated_car
    engine_trace_state = activated_engine
    first_owner_divergence = None
    divergence_masks = []
    for tick in range(12):
        check(zero(C.current(I4, engine_vector(engine_trace_state)) - e0),
              f'AF_activated_engine_current_remains_rest_tick_{tick}', checks)
        check(all(not engine_trace_state.matter[i] for i in engine_guard),
              f'AF_activated_engine_stays_in_owned_support_tick_{tick}', checks)
        engine_next = E.step(engine_trace_state)
        fixed_next = C.mat(U * fixed_trace_state)
        gap = C.mat(fixed_next - engine_vector(engine_next))
        if zero(gap):
            check(tick < 4,
                  f'AF_and_engine_transitions_agree_before_first_divergence_{tick}', checks)
        else:
            if first_owner_divergence is None:
                first_owner_divergence = tick
                divergence_masks = [i for i in range(16) if C.red(gap[i]) != 0]
                check(tick == 4 and engine_trace_state.matter[1].sign() == -1,
                      'AF_and_engine_first_diverge_on_fifth_state_selected_transition', checks)
            if tick >= 4:
                check(not zero(gap),
                      f'AF_and_engine_remain_distinct_after_first_divergence_{tick}', checks)
        fixed_trace_state, engine_trace_state = fixed_next, engine_next
    check(zero(C.current(I4, engine_vector(engine_trace_state)) - e0) and
          all(not engine_trace_state.matter[i] for i in engine_guard),
          'AF_activated_engine_remains_admissible_at_tick_twelve', checks)
    check(first_owner_divergence == 4 and divergence_masks == [0, 1, 14, 15],
          'first_AF_engine_transition_gap_has_exact_four_mask_support', checks)

    expected_rest = sp.Matrix([1, 0, 0, 0])
    canonical_history = canonical_car
    for tick in range(128):
        next_history = C.mat(U * canonical_history)
        J_now = C.current(I4, canonical_history)
        J_next = C.current(I4, next_history)
        J_y = C.current(I4, C.mat(P_y * canonical_history))
        J_z = C.current(I4, C.mat(P_z * canonical_history))
        check(zero(J_now - expected_rest) and zero(J_next - expected_rest) and
              zero(J_y - expected_rest) and zero(J_z - expected_rest),
              f'canonical_blank_trace_has_only_rest_current_tick_{tick}', checks)
        blank_frame = sp.Matrix.hstack(J_now, J_next, J_y, J_z)
        check(blank_frame.rank() == 1 and zero(blank_frame.det()),
              f'canonical_blank_trace_role_frame_collapses_tick_{tick}', checks)
        check(C.red((canonical_history.T * canonical_history)[0] - 2*p**2) == 0,
              f'canonical_blank_trace_M2_norm_is_retained_tick_{tick}', checks)
        canonical_history = next_history

    # The four current columns are generated from one active seed: its present
    # state, its next fixed AF gate tick, and its two proper spatial C3 images.
    x0 = engine_vector(active_state(1))
    check(C.red((x0.T * x0)[0] - 3) == 0,
          'active_seed_has_exact_full16_norm_squared_three', checks)
    check(any(C.red(v) != 0 for v in B_fock*x0-x0),
          'active_seed_is_not_in_AF_fresh_blank_plane', checks)
    check(AF.zero(W * (Psi * x0) - Psi * (U * x0)),
          'actual_AF_gate_executes_active_seed_in_its_M2_sector', checks)
    check(not zero(U * U * x0 - x0),
          'full_state_does_not_return_when_visible_current_does', checks)
    check(zero(C.current(I4, U * U * x0) - C.current(I4, x0)),
          'visible_current_returns_after_two_fixed_gate_ticks', checks)

    _, _, _, _, gram1, expected1, r1 = metric_frame(1, U, P_y, P_z)
    check(r1 == sp.Rational(2, 3), 'unit_memory_amplitude_gives_two_thirds_current_tilt', checks)
    check(zero(gram1 - expected1), 'four_internal_current_labels_have_exact_Gram', checks)
    check(sp.factor(expected1.det()) == -sp.Rational(256, 729),
          'unit_amplitude_Gram_is_nondegenerate_Lorentzian', checks)

    # Check the full fixed-gate orbit, not only the seed and one transition.
    states = {
        'x': x0,
        'y': C.mat(P_y * x0),
        'z': C.mat(P_z * x0),
    }
    current_history = {axis: [] for axis in states}
    for tick in range(129):
        sign = -1 if tick % 2 == 0 else 1
        for axis, state in states.items():
            J = C.current(I4, state)
            expected_J = sp.Matrix([1, sign*sp.Rational(2, 3) if axis == 'x' else 0,
                                    sign*sp.Rational(2, 3) if axis == 'y' else 0,
                                    sign*sp.Rational(2, 3) if axis == 'z' else 0])
            check(zero(J - expected_J),
                  f'full_CAR_current_axis_{axis}_tick_{tick}', checks)
            check(C.red((state.T * state)[0] - 3) == 0,
                  f'full_CAR_norm_axis_{axis}_tick_{tick}', checks)
            check(all(C.red(state[i]) == 0 for i in (2, 3, 4, 5, 8, 9)),
                  f'actual_engine_support_guard_axis_{axis}_tick_{tick}', checks)
            current_history[axis].append(J)
        if tick < 128:
            states = {axis: C.mat(U * state) for axis, state in states.items()}

    for tick in range(128):
        frame = sp.Matrix.hstack(current_history['x'][tick],
                                 current_history['x'][tick+1],
                                 current_history['y'][tick],
                                 current_history['z'][tick])
        gram = C.mat(frame.T * ETA * frame)
        det_expected = sp.Rational(16, 27) if tick % 2 == 0 else -sp.Rational(16, 27)
        check(C.red(frame.det() - det_expected) == 0,
              f'four_state_frame_determinant_tick_{tick}', checks)
        check(zero(gram - expected1),
              f'four_state_Lorentz_Gram_invariant_tick_{tick}', checks)

    # Exact scale controls: no amplitude is fitted to obtain the signature.
    _, _, _, frame0, gram0, _, r0 = metric_frame(0, U, P_y, P_z)
    check(r0 == 0 and frame0.rank() == 1 and gram0.det() == 0,
          'memoryless_control_has_only_one_current_direction', checks)
    _, _, _, frame2, gram2, expected2, r2 = metric_frame(2, U, P_y, P_z)
    check(r2 == sp.Rational(8, 9) and zero(gram2 - expected2),
          'second_exact_amplitude_changes_the_induced_Gram', checks)
    check(sp.factor(expected2.det()) == -4*sp.Rational(8, 9)**6,
          'second_exact_amplitude_remains_Lorentzian', checks)

    # The fixed AF gate and the executor's state-selected negative gate are
    # not the same full transition on the odd state.
    odd = C.mat(U * x0)
    engine_minus = engine_gate_matrix(-1)
    gate_gap = C.mat(U * odd - engine_minus * odd)
    check(any(C.red(v) != 0 for v in gate_gap),
          'fixed_AF_gate_is_not_the_state_selected_engine_gate_after_odd_tick', checks)
    check(C.red(gate_gap[13]) != 0,
          'odd_tick_full_state_gap_has_named_mask13_witness', checks)

    q = sp.symbols('s', positive=True, real=True)
    r = 2*q**2/(1+2*q**2)
    g_diag = 1-r**2
    g_pair = 1+r**2
    derivative_diag = sp.diff(g_diag, q).subs(q, 1)
    derivative_pair = sp.diff(g_pair, q).subs(q, 1)
    check(derivative_diag == -sp.Rational(16, 27) and
          derivative_pair == sp.Rational(16, 27),
          'real_amplitude_extension_has_nonzero_metric_Gram_jet_at_one', checks)

    owner_hashes = {
        path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        for path in INPUTS
    }
    owner_blobs = {
        path: subprocess.check_output(
            ['git', 'rev-parse', f'HEAD:{path}'], cwd=ROOT, text=True).strip()
        for path in INPUTS
    }
    return {
        'status': 'PASS',
        'scope': 'AF_REPRESENTED_FIXED_CAR_GATE_ROLE_ORBIT_LORENTZIAN_GRAM',
        'base_head': '1f936ebfa1b3556245ba708fdeebb0a24500ec4b',
        'current_frame': ['J_x(k)', 'J_x(k+1)', 'J_y(k)', 'J_z(k)'],
        'unit_amplitude_current': 'e0 +/- (2/3)e_i',
        'unit_amplitude_gram': [
            ['5/9', '13/9', '1', '1'],
            ['13/9', '5/9', '1', '1'],
            ['1', '1', '5/9', '1'],
            ['1', '1', '1', '5/9'],
        ],
        'unit_amplitude_gram_determinant': '-256/729',
        'gram_signature': '(1,3) by exact congruence with eta',
        'full_state_after_two_ticks_equals_seed': False,
        'current_after_two_ticks_equals_seed_current': True,
        'real_amplitude_family': {
            'tilt': 'r(s)=2*s^2/(1+2*s^2)',
            'gram_determinant': '-4*r(s)^6',
            'memoryless_limit_s_zero': 'rank one',
            'metric_gram_jet_at_s_one_diagonal': '-16/27',
            'metric_gram_jet_at_s_one_x_pair': '16/27',
            'finite_exact_amplitudes_checked': [0, 1, 2],
        },
        'AF_scope': {
            'full16_M2_embedding_and_gate_intertwiner': True,
            'all_AF_complement_and_scalar_sectors_retained_in_ambient_operator': True,
            'active_seed_in_fresh_blank_plane': False,
            'AF_growth_refinement_map_composed_with_this_orbit': False,
        },
        'canonical_trace_blank_startup_control': {
            'A1_trace_vector': ['p', '0', '0', 'p', 'a*p'],
            'M2_CAR_seed': 'p*(e0+e14)',
            'seed_in_owned_fresh_blank_plane': True,
            'scalar_M1_and_AF_complement_retained': True,
            'actual_AF_activate_equals_embedded_CAR_gate': True,
            'current_for_128_gate_steps': 'e0',
            'four_role_frame_rank': 1,
            'blank_startup_generates_spatial_frame': False,
            'physical_expansion_or_GR_inferred': False,
        },
        'AF_engine_cross_owner_joint_sector': {
            'complete_A1_activation_interface': {
                'A1_input_dimension': 5,
                'AF_activation_isometry': True,
                'AF_P_cut_pullback': 'p*I_5',
                'normalized_A1_P_cut_price': 'p',
                'activation_to_CAR_map_rank': 4,
                'engine_support_constraint_rank': 3,
                'engine_support_kernel_basis': [
                    ['1', '0', '0', '1', '0'],
                    ['0', '0', '0', '0', '1'],
                ],
                'scalar_M1_input_CAR_image': '0',
                'physical_admission_of_full_A1_family_derived': False,
                'complete_D0_action_or_qD_binding_derived': False,
            },
            'inherited_AF_M2_to_full_CAR_rank': 4,
            'inherited_AF_image_intersection_with_engine_support_dimension': 1,
            'engine_support_intersection_M2_coordinates': ['1', '0', '0', '1'],
            'inherited_blank_and_engine_domain_intersection_dimension': 1,
            'intersection_M2_coordinates': ['1', '0', '0', '1'],
            'canonical_trace_M2_seed': 'p*(e0+e14)',
            'canonical_trace_blank_line_engine_rejection':
                'FIRST_GRADE_PAIRING_SINGULARITY',
            'engine_owned_blank_seed': 'e1+e15',
            'engine_blank_seed_in_inherited_AF_M2_image': False,
            'actual_AF_activated_trace_engine_coordinates': {
                'm0': 'a^3', 'm1': '1-p', 'm14': 'a^3', 'm15': 'p-1',
                'all_other_masks': '0',
            },
            'AF_activation_state_is_engine_admissible': True,
            'AF_fixed_and_engine_state_selected_transitions_agree_for':
                'four transitions',
            'first_divergent_transition_zero_based_index': 4,
            'first_divergence_masks': [0, 1, 14, 15],
            'the_two_owner_states_remain_distinct_through_transition': 12,
            'engine_current_at_tick_twelve': 'e0',
            'physical_joint_preparation_or_transition_law_derived': False,
        },
        'physical_scope': {
            'native_q_D_b_m_binding': False,
            'curvature_or_Einstein_equation': False,
            'common_action_source_Ward_or_stationarity': False,
            'soundness_recovery_or_physical_admission': False,
            'global_closure': False,
        },
        'exact_controls': len(checks),
        'checks': sorted(set(checks)),
        'owner_sha256': owner_hashes,
        'owner_git_blob': owner_blobs,
        'note_sha256': hashlib.sha256((ROOT / NOTE).read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-results', action='store_true')
    args = parser.parse_args()
    result = build_result()
    encoded = json.dumps(result, indent=2, sort_keys=True) + '\n'
    if args.write_results:
        RESULT.write_text(encoded)
    else:
        if json.loads(RESULT.read_text()) != result:
            raise AssertionError('STALE_OR_MUTATED_AF_ROLE_ORBIT_RECEIPT')
    print('PASS_AF_ROLE_ORBIT_CURRENT_FRAME controls=%d gram_det=-256/729 ticks=128 '
          'native_q_binding=OPEN' % result['exact_controls'])


if __name__ == '__main__':
    main()
