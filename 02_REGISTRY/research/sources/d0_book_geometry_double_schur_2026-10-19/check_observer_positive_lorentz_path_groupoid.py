#!/usr/bin/env python3
"""Existing observer/exterior CAR16 path functor: explicit positive moving-fibre
composition, reverse dagger and noncompact closed-loop observer memory.
Consumes accepted D0.Geometry.A4DObserverPositiveExterior and existing
A4D Lorentz-restricted path groupoid. No original K(9,11,13) edge compiler claimed.
"""
import sympy as s
from itertools import combinations
r=s.Rational
I=s.eye(4);eta=s.diag(1,-1,-1,-1)
def boost(i,c,sh):
    a=I.copy();a[0,0]=a[i,i]=c;a[0,i]=a[i,0]=sh;return a
def rotation(i,j,c,sh):
    a=I.copy();a[i,i]=a[j,j]=c;a[i,j]=sh;a[j,i]=-sh;return a
g1=boost(1,r(5,4),r(3,4))
g2=rotation(2,3,r(4,5),r(3,5))
g3=boost(2,r(5,3),r(4,3))
for g in (g1,g2,g3):
    assert g.T*eta*g==eta and g.det()==1
blades=[blade for k in range(5) for blade in combinations(range(4),k)]
assert len(blades)==16
def ext(M):
    return s.Matrix(16,16,lambda i,j:
        0 if len(blades[i])!=len(blades[j]) else
        M.extract(blades[i],blades[j]).det() if blades[i] else 1)
def H(n):
    b=eta*n
    return -eta+2*b*b.T
def B(n):
    return ext(H(n))
n0=I[:,0];n1=g1*n0;n2=g2*n1;n3=g3*n2
for n in (n0,n1,n2,n3):
    assert (n.T*eta*n)[0]==1
    assert all(H(n)[:k,:k].det()>0 for k in range(1,5))
    gram=B(n)
    assert all(gram[:k,:k].det()>0 for k in range(1,17))
for g,n,nn in ((g1,n0,n1),(g2,n1,n2),(g3,n2,n3)):
    U=ext(g)
    assert U.T*B(nn)*U==B(n)
    assert B(n).inv()*U.T*B(nn)==U.inv()==ext(g.inv())
whole=g3*g2*g1
word=ext(g3)*ext(g2)*ext(g1)
assert word==ext(whole)
assert word.T*B(n3)*word==B(n0)
assert B(n0).inv()*word.T*B(n3)==word.inv()
assert ext(g1.inv())*ext(g2.inv())*ext(g3.inv())==word.inv()
assert n3!=n0
assert ext(g1).T !=ext(g1).inv() # frozen counting transpose is wrong for boosts
print("PASS true original positive observer-CAR16 H_n composition and reversal dagger on full Fock16")
print("PASS noncompact 3-step Lorentz holonomy changes endpoint observer, no spurious SO(3) restriction")
print("FIREWALL: conditional path groupoid already owned; original full718-to-lattice Lorentz compiler not owned")
