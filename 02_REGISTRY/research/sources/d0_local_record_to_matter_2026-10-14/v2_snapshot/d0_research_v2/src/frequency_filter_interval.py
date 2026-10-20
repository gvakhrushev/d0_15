"""Full-record count-window preparation: interval certification, not a selected rare word.
All paths with an allowed error count are accepted; every path and direction stays
in the retained register. The spatial marginal is a binomial polynomial of E.
"""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import mpmath as mp
R=Path(__file__).resolve().parents[1];OLD=R/'input_v1/d0_local_matter_bridge'
spec=importlib.util.spec_from_file_location('v1_features_frequency',OLD/'src/interval_l8.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
mp.mp.dps=70;mp.iv.dps=60;iv=mp.iv
checks=[]
def ck(n,b):
 if not bool(b):raise AssertionError(n)
 checks.append(n)
def val(q,ctx):return ctx.mpf(q[0])+ctx.mpf(q[1])*ctx.sqrt(2)
L=8;N=L**4;rows=f.features();g=((iv.sqrt(5)-1)/2)**3
gp=((mp.sqrt(5)-1)/2)**3
A1=iv.mpf(128)-64*iv.sqrt(2);e1=g*A1/(4*L*L);e1p=gp*mp.sin(mp.pi/L)**2
eps=iv.mpf(1)/L**10
T=int(mp.ceil(16/e1p*mp.log(L**4*(L**10)/4)))
lo=int(mp.ceil(T*e1p/2));hi=int(mp.floor(3*T*e1p/2))
ck('integer_lower_count_exact',iv.mpf(lo-1)<T*e1/2 and T*e1/2<iv.mpf(lo))
ck('integer_upper_count_exact',iv.mpf(hi)<3*T*e1/2 and 3*T*e1/2<iv.mpf(hi+1))
ck('vacuum_exactly_excluded',lo>=1)
falsebound=iv.exp(-T*e1/16);truefailure=2*iv.exp(-T*e1/12)
ck('multiplicative_Chernoff_target',L**4*falsebound/4<eps)
ck('first_shell_acceptance_at_least_half',truefailure<iv.mpf('0.5'))
cache={}
def accept(A):
 if A==(0,0):return iv.mpf(0)
 if A in cache:return cache[A]
 ee=g*val(A,iv)/(4*L*L)
 ck('effect_valid_'+str(A),0<ee and ee<1)
 w=iv.mpf(math.comb(T,lo))*ee**lo*(1-ee)**(T-lo)
 total=w
 for k in range(lo,hi):
  w*=iv.mpf(T-k)/(k+1)*ee/(1-ee);total+=w
 cache[A]=total
 return total
Z=iv.mpf(0);tail=iv.mpf(0);first=iv.mpf(0);EA=iv.mpf(0);EB=iv.mpf(0)
for (A,B),mul in rows:
 pp=accept(A);w=mul*pp
 Z+=w;EA+=w*val(A,iv);EB+=w*val(B,iv)
 if A==(128,-64):first+=w
 else:tail+=w
prob=Z/N;distance=tail/Z
ck('actual_conditional_trace_error_below_target',distance<eps)
ck('finite_preparation_not_exact_projector',distance>0)
ck('success_lower_improved',prob>iv.mpf(4)/N)
ck('success_approximately_first_shell_prior',prob>iv.mpf('0.0019531249') and prob<iv.mpf('0.0019531251'))
ck('Chernoff_is_actually_conservative',distance<L**4*falsebound/4)
dA=EA/Z-A1;dB=EB/Z
root=json.loads((OLD/'results/interval_L8.json').read_text());center=root['center_decimal_rationals']
dx=iv.mpf(center[0])+iv.mpf(['-1e-12','1e-12']);ox=iv.mpf(center[1])+iv.mpf(['-1e-12','1e-12'])
G=[[dx if i==j else ox for j in range(4)]for i in range(4)]
M=[[dA/4 if i==j else dB/12 for j in range(4)]for i in range(4)]
link=iv.mpf(0)
for r in range(4):
 v=[sum((M[i][r]-M[i][i]/2)*G[i][a]for i in range(4))for a in range(4)]
 for a in range(4):
  for b in range(4):link+=abs((v[r]if a==b else 0)-(v[a]if b==r else 0))
source=L*L*(abs(dA)+abs(dB)+link)
ck('direct_raw_scaled_source_below_1e_minus10',source<iv.mpf('1e-10'))
gap1=iv.mpf(0);gap2=iv.mpf(0)
for (A,B),mul in rows:
 if A in ((0,0),(128,-64)):continue
 gap=(val(A,iv)-A1)*dx+val(B,iv)*ox
 w=mul*accept(A);gap1+=w*gap;gap2+=w*gap*gap
variance=gap2/Z-(gap1/Z)**2
ck('full_matter_residual_nonzero',variance>0)
mr=2*iv.sqrt(variance)
ck('actual_full_Hilbert_residual_below_1e_minus6',mr<iv.mpf('1e-6'))
Bbits=4+4*3+2*T
rsetup=int(mp.ceil(mp.log(2*Bbits)/(-mp.log(1-2*gp))))
setupfail=Bbits*(1-2*g)**rsetup
ck('setup_heralding_counted',setupfail<iv.mpf('0.5'))
setup_success=1-setupfail
# Bounded independent runs; the archived rejected runs are not cleared.
delta=iv.mpf('1e-6')
runs=int(mp.ceil(mp.mpf(L**4)/2*mp.log(1/mp.mpf('1e-6'))))
ck('finite_total_success_bound',iv.exp(-iv.mpf(2)*runs/L**4)<delta)
result={'status':'PASS','L':L,'spatial_modes':N,'Fock_dimension':16,
 'total_comparisons_T':T,'accepted_error_count':[lo,hi],'epsilon_target':'8^-10',
 'effect_first_eigenvalue_interval':str(e1),
 'first_shell_prior':'8/4096','filter_success_probability_interval':str(prob),
 'conditional_trace_distance_interval':str(distance),'universal_trace_error_bound_interval':str(L**4*falsebound/4),
 'hminus2_raw_metric_and_link_source_interval':str(source),
 'matter_full_Hilbert_residual_interval':str(mr),
 'fair_bits_required':Bbits,'trials_per_fair_bit':rsetup,
 'setup_success_lower_interval':str(setup_success),
 'independent_trials_sufficient_for_failure_1e_minus6':runs,
 'all_histories_retained':True,'conditional_not_deterministic_projector':True,
 'no_eigenvalue_catalogue_in_program':True,
 'first_rate_used_is_derived_from_reference_L':True,
 'exact_finite_full_root':False,'physical_admission':False,'native_AF_refinement':False,
 'checks':checks,'interval_checks':len(checks),
 'v1_root_box_is_imported_input_not_new_root':True}
(R/'results/frequency_filter_L8_interval.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS_FREQUENCY_FILTER',T,'comparisons; accept',lo,'..',hi)
print('probability',prob)
print('trace error',distance)
print('hminus2 raw source',source)
print('full matter norm',mr)
print('fair setup',Bbits,rsetup,'bounded whole trials',runs)
