#!/usr/bin/env python3
"""Run actual altered programs; syntax errors and receipt-only failures do not count."""
from __future__ import annotations
import json,os,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CASES=[
 ('freeze_preparation_jet','dx+=channel(0,jets[k])+dchannel(0,states[k])','dx+=channel(0,jets[k])'),
 ('omit_event_normalization','-mean*dp)/prob','-0*mean*dp)/prob'),
 ('reverse_count_boundary_sign','s.diff(f,e)-lower+upper','s.diff(f,e)-lower-upper'),
 ('wrong_reference_effect','gamma*sum(((U-I).H*(U-I) for U in Us)','p**2*sum(((U-I).H*(U-I) for U in Us)'),
]
rows=[]
original=(ROOT/'src/moving_preparation_exact.py').read_text()
for name,old,new in CASES:
 if old not in original:raise AssertionError(('MUTATION_ANCHOR_MISSING',name))
 with tempfile.TemporaryDirectory(prefix='d0_preparation_mutant_') as td:
  root=Path(td);(root/'src').mkdir();(root/'results').mkdir()
  p=root/'src/moving_preparation_exact.py';p.write_text(original.replace(old,new,1))
  r=subprocess.run([sys.executable,'-O',str(p),'--write'],text=True,capture_output=True,timeout=90,
          env={**os.environ,'OPENBLAS_NUM_THREADS':'1','PYTHONDONTWRITEBYTECODE':'1'})
  if r.returncode==0 or 'AssertionError' not in r.stderr or 'IMMUTABLE' in r.stderr:
   raise AssertionError(('MUTATION_NOT_MATHEMATICALLY_REJECTED',name,r.stdout,r.stderr))
  rows.append({'name':name,'returncode':r.returncode,'rejection':r.stderr.splitlines()[-1]})
  print('REJECTED',name,rows[-1]['rejection'],flush=True)
(ROOT/'results/hostile_mutations.json').write_text(json.dumps({'status':'PASS','executed_mutants':rows},indent=2)+'\n')
