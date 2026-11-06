#!/usr/bin/env python3
"""Replay owner code in the current Python/SymPy; do not modify receipts."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

here = Path(__file__).resolve().parent
manifest = json.loads((here / 'MANIFEST.json').read_text())
checker = here / 'check_return_source.py'
if hashlib.sha256(checker.read_bytes()).hexdigest() != manifest['checker_sha256']:
    raise ValueError('checker digest mismatch')
for flags in (['-Werror'], ['-O', '-Werror']):
    run = subprocess.run([sys.executable, *flags, str(checker)], capture_output=True, check=True)
    if run.stderr:
        raise ValueError('checker wrote stderr: ' + run.stderr.decode(errors='replace'))
    if hashlib.sha256(run.stdout).hexdigest() != manifest['owner_expected_stdout_sha256']:
        raise ValueError('checker receipt mismatch')
    print('PASS', ' '.join(flags), '58 owner conditions; receipt matches')
