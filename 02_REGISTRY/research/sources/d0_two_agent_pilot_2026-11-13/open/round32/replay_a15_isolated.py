#!/usr/bin/env python3
"""Run A15 builder/checker in isolated copy of exact dependencies."""
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json,os
P=Path(__file__).resolve().parent
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
files={
 'round11':['SOURCE_TENSOR_DAG.json','PERIODIC_SOURCE_BINDING.json'],
 'round12':['INTERNAL_SELECTOR_PALETTE.json','compile_source_selectors.py'],
 'round13':['reversible_selectors.py','TOP_SOURCE_SELECTOR_CIRCUIT.json','INTERNAL_SELECTOR_CIRCUIT.json','FIRST_SUCCESS_CIRCUITS.json'],
 'round14':['native_boolean.py','NATIVE_BOOLEAN_LIBRARY.json','NATIVE_BOOLEAN_ANGLE.json'],
 'round15':['source_dispatcher.py','check_source_dispatcher.py','SOURCE_DISPATCH_TABLES.json','SOURCE_DISPATCH_COMPILATION.json','SOURCE_DISPATCH_CHECK.json','SOURCE_DISPATCH_RU.md']}
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
original={f'{d}/{n}':sha(root/d/n) for d,names in files.items() for n in names}
with tempfile.TemporaryDirectory(prefix='a15_review_',dir=P) as tmp:
 d=Path(tmp)
 for folder,names in files.items():
  (d/folder).mkdir()
  for name in names:shutil.copy2(root/folder/name,d/folder/name)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1');checks=[]
 for name in ['source_dispatcher.py','check_source_dispatcher.py']:
  cmd=['python3','-B','-W','error',name];x=subprocess.run(cmd,cwd=d/'round15',capture_output=True,text=True,check=True,env=env)
  checks.append({'command':cmd,'stdout':x.stdout.strip(),'stderr':x.stderr});print('passed',name,flush=True)
 names=['SOURCE_DISPATCH_TABLES.json','SOURCE_DISPATCH_COMPILATION.json','SOURCE_DISPATCH_CHECK.json'];outputs={x:sha(d/'round15'/x) for x in names}
 assert all(outputs[n]==original['round15/'+n] for n in names)
res={'status':'PASS_ISOLATED_A15_BUILDER_CHECKER','input_sha256':original,'outputs_byte_identical':outputs,'checks':checks,'owner_modified':False,'all_full_walks_executed':False,'GR_closed':False}
(P/'ISOLATED_REPLAY.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':res['status'],'outputs_byte_identical':len(outputs)}))
