#!/usr/bin/env python3
"""Verify two restored payloads against the separate readable intake."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

repo = Path.cwd()
source = repo / '02_REGISTRY/research/sources/d0_chat_snapshot_2026-10-27/restore.py'
intake = repo / '02_REGISTRY/research/sources/d0_chat_intake_2026-10-28/packages'

def inventory(root):
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}

with tempfile.TemporaryDirectory(prefix='d0-snapshot-comparison-') as tmp:
    roots = [Path(tmp) / 'normal', Path(tmp) / 'optimized']
    outputs = []
    for flags, root in [([], roots[0]), (['-O'], roots[1])]:
        run = subprocess.run([sys.executable, *flags, str(source), '--extract', str(root)],
                             capture_output=True, text=True, check=True)
        if run.stderr:
            raise ValueError('Unexpected archive verifier stderr: ' + run.stderr)
        outputs.append(json.loads(run.stdout))
    expected = {'status': 'PASS_ARCHIVE_INTEGRITY', 'files': 74, 'bytes': 650121,
                'mathematical_tests_executed': False}
    if outputs != [expected, expected]:
        raise ValueError('Unexpected archive verification result')
    normal, optimized = (inventory(root / 'packages') for root in roots)
    if len(normal) != 74 or normal != optimized or normal != inventory(intake):
        raise ValueError('Restored members differ from readable intake')
    print(json.dumps({'status': 'PASS_SNAPSHOT_VS_INTAKE', 'members': len(normal),
                      'bytes': expected['bytes'], 'modes': ['normal', 'optimized'],
                      'mathematical_tests_executed': False,
                      'original_zip_bytes_independently_verified': False}, sort_keys=True))
