#!/usr/bin/env python3
"""Exact controls for the pinned reference/memory preparation proof.

Analytic all-time and complete-class claims remain in that proof. The finite
controls keep every Fock component and both actual AF blocks. No native source
or preparation admission is inferred from the representation constructions.
"""
import argparse
import hashlib
import importlib.util
from itertools import product
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_reference_memory_preparation'
PROOF = '02_REGISTRY/research/A4D_NATIVE_REFERENCE_MEMORY_PREPARATION.md'
INPUTS = [
    '02_REGISTRY/research/A4D_NATIVE_FOCK_RECORD_BINDING.md',
    '02_REGISTRY/research/A4D_NATIVE_RECORD_METRIC_CHRONOLOGY.md',
    '02_REGISTRY/research/A4D_NATIVE_RECORDED_OBSERVER_PREPARATION.md',
    '02_REGISTRY/research/A4D_NATIVE_JONES_RECORD_TRANSPORT.md',
    '02_REGISTRY/research/A4D_NATIVE_FIBONACCI_RECORD_ACTIVATION.md',
    '02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md',
    '02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md',
    '02_REGISTRY/research/A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md',
    '02_REGISTRY/research/certificates/a4d_native_fock_record_binding_check.py',
    '02_REGISTRY/research/certificates/a4d_native_record_metric_chronology_check.py',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.py',
    '02_REGISTRY/research/certificates/a4d_native_fibonacci_record_activation.lean',
    '02_REGISTRY/research/certificates/a4d_native_jones_record_transport.py',
    '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
    '03_FORMALIZATION/D0/Representation/GoldenRelativeChannel.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARRelations.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
    '03_FORMALIZATION/D0/Algebra/FibonacciPerronTraceCanonicity.lean',
    '03_FORMALIZATION/D0/Geometry/Archive1DCochainRefinement.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementChainMap.lean',
]
spec = importlib.util.spec_from_file_location('reference_memory_program',ROOT/(BASE+'.py'))
P = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = P
spec.loader.exec_module(P)
s,a,p,z = P.s,P.a,P.p,P.z


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def source_closure(paths):
    found,pending = set(),list(paths)
    while pending:
        path = pending.pop()
        if path in found:
            continue
        found.add(path)
        if path.endswith('.lean'):
            for line in (ROOT/path).read_text().splitlines():
                if line.startswith('import '):
                    pending.extend('03_FORMALIZATION/'+name.replace('.','/')+'.lean'
                        for name in line.split()[1:] if name.startswith('D0.'))
    return sorted(found)


def controls(include_receipt=True):
    checks,mutants = [],[]
    def zero(value):
        values = value.todok().values() if isinstance(value,s.MatrixBase) else [value]
        return all(P.red(v)==0 for v in values)
    def check(name,truth):
        assert bool(truth),name
        checks.append(name)
    def eq(name,value):
        check(name,zero(value))
    def reject(name,false):
        check('REJECT_'+name,not false)
        mutants.append(name)

    I4,I16 = s.eye(4),s.eye(16)
    U,cut,blank,T = P.literal_tuple()
    UC,PC,BC = [P.mat(T.T*x*T) for x in (U,cut,blank)]
    Rp,Rm = UC[:2,:2],UC[2:,2:]
    eq('literal_fullstep_orthogonal',U.T*U-I4)
    eq('literal_parity_rotation',Rp-s.Matrix([[a,-p],[p,a]]))
    eq('literal_parity_reflection',Rm-s.Matrix([[a,-p],[-p,-a]]))
    eq('literal_blank_in_parity',BC-s.Matrix([[1,0,1,0],[0,1,0,1],[1,0,1,0],[0,1,0,1]])/2)
    UF,PF,BF = P.full_tuple()
    B0 = P.C.B0
    eq('full16_all_occupation_components',B0.T*B0-I16)
    eq('full16_actual_CAR_gate',UF-P.C.record(I4,I4[:,0])[0])
    check('whole_Fock_grade_dimensions',[sum(len(row)==k for row in P.C.old.SUBS)
                                        for k in range(5)]==[1,4,6,4,1])

    collision = P.collision()
    u,v,plus,minus,Up,Um,reflection = [collision[key] for key in
        ('u','v','plus','minus','Up','Um','reflection')]
    eq('collision_reference_plane_orthonormal',u.row_join(v).T*u.row_join(v)-s.eye(2))
    eq('collision_plus_unit_norm',(plus.T*plus)[0]-1)
    eq('collision_minus_unit_norm',(minus.T*minus)[0]-1)
    eq('collision_plus_whole_blank_input',BF*plus-plus)
    eq('collision_minus_whole_blank_input',reflection*BF*reflection*minus-minus)
    eq('collision_actual_plus_output',Up*plus-u)
    eq('collision_actual_minus_output',Um*minus-u)
    eq('collision_input_overlap',(plus.T*minus)[0]-p**3)
    eq('collision_time_reflection_swaps_history',reflection*plus-minus)
    eq('collision_time_reflection_fixes_output',reflection*u-u)
    eq('collision_time_reflection_conjugates_actual_gate',reflection*Up*reflection-Um)
    eq('collision_output_has_no_first_grade',P.C.first(u))
    eq('collision_output_has_no_top_grade',u[15])
    reject('STATE_CONDITIONED_GATE_IS_SINGLE_FIXED_ISOMETRY',zero((plus.T*minus)[0]-(u.T*u)[0]))
    relative = P.mat(Up.T*Um)
    eq('program_relative_gate_nonscalar_entry',relative[0,1]-2*a*p)
    # Cross-inner-product equation alpha I = beta Uplus*Uminus has rank two.
    program_minor = s.Matrix([[1,-relative[0,0]],[0,-relative[0,1]]])
    eq('universal_program_overlap_forcing_minor',program_minor.det()+2*a*p)
    reject('NONORTHOGONAL_CODE_IS_UNIVERSAL_PRODUCT_PROGRAM',zero(program_minor.det()))
    reflection4 = s.diag(-1,1,1,1)
    eq('signed_observer_reflection',reflection4*I4[:,0]+I4[:,0])
    eq('observer_line_survives_reflection',reflection4*I4[:,0]*I4[:,0].T*reflection4-I4[:,0]*I4[:,0].T)
    fixed = s.Matrix.hstack(*(reflection4-I4).nullspace())
    eq('reflection_fixed_space_is_spacelike',fixed.T*P.C.ETA*fixed+s.eye(3))
    eq('positive_pairing_survives_reflection',reflection4.T*I4*reflection4-I4)

    # The actual A1=M2( C ) (+) C bimodule, including its central projections.
    # Its commutant check supports the all-size matrix-unit argument in §2.
    coordinates = [(0,r,t) for r in range(2) for t in range(2)]+[(1,0,0)]
    gram = s.Matrix(5,5,s.symbols('g:25'))
    equations = []
    for block,size in ((0,2),(1,1)):
        for r,t in product(range(size),repeat=2):
            left,right = s.zeros(5),s.zeros(5)
            for col,(j,i,k) in enumerate(coordinates):
                if j!=block:
                    continue
                if i==t:
                    left[coordinates.index((j,r,k)),col]=1
                if k==r:
                    right[coordinates.index((j,i,t)),col]=1
            equations += list(gram*left-left*gram)+list(gram*right-right*gram)
    bimodule,_ = s.linear_eq_to_matrix(equations,list(gram))
    null = bimodule.nullspace()
    expected = [s.Matrix(list(s.diag(1,1,1,1,0))),s.Matrix(list(s.diag(0,0,0,0,1)))]
    check('actual_AF_bimodule_complete_pairing_commutant',
          len(null)==2 and s.Matrix.hstack(*(null+expected)).rank()==2)
    eq('positive_AF_trace_normalization',p+p*p-1)
    eq('positive_AF_inclusion_trace_recurrence',p*p+p**3-p)

    jones_records = []
    # The actual native path order is tested in both blocks; complete all-n
    # path overlap and Fibonacci rank identity are analytic in the proof.
    for j,item in enumerate(P.jones_code(0)):
        G,F,Z,H,R,e,f,Eu,Ev = [item[key] for key in
            ('G','F','Z','H','R','e','f','Eu','Ev')]
        D,r = G.shape
        tag = '_block'+str(j)
        eq('native_Jones_G_isometry'+tag,G.T*G-s.eye(r))
        eq('native_Jones_F_isometry'+tag,F.T*F-s.eye(r))
        eq('native_Jones_overlap'+tag,F.T*G-p**3*s.eye(r))
        eq('native_Jones_code_isometry'+tag,item['code'].T*item['code']-s.eye(2*r))
        eq('native_Jones_code_plus_history'+tag,a*Eu+p*Ev-G)
        eq('native_Jones_code_minus_history'+tag,a*Eu-p*Ev-F)
        eq('native_Jones_code_Eu_actual_H'+tag,Eu-H*G)
        eq('native_Jones_code_Ev_actual_H'+tag,Ev+H*Z)
        eq('native_Jones_H_orthogonal'+tag,H.T*H-s.eye(D))
        eq('native_Jones_H_squared_R'+tag,H*H-R)
        eq('native_Jones_full_complement_retained'+tag,H*(s.eye(D)-item['Q'])-(s.eye(D)-item['Q']))
        eq('native_Jones_H_feedback'+tag,e*H.T*(s.eye(D)-e)*H*e-p*p*e)
        eq('native_Jones_R_feedback'+tag,e*R.T*(s.eye(D)-e)*R*e-4*p**3*e)
        eq('native_Jones_cut_projector'+tag,e*e-e)
        eq('native_Jones_cut_rank'+tag,s.trace(e)-r)
        eq('native_Jones_untouched_complement_dimension'+tag,s.trace(s.eye(D)-item['Q'])-(D-2*r))
        eq('native_Jones_H_restricted_two_plane'+tag,
           G.row_join(Z).T*H*G.row_join(Z)-s.kronecker_product(Rp,s.eye(r)))
        check('native_Jones_ambient_dimensions'+tag,(D,r)==(P.J.E.counts(7)[j],P.J.E.counts(1)[j]))
        jones_records.append(dict(block=j,ambient_dimension=D,cut_rank=r,
            left_regular_multiplicity=D,identity_complement_dimension=D-2*r))
    for n in range(5):
        ranks,sizes = P.J.E.counts(n+1),P.J.E.counts(n+7)
        rank = sum(r*d for r,d in zip(ranks,sizes))
        check('whole_regular_Jones_feedback_rank_n%d'%n,
              rank==sum(d*d for d in P.J.E.counts(n+4)))
        eq('whole_native_Jones_cut_trace_n%d'%n,
           sum(p**(n+8+j)*ranks[j] for j in range(2))-p**6)
    reject('JONES_REDUCED_BLOCK_PRICE_IS_FULL_REGULAR_PRICE',
           sum(P.J.E.counts(1))==sum(r*d for r,d in zip(P.J.E.counts(1),P.J.E.counts(7))))
    reject('NATIVE_TRACE_WEIGHT_IS_NORMALIZED_REGULAR_RANK',zero(p**6-s.Rational(89,1597)))
    # Verify each price exponent from the actual two-plane restriction and
    # identity on its complement. Regular left multiplication repeats D times.
    e2 = s.diag(1,0)
    fH = P.mat(e2*Rp.T*(s.eye(2)-e2)*Rp*e2)
    fR = P.mat(e2*(Rp*Rp).T*(s.eye(2)-e2)*(Rp*Rp)*e2)
    eq('Jones_H_price_factor',(s.eye(2)-z*fH).det()-(1-z*p*p))
    eq('Jones_R_price_factor',(s.eye(2)-z*fR).det()-(1-4*z*p**3))

    U16,P16 = s.kronecker_product(UC,I4),s.kronecker_product(PC,I4)
    frames4 = [I4,s.diag(2,2,1,1),s.Matrix([[1,1,0,0],[0,3,1,0],[0,0,3,1],[0,0,0,1]])]
    endpoints = [P.endpoint_frame(A) for A in frames4]
    for j,(E,W) in enumerate(endpoints):
        eq('actual_W_normalized_frame_%d'%j,E.T*W*E-I16)
        eq('actual_W_frame_complete_%d'%j,E*P.endpoint_adjoint(E,I16,W)-I16)
    E0,W0 = endpoints[0]
    E1,W1 = endpoints[1]
    E2,W2 = endpoints[2]
    T10 = P.endpoint_tick(E1,W1,E0,W0,U16)
    T21 = P.endpoint_tick(E2,W2,E1,W1,U16)
    K = P.mat(T21*T10)
    eq('true_W_endpoint_tick_isometry',T10.T*W1*T10-W0)
    eq('true_W_endpoint_two_ticks_telescope',K-E2*U16*U16*P.endpoint_adjoint(E0,I16,W0))
    P0,PN = E0*P16*P.endpoint_adjoint(E0,I16,W0),E2*P16*P.endpoint_adjoint(E2,I16,W2)
    feedback = P.feedback(K,P0,PN,W0,W2)
    intrinsic = P.mat(P16*(U16*U16).T*(I16-P16)*(U16*U16)*P16)
    eq('true_W_endpoint_feedback_similarity',feedback-E0*intrinsic*P.endpoint_adjoint(E0,I16,W0))
    expected = s.diag(4*p**3*s.eye(4),s.zeros(12))
    eq('full16_two_tick_feedback_keeps_all_copies',intrinsic-expected)
    eq('full16_two_tick_price',(I16-z*intrinsic).det()-(1-4*z*p**3)**4)
    X = s.Matrix(4,4,s.symbols('x:16'))
    equations,_ = s.linear_eq_to_matrix(list(X*U-U*X)+list(X*cut-cut*X)+list(X*blank-blank*X),list(X))
    null = equations.nullspace()
    check('literal_whole_tuple_commutant_exact',len(null)==1 and null[0]==s.Matrix(list(I4)))
    spectator = s.Matrix([[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]])
    holonomy = s.kronecker_product(I4,spectator)
    for label,slot in [('gate',U16),('cut',P16),('blank',s.kronecker_product(BC,I4))]:
        eq('whole16_spectator_holonomy_commutes_'+label,holonomy*slot-slot*holonomy)
    V = holonomy*U16*U16
    eq('spectator_holonomy_invisible_to_feedback',P16*V.T*(I16-P16)*V*P16-intrinsic)
    reset = P.mat(blank*U*I4[:,0])
    eq('reset_discards_positive_native_probability',(reset.T*reset)[0]-p)
    reject('FRESH_BLANK_IS_RETAINED_CHRONOLOGY',zero((reset.T*reset)[0]-1))

    # Full16 radial frame control: the scalar volume density is indispensable.
    c = s.symbols('c',positive=True)
    grades = list(map(len,P.C.old.SUBS))
    Erad = s.diag(*[c**(k-2) for k in grades])
    Wrad = s.diag(*[c**(4-2*k) for k in grades])
    Krad = P.mat(Erad*UF*UF)
    Prad = Erad*PF*Erad.inv()
    actual_rad = P.feedback(Krad,PF,Prad,I16,Wrad)
    wrong_rad = P.mat(PF*Krad.T*(I16-Prad)*Krad*PF)
    eq('radial_frame_true_feedback_constant',actual_rad-4*p**3*B0*s.diag(I4,s.zeros(12))*B0.T)
    wrong_intrinsic = P.mat(B0.T*wrong_rad*B0)
    eq('radial_missed_pairing_feedback_eigenvalues',wrong_intrinsic-
       s.diag(4*p**3/c**2,4*p**3,4*p**3,4*p**3,*([0]*12)))
    wrongdet = (1-4*z*p**3/c**2)*(1-4*z*p**3)**3
    eq('radial_missed_pairing_false_price_jet',(-s.diff(wrongdet,c)/wrongdet).subs(c,1)+8*z*p**3/(1-4*z*p**3))
    reject('EUCLIDEAN_TRANSPOSE_IS_TRUE_ENDPOINT_ADJOINT',zero(wrong_rad-actual_rad))
    rawB = P.C.ext(frames4[1])*B0
    reject('UNNORMALIZED_FOCK_B_IS_W_ISOMETRY',zero(rawB.T*W1*rawB-I16))

    # Keep the distinct, already-owned state-conditioned chronology J(c).
    rotation = s.Matrix([[s.Rational(3,5),-s.Rational(4,5),0,0],
                         [s.Rational(4,5),s.Rational(3,5),0,0],[0,0,1,0],[0,0,0,1]])
    lifted = P.C.ext(rotation)
    nextU = P.mat(lifted*UF*lifted.T)
    actualK = P.mat(nextU*UF)
    chronological = P.feedback(actualK,PF,PF,I16,I16)
    active = list(range(4))+list(range(8,12))
    F8 = P.mat(B0.T*chronological*B0).extract(active,active)
    lam,tr,det,tr0,det0 = P.C.polynomials(s.Rational(3,5))
    pieces = [([0],lam,lam),([1],lam,lam),([2,7],tr,det),([3,6],tr,det),([4,5],tr0,det0)]
    for j,(rows,trace,determinant) in enumerate(pieces):
        block = F8.extract(rows,rows)
        eq('retained_chronology_actual_block_trace_%d'%j,s.trace(block)-trace)
        eq('retained_chronology_actual_block_determinant_%d'%j,block.det()-determinant)
        for r in rows:
            eq('retained_chronology_no_cross_block_%d_%d'%(j,r),
               F8.extract([r],sorted(set(range(8))-set(rows))))
    cp = s.symbols('cp',real=True)
    polynomial = P.chronological_determinant(cp)
    eq('retained_chronology_static_frame_price',polynomial.subs(cp,1)-(1-4*z*p**3)**4)
    derivative = P.red((-s.diff(polynomial,cp)/polynomial).subs({cp:s.Rational(3,5),z:s.Rational(1,2)}))
    reject('TELESCOPING_ELIMINATES_STATE_CONDITIONED_JET',zero(derivative))
    reject('ACTUAL_CHANGED_FRAME_PRODUCT_IS_PURE_BRIDGE',zero(actualK-lifted*UF*UF))

    # Genuine B(q,m) intrinsic component constraints. The following are
    # polynomial obstructions, not tests that redefine the native domain.
    x,y = s.symbols('x y',real=True)
    blank_scalar = s.Matrix([x,y,x,y])
    output = UC*blank_scalar
    eq('self_conditioned_blank_one_tick_opposite_required_signs',output[1]+output[3])
    eq('self_conditioned_first_grade_alignment_forces_second_row_spatial',
       (UC*s.Matrix([0,x,0,y]))[0]+p*x)
    symbolicM = s.Matrix([[x,0,0,0],[y,0,0,0],list(s.symbols('m8:12')),list(s.symbols('m12:16'))])
    eq('one_bridge_full_apparatus_faithfulness_obstruction',symbolicM.det())
    eq('literal_rotation_five_tick_positive_cone_obstruction',Rp**5+(28*p-17)*Rp+4*a*p**3*s.eye(2))
    eq('five_tick_root_threshold_strict',s.Rational(17,28)**2+s.Rational(17,28)-1+s.Rational(19,784))
    exactp = (s.sqrt(5)-1)/2
    check('five_tick_first_coefficient_positive',s.simplify((28*p-17).subs(p,exactp)).is_positive)
    reject('DROP_POSITIVE_INITIAL_TERM_FROM_FIVE_TICK_IDENTITY',zero(Rp**5+(28*p-17)*Rp))

    # Constructive internal whole-Blank trajectory. Faithfulness is only the
    # Pauli system marginal, not the full16 pure density or self-conditioned B.
    M = P.golden_blank_matrix()
    eq('golden_blank_initial_norm',s.trace(M*M.T)-1)
    eq('golden_whole_blank_initial_state',blank*M-M)
    rho = s.diag(p,p*p)
    eq('golden_blank_initial_system_marginal',P.system_marginal(M)-rho)
    parityM = T.T*M
    eq('golden_blank_parity_branches_equal',parityM[:2,:]-parityM[2:,:])
    eq('golden_blank_parity_purification',2*parityM[:2,:]*parityM[:2,:].T-rho)
    fock_vector = B0*s.Matrix(list(parityM))
    eq('golden_blank_actual_Fock_blank',BF*fock_vector-fock_vector)
    eq('golden_blank_not_self_conditioned_first_grade',P.C.first(fock_vector))
    eq('golden_blank_not_self_conditioned_top_grade',fock_vector[15])
    trajectory = []
    Un,Rpn,Rmn = I4,s.eye(2),s.eye(2)
    for n in range(6):
        Mn = P.mat(Un*M)
        sigma = P.system_marginal(Mn)
        eq('golden_all16_tick_norm_%d'%n,s.trace(Mn*Mn.T)-1)
        eq('golden_controlled_channel_formula_%d'%n,sigma-(Rpn*rho*Rpn.T+Rmn*rho*Rmn.T)/2)
        eq('golden_marginal_lower_bound_sum_of_squares_%d'%n,sigma-p*p*s.eye(2)-
           p**3*(Rpn[:,0]*Rpn[:,0].T+Rmn[:,0]*Rmn[:,0].T)/2)
        eq('golden_marginal_upper_bound_sum_of_squares_%d'%n,p*s.eye(2)-sigma-
           p**3*(Rpn[:,1]*Rpn[:,1].T+Rmn[:,1]*Rmn[:,1].T)/2)
        trajectory.append(dict(tick=n,system_marginal=[[str(v) for v in row] for row in sigma.tolist()]))
        Un,Rpn,Rmn = [P.mat(G*N) for G,N in ((U,Un),(Rp,Rpn),(Rm,Rmn))]
    sigma1 = P.system_marginal(P.mat(U*M))
    eq('golden_tick_one_Bloch_length',sigma1[0,0]-sigma1[1,1]-p**6)
    reject('FAITHFUL_INTERNAL_TRAJECTORY_IS_STATIC',zero(sigma1-rho))
    eq('golden_alltime_Pauli_upper_spectral_bound',(1+p**3)/(1-p**3)-1/p)
    eq('golden_alltime_Pauli_lower_spectral_bound',(1-p**3)/(1+p**3)-p)
    h0 = P.pauli_positive_pairing(rho)
    eq('golden_initial_Pauli_extremal_trace',s.trace(h0)-2-p-1/p)
    eq('golden_initial_Pauli_determinant',h0.det()-1)
    reject('FAITHFUL_SYSTEM_MARGINAL_IS_FULL_APPARATUS_FAITHFULNESS',M.rank()==4)
    # Arbitrary orthogonal branch proof kernel: these identities plus XX*=YY*=I
    # establish the positive-semidefinite bounds for every integer tick.
    X,Y = [s.Matrix(2,2,s.symbols(prefix+'0:4')) for prefix in ('v','w')]
    arbitrary = (X*rho*X.T+Y*rho*Y.T)/2
    eq('alltime_arbitrary_branch_lower_bound_kernel',arbitrary-p*p*(X*X.T+Y*Y.T)/2-
       p**3*(X[:,0]*X[:,0].T+Y[:,0]*Y[:,0].T)/2)
    eq('alltime_arbitrary_branch_upper_bound_kernel',p*(X*X.T+Y*Y.T)/2-arbitrary-
       p**3*(X[:,1]*X[:,1].T+Y[:,1]*Y[:,1].T)/2)

    # Complete positive site-local, grade-orthogonal Gram class: the scalar
    # obstruction includes all off-diagonal one-form Gram entries. L2 is a
    # finite symbolic control of the general telescoping proof, not its proof.
    sites = list(product(range(2),repeat=4))
    def shift(x,axis,amount,length):
        return tuple((value+amount)%length if j==axis else value
                     for j,value in enumerate(x))
    gr = {}
    for x in sites:
        tag = ''.join(map(str,x))
        gr[x] = s.Matrix(4,4,lambda i,j:s.Symbol('gram_'+tag+'_'+str(min(i,j))+str(max(i,j)),
                                                positive=True) if i==j else
                         s.Symbol('gram_'+tag+'_'+str(min(i,j))+str(max(i,j)),real=True))
    for role in range(4):
        plane = [x for x in sites if x[role]==0]
        def flux(x,axis):
            return gr[x][axis,role] if x[role]==0 else s.S.Zero
        weighted_div = {x:2*sum(flux(shift(x,r,-1,2),r)-flux(x,r) for r in range(4))
                        for x in sites}
        eq('all_site_local_full_oneform_Gram_plane_sum_role%d'%role,
           sum(weighted_div[x] for x in plane)+2*sum(gr[x][role,role] for x in plane))
        check('all_site_local_plane_sum_strict_negative_role%d'%role,
              (-2*sum(gr[x][role,role] for x in plane)).is_negative)
        # J1 has zero new-plane entries; J0 copies coarse x_r=0 to y_r=L.
        fine_sites = list(product(range(3),repeat=4))
        new_plane = [v for v in fine_sites if v[role]==2]
        check('fine_new_plane_every_adjoint_stencil_zero_role%d'%role,
              all(v[role]!=0 for y in new_plane
                  for v in [y]+[shift(y,r,-1,3) for r in range(4)]))
        check('fine_new_plane_scalar_copy_from_coarse_support_role%d'%role,
              all(tuple(0 if v==2 else v for v in y)[role]==0 for y in new_plane))
    # Arbitrary gamma in the preceding nonlocal repair never preserves the
    # fixed point-projector representation, even though it repairs Dirac.
    gamma = s.symbols('gamma',positive=True)
    Gnonlocal = s.Matrix([[1,0,s.Rational(1,2)],[0,1,s.Rational(1,2)],
                         [s.Rational(1,2),s.Rational(1,2),gamma]])
    point = s.diag(1,0,0)
    eq('nonlocal_repair_point_observable_defect_independent_gamma',
       (Gnonlocal*point-point*Gnonlocal)[0,2]+s.Rational(1,2))
    reject('NONLOCAL_REPAIR_PRESERVES_FIXED_POINT_OBSERVABLE',zero(Gnonlocal*point-point*Gnonlocal))

    # Reuse the preceding packet's algebraic correction to the old notes.
    # The new bridge is numerical identity of already derived native readouts;
    # it neither identifies the observables nor derives spacetime dimension.
    notes = P.golden_note_data()
    phi,psi,delta = [notes[key] for key in ('phi','psi','delta')]
    ph,ps = s.symbols('phi psi')
    AA,BB,CC,DD = ph+ps-1,ph*ps+1,ph*ph-ph-1,ps*ps-ps-1
    eq('AB_imply_C_polynomial_identity',CC-ph*AA+BB)
    eq('AB_imply_D_polynomial_identity',DD-ps*AA+BB)
    eq('A_C_imply_B_polynomial_identity',BB-ph*AA+CC)
    eq('A_C_imply_D_polynomial_identity',DD-(ps-ph)*AA-CC)
    eq('equal_positive_roots_satisfy_C_D',phi*phi-phi-1)
    reject('C_D_ALONE_FORCE_A_B',zero(2*phi-1) or zero(phi*phi+1))
    eq('native_delta_is_half_p_cubed',delta-p**3/2)
    eq('native_dual_roots_sum',phi+psi-1)
    eq('native_dual_roots_product',phi*psi+1)
    eq('native_positive_phi_reciprocal',phi*p-1)
    eq('golden_unit_crossing_Q4',2*delta*phi**3-1)
    for D,value in notes['Q'].items():
        eq('golden_dimension_label_is_unit_power_D%d'%D,value-phi**(D-4))
    eq('history_overlap_is_two_delta',(plus.T*minus)[0]-2*delta)
    eq('history_squared_fidelity_is_four_delta_squared',(plus.T*minus)[0]**2-4*delta*delta)
    eq('native_Fibonacci_recording_corner_weight_is_four_delta_squared',p**6-4*delta*delta)
    eq('uniform_blank_tick_one_contrast_is_four_delta_squared',sigma1[0,0]-sigma1[1,1]-4*delta*delta)
    eq('owned_two_tick_feedback_eigenvalue_is_eight_delta',4*p**3-8*delta)
    eq('owned_two_tick_feedback_eigenvalue_complements_history_fidelity',4*p**3+4*delta*delta-1)
    incidence = notes['incidence']
    check('actual_AF_fixed_space_first_counts',notes['fixed_counts']==[2,3,7,18])
    eq('all_level_fixed_space_recurrence_kernel',incidence**4-3*incidence**2+s.eye(2))
    check('three_inclusions_fixed_space_obstruction',all(f<8 for f in notes['fixed_counts'][:3])
          and notes['fixed_counts'][3]>=8)
    native_frame = P.J.E.frame(0)
    eq('existing_three_inclusion_whole_fourrow_frame',
       native_frame['V'].T*native_frame['V']-s.eye(4*native_frame['old_dimension']))
    reject('ABCD_FOUR_INDEPENDENT_CONSTRAINTS',
           len(s.groebner([AA,BB,CC,DD],ph,ps).polys)==4)

    if not include_receipt:
        return dict(exact_controls=len(checks),mutants=mutants,jones_blocks=jones_records,
                    golden_trajectory=trajectory)
    return finish_receipt(checks,mutants,jones_records,trajectory,check)


def finish_receipt(checks,mutants,jones_records,trajectory,check):
    receipt_path = BASE+'_lean_results.json'
    receipt = json.loads((ROOT/receipt_path).read_text())
    output = (ROOT/(BASE+'_lean_output.txt')).read_text()
    capsule = (ROOT/(BASE+'.lean')).read_text()
    check('narrow_Lean_receipt_success',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
    check('Lean_capsule_fingerprint',receipt['capsule_sha256']==sha(BASE+'.lean'))
    check('Lean_actual_output_fingerprint',receipt['output_sha256']==sha(BASE+'_lean_output.txt'))
    axioms = {name:[a.strip() for a in body.split(',') if a.strip()]
        for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output)}
    check('Lean_actual_axiom_receipt',axioms==receipt['axioms'])
    check('Lean_declarations_resolved',set(axioms)==set(receipt['declarations']))
    printed = set(re.findall(r'^#print axioms ([A-Za-z0-9_.]+)',capsule,re.MULTILINE))
    check('Lean_every_axiom_request_resolved',set(axioms)==printed)
    requested_checks = set(re.findall(r'^#check ([A-Za-z0-9_.]+)',capsule,re.MULTILINE))
    requested_prints = set(re.findall(r'^#print (?!axioms\b)([A-Za-z0-9_.]+)',capsule,re.MULTILINE))
    check('Lean_every_diagnostic_check_bound',requested_checks==set(receipt['diagnostic_checks']))
    check('Lean_every_diagnostic_print_bound',requested_prints==
          set(receipt['diagnostic_definitions'])|set(receipt['diagnostic_printed_propositions']))
    for name,dependencies in axioms.items():
        check('Lean_standard_axioms_'+name,set(dependencies)<={'propext','Classical.choice','Quot.sound'})
    for name in receipt['diagnostic_definitions']:
        check('Lean_actual_definition_'+name,('def '+name+' ') in output or ('theorem '+name+' ') in output)
    for name in receipt['diagnostic_checks']:
        check('Lean_actual_declaration_'+name,
              re.search(r'^'+re.escape(name)+r'(?:\.\{[^}]*\})?(?:\s|:)',output,re.MULTILINE) is not None)
    for name in receipt['diagnostic_printed_propositions']:
        check('Lean_actual_proposition_'+name,('theorem '+name+' ') in output)
    for path,fingerprint in receipt['input_sha256'].items():
        check('Lean_SOURCE_input_'+path,sha(path)==fingerprint)
    check('Lean_original_cache_preserved',receipt['original_cache_unchanged'])
    actual_closure = {path for path in source_closure([BASE+'.lean'])
                      if path.startswith('03_FORMALIZATION/D0/')}
    modules = {path[len('03_FORMALIZATION/'):-5].replace('/','.') for path in actual_closure}
    check('Lean_exact_actual_SOURCE_module_closure',
          set(receipt['cache_source_comparison'])==modules==set(receipt['current_overlay_reuse']))
    check('Lean_exact_SOURCE_receipt_closure',set(receipt['input_sha256'])==actual_closure|{
        '03_FORMALIZATION/lean-toolchain','03_FORMALIZATION/lake-manifest.json'})
    check('Lean_all_dependency_objects_copied',receipt['copied_olean_file_count']==len(modules))
    prior = receipt['verified_overlay_receipt']
    check('Lean_prior_overlay_receipt_binding',sha(prior['path'])==prior['sha256'])
    prior_receipt = json.loads((ROOT/prior['path']).read_text())
    prior_builds = {entry['module']:entry for entry in prior_receipt['source_overlay_rebuilds']}
    builds = {entry['module']:entry for entry in receipt['source_overlay_rebuilds']}
    matching = {module for module,state in receipt['cache_source_comparison'].items() if state=='MATCH'}
    check('Lean_all_source_reuse_classes_accounted',set(builds)|matching==modules and not(set(builds)&matching))
    check('Lean_exact_matching_source_cache_count',receipt['matching_cache_source_reuse_count']==len(matching))
    check('Lean_inherited_rebuild_count_not_new_compilations',
          receipt['verified_prior_source_rebuild_count']==receipt['refreshed_source_module_count']==len(builds)
          and receipt['new_overlay_compilation_count']==0)
    for module,entry in receipt['current_overlay_reuse'].items():
        source_path = '03_FORMALIZATION/'+module.replace('.','/')+'.lean'
        check('Lean_actual_SOURCE_match_'+module,sha(source_path)==entry['source_sha256'])
        check('Lean_actual_overlay_object_pin_'+module,
              receipt['actual_import_olean_sha256'][entry['overlay_olean']]==entry['olean_sha256'])
        if module in matching:
            check('Lean_actual_cached_SOURCE_match_'+module,
                  entry['source_comparison']=='MATCH' and entry['source_sha256']==entry['cache_source_sha256'])
            check('Lean_original_cache_object_pin_'+module,
                  receipt['original_cache_olean_sha256']['.lake/build/lib/lean/'+module.replace('.','/')+'.olean']==entry['olean_sha256'])
        else:
            build = builds[module]
            check('Lean_exact_prior_SOURCE_build_receipt_'+module,build==prior_builds[module])
            check('Lean_inherited_SOURCE_build_success_'+module,build['exit_code']==0)
            check('Lean_inherited_SOURCE_build_stdout_'+module,
                  hashlib.sha256(build['compiler_stdout'].encode()).hexdigest()==build['output_sha256'])
            check('Lean_inherited_SOURCE_build_source_'+module,sha(source_path)==build['source_sha256'])
            check('Lean_inherited_SOURCE_build_object_'+module,
                  entry['source_comparison']=='VERIFIED_SOURCE_OVERLAY' and entry['olean_sha256']==build['olean_sha256'])
    check('Lean_actual_object_pin_count_including_Init_and_Mathlib',
          len(receipt['actual_import_olean_sha256'])==len(modules)+2)
    archived_inputs = []
    for reference in receipt.get('archived_proof_references',[]):
        old_receipt = json.loads((ROOT/reference['receipt']).read_text())
        old_output = (ROOT/reference['output']).read_text()
        old_axioms = {name:[a.strip() for a in body.split(',') if a.strip()]
            for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",old_output)}
        tag = Path(reference['capsule']).stem
        check('archived_Lean_receipt_binding_'+tag,sha(reference['receipt'])==reference['receipt_sha256'])
        check('archived_Lean_compilation_success_'+tag,old_receipt['status']=='PASS' and old_receipt['compiler_exit_code']==0)
        check('archived_Lean_capsule_binding_'+tag,
              sha(reference['capsule'])==reference['capsule_sha256']==old_receipt['capsule_sha256'])
        check('archived_Lean_output_binding_'+tag,
              sha(reference['output'])==reference['output_sha256']==old_receipt['output_sha256'])
        check('archived_Lean_actual_axiom_receipt_'+tag,old_axioms==old_receipt['axioms'])
        check('archived_Lean_named_propositions_resolved_'+tag,
              set(reference['declarations'])<=set(old_axioms))
        check('archived_Lean_SOURCE_receipt_binding_'+tag,reference['input_sha256']==old_receipt['input_sha256'])
        for name in reference['declarations']:
            check('archived_Lean_standard_axioms_'+name,
                  set(old_axioms[name])<={'propext','Classical.choice','Quot.sound'})
        for path,fingerprint in reference['input_sha256'].items():
            check('archived_Lean_SOURCE_input_'+path,sha(path)==fingerprint)
        archived_inputs.extend([reference['capsule'],reference['output'],reference['receipt']])
        archived_inputs.extend(reference['input_sha256'])
    source = re.search(r'Input SOURCE\s+`([0-9a-f]{40})`',(ROOT/PROOF).read_text()).group(1)
    check('proof_Lean_SOURCE_agree',source==receipt['source_commit'])
    inputs = source_closure(INPUTS+list(receipt['input_sha256'])+[prior['path']]+archived_inputs)
    return dict(schema='d0-native-reference-memory-preparation/1',
        verdict='EXACT_NATIVE_HISTORY_CODE_AND_RETAINED_REFERENCE_REQUIREMENT_WITH_UNIFORM_INTERNAL_COMPONENT',
        input_source_sha=source,exact_controls=len(checks),controls=checks,
        executed_mathematical_mutants=mutants,actual_Jones_blocks=jones_records,
        full_regular_Jones_at_zero=dict(dimension=1597,feedback_rank=89,two_plane_rank=178),
        golden_whole_blank_finite_controls=trajectory,
        analytic_alltime_system_density_bounds=['p^2 I','p I'],
        analytic_alltime_Pauli_pairing_spectrum=['p','1/p'],
        reused_golden_identity='history_overlap=2 delta; squared_fidelity=Fibonacci_native_recording_corner_weight=first_tick_Pauli_contrast=4 delta^2; numerical identity, not identification of observables.',
        fixed_space_counts=[2,3,7,18],fixed_space_recurrence='f_(r+2)=3 f_(r+1)-f_r',
        four_levels_scope='Three inclusions plus initial level in the already specified covariant full-record representation class; no spacetime-dimension theorem.',
        scope='Exact full16 collision, endpoint pairings and chronology; actual Jones paths and full complements; primitive and bimodule commutants; exact five-tick identity; controlled-channel SOS kernels and four-dimensional local-Gram plane sums. General-group, all-level, all-time and complete-class arguments remain analytic in the pinned proof, not all in Lean.',
        faithful_object='Pauli system marginal only; the full16 state is pure and not the self-conditioned B(q,m) preparation.',
        signed_vector_obstruction_not_line_obstruction=True,
        previously_nonconstant_state_conditioned_chronology_preserved=True,
        Jones_history_code_native_interaction='OPEN',universal_reference_preparation='OPEN',
        native_shared_preparation='OPEN',native_matter_Pauli_identification='OPEN',
        native_heat_refinement_source_Ward_GR='OPEN',original_parent_terminal='OPEN',
        input_sha256={path:sha(path) for path in inputs},proof_sha256=sha(PROOF),
        program_sha256=sha(BASE+'.py'),checker_sha256=sha(BASE+'_check.py'),
        Lean_capsule_sha256=sha(BASE+'.lean'),Lean_output_sha256=sha(BASE+'_lean_output.txt'),
        Lean_receipt_sha256=sha(receipt_path))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args = parser.parse_args()
    result = controls()
    target = ROOT/(BASE+'_certificate.json')
    if args.write:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        assert json.loads(target.read_text())==result,'REFERENCE_MEMORY_PREPARATION_IMMUTABLE_LEDGER_MISMATCH'
    print('PASS_NATIVE_REFERENCE_MEMORY_PREPARATION controls=%d mutants=%d native_shared_preparation=OPEN'%
          (result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__ == '__main__':
    main()
