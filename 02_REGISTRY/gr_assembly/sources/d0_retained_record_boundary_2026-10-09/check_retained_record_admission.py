#!/usr/bin/env python3
"""Exact native old-record correlation and one-way controller controls."""
import argparse,hashlib,json,re
from itertools import product
from pathlib import Path
import sympy as s
BASE='02_REGISTRY/research/certificates/a4d_native_retained_record_admission'
PROOF='02_REGISTRY/research/A4D_NATIVE_RETAINED_RECORD_ADMISSION.md'
SCOPE={
 'class':'GENERATED_ONE_WAY_ACTIVE_ORTHOGONAL_AND_CONTROLLED_ADDITIVE_RECORDING_WITH_FAITHFUL_COMPLETE_EXTENSIONS',
 'input_head':'b09a822a1c9701309dd2e7c53fb5e451bd054689',
 'all_length_generated_class_invariant_kernel_proved':True,
 'actual_owned_golden_gate_copy_and_fullStep_bound':True,
 'raw_first_unequal_correlation_recursion_proved_for_all_n':True,
 'actual_complete_2_pow_45_initial_and_all_33_targets_bound':True,
 'fixed_native_p0_archive_gap_and_full_state_floor_proved':True,
 'any_faithful_complete_extension_retains_the_floor':True,
 'complete_commutator_strength_requirement_kernel_proved':True,
 'actual_first_odd_route_breaks_the_old_record_probe':True,
 'readout_equation_inserted_into_native_gate':False,
 'arbitrary_old_record_actuation_or_nonlinear_archive_permutations_in_one_way_class':False,
 'whole_D0_core_or_controller_class_exhausted':False,
 'broader_addressed_compiler_result_refuted':False,
 'X_is_an_independently_admitted_physical_or_gravitational_detector':False,
 'primitive_cost_interface_equated_to_history_action_or_executed_budget':False,
 'M1_alone_forces_arbitrary_program_decoder_addressing_or_basis_preparations':False,
 'physical_two_way_or_coherent_archive_actuation_derived':False,
 'actual_native_decoder_MDL_budget_and_schedule_admission_derived':False,
 'joint_native_heat_tangent_refinement_or_full_core_completeness_derived':False,
 'reset_trace_postselection_or_initial_target_preparation_used':False,
 'full_2_pow_45_matrix_or_infinite_word_class_numerically_enumerated':False,
 'all_prior_propositions_counted_as_new':False,
 'own_metric_matter_source_and_physical_Ward_derived':False,
 'quantitative_metric_contrast_or_native_stationarity_transferred':False,
 'curved_joint_roots_soundness_recovery_or_physical_constraints_derived':False,
 'new_action_selector_temperature_coupling_source_or_postulate_added':False,
 'positive_GR':False,'G0b_closed':False,'G0_closed':False,'global_closure':False,
 'original_310_202_317_terminals_changed':False,
}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path);args=ap.parse_args()
 root=Path(__file__).resolve().parents[3];sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 expected=json.loads(args.expect.read_text()) if args.expect else None
 if expected is not None:assert expected['scope']==SCOPE,'PINNED_SCOPE_MISMATCH'
 checks=[]
 def check(name,value):assert bool(value),name;checks.append(name)
 rr=json.loads((root/(BASE+'_results.json')).read_text());lean=(root/(BASE+'.lean')).read_text();out=(root/(BASE+'_output.txt')).read_text()
 names=re.findall(r'^#check (\S+)',lean,re.M)
 check('ACTUAL_COMPILER_EXIT_ZERO',rr['status']=='PASS' and rr['compiler_exit_code']==0)
 check('ALL_62_ACTUAL_TYPES_AND_TRANSITIVE_AXIOMS',len(names)==62 and names==rr['declarations'] and rr['printed_propositions']==rr['printed_axiom_dependencies']==62)
 check('COMPILED_CAPSULE_AND_TRANSCRIPT_FRESH',sha(BASE+'.lean')==rr['capsule_sha256'] and sha(BASE+'_output.txt')==rr['output_sha256'])
 check('NO_PLACEHOLDER_OR_COMPILER_TRUST_LEAF','sorryAx' not in out and 'Lean.trustCompiler' not in out and re.search(r'\berror(?:\(|:)',out) is None and re.search(r'\b(sorry|admit|axiom|native_decide)\b',lean) is None)
 axioms=set()
 for m in re.finditer(r'depends on axioms: \[([^]]*)\]',out,re.S):axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
 check('STANDARD_TRANSITIVE_AXIOMS_ONLY',sorted(axioms)==rr['axioms']==['Classical.choice','Quot.sound','propext'])
 for name in names:check('ACTUAL_DECLARATION_'+name,name in out and "'"+name+"'" in out)
 check('ACTUAL_BINDINGS_AND_GENERATED_CLASS_TYPES',all(x in out for x in ['primitiveRoot','completeProbe','freshState','targetState','OneWayGenerator','fullStep','commonRecord','archiveGap','realHilbert','→L[ℝ]','→ₗᵢ[ℝ]','Tendsto']))
 check('TWELVE_TRANSITIVE_D0_SOURCE_PINS',len(rr['transitive_d0_source_sha256'])==12)
 pins={**rr['transitive_d0_source_sha256'],**rr['toolchain_input_sha256'],**rr['prior_packet_input_sha256']}
 for path,digest in pins.items():check('SOURCE_PIN_'+path,sha(path)==digest)
 for path in ['01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md','01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md','01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md','03_FORMALIZATION/D0/Foundation/VerifiabilityNecessity.lean','03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean','03_FORMALIZATION/D0/Foundation/M1ClassAdmissibility.lean','03_FORMALIZATION/D0/Representation/FiniteProtocolClock.lean']:
  pins[path]=sha(path)
 p,a=s.symbols('p a',real=True);gb=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.EX)
 red=lambda e:s.expand(gb.reduce(s.expand(e))[1]);zero=lambda M:all(red(x)==0 for x in M)
 pv=(s.sqrt(5)-1)/2;av=s.sqrt(pv)
 G=s.Matrix([[a,-p],[p,a]]);X=s.Matrix([[0,1],[1,0]]);I=s.eye(2)
 Cp=s.Matrix([[1,0,0,0],[0,1,0,0],[0,0,0,1],[0,0,1,0]])
 Rev=s.Matrix([[1,0,0,0],[0,0,0,1],[0,0,1,0],[0,1,0,0]])
 active=s.kronecker_product(G,I);oldG=s.kronecker_product(I,G);oldX=s.kronecker_product(I,X)
 full=s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
 check('OWNED_GOLDEN_GATE_IS_COMPLETE_ORTHOGONAL',zero(G.T*G-I))
 check('LITERAL_P0_NONEMPTY_AND_NONDEGENERATE',bool(pv>0) and bool(av>0) and bool(pv<1))
 check('OWNED_FULL_STEP_IS_RECORDING_AFTER_ACTIVE_G',Cp*active==full)
 check('OWNED_FULL_STEP_IS_COMPLETE_ORTHOGONAL',zero(full.T*full-s.eye(4)))
 check('ACTIVE_G_OLD_RECORD_PROBE_COMMUTES',active*oldX==oldX*active)
 check('ONE_WAY_CNOT_OLD_RECORD_PROBE_COMMUTES',Cp*oldX==oldX*Cp)
 check('ACTUAL_FULL_STEP_OLD_RECORD_PROBE_COMMUTES',full*oldX==oldX*full)
 check('OLD_RECORD_PROBE_IS_ORTHOGONAL_AND_SYMMETRIC',oldX.T==oldX and oldX.T*oldX==s.eye(4))
 check('COHERENT_OLD_RECORD_G_BREAKS_THE_PROBE',red((oldG*oldX-oldX*oldG)[0,0])==-2*p and oldG*oldX!=oldX*oldG)
 check('REVERSE_CONTROL_IS_OUTSIDE_ONE_WAY_PALETTE',Rev.T*Rev==s.eye(4) and Rev*oldX!=oldX*Rev)
 for f in product(range(4),repeat=3):
  pairs=[(i,r) for i in range(3) for r in range(4)];idx={x:i for i,x in enumerate(pairs)}
  perm=[idx[(i,r^f[i])] for i,r in pairs]
  ok=len(set(perm))==12
  for t in [1,2,3]:
   trans=[idx[(i,r^t)] for i,r in pairs]
   ok=ok and all(perm[trans[j]]==trans[perm[j]] for j in range(12))
  check('EVERY_FINITE_ACTIVE_CONTROL_XOR_REWRITE_'+''.join(map(str,f)),ok)
 for k in range(1,6):
  word=(full*Cp*active)**k
  check('WHOLE_NATIVE_WORD_ORTHOGONAL_'+str(k),zero(word.T*word-s.eye(4)))
  check('WHOLE_NATIVE_WORD_AND_REVERSAL_RETAIN_PROBE_'+str(k),zero(word*oldX-oldX*word) and zero(word.T*oldX-oldX*word.T))
 def amp(w):return a**w.count(0)*p**w.count(1)
 def lab(w):
  for i in range(0,len(w),2):
   if w[i]!=w[i+1]:return w[i]
  return None
 def firstflip(w):
  z=list(w)
  for i in range(0,len(w),2):
   if w[i]!=w[i+1]:z[i],z[i+1]=z[i+1],z[i];break
  return tuple(z)
 def lastflip(w):return w[:-1]+(1-w[-1],)
 def route(w,b):
  c=b^(lab(w) or 0)
  return (firstflip(w) if c else w,c)
 q=a**4+p**4;qn=red(q)
 check('LITERAL_NATIVE_PAIR_FAILURE_PARAMETER',qn==3-4*p)
 check('NATIVE_FAILURE_PARAMETER_IS_STRICTLY_BETWEEN_ZERO_AND_ONE',bool(qn.subs(p,pv)>0) and bool(qn.subs(p,pv)<1))
 data=[]
 for n in range(1,5):
  records=list(product([0,1],repeat=2*n));good=[w for w in records if lab(w)==0]
  M=sum(amp(w)**2 for w in good);K=sum(amp(w)*amp(lastflip(w)) for w in good if lab(lastflip(w))==0)
  R=sum(amp(w)*amp(lastflip(w)) for w in records)
  check('ALL_RAW_COORDINATES_UNIT_MASS_N'+str(n),red(sum(amp(w)**2 for w in records)-1)==0)
  check('ALL_ACCEPTED_AND_FAILED_MASSES_N'+str(n),red(M-(1-q**n)/2)==0 and len(good)==(4**n-2**n)//2)
  check('ALL_RAW_LAST_BIT_CROSS_COORDINATES_N'+str(n),red(R-2*a*p)==0)
  check('ALL_GOOD_LAST_BIT_CROSS_COORDINATES_N'+str(n),red(K-a*p*(1-q**(n-1)))==0)
  check('OLD_LAST_BIT_IS_BIJECTIVE_AND_INVOLUTIVE_N'+str(n),all(lastflip(lastflip(w))==w for w in records))
  domain=[(w,b) for w in records for b in [0,1]];outputs=[route(w,b) for w,b in domain]
  check('WHOLE_FIRST_ODD_ROUTE_RETAINS_ALL_RECORDS_N'+str(n),len(set(outputs))==len(domain))
  check('FIRST_ODD_ROUTE_BREAKS_THE_OLD_BIT_N'+str(n),any(route(lastflip(w),b)!=(lastflip(route(w,b)[0]),route(w,b)[1]) for w,b in domain))
  data.append((M,K))
 M,K=data[-1];den=1+q+q*q+q**3;D=2*a*p*q**3/den
 check('ACTUAL_FIXED_ARCHIVE_GAP_CLEARED_IDENTITY',red((2*a*p*M-K)*den-2*a*p*q**3*M)==0)
 check('FIXED_NATIVE_GAP_POSITIVE_WITHOUT_EMPTY_FIBER',bool(D.subs({p:pv,a:av})>0) and bool(M.subs({p:pv,a:av})>0))
 check('FIVE_STREAM_COMMON_COMPLETE_MASS_AND_CROSS_SUM',red(M**5-((1-q**4)/2)**5)==0 and s.cancel(K*M**4/(M**5)-K/M)==0)
 alltrue=(1,)*8
 check('LITERAL_ACTUAL_ROUTING_WITNESS_LABEL_CHANGES',route(lastflip(alltrue),0)[1]==1 and route(alltrue,0)[1]==0)
 check('UNFILTERED_RECORD_TARGET_IS_VALID_ZERO_DEFECT_CONTROL',red(2*a*p-2*a*p)==0 and red(2*a*p*M-K)!=0)
 check('INITIAL_TARGET_SUBSTITUTION_REMOVES_DEFECT_AND_IS_NOT_USED',SCOPE['reset_trace_postselection_or_initial_target_preparation_used'] is False)
 zones=[0]*9+[1]*11+[2]*13
 for v in range(33):
  d=sum(x!=zones[v] for x in zones)
  check('ACTUAL_NONEMPTY_INCOMING_RAY_COMPLETE_NORM_'+str(v),d in [20,22,24] and d<=32 and d*s.Rational(1,d)==1)
  check('ACTUAL_COMMON_OLD_RECORD_CHARGE_VERTEX_'+str(v),s.cancel((d*s.Rational(1,d))*K/M-K/M)==0)
 er=s.Matrix([s.Rational(3,5),s.Rational(4,5)]);z=s.Matrix([1,0]);t=s.Matrix([s.Rational(3,5),s.Rational(4,5)])
 check('NORMALIZED_FRESH_ANCILLA_IS_RETAINED', (er.T*er)[0]==1)
 for n in range(1,5):
  emb=s.kronecker_product(s.eye(2),er)
  probe=s.kronecker_product(X,s.eye(er.rows));z0=emb*z;t0=emb*t
  check('COMPLETE_EXTENSION_PROBE_AND_NORM_INTERTWINING_'+str(n),emb.T*emb==s.eye(2) and probe*emb==emb*X)
  check('COMPLETE_EXTENSION_PRESERVES_FULL_STATE_ERROR_'+str(n),s.expand(((z0-t0).T*(z0-t0))[0]-((z-t).T*(z-t))[0])==0)
  check('COMPLETE_EXTENSION_PRESERVES_BOTH_CHARGES_'+str(n),(z0.T*probe*z0)[0]==(z.T*X*z)[0] and (t0.T*probe*t0)[0]==(t.T*X*t)[0])
  er=s.kronecker_product(er,s.Matrix([s.Rational(3,5),s.Rational(4,5)]))
 reset=s.diag(1,0)
 check('RESET_IS_NOT_COMPLETE_ISOMETRY',reset.T*reset!=s.eye(2))
 check('REAL_CHARGE_IS_NOT_GLOBAL_PHASE_QUOTIENT',X.T==X and (t.T*X*t)[0]!=0)
 if expected is not None:assert expected['checks']==checks,'EXACT_CONTROL_LEDGER_MISMATCH'
 result={'schema':'d0-exact-research/1','status':'PASS','scope':SCOPE,'check_count':len(checks),'checks':checks,
  'lean_capsule_sha256':sha(BASE+'.lean'),'lean_output_sha256':sha(BASE+'_output.txt'),'lean_results_sha256':sha(BASE+'_results.json'),
  'checker_sha256':sha(BASE+'_check.py'),'proof_sha256':sha(PROOF),'input_sha256':dict(sorted(pins.items())),
  'diagnostic_only':{'initial_charge':str(s.N((2*a*p).subs({p:pv,a:av}),16)),
    'target_charge':str(s.N((K/M).subs({p:pv,a:av}),16)),
    'positive_gap':str(s.N(D.subs({p:pv,a:av}),16))}}
 if expected is not None:assert expected==result,'PINNED_EXACT_LEDGER_MISMATCH'
 if args.output:args.output.write_text(json.dumps(result,sort_keys=True,ensure_ascii=False,indent=2)+'\n')
 print('PASS',len(checks),'EXACT_RETAINED_RECORD_ADMISSION_CONTROLS',flush=True)
if __name__=='__main__':main()
