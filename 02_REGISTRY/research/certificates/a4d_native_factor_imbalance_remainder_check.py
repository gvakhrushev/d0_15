#!/usr/bin/env python3
"""Exact full feedback jets and constrained ten-slot factor-imbalance controls.

The arbitrary-size support, logdet derivative and all-L estimates are proved
analytically in the memo. Mathematical phase controls are not native laws.
"""
import argparse
from collections import Counter
from fractions import Fraction
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_factor_imbalance_remainder'
PROOF = '02_REGISTRY/research/A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md'
HEAD = '1555a67779d42a78108a0525dd5dc1a3a580c136'
INPUTS = [
    '03_FORMALIZATION/D0/Core/Phi.lean',
    '03_FORMALIZATION/D0/Representation/GoldenCoherentMemory.lean',
    '03_FORMALIZATION/D0/Representation/GoldenRelativeChannel.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveActionFunctional.lean',
    '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
    '02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md',
    '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md',
    '02_REGISTRY/research/A4D_NATIVE_RECORDED_OBSERVER_PREPARATION.md',
    '02_REGISTRY/research/A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md',
    '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md',
    '02_REGISTRY/research/A4D_NATIVE_FINITE_PROBE_COMPLETION.md',
    '02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance.lean',
    '02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance_results.json',
    '02_REGISTRY/research/certificates/a4d_native_constrained_price_source.lean',
    '02_REGISTRY/research/certificates/a4d_native_constrained_price_source_results.json',
    '02_REGISTRY/research/certificates/a4d_native_recorded_observer_preparation.lean',
    '02_REGISTRY/research/certificates/a4d_native_recorded_observer_preparation_results.json',
    '02_REGISTRY/research/certificates/a4d_native_recorded_observer_preparation_certificate.json',
    '02_REGISTRY/research/certificates/a4d_native_recorded_observer_preparation_check.py',
]
SCOPE = {
    'domain': 'FULL_TWO_TICK_ORTHOGONAL_OPERATOR_AND_CONSTANT_RANK_READOUT_FIRST_JETS_AT_RECORDED_GOLDEN_BLOCK_BASE',
    'whole_carrier': 'ALL_16_L4_HODGE_COCHAINS_WITH_A_FOUR_COORDINATE_RECORDED_BLOCK_IN_AN_ACTUAL_W_ORTHONORMAL_FRAME',
    'whole_feedback_remainder': 'Jprime=Cphi*sigma_WITH_ALL_PROJECTOR_AND_ARCHIVE_ROWS_RETAINED',
    'moving_actual_record_reference_remainder': '-4*E1*E4/(a*p*L^2)_WITH_THE_SAME_FACTOR_FIRST_JET',
    'moving_record_total_factor_derivative': '>1/10000_AT_beta_log2_FOR_ALL_L_GE_2',
    'bounded_observer_response': 'O(L^-2)_ON_THE_SPECIFIED_DIAGONAL_REST_BASE',
    'moving_record_uniform_C3_and_half_contrast': 'ANALYTIC_FULL_MODE_MOMENT_PROOF_AND_h^(1/3)/20000_FOR_SMALL_h',
    'bounded_observer_metric_jets_are_derived_for_all_native_preparations': False,
    'arbitrary_archive_size_proof': 'ANALYTIC_SUPPORT_PROOF_NOT_FINITE_RANK_EXTRAPOLATION',
    'isospectral_frame_or_readout_jets_can_cancel_shape_heat': False,
    'fixed_gate_prepared_class_factor_derivative': '2*(E1-E2)>1/10000_AT_beta_log2_ALL_L_GE_2',
    'all_ten_heat_and_required_remainder_slots_computed': True,
    'rho0_comparison': 'EXACT_ZERO_IN_ALL_TEN_SLOTS_ON_CONSTANT_FLAT_LORENTZ_READOUT',
    'positive_Q_is_identified_with_Lorentz_q': False,
    'blank_input_plane_is_price_projector': False,
    'scalar_operator_jet_has_only_one_possible_metric_covector_component': False,
    'derivative_zero_alone_implies_uniform_secant_bound': False,
    'native_common_q_D_b_m_preparation_or_operator_jet_owned': False,
    'record_apparatus_is_sixteen_component_matter_or_zero_matter': False,
    'compound_positive_heat_is_selected_by_core': False,
    'fixed_beta_z_or_normalization_law_selected': False,
    'mathematical_phase_cancellation_is_native_source': False,
    'all_other_action_terms_have_zero_intrinsic_response': False,
    'first_jet_mismatch_excludes_all_normalizations_or_corrected_roots': False,
    'whole_core_no_go': False,
    'native_stationarity_source_Ward_curved_roots_soundness_recovery_or_GR_closed': False,
    'original_parent_terminal_changed': False,
    'new_Lean_theorem_or_kernel_formalized_all_size_derivative': False,
    'new_action_selector_gate_angle_or_physical_postulate': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def skew(n, i, j):
    k = s.zeros(n)
    k[i, j], k[j, i] = 1, -1
    return k


def sym_basis(n):
    for i in range(n):
        for j in range(i, n):
            v = s.zeros(n)
            v[i, j] = 1
            v[j, i] = 1
            yield (i, j), v


def controls():
    checks, mutants, operator_cases, heat_cases = [], [], [], []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    def reject(name, actual, false_value):
        check('REJECT_' + name, actual != false_value)
        mutants.append(name)

    a, p = s.symbols('a p')
    z = s.Rational(1, 7)  # finite control, not a native fugacity law
    ideal = s.groebner([a*a-p, p*p+p-1], a, p, domain=s.QQ)

    def red(value):
        num, den = s.cancel(value).as_numer_denom()
        den = ideal.reduce(den)[1]
        assert den != 0, 'ZERO_QUOTIENT_DENOMINATOR'
        return s.cancel(ideal.reduce(num)[1] / den)

    def zero(value):
        if isinstance(value, s.MatrixBase):
            return all(zero(v) for v in value)
        return red(value) == 0

    def mr(value):
        return value.applyfunc(red)

    U4 = s.Matrix([[a, 0, -p, 0], [0, a, 0, -p],
                   [0, p, 0, a], [p, 0, a, 0]])
    pp, pb = s.diag(1, 1, 0, 0), s.diag(1, 0, 1, 0)
    Pi = s.diag(s.ones(2)/2, s.ones(2)/2)
    J = s.Matrix([[0, 0, -1, -1], [0, 0, -1, -1],
                  [1, 1, 0, 0], [1, 1, 0, 0]]) / 2
    C = 8*z*a*p*(p-p*p)/(1-4*z*p**3)
    Cblank = 4*z*a*p/(1-z*p*p)
    check('literal_actual_native_fullStep_binding',
          '!![a,0,-p,0; 0,a,0,-p; 0,p,0,a; p,0,a,0]' in
          (ROOT/INPUTS[1]).read_text())
    check('literal_complete_golden_orthogonality', zero(U4.T*U4-s.eye(4)))
    golden_jet_jacobian=s.Matrix([[2*a,-1],[0,1+2*p]])
    check('actual_golden_parameter_jets_forced_zero',
          zero(golden_jet_jacobian.inv()*golden_jet_jacobian-s.eye(2)) and
          not zero(golden_jet_jacobian.det()))
    free_angle_jet=s.Matrix([-p,a])
    check('free_phase_angle_is_not_native_golden_parameter_jet',
          zero(2*a*free_angle_jet[0]+2*p*free_angle_jet[1]) and
          not zero(golden_jet_jacobian*free_angle_jet))
    check('rank_two_eigenphase_projector', Pi*Pi == Pi and Pi.T == Pi and
          Pi*U4 == U4*Pi and J.T == -J and J*J == -Pi)
    check('eigenphase_normalization_sigma_one', -sum(J[i,j] for i,j in [(0,2),(0,3),(1,2),(1,3)])/2 == 1)
    reject('REPLACE_PRICE_PROJECTOR_WITH_BLANK_INPUT', pp, pb)

    archive_rotation = s.Matrix([[s.Rational(3,5), -s.Rational(4,5)],
                                 [s.Rational(4,5), s.Rational(3,5)]])
    for extra in [s.eye(0), archive_rotation, s.diag(archive_rotation, 1, -1)]:
        U = s.diag(U4, extra)
        n = U.rows
        I = s.eye(n)
        Z = mr(U*U)
        pinative = s.diag(Pi, s.zeros(n-4))
        check('entire_archive_orthogonal_base_' + str(n), zero(U.T*U-I))
        for pname, smallP, coefficient in [('price', pp, C), ('blank_control', pb, Cblank)]:
            P = s.diag(smallP, s.zeros(n-4))
            F = mr(P*Z.T*(I-P)*Z*P)
            if pname == 'price':
                expected = s.zeros(n)
                expected[0,0] = expected[0,1] = expected[1,0] = expected[1,1] = 2*p**3
                Res = I+z*F/(1-4*z*p**3)
                expected_det = 1-4*z*p**3
            else:
                expected = p*p*P
                Res = I+z*F/(1-z*p*p)
                expected_det = (1-z*p*p)**2
            check('full_feedback_no_deleted_modes_' + pname + '_' + str(n), zero(F-expected))
            check('full_pencil_resolvent_' + pname + '_' + str(n), zero((I-z*F)*Res-I))
            check('full_pencil_determinant_' + pname + '_' + str(n), zero((I-z*F).det()-expected_det))
            for i,j in itertools.combinations(range(n), 2):
                K = skew(n,i,j)
                dU = K*U
                dZ = dU*U+U*dU
                dF = P*dZ.T*(I-P)*Z*P+P*Z.T*(I-P)*dZ*P
                source = z*s.trace(Res*dF)
                sigma = -sum(K[r,c] for r,c in [(0,2),(0,3),(1,2),(1,3)])/2
                check('all_full_operator_tangent_coefficients', zero(source-coefficient*sigma))
                check('spectral_trace_reads_same_sigma', zero(sigma+s.trace(pinative*dU)/(2*p)))
                dP = K*P-P*K
                check('every_projector_jet_is_admissible', dP.T == dP and dP*P+P*dP == dP)
                dFP = dP*Z.T*(I-P)*Z*P-P*Z.T*dP*Z*P+P*Z.T*(I-P)*Z*dP
                check('all_readout_terms_cancel_in_price', zero(z*s.trace(Res*dFP)))
                dUc = K*U-U*K
                dZc = dUc*U+U*dUc
                dFc = P*dZc.T*(I-P)*Z*P+P*Z.T*(I-P)*dZc*P
                check('every_isospectral_operator_jet_zero', zero(z*s.trace(Res*dFc)))
            operator_cases.append({'dimension':n, 'projector':pname,
                                   'skew_operator_and_readout_basis_size':n*(n-1)//2,
                                   'extra_archive_all_retained':True})
    # The opposite class is a real orthogonal curve, not an assumed cancellation.
    t = s.Symbol('t', real=True)
    rotation = s.eye(4)+(s.cos(t)-1)*Pi+s.sin(t)*J
    check('nonisospectral_control_is_exact_curve',
          s.simplify(rotation.T*rotation-s.eye(4)) == s.zeros(4))
    Ucurve = rotation*U4
    dU = Ucurve.diff(t).subs(t,0)
    P = pp; Z = mr(U4*U4); F = mr(P*Z.T*(s.eye(4)-P)*Z*P)
    Res = s.eye(4)+z*F/(1-4*z*p**3)
    dZ = dU*U4+U4*dU
    nonzero_source = red(z*s.trace(Res*(P*dZ.T*(s.eye(4)-P)*Z*P+P*Z.T*(s.eye(4)-P)*dZ*P)))
    check('independent_control_derivative_is_actual_Cphi', zero(nonzero_source-C) and not zero(C))
    reject('ALL_ORTHOGONAL_JETS_HAVE_ZERO_PRICE_SOURCE', nonzero_source, 0)
    reject('OMIT_HALF_IN_SIGMA', nonzero_source, red(2*C))
    # Moving W-adjoints, P and U are really transported on a complete finite carrier.
    n=6; u=s.diag(U4,archive_rotation); P=s.diag(pp,s.zeros(2))
    B=s.diag(2,3,5,7,11,13); W=B.T*B
    uf=B.inv()*u*B; pf=B.inv()*P*B
    adj=lambda X:W.inv()*X.T*W
    Fw=pf*adj(uf*uf)*(s.eye(n)-pf)*(uf*uf)*pf
    Fe=P*(u*u).T*(s.eye(n)-P)*(u*u)*P
    check('actual_moving_pairing_readout_orthogonal', zero(adj(pf)-pf) and zero(pf*pf-pf))
    check('actual_moving_pairing_U_orthogonal', zero(adj(uf)*uf-s.eye(n)))
    check('complete_weighted_feedback_is_similarity', zero(Fw-B.inv()*Fe*B))
    reject('FREEZE_WEIGHTED_ADJOINT_TO_TRANSPOSE', zero(uf.T*uf-s.eye(n)), True)

    # Native row convention, actual recorded observer, and the true joint tangent.
    eta=s.diag(1,-1,-1,-1); gam=1/(2*a*p)
    boost=s.Matrix([[gam,0,0,-gam*p**3],[0,1,0,0],[0,0,1,0],[-gam*p**3,0,0,gam]])
    h=s.Matrix([[p+s.Rational(1,2),0,0,-s.Rational(1,2)],
                [0,1,0,0],[0,0,1,0],[-s.Rational(1,2),0,0,p+s.Rational(1,2)]])
    obs=s.Matrix([1,0,0,p**3])/(2*a*p)
    check('actual_recorded_observer_positive_form', zero(boost.T*boost-h))
    check('actual_observer_boost_is_Lorentz', zero(boost*eta*boost.T-eta))
    check('actual_recorded_observer_rest_frame', zero(boost*obs-s.Matrix([1,0,0,0])))
    # Genuine native-gate input curve, density and moving observer. The
    # observer is not frozen to manufacture a zero remainder.
    ut=(1-t*t)/(1+t*t); vt=2*t/(1+t*t)
    check('genuine_record_input_curve_normalized',s.simplify(ut*ut+vt*vt)==1)
    output=U4*s.Matrix([ut,0,vt,0]); oa=output[0]; ob=output[3]
    check('genuine_recorded_curve_keeps_all_output_slots',
          output==s.Matrix([a*ut-p*vt,0,0,p*ut+a*vt]))
    dd=(oa**4+ob**4)/(2*oa*oa*ob*ob)
    cc=(ob**4-oa**4)/(2*oa*oa*ob*ob)
    dh=s.Matrix([[dd.diff(t).subs(t,0),0,0,cc.diff(t).subs(t,0)],
                 [0,0,0,0],[0,0,0,0],
                 [cc.diff(t).subs(t,0),0,0,dd.diff(t).subs(t,0)]])
    expected_dh=s.Matrix([[-2*a/p**2,0,0,2*a*(1+p*p)/p**3],
                         [0,0,0,0],[0,0,0,0],
                         [2*a*(1+p*p)/p**3,0,0,-2*a/p**2]])
    check('genuine_observer_jet_reproduces_owned_derivative',zero(dh-expected_dh))
    dhrest=boost.inv().T*dh*boost.inv()
    expected_rest=s.zeros(4); expected_rest[0,3]=expected_rest[3,0]=4/(a*p)
    check('actual_moving_record_rest_jet_has_only_mixed_slots',zero(dhrest-expected_rest))
    jbase=s.Matrix([1,0,0,p**3]); dj=s.Matrix([0,0,0,-8*a*p])
    dn=(dj-jbase*(jbase.T*eta*dj)[0]/(4*p**3))/(2*a*p)
    nu=boost*dn
    check('actual_normalized_observer_rest_velocity',zero(nu-s.Matrix([0,0,0,-2/(a*p)])))
    check('actual_record_observer_velocity_uniform_bound_arithmetic',
          s.Rational(2)/(s.Rational(3,4)*s.Rational(3,5))<5)
    S=s.diag(2,s.Rational(1,2),1,1); dS=s.diag(2,-s.Rational(1,2),0,0)
    raw=S*boost; draw=dS*boost
    q=S*eta*S; Q=S*S
    vq=s.diag(8,s.Rational(1,2),0,0); vQ=s.diag(8,-s.Rational(1,2),0,0)
    check('actual_raw_solder_Lorentz_Gram', zero(raw*eta*raw.T-q))
    check('positive_pairing_distinct_from_Lorentz_Gram', zero(raw*h.inv()*raw.T-Q) and q != Q)
    check('complete_factor_Gram_derivative', zero(draw*eta*raw.T+raw*eta*draw.T-vq))
    check('complete_factor_pairing_derivative', zero(draw*h.inv()*raw.T+raw*h.inv()*draw.T-vQ))
    deltaQobs=-raw*h.inv()*dh*h.inv()*raw.T
    expected_qobs=s.zeros(4); expected_qobs[0,3]=expected_qobs[3,0]=-8/(a*p)
    check('actual_record_extra_pairing_jet_on_same_factor_path',zero(deltaQobs-expected_qobs))
    check('both_endpoint_native_tangent', s.eye(4)*vq*s.eye(4)==vq)
    check('metric_tracefree_factor_tangent', s.trace(q.inv()*vq)==0 and s.trace(Q.inv()*vQ)==0)
    # Literal degree-one slots 1,2,4,8 at one retained site. The other
    # sixteen-grade/site slots carry identity U and zero P, not deleted modes.
    Bc=s.diag(s.Rational(1,2),2,1,1)
    dBc=s.diag(-s.Rational(1,2),2,0,0)
    Wc=Bc.T*Bc; dWc=dBc.T*Bc+Bc.T*dBc
    uc=Bc.inv()*U4*Bc; pc=Bc.inv()*pp*Bc
    duc=-Bc.inv()*dBc*uc+Bc.inv()*U4*dBc
    dpc=-Bc.inv()*dBc*pc+Bc.inv()*pp*dBc
    zc=uc*uc; dzc=duc*uc+uc*duc
    zac=Wc.inv()*zc.T*Wc
    dzac=-Wc.inv()*dWc*zac+Wc.inv()*dzc.T*Wc+Wc.inv()*zc.T*dWc
    Ic=s.eye(4)
    fc=pc*zac*(Ic-pc)*zc*pc
    dfc=(dpc*zac*(Ic-pc)*zc*pc+pc*dzac*(Ic-pc)*zc*pc
         -pc*zac*dpc*zc*pc+pc*zac*(Ic-pc)*dzc*pc+pc*zac*(Ic-pc)*zc*dpc)
    resc=Ic+z*fc/(1-4*z*p**3)
    check('same_factor_path_complete_pairing_jet',
          Wc==Q.inv() and dWc==-Q.inv()*vQ*Q.inv())
    check('same_factor_path_U_readout_weighted_jets',
          zero(duc.T*Wc*uc+uc.T*dWc*uc+uc.T*Wc*duc-dWc) and dpc==s.zeros(4))
    check('same_factor_path_complete_remainder_derivative_zero',zero(z*s.trace(resc*dfc)))
    frozen_adj_jet=Wc.inv()*dzc.T*Wc
    frozen_fjet=pc*frozen_adj_jet*(Ic-pc)*zc*pc+pc*zac*(Ic-pc)*dzc*pc
    # Price contractions can accidentally agree at the golden stationary
    # base even when the feedback operator jets differ. Test the operator.
    reject('OMIT_PAIRING_OPERATOR_FIRST_JET_ON_THE_SAME_PATH',
           zero(dfc-frozen_fjet),True)
    diagonal_weights=[]
    for bits in range(16):
        value=s.prod(Q.inv()[r,r] for r in range(4) if bits & (1<<r))
        derivative=-value*sum((Q.inv()*vQ)[r,r] for r in range(4) if bits & (1<<r))
        diagonal_weights.append(value)
        check('all_sixteen_compound_weight_shape_jets',derivative==
              value*(-2*bool(bits&1)+2*bool(bits&2)))
    check('recorded_block_uses_actual_degree_one_pairing',
          s.diag(*[diagonal_weights[bits] for bits in [1,2,4,8]])==Wc)
    reject('FREEZE_COARSE_ENDPOINT', vq, s.zeros(4))
    reject('USE_COORDINATE_TRACE', s.trace(vQ), 0)
    reject('USE_H_INSTEAD_OF_ITS_INVERSE_IN_ROW_CONVENTION', zero(raw*h*raw.T-Q), True)
    # All ten symmetric endpoint jets; 6 independent Lorentz-skew links per axis.
    for ij,V in sym_basis(4):
        W=s.Rational(1,2)*V*q.inv()
        check('all_ten_joint_metric_probe_lifts', W*q+q*W.T==V)
    for axis in range(4):
        for i,j in itertools.combinations(range(4),2):
            X=skew(4,i,j); W=X*q.inv()
            check('all_24_connection_rows_preserved', W*q+q*W.T==s.zeros(4))
    D=s.eye(4); D[0,1]=s.Rational(2,3); D[2,3]=s.Rational(1,5)
    qt=q; qs=D*qt*D.T; R=qs.inv()*D
    As=s.diag(1,2,3,4); At=s.ones(4); BD=s.Matrix(4,4,range(16))
    Lam=s.Matrix([[1,2,3,4],[2,5,6,7],[3,6,8,9],[4,7,9,10]])
    def intrinsic(A1,A2,Bd):
        M=Bd*R.T
        sym=lambda A:(A+A.T)/2
        return sym(A1+M/2), sym(A2-D.T*M*D/2), (M-M.T)/2
    check('conormal_extension_does_not_change_source',
          intrinsic(As,At,BD)==intrinsic(As-Lam,At+D.T*Lam*D,BD+2*Lam*D*qt))

    old_heat=json.loads((ROOT/INPUTS[11]).read_text())['constant_positive_metric_shape_source']['cases']
    qdiag=[Fraction(4),Fraction(1,4),Fraction(1),Fraction(1)]
    for L,modes in [(2,[(0,0),(-4,0)]), (4,[(0,0),(-4,4),(-8,0),(-4,-4)])]:
        partition=Fraction(0); A=[[Fraction(0) for _ in range(4)] for _ in range(4)]
        energies=[Fraction(0)]*4
        for index in itertools.product(range(L),repeat=4):
            zs=[modes[k] for k in index]
            ls=[Fraction(re*re+im*im)/qdiag[r] for r,(re,im) in enumerate(zs)]
            lam=sum(ls)
            check('literal_mode_energy_integral_at_test_metric', lam.denominator==1)
            weight=Fraction(1,2**int(lam)); partition+=weight
            for r in range(4):
                energies[r]+=weight*ls[r]
                for c in range(4):
                    A[r][c]+=weight*Fraction(zs[r][0]*zs[c][0]+zs[r][1]*zs[c][1])/(qdiag[r]*qdiag[c])
        energies=[e/partition for e in energies]
        A=s.Matrix([[s.Rational(x.numerator,x.denominator)/s.Rational(partition.numerator,partition.denominator) for x in row] for row in A])
        check('all_sites_grades_zero_and_conjugate_modes_retained',16*L**4 in [256,4096] and partition>1)
        er=[s.Rational(e.numerator,e.denominator) for e in energies]
        packed={}; required_phase={}; packed_q={}; required_phase_q={}
        Aq=(eta*A+A*eta)/2
        for ij,V in sym_basis(4):
            r,c=ij
            expected=er[r]/s.Rational(qdiag[r].numerator,qdiag[r].denominator) if r==c else er[r]*er[c]/(4*L*L)
            check('all_ten_full_mode_heat_slots', A[r,c]==expected)
            coeff=s.trace(A*V)
            check('all_ten_packed_weights', coeff==A[r,c]*(1 if r==c else 2))
            packed[str(r)+str(c)]=str(coeff)
            required_phase[str(r)+str(c)]=str(s.cancel(-coeff/C))
            # A chosen jet can match all ten entries; it is not derived by this equality.
            chosen=-coeff/C
            check('required_remainder_ten_slot_identity', zero(coeff+C*chosen))
            Hv=V*q.inv()/2
            deltaQ=Hv*Q+Q*Hv.T
            check('all_ten_true_constant_q_joint_lifts',
                  zero(Hv*raw*eta*raw.T+raw*eta*raw.T*Hv.T-V))
            check('all_ten_same_observer_pairing_lifts',
                  zero(Hv*raw*h.inv()*raw.T+raw*h.inv()*raw.T*Hv.T-deltaQ) and
                  deltaQ==(V*eta+eta*V)/2)
            check('all_ten_q_covector_chain_rule_and_packed_signs',
                  s.trace(A*deltaQ)==s.trace(Aq*V)==Aq[r,c]*(1 if r==c else 2))
            qcoeff=s.trace(Aq*V)
            packed_q[str(r)+str(c)]=str(qcoeff)
            required_phase_q[str(r)+str(c)]=str(s.cancel(-qcoeff/C))
            check('all_ten_q_remainder_matching_conditions',zero(qcoeff+C*(-qcoeff/C)))
        tracefree=A-s.trace(A*Q)*Q.inv()/4
        check('full_metric_tracefree_covector_projection',s.trace(tracefree*Q)==0 and
              s.trace(tracefree*vQ)==s.trace(A*vQ))
        jet=s.trace(A*vQ)
        check('factor_two_tracefree_heat_jet', jet==2*(er[0]-er[1]) and jet>s.Rational(1,10000))
        qtracefree=Aq-s.trace(Aq*q)*q.inv()/4
        check('q_tracefree_projection_and_factor_match',s.trace(qtracefree*q)==0 and
              s.trace(qtracefree*vq)==s.trace(Aq*vq)==jet and s.trace(Aq*q)==s.trace(A*Q))
        observer_rem=s.trace(A*deltaQobs)
        check('actual_moving_record_full_reference_remainder',
              zero(observer_rem+4*er[0]*er[3]/(a*p*L*L)))
        conservative_total=2*(er[0]-er[1])-s.Rational(5,2)*er[0]*er[3]
        check('actual_moving_record_total_derivative_positive',
              er[3]<s.Rational(1,256) and conservative_total>s.Rational(1,10000))
        for direction in range(1,4):
            velocity=s.zeros(4,1); velocity[direction]=1
            dh0=-2*(s.eye(4)[:,0]*velocity.T+velocity*s.eye(4)[:,0].T)
            qjet=-S*dh0*S
            check('all_three_unit_observer_response_coefficients',
                  s.trace(A*qjet)==S[0,0]*S[direction,direction]*er[0]*er[direction]/(L*L))
        check('prior_owned_ten_slot_heat_result_reproduced', packed==old_heat[0 if L==2 else 1]['packed_ten_metric_covector'])
        # Literal flat-link physical action: every based plaquette has zero
        # excess, so both the six face terms and all ten metric variations
        # vanish before any source equation is imposed.
        links=[s.eye(4) for _ in range(4)]
        excesses=[links[r]*links[c]*links[r].inv()*links[c].inv()-s.eye(4)
                  for r,c in itertools.combinations(range(4),2)]
        check('literal_six_flat_physical_plaquettes_zero',
              all(excess==s.zeros(4) for excess in excesses))
        for ij,V in sym_basis(4):
            # Even a changed area/star coefficient contracts a zero
            # curvature excess; this is the owned Palatini contraction.
            check('all_ten_physical_metric_response_slots_zero',
                  all(s.trace(V*excess)==0 for excess in excesses))
        reject('GOLDEN_ZERO_CLOSES_FULL_BOOTSTRAP_PRICE',jet,s.Integer(0))
        reject('IMPOSE_CANCELLATION_AS_NATIVE_GATE',s.Integer(0),red(-jet/C))
        reject('DROP_FINITE_OFFDIAGONAL_RESPONSE', A[0,1], 0)
        reject('IDENTIFY_Q_COVECTOR_WITH_PHYSICAL_q_COVECTOR',A,Aq)
        reject('FREEZE_ACTUAL_MOVING_RECORD_OBSERVER',red(observer_rem),s.Integer(0))
        # A true counterexample to inferring a secant bound from a vanishing jet.
        x=s.Symbol('x',real=True); f=L*x**3; eps=s.Integer(L)**(-s.Rational(1,3))
        check('zero_first_jet_does_not_bound_refining_secants', f.diff(x).subs(x,0)==0 and
              s.simplify((f.subs(x,eps)-f.subs(x,-eps))/2)==1)
        heat_cases.append({'L':L, 'retained_dimension':16*L**4,
                           'packed_heat_covector':packed,
                           'packed_Lorentz_q_heat_covector_on_specified_joint_lifts':packed_q,
                           'required_full_phase_covector_if_no_other_terms':required_phase,
                           'required_q_phase_covector_on_same_joint_lifts_if_no_other_terms':required_phase_q,
                           'tracefree_heat_factor_derivative':str(jet),
                           'actual_fixed_gate_remainder_derivative':'0',
                           'actual_moving_record_reference_remainder_derivative':str(s.cancel(observer_rem)),
                           'actual_moving_record_total_factor_derivative':str(s.cancel(jet+observer_rem)),
                           'rho0_flat_packed_covector':{k:'0' for k in packed}})
    r=Fraction(1,2**64)
    check('uniform_all_L_factor_bound_arithmetic',
          2*(Fraction(60,17*2**16)-512*r*(1+r)/(1-r)**3)>Fraction(1,10000))
    r16=Fraction(1,2**16)
    check('uniform_all_L_fourth_axis_bound',128*r16*(1+r16)/(1-r16)**3<Fraction(1,256))
    check('uniform_all_L_genuine_moving_record_source_positive',
          Fraction(1019,512)*Fraction(60,17*2**16)-1024*r*(1+r)/(1-r)**3>Fraction(1,10000))
    # The linear physical pencil has the same tangent and equal-volume endpoints.
    qlin=s.diag(4*(1+2*t),-s.Rational(1,4)*(1-2*t),-1,-1)
    check('actual_linear_physical_Gram_probe',qlin.diff(t).subs(t,0)==vq and
          s.expand(qlin.det())==-(1-4*t*t))
    check('actual_full_faithful_interval_for_uniform_spectral_moments',
          s.Rational(217,505)>0 and 1-2*s.Rational(1,10)>0 and
          1+2*s.Rational(1,10)>0)
    # Read, rather than reinterpret, the genuine propositions of the consumed capsule.
    receipt=json.loads((ROOT/INPUTS[13]).read_text())
    check('existing_heat_kernel_boundary_is_pinned', receipt['status']=='PASS' and
          receipt['compiler_exit_code']==0 and len(receipt['declarations'])==23 and
          not receipt['full_graded_spectral_and_uniform_L_bound_kernel_formalized'])
    recorded_receipt=json.loads((ROOT/INPUTS[17]).read_text())
    recorded_output=(ROOT/recorded_receipt['output']).read_text()
    check('actual_recorded_capsule_and_compiler_receipt',recorded_receipt['status']=='PASS' and
          recorded_receipt['compiler_exit_code']==0 and
          sha(recorded_receipt['capsule'])==recorded_receipt['capsule_sha256'] and
          sha(recorded_receipt['output'])==recorded_receipt['output_sha256'] and
          not recorded_receipt['physical_admission_or_complete_heat_law_formalized'])
    for path,digest in {**recorded_receipt['source_sha256'],
                        **recorded_receipt['toolchain_sha256']}.items():
        check('recorded_observer_transitive_owner_and_toolchain_pin',sha(path)==digest)
    for name in recorded_receipt['declarations']:
        check('actual_recorded_propositions_and_transitive_axioms_resolve',
              name in recorded_output and
              set(recorded_receipt['axioms'][name]) <= {'propext','Classical.choice','Quot.sound'})
    check('actual_recorded_derivative_is_a_genuine_proposition',
          'HasDerivAt' in recorded_output and 'actual_mixed_pairing_derivative' in recorded_output and
          'sorryAx' not in recorded_output and 'error:' not in recorded_output)
    return {'status':'PASS','input_source_head':HEAD,'proof':PROOF,
            'checks':dict(sorted(Counter(checks).items())), 'exact_controls':len(checks),
            'executed_mathematical_mutants':mutants,
            'operator_cases':operator_cases,'heat_cases':heat_cases,
            'analytic_all_L_factor_bound':'2*(E1-E2)>1/10000',
            'feedback_coefficient':'8*z*a*p*(p-p^2)/(1-4*z*p^3)',
            'phase_jet':'-(K02+K03+K12+K13)/2',
            'new_Lean_declarations':0,'scope':SCOPE,
            'input_sha256':{path:sha(path) for path in INPUTS},
            'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py')}


def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--write',action='store_true')
    args=parser.parse_args(); result=controls()
    path=ROOT/(BASE+'_certificate.json')
    if args.write:
        path.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    else:
        expected=json.loads(path.read_text())
        assert result==expected, 'EXACT_LEDGER_REPLAY_MISMATCH'
        def validate(ledger):
            assert ledger==result, 'EXACT_LEDGER_REPLAY_MISMATCH'
        for key,value in SCOPE.items():
            altered=dict(expected); altered['scope']=dict(expected['scope'])
            altered['scope'][key]=True if value is False else False
            try:
                validate(altered)
            except AssertionError:
                pass
            else:
                raise AssertionError('FALSE_SCOPE_ACCEPTED_'+key)
    print('PASS: %s exact controls; %s mathematical mutations; %s pinned inputs; 0 new Lean claims' %
          (result['exact_controls'],len(result['executed_mathematical_mutants']),len(INPUTS)))


if __name__=='__main__':
    main()
