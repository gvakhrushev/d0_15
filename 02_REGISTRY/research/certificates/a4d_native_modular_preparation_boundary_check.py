#!/usr/bin/env python3
"""Finite controls of a named modular preparation route, not an owned heat law."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

import sympy as s

ROOT = None
BASE = '02_REGISTRY/research/certificates/a4d_native_modular_preparation_boundary'
PROOF = '02_REGISTRY/research/A4D_NATIVE_MODULAR_PREPARATION_BOUNDARY.md'
HEAD = '8207558224ee7c419d58f1f468d01b1187e21951'
SCOPE = {
    'complete_finite_faithful_Gibbs_fiber_analytic': True,
    'positive_ground_zero_representative_unique_analytic': True,
    'normalized_state_alone_fixes_full_heat_price': False,
    'scalar_shift_remains_free_with_protected_positive_zero_mode': False,
    'direct_sum_pure_sector_is_faithful_tensor_marginal': False,
    'every_declared_golden_gate_input_has_faithful_marginal': False,
    'bounded_linear_hyperbolic_step_is_real_modular_flow': False,
    'nonlinear_torus_or_all_modular_D0_descriptions_excluded': False,
    'restricted_positive_modular_square_match_retains_all_modes': True,
    'matrix_Gibbs_reconstruction_is_new_Lean_theorem': False,
    'native_state_Gibbs_identification_or_temperature_selected': False,
    'native_F_source_Ward_stationarity_curved_roots_or_GR_derived': False,
    'T0_T3_or_original_parent_terminal_closed': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def simp(matrix):
    return matrix.applyfunc(s.simplify)


def mathematics():
    checks = {}

    def ck(name, condition):
        assert bool(condition), name
        checks[name] = checks.get(name, 0) + 1

    p = (s.sqrt(5) - 1) / 2
    a = s.sqrt(p)
    phi = 1 + p
    ck('golden_identity_and_brackets', s.simplify(p+p**2-1) == 0 and 0 < p < 1)
    U = s.Matrix([[a,0,-p,0], [0,a,0,-p], [0,p,0,a], [p,0,a,0]])
    ck('whole_owned_recording_gate_orthogonal', simp(U.T*U) == s.eye(4))
    psi = simp(U*s.Matrix([1,0,0,0]))
    ck('literal_blank_output', simp(psi-s.Matrix([a,0,0,p])) == s.zeros(4,1))
    ck('whole_joint_state_retained', s.simplify((psi.T*psi)[0]) == 1)

    def reduced(v):
        return simp(s.Matrix(2,2,lambda i,j: sum(v[2*i+k]*v[2*j+k] for k in range(2))))

    rho_golden = reduced(psi)
    ck('actual_tensor_marginal', simp(rho_golden-s.diag(p,p**2)) == s.zeros(2))
    ck('actual_tensor_marginal_faithful', s.simplify(rho_golden.det()-p**3) == 0 and p**3 > 0)
    ck('actual_tensor_marginal_trace', s.simplify(rho_golden.trace()) == 1)
    bad_input = s.Matrix([a,0,-p,0])
    ck('separating_input_normalized', s.simplify((bad_input.T*bad_input)[0]) == 1)
    pure_output = simp(U*bad_input)
    ck('separating_output_exact', pure_output == s.Matrix([1,0,0,0]))
    ck('faithfulness_not_for_all_inputs', reduced(pure_output) == s.diag(1,0))
    sector = s.Matrix([psi[0],psi[1]])
    sector_rho = simp(sector*sector.T/(sector.T*sector)[0])
    ck('direct_sum_conditioning_rank_one', sector_rho.rank() == 1)
    ck('direct_sum_is_not_tensor_readout', sector_rho != rho_golden)

    units = [s.Matrix(2,2,lambda i,j: int(i == r and j == c)) for r,c in [(0,0),(0,1),(1,0),(1,1)]]
    modular_expected = s.diag(1,phi,p,1)
    columns = [s.Matrix(list(simp(rho_golden*e*rho_golden.inv()))) for e in units]
    modular = s.Matrix.hstack(*columns)
    ck('all_four_modular_modes', simp(modular-modular_expected) == s.zeros(4))
    ck('both_diagonal_modes_retained', modular[0,0] == modular[3,3] == 1)
    T = s.Matrix([[0,1],[1,-1]])
    ck('hyperbolic_T_not_isometric', (T.T*T)[1,1] == 2 and T.T*T != s.eye(2))
    S = s.Matrix([[1,1],[p,-phi]])
    ck('golden_eigenbasis_invertible', s.simplify(S.det()+1+2*p) == 0 and S.det() != 0)
    ck('both_golden_eigenvalues', simp(T*S-S*s.diag(p,-phi)) == s.zeros(2))
    modular_square_restriction = (modular**2).extract([2,1],[2,1])
    ck('positive_square_intertwiner', simp(T**2*S-S*modular_square_restriction) == s.zeros(2))
    ck('restricted_square_is_not_full_operator', s.simplify((modular**2).trace()) == 5 and (T**2).trace() == 3)
    theta = s.symbols('theta', real=True)
    phase = s.cos(theta)+s.I*s.sin(theta)
    phaseU = s.diag(phase,1)
    ck('real_flow_implementer_unitary', s.simplify(s.expand(phase*s.conjugate(phase))) == 1)
    for e in units:
        transformed = phaseU*e*phaseU.conjugate().T
        ck('real_flow_unitary_conjugation_norm_control', s.simplify(s.expand(s.trace(transformed.conjugate().T*transformed))) == 1)

    # Complete fiber is proved analytically. These are full finite controls,
    # including a non-diagonal density and noncommuting state variation.
    c = s.symbols('c', real=True)
    beta = s.symbols('beta', positive=True)
    R = s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
    rho = R*s.diag(s.Rational(1,3),s.Rational(2,3))*R.T
    ck('full_factor_trace_one', rho.trace() == 1 and rho.det() == s.Rational(2,9))
    boltzmann = s.exp(-beta*c)*rho
    partition = s.simplify(boltzmann.trace())
    ck('normalizer_preserved_before_division', partition == s.exp(-beta*c))
    ck('normalized_density_scalar_invisible', simp(boltzmann/partition-rho) == s.zeros(2))
    thermal_price = s.simplify(s.log(partition)/beta)
    ck('full_price_sees_scalar', s.simplify(thermal_price+c) == 0)
    ck('full_price_scalar_covector', s.diff(thermal_price,c) == -1)
    ground_boltzmann = R*s.diag(s.Rational(1,2),1)*R.T
    ck('ground_zero_reconstruction_normalized', ground_boltzmann/ground_boltzmann.trace() == rho)
    ck('ground_zero_fixes_normalizer', ground_boltzmann.trace() == s.Rational(3,2))
    ck('shift_breaks_protected_zero_mode', (s.Rational(1,2)*ground_boltzmann-s.eye(2)).det() != 0)
    H0 = s.diag(s.log(2),0)
    ck('particular_zero_vector_is_additional_data', H0*s.Matrix([1,0]) != s.zeros(2,1) and H0*s.Matrix([0,1]) == s.zeros(2,1))
    t = s.symbols('t', real=True)
    Rt = s.Matrix([[1-t*t,-2*t],[2*t,1-t*t]])/(1+t*t)
    ck('state_curve_preserves_full_carrier', simp(Rt.T*Rt) == s.eye(2))
    rhot = Rt*s.diag(s.Rational(1,3),s.Rational(2,3))*Rt.T
    Ht = Rt*H0*Rt.T
    dr = rhot.diff(t).subs(t,0)
    dh = Ht.diff(t).subs(t,0)
    ck('noncommuting_density_jet_retained', dr*rhot.subs(t,0) != rhot.subs(t,0)*dr)
    ck('noncommuting_heat_jet_price_control', s.simplify(s.trace(rhot.subs(t,0)*dh)) == 0)
    ck('eigenvalue_collision_right_price_derivative', s.diff(-s.log((1+t)/2),t).subs(t,0) == -1)
    ck('eigenvalue_collision_left_price_derivative', s.diff(-s.log((1-t)/2),t).subs(t,0) == 1)

    eta = s.diag(1,-1,-1,-1)
    for i in range(4):
        for j in range(i,4):
            V = s.zeros(4)
            V[i,j] = 1
            V[j,i] = 1
            C = s.zeros(4)
            C[i,j] = 1 if i == j else s.Rational(1,2)
            C[j,i] = C[i,j]
            ck('ten_complete_equal_endpoint_tangents', s.eye(4)*V*s.eye(4).T == V)
            ck('ten_packed_coordinate_duals', s.trace(C.T*V) == 1)
    Vtf = s.diag(1,1,0,0)
    ck('central_field_shift_need_not_be_trace_only', s.trace(eta.inv()*Vtf) == 0 and Vtf[0,0] == 1)
    ck('exact_lorentz_constraint_pencil', s.expand((eta+t*Vtf).det()) == t*t-1)
    return {'checks': checks, 'exact_control_count': sum(checks.values()),
            'golden_full_modular_square_trace': 5, 'literal_toral_square_trace': 3,
            'new_Lean_propositions': 4, 'native_preparation_or_source_derived': False}


def verify_lean_receipt():
    rec = json.loads((ROOT/(BASE+'_results.json')).read_text())
    assert rec['status'] == 'PASS' and rec['compiler_exit_code'] == 0 and rec['input_head'] == HEAD
    assert len(rec['declarations']) == 4 and len(rec['axioms']) == 6
    assert sha(rec['capsule']) == rec['capsule_sha256']
    assert sha(rec['output']) == rec['output_sha256']
    for group in ['source_sha256','toolchain_sha256']:
        for path, digest in rec[group].items():
            assert sha(path) == digest, path
    output = (ROOT/rec['output']).read_text()
    assert ': error' not in output and ': warning' not in output and 'sorryAx' not in output
    for name in rec['declarations']+rec['printed_owner_declarations']:
        assert name in output, name
    for axioms in rec['axioms'].values():
        assert set(axioms) <= {'propext','Classical.choice','Quot.sound'}
    assert 'cited : self.timeEqualsModularFlow' in output
    assert 'h.d0PisotTimeLayer ∧ h.timeEqualsModularFlow' in output
    assert '!![0, 1; 1, -1]' in output
    assert not rec['matrix_logarithm_Gibbs_reconstruction_formalized']
    assert not rec['common_native_preparation_or_GR_derived']
    return {'compiled_propositions': 4, 'source_pins': len(rec['source_sha256']),
            'actual_axiom_reports': 6, 'all_axioms_standard': True}


def executed_mutations():
    source = (ROOT/(BASE+'_check.py')).read_text()
    mutations = [
        ('wrong_golden_state', '\n    rho_golden = reduced(psi)\n', '\n    rho_golden = s.eye(2)/2\n'),
        ('tensor_trace_replaced_by_pure_output', '\n    rho_golden = reduced(psi)\n', '\n    rho_golden = s.diag(1,0)\n'),
        ('diagonal_modular_modes_deleted', '\n    modular_expected = s.diag(1,phi,p,1)\n', '\n    modular_expected = s.diag(0,phi,p,0)\n'),
        ('hyperbolic_step_replaced_by_identity', '\n    T = s.Matrix([[0,1],[1,-1]])\n', '\n    T = s.eye(2)\n'),
        ('partition_normalized_before_price', '\n    partition = s.simplify(boltzmann.trace())\n', '\n    partition = s.Integer(1)\n'),
        ('heat_shift_sign_reversed', '\n    boltzmann = s.exp(-beta*c)*rho\n', '\n    boltzmann = s.exp(beta*c)*rho\n'),
        ('packed_offdiagonal_weight_lost', '\n            C[i,j] = 1 if i == j else s.Rational(1,2)\n', '\n            C[i,j] = 1\n'),
    ]
    results = []
    with tempfile.TemporaryDirectory(prefix='d0-modular-mutants-') as temp:
        for name, old, new in mutations:
            assert source.count(old) == 1, name
            path = Path(temp)/(name+'.py')
            path.write_text(source.replace(old,new))
            run = subprocess.run([sys.executable,str(path),'--repo',str(ROOT),'--math-only'],text=True,capture_output=True)
            assert run.returncode != 0 and 'AssertionError' in run.stderr, (name,run.returncode,run.stderr)
            results.append({'name': name, 'rejected_by_mathematical_assertion': True})
    return results


def false_ledger_controls(header):
    """Reject changed scope or input pins before any mathematical replay."""
    results = []
    with tempfile.TemporaryDirectory(prefix='d0-modular-ledgers-') as temp:
        for name in list(SCOPE) + ['proof_sha256','checker_sha256','lean_receipt_sha256']:
            bad = json.loads(json.dumps(header))
            if name in SCOPE:
                bad['scope'][name] = not bad['scope'][name]
            else:
                bad[name] = '0' * 64
            path = Path(temp)/(name+'.json')
            path.write_text(json.dumps(bad))
            run = subprocess.run([sys.executable,str(ROOT/(BASE+'_check.py')),
                                  '--repo',str(ROOT),'--expect',str(path)],
                                 text=True,capture_output=True)
            assert run.returncode != 0 and 'SOURCE_SCOPE_OR_INPUT_MISMATCH' in run.stderr, (name,run.returncode,run.stderr)
            results.append({'name':name,'rejected_before_mathematical_replay':True})
    return results


def main():
    global ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo',type=Path)
    ap.add_argument('--output',type=Path)
    ap.add_argument('--expect',type=Path)
    ap.add_argument('--math-only',action='store_true')
    args = ap.parse_args()
    ROOT = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[3]
    if args.math_only:
        result = mathematics()
        print('PASS_MODULAR_PREPARATION_MATHEMATICS', result['exact_control_count'])
        return
    header = {'schema':'d0-native-modular-preparation-boundary/1','input_head':HEAD,
              'scope':SCOPE,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
              'lean_receipt_sha256':sha(BASE+'_results.json')}
    expected = None
    if not args.output:
        expected = json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
        assert all(expected.get(k) == v for k,v in header.items()), 'SOURCE_SCOPE_OR_INPUT_MISMATCH'
    result = {**header, **mathematics(), 'lean':verify_lean_receipt(),
              'executed_mathematical_mutations':executed_mutations(),
              'executed_false_ledgers':false_ledger_controls(header)}
    if args.output:
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        assert result == expected, 'EXACT_CERTIFICATE_MISMATCH'
    print('PASS_NATIVE_MODULAR_PREPARATION_BOUNDARY', result['exact_control_count'],
          'controls;', len(result['executed_mathematical_mutations']), 'executed mutants;',
          len(result['executed_false_ledgers']), 'false ledgers rejected')


if __name__ == '__main__':
    main()
