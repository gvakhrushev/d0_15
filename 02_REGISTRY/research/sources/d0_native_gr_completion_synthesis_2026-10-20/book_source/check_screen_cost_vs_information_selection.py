#!/usr/bin/env python3
"""Exact original-screen/algebraic Jones 3-score consumer and mixed-source NO-GO.

The source of the three particular Jones-history log scores is an externally
supplied transcription. Reproduce their algebraic determinant, NOT the
underlying 128x128 original full128 Kraus derivation. The geometric screen,
record-score Ward, Fisher and matched-divergence no-go are exact general
calculations; the KL fixture is a symbolic countercontrol, not a new detector.
"""
import sympy as s

def require(ok,msg):
    if not ok:
        raise RuntimeError(msg)

t=s.symbols("t",real=True)
a=s.symbols("a",positive=True,real=True)
k=s.Matrix([-1+s.I,-1+s.I,-2,-1-s.I])
ell=s.Matrix([0,1,-1,1])
eta=s.diag(1,-1,-1,-1)
Q=ell*ell.T
F=s.eye(4)+t*eta*Q
require(ell.dot(k)==0,"screen Qk constraint")
require(s.simplify(F*k-k)==s.zeros(4,1),"full finite port-energy constancy")
require(s.simplify(F.T*eta*F-(eta+(2*t-3*t*t)*Q))==s.zeros(4),"exact Lorentz metric")
require(s.factor(F.det())==1-3*t,"local invertible coframe chart")

J=s.Matrix([
 [0,-s.Rational(4,3),0],
 [s.Rational(16,9),-s.Rational(125,18),s.Rational(5,36)],
 [-16*a**3/s.Integer(13)-s.Rational(9,26),
  32*a**3/s.Integer(13)-s.Rational(1,2),
  -16*a**3/s.Integer(13)-s.Rational(145,52)]])
require(s.simplify(J.det()+(1888*a**3+4595)/702)==0,
        "input Jones three-history log-score determinant")
require(J.det()!=0,"algebraic nondegeneracy")
scores=[-s.Rational(4,3),-s.Rational(181,36),-s.Rational(189,52)]
qq=s.symbols("q1 q2 q3",positive=True)
fisher_lower=s.expand(sum(v*v*q for v,q in zip(scores,qq)))
require(all(v!=0 for v in scores),"positive native record Fisher lower bound")

# Exact proper-divergence cross-source no-go with normalized binary
# probability and a co-moving reference, as a strict symbolic test.
x,y=s.symbols("x y",real=True)
q=s.Rational(1,3)+x/20+y/11+x*y/17
qref=q.subs(y,0)
KL=q*s.log(q/qref)+(1-q)*s.log((1-q)/(1-qref))
require(s.simplify(KL.subs(y,0))==0,"KL co-moving diagonal")
require(s.simplify(s.diff(KL,y).subs(y,0))==0,"proper-score link Ward")
require(s.simplify(s.diff(KL,x,y).subs(y,0))==0,"KL mixed metric-link no-go")
require(s.simplify(s.diff(KL,y,2).subs({x:0,y:0}))==s.Rational(9,242),
        "positive Fisher curvature for nonconstant-record KL")

# The four-corner of individually proper FULLY normalized fixed-anchor KL
# produces a signed mixed Fisher interaction without second q derivatives.
# This is a mathematical four-ARM comparator, not yet an admitted Book price.
q0=q.subs({x:0,y:0})
Dfixed=q*s.log(q/q0)+(1-q)*s.log((1-q)/(1-q0))
Four=s.simplify(Dfixed-Dfixed.subs(y,0)-Dfixed.subs(x,0)+
                Dfixed.subs({x:0,y:0}))
require(s.simplify(s.diff(Four,x,y).subs({x:0,y:0}))==s.Rational(9,440),
        "four-corner KL cross-fisher source")
require(s.hessian(Four,(x,y)).subs({x:0,y:0}).applyfunc(s.simplify)
        ==s.Matrix([[0,s.Rational(9,440)],
                    [s.Rational(9,440),0]]),
        "signed indefinite mixed Hessian from four proper positive arms")

# Original exact P25 Palatini finite mixed saddle (not a fitted action).
u,v=s.symbols("u v",real=True)
Palatini=(1-u)*s.sin(v)
H=s.hessian(Palatini,(u,v)).subs({u:1,v:0})
require(H==s.Matrix([[0,-1],[-1,0]]) and H.det()==-1,
        "indefinite exact Palatini Hessian")
require(s.diff(Palatini,u,v).subs({u:1,v:0})==-1,
        "nonzero original P25 mixed-source jet")

# Rank-3 inversion fits any desired score covector; mere existence
# cannot make a programme's concrete fixed Book code physically selected.
desired=s.Matrix(s.symbols("g1 g2 g3"))
fitted_weights=J.T.inv()*desired
require(s.simplify(J.T*fitted_weights-desired)==s.zeros(3,1),
        "full-rank inverse-design tautology")

print("EXACT input Jones log-score determinant =",s.factor(J.det()))
print("TRUE port-invisible screen: Fk=k, dg/dt|0=2 ell ell^T")
print("Strict Fisher lower bound =",fisher_lower)
print("KL co-moving mixed jet = 0; true Palatini P25 mixed jet = -1")
print("Exact positive KL link-Fisher fixture =",s.Rational(9,242))
print("ALL EXACT SCREEN / INFORMATION SELECTION GATES PASSED")
print("Full original 128 Kraus independent replay: NOT performed here")
print("Physical native Book03 source selected: FALSE")
print("GR_closed: FALSE")
