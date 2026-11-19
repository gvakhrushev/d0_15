#!/usr/bin/env python3
"""Read-only mathematical replay plus explicit rejected semantic variants."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import numpy,scipy,sympy,mpmath

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    root=Path(__file__).resolve().parent
    expected=(root/'RESULT.json').read_bytes()
    before={p.name:digest(p) for p in root.iterdir() if p.is_file() and p.suffix in ('.py','.md','.json') and p.name!='VALIDATION.json'}
    env=os.environ.copy();env.update(OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',PYTHONHASHSEED='0')
    replays=[]
    for optimized in (False,True):
        cmd=[sys.executable]+(['-O'] if optimized else [])+[str(root/'check_two_clocks.py')]
        p=subprocess.run(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=180)
        if p.returncode:raise RuntimeError(p.stderr.decode())
        if p.stdout!=expected:raise ArithmeticError('frozen expected output mismatch in '+str(cmd))
        data=json.loads(p.stdout)
        replays.append({'mode':'optimized' if optimized else 'normal','status':data['status'],
                        'checks':data['check_count'],'stdout_sha256':hashlib.sha256(p.stdout).hexdigest()})
    variants={
       'omit_port_source':'paid source includes mandatory actual surplus-cost derivative',
       'replace_by_equilibrium':'mixing and physical refinement cannot be interchanged',
       'freeze_information_cut':'retained-reference information cut keeps its true field source',
       'short_clock':'old h^-2 physical clock cannot replace h^-4'}
    rejected=[]
    for name,label in variants.items():
        p=subprocess.run([sys.executable,'-O',str(root/'check_two_clocks.py'),'--mutation',name],
                         stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=180)
        if not p.returncode or label not in p.stderr.decode():
            raise ArithmeticError('mutation was not rejected by its intended check: '+name+'\n'+p.stderr.decode())
        rejected.append({'mutation':name,'rejected':True,'decisive_check':label})
    after={name:digest(root/name) for name in before}
    if before!=after:raise ArithmeticError('tracked scientific inputs mutated')
    result={'status':'PASS','replays':replays,'normal_and_optimized_byte_identical':True,
            'read_only_expected_outputs':True,'mutations':rejected,'sha256':before,
            'environment':{'python':sys.version.split()[0],'numpy':numpy.__version__,
                           'scipy':scipy.__version__,'sympy':sympy.__version__,'mpmath':mpmath.__version__},
            'scope':{'independent_review':False,'new_Lean':False,'repository_wide_CI':False,
                     'physical_Book_selection':False,'all42_stationary_root':False,'GR_closed':False}}
    data=json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.output:args.output.write_text(data,encoding='utf-8')
    print(data,end='')
if __name__=='__main__':main()
