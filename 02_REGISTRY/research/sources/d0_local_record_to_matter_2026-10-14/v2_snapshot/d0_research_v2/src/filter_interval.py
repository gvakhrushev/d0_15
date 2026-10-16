"""All-mode outward-interval certificate for the actual retained-history filter.
L=8: features Q(sqrt(2)), no root or eigenstate selected by numerical tolerance.
The input field-root rectangle is the explicitly named v1 conditional result.
"""
from __future__ import annotations
import importlib.util,json,math
from pathlib import Path
import mpmath as mp
R=Path(__file__).resolve().parents[1]
OLD=R/'input_v1/d0_local_matter_bridge'
spec=importlib.util.spec_from_file_location('v1_features',OLD/'src/interval_l8.py')
f=importlib.util.module_from_spec(spec);spec.loader.exec_module(f)
mp.mp.dps=65;mp.iv.dps=55;iv=mp.iv
checks=[]
def ck(n,b):
 if not bool(b):raise AssertionError(n)
 checks.append(n)
def val(q,ctx):return ctx.mpf(q[0])+ctx.mpf(q[1])*ctx.sqrt(2)
def istr(x):return str(x)
L=8;N=L**4;rows=f.features();gamma=((mp.sqrt(5)-1)/2)**3
g=((iv.sqrt(5)-1)/2)**3
A1=iv.mpf(128)-64*iv.sqrt(2)
e1=g*A1/(4*L*L);eps=iv.mpf(1)/L**10
C=iv.mpf(L**4)/(4*iv.sin(iv.pi/L)**2)
e1p=gamma*mp.sin(mp.pi/L)**2;Cp=L**4/(4*mp.sin(mp.pi/L)**2)
n=int(mp.ceil(mp.log(Cp*(L**10))/mp.log((1-e1p)/(1-2*e1p))))
# n is a proposed integer; the following interval verifies it independently.
bound=C*((1-2*e1)/(1-e1))**n
ck('chosen_depth_meets_exact_bound',bound<eps)
ck('all_error_probabilities_below_one',4*g<1)
Z=iv.mpf(0);first=iv.mpf(0);EA=iv.mpf(0);EB=iv.mpf(0);tail=iv.mpf(0)
zero_count=shell_count=0
for (A,B),mul in rows:
 if A==(0,0):
  ck('only_true_zero_A_has_zero_B',B==(0,0));zero_count+=mul;continue
 av,bv=val(A,iv),val(B,iv);e=g*av/(4*L*L)
 ck('positive_nontrivial_reference_defect_'+str(A),e>0)
 ck('probability_strict_'+str(A),e<1)
 w=mul*e*(1-e)**n
 Z+=w;EA+=w*av;EB+=w*bv
 if A==(128,-64):
  ck('lowest_layer_has_zero_cross_feature',B==(0,0));first+=w;shell_count+=mul
 else:tail+=w
ck('zero_multiplicity_all_Fock_retained',zero_count==1)
ck('first_momentum_multiplicity',shell_count==8)
prob=Z/N;distance=tail/Z
ck('full_history_acceptance_positive',prob>0)
ck('certified_trace_distance_target',distance<eps)
ck('finite_filter_is_not_exact_shell',distance>0)
dA=EA/Z-A1;dB=EB/Z
ck('metric_raw_bound',abs(dA)+abs(dB)<128*L*L*eps)
# Uniform perturbation of all metric and linear-link source rows on the old root box.
root=json.loads((OLD/'results/interval_L8.json').read_text())
center=root['center_decimal_rationals'];dx=iv.mpf(center[0])+iv.mpf(['-1e-12','1e-12']);ox=iv.mpf(center[1])+iv.mpf(['-1e-12','1e-12'])
G=[[dx if i==j else ox for j in range(4)]for i in range(4)]
M=[[dA/4 if i==j else dB/12 for j in range(4)]for i in range(4)]
gmax=iv.mpf('.09')
ck('old_root_box_has_uniform_norm_bound',dx+3*ox<gmax)
link_raw=iv.mpf(0)
for r in range(4):
 v=[sum((M[i][r]-M[i][i]/2)*G[i][a]for i in range(4))for a in range(4)]
 for a in range(4):
  for b in range(4):
   # This is N times the local row, so summing nodes exactly cancels 1/N.
   coef=(v[r]if a==b else 0)-(v[a]if b==r else 0)
   link_raw+=abs(coef)
ck('all64_link_raw_bound',link_raw<576*gmax*L*L*eps)
# Keep full norm matter residual with all retained flags; no claim about an enormous
# archive-coordinate l1 norm, and no exact finite full Euler root.
matter_norm_bound=32*gmax*L*L*iv.sqrt(eps)
source_normalized_bound=(128+576*gmax)*L**4*eps
actual_source_scaled=L**2*(abs(dA)+abs(dB)+link_raw)
ck('direct_raw_scaled_residual_below_3e_minus9',actual_source_scaled<iv.mpf('3e-9'))
gap1=iv.mpf(0);gap2=iv.mpf(0)
for (aa,bb),mul in rows:
 if aa in ((0,0),(128,-64)):continue
 av,bv=val(aa,iv),val(bb,iv)
 ee=g*av/(4*L*L);ww=mul*ee*(1-ee)**n
 gap=(av-A1)*dx+bv*ox
 gap1+=ww*gap;gap2+=ww*gap**2
variance=gap2/Z-(gap1/Z)**2
ck('finite_material_residual_strictly_nonzero',variance>0)
actual_matter_norm=2*iv.sqrt(variance)
ck('direct_Hilbert_residual_below_6e_minus6',actual_matter_norm<iv.mpf('6e-6'))
success_floor=512*g*(1-e1)*eps/(L**12)
ck('acceptance_polynomial_lower',prob>success_floor)
q=float(e1p);Bbits=(4+4*3)+2*(n+1);click=2*gamma
extract_tries=int(mp.ceil(mp.log(2*Bbits)/(-mp.log(1-click))))
ck('bounded_fair_extraction_total_failure',Bbits*(1-2*g)**extract_tries<iv.mpf('0.5'))
out={'status':'PASS','L':L,'physical_Fock_dimension':16,'spatial_modes':N,
 'exact_feature_pairs':len(rows),'depth_quiet':n,'total_comparisons':n+1,
 'epsilon_target':'8^-10','trace_distance_interval':istr(distance),
 'full_history_acceptance_probability_interval':istr(prob),
 'expected_trial_lower_diagnostic':str(1/prob),
 'acceptance_polynomial_lower_interval':istr(success_floor),
 'moment_delta_A_interval':istr(dA),'moment_delta_B_interval':istr(dB),
 'raw_metric_source_difference_interval':istr(abs(dA)+abs(dB)),
 'raw_linear_link_source_difference_interval':istr(link_raw),
 'hminus2_raw_source_bound_interval':istr(source_normalized_bound),
 'matter_Hilbert_residual_bound_interval':istr(matter_norm_bound),
 'actual_hminus2_raw_source_interval':istr(actual_source_scaled),
 'actual_matter_Hilbert_residual_interval':istr(actual_matter_norm),
 'all_archive_coordinates_l1_residual_proved':False,
 'initial_uniform_extraction_fair_bits':Bbits,'tries_per_fair_bit':extract_tries,
 'fair_extraction_success_lower':'1/2','all_failures_and_choices_retained':True,
 'conditional_preparation':True,'unconditional_filter_selects_shell':False,
 'exact_finite_full_stationarity':False,'checks':checks,
 'actual_pi0_cycle_placement_derived':False,'physical_admission_derived':False,
 'old_root_input':'v1 results/interval_L8.json rectangle, not new root certification'}
(R/'results/filter_L8_interval.json').write_text(json.dumps(out,indent=2,ensure_ascii=False)+'\n')
print('PASS_FILTER_INTERVAL_L8',n,'quiet steps;',len(checks),'interval conditions')
print('trace distance',distance)
print('success probability',prob)
print('raw metric difference',abs(dA)+abs(dB))
print('raw link difference',link_raw)
