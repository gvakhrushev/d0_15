#!/usr/bin/env python3
import json
import math
import numpy as np
# Exact coefficient arithmetic after clearing the common denominators.
def add(*items):
 out={}
 for P in items:
  for k,v in P.items():
   out[k]=out.get(k,0)+v
 return {k:v for k,v in out.items() if v}
def mul(P,Q):
 out={}
 for (a,b),v in P.items():
  for (c,d),w in Q.items():
   k=(a+c,b+d);out[k]=out.get(k,0)+v*w
 return {k:v for k,v in out.items() if v}
def scale(n,P):
 return {k:n*v for k,v in P.items() if n*v}
one={(0,0):1};Z={(1,0):1};T={(0,1):1}
A=add(one,scale(-1,mul(Z,T)))
Hnumer=scale(2,mul(Z,add(one,scale(-2,T),mul(Z,T))))
Hexpanded=add(scale(2,mul(mul(Z,add(one,scale(-2,T))),A)),scale(4,mul(mul(Z,Z),mul(add(one,scale(-1,T)),T))))
checks={
 'hermitian_coefficient_exact_polynomial':not add(Hnumer,scale(-1,Hexpanded)),
 'mode_gap_exact_polynomial':not add(scale(2,mul(Z,A)),scale(-1,Hnumer),scale(-4,mul(Z,mul(add(one,scale(-1,Z)),T)))),
}
if not all(checks.values()):
 raise RuntimeError(checks)
p=(math.sqrt(5)-1)/2
c=math.sqrt(p)
s=p
z0=2**-20
rng=np.random.default_rng(172928)

def invsqrt(M):
 vals,vecs=np.linalg.eigh(M)
 return (vecs*(1/np.sqrt(vals)))@vecs.conj().T

def direct_price(X,Y,z):
 r=X.shape[0]
 I=np.eye(r)
 A=np.vstack((I,X))@invsqrt(I+X.conj().T@X)
 B=np.vstack((c*I+s*Y,-s*I+c*Y))@invsqrt(I+Y.conj().T@Y)
 # Read the original return, not the mixed-Hessian formula.
 P0=A@A.conj().T
 P1=B@B.conj().T
 F=P0@(np.eye(2*r)-P1)@P0
 vals=np.linalg.eigvalsh((F+F.conj().T)/2)
 return -float(np.log1p(-z*vals).sum())/z

def predicted(X,Y,z):
 Hx=(X+X.conj().T)/2; Ax=(X-X.conj().T)/2
 Hy=(Y+Y.conj().T)/2; Ay=(Y-Y.conj().T)/2
 aa=1-z*s*s
 h=2*(1-(2-z)*s*s)/(aa*aa)
 k=2/aa
 return -h*np.vdot(Hx,Hy).real-k*np.vdot(Ax,Ay).real

def mixed_fd(X,Y,z,h=0.004):
 stencil=((-2,1),(-1,-8),(1,8),(2,-1))
 return sum(ci*cj*direct_price(i*h*X,j*h*Y,z) for i,ci in stencil for j,cj in stencil)/(144*h*h)

records=[]
for r in (1,2,3):
 for zz in (z0,0.2,0.7):
  for mode in ('mixed','hermitian','antihermitian'):
   X=rng.normal(size=(r,r))+1j*rng.normal(size=(r,r))
   Y=rng.normal(size=(r,r))+1j*rng.normal(size=(r,r))
   if mode=='hermitian':
    X=(X+X.conj().T)/2;Y=(Y+Y.conj().T)/2
   elif mode=='antihermitian':
    X=(X-X.conj().T)/2;Y=(Y-Y.conj().T)/2
   X/=np.linalg.norm(X);Y/=np.linalg.norm(Y)
   actual=mixed_fd(X,Y,zz);expect=predicted(X,Y,zz)
   err=abs(actual-expect)
   if err>2e-7:
    raise RuntimeError((r,zz,mode,actual,expect,err))
   records.append(dict(rank=r,z=zz,mode=mode,error=err))

a0=1-z0*p*p
kh0=2*z0*(1-(2-z0)*p*p)/a0**2
ka0=2*z0/a0
th=math.asin(p)
f=lambda d:-math.log1p(-z0*math.sin(d)**2)
fpp=lambda d:2*z0*(1-(2-z0)*math.sin(d)**2)/(1-z0*math.sin(d)**2)**2
actual_two=f(2*th);sum_two=2*f(th)
actual_mixed=-fpp(2*th);glued_mixed=-fpp(th)/2
if not actual_two>sum_two or not actual_mixed>0 or not glued_mixed<0:
 raise RuntimeError('Golden gluing negative control failed')
print(json.dumps(dict(status='PASS',scope='finite original-return endpoint mixed Hessian, not physical admission or GR',symbolic=checks,derivative_checks=records,max_normalized_fd_error=max(x['error'] for x in records),golden_gain=dict(z=z0,kappa_H=kh0,kappa_A=ka0,inverse_norm=1/kh0,condition=ka0/kh0),gluing_control=dict(composed_price=actual_two,sum_step_prices=sum_two,difference=actual_two-sum_two,composed_mixed_hessian=actual_mixed,stationary_glued_mixed_hessian=glued_mixed)),indent=2))
