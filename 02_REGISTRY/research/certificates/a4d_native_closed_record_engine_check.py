#!/usr/bin/env python3
"""Exact controls for the native retained-record engine and hereditary adapter.

Universal orbit/growth proofs are in the memo and the generic Lean capsule.
The finite run is a regression, not a physical-universe closure certificate.
"""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_closed_record_engine'
PROOF = '02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md'
HEAD = '585a6c21e09c07d7704c6c7ef1e2e0b45ba9b83a'
OLD = '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py'
INPUTS = [
    OLD,
    '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_certificate.json',
    '02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md',
    '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md',
    '02_REGISTRY/research/A4D_NATIVE_CONDENSED_PRICE_NATURALITY.md',
    '03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean',
    '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
]
SCOPE = {
    'state': 'ALL_16_REAL_EXTERIOR_COMPONENTS_EXACT_INTEGER_GOLDEN_COEFFICIENTS',
    'transition': 'ACTUAL_CURRENT_FIRST_GRADE_CONDITIONS_LITERAL_FULL_RECORD',
    'all_time_nonempty_sector': 'COLLINEAR_TWO_BAND_DOMAIN_PLUS_ACTUAL_BLANK_SEED',
    'fixed_seed_uniform_first_grade_bound': 'abs(m_1)>1/5',
    'native_physical_admission_or_all_state_closure': False,
    'endpoint_binding': 'PREVIOUS_CONDITIONAL_POSITIVE_PAIRING_SAME_Q',
    'external_tick_history_randomness_or_reset_in_step': False,
    'full_seed_orbit_distinct': 'ANALYTIC_CONJUGATE_GROWTH_PROOF',
    'past_recoverable': 'ALGEBRAIC_SEED_ORBIT_DECODER_NOT_PHYSICAL_INVERSE_ADMISSION',
    'exact_real_storage_free': False,
    'canonical_coefficient_height_bound': 'H_k>4^k/3_ON_COMPLETE_RETURNS',
    'bound_for_every_possible_compressed_codec': False,
    'heredity': 'ACTUAL_ARCHIVE_PROJECTION_PULLBACK_COMMUTES_WITH_LOCAL_TRANSITION',
    'heredity_pairing': 'ISOMETRY_CONDITIONAL_ON_EXPLICIT_FIBRE_NORMALIZATION',
    'native_refinement_trigger_link_interaction_capacity_or_physical_measure_derived': False,
    'seed_adjacent_feedback_pencil': '(1-4*z*p^3)^4_AT_BOTH_OBSERVER_SIGNS',
    'feedback_reads_all_retained_history': False,
    'all_ten_metric_derivatives_proved_zero': False,
    'intrinsic_source_Ward_curved_roots_soundness_recovery_GR': False,
    'new_supported_CORE_owner_or_parent_terminal': False,
}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


engine = load('d0_closed_record_executor', BASE + '.py')
old = load('d0_chronology_owner', OLD)
s, a, p = old.s, old.a, old.p


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def sym(value):
    u, v, w, t = value.coefficients
    return u + v*a + w*p + t*a*p


def vector(state):
    return s.Matrix([sym(x) for x in state.matter])


def controls():
    checks, mutants = [], []

    def check(name, truth):
        assert bool(truth), name
        checks.append(name)

    def reject(name, truth_of_false_claim):
        check('REJECT_' + name, not truth_of_false_claim)
        mutants.append(name)

    def rejected_call(name, exception, call):
        try:
            call()
        except exception:
            check('REJECT_' + name, True)
            mutants.append(name)
        else:
            raise AssertionError(name)

    E = engine
    check('integer_golden_relations', E.A*E.A == E.P and E.P+E.P*E.P == E.ONE)
    # Algebra/sign controls include both quadratic parts, cancellation and all
    # signs. Exact SymPy algebraic comparisons provide an independent oracle.
    alpha = s.sqrt((s.sqrt(5)-1)/2)
    for coefficients in [(1,0,0,0), (0,1,0,0), (0,0,1,0), (0,0,0,1),
                         (-1,1,0,0), (1,-1,0,0), (-1,0,2,0), (1,0,-2,0),
                         (5,-7,4,3), (-5,7,-4,-3), (0,0,0,0)]:
        value = E.Golden(coefficients)
        actual = sum(c*alpha**j for j,c in enumerate(coefficients))
        check('exact_quartic_sign_oracle', value.sign() == s.sign(actual).simplify())
    basis = [E.Golden(tuple(int(i == j) for i in range(4))) for j in range(4)]
    for x in basis:
        for y in basis:
            check('exact_integer_ring_product', old.zero(sym(x*y)-sym(x)*sym(y)))

    Uplus, cut = old.record(s.eye(4), s.Matrix([1,0,0,0]))
    Uminus, cutminus = old.record(s.eye(4), s.Matrix([-1,0,0,0]))
    check('original_price_cut_is_retained', cut == cutminus)
    for sign, U in [(1,Uplus), (-1,Uminus)]:
        for column in range(16):
            values = [E.ZERO]*16
            values[column] = E.ONE
            state = E.State(tuple(values))
            check('all16_columns_are_literal_native_CAR',
                  old.zero(vector(E.literal_axis_gate(state,sign))-U[:,column]))
            check('full_gate_transpose_inverse',
                  E.inverse_axis_gate(E.literal_axis_gate(state,sign),sign) == state)
        check('full_gate_orthogonality', old.zero(U.T*U-s.eye(16)))

    R = old.mat(Uminus*Uplus).extract([14,15],[14,15])
    r, t = 2*p-1, 2*a*p
    check('higher_grade_actual_return', old.zero(R-s.Matrix([[r,-t],[t,r]])))
    check('return_norm_identity', old.zero(r*r+t*t-1))
    q = s.Symbol('q')
    check('conjugate_root_satisfies_same_equation', old.zero((-1-p)**2+(-1-p)-1))
    check('quadratic_root_norm_negative', old.zero(p*(-1-p)+1))
    check('conjugate_return_trace', old.zero(r.subs(p,-1-p)+3+2*p))
    check('seed_is_actual_whole_blank',
          E.seed().matter[1] == E.seed().matter[15] == E.ONE and E.seed().matter[0] == E.seed().matter[14])

    initial, state = E.seed(), E.seed()
    snapshots, seen, short, storage_rows = {}, set(), [], []
    target_ticks = {0,1,2,3,4,16,64,256,1024,4096}
    for tick in range(4097):
        code = E.encode(state)
        check('full_state_exact_codec_roundtrip', E.decode(code) == state)
        digest = hashlib.sha256(code.encode()).hexdigest()
        check('full_state_not_a_visible_only_repeat', digest not in seen)
        seen.add(digest)
        check('full_state_norm_squared_two', E.norm_squared(state) == E.Golden.integer(2))
        check('uniform_first_grade_bound', (5*state.matter[1]*state.matter[1]*5-E.ONE).sign() > 0)
        if tick < 16:
            short.append(state)
        if tick in target_ticks:
            snapshots[tick] = state
            storage_rows.append(E.diagnostic(state,tick))
        if tick >= 4 and tick % 2 == 0:
            k = (tick-2)//2
            u,v,w,tcoef = state.matter[15].coefficients
            check('top_return_is_in_quadratic_subfield', v == tcoef == 0)
            H = max(abs(u),abs(w))
            check('canonical_height_explicit_growth_bound', 3*H > 4**k)
        if tick == 4096:
            break
        out = E.step(state)
        check('index_free_full_predecessor', E.predecessor_on_seed_orbit(out) == state)
        state = out

    Astate, Bstate = snapshots[2], snapshots[3]
    check('lower_band_A', old.zero(vector(Astate)[:2,0]-s.Matrix([-2*a*p,2*p-1])))
    check('lower_band_B', old.zero(vector(Bstate)[:2,0]-s.Matrix([5*p-4,a*(4*p-3)])))
    check('actual_visible_two_cycle', snapshots[2].matter[:2] == snapshots[4].matter[:2])
    reject('VISIBLE_RETURN_IS_FULL_RETURN', snapshots[2] == snapshots[4])
    reject('FIXED_OBSERVER_CAN_REPLACE_CURRENT_STATE', E.literal_axis_gate(Bstate,1) == E.step(Bstate))
    reject('INVERSE_USES_OUTPUT_SIGN', E.inverse_axis_gate(Bstate,-1) == Astate)
    reset = list(snapshots[4].matter)
    reset[14], reset[15] = E.ZERO, E.ONE
    reject('NEW_BLANK_IS_RETAINED_MEMORY', E.State(tuple(reset)) == snapshots[4])
    erased = list(snapshots[4].matter)
    erased[14] = E.ZERO
    reject('DROP_SPATIAL_TOP_WITHOUT_INFORMATION_LOSS', E.norm_squared(E.State(tuple(erased))) == E.Golden.integer(2))
    singular = [E.ZERO]*16
    singular[0] = singular[14] = -E.A-E.A*E.P
    singular[1] = singular[15] = E.ONE
    singular = E.State(tuple(singular))
    check('old_genuine_blank_singularity_retained', not E.literal_axis_gate(singular,1).matter[1])
    rejected_call('ALL_BLANKS_ARE_CLOSED', ValueError, lambda:E.step(singular))
    rejected_call('TRUNCATED_STATE_RETENTION', ValueError, lambda:E.decode(E.encode(initial)[:-1]))
    rejected_call('UNDECLARED_TRAILING_HISTORY', ValueError, lambda:E.decode(E.encode(initial)+'1'))

    bounded, overflow_at = initial, None
    for tick in range(256):
        try:
            bounded = E.bounded_step(bounded,256)
        except OverflowError:
            overflow_at = tick+1
            break
    check('bounded_internal_store_stops', overflow_at is not None and overflow_at > 0)
    reject('UNBOUNDED_RECORD_FITS_256_BITS', len(E.encode(snapshots[4096])) <= 256)
    rejected_call('OVERSIZED_INPUT_IS_FREE', OverflowError, lambda:E.bounded_step(snapshots[4096],256))

    # Genuine nonconstant fields, with both observer signs and varying norms.
    inheritance_rows = []
    for stage in range(3):
        field = tuple(E.State(tuple((i%3+1)*v for v in short[i%len(short)].matter))
                      for i in range(E.archive_modes(stage)))
        inherited = E.inherit(stage,field)
        left = tuple(E.step(v) for v in inherited)
        right = E.inherit(stage,tuple(E.step(v) for v in field))
        check('actual_archive_pullback_intertwines_local_engine', left == right)
        counts = Counter(E.archive_projection(stage,y) for y in range(E.archive_modes(stage+1)))
        check('actual_archive_projection_surjective', set(counts) == set(range(len(field))))
        check('recover_each_whole_parent_state', tuple(inherited[x] for x in range(len(field))) == field)
        parent_norm = sum(Fraction(E.norm_squared(v).coefficients[0],len(field)) for v in field)
        child_norm = sum(Fraction(E.norm_squared(v).coefficients[0],len(field)*counts[E.archive_projection(stage,y)])
                         for y,v in enumerate(inherited))
        check('conditional_hereditary_weight_isometry', parent_norm == child_norm)
        check('conditional_hereditary_weights_sum_to_one',
              sum(Fraction(1,len(field)*counts[E.archive_projection(stage,y)]) for y in range(len(inherited))) == 1)
        reject('UNWEIGHTED_COUNTING_CLONE_IS_ISOMETRY_STAGE_%d'%stage,
               sum(E.norm_squared(v).coefficients[0] for v in field) ==
               sum(E.norm_squared(v).coefficients[0] for v in inherited))
        inheritance_rows.append({'stage':stage,'parent_points':len(field),'child_points':len(inherited),
                                 'fibre_cardinalities':sorted(set(counts.values()))})
    reject('DISTANT_MODULO_IS_COMPOSED_PROJECTION', E.archive_projection(0,E.archive_projection(1,81)) == 81%E.archive_modes(0))
    homogeneous = (initial,)*E.archive_modes(0)
    check('hereditary_homogeneous_field_stays_homogeneous',
          len(set(E.step(v) for v in E.inherit(0,homogeneous))) == 1)

    z = old.z
    for c in [s.Integer(-1),s.Integer(1)]:
        lam,tr,det,tr0,det0 = old.polynomials(c)
        pencil = (1-z*lam)**2*(1-z*tr+z*z*det)**2*(1-z*tr0+z*z*det0)
        check('literal_full_price_constant_on_both_actual_angles', old.zero(pencil-(1-4*z*p**3)**4))
    reject('TWO_TICK_PRICE_DISTINGUISHES_ALL_STATES', snapshots[2] == snapshots[4])

    predecessor = json.loads((ROOT/INPUTS[1]).read_text())
    check('consumed_chronology_checker_hash', predecessor['checker_sha256'] == sha(OLD))
    check('consumed_chronology_proof_hash', predecessor['proof_sha256'] == sha(INPUTS[2]))
    for path,digest in predecessor['input_sha256'].items():
        check('consumed_chronology_transitive_input', sha(path) == digest)
    receipt = json.loads((ROOT/(BASE+'_results.json')).read_text())
    check('genuine_new_Lean_receipt', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0)
    check('genuine_new_Lean_capsule_hash', receipt['capsule_sha256'] == sha(BASE+'.lean'))
    check('genuine_new_Lean_output_hash', receipt['output_sha256'] == sha(BASE+'_output.txt'))
    for path,digest in receipt['input_sha256'].items():
        check('genuine_Lean_transitive_input', sha(path) == digest)
    check('nine_generic_Lean_propositions', len([d for d in receipt['declarations'] if '.ClosedRecordEngine.' in d]) == 9)
    check('no_custom_Lean_axioms', all(set(v) <= {'propext','Classical.choice','Quot.sound'} for v in receipt['axioms'].values()))

    return {
        'status':'PASS','input_source_head':HEAD,'proof':PROOF,'scope':SCOPE,
        'checks':dict(sorted(Counter(checks).items())), 'exact_controls':len(checks),
        'executed_mathematical_mutants':mutants, 'exact_transitions_exercised':4096,
        'new_Lean_declarations':9, 'finite_run':storage_rows,
        'first_256_bit_store_overflow_before_tick':overflow_at,
        'hereditary_projection_controls':inheritance_rows,
        'input_sha256':{path:sha(path) for path in INPUTS},
        'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
        'engine_sha256':sha(BASE+'.py'), 'Lean_receipt_sha256':sha(BASE+'_results.json'),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args = parser.parse_args()
    result = controls()
    path = ROOT/(BASE+'_certificate.json')
    if args.write:
        path.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        assert json.loads(path.read_text()) == result, 'CLOSED_RECORD_ENGINE_IMMUTABLE_LEDGER_MISMATCH'
    print('PASS_CLOSED_RECORD_ENGINE controls=%d mutations=%d ticks=4096 Lean=9 '
          'native_refinement_trigger=OPEN' % (result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__ == '__main__':
    main()
