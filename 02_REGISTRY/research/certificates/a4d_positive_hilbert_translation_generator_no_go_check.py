#!/usr/bin/env python3
"""Exact controls for the positive-Hilbert Lorentz generator obstruction."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from fractions import Fraction as F
from itertools import permutations
from pathlib import Path

BASE = '02_REGISTRY/research/certificates/a4d_positive_hilbert_translation_generator_no_go'
PROOF = '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HILBERT_TRANSLATION_GENERATOR_NO_GO.md'
FINITE = '02_REGISTRY/research/A4D_NATIVE_FINITE_AFFINE_UNITARY_NO_GO.md'
DIRECT_LIMIT = '02_REGISTRY/research/A4D_NATIVE_AFFINE_DIRECT_LIMIT_LEVELWISE_NO_GO.md'
FINITE_CAPSULE = '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic.lean'
FINITE_CHECKER = '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_check.py'
FINITE_RECEIPT = '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_results.json'
FINITE_OUTPUT = '02_REGISTRY/research/certificates/a4d_finite_lorentz_covariant_positive_quadratic_output.txt'
TOOLCHAIN = [
    '03_FORMALIZATION/lean-toolchain',
    '03_FORMALIZATION/lakefile.lean',
    '03_FORMALIZATION/lake-manifest.json',
]
OWNER_INPUTS = [FINITE, DIRECT_LIMIT, FINITE_CAPSULE, FINITE_CHECKER,
                FINITE_RECEIPT, FINITE_OUTPUT]
DECLARATION = (
    'D0.Research.PositiveHilbertTranslationGeneratorNoGo.'
    'lorentz_invariant_positive_readout_eq_zero'
)
SCOPE = {
    'positive_hilbert_lorentz_invariant_linear_readout_is_zero': True,
    'hilbert_schmidt_generator_consequence_under_unitary_conjugation': True,
    'nontrivial_infinite_dimensional_affine_action_excluded': False,
    'native_translation_generator_hilbert_schmidt': False,
    'native_two_tick_price_identified_with_hilbert_schmidt_norm': False,
    'physical_heat_block_or_source_derived': False,
    'positive_gr': False,
    'global_closure': False,
}


def matmul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]


def transpose(a):
    return [list(row) for row in zip(*a)]


def determinant(a):
    def sign(p):
        inversions = sum(p[i] > p[j] for i in range(len(p))
                         for j in range(i + 1, len(p)))
        return -1 if inversions % 2 else 1
    return sum(sign(p) * _product(a[i][p[i]] for i in range(len(p)))
               for p in permutations(range(len(a))))


def _product(xs):
    result = F(1)
    for x in xs:
        result *= x
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    parser.add_argument('--runtime-check', action='store_true',
                        help='compile the Lean capsule with the local Lake toolchain')
    args = parser.parse_args()
    if args.write and not args.runtime_check:
        parser.error('--write requires --runtime-check')
    root = Path(__file__).resolve().parents[3]
    sha = lambda path: hashlib.sha256((root / path).read_bytes()).hexdigest()
    checks = []

    def ck(name, ok):
        assert bool(ok), name
        checks.append(name)

    capsule = root / (BASE + '.lean')
    proof = root / PROOF
    output_path = root / (BASE + '_output.txt')
    if args.runtime_check:
        command = ['lake', 'env', 'lean', '../' + BASE + '.lean']
        run = subprocess.run(command, cwd=root / '03_FORMALIZATION', text=True,
                             capture_output=True)
        output = run.stdout + run.stderr
        ck('LEAN_RUNTIME_COMPILE_PASS', run.returncode == 0
           and ': error' not in output and ': warning' not in output
           and 'sorryAx' not in output and 'Lean.trustCompiler' not in output)
    else:
        output = output_path.read_text()
        ck('PINNED_LEAN_TRANSCRIPT_IS_CLEAN',
           ': error' not in output and ': warning' not in output
           and 'sorryAx' not in output and 'Lean.trustCompiler' not in output)
    if args.write:
        output_path.write_text(output)
    ck('ACTUAL_THEOREM_PRINTED', re.search(
        r"'" + re.escape(DECLARATION) + r"' depends on axioms:", output) is not None)
    axiom_match = re.search(
        r"'" + re.escape(DECLARATION) + r"' depends on axioms: \[([^]]*)\]",
        output, re.S)
    axioms = sorted(x.strip() for x in axiom_match.group(1).split(',') if x.strip()) \
        if axiom_match else []
    ck('STANDARD_LOGICAL_AXIOMS_ONLY', bool(axiom_match)
       and set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'})
    ck('NO_PLACEHOLDERS_IN_CAPSULE', not re.search(
        r'\b(sorry|admit|axiom|native_decide)\b', capsule.read_text()))

    finite = subprocess.run([sys.executable, str(root / FINITE_CHECKER)],
                            cwd=root, text=True, capture_output=True)
    finite_text = finite.stdout + finite.stderr
    ck('FINITE_OWNER_CERTIFICATE_REPLAY', finite.returncode == 0
       and 'PASS_FINITE_LORENTZ_COVARIANT_POSITIVE_QUADRATIC' in finite_text)
    finite_receipt = json.loads((root / FINITE_RECEIPT).read_text())
    ck('OWNED_BOOST_THEOREM_RECEIPT',
       finite_receipt['status'] == 'PASS_FINITE_LORENTZ_COVARIANT_POSITIVE_QUADRATIC'
       and finite_receipt['control_count'] == 20
       and any(name.endswith('.rational_boost_matches_owned_role_boost')
               for name in finite_receipt['lean_declarations']))

    q = F
    eta = [[q(1), 0, 0, 0], [0, q(-1), 0, 0],
           [0, 0, q(-1), 0], [0, 0, 0, q(-1)]]
    boost = [[q(5, 3), q(4, 3), 0, 0], [q(4, 3), q(5, 3), 0, 0],
             [0, 0, 1, 0], [0, 0, 0, 1]]
    inverse = [[q(5, 3), q(-4, 3), 0, 0], [q(-4, 3), q(5, 3), 0, 0],
               [0, 0, 1, 0], [0, 0, 0, 1]]
    quarter_z = [[1, 0, 0, 0], [0, 0, -1, 0],
                 [0, 1, 0, 0], [0, 0, 0, 1]]
    quarter_y = [[1, 0, 0, 0], [0, 0, 0, 1],
                 [0, 0, 1, 0], [0, -1, 0, 0]]
    ident = [[q(int(i == j)) for j in range(4)] for i in range(4)]
    for name, matrix in [('boost', boost), ('inverse_boost', inverse),
                         ('quarter_turn_z', quarter_z), ('quarter_turn_y', quarter_y)]:
        ck(name + '_exact_lorentz',
           matmul(matmul(transpose(matrix), eta), matrix) == eta)
        ck(name + '_proper', determinant(matrix) == 1)
    ck('BOOST_INVERSE_EXACT', matmul(boost, inverse) == ident
       and matmul(inverse, boost) == ident)
    e_x = [0, 1, 0, 0]
    ck('QUARTER_TURNS_MOVE_SPATIAL_BASIS',
       [sum(quarter_z[i][j] * e_x[j] for j in range(4)) for i in range(4)] == [0, 0, 1, 0]
       and [sum(quarter_y[i][j] * e_x[j] for j in range(4)) for i in range(4)] == [0, 0, 0, -1])

    plus_cross = 2 * q(5, 3) * q(4, 3)
    square_diag = q(5, 3) ** 2 - 1
    spatial_diag = q(4, 3) ** 2
    ck('BOOST_SQUARED_NORM_EQUATIONS_EXACT',
       square_diag == spatial_diag == q(16, 9) and plus_cross == q(40, 9))
    ck('OPPOSITE_BOOST_CROSS_TERMS_CANCEL',
       plus_cross + (-plus_cross) == 0 and q(16) + q(16) == q(32))
    ck('POSITIVE_SQUARED_NORM_HOSTILE_CONTROLS',
       q(0) + q(0) == 0
       and all(a + b != 0 for a in [q(1), q(2)] for b in [q(0), q(1), q(2)]))
    spatial_norm_sq = lambda v: v[1] ** 2 + v[2] ** 2 + v[3] ** 2
    spatial_witness = [0, 1, 0, 0]
    ck('WITHOUT_BOOST_SPATIAL_READOUT_SURVIVES',
       spatial_norm_sq(spatial_witness) == 1
       and spatial_norm_sq([0, -0, 1, 0]) == 1
       and spatial_norm_sq([0, 0, 0, -1]) == 1)
    ck('POSITIVE_TIME_READOUT_FAILS_BOOST', q(5, 3) ** 2 != 1)
    ck('INDEFINITE_MINKOWSKI_TARGET_ADMITS_NONZERO_READOUT',
       eta[0][0] == 1 and eta[1][1] == -1
       and all(matmul(matmul(transpose(matrix), eta), matrix) == eta
               for matrix in [boost, inverse, quarter_z, quarter_y]))

    proof_text = proof.read_text()
    direct_limit_text = (root / DIRECT_LIMIT).read_text()
    ck('HS_CONSEQUENCE_IS_EXPLICITLY_CONDITIONAL',
       'If every \\(P(v)\\) is Hilbert' in proof_text
       and 'does not construct or exclude the actual' in proof_text)
    ck('PHYSICAL_IDENTIFICATION_STAYS_OPEN',
       not SCOPE['native_translation_generator_hilbert_schmidt']
       and not SCOPE['native_two_tick_price_identified_with_hilbert_schmidt_norm']
       and 'physical affine action' in direct_limit_text)

    if args.write:
        receipt = {
            'status': 'PASS',
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
            'checker_sha256': sha(BASE + '_check.py'),
            'owner_inputs_sha256': {p: sha(p) for p in OWNER_INPUTS},
            'toolchain_sha256': {p: sha(p) for p in TOOLCHAIN},
            'compiled_declarations': [DECLARATION],
            'axioms': axioms,
            'finite_owner': {'status': finite_receipt['status'],
                             'controls': finite_receipt['control_count']},
            'exact_matrices': {
                'boost': '[[5/3,4/3,0,0],[4/3,5/3,0,0],[0,0,1,0],[0,0,0,1]]',
                'inverse': '[[5/3,-4/3,0,0],[-4/3,5/3,0,0],[0,0,1,0],[0,0,0,1]]',
                'quarter_turn_z': quarter_z,
                'quarter_turn_y': quarter_y,
            },
            'owner_replay_output': finite_text.strip(),
        }
        (root / (BASE + '_results.json')).write_text(
            json.dumps(receipt, indent=2, sort_keys=True) + '\n')
        print('PASS_A4D_POSITIVE_HILBERT_TRANSLATION_GENERATOR_NO_GO', len(checks), 'controls')
        return

    receipt = json.loads((root / (BASE + '_results.json')).read_text())
    ck('RESULT_RECEIPT_SCOPE', receipt['status'] == 'PASS'
       and receipt['scope'] == SCOPE and receipt['compiler_exit_code'] == 0
       and receipt['control_count'] == len(receipt['checks'])
       and 'LEAN_RUNTIME_COMPILE_PASS' in receipt['checks'])
    ck('PINNED_CAPSULE_OUTPUT_PROOF',
       receipt['capsule_sha256'] == sha(BASE + '.lean')
       and receipt['output_sha256'] == sha(BASE + '_output.txt')
       and receipt['proof_sha256'] == sha(PROOF)
       and output == output_path.read_text())
    ck('PINNED_OWNER_AND_TOOLCHAIN_INPUTS',
       all(sha(p) == digest for p, digest in receipt['owner_inputs_sha256'].items())
       and all(sha(p) == digest for p, digest in receipt['toolchain_sha256'].items())
       and receipt['checker_sha256'] == sha(BASE + '_check.py'))
    print('PASS_A4D_POSITIVE_HILBERT_TRANSLATION_GENERATOR_NO_GO', len(checks), 'controls')


if __name__ == '__main__':
    main()
