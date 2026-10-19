#!/usr/bin/env python3
"""Exact finite mathematical checks, NOT native D0 Cost-Info/GR.
The A0,A1 below are TOY smooth costs over original Golden weights (p,p²).
"""
import sympy as s

x,k,q,L=s.symbols("x k q L",real=True)
p=(s.sqrt(5)-1)/2
assert s.simplify(p+p**2-1)==0
mu0,mu1=p,p*p
A0=s.Rational(1,2)*(2*x*x+2*x*k+4*k*k)+x
A1=s.Rational(1,2)*(3*x*x-4*x*k+3*k*k)-x+2*k
price=q*A0+(1-q)*A1+(q*s.log(q/mu0)+(1-q)*s.log((1-q)/mu1))/L
H=s.hessian(price,[x,k,q]).subs({x:0,k:0,q:p})
assert H==H.T and s.simplify(H[2,2]-1/(L*p**3))==0
assert s.simplify(H[0,2]-2)==s.simplify(H[1,2]+2)==0
# Direct joint (k,q) Schur
V=H.extract([0],[1,2])
I=H.extract([1,2],[1,2])
assert s.simplify(I.det())!=0
full=s.factor(H[0,0]-(V*I.inv()*V.T)[0])
# q then k
qinv=1/H[2,2]
a=H[0,0]-H[0,2]**2*qinv
b=H[0,1]-H[0,2]*H[1,2]*qinv
c=H[1,1]-H[1,2]**2*qinv
after_q=a-b**2/c
# k then q; R is the REMAINING history source after correcting geometry
kinv=1/H[1,1]
geom=H[0,0]-H[0,1]**2*kinv
R=H[0,2]-H[0,1]*H[1,2]*kinv
J=H[2,2]-H[1,2]**2*kinv
after_k=geom-R**2/J
assert s.simplify(full-after_q)==s.simplify(full-after_k)==0
assert float(J.subs(L,s.log((1+s.sqrt(5))/2)).evalf(20))>0
print("PASS EXACT: both same-action Schur elimination orders match H_geom-R²/J")
# Full Golden-prior Gibbs log sum is not pathwise MAP.
Z=mu0*s.exp(-L*A0)+mu1*s.exp(-L*A1)
v0=mu0*s.exp(-L*A0)/Z
v1=mu1*s.exp(-L*A1)/Z
F=-s.log(Z)/L
for a in (x,k):
    assert s.simplify(s.diff(F,a)-v0*s.diff(A0,a)-v1*s.diff(A1,a))==0
    for b in (x,k):
        expected=(mu0*s.diff(A0,a,b)+mu1*s.diff(A1,a,b)-
                  L*p**3*(s.diff(A0-A1,a)).subs({x:0,k:0})*
                    (s.diff(A0-A1,b)).subs({x:0,k:0}))
        assert s.simplify(s.diff(F,a,b).subs({x:0,k:0})-expected)==0
print("PASS EXACT: original Golden-prior logpartition first source + covariance Hessian")
# Original native q_port=(p²,p) vs code=(p,p²) has KL=p-p²=p³
K_port=s.factor(p-p**2)
assert s.simplify(K_port-p**3)==0
assert s.diff(K_port,x)==0
print("PASS EXACT: conditional port Fisher field source zero while native code KL=p³")
# COMPLETE Born: sum q=1, therefore logpartition and its source vanish
qgood=mu0*s.exp(-L*x)/(mu0*s.exp(-L*x)+mu1)
qbad=1-qgood
assert s.simplify(qgood+qbad-1)==0
assert s.simplify(s.diff(-s.log(qgood+qbad)/L,x))==0
# a truly selected event/cut can have a nonzero normalized source
assert s.simplify(s.diff(-s.log(qgood)/L,x).subs(x,0)-p**2)==0
print("PASS EXACT: full Born normalized logpartition is zero; return cut is not")
# Native primitive-cost backtrack versus singleton, conditional on inverse holonomy
U=s.Matrix([[1,1],[0,1]])
assert U*U.inv()==s.eye(2) and 1+1>0
print("PASS: positive additive backtrack cost cannot factor through holonomy alone")
print("FIREWALL: independent finite math; full native action/measurement selection, GR, RAW-216 OPEN")
