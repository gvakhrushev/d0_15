#!/usr/bin/env python3
"""Verify the levelwise affine-action obstruction on the golden direct limit."""
import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

BASE = '02_REGISTRY/research/certificates/a4d_affine_direct_limit_levelwise_no_go'
PROOF = '02_REGISTRY/research/A4D_NATIVE_AFFINE_DIRECT_LIMIT_LEVELWISE_NO_GO.md'
FINITE = '02_REGISTRY/research/A4D_NATIVE_FINITE_AFFINE_UNITARY_NO_GO.md'
HISTORY = '02_REGISTRY/research/A4D_NATIVE_HISTORY_RESPONSE_DESCENT.md'
OWNER_CHECKS = [
    ('02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_check.py',
     'PASS_FINITE_LORENTZ_COVARIANT_POSITIVE_QUADRATIC'),
    ('02_REGISTRY/research/certificates/a4d_native_history_response_descent_check.py',
     'PASS_NATIVE_HISTORY_RESPONSE_DESCENT 189 controls 42 Lean propositions'),
]
OWNER_INPUTS = [
    FINITE,
    '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic.lean',
    '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_check.py',
    '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_results.json',
    '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_output.txt',
    HISTORY,
    '02_REGISTRY/research/certificates/a4d_native_history_response_descent.lean',
    '02_REGISTRY/research/certificates/a4d_native_history_response_descent_check.py',
    '02_REGISTRY/research/certificates/a4d_native_history_response_descent_results.json',
    '02_REGISTRY/research/certificates/a4d_native_history_response_descent_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_history_response_descent_output.txt',
]
TOOLCHAIN = [
    '03_FORMALIZATION/lean-toolchain',
    '03_FORMALIZATION/lakefile.lean',
    '03_FORMALIZATION/lake-manifest.json',
]
SCOPE = {
    'class': 'FINITE_POSITIVE_LEVELS_WITH_LEVEL_PRESERVING_AFFINE_UNITARY_ACTION',
    'finite_affine_translation_theorem_consumed': True,
    'actual_golden_isometric_refinement_owner_consumed': True,
    'physical_hilbert_completion_owned': False,
    'conditional_standard_completion_used': True,
    'levelwise_natural_translation_action_on_direct_limit_trivial': True,
    'cross_level_generator_required_for_nontrivial_action_in_this_class': True,
    'native_cross_level_affine_generator_derived': False,
    'physical_heat_block_F_selected': False,
    'whole_core_no_go': False,
    'G0_closed': False,
    'positive_gr': False,
    'global_closure': False,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--runtime-check', action='store_true',
                    help='compile the Lean capsule with the local Lake toolchain')
    args = ap.parse_args()
    if args.write and not args.runtime_check:
        ap.error('--write requires --runtime-check')
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root / p).read_bytes()).hexdigest()
    checks = []

    def ck(name, ok):
        assert bool(ok), name
        checks.append(name)

    lean_path = root / (BASE + '.lean')
    proof_path = root / PROOF
    out_path = root / (BASE + '_output.txt')
    if args.runtime_check:
        cmd = ['lake', 'env', 'lean', '../' + BASE + '.lean']
        run = subprocess.run(cmd, cwd=root / '03_FORMALIZATION', text=True,
                             capture_output=True)
        output = run.stdout + run.stderr
        ck('LEAN_RUNTIME_COMPILE_PASS', run.returncode == 0
           and ': error' not in output and ': warning' not in output
           and 'sorryAx' not in output and 'Lean.trustCompiler' not in output)
    else:
        output = out_path.read_text()
        ck('PINNED_LEAN_TRANSCRIPT_IS_CLEAN',
           ': error' not in output and ': warning' not in output
           and 'sorryAx' not in output and 'Lean.trustCompiler' not in output)
    if args.write:
        out_path.write_text(output)

    declarations = [
        'continuousLinearMap_eq_id_of_dense_fixed',
        'directLimit_translation_eq_id',
    ]
    names = ['D0.Research.AffineDirectLimitLevelwiseNoGo.' + n for n in declarations]
    ck('BOTH_DIRECT_LIMIT_PROPOSITIONS_PRINTED', all(
        re.search(r"'" + re.escape(n) + r"' depends on axioms:", output) for n in names))
    axioms = sorted({a.strip() for group in re.findall(
        r'depends on axioms: \[([^]]*)\]', output, re.S)
        for a in group.split(',') if a.strip()})
    ck('STANDARD_LOGICAL_AXIOMS_ONLY', set(axioms) <= {
        'propext', 'Classical.choice', 'Quot.sound'})
    ck('CAPSULE_HAS_NO_PLACEHOLDERS', not re.search(
        r'\b(sorry|admit|axiom|native_decide)\b', lean_path.read_text()))

    owner_outputs = {}
    for script, marker in OWNER_CHECKS:
        result = subprocess.run([sys.executable, str(root / script)], cwd=root,
                                text=True, capture_output=True)
        combined = result.stdout + result.stderr
        ck('OWNER_CHECK_' + Path(script).stem,
           result.returncode == 0 and marker in combined)
        owner_outputs[script] = combined.strip()

    finite_receipt = json.loads((root / OWNER_INPUTS[3]).read_text())
    history_receipt = json.loads((root / OWNER_INPUTS[8]).read_text())
    history_cert = json.loads((root / OWNER_INPUTS[9]).read_text())
    finite_theorem = (
        'D0.Research.FiniteLorentzCovariantPositiveQuadratic.'
        'invariant_nonnegative_quadratic_eq_zero'
    )
    ck('FINITE_OWNER_RECEIPT_PASS',
       finite_receipt['status'] == 'PASS_FINITE_LORENTZ_COVARIANT_POSITIVE_QUADRATIC'
       and finite_theorem in finite_receipt['lean_declarations']
       and finite_receipt['control_count'] == 20)
    ck('GOLDEN_HISTORY_OWNER_RECEIPT_PASS', history_receipt['status'] == 'PASS'
       and len(history_receipt['declarations']) == 42)
    ck('GOLDEN_HISTORY_EXACT_CERTIFICATE_PASS', history_cert['status'] == 'PASS'
       and len(history_cert['checks']) == 189)
    history_text = (root / HISTORY).read_text()
    proof_text = proof_path.read_text()
    ck('ACTUAL_ISOMETRIC_CYLINDER_INCLUSION_BOUND',
       'J e_w=a e_(wA)+p e_(wB)' in history_text
       and '(A⊗I)J=JA' in history_text)
    ck('PHYSICAL_ADMISSION_STAYS_OPEN',
       'Admission of both preparations' in history_text
       and not SCOPE['native_cross_level_affine_generator_derived'])
    ck('COMPLETION_SCOPE_STAYS_CONDITIONAL',
       'does not construct the completed Hilbert direct limit' in proof_text
       and 'not yet a repository-owned physical state space' in proof_text
       and not SCOPE['physical_hilbert_completion_owned'])

    if args.write:
        results = {
            'status': 'PASS',
            'source_head': 'bdbac63270a52b3da3e3348502682a8fc48459b8',
            'compiler_exit_code': run.returncode,
            'scope': SCOPE,
            'control_count': len(checks),
            'checks': checks,
            'capsule': BASE + '.lean',
            'capsule_sha256': sha(BASE + '.lean'),
            'output': BASE + '_output.txt',
            'output_sha256': sha(BASE + '_output.txt'),
            'proof': PROOF,
            'proof_sha256': sha(PROOF),
            'checker_sha256': sha('02_REGISTRY/research/certificates/a4d_affine_direct_limit_levelwise_no_go_check.py'),
            'owner_inputs_sha256': {p: sha(p) for p in OWNER_INPUTS},
            'toolchain_sha256': {p: sha(p) for p in TOOLCHAIN},
            'compiled_declarations': declarations,
            'axioms': axioms,
            'owner_results': {
                'finite_affine': {'status': finite_receipt['status'], 'controls': 20},
                'golden_history': {'status': history_receipt['status'],
                                   'controls': len(history_cert['checks']),
                                   'lean_propositions': len(history_receipt['declarations'])},
            },
            'owner_check_outputs': owner_outputs,
        }
        (root / (BASE + '_results.json')).write_text(
            json.dumps(results, indent=2, sort_keys=True) + '\n')
        print('PASS_A4D_AFFINE_DIRECT_LIMIT_LEVELWISE_NO_GO', len(checks), 'controls')
        return

    receipt = json.loads((root / (BASE + '_results.json')).read_text())
    ck('RESULT_RECEIPT_PASS', receipt['status'] == 'PASS'
       and receipt['scope'] == SCOPE and receipt['compiler_exit_code'] == 0
       and receipt['control_count'] == len(receipt['checks'])
       and 'LEAN_RUNTIME_COMPILE_PASS' in receipt['checks'])
    ck('PINNED_CAPSULE_OUTPUT_AND_PROOF',
       receipt['capsule_sha256'] == sha(BASE + '.lean')
       and receipt['output_sha256'] == sha(BASE + '_output.txt')
       and receipt['proof_sha256'] == sha(PROOF)
       and output == out_path.read_text())
    ck('PINNED_CHECKER_INPUTS',
       all(sha(p) == d for p, d in receipt['owner_inputs_sha256'].items())
       and all(sha(p) == d for p, d in receipt['toolchain_sha256'].items())
       and receipt['checker_sha256'] == sha(
           '02_REGISTRY/research/certificates/a4d_affine_direct_limit_levelwise_no_go_check.py'))
    print('PASS_A4D_AFFINE_DIRECT_LIMIT_LEVELWISE_NO_GO', len(checks), 'controls')


if __name__ == '__main__':
    main()
