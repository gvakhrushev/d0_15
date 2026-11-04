#!/usr/bin/env python3
"""Verify pinned §7fl source and recorded outputs without executing owner code."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import subprocess

P = Path(__file__).resolve().parent
M = json.loads((P / 'MANIFEST.json').read_text())

def sha(data):
    return hashlib.sha256(data).hexdigest()

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def need(ok, message):
    if not ok:
        raise ValueError(message)

def git(*args):
    return subprocess.check_output(['git', '-C', str(P), *args])

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-source-objects', action='store_true')
    args = parser.parse_args()
    patch = lzma.decompress((P / 'complete_delta.patch.xz').read_bytes())
    need(sha(patch) == M['patch_sha256'], 'patch')
    need(len(M['changed_blobs']) == 2 and len(M['input_pins']) == 18, 'pin counts')
    memo = None
    for path, pins in M['changed_blobs'].items():
        raw = lzma.decompress((P / pins['snapshot']).read_bytes())
        need(blob(raw) == pins['head']['blob'] and sha(raw) == pins['head']['sha256'], 'snapshot: ' + path)
        if path.startswith('02_REGISTRY/'):
            memo = raw
    need(memo is not None, 'missing memo')
    a, b = M['owner_proof_range']
    proof = (P / 'proof_section.md').read_bytes()
    need(memo[a:b] == proof and sha(proof) == M['owner_proof_sha256'], 'proof')
    a, b = M['owner_receipt_range']
    receipt = (P / 'owner_receipt.json').read_bytes()
    need(memo[a:b] == receipt and sha(receipt) == M['owner_receipt_sha256'], 'owner receipt')
    owner = json.loads(receipt)
    need(owner['git_input'] == M['base'] and owner['proof_sha256'] == M['owner_proof_sha256'], 'owner pins')
    owner_checkers = {c['script']: c for c in owner['checkers']}
    need(set(owner_checkers) == set(M['checkers']), 'checker set')
    for name, pins in M['checkers'].items():
        a, b = pins['range']
        src = (P / name).read_bytes()
        need(memo[a:b] == src and sha(src) == pins['sha256'], 'checker: ' + name)
        meta = owner_checkers[name]
        need(meta['checker_sha256'] == pins['sha256'] and meta['check_count'] == pins['check_count'] and meta['normal_result_sha256'] == meta['optimized_result_sha256'] == pins['owner_stdout_sha256'], 'owner result pins: ' + name)
        reconstructed = (P / 'owner_reconstructed' / (name + '.json')).read_bytes()
        need(sha(reconstructed) == pins['owner_stdout_sha256'] and json.loads(reconstructed) == meta['result'], 'reconstructed owner JSON: ' + name)
        for mode in ('normal', 'optimized'):
            out = (P / 'results' / (name + '.' + mode + '.json')).read_bytes()
            err = (P / 'results' / (name + '.' + mode + '.stderr')).read_bytes()
            need(sha(out) == pins['owner_stdout_sha256'] and not err, 'local output: ' + name + ' ' + mode)
    if args.verify_source_objects:
        need(git('rev-parse', M['head'] + '^').decode().strip() == M['base'], 'source parent')
        need(git('diff', '--no-ext-diff', '--binary', '--full-index', M['base'], M['head'], '--') == patch, 'complete diff')
        names = git('diff', '--name-only', M['base'], M['head'], '--').decode().splitlines()
        need(set(names) == set(M['changed_blobs']), 'changed path set')
        for path, pins in M['changed_blobs'].items():
            for rev, role in ((M['base'], 'base'), (M['head'], 'head')):
                raw = git('show', rev + ':' + path)
                need(blob(raw) == pins[role]['blob'] and sha(raw) == pins[role]['sha256'], 'source blob: ' + path)
        for path, pins in M['input_pins'].items():
            raw = git('show', M['base'] + ':' + path)
            need(blob(raw) == pins['blob'] and sha(raw) == pins['sha256'], 'input: ' + path)
    print('PASS: snapshots, full patch, proof, owner receipt, both checker sources, reconstructed and local results' + (' and source Git objects' if args.verify_source_objects else ' (Git objects not checked)'))

if __name__ == '__main__':
    main()
