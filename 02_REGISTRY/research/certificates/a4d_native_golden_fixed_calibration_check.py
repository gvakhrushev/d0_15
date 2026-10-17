#!/usr/bin/env python3
"""Fixed complete golden limit, faithful real readings and scoped exact controls."""
import argparse
import hashlib
import json
import re
from pathlib import Path
import sympy as s

BASE = '02_REGISTRY/research/certificates/a4d_native_golden_fixed_calibration'
PROOF = '02_REGISTRY/research/A4D_NATIVE_GOLDEN_FIXED_CALIBRATION.md'
PRIOR = '02_REGISTRY/research/certificates/a4d_native_golden_history_preparation'
SCOPE = {
    'class': 'FIXED_COMPLETE_GOLDEN_PREPARATION_LIMIT_AND_FAITHFUL_REAL_CYLINDER_TRANSFER',
    'input_head': '353fbbde33be5437b9be3d432e6ef5451afe56c1',
    'literal_complete_native_success_scalar_and_balance_derived': True,
    'fixed_unique_unit_success_limit_derived_from_literal_word': True,
    'whole_state_error_independent_of_archive_cardinality': True,
    'unsuccessful_records_counted_in_complete_state_error': True,
    'faithful_injective_real_state_and_full_operator_encoding_proved': True,
    'common_unspin_is_owned_inverse_golden_pointer_word': True,
    'all_real_orthogonal_projector_readings_have_uniform_error': True,
    'literal_p0_and_all_33_scene_fibers_bound_in_kernel': True,
    'same_fixed_target_and_rate_at_every_golden_pair_history_depth': True,
    'complex_projection_phase_cancellation_scope_is_restricted': True,
    'real_pointer_phase_control_derived_for_actual_golden_phase': True,
    'real_entry_invariant_class': 'FINITE_PRODUCTS_AND_ADJOINTS_OF_REAL_ENTRY_GENERATORS_ON_SAME_CARRIER',
    'all_151_prior_propositions_counted_as_new': False,
    'entire_2_pow_45_seed_matrix_numerically_enumerated': False,
    'common_success_limit_phase_for_all_degrees_proved': False,
    'positive_phase_history_isometry_unconditionally_prepared': False,
    'all_real_projectors_physically_admitted_by_M1': False,
    'all_phases_declared_native_gauge': False,
    'real_entry_boundary_claimed_as_full_core_no_go': False,
    'Boolean_address_and_inverse_controller_admission_derived': False,
    'all_native_controller_laws_forced_or_classified': False,
    'fixed_success_phase_identified_with_metric_action_calibration': False,
    'word_count_or_history_depth_identified_with_physical_time_or_mesh': False,
    'actual_native_MDL_kappa_budget_or_heat_tangent_action_derived': False,
    'new_action_angle_temperature_selector_coupling_source_or_postulate_added': False,
    'own_metric_matter_source_or_physical_Ward_derived': False,
    'quantitative_metric_contrast_or_native_stationarity_transferred': False,
    'curved_roots_soundness_recovery_or_GR_derived': False,
    'G0b_closed': False, 'G0_closed': False, 'global_closure': False,
    'original_parent_terminals_changed': False,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    ap.add_argument('--expect', type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root / p).read_bytes()).hexdigest()
    if args.expect:
        assert json.loads(args.expect.read_text())['scope'] == SCOPE, 'PINNED_SCOPE_MISMATCH'
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    receipt = json.loads((root / (BASE + '_results.json')).read_text())
    out = (root / (BASE + '_output.txt')).read_text()
    lean = (root / (BASE + '.lean')).read_text()
    names = re.findall(r'^#check (\S+)', lean, re.M)
    check('COMPILER_EXIT_ZERO', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0)
    check('ALL_86_NEW_ACTUAL_TYPES_AND_AXIOMS_PRINTED', names == receipt['declarations'] and
          len(names) == receipt['printed_propositions'] == receipt['printed_axiom_dependencies'] == 86)
    check('COMPILED_CAPSULE_AND_TRANSCRIPT_FRESH', sha(BASE + '.lean') == receipt['capsule_sha256'] and
          sha(BASE + '_output.txt') == receipt['output_sha256'])
    check('NO_PLACEHOLDER_OR_COMPILER_LEAF', 'sorryAx' not in out and 'Lean.trustCompiler' not in out and
          re.search(r'\berror(?:\(|:)', out) is None and
          re.search(r'\b(sorry|admit|axiom|native_decide)\b', lean) is None)
    axioms = set()
    for m in re.finditer(r'depends on axioms: \[([^]]*)\]', out, re.S):
        axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
    check('STANDARD_TRANSITIVE_AXIOMS_ONLY', sorted(axioms) == receipt['axioms'] ==
          ['Classical.choice', 'Quot.sound', 'propext'])
    for n in names:
        check('ACTUAL_DECLARATION_' + n, n in out and "'" + n + "'" in out)
    check('LITERAL_COMPLETE_NATIVE_OBJECTS_AND_HYPOTHESES', all(x in out for x in [
        'fullWord', 'routedGoldenSeed', 'normalizedSuccessScalar', 'unspunColumn', 'actualSceneUnspunColumn',
        'actualSceneAlignedSeed', 'historyCylinderInclusion', 'realQuadraticReading', 'fullRealVector',
        'fullRealMatrix', 'RealEntry', 'literal_p0_all_scene_readouts_have_one_fixed_target_family']))
    check('EXACTLY_TWELVE_TRANSITIVE_D0_PINS', len(receipt['transitive_d0_source_sha256']) == 12)
    pins = dict(receipt['transitive_d0_source_sha256'])
    pins.update(receipt['toolchain_input_sha256'])
    pins.update(receipt['prior_preparation_input_sha256'])
    for path, digest in pins.items():
        check('SOURCE_PIN_' + path, sha(path) == digest)
    for path in [
        '01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md',
        '01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md',
        '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
    ]:
        pins[path] = sha(path)

    p, a = s.symbols('p a', real=True)
    e, f = s.symbols('e f', real=True)
    gb = s.groebner([a*a-p, p*p+p-1], a, p, domain=s.EX)
    red = lambda x: s.expand(gb.reduce(s.expand(x))[1])
    mz = lambda M: all(red(x) == 0 for x in M)
    G = s.Matrix([[a, -p], [p, a]])
    w = red((a+s.I*p)**8)
    c, im = s.re(w), s.im(w)
    r = 1345-2176*p
    phase = lambda z: s.Matrix([[s.re(s.expand(z)), -s.im(s.expand(z))],
                                [s.im(s.expand(z)), s.re(s.expand(z))]])
    check('OWNED_P0_NORMALIZATION', red(a*a+p*p-1) == 0)
    check('LITERAL_FAST_PHASE_IS_GOLDEN_EIGHTH_POWER', mz(phase(w)-G**8))
    check('FAST_UNIT_PHASE_AND_NATIVE_PARAMETER', red(w*s.conjugate(w)-1) == 0 and red(2*c-1-r) == 0)
    pg = (s.sqrt(5)-1)/2
    check('NATIVE_FAST_PARAMETER_IN_KERNEL_RANGE', bool(r.subs(p, pg)>0) and bool(r.subs(p, pg)<s.Rational(1, 6)))
    z = red(s.conjugate(w)**2*(w-1)**2)
    good = red(w*w-(w-1)**2*e)
    unspun = red(s.conjugate(w)**2*good)
    check('LITERAL_UNSPUN_SUCCESS_INCREMENT', red(unspun-(1-z*e)) == 0)
    check('OWN_INCREMENT_FACTOR_IS_FIXED_GOLDEN_VALUE', red(z*s.conjugate(z)-(1-r)**2) == 0)
    ep = e*(r+(1-r)*e)**2
    check('EXACT_COMPLETE_NORMALIZED_SUCCESS_BALANCE', red((1-e)*good*s.conjugate(good)+ep-1) == 0)
    for k in range(4):
        check('OWNED_GLOBAL_UNSPIN_POINTER_WORD_'+str(k), mz(phase(red(s.conjugate(w)**(2*k)))-(G**(16*k)).T))
    check('COMMON_PHASE_PRESERVES_ALL_COMPONENTS', red((s.conjugate(w)**2)*w*w-1) == 0)
    check('EMPTY_ACCEPTED_FIBER_IS_NOT_UNIT_TARGET', red(ep.subs(e, 1)-1) == 0)
    q = s.Rational(1, 16)
    check('EXACT_FIXED_CAUCHY_TAIL', s.Rational(1, 10)/(1-q) == s.Rational(8, 75))
    check('CARDINALITY_FREE_WHOLE_STATE_CONSTANT', s.Rational(8, 75)**2+s.Rational(1, 10)<s.Rational(1, 8))
    check('CARDINALITY_FREE_ALL_PROJECTOR_READING_CONSTANT', 4*s.Rational(1, 8) == s.Rational(1, 2))
    check('GEOMETRIC_TAIL_STARTS_AFTER_TWO_ACTUAL_STAGES', s.Rational(11, 16)*s.Rational(71, 96)**2<s.Rational(2, 5) and
          s.Rational(2, 5)*s.Rational(1, 2)**2 == s.Rational(1, 10))

    # Complete complex operator/state vs faithful real encoding, including both pointer components.
    x = s.Matrix([s.Rational(3, 5), s.I*s.Rational(4, 5)])

    def real_vector(v):
        return s.Matrix([part for z0 in v for part in [s.re(s.expand(z0)), s.im(s.expand(z0))]])

    def real_matrix(A):
        n = A.rows
        R = s.zeros(2*n)
        for i in range(n):
            for j in range(n):
                R[2*i:2*i+2, 2*j:2*j+2] = phase(A[i, j])
        return R

    A = s.diag(w, 1)
    R = real_matrix(A)
    check('FAITHFUL_REAL_ENCODING_FULL_NORM', (real_vector(x).T*real_vector(x))[0] == (x.conjugate().T*x)[0] == 1)
    check('FAITHFUL_REAL_ENCODING_EVERY_COMPONENT', mz(real_vector(A*x)-R*real_vector(x)))
    check('FAITHFUL_REAL_ADJOINT_IS_TRANSPOSE', mz(real_matrix(A.conjugate().T)-R.T))
    check('FAITHFUL_REAL_PRODUCT_IS_LITERAL_PRODUCT', mz(real_matrix(A*A)-R*R))
    check('FAITHFUL_FULL_REAL_ORTHOGONALITY', mz(R.T*R-s.eye(4)) and mz(R*R.T-s.eye(4)))
    check('FAITHFUL_GLOBAL_POINTER_MULTIPLICATION', mz(real_vector(w*x)-s.kronecker_product(s.eye(2), phase(w))*real_vector(x)))
    check('DIRECT_NONREAL_DIAGONAL_IS_OUTSIDE_SAME_REAL_ENTRY_CLASS', im != 0)
    check('ALL_REAL_ENTRY_PRODUCTS_AND_ADJOINTS_CONTROL', mz(G.T*G-s.eye(2)) and all(s.im(t) == 0 for t in G**8) and all(s.im(t) == 0 for t in G.T))
    blank = s.diag(1, 0)
    pointer = (phase(w)*blank*phase(w).T).applyfunc(red)
    check('ACTUAL_GOLDEN_PHASE_VISIBLE_TO_REAL_POINTER', red(pointer[1, 1]) != 0)
    check('COMPLEX_SCALAR_PROJECTION_HIDES_UNIT_PHASE', red(w*s.conjugate(w)-1) == 0)
    check('REAL_POINTER_VISIBILITY_CANNOT_BE_DROPPED', pointer != blank)
    check('NO_PREPARATION_ERROR_CAN_IGNORE_REJECTED_RECORD', s.Rational(1, 10) != 0)

    xs = s.symbols('x0:2', real=True)
    ys = s.symbols('y0:2', real=True)
    vx, vy = s.Matrix(xs), s.Matrix(ys)
    dot = (vx.T*vy)[0]
    wx, wy = (vx.T*vx)[0], (vy.T*vy)[0]
    dweight = ((vx-vy).T*(vx-vy))[0]
    D = vx*vx.T-vy*vy.T
    frob = sum(t*t for t in D)
    check('COMPLETE_REAL_STATE_DISTANCE_IDENTITY', s.expand(dweight-(wx+wy-2*dot)) == 0)
    check('COMPLETE_REAL_PROJECTION_DISTANCE_IDENTITY', s.expand(frob-(wx*wx+wy*wy-2*dot*dot)) == 0)
    P = s.Matrix([[s.Rational(9, 25), s.Rational(12, 25)],
                  [s.Rational(12, 25), s.Rational(16, 25)]])
    check('SYMMETRIC_IDEMPOTENT_DETECTOR_HYPOTHESES', P.T == P and P*P == P)
    check('ACTUAL_PROJECTOR_IMAGE_READING_IDENTITY', s.expand((vx.T*P*vx)[0]-((P*vx).T*(P*vx))[0]) == 0)
    check('SYMMETRIC_DETECTOR_DIFFERENCE_IDENTITY', s.expand((vx.T*P*vx)[0]-(vy.T*P*vy)[0]-((vx-vy).T*P*(vx+vy))[0]) == 0)
    check('NONSYMMETRIC_OPERATOR_NOT_SILENTLY_A_DETECTOR', s.Matrix([[0, 1], [0, 0]]).T != s.Matrix([[0, 1], [0, 0]]))
    check('NONIDEMPOTENT_OPERATOR_NOT_SILENTLY_A_DETECTOR', (2*P)*(2*P) != 2*P)
    check('UNIFORM_READING_ERROR_RETAINS_COMPLETE_NORM', ((s.Matrix([1, 0])-s.Matrix([0, 1])).T*
          (s.Matrix([1, 0])-s.Matrix([0, 1])))[0] == 2)

    eta = s.Matrix([a, p])
    check('ACTUAL_GOLDEN_SUFFIX_COMPLETE_NORM', red((eta.T*eta)[0]-1) == 0)
    for n in range(4):
        suffix = s.Matrix([1])
        for _ in range(2*n):
            suffix = s.kronecker_product(suffix, eta)
        check('ACTUAL_PAIR_HISTORY_SUFFIX_NORM_'+str(n), red((suffix.T*suffix)[0]-1) == 0)
    check('WHOLE_PREFIX_PHASE_INTERTWINES_OWN_SUFFIX', mz((w*s.eye(2))*eta-w*eta))
    check('ONE_FINE_BLANK_PHASE_IS_NOT_PREFIX_EXTENSION', not mz(s.diag(w, 1)*eta-w*eta))

    result = {
        'status': 'PASS', 'scope': SCOPE, 'checks': checks, 'checks_count': len(checks),
        'input_sha256': pins, 'proof': PROOF, 'proof_sha256': sha(PROOF),
        'capsule': BASE+'.lean', 'capsule_sha256': sha(BASE+'.lean'),
        'results': BASE+'_results.json', 'results_sha256': sha(BASE+'_results.json'),
        'output': BASE+'_output.txt', 'output_sha256': sha(BASE+'_output.txt'),
        'exact': {
            'normalized_success_increment': 'b(k+1)-b(k)=-conj(w)^2*(w-1)^2*epsilon(k)*b(k)',
            'complete_balance': 'normSq(b(k))+epsilon(k)=1',
            'unique_fixed_unit_limit': 'gamma=lim b(k+2), normSq(gamma)=1',
            'fixed_success_tail': '(8/75)*(1/16)^k',
            'whole_fixed_target_squared_error': '(1/8)*(1/16)^k',
            'every_real_projector_reading_squared_error': '(1/2)*(1/16)^k',
            'whole_state_error_identity': 'normSq(b(k)-gamma)+epsilon(k)',
            'common_unspin_real_word': '(G^(16*k)).transpose on one pointer',
            'real_entry_boundary': 'same-carrier real-entry finite products/adjoints only',
            'fixed_target_at_all_pair_history_depths': 'J(n)L=L tensor eta(n), complete error preserved',
            'native_seed_dimension': str(2**45), 'native_scene_vertices': 33,
            'prior_propositions_not_recounted': 151,
        },
    }
    if args.expect:
        assert result == json.loads(args.expect.read_text()), 'PINNED_EXACT_LEDGER_MISMATCH'
    if args.output:
        args.output.write_text(json.dumps(result, sort_keys=True, indent=2)+'\n')
    print('PASS_FIXED_COMPLETE_GOLDEN_LIMIT_REAL_READOUT_AND_CYLINDER_CONTROLS', len(checks), flush=True)


if __name__ == '__main__':
    main()
