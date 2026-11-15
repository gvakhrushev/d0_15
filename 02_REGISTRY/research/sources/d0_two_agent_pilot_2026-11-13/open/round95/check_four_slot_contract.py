#!/usr/bin/env python3
"""B95: exact conditional budgets, no actual clock/price claim."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
from math import isqrt
import gzip,json,sys
P=Path(__file__).resolve().parent;B=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
def read(p):return json.loads(p.read_text())
postgrid=read(B/'round80/UNIFORM_GOLDEN_GRID_CERTIFICATE.json');q=int(postgrid['denominator_hex'],16);assert q.bit_length()==20080
macro=read(D/'round38/POST_ANGLE_CERTIFICATE.json');k8=int(macro['rotations']['pi8']['exponent_hex'],16);assert k8<=q
control=read(D/'round47/FULL_VECTOR_CONTROL_PLAN.json');Lc=int(control['each_padded_control_calls_hex'],16)
globalplan=read(D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json');assert globalplan['RAW_births']==11893774624
n=globalplan['RAW_births'];W=sum(int(x,16) for x in globalplan['W_G_CX_componentwise_upper'].values());assert W.bit_length()==24272
m=5376;d=1<<m;L=1<<(m-1)
# Generic A41 stars adapted to m=5376, conditional on the same compiler proof.
postG=4*(d-1)*L*q
postCX=4*((d-1)*(m-1)*L+2*(m*L-d+1));post=postG+postCX
# A42 upper for an arbitrary real Givens probe; q and k8 are actual pinned certificates.
probeG=L*q+40*m*k8;probeCX=(m-1)*L+2*(m-1)+4*m;probe=probeG+probeCX
# Four independent slots each receive a common exact target via paid padding;
# one additional optional post-probe slot covers outgoing probe basis.
slot=max(Lc,probe)+4
Lbase=(W+4)+(post+4)+4*slot+(probe+4)
Nbase=n+Lbase;b=Nbase.bit_length();debt=m+(m+1)//2
K=4*(b+3208+1700+20+75+1+debt)
assert F(5,6)**4<F(1,2) and K%4==0 and K//4>b+3208+1700+20+75+debt
# 6/(359*(8/3))<1; 2p>6/5; the heat per row is strictly below this dyadic bound.
heat=F(1,1<<(K//4-b-3208-1700-20));assert heat<F(1,1<<(debt+75))
# Generic output-plane compiler error and duality, conditional on applicable A41 recipe.
sigma=F(1,1<<80);t=F(1,1<<1700);gs=F(1,1<<3208)
e=F(4*(d-1)*L,1<<20000);mu=F(L+40*m,1<<20000);delta=e+mu
assert e<F(1,1<<9247) and delta<F(1,1<<9247)
postrow=(1<<((m+1)//2+1))*delta/gs+F(1<<m,1)*delta**2/(2*t*gs)
postdual=F(1<<((m+1)//2))*postrow
assert postdual<F(1,1<<661) and e/gs<F(1,1<<6039)
# Absolute 2^-44 source-vector result cannot by itself be divided by unknown g.
glower=F(1,1<<3128);old_jet=F(1,1<<44);assert old_jet/glower>1
# One shared bank error E=Bhat-Btilde: conjugation difference cancels O(E/t).
eB=F(1,1<<3423);eP=F(1,1<<5099)
paired_bank=2*eB/gs;paired_controls=2*eP/(t*gs)
assert paired_bank<F(1,1<<213) and paired_controls<F(1,1<<189)
assert paired_bank+paired_controls<F(1,1<<188)
# Geometric scalar Hessian, separate from operator-valued B91 Hessian.
M2I=1<<25;R=104;geometric=M2I*sigma*R*R;assert geometric<F(1,1<<41)
eM=F(1,1<<3298);corner=eM/gs;assert corner==F(1,1<<90)
# Local and all-label source displacement with proof-specific M1 and no selector.
M1=1748;assert 9*2688<156**2
local_lambda=3*M1*sigma+2*eB;whole_delta=156*M1*sigma+2*eB
assert local_lambda<F(1,1<<67) and whole_delta<F(1,1<<61)
# Conditional A44 kernel: exact S0 reflected, insertion eW, M positive diagonal.
a=F(1,1<<3083);tau=2*a*R+M2I*sigma*R*R+corner
eW=F(1,1<<15800);eU=F(1,1<<9247)
assert tau<F(1,1<<41)
Q=(F(3,4)*(tau*(2*whole_delta**2+2*eW)+eW/gs)+eU/gs)
assert Q<F(1,1<<160)
# Under eBcorner<2^-3421, eD,eR<2^-3302, simple telescope satisfies eM target.
assert 2*F(1,1<<3421)+3*F(1,1<<3302)<eM
pins=[B/'round80/UNIFORM_GOLDEN_GRID_CERTIFICATE.json',B/'round65/SCALAR_HESSIAN_ENVELOPE.json',B/'round91/B91_FULL_VECTOR_JET_CHECK.json',B/'round94/B94_CHECKPOINT.json',D/'round38/POST_ANGLE_CERTIFICATE.json',D/'round47/FULL_VECTOR_CONTROL_PLAN.json',D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json',D/'round42/FIXED_POST_PAID_FAMILY_RU.md',D/'round43/LOCAL_Q_PRICE_RU.md',D/'round44/JOINT_SOURCE_REDUCTION_RU.md']
out={'status':'PASS_CONDITIONAL_FOUR_SLOT_HEAT_AND_KERNEL_CONTRACT','CODE_bits':m,'physical_coordinates':2688,'g_sigma_lower':'2^-3208','sigma':'2^-80','control_step':'2^-1700','upper_only_clock_inputs':True,'hypothetical_padded_Nbase_upper_bit_length':b,'hypothetical_retention_pairs_K':K,'full_plane_dual_dimension_debt_bits':debt,'per_row_heat_lt':'2^-(8064+75)','full_plane_heat_dual_lt':'2^-75','conditional_post_error_lt':'2^-9247','conditional_post_probe_dual_lt':'2^-661','naive_full_vector_bound_over_g_small':False,'paired_shared_bank_error_over_g_lt':'2^-213','paired_control_error_over_g_lt':'2^-189','their_sum_lt':'2^-188','conditional_scalar_curvature_term_lt':'2^-41','required_corner_error_lt':'2^-3298','conditional_corner_over_gsigma_lt':'2^-90','local_single_coordinate_source_displacement_lt':'2^-67','all_label_source_displacement_lt':'2^-61','conditional_Q_vs_half_Pf_lt':'2^-160','exact_actual_clock_or_prices_calculated':False,'full_corner_error_proved':False,'S_reflection_and_all_insertion_hypotheses_proved_here':False,'physical_C_closed':False,'GR_closed':False,'source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in pins}}
(P/'FOUR_SLOT_CONDITIONAL_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('source_sha256',)},indent=2))
