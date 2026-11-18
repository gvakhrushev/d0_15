#!/usr/bin/env python3
"""Exact owner-z finite-difference allocation and empty-start history audit."""
from pathlib import Path
from fractions import Fraction as F
from hashlib import sha256
import itertools,json,sys
P=Path(__file__).resolve().parent;O=P.parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');sys.path.insert(0,str(D/'round30'));import marked_source_schedule as a30
certfile=P/'SUFFICIENT_ENDPOINT_G_CERTIFICATE.json';cert=json.loads(certfile.read_text());assert cert['t']=='2^-1618' and cert['each_rotation_operator_error_strict_lt']=='2^-4852';kplus=int(cert['rotations']['plus']['power_hex'],16);kminus=int(cert['rotations']['minus']['power_hex'],16);assert kplus>0 and kminus>0
# Distinct roles: outer feedback z and report z0 happen both to equal 2^-20.
z=F(1,2**20);d=1-z;s=F(1,2**30);n=1618;B=4852;t=F(1,2**n);delta=F(1,2**B)
bracket=64/d+192*z/d**2+128*z*z/d**3;assert bracket<65
# r/Tr(A)=1 only for the empty H0=C, P0=I, no previous word.
fd=t*t*2**3158*bracket/16
implementation=F(3,2)/d*2**3158*delta/t
assert fd<F(1,2**74) and implementation<F(1,2**74) and fd+implementation<F(1,2**73)
assert fd+implementation<F(1,2**74) and s*(fd+implementation)<F(1,2**104)
# R11: fixed after the common finite prefix; strict (5/6)^(4m)<2^-m.
q=11647;Q=1638;T=75;K=4*(q+3158+Q+T+1);assert K==66076
assert F(3,5)**2+F(3,5)<1 and F(5,6)**4<F(1,2)
heat=F(2)**(q+3158+Q-K//4);assert heat==F(1,2**76)
assert fd+implementation+heat<F(1,2**73) and 55*F(1,2**73)<F(1,2**67)
# General bound: d>=2^-Q and r/Tr(A)<=2^H, Q,H nonnegative.
# n=ceil((3237+3Q)/2), B=n+H+Q+3233; separate errors <2^-74.
for Q in range(1,16):
 for H in range(16):
  nn=(3237+3*Q+1)//2;BB=nn+H+Q+3233
  fdb=F(2)**(3163+3*Q-2*nn);ib=F(3,2)*F(2)**(H+Q+3158+nn-BB)
  assert fdb<=F(1,2**74) and ib<F(1,2**74) and fdb+ib<F(1,2**73)
# EMPTY start is literal: no old stage before A30 first births.
initial=list(itertools.islice(a30.execution_stages(0),4));assert [x['kind'] for x in initial]==['canonical_RAW_birth']*4 and [x['wire'] for x in initial]==[0,1,2,3]
assert initial[0]['role']=='active_port_WORK'
# Full pre/post equalized lengths; selected endpoints enormous but finite.
def align(a,b):
 if a==b:return 0,0
 if a>b:
  y,x=align(b,a);return x,y
 diff=b-a;return {1:(5,4),2:(2,0),3:(5,2)}.get(diff,(diff,0))
pa,pb=align(kplus,kminus);assert kplus+pa==kminus+pb
base=json.loads((D/'round30/COMMON_SOURCE_MARKED_PLAN.json').read_text());N=base['total_RAW_births']+int(base['new_native_call_count'])+kplus+kminus+pa+pb;assert N<2**11647
for length in (pa,pb):assert length==0 or length>=2 and (length%2==0 or length>=5)
def split_pad(x):
 if x==0:return (0,0)
 five=x%2;assert x>=5*five;return ((x-5*five)//2,five)
for early in range(1,8):
 for gates in range(1,7):
  for late in range(0,6):
   direct=sum(2**j for j in range(early))+(gates-1)*2**early+sum(3*2**(early+j) for j in range(late))+2**(early+late)
   assert direct==(gates-3)*2**early+4*2**(early+late)-1
paths=[D/'round30/marked_source_schedule.py',D/'round30/COMMON_SOURCE_MARKED_PLAN.json',P.parents[2]/'d0_retained_response_concentration_2026-10-28/SOURCE_PROOF_RU.md',P.parents[2]/'d0_retained_response_concentration_2026-10-28/RAW_CYLINDER_REALIZATION_RU.md',certfile]
out={'status':'PASS_SUFFICIENT_DETERMINANT_FD_BUDGET','outer_feedback_z':'2^-20 fixed by retained owner; distinct role from report z0','beta':'2p^2','empty_initial_carrier':'H0=C, Omega0=1, P0=I, no previous paid prefix','empty_start_rank_P0':1,'empty_start_Tr_A_old':1,'t':'2^-1618','angular_error_each_lt':'2^-4852','fd_truncation_bound_numerator_hex':hex(fd.numerator),'fd_truncation_bound_denominator_hex':hex(fd.denominator),'endpoint_synthesis_bound_numerator_hex':hex(implementation.numerator),'endpoint_synthesis_bound_denominator_hex':hex(implementation.denominator),'both_terms_and_sum_checked':True,'determinant_FD_error_under_Gamma_s_lt':'2^-74','determinant_FD_error_under_Gamma_s_over_s_lt':'2^-104','generic_t_power_n':'ceil((3237+3Q)/2)','generic_angular_error_bits_B':'n+H+Q+3233','generic_hypotheses':'1-z>=2^-Q; rank(P0)/Tr(A_old)<=2^H; Q,H nonnegative; common scalar retention and gain floor','same_initial_layout_and_last_G':True,'pre_plus_padding_counts_2_5_hex':[hex(x) for x in split_pad(pa)],'pre_minus_padding_counts_2_5_hex':[hex(x) for x in split_pad(pb)],'equal_common_precore_stages_hex':hex(kplus+pa),'endpoint_gate_count_before_retention_hex':hex(N-base['total_RAW_births']),'late_birth_clock_dimension_over_initial':'(L-3)*2^n+4*2^(n+K)-1, where L includes all endpoint gates before retention','sufficient_late_retention_pairs_K':K,'heat_normalized_under_Gamma_s_lt':'2^-76 under R11 hypotheses','determinant_plus_heat_per_SAM_row_under_Gamma_s_lt':'2^-73','corrected_2688_component_Euclidean_error_under_Gamma_s_over_s_lt':'2^-67','isolated_N_lt':'2^11647','source_sha256':{str(f):sha256(f.read_bytes()).hexdigest() for f in paths},'actual_heat_marks_readers_other_source_rows_proved':False,'physical_C_closed':False,'GR_closed':False}
(P/'DETERMINANT_FD_BUDGET.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'z':out['outer_feedback_z'],'fd_ratio_2^73':float(fd*2**73),'implementation_ratio_2^73':float(implementation*2**73),'physical_scaled_lt':'2^-104'}))
