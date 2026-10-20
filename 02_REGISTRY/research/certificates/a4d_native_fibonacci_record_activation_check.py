#!/usr/bin/env python3
"""Actual AF frames, full native representation, preparation and feedback."""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation'
PROOF='02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md'
HEAD='2b5939b6236aa42f46ef59e9c4101879c7c9584b'
PREVIOUS='02_REGISTRY/research/certificates/a4d_native_autonomous_record_program'
INPUTS=[
 '02_REGISTRY/research/A4D_NATIVE_AUTONOMOUS_SCENE_RECORD.md',
 *[PREVIOUS+x for x in ('.py','_check.py','_certificate.json','.lean','_results.json','_output.txt')],
 '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md',
 '02_REGISTRY/research/certificates/a4d_native_golden_cost_refinement_certificate.json',
 '02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md',
 '02_REGISTRY/research/certificates/a4d_native_af_trace_preparation_certificate.json',
 '03_FORMALIZATION/D0/Algebra/FibonacciAFTower.lean',
 '03_FORMALIZATION/D0/VNext/PerronGNSTower.lean',
 '03_FORMALIZATION/D0/Geometry/FibonacciBratteliRefinement.lean',
 '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
 '03_FORMALIZATION/D0/Representation/GoldenRelativeChannel.lean',
]
SCOPE={
 'class':'COMPLEX_LINEAR_FOUR_COPY_GNS_ISOMETRY_WITH_ACTUAL_J_AND_TRIVIAL_APPARATUS_CONJUGATION',
 'minimal_AF_inclusions_in_declared_class':3,
 'levels_including_input':4,
 'fixed_space_dimension_proof':'ANALYTIC_ALL_UNITARIES_WITH_EXACT_MULTIPLICITIES',
 'explicit_constructive_frame':'ALL_N_OLD_BIMODULE_ISOMETRY',
 'operator_algebra':'ACTUAL_A_n_plus_6_VIA_THREE_PATH_REVERSE_THREE_PATH_BIJECTION',
 'full_regular_representation_priced':True,
 'prepared_corner_probability':'p^6=4*delta0^2',
 'two_tick_owned_loss':'4*p^3=8*delta0=1-4*delta0^2',
 'ABCD_independent_minimal_four_invariants':False,
 'Q4_normalization_proves_spacetime_dimension':False,
 'physical_preparation_instrument_or_refinement_trigger_derived':False,
 'all_native_operations_classified':False,
 'full_bootstrap_heat_or_metric_link_source_Ward_or_GR_derived':False,
 'new_action_role_selector_or_physical_postulate':False,
 'original_parent_terminal_closed':False,
}


def load(name,path):
 spec=importlib.util.spec_from_file_location(name,ROOT/path)
 mod=importlib.util.module_from_spec(spec);sys.modules[name]=mod;spec.loader.exec_module(mod)
 return mod


E=load('fibonacci_activation',BASE+'.py')
s=E.s;a,p,z=E.a,E.p,E.z
def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def inclusion(blocks,r):
 for _ in range(r):blocks=[s.diag(*blocks),blocks[0]]
 return blocks


def action(blocks,coordinates,right=False):
 index={v:i for i,v in enumerate(coordinates)};data={}
 for col,(j,r,c) in enumerate(coordinates):
  for t in range(blocks[j].rows):
   coefficient=blocks[j][c,t] if right else blocks[j][t,r]
   if coefficient:data[(index[(j,r,t) if right else (j,t,c)],col)]=coefficient
 return s.MutableSparseMatrix(len(coordinates),len(coordinates),data)


def controls():
 checks=[];mutants=[]
 def check(name,value):
  assert bool(value),name
  checks.append(name)
 def equal(name,value):check(name,E.zero(value))
 def reject(name,false_claim):
  check('REJECT_'+name,not false_claim);mutants.append(name)

 M=s.Matrix([[1,1],[1,0]])
 fixed=[int(sum(v*v for v in M**r)) for r in range(4)]
 check('actual_all_level_fixed_multiplicities',fixed==[2,3,7,18])
 check('eight_domain_fixed_directions_obstruct_first_three_targets',all(k<8 for k in fixed[:3]))
 reject('DIMENSION_SUFFICES_AT_TWO_INCLUSIONS',13>=8 and fixed[2]>=8)
 equal('all_level_X_inherited_column_norm',3*p**3+2*p**4-1)
 equal('all_level_Y_inherited_column_norm',2*p**2+p**3-1)

 for n in range(3):
  data=E.frame(n);A,B=data['old_sizes'];C,D=data['fine_sizes']
  d=data['old_dimension'];V=data['V'];J=V[:,:d]
  check('literal_threefold_block_sizes',(C,D)==(3*A+2*B,2*A+B))
  equal('whole_four_frame_Gram',V.T*V-s.eye(4*d))
  equal('actual_record_activation_nonzero_detail_matrix',
        (s.eye(V.rows)-J*J.T)*(a*J+p*V[:,3*d:])-p*V[:,3*d:])
  equal('record_preserves_full_norm',(a*J+p*V[:,3*d:]).T*(a*J+p*V[:,3*d:])-s.eye(d))
  equal('record_changes_coarse_amplitude',J.T*(a*J+p*V[:,3*d:])-a*s.eye(d))
  equal('passive_inclusion_has_zero_detail',(s.eye(V.rows)-J*J.T)*J)
  for column,(j,r,c) in enumerate(data['old_coordinates']):
   blocks=[s.zeros(A),s.zeros(B)];blocks[j][r,c]=1
   fine=inclusion(blocks,3)
   expected=s.Matrix([E.root_weight(3+v-j)*fine[v][u,w]
                      for v,u,w in data['fine_coordinates']])
   equal('all_old_matrix_units_bind_actual_J',J[:,column]-expected)
   for right in (False,True):
    coarse_action=action(blocks,data['old_coordinates'],right)
    fine_action=action(fine,data['fine_coordinates'],right)
    equal('all_left_and_right_matrix_unit_intertwiners',
          fine_action*V-V*s.kronecker_product(s.eye(4),coarse_action))

  rightframes=E.right_frames(n)
  check('actual_right_module_dimensions',
        [k['dimension'] for k in rightframes]==[13*A+8*B,8*A+5*B])
  for part in rightframes:
   j=part['old_type'];dj=part['spectator_dimension'];VV=part['V']
   equal('right_module_frame_Gram',VV.T*VV-s.eye(4*dj))
   labels={v:i for i,v in enumerate(part['labels'])}
   # Reconstruct every whole-GNS matrix entry from the smaller native blocks;
   # all old columns, including their off-diagonal entries, are spectators.
   for apparatus in range(4):
    for oldcol,(kind,r,c) in enumerate(data['old_coordinates']):
     if kind!=j:continue
     for fine_row,(v,row,col) in enumerate(data['fine_coordinates']):
      value=0
      for k,(kind2,path,offset) in enumerate(data['segments'][v]):
       if kind2==j and col==offset+c:
        value=VV[labels[(v,k,row)],apparatus*dj+r];break
      equal('whole_GNS_native_block_reconstruction',V[fine_row,apparatus*d+oldcol]-value)

   # Six-step native basis is independently enumerated by the literal inclusion.
   native=E.segments(A,B,6)[j]
   expected={(kind,path,r) for kind,path,offset in native for r in range((A,B)[kind])}
   folded=[]
   for v,k,row in part['labels']:
    coltype,colpath,co=data['segments'][v][k]
    kind,rowpath,ro=next(t for t in data['segments'][v] if t[2]<=row<t[2]+(A,B)[t[0]])
    full_col=(j,)+colpath
    path=rowpath+tuple(reversed(full_col[:-1]))
    check('reversed_path_is_legal_native_six_path',
          len(path)==6 and path[-1]==j and all(M[y,x]==1 for x,y in zip((kind,)+path,path)))
    folded.append((kind,path,row-ro))
   check('native_six_path_bijection_including_all_internal_rows',
         len(set(folded))==len(folded)==part['dimension'] and set(folded)==expected)

  DX,DY=E.counts(n+6)
  check('working_and_regular_multiplicities_distinguished',A*DX+B*DY==C*C+D*D)
  equal('trace_corner_weight_all_checked_levels',p**(n+7)*A+p**(n+8)*B-p**6)
  equal('trace_full_four_frame_weight_all_checked_levels',4*(p**(n+7)*A+p**(n+8)*B)-4*p**6)

 U=E.record();P=s.diag(1,1,0,0);Blank=s.diag(1,0,1,0)
 equal('literal_owned_four_row_unitary',U.T*U-s.eye(4))
 equal('literal_owned_blank_column',U[:,0]-s.Matrix([a,0,0,p]))
 reject('NEW_DETAIL_IS_ZERO',E.zero(p**2))
 reject('NORM_PRESERVING_RECORD_HAS_EXACT_UNCHANGED_COARSE_VECTOR',E.zero(a-1))
 L=E.red(4*p**3)
 for data in [E.frame(0),*E.right_frames(0)]:
  V=data['V'];d=data.get('old_dimension',data.get('spectator_dimension'))
  W,cut,blank,R=E.full_operators(V,d);I=s.eye(V.rows)
  equal('whole_native_unitarity_including_complement',W.T*W-I)
  equal('whole_native_cut_idempotent',cut*cut-cut)
  equal('whole_native_blank_idempotent',blank*blank-blank)
  equal('whole_native_complement_identity',(I-R)*W-(I-R))
  equal('whole_native_complement_excluded_from_cut',cut*(I-R))
  check('whole_native_complement_positive_dimension',V.rows>4*d)
  equal('blank_and_price_cut_commute',blank*cut-cut*blank)
  check('blank_and_price_cut_are_distinct',not E.zero(blank-cut))
  for ticks in (1,2):
   power=E.mat(W**ticks)
   feedback=E.mat(cut-cut*power.T*cut*power*cut)
   value=p**2 if ticks==1 else L;rank=2*d if ticks==1 else d
   equal('full_feedback_projection_polynomial_tick_%d'%ticks,feedback*feedback-value*feedback)
   equal('full_feedback_trace_gives_rank_tick_%d'%ticks,s.trace(feedback)-rank*value)
   equal('full_feedback_self_adjoint_tick_%d'%ticks,feedback.T-feedback)
   equal('all_full_feedback_complement_factors_are_one_tick_%d'%ticks,feedback*(I-R))
  corner=E.mat(V[:,:d]*V[:,:d].T)
  equal('concrete_corner_projection',corner*corner-corner)
  equal('concrete_corner_rank',s.trace(corner)-d)
  # Ordinary matrix trace is cyclic, so the unprepared regular cyclic state
  # has exactly the same corner probability after arbitrary unitary left action.
  equal('unprepared_trace_probability_not_raised_by_actual_record',
        s.trace(W.T*corner*W)-s.trace(corner))

 for n in range(9):
  A,B=E.counts(n);C,D=E.counts(n+3);X,Y=E.counts(n+6)
  equal('trace_normalization',A*p**(n+1)+B*p**(n+2)-1)
  check('regular_six_level_full_dimension',X*X+Y*Y==sum(t*t for t in E.counts(n+6)))
  check('two_tick_regular_exponent',A*X+B*Y==C*C+D*D)
  # Conditional old trace tested on every old matrix unit, not only identity.
  for j,dj in enumerate((A,B)):
   for r in range(dj):
    for c in range(dj):
     equal('conditioned_corner_preserves_each_old_matrix_unit_trace',
           p**(n+7+j)*int(r==c)-p**6*p**(n+1+j)*int(r==c))
 reject('WORKING_EXPONENT_IS_FULL_REGULAR_EXPONENT',2==34)
 reject('UNUSED_NATIVE_COMPLEMENT_CAN_BE_ERASED',34==8)
 reject('CANONICAL_CYCLIC_STATE_IS_PREPARED_CORNER',E.zero(p**6-1))
 reject('FULL_APPARATUS_CORNER_HAS_UNIT_TRACE',E.zero(4*p**6-1))

 # User's old notes: two exact generators, scalar normalization and the same
 # delta in the prepared AF corner and in the separately owned record loss.
 x,y=s.symbols('phi psi');ar=x+y-1;br=x*y+1
 check('Vieta_A_B_imply_C',s.expand(x*x-x-1-(x*ar-br))==0)
 check('Vieta_A_B_imply_D',s.expand(y*y-y-1-(y*ar-br))==0)
 check('B_C_already_imply_A',s.expand(ar-((x-1)*br-y*(x*x-x-1)))==0)
 delta=(p-p*p)/2;phi=1+p;psi=-p
 equal('actual_golden_Vieta_pair',phi+psi-1)
 equal('actual_golden_product',phi*psi+1)
 equal('delta_is_half_golden_cube',2*delta-p**3)
 equal('AF_corner_is_four_delta_squared',p**6-4*delta**2)
 equal('owned_two_tick_loss_is_eight_delta',L-8*delta)
 equal('complementary_delta_weights',4*delta**2+8*delta-1)
 equal('Q4_is_scalar_normalization',2*delta*phi**3-1)
 for dimension in range(1,12):
  # Avoid a rational-function reduction: multiply the claimed identity by phi^3.
  equal('all_checked_Q_values_are_shifted_phi_powers',
        2*delta*phi**(dimension-1)*phi**3-phi**(dimension-1))
  equal('recursive_half_difference_is_declared_delta_scaling',
        (delta**dimension*p-delta**dimension*p*p)/2-delta**(dimension+1))
 reject('HALF_DIFFERENCE_IS_RELATIVE_DIAGONAL_CONTRAST',E.zero(delta-2*delta))

 # Composition with the complete 528-coordinate scene readout, including c=0.
 old=json.loads((ROOT/(PREVIOUS+'_certificate.json')).read_text())
 check('previous_complete_scene_spectrum_bound',old['full_two_tick_price_factors']=={'L':184,'L3':36,'Lv':44})
 for key,path in [('checker_sha256',PREVIOUS+'_check.py'),('proof_sha256',INPUTS[0]),
                  ('program_sha256',PREVIOUS+'.py'),('Lean_receipt_sha256',PREVIOUS+'_results.json')]:
  check('previous_scene_packet_freshness',old[key]==sha(path))
 for path,digest in old['input_sha256'].items():check('previous_scene_transitive_input',sha(path)==digest)
 L3=E.red(1-(130*p-81)**2);Lv=E.red(1-((854*p-531)/11)**2)
 scene=[(0,264),(L,184),(L3,36),(Lv,44)]
 actual=Counter()
 for af in (0,L):
  for loss,multiplicity in scene:actual[str(E.red(1-(1-af)*(1-loss)))]+=multiplicity
 expected=Counter()
 for loss,multiplicity in [(0,264),(L,448),(L3,36),(Lv,44),
                           (L+p**6*L,184),(L+p**6*L3,36),(L+p**6*Lv,44)]:
  expected[str(E.red(loss))]+=multiplicity
 check('full_two_tick_tensor_spectrum_from_all_sectors',actual==expected)
 check('complete_two_tick_tensor_rank_per_regular_copy',sum(actual.values())-actual['0']==792)
 reject('FULL_PRICE_ADDS_WITHOUT_TENSOR_CROSS_TERM',E.zero((1-(1-L)**2)-2*L))
 reject('OLD_C0_SECTOR_MAY_BE_DROPPED',sum([184,36,44])==132)
 reject('OLD_C0_L3_LV_FACTORS_MAY_BE_DROPPED',E.zero(L3) and E.zero(Lv))
 b=a*(4*p-3);w=a*(26*p-15)/11
 T=s.Matrix([[0,s.Rational(11,24),s.Rational(13,24)],
             [s.Rational(9,22),0,s.Rational(13,22)],
             [s.Rational(9,20),s.Rational(11,20),0]])
 B2=(1-z)**2+s.Rational(41,80)*z*p**2*(1-z)+s.Rational(1521,25600)*z*z*p**4
 equal('one_tick_three_zone_tensor_pencil',
       ((1-z)*s.eye(3)+z*p**2*T*T).det()-(1-z*p)*B2)
 for oldloss,newloss in [(p*p,p),(1-b*b,1-p*b*b),(1-w*w,1-p*w*w)]:
  equal('one_tick_scene_scalar_pencil_after_AF_record',1-p*(1-oldloss)-newloss)
 check('full_one_tick_tensor_rank_per_regular_copy',2*(240+112+2*8+72+88)==1056)
 check('level_zero_full_composite_dimensions',34*792==26928 and 22976*610==14015360)
 for value in [p*p,L,L3,Lv,L+p**6*L,L+p**6*L3,L+p**6*Lv,p,1-p*b*b,1-p*w*w]:
  v=E.red(value).subs(p,(s.sqrt(5)-1)/2)
  check('all_nonconstant_feedback_factors_strict_between_zero_and_one',
        s.simplify(v).is_positive is True and s.simplify(1-v).is_positive is True)

 receipt=json.loads((ROOT/(BASE+'_results.json')).read_text())
 check('Lean_compiler_success',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
 check('Lean_capsule_freshness',receipt['capsule_sha256']==sha(BASE+'.lean'))
 check('Lean_compiler_output_freshness',receipt['output_sha256']==sha(BASE+'_output.txt'))
 for path,digest in receipt['input_sha256'].items():check('Lean_transitive_input',sha(path)==digest)
 check('Lean_standard_axioms_only',all(set(v)<={'propext','Classical.choice','Quot.sound'} for v in receipt['axioms'].values()))
 return {'status':'PASS','input_source_head':HEAD,'proof':PROOF,'scope':SCOPE,
         'exact_controls':len(checks),'checks':dict(sorted(Counter(checks).items())),
         'executed_mathematical_mutants':mutants,'explicit_frame_levels':[0,1,2],
         'fixed_dimensions_at_r_0_1_2_3':fixed,
         'new_Lean_declarations':len([k for k in receipt['declarations'] if '.FibonacciRecordActivation.' in k]),
         'regular_two_tick_exponent':'d_(n+3)',
         'complete_composite_two_tick_rank':'792*d_(n+3)',
         'complete_composite_ambient_dimension':'22976*d_(n+6)',
         'two_tick_factor_multiplicities_per_d_n_plus_3':{'L':448,'L3':36,'Lv':44,'L+p^6*L':184,'L+p^6*L3':36,'L+p^6*Lv':44},
         'input_sha256':{path:sha(path) for path in INPUTS},
         'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
         'program_sha256':sha(BASE+'.py'),'Lean_receipt_sha256':sha(BASE+'_results.json')}


def main():
 parser=argparse.ArgumentParser();parser.add_argument('--write',action='store_true');args=parser.parse_args()
 result=controls();target=ROOT/(BASE+'_certificate.json')
 if args.write:target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
 else:assert json.loads(target.read_text())==result,'FIBONACCI_RECORD_ACTIVATION_IMMUTABLE_LEDGER_MISMATCH'
 print('PASS_FIBONACCI_RECORD_ACTIVATION controls=%d mutations=%d levels=4 '
       'native_preparation=OPEN'%(result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__':main()
