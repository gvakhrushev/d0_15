#!/usr/bin/env python3
"""Rebuild A12 under isolated round11/round12 and compare bytes to snapshot."""
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json,os
P=Path(__file__).resolve().parent
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
files11=['SOURCE_TENSOR_DAG.json','PERIODIC_SOURCE_BINDING.json']
files12=['compile_source_selectors.py','verify_source_selectors.py','INTERNAL_SELECTOR_PALETTE.json','TOP_SOURCE_SELECTOR_PALETTE.json','TEN_SIGN_REPORT_PALETTE.json','SELECTOR_COMPILATION.json','SELECTOR_CHECK.json','COHERENT_SOURCE_SELECTORS_RU.md']
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
original={f'round11/{n}':sha(root/'round11'/n) for n in files11}|{f'round12/{n}':sha(root/'round12'/n) for n in files12}
with tempfile.TemporaryDirectory(prefix='a12_review_',dir=P) as d:
 d=Path(d);(d/'round11').mkdir();(d/'round12').mkdir()
 for n in files11:shutil.copy2(root/'round11'/n,d/'round11'/n)
 for n in files12:shutil.copy2(root/'round12'/n,d/'round12'/n)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1');cmds=[['python3','-B','-W','error','compile_source_selectors.py'],['python3','-B','-W','error','verify_source_selectors.py']];checks=[]
 for cmd in cmds:
  x=subprocess.run(cmd,cwd=d/'round12',capture_output=True,text=True,check=True,env=env);checks.append({'command':cmd,'stdout':json.loads(x.stdout),'stderr':x.stderr})
 names=['INTERNAL_SELECTOR_PALETTE.json','TOP_SOURCE_SELECTOR_PALETTE.json','TEN_SIGN_REPORT_PALETTE.json','SELECTOR_COMPILATION.json','SELECTOR_CHECK.json']
 regenerated={n:sha(d/'round12'/n) for n in names}
 assert all(regenerated[n]==original[f'round12/{n}'] for n in names)
res={'status':'PASS_A12_ISOLATED_BYTE_EXACT_REPLAY','input_sha256':original,'regenerated_sha256':regenerated,'runs':checks,'direct_owner_modified':False,'native_word_executed':False,'GR_closed':False}
(P/'ISOLATED_REPLAY.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':res['status'],'byte_equal_outputs':len(regenerated),'verifier_checks':checks[-1]['stdout']['checks']}))
