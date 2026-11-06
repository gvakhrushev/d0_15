#!/usr/bin/env python3
"""Check §7fy retained bytes; optionally verify exact Git provenance."""
import argparse
import hashlib
import json
import lzma
from pathlib import Path
import re
import subprocess

P = Path(__file__).resolve().parent
M = json.loads((P / 'MANIFEST.json').read_text())
NAMES = {'check_serializer.py', 'check_guard.py', 'check_collision.py', 'check_marked_cost.py', 'check_collision_transfer.py'}

def sha(data):
    return hashlib.sha256(data).hexdigest()

def need(ok, why):
    if not ok:
        raise ValueError(why)

def blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()

def git(*args):
    return subprocess.check_output(['git', '-C', str(P), *args])

def verify_local():
    need(M['schema'] == 'd0-334-7fy-first-repeat-intake-v1' and M['GR_closed'] is False and M['scientific_promotion'] is False, 'scope')
    need(set(M['checkers']) == NAMES, 'checker names')
    sec = (P / 'owner_7fy.md').read_bytes()
    need(sha(sec) == M['owner_section_sha256'], 'owner section')
    need(sha((P / 'HANDOFF_RU.md').read_bytes()) == M['handoff_sha256'], 'handoff')
    raw = (P / 'independent_replay.json').read_bytes()
    need(sha(raw) == M['independent_replay_sha256'], 'replay metadata')
    replay = json.loads(raw)
    need(set(replay) == NAMES, 'replay checker set')
    native = (P / 'inputs/native_execution.py').read_bytes()
    need(len(native) == M['native_input']['bytes'] and sha(native) == M['native_input']['sha256'] and blob(native) == M['native_input']['blob'], 'native input')
    packed = (P / 'complete_delta.patch.xz').read_bytes()
    need(sha(packed) == M['complete_diff_xz_sha256'], 'compressed diff')
    diff = lzma.decompress(packed)
    need(sha(diff) == M['complete_diff_sha256'], 'full diff')
    parsed = {}
    pattern = rb'<summary>([^<]+)</summary>.*?Source SHA256 ([a-f0-9]{64})\. Output SHA256 ([a-f0-9]{64})\..*?```python\n(.*?)```'
    for match in re.finditer(pattern, sec, re.S):
        name = match.group(1).decode()
        need(name not in parsed and name in NAMES, 'unexpected checker block')
        pins = M['checkers'][name]
        a, b = pins['range_in_section']
        source = match.group(4)
        need([match.start(4), match.end(4)] == [a, b] and sec[a:b] == source and sha(source) == pins['source_sha256'] == match.group(2).decode(), 'source block: ' + name)
        need(pins['output_sha256'] == match.group(3).decode(), 'owner output pin: ' + name)
        output = (P / 'results' / (name + '.stdout')).read_bytes()
        need(sha(output) == pins['output_sha256'], 'saved stdout: ' + name)
        for mode in ('normal', 'optimized'):
            entry = replay[name][mode]
            need(entry['exit_code'] == 0 and entry['stderr_bytes'] == 0 and entry['stdout_matches_owner'] is True and entry['stdout_sha256'] == pins['output_sha256'], 'independent run: ' + name + ' ' + mode)
        parsed[name] = source
    need(set(parsed) == NAMES, 'checker extraction set')
    return parsed, native, diff

def verify_git(sec, native, diff):
    base, head = M['owner_base'], M['owner_head']
    need(git('rev-parse', head + '^').decode().strip() == base, 'owner parent')
    need(git('diff', '--no-ext-diff', '--binary', '--full-index', base, head, '--') == diff, 'full Git diff')
    changed = git('diff', '--name-only', base, head, '--').decode().splitlines()
    need(set(changed) == set(M['owner_paths']), 'changed owner path set')
    for path, pins in M['owner_paths'].items():
        for rev, role in ((base, 'base'), (head, 'head')):
            content = git('show', rev + ':' + path)
            pin = pins[role]
            need(len(content) == pin['bytes'] and sha(content) == pin['sha256'] and blob(content) == pin['blob'], 'Git blob ' + role + ': ' + path)
            if role == 'head' and path.startswith('02_REGISTRY/'):
                a, b = M['owner_section_range']
                need(content[a:b] == sec, 'owner section Git binding')
    need(git('show', head + ':' + M['native_input']['path']) == native, 'native Git input')
    for name, pins in M['checkers'].items():
        a, b = pins['range_in_owner']
        x, y = pins['range_in_section']
        need([a, b] == [M['owner_section_range'][0] + x, M['owner_section_range'][0] + y], 'absolute source range: ' + name)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-source-objects', action='store_true')
    args = parser.parse_args()
    _, native, diff = verify_local()
    if args.verify_source_objects:
        verify_git((P / 'owner_7fy.md').read_bytes(), native, diff)
    print('PASS: pinned section, five embedded checkers, native input, replay outputs, complete delta' + (' and original Git objects' if args.verify_source_objects else ' (Git origin not checked)'))
    print('Finite replay only; no physical or GR acceptance.')

if __name__ == '__main__':
    main()
