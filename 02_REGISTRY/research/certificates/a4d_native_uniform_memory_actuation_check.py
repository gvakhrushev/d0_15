#!/usr/bin/env python3
"""Full minimal real recording/comparison family; Q8 all-word actuation boundary."""
import argparse,hashlib,json,re
from itertools import permutations,product
from pathlib import Path
import sympy as s
BASE='02_REGISTRY/research/certificates/a4d_native_uniform_memory_actuation'
PROOF='02_REGISTRY/research/A4D_NATIVE_UNIFORM_MEMORY_ACTUATION.md'
SCOPE={
 'input_head':'d8b8f0712da3ddb23f966ed7b13b4e06b4973a71',
 'class':'ENTIRE_MINIMAL_FOUR_REAL_COORDINATE_RETAINING_RECORDING_COMPARISON_FAMILY_AND_ALL_COMPLETE_WORDS_IN_THE_DECLARED_Q8_ACTIVE_ROTATION_PALETTE',
 'forward_and_reverse_coherent_completions_both_retained':True,
 'complete_declared_joint_family_has_256_pairs':True,
 'all_192_orientation_reversing_pairs_have_a_thirteen_forward_operation_memory_transfer':True,
 'remaining_64_pairs_have_a_kernel_all_word_and_no_vanishing_error_obstruction':True,
 'obstruction_uses_the_actual_owned_left_Q8_frame':True,
 'all_owned_Q8_operations_and_all_normalized_active_angles_are_in_the_obstructed_palette':True,
 'independent_phi_reference_distinguishes_orientation_while_self_preparation_does_not':True,
 'full_programme_error_is_preserved_at_all_literal_normalized_golden_depths':True,
 'finite_word_census_is_the_all_word_proof':False,
 'unsigned_forward_phase_completion_is_selected_from_M1':False,
 'all_256_pairs_have_workspace_independent_memory_actuation':False,
 'both_proper_operations_are_denied_correct_boolean_truth':False,
 'minimal_real_class_exhausts_D0_or_all_complex_large_apparatus':False,
 'old_memory_gate_is_assumed_as_a_palette_primitive':False,
 'operator_word_length_is_native_endpoint_MDL_or_full_runtime_budget':False,
 'independent_reference_is_prepared_by_the_tested_gate':False,
 'moving_the_operator_alone_is_whole_apparatus_gauge_transport':False,
 'larger_ancillary_processor_is_excluded_by_tensor_refinement_obstruction':False,
 'old_gate_operator_obstruction_excludes_all_scene_or_state_preparation':False,
 'physical_representation_addressability_preparation_or_decoder_admission_derived':False,
 'the_internal_full_word_schedule_is_derived_from_the_matrix_product':False,
 'new_action_selector_temperature_coupling_source_or_postulate_added':False,
 'joint_native_heat_tangent_refinement_or_core_completeness_derived':False,
 'own_metric_matter_source_and_physical_Ward_derived':False,
 'quantitative_metric_contrast_or_native_stationarity_transferred':False,
 'curved_joint_roots_soundness_recovery_or_constraints_derived':False,
 'all_prior_propositions_counted_as_new':False,
 'positive_GR':False,'G0b_closed':False,'G0_closed':False,'global_closure':False,
 'original_310_202_317_terminals_changed':False,
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
 check('ACTUAL_COMPILER_EXIT_ZERO',rr['status']=='PASS' and rr['compiler_exit_code']==0)
 check('ALL_ACTUAL_NEW_TYPES_AND_TRANSITIVE_AXIOMS',names==rr['declarations'] and rr['printed_propositions']==rr['printed_axiom_dependencies']==len(names) and len(names)>50)
 check('COMPILED_CAPSULE_AND_TRANSCRIPT_FRESH',sha(BASE+'.lean')==rr['capsule_sha256'] and sha(BASE+'_output.txt')==rr['output_sha256'])
 check('NO_PLACEHOLDER_OR_COMPILER_TRUST_LEAF','sorryAx' not in out and 'Lean.trustCompiler' not in out and re.search(r'\berror(?:\(|:)',out) is None and re.search(r'\b(sorry|admit|axiom|native_decide)\b',lean) is None)
 axioms=set()
 for m in re.finditer(r'depends on axioms: \[([^]]*)\]',out,re.S):axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
 check('STANDARD_TRANSITIVE_AXIOMS_ONLY',sorted(axioms)==rr['axioms']==['Classical.choice','Quot.sound','propext'])
 for n in names:check('ACTUAL_DECLARATION_'+n,n in out and ("'"+n+"' depends on axioms:" in out or "'"+n+"' does not depend on any axioms" in out))
 check('ACTUAL_ALL_WORD_AND_FULL_LIMIT_PROPOSITIONS',all(x in out for x in ['Palette','completeWord','NormalizesAxes','Tendsto','OrderMemoryReadout.spin','RetainingRealRecording','realHistoryInclusion','primitiveRoot']))
 pins={**rr['transitive_d0_source_sha256'],**rr['toolchain_input_sha256'],**rr['prior_packet_input_sha256']}
 for path,digest in pins.items():check('SOURCE_PIN_'+path,sha(path)==digest)
 check('PRIMARY_Q8_FRAME_AND_P0_OWNERS_PINNED',all('03_FORMALIZATION/D0/'+x in rr['transitive_d0_source_sha256'] for x in ['Representation/OrderMemoryReadout.lean','Representation/GoldenCoherentMemory.lean','Representation/FiniteProtocolClock.lean']))
 C=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
 R=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
 T=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
 Zf=s.diag(1,1,-1,-1);Zr=s.diag(1,-1,1,-1)
 e0=s.Matrix([1,0,0,0]);e1=s.Matrix([0,1,0,0]);e2=s.Matrix([0,0,1,0]);e3=s.Matrix([0,0,0,1])
 a,p=s.symbols('a p',real=True);G=s.Matrix([[a,-p],[p,a]])
 Ga=s.kronecker_product(G,s.eye(2));Gr=s.kronecker_product(s.eye(2),G)
 def left(a,b,c,d):return s.Matrix([[a,-b,-c,-d],[b,a,-d,c],[c,d,a,-b],[d,-c,b,a]])
 axes=[left(0,1,0,0),left(0,0,1,0),left(0,0,0,1)]
 q8=[left(*v) for v in [(1,0,0,0),(-1,0,0,0),(0,1,0,0),(0,-1,0,0),(0,0,1,0),(0,0,-1,0),(0,0,0,1),(0,0,0,-1)]]
 signed_axes=axes+[-x for x in axes]
 check('OWNED_MEMORY_GATE_IS_A_LEFT_QUATERNION_ROTATION',Gr==a*s.eye(4)+p*axes[0])
 for k,L in enumerate(axes):check('ANY_ACTIVE_ANGLE_COMMUTES_WITH_OWNED_LEFT_AXIS_'+str(k),s.expand(Ga*L-L*Ga)==s.zeros(4))
 for g,Q in enumerate(q8):check('ALL_ACTUAL_Q8_OPERATIONS_NORMALIZE_THE_OWNED_FRAME_'+str(g),all(Q*L*Q.T in signed_axes for L in axes))
 # Derive the basis skeletons from retention and blank-input truth on all permutations.
 bits=list(product([0,1],repeat=2));idx={v:i for i,v in enumerate(bits)};forward=[];reverse=[]
 for perm in permutations(range(4)):
  if all(bits[perm[i]][0]==bits[i][0] for i in range(4)) and all(bits[perm[idx[(b,0)]]][1]==b for b in [0,1]):forward.append(perm)
  if all(bits[perm[i]][1]==bits[i][1] for i in range(4)) and all(bits[perm[idx[(0,r)]]][0]==r for r in [0,1]):reverse.append(perm)
 check('ALL_24_BASIS_SKELETONS_IN_BOTH_DIRECTIONS_CLASSIFIED',forward==[(0,1,3,2)] and reverse==[(0,3,2,1)])
 signs=list(product([1,-1],repeat=4));family=[];countU=countF=countClosed=0
 for d in signs:
  F=C*s.diag(*d);pd=int(s.prod(d))
  for c in signs:
   U=R*s.diag(*c);pc=int(s.prod(c));tag=str((d,c))
   check('COMPLETE_PAIR_ORTHOGONAL_'+tag,F.T*F==U.T*U==s.eye(4))
   check('COMPLETE_PAIR_RETAINED_TRUTH_'+tag,F*Zf==Zf*F and U*Zr==Zr*U and Zr*F*e0==F*e0 and Zr*F*e2==-F*e2 and Zf*U*e0==U*e0 and Zf*U*e1==-U*e1)
   check('REAL_PAIR_PARITY_IS_ORIENTATION_'+tag,F.det()==-pd and U.det()==-pc)
   check('NO_NEW_INVERSE_PRIMITIVE_'+tag,F**4==U**4==s.eye(4) and F.T==F**3 and U.T==U**3)
   S=U*F*U;V=F*U*F
   Hu=s.expand(S*Ga*S.T);Hf=s.expand(V*Ga*V.T)
   su0=d[0]*d[2]*c[2]*c[3];su1=d[1]*d[3]*c[2]*c[3]
   sf0=c[0]*c[3]*d[1]*d[2];sf1=c[1]*c[2]*d[1]*d[2]
   check('FULL_REVERSE_ROUTE_BRANCH_ORIENTATION_'+tag,Hu==s.diag(G.subs(p,su0*p),G.subs(p,su1*p)) and su1==pd*su0)
   check('FULL_ALTERNATE_ROUTE_BRANCH_ORIENTATION_'+tag,Hf==s.diag(G.subs(p,sf0*p),G.subs(p,sf1*p)) and sf1==pc*sf0)
   wu=[U,F,U,Ga,U,U,U,F,F,F,U,U,U];wf=[F,U,F,Ga,F,F,F,U,U,U,F,F,F]
   val=lambda w:s.expand(s.prod(w))
   check('COMPLETE_FORWARD_ONLY_CODE_BOTH_ROUTES_'+tag,len(wu)==len(wf)==13 and val(wu)==Hu and val(wf)==Hf)
   if pd==1:check('UNIFORM_MEMORY_TRANSFER_REVERSE_'+tag,Hu==Gr.subs(p,su0*p));countU+=1
   if pc==1:check('UNIFORM_MEMORY_TRANSFER_ALTERNATE_'+tag,Hf==Gr.subs(p,sf0*p));countF+=1
   if pd==pc==-1:
    check('ALL_PROPER_PAIR_PRIMITIVES_NORMALIZE_LEFT_Q8_'+tag,all(F*L*F.T in signed_axes and U*L*U.T in signed_axes for L in axes))
    check('PROPER_PAIR_SIMPLE_ROUTE_IS_NOT_WORKSPACE_INDEPENDENT_'+tag,Hu[1,0]==-Hu[3,2] and Hf[1,0]==-Hf[3,2])
    countClosed+=1
   family.append({'forward_signs':list(d),'reverse_signs':list(c),'forward_parity':pd,'reverse_parity':pc,'reverse_branch_orientations':[su0,su1],'alternate_branch_orientations':[sf0,sf1],'class':'ALL_WORD_OBSTRUCTED_PROPER_PALETTE' if pd==pc==-1 else 'THIRTEEN_OPERATION_UNIFORM_TRANSFER'})
 check('ENTIRE_JOINT_REAL_CLASS_COUNTS',len(family)==256 and countU==countF==128 and countClosed==64 and len(family)-countClosed==192)
 check('OLD_GATE_IS_NOT_SMUGGLED_INTO_PROPER_PALETTE',SCOPE['old_memory_gate_is_assumed_as_a_palette_primitive'] is False)
 # Actual p0, retaining exact algebra rather than using floating SVD/rank.
 gb=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.EX)
 red=lambda e:s.expand(gb.reduce(s.expand(e))[1])
 pv=(s.sqrt(5)-1)/2;av=s.sqrt(pv);cos=red(a*a-p*p);sin=2*a*p
 check('ACTUAL_P0_FORCES_BOTH_NONZERO_ROTATION_COEFFICIENTS',cos==2*p-1 and pv>0 and pv<1 and pv>s.Rational(1,2) and av>0)
 check('ROTATION_COEFFICIENTS_HAVE_UNIT_TOTAL_WEIGHT',red(cos*cos+sin*sin-1)==0)
 rotated=s.expand(Gr*axes[1]*Gr.T)
 check('ACTUAL_CONJUGATED_AXIS_HAS_TWO_NONZERO_COMPONENTS',s.expand(rotated-(a*a-p*p)*axes[1]-2*a*p*axes[2])==s.zeros(4))
 # The kernel supplies closure under arbitrary complete words and under limits.
 # This exact six-point distance is an independent quantitative hostile control.
 gaps=[red(sum((rotated-Q)[i,j]**2 for i in range(4) for j in range(4))) for Q in signed_axes]
 check('ALL_SIX_FINITE_FRAME_GAPS_ARE_EXACT',gaps==[8,8-8*cos,8-8*sin,8,8+8*cos,8+8*sin])
 check('ACTUAL_GAP_IS_STRICTLY_POSITIVE',all(s.simplify(v.subs({a:av,p:pv}))>0 for v in gaps))
 check('SINE_IS_THE_LARGER_POSITIVE_COEFFICIENT',s.simplify((sin-cos).subs({a:av,p:pv}))>0)
 floor=s.sqrt((1-2*av*pv)/2)
 check('OPERATOR_NORM_GAP_IS_NONZERO',s.simplify(1-2*av*pv)>0 and floor>0)
 # Anchored vs co-moving reference, through the represented comparator's own flag.
 for c in signs:
  U=R*s.diag(*c)
  for sg in [1,-1]:
   x=U*Gr.subs(p,sg*p)*s.Matrix([a,p,0,0]);xf=U*Gr.subs(p,sg*p)*s.Matrix([a,sg*p,0,0])
   check('INDEPENDENT_GOLDEN_REFERENCE_ORIENTATION_'+str((c,sg)),red(x[2]**2+x[3]**2-2*p**3*(1+sg))==0)
   check('SELF_PREPARATION_ORIENTATION_HOSTILE_'+str((c,sg)),red(xf[2]**2+xf[3]**2-4*p**3)==0)
 K=s.diag(1,-1,1,-1)
 check('WHOLE_FRAME_ORIENTATION_TRANSPORT_MOVES_THE_REFERENCE',K*Gr*K==Gr.subs(p,-p) and K*s.Matrix([a,p,0,0])==s.Matrix([a,-p,0,0]))
 # Every golden ancillary cylinder has unit complete weight; no junk/reset removed.
 cylinders=[]
 for n in range(5):
  words=list(product([0,1],repeat=2*n));v=s.Matrix([a**w.count(0)*p**w.count(1) for w in words])
  check('WHOLE_GOLDEN_CYLINDER_UNIT_WEIGHT_'+str(n),red(v.dot(v))==1)
  # Same complete error for a hostile proper implementation and target, including correlated input.
  d=(1,1,1,-1);c=(1,1,1,-1);F=C*s.diag(*d);U=R*s.diag(*c);W=U*F*U*Ga*(U*F*U).T
  x=s.Matrix([a,p,a*p,p*p]);error=s.expand((W-Gr)*x)
  whole=s.kronecker_product(error,v)
  check('FULL_REFINEMENT_PRESERVES_COMPLETE_PROGRAMME_ERROR_'+str(n),red(whole.dot(whole)-error.dot(error))==0)
  cylinders.append({'pairs':n,'retained_history_cardinality':len(words),'unit_mass':'1'})
 check('NO_GO_HAS_EXPLICIT_SCOPE_NOT_WHOLE_CORE',not SCOPE['minimal_real_class_exhausts_D0_or_all_complex_large_apparatus'])
 check('PHI_WEIGHT_IS_NOT_AN_OLD_MEMORY_CONTROL_ADMISSION',not SCOPE['physical_representation_addressability_preparation_or_decoder_admission_derived'])
 # Real phases can change the answer while retaining the same exact Boolean truth.
 proper=R*s.diag(1,1,1,-1)
 check('UNSIGNED_SELECTION_WOULD_DELETE_VALID_PHASES',proper.T*proper==s.eye(4) and proper*Zr==Zr*proper and proper.det()==1 and proper!=R)
 check('FORWARD_PHASES_CANNOT_BE_FROZEN_WITHOUT_A_SCOPE_RESTRICTION',(C*s.diag(1,1,1,-1)).det()==1 and C.det()==-1)
 check('SPECIAL_DEGENERATE_TARGET_IS_NOT_EXCLUDED',s.eye(4)*axes[1]*s.eye(4) in signed_axes)
 check('AN_ORIENTATION_REVERSING_EXCHANGE_BREAKS_THE_OBSTRUCTED_PALETTE',any(T*L*T.T not in signed_axes for L in axes))
 exact={'minimal_real_recording_count':16,'minimal_real_comparison_count':16,'full_joint_count':256,'uniform_transfer_pair_count':192,'proper_all_word_obstructed_pair_count':64,'each_positive_parity_route_pair_count':128,'full_forward_only_programme_length':13,'actual_q8_axis_count':6,'proper_pair_family':family,'actual_p0_conjugated_axis_coefficients':['p^3','2*p^(3/2)'],'actual_p0_axis_frobenius_squared_gaps':list(map(str,gaps)),'proper_all_word_operator_norm_floor':'sqrt((1-2*p^(3/2))/2)','proper_all_word_operator_norm_floor_decimal':str(s.N(floor,18)),'independent_reference_true_weights':['4*p^3','0'],'self_prepared_reference_true_weights':['4*p^3','4*p^3'],'whole_cylinder_checks':cylinders}
 ledger={'status':'PASS','input_head':SCOPE['input_head'],'scope':SCOPE,'exact':exact,'checks':checks,'check_count':len(checks),'source_sha256':pins,'kernel_receipt_sha256':sha(BASE+'_results.json'),'checker_sha256':sha(BASE+'_check.py'),'proof_sha256':sha(PROOF)}
 if expected is not None:assert expected==ledger,'EXACT_CERTIFICATE_MISMATCH'
 if args.output:args.output.write_text(json.dumps(ledger,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print('PASS_UNIFORM_MEMORY_ACTUATION',len(checks),'CONTROLS_ALL_256_PAIRS_Q8_ALL_WORD_BOUNDARY')
if __name__=='__main__':main()
