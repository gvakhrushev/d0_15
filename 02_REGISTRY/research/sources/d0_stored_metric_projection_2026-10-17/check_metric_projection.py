#!/usr/bin/env python3
"""Regular stored-adjoint metric projection and its generic source residual.

This is a bounded exact consumer, not a mode/rank census. Only pinned
literal CAR definitions are executed. No old checker, root search or Lean
build is run. F=I+J is a NONROOT kinematic fixture, not a Julia admission.

For Q=F eta F^T, tau=F n and n^T eta n=1, put lambda=Q^-1 tau.
Then tau^T Q^-1 tau=1 and S=tau tau^T-Q is PSD of rank3 with
ker S=span(lambda). In the regular stratum a metric is realized by the
full stored-adjoint joint class exactly when one can choose such a tau
whose own-r tau_r and Q_rr are constant along each own-r line. A smooth
rank3 Gram factor S=W^T W gives u_r=(tau_r,w_r); SO3 own-leg alignment
plus its free SO2 angle gives every link, and arbitrary moving observers
are restored by the canonical Lorentz whitening. This is an existence
criterion with an auxiliary line-constant tau, not arbitrary-metric IFT.

On a full-support Fourier mode the exact tangent equations include
H_rr=0 and lambda^T H lambda=0. Their conormal is
Diag(d)+c lambda lambda^T. Put a=Qk and s=tau.k=lambda.a. If every a_i
is nonzero, its Bianchi-compatible part is the single nonzero line
Eres=lambda lambda^T-s Diag(lambda_i/a_i).
The fixed-background, momentum-independent row
Poff=lambda lambda^T-Diag(lambda_i^2) separates this line by
Tr(Eres Poff)=sum_(i!=j) lambda_i^2 lambda_j^2>0.
Poff itself is FORBIDDEN by the full-support stored tangent. Thus this
identifies a physical extra-source obligation, not an added native row.
Exceptional a_i=0 must be treated directly and need not be completed by
Poff. Nothing here selects the native action, source/GR identification,
physical observer/preparation, or a refinement trajectory.
"""

from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
ETA = s.diag(1,-1,-1,-1)
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
LEAN = '03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean'
PINS = {
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    LEAN: '2ccca18cf8ca66b9e1aa020301ce0d84d6fcd12563e913323482ce139928e5fe',
    '02_REGISTRY/research/A4D_NATIVE_FULL_JOINT_KERNEL_AND_MATTER_REDUCTION.md':
        'cc533dc7c8d63442f9e3e52fc984d32dba4cd2e4f5f8f9c164ac46afbbfd4f20',
    '02_REGISTRY/research/A4D_COMPLETE_EXIT_ACTION_AND_SECOND_SOURCE.md':
        '482cf99f280620e7aa6120432cd7b9764671c5ef3fb1c0c3b50d7228d66e08b3',
}


def _creators(repo):
    tree = ast.parse((repo/CURVED).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node,ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node,ast.Assign) and any(isinstance(t,ast.Name)
              and t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('metric_projection:literal_creator_definition_nodes')
    scope = {'s':s,'lru_cache':lru_cache}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),CURVED,'exec'),scope)
    return [scope['creator'](r) for r in range(4)],scope['EXTERIOR_ORDER']


def _zero(value):
    values = list(value) if isinstance(value,s.MatrixBase) else (value,)
    return all(s.cancel(s.expand(x)) == 0 for x in values)


def canonical_whitening(n):
    """Positive Lorentz L on the future chart, L n=e0."""
    v = n[1:4,:]
    return s.BlockMatrix([[s.Matrix([[n[0]]]),-v.T],
                          [-v,s.eye(3)+v*v.T/(1+n[0])]]).as_explicit()


def rest_metric(tau,W):
    return tau*tau.T-W.T*W


def fixed_spatial_factor_reconstruction(Q,tau,reference):
    """The exact local Gram/Schur reconstruction in this two-endpoint test.

    Contract: reference is the 3x3 factor of S_{I,I}, I=(1,2,3). A general
    nearby S uses its own smooth Cholesky factor, not this fixed factor.
    """
    S = tau*tau.T-Q
    indices = (1,2,3)
    block = S.extract(indices,indices)
    if reference.det() == 0 or not _zero(reference.T*reference-block):
        raise ArithmeticError('metric_projection:wrong_spatial_reference_factor')
    w0 = reference.T.inv()*S.extract(indices,(0,))
    W = w0.row_join(reference)
    if not _zero(W.T*W-S):
        raise ArithmeticError('metric_projection:nonzero_Gram_Schur_defect')
    return W


def generic_bianchi_residual(Q,tau,k):
    """Full-support regular source residual; requires all (Qk)_i!=0."""
    lam, a = Q.inv()*tau,Q*k
    if any(x == 0 for x in a):
        raise ValueError('exceptional zero component of Qk requires direct equations')
    scalar = (tau.T*k)[0]
    return lam*lam.T-scalar*s.diag(*(lam[i]/a[i] for i in range(4)))


def offdiagonal_completion(lam):
    return lam*lam.T-s.diag(*(x*x for x in lam))


def linearized_einstein(Q,h,k):
    """Owned sphere-positive convention, covariant h exp(i k.x)."""
    g,kup = Q.inv(),Q*k
    k2 = (k.T*Q*k)[0]
    htr,kh = s.trace(Q*h),kup.T*h
    ric = (k2*h+k*k.T*htr-k*kh-kh.T*k.T)/2
    return ric-g*s.trace(Q*ric)/2


def _exterior_from_creators(A,C,order):
    """Full Lambda(A) in the literal ACDB mask basis, by all16 columns."""
    vacuum = s.eye(16)[:,0]
    images = [sum((A[j,r]*C[j] for j in range(4)),s.zeros(16)) for r in range(4)]
    columns = []
    for mask in range(16):
        vector = vacuum
        for r in reversed(order):
            if mask & (1 << r):
                vector = images[r]*vector
        columns.append(vector)
    return s.Matrix.hstack(*columns)


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition,name):
        if not bool(condition):
            raise ArithmeticError('metric_projection:'+name)
        checks.append(name)

    def eq(actual,expected,name):
        require(_zero(actual-expected),name)

    for path,digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_'+Path(path).name)

    I4,I3 = s.eye(4),s.eye(3)
    n = I4[:,0]
    F = I4+s.ones(4)
    Q = F*ETA*F.T
    V = ETA*F.T
    tau,W = F*n,V[1:4,:]
    lam = Q.inv()*tau
    eq(tau,s.Matrix([2,1,1,1]),'nonroot_regular_fixture_time_legs')
    eq(lam,s.Matrix([4,-1,-1,-1])/5,'normalized_Gram_null_vector')
    eq(W*lam,s.zeros(3,1),'spatial_Gram_null_relation')
    eq((tau.T*lam)[0],1,'unit_observer_dual_constraint')
    eq(tau*tau.T-Q,W.T*W,'positive_rank3_spatial_Gram_identity')
    require(F.det() == 5 and W[:,1:4].det() != 0,
            'fixture_invertible_and_regular_spatial_reference')

    # One real edge, not a Fourier/mode census. Only w0 rotates and tau1
    # changes; own-r=0 time and Minkowski norm are preserved exactly.
    parameter = s.symbols('t',real=True)
    R = s.Matrix([[(1-parameter**2)/(1+parameter**2),-2*parameter/(1+parameter**2),0],
                  [2*parameter/(1+parameter**2),(1-parameter**2)/(1+parameter**2),0],
                  [0,0,1]])
    Rrat = R.subs(parameter,s.Rational(1,10))
    Wy = W.copy()
    Wy[:,0] = Rrat*W[:,0]
    tauy = s.Matrix([2,s.Rational(11,10),1,1])
    Qy = rest_metric(tauy,Wy)
    Vy = tauy.T.col_join(Wy)
    Fy = Vy.T*ETA
    eq(Rrat.T*Rrat,I3,'rational_stereographic_SO3_rotation')
    eq(Rrat.det(),1,'proper_rotation_determinant')
    eq(Qy[0,0],Q[0,0],'own_edge_Minkowski_norm_exactly_preserved')
    eq(tauy[0],tau[0],'own_edge_observer_leg_scalar_exactly_preserved')
    require(Qy != Q and tauy[1] != tau[1],
            'nonconstant_metric_and_other_time_leg_retained')
    reconstructed = fixed_spatial_factor_reconstruction(Qy,tauy,W[:,1:4])
    eq(reconstructed,Wy,'exact_fixed_reference_Gram_reconstruction')
    S = tauy*tauy.T-Qy
    block = S[1:4,1:4]
    eq(S[0,0]-(S[0,1:4]*block.inv()*S[1:4,0])[0],0,
       'rank3_positive_Gram_Schur_identity')
    eq(Fy*ETA*Fy.T,Qy,'reconstructed_full_frame_metric')
    require(Fy.det() != 0,'reconstructed_full_frame_invertible')
    lamy = Qy.inv()*tauy
    eq((tauy.T*lamy)[0],1,'moving_endpoint_unit_observer_constraint')
    eq(S*lamy,s.zeros(4,1),'moving_endpoint_Gram_null_relation')

    A0 = s.diag(1,Rrat.T)
    eq(A0.T*ETA*A0,ETA,'actual_own_edge_link_Lorentz')
    eq(A0.det(),1,'actual_own_edge_link_proper')
    eq(A0*n,n,'actual_own_edge_link_future_observer_transport')
    eq(A0*Vy[:,0],V[:,0],'actual_own_edge_link_full_leg_transport')

    # This representation does not freeze observers. Restore two independent
    # positive future observers by exact canonical-whitening conjugation.
    nx = s.Matrix([s.Rational(5,4),s.Rational(3,4),0,0])
    ny = s.Matrix([s.Rational(13,12),0,s.Rational(5,12),0])
    Lx,Ly = canonical_whitening(nx),canonical_whitening(ny)
    moving_A = Lx.inv()*A0*Ly
    eq(Lx*nx,n,'moving_source_observer_whitening')
    eq(Ly*ny,n,'moving_target_observer_whitening')
    eq(moving_A.T*ETA*moving_A,ETA,'moving_observer_link_remains_Lorentz')
    eq(moving_A*ny,nx,'moving_observer_pair_transport_not_frozen')
    eq(moving_A*(Ly.inv()*Vy[:,0]),Lx.inv()*V[:,0],
       'moving_observer_own_leg_transport_not_frozen')
    eq((Lx.inv()*V).T*ETA*(Lx.inv()*V),Q,
       'moving_observer_restoration_does_not_change_metric')

    # Complete all16 exterior transport from pinned creation definitions.
    C,order = _creators(repo)
    require(order == (0,2,3,1),'literal_ACDB_mask_order')
    eq(_exterior_from_creators(I4,C,order),s.eye(16),
       'full16_exterior_identity_all_degrees_including_vacuum_top')
    EA = _exterior_from_creators(A0,C,order)
    eq(EA.H*EA,s.eye(16),'full16_rest_positive_pairing_transport')
    create_x = sum((V[j,0]*C[j] for j in range(4)),s.zeros(16))
    create_y = sum((Vy[j,0]*C[j] for j in range(4)),s.zeros(16))
    eq(EA*create_y,create_x*EA,'full16_actual_own_leg_creator_intertwiner')
    eq(EA*create_y.H,create_x.H*EA,'full16_actual_own_leg_contraction_intertwiner')
    grade = s.diag(*(bin(mask).count('1') for mask in range(16)))
    eq(EA*grade,grade*EA,'all16_grades_retained_without_grade_cut')

    # Invariant negative controls; no convenient restricted link search.
    bad_time = Vy[:,0]+s.Rational(1,20)*n
    require((n.T*ETA*bad_time)[0] != tau[0],
            'changed_own_time_scalar_forbids_any_pair_preserving_Lorentz_link')
    bad_norm = tauy[0]*n+s.Matrix([0,*((s.Rational(21,20))*Wy[:,0])])
    require((bad_norm.T*ETA*bad_norm)[0] != Q[0,0],
            'changed_own_Minkowski_norm_forbids_any_Lorentz_link')
    badQ = Qy.copy()
    badQ[0,0] += s.Rational(1,100)
    rejected = False
    try:
        fixed_spatial_factor_reconstruction(badQ,tauy,W[:,1:4])
    except ArithmeticError:
        rejected = True
    require(rejected,'nonzero_Gram_Schur_defect_is_rejected')

    # A nonzero actual full-support tangent, with constant tau and every
    # own-leg length fixed. Other metric rows need not be diagonal/free.
    Wcurve = W.copy()
    Wcurve[:,0] = R*W[:,0]
    dW = Wcurve.diff(parameter).subs(parameter,0)
    H = -(dW.T*W+W.T*dW)
    require(H != s.zeros(4),'admissible_tangent_changes_metric_not_common_Lorentz_gauge')
    require(all(H[i,i] == 0 for i in range(4)),
            'full_support_admissible_tangent_all_diagonal_locks')
    eq((lam.T*H*lam)[0],0,'full_support_admissible_tangent_fifth_Gram_lock')

    # Generic symbolic structure, rather than computing ranks over modes.
    av = s.Matrix(s.symbols('a0:4',nonzero=True))
    lv = s.Matrix(s.symbols('l0:4',real=True))
    scalar = (lv.T*av)[0]
    Egen = lv*lv.T-scalar*s.diag(*(lv[i]/av[i] for i in range(4)))
    eq(Egen*av,s.zeros(4,1),'generic_Bianchi_residual_structural_identity')
    entries = s.symbols('H0:10')
    Hgen = s.zeros(4)
    index = 0
    for i in range(4):
        for j in range(i,4):
            Hgen[i,j] = Hgen[j,i] = entries[index]
            index += 1
    eq(s.trace(Egen*Hgen),(lv.T*Hgen*lv)[0]
       -scalar*sum(lv[i]*Hgen[i,i]/av[i] for i in range(4)),
       'generic_source_pairing_including_offdiagonal_factor_two')
    Pgen = offdiagonal_completion(lv)
    positive_pairing = sum(lv[i]**2*lv[j]**2 for i in range(4) for j in range(4) if i != j)
    eq(s.trace(Egen*Pgen),positive_pairing,
       'one_momentum_independent_offdiagonal_completion_structural_identity')
    eq((lv.T*Pgen*lv)[0],positive_pairing,
       'completion_row_is_forbidden_by_native_fifth_constraint')

    k = s.ones(4,1)
    a = Q*k
    Eres = generic_bianchi_residual(Q,tau,k)
    Poff = offdiagonal_completion(lam)
    eq(Eres*a,s.zeros(4,1),'nonnull_rational_fixture_Bianchi')
    eq(s.trace(Eres*H),0,'actual_admitted_tangent_cannot_detect_residual_source')
    eq(s.trace(Q*Eres),s.Rational(14,5),'conformal_pairing_at_generic_fixture')
    eq(s.trace(Eres*Poff),s.Rational(102,625),
       'fixed_offdiagonal_row_strictly_separates_generic_residual')
    require(any(Q[i,i] != 0 for i in range(4)),
            'conformal_metric_probe_is_not_a_full_support_native_tangent')
    eq((k.T*Q*k)[0],-50,'nonnull_fixture_not_a_characteristic_wave')
    barh = 2*Eres/(k.T*Q*k)[0]
    h = barh-Q.inv()*s.trace(Q*barh)/2
    eq((Q*k).T*barh,s.zeros(1,4),'actual_linearized_Einstein_harmonic_gauge')
    eq(linearized_einstein(Q,h,k),Eres,
       'residual_is_an_actual_linearized_Einstein_source_not_arbitrary_matrix')
    dh = -Q.inv()*Hgen*Q.inv()
    eq(Q*dh+Hgen*Q.inv(),s.zeros(4),
       'inverse_metric_derivative_sign_Q_equals_g_inverse')

    # A zero component of Qk is a real exception, even with all k_i!=0.
    # Poff cannot see the resulting residual diagonal covector.
    a_exception = s.Matrix([0,1,1,1])
    k_exception = Q.inv()*a_exception
    E_exception = s.diag(1,0,0,0)
    require(all(value != 0 for value in k_exception),
            'exceptional_Qk_can_have_full_support_k')
    eq(E_exception*(Q*k_exception),s.zeros(4,1),
       'exceptional_diagonal_source_survives_Bianchi')
    eq(s.trace(E_exception*Poff),0,
       'fixed_offdiagonal_completion_not_claimed_on_exceptional_Qk')

    return {
        'status':'PASS','exact_checks':len(checks),'checks':checks,'source_pins':PINS,
        'fixture':'F=I+J, nonstationary nonroot kinematic fixture; not a Julia admission',
        'nonlinear_projection':{
            'variables':'Q=F eta F^T, tau=Fn, lambda=Q^-1 tau',
            'pointwise':'tau^T Q^-1 tau=1; tau tau^T-Q=W^T W, PSD rank3',
            'edge_invariants':'own-r tau_r and Q_rr are constant along each own-r line',
            'construction':'smooth Gram factor + own-leg SO3 alignment + free SO2; arbitrary observer restored by canonical L(n)',
            'scope':'regular spatial legs, fixed time component and local reference Gram chart',
        },
        'source':{
            'convention':'Q=g^-1; delta g=-g delta Q g; EH bulk source is +sqrt(abs(det g))*G_cov against delta Q',
            'full_support_tangent':'H_rr=0 and lambda^T H lambda=0; all observer/link directions already included',
            'generic_residual':'Eres=lambda lambda^T-(tau.k) Diag(lambda_i/(Qk)_i)',
            'generic_condition':'every (Qk)_i != 0; lambda_i != 0 at the regular symmetric root',
            'completion':'Poff=lambda lambda^T-Diag(lambda_i^2), one fixed-background momentum-independent FORBIDDEN native metric row',
            'completion_pairing':'sum_(i!=j) lambda_i^2 lambda_j^2 > 0 when lambda support >=2',
            'exceptional_equations':'d_i*(Qk)_i+c*lambda_i*(tau.k)=0; exceptional diagonal sources may remain',
            'fixture_Eres':[[str(Eres[i,j]) for j in range(4)] for i in range(4)],
            'fixture_completion_pairing':'102/625',
        },
        'scope':[
            'Metric projection of the FULL joint stored-adjoint class, not a frozen-link/observer slice.',
            'The full-Lorentz canonical true-adjoint domain is larger and has no stored own-leg constraints.',
            'The completion row is an exact physical-source obligation, not an added action/detector/admission rule.',
            'Einstein realization uses a nonnull continuum Fourier comparison; its h need not be a stored-admitted metric tangent.',
            'No rank census, old run, physical selector, all-mode source identification or refinement theorem.',
        ],
    }


if __name__ == '__main__':
    print(json.dumps(run(),sort_keys=True,ensure_ascii=False))
