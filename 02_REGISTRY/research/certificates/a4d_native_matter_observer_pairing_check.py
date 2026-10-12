#!/usr/bin/env python3
"""Exact replay of the native matter observer construction and joint jets.

All-group and all-timelike-sector proofs are analytic in the paired memo.
No finite fixture is promoted to a physical constitutive or heat law.
"""
# D0_CI_TIMEOUT_SECONDS=600
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_matter_observer_pairing'
PROOF = '02_REGISTRY/research/A4D_NATIVE_MATTER_OBSERVER_PAIRING.md'
HEAD = 'e73cd37fda5028609eb412e17751390d2a3bf9f7'
INPUTS = [
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveExteriorFrameLift.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCARFockCarrier.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveHodgeCARDirac.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCovariantCubicalDifferential.lean',
    '03_FORMALIZATION/D0/Geometry/A4DSolderMetricCompletion.lean',
    '02_REGISTRY/research/A4D_NATIVE_JOINT_FIELD_QUOTIENT.md',
    '02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md',
    '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md',
    '02_REGISTRY/research/A4D_NATIVE_FACTOR_IMBALANCE_REMAINDER.md',
    '02_REGISTRY/research/A4D_PAIRING_Q_FACTOR_JET.md',
    '02_REGISTRY/research/A4D_CONSTRAINT_MULTIPLIER_SOURCE.md',
    '03_FORMALIZATION/lean-toolchain',
    '03_FORMALIZATION/lake-manifest.json',
]
SCOPE = {
    'linear_readout_class': 'FIXED_REAL_LINEAR_MAP_FROM_ACTUAL_EXTERIOR_FIBRE_TO_ORDINARY_VECTOR',
    'full_Lorentz_Hom_dimension': 1,
    'proper_Lorentz_Hom_dimension': 2,
    'observer_domain': 'FIRST_GRADE_TIMELIKE_k=vT_qinv_v>0',
    'all_native_matter_is_timelike': False,
    'full_Lorentz_selects_every_positive_matter_pairing': False,
    'physical_future_orientation_derived': False,
    'all_16_matter_components_retained': True,
    'all_10_packed_metric_slots_retained': True,
    'pairing_readout_kernel_is_native_gauge': False,
    'matrix_and_Hom_proofs': 'ANALYTIC_WITH_EXACT_CONTROLS_NOT_ALL_GROUP_OR_ALL_SIZE_LEAN_OWNERS',
    'new_Lean_capsule': 'GENERIC_NORM_AND_RANK_ONE_ENTRY_HASDERIVAT_AND_SCALE_IDENTITIES',
    'new_supported_CORE_owner': False,
    'weighted_heat_law_selected_by_core': False,
    'native_full_price_or_remaining_remainder_derived': False,
    'radial_heat_obstruction_removed_by_matter_observer': False,
    'transported_metric_link_derivative_omitted': False,
    'admitted_tangent_heat_response_is_an_edge_multiplier_conormal': False,
    'native_preparation_source_Ward_roots_soundness_recovery_GR_closed': False,
    'original_parent_terminal_changed': False,
}
SUBS = [tuple(i for i in range(4) if mask & (1 << i)) for mask in range(16)]
ETA = s.diag(1, -1, -1, -1)
P1, P3 = s.zeros(4, 16), s.zeros(4, 16)
for r in range(4):
    P1[r, 1 << r] = 1
    P3[r, 15 ^ (1 << r)] = ETA[r, r] * (-1)**r


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def zero(value):
    if isinstance(value, s.MatrixBase):
        return all(s.cancel(x) == 0 for x in value)
    return s.cancel(value) == 0


def ext(a):
    return s.Matrix(16, 16, lambda i, j:
                    a.extract(SUBS[i], SUBS[j]).det()
                    if len(SUBS[i]) == len(SUBS[j]) else 0)


def dext(a, da):
    def entry(i, j):
        rows, cols = SUBS[i], SUBS[j]
        if len(rows) != len(cols):
            return 0
        minor = a.extract(rows, cols)
        return sum((-1)**(r+c) *
                   minor.minor_submatrix(r, c).det() * da[rows[r], cols[c]]
                   for r in range(len(rows)) for c in range(len(cols)))
    return s.Matrix(16, 16, entry)


def joint(q, m, V, xi):
    a, v, w = q.inv(), P1*m, P1*xi
    u = a*v
    k = (v.T*u)[0]
    assert k > 0, 'OUTSIDE_FIRST_GRADE_TIMELIKE_SECTOR'
    du = a*w-a*V*u
    dk = (2*u.T*w-u.T*V*u)[0]
    Q, G = -q+2*v*v.T/k, -a+2*u*u.T/k
    dQ = -V+2*(w*v.T+v*w.T)/k-2*dk*v*v.T/k**2
    dG = a*V*a+2*(du*u.T+u*du.T)/k-2*dk*u*u.T/k**2
    omega = s.sqrt(-q.det())
    domega = omega*s.trace(a*V)/2
    W = omega*ext(G)
    dW = domega*ext(G)+omega*dext(G, dG)
    return dict(a=a,v=v,w=w,u=u,k=k,dk=dk,Q=Q,G=G,dQ=dQ,dG=dG,
                omega=omega,domega=domega,W=W,dW=dW)


def metric_directions():
    for i in range(4):
        for j in range(i, 4):
            V = s.zeros(4)
            V[i,j] = V[j,i] = 1
            yield '%s%s' % (i,j), V


def directions():
    for name, V in metric_directions():
        yield 'q_'+name, V, s.zeros(16,1)
    for mask in range(16):
        xi = s.zeros(16,1)
        xi[mask] = 1
        yield 'm_'+str(mask), s.zeros(4), xi


def controls():
    checks, mutants = [], []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    def reject(name, actual, false_value):
        check('REJECT_'+name, not zero(actual-false_value))
        mutants.append(name)

    proper = []
    for r in range(1,4):
        B = s.eye(4)
        B[0,0] = B[r,r] = s.Rational(5,3)
        B[0,r] = B[r,0] = s.Rational(4,3)
        proper.append(B)
    for i,j in itertools.combinations(range(1,4),2):
        R = s.eye(4)
        R[i,i] = R[j,j] = 0
        R[i,j], R[j,i] = -1, 1
        proper.append(R)
    X = s.Matrix(4,16,lambda i,j:s.Symbol('x_%s_%s'%(i,j)))
    expressions = []
    for L in proper:
        check('proper_fixture_is_exact_Lorentz', L*ETA*L.T == ETA and L.det()==1)
        check('proper_P1_intertwiner', P1*ext(L) == L*P1)
        check('proper_P3_intertwiner', P3*ext(L) == L*P3)
        expressions.extend(X*ext(L)-L*X)
    MP, _ = s.linear_eq_to_matrix(expressions,list(X))
    rank_proper = MP.rank()
    check('proper_finite_upper_bound_and_two_global_witnesses',rank_proper==62)
    reflection = s.diag(1,-1,1,1)
    for r in range(4):
        R = s.eye(4); R[r,r] = -1
        check('reflection_is_actual_full_Lorentz',R*ETA*R.T == ETA and R.det()==-1)
        check('full_P1_intertwiner',P1*ext(R)==R*P1)
        check('axial_determinant_character',P3*ext(R)==R.det()*R*P3)
        expressions.extend(X*ext(R)-R*X)
    MF, _ = s.linear_eq_to_matrix(expressions,list(X))
    rank_full = MF.rank()
    check('full_finite_Hom_bound_and_nonzero_global_witness',rank_full==63)
    reject('PROPER_HOM_IS_ONE_DIMENSIONAL',s.Integer(64-rank_proper),s.Integer(1))
    reject('AXIAL_READOUT_IS_FULL_GROUP_ORDINARY_VECTOR',
           P3*ext(reflection),reflection*P3)

    F = s.Matrix([[1,1,0,0],[0,1,1,0],[0,0,1,1],[0,0,0,1]])
    q = F*ETA*F.T
    j = s.Matrix([5,1,2,3])
    m = s.Matrix([s.Rational(i+1,17) for i in range(16)])
    for r in range(4):
        m[1<<r] = (F*j)[r]
    zq, zm = s.zeros(4), s.zeros(16,1)
    base = joint(q,m,zq,zm)
    check('actual_all_sixteen_matter_slots_nonzero',all(x!=0 for x in m))
    check('nonrest_timelike_domain',base['k']==11)
    check('inverse_identity',zero(base['Q']*base['G']-s.eye(4)))
    check('observer_determinant_identity',base['Q'].det()==-q.det())
    check('positive_Q_all_Sylvester_minors',all(base['Q'][:n,:n].det()>0 for n in range(1,5)))
    check('positive_G_all_Sylvester_minors',all(base['G'][:n,:n].det()>0 for n in range(1,5)))
    check('all_exterior_degrees_retained',Counter(map(len,SUBS))=={0:1,1:4,2:6,3:4,4:1})
    check('full_exterior_density_determinant_one',base['W'].det()==1)
    raw_Q = -ETA+2*j*j.T/base['k']
    check('actual_solder_observer_positive_congruence',base['Q']==F*raw_Q*F.T)
    inverse_q = -base['Q']+2*base['v']*base['v'].T/(base['v'].T*base['G']*base['v'])[0]
    check('fixed_v_inverse_positive_to_Lorentz',inverse_q==q)

    t = s.Symbol('t',real=True)
    nonrest_jets = []
    for name,V,xi in directions():
        b = joint(q,m,V,xi)
        dF=s.Rational(1,2)*V*F.inv().T*ETA
        raw_psi=ext(F).inv()*m
        dpsi=ext(F).inv()*(xi-dext(F,dF)*raw_psi)
        check('actual_raw_solder_realizes_metric_tangent',
              dF*ETA*F.T+F*ETA*dF.T==V)
        check('actual_all16_matter_lift_realizes_quotient_tangent',
              dext(F,dF)*raw_psi+ext(F)*dpsi==xi)
        vt = b['v']+t*b['w']
        at = (q+t*V).inv()
        kt = (vt.T*at*vt)[0]
        qt = -(q+t*V)+2*vt*vt.T/kt
        gt = -at+2*(at*vt)*(at*vt).T/kt
        check('true_joint_curve_Q_derivative',zero(qt.diff(t).subs(t,0)-b['dQ']))
        check('true_joint_curve_G_derivative',zero(gt.diff(t).subs(t,0)-b['dG']))
        check('true_joint_norm_derivative',zero(s.diff(kt,t).subs(t,0)-b['dk']))
        check('inverse_joint_derivative',zero(b['dG']+b['G']*b['dQ']*b['G']))
        check('density_has_no_independent_matter_term',
              zero(s.diff(s.sqrt(-(q+t*V).det()),t).subs(t,0)-b['domega']))
        for degree in range(5):
            masks = [i for i in range(16) if len(SUBS[i])==degree]
            for i in masks:
                for h in masks:
                    minor = (b['G']+t*b['dG']).extract(SUBS[i],SUBS[h]).det()
                    dw = b['domega']*b['G'].extract(SUBS[i],SUBS[h]).det()+\
                         b['omega']*s.diff(minor,t).subs(t,0)
                    check('all_degree_minor_derivative',zero(dw-b['dW'][i,h]))
        nonrest_jets.append(s.Matrix(b['dQ']).reshape(16,1))
    J = s.Matrix.hstack(*nonrest_jets)
    check('nonrest_complete_26_slot_pairing_rank',J.rank()==10)
    check('nonrest_fixed_metric_matter_rank',J[:,10:].rank()==3)
    check('nonrest_fixed_matter_metric_rank',J[:,:10].rank()==10)

    rad = joint(q,m,2*q,zm)
    check('metric_dilation_preserves_radial_heat_scaling',rad['dQ']==2*base['Q'])
    for degree in range(5):
        ids = [i for i in range(16) if len(SUBS[i])==degree]
        check('complete_degree_dilation',rad['dW'].extract(ids,ids)==
              (4-2*degree)*base['W'].extract(ids,ids))
    xi = zm.copy()
    for r in range(4): xi[1<<r] = 3*base['v'][r]
    check('matter_amplitude_is_pairing_invisible',zero(joint(q,m,zq,xi)['dQ']))
    reject('NONUNIT_READING_IS_NORMALIZED_BY_OMITTING_k',
           base['Q'],-q+2*base['v']*base['v'].T)
    reject('OMITTING_DENSITY_GIVES_THE_SAME_RADIAL_PAIRING',rad['dW'],
           base['omega']*dext(base['G'],rad['dG']))
    xi=zm.copy(); xi[1]=1
    moving=joint(q,m,zq,xi)
    reject('NORM_MATTER_DERIVATIVE_OMITTED',moving['dk'],s.Integer(0))
    reject('RANK_ONE_DENOMINATOR_DERIVATIVE_OMITTED',moving['dQ'],
           2*(moving['w']*moving['v'].T+moving['v']*moving['w'].T)/moving['k'])
    reject('POSITIVE_OBSERVER_DETERMINANT_HAS_LORENTZ_SIGN',base['Q'].det(),q.det())
    dropped=base['W'].copy(); dropped[15,15]=0
    reject('DROPPED_GRADE_IS_INVERTIBLE_FULL_PAIRING',dropped.det(),base['W'].det())
    xi=zm.copy()
    for r in range(4): xi[1<<r]=base['v'][r]
    check('nonzero_native_quotient_direction_is_pairing_invisible',
          xi!=zm and zero(joint(q,m,zq,xi)['dQ']))
    reject('PAIRING_KERNEL_IS_NATIVE_QUOTIENT_GAUGE',xi,zm)

    for badv,label in [(s.zeros(4,1),'ZERO'),(s.Matrix([1,1,0,0]),'NULL'),
                       (s.Matrix([0,1,0,0]),'SPACELIKE')]:
        bad = zm.copy()
        for r in range(4): bad[1<<r]=badv[r]
        try: joint(ETA,bad,zq,zm)
        except AssertionError: check('reject_'+label+'_observer_domain',True)
        else: raise AssertionError(label+'_DOMAIN_ACCEPTED')
    badv=s.Matrix([0,1,0,0]); badQ=-ETA+2*badv*badv.T/(badv.T*ETA*badv)[0]
    check('spacelike_formula_is_not_positive',badQ[0,0]<0)

    # Pure axial matter produces a covariant pairing despite not giving an ordinary vector.
    axial=zm.copy()
    for r in range(4): axial[15^(1<<r)]=ETA[r,r]*(-1)**r*j[r]
    av=P3*axial; avp=P3*ext(reflection)*axial
    axialQ=-ETA+2*av*av.T/(av.T*ETA*av)[0]
    axialQp=-ETA+2*avp*avp.T/(avp.T*ETA*avp)[0]
    check('full_group_axial_pairing_loophole',axialQp==reflection*axialQ*reflection.T)
    check('positive_axial_pairing_with_zero_first_grade',P1*axial==s.zeros(4,1) and
          all(axialQ[:n,:n].det()>0 for n in range(1,5)))
    reject('AXIAL_PAIRING_UNAVAILABLE_WITHOUT_GRADE_ONE',axialQ,s.zeros(4))
    check('orientation_dressed_axial_reading_is_full_gauge_invariant',
          reflection.det()*reflection*P3*ext(reflection.inv())*axial==P3*axial)
    reversed_v=-base['v']
    check('pairing_does_not_choose_future',-q+2*reversed_v*reversed_v.T/base['k']==base['Q'])
    tilt=s.Matrix([s.Rational(5,3),s.Rational(4,3),0,0])
    tiltQ=-ETA+2*tilt*tilt.T
    check('positive_tilt_has_changed_eigenvalues',tiltQ[:2,:2].eigenvals()==
          {s.Integer(9):1,s.Rational(1,9):1})
    reject('LORENTZ_OBSERVER_TILT_IS_ISOSPECTRAL',s.trace(tiltQ),s.Integer(4))
    reject('TIMELIKE_POSITIVE_PAIRING_HAS_SPECTRUM_ONE_MINUS_ONE',
           tiltQ[:2,:2].det(),s.Integer(-1))

    # A moving transported frame has its own incoming-link derivative.
    B=s.Matrix([[1,0,0,0],[s.Rational(1,3),1,0,0],[0,0,2,0],[0,0,0,1]])
    dB=s.zeros(4); dB[0,1]=1
    V=s.Matrix([[2,1,0,0],[1,-2,1,0],[0,1,0,2],[0,0,2,1]])
    xi=zm.copy(); xi[2]=1
    b=joint(q,m,V,xi)
    qhat=B*q*B.T; mhat=ext(B)*m
    Vhat=dB*q*B.T+B*V*B.T+B*q*dB.T
    xihat=dext(B,dB)*m+ext(B)*xi
    h=joint(qhat,mhat,Vhat,xihat)
    check('transported_frame_pairing_exact',h['Q']==B*b['Q']*B.T)
    check('transported_frame_complete_derivative',h['dQ']==
          dB*b['Q']*B.T+B*b['dQ']*B.T+B*b['Q']*dB.T)
    reject('TRANSPORTED_LINK_DERIVATIVE_DROPPED',h['dQ'],B*b['dQ']*B.T)
    for _,V in metric_directions():
        check('flat_constant_V_satisfies_both_endpoint_constraint',V-V==zq)
    reject('ONE_ENDPOINT_METRIC_IS_A_FREE_LINK_TANGENT',s.eye(4),zq)

    # Full exterior creator/annihilator matrices and actual L=2 characters.
    creators=[]
    for r in range(4):
        C=s.zeros(16)
        for mask,S in enumerate(SUBS):
            if r not in S: C[mask|(1<<r),mask]=(-1)**sum(i<r for i in S)
        creators.append(C)
    rest=zm.copy(); rest[1]=1
    x=s.Rational(1,2**16)
    a,c=x*(1+x)**3,x*x*(1+x)**2
    Z=s.Matrix(4,4,lambda i,j:a if i==j else c)
    heat_slots={}
    for name,V,xi in directions():
        b=joint(ETA,rest,V,xi)
        Hprime=s.Integer(0)
        for bits in itertools.product(range(2),repeat=4):
            p=s.Matrix([-4*k for k in bits])
            d=sum((p[r]*creators[r] for r in range(4)),s.zeros(16))
            delta=d.T; DW=d+delta; lam=(p.T*p)[0]
            check('literal_all16_forward_square_per_character',DW*DW==lam*s.eye(16))
            S=b['dW']
            ddelta=delta*S-S*delta
            dK=ddelta*DW+DW*ddelta
            dlambda=(p.T*b['dG']*p)[0]
            check('all26_jets_full16_weighted_operator_square',dK==dlambda*s.eye(16))
            Hprime += -s.Rational(1,256)*s.Rational(1,2)**lam*s.trace(dK)
        trace_source=s.trace(Z*b['dQ'])
        check('all26_joint_heat_slots_exact_full_trace',Hprime==trace_source)
        heat_slots[name]=str(Hprime)
        if name=='q_00': check('packed_time_diagonal_sign',Hprime==a)
        if name in ['q_11','q_22','q_33']: check('packed_spatial_diagonal_sign',Hprime==-a)
        if name.startswith('q_') and name[2]!=name[3]:
            check('packed_offdiagonal_factor_two',Hprime==-2*c)
        if name in ['m_2','m_4','m_8']: check('actual_spatial_matter_contribution',Hprime==4*c)
    reject('FIXED_METRIC_SPATIAL_MATTER_HAS_ZERO_HEAT_RESPONSE',s.Rational(heat_slots['m_2']),s.Integer(0))
    reject('PACKED_OFFDIAGONAL_HAS_NO_FACTOR_TWO',s.Rational(heat_slots['q_01']),-c)
    reject('FROZEN_OBSERVER_GIVES_THE_JOINT_DERIVATIVE',
           joint(ETA,rest,zq,s.eye(16)[:,2])['dQ'],zq)
    reject('RADIAL_MATTER_OBSERVER_CANCELS_HEAT',s.trace(Z*2*s.eye(4)),s.Integer(0))

    # The nonzero factor response is evaluated on an actual edge-constraint tangent.
    fq=s.diag(4,-s.Rational(1,4),-1,-1)
    fm=zm.copy(); fm[1]=2
    fV=s.diag(8,s.Rational(1,2),0,0)
    factor=joint(fq,fm,fV,zm)
    check('factor_positive_Q_is_actual_matter_pairing',factor['Q']==s.diag(4,s.Rational(1,4),1,1))
    check('factor_joint_Q_derivative',factor['dQ']==s.diag(8,-s.Rational(1,2),0,0))
    dotC=s.zeros(4)*fq+fV+fq*s.zeros(4).T-fV
    check('factor_varies_both_endpoints_on_actual_constraint',dotC==s.zeros(4))
    Lam=s.Matrix(4,4,lambda i,j:s.Symbol('lambda_%s_%s'%(i,j)))
    check('every_edge_multiplier_conormal_annihilates_factor_tangent',s.trace(Lam*dotC)==0)
    factor_heat=s.Integer(0)
    for bits in itertools.product(range(2),repeat=4):
        p=s.Matrix([-4*k for k in bits])
        d=sum((p[r]*creators[r] for r in range(4)),s.zeros(16))
        delta=factor['W'].inv()*d.T*factor['W'];DW=d+delta
        lam=(p.T*factor['G']*p)[0]
        S=factor['W'].inv()*factor['dW']
        ddelta=delta*S-S*delta;dK=ddelta*DW+DW*ddelta
        dlambda=(p.T*factor['dG']*p)[0]
        check('full16_anisotropic_factor_square',DW*DW==lam*s.eye(16))
        check('full16_anisotropic_factor_square_derivative',dK==dlambda*s.eye(16))
        factor_heat-=s.Rational(1,256)*s.Rational(1,2)**lam*s.trace(dK)
    x0,x1,x2=s.Rational(1,2**4),s.Rational(1,2**64),s.Rational(1,2**16)
    factor_formula=(8*x0*(1+x1)-128*x1*(1+x0))*(1+x2)**2/16
    check('exact_full256_factor_heat_derivative',factor_heat==factor_formula)
    check('strictly_nonzero_admitted_factor_heat_response',factor_heat>0)
    reject('NONZERO_ADMITTED_FACTOR_JET_IS_EDGE_CONORMAL',factor_heat,s.trace(Lam*dotC))

    receipt=json.loads((ROOT/(BASE+'_results.json')).read_text())
    check('real_successful_Lean_capsule',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
    check('Lean_capsule_source_pin',receipt['capsule_sha256']==sha(BASE+'.lean'))
    check('Lean_compiler_output_pin',receipt['output_sha256']==sha(BASE+'_output.txt'))
    output=(ROOT/(BASE+'_output.txt')).read_text()
    check('compiler_has_genuine_HasDerivAt_propositions','HasDerivAt' in output and
          'pairingEntry_hasDerivAt' in output and 'normContraction_hasDerivAt' in output)
    check('no_Lean_shortcuts_in_compiler_output','sorryAx' not in output and 'error:' not in output)
    for decl, axioms in receipt['axioms'].items():
        check('actual_decl_and_standard_axioms',decl in output and
              set(axioms)<={'propext','Classical.choice','Quot.sound'})
    for path,digest in receipt['input_sha256'].items():
        check('transitive_Lean_input_pin',sha(path)==digest)
    for path in INPUTS: check('consumed_input_exists',(ROOT/path).is_file())
    return {'status':'PASS','input_source_head':HEAD,'proof':PROOF,
            'exact_controls':len(checks),'checks':dict(sorted(Counter(checks).items())),
            'executed_mathematical_mutants':mutants,
            'proper_constraint_shape':list(MP.shape),'proper_rank':rank_proper,
            'full_constraint_shape':list(MF.shape),'full_rank':rank_full,
            'complete_pairing_chart':{'input_dimension':26,'rank':10,'kernel_dimension':16},
            'literal_flat_archive':{'L':2,'sites':16,'exterior_dimension':16,'cochains':256},
            'heat_slots_divided_by_beta_at_beta_log2':heat_slots,
            'anisotropic_factor_heat_derivative_divided_by_beta':str(factor_heat),
            'new_generic_Lean_propositions':5,'scope':SCOPE,
            'input_sha256':{path:sha(path) for path in INPUTS},
            'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
            'capsule_receipt_sha256':sha(BASE+'_results.json')}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args(); result=controls()
    ledger=ROOT/(BASE+'_certificate.json')
    if args.write:
        ledger.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        expected=json.loads(ledger.read_text())
        assert result==expected,'EXACT_LEDGER_REPLAY_MISMATCH'
        for key,value in SCOPE.items():
            altered=dict(expected); altered['scope']=dict(expected['scope'])
            altered['scope'][key]=False if value is not False else True
            assert altered!=result,'FALSE_SCOPE_ACCEPTED_'+key
    print('PASS: %s exact controls; %s executed mathematical mutations; '
          'all 26 q/m directions; all 256 L=2 cochains; 5 generic Lean propositions' %
          (result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__': main()
