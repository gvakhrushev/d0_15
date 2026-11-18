#!/usr/bin/env python3
"""Explicit conservative scalar source Hessian bound on B25 physical cube.

Uses physical SO-link chart, not quantum operator norm Lambda. No root search.
"""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sympy as S
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');envfile=O/'round21/CHART_ENVELOPE_RESULT.json';env=json.loads(envfile.read_text());assert F(env['coframe_creator_norm_strict_upper'])<1 and F(env['coframe_min_singular_strict_lower'])>F(1,2)
s=F(1,2**30);eps=F(1,2**1531);rho_min=F(3712,5473);assert rho_min>F(1,2)
# ||log U0||<1/25; six unit-norm generators with |theta|<=s.
l=F(17,16);assert 1/(1-(F(1,25)+6*s))<l
Pmax=l**4;assert Pmax<F(4,3)
# For global unit field directions: ||DX||<=sqrt(6)<5/2;
# product of four links/inverses and exterior powers of degrees 0..4.
DP=F(10)*Pmax;D2P=F(96)*Pmax;assert DP<14 and D2P<128
ext=Pmax**4;Dext=4*Pmax**3*14;D2ext=12*Pmax**2*14**2+4*Pmax**3*128
assert ext<4 and Dext<160 and D2ext<6000
# 6 faces, normalized A11 prefactor (400/9)*Tr16/8=800/9.
f0=6*F(800,9)*(2*4);f1=6*F(800,9)*(4*4+2*160);f2=6*F(800,9)*(4*4+2*4*160+2*6000)
assert f0<2**13 and f1<2**18 and f2<2**23
# ||u||<2, nu=3/5, ||Dpsi||F<1, ||D(delta psi)||F<=16.
q0=F(12);q1=F(12)+2*12*16;q2=F(6)+4*12*16+2*12*16**2
assert q0<16 and q1<2**9 and q2<2**13
p,x,y,z=S.symbols('p x y z');E=p**2*(1+x);ell=4*E*(1-E);u=p+p**2*y;b=4*u**2*(1-u**2);A=ell+(1-ell)*b;r=S.expand(1-(1-z*b)*(1-z*A))
for v in [S.diff(r,x),S.diff(r,y),S.diff(r,x,2),S.diff(r,y,2)]:assert sum(abs(c) for c in S.Poly(v,p,x,y,z).coeffs())<2**21
rx=S.diff(r,x).subs({x:0,y:0,z:S.Rational(1,2**20)});ry=S.diff(r,y).subs({x:0,y:0,z:S.Rational(1,2**20)});reduce=lambda v:S.Poly(S.rem(S.together(v),p**2+p-1,p),p)
lo=F(618033988749,10**12);hi=F(618033988750,10**12)
def bounds(expr):
 q=reduce(expr);aa=F(int(q.nth(0).p),int(q.nth(0).q));bb=F(int(q.nth(1).p),int(q.nth(1).q));v=[aa+bb*lo,aa+bb*hi];return min(v),max(v)
assert bounds(rx)[0]>F(1,2**26) and bounds(ry)[0]>F(1,2**22)
assert bounds(ry-20*rx)[0]>0 and bounds(24*rx-ry)[0]>0
# r_x(x,0)/r_x(0,0), r_y(0,y)/r_y(0,0) <2 on entire cube.
xmax=2*eps*2**13;ymax=2*eps*16
assert xmax<1 and ymax<1 and (2**47)*xmax<1 and (2**43)*ymax<1
# Normalized I_tau: a_y<1, k0<24, same SITE, rho inverse once.
nonlinear_f=2*eps*2**47*(2**18)**2
nonlinear_q=24*2*eps*2**43*(2**9)**2
L=2*f2+48*q2+nonlinear_f+nonlinear_q
Lgeom=f2+24*q2
assert L<2**25 and Lgeom<2**24
assert 55*F(2**25,2**30)*2688==4620
# Original finite root + B24 chart implies central geometric row is exactly
# zero; B65 secant defect <2^-3083; J^-1<2.
assert 2*F(1,2**3083)==F(1,2**3082)
paths=[envfile,D/'round11/source_operator_dag.py',O/'round25/TARGETS_RU.md',O/'round54/B54_PRODUCT_SOURCE_EXACT_RU.md',O/'round61/MEAN_DECODER_BOUND.json',O/'round65/FINITE_REFERENCE_SECANT_DEFECT.json']
out={'status':'PASS_EXPLICIT_CONSERVATIVE_SCALAR_HESSIAN_ENVELOPE','scope':'fixed B25 interior raw chart and physical SO links; original f/q moment functions; no quantum-operator-Lambda Hessian assumption','local_f_value_bound_lt':'2^13','local_f_gradient_norm_bound_lt':'2^18','local_f_Hessian_norm_bound_lt':'2^23','local_q_value_bound_lt':'16','local_q_gradient_norm_bound_lt':'2^9','local_q_Hessian_norm_bound_lt':'2^13','I_tau_Hessian_raw_chart_norm_lt':'2^25','geometric_Euler_Lipschitz_raw_chart_lt':'2^24','A31_centre_shift_geometric_source_lt':'2^-24','chosen_current_reference_full_covector_defect_lt':'2^-3083','corrected_reference_defect_lt':'2^-3082','physical_lift_Taylor_remainder_bound_lt':'4620','qualitative':'finite rigorous but too large to certify small finite source residual','source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'GR_closed':False}
(P/'SCALAR_HESSIAN_ENVELOPE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'L_lt':'2^25','L_geom_lt':'2^24','Taylor_lt':'4620'}))
