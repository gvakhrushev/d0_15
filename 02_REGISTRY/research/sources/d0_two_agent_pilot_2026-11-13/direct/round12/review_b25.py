#!/usr/bin/env python3
"""Replay B25 in isolation, pin provenance, and review B26 receipt inputs.

This checks target matrices and exact selector evidence, not native gates.
Only this directory and temporary copies are written.
"""
from pathlib import Path
from tempfile import TemporaryDirectory
import hashlib
import json
import os
import shutil
import subprocess
import sys

P = Path(__file__).resolve().parent
B = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def verify_outputs(folder, receipt):
    for name, expected in receipt['output_sha256'].items():
        assert sha(folder / name) == expected, (folder, name)

receipt = json.loads((B/'round25/RECEIPT.json').read_text())
verified_inputs = {}
for origin, files in receipt['input_sha256'].items():
    source = P.parent/'round11' if origin == 'A11' else B/origin
    for name, expected in files.items():
        assert sha(source/name) == expected, (origin, name)
        verified_inputs[origin+'/'+name] = expected
verify_outputs(B/'round25', receipt)

scripts = [
    ('check_targets.py', ['CENTRE_JULIA32_TARGETS.npz', 'CENTRE_FIELDS.npz', 'TARGET_CHECK.json']),
    ('check_raw_frame.py', ['RAW_FRAME_CHECK.json']),
    ('certify_reference_slack.py', ['STRICT_SLACK.json']),
    ('build_mark_catalogue.py', ['COPY_SLOTS.jsonl', 'SOURCE_LEAF_BINDING.json', 'MARK_OUTPUT_CATALOG.json']),
    ('check_bound_leaves.py', ['BOUND_LEAF_CHECK.json']),
]
comparisons = {}
with TemporaryDirectory(prefix='d0_a12_review_b25_') as temporary:
    root = Path(temporary)
    for dirname in ('round21', 'round23', 'round24', 'round25'):
        shutil.copytree(B/dirname, root/dirname, ignore=shutil.ignore_patterns('__pycache__'))
    env = dict(os.environ, OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', PYTHONDONTWRITEBYTECODE='1')
    for script, generated in scripts:
        result = subprocess.run([sys.executable, '-B', '-W', 'error', str(root/'round25'/script)], env=env, text=True, capture_output=True)
        assert result.returncode == 0, (script, result.stdout, result.stderr)
        assert not result.stderr, (script, result.stderr)
        for name in generated:
            a = sha(root/'round25'/name)
            b = sha(B/'round25'/name)
            assert a == b, (script, name, a, b)
            comparisons[name] = a
        print(script, 'PASS', len(generated), 'byte-identical outputs', flush=True)

review26 = json.loads((B/'round26/RECEIPT.json').read_text())
for rel, expected in review26['input_sha256'].items():
    assert sha(P.parent/rel) == expected, rel
verify_outputs(B/'round26', review26)

result = {
    'status': 'PASS_ISOLATED_B25_TARGET_REPLAY_AND_B26_INPUT_BINDING',
    'B25_input_sha256': verified_inputs,
    'B25_output_sha256': receipt['output_sha256'],
    'B25_receipt_sha256': sha(B/'round25/RECEIPT.json'),
    'B25_replayed_scripts': [x[0] for x in scripts],
    'B25_byte_identical_regenerated_files': comparisons,
    'B26_receipt_sha256': sha(B/'round26/RECEIPT.json'),
    'B26_verified_input_sha256': review26['input_sha256'],
    'B26_verified_output_sha256': review26['output_sha256'],
    'B26_exact_checker_rerun_by_root': False,
    'review_scope': 'B25 full target diagnostics and binding; B26 receipt/content review, no duplicate independent checker run',
    'native_words_executed': False,
    'full_READY_proved': False,
    'physical_C_closed': False,
    'GR_closed': False,
}
(P/'ROOT_REVIEW_B25_B26.json').write_text(json.dumps(result, indent=2)+'\n')
print(result['status'], flush=True)
