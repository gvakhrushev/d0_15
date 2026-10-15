"""Outward IEEE-754 intervals; existence is certified by a strict contraction."""
import numpy as np,json,time,argparse
from pathlib import Path
import sympy as sp
from nonlinear import residual,inverse,GEN,P,eta,weight
DOWN=-np.inf;UP=np.inf
class I:
 def __init__(self,l,h=None):self.l=np.asarray(l,dtype=float);self.h=np.asarray(l if h is None else h,dtype=float)
 def __add__(a,b):
  if not isinstance(b,I):b=I(b)
  return I(np.nextafter(a.l+b.l,DOWN),np.nextafter(a.h+b.h,UP))
 __radd__=__add__
 def __neg__(a):return I(-a.h,-a.l)
 def __sub__(a,b):return a+(-b if isinstance(b,I) else -I(b))
 def __rsub__(a,b):return I(b)+(-a)
 def __mul__(a,b):
  if not isinstance(b,I):b=I(b)
  four=np.stack(np.broadcast_arrays(a.l*b.l,a.l*b.h,a.h*b.l,a.h*b.h))
  return I(np.nextafter(four.min(axis=0),DOWN),np.nextafter(four.max(axis=0),UP))
 __rmul__=__mul__
 def __truediv__(a,b):
  if not isinstance(b,I):b=I(b)
  if np.any((b.l<=0)&(b.h>=0)):raise ArithmeticError('interval division by zero')
  return a*I(np.nextafter(1/b.h,DOWN),np.nextafter(1/b.l,UP))
 def __matmul__(a,b):
  if a.l.ndim!=2 or b.l.ndim!=2 or a.l.shape[1]!=b.l.shape[0]:raise ValueError('matrix shape')
  out=I(np.zeros((a.l.shape[0],b.l.shape[1])))
  for k in range(a.l.shape[1]):out=out+a[:,k:k+1]*b[k:k+1,:]
  return out
 def __getitem__(a,key):return I(a.l[key],a.h[key])
 @property
 def T(a):return I(a.l.T,a.h.T)
 def absup(a):return np.maximum(np.abs(a.l),np.abs(a.h))
 def scalar(a):return I(a.l.item(),a.h.item())

def inv4(a):
 n=a.l.shape[0];w=I(np.concatenate([a.l,np.eye(n)],axis=1),np.concatenate([a.h,np.eye(n)],axis=1))
 for k in range(n):
  if not (w.l[k,k]>0 or w.h[k,k]<0):raise ArithmeticError('unproved pivot')
  row=w[k:k+1,:]/w[k,k];w.l[k:k+1,:]=row.l;w.h[k:k+1,:]=row.h
  for j in range(n):
   if j==k:continue
   rr=w[j:j+1,:]-w[j,k]*row;w.l[j:j+1,:]=rr.l;w.h[j:j+1,:]=rr.h
 return w[:,n:]

def inj(x):
 y=np.asarray(x,dtype=float);return I(np.nextafter(y,DOWN),np.nextafter(y,UP))

def setup(A,radius,second=True):
 L=len(A);eye=I(np.eye(4));g=[I(x) for x in GEN];met=I(eta);items={}
 for n in range(L):
  for r in range(4):
   v=A[n,6*r:6*r+6];aa=I(np.nextafter(v-radius,DOWN),np.nextafter(v+radius,UP));X=I(np.zeros((4,4)))
   for k in range(6):X=X+aa[k]*g[k]
   S=inv4(eye-X*.5);U=S@(eye+X*.5);d=[S@g[k]@S for k in range(6)]
   dd=[[((S@g[l]@S@g[k]@S)+(S@g[k]@S@g[l]@S))*.5 for l in range(6)] for k in range(6)] if second else []
   items[n,r,1]=(U,d,dd);items[n,r,-1]=(met@U.T@met,[met@x.T@met for x in d],[[met@x.T@met for x in row] for row in dd])
 return items

def calc(A,radius,with_hessian=True,start=0,stop=8):
 L=len(A);vc=24*L;grad=I(np.zeros(vc));H=I(np.zeros((vc,vc)));allU=setup(A,radius,with_hessian);eye=I(np.eye(4))
 sq2=I(np.nextafter(np.sqrt(2.),DOWN),np.nextafter(np.sqrt(2.),UP))
 from fractions import Fraction
 if not Fraction.from_float(float(sq2.l))**2<2<Fraction.from_float(float(sq2.h))**2:raise ArithmeticError('sqrt2 bracket')
 fp=inj(.01)
 if not Fraction.from_float(float(fp.l))<=Fraction(1,100)<=Fraction.from_float(float(fp.h)):raise ArithmeticError('1/100 bracket')
 cs=[I(1),sq2*.5,I(0),-sq2*.5,I(-1),-sq2*.5,I(0),sq2*.5];f=[1+inj(.01)*cs[n] for n in range(L)]
 def addg(k,v):
  val=grad[k]+v;grad.l[k]=val.l;grad.h[k]=val.h
 def addh(k,l,v):
  val=H[k,l]+v;H.l[k,l]=val.l;H.h[k,l]=val.h
 for n in range(start,stop):
  ee=[I(1),I(1),f[n],f[n]]
  for r,s in P:
   ids=[(n,r,1),((n+(r==1))%L,s,1),((n+(s==1))%L,r,-1),(n,s,-1)]
   w0=weight(np.eye(4),r,s)[P.index((r,s))]*eta[s,s];u,v=[j for j in range(4) if j not in (r,s)];coef=ee[u]*ee[v]*w0*.5
   for sign,ls in [(1,ids),(-1,[(m,a,-sg) for m,a,sg in ids[::-1]])]:
    FF=[allU[z][0] for z in ls];prefix=[eye]
    for F in FF:prefix.append(prefix[-1]@F)
    suffix=[None]*5;suffix[4]=eye
    for i in range(3,-1,-1):suffix[i]=FF[i]@suffix[i+1]
    left=[];right=[]
    for i,(m,a,sg) in enumerate(ls):
     U,d,dd=allU[m,a,sg];base=24*m+6*a;pr=prefix[i][r:r+1,:];po=suffix[i+1][:,s:s+1]
     left.append([pr@d[k] for k in range(6)]);right.append([d[k]@po for k in range(6)])
     for k in range(6):addg(base+k,coef*sign*(left[i][k]@po).scalar())
     if with_hessian:
      for k in range(6):
       for l in range(k,6):
        z=coef*sign*(pr@dd[k][l]@po).scalar();addh(base+k,base+l,z)
        if k!=l:addh(base+l,base+k,z)
    if with_hessian:
     for i in range(4):
      mid=eye
      for j in range(i+1,4):
       if j>i+1:mid=mid@FF[j-1]
       basei=24*ls[i][0]+6*ls[i][1];basej=24*ls[j][0]+6*ls[j][1];lm=[li@mid for li in left[i]]
       for k in range(6):
        for l in range(6):
         val=coef*sign*(lm[k]@right[j][l]).scalar();addh(basei+k,basej+l,val);addh(basej+l,basei+k,val)
  print('interval site',n,'done',flush=True)
 return grad,H

def preconditioner(L):
 from algebra import inverse_coefficients
 N=inverse_coefficients()
 Q=sp.zeros(L)
 for i in range(L):Q[i,i]+=14;Q[i,(i+2)%L]+=1;Q[i,(i-2)%L]+=1
 QI=Q.inv();bb=sp.zeros(24*L)
 for i in range(L):
  for j in range(L):bb[24*i:24*i+24,24*j:24*j+24]=sum((QI[(i+k)%L,j]*mat for k,mat in N.items()),sp.zeros(24))
 enclosure=inj(np.array(bb.tolist(),dtype=float))
 from fractions import Fraction
 for i in range(24*L):
  for j in range(24*L):
   value=Fraction(int(bb[i,j].p),int(bb[i,j].q))
   if not Fraction.from_float(enclosure.l[i,j])<=value<=Fraction.from_float(enclosure.h[i,j]):
    raise ArithmeticError('rational preconditioner conversion was not enclosed')
 return enclosure

def rowsum_out(a):
 z=np.zeros(a.shape[0])
 for k in range(a.shape[1]):z=np.nextafter(z+a[:,k],UP)
 return float(z.max())
