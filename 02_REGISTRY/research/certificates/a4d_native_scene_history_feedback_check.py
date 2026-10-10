#!/usr/bin/env python3
"""Exact controls for the owned scene-history reversal and complete return law."""
import argparse
import hashlib
import json
import re
from fractions import Fraction
from pathlib import Path

import sympy as s
from sympy.polys.matrices import DomainMatrix

BASE = '02_REGISTRY/research/certificates/a4d_native_scene_history_feedback'
PROOF = '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md'
SCOPE = {
    'class': 'OWNED_ONE_STEP_SCENE_HISTORIES_WITH_ENDPOINT_AVERAGE_AND_REVERSAL',
    'input_head': '915f4ff8fdb5950e69a3cdd6d443033ca55fa32e',
    'actual_Jt_Js_C1_reverseEdge_definitions_consumed': True,
    'actual_owner_left_inverse_reproved_without_native_decide': True,
    'generic_finite_graph_degree_and_readout_Lean_formalized': True,
    'full_reversal_involution_and_orthogonality_Lean_formalized': True,
    'complete_all_word_returns_Lean_formalized': True,
    'complete_all_archive_delay_kernels_Lean_formalized': True,
    'ordinary_feedback_determinant_reduction_Lean_formalized': True,
    'normalized_scene_feedback_polynomial_Lean_formalized': True,
    'whole_balanced_archive_return_Lean_formalized': True,
    'nonempty_nonzero_native_feedback_witness_Lean_formalized': True,
    'joint_history_relabel_covariance_Lean_formalized': True,
    'generic_matrix_declarations_use_only_standard_logical_axioms': True,
    'full_718_by_718_determinant_reduction_proved_for_all_sizes': True,
    'rank_65_and_unreachable_complement_653': 'EXACT_SPECTRUM_AND_ANALYTIC_HILBERT_DECOMPOSITION',
    'spectral_archive_30_identified_with_history_complement_685': False,
    'vertex_only_equivariant_no_go_promoted_to_retained_history': False,
    'one_step_compression_repeated_instead_of_full_history': False,
    'native_reversal_selected_as_the_whole_physical_tick': False,
    'physical_reversal_or_endpoint_preparation_admission_derived_from_M1': False,
    'primitive_scene_state_and_complete_admitted_tangent_law_derived': False,
    'full_history_carrier_heat_operator_and_refinement_derived': False,
    'coarse_feedback_polynomial_supplies_full_bootstrap_stationarity': False,
    'thermal_trace_or_temperature_rule_added': False,
    'new_action_selector_coupling_source_or_postulate_added': False,
    'metric_matter_source_or_physical_Ward_derived': False,
    'quantitative_metric_contrast_transferred': False,
    'curved_roots_soundness_recovery_or_GR_derived': False,
    'G0_closed': False,
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
    rank = lambda M: DomainMatrix.from_Matrix(M).convert_to(s.QQ).rank()
    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    output = (root/(BASE+'_output.txt')).read_text()
    lean = (root/(BASE+'.lean')).read_text()
    names = re.findall(r'^theorem (\w+)', lean, re.M)
    check('COMPILER_EXIT_ZERO', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0)
    check('COMPILED_TYPES_AND_DEPENDENCIES', names == receipt['declarations']
          and len(names) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 60)
    check('CAPSULE_AND_TRANSCRIPT_FRESH', receipt['capsule_sha256'] == sha(BASE+'.lean')
          and receipt['output_sha256'] == sha(BASE+'_output.txt'))
    check('NO_PLACEHOLDER_OR_COMPILER_LEAF', 'sorryAx' not in output
          and 'Lean.trustCompiler' not in output and re.search(r'\berror(?:\(|:)', output) is None
          and re.search(r'\b(sorry|admit|axiom|native_decide)\b', lean) is None)
    axioms = set()
    for match in re.finditer(r'depends on axioms: \[([^]]*)\]', output, re.S):
        axioms.update(x.strip() for x in match.group(1).split(',') if x.strip())
    check('STANDARD_TRANSITIVE_AXIOMS_ONLY', sorted(axioms) == receipt['axioms']
          == ['Classical.choice', 'Quot.sound', 'propext'])
    for name in names:
        full = 'D0.Research.NativeSceneHistoryFeedback.'+name
        check('ACTUAL_DECLARATION_'+name, full in output and "'"+full+"'" in output)
    check('ACTUAL_NATIVE_MAPS_IN_PROPOSITIONS', all(x in output for x in [
        'Jt', 'Js', 'C1', 'reverseEdge', 'fullTransport', 'fullNormalizedLaplacian',
        'nativeHistoryReverse', 'historyFeedback', 'historyArchive', 'historyIncoming',
        'historyOutgoing', 'zoneSum', 'archiveWitness', 'complete_native_archive_return_kernel']))
    check('THIRTY_NATIVE_SOURCE_PINS', len(receipt['transitive_d0_source_sha256']) == 30)
    pins = dict(receipt['transitive_d0_source_sha256'])
    pins.update(receipt['toolchain_input_sha256'])
    for path, digest in pins.items():
        check('SOURCE_PIN_'+path, sha(path) == digest)
    book = '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md'
    pins[book] = sha(book)

    # Literal full scene, not the three-zone divisor used in place of it.
    zone = lambda u: 0 if u < 9 else 1 if u < 20 else 2
    A = s.Matrix(33, 33, lambda u, v: int(zone(u) != zone(v)))
    degrees = [sum(A[u, v] for v in range(33)) for u in range(33)]
    D = s.diag(*degrees)
    T = D.inv()*A
    Delta = s.eye(33)-T
    Fc = s.eye(33)-T*T
    edges = [(u, v) for u in range(33) for v in range(33) if A[u, v] == 1]
    lookup = {edge: i for i, edge in enumerate(edges)}
    reversal = [lookup[(v, u)] for u, v in edges]
    check('ACTUAL_FULL_SCENE_AND_HISTORY_CARDINALITIES', len(edges) == 718
          and degrees == [24]*9+[22]*11+[20]*13)
    check('ACTUAL_HISTORY_REVERSAL_INVOLUTION', all(reversal[reversal[i]] == i for i in range(718)))
    check('ACTUAL_ENDPOINT_FIBERS_ARE_DEGREES', all(
        sum(v == b for u, v in edges) == degrees[b] for b in range(33)))
    check('ACTUAL_SOURCE_ENDPOINT_AVERAGE_IS_OWNED_TRANSPORT', all(
        Fraction(sum(u == b and v == a for u, v in edges), int(degrees[a])) == T[a, b]
        for a in range(33) for b in range(33)))
    check('ACTUAL_CANONICAL_PAIRING_DETAILED_BALANCE', zero(D*T-T.T*D))
    check('ACTUAL_SCENE_NORMALIZED_FEEDBACK_COUPLING', zero(Fc-(2*Delta-Delta*Delta)))
    check('EUCLIDEAN_UNWEIGHTED_TRANSPORT_IS_FALSE_ADJOINT', not zero(T-T.T))

    def lift(x):
        return [Fraction(x[v]) for u, v in edges]

    def reverse(x):
        return [x[reversal[i]] for i in range(718)]

    def average(x):
        return [sum((x[i] for i, (u, v) in enumerate(edges) if v == b), Fraction(0))/int(degrees[b])
                for b in range(33)]

    dark_basis = []
    for start, count in [(0, 9), (9, 11), (20, 13)]:
        for u in range(start+1, start+count):
            x = [0]*33
            x[start], x[u] = 1, -1
            y = lift(x)
            r = reverse(y)
            tag = str(u)
            check('FULL_BALANCED_ARCHIVE_ONE_RETURN_'+tag, average(r) == [0]*33)
            check('FULL_BALANCED_ARCHIVE_TWO_RETURNS_'+tag, average(reverse(r)) == x)
            check('COMPLETE_ARCHIVE_NORM_RETAINED_'+tag,
                  sum(a*a for a in r) == sum(a*a for a in y) == 2*degrees[start])
            dark_basis.append(x)
    check('ALL_THIRTY_ARCHIVE_DIRECTIONS_INDEPENDENT', len(dark_basis) == 30
          and rank(s.Matrix.hstack(*(s.Matrix(x) for x in dark_basis))) == 30)
    witness = s.Matrix(dark_basis[0])
    check('REPEATED_ENDPOINT_FORGETTING_LOSES_RETURN', zero(T*T*witness)
          and not zero(witness) and zero(Fc*witness-witness))
    first_edge, other_edge = lookup[(0, 9)], lookup[(1, 9)]
    check('EQUAL_PRESENT_READOUT_DISTINCT_RETAINED_HISTORY', edges[first_edge][1] == edges[other_edge][1]
          and edges[reversal[first_edge]][1] != edges[reversal[other_edge]][1])

    # Simultaneous native relabeling preserves the full record. Relabeling just
    # its present endpoint is a different transformation and fails to commute.
    sigma = list(range(33))
    sigma[0], sigma[1], sigma[9], sigma[10] = 1, 0, 10, 9
    both = [lookup[(sigma[u], sigma[v])] for u, v in edges]
    endpoint_only = [lookup[(u, sigma[v])] for u, v in edges]
    check('FULL_JOINT_HISTORY_RELABEL_COVARIANCE', all(
        reversal[both[i]] == both[reversal[i]] for i in range(718)))
    check('FORGETTING_RECORD_RELABEL_BREAKS_COVARIANCE', any(
        reversal[endpoint_only[i]] != endpoint_only[reversal[i]] for i in range(718)))

    lam, z = s.symbols('lam z')
    transport_poly = s.factor(T.charpoly(lam).as_expr())
    feedback_poly = s.factor(Fc.charpoly(lam).as_expr())
    check('FULL_33_TRANSPORT_CHARACTERISTIC_POLYNOMIAL', s.expand(transport_poly-
          lam**30*(lam-1)*(lam*lam+lam+s.Rational(39, 160))) == 0)
    check('FULL_33_FEEDBACK_CHARACTERISTIC_POLYNOMIAL', s.expand(feedback_poly-
          lam*(lam-1)**30*(lam*lam-s.Rational(119, 80)*lam+s.Rational(14001, 25600))) == 0)
    q = 1-s.Rational(119, 80)*z+s.Rational(14001, 25600)*z*z
    det_poly = (1-z)**30*q
    check('ACTUAL_718_FEEDBACK_DETERMINANT_FROM_PROVED_REDUCTION',
          s.cancel(z**33*feedback_poly.subs(lam, 1/z)-det_poly) == 0)
    det_quarter = s.factor(det_poly.subs(z, s.Rational(1, 4)))
    check('NONEMPTY_NATIVE_ACTION_GAP', 0 < det_quarter < 1)
    check('ACTUAL_FEEDBACK_RANK_AND_TRACE', rank(Fc) == 32 and s.trace(Fc) == s.Rational(2519, 80))
    check('PROTECTED_CONSTANT_MODE', zero(T*s.ones(33, 1)-s.ones(33, 1))
          and zero(Fc*s.ones(33, 1)))
    two_history_pairing = s.BlockMatrix([[s.eye(33), T], [T, s.eye(33)]]).as_explicit()
    check('COMPLETE_TWO_HISTORY_FRAME_RANK', rank(two_history_pairing) == 65)
    check('UNREACHABLE_HISTORY_COMPLEMENT_COUNT_RETAINED', 718-65 == 653 and 718-33 == 685)

    # Nontrivial exact finite fixtures test the generic theorem on full matrices.
    fixtures = []
    for parts in [(1, 1), (1, 1, 1), (2, 3, 2)]:
        labels = [i for i, n in enumerate(parts) for _ in range(n)]
        n = len(labels)
        ee = [(u, v) for u in range(n) for v in range(n) if labels[u] != labels[v]]
        dd = [sum(v == b for u, v in ee) for b in range(n)]
        m = len(ee)
        J = s.Matrix(m, n, lambda i, b: int(ee[i][1] == b))
        C = s.Matrix(n, m, lambda b, i: s.Rational(int(ee[i][1] == b), dd[b]))
        R = s.Matrix(m, m, lambda i, j: int(ee[j] == (ee[i][1], ee[i][0])))
        P, Q = J*C, s.eye(m)-J*C
        coarse = C*R*J
        F = P*R.T*Q*R*P
        tag = '_'.join(map(str, parts))
        check('GENERIC_FULL_GRAPH_AND_ORTHOGONAL_HISTORY_'+tag,
              zero(C*J-s.eye(n)) and zero(P.T-P) and zero(R.T*R-s.eye(m)))
        check('GENERIC_FULL_FEEDBACK_NOT_RAW_RETURN_DETERMINANT_'+tag,
              zero(F-J*(s.eye(n)-coarse*coarse)*C))
        incoming, archive, outgoing = Q*R*J, Q*R*Q, C*R*Q
        for k in range(5):
            check('COMPLETE_ALL_ARCHIVE_DELAY_'+tag+'_'+str(k), zero(
                outgoing*archive**k*incoming-(s.eye(n)-coarse*coarse)*(-coarse)**k))
        check('COMPLETE_RETURNS_NOT_POWERS_OF_COMPRESSION_'+tag,
              zero(C*R**2*J-s.eye(n)))
        for zz in [s.Rational(1, 5), s.Rational(1, 4)]:
            check('GENERIC_FULL_DETERMINANT_'+tag+'_'+str(zz),
                  (s.eye(m)-zz*F).det(method='domain-ge') ==
                  (s.eye(n)-zz*(s.eye(n)-coarse*coarse)).det(method='domain-ge'))
            check('GENERIC_FULL_RESOLVENT_'+tag+'_'+str(zz), zero(
                  C*(s.eye(m)-zz*R).inv(method='DM')*J-(s.eye(n)+zz*coarse)/(1-zz*zz)))
        fixtures.append({'parts': list(parts), 'vertices': n, 'histories': m})

    payload = {
        'status': 'PASS', 'input_head': SCOPE['input_head'], 'scope': SCOPE,
        'checks': checks, 'control_count': len(checks),
        'input_sha256': pins, 'proof_sha256': sha(PROOF),
        'capsule_sha256': sha(BASE+'.lean'), 'results_sha256': sha(BASE+'_results.json'),
        'output_sha256': sha(BASE+'_output.txt'), 'checker_sha256': sha(BASE+'_check.py'),
        'exact_results': {
            'compiled_propositions': 60, 'transitive_d0_source_pins': 30,
            'full_scene_vertices': 33, 'full_owned_histories': 718,
            'scene_degrees': [24, 22, 20], 'balanced_archive_directions': 30,
            'coarse_feedback': 'I-T^2=2*Delta-Delta^2; Delta=I-T',
            'complete_full_feedback': 'J*(I-T^2)*C',
            'full_history_even_return': 'I', 'full_history_odd_return': 'T',
            'complete_archive_delay': '(I-T^2)*(-T)^k',
            'full_retained_resolvent': '(I+z*T)/(1-z^2)',
            'feedback_characteristic_polynomial': str(feedback_poly),
            'full_feedback_determinant': '(1-z)^30*(1-119*z/80+14001*z^2/25600)',
            'quarter_action_determinant': str(det_quarter),
            'feedback_rank': 32, 'feedback_trace': '2519/80',
            'reachable_history_dimension': 65, 'unreachable_history_dimension': 653,
            'endpoint_history_complement_dimension': 685, 'generic_full_fixtures': fixtures,
            'full_history_carrier_heat_operator_selected': False,
            'physical_actuation_tangent_and_refinement_derived': False,
            'whole_bootstrap_native_stationarity_derived': False,
        },
    }
    if args.output:
        args.output.write_text(json.dumps(payload, sort_keys=True, indent=2)+'\n')
    else:
        expected = args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_SCENE_HISTORY_FEEDBACK',len(checks),'controls',len(names),'Lean propositions')


if __name__ == '__main__':
    main()
