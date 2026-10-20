#!/usr/bin/env python3
"""Original CAR16 trace = indefinite Lorentz trace pairing, all six generators.
Mathematical representation fact, not a native full128 action or an Einstein proof.
"""
import sympy as s
from itertools import product
n=4
eta=s.diag(1,-1,-1,-1)
def creation(i):
    out=s.zeros(16)
    for bit in range(16):
        if (bit>>i)&1==0:
            out[bit+(1<<i),bit]=(-1)**((bit&((1<<i)-1)).bit_count())
    return out
c=[creation(i) for i in range(n)]
a=[x.T for x in c]
def gamma(X):
    return sum((X[i,j]*c[i]*a[j] for i,j in product(range(n),repeat=2)),s.zeros(16))
def E(i,j):
    out=s.zeros(4);out[i,j]=1
    return out
boosts=[E(0,i)+E(i,0) for i in (1,2,3)]
rots=[E(2,3)-E(3,2),E(3,1)-E(1,3),E(1,2)-E(2,1)]
basis=boosts+rots
assert all(X.T*eta+eta*X==s.zeros(4) for X in basis)
G4=s.Matrix([[s.trace(X*Y) for Y in basis] for X in basis])
G16=s.Matrix([[s.trace(gamma(X)*gamma(Y))/4 for Y in basis] for X in basis])
assert G4==G16==s.diag(2,2,2,-2,-2,-2)
# All matrix units prove the universal identity by bilinearity:
for i,j,k,l in product(range(4),repeat=4):
    X=E(i,j);Y=E(k,l)
    assert s.trace(gamma(X)*gamma(Y))==4*(s.trace(X*Y)+s.trace(X)*s.trace(Y))
def hodge(B):
    low=eta*B*eta
    return s.Matrix(4,4,lambda i,j:sum(s.LeviCivita(i,j,k,l)*low[k,l]
                                        for k,l in product(range(4),repeat=2))/2)
E0,E1=s.eye(4)[:,0],s.eye(4)[:,1]
B=E0*E1.T-E1*E0.T
F=basis[3]
X=hodge(B)*eta
assert X==F
assert s.trace(gamma(X)*gamma(F))==-8
assert -s.trace(gamma(X)*gamma(F))/4 == sum(hodge(B)[i,j]*(eta*F)[i,j] for i,j in product(range(4),repeat=2))
print('PASS 256 CAR matrix-unit and 36 full Lorentz pairings')
print('PASS Lorentz Gram signature (3+,3-), Hodge(e0 wedge e1)=J23')
print('FIREWALL: exact representation, not selected full128 Book/GR action')
