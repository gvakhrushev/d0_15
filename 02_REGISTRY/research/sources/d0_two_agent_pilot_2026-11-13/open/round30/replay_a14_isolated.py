#!/usr/bin/env python3
"""Replay A14 small words, given-k certification and lowering in isolated root."""
from pathlib import Path
import tempfile,shutil,subprocess,hashlib,json,os
P=Path(__file__).resolve().parent
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13')
base=root/'02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct'
files13=['reversible_selectors.py','INTERNAL_SELECTOR_CIRCUIT.json','TOP_SOURCE_SELECTOR_CIRCUIT.json','TEN_SIGN_REPORT_CIRCUIT.json','FIRST_SUCCESS_CIRCUITS.json','CIRCUIT_COMPILATION.json']
files14=['native_boolean.py','certify_boolean_angle.py','check_native_boolean.py','lower_native_selectors.py','NATIVE_BOOLEAN_ANGLE.json','NATIVE_BOOLEAN_CHECK.json','NATIVE_BOOLEAN_LIBRARY.json','NATIVE_SELECTOR_LOWERING.json','NATIVE_BOOLEAN_LOWERING_RU.md']
native=['d0_native_execution_domain_2026-10-24/native_execution.py','d0_native_readiness_amplification_2026-10-24/native_phase.py']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original={f'round13/{n}':sha(base/'round13'/n) for n in files13}|{f'round14/{n}':sha(base/'round14'/n) for n in files14}|{n:sha(root/'02_REGISTRY/research/sources'/n) for n in native}
with tempfile.TemporaryDirectory(prefix='a14_review_',dir=P) as t:
 tmp=Path(t);sources=tmp/'02_REGISTRY/research/sources';d=sources/'d0_two_agent_pilot_2026-11-13/direct';(d/'round13').mkdir(parents=True);(d/'round14').mkdir()
 for n in files13:shutil.copy2(base/'round13'/n,d/'round13'/n)
 for n in files14:shutil.copy2(base/'round14'/n,d/'round14'/n)
 for n in native:
  dst=sources/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/'02_REGISTRY/research/sources'/n,dst)
 env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1');runs=[]
 cert="import json,certify_boolean_angle as c; d=json.load(open('NATIVE_BOOLEAN_ANGLE.json')); assert c.certify(int(d['k']),4096,16640)==d['certificate']; print('given-k owner certificate exact, no candidate search')"
 cmds=[['python3','-B','-W','error','-c',cert],['python3','-B','-W','error','check_native_boolean.py'],['python3','-B','-W','error','lower_native_selectors.py']]
 for cmd in cmds:
  res=subprocess.run(cmd,cwd=d/'round14',capture_output=True,text=True,check=True,env=env);runs.append({'command':cmd,'stdout':res.stdout.strip(),'stderr':res.stderr});print('passed:',cmd[-1][:60],flush=True)
 names=['NATIVE_BOOLEAN_CHECK.json','NATIVE_BOOLEAN_LIBRARY.json','NATIVE_SELECTOR_LOWERING.json']
 regenerated={n:sha(d/'round14'/n) for n in names};assert all(regenerated[n]==original[f'round14/{n}'] for n in names)
res={'status':'PASS_ISOLATED_A14_CERT_SMALL_WORD_AND_LOWERING','input_sha256':original,'outputs_byte_identical':regenerated,'runs':runs,'candidate_search_run':False,'owner_modified':False,'giant_native_word_expanded':False,'GR_closed':False}
(P/'ISOLATED_REPLAY.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':res['status'],'byte_equal_outputs':len(regenerated),'given_k_certificate_equal':True}),flush=True)
