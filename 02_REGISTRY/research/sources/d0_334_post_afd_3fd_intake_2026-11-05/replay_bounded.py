#!/usr/bin/env python3
"""Re-run the hash-checked owner code, not a sandbox and not independent science."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

P=Path(__file__).resolve().parent
M=json.loads((P/'MANIFEST.json').read_text())

def digest(b):return hashlib.sha256(b).hexdigest()

def main():
    env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
    outputs=[]
    for flags in ([],['-O']):
        checker=P/'check_retention_collar.py'
        if digest(checker.read_bytes()) != M['checker_sha256']:
            raise ValueError('checker source mismatch')
        run=subprocess.run([sys.executable,*flags,'-Werror',str(checker)],capture_output=True,env=env)
        if run.returncode:
            sys.stderr.buffer.write(run.stderr)
            raise SystemExit(run.returncode)
        if run.stderr:
            raise ValueError('checker produced stderr')
        result=json.loads(run.stdout)
        if result['status']!='PASS' or result['check_count']!=M['owner_reported_check_count'] or result['classifications']!=M['owner_reported_check_counts']:
            raise ValueError('check classification mismatch')
        outputs.append(run.stdout)
        print('mode','optimized' if flags else 'normal','sha256',digest(run.stdout),'runtime',result['runtime'],'stderr bytes',len(run.stderr))
    if outputs[0]!=outputs[1]:
        raise ValueError('normal and optimized receipts differ')
    print('PASS: bounded q=0 fixture; 5 floating controls remain nominal')

if __name__=='__main__':
    main()
