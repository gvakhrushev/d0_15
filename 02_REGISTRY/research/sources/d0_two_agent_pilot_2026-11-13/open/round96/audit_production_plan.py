#!/usr/bin/env python3
"""Independently recalculate declared A49 padded lengths and heat bounds."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import json,sys
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round49'));import two_bit_paid_family as f
plan=json.loads((D/'round49/TWO_BIT_PAID_FAMILY_PLAN.json').read_text());c=f.production_configuration();ap=f.control.control_plan();gp=json.loads((D/'round48/TWO_BIT_GLOBAL_SOURCE_PLAN.json').read_text());m=5376;assert c['m']==m
n=gp['RAW_births'];q=int(json.loads((P.parent/'round80/UNIFORM_GOLDEN_GRID_CERTIFICATE.json').read_text())['denominator_hex'],16);k8=int(json.loads((D/'round38/POST_ANGLE_CERTIFICATE.json').read_text())['rotations']['pi8']['exponent_hex'],16);W=sum(int(v,16) for v in gp['W_G_CX_componentwise_upper'].values());L=1<<(m-1);d=1<<m
postG=4*(d-1)*L*q;postCX=4*((d-1)*(m-1)*L+2*(m*L-d+1));coreL=W+4;postL=postG+postCX+4
probeL=L*q+40*m*k8+(m-1)*L+2*(m-1)+4*m+4;controlL=int(ap['each_padded_control_calls_hex'],16)+4
base=coreL+postL+probeL+4*controlL;Nbase=n+base;K=4*(Nbase.bit_length()+3208+1700+20+75+1+m+(m+1)//2)
for key,value in [('coreL',coreL),('postL',postL),('probeL',probeL),('controlL',controlL),('Lbase',base),('Nbase',Nbase)]:assert c[key]==value==int(plan['exact_new_padded_lengths_hex'][key],16),key
assert K==175604==plan['late_retention_pairs'] and Nbase.bit_length()==30833
assert int(plan['actual_native_calls_hex'],16)==base+K and int(plan['clock_layers_N_hex'],16)==Nbase+2*K
z=F(1,1<<20);t=F(1,1<<1700);gs=F(1,1<<3208);e=F(4*(d-1)*L,1<<20000);mu=F(L+40*m,1<<20000);delta=e+mu;half=(m+1)//2
post_dual=(1<<half)*((1<<(half+1))*delta/gs+(1<<m)*delta*delta/(2*t*gs));heat=F(6*Nbase,359)/(t*(F(8,3)*z*gs))*F(1,1<<(K//4))
def dec(z):return F(int(z['numerator_hex'],16),int(z['denominator_hex'],16))
assert dec(plan['bounds']['post_full_operator_error'])==e and dec(plan['bounds']['probe_full_operator_error'])==mu
assert dec(plan['bounds']['post_independent_skew_dual_finite_feedback_error'])==post_dual and post_dual<F(1,1<<661)
assert dec(plan['bounds']['heat_one_price_contrast'])==heat and dec(plan['bounds']['heat_full_skew_dual'])==(1<<(m+half))*heat<(F(1,1<<75))
assert plan['production_target_entries_or_word_evaluated'] is False and plan['whole_price_stationarity_proved'] is False
out={'status':'PASS_A49_PRODUCTION_PADDED_UPPER_CLOCK_ARITHMETIC','CODE_bits':m,'RAW_early_births':n,'four_additional_control_reserves_included':16,'Nbase_bit_length':Nbase.bit_length(),'retention_pairs':K,'all_padded_length_expressions_match':True,'post_dual_lt':'2^-661','heat_dual_lt':'2^-75','uppers_become_exact_lengths_only_if_padto_finishes':True,'full_production_word_or_tariff_evaluated':False,'original_marks_or_physical_admission_proved':False,'GR_closed':False}
(P/'PRODUCTION_PLAN_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
