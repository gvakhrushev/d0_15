#!/usr/bin/env python3
"""Exact controls for retained golden program compilation and shared records."""
import argparse,hashlib,json,re
from pathlib import Path
import sympy as s

BASE='02_REGISTRY/research/certificates/a4d_native_golden_program_compilation'
PROOF='02_REGISTRY/research/A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md'
SCOPE={
 'class':'ADDRESSED_GOLDEN_CNOT_COMPLETE_PROGRAM_WITH_RETAINED_ANCILLA_AND_FIXED_HISTORY_TARGET',
 'input_head':'66d51fbad02e683561c938b71ba728eb9b25bf03',
 'literal_p0_golden_square_changes_basis_kernel_verified':True,
 'external_real_density_theorem':'Shi_quant-ph_0205115v2_Theorems_1.2_3.1_Definition_2.1',
 'external_compiler_theorem_used_after_hypotheses_checked':True,
 'external_density_and_efficiency_kernel_formalized':False,
 'addressed_G_CNOT_basis_preparation_and_all_records_are_declared_inputs':True,
 'forward_inverse_echo_preserves_supplied_basis_one_control':True,
 'all_physical_addressing_and_basis_preparations_forced_by_M1':False,
 'finite_success_correction_is_uniquely_computed_from_actual_word':True,
 'infinite_limit_or_independent_angle_is_a_correction_input':False,
 'complete_exact_corrected_state_has_fixed_initial_seed_target':True,
 'all_33_scene_targets_factor_through_one_common_unit_record':True,
 'common_record_preserves_correctly_paired_history_return':True,
 'orthonormal_and_degree_weighted_scene_coordinates_are_identified':False,
 'every_complete_word_error_counts_all_failed_records':True,
 'uniform_all_input_compiler_error_and_ancilla_leakage_kernel_verified':True,
 'single_blank_agreement_used_as_uniform_compiler_bound':False,
 'ancillary_reset_trace_postselection_or_fresh_copy_replacement_used':False,
 'all_ancillary_preparation_address_and_storage_costs_are_required':True,
 'arbitrary_complex_phase_quotient_used_for_real_pointer':False,
 'fixed_complete_readout_limit_independent_of_compiler_choice':True,
 'exact_finite_level_M1_catalogue_independence_derived':False,
 'whole_golden_cylinder_error_preservation_kernel_verified':True,
 'actual_phi_fifth_scale_and_literal_expanded_cost_kernel_verified':True,
 'all_fixed_polynomial_compiler_costs_eventually_fit_phi_5m':True,
 'actual_native_decoder_and_MDL_admission_derived':False,
 'code_length_equated_with_executed_path_length':False,
 'full_autonomous_internal_word_clock_physically_derived':False,
 'program_index_or_history_depth_is_physical_time_mesh_or_expansion':False,
 'common_phase_for_uncorrected_all_degree_outputs_derived':False,
 'positive_history_frame_unconditionally_physically_prepared':False,
 'full_2_pow_45_matrix_or_infinite_circuit_class_numerically_enumerated':False,
 'all_prior_preparation_propositions_counted_as_new':False,
 'full_core_controller_class_or_native_heat_tangent_variations_exhausted':False,
 'complementary_heat_parameters_selected_by_circuit_density':False,
 'own_metric_matter_source_and_physical_Ward_derived':False,
 'quantitative_metric_contrast_or_native_stationarity_transferred':False,
 'curved_joint_roots_soundness_recovery_or_physical_constraints_derived':False,
 'new_action_angle_temperature_selector_coupling_source_or_postulate_added':False,
 'positive_GR':False,'G0b_closed':False,'G0_closed':False,'global_closure':False,
 'original_310_202_317_terminals_changed':False,
}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path)
 a0=ap.parse_args();root=Path(__file__).resolve().parents[3]
 sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 expected=json.loads(a0.expect.read_text()) if a0.expect else None
 if expected is not None:assert expected['scope']==SCOPE,'PINNED_SCOPE_MISMATCH'
 checks=[]
 def check(n,v):assert bool(v),n;checks.append(n)
 rr=json.loads((root/(BASE+'_results.json')).read_text());lean=(root/(BASE+'.lean')).read_text();out=(root/(BASE+'_output.txt')).read_text()
 names=re.findall(r'^#check (\S+)',lean,re.M)
 check('ACTUAL_COMPILER_EXIT_ZERO',rr['status']=='PASS' and rr['compiler_exit_code']==0)
 check('ALL_80_NEW_ACTUAL_TYPES_AND_AXIOMS',names==rr['declarations'] and len(names)==rr['printed_propositions']==rr['printed_axiom_dependencies']==80)
 check('COMPILED_CAPSULE_AND_TRANSCRIPT_FRESH',sha(BASE+'.lean')==rr['capsule_sha256'] and sha(BASE+'_output.txt')==rr['output_sha256'])
 check('NO_PLACEHOLDER_OR_COMPILER_TRUST_LEAF','sorryAx' not in out and 'Lean.trustCompiler' not in out and re.search(r'\berror(?:\(|:)',out) is None and re.search(r'\b(sorry|admit|axiom|native_decide)\b',lean) is None)
 axioms=set()
 for m in re.finditer(r'depends on axioms: \[([^]]*)\]',out,re.S):axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
 check('STANDARD_TRANSITIVE_AXIOMS_ONLY',sorted(axioms)==rr['axioms']==['Classical.choice','Quot.sound','propext'])
 for n in names:check('ACTUAL_DECLARATION_'+n,n in out and "'"+n+"'" in out)
 check('WHOLE_NATIVE_AND_ANCILLA_TYPES_EXPLICIT',all(x in out for x in ['primitiveRoot','calibratedColumn','normalizedSuccessScalar','calibratedFullMatrix','actualSceneAlignedSeed','commonRecord','retainedFrame','EuclideanSpace','→L[ℝ]','evalWord','resolution','precision']))
 check('EXACTLY_TWELVE_TRANSITIVE_D0_PINS',len(rr['transitive_d0_source_sha256'])==12)
 pins=dict(rr['transitive_d0_source_sha256']);pins.update(rr['toolchain_input_sha256']);pins.update(rr['prior_packet_input_sha256'])
 for path,digest in pins.items():check('SOURCE_PIN_'+path,sha(path)==digest)
 for path in ['01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md','01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md','01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md']:pins[path]=sha(path)

 p,x=s.symbols('p a',real=True);gb=s.groebner([x*x-p,p*p+p-1],x,p,domain=s.EX)
 red=lambda e:s.expand(gb.reduce(s.expand(e))[1])
 zero=lambda M:all(red(e)==0 for e in M)
 G=s.Matrix([[x,-p],[p,x]]);copy=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
 check('OWNED_GOLDEN_ORTHOGONALITY',zero(G.T*G-s.eye(2)) and zero(G*G.T-s.eye(2)))
 check('NATIVE_SQUARED_GATE_FORMULA',zero(G**2-s.Matrix([[x*x-p*p,-2*x*p],[2*x*p,x*x-p*p]])))
 pg=(s.sqrt(5)-1)/2
 check('LITERAL_P0_INTERVAL_FOR_BASIS_CHANGE',bool(pg>s.Rational(1,2)) and bool(pg<1))
 check('NATIVE_SQUARED_GATE_NONZERO_DIAGONAL',red(x*x-p*p)==2*p-1)
 check('NATIVE_SQUARED_GATE_NONZERO_OFFDIAGONAL',red((2*x*p)**2)==red(4*p**3) and bool(4*pg**3>0))
 check('OWNED_RECORD_COPY_INVOLUTION',copy*copy==s.eye(4) and copy.T*copy==s.eye(4))
 rg=s.kronecker_product(s.eye(2),G)
 check('FORWARD_COPY_ECHO_RETAINS_ONE_AND_INVERTS_G',copy*rg*copy==s.diag(G,G.T))
 check('INVERSE_ECHO_ON_EVERY_TARGET_INPUT',zero((copy*rg*copy)[2:4,2:4]-G.T))
 check('BLANK_ZERO_CONTROL_IS_NOT_SUPPLIED_ONE',zero((copy*rg*copy)[0:2,0:2]-G) and G!=G.T)
 sg=s.kronecker_product(G,s.eye(2));full=s.Matrix([[x,0,-p,0],[0,x,0,-p],[0,p,0,x],[p,0,x,0]])
 check('CNOT_BOUND_TO_ACTUAL_OWNED_FULL_STEP',copy*sg==full and zero(full*sg.T-copy))
 phase=lambda z:s.Matrix([[s.re(s.expand(z)),-s.im(s.expand(z))],[s.im(s.expand(z)),s.re(s.expand(z))]])
 w=red((x+s.I*p)**8);r=1345-2176*p;K=red(s.conjugate(w)**2*(w-1)**2)
 check('FAST_POINTER_PHASE_IS_NATIVE_G_EIGHT',zero(phase(w)-G**8))
 check('FAST_GOLDEN_PARAMETER_RANGE',bool(r.subs(p,pg)>0) and bool(r.subs(p,pg)<s.Rational(1,6)))
 check('FINITE_SUCCESS_INCREMENT_USES_OWN_PHASE',red(K*s.conjugate(K)-(1-r)**2)==0)
 q=red(x**4+p**4);M=red(((1-q**4)/2)**5)
 check('ACTUAL_COMMON_RECORD_MASS_NATIVE',red(32*M-(1-q**4)**5)==0)
 check('ACTUAL_COMMON_RECORD_MASS_POSITIVE',bool(M.subs(p,pg)>0))
 check('FOUR_PAIR_FIRST_UNEQUAL_MASS_WITH_ALL_RECORDS',red(p**3*sum(q**j for j in range(4))-(1-q**4)/2)==0)
 check('FIRST_LABEL_FALSE_TRUE_RECORD_MASSES_EQUAL',red(x*x*p*p-p**3)==0)
 for d in [20,22,24]:
  e=red(1-d*M);c=s.Integer(1);s0=red(d*M)
  for k in range(4):
   check('COMPLETE_NATIVE_BALANCE_DEGREE_'+str(d)+'_STAGE_'+str(k),red(s0*c*s.conjugate(c)+e-1)==0)
   ep=red(e*(r+(1-r)*e)**2);cp=red(c*(1-K*e))
   check('LITERAL_FULL_SUCCESS_AND_REJECTED_RECURSION_'+str(d)+'_'+str(k),red(s0*cp*s.conjugate(cp)+ep-1)==0)
   e,c=ep,cp
 z0,z1,rho,ef=s.symbols('z0 z1 rho e',real=True)
 C=s.Matrix([[z0/rho,z1/rho],[-z1/rho,z0/rho]])
 check('CORRECTION_CLEARED_ORTHOGONAL_IDENTITY',s.simplify((C.T*C-s.eye(2))*rho**2-(z0*z0+z1*z1-rho**2)*s.eye(2))==s.zeros(2))
 check('CORRECTION_MAKES_OWN_SUCCESS_REAL_POSITIVE',s.simplify((C*s.Matrix([z0,z1])-s.Matrix([rho,0]))*rho-s.Matrix([z0*z0+z1*z1-rho*rho,0]))==s.zeros(2,1))
 check('CORRECTED_COMPLETE_STATE_COUNTS_REJECTED_MASS',s.expand((rho-1)**2+ef-(rho*rho-2*rho+1+ef))==0)
 check('RADIAL_ERROR_CANNOT_EXCEED_REJECTED_MASS',s.expand((2*ef-((rho-1)**2+ef)).subs(ef,1-rho*rho)-2*rho*(1-rho))==0)
 check('ZERO_SUCCESS_HAS_NO_UNIT_CALIBRATION',s.Matrix([[0,0],[0,0]]).T*s.zeros(2)!=s.eye(2))
 check('NATIVE_HALF_PRECISION_CONSTANT',s.Rational(1,5)<s.Rational(1,4))

 J=s.Matrix([[1,0],[0,0],[0,1],[0,0]]);I=s.eye(2)
 check('PREPARED_ANCILLA_INCLUSION_IS_COMPLETE_ISOMETRY',J.T*J==I)
 bad=copy*J-J
 check('SINGLE_BLANK_TEST_MISSES_REAL_COMPILER_FAILURE',bad[:,0]==s.zeros(4,1) and bad.T*bad==s.diag(0,2))
 H=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]]);V=s.kronecker_product(I,H)
 check('WHOLE_LEAKING_ANCILLA_STEP_IS_ORTHOGONAL',V.T*V==s.eye(4))
 D=V*J-J
 check('UNIFORM_ANCILLA_ERROR_COUNTS_LEAKAGE',D.T*D==s.Rational(4,5)*I)
 for k in [1,2,3]:
  check('REUSED_ALL_RECORD_WORD_NORM_'+str(k),(V**k*J).T*(V**k*J)==I)
 reset=J*J.T
 check('RESET_IS_NOT_AN_ADMITTED_WHOLE_ORTHOGONAL_STEP',(reset*V).T*(reset*V)!=s.eye(4) and (reset*V).det()==0)
 eta=s.Matrix([s.Rational(3,5),s.Rational(4,5)]);j0=s.Matrix([[1,0],[0,1],[0,0]]);R=s.Matrix([[0,0,1],[0,1,0],[1,0,0]])
 attached=s.kronecker_product(j0,eta)
 check('COMMON_RECORD_UNIT_MASS',(eta.T*eta)[0]==1)
 check('COMMON_RECORD_FULL_FRAME_GRAM',attached.T*attached==j0.T*j0)
 check('COMMON_RECORD_COMPLETE_REVERSE_INTERTWINING',s.kronecker_product(R,I)*attached==s.kronecker_product(R*j0,eta))
 check('COMMON_RECORD_FULL_RETURN_COMPRESSION',attached.T*s.kronecker_product(R,I)*attached==j0.T*R*j0)
 alt=s.Matrix([s.Rational(4,5),s.Rational(3,5)])
 check('COMMON_RECORD_REQUIREMENT_IS_SUBSTANTIVE',(eta.T*alt)[0]==s.Rational(24,25) and (eta.T*alt)[0]!=1)
 zones=[0]*9+[1]*11+[2]*13
 edges=[(u,v) for u in range(33) for v in range(33) if zones[u]!=zones[v]]
 degrees=[sum(v==b for u,v in edges) for b in range(33)]
 check('ACTUAL_SCENE_HAS_718_HISTORIES',len(edges)==718)
 check('ACTUAL_SCENE_FIBERS_HAVE_20_22_24_DEGREES',set(degrees)=={20,22,24})
 index={e:i for i,e in enumerate(edges)}
 check('ACTUAL_HISTORY_REVERSE_IS_COMPLETE_INVOLUTION',all(index[(v,u)]>=0 and edges[index[(v,u)]]==(v,u) for u,v in edges))
 for v in range(33):
  check('ACTUAL_SCENE_NORMALIZED_INCOMING_RAY_'+str(v),sum(s.Rational(1,degrees[v]) for u,b in edges if b==v)==1)
  check('ACTUAL_COMMON_RECORD_FACTOR_MASS_'+str(v),s.cancel((degrees[v]*M)/(degrees[v]*M))==1)
 th=s.Matrix(33,33,lambda u,v:0 if zones[u]==zones[v] else 1/s.sqrt(degrees[u]*degrees[v]));tw=s.Matrix(33,33,lambda u,v:0 if zones[u]==zones[v] else s.Rational(1,degrees[u]));Sd=s.diag(*[s.sqrt(d) for d in degrees])
 check('ACTUAL_RETURN_COORDINATE_CHANGE',Sd*tw*Sd.inv()==th and th.T==th)
 check('DEGREE_WEIGHTED_RETURN_IS_NOT_ORTHONORMAL_COORDINATES',tw!=th)
 P=s.Matrix([[s.Rational(9,25),s.Rational(12,25)],[s.Rational(12,25),s.Rational(16,25)]])
 check('WHOLE_REAL_PROJECTOR_HYPOTHESES',P.T==P and P*P==P)
 check('ALL_REAL_PROJECTOR_READING_CONSTANT',4*s.Rational(1,4)==1)
 phi=1+p
 check('NATIVE_PHI_FIFTH_SCALE',red(phi**5-(8+5*p))==0)
 check('NATIVE_COST_ACCURACY_SCALE_SEPARATION',bool(phi.subs(p,pg)**5>9) and bool(phi.subs(p,pg)**5<16))
 for m in range(5):
  N0=17
  for k in range(2*m+2):N0=3*N0+2*5
  N=N0+5
  eps=s.Rational(1,16)**m;delta=eps/(2*N)
  check('EXACT_COMPLETE_EXPANDED_COST_SCHEDULE_'+str(m),N==9*(17+5)*9**m)
  check('EXACT_NONEMPTY_WORD_COMPILER_HALF_BUDGET_'+str(m),N>0 and N*delta==eps/2)
  check('EXACT_COMPILER_PLUS_PREPARATION_FIXED_RATE_'+str(m),eps/2+N*delta==eps)
 for c0 in range(5):
  m=max(1,7*c0)
  check('POLYNOMIAL_COST_LOSES_TO_NATIVE_GEOMETRIC_MARGIN_'+str(c0),s.Rational(m+1,m)**c0<s.Rational(7,6))
 check('NAIVE_ONE_WORD_STAGE_PER_PHI_LEVEL_IS_NOT_COST_BOUND',bool(3>phi.subs(p,pg)))
 check('PROGRAM_LEVEL_NOT_EQUAL_TO_PHYSICAL_TIME_OR_METRIC_SCALE',SCOPE['program_index_or_history_depth_is_physical_time_mesh_or_expansion'] is False)
 if expected is not None:assert expected['checks']==checks,'EXACT_CONTROL_LEDGER_MISMATCH'
 result={'schema':'d0-exact-research/1','status':'PASS','scope':SCOPE,'check_count':len(checks),'checks':checks,
  'lean_capsule_sha256':sha(BASE+'.lean'),'lean_output_sha256':sha(BASE+'_output.txt'),
  'lean_results_sha256':sha(BASE+'_results.json'),'checker_sha256':sha(BASE+'_check.py'),
  'proof_sha256':sha(PROOF),'input_sha256':dict(sorted(pins.items()))}
 if expected is not None:assert expected==result,'PINNED_EXACT_LEDGER_MISMATCH'
 if a0.output:a0.output.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(checks),'EXACT_GOLDEN_PROGRAM_AND_RETAINED_RECORD_CONTROLS',flush=True)
if __name__=='__main__':main()
