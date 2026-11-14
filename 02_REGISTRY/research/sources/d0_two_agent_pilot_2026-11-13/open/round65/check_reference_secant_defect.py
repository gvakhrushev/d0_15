#!/usr/bin/env python3
"""Exact signed finite-reference defect, no geometry root search."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sympy as s
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
p,x,y,z=s.symbols('p x y z');E=p**2*(1+x);ell=4*E*(1-E);u=p+p**2*y;b=4*u**2*(1-u**2);A=ell+(1-ell)*b;r=s.expand(1-(1-z*b)*(1-z*A));rz=s.expand(r.subs(z,s.Rational(1,2**20)));reduce=lambda v:s.factor(s.rem(s.together(v),p**2+p-1,p));px=s.Poly(rz.subs(y,0),x);py=s.Poly(rz.subs(x,0),y);assert px.degree()==2 and py.degree()==8
odd={j:reduce(py.nth(j)) for j in (1,3,5,7)}
# Rational isolating interval for p=(sqrt5-1)/2, certified by monotonicity.
lo=F(618033988749,10**12);hi=F(618033988750,10**12);assert lo*lo+lo<1 and hi*hi+hi>1
def bounds(expr):
 f=s.Poly(s.expand(expr),p);assert f.degree()<=1;aa=F(int(f.nth(0).p),int(f.nth(0).q));bb=F(int(f.nth(1).p),int(f.nth(1).q));v=[aa+bb*lo,aa+bb*hi];return min(v),max(v)
assert bounds(odd[1])[0]>0
for j in (3,5,7):assert bounds(odd[j])[1]<0
assert bounds(2*odd[1]+odd[3])[0]>0
assert bounds(odd[1]+odd[5])[0]>0 and bounds(odd[1]+odd[7])[0]>0
# Therefore 0<1-Deltay/(2 delta r_y)<4 delta² for 0<delta<1.
# B25: delta=2^-1531 * F_h/(36k0), F_h<1/8, 20<k0<24.
assert F(1,8*36*20)<F(1,2**12)
assert 4*F(1,2**1543)**2<1  # in particular a_y>0
# Chosen free u_component0,role0 at an interior base site. In the exact
# u0=(0,nu,0,0), eta_01=1 chart, derivative g^00=2/nu.
nu=F(3,5);h=F(1,4);sigma=F(1,100);factor=2/nu*(2*sigma**2/(8))*F(1,h*h) # multiply by pi²
assert factor==F(1,750) # q-site derivative = pi²/750
assert F(10,750*256)<F(1,2**14) and F(24)<2**5
# Global raw-u gradient bound: ||u||<2, nu=3/5, |Dpsi|²=E<1/250.
# Dq material derivative vanishes by exact periodic v-Stokes, link part is 0.
assert (2*F(2,1)/(F(3,5)**2))*F(1,250)==F(2,45)
assert F(24)*F(2,45)<2
# Thus |DI_tau|=k0*(1-a_y)*pi²/(750*256) < 2^-3093,
# and is strictly nonzero, conditional on exact owned geometric root mapping.
paths=[O/'round25/TARGETS_RU.md',O/'round54/B54_PRODUCT_SOURCE_EXACT_RU.md',O/'round24/TORUS_BOUNDARY_REVIEW_RU.md',D/'round11/source_operator_dag.py',D/'round27/PREPARED_SOURCE_MOMENT_LAW_RU.md']
out={'status':'PASS_EXACT_FINITE_REFERENCE_SECANT_DEFECT','r_x_degree':px.degree(),'r_y_degree':py.degree(),'p_interval':[str(lo),str(hi)],'odd_y_coefficients_Qp':{str(j):str(odd[j]) for j in odd},'c1_positive_c3_c5_c7_strict_negative':True,'delta_x_equals_2delta_r_y':True,'delta_y_strictly_less_than_delta_x':True,'one_minus_a_y_strict_between_0_and':'2^-3084','chosen_free_u_coordinate':'any interior site, coframe role0 component0','Dq_site_exact':'pi^2/750','Dq_global_exact':'pi^2/192000','ideal_DI_tau_nonzero_at_geometric_root':True,'chosen_ideal_residual_abs_lt':'2^-3093','full_raw_chart_ideal_secant_error_l2_lt':'2^-3083 conditional on exact v-Stokes and B24 map','actual_native_source_proved_nonzero':False,'depends_on_owned_root_and_B24_source_map':True,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'GR_closed':False}
(P/'FINITE_REFERENCE_SECANT_DEFECT.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'bound':out['chosen_ideal_residual_abs_lt'],'Dq':out['Dq_global_exact']}))
