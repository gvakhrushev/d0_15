#!/usr/bin/env python3
"""Numeric L4 torus all-column Choi completion at the B21 centre.
This evaluates the centre target, not a gate word or every SAM branch.
"""
from pathlib import Path
import math,json,numpy as np
P=Path(__file__).resolve().parent;B=P.parent/'round21'
a=[json.loads(s) for s in (P/'TORUS_CHOI_ADDRESSES.jsonl').read_text().splitlines()]
g=[json.loads(s) for s in (B/'BRINKMANN_L4_CENTRE.jsonl').read_text().splitlines()]
idx={tuple(r['site']):i for i,r in enumerate(g)};z=np.load(B/'CENTRE_JULIA32_TARGETS_NUMERIC.npz')
co=z['coframe_raw_and_pf']; link=z['proper_links'];A=len(a);D=2**22;assert A==2049
b=np.zeros(D); max_orth=0.0
for v in a:
 if v['kind']=='identity_anchor':J=np.eye(32)
 elif v['kind']=='inverse_coframe_column':J=co[idx[tuple(v['site'])],0,v['direction']]
 else:J=link[idx[tuple(v['site'])],v['direction']]
 orth=np.einsum('ij,jk->ik',J.T,J,optimize=False)
 max_orth=max(max_orth,float(np.max(np.abs(orth-np.eye(32)))))
 b[1024*v['a']:1024*(v['a']+1)]=J.T.reshape(1024)/math.sqrt(32*A)
c=b[0];assert abs(c-1/math.sqrt(32*A))<1e-16 and abs(np.linalg.norm(b)-1)<1e-12

def O(v,rev=False):
 dot=float(np.dot(b,v));k=b*v[0];k[0]-=dot
 k2=b*(c*v[0]-dot);k2[0]-=v[0]-c*dot
 return v+(-k if rev else k)+k2/(1+c)
r=np.zeros(D);r[0]=1;anchor=float(np.max(np.abs(O(r)-b)))
# Deliberately sample active and padded input columns to exercise b overlap and fixed complement.
v=np.zeros(D); v[0]=.3;v[1]=.4;v[20_000]=.5;v[2_098_176]=.2;v[D-1]=.6;v/=np.linalg.norm(v)
w=O(v);rev=float(np.linalg.norm(O(w,True)-v));norm=abs(float(np.linalg.norm(w))-1)
pad=np.zeros(D);pad[2_098_176]=1;paderr=float(np.max(np.abs(O(pad)-pad)))
assert max(max_orth,anchor,rev,norm,paderr)<1e-12
result={'status':'NUMERIC_TORUS_CENTRE_ALL_COLUMN_FORMULA_DIAGNOSTIC', 'active_A':A,'vector_dimension':D,'anchor_squared':'1/65568','orthogonality_error':max_orth,'anchor_error':anchor,'inverse_error':rev,'norm_error':norm,'padding_error':paderr,'coframe':'B21 raw u=nu eta e^-T, A11 source interface; actual all-SAM binding remains uncompiled','full_22_qubit_operator_allocated':False,'native_compiled':False,'all_SAM_branches_evaluated':False,'GR_closed':False}
(P/'TORUS_CHOI_TEST.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
