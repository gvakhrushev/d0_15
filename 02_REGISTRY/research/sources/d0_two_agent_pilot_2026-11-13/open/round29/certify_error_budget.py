#!/usr/bin/env python3
"""Outward-interval/rational conditional H.1 gain and error allocations.
No claim that the full target readiness or final native writer exists.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,mpmath as mp
P=Path(__file__).resolve().parent
root=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct')
a13=root/'round13/CIRCUIT_COMPILATION.json';r21=P.parent/'round21/REFERENCE_METADATA.json'
compile=json.loads(a13.read_text());meta=json.loads(r21.read_text());cost=compile['decoder_label_routing_counts_per_report']
assert cost=={'X':3776997052,'CX':9400485374,'CCX':9403481772}
N_X=7*cost['X'];N_CCX=7*cost['CCX'];N_CX=7*cost['CX'];N=N_X+N_CCX
assert N==92263351768 and N<2**37
# Interval p and visibility via exact owner integer power of cos+i sin, not numerical asin.
mp.iv.dps=140;iv=mp.iv;p=(iv.sqrt(5)-1)/2;a=iv.sqrt(p);re,im=iv.mpf(1),iv.mpf(0);cr,ci=a,p;n=512
while n:
 if n&1:re,im=re*cr-im*ci,re*ci+im*cr
 cr,ci=cr*cr-ci*ci,2*cr*ci;n//=2
kappa=im*im;z=iv.mpf(1)/2**20;ell=4*p**3;Q=1-z*ell;R=1-z*ell*(1+p**6)
rx=4*z*Q*p**11;ry=8*z*p**6*(R+Q*p**6);k0=ry/rx
Fh=F(meta['F_h_rational']);Fiv=iv.mpf(Fh.numerator)/Fh.denominator;d=Fiv/(36*k0)
# g = [2 κ p^7 d rx ry α²] 2^-3062, Λ=2^1525, ε=2^-1531.
# Evaluate conservative α=1/2 only CONDITIONALLY on full ideal reporter.
Cfloor=2*kappa*p**7*d*rx*ry/4
assert kappa>iv.mpf('0.93793197770933667') and kappa<iv.mpf('0.93793197770933668')
assert rx>0 and ry>0 and d>0 and Cfloor>iv.mpf(1)/2**66
assert F(619,1000)**7<F(1,25) # p<.619 => c_target >=1-12p^7 >13/25
eta=F(1,2**3169);eB=2*eta;gsfloor=F(1,2**3158)
assert eB/gsfloor==F(1,2**10)
logical_error=F(1,2**3207);known=N*logical_error;reserve=F(1,2**3170)
assert known<reserve and known+reserve<eta
assert N*F(1,2**4096)<F(1,2**4059) and F(1,2**4059)<F(1,2**3206)
# Illustrative T10 total 2^-9 if L<=1000; p²=1-p<191/500.
assert F(1000*2688*191,500*2**30)<F(1,2**10)
# H.5 right inverse for scaled coordinates: u=2p sqrt(p)>24/25,
# sqrt(2688)<52, hence K=sqrt(m)/u<55. The physical unit lift
# uses K/s, not K; this is a separate factor from the gain denominator.
assert F(2)*F(309,500)*F(39,50)>F(24,25) and F(39,50)**2<F(309,500)
assert 2688<52**2 and F(52*25,24)<55
# Scaled-chart or unit-physical lift budgets with target native error 2^-10.
for eta_exp, gate_exp, factor in [(3175,3213,F(55)),(3205,3243,F(55)*2**30)]:
 eta_i=F(1,2**eta_exp); delta_i=F(1,2**gate_exp)
 assert N*delta_i<F(1,2**(eta_exp+1))
 assert (2*eta_i/gsfloor)*factor<F(1,2**10)
# Example total scaled T10 error <2^-9 under the ADDITIONAL L<=10.
assert F(55*10*2688*191,500*2**30)<F(1,2**10)
# Example EACH leaf-reader mark threshold μ=2^-3168, max norm 32*A<2^17:
# 2*65568*2^-3187 < 2^-3169, reader error may independently use <=2^-3169.
mark_mu=F(1,2**3168);mark_eta=F(1,2**3187);mark_other=F(1,2**3169)
assert 2*65568*mark_eta+mark_other<mark_mu
# Human-readable values are diagnostics; dyadic assertions above are interval certified.
mp.mp.dps=100;pp=(mp.sqrt(5)-1)/2;zz=mp.mpf(1)/2**20;ll=4*pp**3;qq=1-zz*ll;rr=1-zz*ll*(1+pp**6)
xx=4*zz*qq*pp**11;yy=8*zz*pp**6*(rr+qq*pp**6);kk=yy/xx;dd=(mp.mpf(Fh.numerator)/Fh.denominator)/(36*kk)
kap=mp.sin(512*mp.atan2(pp,mp.sqrt(pp)))**2;cf=2*kap*pp**7*dd*xx*yy/4
c=lambda x:mp.nstr(x,30)
result={'status':'PASS_OUTWARD_INTERVAL_CONDITIONAL_GATE_TO_SOURCE_BUDGET','scope':'ideal full reporter alpha >=1/2 is a hypothesis; physical alpha and physical C not proved',
 'A':2049,'m':2688,'Lambda_h':'2^1525','epsilon_h':'2^-1531','s':'2^-30','alpha_full_target_lower_bound_assumption':'1/2, NOT established by A12 component',
 'reference_d_h_interval':str(d),'r_x_interval':str(rx),'r_y_interval':str(ry),'kappa_interval':str(kappa),
 'coefficient_at_alpha_half_interval':str(Cfloor),'coefficient_gt':'2^-66','g_floor_gt':'2^-3128','g_times_s_floor_gt':'2^-3158',
 'diagnostic':{'kappa':c(kap),'d_h':c(dd),'r_x':c(xx),'r_y':c(yy),'g_log2_at_alpha_half':c(mp.log(cf,2)-3062),'g_s_log2_at_alpha_half':c(mp.log(cf,2)-3092)},
 'A13_per_report_logical_counts':cost,'seven_reports_in_A_assumption':True,'seven_known_counts':{'X':N_X,'CCX':N_CCX,'CX_exact_if_native':N_CX,'approx_X_plus_CCX':N},
 'A14_hypothetical_2^-4096_per_gate':'the known seven-report X+CCX sum <2^-4059; A14 certificate and complete remaining assembly not verified here',
 'illustrative_budget':{'eta_total_le':'2^-3169','e_B_le':'2^-3168','T10_native_term_strict_lt':'2^-10','uniform_error_per_known_X_CCX':'2^-3207','known_gate_sum_lt':'2^-3170','all_other_errors_reserved_le':'2^-3170','CCX_angle_error_le':'2^-3207/3 if A14 bound 3*angle_error applies'},
 'illustrative_T10_total':'<2^-9 ||X|| only if L<=1000 and all other H1 hypotheses hold; no value of L certified here',
 'H5_right_inverse':{'scaled_chart_norm_strict_lt':55,'unit_physical_field_norm_strict_lt':'55*2^30','assumptions':'owner J_j and same target chart; Neumann correction for actual marks not included'},
 'scaled_chart_lift_example':{'eta_total_le':'2^-3175','e_B_le':'2^-3174','per_known_X_CCX':'2^-3213','all_other_errors_le':'2^-3176','post_lift_native_term':'<2^-10 for unit scaled chart vector','additional_Taylor_condition':'L<=10 suffices for separate <2^-10 Taylor term; L not established'},
 'physical_unit_lift_example':{'eta_total_le':'2^-3205','e_B_le':'2^-3204','per_known_X_CCX':'2^-3243','all_other_errors_le':'2^-3206','post_lift_native_term':'<2^-10 per unit physical field vector; actual mark right inverse and Jacobian not certified'},
 'illustrative_mark':{'leaf_norm_upper':65568,'eta_prefix_le':'2^-3187','independent_reader_error_le':'2^-3169','mark_abs_error_lt':'2^-3168','not_a_required_accuracy':'illustrative per-prefix allocation'},
 'actual_scalar_corner_lower':'>13/25-e_B>1/2 when T6 structure holds',
 'GR_closed':False}
(P/'BUDGET_CERTIFICATE.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:result[k] for k in ['status','g_floor_gt','g_times_s_floor_gt','seven_known_counts','illustrative_budget','diagnostic']}))
