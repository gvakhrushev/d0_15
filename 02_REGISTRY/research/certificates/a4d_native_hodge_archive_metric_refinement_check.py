#!/usr/bin/env python3
"""Actual archive fibres versus full Hodge point metric; no physical law installed."""
import argparse,copy,hashlib,itertools,json,math
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_hodge_archive_metric_refinement'
PROOF='02_REGISTRY/research/A4D_NATIVE_HODGE_ARCHIVE_METRIC_REFINEMENT.md'
INPUT='025bf30c3d7c2cfba1a1d57676d65e536453b66b'
SCOPE={
 'class':'ALL_LEVELWISE_BIJECTIONS_FROM_ACTUAL_ARCHIVE_POINTS_TO_FIXED_FULL_HODGE_SCALAR_SITES',
 'actual_successive_flat_index_modulo_projections_used':True,
 'direct_modulo_or_coordinatewise_projection_substituted':False,
 'all_level_growing_zero_fiber_kernel_formalized':True,
 'all_size_metric_packing_and_rate_status':'ANALYTIC_NOT_FULL_LEAN_FORMALIZATION',
 'all_bijective_numberings_covered_by_cardinality_proof':True,
 'uniform_O_h_full_metric_distortion_on_actual_doubling_arrows_impossible':True,
 'lower_bound_h_three_quarters_is_an_optimal_upper_bound':False,
 'slower_o_one_metric_refinement_excluded':False,
 'nonbijective_physical_readouts_or_prepared_algebras_exhausted':False,
 'native_physical_observable_algebra_admission_derived':False,
 'archive_phi_index_identified_with_physical_mesh':False,
 'O_h_action_contrast_or_raw_Euler_obstruction_inferred_from_metric_rate':False,
 'complete_archive_deleted_or_new_selector_action_source_installed':False,
 'absence_of_Gamma_F_for_whole_core_proved':False,
 'own_source_Ward_curved_roots_GR_or_original_parent_terminals_closed':False,
}

def sha(p):return hashlib.sha256((ROOT/p).read_bytes()).hexdigest()
def forget(L,K,a):
 assert 2<=L<=K and 0<=a<K**4
 for j in range(K-1,L-1,-1):a%=j**4
 return a

def controls():
 checks={}
 def ck(n,c,count=1):
  assert bool(c),n;checks[n]=checks.get(n,0)+count
 rec=json.loads((ROOT/(BASE+'_results.json')).read_text())
 out=(ROOT/(BASE+'_output.txt')).read_text()
 ck('compiled_actual_all_level_capsule',rec['status']=='PASS' and rec['compiler_exit_code']==0 and rec['input_head']==INPUT)
 ck('eleven_actual_resolved_propositions',len(rec['declarations'])==11 and len(rec['primary_owner_propositions'])==3)
 ck('no_sorry_or_compiler_errors',': error' not in out and ': warning' not in out and 'sorryAx' not in out)
 for n in rec['declarations']+rec['primary_owner_propositions']:
  ck('literal_proposition_resolution',n in out and n in rec['axioms'])
  ck('transitive_standard_axioms',set(rec['axioms'][n])<={'propext','Classical.choice','Quot.sound'})
 ck('all_level_fibre_proposition_contains_actual_typed_composite','longProjection' in rec['printed_propositions'][rec['declarations'][-1]])
 for group in ['transitive_d0_source_sha256','primary_and_prior_input_sha256','toolchain_input_sha256']:
  for p,h in rec[group].items():ck('sha_'+group,sha(p)==h)
 ck('capsule_sha',sha(BASE+'.lean')==rec['capsule_sha256'])
 ck('output_sha',sha(BASE+'_output.txt')==rec['output_sha256'])
 ck('exact_formalization_scope',rec['actual_all_level_growing_collapsed_fiber_kernel_formalized'] and not rec['all_size_Connes_distance_packing_and_rate_kernel_formalized'])
 ck('native_admission_scope',not rec['physical_observable_algebra_or_Gamma_F_GR_derived'])
 prior=json.loads((ROOT/'02_REGISTRY/research/certificates/a4d_native_hodge_connes_metric_certificate.json').read_text())
 ck('prior_actual_metric_analytic_and_native_scope',prior['scope']['all_size_exact_product_circle_Connes_distance']=='ANALYTIC_PROOF_NOT_FULL_LEAN_FORMALIZATION' and not prior['scope']['native_archive_RG_is_physical_metric_refinement'])
 ck('wrong_long_direct_modulo_rejected',forget(2,4,81)==0 and 81%16==1)
 for L in range(2,7):
  K=2*L
  counts=[0]*(L**4)
  for a in range(K**4):
   b=forget(L,K,a);ck('actual_full_long_projection_range',0<=b<L**4)
   counts[b]+=1
  ck('all_actual_long_fibers_nonempty',min(counts)>0)
  ck('literal_zero_fiber_bound',counts[0]>=K-L+1)
  ck('fiber_partition_conserves_all_points',sum(counts)==K**4)
 for L in list(range(2,73))+[628]:
  K=2*L;labels=[0]+[t**4 for t in range(L,K)]
  ck('positive_distinct_birth_labels',len(set(labels))==L+1 and all(0<=a<K**4 for a in labels))
  for a in labels:ck('actual_birth_witness_maps_zero',forget(L,K,a)==0)
 ck('macro_fiber_not_regular_16_replication',len([0]+[t**4 for t in range(16,32)])>16)
 # Coordinate packing, including all wraps and all possible centres.
 for K in range(2,25):
  for m in range(K+1):
   for c in range(K):
    vals=[j for j in range(K) if min((j-c)%K,(c-j)%K)<=m]
    ck('exact_cyclic_coordinate_ball_count',len(vals)==min(K,2*m+1))
    ck('four_role_product_packing',len(vals)**4<=(2*m+1)**4)
 for K in range(2,11):
  for m in range(K+1):
   count=sum(sum(min(j,K-j)**2 for j in x)<=m*m for x in itertools.product(range(K),repeat=4))
   ck('actual_euclidean_ball_inside_coordinate_box',count<=min(K,2*m+1)**4)
 # Exact rate contradiction, with no floating root or numerically fitted constant.
 for C in [Fraction(0),Fraction(1,8),Fraction(1,4),Fraction(1,2),Fraction(3,4),Fraction(1),Fraction(2),Fraction(5)]:
  cap=(4*C+1)**4;L=4*(cap.numerator//(4*cap.denominator)+1)
  if L+1<=cap:L+=4
  ck('every_tested_fixed_rate_constant_has_valid_declared_mesh',L>=4 and L%4==0 and L+1>cap)
  K=2*L;radius=Fraction(C,L)
  ck('rate_packing_capacity_exact', (2*K*radius+1)**4==cap)
  ck('native_birth_count_exceeds_O_h_packing_capacity',K-L+1>cap)
 ck('unit_constant_hostile_control_at_628',628+1>5**4 and 628%4==0)
 # A relabeling can change distances but cannot change the native fibre size.
 L=2;K=4;M=K**4;fiber=[a for a in range(M) if forget(L,K,a)==0]
 for mult in [1,3,5,7,11,13,17,31]:
  for off in [0,1,37]:
   image={(mult*a+off)%M for a in fiber}
   ck('finite_bijection_control_preserves_fiber_cardinality',math.gcd(mult,M)==1 and len(image)==len(fiber))
 # Noninjective reading is a different algebra, not an escape for the full metric.
 ck('nonbijective_control_is_outside_complete_tested_class',len({0 for a in fiber})<len(fiber))
 return checks

def expected(checks):return {'status':'PASS','input_head':INPUT,'scope':SCOPE,'checks':checks,'controls':sum(checks.values()),'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),'capsule_sha256':sha(BASE+'.lean'),'lean_receipt_sha256':sha(BASE+'_results.json')}
def validate(candidate,checks):
 assert candidate==expected(checks),'certificate scope, counts, proof or source hash mismatch'

def main():
 p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
 checks=controls();e=expected(checks)
 if args.write:(ROOT/(BASE+'_certificate.json')).write_text(json.dumps(e,sort_keys=True,indent=2)+'\n')
 validate(json.loads((ROOT/(BASE+'_certificate.json')).read_text()),checks)
 mutants=[]
 for key,v in SCOPE.items():
  if isinstance(v,bool):
   bad=copy.deepcopy(e);bad['scope'][key]=not v;mutants.append(bad)
 for key in ['proof_sha256','checker_sha256','lean_receipt_sha256']:
  bad=copy.deepcopy(e);bad[key]='0'*64;mutants.append(bad)
 for bad in mutants:
  try:validate(bad,checks)
  except AssertionError:pass
  else:raise AssertionError('false ledger accepted')
 print('PASS_NATIVE_HODGE_ARCHIVE_METRIC_REFINEMENT',sum(checks.values()),'CONTROLS',len(mutants),'FALSE_LEDGERS_REJECTED')
if __name__=='__main__':main()
