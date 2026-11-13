#!/usr/bin/env python3
"""Replay A11 in a temporary copy; never write to its direct/round11 owner."""
from pathlib import Path
import shutil,tempfile,subprocess,os,hashlib,json
out=Path(__file__).resolve().parent
parent=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round11')
names=['source_operator_dag.py','SOURCE_TENSOR_DAG.json','certify_source_norm.py','check_source_operator.py','SOURCE_NORM_CERTIFICATE.json','SOURCE_OPERATOR_CHECK.json']
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
original={n:sha(parent/n) for n in names}
with tempfile.TemporaryDirectory(prefix='a11_review_',dir=out) as d:
 d=Path(d)
 for n in names:shutil.copy2(parent/n,d/n)
 env=dict(os.environ,OPENBLAS_NUM_THREADS='1',PYTHONDONTWRITEBYTECODE='1')
 cmds=[['python3','-B','-W','error','source_operator_dag.py'],['python3','-B','-W','error','certify_source_norm.py'],['python3','-B','-W','error','check_source_operator.py','--b21',str(out.parent/'round21')]]
 checks=[]
 for cmd in cmds:
  x=subprocess.run(cmd,cwd=d,env=env,capture_output=True,text=True,check=True);checks.append({'command':cmd,'stdout':x.stdout.strip(),'stderr':x.stderr})
 generated={n:sha(d/n) for n in ['SOURCE_TENSOR_DAG.json','SOURCE_NORM_CERTIFICATE.json','SOURCE_OPERATOR_CHECK.json']}
 assert all(generated[n]==original[n] for n in generated),(generated,original)
 r={'status':'ISOLATED_A11_EXACT_REPLAY_PASSED','input_sha256':original,'generated_sha256':generated,'checks':checks,'scope':'bounded copy/operator/norm interface replay and independent inspection; not full H1 or native sign implementation','GR_closed':False}
(out/'A11_REPLAY.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
