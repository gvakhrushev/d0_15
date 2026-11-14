#!/usr/bin/env python3
"""Prove A11 H_f vanishes for all coframes when all proper links are I."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');file=D/'round11/SOURCE_TENSOR_DAG.json';dag=json.loads(file.read_text());nodes=dag['nodes'];root=dag['roots']['H_f_before_inverse_PF'];needed=set();todo=[root]
while todo:
 i=todo.pop()
 if i in needed:continue
 needed.add(i);todo.extend(nodes[i].get('args',[]))
order=sorted(needed);parsed={};names=sorted({z['name'] for i in needed for z in [nodes[i]] if z['op']=='var' and z['kind']=='choi_coframe'});assert len(names)==16
for i in order:
 z=nodes[i]
 if z['op']=='const':assert z['b']=='0';parsed[i]=F(z['a'])
 elif z['op']=='var':
  n=z['name'].split('/')
  parsed[i]=('u',names.index(z['name'])) if n[0]=='u' else ('M',int(n[3])==int(n[4]))
def evalf(active):
 values={}
 for i in order:
  z=nodes[i];op=z['op']
  if op=='const':v=parsed[i]
  elif op=='var':kind,value=parsed[i];v=int(value in active) if kind=='u' else int(value)
  elif op=='add':v=sum((values[j] for j in z['args']),0)
  else:
   assert op=='mul';v=1
   for j in z['args']:v*=values[j]
  values[i]=v
 return values[root]
assert evalf(set())==0
for i in range(16):assert evalf({i})==0
for i in range(16):
 for j in range(i+1,16):assert evalf({i,j})==0
# The previous exact DAG degree proof establishes a homogeneous quadratic in
# the 16 coframe variables. Zero on 0, e_i, e_i+e_j forces every coefficient 0.
previous=json.loads((P/'REFERENCE_GEOMETRY_EXACT_CHECK.json').read_text());assert previous['coframe_and_matter_source_homogeneity']['H_f']==[2,0]
out={'status':'PASS_FLAT_LINK_HF_ZERO_FOR_ALL_COFRAMES','input_sha256':sha256(file.read_bytes()).hexdigest(),'source_ancestor_nodes':len(needed),'coframe_variables':len(names),'exact_polarization_evaluations':1+16+120,'flat_all_links_identity_implies_Hf_zero_for_every_coframe':True,'scope':'Polynomial identity for the A11 ideal source, not a native gate execution or proof of physical marked-map equality.','GR_closed':False}
(P/'FLAT_HF_ALL_COFRAMES_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'exact_polarization_evaluations':out['exact_polarization_evaluations']}))
