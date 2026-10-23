#!/usr/bin/env python3
"""Original based plaquette Palatini, HOMOGENEOUS flat link mixed zero.

The genuine Jones34 tangent uses constant coframes/links on a 4-torus
with independent physical SO(1,3) link generators. Original six-based
plaquette P_rs=U_r U_s U_r^-1 U_s^-1 has exact first link jet ZERO
at identity for homogeneous links. This checker does not identify the
separately certified Hellinger cross source as Book03 physical action.
"""
import sympy as s
t,x=s.symbols("t x",real=True)
I=s.eye(4)
E=lambda i,j: s.eye(4)[:,i]*s.eye(4)[j,:]
# Two noncommuting ACTUAL Lorentz boosts on same four-dimensional tangent.
X=E(0,1)+E(1,0)
Y=E(0,2)+E(2,0)
eta=s.diag(1,-1,-1,-1)
assert s.simplify(X.T*eta+eta*X)==s.zeros(4)
assert s.simplify(Y.T*eta+eta*Y)==s.zeros(4)
assert X*Y-Y*X!=s.zeros(4)
# Evaluate finite exact first-jet identity with inverse true matrices,
# using an EXACT proper-Lorentz Cayley parametrization of both links.
Ur=(I+t*X/2)*(I-t*X/2).inv()
Us=(I+t*Y/2)*(I-t*Y/2).inv()
assert (Ur.T*eta*Ur-eta).applyfunc(s.simplify)==s.zeros(4)
assert (Us.T*eta*Us-eta).applyfunc(s.simplify)==s.zeros(4)
P=s.simplify(Ur*Us*Ur.inv()*Us.inv())
dP=s.diff(P,t).subs(t,0).applyfunc(s.simplify)
assert dP==s.zeros(4)
assert P.subs(t,0)==I
odd=(P-P.inv())/2
assert s.diff(odd,t).subs(t,0).applyfunc(s.simplify)==s.zeros(4)
# Any genuinely coframe-dependent fixed solder/star contraction is a
# multiplier of the original odd curvature, and therefore has zero
# mixed derivative with ANY coframe direction on this chart.
coframe_weight=1+x+x*x
S=coframe_weight*s.trace((E(0,1)+E(1,0))*odd)
assert s.simplify(s.diff(S,x,t).subs({x:0,t:0}))==0
# The original commutator curvature appears only at t²; it is not
# identically flat at finite nonzero t (so the control is not vacuous).
assert s.simplify(s.diff(P,t,2).subs(t,0)-2*(X*Y-Y*X))==s.zeros(4)
print("PASS original homogenous based plaquette first link jet=0")
print("PASS all constant metric-link Palatini mixed jets=0 at U=I")
print("PASS curvature is nontrivial at second order for noncommuting boosts")
print("This DOES NOT prove Palatini mixed zero for spatially varying links")
print("Native full128 Hellinger original homogeneous rank10: separate exact owner")
print("GR_closed=false")
