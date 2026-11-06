#!/usr/bin/env python3
"""Verify the pinned §7fj packet, without executing the embedded owner code."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess

P = Path(__file__).resolve().parent
M = json.loads((P / 'MANIFEST.json').read_text())

def need(ok, why):
    if not ok:
        raise ValueError(why)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', '-C', str(P), *args])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verify-source-objects', action='store_true')
    args = ap.parse_args()
    patch = lzma.decompress((P / 'complete_delta.patch.xz').read_bytes())
    need(sha(patch) == M['patch_sha256'], 'complete diff hash')
    for path, info in M['changed_blobs'].items():
        raw = lzma.decompress((P / info['snapshot']).read_bytes())
        need(blob(raw) == info['head_blob'] and sha(raw) == info['head_sha256'], 'owner snapshot: ' + path)
    memo_path = next(x for x in M['changed_blobs'] if x.startswith('02_REGISTRY/'))
    memo = lzma.decompress((P / M['changed_blobs'][memo_path]['snapshot']).read_bytes()).decode()
    section = '## 7fj. ' + memo.split('## 7fj. ', 1)[1].split('\n## 7', 1)[0]
    fences = re.findall(r'^```(\w+)\n(.*?)^```[ \t]*$', section, re.S | re.M)
    checker = (P / 'check_clock_price.py').read_bytes()
    receipt = (P / 'owner_receipt.json').read_bytes()
    py = [x[1].encode() for x in fences if x[0] == 'python']
    js = [x[1].encode() for x in fences if x[0] == 'json']
    need(len(py) == 1 and py[0] == checker and sha(checker) == M['checker_sha256'], 'checker bytes')
    need(len(js) == 2 and js[1] == receipt and sha(receipt) == M['owner_receipt_sha256'], 'owner receipt')
    meta = json.loads(js[0])
    need(meta['input_head'] == M['base'] and meta['checker_sha256'] == M['checker_sha256'], 'owner metadata')
    need(meta['predecessor_checker_sha256'] == M['predecessor_checker_sha256'], 'predecessor metadata')
    need(len(M['owner_inputs']) == 17 and meta['owner_sha256'] == {p: v['sha256'] for p, v in M['owner_inputs'].items()}, 'owner input set')
    previous = memo.split('#### 7fh.G1. check_transport.py\n\n```python\n', 1)[1].split('```', 1)[0].encode()
    need(previous == (P / 'predecessor_check_transport.py').read_bytes() and sha(previous) == M['predecessor_checker_sha256'], 'predecessor bytes')
    original = (P / 'original_uniform_source.py').read_bytes()
    need(sha(original) == M['original_constructor_sha256'] and blob(original) == M['original_constructor_blob'], 'constructor bytes')
    comparison_bytes = (P / 'results/comparison.json').read_bytes()
    need(sha(comparison_bytes) == M['comparison_sha256'], 'comparison bytes')
    comp = json.loads(comparison_bytes)
    for name, info in comp['files'].items():
        data = (P / 'results' / name).read_bytes()
        need(len(data) == info['bytes'] and sha(data) == info['sha256'], 'replay file: ' + name)
    normal = (P / 'results/python312_normal.json').read_bytes()
    optimized = (P / 'results/python312_optimized.json').read_bytes()
    need(normal == optimized and not (P / 'results/python312_normal.stderr').read_bytes() and
         not (P / 'results/python312_optimized.stderr').read_bytes(), 'local normal/optimized output')
    result = json.loads(normal)
    owner = json.loads(receipt)
    need(result['check_count'] == 90 and result['classifications'] == M['owner_counts'] and
         result['checks'] == owner['checks'], 'observed labels and check counts')
    if args.verify_source_objects:
        need(git('rev-parse', M['head'] + '^').decode().strip() == M['base'], 'parent commit')
        need(git('diff', '--no-ext-diff', '--binary', '--full-index', M['base'], M['head'], '--') == patch, 'Git diff')
        for path, info in M['changed_blobs'].items():
            for ref, tag in ((M['base'], 'base'), (M['head'], 'head')):
                data = git('show', ref + ':' + path)
                need(blob(data) == info[tag + '_blob'] and sha(data) == info[tag + '_sha256'], 'source blob: ' + path)
        for path, info in M['owner_inputs'].items():
            data = git('show', M['base'] + ':' + path)
            need(blob(data) == info['blob'] and sha(data) == info['sha256'], 'input pin: ' + path)
    print('PASS: §7fj stored bytes, bounded receipts' + (' and source Git objects' if args.verify_source_objects else ' (Git objects not checked)'))

if __name__ == '__main__':
    main()
