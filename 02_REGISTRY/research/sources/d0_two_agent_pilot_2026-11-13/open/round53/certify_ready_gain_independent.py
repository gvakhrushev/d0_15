#!/usr/bin/env python3
"""Integer-interval A26 readiness and independent Chebyshev B29 gain floor."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
from hashlib import sha256
import json
P=Path(__file__).resolve().parent;D=Path('/Users/grigorijvahrusev/Downloads/d0_pilot_direct_2026-11-13/02_REGISTRY/research/sources/d0_two_agent_pilot_2026-11-13/direct');O=P.parent
files=[D/'round26/consume_full_ready.py',D/'round26/FULL_READY_GAIN_CHECK.json',D/'round25/GLOBAL_H1_PLAN.json',D/'round25/H1_NAMESPACE_PLAN.json',D/'round17/GLOBAL_REPORT_PLAN.json',D/'round12/SELECTOR_COMPILATION.json',D/'round15/PREPROCESSOR_READY_COMPOSITION.json',O/'round29/BUDGET_CERTIFICATE.json',O/'round21/REFERENCE_METADATA.json'];h=lambda x:sha256(x.read_bytes()).hexdigest();pins={str(q):h(q) for q in files};a26=json.loads(files[1].read_text());globalplan=json.loads(files[2].read_text());ns=json.loads(files[3].read_text());local=json.loads(files[4].read_text());sel=json.loads(files[5].read_text());prev=json.loads(files[6].read_text());budget=json.loads(files[7].read_text());meta=json.loads(files[8].read_text())
for path,digest in a26['source_sha256'].items():assert h(Path(path))==digest,path
M=sel['selector_fair_qubits_per_report'];T=sel['padded_interpreter_slots_per_ten_sign_report'];ti=F(sel['ready_probabilities']['internal_slot']);tt=F(sel['ready_probabilities']['top_slot']);assert M==10248262 and T==2*455+8*18==1054 and local['READY_total_flags']==M+T+10+1==10249327 and F(sel['ready_probabilities']['postprocessor'])==1
assert 0<ti<=1 and 0<tt<=1
failure=M*F(53,100)**28+T*(1-ti)**7+10*(1-tt)**7;assert failure==F(prev['failure_union_bound_rational']) and failure<F(1,2)
# Fixed-denominator outward integer intervals. For nonnegative powers all
# endpoint propagation is monotone; signed multiplication uses all corners.
B=1536;Q=1<<B
def lohi(x):return (x.numerator*Q//x.denominator,-(-x.numerator*Q//x.denominator))
def mul(x,y):
 products=[a*b for a in x for b in y];return min(products)//Q,-(-max(products)//Q)
def add(x,y):return (x[0]+y[0],x[1]+y[1])
def sub(x,y):return (x[0]-y[1],x[1]-y[0])
def mul_int(x,n):return (n*x[0],n*x[1]) if n>=0 else (n*x[1],n*x[0])
def powiv(x,n):
 assert n>=0;y=(Q,Q)
 while n:
  if n&1:y=mul(y,x)
  x=mul(x,x);n//=2
 return y
def contains(x,y):return F(x[0],Q)<=y<=F(x[1],Q)
root=isqrt(5*Q*Q);p=((root-Q)//2,(root+2-Q)//2);assert F(p[0],Q)>F(309,500) and F(p[1],Q)<F(619,1000)
fail=sub((3*Q,3*Q),mul_int(p,4));assert 0<fail[0]<=fail[1]<Q
q28=sub((Q,Q),powiv(fail,28));internal=sub((Q,Q),powiv(lohi(1-ti),7));top=sub((Q,Q),powiv(lohi(1-tt),7));alpha=mul(mul(powiv(q28,M),powiv(internal,T)),powiv(top,10));joint=powiv(alpha,7)
assert F(alpha[0],Q)>F(74068,100000) and F(alpha[1],Q)<F(74069,100000)
assert F(joint[0],Q)>F(12229,100000) and F(joint[1],Q)<F(12231,100000)
def parse_interval(txt):
 low,up=txt.strip('[]').split(',');return F(low.strip()),F(up.strip())
for iv,name in [(alpha,'alpha_interval'),(joint,'ideal_seven_report_joint_ready_interval')]:
 l,u=parse_interval(a26[name]);assert l<=F(iv[0],Q)<=F(iv[1],Q)<=u,name
# Independent visibility via Chebyshev: cos(2θ)=2p−1,
# κ=sin²(512θ)=(1−T_512(2p−1))/2. 1536-bit signed interval
# recurrence is independent of the original complex-ball powering method.
x=sub(mul_int(p,2),(Q,Q));t0=(Q,Q);t1=x
for _ in range(1,512):t0,t1=t1,sub(mul_int(mul(x,t1),2),t0)
kappa=( (Q-t1[1])//2, -(-(Q-t1[0])//2) )
kl=F(93793197770933667,10**17);ku=F(93793197770933668,10**17);assert F(kappa[0],Q)>kl and F(kappa[1],Q)<ku
# d=F_h/(36 k0), k0=r_y/r_x. At α>=1/2 the gain
# coefficient = κ p^7 F_h r_x²/72; r_y cancels exactly.
fh=F(meta['F_h_rational']);assert fh==F(16517734400,162621047169);pp=F(309,500);z=F(1,2**20);rx_lower=4*z*(1-4*z)*pp**11;coefficient_lower=kl*pp**7*fh*rx_lower**2/72
assert coefficient_lower>F(1,2**66);assert budget['g_floor_gt']=='2^-3128' and budget['g_times_s_floor_gt']=='2^-3158'
# Exact A25 fraction for e_B=2η and source-floor denominator g s >2^-3158.
def decode(x):return F(int(x['numerator_hex'],16),int(x['denominator_hex'],16))
eta=decode(globalplan['canonical_input_error_bound']);e=2*eta;gs=F(1,2**3158);ratios={'unit_generator':e/gs,'unit_scaled_chart_with_owner_lift':55*e/gs,'unit_physical_chart_with_owner_lift':55*2**30*e/gs};limits={'unit_generator':73,'unit_scaled_chart_with_owner_lift':67,'unit_physical_chart_with_owner_lift':37}
for name,val in ratios.items():assert val<F(1,2**limits[name]) and val==decode(a26['conditional_native_only_normalized_error'][name]['exact_conservative_ratio'])
for path,digest in pins.items():assert h(Path(path))==digest,path
out={'status':'PASS_INDEPENDENT_INTEGER_READY_AND_GAIN_FLOOR','input_sha256':pins,'integer_interval_bits':B,'selector_and_ready_counts':{'fair_banks':M,'internal_slots':T,'top_slots':10,'postprocessor':1,'READY_flags':local['READY_total_flags']},'alpha_interval_strict':'0.74068 < alpha < 0.74069','alpha_seven_joint_strict':'0.12229 < alpha^7 < 0.12231','A26_outward_intervals_contain_independent_integer_intervals':True,'union_failure_lt_half':True,'kappa_chebyshev_strict_interval':'0.93793197770933667 < κ < 0.93793197770933668','gain_coefficient_simplified':'κ p^7 F_h r_x^2 /72 at alpha=1/2','gain_coefficient_gt':'2^-66','g_gt_given_original_law':'2^-3128','g_times_s_gt_given_original_law':'2^-3158','native_only_normalized_bounds':{q:'2^-'+str(n) for q,n in limits.items()},'scope':'Consumes ideal per-report READY identity effect and actual fresh/disjoint bindings. Does not independently prove original H1 moment law, marks, physical admission, alpha_hat field-independence, or full T10/Info.','physical_C_closed':False,'GR_closed':False}
(P/'READY_GAIN_INTEGER_INDEPENDENT_CHECK.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({'status':out['status'],'alpha':out['alpha_interval_strict'],'gain_coefficient_gt':out['gain_coefficient_gt']}))
