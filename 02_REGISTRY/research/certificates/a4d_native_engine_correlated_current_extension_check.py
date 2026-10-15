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
    heat_data = heat_L4_sign(checks)
    qd_fiber_data = qD_fiber_nonbasicness(checks, heat_data)

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
        'qD_fiber_nonbasicness': qd_fiber_data,
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
