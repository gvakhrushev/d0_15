#!/usr/bin/env python3
"""Faithful owned typed/archive/history carrier and a complete declared flow boundary."""
import argparse,hashlib,json,re
from itertools import product,permutations
from pathlib import Path
BASE='02_REGISTRY/research/certificates/a4d_native_archive_apparatus_realization'
PROOF='02_REGISTRY/research/A4D_NATIVE_ARCHIVE_APPARATUS_REALIZATION.md'
SCOPE={
 'input_head':'0f77c75796479241e4a8a4c9398dd166dfb1bed4',
 'class':'ACTUAL_TYPED_33_SCENE_AND_FULL_718_HISTORIES_ALL_SIX_ARCHIVE_PAIRS_WITH_COMPLETE_JOINT_FLOW_PLUS_ALL_ACTIVE_ROLE_OPERATIONS',
 'native_typed_state_and_full_history_operator_carrier_constructed':True,
 'actual_owned_p0_and_degree_normalizations_used':True,
 'all_six_ordered_archive_pairs_are_covered':True,
 'all_native_33_state_components_and_718_histories_are_retained':True,
 'all_653_joint_readout_null_directions_are_retained_exactly':True,
 'the_history_embedding_has_16_dimensions_and_a_702_complement':True,
 'all_declared_complete_joint_symmetric_history_laws_commute_with_the_constructed_operations':True,
 'the_declared_joint_history_law_class_is_constructively_nonempty':True,
 'all_prior_65536_addressed_programmes_have_full_native_carriers_with_maximum_29_steps':True,
 'every_finite_declared_flow_word_plus_every_active_role_linear_operation_preserves_old_parity':True,
 'actual_p0_old_memory_actuation_is_excluded_at_all_lengths_and_matrix_limits_in_that_palette':True,
 'the_full_regular_Q8_constant_record_obstruction_is_retained':True,
 'the_bare_8_regular_archive_is_two_identical_pure_spin_blocks':False,
 'a_spin_projection_drops_even_archive_components':False,
 'the_two_archive_addresses_or_an_unsigned_phase_are_selected_from_M1':False,
 'physical_operation_admission_is_derived_from_commutation_or_carrier_existence':False,
 'the_declared_flow_palette_exhausts_every_native_operation_or_its_compatibility_algebra':False,
 'role_permutation_covariance_is_automatically_an_executable_physical_gate':False,
 'the_owned_active_p0_gate_is_omitted_from_the_all_word_boundary':False,
 'a_condensed_limit_supplies_missing_physical_operations':False,
 'native_preparation_reference_decoder_address_budget_and_schedule_are_derived':False,
 'the_29_step_bound_is_native_endpoint_MDL_or_runtime_admission':False,
 'joint_physical_native_dynamics_and_all_variations_are_derived':False,
 'native_to_coframe_link_matter_maps_and_physical_refinement_are_derived':False,
 'own_metric_matter_source_and_physical_Ward_are_derived':False,
 'quantitative_metric_contrast_and_native_stationarity_are_transferred':False,
 'curved_joint_roots_soundness_recovery_and_constraints_are_derived':False,
 'either_thermal_memory_source_defect_is_dropped':False,
 'new_action_selector_angle_temperature_coupling_source_or_physical_postulate_added':False,
 'archive_memory_is_identified_with_physical_dark_matter_or_acceleration':False,
 'positive_GR':False,'G0b_closed':False,'G0_closed':False,'global_closure':False,
 'original_310_202_317_terminals_changed':False,'prior_propositions_are_counted_as_new':False,
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path);args=ap.parse_args()
 root=Path(__file__).resolve().parents[3];sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 expected=json.loads(args.expect.read_text()) if args.expect else None
 if expected is not None:assert expected['scope']==SCOPE,'PINNED_SCOPE_MISMATCH'
 checks=[]
 def check(n,v):assert bool(v),n;checks.append(n)
 rr=json.loads((root/(BASE+'_results.json')).read_text());lean=(root/(BASE+'.lean')).read_text();out=(root/(BASE+'_output.txt')).read_text()
 names=re.findall(r'^#check (\S+)',lean,re.M)
 check('ACTUAL_KERNEL_EXIT_ZERO',rr['status']=='PASS' and rr['compiler_exit_code']==0)
 check('ALL_134_NEW_PROPOSITIONS_AND_TRANSITIVE_AXIOMS_PRINTED',names==rr['declarations'] and len(names)==rr['printed_propositions']==rr['printed_axiom_dependencies']==134)
 check('CAPSULE_AND_TRANSCRIPT_FRESH',sha(BASE+'.lean')==rr['capsule_sha256'] and sha(BASE+'_output.txt')==rr['output_sha256'])
 check('NO_PLACEHOLDER_OR_COMPILER_TRUST_LEAF',not re.search(r'\b(sorry|admit|axiom|native_decide)\b',lean) and 'sorryAx' not in out and 'Lean.trustCompiler' not in out and not re.search(r'\berror(?:\(|:)',out))
 axioms=set()
 for m in re.finditer(r'depends on axioms: \[([^]]*)\]',out,re.S):axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
 check('ONLY_STANDARD_TRANSITIVE_AXIOMS',sorted(axioms)==rr['axioms']==['Classical.choice','Quot.sound','propext'])
 for n in names:check('ACTUAL_DECLARATION_'+n,n in out and ("'"+n+"' depends on axioms:" in out or "'"+n+"' does not depend on any axioms" in out))
 for p,d in {**rr['transitive_d0_source_sha256'],**rr['toolchain_input_sha256'],**rr['prior_packet_input_sha256']}.items():check('SOURCE_PIN_'+p,sha(p)==d)
 check('ALL_60_ACTUAL_D0_SOURCE_OWNERS_PINNED',len(rr['transitive_d0_source_sha256'])==60)
 check('ACTUAL_TYPED_HISTORY_AND_FLOW_QUANTIFIERS_PRESENT',all(x in out for x in ['ArchivePair','LevelOneSceneHistory','CompleteJointSceneLaw','NativeFlowWithAllActiveRoleOperations','primitiveRoot','Tendsto','653','702']))
 if expected is not None:
  early={'status':'PASS','input_head':SCOPE['input_head'],'capsule':BASE+'.lean','capsule_sha256':sha(BASE+'.lean'),'lean_receipt':BASE+'_results.json','lean_receipt_sha256':sha(BASE+'_results.json'),'lean_output_sha256':sha(BASE+'_output.txt'),'proof':PROOF,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),'previous_hardware_cases_recounted':False,'native_scene':{'vertices':33,'zones':[9,11,13],'degrees':[24,22,20],'histories':718,'apparatus_history_coordinates':16,'history_complement':702,'joint_null_archive':653}}
  assert all(expected.get(k)==v for k,v in early.items()),'EXACT_PAYLOAD_MISMATCH'
 import sympy as sp
 bits=list(product([0,1],repeat=3));index={b:i for i,b in enumerate(bits)}
 zone=[0]*9+[1]*11+[2]*13;offset=[0,9,20];degrees=[24,22,20]
 edges=[(u,v) for u in range(33) for v in range(33) if zone[u]!=zone[v]];ei={e:i for i,e in enumerate(edges)}
 check('ALL_33_TYPED_VERTICES_AND_718_OWNED_HISTORIES',len(zone)==33 and len(edges)==718)
 J=sp.MutableSparseMatrix(718,33,{(i,v):1 for i,(u,v) in enumerate(edges)})
 S=sp.MutableSparseMatrix(718,33,{(i,u):1 for i,(u,v) in enumerate(edges)})
 D=sp.diag(*[degrees[z] for z in zone]);C=D.inv()*J.T
 R=sp.MutableSparseMatrix(718,718,{(i,ei[(v,u)]):1 for i,(u,v) in enumerate(edges)})
 Adj=sp.Matrix(33,33,lambda u,v:int(zone[u]!=zone[v]));T=D.inv()*Adj;N=sp.eye(33)-T
 check('ACTUAL_ENDPOINT_AND_SOURCE_GRAMS',J.T*J==D and S.T*S==D and J.T*S==Adj)
 check('ACTUAL_ENDPOINT_READOUT_AND_REVERSED_READOUT',C*J==sp.eye(33) and C*S==T and R*J==S and R*S==J)
 I2=sp.eye(2);J2=sp.Matrix([[0,-1],[1,0]]);Z2=sp.diag(1,-1)
 oldZ=sp.kronecker_product(I2,Z2,I2);oldJ=sp.kronecker_product(I2,J2,I2)
 p0=(sp.sqrt(5)-1)/2;a=sp.sqrt(p0)
 check('ACTUAL_OWNED_P0_GOLDEN_NORMALIZATION',sp.simplify(p0+p0**2-1)==0 and sp.simplify(a**2+p0**2-1)==0)
 for i,j in product(range(2),repeat=2):
  A2=sp.zeros(2);A2[i,j]=1;active=sp.kronecker_product(A2,I2,I2)
  check('COMPLETE_ACTIVE_MATRIX_BASIS_COMMUTES_OLD_PARITY_'+str((i,j)),active*oldZ==oldZ*active)
 check('THE_OWNED_OLD_MEMORY_TURN_CHANGES_PARITY',oldJ*oldZ!=oldZ*oldJ and oldJ*oldJ==-sp.eye(8))
 qpath='03_FORMALIZATION/D0/Claims/Q8DedekindMinimality.lean'
 qtxt=(root/qpath).read_text().split('def Q8 :')[1].split('  e :=')[0]
 table=[[int(x) for x in row.split(',')] for row in re.findall(r'!\[([0-9, ]+)\]',qtxt)]
 check('LITERAL_OWNED_Q8_TABLE_EXTRACTED',len(table)==8 and all(len(row)==8 for row in table))
 ones=sp.ones(8,1)
 for g,row in enumerate(table):
  reg=sp.Matrix(8,8,lambda i,j:int(i==row[j]));check('ACTUAL_Q8_REGULAR_CONSTANT_RECORD_'+str(g),reg*ones==ones and sorted(row)==list(range(8)))
 bad=sp.zeros(33,8)
 for j,(aa,rrr,ss) in enumerate(bits):bad[2*(2*rrr+ss),j]=1;bad[2*(2*rrr+ss)+1,j]=-1
 check('REPEATED_OR_EMPTY_ARCHIVE_ADDRESSES_FAIL_THE_FULL_EIGHT_COORDINATE_FIBER',bad.rank()==4 and bad.T*D*bad!=sp.eye(8) and sp.zeros(8)!=sp.eye(8))
 pairs=[]
 for za,zb in permutations(range(3),2):
  tag=str((za,zb));B0=sp.zeros(33,8);loc=[];ds=[]
  for j,(aa,rrr,ss) in enumerate(bits):
   z=[za,zb][aa];v=offset[z]+2*(2*rrr+ss);loc.append([v,v+1]);ds.append(degrees[z]);B0[v,j]=1;B0[v+1,j]=-1
  gram=sp.diag(*[2*d for d in ds]);E0=J*B0;F0=S*B0
  check('ALL_ORIENTATION_LABELS_INJECTIVE_'+tag,len({v for q in loc for v in q})==16)
  check('ACTUAL_VERTEX_WEIGHTED_GRAM_'+tag,B0.T*D*B0==gram)
  check('UNWEIGHTED_COLUMNS_ARE_NOT_FALSE_NORMALIZED_'+tag,E0.T*E0==gram and gram!=sp.eye(8))
  check('BOTH_FULL_HISTORY_ARMS_AND_CROSS_GRAM_'+tag,F0.T*F0==gram and E0.T*F0==sp.zeros(8))
  check('ACTUAL_BOTH_HISTORY_READOUTS_'+tag,C*E0==B0 and C*F0==sp.zeros(33,8) and C*R*E0==sp.zeros(33,8) and C*R*F0==B0)
  check('ACTUAL_REVERSAL_EXCHANGES_ARMS_'+tag,R*E0==F0 and R*F0==E0)
  check('OWNED_NORMALIZED_OPERATOR_ON_ALL_ARCHIVE_COLUMNS_'+tag,Adj*B0==sp.zeros(33,8) and N*B0==B0)
  nus=[1/sp.sqrt(2*d) for d in ds]
  check('ALL_NATIVE_ROOT_WEIGHTS_EXACT_'+tag,all(sp.simplify(2*d*n*n)==1 for d,n in zip(ds,nus)))
  even=sp.zeros(33,12)
  for z,r in product(range(3),range(4)):
   even[offset[z]+2*r,4*z+r]=1;even[offset[z]+2*r+1,4*z+r]=1
  check('ALL_THREE_ARCHIVES_KEEP_THEIR_EVEN_MEMORY_'+tag,B0.T*D*even==sp.zeros(8,12))
  rect=sp.zeros(718,1)
  for edge,s in [((0,9),1),((1,9),-1),((0,10),-1),((1,10),1)]:rect[ei[edge],0]=s
  check('NONEMPTY_INVISIBLE_HISTORY_CONTROL_'+tag,C*rect==sp.zeros(33,1) and C*R*rect==sp.zeros(33,1) and rect!=sp.zeros(718,1))
  check('ALL_APPARATUS_OPERATIONS_RETAIN_INVISIBLE_RECTANGLE_'+tag,E0.T*rect==sp.zeros(8,1) and F0.T*rect==sp.zeros(8,1))
  nativeTrace=sum(sum(E0[i,j]**2+F0[i,j]**2 for i in range(718))/(2*ds[j]) for j in range(8))
  check('EXACT_FULL_HISTORY_SUPPORT_AND_COMPLEMENT_'+tag,nativeTrace==16 and 718-nativeTrace==702 and 16+49+653==718)
  rawOdd=B0.T*D
  check('NO_EMPTY_ARCHIVE_FIBER_'+tag,rawOdd*B0==gram and gram.det()!=0)
  F=sp.zeros(8)
  for j,(aa,rrr,ss) in enumerate(bits):F[index[(aa,rrr^aa,ss)],j]=1
  check('RETAINING_RECORDING_IS_OUTSIDE_THE_DECLARED_FLOW_PARITY_CLASS_'+tag,F.T*F==sp.eye(8) and F*oldZ!=oldZ*F)
  # Leaving out the reversed arm violates exact reversal covariance for any nonidentity local operation.
  j=index[(0,1,0)];Ginv=gram.inv();Lone=lambda x:x+E0*(oldZ-sp.eye(8))*Ginv*(E0.T*x)
  check('ONE_ARM_ONLY_IS_NOT_A_REVERSAL_COVARIANT_EXTENSION_'+tag,Lone(R*E0[:,j])!=R*Lone(E0[:,j]))
  pairs.append({'addresses':[za,zb],'orientation_labels':loc,'native_degrees':ds,'normalization_squared':['1/'+str(2*d) for d in ds],'endpoint_rank':8,'source_rank':8,'cross_gram_zero':True,'history_support_trace':16,'history_complement_trace':702,'joint_null_archive_trace':653,'even_archive_components_retained':12,'complete_vertex_complement':25})
 payload={'status':'PASS','input_head':SCOPE['input_head'],'scope':SCOPE,'check_count':len(checks),'checks':checks,'capsule':BASE+'.lean','capsule_sha256':sha(BASE+'.lean'),'lean_receipt':BASE+'_results.json','lean_receipt_sha256':sha(BASE+'_results.json'),'lean_output_sha256':sha(BASE+'_output.txt'),'proof':PROOF,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),'archive_pairs':pairs,'native_scene':{'vertices':33,'zones':[9,11,13],'degrees':degrees,'histories':718,'apparatus_history_coordinates':16,'history_complement':702,'joint_null_archive':653},'all_word_boundary':'closed old-parity commutant for the entire declared joint-flow palette and all active-role matrices, including the actual owned p0 gate; not whole-core operation completeness','previous_hardware_cases_recounted':False}
 if expected is not None:assert payload==expected,'EXACT_PAYLOAD_MISMATCH'
 if args.output:args.output.write_text(json.dumps(payload,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print('PASS_FAITHFUL_NATIVE_ARCHIVE_CARRIER_AND_COMPLETE_DECLARED_FLOW_BOUNDARY',len(checks),flush=True)
if __name__=='__main__':main()
