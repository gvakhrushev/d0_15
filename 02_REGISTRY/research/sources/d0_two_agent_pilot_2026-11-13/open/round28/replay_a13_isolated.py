#!/usr/bin/env python3
"""Replay A13 builder and checker without writing to owner worktree."""
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json,os
P=Path(__file__).resolve().parent
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
files12=['INTERNAL_SELECTOR_PALETTE.json','TOP_SOURCE_SELECTOR_PALETTE.json','TEN_SIGN_REPORT_PALETTE.json','SELECTOR_COMPILATION.json']
files13=['reversible_selectors.py','build_selector_circuits.py','check_selector_circuits.py','INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json','FIRST_SUCCESS_CIRCUITS.json','CIRCUIT_COMPILATION.json','CIRCUIT_CHECK.json','REVERSIBLE_SELECTORS_RU.md']
sha=lambda x:hashlib.sha256(x.read_bytes()).hexdigest()
original={f'round12/{n}':sha(root/'round12'/n) for n in files12}|{f'round13/{n}':sha(root/'round13'/n) for n in files13}
with tempfile.TemporaryDirectory(prefix='a13_review_',dir=P) as d:
 d=Path(d);(d/'round12').mkdir();(d/'round13').mkdir()
 for n in files12:shutil.copy2(root/'round12'/n,d/'round12'/n)
 for n in files13:shutil.copy2(root/'round13'/n,d/'round13'/n)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1');checks=[]
 for script in ['build_selector_circuits.py','check_selector_circuits.py']:
  cmd=['python3','-B','-W','error',script];x=subprocess.run(cmd,cwd=d/'round13',capture_output=True,text=True,check=True,env=env);checks.append({'command':cmd,'stdout':x.stdout.strip(),'stderr':x.stderr})
 names=['INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json','FIRST_SUCCESS_CIRCUITS.json','CIRCUIT_COMPILATION.json','CIRCUIT_CHECK.json']
 regenerated={n:sha(d/'round13'/n) for n in names}
 assert all(regenerated[n]==original[f'round13/{n}'] for n in names)
res={'status':'PASS_A13_ISOLATED_BYTE_EXACT_REPLAY','input_sha256':original,'regenerated_sha256':regenerated,'runs':checks,'owner_modified':False,'native_word_executed':False,'GR_closed':False}
(P/'ISOLATED_REPLAY.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':res['status'],'byte_equal_outputs':len(regenerated),'checker':checks[-1]['stdout']}))
