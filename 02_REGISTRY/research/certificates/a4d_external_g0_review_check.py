#!/usr/bin/env python3
"""Exact independent review; the submitted 50 PASS are not theorem acceptance."""
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

HEAD = 'a2a2ccae43ec4812ade33db7b0610245e173f4b9'
PREFIX = '02_REGISTRY/research/certificates/a4d_external_g0_review'
PROOF = '02_REGISTRY/research/A4D_EXTERNAL_G0_RESULT_REVIEW_2026-10-07.md'
RAW = '02_REGISTRY/research/inputs/2026-10-07_external_g0/'
RECEIVED = {
    '00_RESULT.md': '9221d8ece88f5cb42cbd7e052876b0a7674cfe1c9f9cb1649ba75b45e1e73db3',
    '01_MAIN_PROOF.md': '84125a80b57e2b3b91c2f7a7c3f787e70a9fb564a635125c7a9b66e75243edfb',
    '03_EXACT_CERTIFICATE.py': 'f7e6b52fa69f006705282bf0c95afba6f46e3b330cc8cfb07158dc2d0378a073',
    '03_certificate_results.json': '8f1a91c65e655cfdf89d66b2020d3c0219caf8a2ddaed53b436c5c9057eef7d7',
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path)
    ap.add_argument('--expect', type=Path)
    args = ap.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    for name, digest in RECEIVED.items():
        check('ORIGINAL_BYTES_' + name, sha(RAW+name) == digest)
    submitted = json.loads((root/(RAW+'03_certificate_results.json')).read_text())
    check('SUBMITTED_50_REPORTED_PASSES', len(submitted) == 50 and all(x['ok'] for x in submitted))
    replay = json.loads((root/(PREFIX+'_submitted_replay.json')).read_text())
    check('SEPARATE_REPLAY_BOUND_TO_ORIGINAL_INPUTS', replay['script_exit_code'] == 0
          and replay['reported_controls'] == 50 and replay['reported_failures'] == 0
          and replay['json_semantically_identical_to_submission']
          and not replay['universal_theorems_or_physical_status_certified']
          and replay['inputs_sha256'] == {RAW+n: h for n, h in RECEIVED.items()})
    receipt = json.loads((root/(PREFIX+'_results.json')).read_text())
    check('COMPILED_20_ACTUAL_PROPOSITIONS', receipt['status'] == 'PASS'
          and receipt['owner_input_head'] == HEAD and receipt['compiler_exit_code'] == 0
          and receipt['printed_axiom_dependencies'] == 20 and not receipt['sorryAx']
          and set(receipt['axioms']) <= {'propext', 'Classical.choice', 'Quot.sound'})
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_OWNER_CAPSULE_AND_TOOLCHAIN_PINS', all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('CLEAN_COMPILER_OUTPUT', all(x not in out for x in ['sorryAx', 'error:', 'warning:']))
    for name in ['native_constant_cycle_cube_nonzero', 'single_direction_evaluation_surjective',
                 'single_direction_has_nonzero_kernel', 'all_diagonals_determine_symmetric_form',
                 'full_transport_composition', 'transport_background_second_derivative',
                 'transport_parameter_second_derivative',
                 'isotropy_covariance_does_not_force_frame_invariance',
                 'failed_isotropy_covariance_does_not_force_frame_sensitivity']:
        check('BOUND_'+name, "'D0.Research.ExternalG0Review."+name+"' depends on axioms:" in out)

    for n in range(3, 129):
        entry = sum(sp.prod(signs) for signs in itertools.product([-1, 1], repeat=3)
                    if sum(signs) % n == 1) * sp.Rational(n, 2)**3
        formula = -sp.Rational(n**3, 8)*(3+int(n == 4))
        assert entry == formula and entry != 0, n
    check('T4_EIGHT_PATH_FORMULA_3_TO_128', True)
    for n in [3, 4, 5, 6, 9]:
        P = sp.zeros(n)
        for i in range(n):
            P[i, (i+1) % n] = 1
        G = sp.Rational(n, 2)*(P-P.T)
        assert G.T == -G and (G**3)[0, 1] == -sp.Rational(n**3, 8)*(3+int(n == 4))
    check('T4_LITERAL_MATRIX_CONTROLS', True)
    J = sp.zeros(4)
    for i in range(3):
        J[i, i+1] = 1
    E = sp.zeros(4); E[0, 3] = 1
    K = sp.zeros(4); K[1, 3] = 2
    Dg = K-J*J
    check('T5_CORRECT_NONZERO_J_CUBE_AND_JK', J**3 == E and J*K == 2*E and E != sp.zeros(4))
    check('T5_EXACT_CANCELLATION_NOT_ZERO_FACTORS', Dg*J == -E and J*K/2+Dg*J == sp.zeros(4))
    check('T5_ALL_FIVE_COEFFICIENTS', J*J+Dg-K == sp.zeros(4) and Dg*K == sp.zeros(4)
          and K*J == sp.zeros(4) and K*K == sp.zeros(4))

    e, x, y, t = sp.symbols('e x y t', real=True)
    N = sp.Matrix([[0, 1], [0, 0]]); I = sp.eye(2)
    U = lambda b: I+b*b*N/2
    R = lambda b, z: I+(b*z+z*z/2)*N
    check('T9_GLOBALLY_INVERTIBLE_FRAME', sp.det(U(e)) == 1 and sp.simplify(U(e).inv()-(I-e*e*N/2)) == sp.zeros(2))
    check('T9_TRUE_FRAME_BINDING', sp.simplify(U(e+x)*U(e).inv()-R(e, x)) == sp.zeros(2))
    check('T9_EXACT_FULL_GROUP_COMPOSITION', sp.simplify(R(e+x, y)*R(e, x)-R(e, x+y)) == sp.zeros(2))
    check('T9_WRONG_BACKGROUND_DERIVATIVE_IS_ZERO', sp.diff(R(e, 1), e, 2) == sp.zeros(2))
    check('T9_CORRECT_PARAMETER_DERIVATIVE_IS_NONZERO', sp.diff(R(0, t), t, 2).subs(t, 0) == N)
    vx = sp.Matrix([0, 1])
    check('T16_POSITIVE_BRANCH_COUNTER', U(2)*vx == sp.Matrix([2, 1]) and vx[0] == 0)
    constant_readout = lambda v: vx
    rho = lambda s: I+s*N
    check('T16_NEGATIVE_BRANCH_COUNTER', constant_readout(rho(1)*sp.zeros(2, 1)) != rho(1)*constant_readout(sp.zeros(2, 1))
          and constant_readout(U(e)*vx) == constant_readout(vx))
    check('T16_NONTRIVIAL_ISOTROPY_IS_ACTUAL_ADDITIVE_REPRESENTATION',
          sp.expand(rho(x)*rho(y)-rho(x+y)) == sp.zeros(2))

    S = sp.Matrix([[0, 0], [0, 1]]); h = sp.Matrix([1, 0]); k = sp.Matrix([0, 1])
    check('T15_NONZERO_SINGLE_PROBE_KERNEL', S != sp.zeros(2) and (h.T*S*h)[0] == 0 and (k.T*S*k)[0] == 1)
    a, b, c = sp.symbols('a b c')
    S = sp.Matrix([[a, b], [b, c]])
    diag_values = sp.Matrix([(h.T*S*h)[0], (k.T*S*k)[0], ((h+k).T*S*(h+k))[0]])
    check('T15_ALL_DIAGONALS_POLARIZE', diag_values.jacobian([a, b, c]).det() != 0
          and sp.expand((diag_values[2]-diag_values[0]-diag_values[1])/2) == b)

    d = sp.Matrix([[1, 0, 1, 1], [0, 1, 1, -1]])
    basis = [sp.eye(4)[:, i] for i in range(4)]
    T = d.T
    correct = all((z.T*T*d*v)[0] == (v.T*T*d*z)[0] for z in basis for v in basis)
    wrong = all((T[i, :]*d*v)[0] == (T[i, :]*d*z)[0]
                for i in range(4) for z in basis for v in basis)
    check('C10_EXPLICIT_VALID_FORM_REJECTED_BY_SUBMITTED_PREDICATE', correct and not wrong)
    z = sp.symbols('z:8'); TT = sp.Matrix(4, 2, z)
    equations = list(TT*d-(TT*d).T)
    B = sp.linear_eq_to_matrix(equations, z)[0]
    check('C10_COMPLETE_CORRECT_SOLUTION_DIMENSION', B.rank() == 5 and len(B.nullspace()) == 3)
    for Q in [sp.Matrix([[1, 0], [0, 0]]), sp.Matrix([[0, 1], [1, 0]]), sp.Matrix([[0, 0], [0, 1]])]:
        assert (d.T*Q*d).T == d.T*Q*d
    check('C10_POSITIVE_SYMMETRIC_BASIS_TESTED', True)
    source = (root/(RAW+'03_EXACT_CERTIFICATE.py')).read_text()
    calls = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == 'rep']
    placeholder = [n for n in calls if isinstance(n.args[0], ast.Constant)
                   and str(n.args[0].value).startswith('C14c')]
    check('C14C_IS_LITERAL_TRUE_NOT_COMPUTATION', len(placeholder) == 1
          and isinstance(placeholder[0].args[1], ast.Constant) and placeholder[0].args[1].value is True)
    A0 = sp.ones(3)-sp.eye(3); A1 = sp.Matrix([[0, 1, 2], [1, 0, 1], [2, 1, 0]])
    for p in itertools.permutations(range(3)):
        scale = A0[0, 1]/A1[p[0], p[1]]
        assert any(A0[i, j] != scale*A1[p[i], p[j]] for i in range(3) for j in range(3))
    check('C12C_ALL_SCALES_EXCLUDED_EXACTLY', True)

    inputs = [PROOF, PREFIX+'_submitted_replay.json',
              '02_REGISTRY/research/A4D_NATIVE_DYNAMICAL_OWNERSHIP.md',
              '02_REGISTRY/research/A4D_NATIVE_PARENT_SOURCE_BOUNDARY.md']
    inputs += [RAW+n for n in RECEIVED]
    payload = {
        'status': 'PARTIAL_ACCEPTANCE_WITH_CORRECTIONS', 'input_head': HEAD,
        'inputs_sha256': {p: sha(p) for p in inputs},
        'checker_sha256': sha(PREFIX+'_check.py'),
        'lean_receipt_sha256': sha(PREFIX+'_results.json'),
        'compiled_declarations': receipt['printed_axiom_dependencies'],
        'transitive_d0_source_pins': len(receipt['transitive_d0_source_sha256']),
        'checks': checks, 'submitted_reported_passes': 50,
        'disposition': {
            'T4_all_carrier_sizes_native_cube_nonzero': 'PROVED_LEAN',
            'T4_specific_entry_formula': 'ANALYTIC_PROOF_WITH_EXACT_CONTROLS',
            'T9_as_printed': 'REFUTED_WRONG_DERIVATIVE_VARIABLE',
            'T15_single_probe_injective': False,
            'T15_all_diagonal_observations_injective': True,
            'T16_positive_implication': 'REFUTED', 'T16_negative_implication': 'REFUTED',
            'C10_submitted_predicate_correct': False, 'C14c_is_a_check': False,
            'abstract_countermodels_are_native_physical_solutions': False,
            'all_flat_transport_completions_are_physically_admitted': False,
            'G0_closed': False, 'positive_gr': False, 'whole_core_no_go': False,
            'original_parent_terminals_changed': False,
        },
    }
    encoded = json.dumps(payload, sort_keys=True, indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        expected = args.expect or root/(PREFIX+'_certificate.json')
        assert json.loads(expected.read_text()) == json.loads(encoded), 'PINNED_LEDGER_MISMATCH'
    print('PASS_EXTERNAL_G0_REVIEW', len(checks), 'exact controls; submitted 50 PASS kept separate')


if __name__ == '__main__':
    main()
