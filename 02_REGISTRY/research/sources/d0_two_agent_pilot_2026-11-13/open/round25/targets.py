#!/usr/bin/env python3
"""Computable L4 H1 target family: float64 evaluator, lazy full columns.
All objects are target matrices, not native words; see TARGETS_RU.md.
"""
from pathlib import Path
from functools import lru_cache
import json, math
import numpy as np
from scipy.linalg import expm
LAMBDA_INTEGER=2**1525
from fractions import Fraction
EPSILON_EXACT=Fraction(1,2**1531)
P=Path(__file__).resolve().parent; B=P.parent/'round21'; C=P.parent/'round24'
mm=lambda x,y:np.einsum('ij,jk->ik',x,y,optimize=False)
PVAL=(math.sqrt(5)-1)/2; ROOTP=math.sqrt(PVAL); NU=.6; H=.25; SAMP=2**-30
META=json.loads((B/'REFERENCE_METADATA.json').read_text()); K0=float(META['k0_original'])
F=float(__import__('fractions').Fraction(META['F_h_rational'])); DREF=F/(36*K0); AMP=H*6*math.sqrt(DREF)/2
ETA=np.array([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]],float); CART=np.diag([1.,-1.,-1.,-1.]);I4=np.eye(4);I16=np.eye(16);I32=np.eye(32)
T=np.array([[1,1,0,0],[1,-1,0,0],[0,0,math.sqrt(2),0],[0,0,0,-math.sqrt(2)]],float)/math.sqrt(2)
assert np.max(np.abs(mm(mm(T,CART),T.T)-ETA))<1e-15
ca=(1+(H/2)**2)/(1-(H/2)**2);sa=H/(1-(H/2)**2);vb=H/20;cb=(1-vb*vb)/(1+vb*vb);sb=2*vb/(1+vb*vb)
AC=I4.copy();AC[0,0]=AC[2,2]=ca;AC[0,2]=AC[2,0]=sa
BC=I4.copy();BC[1,1]=BC[2,2]=cb;BC[1,2]=sb;BC[2,1]=-sb
AREF=mm(mm(T,AC),T.T);BREF=mm(mm(T,BC),T.T)
PSI_AMP=.01*math.pi/(2*math.sqrt(2)); ZETA=2**-20
ROWS=[json.loads(x) for x in (B/'ORIGINAL_PF_N20_L4.jsonl').read_text().splitlines()];SITES=[tuple(r['site']) for r in ROWS];INDEX={x:i for i,x in enumerate(SITES)}
COORD=[json.loads(x) for x in (B/'L4_INTERIOR_CHART_COORDINATES.jsonl').read_text().splitlines()]
ADDR=[json.loads(x) for x in (C/'TORUS_CHOI_ADDRESSES.jsonl').read_text().splitlines()];assert len(ADDR)==2049
ADDR_LOOKUP={(r['kind'],tuple(r['site']),r['direction']):r['a'] for r in ADDR if 'site' in r}
KS=json.loads((B/'ORIGINAL_FOURIER128_L4.json').read_text())['kappa']; COUNT=np.array([r['N'] for r in ROWS]);RHO=256*COUNT/10946;CHI=np.sqrt(COUNT/10946)
ORDER=(0,2,3,1);CREATORS=[]
for i in range(4):
 m=np.zeros((16,16))
 for mask in range(16):
  if not (mask>>i)&1:m[mask|(1<<i),mask]=(-1)**sum(bool(mask&(1<<j)) for j in ORDER[:ORDER.index(i)])
 CREATORS.append(m)
N2=np.zeros((4,4));N2[1,2]=N2[2,0]=1
N3=np.zeros((4,4));N3[1,3]=N3[3,0]=1
GENERATORS={}
for i in range(4):
 for j in range(i+1,4):
  a=np.zeros((4,4));a[i,j]=1;a[j,i]=-1;GENERATORS[i,j]=mm(ETA,a)
for z in GENERATORS.values():assert np.max(np.abs(mm(z.T,ETA)+mm(ETA,z)))<1e-15
BANKS=('y+','y-','f','0','x+','x-','q');A=2049;D=2**22;ANCHOR=1/math.sqrt(32*A)

def canonical_label(label):
 if label is None:return None  # exact Y0, not the all-zero SAM vertex
 if isinstance(label,str):
  assert len(label)==len(COORD) and set(label)<=set('01');return np.fromiter((int(x) for x in label),dtype=np.int8)
 arr=np.asarray(label,dtype=np.int8);assert arr.shape==(len(COORD),) and np.all((arr==0)|(arr==1));return arr

def current(label=None):
 bits=canonical_label(label); u=np.zeros((256,4,4)); links=np.tile(I4,(256,4,1,1));psi=np.zeros((256,2))
 for x in SITES:
  n=INDEX[x];xx,yy=x[2]*H,x[3]*H
  def hh(a,b):return K0*(2*math.pi)**2*.01**2*(a*a+b*b)+.03*(a*a-b*b)
  hval=hh(xx,yy);kx=(hval-hh(xx-H,yy))/2;ky=(hval-hh(xx,yy-H))/2
  u[n]=np.array([[0,NU,0,0],[NU,-NU*hval/2,0,0],[0,0,NU,0],[0,0,0,NU]])
  gen=-kx*N2-ky*N3;links[n,0]=I4+gen+mm(gen,gen)/2
  psi[n]=PSI_AMP*np.array([math.cos(math.pi*x[0]/2),math.sin(math.pi*x[0]/2)])
 if bits is not None:
  theta=np.zeros((256,4,4,4))
  for coord,b in zip(COORD,bits):
   ix=INDEX[tuple(coord['site'])]; delta=SAMP*(int(b)-PVAL**2);kind=coord['kind']
   if kind=='coframe':u[ix,coord['component'],coord['role']]+=delta
   elif kind=='matter':psi[ix,0 if coord['grade']==0 else 1]+=delta
   else:theta[ix,coord['role']]+=delta*GENERATORS[tuple(coord['generator'])]
  for ix in range(256):
   for role in range(4):
    if np.any(theta[ix,role]):links[ix,role]=mm(expm(theta[ix,role]),links[ix,role])
 return u,links,psi

def fields(bank,label=None):
 assert bank in BANKS or bank=='current_mark'
 u0,l0,m0=current(label)
 if bank in ('f','q','current_mark'):
  return u0,(l0 if bank in ('f','current_mark') else np.tile(I4,(256,4,1,1))),(m0 if bank in ('q','current_mark') else np.zeros_like(m0))
 u=np.array([NU*math.sqrt(rho)/6*(mm(T,CART)) for rho in RHO]); links=np.tile(I4,(256,4,1,1));psi=np.zeros((256,2))
 if bank in ('x+','x-'):
  links[:,0]=AREF;links[:,1]=BREF if bank=='x+' else BREF.T
 if bank in ('y+','y-'):
  axis=1 if bank=='y+' else 0
  for x in SITES:psi[INDEX[x],0]=AMP*(-1)**x[axis]
 return u,links,psi

def exterior(U):
 out=np.zeros((16,16)); inds=[[i for i in ORDER if (m>>i)&1] for m in range(16)]
 for i,aa in enumerate(inds):
  for j,bb in enumerate(inds):
   if len(aa)==len(bb):out[i,j]=np.linalg.det(U[np.ix_(aa,bb)]) if aa else 1.
 return out

def posroot(M):
 vals,vec=np.linalg.eigh((M+M.T)/2);assert vals.min()>0
 return np.einsum('ij,jk->ik',vec*np.sqrt(vals),vec.T,optimize=False)

def julia(C):
 return np.block([[C,posroot(I16-mm(C,C.T))],[posroot(I16-mm(C.T,C)),-C.T]])

def local_m(psi):
 d=1-PVAL-float(float(np.dot(psi,psi)));assert d>0
 m=np.zeros(16);m[1]=ROOTP;m[0]=psi[0];m[14]=math.sqrt(d);m[15]=psi[1];return m

def rot(m,anchor=1):
 e=np.eye(len(m))[:,anchor];c=float(m[anchor]);k=np.outer(m,e)-np.outer(e,m)
 return np.eye(len(m))+k+mm(k,k)/(1+c)
MSTAR=local_m(np.zeros(2)); MSTAR_ROT=rot(MSTAR)

def car_map(psi):return mm(rot(local_m(psi)),MSTAR_ROT.T)

def chi_ref(x,r):
 pair,typ=divmod(r,2);z=sum(int(a)*int(b) for a,b in zip(KS[pair],x))%4
 return ((1,0,-1,0) if typ==0 else (0,1,0,-1))[z]/128

@lru_cache(maxsize=8192)
def creator_julia_cached(key):
 v=np.frombuffer(key,dtype=np.float64);C=sum(v[q]*CREATORS[q] for q in range(4))
 # CAR identity makes square roots explicit on all columns.
 norm2=float(np.dot(v,v));assert norm2<1
 d=1/(1+math.sqrt(1-norm2));left=I16-d*mm(C,C.T);right=I16-d*mm(C.T,C)
 return np.block([[C,left],[right,-C.T]])

@lru_cache(maxsize=8192)
def link_julia_cached(key):return julia(exterior(np.frombuffer(key,dtype=np.float64).reshape(4,4))/2)

def bank_julia(bfields,a):
 if a==0:return I32
 row=ADDR[a];i=INDEX[tuple(row['site'])];u,links,_=bfields
 if row['kind']=='inverse_coframe_column':return creator_julia_cached(np.ascontiguousarray(u[i,:,row['direction']]).tobytes())
 return link_julia_cached(np.ascontiguousarray(links[i,row['direction']]).tobytes())

def omega_entry(bfields,a,i,j):
 assert 0<=a<4096 and 0<=i<32 and 0<=j<32
 return bank_julia(bfields,a)[j,i]*ANCHOR if a<A else 0.

def o_entry(bfields,out_address,in_address):
 # Each is (a,input,output) in computational ordering. Padding is identity.
 x,y=out_address,in_address;anchor=(0,0,0); bx=omega_entry(bfields,*x);by=omega_entry(bfields,*y)
 dx=float(x==anchor);dy=float(y==anchor)
 return float(x==y)+bx*dy-dx*by+(bx*(ANCHOR*dy-by)-dx*(dy-ANCHOR*by))/(1+ANCHOR)

def car_column(bfields,site,car_input,right_input):
 # Sum over output CAR at fixed internal site and RIGHT. Protected oldRIGHT is identity.
 assert 0<=car_input<16 and 0<=right_input<128
 site=tuple(site);m=car_map(bfields[2][INDEX[site]])
 return [(site,int(j),right_input,float(m[j,car_input])) for j in range(16) if m[j,car_input]!=0]

def target_entry_state(bfields,site,grade,right):
 return local_m(bfields[2][INDEX[tuple(site)]])[grade]*chi_ref(site,right)

@lru_cache(maxsize=1)
def site_matrix():
 # O_chi (G^tensor 8)^T on ALL 256 computational columns; born v^tensor8.
 G=np.array([[ROOTP,-PVAL],[PVAL,ROOTP]]);B=G
 for _ in range(7):B=np.kron(B,G)
 return mm(rot(CHI,anchor=0),B.T)

def site_entry(out,in_):
 assert 0<=out<256 and 0<=in_<256
 return site_matrix()[out,in_]

def choi_b_vector(bfields):
 """One target vector in the full 22-wire space, 32 MiB, no dense operator."""
 b=np.zeros(D)
 for a in range(A):b[a*1024:(a+1)*1024]=bank_julia(bfields,a).T.reshape(1024)*ANCHOR
 return b

def raw_choi_column(bfields,in_address):
 """Full column of O_b (G^tensor22)^T from the 22 RAW born wires.
 Return one vector, not the 2^22 by 2^22 matrix. Includes the true padded input
 and output columns: after B^T, padding is generally mixed before O_b.
 """
 a,i,j=in_address;assert 0<=a<4096 and 0<=i<32 and 0<=j<32
 y=(a<<10)|(i<<5)|j;G=np.array([[ROOTP,-PVAL],[PVAL,ROOTP]])
 v=np.array([1.])
 for shift in range(21,-1,-1):v=np.kron(v,G[(y>>shift)&1,:])
 b=choi_b_vector(bfields);dot=float(np.dot(b,v));v0=v[0];K=b*v0;K[0]-=dot
 K2=b*(ANCHOR*v0-dot);K2[0]-=v0-ANCHOR*dot
 return v+K+K2/(1+ANCHOR)
