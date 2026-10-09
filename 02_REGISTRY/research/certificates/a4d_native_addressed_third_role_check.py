#!/usr/bin/env python3
"""Complete addressed real memory family: uniform actuation without a blank helper."""
import argparse,hashlib,json,re
from collections import Counter,deque
from itertools import product,permutations
from pathlib import Path
BASE='02_REGISTRY/research/certificates/a4d_native_addressed_third_role'
PROOF='02_REGISTRY/research/A4D_NATIVE_ADDRESSED_THIRD_ROLE.md'
SCOPE={
 'input_head':'074192ae3c76eb6deb426d395f779e43678044a6',
 'class':'ENTIRE_TWO_ADDRESS_MINIMAL_REAL_RETAINING_RECORDING_COMPARISON_FAMILY_ON_THREE_COHERENT_DYAD_ROLES',
 'four_independent_signed_primitives_all_65536_realizations_classified':True,
 'complete_programmes_use_at_most_29_forward_primitives':True,
 'same_hardware_256_pairs_require_only_13_or_21_forward_primitives':True,
 'the_512_proper_three_primitive_cases_have_the_same_five_step_generator_route':True,
 'full_operator_identity_retains_arbitrary_correlated_active_and_helper_states':True,
 'no_blank_helper_reset_or_discarded_history_is_required_by_the_operator_identity':True,
 'physical_permission_to_copy_and_address_the_operations_is_an_application_input':True,
 'all_literal_retained_golden_depths_intertwine_the_full_programme':True,
 'full_programme_error_is_not_diluted_by_normalized_golden_refinement':True,
 'conditional_constant_expansion_keeps_the_prior_owned_phi_resource_bound':True,
 'old_minimal_Q8_all_word_and_limit_obstruction_is_preserved_in_its_scope':True,
 'the_m8_active_angle_is_bound_to_the_actual_owned_m4_gate_and_p0':True,
 'an_extra_orthogonal_angle_or_old_memory_gate_is_added_as_a_primitive':False,
 'an_unsigned_phase_completion_is_selected_from_M1':False,
 'the_28_axis_exploration_is_the_terminal_generic_proof':False,
 'all_65536_realizations_have_the_same_five_step_route':False,
 'one_positive_helper_recording_without_helper_comparison_closes_all_cases':False,
 'whole_apparatus_gauge_makes_the_memory_orientation_unobservable':False,
 'the_tested_gate_is_used_to_prepare_its_independent_calibration_reference':False,
 'functional_retention_truth_alone_derives_coherent_representation_and_physical_addressability':False,
 'a_passive_condensed_limit_theorem_supplies_the_actively_addressed_operations':False,
 'a_new_physical_qubit_or_coherent_role_is_forced_by_this_matrix_construction':False,
 'native_preparation_decoder_address_resources_and_internal_full_word_schedule_are_derived':False,
 'primitive_word_length_is_native_endpoint_MDL_or_full_runtime_cost':False,
 'the_phi_resource_bound_is_full_physical_budget_admission':False,
 'the_larger_processor_disproves_the_scoped_minimal_Q8_obstruction':False,
 'the_old_operator_obstruction_excludes_every_scene_or_state_preparation':False,
 'the_complete_addressed_real_class_exhausts_all_native_complex_or_larger_apparatus':False,
 'joint_native_heat_tangent_refinement_and_core_completeness_are_derived':False,
 'the_653_complementary_histories_or_either_thermal_memory_source_defect_are_dropped':False,
 'own_metric_matter_source_and_physical_Ward_are_derived':False,
 'quantitative_metric_contrast_and_native_stationarity_are_transferred':False,
 'curved_joint_roots_soundness_recovery_and_constraints_are_derived':False,
 'prior_propositions_are_counted_as_new':False,
 'new_action_selector_temperature_coupling_source_or_physical_postulate_added':False,
 'positive_GR':False,'G0b_closed':False,'G0_closed':False,'global_closure':False,
 'original_310_202_317_terminals_changed':False,
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path);args=ap.parse_args()
 root=Path(__file__).resolve().parents[3];sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 expected=json.loads(args.expect.read_text()) if args.expect else None
 if expected is not None:assert expected['scope']==SCOPE,'PINNED_SCOPE_MISMATCH'
 checks=[];check_count=0
 def check(n,v,retain=True):
  nonlocal check_count
  assert bool(v),n;check_count+=1
  if retain:checks.append(n)
 rr=json.loads((root/(BASE+'_results.json')).read_text());lean=(root/(BASE+'.lean')).read_text();out=(root/(BASE+'_output.txt')).read_text()
 names=re.findall(r'^#check (\S+)',lean,re.M)
 check('ACTUAL_KERNEL_EXIT_ZERO',rr['status']=='PASS' and rr['compiler_exit_code']==0)
 check('ALL_NEW_ACTUAL_DECLARATIONS_AND_AXIOMS_PRINTED',names==rr['declarations'] and len(names)==rr['printed_propositions']==rr['printed_axiom_dependencies']==95)
 check('CAPSULE_AND_TRANSCRIPT_FRESH',sha(BASE+'.lean')==rr['capsule_sha256'] and sha(BASE+'_output.txt')==rr['output_sha256'])
 check('NO_PLACEHOLDER_OR_COMPILER_TRUST_LEAF',not re.search(r'\b(sorry|admit|axiom|native_decide)\b',lean) and 'sorryAx' not in out and 'Lean.trustCompiler' not in out and not re.search(r'\berror(?:\(|:)',out))
 axioms=set()
 for m in re.finditer(r'depends on axioms: \[([^]]*)\]',out,re.S):axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
 check('ONLY_STANDARD_TRANSITIVE_AXIOMS',sorted(axioms)==rr['axioms']==['Classical.choice','Quot.sound','propext'])
 for n in names:check('ACTUAL_DECLARATION_'+n,n in out and ("'"+n+"' depends on axioms:" in out or "'"+n+"' does not depend on any axioms" in out))
 check('ACTUAL_QUANTIFIED_FULL_STATE_AND_ALL_DEPTH_TERMINALS',all(v in out for v in ['AddressedPrimitive','word8','Triple','realHistoryInclusion','RetainingRealRecording','RetainingRealComparison','primitiveRoot','code.length ≤ 29','code.length ≤ 21','∀ (x : D0.Research.AddressedThirdRole.Triple → ℝ)']))
 pins={**rr['transitive_d0_source_sha256'],**rr['toolchain_input_sha256'],**rr['prior_packet_input_sha256']}
 for p,d in pins.items():check('SOURCE_PIN_'+p,sha(p)==d)
 check('ACTUAL_COERENT_MEMORY_CLOCK_P0_AND_Q8_OWNERS_PINNED',all('03_FORMALIZATION/D0/'+v in rr['transitive_d0_source_sha256'] for v in ['Representation/GoldenCoherentMemory.lean','Representation/OrderMemoryReadout.lean','Representation/FiniteProtocolClock.lean']))
 bits=list(product([0,1],repeat=3));idx={b:i for i,b in enumerate(bits)}
 signs=list(product([1,-1],repeat=4));I=(tuple(range(8)),(1,)*8)
 def mul(P,Q):return (tuple(P[0][Q[0][j]] for j in range(8)),tuple(P[1][Q[0][j]]*Q[1][j] for j in range(8)))
 def tr(P):
  p=[0]*8;v=[0]*8
  for j in range(8):p[P[0][j]]=j;v[P[0][j]]=P[1][j]
  return tuple(p),tuple(v)
 def power(P,n):
  V=I
  for _ in range(n):V=mul(V,P)
  return V
 def value(w):
  V=I
  for A in w:V=mul(V,A)
  return V
 def lift(skel,sg,address):
  p=[];v=[]
  for b in bits:
   j=2*b[0]+b[address];k=skel[j];o=list(b);o[0]=k//2;o[address]=k%2
   p.append(idx[tuple(o)]);v.append(sg[j])
  return tuple(p),tuple(v)
 def axis(role):
  p=[];v=[]
  for b in bits:
   o=list(b);o[role]=1-b[role];p.append(idx[tuple(o)]);v.append(1 if b[role]==0 else -1)
  return tuple(p),tuple(v)
 def scale(P,sg):return P[0],tuple(sg*v for v in P[1])
 J0=axis(0);J1=axis(1)
 F=(0,1,3,2);U=(0,3,2,1)
 # Re-derive the basis skeletons from represented retention/truth; no blank helper claim.
 b2=list(product([0,1],repeat=2));i2={b:i for i,b in enumerate(b2)}
 fw=[];rv=[]
 for p in permutations(range(4)):
  if all(b2[p[j]][0]==b2[j][0] for j in range(4)) and all(b2[p[i2[b,0]]][1]==b for b in [0,1]):fw.append(p)
  if all(b2[p[j]][1]==b2[j][1] for j in range(4)) and all(b2[p[i2[0,b]]][0]==b for b in [0,1]):rv.append(p)
 check('COMPLETE_REPRESENTED_RETENTION_TRUTH_SKELETONS',fw==[F] and rv==[U])
 prim={}
 for skel,name in [(F,'F'),(U,'U')]:
  for address in [1,2]:
   for v in signs:
    A=lift(skel,v,address);prim[name,address,v]=A
    check('ALL_PHASES_FULL_ORTHOGONAL_THREE_FORWARD_INVERSE_'+str((name,address,v)),mul(tr(A),A)==I and power(A,4)==I and power(A,3)==tr(A))
 route_counts=Counter();orientation_counts=Counter();same_counts=Counter();sweep=hashlib.sha256();proper_counts=Counter()
 for c,d,e,f in product(signs,repeat=4):
  pc,pd,pe,pf=[__import__('math').prod(v) for v in [c,d,e,f]]
  B=prim['U',1,c];C=prim['F',1,d];A=prim['F',2,e];D=prim['U',2,f]
  if pd==1:w=[B,C,B];sg=d[0]*d[2]*c[2]*c[3];route='POSITIVE_FORWARD_13'
  elif pc==1:w=[C,B,C];sg=c[0]*c[3]*d[1]*d[2];route='POSITIVE_REVERSE_13'
  elif pe==-1:
   w=[B,A,C,B,A];sg=e[0]*e[2]*c[0]*c[2]*d[0]*d[2]*e[0]*e[3]*c[0]*c[3];route='PROPER_HELPER_21'
  elif pf==1:
   w=[B,A,B,D,C,A];sg=e[0]*e[2]*d[0]*d[2]*f[0]*f[3]*c[0]*c[1]*e[0]*e[3]*c[0]*c[3];route='POSITIVE_HELPER_PAIR_25'
  else:
   w=[B,A,D,B,A,D,C];sg=d[0]*d[2]*f[0]*f[2]*e[0]*e[2]*c[0]*c[3]*f[0]*f[1]*e[0]*e[3]*c[0]*c[3];route='MIXED_HELPER_PAIR_29'
  inverse=[K for P in reversed(w) for K in [P,P,P]]
  left=value(w);right=value(inverse);code_length=len(w)+1+len(inverse)
  # Both coefficients in a I+p J0 are checked on the FULL eight-dimensional workspace.
  check('COMPLETE_HARDWARE_FULL_OPERATOR_AND_FORWARD_CODE_'+str((c,d,e,f)),sg in [1,-1] and right==tr(left) and mul(left,right)==I and mul(mul(left,J0),right)==scale(J1,sg) and code_length in [13,21,25,29] and code_length<=29 and all(K in [A,B,C,D] for K in w+inverse),False)
  route_counts[route]+=1;orientation_counts[sg]+=1
  sweep.update(json.dumps([c,d,e,f,route,sg,code_length],separators=(',',':')).encode()+b'\n')
  if d==e and c==f:same_counts[code_length]+=1
  if pc==pd==pe==-1:proper_counts[sg]+=1
 check('ALL_65536_REALIZATIONS_CONSTRUCTIVE',sum(route_counts.values())==65536 and dict(route_counts)=={'POSITIVE_FORWARD_13':32768,'POSITIVE_REVERSE_13':16384,'PROPER_HELPER_21':8192,'POSITIVE_HELPER_PAIR_25':4096,'MIXED_HELPER_PAIR_29':4096})
 check('SAME_HARDWARE_FULL_256_PAIRS_NEED_ONLY_13_OR_21',dict(same_counts)=={13:192,21:64})
 check('PROPER_HELPER_ALL_512_INDEPENDENT_TRIPLES_PLUS_16_UNUSED_COMPARATORS',sum(proper_counts.values())==8192 and proper_counts[1]==proper_counts[-1]==4096)
 check('BOTH_ORIENTATIONS_RETAINED',orientation_counts[1]==orientation_counts[-1]==32768)
 # Hostile controls reject loss of the restoring word, absent addressing and phase selection.
 cv=(1,1,1,-1);pv=(1,1,1,1)
 B=prim['U',1,cv];C=prim['F',1,cv];A=prim['F',2,cv]
 w=[B,A,C,B,A];S=value(w)
 check('PROPER_COMPLETE_ROUTE_TRANSFERS_OLD_TURN',mul(mul(S,J0),tr(S))[0]==J1[0])
 check('DROPPING_INVERSE_DOES_NOT_RESTORE_FULL_WORKSPACE',S!=I and mul(S,J0)!=scale(J1,1) and mul(S,J0)!=scale(J1,-1))
 wrong=value([B,C,C,B,C])
 check('REPLACING_HELPER_ADDRESS_BY_OLD_ADDRESS_FAILS',mul(mul(wrong,J0),tr(wrong)) not in [J1,scale(J1,-1)])
 bad=value([B,prim['F',2,pv],C,B,prim['F',2,pv]])
 check('FIVE_ROUTE_DOES_NOT_FIT_POSITIVE_HELPER_WITH_PROPER_TARGET',mul(mul(bad,J0),tr(bad)) not in [J1,scale(J1,-1)])
 # Retain the original four-coordinate terminal as a parent input, never overwrite it.
 parent=json.loads((root/'02_REGISTRY/research/certificates/a4d_native_uniform_memory_actuation_certificate.json').read_text())
 check('OLD_256_PAIR_Q8_TERMINAL_REMAINS_SCOPED_AND_PINNED',parent['exact']['full_joint_count']==256 and parent['exact']['proper_all_word_obstructed_pair_count']==64 and parent['scope']['remaining_64_pairs_have_a_kernel_all_word_and_no_vanishing_error_obstruction'] is True)
 check('FULL_DEPTH_TERMINAL_IS_A_KERNEL_PROPOSITION_NOT_A_FINITE_DEPTH_CENSUS','full_constructive_actuation_commutes_with_every_retained_golden_depth' in out and '∀ (n : ℕ)' in out)
 exact={'two_address_realization_count':65536,'route_counts':dict(sorted(route_counts.items())),'full_forward_only_code_lengths':[13,21,25,29],'max_full_forward_only_code_length':29,'same_hardware_realization_count':256,'same_hardware_code_length_counts':dict(sorted(same_counts.items())),'proper_three_primitive_realization_count':512,'proper_three_primitive_code_length':21,'full_eight_coordinate_workspace_checked':True,'full_operator_identity_coefficients':['I','J0'],'target_generator':'I tensor J tensor I','both_orientation_counts':dict(sorted(orientation_counts.items())),'complete_hardware_sweep_sha256':sweep.hexdigest(),'helper_blank_assumption':False,'all_depth_normalized_error_mass':'unchanged, actual quantified Lean proposition','parent_minimal_Q8_proper_pair_count':64,'phi_cost_expansion_factor':29}
 result={'status':'PASS_COMPLETE_ADDRESSED_REAL_FAMILY_NATIVE_APPLICATION_PENDING','input_head':SCOPE['input_head'],'scope':SCOPE,'proof_sha256':sha(PROOF),'kernel_receipt_sha256':sha(BASE+'_results.json'),'checker_sha256':sha(BASE+'_check.py'),'source_sha256':pins,'check_count':check_count,'checks':checks,'batched_exact_controls':{'COMPLETE_HARDWARE_FULL_OPERATOR_AND_FORWARD_CODE':65536},'exact':exact}
 if expected is not None:assert expected==result,'EXACT_CERTIFICATE_MISMATCH'
 if args.output:args.output.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print(result['status'],check_count,'ALL_65536_HARDWARE_REALIZATIONS',flush=True)
if __name__=='__main__':main()
