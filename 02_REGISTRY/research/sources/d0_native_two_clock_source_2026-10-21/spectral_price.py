"""High-precision exact-spectrum evaluation; finite n is held fixed in all field derivatives.

The 256 Pauli error probabilities evaluate the coherent-record SPECTRUM.
They are not the Shannon distribution on 128**n physical histories.
"""
import numpy as np
import mpmath as mp
from itertools import product
from scipy.optimize import brentq
mp.mp.dps=100
pop=lambda s: bin(int(s)).count("1")
keys=[]
for s in range(256):
 k=pop(s); o=sum(pop((s>>(2*r))&3)==1 for r in range(4))
 u=(-1)**(k-((s>>0)&1))
 keys.append((k,o,u))
classes=sorted(set(keys)); ci={key:i for i,key in enumerate(classes)}
chi=np.array([[(-1)**((pop(s)*pop(g)-pop(s&g))%2) for g in range(256)] for s in range(256)],dtype=np.int64)
co=np.zeros((256,len(classes)),dtype=np.int64)
for s,key in enumerate(keys): co[:,ci[key]]+=chi[s,:]
p=(mp.sqrt(5)-1)/2; ell=mp.log(1/p)

def evaluate(L,a,n=None,derivatives=True):
 h=mp.mpf(1)/L; a=mp.mpf(a); n=int(128*L**4) if n is None else int(n)
 v=h*a; b=mp.sqrt(1-v*v); q=p*p*v*v*4*mp.sin(mp.pi*h)**2/64
 qa=2*q/a; qaa=2*q/a**2
 ba=-h*h*a/b; baa=-h*h/b**3
 wi=(1+b)**2/4; wm=v*v/16; wz=(1-b)**2/16
 wia=(1+b)*ba/2; wmaa=h*h/8; wma=h*h*a/8; wza=-(1-b)*ba/8
 wiaa=(ba*ba+(1+b)*baa)/2; wzaa=(ba*ba-(1-b)*baa)/8
 vv=[]; dd=[]; ee=[]
 for k,o,u in classes:
  x=(-1)**k*(8-2*k); y=4-2*o
  t=wi+wm*x+wz*y; ta=wia+wma*x+wza*y; taa=wiaa+wmaa*x+wzaa*y
  z=q*(u*t-1); za=qa*(u*t-1)+q*u*ta; zaa=qaa*(u*t-1)+2*qa*u*ta+q*u*taa
  l=mp.exp(n*mp.log1p(z)); dlog=n*za/(1+z)
  vv.append(l); dd.append(l*dlog); ee.append(l*(dlog*dlog+n*(zaa/(1+z)-(za/(1+z))**2)))
 probs=[]; dp=[]; d2p=[]
 for row in co:
  probs.append(mp.fsum(int(c)*v for c,v in zip(row,vv))/256)
  dp.append(mp.fsum(int(c)*v for c,v in zip(row,dd))/256)
  d2p.append(mp.fsum(int(c)*v for c,v in zip(row,ee))/256)
 if n<8:
  # The n<8 word space may have exact zero Choi eigenvalues for every a.
  # Only roundoff-size zeros in value AND both jets may be removed.
  tol=mp.mpf(10)**(-mp.mp.dps+12)
  for j,x in enumerate(probs):
   if abs(x)<tol:
    if abs(dp[j])>=tol or abs(d2p[j])>=tol:
     raise ArithmeticError('uncontrolled support birth')
    probs[j]=dp[j]=d2p[j]=mp.mpf(0)
 if min(probs)<0 or (n>=8 and min(probs)<=0):
  raise ArithmeticError('insufficient precision or nonfaithful spectrum')
 positive=[j for j,x in enumerate(probs) if x>0]
 ent=-mp.fsum(probs[j]*mp.log(probs[j]) for j in positive)/ell
 enta=-mp.fsum(dp[j]*mp.log(probs[j]) for j in positive)/ell
 entaa=-mp.fsum(d2p[j]*mp.log(probs[j])+dp[j]*dp[j]/probs[j] for j in positive)/ell
 g=q*(1-b)/4
 return dict(f=n*p*q-ent,fa=n*p*qa-enta,faa=n*p*qaa-entaa,H=ent,Ha=enta,Haa=entaa,pi=probs,dpi=dp,q=q,gap=g,n=n,ngap=n*g,charge_surplus=n*p*q)

def limit(a):
 a=mp.mpf(a); tau=8*mp.pi**2*p*p*a*a; c=mp.exp(-2*tau)
 x=(1+c)/2
 ent=-(x*mp.log(x)+(1-x)*mp.log(1-x))/ell
 fp=p-c*mp.log((1+c)/(1-c))/ell
 return dict(tau=tau,f=p*tau-ent,fa=16*mp.pi**2*p*p*a*fp,H=ent)
