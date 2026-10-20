#!/usr/bin/env python3
"""Original full GOOD/BAD Golden p² two-density CAR16 atlas -> all-six signed Palatini curvature jets.
Independent symbolic reproduction of the already-owned six native phase anchors.
Representation/observability only, not the native physically selected Book03 action.
"""
import sympy as s
import numpy as np
p=(s.sqrt(5)-1)/2;g=s.simplify(p**2);I=s.eye(4)
def E(i,j):
    M=s.zeros(4);M[i,j]=1;return M
eta=s.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
N2,N3=E(1,2)+E(2,0),E(1,3)+E(3,0)
B2,B3=E(0,2)+E(2,1),E(0,3)+E(3,1)
J23,B=E(2,3)-E(3,2),E(1,1)-E(0,0)
L=[N2,N3,B2,B3,J23,B]
assert all(X.T*eta+eta*X==s.zeros(4) for X in L)
a=(I[:,0]+I[:,2]+s.I*I[:,3])/s.sqrt(3)
b=(I[:,1]+I[:,2]+s.I*I[:,3])/s.sqrt(3)
OI=lambda i,j:(E(j,i)-E(i,j))/(2*s.I)
probes=[(a,E(0,0)),(a,E(2,2)),(a,OI(0,1)),(a,OI(0,2)),
        (b,E(1,1)),(b,OI(0,1))]
rows=[]
for v,O in probes:
    rho=v*v.conjugate().T
    anchor=(I+O)/2
    z0=s.simplify((g*g+(1-g)**2)*s.trace(anchor*rho))
    assert s.im(z0)==0 and z0>0
    row=[]
    for X in L:
        dgood=g*(X*rho+rho*X.T)
        dbad=-g/2*((X+X.T)*rho+rho*(X+X.T))
        dz=s.trace(anchor*(g*rho*dgood+(1-g)*rho*dbad))
        row.append(s.simplify(s.im(s.expand_complex(dz))/z0))
    rows.append(row)
Dphi=s.Matrix(rows)
assert s.simplify(Dphi.det()-p**9/s.Integer(15552000))==0
Gram=s.Matrix([[s.trace(X*Y) for Y in L] for X in L])
W=s.simplify(-Gram*Dphi.inv()/2)
assert s.simplify(W*Dphi+Gram/2)==s.zeros(6)
expected=[
 [0,0,-15-6*s.sqrt(5),0,0,3*s.sqrt(5)],
 [-10-12*s.sqrt(5),-20-12*s.sqrt(5),0,0,6*s.sqrt(5),0],
 [0,0,-3*s.sqrt(5),0,0,15+6*s.sqrt(5)],
 [-40-18*s.sqrt(5),-20-12*s.sqrt(5),0,0,30+12*s.sqrt(5),0],
 [-30-6*s.sqrt(5),-30-6*s.sqrt(5),0,0,30+6*s.sqrt(5),0],
 [0,0,15+9*s.sqrt(5),-15-9*s.sqrt(5),0,15+9*s.sqrt(5)]]
assert all(s.simplify(W[i,j]-expected[i][j])==0 for i in range(6) for j in range(6))
sv=np.linalg.svd(np.array(Dphi.evalf(24),dtype=float),compute_uv=False)
assert sv[-1]>.0069 and sv[0]<.084
print('PASS full original Golden GOOD+BAD six density phase jacobian exact det=p^9/15552000')
print('PASS all-six signed Palatini linear source W=−Gram·Dphi^(-1)/2, entries in Q(sqrt5)')
print('Native phase singular values:',sv)
print('GR_closed=false; native full128 field-priced Book action NOT forced by observability')
