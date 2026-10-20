#!/usr/bin/env python3
"""Exact controls for complete golden-active-block joint dynamics and refinement."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import sympy as s

HEAD = '45f19d1399829b284f15b41899b49ee9961ea394'
BASE = '02_REGISTRY/research/certificates/a4d_native_composed_feedback_dynamics'
PROOF = '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md'
SCOPE = {
    'class': 'ALL_REAL_ORTHOGONAL_JOINT_OPERATORS_WITH_FIXED_GOLDEN_ACTIVE_BLOCK',
    'arbitrary_finite_archive_dimension_Lean_formalized': True,
    'complete_raw_block_reconstruction_Lean_formalized': True,
    'orthogonality_iff_and_all_six_constraints_Lean_formalized': True,
    'complete_initial_archive_retained': True,
    'minimal_archive_full_two_step_reconstruction_Lean_formalized': True,
    'nonminimal_delayed_return_control': True,
    'actual_golden_and_recorded_owner_definitions_consumed': True,
    'feedback_bound_to_literal_block_projection_Lean_formalized': True,
    'native_one_step_equal_two_step_action_gap_Lean_formalized': True,
    'source': 'ACTUAL_DERIVATIVE_IN_DECLARED_ORTHOGONAL_COMPLETION_COORDINATE',
    'actual_matrix_action_and_derivative_binding_Lean_formalized': True,
    'same_record_reused_without_reset': True,
    'golden_joint_inclusion_and_pairing_Lean_formalized': True,
    'operator_and_projection_refined_together': True,
    'all_internal_powers_feedback_refinement_Lean_formalized': True,
    'raw_determinant_action_and_source_double_Lean_formalized': True,
    'owned_golden_matrix_preparation_Lean_formalized': True,
    'complete_compatible_fine_projector_class_Lean_formalized': True,
    'image_supported_preparation_test_has_no_added_active_range': True,
    'literal_cylinder_value_pullback_is_replicated_Lean_formalized': True,
    'image_supported_test_substituted_for_literal_cylinder_readout': False,
    'arbitrary_orthogonal_full_history_return_action_Lean_formalized': True,
    'exact_preparation_norm_defect_Lean_formalized': True,
    'actual_action_factors_through_full_return_with_leakage_Lean_formalized': True,
    'moving_preparation_readout_and_operator_source_Lean_formalized': True,
    'all_size_quantitative_action_stability': 'ANALYTIC_WITH_EXPLICIT_RANK_AND_RESOLVENT_FACTORS',
    'two_owned_golden_preparations_bound_Lean_formalized': True,
    'all_four_cross_returns_reconstruct_arbitrary_full_operator_Lean_formalized': True,
    'literal_cylinder_action_from_all_four_returns_Lean_formalized': True,
    'actual_two_preparation_source_transport_Lean_formalized': True,
    'one_layer_reconstruction_error_bound': 'ANALYTIC_WITH_FACTOR_1_OVER_1_MINUS_ABS_A',
    'all_cross_return_physical_readout_availability_derived': False,
    'owned_recorded_quadratic_feedback_reconstruction_Lean_formalized': True,
    'both_comparison_records_and_preparation_flag_retained_Lean_formalized': True,
    'literal_cylinder_flag_bound_to_owned_reversible_registration_Lean_formalized': True,
    'full_flagged_comparison_orthogonality_Lean_formalized': True,
    'comparison_compiled_into_owned_internal_clock_Lean_formalized': True,
    'actual_recorded_feedback_action_and_source_transport_Lean_formalized': True,
    'normalized_mixed_response_fixed_calibration': 2,
    'direct_feedback_reconstruction_requires_signed_U_or_inverse_oracle': False,
    'common_full_word_reuses_old_target_memory_without_reset': True,
    'native_physical_pair_preparation_and_readout_admission_derived': False,
    'internal_clock_compiler_derives_physical_primitives_from_M1': False,
    'quadratic_reading_to_feedback_bound': 'ALL_SIZE_ANALYTIC_WITH_CALIBRATION_DIMENSION_AND_CONDITIONING',
    'whole_bootstrap_finite_spectral_source_Lean_formalized': True,
    'actual_combinatorial_scene_heat_coefficient_binding_Lean_formalized': True,
    'replicated_thermal_source_unchanged_Lean_formalized': True,
    'joint_stationarity_refinement_iff_Lean_formalized': True,
    'required_fine_thermal_covector_on_coarse_slice': 'TWICE_THE_COARSE_THERMAL_COVECTOR',
    'uniform_spectral_shift_no_stationarity_Lean_formalized': True,
    'uniform_spectral_shift_admitted_by_native_scene': False,
    'fixed_connected_Laplacian_Cayley_coupled_slice_nonempty_Lean_formalized': True,
    'coupled_slice_stationarity_is_whole_native_joint_gate': False,
    'native_Delta_P_U_coupling_or_fine_spectral_law_derived': False,
    'native_zero_mode_constraints_removed': False,
    'single_calibration_obstruction_exhausts_constrained_native_variations': False,
    'actual_source_port_constituent_map_Lean_formalized': True,
    'actual_source_definitions_bound_with_standard_axioms': True,
    'normalizer_and_canonical_pairing_jet_retained_Lean_formalized': True,
    'all_retained_word_jets_genuine_Lean_formalized': True,
    'moving_eigenvector_matrix_heat_derivative_Lean_formalized': True,
    'noncommuting_heat_source_all_C1_finite_curves': 'ANALYTIC_WITH_UNIFORM_SERIES_REMAINDER',
    'general_matrix_heat_and_Jacobi_derivatives_fully_Lean_formalized': False,
    'whole_basis_Ward_genuine_Lean_formalized': True,
    'basis_Ward_identified_with_physical_metric_matter_Ward': False,
    'both_native_history_intertwining_spectral_class_complete_Lean_formalized': True,
    'actual_history_scene_commutator_defect_Lean_formalized': True,
    'doubled_heat_source_defect_contraction_Lean_formalized': True,
    'two_history_stationarity_derived_as_native_admission_gate': False,
    'scene_passivity_under_golden_history_forced_by_M1': False,
    'all_native_refinements_exhausted_by_two_history_spectral_naturality': False,
    'source_port_polynomials_admit_arbitrary_spectrum': False,
    'arbitrary_primitive_matrix_curve_physically_admitted': False,
    'quotient_degree_squared_identified_with_scene_Laplacian': False,
    'diagonal_return_probabilities_determine_full_operator': False,
    'whole_native_scene_process_selected_by_tomography': False,
    'full_return_equals_power_of_one_step_compression': False,
    'invariant_prepared_subspace_assumed_for_full_return_identity': False,
    'whole_physical_fine_readout_selected_as_image_projector': False,
    'native_metric_preparation_Oh_bounds_derived': False,
    'Palatini_contrast_or_stationarity_transferred': False,
    'arbitrary_fine_extension_determined_by_prepared_inclusion': False,
    'ordinary_determinant_invariant_under_binary_replication': False,
    'fine_independent_variations_exhausted_by_coarse_lifts': False,
    'block_projection_identified_with_record_partial_trace': False,
    'F2_alone_reconstructs_full_minimal_operator': False,
    'two_step_H_reconstructs_nonminimal_archive': False,
    'fixed_active_block_exhausts_entire_D0_core': False,
    'orthogonal_completion_implies_physical_admission': False,
    'continuous_Cayley_curve_forced_by_M1': False,
    'two_step_component_is_full_bootstrap_action': False,
    'whole_scene_history_partition_equals_composed_feedback_proved': False,
    'physical_feedback_action_replaced_by_U_determinant': False,
    'new_action_or_level_counterterm_added': False,
    'physical_source_fitted_to_root': False,
    'metric_matter_source_or_physical_Ward_derived': False,
    'profinite_point_and_Hilbert_amplitude_process_identified': False,
    'causal_time_or_spatial_geometry_derived': False,
    'GR_soundness_or_curved_recovery_proved': False,
    'G0_closed': False,
    'positive_GR': False,
    'global_closure': False,
    'original_parent_terminals_changed': False,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    ap.add_argument('--expect', type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda path: hashlib.sha256((root/path).read_bytes()).hexdigest()
    if args.expect:
        assert json.loads(args.expect.read_text())['scope'] == SCOPE, 'PINNED_LEDGER_MISMATCH'
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    zero = lambda M: all(s.cancel(x) == 0 for x in M)
    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    transcript = (root/(BASE+'_output.txt')).read_text()
    lean = (root/(BASE+'.lean')).read_text()
    declarations = re.findall(r'^theorem (\w+)', lean, re.M)
    check('COMPILER_EXIT_ZERO', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0)
    check('CAPSULE_AND_TRANSCRIPT_FRESH', receipt['capsule_sha256'] == sha(BASE+'.lean')
          and receipt['output_sha256'] == sha(BASE+'_output.txt'))
    check('ALL_ACTUAL_PROPOSITIONS_AND_DEPENDENCIES', declarations == receipt['declarations']
          and len(declarations) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 215)
    check('NO_PLACEHOLDER_OR_COMPILER_ERROR', 'sorryAx' not in transcript
          and re.search(r'\berror(?:\(|:)', transcript) is None
          and re.search(r'\b(sorry|admit|axiom)\b', lean) is None)
    axioms = set()
    for match in re.finditer(r'depends on axioms: \[([^]]*)\]', transcript, re.S):
        axioms.update(x.strip() for x in match.group(1).split(',') if x.strip())
    check('STANDARD_TRANSITIVE_LOGICAL_AXIOMS_ONLY', sorted(axioms) == receipt['axioms']
          == ['Classical.choice', 'Quot.sound', 'propext'])
    for name in declarations:
        full = 'D0.Research.NativeComposedFeedbackDynamics.'+name
        check('ACTUAL_DECLARATION_'+name, full in transcript and "'"+full+"'" in transcript)
    check('REAL_OPERATOR_AND_DERIVATIVE_PROPOSITIONS', all(x in transcript for x in
          ['Function.Injective', 'HasDerivAt', 'minimalJoint', 'fullStep', 'directStep',
           'joint', 'goldenInclusion', 'fullFeedback', 'feedbackAction', 'liftOperator',
           'recordedQuadraticKernel', 'fullFlaggedComparison', 'FiniteProtocolClock.run']))
    check('SEVENTEEN_TRANSITIVE_NATIVE_SOURCE_PINS', len(receipt['transitive_d0_source_sha256']) == 17
          and all(x in receipt['transitive_d0_source_sha256'] for x in
                  ['03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean',
                   '03_FORMALIZATION/D0/Synthesis/SceneHeatKernel.lean',
                   '03_FORMALIZATION/D0/Spectral/DarkArchiveStructure.lean',
                   '03_FORMALIZATION/D0/Representation/SourcePortPreparation.lean',
                   '03_FORMALIZATION/D0/Integration/V15/RawZone.lean',
                   '03_FORMALIZATION/D0/Representation/OrderMemoryReadout.lean']))
    check('ACTUAL_THERMAL_AND_JOINT_DERIVATIVE_PROPOSITIONS', all(x in transcript for x in
          ['thermalPartition', 'thermalSource', 'bootstrapAction', 'replicatedSpectrum',
           'sceneZoneHeatReal', 'controlLaplacian', 'controlSpectrum', 'controlFeedbackSource',
           'control_slice_stationary_refinement_failure']))
    check('ACTUAL_SHARED_PRIMITIVE_SOURCE_AND_WORD_PROPOSITIONS', all(x in transcript for x in
          ['sourcePort', 'sourceActive', 'compressionJet', 'portJet', 'sourceCoupled',
           'weightedFeedbackJet', 'genuine_native_interaction_from_primitives',
           'genuine_whole_native_word_derivative', 'matrixPowerJet']))
    check('ACTUAL_MATRIX_EXPONENTIAL_AND_WHOLE_WARD_PROPOSITIONS', all(x in transcript for x in
          ['matrixHeat', 'matrixBootstrap', 'sourceConj', 'movedMetric', 'movedInverseMetric',
           'actual_matrix_heat_derivative', 'genuine_whole_basis_ward']))
    check('ACTUAL_TWO_HISTORY_SCENE_AND_FIRST_JET_PROPOSITIONS', all(x in transcript for x in
          ['historySpectralDefect', 'nativePreparationFrameInverse',
           'two_history_spectral_naturality_iff', 'second_history_defect_is_commutator',
           'genuine_two_history_bootstrap_source', 'fine_thermal_source_defect_identity']))
    pins = dict(receipt['transitive_d0_source_sha256'])
    pins.update(receipt['toolchain_input_sha256'])
    for path, digest in pins.items():
        check('SOURCE_PIN_'+path, sha(path) == digest)
    for path in ['01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
                 '02_REGISTRY/research/A4D_NATIVE_HISTORY_RESPONSE_DESCENT.md',
                 '02_REGISTRY/research/certificates/a4d_native_history_response_descent.lean']:
        pins[path] = sha(path)

    # Exact all-block fixtures supplement, rather than replace, the generic Lean iff.
    def reflection(dim, shift):
        if dim == 0:
            return s.zeros(0)
        v = s.Matrix([i+shift for i in range(dim)])
        return s.eye(dim)-2*v*v.T/(v.T*v)[0]

    def joint(a, p, R, S, V):
        n, m = R.cols, R.rows
        D = a*S*R.T+V
        return s.BlockMatrix([[a*s.eye(n), -p*R.T], [p*S, D]]).as_explicit()

    def feedback(P, U):
        return P*U.T*(s.eye(P.rows)-P)*U*P

    def active(U, n):
        C = U[n:, :n]
        return C.T*C

    aa, pp = s.Rational(3, 5), s.Rational(4, 5)
    cases = []
    for n in (1, 2, 3):
        for m in (n, n+1, n+2):
            QR, QS = reflection(m, 1), reflection(m, 2)
            R, S = QR[:, :n], QS[:, :n]
            V = QS[:, n:]*reflection(m-n, 3)*QR[:, n:].T
            D = aa*S*R.T+V
            U = joint(aa, pp, R, S, V)
            tag = f'{n}_{m}'
            check('ALL_SIX_COMPLETION_CONSTRAINTS_'+tag,
                  zero(R.T*R-s.eye(n)) and zero(S.T*S-s.eye(n)) and zero(V*R)
                  and zero(S.T*V) and zero(V.T*V-(s.eye(m)-R*R.T))
                  and zero(V*V.T-(s.eye(m)-S*S.T)))
            check('COMPLETE_ORTHOGONALITY_'+tag, zero(U.T*U-s.eye(n+m)) and zero(U*U.T-s.eye(n+m)))
            BR, SC = -U[:n, n:].T/pp, U[n:, :n]/pp
            VR = U[n:, n:]-aa*SC*BR.T
            check('ACTUAL_RAW_RECONSTRUCTION_'+tag, zero(BR-R) and zero(SC-S) and zero(VR-V)
                  and zero(joint(aa, pp, BR, SC, VR)-U))
            check('ARCHIVE_INPUT_OUTPUT_CONSTRAINTS_'+tag, zero(D*R-aa*S) and zero(D.T*S-aa*R))
            check('ONE_RETURN_FULL_BLOCK_FEEDBACK_'+tag, zero(active(U, n)-pp**2*s.eye(n)))
            A2 = (U*U)[:n, :n]
            check('TWO_RETURN_RETAINED_AND_FEEDBACK_'+tag, zero(A2-(aa**2*s.eye(n)-pp**2*R.T*S))
                  and zero(active(U*U, n)-(s.eye(n)-A2.T*A2)))
            if m == n:
                T = s.diag(s.eye(n), R.T)
                check('MINIMAL_ARCHIVE_COORDINATE_NORMAL_FORM_'+tag,
                      zero(V) and zero(T*U*T.T-joint(aa, pp, s.eye(n), R.T*S, s.zeros(n))))
            else:
                erased = joint(aa, pp, R, S, s.zeros(m))
                check('ERASING_ARCHIVE_COMPLEMENT_FAILS_'+tag, not zero(erased.T*erased-s.eye(n+m)))
            cases.append([n, m])
    b1, b2 = s.symbols('b1 b2', real=True)
    small_S = s.Matrix([[b1, b2]])
    check('SMALLER_ARCHIVE_CANNOT_BE_ISOMETRIC', s.expand((small_S.T*small_S).det()) == 0)

    a, p, z, t = s.symbols('a p z t', real=True)

    def golden(expr):
        num, den = s.fraction(s.cancel(expr))
        return s.rem(s.rem(s.expand(num), a*a-p, a), p*p+p-1, p).expand()/den

    gzero = lambda M: all(golden(x) == 0 for x in M)
    I2, X = s.eye(2), s.Matrix([[0, 1], [1, 0]])
    direct = s.Matrix([[a, 0, -p, 0], [0, a, 0, -p], [p, 0, a, 0], [0, p, 0, a]])
    recorded = s.Matrix([[a, 0, -p, 0], [0, a, 0, -p], [0, p, 0, a], [p, 0, a, 0]])
    P = s.diag(1, 1, 0, 0)
    check('ACTUAL_NATIVE_JOINT_DEFINITIONS', direct == joint(a, p, I2, I2, s.zeros(2))
          and recorded == joint(a, p, I2, X, s.zeros(2)))
    check('NATIVE_JOINT_ORTHOGONALITY', gzero(direct.T*direct-s.eye(4)) and gzero(recorded.T*recorded-s.eye(4)))
    F1d, F1r = active(direct, 2), active(recorded, 2)
    F2d, F2r = active(direct**2, 2), active(recorded**2, 2)
    check('NATIVE_ONE_TRANSITION_SAME_FEEDBACK', F1d == F1r == p*p*I2)
    check('NATIVE_TWO_TRANSITIONS_KEEP_RECORD', gzero(F2d-4*p**3*I2) and gzero(F2r-2*p**3*(I2+X)))
    check('LITERAL_OWNED_FULL_FEEDBACK', feedback(P, direct) == s.diag(F1d, s.zeros(2))
          and feedback(P, recorded**2) == s.diag(F2r, s.zeros(2)))
    detd, detr = (I2-z*F2d).det(), (I2-z*F2r).det()
    check('BOTH_TWO_HISTORY_DETERMINANTS', golden(detd-(1-4*z*p**3)**2) == 0
          and golden(detr-(1-4*z*p**3)) == 0)
    check('ONE_ACTION_EQUALITY_DOES_NOT_EXTEND', golden(detd-detr) != 0)
    check('U_DETERMINANT_SUBSTITUTION_REJECTED', golden((s.eye(4)-z*recorded**2).det()-detr) != 0)
    start = s.Matrix([1, 0, 0, 0])
    vd, vr = direct**2*start, recorded**2*start
    wd, wr = sum(x*x for x in vd[:2]), sum(x*x for x in vr[:2])
    check('ACTUAL_SECOND_RETURN_READING', golden(wd-p**6) == 0 and golden(wr-(p*p+p**4)) == 0)
    check('SECOND_RETURN_READING_GAP', golden(wr-wd-2*p**3) == 0)
    check('WRONG_RETURN_SIGN_REJECTED', golden(wr-wd+2*p**3) != 0)
    # Erasing the port/archive amplitudes is a changed process, not reuse of W.
    rho1 = recorded*start*start.T*recorded.T
    rho_erased = s.diag(*rho1.diagonal())
    full2, erased2 = recorded*rho1*recorded.T, recorded*rho_erased*recorded.T
    check('ERASURE_CHANGES_TWO_RETURN_JOINT_STATE', not gzero(full2-erased2))

    delayed = lambda eps: s.Matrix([[a, -p, 0], [0, 0, eps], [p, a, 0]])
    plus, minus = delayed(1), delayed(-1)
    check('NONMINIMAL_BOTH_ORTHOGONAL', gzero(plus.T*plus-s.eye(3)) and gzero(minus.T*minus-s.eye(3)))
    check('NONMINIMAL_SAME_TWO_RETAINED_STEPS', (plus**2)[0, 0] == (minus**2)[0, 0] == a*a)
    check('NONMINIMAL_THIRD_STEP_ARCHIVE_RETURN', s.expand((plus**3)[0, 0]-a**3+p*p) == 0
          and s.expand((minus**3)[0, 0]-a**3-p*p) == 0)
    check('NONMINIMAL_THIRD_FEEDBACK_GAP', golden(active(plus**3, 1)[0, 0]
          - active(minus**3, 1)[0, 0]-4*a**3*p*p) == 0)

    H = s.Matrix([[1-t*t, -2*t], [2*t, 1-t*t]])/(1+t*t)
    check('ENTIRE_CAYLEY_COORDINATE_ORTHOGONAL', zero(H.T*H-I2))
    U = joint(a, p, I2, H, s.zeros(2))
    F = active(U*U, 2)
    f = 4*p**3/(1+t*t)
    check('CAYLEY_ACTUAL_MATRIX_FEEDBACK', gzero(F-f*I2))
    source = -16*p**3*z*t/((1+t*t)*(1+t*t-4*z*p**3))
    calculated = s.diff(-2*s.log(1-z*f), t)
    check('INDEPENDENT_GENUINE_SOURCE_DERIVATIVE', s.cancel(calculated-source) == 0)
    check('CAYLEY_SOURCE_NONZERO', s.cancel(source.subs(t, 1)+16*p**3*z/(2*(2-4*z*p**3))) == 0)
    check('WRONG_SOURCE_SIGN_REJECTED', s.cancel(calculated+source) != 0)
    check('F2_DOES_NOT_DETERMINE_ORIENTED_MINIMAL_HISTORY',
          zero(H+H.T-(H.T+H)) and not zero(H-H.T)
          and not zero((aa**2*I2-pp**2*H)-(aa**2*I2-pp**2*H.T)))

    # Rational exact joint operators supplement all-size golden statements.
    U0 = direct.subs({a: aa, p: pp})
    W0 = recorded.subs({a: aa, p: pp})
    lift = lambda A: s.diag(A, A)
    J = s.Matrix.vstack(aa*s.eye(4), pp*s.eye(4))
    check('GOLDEN_FORM_INCLUSION_PAIRING', J.T*J == s.eye(4))
    check('OPERATOR_AND_PROJECTION_INTERTWINING', lift(W0)*J == J*W0 and lift(P)*J == J*P)
    for k in range(5):
        check('EVERY_DECLARED_HISTORY_JOINT_REFINEMENT_'+str(k),
              feedback(lift(P), lift(W0)**k) == lift(feedback(P, W0**k)))
    word = W0*U0*W0.T*U0
    check('NONCOMMUTING_WORD_JOINT_REFINEMENT', lift(W0)*lift(U0)*lift(W0.T)*lift(U0) == lift(word)
          and feedback(lift(P), lift(word)) == lift(feedback(P, word)))
    check('NONCOMMUTING_WORD_IS_NONTRIVIAL', W0*U0 != U0*W0)
    F0 = feedback(P, W0**2)
    coarse_det = (s.eye(4)-z*F0).det()
    fine_det = (s.eye(8)-z*lift(F0)).det()
    check('ACTUAL_REPLICATED_FEEDBACK_DETERMINANT_SQUARE', s.expand(fine_det-coarse_det**2) == 0)
    check('RAW_ACTION_INVARIANCE_REJECTED', s.expand(fine_det-coarse_det) != 0)
    check('ACTUAL_SOURCE_DOUBLES_UNDER_REPLICATION',
          s.cancel(s.diff(-4*s.log(1-z*f), t)-2*calculated) == 0)
    unrefined_P = s.diag(P, s.zeros(4))
    check('LIFTING_U_WITHOUT_P_DOES_NOT_REFINE_FEEDBACK',
          feedback(unrefined_P, lift(W0)) != lift(feedback(P, W0)))
    # The prepared inclusion leaves a genuine operator complement unobserved.
    Q = s.BlockMatrix([[aa*s.eye(4), -pp*s.eye(4)], [pp*s.eye(4), aa*s.eye(4)]]).as_explicit()
    alternative = Q*s.diag(W0, s.eye(4))*Q.T
    replicated = lift(W0)
    check('BOTH_EXTENSIONS_ORTHOGONAL', alternative.T*alternative == replicated.T*replicated == s.eye(8))
    check('SAME_PREPARED_INCLUSION_ALL_INTERNAL_STEPS', alternative*J == replicated*J == J*W0)
    check('FINE_COMPLEMENT_NOT_DETERMINED', alternative != replicated)
    Falt, Frep = feedback(lift(P), alternative), feedback(lift(P), replicated)
    check('PREPARED_RESPONSES_STILL_AGREE', Falt*J == Frep*J == J*feedback(P, W0))
    detalt = (s.eye(8)-z*Falt).det()
    detrep = (s.eye(8)-z*Frep).det()
    determinant_base = (s.eye(4)-z*feedback(P, W0)).det()
    check('COMPLEMENT_CHANGES_FULL_ACTION_DETERMINANT',
          s.expand(detalt-determinant_base) == 0
          and s.expand(detrep-determinant_base**2) == 0 and s.expand(detalt-detrep) != 0)

    # The same complement control at the actual golden value, symbolically.
    G = s.Matrix([[a, -p], [p, a]])
    Qg = s.BlockMatrix([[a*I2, -p*I2], [p*I2, a*I2]]).as_explicit()
    Jg, Pg = s.Matrix.vstack(a*I2, p*I2), s.diag(1, 0, 1, 0)
    Ug = (Qg*s.diag(G, I2)*Qg.T).applyfunc(golden)
    Lg = s.diag(G, G)
    check('ACTUAL_GOLDEN_COMPLEMENT_EXTENSIONS_ORTHOGONAL',
          gzero(Ug.T*Ug-s.eye(4)) and gzero(Lg.T*Lg-s.eye(4)))
    check('ACTUAL_GOLDEN_SAME_PREPARED_INCLUSION', gzero(Ug*Jg-Jg*G) and gzero(Lg*Jg-Jg*G))
    Fag, Frg = feedback(Pg, Ug).applyfunc(golden), feedback(Pg, Lg).applyfunc(golden)
    check('ACTUAL_GOLDEN_SAME_PREPARED_FEEDBACK', gzero((Fag-Frg)*Jg) and not gzero(Fag-Frg))
    check('ACTUAL_GOLDEN_DIFFERENT_FULL_COMPLEMENT_ACTION',
          golden((s.eye(4)-z*Fag).det()-(1-z*p*p)) == 0
          and golden((s.eye(4)-z*Frg).det()-(1-z*p*p)**2) == 0)

    # Transport the old readout, rather than silently activating its complement.
    return_feedback = lambda proj, C: proj*proj-proj*C.T*proj*C*proj
    old_projector = s.diag(1, 0)
    image_projector = (Jg*old_projector*Jg.T).applyfunc(golden)
    image_alt = feedback(image_projector, Ug).applyfunc(golden)
    image_rep = feedback(image_projector, Lg).applyfunc(golden)
    check('GOLDEN_OLD_READOUT_SAME_PREPARED_READING', gzero(image_projector*Jg-Pg*Jg))
    check('GOLDEN_OLD_READOUT_IS_DIFFERENT_FULL_EXPERIMENT', not gzero(image_projector-Pg))
    check('GOLDEN_OLD_READOUT_ACTION_IGNORES_INVISIBLE_COMPLETION',
          golden((s.eye(4)-z*image_alt).det()-(1-z*p*p)) == 0
          and golden((s.eye(4)-z*image_rep).det()-(1-z*p*p)) == 0)
    check('GOLDEN_ADDED_ACTIVE_RANGE_RETAINED',
          gzero((Pg-image_projector)*Jg)
          and gzero((Pg-image_projector)**2-(Pg-image_projector))
          and not gzero(Pg-image_projector))
    f0, f1 = s.symbols('f0 f1', real=True)
    check('LITERAL_CYLINDER_MULTIPLICATION_PULLBACK',
          s.diag(f0, f1, f0, f1) == lift(s.diag(f0, f1)))
    check('IMAGE_FILTER_CHANGES_ACTUAL_CHILD_POINT_READING',
          Pg[0, 0] == 1 and golden(image_projector[0, 0]-p) == 0
          and golden(Pg[0, 0]-image_projector[0, 0]-p*p) == 0)

    # Actual native words, no invariance of the prepared subspace and no resets.
    prepared_cases = []
    for label, native_U in [('direct', direct), ('recorded', recorded)]:
        for power in (1, 2, 3):
            full_word = (native_U**power).applyfunc(golden)
            C = (Jg.T*full_word*Jg).applyfunc(golden)
            leak = (full_word*Jg-Jg*C).applyfunc(golden)
            defect = (I2-C.T*C).applyfunc(golden)
            tag = f'{label}_{power}'
            check('NATIVE_FULL_WORD_ORTHOGONAL_LEAK_'+tag, gzero(Jg.T*leak))
            check('NATIVE_FULL_WORD_EXACT_NORM_DEFECT_'+tag, gzero(leak.T*leak-defect))
            for proj_label, proj in [('one', I2), ('proper', old_projector)]:
                readout = (Jg*proj*Jg.T).applyfunc(golden)
                Ffine = feedback(readout, full_word).applyfunc(golden)
                Freturn = return_feedback(proj, C).applyfunc(golden)
                tagp = tag+'_'+proj_label
                check('NATIVE_FULL_PREPARED_FEEDBACK_'+tagp, gzero(Ffine-Jg*Freturn*Jg.T))
                check('NATIVE_LEAKAGE_CORRECTION_'+tagp,
                      gzero(Freturn-feedback(proj, C)-proj*defect*proj))
                check('NATIVE_PREPARED_ACTION_DETERMINANT_'+tagp,
                      golden((s.eye(4)-z*Ffine).det()-(I2-z*Freturn).det()) == 0)
            prepared_cases.append([label, power])
    scalar_J = s.Matrix([a, p])
    c1 = (scalar_J.T*G*scalar_J)[0]
    c2 = (scalar_J.T*G**2*scalar_J)[0]
    check('OWNED_GOLDEN_PREPARED_FIRST_RETURN', golden(c1-a) == 0)
    check('OWNED_GOLDEN_PREPARED_SECOND_RETURN', golden(c2-(a*a-p*p)) == 0)
    check('FRESH_RESET_OR_COMPRESSED_POWER_SUBSTITUTION_REJECTED', golden(c2-c1*c1) != 0)
    check('OMITTING_ARCHIVE_LEAKAGE_GIVES_FALSE_ZERO_FEEDBACK',
          s.Matrix([[0]]) == feedback(s.eye(1), s.Matrix([[a]]))
          and golden(return_feedback(s.eye(1), s.Matrix([[a]]))[0, 0]-p*p) == 0)

    # All compatible readouts: image projector plus an orthogonal complementary one.
    for n in (1, 2, 3):
        m = n+2
        frame = reflection(m, 2)
        Jtest, Ktest = frame[:, :n], frame[:, n:]
        Ptest = s.diag(*([1]+[0]*(n-1)))
        Stest = Ktest*s.diag(1, 0)*Ktest.T
        Atest = Jtest*Ptest*Jtest.T
        Rtest = Atest+Stest
        check(f'COMPLETE_PROJECTOR_EXTENSION_{n}',
              Rtest*Rtest == Rtest and Rtest.T == Rtest and Rtest*Jtest == Jtest*Ptest
              and Stest*Jtest == s.zeros(m, n) and Jtest.T*Stest == s.zeros(n, m))
        check(f'EXTRA_ACTIVE_RANGE_HAS_OWN_READING_{n}',
              Stest*Ktest[:, 0] == Ktest[:, 0] and Atest*Ktest[:, 0] == s.zeros(m, 1))

    # Noncommuting moving preparation: delta J must enter the actual source.
    q = s.symbols('q', real=True)
    ct, st = (1-t*t)/(1+t*t), 2*t/(1+t*t)
    cq, sq = (1-q*q)/(1+q*q), 2*q/(1+q*q)
    moving_frame = s.Matrix([[1, 0, 0], [0, ct, -st], [0, st, ct]])
    moving_J = moving_frame[:, :2]
    core_U = s.Matrix([[cq, 0, -sq], [0, 1, 0], [sq, 0, cq]])
    covariant_U = moving_frame*core_U*moving_frame.T
    Ccov = (moving_J.T*covariant_U*moving_J).applyfunc(s.cancel)
    check('MOVING_NONCOMMUTING_PREPARATION_FULL_RETURN', Ccov == s.diag(cq, 1)
          and not zero(moving_frame*core_U-core_U*moving_frame))
    Fcov = return_feedback(I2, Ccov)
    covdet = (I2-z*Fcov).det()
    check('MOVING_PREPARATION_FRAME_SOURCE_CANCELS', s.diff(covdet, t) == 0)
    source_q = -2*z*cq*s.diff(cq, q)/(1-z+z*cq*cq)
    check('GENUINE_PREPARED_RETURN_SOURCE', s.cancel(-s.diff(covdet, q)/covdet-source_q) == 0)
    fixed_U = s.Matrix([[aa, 0, -pp], [0, 1, 0], [pp, 0, aa]])
    Cmoving = (moving_J.T*fixed_U*moving_J).applyfunc(s.cancel)
    Fmoving = return_feedback(I2, Cmoving)
    moving_det = s.factor((I2-z*Fmoving).det())
    moving_source = s.cancel(-s.diff(moving_det, t)/moving_det)
    source_value = moving_source.subs({t: s.Rational(1, 3), z: s.Rational(1, 4)})
    check('IGNORING_PREPARATION_DERIVATIVE_FALSE_ZERO_REJECTED', source_value != 0)
    # Genuine differential formula for all four independent compressed entries.
    entries = s.symbols('u0:4', real=True)
    Csym = s.Matrix(2, 2, entries)
    for proj_label, proj in [('one', I2), ('proper', old_projector)]:
        FF = return_feedback(proj, Csym)
        pencil = I2-z*FF
        det = pencil.det()
        for idx, entry in enumerate(entries):
            tangent = s.zeros(2)
            tangent[idx//2, idx % 2] = 1
            jacobi_source = s.trace(pencil.adjugate()*z*FF.diff(entry))/det
            native_source = -2*z*s.trace(pencil.adjugate()*proj*Csym.T*proj*tangent*proj)/det
            check(f'ALL_COMPRESSED_SOURCE_ENTRIES_{proj_label}_{idx}',
                  s.cancel(-s.diff(det, entry)/det-jacobi_source) == 0
                  and s.cancel(jacobi_source-native_source) == 0)
    # Rank and pole dependence in the proven analytic transfer cannot be dropped.
    eps = s.symbols('eps', positive=True)
    pole_z = 1-eps**2
    ratio = s.cancel((1-pole_z*(1-eps**2))/(1-pole_z))
    check('APPROACHING_POLE_DEFEATS_UNIFORM_CONTINUITY', ratio == 2-eps**2
          and s.limit(ratio, eps, 0) == 2)
    scalar_det = 1-z*(1-cq*cq)
    check('ACTIVE_RANK_FACTOR_IS_REAL', s.cancel(s.diag(*([scalar_det]*3)).det()-scalar_det**3) == 0)

    # Native GJ supplies the missing direction. Keep all four signed cross returns.
    T = s.BlockMatrix([[I2, a*I2], [s.zeros(2), p*I2]]).as_explicit()
    Ti = s.BlockMatrix([[I2, -a/p*I2], [s.zeros(2), I2/p]]).as_explicit()
    B = (Qg*T).applyfunc(golden)
    check('TWO_NATIVE_PREPARATIONS_LITERAL_COLUMNS', gzero(B[:, :2]-Jg)
          and gzero(B[:, 2:]-Qg*Jg))
    check('NONZERO_GOLDEN_BRANCH_INVERTS_BOTH_PREPARATIONS', zero(T*Ti-s.eye(4))
          and zero(Ti*T-s.eye(4)))
    check('TWO_PREPARATION_GRAM_AND_EXACT_CONDITIONING',
          gzero(B.T*B-s.BlockMatrix([[I2, a*I2], [a*I2, I2]]).as_explicit()))
    check('LITERAL_CYLINDER_READOUT_COMMUTES_WITH_NATIVE_FACTOR', zero(Qg*Pg-Pg*Qg))
    two_preparation_cases = []
    for label, native_U in [('direct', direct), ('recorded', recorded)]:
        for power in (1, 2, 3):
            full_word = (native_U**power).applyfunc(golden)
            returns = (B.T*full_word*B).applyfunc(golden)
            recovered = (Ti.T*returns*Ti).applyfunc(golden)
            tag = f'{label}_{power}'
            check('ALL_FOUR_NATIVE_RETURNS_RECOVER_FULL_OPERATOR_'+tag,
                  gzero(Qg*recovered*Qg.T-full_word))
            check('ALL_FOUR_NATIVE_RETURNS_RECOVER_LITERAL_FEEDBACK_'+tag,
                  gzero(feedback(Pg, recovered)-Qg.T*feedback(Pg, full_word)*Qg))
            check('ALL_FOUR_NATIVE_RETURNS_RECOVER_LITERAL_ACTION_'+tag,
                  golden((s.eye(4)-z*feedback(Pg, recovered)).det()
                         -(s.eye(4)-z*feedback(Pg, full_word)).det()) == 0)
            two_preparation_cases.append(tag)
    Ralt, Rrep = (B.T*Ug*B).applyfunc(golden), (B.T*Lg*B).applyfunc(golden)
    check('SECOND_NATIVE_PREPARATION_DETECTS_PRIOR_INVISIBLE_COMPLEMENT',
          gzero(Ralt[:2, :2]-Rrep[:2, :2]) and not gzero(Ralt-Rrep))
    # A true complement variation has a literal action source despite constant J return.
    complement_curve = (Qg*s.diag(I2, H)*Qg.T).applyfunc(golden)
    all_curve_returns = (B.T*complement_curve*B).applyfunc(golden)
    reconstructed_curve = (Ti.T*all_curve_returns*Ti).applyfunc(golden)
    curve_det = golden((s.eye(4)-z*feedback(Pg, complement_curve)).det())
    expected_curve_det = 1-4*z*t*t/(1+t*t)**2
    check('NATIVE_FIRST_PREPARATION_BLIND_TO_FULL_COMPLEMENT_VARIATION',
          gzero(Jg.T*complement_curve*Jg-I2))
    check('TWO_PREPARATIONS_RETAIN_FULL_COMPLEMENT_ACTION_SOURCE',
          s.cancel(curve_det-expected_curve_det) == 0 and gzero(reconstructed_curve-s.diag(I2, H)))
    genuine_complement_source = s.cancel(-s.diff(curve_det, t)/curve_det)
    complement_source_value = genuine_complement_source.subs({t:s.Rational(1, 3),z:s.Rational(1, 4)})
    check('IGNORING_SECOND_PREPARATION_FALSE_ZERO_SOURCE_REJECTED', complement_source_value != 0)
    recovered_det = golden((s.eye(4)-z*feedback(Pg, reconstructed_curve)).det())
    check('ALL_FOUR_RETURN_GENUINE_SOURCE_IDENTITY',
          s.cancel(-s.diff(recovered_det, t)/recovered_det-genuine_complement_source) == 0)
    # Even two diagonal amplitudes cannot distinguish G and G^T without cross readings.
    one_B = s.Matrix.hstack(G[:, :1], G*G[:, :1])
    left_reads = (one_B.T*G*one_B).applyfunc(golden)
    right_reads = (one_B.T*G.T*one_B).applyfunc(golden)
    check('DIAGONAL_RETURNS_ALONE_FALSE_TOMOGRAPHY_REJECTED',
          gzero(s.diag(*(left_reads-right_reads).diagonal())) and not gzero(left_reads-right_reads))
    check('ZERO_BRANCH_BREAKS_TWO_PREPARATION_COMPLETENESS', T.subs({a:1,p:0}).rank() == 2)

    # The owned recorded gate supplies cross RESPONSE terms without an amplitude oracle for U.
    def norm_sq(v):
        return (v.T*v)[0]

    def recovered_pairing(A, x, y):
        ax, ay = A*x, A*y
        qx, qy = norm_sq(ax), norm_sq(ay)
        mixed = norm_sq(a*ax-p*ay)
        return golden((a*a*qx+p*p*qy-mixed)/(2*a*p))

    recorded_response_cases = []
    for label, native_U in [('direct', direct), ('recorded', recorded)]:
        for power in (1, 2, 3):
            word = (native_U**power).applyfunc(golden)
            Aread = ((s.eye(4)-Pg)*word*Pg*B).applyfunc(golden)
            kernel = s.Matrix(4, 4, lambda i,j: recovered_pairing(
                Aread, s.eye(4)[:,i], s.eye(4)[:,j]))
            Fword = feedback(Pg, word).applyfunc(golden)
            Frecovered = (Qg*Ti.T*kernel*Ti*Qg.T).applyfunc(golden)
            tag = f'{label}_{power}'
            check('RECORDED_QUADRATIC_READINGS_RECONSTRUCT_COMPLETE_GRAM_'+tag,
                  gzero(kernel-B.T*Fword*B))
            check('RECORDED_QUADRATIC_READINGS_RECONSTRUCT_LITERAL_FEEDBACK_'+tag,
                  gzero(Frecovered-Fword))
            check('RECORDED_QUADRATIC_READINGS_RECONSTRUCT_OWNED_ACTION_'+tag,
                  golden((s.eye(4)-z*Frecovered).det()-(s.eye(4)-z*Fword).det()) == 0)
            for i in range(4):
                check(f'UNIT_NATIVE_PREPARATION_{tag}_{i}', golden(norm_sq(B[:,i])-1) == 0)
            recorded_response_cases.append(tag)

    # Exact complete carrier: comparison port/record, preparation flag, old target.
    def flagged(P):
        dim = P.rows
        Q = s.eye(dim)-P
        return s.BlockMatrix([[P,Q],[Q,P]]).as_explicit()

    native_recorded = recorded
    complete_operational_cases = []
    for dim in (1,2,3):
        old_U = reflection(dim,1)
        pframe = reflection(dim,2)
        old_P = pframe*s.diag(*([1]*((dim+1)//2)+[0]*(dim//2)))*pframe.T
        flag_op = flagged(old_P)
        common_op = s.diag(old_U,old_U)
        prep_stage = s.kronecker_product(s.eye(4),flag_op)
        word_stage = s.kronecker_product(s.eye(4),common_op)
        record_stage = s.kronecker_product(native_recorded,s.eye(2*dim))
        full_op = record_stage*word_stage*prep_stage
        check(f'FLAGGED_PREPARATION_RETAINS_ALL_BRANCHES_{dim}',
              flag_op*flag_op == s.eye(2*dim) and flag_op.T*flag_op == s.eye(2*dim))
        check(f'COMPLETE_COMPARISON_OPERATOR_FACTORIZATION_{dim}',
              gzero(full_op-s.kronecker_product(native_recorded,common_op*flag_op)))
        check(f'COMPLETE_COMPARISON_ORTHOGONAL_{dim}', gzero(full_op.T*full_op-s.eye(8*dim)))
        x,y = s.eye(dim)[:,0],s.eye(dim)[:,-1]
        blank_x,blank_y = x.col_join(s.zeros(dim,1)),y.col_join(s.zeros(dim,1))
        pair = blank_x.col_join(s.zeros(2*dim,1)).col_join(blank_y).col_join(s.zeros(2*dim,1))
        result = full_op*pair
        active_arm = result[:dim,0]
        returned = (s.eye(dim)-old_P)*active_arm
        reading_A = (s.eye(dim)-old_P)*old_U*old_P
        check(f'ACTUAL_JOINT_EVENT_IS_FEEDBACK_QUADRATIC_{dim}',
              gzero(returned-a*reading_A*x+p*reading_A*y))
        check(f'FIXED_FULL_INPUT_AND_OUTPUT_MASS_TWO_{dim}', norm_sq(pair) == 2 and golden(norm_sq(result)-2) == 0)
        check(f'RECORDED_AND_COMPLEMENT_BRANCHES_NOT_ERASED_{dim}',
              golden(norm_sq(result[:2*dim,0])+norm_sq(result[6*dim:8*dim,0])-2) == 0)
        clock,state = 0,pair
        stages = [prep_stage,word_stage,record_stage]+[s.eye(8*dim)]*13
        for _ in range(3):
            state = stages[clock]*state
            clock = (clock+1) % 16
        check(f'OWNED_INTERNAL_THREE_STAGE_PROGRAM_{dim}', clock == 3 and state == result)
        complete_operational_cases.append(dim)
    for event in (False,True):
        for record in (False,True):
            registered = (event, bool((not event) ^ record))
            inverse = (registered[0],bool((not registered[0]) ^ registered[1]))
            check(f'LITERAL_CYLINDER_FLAG_XOR_IS_REVERSIBLE_{event}_{record}', inverse == (event,record))

    test_P = s.diag(1,1,0,0)
    test_A = ((s.eye(4)-test_P)*recorded**2*test_P).applyfunc(golden)
    test_x,test_y = s.eye(4)[:,0],s.eye(4)[:,1]
    test_pair = golden(((test_A*test_x).T*(test_A*test_y))[0])
    qx,qy = norm_sq(test_A*test_x),norm_sq(test_A*test_y)
    qm = norm_sq(a*test_A*test_x-p*test_A*test_y)
    check('DEPHASING_BEFORE_RECORDING_FALSE_GRAM_REJECTED', test_pair != 0
          and golden((a*a*qx+p*p*qy-(a*a*qx+p*p*qy))/(2*a*p)-test_pair) != 0)
    check('DROPPING_FIXED_NORMALIZED_MIXED_FACTOR_TWO_REJECTED',
          golden((a*a*qx+p*p*qy-qm/2)/(2*a*p)-test_pair) != 0)
    check('BOTH_RECORDS_PRESERVE_QUADRATIC_RESPONSE',
          golden(norm_sq(a*test_A*test_x-p*test_A*test_y)
                 +norm_sq(p*test_A*test_x+a*test_A*test_y)-qx-qy) == 0)
    # The retained preparation is not postselection: its branch mass varies with P.
    basis_curve = s.Matrix([[ct,-st],[st,ct]])
    Pcurve = basis_curve*s.diag(1,0)*basis_curve.T
    Ureflect = s.diag(1,-1)
    Acurve = ((I2-Pcurve)*Ureflect*Pcurve).applyfunc(s.cancel)
    Fcurve = (Acurve.T*Acurve).applyfunc(s.cancel)
    initial = s.Matrix([1,0,0,0])
    prepared_state = flagged(Pcurve)*initial
    branch_mass = norm_sq(prepared_state[:2,0])
    physical_q = norm_sq(Acurve*s.Matrix([1,0]))
    postselected_q = s.cancel(physical_q/branch_mass)
    exact_det = s.factor((I2-z*Fcurve).det())
    wrong_det = s.factor(1-z*postselected_q)
    check('MOVING_FLAG_COMPLEMENT_RETAINS_FULL_NORM', s.cancel(norm_sq(prepared_state)-1) == 0
          and s.diff(branch_mass,t) != 0)
    check('POSTSELECTION_CHANGES_PREPARED_QUADRATIC_RESPONSE', s.cancel(physical_q-postselected_q) != 0)
    physical_query_source = s.cancel(-s.diff(1-z*physical_q,t)/(1-z*physical_q))
    postselect_query_source = s.cancel(-s.diff(wrong_det,t)/wrong_det)
    source_gap = s.cancel(physical_query_source-postselect_query_source).subs({t:s.Rational(1,3),z:s.Rational(1,4)})
    check('POSTSELECTION_CHANGES_GENUINE_QUERY_SOURCE', source_gap != 0)
    curve_kernel = s.Matrix(2,2,lambda i,j:s.cancel(((Acurve*s.eye(2)[:,i]).T*(Acurve*s.eye(2)[:,j]))[0]))
    check('MOVING_NATIVE_RECORDED_KERNEL_RETAINS_ACTUAL_SOURCE', zero(curve_kernel-Fcurve)
          and s.cancel(-s.diff((I2-z*curve_kernel).det(),t)/(I2-z*curve_kernel).det()
                       +s.diff(exact_det,t)/exact_det) == 0)
    e1,e2,e3 = s.symbols('e1 e2 e3', real=True)
    calibration_error = (a*a*e1+p*p*e2-2*e3)/(2*a*p)
    check('FIXED_READING_ERROR_FORMULA',
          s.expand(calibration_error*2*a*p-a*a*e1-p*p*e2+2*e3) == 0)
    check('ENTRYWISE_ERROR_NEEDS_MATRIX_DIMENSION_FACTOR', s.ones(3).eigenvals() == {3:1,0:2})

    # Whole existing bootstrap: no independently chosen geometric action or source.
    beta = s.symbols('beta', positive=True)
    hs, fs, hfine, copies, calibration = s.symbols('hs fs hfine copies calibration', real=True)
    thermal_cases = []
    for dim in (1,2,3,6):
        lam = s.symbols('lambda0:'+str(dim), real=True)
        vel = s.symbols('velocity0:'+str(dim), real=True)
        partition = sum(s.exp(-beta*(lam[i]+t*vel[i])) for i in range(dim))
        genuine_heat = s.diff(s.log(partition)/beta,t)
        expected_heat = -sum(s.exp(-beta*(lam[i]+t*vel[i]))*vel[i] for i in range(dim))/partition
        check('WHOLE_THERMAL_GENUINE_COVECTOR_'+str(dim), s.simplify(genuine_heat-expected_heat) == 0)
        check('REPLICATED_HEAT_COVECTOR_UNCHANGED_'+str(dim),
              s.simplify(s.diff(s.log(2*partition)/beta,t)-genuine_heat) == 0)
        shift_partition = sum(s.exp(-beta*(lam[i]+t)) for i in range(dim))
        check('UNIFORM_SHIFT_HAS_SOURCE_MINUS_ONE_'+str(dim),
              s.simplify(s.diff(s.log(shift_partition)/beta,t)+1) == 0)
        thermal_cases.append(dim)
    heat_poly = 1+12*t**20+10*t**22+8*t**24+2*t**33
    zone_terms = [s.Rational(nz,33)+(1-s.Rational(nz,33))*t**33+(nz-1)*t**dz
                  for nz,dz in [(9,24),(11,22),(13,20)]]
    check('ACTUAL_SCENE_HEAT_COEFFICIENTS_AND_TRACE33', s.expand(sum(zone_terms)-heat_poly) == 0
          and heat_poly.subs(t,1) == 33)
    check('JOINT_REPLICATED_SOURCE_IS_HEAT_PLUS_TWICE_FEEDBACK',
          s.expand((hs+2*fs)-(hs+fs)-fs) == 0)
    check('COARSE_STATIONARITY_REFINED_RESIDUAL_IS_FEEDBACK',
          (hs+2*fs).subs(hs,-fs) == fs)
    check('COARSE_STATIONARITY_REQUIRES_DOUBLED_FINE_THERMAL_SOURCE',
          s.expand((hfine+2*fs).subs(fs,-hs)-(hfine-2*hs)) == 0)
    calibration_equations = [1-calibration,copies-calibration]
    check('UNIVERSAL_SINGLE_CALIBRATION_ONLY_TRIVIAL_COPY',
          s.solve(calibration_equations,[copies,calibration]) == {copies:1,calibration:1})
    check('JOINT_SOURCE_CANCELLATION_NOT_SEPARATE_STATIONARITY',
          (hs+fs).subs({hs:-1,fs:1}) == 0 and (hs+2*fs).subs({hs:-1,fs:1}) == 1)

    # Fixed connected graph Laplacian and fixed Cayley rule; solve, do not fit sources.
    LP = s.Matrix([[t,-t],[-t,t]])
    PP = s.diag(1,0)
    UU = s.Matrix([[1-t*t,-2*t],[2*t,1-t*t]])/(1+t*t)
    FF = feedback(PP,UU)
    pencil = s.eye(2)-FF/2
    det_control = (1+t**4)/(1+t*t)**2
    feedback_source = 4*t*(1-t*t)/((1+t*t)*(1+t**4))
    heat_source = -2*s.exp(-2*t)/(1+s.exp(-2*t))
    control_source = heat_source+feedback_source
    check('CONTROL_LAPLACIAN_EXACT_ZERO_AND_POSITIVE_MODES', LP*s.Matrix([1,1]) == s.zeros(2,1)
          and LP*s.Matrix([1,-1]) == 2*t*s.Matrix([1,-1]))
    check('CONTROL_LAPLACIAN_EXACT_QUADRATIC_FORM',
          s.expand((s.Matrix([e1,e2]).T*LP*s.Matrix([e1,e2]))[0]-t*(e1-e2)**2) == 0)
    check('CONTROL_READOUT_IS_ORTHOGONAL_PROJECTION', zero(PP.T-PP) and zero(PP*PP-PP))
    check('CONTROL_CAYLEY_IS_ORTHOGONAL', zero(UU.T*UU-s.eye(2)))
    check('CONTROL_POSITIVE_PENCIL_EXACT_DIAGONAL', zero(pencil-s.diag(det_control,1)))
    check('CONTROL_DETERMINANT_NEVER_EMPTY_ON_REAL_LINE',
          s.cancel(pencil.det()-det_control) == 0 and (1+t*t).is_positive and (1+t**4).is_positive)
    check('CONTROL_FEEDBACK_SOURCE_IS_ACTUAL_LOGDET_DERIVATIVE',
          s.cancel(-s.diff(pencil.det(),t)/pencil.det()-feedback_source) == 0)
    control_partition = 1+s.exp(-2*t)
    check('CONTROL_HEAT_SOURCE_IS_ACTUAL_UNSHIFTED_GRAPH_TRACE_DERIVATIVE',
          s.simplify(s.diff(s.log(control_partition),t)-heat_source) == 0)
    check('CONTROL_COUPLED_SLICE_ENDPOINT_SOURCE_NEGATIVE', control_source.subs(t,0) == -1)
    feedback_half = feedback_source.subs(t,s.Rational(1,2))
    check('CONTROL_COUPLED_SLICE_ENDPOINT_SOURCE_POSITIVE_CERTIFICATE',
          feedback_half == s.Rational(96,85) and feedback_half-1 == s.Rational(11,85))
    E = s.symbols('E', positive=True)
    check('CONTROL_HEAT_LOWER_BOUND_FOR_EXP_MINUS_ONE',
          s.cancel(-2*E/(1+E)+1) == (1-E)/(1+E))
    fine_control_partition = 2*control_partition
    fine_control_det = pencil.det()**2
    genuine_coarse = s.diff(s.log(control_partition),t)-s.diff(pencil.det(),t)/pencil.det()
    genuine_fine = s.diff(s.log(fine_control_partition),t)-s.diff(fine_control_det,t)/fine_control_det
    check('CONTROL_GENUINE_JOINT_DERIVATIVES_RETAIN_BOTH_TERMS',
          s.simplify(genuine_coarse-control_source) == 0
          and s.simplify(genuine_fine-heat_source-2*feedback_source) == 0)
    check('CONTROL_REFINED_MINUS_COARSE_EXACTLY_FEEDBACK_SOURCE',
          s.cancel(genuine_fine-genuine_coarse-feedback_source) == 0)
    check('CONTROL_FEEDBACK_NONZERO_ON_OPEN_ROOT_INTERVAL',
          s.factor(feedback_source) == -4*t*(t-1)*(t+1)/((t*t+1)*(t**4+1)))

    # Actual source-port data; the degree operator is not a Dirac square.
    native_D = s.diag(24,22,20)
    native_A = s.Matrix([[0,11,13],[9,0,13],[9,11,0]])
    native_G = s.diag(9,11,13)
    native_GI = native_G.inv()
    native_K = native_D*native_A-native_A*native_D
    native_PA = -native_K*native_K/2840
    degree_port = (native_D-22*s.eye(3))*(native_D-20*s.eye(3))/8
    native_M = native_PA*degree_port*native_PA
    native_tau = s.trace(native_M)
    native_R = native_M/native_tau
    native_Q = native_PA-native_R
    Li = s.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,-1],[0,0,1,0]])
    Lj = s.Matrix([[0,0,-1,0],[0,0,0,1],[1,0,0,0],[0,-1,0,0]])
    native_X = s.kronecker_product(s.eye(3)-native_R,s.eye(4))+s.kronecker_product(native_R,Li)
    native_Y = s.kronecker_product(s.eye(3),Lj)
    native_G12 = s.kronecker_product(native_G,s.eye(4))
    check('SOURCE_ACTUAL_DEGREE_COMMUTATOR_BINDING',
          native_K == s.Matrix([[0,22,52],[-18,0,26],[-36,-22,0]]))
    check('SOURCE_ACTUAL_ACTIVE_PLANE_ANCHOR', zero(native_PA*native_PA-native_PA)
          and s.trace(native_PA) == 2 and zero(native_PA.T*native_G-native_G*native_PA))
    check('SOURCE_ACTUAL_MAX_DEGREE_POLYNOMIAL', degree_port == s.diag(1,0,0))
    check('SOURCE_ACTUAL_PORT_NORMALIZER_POSITIVE', native_tau == s.Rational(567,710))
    check('SOURCE_ACTUAL_TWO_PORTS_RETAIN_FULL_ACTIVE_PLANE',
          zero(native_R*native_R-native_R) and zero(native_Q*native_Q-native_Q)
          and zero(native_R*native_Q) and native_R+native_Q == native_PA)
    check('SOURCE_ACTUAL_METRIC_ORTHOGONAL_PORTS', zero(native_R.T*native_G-native_G*native_R)
          and zero(native_Q.T*native_G-native_G*native_Q))
    check('SOURCE_ACTUAL_SPIN_TWO_AND_FOUR_CONVENTION', Li*Li == -s.eye(4)
          and Lj*Lj == -s.eye(4) and Li*Lj == -Lj*Li)
    check('SOURCE_ACTUAL_COUPLED_MATRIX_ANCHOR',
          s.cancel(native_X[0,0]*native_X[4,5]-native_X[0,1]*native_X[4,4]) == s.Rational(5657,8946))
    check('SOURCE_ACTUAL_COUPLED_PAIRING', zero(native_X.T*native_G12*native_X-native_G12))
    check('SOURCE_CHRONOLOGICAL_Q8_ORDER_RETAINED', not zero(native_X*native_Y-native_Y*native_X))

    # Genuine primitive chain jets; the curve is a calculus control, not admitted M1 data.
    cancel_matrix = lambda X: X.applyfunc(s.cancel)
    Dt = native_D+t*s.diag(1,0,0)
    At = native_A
    Kt = Dt*At-At*Dt
    Pt = cancel_matrix(-Kt*Kt/2840)
    Et = cancel_matrix((Dt-22*s.eye(3))*(Dt-20*s.eye(3))/8)
    Mt = cancel_matrix(Pt*Et*Pt)
    Rt = cancel_matrix(Mt/s.cancel(s.trace(Mt)))
    Qt = Pt-Rt
    at0 = lambda X: X.subs(t,0)
    HD,HA = s.diag(1,0,0),s.zeros(3)
    dK = HD*native_A-native_A*HD+native_D*HA-HA*native_D
    dPA = -(dK*native_K+native_K*dK)/2840
    dE = (HD*(native_D-20*s.eye(3))+(native_D-22*s.eye(3))*HD)/8
    dM = dPA*degree_port*native_PA+native_PA*dE*native_PA+native_PA*degree_port*dPA
    dR = dM/native_tau-native_M*s.trace(dM)/native_tau**2
    check('SOURCE_COMMUTATOR_JET_FROM_SHARED_PRIMITIVES', zero(at0(Kt.diff(t))-dK))
    check('SOURCE_ACTIVE_JET_FROM_SHARED_PRIMITIVES', zero(at0(Pt.diff(t))-dPA))
    check('SOURCE_COMPRESSION_JET_FROM_SHARED_PRIMITIVES', zero(at0(Mt.diff(t))-dM))
    check('SOURCE_PORT_JET_INCLUDES_ACTUAL_NORMALIZER', zero(at0(Rt.diff(t))-dR))
    check('SOURCE_INPUT_JET_FROM_SAME_TWO_PRIMITIVES', zero(at0(Qt.diff(t))-(dPA-dR)))
    Xt = s.kronecker_product(s.eye(3)-Rt,s.eye(4))+s.kronecker_product(Rt,Li)
    dX = s.kronecker_product(dR,Li-s.eye(4))
    check('SOURCE_ACTUAL_INTERACTION_JET_FROM_SHARED_PRIMITIVES', zero(at0(Xt.diff(t))-dX))
    stages = [native_X,native_Y,native_X,native_Y]
    jets = [dX,s.zeros(12),dX,s.zeros(12)]
    word,jet = s.eye(12),s.zeros(12)
    for stage,variation in zip(stages,jets):
        word,jet = stage*word,variation*word+stage*jet
    # Exact tensor expansion keeps R^2, including curves leaving the projector class.
    Cmemory = Li-s.eye(4)
    linear_memory = Lj*Cmemory*Lj+Lj*Lj*Cmemory
    quadratic_memory = Lj*Cmemory*Lj*Cmemory
    expanded_word = s.kronecker_product(s.eye(3),Lj*Lj)+s.kronecker_product(native_R,linear_memory)+s.kronecker_product(native_R*native_R,quadratic_memory)
    check('SOURCE_FULL_WORD_EXACT_TENSOR_EXPANSION', zero(word-expanded_word))
    actual_word_jet = s.kronecker_product(at0(Rt.diff(t)),linear_memory)+s.kronecker_product(at0((Rt*Rt).diff(t)),quadratic_memory)
    check('SOURCE_FULL_WORD_JET_REUSES_ALL_PRIOR_STAGES', zero(actual_word_jet-jet))
    check('SOURCE_PRIMITIVE_CURVE_NOT_PROMOTED_TO_PROJECTOR_CLASS',
          not zero(at0((Pt*Pt-Pt).diff(t))))
    check('SOURCE_FROZEN_NORMALIZER_FALSE_JET_REJECTED', not zero(dM/native_tau-dR))

    # Strong cancellation control: a compression changes by scalar, its normalized port does not.
    scale_M = cancel_matrix(native_PA*Et*native_PA)
    scale_R = cancel_matrix(scale_M/s.cancel(s.trace(scale_M)))
    scale_dM = at0(scale_M.diff(t))
    scale_dR = scale_dM/native_tau-native_M*s.trace(scale_dM)/native_tau**2
    check('SOURCE_SCALAR_COMPRESSION_ACTUAL_TRACE_JET', s.trace(scale_dM) == s.Rational(1701,2840))
    check('SOURCE_NORMALIZED_PORT_EXACT_CANCELLATION', zero(at0(scale_R.diff(t))) and zero(scale_dR))
    check('SOURCE_OMITTED_NORMALIZER_PRODUCES_FALSE_NONZERO_RESPONSE',
          s.trace((scale_dM/native_tau)**2) == s.Rational(9,16))
    check('SOURCE_OMITTED_NORMALIZER_CHANGES_INTERACTION_JET',
          not zero(s.kronecker_product(scale_dM/native_tau,Li-s.eye(4))))

    # Shared basis covariance, with the canonical pairing and inverse moved together.
    frame = s.Matrix([[1,t,0],[0,1,t],[0,0,1]])
    frame_inv = frame.inv()
    conj = lambda X: frame*X*frame_inv
    Gframe = frame_inv.T*native_G*frame_inv
    GIframe = frame*native_GI*frame.T
    O = at0(frame.diff(t))
    frame_D,frame_A = cancel_matrix(conj(native_D)),cancel_matrix(conj(native_A))
    frame_K = cancel_matrix(frame_D*frame_A-frame_A*frame_D)
    frame_PA = cancel_matrix(-frame_K*frame_K/2840)
    frame_E = cancel_matrix((frame_D-22*s.eye(3))*(frame_D-20*s.eye(3))/8)
    frame_M = cancel_matrix(frame_PA*frame_E*frame_PA)
    frame_R = cancel_matrix(frame_M/s.cancel(s.trace(frame_M)))
    frame_Q = frame_PA-frame_R
    frame_joint = s.kronecker_product(frame,s.eye(4))
    frame_joint_inv = s.kronecker_product(frame_inv,s.eye(4))
    frame_X = s.kronecker_product(s.eye(3)-frame_R,s.eye(4))+s.kronecker_product(frame_R,Li)
    check('SOURCE_BASIS_HAS_TRUE_INVERSE_AND_POSITIVE_PAIRING', frame.det() == 1
          and zero(Gframe*GIframe-s.eye(3)))
    check('SOURCE_SHARED_ACTIVE_DEGREE_COMPRESSION_COVARIANCE', zero(frame_PA-conj(native_PA))
          and zero(frame_E-conj(degree_port)) and zero(frame_M-conj(native_M)))
    check('SOURCE_SHARED_NORMALIZED_TWO_PORT_COVARIANCE', zero(frame_R-conj(native_R))
          and zero(frame_Q-conj(native_Q)) and s.cancel(s.trace(frame_M)-native_tau) == 0)
    check('SOURCE_COUPLED_TENSOR_COVARIANCE', zero(frame_X-frame_joint*native_X*frame_joint_inv))
    frame_word = frame_joint*word*frame_joint_inv
    check('SOURCE_COMPLETE_WORD_COVARIANCE', zero(frame_word-
          (frame_joint*native_Y*frame_joint_inv)*frame_X*
          (frame_joint*native_Y*frame_joint_inv)*frame_X))
    weighted_F = lambda gram,gi,pp,uu: pp*gi*uu.T*gram*(s.eye(pp.rows)-pp)*uu*pp
    reversal = s.eye(3)-2*native_R
    F0 = weighted_F(native_G,native_GI,degree_port,reversal)
    frame_F = cancel_matrix(weighted_F(Gframe,GIframe,conj(degree_port),conj(reversal)))
    false_frame_F = cancel_matrix(weighted_F(native_G,native_GI,conj(degree_port),conj(reversal)))
    check('SOURCE_WEIGHTED_FEEDBACK_TRUE_COVARIANCE', zero(frame_F-conj(F0)))
    check('SOURCE_WEIGHTED_FEEDBACK_FRAME_JET', zero(at0(frame_F.diff(t))-(O*F0-F0*O)))
    check('SOURCE_METRIC_FRAME_JET_RETAINED', zero(at0(Gframe.diff(t))+O.T*native_G+native_G*O))
    check('SOURCE_INVERSE_METRIC_FRAME_JET_RETAINED', zero(at0(GIframe.diff(t))-O*native_GI-native_GI*O.T))
    check('SOURCE_INVERSE_METRIC_DERIVED_FROM_TWO_SIDED_IDENTITY',
          zero(at0(GIframe.diff(t))+native_GI*at0(Gframe.diff(t))*native_GI))
    native_det = (s.eye(3)-F0/2).det()
    frame_det = (s.eye(3)-frame_F/2).det()
    false_frame_det = (s.eye(3)-false_frame_F/2).det()
    false_frame_source = s.cancel(-s.diff(false_frame_det,t).subs(t,0)/false_frame_det.subs(t,0))
    check('SOURCE_WHOLE_FRAME_DETERMINANT_GENUINELY_CONSTANT',
          s.cancel(frame_det-native_det) == 0 and native_det == s.Rational(170969,252050))
    check('SOURCE_FREEZING_NATIVE_PAIRING_FALSE_WARD_REJECTED',
          false_frame_source == s.Rational(42588,170969) and false_frame_source != 0)

    # Actual moving eigenvectors: zero mode fixed, noncommuting jet, exact matrix exponential.
    beta0 = s.Rational(2,3)
    lambda0 = s.diag(0,20,33)
    lambda_jet = s.diag(0,1,-1)
    delta_curve = frame*(lambda0+t*lambda_jet)*frame_inv
    delta_jet = at0(delta_curve.diff(t))
    eig_exp = s.diag(1,s.exp(-beta0*20),s.exp(-beta0*33))
    heat_matrix = frame*s.diag(1,s.exp(-beta0*(20+t)),s.exp(-beta0*(33-t)))*frame_inv
    Z0 = s.trace(eig_exp)
    rho0 = eig_exp/Z0
    heat_operator_source = -s.trace(rho0*delta_jet)
    heat_curve_source = at0(s.trace(heat_matrix).diff(t))/(beta0*Z0)
    check('SOURCE_HEAT_CURVE_RETAINS_ZERO_MODE_AND_MOVING_EIGENVECTORS',
          delta_curve.det() == 0 and not zero(lambda0*delta_jet-delta_jet*lambda0))
    check('SOURCE_HEAT_JET_SPLITS_SPECTRUM_AND_FRAME', zero(delta_jet-lambda_jet-O*lambda0+lambda0*O))
    check('SOURCE_ACTUAL_MATRIX_EXPONENTIAL_HEAT_DERIVATIVE',
          s.simplify(heat_curve_source-heat_operator_source) == 0)
    check('SOURCE_HEAT_FRAME_WARD_IS_CYCLIC_TRACE', s.simplify(s.trace(rho0*(O*lambda0-lambda0*O))) == 0)
    check('SOURCE_HEAT_AND_FEEDBACK_WHOLE_BASIS_WARD',
          s.simplify(s.trace(rho0*(O*lambda0-lambda0*O))) == 0
          and s.cancel(s.diff(frame_det,t)) == 0)
    check('SOURCE_SPECTRAL_COEFFICIENT_HEAT_JET_NONZERO', heat_operator_source != 0)

    # Arbitrary finite noncommutative powers; all-size identities are proved in Lean.
    power_A = native_D-native_A
    power_V = s.Matrix([[0,1,2],[3,0,1],[0,-1,2]])
    power_cases = []
    power_jet = s.zeros(3)
    for m in range(1,6):
        power_jet = power_jet*power_A+power_A**(m-1)*power_V
        actual_power = (power_A+t*power_V)**m
        check('SOURCE_NONCOMMUTATIVE_POWER_GENUINE_JET_'+str(m), zero(at0(actual_power.diff(t))-power_jet))
        check('SOURCE_NONCOMMUTATIVE_POWER_CYCLIC_TRACE_'+str(m),
              s.trace(power_jet) == m*s.trace(power_A**(m-1)*power_V))
        power_cases.append(m)
    # Jacobi holds for arbitrary invertible pencils; this exact affine test is not the proof.
    Vfeedback = s.Matrix([[0,1,0],[1,0,2],[0,0,1]])
    N0 = s.eye(3)-F0/2
    Nt = N0-t*Vfeedback/2
    actual_logdet_jet = -at0(s.diff(Nt.det(),t))/N0.det()
    jacobi_source = s.trace(N0.inv()*Vfeedback)/2
    check('SOURCE_FEEDBACK_JACOBI_ACTUAL_DETERMINANT_JET', s.cancel(actual_logdet_jet-jacobi_source) == 0)

    # The same owned J and next history GJ resolve the whole spectral layer.
    spectral_history_cases = []
    for dim in (1,2,3):
        ii, oo = s.eye(dim), s.zeros(dim)
        gg = s.BlockMatrix([[a*ii,-p*ii],[p*ii,a*ii]]).as_explicit()
        tt = s.BlockMatrix([[ii,a*ii],[oo,p*ii]]).as_explicit()
        tti = s.BlockMatrix([[ii,-a/p*ii],[oo,ii/p]]).as_explicit()
        bb, bbi = gg*tt, tti*gg.T
        jj = s.Matrix.vstack(a*ii,p*ii)
        jj1 = gg*jj
        dd = s.diag(*range(dim))
        archive = dd+ii
        passive = lift(dd)
        first_only = (gg*s.diag(dd,archive)*gg.T).applyfunc(golden)
        check('HISTORY_SPECTRAL_FRAME_BOTH_INVERSES_'+str(dim),
              gzero(bb*bbi-s.eye(2*dim)) and gzero(bbi*bb-s.eye(2*dim)))
        check('HISTORY_SPECTRAL_FRAME_ACTUAL_COLUMNS_'+str(dim),
              gzero(bb[:,0:dim]-jj) and gzero(bb[:,dim:]-jj1))
        check('HISTORY_SPECTRAL_COMPLETE_PASSIVE_INTERTWINING_'+str(dim),
              gzero(passive*jj-jj*dd) and gzero(passive*jj1-jj1*dd))
        check('HISTORY_SPECTRAL_ONE_PREPARATION_DOES_NOT_FIX_SCENE_'+str(dim),
              gzero(first_only*jj-jj*dd) and not gzero(first_only-passive))
        e0,e1 = first_only*jj-jj*dd, first_only*jj1-jj1*dd
        defect = first_only*bb-bb*passive
        check('HISTORY_SPECTRAL_SECOND_PREPARATION_DETECTS_COMPLEMENT_'+str(dim),
              not gzero(e1) and gzero(defect-s.Matrix.hstack(e0,e1)))
        check('HISTORY_SPECTRAL_DEFECT_RECONSTRUCTS_FULL_SCENE_'+str(dim),
              gzero(defect*bbi-(first_only-passive)))
        check('HISTORY_SPECTRAL_SECOND_DEFECT_IS_ACTUAL_COMMUTATOR_'+str(dim),
              gzero(e1-(first_only*gg-gg*first_only)*jj))
        check('HISTORY_SPECTRAL_NONPASSIVE_COMPLETE_ONE_HISTORY_CLASS_'+str(dim),
              gzero(first_only.T-first_only) and not gzero(first_only*gg-gg*first_only))
        # Generic arbitrary full matrices also obey the complete reconstruction.
        generic = s.Matrix(2*dim,2*dim,lambda i,j:s.Rational((i+2*j)%7,5))
        generic_defect = generic*bb-bb*passive
        check('HISTORY_SPECTRAL_ARBITRARY_FULL_OPERATOR_DEFECT_'+str(dim),
              gzero(generic_defect*bbi-(generic-passive)))
        rr = s.diag(*[s.Rational(i+1,dim*(dim+1)//2) for i in range(dim)])
        ddd = s.diag(*[i+1 for i in range(dim)])
        ev = s.diag(*range(2*dim))
        dfine = lift(ddd)+ev
        coarse_covector = -s.trace(rr*ddd)
        fine_covector = -s.trace(lift(rr)*dfine)/2
        check('HISTORY_SPECTRAL_GIBBS_DEFECT_CONTRACTION_'+str(dim),
              s.cancel(fine_covector-coarse_covector+s.trace(lift(rr)*ev)/2)==0)
        cross_null = s.BlockMatrix([[oo,ii],[ii,oo]]).as_explicit()
        check('HISTORY_SPECTRAL_NONZERO_RESPONSE_NULL_DEFECT_RETAINED_'+str(dim),
              cross_null != s.zeros(2*dim) and s.trace(lift(rr)*cross_null)==0)
        check('HISTORY_SPECTRAL_FALSE_NORMALIZER_OMISSION_REJECTED_'+str(dim),
              -s.trace(lift(rr)*lift(ddd))==2*coarse_covector and coarse_covector != 0)
        # At t=0 both intertwinings hold, but their jets need not hold.
        dcurve = dd+t*ddd
        fullcurve = (gg*s.diag(dcurve,dcurve+t*ii)*gg.T).applyfunc(golden)
        historycurve = fullcurve*bb-bb*lift(dcurve)
        check('HISTORY_SPECTRAL_POINT_COMPATIBILITY_DOES_NOT_FIX_SOURCE_'+str(dim),
              gzero(historycurve.subs(t,0)) and not gzero(historycurve.diff(t).subs(t,0)))
        fine_jet = fullcurve.diff(t).subs(t,0)
        check('HISTORY_SPECTRAL_POINT_DEFECT_GENUINE_FIRST_JET_RECONSTRUCTION_'+str(dim),
              gzero(historycurve.diff(t).subs(t,0)*bbi-(fine_jet-lift(ddd))))
        partition_coarse = sum(s.exp(-beta*(i+t*(i+1))) for i in range(dim))
        partition_archive = sum(s.exp(-beta*(i+t*(i+2))) for i in range(dim))
        hcoarse = s.diff(s.log(partition_coarse)/beta,t).subs(t,0)
        hfine = s.diff(s.log(partition_coarse+partition_archive)/beta,t).subs(t,0)
        check('HISTORY_SPECTRAL_POINT_GENUINE_THERMAL_SOURCE_DIFFERS_'+str(dim),
              s.simplify(hfine-hcoarse+s.Rational(1,2))==0)
        spectral_history_cases.append(dim)

    # Actual 33-coordinate scene profile, with its zero mode and multiplicities.
    profile = [(0,1),(20,12),(22,10),(24,8),(33,2)]
    moment_poly = sum(mult*level*t**level for level,mult in profile)
    check('HISTORY_SPECTRAL_ACTUAL_SCENE_GIBBS_NORMALIZATION33',
          sum(mult for _,mult in profile)==33 and
          s.expand(sum(mult*t**level for level,mult in profile)-heat_poly)==0 and
          s.expand(moment_poly-t*s.diff(heat_poly,t))==0)
    check('HISTORY_SPECTRAL_SCENE_ZERO_MODE_RETAINED_IN_SCALE_JET',
          profile[0]==(0,1) and moment_poly.subs(t,0)==0 and heat_poly.subs(t,0)==1)
    check('HISTORY_SPECTRAL_COARSE_TANGENT_DOUBLING_CONTRACTION_NECESSARY',
          s.solve(s.Eq(hs- s.Rational(1,2)*s.Symbol('trace_defect'),2*hs),
                  s.Symbol('trace_defect'))==[-2*hs])


    payload = {
        'status': 'PASS', 'owner_input_head': HEAD, 'scope': SCOPE, 'checks': checks,
        'input_sha256': pins, 'proof_sha256': sha(PROOF),
        'checker_sha256': sha(BASE+'_check.py'), 'receipt_sha256': sha(BASE+'_results.json'),
        'exact_results': {
            'compiled_propositions': len(declarations), 'all_block_fixture_dimensions': cases,
            'complete_class': 'U=[[aI,-pR^T],[pS,aSR^T+V]]; all six constraints retained',
            'one_return_feedback': 'p^2 I',
            'two_return_retained': 'a^2 I-p^2 R^T S',
            'nonminimal_third_return': 'a^3-epsilon*p^2',
            'native_two_step_feedback': ['4*p^3 I2', '2*p^3 (I2+X)'],
            'native_composed_action_gap': '-log(1-4*z*p^3)',
            'native_second_return_probability_gap': '2*p^3',
            'actual_completion_source': '-16*p^3*z*t/((1+t^2)*(1+t^2-4*z*p^3))',
            'joint_refinement': 'L(U)J=JU; F(L(P),L(U)^k)=L(F(P,U^k))',
            'raw_action_and_source_refinement_factor': 2,
            'same_prepared_inclusion_determines_full_action': False,
            'complete_fine_readout': 'R=J P J^T+S; S^T=S; S^2=S; SJ=0',
            'full_prepared_return': 'C_word=J^T U_word J; not a power of C_1',
            'full_preparation_defect': 'L^T L=I-C_word^T C_word',
            'prepared_feedback': 'F(P,C)+P(I-C^T C)P=P-PC^TPCP',
            'prepared_action_refinement_factor': 1,
            'literal_cylinder_value_pullback': 'L(diag f); image filter differs on child point reading by p^2',
            'native_prepared_word_cases': prepared_cases,
            'moving_preparation_nonzero_source_control': str(source_value),
            'fixed_readout_action_bound': '2*r*z/(1-z)*norm(C-D)',
            'moving_readout_action_bound': 'n*z/(1-z)*(4*norm(P-Q)+2*norm(C-D))',
            'preparation_operator_error_bound': 'norm(U-V)+2*norm(J-K)',
            'approaching_pole_gap_limit': 'log(2)',
            'native_two_preparation_frame': '[J,GJ]=G[[I,aI],[0,pI]]',
            'full_operator_from_four_returns': 'U=G T^(-T) R T^(-1) G^T',
            'literal_action_from_four_returns': 'S(F(L(P),U))=S(F(L(P),T^(-T) R T^(-1)))',
            'native_two_preparation_word_cases': two_preparation_cases,
            'two_preparation_inverse_squared_norm': '1/(1-abs(a))',
            'full_complement_genuine_source_control': str(complement_source_value),
            'recorded_response_native_word_cases': recorded_response_cases,
            'complete_operational_fixture_dimensions': complete_operational_cases,
            'recorded_pairing_formula': '(a^2*qx+p^2*qy-2*normalized_mixed_reading)/(2*a*p)',
            'full_flagged_comparison': '(fullStep tensor I)*(I4 tensor L(U))*(I4 tensor flagged(P))',
            'fixed_comparison_input_norm_squared': 2,
            'native_recorded_action': 'S(F(L(P),U))=S(T^(-T) K T^(-1)); K=B^T F B',
            'quadratic_entry_error_bound': '3*epsilon/(2*abs(a*p))',
            'feedback_error_bound': 'm*3*epsilon/(2*abs(a*p)*(1-abs(a)))',
            'direct_feedback_action_bound': '2*r*z/((1-z)*(1-abs(a)))*norm(K-Khat)',
            'postselection_query_source_gap_control': str(source_gap),
            'whole_bootstrap': 'beta^(-1)*log(sum_i exp(-beta*lambda_i))-log(det(I-zF))',
            'whole_thermal_covector': '-sum_i exp(-beta*lambda_i)*v_i/sum_i exp(-beta*lambda_i)',
            'thermal_fixture_dimensions': thermal_cases,
            'actual_scene_heat_polynomial': str(heat_poly),
            'binary_heat_action_shift': 'beta^(-1)*log(2)',
            'joint_binary_source': 'heat+2*feedback',
            'stationarity_transfer_on_coarse_slice': 'fineHeat=2*heat',
            'uniform_spectral_shift_source': -1,
            'stationary_control_graph_spectrum': ['0','2*t'],
            'stationary_control_root_interval': '0<t<1/2; IVT existence compiled in Lean',
            'stationary_control_is_whole_native_root': False,
            'stationary_control_feedback_source': str(feedback_source),
            'stationary_control_heat_source': str(heat_source),
            'stationary_control_endpoint_sources': ['-1','at least 11/85'],
            'stationary_control_refined_source_on_root': 'feedbackSource(t)>0',
            'actual_source_port_chain': 'D,A -> [D,A] -> Pact,degreePort -> compressed,trace -> signalPort,inputPort -> coupled',
            'actual_source_port_normalizer': str(native_tau),
            'actual_source_port_jet': 'dR=dM/tau-trace(dM)*M/tau^2',
            'actual_source_interaction_jet': 'dR tensor (spin(2)-I)',
            'full_retained_word_jet': 'sum_j U_m...U_(j+1)*dU_j*U_(j-1)...U_1',
            'moving_native_pairing': 'G+=T^(-T)*G*T^(-1); GI+=T*GI*T^T',
            'whole_operator_source': '-trace(rho*dDelta)+trace(z*(I-zF)^(-1)*dF)',
            'whole_operator_basis_Ward': 'actual whole action invariant; genuine derivative zero',
            'source_normalizer_cancellation_trace_jet': '1701/2840',
            'false_frozen_normalizer_response': '9/16',
            'false_frozen_pairing_source': str(false_frame_source),
            'noncommutative_power_jet_controls': power_cases,
            'two_history_passive_spectral_class': 'DeltaPlus=L(Delta) iff both J and GJ intertwine',
            'full_history_spectral_defect_reconstruction': 'DeltaPlus-L(Delta)=EH*B^(-1)',
            'second_history_scene_defect': 'e1=[DeltaPlus,G]J when e0=0',
            'spectral_history_fixture_dimensions': spectral_history_cases,
            'required_spectral_jet_contraction': 'trace(L(rho)*EV)=-2*heat',
            'pointwise_history_compatibility_implies_source_compatibility': False,
            'nonzero_thermal_response_null_defects_retained': True,
            'native_spectral_passivity_forced_by_M1': False,
            'general_heat_Jacobi_formal_status': 'ANALYTIC_PROOF; finite jets and declared moving spectral factorization compiled',

        },
    }
    if args.output:
        args.output.write_text(json.dumps(payload, sort_keys=True, indent=2)+'\n')
    else:
        expected = args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_COMPOSED_FEEDBACK_DYNAMICS', len(checks), 'controls', len(declarations), 'Lean propositions')


if __name__ == '__main__':
    main()
