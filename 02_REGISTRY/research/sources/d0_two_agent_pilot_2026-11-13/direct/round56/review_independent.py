#!/usr/bin/env python3
"""Replay a pinned partner checker without changing partner artifacts."""
from pathlib import Path
from hashlib import sha256
from unittest.mock import patch
import contextlib
import io
import json
import runpy
import subprocess
import sys

sys.dont_write_bytecode = True
P = Path(__file__).resolve().parent
B = Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13')
O = B/'02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/open'


def replay(round_number, commit, checker, receipt):
    folder = O/f'round{round_number}'
    expected = folder/receipt
    files = sorted(p for p in folder.iterdir() if p.is_file())
    for p in files:
        blob = subprocess.check_output(['git', 'show', f'{commit}:{p.relative_to(B)}'], cwd=B)
        if blob != p.read_bytes():
            raise AssertionError(f'Git/disk mismatch: {p}')
    data = json.loads(expected.read_text())
    for name, digest in data['input_sha256'].items():
        assert sha256(Path(name).read_bytes()).hexdigest() == digest, name
    captured = {}

    def capture(path, text, *args, **kwargs):
        path = Path(path).resolve()
        if path != expected.resolve():
            raise AssertionError(f'Unexpected attempted write: {path}')
        captured[str(path)] = text.encode('utf-8')
        return len(text)

    with patch.object(Path, 'write_text', capture), contextlib.redirect_stdout(io.StringIO()):
        scope = runpy.run_path(str(folder/checker), run_name='__main__')
    assert captured == {str(expected.resolve()): expected.read_bytes()}
    return scope, {
        'status': f'PASS_ROOT_B{round_number}_PINNED_READ_ONLY_BYTE_IDENTICAL_REPLAY',
        'commit': commit,
        'all_Git_blobs_and_source_pins_verified': True,
        'owner_writes_suppressed': [receipt],
        'artifact_sha256': {p.name: sha256(p.read_bytes()).hexdigest() for p in files},
        'physical_C_closed': False, 'GR_closed': False}


if __name__ == '__main__':
    number, commit, checker, receipt = sys.argv[1:]
    _, result = replay(int(number), commit, checker, receipt)
    (P/f'ROOT_REVIEW_B{number}.json').write_text(json.dumps(result, indent=2)+'\n')
    print(result['status'])
