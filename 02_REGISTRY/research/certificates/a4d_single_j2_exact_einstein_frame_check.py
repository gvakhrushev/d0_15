#!/usr/bin/env python3
"""D0 single J2 / exact Einstein-frame partial Legendre source checks.

Mathematical declared volume-normalized *controlled* AF×scene J2 only.
Actual mandatory raw D0 Book/H+J+R selection, native clock/return
admission, spin and original #216 GR terminal are NOT certified.
"""
from __future__ import annotations
from math import sqrt
from dataclasses import dataclass
import json
import mpmath as mp
import sympy as s

r, X = s.symbols('r X', real=True)
p = (s.sqrt(5)-1)/2
z = s.Rational(1, 2**20)
T = s.Rational(1,25)   # t²=0.04, one exact positive test window
sig = s.Integer(1)
E = p**2*(1+T*r)
bb = (p+sig*p**2*T*X)**2
lam = 4*E*(1-E)
B = 4*bb*(1-bb)          # literal TWO-TICK scene, NOT bb
Q = 1-z*B
R = 1-z*(lam+(1-lam)*B)
F = -s.log(Q)-s.log(R)
F0 = F.subs({r:0,X:0})
Fr = s.diff(F,r)
Fx = s.diff(F,X)
Frr = s.diff(Fr,r)
Frx = s.diff(Fr,X)
Fxx = s.diff(Fx,X)
L0=4*p**3
a=1-L0
Q0=1-z*L0
R0=1-z*(L0+a*L0)

# Check the exact Golden baseline identities; no external fitting.
assert s.simplify(p+p**2-1)==0
assert s.simplify(a-p**6)==0
assert s.simplify(4*(1-2*p**2)-L0)==0

at0={r:0,X:0}
c=s.simplify(Fr.subs(at0))
d=s.simplify(Fx.subs(at0))
known_c=4*z*p**11*T/R0
known_d=8*z*p**6*T*(1/Q0+a/R0)
assert abs(float(s.N(c-known_c,25)))<1e-23
assert abs(float(s.N(d-known_d,25)))<1e-23
ratio=float(s.N(d/c,22))
assert abs(ratio-23.41640675188407)<1e-10

# Entire nonlinear mixed radial/matter jet has its own source:
# differentiation of the literal matrix Q,R and no independent action.
mixed_analytic=-z*(1-z)*s.diff(lam,r)*s.diff(B,X)/R**2
for rv,xv in [(0,0),(s.Rational(1,5),s.Rational(-1,9))]:
    v=float(s.N((Frx-mixed_analytic).subs({r:rv,X:xv}),25))
    assert abs(v)<1e-18

known_rr=z*p**10*T**2/R0**2*(-8*R0+z*a*L0**2)
assert abs(float(s.N(Frr.subs(at0)-known_rr,26)))<1e-21
assert float(s.N(known_rr,25))<0
zcritical=float(s.N(8/(8*(1-a**2)+a*L0**2),25))
assert .996<zcritical<.997
assert float(z)<zcritical

# Compute exact source-jet derivatives symbolically, then evaluate in high
# precision to reject frozen preparation, wrong scene one-tick or
# missing A/V normalization.
mp.mp.dps=55
Ffun=s.lambdify((r,X),F,'mpmath')
Frfun=s.lambdify((r,X),Fr,'mpmath')
Fxfun=s.lambdify((r,X),Fx,'mpmath')
Fbase=mp.mpf(str(s.N(F0,60)))
c0=mp.mpf(str(s.N(c,60)))
d0=mp.mpf(str(s.N(d,60)))

def LF(rv,xv):
    return Ffun(rv,xv)-Fbase

# Sitewise exact algebraic identity: h=(beta/c)*g,
# J_h/J_g=(beta/c)^2, r_h=(c/beta)*r, X_h=(c/beta)*X.
# Algebraically Legendre U=beta*r-L_F, and the gravity numerator
# and matter remainder of ONE J2 are identical off shell.
checks=[]
for rv,xv in [
    (mp.mpf('.075'),mp.mpf('.031')),
    (mp.mpf('-.08'),mp.mpf('-.019')),
    (mp.mpf('.001'),mp.mpf('.012'))]:
    beta=Frfun(rv,xv)
    yh=beta/c0
    xh=xv/yh
    rh=rv/yh
    U=beta*rv-LF(rv,xv)
    transformed=yh**2*(c0*rh-(c0/beta)**2*U)
    assert mp.almosteq(transformed,LF(rv,xv),abs_eps=mp.mpf('1e-46'))
    checks.append(float(transformed-LF(rv,xv)))

# Two different physical cells: the normalized mean derivative is NOT
# just DA/V; the global -Gamma DV term is necessary.
states=[(mp.mpf('.06'),mp.mpf('.032'),mp.mpf('1.2')),
        (mp.mpf('-.04'),mp.mpf('.018'),mp.mpf('1.6'))]
def mean(k):
    A=mp.mpf(0);V=mp.mpf(0)
    for i,(rv,xv,J) in enumerate(states):
        sscale=mp.e**k if i==0 else mp.mpf(1)
        Jnew=J*sscale**4
        rvnew=rv*sscale**(-2)
        xvnew=xv*sscale**(-2)
        A+=Jnew*LF(rvnew,xvnew);V+=Jnew
    return A/V
Gamma=mean(mp.mpf(0))
rv,xv,J=states[0]
predicted=J/(states[0][2]+states[1][2])*(
     4*(LF(rv,xv)-Gamma)-2*rv*Frfun(rv,xv)-2*xv*Fxfun(rv,xv))
h=mp.mpf('1e-10')
observed=(mean(h)-mean(-h))/(2*h)
assert abs(observed-predicted)<mp.mpf('1e-25')
# A constant subtraction from the MEAN does not change this source;
# removing the volume source from A/V generally does.
wrong=(J/(states[0][2]+states[1][2]))*(
      4*LF(rv,xv)-2*rv*Frfun(rv,xv)-2*xv*Fxfun(rv,xv))
assert abs(wrong-predicted)>mp.mpf('1e-10')

# Algebraic trace/Radial law in original variables:
# beta r-X F_X=2(F-Gamma) exactly equals Einstein-frame d_beta P=0.
# Solve the SAME two equations β=F_r and trace at Γ=0 for finite non-null X_h.
source_lambda=d0/c0
def algebraic_equations(rv,y,xh):
    beta=y*c0
    xv=y*xh
    return (
       (Frfun(rv,xv)-beta)/c0,
       (2*LF(rv,xv)-beta*rv-xv*Fxfun(rv,xv))/c0
    )
solved=[]
for xh in [mp.mpf('.0001'),mp.mpf('-.0001')]:
    rs,ys=mp.findroot(
        lambda rr,yy: algebraic_equations(rr,yy,xh),
        (-source_lambda*xh,mp.mpf(1)),
        solver='mdnewton',tol=mp.mpf('1e-40'))
    xold=ys*xh
    beta=ys*c0
    U=beta*rs-LF(rs,xold)
    P_eff=-(1/ys**2)*U
    assert abs(algebraic_equations(rs,ys,xh)[0])<mp.mpf('1e-36')
    assert abs(algebraic_equations(rs,ys,xh)[1])<mp.mpf('1e-36')
    assert abs(rs+source_lambda*xh)<mp.mpf('.000002')
    solved.append({'Xh':float(xh),'r':float(rs),
                   'beta_over_c':float(ys),
                   'trace_error':float(algebraic_equations(rs,ys,xh)[1]),
                   'P_eff':float(P_eff)})

# Explicit eigenvalue-free nonlinear kinetic jet of SAME source,
# including its mixed curvature term. At fixed Γ=0:
# P_eff(X)=d X +[F_XX-2λ F_rX+λ²F_rr]X²/2+O(X³).
ff=float(s.N(Frr.subs(at0),30))
fx=float(s.N(Frx.subs(at0),30))
xx=float(s.N(Fxx.subs(at0),30))
K=xx-2*ratio*fx+ratio*ratio*ff
assert abs(K/(2*float(c0))+29.5791597430433)<1e-5

# Alternate σ=- orientation gives the opposite linear matter
# source but does not select which direction D0 physically executes.
assert float(c0)>0 and abs(float(source_lambda))>1

print(json.dumps({
 "status":"PASS: one J2 Einstein-frame / exact trace-elimination tests",
 "scope":"conditional volume-normalized J2 mean, NOT compulsory full D0",
 "z":"2^-20","t_squared":"1/25",
 "golden_ratio_relative_matter_coupling":ratio,
 "L_rr":ff,"L_rX":fx,"L_XX":xx,
 "Legendre_inversion_z_threshold":zcritical,
 "same_original_action_identity_errors":checks,
 "complete_mean_trace_derivative_error":float(observed-predicted),
 "wrong_unnormalized_source_gap":float(wrong-predicted),
 "global_normalizer_retained":True,
 "algebraic_matter_solutions":solved,
 "nonlinear_kessence_X2_coefficient_relative_to_c":K/(2*float(c0)),
 "extra_propagating_scalar_introduced":False,
 "native_full_Book_selection":False,
 "Einstein_physical_GR_derived":False
},indent=2,ensure_ascii=False,sort_keys=True))
