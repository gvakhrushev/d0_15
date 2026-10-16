#!/usr/bin/env python3
"""Execute altered mathematics; no printed-only hostile controls."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile

MUTATIONS = [
    ('wrong_isotropic_fourth_moment',
     'fourth = 3*sum(dets, s.S.Zero)+mixed',
     'fourth = 2*sum(dets, s.S.Zero)+mixed'),
    ('dropped_mixed_normal_shapes',
     'fourth = 3*sum(dets, s.S.Zero)+mixed',
     'fourth = 3*sum(dets, s.S.Zero)'),
    ('wrong_euler_contraction',
     'GB = s.expand(Rm2-4*Ric2+R**2)',
     'GB = s.expand(Rm2-3*Ric2+R**2)'),
    ('mean_log_in_place_of_normalizer',
     '1+c2*t**2*second+c4*t**4*fourth',
     '1+c2*t**2*sum((s.trace(B*B) for B in shapes),s.S.Zero)/2+c4*t**4*fourth'),
]


def run(root, source):
    text=source.read_text(encoding='utf8')
    results=[]
    with tempfile.TemporaryDirectory(prefix='d0-normal-volume-mutants-') as tmp:
        for name,old,new in MUTATIONS:
            if text.count(old)!=1: raise RuntimeError('Mutation location is not unique: '+name)
            candidate=Path(tmp)/(name+'.py')
            candidate.write_text(text.replace(old,new),encoding='utf8')
            proc=subprocess.run([sys.executable,str(candidate),'--repo-root',str(root)],
                                capture_output=True,text=True,timeout=45)
            if proc.returncode==0 or 'ArithmeticError:' not in proc.stderr:
                raise RuntimeError('Mutant not rejected mathematically: '+name+'\n'+proc.stderr)
            reason=proc.stderr.strip().splitlines()[-1]
            results.append({'name':name,'returncode':proc.returncode,'reason':reason})
    return {'scope':'four executed mathematical mutations, not physical validation',
            'mutations':results,'all_rejected':True}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path)
    parser.add_argument('--source',type=Path,default=Path(__file__).with_name('check_normal_volume.py'))
    parser.add_argument('--output',type=Path)
    args=parser.parse_args()
    root=args.repo_root or Path(__file__).resolve().parents[4]
    text=json.dumps(run(root,args.source),ensure_ascii=False,sort_keys=True,indent=2)+'\n'
    if args.output: args.output.write_text(text,encoding='utf8')
    print(text,end='')

if __name__=='__main__': main()
