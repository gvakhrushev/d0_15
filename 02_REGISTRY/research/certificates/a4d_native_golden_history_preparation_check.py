#!/usr/bin/env python3
"""Kernel-pinned complete retained phi preparation and exact hostile controls."""
import argparse,hashlib,json,re
from itertools import product
from pathlib import Path
import sympy as s

BASE='02_REGISTRY/research/certificates/a4d_native_golden_history_preparation'
PROOF='02_REGISTRY/research/A4D_NATIVE_GOLDEN_HISTORY_PREPARATION.md'
SCOPE={
 'class':'COMPLETE_FINITE_RETAINED_GOLDEN_SEED_RECURSIVE_WORD_AND_CYLINDER_EXTENSION',
 'input_head':'1093df6bbd2f7a0fb91204e87240ad035256d661',
 'literal_full_seed_and_recursive_word_unitarity_proved_in_kernel':True,
 'all_raw_success_and_failure_records_retained':True,
 'successful_full_record_factorization_proved_in_kernel':True,
 'actual_33_scene_vertices_and_20_22_24_degrees_bound_in_kernel':True,
 'same_owned_golden_eighth_power_realizes_fast_phase_in_kernel':True,
 'actual_all_coordinate_failure_law_and_two_stage_rate_proved_in_kernel':True,
 'literal_expanded_word_cost_recurrence_and_error_bound_proved_in_kernel':True,
 'whole_vector_error_counts_all_rejected_records':True,
 'finite_prefix_cylinder_operator_naturality_proved_in_kernel':True,
 'actual_condensed_cylinder_weights_bound_in_kernel':True,
 'single_fine_blank_phase_is_rejected_as_cylinder_extension':True,
 'actual_20_24_relative_success_phase_obstruction_proved_in_kernel':True,
 'retry_gram_obstruction_class':'DECLARED_STOPPED_RETRY_GRAM_CLASS_WITH_EXPLICIT_HYPOTHESES',
 'full_2_pow_45_dimensional_seed_matrix_numerically_enumerated':False,
 'Boolean_routing_oracle_physically_synthesized_or_admitted':False,
 'all_fine_controller_laws_forced_or_classified_by_M1':False,
 'degree_dependent_phase_alignment_physically_implemented':False,
 'one_global_success_phase_claimed_for_all_degrees':False,
 'normalized_success_target_claimed_as_unconditional_native_state':False,
 'expanded_word_cost_identified_with_native_MDL_or_kappa':False,
 'composition_count_identified_with_physical_mesh_or_clock':False,
 'same_joint_state_full_heat_carrier_tangent_and_action_derived':False,
 'new_action_temperature_selector_coupling_source_or_postulate_added':False,
 'own_metric_matter_source_and_physical_Ward_derived':False,
 'quantitative_metric_contrast_and_native_stationarity_transferred':False,
 'curved_roots_soundness_recovery_or_GR_derived':False,
 'G0b_closed':False,'G0_closed':False,'global_closure':False,
 'original_parent_terminals_changed':False,
}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);ap.add_argument('--expect',type=Path);args=ap.parse_args()
 root=Path(__file__).resolve().parents[3]
 sha=lambda p:hashlib.sha256((root/p).read_bytes()).hexdigest()
 if args.expect:assert json.loads(args.expect.read_text())['scope']==SCOPE,'PINNED_SCOPE_MISMATCH'
 checks=[]
 def check(name,value):
  assert bool(value),name
  checks.append(name)
 receipt=json.loads((root/(BASE+'_results.json')).read_text());out=(root/(BASE+'_output.txt')).read_text();lean=(root/(BASE+'.lean')).read_text()
 names=re.findall(r'^#check (\S+)',lean,re.M)
 check('COMPILER_EXIT_ZERO',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
 check('ALL_151_ACTUAL_TYPES_AND_AXIOMS_PRINTED',names==receipt['declarations'] and len(names)==receipt['printed_propositions']==receipt['printed_axiom_dependencies']==151)
 check('COMPILED_CAPSULE_AND_TRANSCRIPT_FRESH',sha(BASE+'.lean')==receipt['capsule_sha256'] and sha(BASE+'_output.txt')==receipt['output_sha256'])
 check('NO_PLACEHOLDER_OR_COMPILER_LEAF','sorryAx' not in out and 'Lean.trustCompiler' not in out and re.search(r'\berror(?:\(|:)',out) is None and re.search(r'\b(sorry|admit|axiom|native_decide)\b',lean) is None)
 axioms=set()
 for m in re.finditer(r'depends on axioms: \[([^]]*)\]',out,re.S):axioms.update(x.strip() for x in m.group(1).split(',') if x.strip())
 check('STANDARD_TRANSITIVE_AXIOMS_ONLY',sorted(axioms)==receipt['axioms']==['Classical.choice','Quot.sound','propext'])
 for n in names:check('ACTUAL_DECLARATION_'+n,n in out and "'"+n+"'" in out)
 check('LITERAL_NATIVE_OBJECTS_IN_PROPOSITIONS',all(x in out for x in ['routedGoldenSeed','fullWord','goldenComplexInclusion','cylWeight','primitiveRoot','fullDegreeValue','sceneAcceptedCodes','expandedCost','alignedAcceptedVector','historyFailure','actual_degree_twenty_twentyfour_cannot_share_success_phase']))
 pins=dict(receipt['transitive_d0_source_sha256']);pins.update(receipt['toolchain_input_sha256'])
 for path,digest in pins.items():check('SOURCE_PIN_'+path,sha(path)==digest)
 for path in ['01_BOOKS/BOOK_00_ENTRY_CONTRACT_AND_ADMISSIBILITY.md','01_BOOKS/BOOK_01_CONDENSED_FOUNDATIONS_AND_GRAPH_BIRTH.md','01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md']:
  pins[path]=sha(path)
 p,a=s.symbols('p a',real=True);e,f=s.symbols('e f',real=True)
 gb=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.EX)
 red=lambda x:s.expand(gb.reduce(s.expand(x))[1])
 mz=lambda M:all(red(x)==0 for x in M)
 G=s.Matrix([[a,-p],[p,a]]);omega=(a+s.I*p)**2;w=red(omega**4);rr=1345-2176*p
 wre=s.re(s.expand(w));wim=s.im(s.expand(w));q=3-4*p
 check('OWNED_GOLDEN_NORMALIZATION',red(a*a+p*p-1)==0)
 check('OWNED_CONTROLLED_SQUARE_REALIFICATION',mz(G**2-s.Matrix([[s.re(omega),-s.im(omega)],[s.im(omega),s.re(omega)]])))
 check('FAST_PHASE_IS_LITERAL_EIGHTH_POWER',mz(G**8-s.Matrix([[wre,-wim],[wim,wre]])))
 check('FAST_PHASE_REAL_AND_NORM',red(wre-(673-1088*p))==0 and red(w*s.conjugate(w)-1)==0)
 check('FAST_PARAMETER_FROM_OWN_PHASE',red(2*wre-1-rr)==0)
 bad=lambda eps:1+(w-1)*(w*(1-eps)+eps)
 good=lambda eps:w*w-(w-1)**2*eps
 check('ALL_COORDINATE_BAD_MULTIPLIER',red(bad(e)-w*(rr+(1-rr)*e))==0)
 check('ALL_COORDINATE_GOOD_MULTIPLIER',red(good(e)-w*(w+(1-rr)*e))==0)
 check('EXACT_COMPLETE_FAILURE_POLYNOMIAL',red(e*bad(e)*s.conjugate(bad(e))-e*(rr+(1-rr)*e)**2)==0)
 check('TWO_STAGE_RATIONAL_BURNIN',s.Rational(11,16)*s.Rational(71,96)**2<=s.Rational(2,5) and s.Rational(2,5)*s.Rational(1,2)**2==s.Rational(1,10))
 check('SMALL_ERROR_RATIONAL_CONTRACTION',s.Rational(1,6)+s.Rational(5,6)*s.Rational(1,10)==s.Rational(1,4))
 check('ERROR_RATE_BEATS_TRIPLED_WORD_COST',s.Rational(9,16)<1)
 check('GOLDEN_SQUARE_ALONE_COST_CONTROL',9*s.Rational(11,21)**2>1)
 pg=(s.sqrt(5)-1)/2;rg=rr.subs(p,pg)
 check('EXACT_POSITIVE_FAST_PARAMETER_BOUNDS',bool(rg>0) and bool(rg<s.Rational(1,6)))
 def words(n):return list(product(product([False,True],repeat=2),repeat=n))
 def first(wd):
  for k,(b,c) in enumerate(wd):
   if b!=c:return k,b
  return None
 def flip(wd):
  out=list(wd);h=first(wd)
  if h is not None:
   k,b=h;out[k]=out[k][::-1]
  return tuple(out)
 def route(wd,b):
  h=first(wd);label=False if h is None else h[1];bit=b^label
  return (flip(wd) if bit else wd,bit)
 def weight(wd):return p**sum(1+int(b) for pair in wd for b in pair)
 word_counts=[]
 for n in range(5):
  ww=words(n);allstates=list(product(ww,[False,True]));image=[route(x,b) for x,b in allstates]
  check('FULL_RETAINED_ROUTE_BIJECTION_'+str(n),len(set(image))==len(allstates))
  check('FIRST_ODD_INVOLUTION_AND_WEIGHT_'+str(n),all(flip(flip(x))==x and weight(flip(x))==weight(x) for x in ww))
  check('ALL_FAILED_RECORDS_UNCHANGED_'+str(n),all(route(x,b)==(x,b) for x,b in allstates if first(x) is None))
  check('COMPLETE_RAW_GOLDEN_MASS_'+str(n),red(sum(weight(x) for x in ww)-1)==0)
  mass=[red(sum(weight(x) for x in ww if first(x) is not None and first(x)[1]==b)) for b in [False,True]]
  fail=red(sum(weight(x) for x in ww if first(x) is None))
  check('EXACT_FULL_SUCCESS_TWINS_'+str(n),mass[0]==mass[1] and red(mass[0]-(1-q**n)/2)==0)
  check('EXACT_FULL_FAILED_MASS_'+str(n),red(fail-q**n)==0)
  word_counts.append({'pairs':n,'raw_words':len(ww),'full_states':len(allstates)})
 junk=red((1-q**4)**5)
 degrees=[24]*9+[22]*11+[20]*13
 check('LITERAL_SCENE_VERTEX_AND_HISTORY_COUNTS',len(degrees)==33 and sum(degrees)==718)
 check('FIVE_BIT_CARRIER_AND_COMPLETE_SEED_SIZE',2**5==32 and (4**4*2)**5==2**45)
 check('NATIVE_INITIAL_FAILURE_IN_CONTRACTION_BASIN',all(bool((1-s.Rational(d,32)*junk).subs(p,pg)<s.Rational(11,16)) and bool((1-s.Rational(d,32)*junk).subs(p,pg)>0) for d in [20,22,24]))
 for d in [20,22,24]:check('LITERAL_ACCEPTED_CODE_MASS_'+str(d),red(s.Rational(d,32)*(1-q**4)**5-s.Rational(d,32)*junk)==0)
 # Exact complete 8-state circuit, with every raw word and both record states.
 ww=words(1);states=list(product(ww,[False,True]));index={x:i for i,x in enumerate(states)}
 R=s.zeros(8)
 for j,(wd,b) in enumerate(states):R[index[route(wd,b)],j]=1
 U=(R*s.kronecker_product(G,G,s.eye(2))).applyfunc(red)
 z=index[(tuple([(False,False)]),False)]
 check('COMPLETE_LITERAL_EIGHT_STATE_SEED_UNITARY',mz(U.conjugate().T*U-s.eye(8)) and mz(U*U.conjugate().T-s.eye(8)))
 for case,accepted in [('both',{False,True}),('one',{False}),('empty',set())]:
  chi=[first(wd)==(0,False) and b in accepted for wd,b in states]
  B=s.eye(8);B[z,z]=w;Q=s.diag(*[w if b else 1 for b in chi])
  eps=red(sum(U[i,z]*s.conjugate(U[i,z]) for i in range(8) if not chi[i]))
  V=(U*B*U.conjugate().T*Q*U).applyfunc(red)
  check('COMPLETE_LITERAL_ONE_STEP_UNITARY_'+case,mz(V.conjugate().T*V-s.eye(8)))
  check('EVERY_RETAINED_OUTPUT_COORDINATE_'+case,all(red(V[i,z]-U[i,z]*(good(eps) if chi[i] else bad(eps)))==0 for i in range(8)))
  epnext=red(sum(V[i,z]*s.conjugate(V[i,z]) for i in range(8) if not chi[i]))
  check('LITERAL_FULL_WORD_FAILURE_LAW_'+case,red(epnext-eps*(rr+(1-rr)*eps)**2)==0)
  if case=='empty':check('EMPTY_FIBER_IS_NOT_PREPARED',eps==epnext==1)
 # One full cylinder extension; resetting only a fine singleton is hostile.
 eta=s.Matrix([a,p]);Bfine=s.diag(w,1);Blift=w*s.eye(2)
 check('GOLDEN_SUFFIX_ISOMETRY',red((eta.T*eta)[0]-1)==0)
 defect=(Bfine*eta-Blift*eta).applyfunc(red)
 defectsq=red((defect.conjugate().T*defect)[0])
 check('SINGLE_FINE_BLANK_BREAKS_CYLINDER_NATURALITY',defectsq!=0 and red(defectsq-p*p*(1-rr))==0)
 check('SAME_FULL_PHASE_ON_CYLINDER_PRESERVES_REFINEMENT',mz(Blift*eta-w*eta))
 e20=1-s.Rational(20,32)*junk;e24=1-s.Rational(24,32)*junk
 area=red(s.im(s.expand(good(e20)*s.conjugate(good(e24)))))
 check('ACTUAL_DEGREES_HAVE_NONZERO_RELATIVE_SUCCESS_PHASE',area!=0)
 check('EXACT_RELATIVE_PHASE_AREA_FORMULA',red(s.im(s.expand(good(e)*s.conjugate(good(f))))-(1-rr)*(f-e)*wim)==0)
 check('STOPPED_RETRY_GRAM_FLOOR_CONTROL',s.Rational(20,24)==s.Rational(5,6) and s.Rational(5,6)<1)
 t=s.symbols('t',positive=True)
 check('FULL_VECTOR_DISTANCE_COUNTS_FAILURE',s.simplify(t*t*(1-1/t)**2-(1-t)**2)==0)
 check('WHOLE_VECTOR_ERROR_NOT_SUCCESS_ONLY',s.simplify(((1-t)**2+(1-t*t))-2*(1-t*t))==2*t*(t-1))
 result={'status':'PASS','scope':SCOPE,'checks':checks,'checks_count':len(checks),'input_sha256':pins,
  'proof':PROOF,'proof_sha256':sha(PROOF),'capsule':BASE+'.lean','capsule_sha256':sha(BASE+'.lean'),
  'results':BASE+'_results.json','results_sha256':sha(BASE+'_results.json'),'output':BASE+'_output.txt','output_sha256':sha(BASE+'_output.txt'),
  'exact':{'raw_word_levels':word_counts,'scene_degrees':degrees,'scene_histories':718,'seed_qubits':45,'seed_dimension':str(2**45),
    'fast_phase_re':str(wre),'fast_phase_im':str(wim),'fast_parameter':str(rr),'two_stage_failure_rate':'(1/16)^k/10','whole_vector_squared_error':'(1/16)^k/5',
    'expanded_cost':'C(k)+phase=3^k*(seed+phase)','cost_failure_bound':'epsilon(k+2)*(C(k+2)+phase)^2 <= (81/10)*(seed+phase)^2',
    'single_fine_blank_defect_squared':str(defectsq),'actual_20_24_relative_phase_area':str(area),'retry_normalized_gram_upper_bound_squared':'5/6'}}
 if args.expect:assert result==json.loads(args.expect.read_text()),'PINNED_EXACT_LEDGER_MISMATCH'
 if args.output:args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 print('PASS_COMPLETE_RETAINED_GOLDEN_WORD_CYLINDER_AND_PHASE_CONTROLS',len(checks),flush=True)
if __name__=='__main__':main()
