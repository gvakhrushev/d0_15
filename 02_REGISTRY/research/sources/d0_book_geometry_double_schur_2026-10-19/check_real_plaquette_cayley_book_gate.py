#!/usr/bin/env python3
"""Actual Lorentz plaquette P, not curvature inserted as auxiliary source:
exact original CAR16 positive marked-event inversion/composition NO-GO,
six-generator Cayley curvature readout and native Golden contraction domain.
Research only; the compulsory full128/Book event/field source is still open.
"""
import sympy as s
import numpy as np
from itertools import combinations
eta=s.diag(1,-1,-1,-1)
p=(s.sqrt(5)-1)/2
I=s.eye(4)
def E(i,j):
    a=s.zeros(4);a[i,j]=1;return a
G=[E(0,i)+E(i,0) for i in (1,2,3)]+[
    E(2,3)-E(3,2),E(3,1)-E(1,3),E(1,2)-E(2,1)]
gram=s.Matrix([[s.trace(X*Y) for Y in G] for X in G])
assert gram==s.diag(2,2,2,-2,-2,-2)
def boost(i,c,sh):
    a=I.copy();a[0,0]=a[i,i]=c;a[0,i]=a[i,0]=sh;return a
ROT=I.copy()
ROT[2,2]=ROT[3,3]=s.Rational(4,5)
ROT[2,3]=s.Rational(3,5);ROT[3,2]=-s.Rational(3,5)
B=boost(1,s.Rational(101,99),s.Rational(20,99))
C=boost(2,s.Rational(113,112),s.Rational(15,112))
P=B*ROT*C
assert P.T*eta*P==eta and P.det()==1 and (I+P).det()!=0
T=(P-I)*(P+I).inv()
curv=(P-P.inv())/2
assert s.simplify(T.T*eta+eta*T)==s.zeros(4)
assert s.simplify(curv-2*T*(I-T*T).inv())==s.zeros(4)
assert s.simplify((P.inv()-I)*(P.inv()+I).inv()+T)==s.zeros(4)
mark=lambda U:s.factor(p*p*(I+U).det()**2/256)
assert s.simplify(mark(P)-mark(P.inv()))==0
assert s.simplify(mark(I)-p*p)==0
for X in G:
    direct=s.trace(X*T)
    det_derivative=2*s.trace((I+P).inv()*X*P)
    reverse_derivative=2*s.trace((I+P.inv()).inv()*X*P.inv())
    assert s.simplify(direct-det_derivative)==0
    assert s.simplify(direct+reverse_derivative)==0
    odd_score=-(det_derivative-reverse_derivative)/2
    star=-s.trace(X*curv)/2
    assert s.simplify(star-odd_score+s.trace(X*T**3*(I-T*T).inv()))==0
reconstructed=sum((s.trace(X*T)/a)*X for X,a in zip(G,[2,2,2,-2,-2,-2]),s.zeros(4))
assert s.simplify(reconstructed-T)==s.zeros(4)
assert s.simplify(2*reconstructed*(I-reconstructed**2).inv()-curv)==s.zeros(4)
# Explicit original J23 old face changes sign even though marked mass doesn't.
X=G[3]
assert s.simplify(mark(ROT)-mark(ROT.inv()))==0
assert s.simplify(-s.trace(X*(ROT-ROT.inv()))/4)==s.Rational(3,5)
w=lambda U:s.factor(mark(U)/(p*p))
assert w(ROT)==s.Rational(81,100)
assert w(ROT**2)==s.Rational(256,625)
assert s.simplify(w(ROT**2)-w(ROT)**2)!=0
h=s.symbols("h",real=True)
assert s.limit((s.sin(h)-2*s.tan(h/2))/h**3,h,0)==-s.Rational(1,4)
# Native p Lambda(P) truly allows a complete positive Julia (good/unmarked/fail) near this P.
blades=[b for d in range(5) for b in combinations(range(4),d)]
def exterior(M):
    return s.Matrix(16,16,lambda i,j:
        0 if len(blades[i])!=len(blades[j]) else
        M.extract(blades[i],blades[j]).det() if blades[i] else 1)
for U in (P,P.inv(),ROT,ROT.inv()):
    z=np.array(exterior(U),dtype=float)*float(p)
    assert 1-np.linalg.eigvalsh(z.T@z).max()>0.02
print("PASS original real plaquette: inversion-even scalar marked mass, nonmultiplicative Book path weight")
print("PASS all six native SO(1,3) odd marked gradients reconstruct full EXACT Cayley and old finite curvature")
print("PASS O(h^6) per-cell star/Cayley discrepancy for smooth P=I+O(h^2)")
print("PASS Golden CAR16 full positive Julia chart for actual noncommuting Lorentz test P")
print("GR_closed=false; physical Book marked readout and field->Cost/Info source unselected")
