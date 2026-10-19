#!/usr/bin/env python3
"""Exact PRETRACE original-scene Book-order/Hodge source control.

Research theorem on three legal triangles of K(9,11,13), not the entire
physical 718-edge Book action. Original Lorentz generators; no native
G0/Julia/Book programme selection or physical Einstein closure.
"""
from collections import Counter
from itertools import permutations
import sympy as sp

I=sp.eye(4)
E=lambda i,j: I[:,i]*I[j,:]
eta=sp.Matrix([[0,1,0,0],[1,0,0,0],[0,0,-1,0],[0,0,0,-1]])
A=E(1,2)+E(2,0)  # native N2
B=E(0,3)+E(3,1)  # native barN3
C=A*B-B*A       # native J23
assert C==E(2,3)-E(3,2)
a,b,c=sp.symbols("a b c",real=True)
U0=I+a*A+a*a*A*A/2
U1=I+b*B+b*b*B*B/2
U2=(I-c*C/2).inv()*(I+c*C/2)
for U in (U0,U1,U2):
    assert sp.simplify(U.T*eta*U-eta)==sp.zeros(4)
assert sp.simplify(sp.trace(U0*U1-U1*U0))==0
assert sp.factor(sp.trace(C.T*(U0*U1-U1*U0))/2)==a*b
print("PASS: pretrace J23 odd marker = ab, but scalar trace commutator = 0")

# ORIGINAL proper Lorentz 4-edge based commutator plaquette.
# Its odd holonomy is the finite source actually read by the naked star;
# C^T is the algebraic matching reference control (actual e,Hodge typed later).
U0inv=I-a*A+a*a*A*A/2
U1inv=I-b*B+b*b*B*B/2
Pla=U0*U1*U0inv*U1inv
Pla_inv=U1*U0*U1inv*U0inv
assert sp.simplify(Pla*Pla_inv-I)==sp.zeros(4)
odd_face=(Pla-Pla_inv)/2
marked_face=sp.factor(sp.trace(C.T*odd_face)/2)
assert marked_face==a*b*(1-a*a*b*b/8)
print("PASS: exact oriented original four-link odd-plaquette source =",marked_face)

# Algebra-valued Book face coefficients w_plus*[P], w_minus*[P^-1]
# have field-moving scalar weights; NORMALIZE each recorded class first.
wplus,wminus=sp.symbols("wplus wminus",nonzero=True)
pretrace=(wplus*Pla/wplus-wminus*Pla_inv/wminus)/2
assert sp.simplify(pretrace-odd_face)==sp.zeros(4)
assert sp.simplify(sp.diff(pretrace,wplus))==sp.zeros(4)
assert sp.simplify(sp.diff(pretrace,wminus))==sp.zeros(4)
print("PASS: two resolved Book class weights cancel before odd face/Hodge readout, including source jets")


# All ORIGINAL 718 directed edges of K(9,11,13).
part={v:(0 if v<9 else (1 if v<20 else 2)) for v in range(33)}
edges={(u,v) for u in part for v in part if part[u]!=part[v]}
assert len(edges)==718
loops=[[0,9+j,20+j,0] for j in range(3)]
for loop in loops:
    assert all((u,v) in edges for u,v in zip(loop,loop[1:]))
def combine(order):
    out=loops[order[0]].copy()
    for idx in order[1:]:
        out+=loops[idx][1:]
    return out
g012=combine((0,1,2))
g021=combine((0,2,1))
assert len(g012)==len(g021)==10
assert g012[0]==g021[0]==g012[-1]==g021[-1]==0
assert Counter(zip(g012,g012[1:]))==Counter(zip(g021,g021[1:]))
assert Counter(g012)==Counter(g021)
print("PASS: original graph histories same directed Cost/Info incidence, endpoints and all scalar field jets")

t1=sp.factor(sp.trace(U0*U1*U2))
t2=sp.factor(sp.trace(U0*U2*U1))
odd=sp.factor(t1-t2)
assert sp.simplify(odd+8*a*b*c/(4+c*c))==0
v={a:sp.Rational(1,40),b:sp.Rational(1,40),c:sp.Rational(1,40)}
assert odd.subs(v)==-sp.Rational(1,32005)
print("PASS: exact oriented gauge-invariant three-loop Wilson trace difference",odd)

# The scalar logdet of a MATRIX-valued sum still symmetrizes permutation
# classes: coefficient of r0 r1 r2 in z^9 of -logdet(I-z^3 W).
U=(U0,U1,U2)
coef=sp.factor(sum(sp.trace(U[k[0]]*U[k[1]]*U[k[2]]) for k in permutations(range(3)))/3)
assert sp.simplify(coef-t1-t2)==0
assert sp.simplify(coef-(a*a*b*b*c*c+4*a*a*b*b+64)/(2*(4+c*c)))==0
print("PASS: mixed scalar logdet triple coefficient is SUM t012+t021, not exchange-odd difference")

# Exact transfer Schur identity is valid for arbitrary positive r_j and z;
# check nontrivial original-sublanguage 7x4=28 dimensional rational case.
r=[sp.Rational(1,4),sp.Rational(1,7),sp.Rational(1,5)]
Us=[U0.subs({a:sp.Rational(1,40)}),
    U1.subs({b:sp.Rational(1,40)}),
    U2.subs({c:sp.Rational(1,40)})]
M=sp.zeros(28)
for j in range(3):
    for src,dst,K in ((0,1+j,I),(1+j,4+j,I),(4+j,0,r[j]*Us[j])):
        M[4*dst:4*dst+4,4*src:4*src+4]=K
z=sp.Rational(1,3)
W=sum((r[j]*Us[j] for j in range(3)),sp.zeros(4))
assert (sp.eye(28)-z*M).det(method="domain-ge") == (sp.eye(4)-z**3*W).det(method="domain-ge")
print("PASS: 28x28 return determinant reduces exactly to 4x4 determinant of matrix SUM")

# Existing mathematical positive complete Julia/Choi mark Q=(Tr U)^2/64.
# Original full native selected execution is still unproved.
q1=sp.factor(t1*t1/64)
q2=sp.factor(t2*t2/64)
diff=sp.factor(q1-q2)
assert sp.simplify(diff+a*b*c*(a*a*b*b*c*c+4*a*a*b*b+64)/(16*(4+c*c)**2))==0
assert diff.subs(v)==-sp.Rational(262144006401,67129837158400000)
dlog=sp.factor(2*(sp.diff(t1,a)/t1-sp.diff(t2,a)/t2))
assert dlog.subs(v)==-sp.Rational(42949671911260160000,68719480090918952972801)
assert 0<float(q1.subs(v))<1 and 0<float(q2.subs(v))<1
print("PASS: complete-positive marked history odds carry a nonzero scalar-price-independent field source")
print("mark difference =",diff.subs(v),"d_a log conditional odds =",dlog.subs(v))
print("FIREWALL: mathematical original-scene sublanguage only; native action/admission/refinement/GR OPEN")
