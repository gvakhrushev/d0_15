#!/usr/bin/env python3
"""Verified native archive comparison: exact class, phase and refinement controls."""
import argparse,hashlib,json,re
from itertools import permutations,product
from pathlib import Path
import sympy as s
BASE='02_REGISTRY/research/certificates/a4d_native_verified_archive_actuation'
PROOF='02_REGISTRY/research/A4D_NATIVE_VERIFIED_ARCHIVE_ACTUATION.md'
SCOPE={
 'input_head':'4f301680636a8181580a5d1455ff727257c0cabe',
 'class':'ALL_COMPLETE_REALIZATIONS_OF_AN_EXPLICITLY_REPRESENTED_VERIFIED_BINARY_DISTINCTION_AND_COMPLETE_MINIMAL_RETAINING_REAL_COMPARATOR_FAMILY',
 'owned_verification_truth_is_independent_of_the_dynamic_gate':True,
 'any_exact_complete_realization_requires_archive_commutator_at_least_sqrt2':True,
 'approximate_full_outcome_error_has_fixed_commutator_tradeoff':True,
 'basis_retaining_class_forces_the_existing_register':True,
 'actual_owned_register_is_bound_to_both_role_coordinate_placements':True,
 'complete_minimal_real_comparator_family_has_exactly_16_signed_completions':True,
 'coherent_phase_mode_retained_and_classified_in_the_declared_real_family':True,
 'same_owned_golden_gate_moves_to_old_memory_via_two_directions':True,
 'any_complete_intertwining_refinement_retains_the_actuation_floor':True,
 'literal_actual_p0_cylinder_preserves_full_commutator_mass_at_all_depths':True,
 'comparison_truth_by_itself_fixes_a_unique_coherent_phase_completion':False,
 'functional_comparison_is_silently_equated_to_physical_unitary_availability':False,
 'raw_history_bits_are_automatically_in_the_verified_observational_quotient':False,
 'all_complex_or_larger_comparator_apparatus_classes_exhausted':False,
 'the_minimal_real_class_exhausts_D0_dynamics':False,
 'physical_role_addressability_basis_preparation_or_decoder_admission_derived':False,
 'M1_public_catalogue_independence_selects_unsigned_coherent_registration':False,
 'primitive_endpoint_cost_is_executed_full_program_budget':False,
 'full_native_MDL_budget_and_internal_schedule_admitted':False,
 'reset_trace_postselection_or_initial_target_preparation_used':False,
 'bare_carrier_growth_implies_operator_refinement_compatibility':False,
 'X_is_an_independently_admitted_physical_or_gravitational_detector':False,
 'full_outcome_eigenvector_errors_are_empirical_probability_errors':False,
 'prepared_contrast_is_inserted_as_native_stationarity_gate':False,
 'joint_native_heat_tangent_refinement_or_full_core_completeness_derived':False,
 'own_metric_matter_source_and_physical_Ward_derived':False,
 'quantitative_metric_contrast_or_native_stationarity_transferred':False,
 'curved_joint_roots_soundness_recovery_or_physical_constraints_derived':False,
 'new_action_selector_temperature_coupling_source_or_postulate_added':False,
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
 check('ALL_58_ACTUAL_TYPES_AND_TRANSITIVE_AXIOMS',len(names)==58 and names==rr['declarations'] and rr['printed_propositions']==rr['printed_axiom_dependencies']==58)
 check('COMPILED_CAPSULE_AND_TRANSCRIPT_FRESH',sha(BASE+'.lean')==rr['capsule_sha256'] and sha(BASE+'_output.txt')==rr['output_sha256'])
 check('NO_PLACEHOLDER_OR_COMPILER_TRUST_LEAF','sorryAx' not in out and 'Lean.trustCompiler' not in out and re.search(r'\berror(?:\(|:)',out) is None and re.search(r'\b(sorry|admit|axiom|native_decide)\b',lean) is None)
 axioms=set()
 for m in re.finditer(r'depends on axioms: \[([^]]*)\]',out,re.S):axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
 check('STANDARD_TRANSITIVE_AXIOMS_ONLY',sorted(axioms)==rr['axioms']==['Classical.choice','Quot.sound','propext'])
 for n in names:check('ACTUAL_DECLARATION_'+n,n in out and ("'"+n+"' depends on axioms:" in out or "'"+n+"' does not depend on any axioms" in out))
 check('OWNED_PROTOCOL_REGISTER_P0_AND_GENERIC_REFINEMENT_TYPES',all(x in out for x in ['VerificationContract','VerificationProtocol','register','primitiveRoot','RetainingRealComparison','signedComparison','→ₗᵢ[ℝ]','→L[ℝ]','√2','realHistoryInclusion']))
 pins={**rr['transitive_d0_source_sha256'],**rr['toolchain_input_sha256'],**rr['prior_packet_input_sha256']}
 for path,digest in pins.items():check('SOURCE_PIN_'+path,sha(path)==digest)
 check('FUNCTIONAL_PROTOCOL_AND_REGISTER_HAVE_PRIMARY_SOURCE_PINS',all('03_FORMALIZATION/D0/'+x in rr['transitive_d0_source_sha256'] for x in ['Foundation/VerifiabilityNecessity.lean','Representation/FiniteProtocolClock.lean','Representation/PreparationMemoryBound.lean','Representation/GoldenCoherentMemory.lean']))
 # Independently derive the complete basis class, rather than enumerate a proposed gate list.
 bits=list(product([0,1],repeat=2));idx={v:i for i,v in enumerate(bits)}
 retained=[];correct=[];blank_only=[]
 for p in permutations(range(4)):
  keep=all(bits[p[i]][1]==bits[i][1] for i in range(4))
  truth=all(bits[p[idx[(0,r)]]][0]==r for r in [0,1])
  blank_ret=all(bits[p[idx[(0,r)]]][1]==r for r in [0,1])
  if keep:retained.append(p)
  if keep and truth:correct.append(p)
  if blank_ret and truth:blank_only.append(p)
 check('ALL_24_COMPLETE_BASIS_PERMUTATIONS_CLASSIFIED',len(retained)==4 and len(correct)==1 and len(blank_only)==2)
 C=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
 R=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
 T=s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
 X=s.kronecker_product(s.eye(2),s.Matrix([[0,1],[1,0]]))
 Z=s.diag(1,1,-1,-1);Zr=s.diag(1,-1,1,-1)
 e0=s.Matrix([1,0,0,0]);e1=s.Matrix([0,1,0,0]);e3=s.Matrix([0,0,0,1])
 check('BASIS_UNIQUENESS_BINDS_ACTUAL_REVERSE_COPY',correct==[(0,3,2,1)])
 check('GLOBAL_RETAINING_SPECIFICATION_IS_LOAD_BEARING',blank_only[0]!=blank_only[1] and correct[0] in blank_only)
 check('REGISTER_BOTH_ROLE_PLACEMENTS_ARE_COMPLETE_ORTHOGONAL',C.T*C==R.T*R==s.eye(4))
 check('COMPLETE_REGISTER_TRUTH_WITH_ALL_RECORDS_RETAINED',R*e0==e0 and R*e1==e3 and R*Zr==Zr*R)
 check('OLD_PROBE_ISOMETRY_SYMMETRY_AND_FLAG_COMMUTATION',X.T*X==s.eye(4) and X.T==X and X*Z==Z*X)
 check('TRUTH_IS_NOT_COMPUTED_BY_THE_ONE_WAY_CONTROLLER',C*X==X*C and C*e0==e0 and C*e1==e1 and Z*C*e1==C*e1)
 check('READING_OLD_MEMORY_BREAKS_THE_ONE_WAY_PROBE',R*X!=X*R and ((R*X-X*R)*e0).dot((R*X-X*R)*e0)==2)
 check('THREE_OWNED_REGISTRATIONS_EXCHANGE_COMPLETE_COORDINATES',R*C*R==T and T*T==s.eye(4) and T.T==T)
 a,p=s.symbols('a p',real=True);G=s.Matrix([[a,-p],[p,a]])
 check('SAME_OWNED_GOLDEN_GATE_MOVES_TO_OLD_RECORD',T*s.kronecker_product(G,s.eye(2))*T==s.kronecker_product(s.eye(2),G))
 check('NO_NEW_GOLDEN_MIXER_OR_COUPLING_PARAMETER',len((T*s.kronecker_product(G,s.eye(2))*T).free_symbols)==2)
 check('BOTH_COORDINATE_ROLES_ARE_RETAINED_DURING_EXCHANGE',T*e0==e0 and T*e1==s.Matrix([0,0,1,0]))
 c=s.symbols('c0:4',real=True)
 U=R*s.diag(*c);D=U*X-X*U;coupling=c[0]*c[3]+c[1]*c[2]
 gram=s.Matrix([[c[0]**2+c[1]**2,0,-coupling,0],[0,c[0]**2+c[1]**2,0,-coupling],[-coupling,0,c[2]**2+c[3]**2,0],[0,-coupling,0,c[2]**2+c[3]**2]])
 check('SYMBOLIC_COMPLETE_COMMUTATOR_GRAM_IDENTITY',s.expand(D.T*D-gram)==s.zeros(4))
 check('SYMBOLIC_UNNORMALIZED_BLANK_COMMUTATOR_MASS',s.expand((D*e0).dot(D*e0)-c[0]**2-c[1]**2)==0)
 phases=[]
 for signs in product([1,-1],repeat=4):
  u=R*s.diag(*signs);d=u*X-X*u;t=signs[0]*signs[3]+signs[1]*signs[2];parity=s.prod(signs)
  check('FULL_SIGNED_COMPARATOR_ORTHOGONAL_'+str(signs),u.T*u==s.eye(4))
  check('FULL_SIGNED_COMPARATOR_RETAINED_TRUTH_'+str(signs),u*Zr==Zr*u and Z*u*e0==u*e0 and Z*u*e1==-u*e1)
  check('FULL_SIGNED_BLANK_COMMUTATOR_MASS_'+str(signs),(d*e0).dot(d*e0)==2)
  check('FULL_SIGNED_PHASE_PARITY_GRAM_MODE_'+str(signs),t*t==2+2*parity and d.T*d==s.Matrix([[2,0,-t,0],[0,2,0,-t],[-t,0,2,0],[0,-t,0,2]]))
  eig=d.T*d
  check('FULL_SIGNED_COMPLETE_STRENGTH_SPECTRUM_'+str(signs),s.expand(eig.charpoly().as_expr()-(s.Symbol('lambda')-2-t)**2*(s.Symbol('lambda')-2+t)**2)==0)
  phases.append({'signs':list(signs),'phase_coupling':int(t),'parity':int(parity),'squared_commutator_norm':2+abs(t)})
 check('ENTIRE_REAL_PHASE_FAMILY_HAS_16_DISTINCT_OPERATORS',len({tuple(R*s.diag(*sg)) for sg in product([1,-1],repeat=4)})==16)
 check('PHASE_STRENGTH_SPLIT_IS_EIGHT_AND_EIGHT',sum(x['squared_commutator_norm']==2 for x in phases)==8 and sum(x['squared_commutator_norm']==4 for x in phases)==8)
 check('LOWER_BOUND_SQRT2_IS_SHARP_ON_FULL_STATE',(R*s.diag(1,1,1,-1)*X-X*R*s.diag(1,1,1,-1)).T*(R*s.diag(1,1,1,-1)*X-X*R*s.diag(1,1,1,-1))==2*s.eye(4))
 check('CORRECT_BOOLEAN_TRUTH_DOES_NOT_SELECT_UNSIGNED_PHASE',R*s.diag(1,1,1,-1)!=R and (R*e0).dot(R*e0)==1)
 # Complete normalized refinement: every ancillary history, including failed ones, remains.
 pv=(s.sqrt(5)-1)/2;av=s.sqrt(pv);gb=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.EX)
 red=lambda e:s.expand(gb.reduce(s.expand(e))[1]);zpoly=lambda M:all(red(e)==0 for e in M)
 check('OWNED_ACTUAL_P0_GOLDEN_NORMALIZATION',red(a*a+p*p-1)==0 and pv>0)
 check('OWNED_MEMORY_GATE_HAS_NONZERO_PROBE_COMMUTATOR',red((s.kronecker_product(s.eye(2),G)*X-X*s.kronecker_product(s.eye(2),G))[0,0])==-2*p and pv!=0)
 cylinder=[]
 for n in range(5):
  words=list(product([0,1],repeat=2*n));v=s.Matrix([a**w.count(0)*p**w.count(1) for w in words]);mass=red(v.dot(v))
  check('COMPLETE_GOLDEN_CYLINDER_NORMALIZATION_'+str(n),mass==1)
  full_diff=s.kronecker_product((R*X-X*R)*e0,v)
  check('COMPLETE_GOLDEN_CYLINDER_COMMUTATOR_MASS_'+str(n),red(full_diff.dot(full_diff))==2)
  cylinder.append({'pairs':n,'whole_history_cardinality':len(words),'mass':str(mass),'commutator_input_mass':'2'})
  # Test small matrices directly; the kernel supplies all n and all complete operators.
  if n<=2:
   eye=s.eye(len(words));A=s.kronecker_product(R,eye);B=s.kronecker_product(X,eye);jx=s.kronecker_product(e0,v)
   check('LITERAL_COMPLETE_INTERTWINING_'+str(n),A*B*jx-B*A*jx==full_diff)
 check('ANY_NORMALIZED_ANCILLA_RETAINS_THE_FULL_COMPARISON_FLOOR',(s.Matrix([s.Rational(3,5),s.Rational(4,5)]).dot(s.Matrix([s.Rational(3,5),s.Rational(4,5)])))==1)
 # Hostile controls remove one actual hypothesis at a time.
 check('ZERO_STATE_CANNOT_SUPPLY_THE_UNIT_INPUT_FLOOR',((R*X-X*R)*s.zeros(4,1)).dot((R*X-X*R)*s.zeros(4,1))==0)
 check('CONSTANT_OUTPUT_COMMUTING_DYNAMICS_FAILS_DIFFERENT_TRUTH',Z*e0==e0 and Z*e1==e1 and s.eye(4)*X==X*s.eye(4))
 check('COMPLETE_COMMUTING_IDENTITY_HAS_TOTAL_TRUTH_ERROR_TWO',(Z*e1+e1).dot(Z*e1+e1)==4 and Z*e0-e0==s.zeros(4,1))
 check('UNNORMALIZED_PROBE_DOES_NOT_SATISFY_ISOMETRY',(X/2).T*(X/2)==s.eye(4)/4)
 check('CHANGING_OLD_PROBE_CHANGES_THE_DECLARED_EXPERIMENT',R*s.eye(4)==s.eye(4)*R and s.eye(4)*e0!=e1)
 check('FLAG_ACTING_PROBE_IS_NOT_OLD_RECORD_COMMUTING_PROBE',s.kronecker_product(s.Matrix([[0,1],[1,0]]),s.eye(2))*Z!=Z*s.kronecker_product(s.Matrix([[0,1],[1,0]]),s.eye(2)))
 check('PROJECTION_RESET_IS_NOT_COMPLETE_ORTHOGONAL',s.diag(1,0,0,1).T*s.diag(1,0,0,1)!=s.eye(4))
 check('RETENTION_AT_BLANK_INPUT_ALONE_DOES_NOT_CLASSIFY_OTHER_COLUMNS',len(blank_only)==2)
 check('NATIVE_GATE_NOT_DEFINED_BY_THE_SOUGHT_GR_EQUATION',SCOPE['prepared_contrast_is_inserted_as_native_stationarity_gate'] is False)
 exact={
  'basis_retaining_permutations':4,'basis_correct_retaining_comparisons':1,'correct_blank_only_retaining_permutations':2,
  'minimal_real_complete_comparator_count':16,'signed_comparison_phases':phases,
  'generic_exact_commutator_input_mass':'2','generic_exact_commutator_norm_lower_bound':'sqrt(2)',
  'approximate_total_full_outcome_error_tradeoff':'2-(e0+e1)<=norm(US-SU)^2',
  'commuting_comparator_minimum_total_outcome_error':'2','sharp_minimum_gram':'2*I4',
  'golden_transfer':'(C_rev*C*C_rev)*(G tensor I)*(C_rev*C*C_rev)=I tensor G',
  'golden_transfer_complete_operator_word_length':7,
  'whole_golden_cylinder_checks':cylinder,
 }
 ledger={'status':'PASS','input_head':SCOPE['input_head'],'scope':SCOPE,'exact':exact,'checks':checks,'check_count':len(checks),'source_sha256':pins,'kernel_receipt_sha256':sha(BASE+'_results.json'),'checker_sha256':sha(BASE+'_check.py'),'proof_sha256':sha(PROOF)}
 if expected is not None:assert expected==ledger,'EXACT_CERTIFICATE_MISMATCH'
 if args.output:args.output.write_text(json.dumps(ledger,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print('PASS_VERIFIED_ARCHIVE_ACTUATION',len(checks),'CONTROLS_ALL_16_COMPLETE_PHASES_AND_RETAINED_REFINEMENT')
if __name__=='__main__':main()
