#!/usr/bin/env python3
"""Isolated exact A13 native-CZ replay + independent signed-basis interpreter."""
from pathlib import Path
from collections import Counter
import tempfile,shutil,subprocess,hashlib,json,os
P=Path(__file__).resolve().parent
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round13')
N=P.parents[5]/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest();initial={str(x):sha(x) for x in [D/'compile_native_cz.py',D/'NATIVE_CZ_CHECK.json',D/'NATIVE_CONTROLLED_PHASE_RU.md',N]}
with tempfile.TemporaryDirectory(prefix='cz_review_',dir=P) as tmp:
 root=Path(tmp);dest=root/'02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct/round13';dest.mkdir(parents=True)
 nat=root/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24';nat.mkdir(parents=True)
 shutil.copy2(D/'compile_native_cz.py',dest/'compile_native_cz.py');shutil.copy2(N,nat/'native_execution.py')
 out=subprocess.run(['python3','-B','-W','error','compile_native_cz.py'],cwd=dest,capture_output=True,text=True,check=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 assert sha(dest/'NATIVE_CZ_CHECK.json')==initial[str(D/'NATIVE_CZ_CHECK.json')]
# SourceI local L_i in basis (1,i,j,k): explicit signed permutation, not
# the owner's matrix executor. All input bit columns get tested independently.
doc=json.loads((D/'NATIVE_CZ_CHECK.json').read_text());assert doc['native_source_sha256']==sha(N)
spinmap=[(1,1),(0,-1),(3,1),(2,-1)];basis_checks=0;inventories=[]
for ex in doc['examples']:
 execution=ex['word'];n=execution['qubits'];port=execution['source_port'];s0,s1=execution['source_spin'];control=ex['control'];target=ex['target'];gates=execution['gates'];hist=Counter(g['op'] for g in gates)
 assert hist=={'CX':8 if port in (control,target) else 14,'SourceI':5}
 assert not execution['blank_wires'] and not execution['old_right']
 for word in range(1<<n):
  state=word;phase=1
  for gate in gates:
   if gate['op']=='CX':
    c,t=gate['wires'];cb=(state>>(n-1-c))&1
    if cb:state^=1<<(n-1-t)
   elif gate['op']=='SourceI':
    assert gate['wires']==[port,s0,s1]
    if (state>>(n-1-port))&1:
     v=(((state>>(n-1-s0))&1)<<1)|((state>>(n-1-s1))&1);new,sgn=spinmap[v];phase*=sgn
     for wire,bit in ((s0,(new>>1)&1),(s1,new&1)):
      state=(state&~(1<<(n-1-wire)))|(bit<<(n-1-wire))
   else:raise AssertionError(gate['op'])
  c=(word>>(n-1-control))&1;t=(word>>(n-1-target))&1
  assert state==word and phase==(-1)**(c*t);basis_checks+=1
 inventories.append({'control':control,'target':target,'port':port,'columns':1<<n,'gates':dict(hist)})
for c in (0,1):
 for t in (0,1):assert c+t-(c^t)==2*c*t
res={'status':'PASS_ISOLATED_NATIVE_CZ_AND_INDEPENDENT_ALL_COLUMN_INTERPRETER','input_sha256':initial,'owner_byte_identical':True,'owner_stdout':out.stdout.strip(),'basis_columns_checked':basis_checks,'arrangements':inventories,'no_clean_resource_or_postselection':True,'Spin_not_individually_addressed':True,'all_other_primitives_compiled':False,'GR_closed':False}
(P/'NATIVE_CZ_REVIEW.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps({'status':res['status'],'basis_columns_checked':basis_checks,'arrangements':len(inventories)}))
