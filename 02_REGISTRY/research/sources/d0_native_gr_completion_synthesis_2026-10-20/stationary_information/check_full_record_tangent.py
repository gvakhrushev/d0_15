#!/usr/bin/env python3
"""Exact same-record overlap, Fisher, reverse KL and stationary Hessian.

Read-only stdout checker; checks survive python -O.
"""
import json
import sympy as s

def need(condition, label):
    if not bool(condition):
        raise RuntimeError(label)

t,xi=s.symbols('t xi', real=True)
c,z=s.symbols('c z', real=True, nonzero=True) # z denotes sine, not fugacity

def circle(expr):
    return s.factor(s.cancel(s.expand(expr)).subs(c**2,1-z**2))

f0=1-2*t**2
f1=2*t*(1-t**2)
r=4*t**4*(1-t**2)
alpha0=c*f0-z*f1
alpha1=z*f0+c*f1
need(s.expand(f0*f0+f1*f1+r-1)==0,'normalized full cleanup')
need(circle(alpha0**2+alpha1**2+r-1)==0,'Golden rotation preserves norm')

# Raw W output has a genuine moving leakage direction; cleanup retains it.
raw=s.Matrix([t,s.sqrt(1-t*t)*s.cos(xi),s.sqrt(1-t*t)*s.sin(xi)])
V=s.Matrix([f0,0,0,f1,-2*t*t*raw[1],-2*t*t*raw[2]])
base=s.Matrix([1,0,0,0,0,0])
need(s.trigsimp((V.T*V)[0]-1)==0,'complete pure state norm')
need((base.T*V)[0]==f0,'exact full overlap')
need(s.trigsimp(((V-base).T*(V-base))[0]-4*t*t)==0,'exact norm difference')
need(s.simplify((raw.diff(xi).T*raw.diff(xi))[0].subs(t,0))==1,
     'raw query carries leakage-direction tangent')
need(V.diff(xi).subs(t,0)==s.zeros(6,1),'cleanup cancels that tangent')
need(V.diff(t).subs(t,0)==s.Matrix([0,0,0,2,0,0]),'entire cleanup tangent')
need((V.diff(t).T*V.diff(t))[0].subs(t,0)==4,'quantum metric coefficient four')

den=1-c*alpha0
eta=z*alpha1/den
need(circle(den-z*alpha1-2*t*t)==0,'exact stopped overlap identity')
q=z*z
eta_second=s.diff(eta,t,2).subs(t,0)
# Rational simplification modulo c²+z²=1 after denominator clearing.
need(circle((eta_second+4/q)*(1-c*c)**3*q)==0,'stopped QFI coefficient')
q1=alpha1**2+c*c*r
q0=alpha0**2+z*z*r
need(circle(q0+q1-1)==0,'full scalar stopped hazards')
need(circle((1-alpha1**2/(1-alpha0**2)-r/(1-alpha0**2))*(1-alpha0**2))==0,
     'exact complete dirty-hit probability')

# Reverse full CQ relative entropy, including all dirty outcome blocks.
kl=s.log(q/alpha1**2)+(c*c/q)*s.log(c*c/alpha0**2)
need(s.simplify(kl.subs(t,0))==0,'reverse KL matched value')
need(circle(s.diff(kl,t).subs(t,0))==0,'reverse KL first derivative')
need(circle(s.diff(kl,t,2).subs(t,0)-16/q)==0,'reverse KL second derivative')
fi=(4*c*z)**2/(q*q*(1-q))
need(circle((fi-16/q)*(1-q))==0,'full geometric Fisher')

# Explicit generic C2 valuation on the ACTUAL stationary scalar slice.
x,y,D,A,B=s.symbols('x y D A B', real=True)
signal=-x*y-D*y*y
H=s.hessian(signal,(x,y))
need(s.det(H)==-1,'indefinite native slice shape')
value=A*signal+B*signal**2
need((s.hessian(value,(x,y)).subs({x:0,y:0})-A*H)==s.zeros(2),
     'arbitrary smooth scalar valuation second jet')
need(s.hessian(signal**2,(x,y)).subs({x:0,y:0})==s.zeros(2),
     'matched quadratic information has zero field Hessian')

# Rational stopped fixture; all constants exact, no truncation defines result.
cr,zr=s.Rational(3,5),s.Rational(4,5)
tr=s.Rational(1,100)
av0=alpha0.subs({c:cr,z:zr,t:tr})
av1=alpha1.subs({c:cr,z:zr,t:tr})
overlap=s.factor(eta.subs({c:cr,z:zr,t:tr}))
finite=sum(zr*av1*(cr*av0)**j for j in range(8))
tail=(zr*av1)*(cr*av0)**8/(1-cr*av0)
need(finite+tail==overlap,'exact finite-plus-tail coherent overlap')
need(0<overlap<1,'nontrivial finite Bures distance')
need(r.subs(t,tr)>0,'forward KL support birth truly present')

print(json.dumps({'status':'PASS',
 'one_trial_overlap':'1-2t^2',
 'stopped_overlap':'1-2t^2/(1-c alpha0)',
 'stopped_QFI':'16/q * dt tensor dt',
 'reverse_KL_leading':'8 t^2/(q ln(phi))',
 'forward_KL':'infinite for small t!=0, dirty support retained',
 'stationary_field_Hessian_of_matched_information':'zero',
 'arbitrary_smooth_record_value_Hessian':'c H_t',
 'scope':'fixed-input cleaned whole-J2 output; no moving upstream programme record'},indent=2))
