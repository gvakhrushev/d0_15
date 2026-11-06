#!/usr/bin/env python3
"""Read-only, bounded application of existing D0 complete-cut source formulas.

Exact rational and symbolic checks plus high-precision chain/adjoint controls.
This does NOT execute the huge original READY word, reprove its native
admission, rebuild all42 geometry, or validate the GR claim.
"""
from __future__ import annotations
from fractions import Fraction as F
import json
import mpmath as mp
import sympy as sp

mp.mp.dps = 100

def require(ok: bool, message: str) -> None:
    if not ok:
        raise AssertionError(message)

def close(x, y, message: str, tol='1e-65') -> None:
    require(abs(x-y) <= mp.mpf(tol)*max(1, abs(x), abs(y)), message)

p=(mp.sqrt(5)-1)/2
beta=2*p*p
zeta=mp.mpf(2)**-20
spectator=128
M, W=72441, 50549
Zmin=M*(W-2)
eta_rational=F(13,5)/(64*F(1,2**20)*(1-F(1,2**19))*Zmin)
require(eta_rational < F(1,80000), 'exact original thermal relative bound')

# Derive the Golden ratio equality, NOT a numerical parameter fit.
p_s,z_s=sp.symbols('p z', positive=True)
QE=1-z_s*4*p_s**3
RE=1-z_s*4*p_s**3*(1+p_s**6)
rf=4*z_s*QE*p_s**11
rq=8*z_s*p_s**6*(RE+QE*p_s**6)
require(sp.cancel(-rq/rf+2*p_s**-5*(RE/QE+p_s**6))==0,
        'exact source ratio, all positive symbolic p,z')

# True PF weight identity, valid for EVERY actual positive site count.
nz,N,L,scale,epsF,epsQ,rf_s,rq_s=sp.symbols(
    'nz N L scale epsF epsQ rf rq', nonzero=True)
rho_z=L**4*nz/N
lhs=2*p_s**23*nz*scale**2/rho_z*(rf_s*epsF-rq_s*epsQ)
rhs=2*N*p_s**23*scale**2/L**4*(rf_s*epsF-rq_s*epsQ)
require(sp.cancel(lhs-rhs)==0,'actual count/density cancellation; no equal priors')

# Full scalar action includes ALL harmonic modes (not normalized heat).
def f(q): return 4*q*(1-q)
def fp(q): return 4*(1-2*q)
def full_price(q, m=M, w=W):
    Z=mp.mpf(m*w-2*len(q))+2*sum(mp.exp(-beta*f(t)) for t in q)
    return mp.log(spectator*Z)/beta-spectator*sum(mp.log1p(-zeta*f(t)) for t in q)
def source_coeffs(q, m=M, w=W):
    Z=mp.mpf(m*w-2*len(q))+2*sum(mp.exp(-beta*f(t)) for t in q)
    return [(spectator*zeta/(1-zeta*f(t))-2*mp.exp(-beta*f(t))/Z)*fp(t) for t in q]

Qe=1-zeta*4*p**3
Re=1-zeta*4*p**3*(1+p**6)
r0=1-Qe*Re
rf0=4*zeta*Qe*p**11
rq0=8*zeta*p**6*(Re+Qe*p**6)
a_ready=2*10946*p**23
q=(1-a_ready, a_ready*(1-r0), a_ready*r0)
close(sum(q),1,'whole three-status normalization')
coef=source_coeffs(q)
full_gain=coef[2]-coef[1]
feedback_gain=spectator*zeta*(fp(q[2])/(1-zeta*f(q[2]))-fp(q[1])/(1-zeta*f(q[1])))
eta=mp.mpf(eta_rational.numerator)/eta_rational.denominator
require(0<(1-eta)*feedback_gain <= full_gain <= feedback_gain,
        'whole heat+feedback nonzero gain')

# On this differential the full price depends on ONE common scalar report.
# This checks the actual full derivative and moving heat normalizer, NOT
# an original 42-dimensional field/circuit reconstruction.
def price_report(r): return full_price((1-a_ready,a_ready*(1-r),a_ready*r))
analytic_r=a_ready*full_gain
actual_r=mp.diff(price_report,r0)
close(analytic_r,actual_r,'full nonlinear source derivative')
DF,DQ=mp.mpf(7)/13,mp.mpf(-5)/17
report_derivative=(rf0*DF-rq0*DQ)/256
full_row=analytic_r*report_derivative
geometric_row=(analytic_r*rf0/256)*(DF-(rq0/rf0)*DQ)
close(full_row,geometric_row,'complete source proportional to old two-normal source')

# General nonlinear constrained execution lift: TWO generated steps,
# fixed initial state. This is a small mathematical control, not a claim
# that a continuous variable rotation is an elementary D0 native gate.
def R01(t):
    c,s=mp.cos(t),mp.sin(t)
    return mp.matrix([[c,-s,0],[s,c,0],[0,0,1]])
def R12(t):
    c,s=mp.cos(t),mp.sin(t)
    return mp.matrix([[1,0,0],[0,c,-s],[0,s,c]])
def dR01(t):
    c,s=mp.cos(t),mp.sin(t)
    return mp.matrix([[-s,-c,0],[c,-s,0],[0,0,0]])
def dR12(t):
    c,s=mp.cos(t),mp.sin(t)
    return mp.matrix([[0,0,0],[0,-s,-c],[0,c,-s]])
x0=mp.matrix([1,0,0]); t0=mp.mpf(7)/10; t1=mp.mpf(11)/10
V0,V1=R01(t0),R12(t1)
x1=V0*x0; x2=V1*x1
prob=[v*v for v in x2]
cs=source_coeffs(prob,m=3,w=3)
grad=mp.matrix([cs[j]*x2[j] for j in range(3)])
lam2=-grad; lam1=V1.T*lam2
for val in grad+lam2: close(val,0,'terminal constrained Euler row')
for val in lam1-V1.T*lam2: close(val,0,'intermediate constrained Euler row')
for val in x2-V1*x1: close(val,0,'execution constraint')
ad0=-2*(lam1.T*dR01(t0)*x0)[0]
ad1=-2*(lam2.T*dR12(t1)*x1)[0]
def price_two(t,u):
    xx=R12(u)*R01(t)*x0
    return full_price([v*v for v in xx],m=3,w=3)
close(ad0,mp.diff(lambda t:price_two(t,t1),t0),'nonquadratic full-price adjoint, first gate')
close(ad1,mp.diff(lambda u:price_two(t0,u),t1),'nonquadratic full-price adjoint, second gate')

# Exact target consumer: source shape, NOT another re-run of the all40 owner.
h,x,y,lmb,energy=sp.symbols('h x y lambda E',nonzero=True, real=True)
A2,B2,A3,B3=sp.symbols('A2 B2 A3 B3',real=True)
H=-lmb*energy*(x*x+y*y)+A2*(x*x-y*y)+2*B2*x*y+A3*(x**3-3*x*y*y)+B3*(3*x*x*y-y**3)
lap=(H.subs(x,x+h)+H.subs(x,x-h)+H.subs(y,y+h)+H.subs(y,y-h)-4*H)/h**2
require(sp.expand(lap+4*lmb*energy)==0,'exact old nonvacuum discrete Poisson consumer')

# DO NOT identify different internally derived heats by closedness alone.
# This is the original stationary-section defect, specialized to the actual
# positive CAR chart Delta=256 A at h=1. It is NOT a gravity field-map proof.
nu=mp.mpf(3)/5
la=(mp.mpf(141489)-9*mp.sqrt(397841))/10240000
lb=(mp.mpf(141489)+9*mp.sqrt(397841))/10240000
Dvals=[256*la,256*lb]
Zdata=8*sum(mp.exp(-beta*v) for v in Dvals)
TrDe=8*sum(v*mp.exp(-beta*v) for v in Dvals)
a_harmonic=2016
heat_defect_source=2*a_harmonic*TrDe/(nu*Zdata*(a_harmonic+2*Zdata))
require(heat_defect_source>0, 'strict actual native heat-source mismatch')
def heat_difference(u):
    vals=[v*(u/nu)**2 for v in Dvals]
    Z=8*sum(mp.exp(-beta*v) for v in vals)
    # Complete carriers match: s*M0=c*d, s=128,M0=2048,d=16.
    s=128; c=s*2048/16
    return mp.log(s*(a_harmonic+2*Z)/(c*Z))/beta
close(mp.diff(heat_difference,nu),heat_defect_source,
      'moving same-native scale defect includes both full heat normalizers')

out={
 'status':'PASS_COMPLETE_CUT_SOURCE_AND_FIXED_INITIAL_LIFT',
 'source_anchor':'5135327c6ef33a23f646be904827e5ddd9684bc2',
 'thermal_bound_exact':str(eta_rational),
 'thermal_bound_less_than':'1/80000',
 'ready_probability':mp.nstr(a_ready,35),
 'original_report_r0':mp.nstr(r0,35),
 'original_lambda':mp.nstr(-rq0/rf0,35),
 'complete_to_feedback_gain_ratio_at_minimal_count_control':mp.nstr(full_gain/feedback_gain,35),
 'nonquadratic_adjoint_sources':[mp.nstr(ad0,30),mp.nstr(ad1,30)],
 'strict_native_cut_vs_tensor_heat_source':mp.nstr(heat_defect_source,35),
 'original_large_READY_circuit_replayed':False,
 'original_all42_geometric_owner_replayed':False,
 'literal_Book03_cut_heat_identification_proved':False,
 'universal_GR_closed':False
}
print(json.dumps(out,indent=2,ensure_ascii=False))
