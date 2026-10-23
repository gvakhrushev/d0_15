#!/usr/bin/env python3
"""Original ALL 718 Book edges: unique flow Cost−Info/pressure, first source,
and strictly negative historical Schur correction. Not full D0→GR.
"""
import math
import numpy as np
import sympy as s

phi=(1+math.sqrt(5))/2
p=1/phi
ell=math.log(phi)
V=list(range(33))
zone={u:(0 if u<9 else 1 if u<20 else 2) for u in V}
E=[(u,v) for u in V for v in V if zone[u]!=zone[v]]
assert len(E)==718

def native_cost(u,v,t):
    return 1+t*(zone[u]!=zone[v] and {zone[u],zone[v]}=={0,1})

def native_flow(t):
    K=np.zeros((33,33))
    for u,v in E:K[u,v]=phi**(-native_cost(u,v,t))
    eigen,vec=np.linalg.eigh(K)
    lam=eigen[-1]
    r=vec[:,-1]
    if sum(r)<0:r=-r
    assert min(r)>0
    pi=r*r
    P=K*r[None,:]/(lam*r[:,None])
    f=pi[:,None]*P
    assert np.max(np.abs(P.sum(axis=1)-1))<1e-12
    assert abs(f.sum()-1)<1e-12
    assert np.max(np.abs(f.sum(axis=0)-pi))<1e-12
    return lam,r,pi,P,f

R,a=s.symbols('R a',positive=True)
F=R**3-(260+99*a*a)*R-2574*a
assert s.factor(F.subs(a,1))==R**3-359*R-2574
rho=max(float(s.re(v)) for v in s.nroots(F.subs(a,1)))
Fr=s.diff(F,R)
Ra=-s.diff(F,a)/Fr
Raa=-(s.diff(F,R,2)*Ra**2+2*s.diff(F,R,a)*Ra+s.diff(F,a,2))/Fr
first=float((Ra/R).subs({R:rho,a:1}).evalf())
second=float((-s.log((1+s.sqrt(5))/2)*
  ((Ra+Raa)/R-(Ra/R)**2)).subs({R:rho,a:1}).evalf())
assert 0.29476222<first<0.29476223
assert -0.12972844<second<-0.12972841
lam,r,pi,P,f=native_flow(0)
assert abs(lam/p-rho)<1e-11

action=0;KL=0
for u,v in E:
    ff=f[u,v]
    action+=ff*(native_cost(u,v,0)+math.log(ff/pi[u])/ell)
    KL+=ff*math.log(ff/(pi[u]*P[u,v]))/ell
assert abs(action-(KL-math.log(lam)/ell))<1e-12
assert abs(KL)<1e-12
massAB=sum(f[u,v] for u,v in E if {zone[u],zone[v]}=={0,1})
assert abs(massAB-first)<1e-12

# A real original balanced tangent exchanging the 2-cycles A<->B and A<->C.
q=np.zeros((33,33))
q[0,9]=q[9,0]=.5
q[0,20]=q[20,0]=-.5
assert abs(q.sum())<1e-14
assert np.max(np.abs(q.sum(axis=0)-q.sum(axis=1)))<1e-14
row=q.sum(axis=1)
H=(sum(q[u,v]**2/f[u,v] for u,v in E if q[u,v]!=0)-
   sum(row[u]**2/pi[u] for u in V if row[u]!=0))/ell
assert H>0
assert sum(q[u,v] for u,v in E if {zone[u],zone[v]}=={0,1})==1

# Original primitive edge cost s_uv=1+t*chi_AB has zero direct Hessian,
# so nonzero second derivative of reduced -log_phi lambda is 100%
# the genuine negative history-relaxation Schur correction.
def effective(t):return -math.log(native_flow(t)[0])/ell
step=.002
finitefirst=(effective(step)-effective(-step))/(2*step)
finitesecond=(effective(step)-2*effective(0)+effective(-step))/step**2
assert abs(finitefirst-first)<1e-6
assert abs(finitesecond-second)<1e-6
print('PASS exact original tripartite 718-edge primitive Book Cost and Perron flow')
print('PASS induced ALL-path Cost−Info rate = conditional KL − absolute log_phi Perron')
print('PASS unique balanced stationary flow and first source = original mean edge Cost source')
print('PASS native mixed history Cost covector nonzero on balanced flow tangent')
print('PASS strictly positive history Hessian and negative relaxed effective Hessian')
print('rho=',rho,'native_lambda=',lam)
print('first=',first,'finite=',finitefirst)
print('second=',second,'finite=',finitesecond)
print('positive_flow_tangent_H=',H)
print('SCOPE original scalar macro history only; full Book ordered memory & Einstein open')
