#!/usr/bin/env python3
"""Observer-positive complete CAR16 Julia/Choi test is local Lorentz covariant.
Consumes existing D0.Geometry.A4DObserverPositiveExterior. NOT selected full128.
"""
import numpy as np
eta=np.diag([1.,-1.,-1.,-1.]);eye=np.eye(4)
def E(i,j):
    A=np.zeros((4,4));A[i,j]=1.;return A
def boost(i,t):
    X=E(0,i)+E(i,0)
    return eye+np.sinh(t)*X+(np.cosh(t)-1)*(X@X)
def h(n):
    v=eta@n
    return -eta+2*np.outer(v,v)
S=[[i for i in range(4) if (mask>>i)&1] for mask in range(16)]
def exterior(M):
    return np.array([[0. if len(a)!=len(b) else np.linalg.det(M[np.ix_(a,b)]) if a else 1.
                      for b in S] for a in S])
def adj(M,H):return np.linalg.solve(H,M.T@H)
def measure(Uf,H):
    T=Uf/2
    C=adj(T,H)@T
    ev=np.linalg.eigvals(C)
    assert abs(ev.imag).max()<1e-12 and ev.real.max()<1-1e-9
    good=np.trace(C).real/16
    marked=(np.trace(T).real/16)**2
    rates=np.array([marked,good-marked,1-good])
    assert rates.min()>-1e-12 and abs(rates.sum()-1)<1e-12
    return rates
n=np.array([1.,0,0,0]);U=boost(1,.17);g=boost(2,.26)
np_=g@n;Up=g@U@np.linalg.inv(g)
H=h(n);Hp=h(np_)
assert np.linalg.eigvalsh(Hp).min()>0
assert np.linalg.norm(g.T@Hp@g-H)<1e-13
Q=exterior(H);Qp=exterior(Hp)
Lf=exterior(g);Uf=exterior(U);Ufp=exterior(Up)
assert np.linalg.eigvalsh(Qp).min()>0
assert np.linalg.norm(Lf.T@Qp@Lf-Q)<1e-12
assert np.linalg.norm(Ufp@Lf-Lf@Uf)<1e-12
p0=measure(Uf,Q);p1=measure(Ufp,Qp)
assert np.linalg.norm(p0-p1)<1e-13
bad=measure(Ufp,Q)
assert abs(bad[0]-p0[0])<1e-13
assert abs((bad[0]+bad[1])-(p0[0]+p0[1]))>1e-4
print('PASS observer co-moving all-3 CAR16 Julia rates:',p0)
print('PASS fixed Euclidean metric fails complete local Lorentz frame covariance:',bad)
print('GR_closed=false: observer gauge and mathematical tester, not selected physical full128 action')
