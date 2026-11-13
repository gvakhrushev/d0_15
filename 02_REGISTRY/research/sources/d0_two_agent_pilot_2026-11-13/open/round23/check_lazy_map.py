#!/usr/bin/env python3
"""Numerical centre illustration of the exact lazy all-column formula.
This is not sampled-vertex verification, native compilation or a halo policy.
"""
from pathlib import Path
from functools import lru_cache
import json, math
import numpy as np
P=Path(__file__).resolve().parent; B=P.parent/'round21'
a=[json.loads(x) for x in (P/'CHOI_ADDRESSES.jsonl').read_text().splitlines()]
g=[json.loads(x) for x in (B/'BRINKMANN_L4_CENTRE.jsonl').read_text().splitlines()]
siteindex={tuple(x['site']):i for i,x in enumerate(g)}
z=np.load(B/'CENTRE_JULIA32_TARGETS_NUMERIC.npz')
co=z['coframe_raw_and_pf']; links=z['proper_links']; meta=json.loads((B/'REFERENCE_METADATA.json').read_text())
I=np.eye(16); order=(0,2,3,1)
mm=lambda x,y:np.einsum('ij,jk->ik',x,y,optimize=False)
def H(x,y): return float(meta['k0_original'])*(2*math.pi)**2*.01**2*(x*x+y*y)+.03*(x*x-y*y)
@lru_cache(None)
def halo_matrix(ix,iy,d):
 if d!=0:return links[0,1]
 x=ix/4;y=iy/4;kx=(H(x,y)-H(x-.25,y))/2;ky=(H(x,y)-H(x,y-.25))/2
 N2=np.zeros((4,4));N2[1,2]=N2[2,0]=1
 N3=np.zeros((4,4));N3[1,3]=N3[3,0]=1
 V=-kx*N2-ky*N3;U=np.eye(4)+V+mm(V,V)/2
 exterior=np.zeros((16,16))
 for q in range(16):
  qr=[j for j in order if (q>>j)&1]
  for t in range(16):
   tr=[j for j in order if (t>>j)&1]
   if len(qr)==len(tr):exterior[q,t]=1 if not qr else np.linalg.det(U[np.ix_(qr,tr)])
 C=exterior/2
 def root(M):
  eig,v=np.linalg.eigh((M+M.T)/2);assert eig.min()>0
  return mm(v*np.sqrt(eig),v.T)
 J=np.block([[C,root(I-mm(C,C.T))],[root(I-mm(C.T,C)),-C.T]])
 assert np.max(np.abs(mm(J.T,J)-np.eye(32)))<1e-12
 return J
A=len(a);D=2**22; b=np.zeros(D)
for v in a:
 if v['kind']=='identity_anchor':J=np.eye(32)
 elif v['kind']=='inverse_coframe_column':J=co[siteindex[tuple(v['site'])],1,v['direction']]
 else:
  x=tuple(v['site']);d=v['direction']
  J=halo_matrix(x[2],x[3],d) if v['exterior_halo'] else links[siteindex[x],d]
 off=v['a']*1024;b[off:off+1024]=J.T.reshape(1024)/math.sqrt(32*A)
c=b[0];expected=1/math.sqrt(32*A)
assert abs(c-expected)<1e-16 and abs(np.linalg.norm(b)-1)<1e-12
# K v = b*v0-e0*(b.v); K² v derived directly. O^T changes sign of K only.
def transform(v,reverse=False):
 dot=float(np.dot(b,v));k=b*v[0];k[0]-=dot
 # K²v=b*(c*v0-b.v)-e0*(v0-c*b.v)
 k2=b*(c*v[0]-dot);k2[0]-=v[0]-c*dot
 return v+(-k if reverse else k)+k2/(1+c)
v=np.zeros(D);v[0]=1; y=transform(v)
anchor_error=float(np.max(np.abs(y-b)))
rng=np.random.default_rng(23);inds=rng.choice(D,size=20,replace=False)
v=np.zeros(D);v[inds]=rng.normal(size=20);v/=np.linalg.norm(v)
w=transform(v);back=transform(w,True)
reversal=float(np.linalg.norm(v-back));norm_error=abs(float(np.linalg.norm(w))-1)
padding_index=D-1;v2=np.zeros(D);v2[padding_index]=1; padding_error=float(np.max(np.abs(transform(v2)-v2)))
assert max(anchor_error,reversal,norm_error,padding_error)<1e-12
res={'status':'NUMERIC_CENTRE_MAP_ILLUSTRATION_NOT_GATE_WORD','vector_dimension':D,'active_coordinates':A*1024,
 'anchor_error':anchor_error,'inverse_replay_l2_error':reversal,'sparse_column_superposition_norm_error':norm_error,'padding_column_error':padding_error,
 'coframe_mode':'B21 sqrt(rho)-dressed candidate; exact ownership/binding to complete source remains to be checked',
 'halo_links':'polynomial central geometry only; not verified as full H1 boundary extension',
 'allocated_dense_operator':False,'all_sam_vertices_tested':False,'GR_closed':False}
(P/'LAZY_MAP_TEST.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
