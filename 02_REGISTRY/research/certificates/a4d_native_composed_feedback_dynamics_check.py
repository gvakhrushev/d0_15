#!/usr/bin/env python3
"""Exact controls for complete golden-active-block joint dynamics and refinement."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import sympy as s

HEAD = '7c204c9d0e6a405216f9762ddd4d4d55ba57dab4'
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
          and len(declarations) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 115)
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
    check('FIVE_TRANSITIVE_NATIVE_SOURCE_PINS', len(receipt['transitive_d0_source_sha256']) == 5
          and '03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean' in receipt['transitive_d0_source_sha256'])
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
