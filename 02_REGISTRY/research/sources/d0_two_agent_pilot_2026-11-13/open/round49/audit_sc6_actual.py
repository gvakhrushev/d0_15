#!/usr/bin/env python3
"""Re-read actual SC6 gate stream as exact port normal form on every control column."""
from pathlib import Path
from hashlib import sha256
from collections import Counter
import importlib.util,json,sys
import numpy as np
import sympy as s
P=Path(__file__).resolve().parent;O=P.parent;repo=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_open_2026-11-13');owner=O/'round21';domain=repo/'02_REGISTRY/research/sources/d0_native_execution_domain_2026-10-24/native_execution.py'
sp=importlib.util.spec_from_file_location('b49_nt',domain);nt=importlib.util.module_from_spec(sp);sys.modules[sp.name]=nt;sp.loader.exec_module(nt)
assert nt.SOURCE_I_LOCAL**2==s.kronecker_product(s.diag(1,-1),s.eye(4))
G=s.Matrix(nt.G_LOCAL);assert nt.exact_matrix_equal(G.T*G,s.eye(2));assert nt.exact_matrix_equal(s.diag(1,-1)*G*s.diag(1,-1),G.T)
forward=[json.loads(x) for x in (owner/'SC6_FORWARD.jsonl').read_text().splitlines()];assert len(forward)==18176
terms=[(1,0,2),(1,1,3),(-1,0,3),(-1,1,2),(1,4,6),(1,5,3),(-1,4,3),(-1,5,6)];selectors=[i for i in range(32) if bin(i).count('1')==2][:8];a=np.arange(512,dtype=np.int64);at=0;results=[]
for selector,(sign,ia,ib) in zip(selectors,terms):
 control=list(range(5))+[5+2*ia,6+2*ia,5+2*ib,6+2*ib];exp=np.zeros(512,dtype=np.int64);xb=exp.copy();zb=exp.copy();sg=np.ones(512,dtype=np.int64);cx=0;counts=Counter()
 while cx<512:
  gate=forward[at];at+=1;op=gate['op'];ws=gate['wires'];counts[op]+=1
  if op=='G':assert ws==[19];exp+=1
  elif op=='CX':
   assert ws[1]==19 and ws[0] in control;bit=(a>>(8-control.index(ws[0])))&1;exp*=1-2*bit;xb^=bit;cx+=1
  else:
   assert op=='SourceI' and ws==[19,20,21] and forward[at]==gate;at+=1;counts['SourceI']+=1
   exp=-exp;sg*=1-2*xb;zb^=1
 pred=((a>>4)==selector)&(((a&15)==15) if sign==1 else ((a&15)!=15))
 assert np.array_equal(exp,512*pred) and not xb.any() and not zb.any() and np.all(sg==1)
 results.append({'selector':format(selector,'05b'),'sign':sign,'call_indices':[ia,ib],'columns':len(a),'accepted_columns':int(pred.sum()),'native_calls':sum(counts.values())})
assert at==len(forward)
# Exact all-selector/all-seven-pair truth count; terms are mutually disjoint.
patterns=np.arange(1<<19,dtype=np.uint32);sbits=patterns>>14;ready_report=patterns&((1<<14)-1);aggregate=np.zeros(len(patterns),dtype=np.uint8)
for sel,(sign,ia,ib) in zip(selectors,terms):
 mask=(3<<(2*ia))|(3<<(2*ib));both=(ready_report&mask)==mask;hit=(sbits==sel)&(both if sign==1 else ~both);aggregate+=hit.astype(np.uint8)
assert aggregate.max()==1 and int(aggregate.sum())==8192*8
# Under owner embedding v=G|0>, paid G^-1 maps v to |0>. For rejected
# selector V=I, and the canonical conversion is necessary: arbitrary v at
# readout would give |<1|v>|^2=p^2 instead of zero.
p=s.Symbol('p',positive=True);a0=s.Symbol('a',positive=True);v=s.Matrix([a0,p]);assert v==s.Matrix([[a0,-p],[p,a0]])*s.Matrix([1,0]);assert s.expand((s.diag(1,-1)*s.Matrix([[a0,-p],[p,a0]])*s.diag(1,-1))*v-s.Matrix([a0*a0+p*p,0]))==s.zeros(2,1)
result={'status':'PASS_SC6_EXACT_ACTUAL_PORT_CONTROL_AND_OWNER_EMBEDDING','input_sha256':{str(q):sha256(q.read_bytes()).hexdigest() for q in [owner/'SC6_FORWARD.jsonl',domain]},'term_normal_forms':results,'total_local_columns_checked':4096,'global_boolean_controls_checked':len(patterns),'global_accepted_columns':int(aggregate.sum()),'exact_global_normal_form':'V = sum_controls |control><control| tensor G_port^(512 chi(control)) tensor I_Spin','spin_and_control_identity_at_completed_V':True,'active_port_requires_canonical_born_v_then_paid_G_inverse':True,'rejected_input_false_click_if_conversion_omitted':'p^2 for input port v','paid_G_inverse_cost':{'G':1,'CX':0,'SourceI':4},'report_observable':'pre-sign Z_port, not per-call READY or REPORT','global_H1_binding_or_marks_admission_proved':False,'GR_closed':False}
(P/'SC6_ACTIVE_PORT_OWNER_CHECK.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'control_columns':len(patterns),'accepted_columns':int(aggregate.sum())}))
