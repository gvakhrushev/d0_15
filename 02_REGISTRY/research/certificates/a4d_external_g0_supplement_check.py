#!/usr/bin/env python3
"""Independent supplement review; original PASS count is not theorem acceptance."""
import argparse
import ast
import hashlib
import itertools
import json
from pathlib import Path

import sympy as sp

PREFIX = '02_REGISTRY/research/certificates/a4d_external_g0_supplement'
RAW = '02_REGISTRY/research/inputs/2026-10-07_external_g0_supplement/'
PROOF = '02_REGISTRY/research/A4D_EXTERNAL_G0_SUPPLEMENT_REVIEW_2026-10-07.md'
HISTORY = '02_REGISTRY/research/certificates/a4d_native_history_action'
HASHES = {
    'extra_dim.json': 'b4b2fef01d3693731633e8e98555939c53223e8d3207a2284ae8fbc7cb4be73f',
    '03_certificate_results (1).json': 'a252a2688a12adaab8a1a4b6d97c140fcd1a9fb2e30be54a2ddf3e151f4f12d3',
    'patch_s5.py': '0817a6055cf2dbcc3a9010303431229815c7ba7f738b4b56941d4fa692dc18f3',
    '03_EXACT_CERTIFICATE (1).py': 'ef444f34ae5c0c2cb4f1de419e0e2e068f7716d5c533e879378c8740bd5fefc6',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    for name, digest in HASHES.items():
        check('UNCHANGED_'+name, sha(RAW+name) == digest)
    replay = json.loads((root/(PREFIX+'_replay.json')).read_text())
    check('49_PASS_REPLAY_BOUND_TO_ORIGINALS', replay['script_exit_code'] == 0
          and replay['reported_passes'] == 49 and replay['reported_failures'] == 0
          and replay['json_semantically_identical_to_submission'] and replay['script_unmodified']
          and replay['inputs_sha256'] == {RAW+n: h for n, h in HASHES.items()}
          and not replay['universal_or_physical_claims_certified_by_replay'])
    source = (root/(RAW+'03_EXACT_CERTIFICATE (1).py')).read_text()
    calls = [n for n in ast.walk(ast.parse(source)) if isinstance(n, ast.Call)
             and isinstance(n.func, ast.Name) and n.func.id == 'rep']
    tagged = {ast.literal_eval(n.args[0]).split()[0]: n for n in calls}
    first = tagged['S1d'].args[1].values[0]
    check('S1D_HIDDEN_UNCONDITIONAL_SUCCESS', isinstance(first, ast.Call) and first.func.id == 'all'
          and isinstance(first.args[0].elt, ast.IfExp)
          and ast.literal_eval(first.args[0].elt.test) is False
          and ast.literal_eval(first.args[0].elt.orelse) is True
          and ast.literal_eval(first.args[0].generators[0].iter) == [3])
    patch_tree = ast.parse((root/(RAW+'patch_s5.py')).read_text())
    markers = [ast.literal_eval(n.args[0]) for n in ast.walk(patch_tree) if isinstance(n, ast.Call)
               and isinstance(n.func, ast.Attribute) and n.func.attr == 'index']
    check('PATCH_DOES_NOT_MATCH_SUPPLIED_VERSION', len(markers) == 2 and all(m not in source for m in markers)
          and replay['patch_executed'] is False)
    check('S6J_CHECKS_ONLY_DIFFERENT_SYMBOLS', ast.unparse(tagged['S6j'].args[1]) == "sp.Symbol('F0') != sp.Symbol('F1')")
    check('S5F_IS_ARITHMETIC_NOT_OPERATOR_RANK', ast.unparse(tagged['S5f'].args[1]) == '15 * 4 == 60 and 2 ** 4 - 1 == 15')
    check('T16_RETRACTION_IS_EXPLICIT', 'прежняя T16 отозвана' in source)

    L = sp.Symbol('L', integer=True, positive=True)
    kernel = sum(sp.binomial(4, z)*(L-1)**(4-z)*(6+z*(z+1)/sp.Integer(2)) for z in range(5))
    check('FULL_METRIC_KERNEL_POLYNOMIAL', sp.expand(kernel) == 6*L**4+4*L**3+6*L**2)
    check('EXACT_RESTRICTION_RANK_IDENTITY_EVEN', sp.expand(4*(L**4-1)-4*(L**4-16)) == 60)
    check('EXACT_RESTRICTION_RANK_IDENTITY_ODD', sp.expand(4*(L**4-1)-4*(L**4-1)) == 0)
    check('CORRECT_QUOTIENT_AT_L4', 6*4**4+4*4**3+6*4**2-60 == 1828)
    check('L2_EXCEPTION_NOT_EXTENDED_TO_L4', 4*(2**4-16) == 0 and 4*(4**4-16) > 0)
    check('LOWER_BOUND_HOLDS_FOR_EVEN_L_GE2', sp.expand((6*L**4+4*L**3+6*L**2-60)
          -(2*L**4+4*L**3+6*L**2+4)-4*(L-2)*(L+2)*(L**2+4)) == 0)

    # Literal Fourier multipliers; all characters at the three test sizes.
    for size, phases in [(2, [1, -1]), (3, [1, -sp.Rational(1, 2)+sp.sqrt(3)*sp.I/2,
                                          -sp.Rational(1, 2)-sp.sqrt(3)*sp.I/2]),
                         (4, [1, sp.I, -1, -sp.I])]:
        symbols = [(sp.simplify((1+1/sp.sympify(p))/2), sp.simplify(size*(p-1)),
                    sp.simplify(size*(p-1/p)/2)) for p in map(sp.sympify, phases)]
        totals = [0, 0, 0]
        for ks in itertools.product(range(size), repeat=4):
            m, s, t = zip(*(symbols[k] for k in ks))
            assert all(sp.simplify(m[a]*s[a]-t[a]) == 0 for a in range(4))
            z = sum(x == 0 for x in m)
            totals[0] += 10-z*(z+1)//2
            totals[1] += 4*int(any(x != 0 for x in s))
            totals[2] += 4*int(any(x != 0 for x in t))
            for vec in [s, t]:
                if any(x != 0 for x in vec):
                    pivot = next(x for x in vec if x != 0)
                    assert sp.simplify(pivot**4) != 0
        expected_r = 10*size**4-(4*size**3+6*size**2 if size % 2 == 0 else 0)
        expected_rd = 4*(size**4-(16 if size % 2 == 0 else 1))
        check('ALL_CHARACTER_SYMBOLS_L'+str(size), totals == [expected_r, 4*(size**4-1), expected_rd]
              and totals[1]-totals[2] == (60 if size % 2 == 0 else 0))

    size = 4
    sites = list(itertools.product(range(size), repeat=4))

    def shifted(x, a, step):
        y = list(x); y[a] = (y[a]+step) % size
        return tuple(y)

    def witness(x, a, b):
        return (-1)**(x[0]+x[1]) if (a, b) == (0, 1) else 0

    def average(x, a, b):
        return sp.Rational(witness(x, a, b)+witness(shifted(x, a, -1), a, b), 2)

    check('ALL_CENTERED_COFRAME_COMPONENTS_ZERO', all(average(x, a, b) == 0
          for x in sites for a in range(4) for b in range(4)))
    check('ALL_TEN_METRIC_COMPONENTS_ZERO', all(average(x, a, b)+average(x, b, a) == 0
          for x in sites for a in range(4) for b in range(a, 4)))
    origin = (0, 0, 0, 0)
    curl = size*(witness(shifted(origin, 0, 1), 1, 1)-witness(origin, 1, 1))
    curl -= size*(witness(shifted(origin, 1, 1), 0, 1)-witness(origin, 0, 1))
    check('CURL_WITNESS_SIGN_IS_PLUS_EIGHT', curl == 8 and curl != -8)
    check('FORWARD_CURL_ZERO_ON_IMAGE_STRUCTURALLY', all(shifted(shifted(x, a, 1), b, 1)
          == shifted(shifted(x, b, 1), a, 1) for x in sites for a in range(4) for b in range(4)))
    eta = sp.diag(-1, 1, 1, 1)
    B = sp.zeros(4); B[1, 2] = 1; B[2, 1] = -1
    check('LINEAR_METRIC_KERNEL_NOT_FULL_GRAM_FIBER', B+B.T == sp.zeros(4)
          and B*eta+eta*B.T == sp.zeros(4) and B*eta*B.T != sp.zeros(4))
    extra = json.loads((root/(RAW+'extra_dim.json')).read_text())
    check('EXTRA_DIM_IS_NOT_FOUR_DIMENSIONAL_CARRIER', all(r['dimE'] == 16*r['L']
          and r['dimE'] != 16*r['L']**4 and r['dimM'] == 10*r['L'] for r in extra))
    check('EXTRA_DIM_MISSING_INTERSECTION_EVIDENCE', all(r['rankR_on_imD'] is None for r in extra))
    check('EXTRA_DIM_MATCHES_ONLY_DIAGONAL_CYCLE_COUNTS', all(r['rankR'] == 10*(r['L']-int(r['L'] % 2 == 0))
          and r['rankD'] == 4*(r['L']-1) for r in extra))

    p, q = [0, 9], [9, 0]
    combined = p+q[1:]
    indicator = lambda v: int(v == p)
    occurrences = lambda v: sum((u, w) == (0, 9) for u, w in zip(v, v[1:]))
    check('PATH_INDICATOR_IS_NOT_ADDITIVE', indicator(combined) != indicator(p)+indicator(q))
    check('EDGE_OCCURRENCE_EXTENSION_IS_ADDITIVE', occurrences(combined) == occurrences(p)+occurrences(q))
    history = json.loads((root/(HISTORY+'_certificate.json')).read_text())
    check('FULL_HISTORY_RESULT_NOT_JUST_718_MINUS_33', history['status'] == 'PASS_COMPLETE_SCENE_HISTORY_INTERFACE_BOUNDARY'
          and history['compiled_declarations'] == 20 and history['transitive_d0_source_pins'] == 48
          and 'ENDPOINT_BOUNDARY_OPERATOR_IS_I_MINUS_T' in history['checks']
          and 'SAME_LENGTH_ENDPOINTS_DISTINCT_ADDITIVE_ACTION' in history['checks'])
    check('DISTINCT_HISTORY_QUOTIENTS', 718-33 == 685 and 718-32 == 686 and 685+32+1 == 718)

    scope = {
        'kernel_intersection': '60_EVEN_0_ODD_BY_EXISTING_ALL_SIZE_RANK_THEOREMS',
        'linear_coframe_quotient_L4': 1828,
        'T16_retracted': True,
        'submitted_49_passes_prove_all_labels': False,
        'S1d_has_no_unconditional_success': False,
        'raw_curl_is_physical_curvature': False,
        'outside_forward_image_excludes_all_physical_gauge': False,
        'linear_metric_kernel_equals_nonlinear_gram_fiber': False,
        'extra_dim_is_4d_evidence': False,
        'patch_applied': False,
        'new_full_proof_document_received': False,
        'S6j_proves_full_core_independence': False,
        'G0_closed': False,
        'native_source_constructed': False,
        'positive_gr': False,
        'original_parent_terminals_changed': False,
    }
    inputs = [PROOF, PREFIX+'_replay.json', HISTORY+'_certificate.json',
              '02_REGISTRY/research/A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md',
              '02_REGISTRY/research/A4D_NATIVE_CENTERED_METRIC_LIFT.md',
              '02_REGISTRY/research/A4D_NATIVE_DYNAMICAL_OWNERSHIP.md',
              '03_FORMALIZATION/D0/Geometry/A4DCoframeParentConstraint.lean']
    payload = {'status': 'PASS_PARTIAL_SUPPLEMENT_ACCEPTANCE',
               'input_head': '27175008f7dbba9a98bc739f6cde0958a53858e8',
               'inputs_sha256': {p: sha(p) for p in inputs},
               'checker_sha256': sha(PREFIX+'_check.py'), 'checks': checks, 'scope': scope,
               'submitted_pass_count': 49, 'raw_inputs_sha256': {RAW+n: h for n, h in HASHES.items()}}
    encoded = json.dumps(payload, sort_keys=True, indent=2)+'\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        expected = args.expect or root/(PREFIX+'_certificate.json')
        assert json.loads(expected.read_text()) == json.loads(encoded), 'PINNED_LEDGER_MISMATCH'
    print('PASS_EXTERNAL_G0_SUPPLEMENT', len(checks), 'independent controls; original 49 PASS separate')


if __name__ == '__main__':
    main()
