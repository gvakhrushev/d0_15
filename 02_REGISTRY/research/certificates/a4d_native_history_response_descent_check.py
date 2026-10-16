#!/usr/bin/env python3
"""Exact controls for the generic history/descent proofs and the owned golden gate."""
import argparse
import hashlib
import itertools
import json
import re
from pathlib import Path

import sympy as s

HEAD = 'ad2e43f4eae418d6fe7386d37c7ee4c76400ed42'
BASE = '02_REGISTRY/research/certificates/a4d_native_history_response_descent'
PROOF = '02_REGISTRY/research/A4D_NATIVE_HISTORY_RESPONSE_DESCENT.md'
PLAN = '02_REGISTRY/research/D0_NATIVE_CORE_EXECUTION_PLAN_2026-10-08.md'
SCOPE = {
    'future_quotient': 'ALL_FINITE_WORDS_OF_THE_DECLARED_INTERNAL_OPERATION_FAMILY',
    'complete_future_equivalence_Lean_formalized': True,
    'realized_response_tower_Lean_formalized': True,
    'actual_maps_and_process_naturality_Lean_formalized': True,
    'truncations_surjective_Lean_formalized': True,
    'generic_finite_table_theorem_assumes_finite_operations_and_readout': True,
    'all_depths_equal_iff_full_future_equal_Lean_formalized': True,
    'finite_depth_autonomy_requires_full_future_factorization': True,
    'full_archive_history_Lean_formalized': True,
    'joint_source_schur_equivalence_Lean_formalized': True,
    'archive_determinant_and_source_derivative_Lean_formalized': True,
    'generic_three_block_assembly': 'ANALYTIC_UNIQUENESS_PROOF_WITH_EXACT_NONCOMMUTING_CONTROLS',
    'native_witness': 'OWNED_GOLDEN_COHERENT_MEMORY_FULLSTEP_REUSED_TWICE',
    'both_present_marginals_equal_Lean_formalized': True,
    'native_two_return_gap_Lean_formalized': True,
    'native_depth_two_separation_Lean_formalized': True,
    'complete_response_local_constancy_Lean_formalized': True,
    'actual_profinite_finite_factorization_owner_consumed': True,
    'compact_compatible_history_realization_Lean_formalized': True,
    'compact_local_constancy_implies_finite_realized_range': True,
    'golden_cylinder_expectation_descent_Lean_formalized': True,
    'golden_cylindrical_amplitude_weights_Lean_formalized': True,
    'golden_refinement_pairing_and_operator_naturality_Lean_formalized': True,
    'refined_factor_blank_preparation_by_owned_inverse_gate_Lean_formalized': True,
    'profinite_point_process_identified_with_hilbert_amplitude_process': False,
    'fresh_blank_inserted_between_two_reuses': False,
    'both_recorded_preparations_forced_by_M1': False,
    'physical_feedback_action_replaced_by_U_determinant': False,
    'finite_outcome_detector_implies_finite_probability_space': False,
    'infinite_compatible_table_always_has_native_realization': False,
    'fixed_depth_process_is_automatically_autonomous': False,
    'full_native_history_dynamics_bound_to_golden_tower': False,
    'condensed_sheaf_descent_derived': False,
    'whole_core_state_preparation_exhausted': False,
    'source_fitted_from_chosen_root': False,
    'singular_archive_inverse_admitted': False,
    'discarded_directions_are_physical_gauge': False,
    'metric_matter_source_or_Ward_derived': False,
    'physical_time_or_spatial_geometry_derived': False,
    'soundness_or_recovery_proved': False,
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

    zero = lambda matrix: all(s.cancel(x) == 0 for x in matrix)
    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    text = (root/(BASE+'_output.txt')).read_text()
    lean = (root/(BASE+'.lean')).read_text()
    declarations = re.findall(r'^theorem (\w+)', lean, re.M)
    check('COMPILER_EXIT_ZERO', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0)
    check('CAPSULE_AND_TRANSCRIPT_FRESH', receipt['capsule_sha256'] == sha(BASE+'.lean')
          and receipt['output_sha256'] == sha(BASE+'_output.txt'))
    check('EVERY_ACTUAL_PROPOSITION_PRINTED', declarations == receipt['declarations']
          and len(declarations) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 42)
    check('NO_PROOF_PLACEHOLDER_OR_COMPILER_ERROR', 'sorryAx' not in text and 'error:' not in text
          and re.search(r'\b(sorry|admit|axiom)\b', lean) is None)
    axioms = set()
    for match in re.finditer(r'depends on axioms: \[([^]]*)\]', text, re.S):
        axioms.update(x.strip() for x in match.group(1).split(',') if x.strip())
    check('TRANSITIVE_STANDARD_LOGICAL_AXIOMS_ONLY', sorted(axioms) == receipt['axioms']
          == ['Classical.choice', 'Quot.sound', 'propext'])
    for name in declarations:
        check('ACTUAL_DECLARATION_'+name, 'D0.Research.NativeHistoryResponseDescent.'+name in text
              and "'D0.Research.NativeHistoryResponseDescent."+name+"'" in text)
    check('REAL_PROPOSITIONS_NOT_FLAGS', all(x in text for x in
          ['Function.Surjective', 'FutureEq', 'HasDerivAt', 'Finite', 'responseTree', 'fullStep',
           'Profinite', 'DiscreteQuotient', 'CompactSpace', 'IsLocallyConstant', 'cylWeight', 'goldenRefine']))
    pins = dict(receipt['transitive_d0_source_sha256'])
    pins.update(receipt['toolchain_input_sha256'])
    for path, digest in pins.items():
        check('SOURCE_PIN_'+path, sha(path) == digest)

    # The table is the realized image, so all tests use actual states and operations.
    states = tuple(range(7))
    labels = (0, 1)
    transition = lambda label, x: max(x-1, 0) if label == 0 else (x+2) % 7
    read = lambda x: x % 2

    def tree(depth, x):
        return read(x) if depth == 0 else (read(x), tuple(tree(depth-1, transition(a, x)) for a in labels))

    def trim(depth, r):
        return r[0] if depth == 0 else (r[0], tuple(trim(depth-1, t) for t in r[1]))

    cardinalities = []
    for depth in range(5):
        coarse = {tree(depth, x) for x in states}
        fine = {tree(depth+1, x) for x in states}
        cardinalities.append(len(coarse))
        check(f'REALIZED_SURJECTIVE_TRUNCATION_{depth}', {trim(depth, r) for r in fine} == coarse)
        check(f'FINITE_CARDINAL_BOUND_{depth}', len(coarse) <= 2**(2**(depth+1)-1))
        for a in labels:
            check(f'ALL_STATES_PROCESS_DESCENT_{depth}_{a}', all(
                tree(depth+1, x)[1][a] == tree(depth, transition(a, x)) for x in states))
            check(f'ALL_STATES_PROCESS_NATURALITY_{depth}_{a}', all(
                trim(depth, tree(depth+2, x)[1][a]) == trim(depth+1, tree(depth+2, x))[1][a]
                for x in states))
    check('PRESENT_OUTPUT_IS_NOT_AUTONOMOUS_CONTROL', read(0) == read(2)
          and read(transition(0, 0)) != read(transition(0, 2)))
    check('DELAYED_DIFFERENCE_IS_RETAINED', tree(0, 0) == tree(0, 2) and tree(1, 0) != tree(1, 2))
    for depth in range(9):
        countdown = lambda k: tuple(int(max(k-j, 0) == 0) for j in range(depth+1))
        check(f'INFINITE_FIBER_NOT_IMPLIED_BY_FINITE_REALIZATIONS_{depth}',
              countdown(depth+1) == (0,)*(depth+1) and countdown(depth)[-1] == 1)

    # Reuse the exact joint gate; never partial-trace-and-reprepare between steps.
    a, p, z = s.symbols('a p z', real=True)
    reduce_golden = lambda expr: s.rem(s.rem(s.expand(expr), a*a-p, a), p*p+p-1, p).expand()
    W = s.Matrix([[a, 0, -p, 0], [0, a, 0, -p], [0, p, 0, a], [p, 0, a, 0]])
    plus, minus = s.Matrix([a, 0, 0, p]), s.Matrix([a, 0, 0, -p])

    def retained(v):
        return s.Matrix([[v[0]**2+v[1]**2, v[0]*v[2]+v[1]*v[3]],
                         [v[0]*v[2]+v[1]*v[3], v[2]**2+v[3]**2]])

    def archive(v):
        return s.Matrix([[v[0]**2+v[2]**2, v[0]*v[1]+v[2]*v[3]],
                         [v[0]*v[1]+v[2]*v[3], v[1]**2+v[3]**2]])

    def read_z(v):
        return v[0]**2+v[1]**2-v[2]**2-v[3]**2

    check('OWNED_W_ORTHOGONAL', all(reduce_golden(x) == 0 for x in W.T*W-s.eye(4)))
    check('OWNED_RECORD_PREPARATION', W*s.Matrix([1, 0, 0, 0]) == plus)
    check('BOTH_NORMALIZED', all(reduce_golden((v.T*v)[0]-1) == 0 for v in [plus, minus]))
    check('BOTH_PRESENT_MARGINALS_IDENTICAL', retained(plus) == retained(minus)
          and archive(plus) == archive(minus))
    check('CORRELATIONS_NOT_EQUAL', not zero(plus*plus.T-minus*minus.T))
    check('FIRST_Z_RETURN_MISSES_MEMORY', s.expand(read_z(W*plus)-read_z(W*minus)) == 0)
    gap = s.expand(read_z(W**2*plus)-read_z(W**2*minus))
    check('EXACT_TWO_RETURN_RAW_GAP', s.expand(gap-8*a*a*p*p*(p*p-a*a)) == 0)
    check('EXACT_GOLDEN_TWO_RETURN_GAP', reduce_golden(gap+8*p**6) == 0)
    check('WRONG_GAP_SIGN_REJECTED', reduce_golden(gap-8*p**6) != 0)
    check('BINARY_PROBABILITY_GAP', reduce_golden(
        retained(W**2*plus)[0, 0]-retained(W**2*minus)[0, 0]+4*p**6) == 0)
    # Erasing correlations to the common diagonal density matrix removes the gap.
    rho_plus, rho_minus = plus*plus.T, minus*minus.T
    dephase = lambda rho: s.diag(*rho.diagonal())
    z_readout = s.diag(1, 1, -1, -1)
    erased_plus, erased_minus = dephase(rho_plus), dephase(rho_minus)
    erased_gap = s.trace(z_readout*W**2*(erased_plus-erased_minus)*(W.T)**2)
    check('DISCARDED_CORRELATIONS_GIVE_FAKE_EQUALITY',
          erased_plus == erased_minus and erased_gap == 0
          and rho_plus != erased_plus and reduce_golden(gap) != 0)
    projection = s.diag(1, 1, 0, 0)
    F = (projection*W.T*(s.eye(4)-projection)*W*projection)[:2, :2]
    check('NATIVE_ONE_RETURN_FEEDBACK', F == p*p*s.eye(2))
    det_u = (s.eye(4)-z*W).det()
    det_f = (s.eye(2)-z*F).det()
    check('FULL_U_CHARACTERISTIC', reduce_golden(det_u-(1-z*z)*(1-2*a*z+z*z)) == 0)
    check('FEEDBACK_ACTION_U_SUBSTITUTION_REJECTED', reduce_golden(det_u-det_f) != 0
          and s.expand(det_f-(1-z*p*p)**2) == 0)

    def cylinder_weight(word):
        return p**sum(1 if b else 2 for b in word)

    for depth in range(6):
        words = list(itertools.product([True, False], repeat=depth))
        check(f'OWNED_GOLDEN_CYLINDER_TOTAL_MASS_{depth}',
              reduce_golden(sum(cylinder_weight(w) for w in words)-1) == 0)
        # Compare coefficients of every independently variable parent reading.
        check(f'ALL_PARENT_READING_COEFFICIENTS_DESCEND_{depth}', all(
            reduce_golden(cylinder_weight(w+(True,))+cylinder_weight(w+(False,))-cylinder_weight(w)) == 0
            for w in words))
    check('NON_GOLDEN_WEIGHT_REFINEMENT_FAILS', s.Rational(1, 2)+s.Rational(1, 4) != 1)
    G = s.Matrix([[a, -p], [p, a]])
    factor = s.Matrix([a, p])
    check('REFINED_GOLDEN_FACTOR_BORN_WEIGHTS', reduce_golden(factor[0]**2-p) == 0
          and factor[1]**2 == p*p)
    check('OWNED_INVERSE_GATE_PREPARES_BLANK', all(reduce_golden(x) == 0
          for x in G.T*factor-s.Matrix([1, 0])))
    u, v, up, vp = s.symbols('u v up vp', real=True)
    parent_vec, other_vec = s.Matrix([u, v]), s.Matrix([up, vp])
    Jg = s.kronecker_product(s.eye(2), factor)
    check('FULL_SYMBOLIC_GOLDEN_REFINEMENT_PAIRING', reduce_golden(
        ((Jg*parent_vec).T*(Jg*other_vec))[0]-(parent_vec.T*other_vec)[0]) == 0)
    AA = s.Matrix(2, 2, s.symbols('A:4'))
    check('ARBITRARY_LINEAR_OPERATOR_NATURALITY', s.kronecker_product(AA, s.eye(2))*Jg == Jg*AA)
    check('PREPARATION_IS_REVERSIBLE_NOT_RECORD_ERASURE', all(reduce_golden(x) == 0
          for x in G.T*G-s.eye(2)) and G.det() != 0)

    # Retain initial archive and every prior input on a coupled noncommuting system.
    A = s.Matrix([[1, 1], [0, 1]])
    B = s.Matrix([[1, 0], [1, 1]])
    C = s.Matrix([[0, 1], [-1, 0]])
    D = s.Matrix([[1, 1], [1, 0]])
    x, y0 = s.Matrix([2, -1]), s.Matrix([1, 3])
    y = y0
    history = []
    for n in range(7):
        forced = sum((D**(n-1-j)*C*history[j] for j in range(n)), s.zeros(2, 1))
        check(f'COMPLETE_ARCHIVE_AND_ACTIVE_HISTORY_{n}', y == D**n*y0+forced
              and A*x+B*y == A*x+B*D**n*y0+B*forced)
        history.append(x)
        x, y = A*x+B*y, C*x+D*y
    check('INITIAL_ARCHIVE_IS_NOT_ZERO_BY_DEFAULT', B*y0 != s.zeros(2, 1))
    delay = s.zeros(4)
    for i in range(3):
        delay[i+1, i] = 1
    bc, cc = s.Matrix([[0, 0, 0, 1]]), s.Matrix([1, 0, 0, 0])
    check('ARBITRARILY_TRUNCATED_KERNEL_CAN_RETURN_LATER',
          all(bc*delay**k*cc == s.zeros(1) for k in range(3)) and bc*delay**3*cc == s.ones(1))

    # Six-dimensional, noncommuting three-block system. Every source is independent.
    K = s.Matrix([[8, 1, 1, 0, 2, -1], [0, 9, 0, 2, 1, 1],
                  [1, -1, 10, 1, 1, 2], [2, 1, 0, 11, -1, 1],
                  [1, 0, 2, 1, 12, 1], [-1, 2, 1, -1, 0, 13]])
    K33 = K[4:6, 4:6]
    J = K[:4, :4]-K[:4, 4:6]*K33.inv()*K[4:6, :4]
    H = K[2:6, 2:6]
    direct = K[:2, :2]-K[:2, 2:6]*H.inv()*K[2:6, :2]
    nested = J[:2, :2]-J[:2, 2:4]*J[2:4, 2:4].inv()*J[2:4, :2]
    check('NONSYMMETRIC_NONCOMMUTING_DOMAIN', K != K.T and K33*J[2:4, 2:4] != J[2:4, 2:4]*K33)
    check('ALL_REQUIRED_PIVOTS_INVERTIBLE', K.det() != 0 and K33.det() != 0
          and J[2:4, 2:4].det() != 0 and H.det() != 0)
    check('NESTED_OPERATOR_EQUALS_DIRECT', direct == nested)
    check('NESTED_FULL_DETERMINANTS', K.det() == K33.det()*J[2:4, 2:4].det()*nested.det()
          and K.det() == H.det()*direct.det())
    for j in range(6):
        source = s.eye(6)[:, j]
        b1 = source[:4, :]-K[:4, 4:6]*K33.inv()*source[4:6, :]
        fn = b1[:2, :]-J[:2, 2:4]*J[2:4, 2:4].inv()*b1[2:4, :]
        fd = source[:2, :]-K[:2, 2:6]*H.inv()*source[2:6, :]
        xf = direct.inv()*fd
        yf = H.inv()*(source[2:6, :]-K[2:6, :2]*xf)
        check(f'INDEPENDENT_SOURCE_AND_EXACT_RECONSTRUCTION_{j}', fn == fd
              and K*xf.col_join(yf) == source)
    check('FITTING_ARCHIVE_SOURCE_WOULD_CHANGE_RETAINED_SOURCE',
          K[:2, 2:6]*H.inv() != s.zeros(2, 4))
    # Analytic variation of Schur, with every entry direction, including archive blocks.
    Ai, Bi, Ci, Di = K[:2, :2], K[:2, 2:6], K[2:6, :2], H
    Di_inv, Si_inv = Di.inv(), direct.inv()
    for i in range(6):
        for j in range(6):
            dK = s.zeros(6)
            dK[i, j] = 1
            dA, dB, dC, dD = dK[:2, :2], dK[:2, 2:6], dK[2:6, :2], dK[2:6, 2:6]
            dS = dA-dB*Di_inv*Ci+Bi*Di_inv*dD*Di_inv*Ci-Bi*Di_inv*dC
            full = -s.trace(K.inv()*dK)
            both = -s.trace(Di_inv*dD)-s.trace(Si_inv*dS)
            check(f'FULL_SOURCE_VARIATION_ALL_ENTRY_DIRECTIONS_{i}_{j}', full == both)
    archive_direction = s.diag(0, 0, 1, 0, 0, 0)
    check('OMITTED_ARCHIVE_DETERMINANT_SOURCE_DETECTED',
          s.trace(Di_inv*archive_direction[2:6, 2:6]) != 0)
    singular = s.Matrix([[1, 0], [0, 0]])
    check('SINGULAR_ARCHIVE_HAS_UNIQUE_RECONSTRUCTION_FAILURE', singular*s.Matrix([0, 1]) == s.zeros(2, 1)
          and singular.det() == 0)
    # Generic two-block coefficient signs, without finite-sample interpolation.
    aa, bb, cc, dd, xx, ff, gg = s.symbols('aa bb cc dd xx ff gg', nonzero=True)
    yy = (gg-cc*xx)/dd
    check('ALL_SCALAR_SYMBOLIC_SOURCE_SIGNS', s.cancel(aa*xx+bb*yy-ff
          - ((aa-bb*cc/dd)*xx-(ff-bb*gg/dd))) == 0)
    check('WRONG_SCHUR_SIGN_REJECTED', s.cancel(aa*xx+bb*yy-ff
          - ((aa+bb*cc/dd)*xx-(ff-bb*gg/dd))) != 0)

    payload = {
        'status': 'PASS', 'owner_input_head': HEAD, 'scope': SCOPE, 'checks': checks,
        'input_sha256': pins, 'proof_sha256': sha(PROOF), 'plan_sha256': sha(PLAN),
        'checker_sha256': sha(BASE+'_check.py'), 'receipt_sha256': sha(BASE+'_results.json'),
        'exact_results': {
            'compiled_propositions': len(declarations),
            'native_two_return_readout_gap': '-8*p^6',
            'native_binary_probability_gap': '-4*p^6',
            'native_present_marginals': 'both diag(p,p^2)',
            'canonical_depth_finite_fixture_cardinalities': cardinalities,
            'nested_elimination_source_directions': 6,
            'full_action_source_entry_directions': 36,
            'future_quotient': 'x~y iff all admitted finite-word readouts agree',
            'archive_feedback_pencil': 'I-zF with F=P U^dagger Q U P; not I-zU',
            'profinite_factorization': 'whole finite-depth locally constant response factors through an owned finite quotient',
            'compact_realization': 'nested closed realized fibers have a common state',
            'golden_refinement': 'J x=x tensor (a,p); a^2=p; p+p^2=1; G^T(a,p)=(1,0)',
            'G0_closed': False,
        },
    }
    if args.output:
        args.output.write_text(json.dumps(payload, sort_keys=True, indent=2)+'\n')
    else:
        expected = args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_HISTORY_RESPONSE_DESCENT', len(checks), 'controls', len(declarations), 'Lean propositions')


if __name__ == '__main__':
    main()
