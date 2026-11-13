#!/usr/bin/env python3
"""Exact constant frame identities plus all 256 actual B21 raw-column matches."""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np

parser=argparse.ArgumentParser();parser.add_argument('b21',type=Path);args=parser.parse_args()
eta=np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]],dtype=np.int64)
R=np.diag([1,1,-1,-1]);eye=np.eye(4,dtype=np.int64)
assert np.array_equal(R.T@eta@R,eta) and np.prod(np.diag(R))==1
order=(0,2,3,1)
Gamma=np.diag([int(np.prod([R[i,i] for i in range(4) if b&(1<<i)])) for b in range(16)])
for i in range(4):
 C=np.zeros((16,16),dtype=np.int64)
 for bits in range(16):
  if not bits&(1<<i):C[bits|(1<<i),bits]=(-1)**sum(bool(bits&(1<<j)) for j in order[:order.index(i)])
 assert np.array_equal(Gamma@C@Gamma.T,R[i,i]*C)
N=[]
for i in (2,3):
 n=np.zeros((4,4),dtype=np.int64);n[1,i]=n[i,0]=1;N.append(n)
 assert np.array_equal(R@n@R,-n) and not (n@n@n).any()
assert np.array_equal(N[0]@N[1],N[1]@N[0])
e10=np.zeros((4,4),dtype=np.int64);e10[1,0]=1
# Both sides affine in H, and exact inverse is I-H E10/2, since E10²=0.
for H in (F(0),F(1)):
 e0=eye.astype(object)+H/2*e10;inverse0=eye.astype(object)-H/2*e10
 e=R@e0
 assert np.array_equal(e@(inverse0@R),eye)
 u=F(3,5)*eta@(inverse0@R).T
 expected=np.zeros((4,4),dtype=object);expected[1,0]=expected[0,1]=F(3,5)
 expected[1,1]=-F(3,5)*H/2;expected[2,2]=expected[3,3]=F(3,5)
 assert np.array_equal(u,expected)
 assert np.array_equal(u,R@(F(3,5)*eta@inverse0.T))
path=args.b21/'BRINKMANN_L4_CENTRE.jsonl'
rows=[json.loads(x) for x in path.read_text().splitlines()]
max_u=max_U=0.
mm=lambda a,b:np.einsum('ij,jk->ik',a,b,optimize=False)
for row in rows:
 H=float(row['H']);inv=eye-H/2*e10
 u=.6*mm(eta,mm(inv,R).T)
 K=float(row['Kx'])*N[0]+float(row['Ky'])*N[1]
 original=eye+K+mm(K,K)/2
 U=mm(mm(R,original),R)
 max_u=max(max_u,float(np.max(np.abs(u-np.array(row['native_coframe_columns_approx'])))))
 max_U=max(max_U,float(np.max(np.abs(U-np.array(row['U_u_approx'])))))
assert len(rows)==256 and max_u<2e-16 and max_U<2e-16
out={'status':'PASS_CURRENT_RAW_INVERSE_COFRAME_BINDING',
     'exact_R':'diag(1,1,-1,-1)', 'proper_Lorentz_R':True,
     'source_frame':'e=R*(I+H E_10/2); u=nu eta e^-T',
     'link_frame':'U=R exp(+Kx N2+Ky N3) R^-1=exp(-Kx N2-Ky N3)',
     'all_CAR_creator_covariances_exact':4,
     'all_exported_sites':256,'max_raw_u_match_error':max_u,'max_link_match_error':max_U,
     'chosen_chart':'additive raw u entries, 24 proper-link coordinates and two material values at each of 64 free sites; e=nu eta u^-T; fixed collar',
     'PF_dressing_in_this_binding':False,
     'B21_geometry_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
     'physical_boundary_or_native_price_proved':False,'GR_closed':False}
(Path(__file__).resolve().parent/'CURRENT_FRAME_CHECK.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
