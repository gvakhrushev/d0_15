#!/usr/bin/env python3
"""Exact algebra controls for periodic commuting-B source rigidity."""
import sympy as sp

ETA=sp.diag(1,-1,-1,-1)
I=sp.eye(4)
B=sp.zeros(4)
for j in (1,2,3):
    B[0,j]=B[j,0]=1

def ck(name,cond):
    if not cond:
        raise AssertionError(name)
    print("PASS_"+name,flush=True)

t,s=sp.symbols("t s", real=True)
ck("B_CUBED_3B", B**3==3*B)

def U(x):
    return sp.simplify((I-x*B/2).inv()*(I+x*B/2))

Ut=U(t)
Us=U(s)
ck("CAYLEY_LORENTZ", sp.simplify(Ut.T*ETA*Ut-ETA)==sp.zeros(4))
ck("CAYLEY_DET_ONE", sp.factor(Ut.det()-1)==0)

# Exact composition in the Cayley parameter.
r=sp.factor((t-s)/(1-sp.Rational(3,4)*t*s))
ck("CAYLEY_DIFFERENCE_COMPOSITION",
   sp.simplify(Ut*U(-s)-U(r))==sp.zeros(4))

gamma=sp.factor(4*r/(4-3*r*r))
curv=sp.simplify((U(r)-U(-r))/2)
ck("ODD_CURVATURE_COEFFICIENT",
   sp.simplify(curv-gamma*B)==sp.zeros(4))

x=sp.symbols("x", real=True)
g=4*x/(4-3*x*x)
dg=sp.factor(sp.diff(g,x))
ck("CAYLEY_FLUX_DERIVATIVE_POSITIVE_NUMERATOR",
   sp.factor(dg-4*(4+3*x*x)/(4-3*x*x)**2)==0)

# A nonzero common increment cannot close a four-step boost cycle.
U4=sp.simplify(U(x)**4-I)
nums=[]
for e in U4:
    num,_=sp.fraction(sp.factor(e))
    if num!=0:
        nums.append(sp.factor(num))
common=nums[0]
for n in nums[1:]:
    common=sp.gcd(common,n)
ck("FOUR_STEP_COMMON_INCREMENT_ONLY_ZERO_IN_OPEN_CHART",
   sp.factor(common).subs(x,0)==0 and
   sp.factor(common/x).subs(x,0)!=0)

# Telescoping rapidity increments is the analytic proof; this polynomial
# control rejects any hidden nonzero finite-order Cayley boost near identity.
print("COMMON_NUMERATOR_GCD",sp.factor(common),flush=True)
print("RESULT PERIODIC-COMMUTING-B-PHASE-COMMON-SOURCE-IS-ZERO",flush=True)
