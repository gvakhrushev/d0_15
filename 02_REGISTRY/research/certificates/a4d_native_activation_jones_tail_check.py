#!/usr/bin/env python3
"""Bind the four-level AF activation to the existing all-level Jones tail."""
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
ACT = '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation'
JONES = '02_REGISTRY/research/certificates/a4d_native_jones_record_transport'
BASE = '02_REGISTRY/research/certificates/a4d_native_activation_jones_tail'
PROOF = '02_REGISTRY/research/A4D_NATIVE_FOUR_LEVEL_SELF_SIMILAR_TAIL.md'
SOURCE_HEAD = 'b45e32ebce6f04553e1d0212cba4c1ccf3cb78bf'
INPUTS = [
    '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md',
    '02_REGISTRY/research/A4D_NATIVE_JONES_RECORD_TRANSPORT.md',
    ACT + '.py', ACT + '_check.py', ACT + '_certificate.json',
    ACT + '.lean', ACT + '_results.json',
    JONES + '.py', JONES + '_check.py', JONES + '_certificate.json',
    JONES + '.lean', JONES + '_results.json',
]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


E = load('activation_tail_input', ACT + '.py')
N = load('jones_tail_input', JONES + '.py')
s, p = E.s, E.p
U = E.record()
PRICE = s.diag(1, 1, 0, 0)
BLANK = s.diag(1, 0, 1, 0)


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def check(name, value, checks):
    assert bool(value), name
    checks.append(name)


def equal(name, value, checks):
    check(name, E.zero(value), checks)


def verify_parent(base, checks):
    cert = json.loads((ROOT / (base + '_certificate.json')).read_text())
    check(base + '_parent_certificate_passes', cert['status'] == 'PASS', checks)
    check(base + '_parent_proof_hash', cert['proof_sha256'] == sha(cert['proof']), checks)
    check(base + '_parent_checker_hash', cert['checker_sha256'] == sha(base + '_check.py'), checks)
    check(base + '_parent_program_hash', cert['program_sha256'] == sha(base + '.py'), checks)
    for path, digest in cert['input_sha256'].items():
        check(base + '_parent_input_' + path, sha(path) == digest, checks)
    receipt = json.loads((ROOT / (base + '_results.json')).read_text())
    check(base + '_lean_receipt_passes',
          receipt.get('status') == 'PASS' and receipt.get('compiler_exit_code') == 0,
          checks)
    check(base + '_lean_receipt_hash',
          cert['Lean_receipt_sha256'] == sha(base + '_results.json'), checks)


def activation_package(level, checks):
    """Actual four-frame operators in literal native six-path order."""
    sizes = E.counts(level)
    three_step_rows = E.segments(*sizes, 3)
    result = []
    for part in E.right_frames(level):
        j = part['old_type']
        d = part['spectator_dimension']
        V = part['V']
        frames = [V[:, i*d:(i+1)*d] for i in range(4)]

        # The activation constructor uses reverse-column path coordinates;
        # the Jones constructor uses literal inclusion order.
        native = E.segments(*sizes, 6)[j]
        index = {(kind, path, row): offset + row
                 for kind, path, offset in native
                 for row in range(sizes[kind])}
        Q = s.zeros(V.rows)
        targets = []
        for oldrow, (v, k, row) in enumerate(part['labels']):
            _, colpath, _ = three_step_rows[v][k]
            kind, rowpath, row_offset = next(
                item for item in three_step_rows[v]
                if item[2] <= row < item[2] + sizes[item[0]])
            path = rowpath + tuple(reversed(((j,) + colpath)[:-1]))
            target = index[(kind, path, row - row_offset)]
            targets.append(target)
            Q[target, oldrow] = 1
        check('activation_to_native_path_order_is_bijection_level_' + str(level),
              len(set(targets)) == V.rows, checks)

        units = [[E.mat(Q * (frames[i] * frames[k].T) * Q.T)
                  for k in range(4)] for i in range(4)]
        support = E.mat(sum((units[i][i] for i in range(4)), s.zeros(V.rows)))
        identity = s.eye(V.rows)
        W = E.mat(sum((U[i, k] * units[i][k]
                       for i in range(4) for k in range(4)), s.zeros(V.rows))
                  + identity - support)
        price = E.mat(sum((PRICE[i, k] * units[i][k]
                           for i in range(4) for k in range(4)), s.zeros(V.rows)))
        blank = E.mat(sum((BLANK[i, k] * units[i][k]
                           for i in range(4) for k in range(4)), s.zeros(V.rows)))
        result.append({'units': units, 'R': support, 'W': W,
                       'P': price, 'B': blank, 'e': units[0][0], 'd': d})
    return result


def package_from_units(units):
    result = []
    for block_units in units:
        n = block_units[0][0].rows
        support = E.mat(sum((block_units[i][i] for i in range(4)), s.zeros(n)))
        identity = s.eye(n)
        W = E.mat(sum((U[i, j] * block_units[i][j]
                       for i in range(4) for j in range(4)), s.zeros(n))
                  + identity - support)
        price = E.mat(sum((PRICE[i, j] * block_units[i][j]
                           for i in range(4) for j in range(4)), s.zeros(n)))
        blank = E.mat(sum((BLANK[i, j] * block_units[i][j]
                           for i in range(4) for j in range(4)), s.zeros(n)))
        result.append({'units': block_units, 'R': support, 'W': W,
                       'P': price, 'B': blank, 'e': block_units[0][0]})
    return result


def controls():
    checks = []
    verify_parent(ACT, checks)
    verify_parent(JONES, checks)

    seed = activation_package(0, checks)
    fresh = activation_package(1, checks)

    # The activation's V0 corner is exactly the existing native Jones corner.
    jones_seed = [E.mat(J*J.T) for J in N.corner_frames(0)]
    for b in range(2):
        equal(f'seed_Jones_corner_identity_block_{b}',
              seed[b]['e'] - jones_seed[b], checks)

    # Transport each of the sixteen matrix units using the actual Jones map.
    mapped_units = [[[None for _ in range(2)] for _ in range(4)] for _ in range(4)]
    for i in range(4):
        for j in range(4):
            old_blocks = [seed[b]['units'][i][j] for b in range(2)]
            new_blocks = N.transport(0, old_blocks)
            for b in range(2):
                mapped_units[i][j][b] = new_blocks[b]
            equal(f'matrix_unit_trace_preserved_{i}_{j}',
                  N.native_trace(7, new_blocks) - N.native_trace(6, old_blocks), checks)
    tail = package_from_units([
        [[mapped_units[i][j][b] for j in range(4)] for i in range(4)]
        for b in range(2)])

    # Bind the reconstructed package to direct transport of its full readouts.
    for key in ('W', 'P', 'B', 'R'):
        direct = N.transport(0, [seed[b][key] for b in range(2)])
        for b in range(2):
            equal(f'direct_transport_reconstruction_{key}_{b}',
                  tail[b][key] - direct[b], checks)
    for b in range(2):
        equal(f'Jones_transport_matches_fresh_corner_block_{b}',
              tail[b]['e'] - fresh[b]['e'], checks)

    # Exact hostile boundary: the canonical fresh apparatus is not the
    # recursively transported seed, although their prepared corner is equal.
    fresh_diffs = {}
    for key in ('W', 'P', 'B', 'R'):
        vals = [not E.zero(tail[b][key] - fresh[b][key]) for b in range(2)]
        fresh_diffs[key] = vals
        check(f'transported_{key}_differs_from_fresh_canonical_frame',
              all(vals), checks)

    for b, block in enumerate(tail):
        n = block['W'].rows
        I = s.eye(n)
        equal(f'tail_full_step_unitary_{b}', block['W'].T*block['W'] - I, checks)
        equal(f'tail_price_projection_{b}', block['P']*block['P'] - block['P'], checks)
        equal(f'tail_blank_projection_{b}', block['B']*block['B'] - block['B'], checks)
        equal(f'tail_readouts_commute_{b}', block['P']*block['B'] - block['B']*block['P'], checks)
        check(f'tail_readouts_distinct_{b}', not E.zero(block['P'] - block['B']), checks)
        equal(f'tail_support_projection_{b}', block['R']*block['R'] - block['R'], checks)
        equal(f'tail_complement_fixed_{b}',
              (I - block['R'])*block['W'] - (I - block['R']), checks)
        for ticks, value, rank in ((1, p*p, 2*E.counts(1)[b]),
                                   (2, E.red(4*p**3), E.counts(1)[b])):
            power = E.mat(block['W']**ticks)
            feedback = E.mat(block['P'] - block['P']*power.T*block['P']*power*block['P'])
            equal(f'tail_feedback_polynomial_{b}_{ticks}',
                  feedback*feedback - value*feedback, checks)
            equal(f'tail_feedback_rank_trace_{b}_{ticks}',
                  s.trace(feedback) - rank*value, checks)
            equal(f'tail_feedback_complement_zero_{b}_{ticks}',
                  feedback*(I - block['R']), checks)

    for label, package, level in (('seed', seed, 6), ('tail', tail, 7)):
        e_blocks = [block['e'] for block in package]
        r_blocks = [block['R'] for block in package]
        p_blocks = [block['P'] for block in package]
        b_blocks = [block['B'] for block in package]
        equal(label + '_corner_trace_p6',
              N.native_trace(level, e_blocks) - p**6, checks)
        equal(label + '_four_frame_trace_4p6',
              N.native_trace(level, r_blocks) - 4*p**6, checks)
        equal(label + '_price_cut_trace_2p6',
              N.native_trace(level, p_blocks) - 2*p**6, checks)
        equal(label + '_blank_cut_trace_2p6',
              N.native_trace(level, b_blocks) - 2*p**6, checks)

    for ticks in (1, 2):
        def feedback(package):
            return [E.mat(block['P'] - block['P']*E.mat(block['W']**ticks).T
                          * block['P']*E.mat(block['W']**ticks)*block['P'])
                    for block in package]
        equal(f'weighted_feedback_trace_preserved_{ticks}',
              N.native_trace(7, feedback(tail)) - N.native_trace(6, feedback(seed)), checks)
        expected = 2*p**8 if ticks == 1 else p**6*E.red(4*p**3)
        equal(f'weighted_feedback_exact_value_{ticks}',
              N.native_trace(6, feedback(seed)) - expected, checks)
        equal(f'weighted_feedback_tail_value_{ticks}',
              N.native_trace(7, feedback(tail)) - expected, checks)

    return {
        'status': 'PASS',
        'source_head': SOURCE_HEAD,
        'proof': PROOF,
        'scope': {
            'seed': 'ACTUAL_FOUR_LEVEL_ACTIVATION_IN_A6',
            'tail': 'ITERATED_EXISTING_TRACE_PRESERVING_JONES_HOMOMORPHISMS',
            'same_prepared_corner': True,
            'all_16_matrix_units_transported': True,
            'full_step_and_both_readouts_transported': True,
            'complement_retained': True,
            'canonical_fresh_activation_equals_transported_tail': False,
            'metric_link_tangent_source_Ward_curved_root_or_GR': 'OPEN',
            'physical_time_or_spatial_expansion_identification': 'OPEN',
        },
        'exact_controls': len(checks),
        'checks': dict(sorted(Counter(checks).items())),
        'fresh_activation_differences_by_block': fresh_diffs,
        'input_sha256': {path: sha(path) for path in INPUTS},
        'proof_sha256': sha(PROOF),
        'checker_sha256': sha(BASE + '_check.py'),
        'activation_parent_certificate_sha256': sha(ACT + '_certificate.json'),
        'jones_parent_certificate_sha256': sha(JONES + '_certificate.json'),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = controls()
    target = ROOT / (BASE + '_certificate.json')
    if args.write:
        target.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    else:
        assert json.loads(target.read_text()) == result, 'ACTIVATION_JONES_TAIL_LEDGER_MISMATCH'
    print('PASS_ACTIVATION_JONES_SEEDED_TAIL controls=%d' % result['exact_controls'])


if __name__ == '__main__':
    main()
