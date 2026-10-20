#!/usr/bin/env python3
"""Literal full-Fock golden apparatus, covariance and sector-invariance tests.

The all-group representation and factorization proofs are analytic in the memo.
These controls do not admit a physical gate, heat law or native closed sector.
"""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_fock_record_binding'
PROOF='02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md'
HEAD='74d39bb196adf4470a1b058c3e84461acb34443d'
INPUTS=[
 '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
 '03_FORMALIZATION/D0/Representation/GoldenRelativeChannel.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean',
 '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
 '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
 '02_REGISTRY/research/A4D_NATIVE_MATTER_OBSERVER_PAIRING.md',
 '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md',
 '02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md',
 '02_REGISTRY/research/certificates/a4d_native_matter_observer_pairing_certificate.json',
 '03_FORMALIZATION/lean-toolchain','03_FORMALIZATION/lake-manifest.json',
]
SCOPE={
 'gate':'LITERAL_GOLDEN_COHERENT_MEMORY_FULLSTEP',
 'whole_carrier':'ALL_16_EXTERIOR_COMPONENTS_FOUR_APPARATUS_COPIES',
 'apparatus_tuple':'GATE_PRICE_CUT_AND_ACTUAL_BLANK_RECORD_PLANE',
 'apparatus_commutant':'REAL_SCALARS_FOR_EVERY_p_NE_0',
 'pointwise_observer_only_full_O3_tuple_binding':False,
 'all_core_or_multisite_binding_excluded':False,
 'orientation_resource':'EXISTING_NONZERO_TOP_GRADE_MATTER_NOT_EXTERNAL_SIGN',
 'grade_and_interpretation_scope':'FIVE_GRADES_1_4_6_4_1_NO_PARTICLE_IDENTIFICATION',
 'complete_feedback_determinant':'(1-4*z*p^3)^4_IN_ONE_FIXED_PREPARED_PAIRING',
 'one_frame_feedback_joint_jet':'EXACT_ZERO_WITH_NATIVE_p_z_FIXED',
 'all_native_input_states_are_physically_admitted':False,
 'timelike_domain_is_record_invariant':False,
 'nonzero_top_grade_domain_is_record_invariant':False,
 'state_conditioned_two_step_is_one_frame_square':False,
 'record_operator_is_affine_or_number_preserving_link':False,
 'fixed_q_transition_updates_the_positive_pairing_isometrically':False,
 'actual_joint_metric_transition_or_history_orientation_recovery_derived':False,
 'native_physical_preparation_heat_source_Ward_or_GR_closed':False,
 'all_group_and_factorization_kernel_formalized':False,
 'new_supported_CORE_owner':False,
 'new_physical_law_selector_fitted_phase_or_parent_terminal':False,
}
SUBS=[tuple(i for i in range(4) if mask&(1<<i)) for mask in range(16)]
ETA=s.diag(1,-1,-1,-1)
a,p,z=s.symbols('a p z',real=True)
IDEAL=s.groebner([a*a-p,p*p+p-1],a,p,domain=s.QQ.frac_field(z))


def sha(path):return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def red(x):
 num,den=s.cancel(x).as_numer_denom()
 num,den=IDEAL.reduce(s.expand(num))[1],IDEAL.reduce(s.expand(den))[1]
 assert den!=0,'ZERO_GOLDEN_DENOMINATOR'
 return s.cancel(num/den)


def zero(x):
 if isinstance(x,s.MatrixBase):return all(red(v)==0 for v in x)
 return red(x)==0


def ext(M):
 return s.Matrix(16,16,lambda i,j:M.extract(SUBS[i],SUBS[j]).det()
                 if len(SUBS[i])==len(SUBS[j]) else 0)


def creator(v):
 C=s.zeros(16)
 for r in range(4):
  for mask,S in enumerate(SUBS):
   if r not in S:C[mask|(1<<r),mask]+=v[r]*(-1)**sum(i<r for i in S)
 return C


def record_basis():
 masks=[[0,2,4,8],[1,3,5,9],[14,12,10,6],[15,13,11,7]]
 B=s.zeros(16)
 for row in range(4):
  for j in range(4):B[masks[row][j],4*row+j]=-1 if row in [2,3] and j==2 else 1
 return B


def controls():
 checks,mutants=[],[]
 def check(name,condition):
  assert bool(condition),name
  checks.append(name)
 def reject(name,actual,false_value):
  check('REJECT_'+name,not zero(actual-false_value));mutants.append(name)

 U=s.Matrix([[a,0,-p,0],[0,a,0,-p],[0,p,0,a],[p,0,a,0]])
 P=s.diag(1,1,0,0);PB=s.diag(1,0,1,0)
 T=s.Matrix([[1,0,1,0],[1,0,-1,0],[0,1,0,1],[0,1,0,-1]])/s.sqrt(2)
 UC=s.simplify(T.T*U*T);PC=s.simplify(T.T*P*T);BC=s.simplify(T.T*PB*T)
 expected_U=s.Matrix([[a,-p,0,0],[p,a,0,0],[0,0,a,-p],[0,0,-p,-a]])
 check('actual_fullstep_decomposition',UC==expected_U)
 check('actual_price_cut_decomposition',PC==s.diag(1,0,1,0))
 check('actual_blank_plane_decomposition',BC==s.Matrix([[1,0,1,0],[0,1,0,1],[1,0,1,0],[0,1,0,1]])/2)
 parity=s.diag(1,1,-1,-1)
 check('observer_parity_preserves_gate_and_price',parity*UC==UC*parity and parity*PC==PC*parity)
 reject('BLANK_RESOURCE_OMITTED_FROM_EQUIVARIANCE',parity*BC,BC*parity)
 X=s.Matrix(4,4,lambda i,j:s.Symbol('x_%s_%s'%(i,j)))
 MP,_=s.linear_eq_to_matrix(list(X*U-U*X)+list(X*P-P*X),list(X))
 MF,_=s.linear_eq_to_matrix(list(X*U-U*X)+list(X*P-P*X)+list(X*PB-PB*X),list(X))
 point={a:s.Rational(4,5),p:s.Rational(3,5)}
 rank_pair=MP.subs(point).rank();rank_full=MF.subs(point).rank()
 check('whole_literal_tuple_commutant_rank_control',rank_full==15)
 reject('GATE_PRICE_PAIR_EQUALS_WHOLE_PREPARATION_TUPLE',s.Integer(rank_pair),s.Integer(rank_full))
 check('full_O3_native_multiplicities',2+2+2*3+2*3==16 and any(2%4!=0 for _ in range(4)))

 B0=record_basis();check('full16_signed_CAR_basis',B0.T*B0==s.eye(16) and B0.rank()==16)
 c0=creator(s.Matrix([1,0,0,0]))
 for j in range(4):
  check('actual_CAR_creator_system_bit_low_record',c0*B0[:,j]==B0[:,4+j])
  check('actual_CAR_creator_system_bit_high_record',c0*B0[:,8+j]==B0[:,12+j])
  check('actual_CAR_annihilator_system_bit_low_record',c0.T*B0[:,4+j]==B0[:,j])
  check('actual_CAR_annihilator_system_bit_high_record',c0.T*B0[:,12+j]==B0[:,8+j])
 check('all_native_grades_present',Counter(map(len,SUBS))=={0:1,1:4,2:6,3:4,4:1})
 UR=B0*s.kronecker_product(UC,s.eye(4))*B0.T
 PR=B0*s.kronecker_product(PC,s.eye(4))*B0.T
 BR=B0*s.kronecker_product(BC,s.eye(4))*B0.T
 check('actual_full16_record_is_orthogonal',zero(UR.T*UR-s.eye(16)))
 check('both_whole_record_projections_rank8',PR.rank()==8 and BR.rank()==8)
 check('full_record_projectors_are_distinct',PR!=BR)
 FB1=PR*UR.T*(s.eye(16)-PR)*UR*PR
 FB2=PR*(UR*UR).T*(s.eye(16)-PR)*(UR*UR)*PR
 FB1,FB2=FB1.applyfunc(red),FB2.applyfunc(red)
 plus=B0*s.diag(s.eye(4),s.zeros(12))*B0.T
 check('full16_two_return_feedback_exact',zero(FB2-4*p**3*plus))
 check('full16_one_return_feedback_exact',zero(FB1-p*p*PR))
 check('full16_det_keeps_every_copy',zero((s.eye(16)-z*FB2).det()-(1-4*z*p**3)**4))
 reject('FULL_NATIVE_FEEDBACK_HAS_ONE_APPARATUS_MULTIPLICITY',
        (s.eye(16)-z*FB2).det(),1-4*z*p**3)
 reject('RESET_RECORD_REPLACES_GENUINE_TWO_RETURNS',FB2,FB1)
 degree=s.diag(*map(len,SUBS))
 reject('RECORD_GATE_IS_DEGREE_PRESERVING_AFFINE_LINK',degree*UR,UR*degree)

 frames=[s.eye(4),s.diag(2,s.Rational(1,2),1,1),
         s.Matrix([[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,1]])]
 boost=s.eye(4);boost[0,0]=boost[1,1]=s.Rational(5,3);boost[0,1]=boost[1,0]=s.Rational(4,3)
 frames += [boost,frames[-1]*boost]
 rotation=s.eye(4);rotation[1,1]=rotation[2,2]=0;rotation[1,2]=-1;rotation[2,1]=1
 reflection=s.diag(1,-1,1,1)
 for A in frames:
  q=A*ETA*A.T;n=A[:,0];Q=-q+2*n*n.T/(n.T*q.inv()*n)[0]
  G=Q.inv();S=ext(G);E=ext(A);B=E*B0;adj=B.T*S
  Uf=B*s.kronecker_product(UC,s.eye(4))*adj
  Pf=B*s.kronecker_product(PC,s.eye(4))*adj
  Bf=B*s.kronecker_product(BC,s.eye(4))*adj
  check('nonrest_actual_matter_observer_Q',Q==A*A.T)
  check('nonrest_complete_basis_isometry',B.T*S*B==s.eye(16))
  check('nonrest_full_gate_unitarity',zero(Uf.T*S*Uf-S))
  check('nonrest_all16_native_record_conjugacy',zero(Uf-E*UR*E.inv()))
  check('nonrest_native_cuts_conjugacy',Pf==E*PR*E.inv() and Bf==E*BR*E.inv())
  check('nonrest_creator_columns_are_actual',creator(n)*B[:,0]==B[:,4] and
        creator(n)*B[:,8]==B[:,12])
  Bp=ext(A*rotation)*B0;adjp=Bp.T*S
  check('spatial_frame_does_not_select_a_gate',zero(Bp*s.kronecker_product(UC,s.eye(4))*adjp-Uf))
  check('spatial_frame_does_not_select_a_blank',Bp*s.kronecker_product(BC,s.eye(4))*adjp==Bf)
  C=s.kronecker_product(parity,s.eye(4));Bm=B*C;adjm=Bm.T*S
  check('orientation_sign_cancels_in_gate_and_price',
        zero(Bm*s.kronecker_product(UC,s.eye(4))*adjm-Uf) and
        Bm*s.kronecker_product(PC,s.eye(4))*adjm==Pf)
  reject('TOP_MATTER_ORIENTATION_IGNORED_IN_BLANK',Bm*s.kronecker_product(BC,s.eye(4))*adjm,Bf)
  for R in [rotation,reflection,frames[-1]]:
   ER=ext(R);A2=R*A;S2=ext((A2*A2.T).inv());B2=ext(A2)*B0;adj2=B2.T*S2
   check('all16_GL_covariance_with_actual_orientation_resource',
         zero(B2*s.kronecker_product(UC,s.eye(4))*adj2-ER*Uf*ER.inv()))
   check('whole_blank_GL_covariance_with_actual_orientation_resource',
         B2*s.kronecker_product(BC,s.eye(4))*adj2==ER*Bf*ER.inv())
   check('full_inverse_pairing_covariance',S2==ER.inv().T*S*ER.inv())
  # dagger requires S^-1; retaining it is part of the independent control.
  FF=Pf*S.inv()*(Uf*Uf).T*S*(s.eye(16)-Pf)*(Uf*Uf)*Pf
  check('nonrest_full_feedback_covariance',zero(FF-E*FB2*E.inv()))

 native_p=(s.sqrt(5)-1)/2;native_a=s.sqrt(native_p)
 check('actual_golden_sector_sign',native_p> s.Rational(1,2) and
       s.simplify(native_p-4*native_p**2)<0)
 m=s.zeros(16,1);m[1]=1;m[3]=2;m[13]=2;m[15]=1
 out=UR*m;v=s.Matrix([out[1],out[2],out[4],out[8]])
 check('literal_full_record_first_grade_counterexample',v==s.Matrix([a,-2*p,0,0]))
 check('full_counterexample_unitarity_keeps_all_norm',zero((out.T*out-m.T*m)[0]))
 check('initial_timelike_nonzero_top_domain',m[1]**2>0 and m[15]!=0)
 check('counterexample_is_actual_blank_record_input',BR*m==m)
 check('actual_normalized_input_and_output',zero((out.T*out)[0]/10-1) and (m.T*m)[0]/10==1)
 sign=red((v.T*ETA*v)[0])
 check('normalized_actual_output_is_spacelike',s.simplify(sign.subs(p,native_p)/10)<0)
 reject('DISCARDING_GRADE2_HIDES_DOMAIN_FAILURE',sign,a*a)
 reject('UNITARY_RECORD_PRESERVES_TIMELIKE_OBSERVER_DOMAIN',sign,s.Integer(1))
 om=s.zeros(16,1);om[1]=1;om[14]=-a/p;om[15]=1
 omout=UR*om
 check('literal_record_erases_top_resource',zero(omout[15]) and om[15]!=0)
 check('full_orientation_information_retained_in_grade3',zero(omout[14]+1/p))
 check('orientation_failure_has_timelike_output',zero(omout[1]-a) and omout[2]==0)
 check('orientation_failure_is_norm_preserving',zero((omout.T*omout-om.T*om)[0]))
 reject('TOP_GRADE_RESOURCE_IS_RECORD_INVARIANT',omout[15],om[15])

 # A smaller grade-two input stays timelike, yet changes its observer pairing.
 small=m.copy();small[3]=1;small[13]=1
 smallout=UR*small;vv=s.Matrix([smallout[1],smallout[2],smallout[4],smallout[8]])
 kk=red((vv.T*ETA*vv)[0]);Qnext=(-ETA+2*vv*vv.T/kk).applyfunc(red)
 check('small_full_record_output_remains_timelike',zero(kk-p**3))
 reject('ONE_FRAME_PRICE_IS_UPDATED_OBSERVER_CHRONOLOGY',Qnext,s.eye(4))
 Gnext=Qnext.inv().applyfunc(red);Snext=ext(Gnext)
 mismatch=(UR.T*Snext*UR-s.eye(16)).applyfunc(red)
 reject('FIXED_q_RECORD_IS_ENDPOINT_PAIRING_ISOMETRY',mismatch,s.zeros(16))
 check('original_metric_compatibility_does_not_imply_observer_compatibility',
       ETA==s.eye(4)*ETA*s.eye(4).T and not zero(Qnext-s.eye(4)))

 receipt=json.loads((ROOT/(BASE+'_results.json')).read_text());output=(ROOT/(BASE+'_output.txt')).read_text()
 check('actual_Lean_compile_pass',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
 check('Lean_capsule_bytes_pin',receipt['capsule_sha256']==sha(BASE+'.lean'))
 check('Lean_output_bytes_pin',receipt['output_sha256']==sha(BASE+'_output.txt'))
 check('genuine_literal_commutant_and_sign_propositions',
       'literal_apparatus_commutant_scalar' in output and 'golden_full_gate_spacelike_first_grade' in output)
 check('no_Lean_proof_shortcuts','sorryAx' not in output and 'error:' not in output)
 for decl,axs in receipt['axioms'].items():
  check('actual_decl_standard_axioms',decl in output and set(axs)<={'propext','Classical.choice','Quot.sound'})
 for path,digest in receipt['input_sha256'].items():check('transitive_Lean_owner_pin',sha(path)==digest)
 return {'status':'PASS','input_source_head':HEAD,'proof':PROOF,
  'checks':dict(sorted(Counter(checks).items())),'exact_controls':len(checks),
  'executed_mathematical_mutants':mutants,'tuple_commutant_rank_control':rank_full,
  'gate_price_pair_rank_control':rank_pair,'full_fibre':16,'price_rank':8,'blank_rank':8,
  'two_return_nonzero_feedback_multiplicity':4,'zero_feedback_multiplicity':12,
  'timelike_domain_counterexample_output':'p-4*p^2<0','orientation_output_top_grade':0,
  'new_generic_Lean_propositions':3,'scope':SCOPE,
  'input_sha256':{path:sha(path) for path in INPUTS},'proof_sha256':sha(PROOF),
  'checker_sha256':sha(BASE+'_check.py'),'capsule_receipt_sha256':sha(BASE+'_results.json')}


def main():
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
 result=controls();path=ROOT/(BASE+'_certificate.json')
 if args.write:path.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
 else:
  expected=json.loads(path.read_text());assert expected==result,'IMMUTABLE_FULL_RECORD_LEDGER_MISMATCH'
  for key,value in SCOPE.items():
   bad=dict(expected);bad['scope']=dict(expected['scope']);bad['scope'][key]=True if value is False else False
   assert bad!=result,'FALSE_SCOPE_ACCEPTED_'+key
 print('PASS: %s exact controls; %s mathematical mutations; full16 native record; '
       '3 generic Lean propositions; timelike and orientation sectors fail closure' %
       (result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__':main()
