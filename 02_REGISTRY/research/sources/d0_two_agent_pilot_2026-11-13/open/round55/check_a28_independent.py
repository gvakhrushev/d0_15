#!/usr/bin/env python3
"""Independent compact A28 input partition and finite clock checks."""
from pathlib import Path
from hashlib import sha256
from fractions import Fraction
from collections import deque
import json,sys,numpy as np
D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
P=Path(__file__).resolve().parent
f=D/'round28/FRESH_AUX_BIRTH_CLOCK_PLAN.json'; a25=D/'round25/GLOBAL_H1_PLAN.json';ns=D/'round25/H1_NAMESPACE_PLAN.json'
a=json.loads(f.read_text());b=json.loads(a25.read_text());x=json.loads(ns.read_text())
blocks=a['chronological_birth_blocks']; boundaries=sorted({0,x['layout']['qubits'],1,2,3,4,*[v for z in blocks for v in (z['start'],z['stop'])]})
cells=[]
for left,right in zip(boundaries,boundaries[1:]):
 coverage=sum(z['start']<=left and right<=z['stop'] for z in blocks)
 old=(left in (0,1,3) and right==left+1)
 assert coverage==(0 if old else 1),(left,right,coverage)
 cells.append([left,right,coverage])
n=sum(z['stop']-z['start'] for z in blocks);L=int(b['W_primitive_call_count_decimal']); assert n==10407050781 and n==a['total_canonical_RAW_birth_stages']; assert sum(int(v) for v in b['global_native_counts']['W_literal_echo'].values())==L==int(a['native_unitary_call_count']); assert int(a['clock_layer_count_N'])==n+L
# Geometric sum checks, including the last actual native unitary g as a layer.
for births in range(1,11):
 for length in range(1,11):
  assert sum(2**k for k in range(births))+length*2**births==(length+1)*2**births-1
# Two births plus two distinct noncommuting unitary stages; build Book clock
# from G1-G5 directly, verify both unitarities and every actual edge.
p=(5**.5-1)/2;v=np.array([p**.5,p]);j0=np.kron(np.eye(2),v[:,None]);j1=np.kron(np.eye(4),v[:,None]);b0=j1@j0;d1=np.eye(4)-j0@j0.T;d2=np.eye(8)-j1@j1.T
r=np.vstack([b0.T,d1@j1.T,d2,np.zeros((8,8))]);d=[2,4,8,8];off=np.cumsum([0]+d);q1=np.eye(8)[[1,0,2,3,4,5,6,7]];q2=np.eye(8)[[0,2,1,3,4,5,6,7]];assert np.linalg.norm(q1@q2-q2@q1)>1
T=np.zeros((sum(d),sum(d))); fs=[j0,j1,q1]
for i,F in enumerate(fs):T[off[i+1]:off[i+2],off[i]:off[i+1]]=F
T[:,off[-2]:off[-1]]=r@q2
with np.errstate(all='ignore'):
 errors=[np.linalg.norm(r.T@r-np.eye(8)),np.linalg.norm(T.T@T-np.eye(sum(d))),np.linalg.norm(T@T.T-np.eye(sum(d)))]
assert all(np.isfinite(e) and e<1e-12 for e in errors)
# Determine actual final primitive from the terminal inverse SITE stage,
# without expanding repeated internal streams.
sys.path.insert(0,str(D/'round25'));import global_h1 as g
last=deque(g.stage_blocks({'kind':'SITE'},g.namespace(),1),maxlen=1)[0]
def lastleaf(t):
 while t['op'] in ('seq','repeat'):
  t=t['children'][-1] if t['op']=='seq' else t['child']
 return t
end=lastleaf(last); assert end['op']=='CX' and end['wires']==[2692,2705],end
out={'status':'PASS_INDEPENDENT_A28_PARTITION_CLOCK','partition_cells':cells,'births':n,'L_bits':L.bit_length(),'births_plus_L_lt_2^4189':n+L<2**4189,'geometric_sum_exact_cases':100,'finite_growing_clock_unitary_numerical':True,'last_actual_primitive':end,'same_unknown_aux_input_contract':False,'full_giant_stream_executed':False,'physical_admission_or_marked_map_proved':False,'physical_C_closed':False,'GR_closed':False,'sha256':{str(t):sha256(t.read_bytes()).hexdigest() for t in (f,a25,ns)}}
(P/'A28_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'cells':len(cells),'last':end}))
