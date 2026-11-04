#!/usr/bin/env python3
"""Verify the source, patch and bounded-replay receipts without executing them."""
from __future__ import annotations
import argparse
import hashlib
import json
import lzma
import re
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
BASE = '05cc38dc6283f45995a4c86fb69067c87734bb4c'
HEAD = '2900145fe674629b61949587917a3a2ea5188797'
COMMITS = ['e6e46c805f8a51c6965aa6abbd8fc3e4b71a7d74',
           '66edbcfd458daecd133baca3b44528931e2ebfc5',
           'cfe6755a0ddf5174698f003db59531a1ebd93fa1', HEAD]


def need(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--verify-source-objects', action='store_true')
    args = parser.parse_args()
    m = json.loads((ROOT / 'MANIFEST.json').read_text(encoding='utf-8'))
    need(m['base'] == BASE and m['head'] == HEAD and m['commits'] == COMMITS,
         'source range differs from this verifier')
    paths = {'task': '00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md',
             'memo': '02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'}
    need(m['changed_paths'] == paths, 'changed path set differs')
    expected_pairs = {(ref, path) for ref in [BASE, *COMMITS] for path in paths.values()}
    pairs = set()
    final_memo = None
    for item in m['snapshots']:
        path = ROOT / item['snapshot']
        packed = path.read_bytes()
        need(sha(packed) == item['snapshot_sha256'], 'compressed snapshot differs')
        data = lzma.decompress(packed)
        need(len(data) == item['bytes'] and sha(data) == item['sha256'] and blob(data) == item['git_blob'],
             'snapshot content/blob differs')
        pair = (item['commit'], item['source_path'])
        need(pair not in pairs, 'duplicate source snapshot')
        pairs.add(pair)
        if pair == (HEAD, m['changed_paths']['memo']):
            final_memo = data.decode('utf-8')
        if args.verify_source_objects:
            actual = subprocess.check_output(['git', 'show', pair[0] + ':' + pair[1]], cwd=ROOT)
            need(actual == data, 'snapshot differs from actual source object')
    need(pairs == expected_pairs, 'snapshot set differs')
    need(final_memo is not None, 'final memo is missing')
    memo_bytes = final_memo.encode('utf-8')
    need({row['label'] for row in m['source_sections']} == {'SR', 'XF', 'SC', 'PB'},
         'source section set differs')
    for row in m['source_sections']:
        start, end = row['byte_start'], row['byte_end_exclusive']
        part = memo_bytes[start:end]
        need(part.startswith(row['heading'].encode('utf-8')) and sha(part) == row['sha256'] and
             memo_bytes[:start].count(b'\n') + 1 == row['line_start'], 'source section differs')
    p = m['patch']
    packed = (ROOT / p['path']).read_bytes()
    patch = lzma.decompress(packed)
    need(sha(packed) == p['compressed_sha256'] and sha(patch) == p['sha256'] and len(patch) == p['bytes'],
         'patch differs')
    for row in m['inputs']:
        data = (ROOT / row['path']).read_bytes()
        need(len(data) == row['bytes'] and sha(data) == row['sha256'] and blob(data) == row['git_blob'],
             'source input differs')
        if args.verify_source_objects:
            actual = subprocess.check_output(['git', 'show', HEAD + ':' + row['source_path']], cwd=ROOT)
            need(actual == data, 'input differs from actual source object')
    if args.verify_source_objects:
        refs = subprocess.check_output(['git', 'rev-list', '--reverse', BASE + '..' + HEAD], cwd=ROOT,
                                       text=True).splitlines()
        need(refs == COMMITS, 'commit range differs')
        changed = subprocess.check_output(['git', 'diff', '--no-ext-diff', '--name-only', BASE, HEAD],
                                          cwd=ROOT, text=True).splitlines()
        need(set(changed) == set(paths.values()), 'full changed path set differs')
        actual_patch = subprocess.check_output(['git', 'diff', '--no-ext-diff', '--binary', BASE, HEAD, '--',
                                                *(':(top)' + path for path in m['changed_paths'].values())], cwd=ROOT)
        need(actual_patch == patch, 'patch differs from actual source objects')
    pins = {'sr': ('<!-- SR-ORIGINAL-READER-CLOCK-CHECK:BEGIN -->',
                   '<!-- SR-ORIGINAL-READER-CLOCK-CHECK:END -->',
                   'b785b3f595ea130e6d0b4dc85a8dd09f4b989f59a549dae5aa806d2fd8219048', 59),
            'xf': ('<!-- XF-FULL-COMPARISON-CHECK:BEGIN -->',
                   '<!-- XF-FULL-COMPARISON-CHECK:END -->',
                   'a879ac7dabc3e3a9511796fa1771999100def36d59f383a7f6284ee67e8253d4', 61),
            'clock': ('#### 7fd.G1. check_clock_source.py', 'Observed normal and optimized receipt:',
                      'ac11be45b2cec5581abb05bd1de8973d4ea9d8283a1f31ddab1ea6b65fcf84e8', 8),
            'price': ('#### 7fe.G1. check_prepared_price.py', None,
                      'c34cd7740cba0cca4a3d67e6d8877fa4519cfc3886e45c85077fa86e43ed737f', 24)}
    need(final_memo is not None and set(m['checks']) == set(pins), 'missing checker inventory')
    receipt_pins = {'sr': '30a5c02c586b1d2d6fdd514a640ab2a996084a0025706fa8c5476055cda6cecc',
                    'xf': '2dba5bc0a7e4c5bc7d2e3de4bbc9a7574d6a1ec37d203580fecc326944182c16',
                    'clock': '438255ae32ea69621bda16b514e184dc173409c7228568c0fade4b0440a6fb18',
                    'price': 'db13c0b3acfd35c52340206abd00ffbe71161d4e1fc90941a1b10edf18364b2d'}
    for name, row in m['checks'].items():
        need(row['owner_receipt_sha256'] == receipt_pins[name], 'owner receipt pin differs')
        start, end, expected_sha, expected_count = pins[name]
        section = final_memo.split(start, 1)[1]
        if end is not None:
            section = section.split(end, 1)[0]
        match = re.search(r'^```python\r?\n(.*?)^```[ \t]*(?:\n|$)', section, re.S | re.M)
        need(match is not None, 'missing embedded checker')
        extracted = match.group(1).replace('\r\n', '\n').encode()
        need(sha(extracted) == expected_sha == row['sha256'] and row['checks'] == expected_count and
             extracted == (ROOT / 'checks' / (name + '.py')).read_bytes(),
             'checker differs from pinned embedded block')
        need(sha((ROOT / 'checks' / (name + '.py')).read_bytes()) == row['sha256'], 'checker differs')
        normal = (ROOT / 'results' / (name + '_normal.json')).read_bytes()
        optimized = (ROOT / 'results' / (name + '_optimized.json')).read_bytes()
        need(normal == optimized and sha(normal) == row['owner_receipt_sha256'], 'bounded receipt differs')
        for mode in ('normal', 'optimized'):
            need(not (ROOT / 'results' / (name + '_' + mode + '.stderr')).read_bytes(), 'bounded stderr not empty')
        result = json.loads(normal)
        count = result.get('number_of_checks', result.get('checks'))
        need(result['status'] == 'PASS' and count == row['checks'], 'bounded check count/status differs')
    for path, expected in m['supplementary_sha256'].items():
        need(sha((ROOT / path).read_bytes()) == expected, 'supplementary log differs')
    need(m['scientific_acceptance'] is False and m['GR_closed'] is False, 'scope changed')
    print(json.dumps({'status': 'PASS_PINNED_INTAKE', 'source_head': HEAD,
                      'source_objects_checked': args.verify_source_objects,
                      'snapshots': len(pairs), 'bounded_receipts_verified': 4,
                      'archived_code_executed': False, 'scientific_acceptance': False,
                      'GR_closed': False}, sort_keys=True))


if __name__ == '__main__':
    main()
