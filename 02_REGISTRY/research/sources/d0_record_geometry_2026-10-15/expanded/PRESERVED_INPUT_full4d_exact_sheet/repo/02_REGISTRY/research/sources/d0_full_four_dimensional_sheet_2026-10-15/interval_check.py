"""Directed IEEE binary64 Hessian enclosures, independent high-precision
interval residual. No floating-point small residual is a zero certificate.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
import numpy as np
from fractions import Fraction
from itertools import combinations
import json,sys,time
from pathlib import Path
ROOT=Path(__file__).parent
P=list(combinations(range(4),2));ET=np.diag([1.,-1.,-1.,-1.]);GN=[]
for a,b in P:
 X=np.zeros((4,4));X[a,b]=1;X[b,a]=-ET[a,a]*ET[b,b];GN.append(X)
GN=np.array(GN);DOWN=-np.inf;UP=np.inf
class I:
 __array_priority__=10000
 def __init__(self,l,h=None): self.l=np.array(l,float,copy=True);self.h=np.array(l if h is None else h,float,copy=True)
 def __add__(a,b):
  b=b if isinstance(b,I) else I(b)
  return I(np.nextafter(a.l+b.l,DOWN),np.nextafter(a.h+b.h,UP))
 __radd__=__add__
 def __neg__(a):return I(-a.h,-a.l)
 def __sub__(a,b):return a+(-(b if isinstance(b,I) else I(b)))
 def __rsub__(a,b):return I(b)-a
 def __mul__(a,b):
  b=b if isinstance(b,I) else I(b)
  vs=np.stack(np.broadcast_arrays(a.l*b.l,a.l*b.h,a.h*b.l,a.h*b.h))
  return I(np.nextafter(vs.min(0),DOWN),np.nextafter(vs.max(0),UP))
 __rmul__=__mul__
 def __truediv__(a,b):
  b=b if isinstance(b,I) else I(b)
  if np.any((b.l<=0)&(b.h>=0)): raise ArithmeticError('unproved denominator')
  return a*I(np.nextafter(1/b.h,DOWN),np.nextafter(1/b.l,UP))
 def __matmul__(a,b):
  b=b if isinstance(b,I) else I(b)
  if a.l.shape[-1]!=b.l.shape[-2]:raise ValueError('matmul shape')
  dims=np.broadcast_shapes(a.l.shape[:-2],b.l.shape[:-2]);out=I(np.zeros(dims+(a.l.shape[-2],b.l.shape[-1])))
  for k in range(a.l.shape[-1]):out=out+a[...,k:k+1]*b[...,k:k+1,:]
  return out
 def __getitem__(a,k):return I(a.l[k],a.h[k])
 def reshape(a,*shape):return I(a.l.reshape(*shape),a.h.reshape(*shape))
 def swapaxes(a,i,j):return I(np.swapaxes(a.l,i,j),np.swapaxes(a.h,i,j))
 @property
 def T(a):return a.swapaxes(-1,-2)
 def absup(a):return np.maximum(abs(a.l),abs(a.h))

def rational(q):
 q=Fraction(q);v=float(q);lo=hi=v
 if Fraction.from_float(v)>q:lo=np.nextafter(v,DOWN)
 if Fraction.from_float(v)<q:hi=np.nextafter(v,UP)
 return I(lo,hi)

def inv(a):
 n=a.l.shape[0];w=I(np.concatenate([a.l,np.eye(n)],1),np.concatenate([a.h,np.eye(n)],1))
 for k in range(n):
  rr=w[k:k+1,:]/w[k,k];w.l[k:k+1,:]=rr.l;w.h[k:k+1,:]=rr.h
  for j in range(n):
   if j==k:continue
   row=w[j:j+1,:]-w[j,k]*rr;w.l[j:j+1,:]=row.l;w.h[j:j+1,:]=row.h
 return w[:,n:]

def stack(xs,axis=0):return I(np.stack([x.l for x in xs],axis),np.stack([x.h for x in xs],axis))
def setup(A,rad):
 n=len(A);res={};eye=I(np.eye(4));g=I(GN);et=I(ET)
 for ix in range(n):
  for r in range(4):
   a=A[ix,6*r:6*r+6];a=I(np.nextafter(a-rad,DOWN),np.nextafter(a+rad,UP));X=I(np.zeros((4,4)))
   for k in range(6):X=X+a[k]*g[k]
   S=inv(eye-X*.5);U=S@(eye+X*.5);d=S@g@S
   dd=((d.reshape(6,1,4,4)@g.reshape(1,6,4,4)@S)+(d.reshape(1,6,4,4)@g.reshape(6,1,4,4)@S))*.5
   res[ix,r,1]=(U,d,dd)
   res[ix,r,-1]=(et@U.T@et,et@d.T@et,et@dd.T@et)
 return res

def neighbor(n,r,L):
 x,y=divmod(n,L)
 if r==1:x=(x+1)%L
 if r==2:y=(y+1)%L
 return x*L+y

def frame_f(n,L=4):
 x,y=divmod(n,L);c=[1,0,-1,0]
 return rational(1+Fraction(c[x],100)+Fraction(c[y],1000))

def hessian_enclosure(A,rad,keep_bloch=False):
 L=4;n=L*L;vc=24*n;H=I(np.zeros((vc,vc)));UU=setup(A,rad);eye=I(np.eye(4))
 bloch={}
 def add(ix,jx,block,ex=(0,0)):
  if keep_bloch:
   if ex not in bloch:bloch[ex]=I(np.zeros((vc,vc)))
   xx=slice(ix,ix+6); yy=slice(jx,jx+6); vv=bloch[ex][xx,yy]+block
   bloch[ex].l[xx,yy]=vv.l;bloch[ex].h[xx,yy]=vv.h
  x=slice(ix,ix+6);y=slice(jx,jx+6);rr=H[x,y]+block;H.l[x,y]=rr.l;H.h[x,y]=rr.h
 # At a diagonal coframe the literal G2*STAR weight contracted with eta
 # on every upper (r,s) odd entry is +1, checked independently in verify.
 for m in range(n):
  ee=[I(1),I(1),frame_f(m),frame_f(m)]
  for r,s in P:
   u,v=[a for a in range(4) if a not in (r,s)]
   coef=ee[u]*ee[v]*.5
   ids=[(m,r,1),(neighbor(m,r,L),s,1),(neighbor(m,s,L),r,-1),(m,s,-1)]
   offsets=[(0,0),(int(r==0),int(r==3)),(int(s==0),int(s==3)),(0,0)]
   for sg,ls,off in [(1,ids,offsets),(-1,[(k,a,-z) for k,a,z in ids[::-1]],offsets[::-1])]:
    ff=[UU[k][0] for k in ls];pre=[eye]
    for z in ff:pre.append(pre[-1]@z)
    suf=[None]*5;suf[4]=eye
    for i in range(3,-1,-1):suf[i]=ff[i]@suf[i+1]
    left=[];right=[]
    for i,(k,a,z) in enumerate(ls):
     U,d,dd=UU[k,a,z];pr=pre[i][r:r+1,:];po=suf[i+1][:,s:s+1]
     left.append((pr@d).reshape(6,4));right.append((d@po).reshape(6,4).T)
     dg=(pr@dd@po).reshape(6,6)*coef*sg
     add(24*k+6*a,24*k+6*a,dg)
    for i in range(4):
     mid=eye
     for j in range(i+1,4):
      if j>i+1:mid=mid@ff[j-1]
      dg=(left[i]@mid@right[j])*coef*sg
      ii=24*ls[i][0]+6*ls[i][1];jj=24*ls[j][0]+6*ls[j][1]
      ex=(off[j][0]-off[i][0],off[j][1]-off[i][1])
      add(ii,jj,dg,ex);add(jj,ii,dg.T,(-ex[0],-ex[1]))
  print('hessian site',m,flush=True)
 return (H,bloch) if keep_bloch else H

def rowsup(A):
 acc=np.zeros(A.shape[0])
 for k in range(A.shape[1]):acc=np.nextafter(acc+A[:,k],UP)
 return float(acc.max())
