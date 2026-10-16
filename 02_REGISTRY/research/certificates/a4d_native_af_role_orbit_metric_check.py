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
    return Psi, W, B_fock, U


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

    Psi, W, B_fock, U_embedded = af_embedding(checks)
    check(zero(U_embedded - U), 'AF_embedding_uses_same_literal_gate', checks)

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
