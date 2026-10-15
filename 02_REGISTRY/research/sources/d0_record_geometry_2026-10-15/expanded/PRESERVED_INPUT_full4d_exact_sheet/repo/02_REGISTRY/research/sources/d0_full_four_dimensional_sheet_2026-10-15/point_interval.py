"""80-decimal-digit outward mpmath interval residual, at an exactly dyadic center."""
import mpmath as mp
import numpy as np,json,time
from pathlib import Path
from fractions import Fraction
from interval_check import GN,P,ET,neighbor,I,rowsup
mp.iv.dps=80
iv=mp.iv;ROOT=Path(__file__).parent

def exact(x):
 f=Fraction(float(x)) if isinstance(x,(float,np.floating)) else Fraction(x)
 return iv.mpf(f.numerator)/f.denominator

def inverse4(M):
 n=4;W=iv.matrix(n,2*n)
 for i in range(n):
  for j in range(n):W[i,j]=M[i,j];W[i,n+j]=int(i==j)
 for k in range(n):
  piv=W[k,k]
  if piv.a<=0<=piv.b:raise ArithmeticError('zero pivot interval')
  rr=[W[k,j]/piv for j in range(2*n)]
  for j in range(2*n):W[k,j]=rr[j]
  for i in range(n):
   if i==k:continue
   c=W[i,k]
   for j in range(2*n):W[i,j]=W[i,j]-c*rr[j]
 return W[:,n:]

def endpoint_frac(ep):
 sign,man,ex,bc=ep
 return (-1 if sign else 1)*Fraction(int(man))*(Fraction(2)**int(ex))

def to_I(vals):
 lo=[];hi=[]
 for x in vals:
  lq,hq=map(endpoint_frac,x._mpi_)
  lv,hv=float(lq),float(hq)
  if Fraction(lv)>lq:lv=np.nextafter(lv,-np.inf)
  if Fraction(hv)<hq:hv=np.nextafter(hv,np.inf)
  lo.append(lv);hi.append(hv)
 return I(np.array(lo),np.array(hi))

def residual_interval(A):
 A=A.reshape(16,24);U={};eye=iv.eye(4);et=iv.matrix(ET.tolist());gens=[iv.matrix(x.tolist()) for x in GN]
 out=[iv.mpf(0) for _ in range(384)]
 for m in range(16):
  for r in range(4):
   X=iv.zeros(4)
   for k in range(6):X+=exact(A[m,6*r+k])*gens[k]
   S=inverse4(eye-X/2);u=S*(eye+X/2);ds=[S*g*S for g in gens]
   U[m,r,1]=(u,ds);U[m,r,-1]=(et*u.T*et,[et*d.T*et for d in ds])
 cos=[1,0,-1,0]
 for m in range(16):
  x,y=divmod(m,4);f=exact(Fraction(1)+Fraction(cos[x],100)+Fraction(cos[y],1000));ee=[iv.mpf(1),iv.mpf(1),f,f]
  for r,s in P:
   other=[i for i in range(4) if i not in (r,s)];coef=ee[other[0]]*ee[other[1]]/2
   ids=[(m,r,1),(neighbor(m,r,4),s,1),(neighbor(m,s,4),r,-1),(m,s,-1)]
   for sg,ls in [(1,ids),(-1,[(k,a,-z) for k,a,z in ids[::-1]])]:
    fac=[U[k][0] for k in ls];pre=[eye]
    for z in fac:pre.append(pre[-1]*z)
    suf=[None]*5;suf[4]=eye
    for i in range(3,-1,-1):suf[i]=fac[i]*suf[i+1]
    for i,(k,a,z) in enumerate(ls):
     pr=pre[i][r:r+1,:];po=suf[i+1][:,s:s+1]
     for j,d in enumerate(U[k,a,z][1]):out[24*k+6*a+j]+=sg*coef*(pr*d*po)[0,0]
 return to_I(out)
