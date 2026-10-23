#!/usr/bin/env python3
"""Bounded independent checks; exact algebra first, numerical sums diagnostic."""
import math
import sympy as s

a=s.symbols('a', real=True)
relation=a**4+a**2-1
def red(x):
    return s.cancel(s.rem(s.expand(x), relation, a))
def matrix_red(m):
    return m.applyfunc(red)
def same(x,y):
    assert matrix_red(x-y)==s.zeros(*x.shape), (x,y)

p=a*a
I=s.eye(2)
X=s.Matrix([[0,1],[1,0]])
Y=s.Matrix([[0,-s.I],[s.I,0]])
Z=s.diag(1,-1)
V=s.Matrix([[a,-p],[0,0],[0,0],[p,a]])
same(V.T*V,I)
c=p-p*p
b=2*a*p
same(V.T*s.kronecker_product(Z,I)*V, c*Z-b*X)
same(V.T*s.kronecker_product(X,X)*V, b*Z+c*X)
same(V.T*s.kronecker_product(Y,X)*V, Y)
assert red(c*c+b*b-1)==0

code=s.Matrix([[1,0],[0,0],[0,0],[0,1]])
observables=[s.eye(4),s.kronecker_product(Z,I),s.kronecker_product(X,X),s.kronecker_product(Y,X)]
compressed=[code.T*o*code for o in observables]
assert s.Matrix.hstack(*[o.reshape(4,1) for o in compressed]).rank()==4
psi=V[:,0]
rho=psi*psi.T
delta=s.diag(*[rho[j,j] for j in range(4)])
assert red(s.trace((rho-delta)*s.kronecker_product(X,X))-2*a*p)==0

q,L,A,B=s.symbols('q L A B', positive=True)
H=(-q*s.log(q)-(1-q)*s.log(1-q))/(L*q)
assert s.simplify(s.diff(H,q)-s.log(1-q)/(L*q*q))==0
mean_cost=B+A/q+1
mean_info=mean_cost+(s.log(q)+(1/q-1)*s.log(1-q))/L
assert s.simplify(mean_cost-mean_info-H)==0

phi=(1+math.sqrt(5))/2
pn=1/phi
lnphi=math.log(phi)
theta=math.asin(pn)
def entropy_geom(q):
    return (-q*math.log(q)-(1-q)*math.log1p(-q))/(lnphi*q)

receipts=[]
for k in (1,2,3,7):
    qn=math.sin(k*theta)**2
    An=7+k+1
    Bn=3
    Zk=pn**(Bn+An+1)/(1-pn**An)
    M=max(50, math.ceil(math.log(1e-17)/math.log1p(-qn)))
    norm=cost=info=info_normalized=kraft=0.0
    for n in range(1,M+1):
        probability=qn*(1-qn)**(n-1)
        C=Bn+n*An+1
        log_probability=math.log(qn)+(n-1)*math.log1p(-qn)
        gain=C+log_probability/lnphi
        norm+=probability
        cost+=probability*C
        info+=probability*gain
        info_normalized+=probability*(gain+math.log(Zk)/lnphi)
        kraft+=pn**C
    Hn=entropy_geom(qn)
    assert abs(norm-1)<1e-13
    assert abs(cost-(Bn+An/qn+1))<1e-10
    assert abs((cost-info)-Hn)<1e-10
    assert abs((cost-info_normalized)-(Hn-math.log(Zk)/lnphi))<1e-10
    assert abs(kraft-Zk)<1e-14
    derivative=math.log1p(-qn)/(lnphi*qn*qn)*4*math.sin(k*theta)*math.cos(k*theta)
    assert derivative!=0
    receipts.append((k,qn,Hn,Hn-math.log(Zk)/lnphi,derivative))

print('PASS exact Golden complete-readout algebra and dephasing control')
print('PASS symbolic stopped-cocycle mean and derivative')
print('PASS raw/subnormalized/normalized-reference sums with preparation B=3')
for row in receipts:
    print('k=%d q=%.12g raw=%.12g normalized=%.12g source=%.12g'%row)
