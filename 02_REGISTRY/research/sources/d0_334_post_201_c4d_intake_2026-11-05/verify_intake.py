#!/usr/bin/env python3
"""Verify preserved bytes; optional Git-object provenance, no owner code execution."""
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

def sha(b):
    return hashlib.sha256(b).hexdigest()

def blob(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def git(*args):
    return subprocess.check_output(['git', '-C', str(P), *args])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--verify-source-objects', action='store_true')
    args = ap.parse_args()
    patch = lzma.decompress((P / 'complete_delta.patch.xz').read_bytes())
    need(sha(patch) == M['patch_sha256'], 'patch mismatch')
    for path, pins in M['changed_blobs'].items():
        raw = lzma.decompress((P / pins['snapshot']).read_bytes())
        need(blob(raw) == pins['head_blob'] and sha(raw) == pins['head_sha256'], 'snapshot mismatch: ' + path)
    checker = (P / 'check_transport.py').read_bytes()
    receipt = (P / 'owner_receipt.json').read_bytes()
    constructor = (P / 'original_uniform_source.py').read_bytes()
    need(sha(checker) == M['checker_sha256'], 'checker mismatch')
    need(sha(receipt) == M['owner_receipt_sha256'] == M['owner_expected_stdout_sha256'], 'owner receipt mismatch')
    need(sha(constructor) == M['original_uniform_source_sha256'] and blob(constructor) == M['original_uniform_source_blob'], 'constructor mismatch')
    memo_path = next(x for x in M['changed_blobs'] if x.startswith('02_REGISTRY/'))
    memo = lzma.decompress((P / M['changed_blobs'][memo_path]['snapshot']).read_bytes()).decode()
    section = '## 7fh. ' + memo.split('## 7fh. ', 1)[1].split('\n## 7', 1)[0]
    fences = re.findall(r'```(\w+)\n(.*?)```', section, re.S)
    need([x[1].encode() for x in fences if x[0] == 'python'] == [checker], 'checker differs from source')
    js = [x[1].encode() for x in fences if x[0] == 'json']
    need(len(js) == 2 and js[1] == receipt, 'owner receipt differs from source')
    owner_meta = json.loads(js[0])
    need(len(M['owner_inputs']) == 22 and owner_meta['owner_sha256'] == {p: v['sha256'] for p, v in M['owner_inputs'].items()}, 'input set differs from source')
    if args.verify_source_objects:
        need(git('rev-parse', M['head'] + '^').decode().strip() == M['base'], 'parent mismatch')
        need(git('diff', '--no-ext-diff', '--binary', '--full-index', M['base'], M['head'], '--') == patch, 'full diff mismatch')
        for path, pins in M['changed_blobs'].items():
            for rev, prefix in ((M['base'], 'base'), (M['head'], 'head')):
                raw = git('show', rev + ':' + path)
                need(blob(raw) == pins[prefix + '_blob'] and sha(raw) == pins[prefix + '_sha256'], 'source blob mismatch: ' + path)
        for path, pins in M['owner_inputs'].items():
            raw = git('show', M['base'] + ':' + path)
            need(blob(raw) == pins['blob'] and sha(raw) == pins['sha256'], 'input mismatch: ' + path)
    print('PASS: source bundle, checker, receipt, constructor, 22 inputs' + (' and Git objects' if args.verify_source_objects else ' (Git inputs not checked)'))

if __name__ == '__main__':
    main()
