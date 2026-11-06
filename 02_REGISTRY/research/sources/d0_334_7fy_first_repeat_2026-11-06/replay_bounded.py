#!/usr/bin/env python3
"""Extract and replay the pinned owner checks in /tmp; this is not a sandbox."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
import verify_intake as verify

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--verify-source-objects', action='store_true')
    args = parser.parse_args()
    scripts, native, diff = verify.verify_local()
    if args.verify_source_objects:
        verify.verify_git((verify.P / 'owner_7fy.md').read_bytes(), native, diff)
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', OPENBLAS_NUM_THREADS='1', OMP_NUM_THREADS='1', MKL_NUM_THREADS='1')
    results = {}
    with tempfile.TemporaryDirectory(prefix='d0-7fy-replay-', dir='/tmp') as temp:
        root = Path(temp)
        native_path = root / verify.M['native_input']['path']
        native_path.parent.mkdir(parents=True)
        native_path.write_bytes(native)
        for name, source in scripts.items():
            script = root / name
            script.write_bytes(source)
            outputs = []
            for mode, flags in (('normal', []), ('optimized', ['-O'])):
                verify.need(verify.sha(script.read_bytes()) == verify.M['checkers'][name]['source_sha256'], 'checker before execution: ' + name)
                verify.need(verify.sha(native_path.read_bytes()) == verify.M['native_input']['sha256'], 'native input before execution')
                proc = subprocess.run([sys.executable, *flags, '-B', '-Werror', str(script)], cwd=root, env=env, capture_output=True)
                verify.need(proc.returncode == 0 and not proc.stderr, 'execution failed: ' + name + ' ' + mode + ' ' + repr(proc.stderr))
                digest = verify.sha(proc.stdout)
                verify.need(digest == verify.M['checkers'][name]['output_sha256'], 'stdout mismatch: ' + name + ' ' + mode)
                outputs.append(proc.stdout)
                results[name + ':' + mode] = {'exit_code': proc.returncode, 'stderr_bytes':len(proc.stderr), 'stdout_sha256':digest}
            verify.need(outputs[0] == outputs[1], 'normal/optimized mismatch: ' + name)
    print(json.dumps({'status':'PASS', 'runs':results, 'boundary':'finite replay; same owner programs; no physical or GR acceptance'}, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
