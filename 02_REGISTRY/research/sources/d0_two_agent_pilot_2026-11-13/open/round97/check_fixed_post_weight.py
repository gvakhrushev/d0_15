#!/usr/bin/env python3
"""A49 actual fixed-post feedback weight, corrected scalar source and bounds."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sympy as sp
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
get=lambda p:json.loads(p.read_text());m3=get(P/'SCALAR_THIRD_DERIVATIVE_CHECK.json');assert m3['I_tau_third_derivative_norm_lt']=='2^31'
bridge=get(D/'round49/CORNER_AND_PRICE_BRIDGE.json');assert bridge['status']=='TYPED_FOUR_VALUED_IDEAL_MOMENT_LAW_AND_ACTUAL_CORNER_GATE'
cplan=get(D/'round49/TWO_BIT_PAID_FAMILY_PLAN.json');A47=get(D/'round47/FULL_VECTOR_CONTROL_PLAN.json');b29=get(O/'round29/BUDGET_CERTIFICATE.json')
decode=lambda z:F(int(z['numerator_hex'],16),int(z['denominator_hex'],16))
eM=decode(bridge['mathematical_cold_corner_error']);eU=decode(cplan['bounds']['post_full_operator_error']);eP=decode(A47['control_vs_exp_tX_error']);heat=decode(cplan['bounds']['heat_one_price_contrast'])
sigma=F(1,1<<80);step=F(1,1<<1700);gs=F(1,1<<3208);z=F(1,1<<20)
assert eM<F(1,1<<3421) and eU<F(1,1<<9247) and eP<F(1,1<<5099)
# Exact independent finite-dimensional algebra including arbitrary diagonal E.
c,g,st=sp.symbols('c g st',nonzero=True,real=True);f0,f1,f2=sp.symbols('f0 f1 f2',real=True);e0,e1,e2=sp.symbols('e0 e1 e2',real=True)
Fmat=sp.diag(f0,f1,f2);E=sp.diag(e0,e1,e2);M0=c*sp.eye(3)-2*g*Fmat;M=M0+E;X=sp.Matrix([[0,-1,0],[1,0,0],[0,0,0]]);phi=sp.Matrix([sp.Rational(3,5),sp.Rational(4,5),0]);comm=lambda A:A*X-X*A
moment=lambda A:(phi.T*A*phi)[0]
lhs=-moment(comm(M*M))/(4*c*g*st)
rhs=moment(comm(Fmat))/st-g*moment(comm(Fmat*Fmat))/(c*st)-moment(comm(M*M-M0*M0))/(4*c*g*st)
assert sp.simplify(lhs-rhs)==0
# g=2 kappa p^7 d_h eps^2 alpha² r_x r_y; exact B29 interval
# uppers <1, 0<alpha<=1, 0<kappa<=1, 0<p<1.
def upper(key):return F(b29[key].strip('[]').split(',')[1].strip())
assert upper('reference_d_h_interval')<1 and upper('r_x_interval')<1 and upper('r_y_interval')<1 and upper('kappa_interval')<1
epsilon=F(1,1<<1531);gupper=2*epsilon**2;assert gupper==F(1,1<<3061)
Imax=1<<15;I1=1<<20;Lsum=F(3,2)
# For the four local digits, any single-coordinate separation <=3sigma;
# ||[I,X_j]|| <= 3sigma*Lsum*I1.
weighted=F(3,2)*gupper*2*Imax*3*Lsum*I1
assert weighted<F(1,1<<3021)
# Norm ||Mhat^2-M0^2||<=2 eM (both contractions), and c_ref>2/3.
actual_corner=F(3,2)*eM/gs;post_error=eU/gs
assert actual_corner<F(1,1<<212) and post_error<F(1,1<<6039)
scalar_bias=F(1<<31)*sigma**2*104**3/3;assert scalar_bias<F(1,1<<109)
# A42 finite-J third derivative, two independently compiled endpoints, and
# the actual A49 common clock heat (not assumed exactly zero).
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
finite_taylor=step**2*bracket/(16*gs);control=2*eP/(step*gs)
assert finite_taylor<F(1,1<<192) and control<F(1,1<<190) and heat<F(1,1<<8139)
source_error=scalar_bias+weighted+actual_corner+post_error+finite_taylor+control+heat
assert source_error<F(1,1<<108)
centre=F(1,1<<3083);assert source_error+centre<F(1,1<<108)
paths=[P/'SCALAR_THIRD_DERIVATIVE_CHECK.json',O/'round95/QUADRATIC_LIFT_CHECK.json',O/'round96/CORNER_LAW_CHECK.json',O/'round96/PRICE_BRIDGE_CHECK.json',D/'round47/FULL_VECTOR_CONTROL_PLAN.json',D/'round49/TWO_BIT_PAID_FAMILY_PLAN.json',D/'round49/CORNER_AND_PRICE_BRIDGE.json',O/'round29/BUDGET_CERTIFICATE.json',O/'round65/FINITE_REFERENCE_SECANT_DEFECT.json']
out={'status':'PASS_A49_BORN_PRODUCT_FIXED_POST_WEIGHTED_SCALAR_SOURCE','exact_weighted_correction_identity_checked':True,'identity':'d_Pf=D_sigma I-(g/c_ref)D_sigma(I^2)-<[Mhat^2-M0^2,X]>/(4 c_ref g sigma)','scope':'A49 empty initial H0=C, fixed actual post, born product CODE, selected typed source/private RAW fibre, original same-reader H+J gain','conditional_g_upper_lt':'2^-3061','normalized_weight_correction_lt':'2^-3021','actual_compressed_corner_correction_lt':'2^-212','actual_post_correction_lt':'2^-6039','scalar_quadratic_remainder_lt':'2^-109','finite_J_taylor_lt':'2^-192','independent_control_angle_error_lt':'2^-190','growing_clock_heat_row_lt':'2^-8139','total_Pf_full_price_vs_DI_tau_centre_lt':'2^-108','original_B65_centre_DI_tau_lt':'2^-3083','actual_Pf_price_source_row_lt':'2^-108','production_path_sum_or_word_executed':False,'arbitrary_correlated_old_input_weight_closed':False,'other_three_price_rows_closed':False,'original_Dnu_or_Cost_Info_admission_proved':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths}}
(P/'FIXED_POST_WEIGHT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='source_sha256'}))
