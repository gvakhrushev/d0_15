#!/usr/bin/env python3
"""Exact readout classification controls; universal proofs are in the Lean capsule."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

HEAD = 'ad2e43f4eae418d6fe7386d37c7ee4c76400ed42'
BASE = '02_REGISTRY/research/certificates/a4d_native_time_field_intertwiner'
PROOF = '02_REGISTRY/research/A4D_NATIVE_TIME_FIELD_INTERTWINER.md'
PARENT = '02_REGISTRY/research/APARENT_FINITE_GRAVITY_COMMON_ACTION_SELECTOR.md'
SCOPE = {
    'linear_class': 'ALL_REAL_LINEAR_READOUTS_B_TO_M_A_WITH_ARBITRARY_LINEAR_A',
    'complete_linear_class_Lean_formalized': True,
    'actual_integer_and_rational_native_bindings_Lean_formalized': True,
    'nonlinear_first_jet_Lean_formalized': True,
    'nonlinear_class': 'DIFFERENTIABLE_AT_NATIVE_ZERO_WITH_EXACT_FIXED_READOUT_INTERTWINING',
    'quantitative_identity_Lean_formalized': True,
    'norm_and_uniform_limit_corollaries_Lean_formalized': False,
    'norm_corollary': 'EXPLICIT_SPATIAL_GAP_RIGHT_INVERSE_AND_OPERATOR_NORM_BOUNDS',
    'smooth_elliptic_countercontrol': 'ANALYTIC_NONCONSTANT_FACTOR_WITH_ZERO_FIRST_JET',
    'A_is_assumed_self_adjoint_in_linear_class': False,
    'all_nonlinear_preparations_excluded': False,
    'zero_first_jet_forces_constant_nonlinear_readout': False,
    'native_integer_states_have_derived_continuous_variations': False,
    'native_coupled_action_or_spatial_preparation_selected': False,
    'copies_or_independent_memory_dynamics_derived': False,
    'kernel_directions_are_gauge': False,
    'uniform_inverse_bounds_derived_from_native_preparation': False,
    'small_value_residual_implies_small_derivative': False,
    'time_intertwining_bound_is_metric_action_contrast_bound': False,
    'physical_time_or_spatial_refinement_derived': False,
    'whole_core_admission_exhausted': False,
    'G0_closed': False,
    'source_or_Ward_derived': False,
    'soundness_or_recovery_proved': False,
    'positive_GR': False,
    'global_closure': False,
    'original_parent_terminals_changed': False,
}


def zero(M):
    return all(s.expand(x) == 0 for x in M)


def parent(A):
    I = s.eye(A.rows)
    return (I.row_join(-I)).col_join((A-I).row_join(2*I-A))


def infnorm(M):
    return max(sum(abs(x) for x in M.row(i)) for i in range(M.rows))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    if args.expect:
        assert json.loads(args.expect.read_text())['scope'] == SCOPE, 'PINNED_LEDGER_MISMATCH'
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    check('COMPILER_REALLY_SUCCEEDED', receipt['compiler_exit_code'] == 0 and receipt['status'] == 'PASS')
    check('CAPSULE_AND_TRANSCRIPT_FRESH', sha(BASE+'.lean') == receipt['capsule_sha256']
          and sha(BASE+'_output.txt') == receipt['output_sha256'])
    output = (root/(BASE+'_output.txt')).read_text()
    check('NO_PROOF_PLACEHOLDER_OR_COMPILER_ERROR', 'sorryAx' not in output and 'error:' not in output)
    check('EXACT_PRINTED_PROPOSITIONS_AND_STANDARD_AXIOMS', receipt['printed_axiom_dependencies'] == 20
          and receipt['printed_propositions'] == 20
          and receipt['axioms'] == ['Classical.choice', 'Quot.sound', 'propext'])
    pins = dict(receipt['transitive_d0_source_sha256'])
    pins.update(receipt['toolchain_input_sha256'])
    pins[PARENT] = sha(PARENT)
    for path, digest in pins.items():
        check('SOURCE_PIN_'+path, sha(path) == digest)
    check('PRINTED_COMPLETE_CLASS_AND_GENUINE_CALCULUS',
          all(x in output for x in ['complete_linear_readout', 'nonlinear_readout_derivative_range',
              'HasFDerivAt', 'quantitative_defect_identity', 'owned_integer_update']))

    T = s.Matrix([[0, 1], [1, -1]])
    B = T**2
    check('LITERAL_NATIVE_TWO_TICK', B == s.Matrix([[1, -1], [-1, 2]]))
    check('NATIVE_QUADRATIC_AND_INVERSE', B**2-3*B+s.eye(2) == s.zeros(2)
          and B.inv() == s.Matrix([[2, 1], [1, 1]]))

    symbols = s.symbols('a:4')
    A = s.Matrix(2, 2, symbols)
    M = parent(A)
    DA = s.diag(A, A)
    MI = ((2*s.eye(2)-A).row_join(s.eye(2))).col_join((s.eye(2)-A).row_join(s.eye(2)))
    check('FULL_NONSYMMETRIC_SYMBOLIC_PARENT_INVERSE', zero(M*MI-s.eye(4)) and zero(MI*M-s.eye(4)))
    check('FULL_SYMBOLIC_PARENT_CHARACTERISTIC_DEFECT', zero(M*M-3*M+s.eye(4)+DA*M))
    P = s.Matrix(4, 4, s.symbols('p:16'))
    BB = parent(s.zeros(2))
    defect = M*P-P*BB
    check('ALL_ENTRIES_SYMBOLIC_QUANTITATIVE_IDENTITY', zero(DA*P+defect-MI*defect*BB.inv()))
    check('WRONG_CHARACTERISTIC_COEFFICIENT_DETECTED', not zero(M*M-4*M+s.eye(4)+DA*M))
    check('WRONG_DEFECT_SIGN_DETECTED', not zero(DA*P-defect+MI*defect*BB.inv()))

    cases = [s.zeros(1), s.Matrix([[1]]), s.Matrix([[2]]),
             s.zeros(2), s.diag(0, 2), s.Matrix([[0, 1], [0, 0]]),
             s.Matrix([[1, 2], [0, 3]]), s.diag(0, 0, 2),
             s.Matrix([[0, 1, 0], [0, 0, 1], [0, 0, 0]])]
    classes = []
    for idx, A in enumerate(cases):
        n = A.rows
        M = parent(A)
        K = A.nullspace()
        for m in [1, 2]:
            BB = parent(s.zeros(m))
            sylvester = s.kronecker_product(s.eye(2*m), M)-s.kronecker_product(BB.T, s.eye(2*n))
            null = sylvester.nullspace()
            expected = 2*m*len(K)
            check(f'FULL_SYLVESTER_NULLITY_{idx}_{m}', len(null) == expected)
            basis = []
            for v, col, block in itertools.product(K, range(m), range(2)):
                U, V = s.zeros(n, m), s.zeros(n, m)
                (U if block == 0 else V)[:, col] = v
                Q = U.row_join(V).col_join(V.row_join(U-V))
                basis.append(Q.vec())
                check(f'ADMITTED_BASIS_{idx}_{m}_{len(basis)}', zero(M*Q-Q*BB))
            if basis:
                span = s.Matrix.hstack(*basis)
                check(f'COMPLETE_SPAN_NOT_ONLY_KERNEL_COUNT_{idx}_{m}', span.rank() == expected
                      and s.Matrix.hstack(span, *null).rank() == expected)
            else:
                check(f'INJECTIVE_A_FULL_READOUT_SPACE_ZERO_{idx}_{m}', sylvester.rank() == 4*n*m)
            for j, v in enumerate(null):
                Q = s.Matrix(2*m, 2*n, list(v)).T
                check(f'ALL_KERNEL_VECTORS_REACH_ONLY_SPATIAL_KERNEL_{idx}_{m}_{j}',
                      zero(s.diag(A, A)*Q))
            classes.append({'case': idx, 'native_copies': m, 'target_dimension': n,
                            'A_rank': A.rank(), 'readout_dimension': expected})

    A2 = s.Matrix([[2]])
    M2 = parent(A2)
    check('EXACT_STABLE_COUPLED_TARGET_NONTRIVIAL', M2.trace() == 1 and M2**6 == s.eye(2)
          and M2**3 == -s.eye(2))
    check('EXACT_MAX_NORM_BOUND', infnorm(B.inv()) == 3 and infnorm(M2.inv()) == 2)
    for entries in [(1, 0, 0, 1), (2, 1, -1, 3), (1, 2, 3, 5)]:
        Q = s.Matrix(2, 2, entries)
        E = M2*Q-Q*B
        check('RATIONAL_RIGHT_INVERSE_LOWER_BOUND_'+str(entries),
              infnorm(E)*7*infnorm(Q.inv()) >= 2)
    h = s.symbols('h', positive=True)
    Mh = parent(s.Matrix([[h]]))
    check('VANISHING_SPATIAL_GAP_EXCEPTION', Mh-B == s.Matrix([[0, 0], [h, -h]]))
    check('MISSING_INTERTWINING_IS_SUBSTANTIVE', M2 != B)

    q, p = s.symbols('q p', real=True)
    invariant = q*q-q*p-p*p
    transformed = invariant.subs({q: q-p, p: -q+2*p}, simultaneous=True)
    check('NONLINEAR_INVARIANT_EXACT', s.expand(transformed-invariant) == 0)
    check('NONLINEAR_NONCONSTANT_ZERO_FIRST_JET', invariant.subs({q: 1, p: 0}) == 1
          and s.Matrix([invariant, 0]).jacobian([q, p]).subs({q: 0, p: 0}) == s.zeros(2))
    M1 = parent(s.Matrix([[1]]))
    check('INJECTIVE_A_NONLINEAR_CONTROL', M1*s.Matrix([invariant, 0]) == s.Matrix([invariant, 0]))
    t = s.symbols('t', real=True)
    w = s.Matrix([s.cos(s.pi*t/3)+s.sin(s.pi*t/3)/s.sqrt(3), 2*s.sin(s.pi*t/3)/s.sqrt(3)])
    check('SMOOTH_ELLIPTIC_FACTOR_ANGULAR_IDENTITY', all(s.trigsimp(x) == 0 for x in w.subs(t, t+1)-M2*w))
    check('SMALL_VALUE_ERROR_NEED_NOT_HAVE_SMALL_DERIVATIVE', s.diff(h*s.sin(q/h), q).subs(q, 0) == 1)

    payload = {
        'status': 'PASS', 'owner_input_head': HEAD, 'scope': SCOPE, 'checks': checks,
        'input_sha256': pins, 'proof_sha256': sha(PROOF), 'checker_sha256': sha(BASE+'_check.py'),
        'receipt_sha256': sha(BASE+'_results.json'),
        'transitive_d0_source_count': len(receipt['transitive_d0_source_sha256']),
        'exact_results': {
            'linear_family': 'P=[[U,V],[V,U-V]], AU=AV=0',
            'complete_dimension': '2*m*dim(ker A)',
            'finite_full_sylvester_classes': classes,
            'quantitative_identity': 'D_A P=-E+M_A^-1 E B^-1',
            'A2_max_norm_constants': {'B_inverse': 3, 'M_inverse': 2, 'gap': 2, 'denominator': 7},
            'standard_logical_axioms_only': True,
            'G0_closed': False,
        },
    }
    if args.output:
        args.output.write_text(json.dumps(payload, sort_keys=True, indent=2)+'\n')
    else:
        expected = args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_TIME_FIELD_INTERTWINER', len(checks), 'controls',
          len(receipt['transitive_d0_source_sha256']), 'D0 pins')


if __name__ == '__main__':
    main()
