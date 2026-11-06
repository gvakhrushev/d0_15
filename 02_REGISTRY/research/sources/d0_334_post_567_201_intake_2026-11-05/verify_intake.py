#!/usr/bin/env python3
"""Check pinned #334 §7fg packet without executing the owner checker."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]

def digest(data):
    return hashlib.sha256(data).hexdigest()

def require(condition, message):
    if not condition:
        raise ValueError(message)

def git(*args):
    return subprocess.check_output(['git', *args], cwd=REPO)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-source-objects', action='store_true')
    args = parser.parse_args()
    manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    receipt_bytes = (HERE / 'owner_receipt.json').read_bytes()
    receipt = json.loads(receipt_bytes)
    require(digest(receipt_bytes) == manifest['owner_receipt_sha256'], 'receipt hash')
    require(receipt['owner_sha256'] == {path: meta['sha256'] for path, meta in manifest['owner_inputs'].items()}, 'input pins')
    require(receipt['input_head'] == manifest['base'], 'input head')
    require(receipt['checker_sha256'] == manifest['checker_sha256'], 'receipt checker')
    require(receipt['normal_optimized_receipt_sha256'] == manifest['owner_expected_stdout_sha256'], 'owner stdout')
    patch = lzma.decompress((HERE / 'complete_delta.patch.xz').read_bytes())
    require(digest(patch) == manifest['patch_sha256'], 'patch hash')
    for path, info in manifest['changed_blobs'].items():
        data = lzma.decompress((HERE / info['snapshot']).read_bytes())
        require(digest(data) == info['head_sha256'], 'snapshot '+path)
        if '/research/A4D_NONVACUUM_' in path:
            marker = b'#### 7fg.G1. check_return_source.py\n\n```python\n'
            require(data.count(marker) == 1, 'checker marker')
            checker = data.split(marker, 1)[1].split(b'```', 1)[0]
            require(checker == (HERE / 'check_return_source.py').read_bytes(), 'extracted checker')
    require(digest((HERE / 'check_return_source.py').read_bytes()) == manifest['checker_sha256'], 'checker hash')
    for version in ('312', '39'):
        for mode in ('normal', 'optimized'):
            output = (HERE / 'results' / ('python'+version+'-'+mode+'.json')).read_bytes()
            stderr = (HERE / 'results' / ('python'+version+'-'+mode+'.stderr')).read_bytes()
            require(digest(output) == manifest['owner_expected_stdout_sha256'], 'replay receipt')
            require(not stderr, 'replay stderr')
            parsed = json.loads(output)
            require(parsed['number_of_checks'] == 58 and len(parsed['checks']) == 58, 'check count')
    if args.verify_source_objects:
        base, head = manifest['base'], manifest['head']
        require(git('rev-parse', head+'^').decode().strip() == base, 'commit parent')
        require(git('diff', '--binary', base, head, '--') == patch, 'git diff')
        for path, info in manifest['changed_blobs'].items():
            for ref, prefix in ((base, 'base'), (head, 'head')):
                require(git('rev-parse', ref+':'+path).decode().strip() == info[prefix+'_blob'], 'blob '+path)
                require(digest(git('show', ref+':'+path)) == info[prefix+'_sha256'], 'sha '+path)
        for path, info in manifest['owner_inputs'].items():
            require(git('rev-parse', base+':'+path).decode().strip() == info['blob'], 'input blob '+path)
            require(digest(git('show', base+':'+path)) == info['sha256'], 'input sha '+path)
    print('PASS: §7fg stored bytes and receipts' + (' and source Git objects' if args.verify_source_objects else ''))

if __name__ == '__main__':
    main()
