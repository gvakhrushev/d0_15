#!/usr/bin/env python3
"""Independent A50 bounds from raw A47/A48/A49/B97 receipts, not A50 code."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
read=lambda p:json.loads(p.read_text());plan=read(D/'round50/INDEPENDENT_PRICE_ROWS_PLAN.json');b48=read(D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json');b49=read(D/'round49/TWO_BIT_PAID_FAMILY_PLAN.json');a47=read(D/'round47/FULL_VECTOR_CONTROL_PLAN.json');b97=read(O/'round97/FIXED_POST_WEIGHT_CHECK.json');third=read(O/'round97/SCALAR_THIRD_DERIVATIVE_CHECK.json')
for p,h in plan['source_sha256'].items():assert sha256(Path(p).read_bytes()).hexdigest()==h,p
Dq=lambda z:F(int(z['numerator_hex'],16),int(z['denominator_hex'],16))
sigma=F(1,1<<80);t=F(1,1<<1700);gs=F(1,1<<3208);z=F(1,1<<20);a=F(1,1<<3083)
eW=Dq(b48['errors']['replacement_error']);eM=Dq(b48['errors']['full_canonical_compressed_error']);ep=Dq(b48['errors']['full_SOURCE_DATA_fibre_prefix_error']);eU=Dq(b49['bounds']['post_full_operator_error']);eP=Dq(a47['control_vs_exp_tX_error']);heat=Dq(b49['bounds']['heat_one_price_contrast'])
assert eW<F(1,1<<15800) and ep<F(1,1<<3423) and eM<F(1,1<<3421)
assert 9*2688<156*156
radius=156*1748*sigma+2*ep;assert radius<F(1,1<<61)
tau=2*a*104+(1<<25)*sigma*104**2+eM/gs;assert tau<F(1,1<<41)
qK=F(3,4)*(tau*(2*radius*radius+2*eW)+eW/gs);post=eU/gs;qA=qK+post;assert qA<F(1,1<<160)
bracket=8/(1-z)+24*z/(1-z)**2+16*z*z/(1-z)**3
taylor=t*t*bracket/(16*gs);native=2*eP/(t*gs);finite=taylor+native+heat
assert taylor<F(1,1<<192) and native<F(1,1<<190) and heat<F(1,1<<8139)
assert third['I_tau_third_derivative_norm_lt']=='2^31' and b97['actual_Pf_price_source_row_lt']=='2^-108'
scalar=F(1<<31)*sigma*sigma*104**3/3;weight=F(3,2)*F(1,1<<3061)*2*(1<<15)*3*F(3,2)*(1<<20);corner=F(3,2)*eM/gs
reduced=scalar+weight+corner+a;pf=reduced+post+finite;qrow=reduced/2+qA+finite;pb=post+finite
assert max(pf,qrow)<F(1,1<<108) and pb<F(1,1<<189)
qhalf=qA+post/2+F(3,2)*finite;assert qhalf<F(1,1<<159)
all2=2688*(pf**2+2*qrow**2+pb**2);assert all2<F(1,1<<204)
allpf=F(3,2)*tau+post;allq=F(3,4)*tau+qA
assert allpf<F(1,1<<40) and allq<F(1,1<<41) and post<F(1,1<<6039)
for key,val in {'full_profile_insertion_replacement_error':eW,'whole_label_reflected_prefix_distance':radius,'centred_M_spread_over_g_sigma':tau,'Qb_analytic_minus_half_reduced_Pf':qA,'post_analytic_error':post,'finite_J_Taylor':taylor,'independent_native_control_error':native,'heat_each_paid_row':heat,'reduced_Pf_vs_DI':reduced-a,'Pf_full_price_each_axis':pf,'Qf_Qb_full_price_each_axis':qrow,'Pb_full_price_each_axis':pb,'Qb_full_price_minus_half_Pf_full_price':qhalf,'all_four_2688_axis_rows_Euclidean_norm_squared':all2,'arbitrary_CODE_skew_Pf_analytic_dual':allpf,'arbitrary_CODE_skew_Q_analytic_dual':allq}.items():assert Dq(plan['bounds'][key])==val,key
out={'status':'PASS_INDEPENDENT_A50_ROW_ARITHMETIC_AND_NORM','actual_kernel_assumed_symmetric':False,'Qb_analytic_vs_half_reduced_lt':'2^-160','Qb_finite_vs_half_Pf_lt':'2^-159','Pf_Qf_Qb_each_axis_lt':'2^-108','Pb_each_axis_lt':'2^-189','four_by_2688_Euclidean_norm_lt':'2^-102','arbitrary_skew_Pf_analytic_dual_lt':'2^-40','arbitrary_skew_Q_analytic_dual_lt':'2^-41','arbitrary_skew_Pb_analytic_dual_lt':'2^-6039','all_skew_finite_dual_or_original_Vh_norm_proved':False,'production_word_executed':False,'GR_closed':False}
(P/'INDEPENDENT_ROW_BOUNDS_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
