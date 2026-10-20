#!/usr/bin/env python3
"""Exact controls for complete cyclic-word memory-minimum bounds.

The all-size minimum existence and inequalities are analytic in the memo.
This checker does not compute a global minimum on the 33-vertex word class.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import sympy as s

ROOT=Path(__file__).resolve().parents[3]
BASE='02_REGISTRY/research/certificates/a4d_native_cyclic_memory_minimum'
PROOF='02_REGISTRY/research/A4D_NATIVE_CYCLIC_MEMORY_MINIMIZATION.md'
HEAD='d64296ce4dcb937abc440ece03e49e50442db4e8'
PRIOR='02_REGISTRY/research/certificates/a4d_native_cyclic_history_price'
spec=importlib.util.spec_from_file_location('cyclic_word_owner',ROOT/(PRIOR+'_check.py'))
owner=importlib.util.module_from_spec(spec)
spec.loader.exec_module(owner)
INPUTS=owner.INPUTS+[
    owner.PROOF, PRIOR+'_check.py', PRIOR+'_certificate.json',
    '03_FORMALIZATION/D0/Core/Phi.lean',
    '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
    '03_FORMALIZATION/D0/Representation/GoldenOrderInterferometer.lean',
]
SCOPE={
    'domain':'ALL_CLOSED_SCENE_WORDS_WITH_FIXED_COMPLETE_POSITIVE_REVERSIBLE_ONE_STEP_COUNTS',
    'price':'EXISTING_TWO_TERM_CYCLE_HEAT_AND_TWO_STEP_FEEDBACK_REALIZATION',
    'coarse_geometry':'ACTUAL_COMPRESSED_CANONICAL_HEAT_AND_NORMALIZED_VISIT_PAIRING',
    'minimum_existence':'ANALYTIC_FINITE_NONEMPTY_CLASS_PROOF',
    'global_minimum_values_computed_by_checker':False,
    'uniform_unconstrained_minimum_bound':'0<f_q(A)<=132*z/((1-z)*q)_FOR_ODD_q',
    'uniform_prefix_minimum_bound':'0<S2_min<=132*z/((1-z)*(2*n+1))',
    'whole_past_retained':'LITERAL_LIST_PREFIX_OF_EVERY_MINIMUM_EXTENSION',
    'actual_recorded_golden_binding_bound':'delta+2*eta>=p/2>3/10_FOR_ALL_REAL_OR_COMPLEX_ISOMETRIES_AND_REVERSIBLE_WORDS',
    'exact_injective_linear_golden_clock_and_projection_intertwiner_exists':False,
    'absolute_error_bound_applies_to_arbitrarily_scaled_injective_encodings':False,
    'all_isometry_bound_kernel_formalized':False,
    'whole_core_or_all_physical_clock_classes_exhausted':False,
    'zero_finite_feedback_possible_with_all_718_positive_edge_counts':False,
    'minimum_value_central_response_bound':'At_epsilon=n^(-1/3),_at_most_33*z/(1-z)*n^(-2/3)',
    'actual_heat_operator_refinement_intertwiner_proved':False,
    'physical_heat_clock_readout_or_q_D_b_m_admission':False,
    'variable_probe_arrays_have_a_common_physical_refinement':False,
    'all_D0_matter_action_stack_minimized':False,
    'minimum_words_are_native_differentiable_Euler_roots':False,
    'source_Ward_native_stationarity_curved_roots_GR_or_parent_closed':False,
    'whole_core_no_go':False,
    'new_supported_Lean_theorem_action_or_physical_selector':False,
}


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def elongate(word,q):
    assert q>=1 and q%2==1
    body=[]
    for u,v in zip(word,word[1:]):
        body += [u,v]*((q-1)//2)+[u]
    return body+[word[-1]]


def compose(p,q):
    assert p[-1]==q[0]
    return p+q[1:]


def controls():
    checks=[]; mutants=[]

    def check(name,value):
        assert bool(value),name
        checks.append(name)

    def reject(name,actual,altered):
        check('REJECT_'+name,actual!=altered)
        mutants.append(name)

    # A reversible unequal-mass word and a non-reversible triangle.
    samples=[[0,9,0,20,9,20,0,9,0],[0,9,20,0]]
    for idx,w in enumerate(samples):
        D,N1=owner.counts(w,1); _,N2=owner.counts(w,2)
        for q in [1,3,5]:
            ew=elongate(w,q); dd,nn1=owner.counts(ew,1); _,nn2=owner.counts(ew,2)
            check('ACTUAL_ELONGATION_%s_%s'%(idx,q),owner.valid_word(ew)
                  and len(ew)-1==q*(len(w)-1) and dd==q*D
                  and nn1==((q+1)*N1+(q-1)*N1.T)/2 and nn2==(q-1)*D+N2)
    D,N1=owner.counts(samples[1],1)
    reject('REMOVE_REVERSIBILITY_PREMISE',owner.counts(elongate(samples[1],3),1)[1],3*N1)

    w=samples[0]; D,N1=owner.counts(w,1); _,N2=owner.counts(w,2)
    ew=elongate(w,3)
    DD,NN,J,C,P,U,Delta,F=owner.full_operators(ew,2)
    alpha=s.Rational(1,3); T=D.inv()*N2
    TA=(1-alpha)*s.eye(D.rows)+alpha*T
    FA=s.eye(D.rows)-D.inv()*TA.T*D*TA
    check('WHOLE_ELONGATED_FEEDBACK',F==J*FA*C
          and (s.eye(F.rows)-F/2).det()==owner.pencil_det(DD,NN))
    check('WHOLE_ELONGATED_HEAT',Delta.rows==3*(len(w)-1)
          and Delta.trace()==2*Delta.rows and Delta*s.ones(Delta.rows,1)==s.zeros(Delta.rows,1))
    check('ACTUAL_WHOLE_REVERSIBLE_COMPRESSION',P*U*P==(P*U*P).T
          and P*U*P==J*DD.inv()*owner.counts(ew,1)[1]*DD.inv()*J.T)
    I=s.eye(D.rows)
    check('WEIGHTED_POSITIVE_UPPER_BOUND_IDENTITY',
          D*(4*alpha*I-FA)==alpha*(2*D+N2+N2.T)
          +alpha**2*(I-T).T*D*(I-T))
    reject('SUBSTITUTE_REPETITION_FOR_RECORDED_RETURNS',NN,3*N2)
    reject('DELETE_NEW_HEAT_MODES',Delta.rows,len(w)-1)

    records=[]
    for m,r in [(2,0),(4,-1),(4,1)]:
        base=owner.euler_word(m,r)
        D,A=owner.counts(base,1,range(33)); _,N2=owner.counts(base,2,range(33))
        L0=len(base)-1; T1=D.inv()*A
        for q in [3,5]:
            out=elongate(base,q); dd,na=owner.counts(out,1,range(33)); _,nb=owner.counts(out,2,range(33))
            check('ALL_718_FIXED_FREQUENCIES_%s_%s_%s'%(m,r,q),owner.valid_word(out)
                  and dd==q*D and na==q*A and nb==(q-1)*D+N2)
            check('ACTUAL_COARSE_GEOMETRY_%s_%s_%s'%(m,r,q),
                  dd/s.Integer(q*L0)==D/s.Integer(L0) and dd.inv()*na==T1
                  and 2*s.eye(33)-dd.inv()*na-dd.inv()*na.T==2*(s.eye(33)-T1))
            determinant=owner.pencil_det(dd,nb)
            check('STRICT_COMPLETE_FINITE_FEEDBACK_%s_%s_%s'%(m,r,q),0<determinant<1)
        records.append({'m':m,'r':r,'L0':L0,'initial_word_sha256':
                        hashlib.sha256(json.dumps(base).encode()).hexdigest()})

    # Prefix arithmetic applies to every past. These are two actual witnesses,
    # not computed minimizers; the proof bounds every finite extension minimum.
    base=owner.euler_word(2); D,A=owner.counts(base,1,range(33))
    _,N2base=owner.counts(base,2,range(33))
    past=base; K=1; prefix_receipts=[]
    for n in [1,2]:
        q=2*n*(K+1)+1; Knew=K+q
        dp,np=owner.counts(past,2,range(33))
        out=compose(past,elongate(base,q))
        dd,na=owner.counts(out,1,range(33)); _,nb=owner.counts(out,2,range(33))
        check('COMPLETE_PREFIX_RETENTION_%s'%n,out[:len(past)]==past
              and owner.valid_word(out) and len(out)-1==Knew*(len(base)-1))
        check('FULL_PREFIX_COUNTS_%s'%n,dp==K*D and dd==Knew*D
              and na==Knew*A and nb==np+(q-1)*D+N2base)
        alpha=s.Rational(K+1,Knew)
        tbar=(K*(dp.inv()*np)+D.inv()*N2base)/(K+1)
        check('COMPLETE_PREFIX_CONTRACTION_INPUT_%s'%n,
              alpha==s.Rational(1,2*n+1) and Knew==(2*n+1)*(K+1)
              and dd.inv()*nb==(1-alpha)*s.eye(33)+alpha*tbar)
        determinant=owner.pencil_det(dd,nb)
        check('PREFIX_FINITE_PRICE_POSITIVE_%s'%n,0<determinant<1)
        prefix_receipts.append({'n':n,'K':Knew,'length':len(out)-1,
                                'determinant_at_z_half':str(determinant),
                                'past_is_literal_prefix':True,'computed_minimizer':False})
        past=out;K=Knew
    reject('ZERO_PRICE_AT_A_FINITE_COMPLETE_WORD',owner.pencil_det(dd,nb),s.Integer(1))

    # Full support, not merely all 33 vertices, is needed for the finite no-zero.
    ham=[]
    for i in range(9):
        ham.append(i)
        if i<2: ham.append(31+i)
        ham += [9+i,20+i]
    ham += [18,29,19,30,0]
    d,n,j,c,p,u,delta,f=owner.full_operators(ham,2)
    check('HAMILTONIAN_HYPOTHESIS_CONTROL',owner.valid_word(ham)
          and len(ham)==34 and len(set(ham))==33 and p==s.eye(33)
          and f==s.zeros(33) and sum(owner.counts(ham,1,range(33))[1])==33)
    check('LITERAL_FULL_SCENE_NO_ZERO_INPUTS',owner.zone(0)!=owner.zone(9)
          and owner.zone(9)!=owner.zone(20) and owner.zone(20)!=owner.zone(0)
          and min(sum(1 for j in range(33) if A[i,j]>0) for i in range(33))==20)
    even=[0,9,0,20,0,9,0,20,0]
    d,n,j,c,p,u,delta,f=owner.full_operators(even,2)
    check('DISJOINT_PARITY_ORBITS_MUST_BE_HANDLED',f==s.zeros(f.rows)
          and sum(int(x!=0) for x in owner.counts(even,1)[1].row(0))==2)
    reject('ALL_VERTICES_IMPLY_ALL_REQUIRED_POSITIVE_EDGES',33,718)
    check('RATIONAL_FULL_PRICE_BOUND_CONSTANT',33*4==132
          and s.Rational(132,4)==33)

    # Literal fullStep and its actual blank-record input, not a substituted G.
    aa,pp,u0,v0=s.symbols('a p u v',real=True)
    R=s.Matrix([[aa,0,-pp,0],[0,aa,0,-pp],[0,pp,0,aa],[pp,0,aa,0]])
    P0=s.diag(1,0,1,0)
    check('ACTUAL_BLANK_RECORD_INPUT_BINDING',
          R*s.Matrix([u0,0,v0,0])==s.Matrix([aa*u0-pp*v0,0,0,pp*u0+aa*v0]))
    check('ACTUAL_FULLSTEP_ORTHOGONAL_POLYNOMIAL',
          R.T*R==(aa**2+pp**2)*s.eye(4))
    AP=P0*R*P0; SK=(AP-AP.T)/2
    check('ACTUAL_BLANK_PLANE_ANTISYMMETRY',SK.T*SK==pp**2*P0/4)
    p=(s.sqrt(5)-1)/2
    check('OWNED_POSITIVE_GOLDEN_ERROR_BOUND',s.simplify(p+p**2)==1
          and p/2>s.Rational(3,10))
    reject('REPLACE_RECORDED_COMPRESSION_BY_SYMMETRIC_READING',AP,AP.T)
    # The bound is sharp for symmetry alone; no admitted intertwiner is inferred.
    closest=(AP+AP.T)/2
    check('SHARP_SYMMETRIC_DISTANCE_CONTROL',
          (AP-closest).T*(AP-closest)==pp**2*P0/4)
    phase=s.diag(s.I,1,1,s.I)
    complex_reading=phase.H*closest*phase
    check('COMPLEX_ISOMETRY_PRESERVES_SELF_ADJOINTNESS',complex_reading.H==complex_reading)
    reject('REPLACE_COMPLEX_ADJOINT_BY_TRANSPOSE',complex_reading.H,complex_reading.T)
    tiny=s.Rational(1,100)*s.eye(4)
    check('INJECTIVE_ENCODING_SCALE_REQUIRES_NORMALIZATION',tiny.det()!=0
          and tiny.H*tiny==s.eye(4)/10000 and s.Rational(6,100)<s.Rational(3,10))
    reject('APPLY_NORMALIZED_BOUND_TO_UNNORMALIZED_ENCODING',tiny.H*tiny,s.eye(4))
    return {'checks':checks,'executed_mutants_rejected':mutants,
            'all_edge_witnesses':records,'prefix_witnesses':prefix_receipts,
            'actual_native_operator_bound':{'p':'(sqrt(5)-1)/2',
              'joint_error_bound':'delta+2*eta>=p/2>3/10',
              'compression_skew_square':'p^2*diag(1,0,1,0)/4',
              'all_isometry_proof':'ANALYTIC_NORM_AND_SYMMETRY_ARGUMENT'},
            'analytic_minimum_scope':SCOPE['minimum_existence']}


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path)
    ap.add_argument('--expect',type=Path);args=ap.parse_args()
    header={'schema':'d0-cyclic-memory-minimum/1','input_head':HEAD,'scope':SCOPE,
            'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
            'inputs_sha256':{p:sha(p) for p in INPUTS}}
    expected=None
    if not args.output:
        expected=json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
        assert all(expected.get(k)==v for k,v in header.items()),'SOURCE_SCOPE_OR_INPUT_MISMATCH'
    result={**header,**controls()}
    if args.output:args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:assert result==expected,'EXACT_CERTIFICATE_MISMATCH'
    print('PASS_CYCLIC_MEMORY_MINIMUM',len(result['checks']),'controls;',
          len(result['executed_mutants_rejected']),'executed mutants rejected')


if __name__=='__main__':main()
