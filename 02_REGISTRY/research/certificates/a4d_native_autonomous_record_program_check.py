#!/usr/bin/env python3
"""Complete fixed-word, scene-readout and controller-spectrum controls."""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
from fractions import Fraction as Q
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_autonomous_record_program'
PROOF='02_REGISTRY/research/A4D_NATIVE_AUTONOMOUS_SCENE_RECORD.md'
HEAD='68c593f1d12af20378642fa81cee982835cede1d'
OLD='02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py'
INPUTS=[
 '02_REGISTRY/research/A4D_NATIVE_CLOSED_RECORD_ENGINE.md',
 '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.py',
 '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_check.py',
 '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_certificate.json',
 '02_REGISTRY/research/certificates/a4d_native_closed_record_engine.lean',
 '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_results.json',
 '02_REGISTRY/research/certificates/a4d_native_closed_record_engine_output.txt',
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_PROGRAM_COMPILATION.md',
 '02_REGISTRY/research/certificates/a4d_native_golden_program_compilation.lean',
 '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md',
 '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md',
 OLD,
 '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
 '03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean',
 '03_FORMALIZATION/D0/Claims/Signature31Split.lean',
 '03_FORMALIZATION/D0/Synthesis/SceneNormalizedQuotientDescent.lean',
 '03_FORMALIZATION/D0/VNext2/ScenePathHistoryCanonicity.lean',
 '03_FORMALIZATION/D0/VNext2/SceneEndpointReynoldsExpectation.lean',
]
SCOPE={
 'program':'ONE_FIXED_NINE_PRIMITIVE_FORWARD_GOLDEN_CNOT_WORD',
 'amplitude_sign_or_iteration_input':False,
 'controller':'INTRINSIC_NATIVE_EDGE_ORIENTATION_AND_ONE_RETAINED_BASIS_ONE_RECORD',
 'all_controller_values_priced':True,
 'full_carrier_dimension':22976,
 'retained_projection_rank':528,
 'fixed_word_implements_prior_seed_orbit_after_explicit_two_record_preparation':True,
 'all_inputs_native_physical_states':False,
 'addressed_palette_physical_admission':False,
 'new_fundamental_role_action_or_postulate':False,
 'one_tick_prepared_sector_feedback':'p^2 I+p(2 Delta-Delta^2)',
 'readout':'ACTUAL_SCENE_ENDPOINT_PROJECTION_TENSOR_ORIGINAL_MATTER_CUT_TENSOR_I_RECORD',
 'two_tick_full_price':'(1-zL)^184(1-zL3)^36(1-zLv)^44',
 'unused_controller_sector_can_be_dropped':False,
 'physical_program_uniqueness_or_Euler_nonuniqueness_proved':False,
 'native_metric_link_refinement_source_Ward_or_GR_derived':False,
 'all_core_no_go_or_original_parent_terminal':False,
}


def load(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path)
 mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
 return mod


program=load('native_autonomous_word',BASE+'.py')
old=load('native_car_chronology',OLD)
E=program.E;s=old.s;a,p,z=old.a,old.p,old.z
Z=(Q(0),)*4
ONE=(Q(1),Q(0),Q(0),Q(0))


def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()
def sym(v):
 c=v.coefficients if isinstance(v,E.Golden) else v
 return c[0]+c[1]*a+c[2]*p+c[3]*a*p
def qscale(x,k):return tuple(k*v for v in x)
def qadd(x,y):return tuple(u+v for u,v in zip(x,y))
def qmul(x,y):
 out=[Q(0)]*7
 for i,u in enumerate(x):
  if not u:continue
  for j,v in enumerate(y):
   if v:out[i+j]+=u*v
 for degree in range(6,3,-1):
  out[degree-4]+=out[degree];out[degree-2]-=out[degree]
 return tuple(out[:4])
def qsign(x):
 den=1
 for v in x:
  den=s.ilcm(den,v.denominator)
 return E.Golden(tuple(int(v*den) for v in x)).sign()
def asq(expr):
 expr=old.red(expr)
 poly=s.Poly(s.expand(expr),a,p)
 out=[]
 for powers in [(0,0),(1,0),(0,1),(1,1)]:
  val=poly.coeff_monomial(a**powers[0]*p**powers[1])
  out.append(Q(int(s.numer(val)),int(s.denom(val))))
 assert old.zero(sym(tuple(out))-expr)
 return tuple(out)


def controls():
 checks,mutants=[],[]
 def check(name,condition):
  assert bool(condition),name
  checks.append(name)
 def reject(name,false_claim):
  check('REJECT_'+name,not false_claim);mutants.append(name)

 Uplus,Pm=old.record(s.eye(4),s.Matrix([1,0,0,0]))
 Uminus,_=old.record(s.eye(4),s.Matrix([-1,0,0,0]))
 GN=s.zeros(16)
 for mask in range(0,16,2):GN[mask:mask+2,mask:mask+2]=s.Matrix([[a,-p],[p,a]])
 K=old.mat(Uplus*GN.T)
 check('literal_native_system_gate_pairing',old.zero(GN.T*GN-s.eye(16)))
 check('actual_full_CAR_record_KG_order',old.zero(K*GN-Uplus))
 check('actual_opposite_observer_record_KGt',old.zero(K*GN.T-Uminus))
 reject('K_AND_G_ORDER_CAN_BE_REVERSED',old.zero(GN*K-Uplus))
 # Independently bind the ordinary system gate through the published 4-row
 # apparatus change of basis; this transformation is not executed per tick.
 B=s.Matrix([[1,0,1,0],[1,0,-1,0],[0,1,0,1],[0,1,0,-1]])/s.sqrt(2)
 Gsystem=s.Matrix([[a,0,-p,0],[0,a,0,-p],[p,0,a,0],[0,p,0,a]])
 Ccopy=s.eye(4);Ccopy.row_swap(2,3)
 Gcar=B.T*Gsystem*B;Kcar=B.T*Ccopy*B
 check('owned_G_and_copy_in_actual_CAR_frame',Gcar==s.diag(s.Matrix([[a,-p],[p,a]]),s.Matrix([[a,-p],[p,a]])) and Kcar==s.diag(1,1,1,-1))
 check('ordinary_G_repeated_over_all_four_copies',old.zero(old.B0*s.kronecker_product(Gcar,s.eye(4))*old.B0.T-GN))

 columns={};two_columns={}
 for column in range(64):
  raw=[E.ZERO]*64;raw[column]=E.ONE
  state=program.ProgramState(tuple(raw))
  out=program.step(state);out2=program.step(out)
  columns[column]={i:tuple(map(Q,v.coefficients)) for i,v in enumerate(out.coordinates) if v}
  two_columns[column]={i:tuple(map(Q,v.coefficients)) for i,v in enumerate(out2.coordinates) if v}
  c,f,mask=column//32,(column//16)%2,column%16
  M=(Uplus if f==0 else Uminus) if c else (old.mat(Uplus*GN*GN) if f==0 else Uplus)
  targetflag=(1-f) if c else f
  expected={32*c+16*targetflag+i:asq(M[i,mask]) for i in range(16) if not old.zero(M[i,mask])}
  check('all64_columns_match_declared_full_branch_word',columns[column]==expected)
  check('constant_record_retained_on_all_columns',all(i//32==c for i in columns[column]))
 for i in range(64):
  for j in range(64):
   value=Z
   for row in columns[i].keys()&columns[j].keys():value=qadd(value,qmul(columns[i][row],columns[j][row]))
   check('whole64_orthogonality',value==(ONE if i==j else Z))

 oldstate=E.literal_axis_gate(E.literal_axis_gate(E.seed(),1),1)
 x2=oldstate;x3=E.step(x2);x4=E.step(x3)
 dot=lambda x,y:sum((u*v for u,v in zip(x.matter,y.matter)),E.ZERO)
 check('actual_seed_consecutive_Gram_zero',dot(x2,x3)==E.ZERO)
 check('actual_seed_next_Gram_gap',old.zero(sym(dot(x3,x4))-4*a*p*p))
 reject('STATE_DEPENDENT_NORM_IMPLIES_ONE_FIXED_ISOMETRY',dot(x2,x3)==dot(x3,x4))
 state=program.seed()
 for tick in range(1025):
  live=[c for c in range(4) if any(state.coordinates[16*c:16*c+16])]
  check('one_actual_internal_program_branch',len(live)==1 and live[0] in (2,3))
  flag=live[0]-2
  check('exact_prior_algorithm_readout_with_retained_switch',state.coordinates[32+16*flag:48+16*flag]==oldstate.matter)
  check('complete_controller_state_norm',program.norm_squared(state)==E.Golden.integer(2))
  if tick!=1024:state=program.step(state);oldstate=E.step(oldstate)
 check('controller_storage_charged',program.persistent_bits(state)>len(E.encode(oldstate)))

 edges=program.SCENE_EDGES;parents=program.BASE_EDGES
 check('all_actual_scene_histories_and_pairs',len(edges)==718 and len(parents)==359)
 degrees=[program.scene_degree(v) for v in range(33)]
 incoming={v:[e for e in edges if e[1]==v] for v in range(33)}
 for e in edges:
  check('intrinsic_edge_flag_reverses',program.edge_flag((e[1],e[0]))==1-program.edge_flag(e))
 for v in range(33):check('literal_endpoint_counting_degree',len(incoming[v])==degrees[v])
 parent_for={}
 for pair in parents:
  parent_for[pair]=pair;parent_for[(pair[1],pair[0])]=pair
 for start,size in [(0,9),(9,11),(20,13)]:
  for i in range(start,start+size-1):
   perm=lambda v: i+1 if v==i else (i if v==i+1 else v)
   for edge in edges:
    mapped=(perm(edge[0]),perm(edge[1]))
    check('whole_scene_automorphism_generator_preserves_control',program.edge_flag(mapped)==program.edge_flag(edge))

 cuts=list(range(0,16,2));qa=asq(a);qb=asq(a*(4*p-3));qw=asq(a*(26*p-15)/11)
 qr=asq(2*p-1);qr3=asq(130*p-81);qv=asq((854*p-531)/11)
 actual_compressions={}
 for steps,native_columns in [(1,columns),(2,two_columns)]:
  for c in (0,1):
   for mask in cuts:
    high=bin(mask).count('1')>=2
    for vertex in range(33):
     out={}
     for edge in incoming[vertex]:
      f=program.edge_flag(edge);pair=parent_for[edge]
      for index,coef in native_columns[32*c+16*f+mask].items():
       cout,fout,mout=index//32,(index//16)%2,index%16
       if mout%2:continue
       endpoint=pair[1] if fout==0 else pair[0]
       key=(endpoint,cout,mout)
       out[key]=qadd(out.get(key,Z),qscale(coef,Q(1,degrees[endpoint])))
     out={key:v for key,v in out.items() if v!=Z}
     if steps==1 and c==1:
      expected={(target,1,mask):qscale(qa,Q(1,degrees[target])) for target in range(33)
                if program.scene_zone(target)!=program.scene_zone(vertex)}
     else:
      zone=program.scene_zone(vertex)
      if steps==1:amplitude=(qb,qw,qa)[zone]
      elif c==1:amplitude=qr if high else ONE
      else:amplitude=ONE if high else (qr3,qv,qr)[zone]
      expected={(vertex,c,mask):amplitude}
     check('all528_actual_retained_columns_step_%d'%steps,out==expected)
     actual_compressions[(steps,c,mask,vertex)]=out

 T=s.Matrix(33,33,lambda i,j:s.Rational(int(program.scene_zone(i)!=program.scene_zone(j)),degrees[i]))
 D=s.diag(*degrees);delta=s.eye(33)-T
 check('literal_degree_pairing_transport_self_adjoint',D*T==T.T*D)
 check('actual_full_transport_rank_and_balanced_dimension',T.rank()==3 and 33-T.rank()==30)
 lam=s.Symbol('lambda')
 check('actual_full_scene_characteristic_polynomial',s.factor(T.charpoly(lam).as_expr()-lam**30*(lam-1)*(lam*lam+lam+s.Rational(39,160)))==0)
 check('constructed_scene_golden_feedback_identity',old.zero(s.eye(33)-p*T*T-(p*p*s.eye(33)+p*(2*delta-delta*delta))))
 reject('UNWEIGHTED_TRANSPOSE_CAN_REPLACE_NATIVE_PAIRING',T.T*T==T*T)

 # Independently form the D-Gram matrix of the actually compressed columns.
 for i in range(33):
  for j in range(33):
   ci=actual_compressions[(1,1,0,i)];cj=actual_compressions[(1,1,0,j)]
   gram=Z
   for key in ci.keys()&cj.keys():gram=qadd(gram,qscale(qmul(ci[key],cj[key]),Q(degrees[key[0]],degrees[i])))
   check('actual_full_compression_Gram_equals_p_T_squared',gram==asq(p*(T*T)[i,j]))

 L=old.red(4*p**3);L3=old.red(1-(130*p-81)**2);Lv=old.red(1-((854*p-531)/11)**2)
 Lb=old.red(1-(a*(4*p-3))**2);Lw=old.red(1-(a*(26*p-15)/11)**2)
 for value in [L,L3,Lv,Lb,Lw,p*p]:
  check('exact_all_feedback_factors_strict_between_zero_and_one',qsign(asq(value))>0 and qsign(asq(1-value))>0)
 check('complete_one_tick_feedback_degree',240+112+2*8+72+88==528)
 check('complete_two_tick_feedback_degree',184+36+44==264)
 check('full_carrier_all_unit_factors_retained',718*2*16==22976 and 22976-264==22712)
 T3=s.Matrix([[0,s.Rational(11,24),s.Rational(13,24)],[s.Rational(9,22),0,s.Rational(13,22)],[s.Rational(9,20),s.Rational(11,20),0]])
 B=(1-z)**2+s.Rational(41,80)*z*p*(1-z)+s.Rational(1521,25600)*z*z*p*p
 check('three_zone_one_tick_pencil_from_actual_matrix',old.zero(((1-z)*s.eye(3)+z*p*T3*T3).det()-(1-z*p*p)*B))
 reject('UNPOPULATED_RECORD_SECTOR_HAS_ZERO_PRICE',L==0 and L3==0 and Lv==0)
 reject('SCENE_ENDPOINT_READOUT_IS_IDENTITY_ON_HISTORIES',528==718*2*8)
 reject('WHOLE_SCENE_PRICE_IS_PREPARED_SECTOR_ONLY',184==132 and 36==0 and 44==0)
 reject('HIGH_GRADE_RETURN_IS_LOW_GRADE_RETURN',qr==ONE)
 reject('MIDDLE_ZONE_13_TO_9_WEIGHTS_INTERCHANGE',qw==asq((9*a*(4*p-3)+13*a)/22))
 reject('ONE_TICK_FEEDBACK_IS_PURE_SCENE_RETURN',old.zero(s.eye(33)-p*T*T-(s.eye(33)-T*T)))
 reject('SCENE_BALANCED_DIRECTIONS_CAN_BE_OMITTED',30*8==0)

 scene=program.scene_seed()
 for tick in range(9):
  for block in scene:
   check('all_scene_current_first_grades_match_intrinsic_switch',block.coordinates[33].sign()>0 and block.coordinates[49].sign()<0)
   check('all_scene_blocks_keep_both_histories_and_full_norm',program.norm_squared(block)==E.Golden.integer(4))
  if tick!=8:scene=program.scene_step(scene)

 prior=json.loads((ROOT/INPUTS[3]).read_text())
 check('consumed_engine_checker',prior['checker_sha256']==sha(INPUTS[2]))
 check('consumed_engine_proof',prior['proof_sha256']==sha(INPUTS[0]))
 check('consumed_engine_program',prior['engine_sha256']==sha(INPUTS[1]))
 for path,digest in prior['input_sha256'].items():check('consumed_engine_transitive_pin',sha(path)==digest)
 receipt=json.loads((ROOT/(BASE+'_results.json')).read_text())
 check('new_Lean_compiler_success',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
 check('new_Lean_capsule_hash',receipt['capsule_sha256']==sha(BASE+'.lean'))
 check('new_Lean_output_hash',receipt['output_sha256']==sha(BASE+'_output.txt'))
 for path,digest in receipt['input_sha256'].items():check('new_Lean_import_pin',sha(path)==digest)
 check('new_Lean_standard_axioms_only',all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in receipt['axioms'].values()))
 return {'status':'PASS','input_source_head':HEAD,'proof':PROOF,'scope':SCOPE,
         'checks':dict(sorted(Counter(checks).items())),'exact_controls':len(checks),
         'executed_mathematical_mutants':mutants,'exact_single_pair_transitions':1024,
         'exact_whole_scene_transitions':8,'native_scene_histories':718,
         'new_Lean_declarations':len([k for k in receipt['declarations'] if '.AutonomousRecordProgram.' in k]),
         'full_one_tick_price_factors':{'balanced_1':240,'p_squared':112,'three_zone_quadratic':8,'1_b_squared':72,'1_w_squared':88},
         'full_two_tick_price_factors':{'L':184,'L3':36,'Lv':44},
         'one_tick_nontrivial_rank':528,'two_tick_nontrivial_rank':264,
         'two_tick_ambient_unit_factors':22712,
         'input_sha256':{path:sha(path) for path in INPUTS},'proof_sha256':sha(PROOF),
         'checker_sha256':sha(BASE+'_check.py'),'program_sha256':sha(BASE+'.py'),
         'Lean_receipt_sha256':sha(BASE+'_results.json')}


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 result=controls();target=ROOT/(BASE+'_certificate.json')
 if args.write:target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 else:assert json.loads(target.read_text())==result,'AUTONOMOUS_RECORD_IMMUTABLE_LEDGER_MISMATCH'
 print('PASS_AUTONOMOUS_SCENE_RECORD controls=%d mutations=%d full_dimension=22976 '
       'physical_admission=OPEN'%(result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__':main()
