#!/usr/bin/env python3
"""Run actual corrupted second-jet fixtures in temporary files."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile

base=Path(__file__).resolve().parent
text=(base/'check_record_2jet.py').read_text()
mutations={
 'remove_real_second_jet':('I*getB(m,n)-','0*getB(m,n)-'),
 'duplicate_tangent_generator':('Alabels=[(0,1),(0,2),(0,3),(1,0)]','Alabels=[(0,1),(0,2),(0,3),(0,1)]'),
 'wrong_signature_reflection':('images=[2*(V*tt+tt*V-tt*(t.T*V*t)[0])-V','images=[1*(V*tt+tt*V-tt*(t.T*V*t)[0])-V')}
results={}
with tempfile.TemporaryDirectory(prefix='d0-2jet-mutants-') as td:
 for name,(old,new) in mutations.items():
  if text.count(old)!=1:raise ValueError('Mutation target not unique: '+name)
  script=Path(td)/(name+'.py');script.write_text(text.replace(old,new))
  cp=subprocess.run([sys.executable,'-O',str(script)],capture_output=True,text=True,timeout=40)
  if cp.returncode==0:raise ValueError('Mutant survived: '+name)
  if 'RuntimeError:' not in cp.stderr:raise ValueError('Non-mathematical mutant failure: '+name+cp.stderr[-400:])
  results[name]={'rejected':True,'last_error':cp.stderr.strip().splitlines()[-1]}
print(json.dumps(results,sort_keys=True,indent=2))
