#!/usr/bin/env python3
"""Verify the pinned 7ff source/diff and recorded bounded control; execute no owner code."""
from __future__ import annotations
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent
BASE = '2900145fe674629b61949587917a3a2ea5188797'
HEAD = '567e3806c58861eeebadf57ae34e8c4b2142141a'
PATHS = {'task': '00_WORK/tasks/EXP-A4D-JOINT-RESPONSE-DECOUPLING-MICROSTRUCTURE.md',
         'memo': '02_REGISTRY/research/A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md'}
CHECKER = '9d7e7cdd2e6bd02a070a4327e556b513618f51c756fd46fa1b572b4a883968fe'
OUTPUT = '9c475bad9680141457ca6c4a519e02716ea1072aac3486cd0c4e6929145c3881'


def need(ok: bool, message: str) -> None:
    if not ok:
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
    need(m['base'] == BASE and m['head'] == HEAD and m['changed_paths'] == PATHS, 'bad owner pins')
    need(m['checker_sha256'] == CHECKER and m['output_sha256'] == OUTPUT and m['checks'] == 42,
         'bad checker or receipt pins')
    expected = {(ref, path) for ref in (BASE, HEAD) for path in PATHS.values()}
    seen = set()
    final_memo = None
    for row in m['snapshots']:
        pair = (row['commit'], row['source_path'])
        need(pair not in seen, 'duplicate snapshot')
        seen.add(pair)
        packed = (ROOT / (row['snapshot'] if pair[0] == HEAD else row['previous_snapshot'])).read_bytes()
        if pair[0] == HEAD:
            need(sha(packed) == row['snapshot_sha256'], 'compressed snapshot differs')
        data = lzma.decompress(packed)
        need(len(data) == row['bytes'] and sha(data) == row['sha256'] and blob(data) == row['git_blob'],
             'source snapshot differs')
        if pair == (HEAD, PATHS['memo']):
            final_memo = data
        if args.verify_source_objects:
            actual = subprocess.check_output(['git', 'show', pair[0] + ':' + pair[1]], cwd=ROOT)
            need(data == actual, 'source object differs')
    need(seen == expected and final_memo is not None, 'incomplete snapshot set')
    sec = m['source_section']; start = sec['byte_start']; end = sec['byte_end_exclusive']
    need(final_memo[start:end].startswith(b'## 7ff. Same-history quadratic memory source:') and
         sha(final_memo[start:end]) == sec['sha256'] and
         final_memo[:start].count(b'\n') + 1 == sec['line_start'], '7ff section differs')
    owner_bytes = (ROOT / 'owner_receipt.json').read_bytes()
    owner_section = final_memo.decode('utf-8').split('### 7ff.G. Exact bounded check and reviewed input snapshot', 1)[1].split('#### 7ff.G1.', 1)[0]
    owner_block = re.search(r'^```json\r?\n(.*?)^```[ \t]*(?:\n|$)', owner_section, re.S | re.M)
    need(owner_block is not None and owner_block.group(1).replace('\r\n', '\n').encode() == owner_bytes,
         'owner receipt is not the pinned source block')
    owner = json.loads(owner_bytes)
    need(sha((ROOT / 'owner_receipt.json').read_bytes()) == m['owner_receipt_sha256'] and
         owner['input_head'] == BASE and owner['checker_sha256'] == CHECKER and
         owner['normal_optimized_receipt_sha256'] == OUTPUT and owner['new_exact_checks'] == 42 and
         owner['scientific_promotion'] is False and owner['GR_closed'] is False,
         'owner receipt differs')
    text = final_memo.decode('utf-8').split('#### 7ff.G1. check_virtual_source.py', 1)[1]
    match = re.search(r'^```python\r?\n(.*?)^```[ \t]*(?:\n|$)', text, re.S | re.M)
    need(match is not None, 'embedded checker missing')
    code = match.group(1).replace('\r\n', '\n').encode()
    need(sha(code) == CHECKER and code == (ROOT / 'check_virtual_source.py').read_bytes(),
         'checker is not the pinned source block')
    normal = (ROOT / 'results/normal.json').read_bytes()
    optimized = (ROOT / 'results/optimized.json').read_bytes()
    need(normal == optimized and sha(normal) == OUTPUT, 'bounded output differs')
    result = json.loads(normal)
    need(result['status'] == 'PASS' and result['number_of_checks'] == 42 and
         'same initial-cut quadratic response loses every field cross term' in result['checks'],
         'bounded negative control missing')
    for mode in ('normal', 'optimized'):
        need(not (ROOT / 'results' / (mode + '.stderr')).read_bytes(), 'unexpected checker stderr')
    patch = m['patch']; packed = (ROOT / patch['path']).read_bytes(); data = lzma.decompress(packed)
    need(sha(packed) == patch['compressed_sha256'] and len(data) == patch['bytes'] and
         sha(data) == patch['sha256'], 'patch differs')
    need(len(m['owner_inputs']) == 12 and
         {r['source_path']:r['sha256'] for r in m['owner_inputs']} == owner['owner_sha256'],
         'owner input pin set differs')
    if args.verify_source_objects:
        parent = subprocess.check_output(['git', 'show', '-s', '--format=%P', HEAD], cwd=ROOT, text=True).strip()
        need(parent == BASE, 'commit is not a direct child of base')
        changed = subprocess.check_output(['git', 'diff', '--no-ext-diff', '--name-only', BASE, HEAD],
                                          cwd=ROOT, text=True).splitlines()
        need(set(changed) == set(PATHS.values()), 'full changed paths differ')
        actual_patch = subprocess.check_output(['git', 'diff', '--no-ext-diff', '--binary', BASE, HEAD, '--',
                                                *(':(top)' + p for p in PATHS.values())], cwd=ROOT)
        need(data == actual_patch, 'full patch differs from source')
        for row in m['owner_inputs']:
            actual = subprocess.check_output(['git', 'show', BASE + ':' + row['source_path']], cwd=ROOT)
            need(row['commit'] == BASE and len(actual) == row['bytes'] and
                 blob(actual) == row['git_blob'] and sha(actual) == row['sha256'], 'owner input differs')
    need(m['scientific_promotion'] is False and m['GR_closed'] is False, 'scope changed')
    print(json.dumps({'status':'PASS_PINNED_7FF', 'source_head':HEAD,
                      'source_objects_checked':args.verify_source_objects,
                      'source_files':2, 'owner_input_pins':len(m['owner_inputs']),
                      'checker_executed':False, 'bounded_receipt_checks':42,
                      'scientific_promotion':False, 'GR_closed':False}, sort_keys=True))


if __name__ == '__main__':
    main()
