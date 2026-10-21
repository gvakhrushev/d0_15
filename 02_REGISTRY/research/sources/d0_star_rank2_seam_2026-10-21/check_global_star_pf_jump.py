#!/usr/bin/env python3
"""Exact rank-two original-six-face truncation and nonuniform-PF material
obstruction for the SAME N=1 native GoldenMaster, NOT a selected full Book law.
"""
from __future__ import annotations
import sys,json
from pathlib import Path
import numpy as np
import sympy as s
from scipy.special import erfi
from scipy.optimize import brentq
from check_star_rank2_seam import cell,star_density,KAPPA
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/"02_REGISTRY/research/sources/d0_weighted_two_field_rank2_2026-10-21"))
from native_master import GoldenMaster

r,h=s.symbols('r h',positive=True)
T=s.exp(-r*r/2)
A=s.sqrt(r)*s.exp(-r*r/4)
B=s.exp(r*r/4)/s.sqrt(r)
k1=(1-r**-2)/2
k2=s.exp(-r*r/4)/s.sqrt(r)
Dt=lambda f:s.simplify(T*s.diff(f,r))
time0=s.simplify(r*r*Dt(k1)+2*B*r*Dt(k2))
space0=s.simplify(2*A*r*k1*k2+A*B*k2*k2)
assert s.simplify(time0+space0)==0
lead=s.factor((r*r*Dt(Dt(k1))+2*B*r*Dt(Dt(k2)))/2)
expected=3*(r**4-1)*s.exp(-r*r)/(4*r*r)
assert s.simplify(lead-expected)==0
assert lead.subs(r,1)==0
assert lead.subs(r,s.Rational(6,5))!=0

# The noncommutative finite TWO-boost spatial plaquette, actual P-P^-1.
x,y=s.symbols('x y',real=True)
def bb(k,t):
    U=s.eye(3)
    U[0,0]=U[k,k]=s.cosh(t)
    U[0,k]=U[k,0]=s.sinh(t)
    return U
Bi=B1=bb(1,x); Bj=bb(2,y)
P=Bi*Bj*Bi.subs(x,-x)*Bj.subs(y,-y)
bcomm=s.sinh(x)*s.sinh(y)*(1-(s.cosh(x)-1)*(s.cosh(y)-1)/2)
assert s.trigsimp((P[1,2]-P[2,1])/2-bcomm)==0

def time_at_r(R):
    return np.sqrt(np.pi/2)*(erfi(R/np.sqrt(2))-erfi(1/np.sqrt(2)))
def radii(tt):
    f=lambda R:time_at_r(R)-tt
    return brentq(f,.6,1.7,xtol=5e-15)
def k(R):
    return ((1-R**-2)/2,np.exp(-R*R/4)/np.sqrt(R))
def scalar_closed(R,Next,hval):
    aa=np.sqrt(R)*np.exp(-R*R/4)
    bb_=np.exp(R*R/4)/np.sqrt(R)
    kx,ky=k(R);knx,kny=k(Next)
    BC=lambda q,w:np.sinh(q)*np.sinh(w)*(1-.5*(np.cosh(q)-1)*(np.cosh(w)-1))
    temp=R*R*np.sinh(hval*(knx-kx))+2*bb_*R*np.sinh(hval*(kny-ky))
    spatial=2*aa*R*BC(hval*kx,hval*ky)+aa*bb_*BC(hval*ky,hval*ky)
    return (temp+spatial)/(hval*hval)

native=GoldenMaster(65)
a=float(native.a)
fxy=float(native.hxy)
assert a<0 and fxy<0
tau=.05
amp=(1/(2*KAPPA))**.5
R=1.2
first=float(expected.subs(r,s.Rational(6,5)))
PF_L,PF_R=1.,2.
limit=2*amp*tau*(fxy/a)*first*(1/PF_L-1/PF_R)
assert limit>0
uniform=[];jump=[]
for n in (16,32,64,128,256,512):
    hh=1/n
    now=time_at_r(R)
    pm,cc,nx=[cell(now+dt,hh,amp) for dt in (-hh,0,hh)]
    fprev=float(star_density(pm,cc,hh).real)
    fcur=float(star_density(cc,nx,hh).real)
    cal=scalar_closed(R,radii(now+hh),hh)
    assert abs(cal-fcur)<4e-12
    assert abs(fcur/hh-first)<.3/n**.5  # controlled convergence diagnostic
    def slope(ff,rho):
        return float(-native.fy(-tau*ff/rho,0)/native.a)
    smoothprev=1+.2*np.sin(3*(now-hh))
    smoothnow=1+.2*np.sin(3*now)
    e_smooth=2*amp*(slope(fprev,smoothprev)-slope(fcur,smoothnow))/hh
    e_jump=2*amp*(slope(fprev,PF_L)-slope(fcur,PF_R))/hh
    assert abs(e_smooth)<.25*hh
    assert abs(e_jump-limit)<.6*hh
    uniform.append({'n':n,'finite_fstar_over_h':fcur/hh,
                    'scalar_material_smooth_rho':e_smooth})
    jump.append({'n':n,'rho_previous':PF_L,'rho_current':PF_R,
                 'scalar_material_pf_jump':e_jump})
print(json.dumps({
 'status':'PASS_STAR_GLOBAL_TRUNCATION_AND_PF_JUMP_CONTROL',
 'analytic_original_six_face':{
    'zero_continuum_R':'r^2 k1_t+2 B r k2_t+2 A r k1 k2+A B k2^2=0',
    'finite_coefficient':'3*(r^4-1)*exp(-r^2)/(4*r^2)',
    'commutator_rotation_exact':'sinh(x)sinh(y)[1-(cosh(x)-1)(cosh(y)-1)/2]',
    'special_r_equal_1':'the O(h) coefficient vanishes ONLY at this center'},
 'native_model':'same GoldenMaster sigma-minus, no sigma-plus substitution',
 'pf_jump_limit_predicted':limit,'smooth_samples':uniform,'jump_samples':jump,
 'scope':{'actual_native_PF_counts_have_jumps':False,
          'bounded_PF_positivity_alone_suffices':False,
          'smooth_PF_or_compensating_discrete_source_needed':True,
          'full42_exact_finite_root_proved':False,
          'Book03_compulsory_selection_proved':False,
          'GR_closed':False}},indent=2))
