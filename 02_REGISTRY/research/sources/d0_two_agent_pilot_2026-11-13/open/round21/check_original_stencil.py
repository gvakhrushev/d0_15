#!/usr/bin/env python3
"""Actual CAR16 six-face stencil at one interior point of exported L4 centre.

Numerical source-operand verification, not the seven-bank gate writer.
"""
from pathlib import Path
import json
import numpy as np

d=Path(__file__).resolve().parent
rows=[json.loads(x) for x in (d/'BRINKMANN_L4_CENTRE.jsonl').read_text().splitlines()]
data={tuple(r['site']):r for r in rows};base=(0,0,1,1);order=(0,2,3,1)
eye4=np.eye(4);eta=np.array([[0.,1.,0.,0.],[1.,0.,0.,0.],[0.,0.,-1.,0.],[0.,0.,0.,-1.]])
mm=lambda a,b:np.einsum('ij,jk->ik',a,b,optimize=False)
def mul(*m):
    x=m[0]
    for a in m[1:]:x=mm(x,a)
    return x
def ext(U):
    A=np.zeros((16,16))
    for i in range(16):
      a=[j for j in order if (i>>j)&1]
      for k in range(16):
        b=[j for j in order if (k>>j)&1]
        if len(a)==len(b):A[i,k]=1. if not a else np.linalg.det(U[np.ix_(a,b)])
    return A
def shift(site,axis):
    s=list(site);s[axis]=(s[axis]+1)%4 if axis<2 else s[axis]+1
    return tuple(s)
def link(site,axis):return np.array(data[site]['U_u_approx']) if axis==0 else eye4

creators=[]
for r in range(4):
    C=np.zeros((16,16));before=order[:order.index(r)]
    for bits in range(16):
        if not ((bits>>r)&1):C[bits|(1<<r),bits]=(-1)**sum((bits>>j)&1 for j in before)
    creators.append(C)
V=np.array(data[base]['native_coframe_columns_approx'])
C=[sum(V[j,r]*creators[j] for j in range(4)) for r in range(4)]
H=ext(eta); faces=[]
for r in range(4):
  for s in range(r+1,4):
    sr,ss=shift(base,r),shift(base,s)
    # P_rs=U_r(z) U_s(z+r) U_r(z+s)^-1 U_s(z)^-1.
    P=mul(link(base,r),link(sr,s),np.linalg.inv(link(ss,r)),np.linalg.inv(link(base,s)))
    comm=mul(C[r],H,C[s].T,H)-mul(C[s],H,C[r].T,H)
    value=-np.trace(mm(comm,ext(P)))/8
    faces.append({'roles':[r,s],'link_operands':[[list(base),r],[list(sr),s],[list(ss),r],[list(base),s]],
                  'source_moment_float':float(value),'lorentz_error_float':float(np.max(np.abs(mul(P.T,eta,P)-eta)))})

psi=lambda site:np.array([float(data[site]['psi0']),float(data[site]['psi15'])])
dp=np.array([(psi(shift(base,r))-psi(base))*4 for r in range(4)])
ginv=mul(V.T,eta,V)/(0.6**2)
q=float(sum(ginv[r,s]*np.dot(dp[r],dp[s]) for r in range(4) for s in range(4)))
assert max(abs(x['source_moment_float']) for x in faces)<1e-12
assert max(x['lorentz_error_float'] for x in faces)<1e-12 and abs(q)<1e-12
result={'status':'PASS_NUMERIC_ORIGINAL_CAR16_LOCAL_STENCIL','site':base,'faces':faces,
        'q_moment_float':q,'note':'original nonvacuum centre only; no H.1 sampled Y_b, emitted source-sign gate or source jet',
        'all_fields_and_pf_source_transport_verified':False,'GR_closed':False}
(d/'ORIGINAL_STENCIL_CHECK.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':result['status'],'site':base,'max_abs_face_moment':max(abs(x['source_moment_float']) for x in faces),'q_moment':q}))
