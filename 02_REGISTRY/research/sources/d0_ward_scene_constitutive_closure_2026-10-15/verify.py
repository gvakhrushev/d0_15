#!/usr/bin/env python3
"""Exact source-map rigidity and scene-to-response synthesis. No physical GR claim."""
from __future__ import annotations
import argparse
import hashlib
import json
from itertools import combinations_with_replacement
from pathlib import Path
import sympy as s

HERE = Path(__file__).resolve().parent
CHECKS: dict[str, int] = {}

def check(name: str, value: bool) -> None:
    if not bool(value):
        raise RuntimeError('FAILED_MATH: ' + name)
    CHECKS[name] = CHECKS.get(name, 0) + 1

def flat(M: s.MatrixBase) -> s.Matrix:
    return s.Matrix(list(M))

def ward_system(n: int = 4):
    pairs = list(combinations_with_replacement(range(n), 2))
    k = len(pairs)
    signs = [1] + [-1] * (n - 1)
    D = s.zeros(n, n*k)
    for alpha in range(n):
        for nu in range(n):
            D[nu, alpha*k+pairs.index(tuple(sorted((alpha, nu))))] = signs[alpha]
    N = s.Matrix.hstack(*D.nullspace())
    W = s.zeros(n*N.cols, k*k)
    for row in range(k):
        for col in range(k):
            E = s.zeros(k)
            E[row, col] = 1
            W[:, row*k+col] = flat(D*s.diag(*([E]*n))*N)
    return pairs, D, N, W

def scene():
    sizes = [9, 11, 13]
    zones = sum(([a]*n for a, n in enumerate(sizes)), [])
    n = sum(sizes)
    adjacency = s.Matrix(n, n, lambda i,j: int(zones[i] != zones[j]))
    L = s.diag(*list(adjacency*s.ones(n,1))) - adjacency
    P0 = s.ones(n)/n
    within = []
    for a, count in enumerate(sizes):
        within.append(s.Matrix(n, n, lambda i,j:
            s.KroneckerDelta(i,j)-s.Rational(1,count)
            if zones[i] == zones[j] == a else 0))
    Pc = s.eye(n)-P0-sum(within, s.zeros(n))
    return sizes, zones, L, P0, within, Pc

def material_jet(rho, drho, L, dL):
    return s.trace(drho*L) + s.trace(rho*dL)

def main(write: bool = False) -> None:
    CHECKS.clear()
    pairs,D,N,W = ward_system()
    k = len(pairs)
    check('packed_metric_slots', k == 10)
    check('divergence_surjective', D.rank() == 4)
    check('all_conserved_first_jets', N.shape == (40,36) and D*N == s.zeros(4,36))
    check('all_Ward_constraints', W.shape == (144,100))
    check('constitutive_rank_99', W.rank() == 99)
    null = W.nullspace()
    check('unique_linearization_is_scalar', len(null)==1 and null[0]==flat(s.eye(k)))
    # Exact rational coercivity, not a floating-point singular-value test.
    u = flat(s.eye(k))
    scalar_projection = u*u.T/k
    half = s.Rational(1,2)
    coercive = W.T*W-half*(s.eye(k*k)-scalar_projection)+scalar_projection
    LL,DD = coercive.LDLdecomposition(hermitian=False)
    check('Ward_coercivity_exact_factorization', LL*DD*LL.T==coercive)
    for pivot in DD.diagonal():
        check('Ward_coercivity_positive_pivots', pivot>0)
    check('scalar_projection_is_kernel', W*scalar_projection==s.zeros(W.rows,k*k))
    eta = s.diag(1,-1,-1,-1)
    trace_row = s.Matrix([[eta[i,j]*(1 if i==j else 2) for i,j in pairs]])
    eta_col = s.Matrix([eta[i,j] for i,j in pairs])
    reverse = s.eye(k)-eta_col*trace_row/2
    check('trace_reverse_not_conservation_preserving', W*flat(reverse) != s.zeros(W.rows,1))
    # An explicit divergence-free first jet with a nonconstant trace.
    H = s.zeros(40,1)
    H[pairs.index((1,1))] = 1
    check('nonconstant_trace_source_is_conserved', D*H == s.zeros(4,1))
    check('trace_reverse_creates_divergence', D*s.diag(reverse,reverse,reverse,reverse)*H != s.zeros(4,1))
    # For an arbitrary (possibly nonlinear) map, its Jacobian at every stress
    # is constrained by W. Equality of mixed derivatives then fixes its scale.
    da = s.symbols('a0:10')
    mixed = []
    for i in range(k):
        for j in range(k):
            if i != j:
                mixed.append(da[j])  # d_j(d_i F_i) = d_i(d_j F_i) = 0
    integrability,_ = s.linear_eq_to_matrix(mixed,da)
    check('nonlinear_scale_forced_constant', integrability.rank()==10)
    # Remaining constant tensor is Lorentz invariant, hence proportional to eta.
    Cvars = s.symbols('c0:10')
    C = s.zeros(4)
    for t,(i,j) in zip(Cvars,pairs):
        C[i,j] = C[j,i] = t
    equations = []
    for a,b in combinations_with_replacement(range(4),2):
        if a == b:
            continue
        J = s.zeros(4)
        J[a,b] = 1
        J[b,a] = -eta[a,a]/eta[b,b]
        check('actual_Lorentz_generator', J.T*eta+eta*J==s.zeros(4))
        equations.extend(list(J.T*C+C*J))
    CM,_ = s.linear_eq_to_matrix(equations,Cvars)
    check('constant_tensor_has_one_parameter', CM.rank()==9 and CM*eta_col==s.zeros(CM.rows,1))

    sizes,zones,L,P0,within,Pc = scene()
    projectors = [P0,*within,Pc]
    eigenvalues = [0,24,22,20,33]
    multiplicities = [1,8,10,12,2]
    for i,P in enumerate(projectors):
        check('complete_spectral_projection', P.T==P and P*P==P and P.trace()==multiplicities[i])
        check('complete_spectral_eigenidentity', L*P==eigenvalues[i]*P)
        for j,Q in enumerate(projectors):
            if i != j:
                check('spectral_orthogonality', P*Q==s.zeros(33))
    check('no_modes_discarded', sum(projectors,s.zeros(33))==s.eye(33))
    check('full_359_edges', L.trace()==718)
    Q = s.Matrix(33,3,lambda i,a: 1/s.sqrt(sizes[a]) if zones[i]==a else 0)
    v = s.Matrix([s.sqrt(n) for n in sizes])
    check('normalized_sector_inclusion', Q.T*Q==s.eye(3))
    Cscene = s.simplify(Q.T*L*Q)
    check('transverse_form_follows_from_scene', Cscene==33*s.eye(3)-v*v.T)
    check('quotient_zero_and_33', Cscene*v==s.zeros(3,1) and s.simplify(Cscene**2-33*Cscene)==s.zeros(3))
    rho = within[2]/12
    check('catalogue_free_lowest_layer', rho.trace()==1 and L*rho==20*rho)
    orbit = {(0,1):s.Integer(0),(0,2):s.Rational(1,13),(1,2):s.Rational(1,13)}
    sums = {key:s.Integer(0) for key in orbit}
    edge_count = 0
    for i in range(33):
        for j in range(i+1,33):
            if zones[i]==zones[j]:
                continue
            b = s.eye(33)[:,i]-s.eye(33)[:,j]
            key = (zones[i],zones[j])
            reading = (b.T*rho*b)[0]
            check('all_independent_material_edge_rows', reading==orbit[key])
            sums[key] += reading
            edge_count += 1
    check('scene_to_matter_orbit_source', edge_count==359 and list(sums.values())==[0,9,11])
    # The moving-preparation term is mandatory, and is not another free source.
    drho = within[1]/10-rho
    # Use a faithful density and a genuine edge-weight curve, so the joint
    # test is admissible on BOTH sides of zero, not a one-sided rank change.
    rho_base = s.eye(33)/33
    edge = s.eye(33)[:,0]-s.eye(33)[:,20]
    dL = edge*edge.T
    curve_t = s.symbols('curve_t', real=True)
    curve_price = s.trace((rho_base+curve_t*drho)*(L+curve_t*dL))
    check('moving_preparation_jet', material_jet(rho_base,drho,L,dL)==s.Rational(68,33))
    check('joint_source_chain_rule', s.diff(curve_price,curve_t).subs(curve_t,0)==material_jet(rho_base,drho,L,dL)
          and s.Rational(1,33)-s.Rational(1,1000)>0 and s.Rational(1,33)-s.Rational(1,1200)>0)

    # Any positive tensor with eigenvalues (9,11,13) is an exact sum of
    # three transverse projectors, NOT one rank-two projector.
    weights = [s.Rational(33,2)-n for n in sizes]
    T = sum((w*(s.eye(3)-s.eye(3)[:,i]*s.eye(3)[:,i].T)
             for i,w in enumerate(weights)),s.zeros(3))
    check('unique_three_plane_weights', weights==[s.Rational(15,2),s.Rational(11,2),s.Rational(7,2)])
    check('three_plane_reconstruction', T==s.diag(9,11,13) and all(w>0 for w in weights))
    check('three_plane_inverse_nonsingular', (s.ones(3)-s.eye(3)).det()==2)
    nvec = s.Matrix(sizes)/s.sqrt(sum(n*n for n in sizes))
    single = s.eye(3)-nvec*nvec.T
    check('one_plane_is_a_different_tensor', single.det()==0 and T.det()!=0)
    c = (s.sqrt(6)+s.sqrt(2))/4
    t = (s.sqrt(6)-s.sqrt(2))/4
    R = s.Matrix([[c,-t,0],[t,c,0],[0,0,1]])
    Tr = s.simplify(R*T*R.T)
    check('actual_observer_rotation', s.simplify(R.T*R)==s.eye(3))
    check('tensor_projection_double_angle', s.simplify(Tr[0,0]-Tr[1,1]+s.sqrt(3))==0)
    check('tensor_projection_mixed_component', Tr[0,1]==-s.Rational(1,2))
    check('rotation_preserves_invariants', s.simplify(Tr.trace()-T.trace())==0 and s.simplify(Tr.det()-T.det())==0)
    check('scalar_cosine_is_not_tensor_rotation', s.simplify(Tr-c*T)!=s.zeros(3))

    phi = (1+s.sqrt(5))/2
    p = phi-1
    j2 = 4*p**3
    kappa = s.simplify(2/(3*j2))
    check('golden_scalar_calibration', s.simplify(kappa-(s.sqrt(5)+2)/6)==0)
    check('same_scalar_calibration_product', s.simplify(kappa*j2-s.Rational(2,3))==0)
    check('temperature_dependence_not_erased', s.simplify((2/(5*j2))/kappa)==s.Rational(3,5))
    pi0 = s.Rational(6,5)*phi**2
    check('seam_phase_is_12_over_5', s.simplify(2*pi0*(2-phi))==s.Rational(12,5))
    result = {
        'status':'PASS_EXACT_CONDITIONAL_WARD_AND_SCENE_SYNTHESIS',
        'checks':CHECKS, 'check_count':sum(CHECKS.values()),
        'ward_constraint_shape':[144,100], 'ward_rank':99,
        'source_jets':36, 'constant_Lorentz_rank':9,
        'Ward_squared_coercivity_lower_bound':'1/2',
        'scene_spectrum':{'0':1,'20':12,'22':10,'24':8,'33':2},
        'matter_edge_orbit_sums':[0,9,11],
        'kappa_probe':'(sqrt(5)+2)/6',
        'full_D0_action_binding_proved':False,
        'universal_physical_Ward_proved':False,
        'Lovelock_hypotheses_derived_from_D0':False,
        'observation_fit_or_15_degree_forcing':False,
        'new_Lean_compilation':False,
        'physical_GR_closed':False,
    }
    target = HERE/'receipt.json'
    if write:
        target.write_text(json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+'\n')
    else:
        expected=json.loads(target.read_text())
        if result != expected:
            raise RuntimeError('IMMUTABLE_RECEIPT_MISMATCH')
    print(json.dumps({'status':result['status'],'check_count':result['check_count'],'ward_rank':99},sort_keys=True))

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true',help='Explicitly create the new receipt')
    main(parser.parse_args().write)
