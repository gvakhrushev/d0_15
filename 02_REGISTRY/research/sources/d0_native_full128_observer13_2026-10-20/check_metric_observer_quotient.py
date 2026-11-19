#!/usr/bin/env python3
"""Exact D0 coframe16/SO3_n = Lorentz metric10 + unit observer3,
and the already-owned positive observer metric h=-g+2uu^T.
No physical Book03 action/GR selection implied.
"""
import sympy as s
from itertools import combinations_with_replacement
eta=s.diag(1,-1,-1,-1);e0=s.eye(4)[:,0]
pairs=list(combinations_with_replacement(range(4),2))
J=s.zeros(13,16)
for i in range(4):
    for r in range(4):
        E=s.zeros(4);E[i,r]=1
        dg=E.T*eta+eta*E
        du=E.T*eta*e0
        J[:,4*i+r]=s.Matrix([dg[a,b] for a,b in pairs]+[du[j] for j in (1,2,3)])
assert J.rank()==13 and len(J.nullspace())==3
for a,b in ((1,2),(1,3),(2,3)):
    A=s.zeros(4);A[a,b]=1;A[b,a]=-1
    assert J*s.Matrix(16,1,list(A))==s.zeros(13,1)
F=s.Matrix([[1,s.Rational(1,7),0,0],[0,1,s.Rational(1,5),0],
            [0,0,1,s.Rational(1,11)],[s.Rational(1,13),0,0,1]])
g=F.T*eta*F;u=F.T*eta*e0
assert (u.T*g.inv()*u)[0]==1
h=-g+2*u*u.T
h0=-eta+2*(eta*e0)*(eta*e0).T
assert h==F.T*h0*F
assert all(h[:k,:k].det()>0 for k in range(1,5))
R=s.eye(4);R[1,1]=R[2,2]=s.Rational(4,5)
R[1,2]=s.Rational(3,5);R[2,1]=-s.Rational(3,5)
assert R.T*eta*R==eta and R*e0==e0
assert (R*F).T*eta*(R*F)==g and (R*F).T*eta*e0==u
print('PASS coframe16/SO3=metric10+observer3, exact Jacobian rank13, null=spatial rotations')
print('PASS unit-timelike observer and positive original D0 observer metric h')
print('GR_closed=false; selected physical full128 Book action not proved')
