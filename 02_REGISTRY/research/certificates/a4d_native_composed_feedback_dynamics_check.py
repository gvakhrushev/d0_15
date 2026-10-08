#!/usr/bin/env python3
"""Exact controls for complete golden-active-block joint dynamics and refinement."""
import argparse
import hashlib
import json
import re
from pathlib import Path

import sympy as s

HEAD = '609e7daa7c801254ee671874750c5bc61f4efc71'
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
          and len(declarations) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 56)
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
           'joint', 'goldenInclusion', 'fullFeedback', 'feedbackAction', 'liftOperator']))
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
