#!/usr/bin/env python3
"""Integrity and bounded replay of the new spatial/source application only."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


PACKET = Path(__file__).resolve().parent
ROOT = PACKET.parents[3]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(ok, label):
    if not ok:
        raise RuntimeError(label)


def git(*args):
    # The explicit flag avoids an unrelated common core.worktree audit setting.
    return subprocess.check_output(['/usr/bin/git', '--work-tree='+str(ROOT), *args], cwd=ROOT)


def integrity():
    manifest_path = PACKET/'MANIFEST.json'
    manifest = json.loads(manifest_path.read_text())
    for row in manifest['artifacts']:
        path = ROOT/row['path']
        require(path.is_file() and sha(path.read_bytes()) == row['sha256'], 'Changed artifact: '+row['path'])
    source_checks = 0
    runtime_input = '02_REGISTRY/research/sources/d0_native_gr_completion_synthesis_2026-10-20/geometric_source/inputs/literal_null_all40.py'
    runtime_verified = False
    for pinfile in [PACKET/'SOURCE_PINS.json', *sorted(PACKET.glob('*/SOURCE_PINS.json'))]:
        pins = json.loads(pinfile.read_text())
        revision = pins.get('repository_head') or pins.get('input_commit') or pins.get('head')
        require(bool(revision), 'Missing source revision: '+str(pinfile))
        for row in pins.get('sources', pins.get('files', [])):
            blob = git('rev-parse', revision+':'+row['path']).decode().strip()
            data = git('show', revision+':'+row['path'])
            require(blob == row['git_blob'] and sha(data) == row['sha256'], 'Changed source pin: '+row['path'])
            if row['path'] == runtime_input:
                require(sha((ROOT/runtime_input).read_bytes()) == row['sha256'], 'Runtime literal carrier changed')
                runtime_verified = True
            source_checks += 1
    require(runtime_verified, 'The runtime literal carrier is not pinned')
    return {'artifacts': len(manifest['artifacts']), 'source_pin_checks': source_checks,
            'runtime_literal_carrier_verified': True, 'manifest_sha256': sha(manifest_path.read_bytes())}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--integrity-only', action='store_true')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    result = {'status': 'PASS_SAME_EXECUTION_SPATIAL_SOURCE_INTEGRATION',
              'utc': datetime.now(timezone.utc).isoformat(), 'integrity': integrity(), 'runs': []}
    entries = [('weights/check_same_execution_spatial_weights.py', []),
               ('geometry/check_spatial_source.py', ['--repo', str(ROOT)]),
               ('check_n1_entropy_adjoint.py', [])]
    if not args.integrity_only:
        for rel, extra in entries:
            script = PACKET/rel
            start = time.perf_counter()
            run = subprocess.run([sys.executable, str(script), *extra], cwd=ROOT,
                                 capture_output=True, text=True)
            require(run.returncode == 0, 'Failed calculation: '+rel+'\n'+run.stdout+run.stderr)
            require(not run.stderr.strip(), 'Unexpected diagnostic: '+run.stderr)
            output = json.loads(run.stdout)
            require(str(output.get('status', '')).startswith('PASS'), 'No PASS result: '+rel)
            result['runs'].append({'entrypoint': rel, 'checker_sha256': sha(script.read_bytes()),
                                   'elapsed_seconds': time.perf_counter()-start, 'result': output})
    payload = json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        args.output.write_text(payload)
        print(json.dumps({'status': result['status'], 'output': str(args.output),
                          'runs': len(result['runs']), 'integrity': result['integrity']}))
    else:
        print(payload, end='')


if __name__ == '__main__':
    main()
