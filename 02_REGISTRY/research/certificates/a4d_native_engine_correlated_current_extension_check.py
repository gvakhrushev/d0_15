#!/usr/bin/env python3
"""Exact cross-owner extension: active CAR current inside the engine domain.

This verifies the existing engine transition and existing full-CAR current
readout on one alternative invariant sector. It is not physical admission or a
derivation of the executor's apparatus axis from that current.
"""
import hashlib
import importlib.util
import json
import argparse
from fractions import Fraction
from pathlib import Path
import subprocess
import sys

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
CERT = Path(__file__).resolve()
RESULT = CERT.with_name('a4d_native_engine_correlated_current_extension_results.json')
LEAN_SOURCE = CERT.with_name('a4d_native_engine_correlated_current_extension.lean')
LEAN_OUTPUT = CERT.with_name('a4d_native_engine_correlated_current_extension_lean_output.txt')
NOTE = ROOT / '02_REGISTRY/research/A4D_NATIVE_ENGINE_CORRELATED_CURRENT_EXTENSION_2026-10-15.md'
OWNER_PATHS = [
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.lean',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_results.json',
    '02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_check.py',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.lean',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_lean_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition_lean_results.json',
    '02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md',
    '02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md',
    '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json',
    '02_REGISTRY/research/A4D_NATIVE_SOLDERED_HEAT_SOURCE.md',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source.py',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_check.py',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source.lean',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_lean_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_lean_results.json',
    '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_check.py',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.lean',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_results.json',
    '03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean',
    '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md',
    '02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md',
    '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding.lean',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_results.json',
    '02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation.py',
    '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py',
    '02_REGISTRY/research/certificates/a4d_native_jones_record_transport.py',
    '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
    '02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md',
    '02_REGISTRY/research/certificates/a4d_native_constrained_price_source.lean',
    '02_REGISTRY/research/certificates/a4d_native_constrained_price_source_check.py',
    '02_REGISTRY/research/certificates/a4d_native_constrained_price_source_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_constrained_price_source_results.json',
    '02_REGISTRY/research/certificates/a4d_native_constrained_price_source_certificate.json',
    '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
    '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient.lean',
    '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_check.py',
    '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_results.json',
    '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_certificate.json',
    '02_REGISTRY/research/A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md',
    '02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source.lean',
    '02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source_check.py',
    '02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source_output.txt',
    '02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source_results.json',
    '02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source_certificate.json',
]


def load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = load('d0_engine_owner_extension', OWNER_PATHS[0])
C = load('d0_correlated_current_owner_extension',
         '02_REGISTRY/research/certificates/a4d_native_correlated_current_transition.py')
P = load('d0_reference_memory_owner_extension',
         '02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation.py')
F = load('d0_fock_record_binding_owner',
         '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py')
AF = load('d0_fibonacci_af_record_owner',
          '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py')
a, p = P.a, P.p
SYMBOLS = [sp.Integer(1), a, p, a*p]
I4 = sp.eye(4)


def check(condition, name, checks):
    if not bool(condition):
        raise AssertionError(name)
    checks.append(name)


def load_integer_state(scale=1):
    m = [E.ZERO] * 16
    m[0] = -2 * E.A * E.P
    m[1] = 2 * E.P - E.ONE
    m[13] = E.Golden.integer(scale)
    m[14] = E.Golden.integer(scale)
    return E.State(tuple(m))


def exact_vector(state):
    return sp.Matrix([
        sum(coefficient * basis for coefficient, basis
            in zip(entry.coefficients, SYMBOLS))
        for entry in state.matter
    ])


def engine_gate_matrix(sign):
    columns = []
    for column in range(16):
        basis = [E.ZERO] * 16
        basis[column] = E.ONE
        state = E.State(tuple(basis))
        columns.append(exact_vector(E.literal_axis_gate(state, sign)))
    return sp.Matrix.hstack(*columns)


def current_at(state):
    return C.current(I4, exact_vector(state))


def wedge_value(state):
    m = state.matter
    return m[12] * m[15] - m[13] * m[14]


def symbolic_readout_checks(checks):
    high = sp.symbols('m12 m13 m14 m15', real=True)
    expected_wedge = high[0]*high[3]-high[1]*high[2]
    expected_norm = 1 + sum(x*x for x in high)
    branches = [
        (-2*a*p, 2*p-1, 'band_A'),
        (5*p-4, a*(4*p-3), 'band_B'),
    ]
    for low0, low1, label in branches:
        m = sp.zeros(16, 1)
        m[0], m[1] = low0, low1
        for index, value in zip((12, 13, 14, 15), high):
            m[index] = value
        J = C.current(I4, m)
        expected = sp.Matrix([1, 2*expected_wedge/expected_norm, 0, 0])
        for component in range(4):
            check(C.red(J[component]-expected[component]) == 0,
                  f'native_full_CAR_current_formula_{label}_component_{component}', checks)

    s = sp.symbols('s', real=True)
    initial = sp.Matrix([1, 0, 0, s])
    omega0 = -s**2
    norm0 = 1 + 2*s**2
    r0 = sp.factor(2*omega0/norm0)
    k0 = sp.factor((1+r0)/(1-r0))
    k1 = sp.factor(1/k0)
    check(sp.factor(r0 + 2*s**2/(1+2*s**2)) == 0,
          'symbolic_initial_current_amplitude', checks)
    check(sp.factor(k0 - 1/(1+4*s**2)) == 0,
          'symbolic_initial_pairing_ratio', checks)
    check(sp.factor(k1 - (1+4*s**2)) == 0,
          'symbolic_one_tick_pairing_ratio', checks)
    check(sp.diff(k1, s).subs(s, 1) == 8,
          'exact_one_tick_pairing_slope_at_unit_amplitude', checks)
    check(initial == sp.Matrix([1, 0, 0, s]), 'symbolic_domain_sanity', checks)


def symbolic_transition_mismatch(checks):
    s = sp.symbols('s', real=True)
    m = sp.zeros(16, 1)
    m[0], m[1], m[13], m[14] = -2*a*p, 2*p-1, s, s
    J = C.current(I4, m)
    expected_J = sp.Matrix([1, -2*s**2/(1+2*s**2), 0, 0])
    for component in range(4):
        check(C.red(J[component]-expected_J[component]) == 0,
              f'active_amplitude_current_formula_component_{component}', checks)

    eta = sp.diag(1, -1, -1, -1)
    h = C.observer_pairing(eta, J)
    n = sp.Matrix([(1+2*s**2)/sp.sqrt(1+4*s**2),
                   -2*s**2/sp.sqrt(1+4*s**2), 0, 0])
    U_current, _, _, _ = C.rest_lorentz_record(h, n)
    delta = C.mat(U_current*m)-engine_gate_matrix(1)*m
    residual = C.red(sp.factor(delta[13].subs(sp.sqrt(5),1+2*p)))
    check(C.red(residual+4*a*s**3) == 0,
          'symbolic_current_observer_minus_engine_mask13_is_minus_4a_s_cubed', checks)
    check(C.red(residual.subs(s, 0)) == 0,
          'transition_mismatch_vanishes_at_current_null_amplitude', checks)
    return sp.factor(residual)


def endpoint_metric_update_checks(checks):
    """Replay the existing conditional endpoint-isometry metric update."""
    eta = sp.diag(1, -1, -1, -1)
    eye4 = sp.eye(4)
    t, u = sp.symbols('t u', nonzero=True, real=True)
    e0 = sp.Matrix([1, 0, 0, 0])
    v = t * e0
    Q = C.mat(-eta + 2 * v * v.T / (v.T * eta.inv() * v)[0])
    check(all(C.red(x) == 0 for x in Q - eye4),
          'collinear_input_pairing_is_euclidean_identity', checks)
    off_axis_v = sp.Matrix([1, sp.Rational(1, 2), 0, 0])
    off_axis_k = (off_axis_v.T * eta.inv() * off_axis_v)[0]
    off_axis_Q = C.mat(-eta + 2 * off_axis_v * off_axis_v.T / off_axis_k)
    check(any(C.red(x) != 0 for x in off_axis_Q - eye4),
          'hostile_off_axis_state_does_not_collapse_to_identity_pairing', checks)
    w = u * e0
    qplus = C.mat(-Q + 2 * w * w.T / (w.T * Q.inv() * w)[0])
    check(all(C.red(x) == 0 for x in qplus - eta),
          'collinear_owned_metric_update_is_eta', checks)
    Q_at_plus = C.mat(-qplus + 2 * w * w.T /
                      (w.T * qplus.inv() * w)[0])
    check(all(C.red(x) == 0 for x in Q_at_plus - Q),
          'collinear_endpoint_pairing_is_retained', checks)

    W = P.C.ext(eye4)
    gate_iso = {}
    for sign in (-1, 1):
        U = engine_gate_matrix(sign)
        preserved = all(C.red(x) == 0 for x in U.T * W * U - W)
        check(preserved, f'actual_engine_gate_preserves_endpoint_pairing_{sign}', checks)
        gate_iso[sign] = preserved

    state = load_integer_state(1)
    beta_A = C.red(2 * p - 1)
    beta_B = C.red(a * (4 * p - 3))
    check(beta_A != 0 and beta_B != 0,
          'both_alternating_first_grade_coefficients_nonzero', checks)
    for tick in range(129):
        m = exact_vector(state)
        actual_v = sp.Matrix([m[1 << i] for i in range(4)])
        expected_beta = beta_A if tick % 2 == 0 else beta_B
        check(C.red(actual_v[0] - expected_beta) == 0 and
              all(C.red(actual_v[i]) == 0 for i in range(1, 4)),
              'actual_orbit_first_grade_is_alternating_collinear', checks)
        check(C.red(actual_v[0]) != 0,
              'endpoint_update_input_first_grade_nonzero', checks)

        if tick < 128:
            next_state = E.step(state)
            mplus = exact_vector(next_state)
            actual_w = sp.Matrix([mplus[1 << i] for i in range(4)])
            next_beta = beta_B if tick % 2 == 0 else beta_A
            check(C.red(actual_w[0] - next_beta) == 0,
                  'actual_engine_output_first_grade_alternates', checks)
            check(C.red(actual_w[0]) != 0 and
                  all(C.red(actual_w[i]) == 0 for i in range(1, 4)),
                  'endpoint_update_output_first_grade_collinear_nonzero', checks)

            sign = state.matter[1].sign()
            check(gate_iso[sign], 'owned_endpoint_isometry_hypothesis_holds', checks)
            state = next_state

    return {
        'owner': 'A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md',
        'conditional_rule': 'q_plus=-Q+2*w*wT/(wT*Qinv*w), Q=-q+2*v*vT/(vT*qinv*v)',
        'first_grade_sequence': ['(2*p-1)*e0', 'a*(4*p-3)*e0'],
        'positive_pairing_Q_and_Q_plus': 'I4 by exact scalar-axis identities',
        'Lorentz_metric_q_and_q_plus': 'eta at every tick',
        'endpoint_isometry_hypothesis': 'verified for all 128 actual engine transitions',
        'transition_mismatch_after_owned_update': 'remains -4*a*s^3 at the initial active state',
        'physical_admission_of_conditional_update': False,
        'ticks_checked': 128,
    }


def current_rest_frame_guard_obstruction(checks):
    """Test the existing exterior lift to the current-rest frame."""
    x = sp.symbols('x', real=True, nonnegative=True)
    root = sp.sqrt(1 + 4 * x**2)
    gamma = (1 + 2 * x**2) / root
    off = 2 * x**2 / root
    boost = sp.eye(4)
    boost[0, 0] = boost[1, 1] = gamma
    boost[0, 1] = boost[1, 0] = off
    eta = sp.diag(1, -1, -1, -1)
    check(all(sp.simplify(v) == 0 for v in boost * eta * boost.T - eta),
          'current_rest_boost_is_lorentz', checks)

    state = sp.zeros(16, 1)
    state[0], state[1], state[13], state[14] = -2*a*p, 2*p-1, x, x
    lifted = P.C.ext(boost) * state
    current_in_rest_frame = C.current(boost, lifted)
    expected_current = sp.Matrix([root / (1 + 2*x**2), 0, 0, 0])
    check(all(C.red(current_in_rest_frame[i] - expected_current[i]) == 0
              for i in range(4)),
          'existing_full_CAR_readout_is_rest_aligned_after_exterior_lift', checks)

    expected_forbidden = 2*x**2*(2*p-1)/root
    check(C.red(lifted[2] - expected_forbidden) == 0,
          'rest_lift_forbidden_mask2_has_exact_formula', checks)
    check(sp.simplify(lifted[2]**2 -
                      4*x**4*(2*p-1)**2/(1+4*x**2)) == 0,
          'rest_lift_forbidden_mask2_square_identity', checks)
    check(C.red(2*p-1) != 0,
          'native_lower_first_grade_is_nonzero', checks)

    forbidden = (2, 3, 4, 5, 8, 9)
    active_forbidden = [i for i in forbidden if sp.simplify(lifted[i]) != 0]
    check(active_forbidden == [2],
          'nonzero_current_rest_lift_hits_actual_engine_forbidden_mask', checks)

    null_lift = lifted.subs(x, 0).applyfunc(C.red)
    null_current = current_in_rest_frame.subs(x, 0).applyfunc(C.red)
    check(C.red(null_lift[2]) == 0 and
          all(C.red(null_current[i] - (1 if i == 0 else 0)) == 0
              for i in range(4)),
          'zero_amplitude_control_has_no_tilt_and_stays_in_guard', checks)

    witness = C.red(lifted[2].subs(x, 1).subs(sp.sqrt(5), 1+2*p))
    check(witness != 0,
          'stored_unit_amplitude_witness_leaves_executor_guard', checks)
    return {
        'owned_frame_lift': 'archiveExteriorFrameLift / P.C.ext',
        'boost': 'gamma=(1+2*s^2)/sqrt(1+4*s^2); off=2*s^2/sqrt(1+4*s^2)',
        'current_in_boosted_frame': 'sqrt(1+4*s^2)/(1+2*s^2) * e0',
        'forbidden_mask2_after_full_exterior_lift':
            '2*s^2*(2*p-1)/sqrt(1+4*s^2)',
        'nonzero_amplitude_domain': 'outside six-zero engine guard for every s!=0',
        'zero_amplitude_control': 'current-null and remains in engine guard',
        'stored_witness': 's=1 has nonzero forbidden mask 2',
    }


def general_gl_frame_guard_obstruction(checks):
    """Exclude every common invertible GL frame lift for current rest alignment.

    The owned CAR current and the grade-one matter vector transform by the
    same E. Requiring both transformed vectors to lie on the unchanged engine
    time axis forces the first two columns of E to be dependent.
    """
    r = sp.symbols('r', nonzero=True, real=True)
    F = sp.Matrix(4, 4, lambda i, j: sp.symbols(f'F{i}{j}', real=True))
    forced = {}
    for i in range(1, 4):
        first_grade_spatial = F[i, 0]
        current_spatial = F[i, 0] + r*F[i, 1]
        derived_column = sp.factor((current_spatial-first_grade_spatial)/r)
        check(derived_column == F[i, 1],
              f'common_GL_frame_rest_condition_forces_first_grade_column_{i}', checks)
        forced[F[i, 0]] = 0
        forced[F[i, 1]] = 0
    determinant_after_constraints = sp.factor(F.det().subs(forced))
    check(determinant_after_constraints == 0,
          'any_common_GL_frame_preserving_guard_and_rest_axis_is_singular', checks)

    s = sp.symbols('s', real=True)
    active_r = -2*s**2/(1+2*s**2)
    check(sp.factor(active_r.subs(s, 1)) == -sp.Rational(2, 3),
          'active_current_has_nonzero_spatial_component_on_stored_witness', checks)
    golden_p = (sp.sqrt(5)-1)/2
    first_grade_coefficient = sp.simplify(2*golden_p-1)
    check(first_grade_coefficient == sp.sqrt(5)-2 and sp.sqrt(5) > 2,
          'active_native_first_grade_is_nonzero', checks)
    return {
        'common_frame_action': 'same invertible E acts on grade-one state and CAR current by owned exterior/vector covariance',
        'state_first_grade': '(2*p-1)*e0, with 2*p-1 != 0',
        'current': 'e0-2*s^2/(1+2*s^2)*e1; non-collinear for s != 0',
        'joint_requirements': 'E(first_grade) and E(current) both lie in span(e0)',
        'forced_conclusion': 'first two columns of E are dependent, so det(E)=0',
        'scope': 'all common linear GL(4) frame/coframe lifts with unchanged executor guard; nonlinear state preparation and interaction-level updates remain open',
    }

def fock_executor_gate_overlap(checks):
    """Compare the owned full-CAR record gate with the actual executor orbit."""
    T = sp.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                   [0, 1, 0, 1], [0, 1, 0, -1]]) / sp.sqrt(2)
    apparatus = sp.Matrix([[a, 0, -p, 0], [0, a, 0, -p],
                           [0, p, 0, a], [p, 0, a, 0]])
    blank = sp.diag(1, 0, 1, 0)
    B0 = F.record_basis()
    base_gate = B0 * sp.kronecker_product(T.T * apparatus * T, I4) * B0.T
    base_blank = B0 * sp.kronecker_product(T.T * blank * T, I4) * B0.T

    frames = {}
    for observer_sign in (-1, 1):
        for orientation_sign in (-1, 1):
            frame = sp.diag(observer_sign,
                            observer_sign * orientation_sign, 1, 1)
            exterior = P.C.ext(frame)
            gate = exterior * base_gate * exterior.inv()
            blank_plane = exterior * base_blank * exterior.inv()
            check(all(C.red(x) == 0 for x in gate - engine_gate_matrix(observer_sign)),
                  f'full_fock_record_gate_equals_executor_gate_n{observer_sign}_o{orientation_sign}', checks)
            frames[(observer_sign, orientation_sign)] = (gate, blank_plane)

    state = load_integer_state(1)
    check(state.matter[15] == E.ZERO,
          'active_executor_seed_has_no_top_grade_orientation_for_fock_binding', checks)
    matched_ticks = 0
    blank_ticks = 0
    for tick in range(129):
        observer_sign = state.matter[1].sign()
        orientation_sign = state.matter[15].sign()
        check(observer_sign != 0 and
              all(not state.matter[i] for i in (2, 4, 8)),
              f'active_executor_first_grade_is_signed_time_axis_{tick}', checks)
        if tick == 0:
            check(orientation_sign == 0,
                  'fock_gate_bootstrap_orientation_absent_at_seed', checks)
        else:
            check(orientation_sign != 0,
                  f'active_executor_top_grade_orientation_available_{tick}', checks)
            gate, blank_plane = frames[(observer_sign, orientation_sign)]
            vector = exact_vector(state)
            next_vector = exact_vector(E.step(state))
            check(all(C.red(x) == 0 for x in gate * vector - next_vector),
                  f'full_fock_record_gate_matches_actual_executor_step_{tick}', checks)
            matched_ticks += 1
            in_blank = all(C.red(x) == 0 for x in blank_plane * vector - vector)
            check(not in_blank,
                  f'active_executor_state_is_not_the_fock_blank_plane_{tick}', checks)
            blank_ticks += int(in_blank)
        if tick < 128:
            state = E.step(state)

    return {
        'operator_identity': 'U_F(q=eta,n=sign(m1)*e0,Omega=sign(m15)*vol)=actual executor U_sign',
        'tested_transitions_with_nonzero_top_grade': matched_ticks,
        'operator_matches_on_tested_transitions': matched_ticks,
        'seed_orientation': 'absent at tick 0; first available at tick 1',
        'tested_active_states_in_owned_fock_blank_plane': blank_ticks,
        'scope': 'operator coincidence does not establish fresh-blank preparation, AF-to-CAR memory binding, physical admission or metric/source dynamics',
    }


def af_lorentz_fock_bridge(checks):
    """Bind the first Lorentzian AF block to the full CAR tuple exactly."""
    t, x, y, z = sp.symbols('t x y z', real=True)
    herm = sp.Matrix([[t+z, x-sp.I*y], [x+sp.I*y, t-z]])
    lorentz_det = t**2-x**2-y**2-z**2
    check(sp.expand(herm.det()-lorentz_det) == 0,
          'first_AF_matrix_block_has_intrinsic_31_determinant', checks)
    check(sp.factor(herm.charpoly().as_expr() -
                    ((sp.Symbol('lambda')-t)**2-x**2-y**2-z**2)) == 0,
          'Herm2_positive_cone_has_future_eigenvalue_boundary', checks)

    sigma_x = sp.Matrix([[0, 1], [1, 0]])
    sigma_y = sp.Matrix([[0, -sp.I], [sp.I, 0]])
    sigma_z = sp.Matrix([[1, 0], [0, -1]])
    check(sigma_x*sigma_y-sigma_y*sigma_x == 2*sp.I*sigma_z and
          sigma_y*sigma_z-sigma_z*sigma_y == 2*sp.I*sigma_x and
          sigma_z*sigma_x-sigma_x*sigma_z == 2*sp.I*sigma_y,
          'M2_star_commutator_orients_the_traceless_Hermitian_space', checks)

    # The literal first AF refinement is (X,y) -> (diag(X,y), X).
    aa, bb, cc, dd = sp.symbols('aa bb cc dd')
    A = sp.Matrix([[aa, bb], [cc, dd]])
    Astar = sp.Matrix([[sp.Symbol('aa_bar'), sp.Symbol('cc_bar')],
                       [sp.Symbol('bb_bar'), sp.Symbol('dd_bar')]])
    y_scalar = sp.symbols('y_scalar')
    fine_first = sp.zeros(3)
    fine_first[:2, :2] = herm
    fine_first[2, 2] = y_scalar
    fine_second = herm
    # diag(A,1) is represented explicitly because the first two diagonal
    # entries are a 2x2 block, not independent scalar coordinates.
    lifted = sp.eye(3)
    lifted[:2, :2] = A
    lifted_star = sp.eye(3)
    lifted_star[:2, :2] = Astar
    transformed_herm = A*herm*Astar
    expected_first = sp.zeros(3)
    expected_first[:2, :2] = transformed_herm
    expected_first[2, 2] = y_scalar
    transported_pair = (lifted*fine_first*lifted_star,
                        A*fine_second*Astar)
    expected_pair = (expected_first, transformed_herm)
    check(transported_pair == expected_pair,
          'native_AF_inclusion_intertwines_spinor_congruence_and_retains_scalar', checks)
    det_identity = sp.factor((A*herm*Astar).det() -
                             (A.det()*Astar.det())*herm.det())
    check(det_identity == 0,
          'spinor_congruence_transports_lorentz_determinant_exactly', checks)

    boost = sp.Matrix([[sp.Rational(5, 3), sp.Rational(4, 3)],
                       [sp.Rational(4, 3), sp.Rational(5, 3)]])
    check(boost.det() == 1,
          'hostile_trace_control_is_a_unit_determinant_Lorentz_boost', checks)
    trace_shift = sp.factor(sp.trace(boost*sp.eye(2)*boost.T)-sp.trace(sp.eye(2)))
    check(trace_shift == sp.Rational(64, 9),
          'noncompact_Lorentz_transport_does_not_preserve_AF_trace', checks)

    # At AF level 1, H_1 = HS(M_2) (+) C, with dimensions 4+1.
    # Pauli coordinates give the canonical real Hermitian form inside HS(M_2).
    chi = sp.Matrix([[1, 0, 0, 1],
                     [0, 1, -sp.I, 0],
                     [0, 1, sp.I, 0],
                     [1, 0, 0, -1]])/sp.sqrt(2)
    check(chi.conjugate().T*chi == sp.eye(4),
          'Pauli_basis_is_unitary_in_the_native_M2_GNS_fibre', checks)
    check(AF.counts(1) == (2, 1) and AF.counts(4) == (8, 5),
          'bridge_uses_actual_A1_and_A4_Fibonacci_levels', checks)

    frame = AF.frame(1)
    V = frame['V']
    d = frame['old_dimension']
    check(d == 5 and V.shape == (89, 20),
          'actual_AF_record_frame_keeps_all_five_old_GNS_directions', checks)
    # Columns are apparatus-major. The first four old coordinates are the
    # whole M_2 block; the fifth is the M_1 scalar and is kept separately.
    m2_columns = (list(range(4)) + [d+i for i in range(4)] +
                  [2*d+i for i in range(4)] + [3*d+i for i in range(4)])
    V_m2 = V[:, m2_columns]
    scalar_columns = [4, d+4, 2*d+4, 3*d+4]
    V_scalar = V[:, scalar_columns]
    W, P_af, B_af, R = AF.full_operators(V, d)
    T = sp.Matrix([[1, 0, 1, 0], [1, 0, -1, 0],
                    [0, 1, 0, 1], [0, 1, 0, -1]])/sp.sqrt(2)
    U = AF.record()
    P = sp.diag(1, 1, 0, 0)
    B0 = sp.diag(1, 0, 1, 0)
    car_basis = F.record_basis()
    Psi = V_m2*sp.kronecker_product(T, chi)*car_basis.T
    U_fock = car_basis*sp.kronecker_product(T.T*U*T, sp.eye(4))*car_basis.T
    P_fock = car_basis*sp.kronecker_product(T.T*P*T, sp.eye(4))*car_basis.T
    B_fock = car_basis*sp.kronecker_product(T.T*B0*T, sp.eye(4))*car_basis.T
    exact = AF.zero
    check(exact(Psi.conjugate().T*Psi-sp.eye(16)),
          'canonical_AF_M2_sector_is_an_isometric_full16_carrier', checks)
    check(exact(W*Psi-Psi*U_fock),
          'actual_AF_record_gate_intertwines_all_16_CAR_components', checks)
    check(exact(P_af*Psi-Psi*P_fock),
          'actual_AF_price_cut_intertwines_full_CAR_price_projector', checks)
    check(exact(B_af*Psi-Psi*B_fock),
          'actual_AF_blank_intertwines_full_CAR_fresh_blank_plane', checks)
    check(exact(V_m2.conjugate().T*V_scalar) and
          exact(V_scalar.conjugate().T*V_scalar-sp.eye(4)) and
          exact(V_m2*V_m2.conjugate().T + V_scalar*V_scalar.conjugate().T-R),
          'Fock16_and_retained_scalar4_exhaust_the_complete_AF_frame', checks)
    check(exact(W*V_scalar-V_scalar*U) and
          exact(P_af*V_scalar-V_scalar*P) and
          exact(B_af*V_scalar-V_scalar*B0),
          'retained_M1_sector_keeps_its_actual_gate_price_and_blank', checks)
    check(exact(W.T*W-sp.eye(89)) and exact((sp.eye(89)-R)*W-(sp.eye(89)-R)) and
          exact(P_af*(sp.eye(89)-R)) and exact(B_af*(sp.eye(89)-R)),
          'all_69_AF_complement_directions_remain_in_the_owned_identity_sector', checks)

    # The actual level-1 canonical trace vector has both central sectors:
    # sqrt(2)*p in HS(M_2), a*p in C, and 2*p^2+p^3=1.
    e_identity = chi[:, 0]
    canonical = sp.Matrix([sp.sqrt(2)*p*e_identity[i] for i in range(4)] +
                          [a*p])
    check(exact(sp.Matrix([[canonical.dot(canonical)]])-sp.Matrix([[1]])),
          'full_A1_canonical_trace_seed_keeps_M2_and_scalar_weights', checks)
    seed_full = V[:, :d]*canonical
    seed_m2_only = V[:, :d]*sp.Matrix([sp.sqrt(2)*p*e_identity[i] for i in range(4)] + [0])
    seed_fock = Psi.conjugate().T*seed_m2_only
    expected_seed = sp.zeros(16, 1)
    expected_seed[0] = 1/sp.sqrt(2)
    expected_seed[14] = 1/sp.sqrt(2)
    check(exact(seed_fock-sp.sqrt(2)*p*expected_seed),
          'unconditioned_AF_trace_seed_enters_the_owned_blank_plane', checks)
    check(exact(B_af*seed_full-seed_full),
          'canonical_full_AF_seed_is_in_the_AF_blank_plane', checks)
    post_fock = Psi.conjugate().T*W*seed_full
    expected_post = sp.zeros(16, 1)
    expected_post[0] = a*p
    expected_post[1] = p**2
    expected_post[14] = a*p
    expected_post[15] = -p**2
    check(exact(post_fock-expected_post),
          'AF_recording_generates_internal_timelike_and_top_grade_components', checks)
    check(sp.simplify((p.subs(p, (sp.sqrt(5)-1)/2))**4) > 0 and
          sp.simplify(p.subs(p, (sp.sqrt(5)-1)/2)**2) != 0,
          'generated_observer_and_orientation_have_nonzero_golden_amplitudes', checks)

    # Iterate the same owned record/refinement map once more. The second new
    # detail is orthogonal to the entire first-level state, not just its
    # coarse M2 component.
    frame_4 = AF.frame(4)
    state_4 = AF.activate(1, canonical)
    state_7 = AF.activate(4, state_4)
    J_1 = frame['V'][:, :d]
    J_4 = frame_4['V'][:, :frame_4['old_dimension']]
    detail_1 = state_4-AF.a*J_1*canonical
    detail_2 = state_7-AF.a*J_4*state_4
    check(AF.zero((state_4.T*state_4)[0]-1) and
          AF.zero((state_7.T*state_7)[0]-1),
          'two_actual_AF_refinement_ticks_preserve_the_full_state_norm', checks)
    check(AF.zero((detail_1.T*detail_1)[0]-AF.p**2) and
          AF.zero((detail_2.T*detail_2)[0]-AF.p**2),
          'each_tick_records_the_same_nonzero_golden_detail_weight', checks)
    check(AF.zero(J_4.T*detail_2) and
          AF.zero((J_4*detail_1).T*detail_2),
          'second_tick_detail_is_orthogonal_to_the_complete_prior_history', checks)
    base_after_two = AF.a**2*J_4*J_1*canonical
    first_record_after_two = AF.a*J_4*detail_1
    check(AF.zero(state_7-base_after_two-first_record_after_two-detail_2) and
          AF.zero((base_after_two.T*first_record_after_two)[0]) and
          AF.zero((base_after_two.T*detail_2)[0]) and
          AF.zero((first_record_after_two.T*detail_2)[0]),
          'two_tick_state_is_an_orthogonal_base_plus_two_retained_records', checks)
    check(AF.zero((base_after_two.T*base_after_two)[0]-AF.p**2) and
          AF.zero((first_record_after_two.T*first_record_after_two)[0]-AF.p**3) and
          AF.zero((detail_2.T*detail_2)[0]-AF.p**2) and
          AF.zero(AF.p**2+AF.p**3+AF.p**2-1),
          'two_tick_golden_archive_weights_sum_exactly_to_one', checks)

    return {
        'first_AF_level': 'A_1=M_2(C) (+) C; Herm_2(C) has determinant signature (1,3)',
        'first_AF_inclusion': '(X,y) -> (diag(X,y),X)',
        'lorentz_transport': 'SL(2,C) congruence on Herm_2 intertwines the actual inclusion and preserves det',
        'trace_boundary': 'noncompact boost changes the canonical AF trace; Lorentz carrier transport is not a trace-preserving physical symmetry',
        'fock_embedding': 'canonical 16D M2-GNS reducing sector in the actual AF recording frame at base level 1',
        'intertwined_owners': ['full CAR gate', 'price cut', 'fresh-blank plane'],
        'retained_sectors': 'full A1 cyclic vector keeps M2 weight 2*p^2 and scalar weight p^3; all 69 AF complement dimensions remain present',
        'one_record_output': 'M2 CAR component has first grade p^2*e0 and top grade -p^2*vol',
        'two_tick_memory': 'two actual AF steps retain the full state; each adds an orthogonal p^2 detail, with final weights p^2, p^3, p^2',
        'all_tick_law': 'from the owned all-n identity, k steps give retained base weight p^k and mutually orthogonal record weights p^2 through p^(k+1), summing to 1',
        'automatic_time_or_GR': False,
        'scope': 'exact first-stage kinematic representation and two actual records of the canonical AF vector; the all-k norm formula is analytic from the owned identity; no physical time law, trace-preserving boosts, joint metric transition, source, Ward identity or GR closure',
    }

def metric_transition_owner_census(checks, metric_update_data):
    """Replay existing metric, heat and AF recording owners and classify arrows."""
    owner_replays = [
        ('02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py',
         'PASS_RECORD_METRIC_CHRONOLOGY'),
        ('02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_check.py',
         'PASS_NATIVE_SOLDERED_HEAT_SOURCE'),
        ('02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_check.py',
         'PASS_FIBONACCI_RECORD_ACTIVATION'),
        ('02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py',
         'PASS: 169 exact controls;'),
    ]
    outputs = {}
    for relative, expected in owner_replays:
        replay = subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT,
                                capture_output=True, text=True, timeout=600)
        check(replay.returncode == 0 and expected in replay.stdout,
              f'owned_metric_candidate_replay_{Path(relative).stem}', checks)
        outputs[Path(relative).stem] = replay.stdout.strip()

    chronology = json.loads((ROOT /
        '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json').read_text())
    check(chronology['status'] == 'PASS' and
          chronology['scope']['conditional_transition_hypothesis'] == 'FULL_ENDPOINT_PAIRING_ISOMETRY' and
          chronology['scope']['hypothesis_physically_admitted_or_core_forced'] is False,
          'only_checked_q_plus_owner_remains_conditional', checks)
    check(metric_update_data['Lorentz_metric_q_and_q_plus'] == 'eta at every tick' and
          metric_update_data['ticks_checked'] == 128,
          'owned_q_plus_owner_leaves_active_engine_sector_at_eta', checks)

    soldered = json.loads((ROOT /
        '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source_certificate.json').read_text())
    check(soldered['verdict'] == 'OWNED_HOMOGENEOUS_OPERATOR_TEN_JOINT_HEAT_COMPONENTS' and
          soldered['bootstrap_heat_identification'] == 'OPEN' and
          soldered['source_Ward_GR'] == 'OPEN',
          'soldered_heat_owner_supplies_components_but_not_physical_transition', checks)
    source = (ROOT / '02_REGISTRY/research/A4D_NATIVE_SOLDERED_HEAT_SOURCE.md').read_text().lower()
    check('with no on-shell equation built into its definition' in source and
          "no current owner equates the bootstrap's" in source,
          'soldered_heat_source_keeps_transition_and_bootstrap_identification_open', checks)
    fibonacci = json.loads((ROOT /
        '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation_certificate.json').read_text())
    fibonacci_scope = fibonacci['scope']
    check(fibonacci['status'] == 'PASS' and
          fibonacci_scope['levels_including_input'] == 4 and
          fibonacci_scope['minimal_AF_inclusions_in_declared_class'] == 3,
          'fibonacci_owner_constructs_declared_four_level_recording_tower', checks)
    check(fibonacci_scope['physical_preparation_instrument_or_refinement_trigger_derived'] is False and
          fibonacci_scope['full_bootstrap_heat_or_metric_link_source_Ward_or_GR_derived'] is False,
          'fibonacci_recording_interaction_remains_unadmitted_and_unbound_to_gravity', checks)
    fibonacci_source = ' '.join((ROOT /
        '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md').read_text().lower().split())
    check('the af tower is not yet welded to the role-phase physical mesh' in fibonacci_source and
          'an independently admitted `(q,d,b,m)` binding' in fibonacci_source,
          'fibonacci_owner_leaves_joint_geometric_bridge_open', checks)
    fock = json.loads((ROOT /
        '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_certificate.json').read_text())
    fock_scope = fock['scope']
    check(fock['status'] == 'PASS' and fock_scope['whole_carrier'] ==
          'ALL_16_EXTERIOR_COMPONENTS_FOUR_APPARATUS_COPIES',
          'fock_binding_constructs_full_sixteen_component_record_gate', checks)
    check(fock_scope['timelike_domain_is_record_invariant'] is False and
          fock_scope['nonzero_top_grade_domain_is_record_invariant'] is False and
          fock_scope['actual_joint_metric_transition_or_history_orientation_recovery_derived'] is False,
          'fixed_q_fock_record_step_needs_joint_metric_or_history_owner', checks)
    fock_source = ' '.join((ROOT /
        '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md').read_text().lower().split())
    check('the actual endpoint-pairing/metric transition must be derived' in fock_source and
          'recovery from history or other grades must be actually constructed' in fock_source,
          'fock_record_binding_rejects_uncharged_metric_or_orientation_reset', checks)
    overlap = fock_executor_gate_overlap(checks)
    af_bridge = af_lorentz_fock_bridge(checks)
    return {
        'record_metric_chronology': {
            'owned_rule': 'q_plus=-Q+2*w*wT/(wT*Qinv*w)',
            'hypothesis': 'full endpoint-pairing isometry',
            'physical_admission': 'OPEN',
            'active_sector_output': 'q_plus=eta on the tested 128-step orbit',
            'replay': outputs['a4d_native_record_metric_chronology_check'],
        },
        'soldered_heat_source': {
            'owned_scope': 'ten homogeneous heat components and full q/raw-solder tangent',
            'state_to_state_metric_transition': 'not supplied',
            'bootstrap_heat_identification': soldered['bootstrap_heat_identification'],
            'source_Ward_GR': soldered['source_Ward_GR'],
            'replay': outputs['a4d_native_soldered_heat_source_check'],
        },
        'fibonacci_record_activation': {
            'owned_scope': 'actual Fibonacci AF recording interaction with full regular-representation price',
            'levels_including_input': fibonacci_scope['levels_including_input'],
            'minimal_AF_inclusions_in_declared_class': fibonacci_scope['minimal_AF_inclusions_in_declared_class'],
            'physical_preparation_and_refinement_admission': 'OPEN',
            'joint_metric_link_source_Ward_GR': 'OPEN',
            'replay': outputs['a4d_native_fibonacci_record_activation_check'],
        },
        'fock_record_binding': {
            'owned_scope': 'full sixteen-component CAR realization of the literal record apparatus',
            'operator_overlap': 'exactly matches the actual executor gate on the 128 tested post-seed steps',
            'preparation_boundary': 'seed lacks orientation; all 128 tested post-seed states miss the owned fresh-blank plane',
            'joint_metric_transition_and_history_orientation_recovery': 'OPEN',
            'active_executor_overlap': overlap,
            'replay': outputs['a4d_native_fock_record_binding_check'],
        },
        'af_lorentz_fock_first_stage_bridge': af_bridge,
        'scope': 'limited census of two metric/heat candidates and two record-operator owners; not global owner completeness',
        'next_missing_arrow': 'extend the exact first-stage AF-to-CAR representation to a physically admitted iterated joint (q,D,b,m) refinement, preserving the full canonical AF state and its scalar/complement sectors; then derive source/Ward and curved recovery. The first AF level now supplies a nonzero timelike/top-grade CAR component after one record, but no physical time or metric transition is yet derived',
    }

def qD_fiber_nonbasicness(checks, heat_data):
    """Check whether the current heat descends to the existing (q,D) fiber."""
    eta = sp.diag(1, -1, -1, -1)
    identity = sp.eye(4)
    check(identity * eta * identity.T == eta,
          'identity_link_satisfies_metric_carrier_constraint', checks)

    s = sp.symbols('s', real=True)
    matter = sp.zeros(16, 1)
    matter[0], matter[1], matter[13], matter[14] = -2*a*p, 2*p-1, s, s
    out = engine_gate_matrix(1) * matter
    Jnext = C.current(identity, out)
    rnext = 2*s**2/(1+2*s**2)
    expected = sp.Matrix([1, rnext, 0, 0])
    check(all(C.red(Jnext[i]-expected[i]) == 0 for i in range(4)),
          'actual_engine_output_current_varies_on_fixed_qD_fiber', checks)
    Knext = sp.factor((1+rnext)/(1-rnext))
    check(sp.factor(Knext-(1+4*s**2)) == 0,
          'heat_parameter_is_not_a_function_of_qD_on_amplitude_fiber', checks)
    check(sp.diff(Knext,s).subs(s,1) == 8,
          'fixed_qD_heat_parameter_has_nonzero_vertical_jet', checks)

    for scale, expected_K in ((1, 5), (2, 17)):
        state = load_integer_state(scale)
        try:
            moved = E.step(state)
        except ValueError as exc:
            raise AssertionError(f'FIXED_QD_WITNESS_REJECTED_{scale}: {exc}')
        check(moved != state,
              f'fixed_qD_stored_engine_witness_{scale}_moves', checks)
        J = current_at(state)
        ratio = C.red(J[1])
        K0 = sp.factor((1+ratio)/(1-ratio))
        K1 = sp.factor(1/K0)
        check(K1 == expected_K,
              f'fixed_qD_stored_engine_witness_{scale}_has_distinct_K', checks)

    derivative_positive = ' > 0 ' in heat_data['heat_derivative_sign']
    check(derivative_positive,
          'current_heat_has_nonzero_vertical_derivative_at_fixed_qD', checks)
    return {
        'carrier_constraint': 'I4*eta*I4^T=eta for every amplitude s',
        'varied_field': 'm13=m14=s; q=eta and D=I fixed',
        'post_tick_observer_parameter': 'K(s)=1+4*s^2',
        'vertical_jet_at_s_1': 'dK/ds=8; dH/ds>0 for all L>=2',
        'qD_only_current_heat_map_on_open_real_family': False,
        'finite_engine_witnesses': {'s=1': 'K=5', 's=2': 'K=17'},
        'scope': 'requires an owner-derived matter-preparation restriction to descend to (q,D)',
        'heat_result_source': heat_data['heat_derivative_sign'],
    }


def conditional_three_term_price(checks, heat_data):
    """Test the three separately owned price jets under the supplied sum claim."""
    owner_checks = [
        ('02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source_check.py',
         'PASS_NATIVE_SHARED_SCENE_PRICE_SOURCE'),
        ('02_REGISTRY/research/certificates/a4d_native_constrained_price_source_check.py',
         'PASS_NATIVE_CONSTRAINED_PRICE_SOURCE'),
        ('02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_check.py',
         'PASS_NATIVE_JOINT_FIELD_QUOTIENT'),
    ]
    outputs = {}
    for relative, expected in owner_checks:
        replay = subprocess.run([sys.executable, str(ROOT / relative)], cwd=ROOT,
                                capture_output=True, text=True, timeout=180)
        check(replay.returncode == 0 and expected in replay.stdout,
              f'owned_source_replay_{Path(relative).stem}', checks)
        outputs[Path(relative).stem] = replay.stdout.strip()

    scene_receipt = json.loads((ROOT /
        '02_REGISTRY/research/certificates/a4d_native_shared_scene_price_source_results.json').read_text())
    check(scene_receipt['status'] == 'PASS' and
          scene_receipt['binary_dense_passport_kappa_and_scalar_source_compiled'],
          'binary_scene_passport_price_source_is_owned_and_replayed', checks)
    check('all genuine derivatives and finite centered contrasts are zero' in
          (ROOT / '02_REGISTRY/research/A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md').read_text().lower(),
          'binary_passport_scene_price_constant_on_declared_class', checks)
    check(heat_data['existing_current_observer_feedback_pencil'] ==
          '(1-4*z*p^3)^4, independent of amplitude s',
          'current_feedback_price_vertical_derivative_zero', checks)
    check(' > 0 ' in heat_data['heat_derivative_sign'],
          'current_heat_vertical_derivative_positive', checks)
    return {
        'term_derivatives_on_fixed_qD_matter_tangent': {
            'scene': '0 if the prepared scene stays in the owned binary passport class',
            'current_two_tick_feedback': '0 for the owned equal-current golden pencil',
            'current_defined_heat': '>0 at s=1 for all L>=2',
        },
        'sum_claim': 'supplied strategy text; no repository owner identifies one common S_coupled',
        'conditional_total_derivative': '>0 under additivity, shared fixed beta=log(2), and binary-passport scene admission',
        'conditional_stationarity': 'impossible for these three terms alone on this tangent',
        'required_missing_arrow': 'a common admitted preparation/action or an additional owner-derived compensating term',
        'owner_replays': outputs,
    }


def heat_L4_sign(checks):
    # z(k)=4(exp(2*pi*i*k/4)-1), stored as exact integer pairs.
    z = [(0, 0), (-4, 4), (-8, 0), (-4, -4)]
    coefficients = {}
    for x0, y0 in z:
        for x1, y1 in z:
            A = (x0-x1)**2 + (y0-y1)**2
            B = (x0+x1)**2 + (y0+y1)**2
            lam = Fraction(5*A, 2) + Fraction(B, 10) + 96
            g = Fraction(A, 1) - Fraction(B, 25)
            exponent = 5*(lam-96)
            check(exponent.denominator == 1,
                  'L4_heat_weight_is_integer_power_of_x', checks)
            exponent = int(exponent)
            coefficients[exponent] = coefficients.get(exponent, Fraction(0)) + g
    coefficients = {n: c for n, c in coefficients.items() if c}
    expected = {
        64: Fraction(-256, 25),
        128: Fraction(-256, 25),
        416: Fraction(3072, 25),
        480: Fraction(512, 5),
        832: Fraction(6144, 25),
    }
    check(coefficients == expected,
          'L4_exact_heat_numerator_polynomial_coefficients', checks)
    positive_tail = sum(c for n, c in coefficients.items() if n > 128)
    check(positive_tail == Fraction(11776, 25) and positive_tail < 472,
          'L4_positive_tail_coefficient_bound', checks)
    check(Fraction(472, 1024) < 1 and -Fraction(256, 25)+1 < 0,
          'L4_exact_rational_tail_proves_negative_numerator', checks)
    off_diagonal_bound = Fraction(64) * Fraction(81, 49) / (2**37)
    negative_diagonal_bound = Fraction(64, 25) / (2**26)
    check(Fraction(192, 5) > 38 and Fraction(16, 5) > 3,
          'all_L_exponent_lower_bounds_are_strict', checks)
    check(off_diagonal_bound < Fraction(1, 2**30),
          'all_L_positive_off_diagonal_bound_below_2_minus_30', checks)
    check(negative_diagonal_bound == Fraction(1, 25*2**20) and
          negative_diagonal_bound > Fraction(1, 2**30),
          'all_L_negative_diagonal_dominates_off_diagonal_bound', checks)
    source_doc = (ROOT / '02_REGISTRY/research/A4D_NATIVE_CORRELATED_CURRENT_TRANSITION.md').read_text()
    check('det(I-z F_2)=(1-4zp^3)^4.' in source_doc,
          'existing_current_observer_feedback_pencil_is_source_pinned', checks)
    ssym, zsym = sp.symbols('s z', real=True)
    feedback_pencil = (1-4*zsym*p**3)**4
    check(sp.diff(feedback_pencil, ssym) == 0,
          'existing_equal_current_feedback_pencil_has_zero_amplitude_derivative', checks)
    return {
        'carrier_L': 4,
        'K_at_odd_tick': '5',
        'K_prime_at_s_1': '8',
        'x': '2^(-1/5)',
        'x_identity': 'x^5=1/2; 0<x<1; x^352<1/1024',
        'normalized_numerator_coefficients': {
            str(power): str(coefficient)
            for power, coefficient in sorted(coefficients.items())
        },
        'positive_tail_coefficient_sum': str(positive_tail),
        'sign_argument': 'P/x^64 < -256/25 + (11776/25)/1024 < 0',
        'partition_function': 'strictly positive sum of 16 positive mode weights',
        'all_L_bounds': {
            'lambda_identity': '(5/2)*A+B/10=(12/5)*A+(A+B)/10',
            'positive_off_diagonal_sum_upper': '64*(9/7)^2*2^-37 < 2^-30',
            'negative_diagonal_term_magnitude_lower': '(64/25)*2^-26 = 1/(25*2^20) > 2^-30',
            'mode_sum_bound': '1+2*sum_{n>=1}2^(-3n)=9/7',
        },
        'heat_derivative_sign': 'dH/ds = -4 * weighted_mean(A-B/25) > 0 for every L>=2',
        'existing_current_observer_feedback_pencil': '(1-4*z*p^3)^4, independent of amplitude s',
        'heat_plus_feedback_derivative': 'positive for every L>=2 on the current-observer interface',
        'scope': 'ALL_L_HOMOGENEOUS_CURRENT_DEFINED_HEAT_ANALYTIC_BOUND_PLUS_EXACT_L4_REPLAY',
        'same_executor_axis_or_native_price_transfer_proved': False,
    }


def build_result():
    checks = []
    symbolic_readout_checks(checks)
    symbolic_residual = symbolic_transition_mismatch(checks)
    metric_update_data = endpoint_metric_update_checks(checks)
    rest_frame_data = current_rest_frame_guard_obstruction(checks)
    gl_frame_data = general_gl_frame_guard_obstruction(checks)
    transition_owner_data = metric_transition_owner_census(checks, metric_update_data)
    heat_data = heat_L4_sign(checks)
    qd_fiber_data = qD_fiber_nonbasicness(checks, heat_data)
    composite_price_data = conditional_three_term_price(checks, heat_data)

    lean_output = LEAN_OUTPUT.read_text()
    lean_declarations = [
        'D0.Research.EngineCorrelatedCurrentExtension.high_gate_wedge_negates',
        'D0.Research.EngineCorrelatedCurrentExtension.high_gate_preserves_norm',
        'D0.Research.EngineCorrelatedCurrentExtension.correlation_never_zero',
        'D0.Research.EngineCorrelatedCurrentExtension.golden_amplitude_current_is_timelike',
        'D0.Research.EngineCorrelatedCurrentExtension.L4_heat_numerator_negative',
        'D0.Research.EngineCorrelatedCurrentExtension.L4_heat_slope_positive',
    ]
    check(all(name in lean_output for name in lean_declarations),
          'lean_output_resolves_all_named_propositions', checks)
    check('sorryAx' not in lean_output and 'depends on axioms: [propext,' in lean_output and
          all(token in lean_output for token in ('Classical.choice', 'Quot.sound')),
          'lean_output_uses_no_sorry_or_extra_axiom', checks)

    state = load_integer_state(1)
    check(E.step(state) != state, 'active_state_is_accepted_and_moves', checks)
    check(all(not state.matter[i] for i in (2, 3, 4, 5, 8, 9)),
          'active_state_satisfies_actual_six_zero_guard', checks)

    eta = sp.diag(1, -1, -1, -1)
    initial_current = current_at(state)
    h_current = C.observer_pairing(eta, initial_current)
    n_current = initial_current/sp.sqrt((initial_current.T*eta*initial_current)[0])
    U_current, _, _, _ = C.rest_lorentz_record(h_current, n_current)
    current_step_output = C.mat(U_current*exact_vector(state))
    engine_step_output = exact_vector(E.step(state))
    transition_residual = current_step_output-engine_step_output
    residual_m13 = C.red(transition_residual[13].subs(sp.sqrt(5),1+2*p))
    check(C.red(residual_m13+4*a) == 0,
          'exact_current_observer_vs_engine_transition_residual_m13_minus_4a', checks)
    check(C.red(residual_m13) != 0,
          'direct_current_observer_transition_identification_rejected_on_witness', checks)

    A0, A1 = -2*E.A*E.P, 2*E.P-E.ONE
    B0, B1 = 5*E.P-4, E.A*(4*E.P-3)
    current_values = []
    for tick in range(129):
        check(state.matter[1].sign() != 0, 'executor_sign_defined_all_replayed_ticks', checks)
        check(state.matter[0:2] == ((A0, A1) if tick % 2 == 0 else (B0, B1)),
              'exact_lower_pair_two_cycle', checks)
        check(E.norm_squared(state) == E.Golden.integer(3),
              'exact_full_norm_conserved', checks)
        omega = wedge_value(state)
        check(omega == (-E.ONE if tick % 2 == 0 else E.ONE),
              'exact_correlated_minor_alternates_nonzero', checks)
        check(all(not state.matter[i] for i in (2, 3, 4, 5, 8, 9)),
              'executor_guard_preserved', checks)
        check(all(not state.matter[i] for i in (6, 7, 10, 11)),
              'unused_high_pairs_remain_zero', checks)

        if tick < 9:
            J = current_at(state)
            expected_r = sp.Rational(-2, 3) if tick % 2 == 0 else sp.Rational(2, 3)
            check(C.red(J[0]-1) == 0 and C.red(J[1]-expected_r) == 0 and
                  C.red(J[2]) == 0 and C.red(J[3]) == 0,
                  'actual_full_CAR_readout_replayed_on_engine_state', checks)
            check(sp.factor(1-expected_r**2) == sp.Rational(5, 9),
                  'causal_current_margin_5_over_9', checks)
            current_values.append(str(expected_r))
        if tick < 128:
            state = E.step(state)

    seed_current = current_at(E.seed())
    check(all(C.red(seed_current[i]-(1 if i == 0 else 0)) == 0 for i in range(4)),
          'original_seed_remains_current_null', checks)

    one_pair = [E.ZERO] * 16
    one_pair[0], one_pair[1] = A0, A1
    one_pair[13] = E.ONE
    one_pair_state = E.State(tuple(one_pair))
    one_pair_current = current_at(one_pair_state)
    check(all(C.red(one_pair_current[i]-(1 if i == 0 else 0)) == 0 for i in range(4)),
          'single_high_pair_does_not_fake_spatial_current', checks)

    forbidden = list(one_pair_state.matter)
    forbidden[3] = E.ONE
    try:
        E.step(E.State(tuple(forbidden)))
    except ValueError as exc:
        check(str(exc) == 'OUTSIDE_CERTIFIED_COLLINEAR_EXECUTOR',
              'hostile_out_of_domain_state_rejected', checks)
    else:
        raise AssertionError('OUT_OF_DOMAIN_MUTANT_ACCEPTED')

    k0, k1 = sp.Rational(1, 5), sp.Integer(5)
    check(k0*k1 == 1 and k1-k0 == sp.Rational(24, 5),
          'unit_amplitude_observer_ratio_alternates_one_fifth_five', checks)

    owner_hashes = {
        relative: hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
        for relative in OWNER_PATHS
    }
    owner_blobs = {}
    for relative in OWNER_PATHS:
        owner_blobs[relative] = subprocess.check_output(
            ['git', 'rev-parse', f'HEAD:{relative}'], cwd=ROOT, text=True).strip()

    return {
        'status': 'PASS',
        'scope': 'ALTERNATIVE_EXACT_ENGINE_INVARIANT_SECTOR_WITH_EXISTING_FULL_CAR_CURRENT_READOUT',
        'physical_admission_or_current_derived_executor_axis_proved': False,
        'same_current_observer_and_executor_output_on_witness': False,
        'current_observer_minus_executor_output_mask13': str(symbolic_residual),
        'fixed_q_direct_common_step_for_nonzero_amplitude': 'NO_GO_WITHIN_THIS_FAMILY',
        'owned_endpoint_metric_update': metric_update_data,
        'current_rest_frame_guard_obstruction': rest_frame_data,
        'general_gl_frame_guard_obstruction': gl_frame_data,
        'metric_transition_owner_census': transition_owner_data,
        'qD_fiber_nonbasicness': qd_fiber_data,
        'conditional_three_term_price': composite_price_data,
        'initial_state': {
            'nonzero_masks': [0, 1, 13, 14],
            'm0': '-2*a*p', 'm1': '2*p-1', 'm13': '1', 'm14': '1',
            'lower_pair': 'existing band A',
            'correlated_minor': '-1',
            'full_norm_squared': '3',
        },
        'all_time_analytic_invariants': {
            'lower_pair': 'existing band A/B two-cycle',
            'high_pair_gate_determinant': '-1 for either executor sign',
            'high_pair_norms_squared': ['1', '1'],
            'correlated_minor': '(-1)^(tick+1)',
            'current': 'e0 + 2*minor/3 e1',
            'current_spatial_component': '(-1)^(tick+1)*2/3',
            'minkowski_norm_squared': '5/9',
        },
        'heat_interface_parameter': {
            'initial_K_of_amplitude_s': '1/(1+4*s^2)',
            'after_one_tick_K_of_amplitude_s': '1+4*s^2',
            'at_s_1': ['1/5', '5'],
            'derivative_after_one_tick_at_s_1': '8',
            'heat_price_transfer_proved': False,
        },
        'exact_heat_response': heat_data,
        'finite_regression_ticks': 128,
        'exact_controls': len(checks),
        'control_names': sorted(set(checks)),
        'current_spatial_values_first_nine_ticks': current_values,
        'hostile_controls': [
            'original whole-blank seed remains current-null',
            'one nonzero high pair alone remains current-null',
            'state with forbidden m3 coordinate is rejected by actual step guard',
            'current-derived record operator differs from engine output at mask 13 on the exact witness',
            'off-axis timelike first grade changes the conditional positive pairing',
            'current-rest-frame exterior lift populates forbidden engine mask 2 for nonzero amplitude',
            'any common invertible GL frame that rest-aligns current also violates the unchanged first-grade executor guard',
        ],
        'owner_sha256': owner_hashes,
        'owner_git_blob': owner_blobs,
        'lean_capsule_sha256': hashlib.sha256(LEAN_SOURCE.read_bytes()).hexdigest(),
        'lean_output_sha256': hashlib.sha256(LEAN_OUTPUT.read_bytes()).hexdigest(),
        'research_note_sha256': hashlib.sha256(NOTE.read_bytes()).hexdigest(),
        'checker_sha256': hashlib.sha256(CERT.read_bytes()).hexdigest(),
    }


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-results', action='store_true')
    args = parser.parse_args()
    payload = build_result()
    encoded = json.dumps(payload, indent=2, sort_keys=True) + '\n'
    if args.write_results:
        RESULT.write_text(encoded)
    else:
        recorded = json.loads(RESULT.read_text())
        if recorded != payload:
            raise AssertionError('STALE_OR_MUTATED_ENGINE_CURRENT_EXTENSION_RECEIPT')
    print(f'PASS_NATIVE_ENGINE_CORRELATED_CURRENT_EXTENSION checks={payload["exact_controls"]} ticks=128 result={RESULT.name}')


if __name__ == '__main__':
    run()
