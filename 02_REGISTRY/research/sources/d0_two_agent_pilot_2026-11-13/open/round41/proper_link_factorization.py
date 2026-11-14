#!/usr/bin/env python3
"""Diagnostic evaluator of exact SO+(1,3) proper-link Julia factorization.

Float64 only evaluates named target matrices and is NOT a native compiler or
an interval certificate. Near-zero branch is approximate in this evaluator;
the exact branch and its proof are stated in the accompanying report.
"""
from pathlib import Path
import importlib.util,sys
import numpy as np
P=Path(__file__).resolve().parent
BASE=P.parent/'round25/targets.py'
spec=importlib.util.spec_from_file_location('b41_b25_targets',BASE);t=importlib.util.module_from_spec(spec);sys.modules[spec.name]=t;spec.loader.exec_module(t)
def factor(U,tol=1e-13):
 """Return float diagnostic L,D,R, singular max and zero-branch flag."""
 A=t.T.T@U@t.T;gamma=float(A[0,0]);sp=A[1:,0];h=float(np.linalg.norm(sp))
 if h<tol:
  # Only the mathematical h=0 branch is exact; numerical threshold is diagnostic.
  return np.eye(4),np.ones(4),U.T,1.,True
 n=sp/h; j=int(np.argmin(abs(n)));v=np.eye(3)[:,j]-n[j]*n;v/=np.linalg.norm(v);O3=np.column_stack((n,v,np.cross(n,v)))
 O=np.eye(4);O[1:,1:]=O3
 B=np.eye(4);B[0,0]=gamma;B[0,1:]=h*n;B[1:,0]=h*n;B[1:,1:]+=(gamma-1)*np.outer(n,n)
 Binv=B.copy();Binv[0,1:]*=-1;Binv[1:,0]*=-1
 K=Binv@A
 P4=np.eye(4);P4[:2,:2]=np.array([[1,1],[1,-1]])/np.sqrt(2);P4[3,3]=-1
 L=t.T@O@P4;R=t.T@K.T@O@P4
 D=np.array([gamma+h,gamma-h,1.,1.])
 return L,D,R,float(gamma+h),False

def so4_givens(M):
 """Diagnostic six-plane SO(4) elimination; use exact zero predicate in a compiler."""
 Q=np.array(M,dtype=float).copy();elim=[]
 for col in range(3):
  for row in range(3,col,-1):
   a,b=Q[col,col],Q[row,col];radius=float(np.hypot(a,b))
   c,si=(1.,0.) if radius==0 else (a/radius,-b/radius)
   G=np.eye(4);G[col,col]=G[row,row]=c;G[row,col]=si;G[col,row]=-si
   Q=t.mm(G,Q);elim.append((col,row,c,si))
 # Chronological factors of M are inverse eliminators in reversed order.
 return [(i,j,c,-si) for i,j,c,si in reversed(elim)],Q

def compose_givens(factors):
 M=np.eye(4)
 for i,j,c,si in factors:
  G=np.eye(4);G[i,i]=G[j,j]=c;G[j,i]=si;G[i,j]=-si;M=t.mm(G,M)
 return M

def fock_pairs(i,j):
 order=t.ORDER;between=order[min(order.index(i),order.index(j))+1:max(order.index(i),order.index(j))]
 rest=[q for q in range(4) if q not in (i,j)]
 for bits in range(4):
  m=sum(((bits>>k)&1)<<q for k,q in enumerate(rest));sgn=(-1)**sum(bool(m&(1<<q)) for q in between)
  yield m|(1<<i),m|(1<<j),sgn

def diagonal_julia(diag):
 vals=np.array([np.prod([diag[q] for q in range(4) if mask>>q&1])/2 for mask in range(16)])
 assert max(abs(vals))<1
 D=np.diag(vals);S=np.diag(np.sqrt(1-vals*vals))
 return np.block([[D,S],[S,-D]])

def factorized_julia(U):
 L,d,R,r,z=factor(U); LF=t.exterior(L);RF=t.exterior(R); zero=np.zeros((16,16))
 left=np.block([[LF,zero],[zero,RF]]);right=np.block([[RF.T,zero],[zero,LF.T]])
 return t.mm(t.mm(left,diagonal_julia(d)),right),(L,d,R,r,z)
