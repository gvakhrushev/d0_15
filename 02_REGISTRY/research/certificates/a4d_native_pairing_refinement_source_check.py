#!/usr/bin/env python3
"""Exact finite controls; complete-class arguments reside in the pinned proof.

Default mode replays the immutable certificate. --write may only seal a stable
proof and successful narrow Lean receipt. No native physical admission follows.
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
BASE = '02_REGISTRY/research/certificates/a4d_native_pairing_refinement_source'
PROOF = '02_REGISTRY/research/A4D_NATIVE_PAIRING_REFINEMENT_SOURCE.md'
INPUTS = [
    '02_REGISTRY/research/A4D_NATIVE_COCHAIN_REFINEMENT.md',
    '02_REGISTRY/research/certificates/a4d_native_cochain_refinement.lean',
    '02_REGISTRY/research/A4D_NATIVE_JOINT_ADJOINT_SOURCE.md',
    '02_REGISTRY/research/certificates/a4d_native_joint_adjoint_source.py',
    '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py',
    '02_REGISTRY/research/certificates/a4d_native_soldered_heat_source.py',
    '03_FORMALIZATION/D0/Geometry/ArchiveAffineExteriorLink.lean',
    '03_FORMALIZATION/D0/Geometry/A4DObserverPositiveExterior.lean',
    '03_FORMALIZATION/D0/Geometry/Archive1DCochainRefinement.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveGradedRefinementChainMap.lean',
    '03_FORMALIZATION/D0/Geometry/Archive1Dto4DRGLiftNoGo.lean',
]
spec = importlib.util.spec_from_file_location('pairing_refinement_program',ROOT/(BASE+'.py'))
P = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = P
spec.loader.exec_module(P)
s,J = P.s,P.J


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
        return all(s.simplify(v)==0 for v in values)
    def check(name,truth):
        assert bool(truth),name
        checks.append(name)
    def eq(name,value):
        check(name,zero(value))
    def reject(name,false):
        check('REJECT_'+name,not false)
        mutants.append(name)

    E,I4,I16 = P.ETA,s.eye(4),s.eye(16)
    e0,e1,e2,e3 = [I4[:,r] for r in range(4)]
    boost = s.Matrix([[s.Rational(5,4),s.Rational(3,4),0,0],
                      [s.Rational(3,4),s.Rational(5,4),0,0],[0,0,1,0],[0,0,0,1]])
    ny = s.Matrix([s.Rational(13,12),0,s.Rational(5,12),0])
    nx,vy = boost*ny,s.Matrix([1,2,-1,3])
    mux,muy = s.Rational(2),s.Rational(3)
    ratio = mux/muy
    vx = boost*vy/ratio
    edge = P.weighted_edge(boost,nx,ny,vx,vy,mux,muy)
    eq('weighted_full16_rational_Lorentz_edge',edge['weighted_defect'])
    eq('weighted_observer_congruence',boost.T*edge['hx']*boost-edge['hy'])
    eq('weighted_leg_ratio',boost*vy-ratio*vx)
    eq('weighted_full16_direct_Gram_adjoint',
       edge['weighted_adjoint']-(muy*edge['Gy']).inv()*edge['forward'].T*(mux*edge['Gx']))
    eq('weighted_full16_reduction',J.creator(edge['b']).T-
       ratio*J.exterior(edge['T'])*J.creator(edge['c']).T)
    for degree,rows,cols in [(1,[0],[1,2,4,8]),(4,[7,11,13,14],[15])]:
        check('weighted_grade_%d_block_nontrivial'%degree,
              not zero(edge['weighted_adjoint'].extract(rows,cols)))
        eq('weighted_grade_%d_block_matches'%degree,edge['weighted_defect'].extract(rows,cols))
    reject('INVERT_WEIGHT_RATIO',zero(edge['stored']-edge['adjoint']/ratio))
    reject('DROP_WEIGHT_RATIO',zero(edge['stored']-edge['adjoint']))
    reject('WEIGHT_ALONE_FIXES_OBSERVER',zero(P.weighted_edge(boost,e0,e0,vx,vy,mux,muy)['weighted_defect']))
    n = s.Matrix(s.symbols('n0:4',real=True))
    observer = J.observer(n)
    for r in range(1,4):
        eq('observer_diagonal_time_space_constraint_%d'%r,observer[0,r]+2*n[0]*n[r])
    eq('rest_observer_diagonal_intersection',J.observer(e0)-I4)
    frozen_h = s.Rational(9,8)*I4
    eq('actual_frozen_metric_measure_Gram',16*J.exterior_gram(frozen_h)-
       s.diag(*[s.Rational(9,4)**bin(mask).count('1')*2**(4-bin(mask).count('1')) for mask in range(16)]))
    reject('FROZEN_DIAGONAL_PAIRING_IS_OBSERVER_PAIRING',frozen_h.det()==1)
    eq('weighted_counting_reparameterized_edge',J.edge(boost,nx,ny,mux*vx,muy*vy)['defect'])
    # Reparameterization of the admissible class is not spectral conjugacy.
    base = s.Matrix([[0,1],[1,0]])
    mu = s.diag(2,3)
    D = mu.inv()*base
    eq('weighted_stored_operator_selfadjoint',mu*D-D.T*mu)
    eq('rescaled_counting_operator',mu*D-base)
    rootmu = s.diag(s.sqrt(2),s.sqrt(3))
    transported = rootmu*D*rootmu.inv()
    eq('actual_pairing_isometry_operator',transported-rootmu.inv()*base*rootmu.inv())
    reject('ADMISSIBLE_CLASS_REPARAMETERIZATION_PRESERVES_HEAT_SQUARE',zero(transported**2-base**2))

    ranks = []
    for flags in product((0,1),repeat=4):
        b,spatial = flags[0],sum(flags[1:])
        active = b+spatial
        tag = ''.join(map(str,flags))
        for volume in (False,True):
            A,H = P.tangent_system(flags,volume)
            rank = A.rank()
            image = A.col_join(H).rank()-rank
            count = 43 if volume else 44
            expected = 10-b-spatial-b*spatial+(int(active>0) if not volume else 0)
            label = ('native_volume_' if volume else 'independent_volume_')+tag
            check(label+'_constraint_rank',rank==18+4*b+2*spatial)
            check(label+'_solution_dimension',count-rank==count-18-4*b-2*spatial)
            check(label+'_metric_image',image==expected)
            kernel = count-rank-image
            check(label+'_metric_kernel',kernel==15-3*b-spatial+b*spatial+int(not volume and active==0))
            null = s.Matrix.hstack(*A.nullspace())
            image_matrix = H*null
            # Compare the complete subspace, not just its dimension.
            oldA,oldH = J.tangent_system(flags)
            old_image = oldH*s.Matrix.hstack(*oldA.nullspace())
            transformed = []
            for column in old_image.columnspace():
                M = s.zeros(4)
                for value,(r,t) in zip(column,P.SLOTS):
                    M[r,t]=M[t,r]=value
                transformed.append(s.Matrix([P.metric_rescale_inverse(M)[r,t] for r,t in P.SLOTS]) if volume else column)
            if not volume:
                transformed.append(s.Matrix([E[r,t] for r,t in P.SLOTS]))
            expected_image = s.Matrix.hstack(*transformed)
            check(label+'_exact_image_subspace',
                  image_matrix.row_join(expected_image).rank()==image==expected_image.rank())
            ranks.append(dict(nonzero_pattern=list(flags),native_volume=volume,
                constraint_rank=rank,solution_dimension=count-rank,metric_image_rank=image,metric_kernel=kernel))
    L = s.symbols('L',integer=True,positive=True)
    lattice_sum = lambda f:sum(s.binomial(3,k)*(L-1)**(b+k)*f(b,k) for b in (0,1) for k in range(4))
    eq('all_level_independent_volume_solutions',lattice_sum(lambda b,k:26-4*b-2*k)-(16*L**4+10*L**3))
    eq('all_level_independent_volume_metric_image',lattice_sum(lambda b,k:10-b-k-b*k+int(b+k>0))-(4*L**4+10*L**3-3*L**2-1))
    eq('all_level_independent_volume_metric_kernel',lattice_sum(lambda b,k:15-3*b-k+b*k+int(b+k==0))-(12*L**4+3*L**2+1))
    symbolic_H = s.zeros(4)
    for x,(r,t) in zip(s.symbols('h:10'),P.SLOTS):
        symbolic_H[r,t]=symbolic_H[t,r]=x
    eq('native_volume_metric_rescale_inverse',P.metric_rescale_inverse(P.metric_rescale(symbolic_H))-symbolic_H)
    rho = s.symbols('rho',positive=True)
    F = s.diag(rho,-1,-1,-1)
    Ft = rho*F
    eq('native_volume_fifth_power_det',-Ft.det()-rho**5)
    eq('native_volume_exact_inverse',Ft/rho-F)
    # Direct Christoffel derivative using the exact stationary two-jet of
    # 2+cos(2*pi*t). The reported R_0101 has its first index lowered.
    t = s.symbols('t',real=True)
    profile_jet = 3-2*s.pi**2*t*t
    q00,q11 = profile_jet**s.Rational(-2,5),-profile_jet**s.Rational(8,5)
    christoffel011 = -s.diff(q11,t)/(2*q00)
    eq('volume_warp_stationary_connection_zero',christoffel011.subs(t,0))
    lowered_curvature = (q00*s.diff(christoffel011,t)).subs(t,0)
    eq('volume_warp_stationary_lowered_R0101',lowered_curvature+
       s.Rational(16,5)*s.pi**2*3**s.Rational(3,5))
    allowed = s.Matrix.hstack(*[s.eye(10)[:,P.SLOTS.index(slot)] for slot in [(1,2),(1,3),(2,3)]])
    weighted = allowed.row_join(s.Matrix([E[r,t] for r,t in P.SLOTS]))
    for frequency,expected in [((1,1,1,1),7),((1,2,3,4),8),((1,-1,1,-1),7)]:
        gauge = s.Matrix([[frequency[r]*int(t==j)+frequency[t]*int(r==j) for j in range(4)] for r,t in P.SLOTS])
        check('independent_volume_coordinate_gauge_rank_'+str(frequency),weighted.row_join(gauge).rank()==expected)
        check('native_volume_coordinate_gauge_rank_'+str(frequency),allowed.row_join(gauge).rank()==7)
    allones_gauge = s.Matrix([[int(r==j)+int(t==j) for j in range(4)] for r,t in P.SLOTS])
    witness = s.Matrix([0,0,0,0,1,0,0,-1,0,0])
    reject('VOLUME_FREES_ALL_NONGAUGE_METRIC_COMPONENTS',weighted.row_join(allones_gauge).row_join(witness).rank()==7)

    refinement_records = []
    for length in (2,3,4):
        K = length+1
        data = P.complex_data(length,length,K)
        P0,P1,dc,df = [data[k] for k in ('P0','P1','dc','df')]
        c = data['c']
        eq('actual_scaled_chain_map_L%d'%length,df*P0-P1*dc)
        eq('vertex_pullback_Gram_L%d'%length,P0.T*P0-s.diag(2,*([1]*(length-1))))
        eq('edge_pullback_Gram_L%d'%length,P1.T*P1-c*c*s.eye(length))
        pullback = P.complex_data(length,length,K,P0.T*P0,P1.T*P1)
        embedding = pullback['P']
        readback = P.rectangular_adjoint(embedding,pullback['Gc'],pullback['Gf'])
        complement = s.eye(2*K)-embedding*readback
        reaction = complement*pullback['Df']*embedding
        reaction_adj = P.rectangular_adjoint(reaction,pullback['Gc'],pullback['Gf'])
        eq('actual_pullback_Dirac_compression_L%d'%length,
           readback*pullback['Df']*embedding-pullback['Dc'])
        eq('actual_pullback_square_forced_reaction_L%d'%length,
           readback*pullback['Df']**2*embedding-pullback['Dc']**2-reaction_adj*reaction)
        check('actual_pullback_reaction_rank_one_L%d'%length,reaction.rank()==1)
        eq('actual_pullback_reaction_HS_norm_L%d'%length,s.trace(reaction_adj*reaction)-K*K)
        reject('CHAIN_MAP_IS_ADJOINT_INTERTWINER_L%d'%length,zero(data['af']*P1-P0*data['ac']))
        one = s.ones(length,1)
        endpoint = s.eye(K)[:,K-1]-s.eye(K)[:,0]
        defect = pullback['af']*P1*one-P0*pullback['ac']*one
        eq('constant_oneform_coarse_harmonic_L%d'%length,pullback['ac']*one)
        eq('constant_oneform_actual_adjoint_defect_L%d'%length,defect-K*c*endpoint)
        eq('constant_oneform_defect_norm_L%d'%length,(defect.T*defect)[0]-2*K*K*c*c)
        eq('constant_oneform_normalized_L1_L%d'%length,2*K*c/K-s.Rational(2*K,length))
        eq('constant_oneform_normalized_L2_square_L%d'%length,2*K*K*c*c/K-s.Rational(2*K**3,length**2))
        scalar_square_defect = df*defect
        eq('constant_oneform_square_defect_L%d'%length,scalar_square_defect-K*K*c*P.cycle_difference(K)*endpoint)
        reject('COUNTING_CONSTANT_ONEFORM_REMAINS_HARMONIC_L%d'%length,zero(scalar_square_defect))
        # Complete positive-diagonal class: a nonzero symbolic corner is forced.
        a = s.symbols('a0:'+str(length),positive=True)
        b = s.symbols('b0:'+str(length),positive=True)
        af = s.symbols('af0:'+str(K),positive=True)
        bf = s.symbols('bf0:'+str(K),positive=True)
        weighted_data = P.complex_data(length,length,K,s.diag(*a),s.diag(*b),s.diag(*af),s.diag(*bf))
        adjoint_defect = weighted_data['af']*P1-P0*weighted_data['ac']
        eq('all_positive_diagonal_forced_corner_0_L%d'%length,adjoint_defect[0,length-1]+length*b[-1]/a[0])
        eq('all_positive_diagonal_forced_corner_last_L%d'%length,adjoint_defect[length,0]-length*b[0]/a[0])
        check('all_positive_diagonal_corner_nonzero_L%d'%length,(-length*b[-1]/a[0]).is_negative)
        refinement_records.append(dict(L=length,c=str(c),constant_oneform_defect_norm=str(2*K*K*c*c)))

    # Every actual exterior component is retained in each active tensor factor.
    for role in range(4):
        Dc,Df,refinement = P.full16_line_refinement(2,role,2,3)
        C = J.P.creator(role)
        dc = s.kronecker_product(2*P.cycle_difference(2),C)
        df = s.kronecker_product(3*P.cycle_difference(3),C)
        eq('full16_chain_map_role%d'%role,df*refinement-refinement*dc)
        reject('FULL16_CHAIN_IMPLIES_DIRAC_role%d'%role,zero(Df*refinement-refinement*Dc))
        reject('FULL16_CHAIN_IMPLIES_SQUARE_role%d'%role,zero(Df*Df*refinement-refinement*Dc*Dc))
        for mask in range(16):
            if mask & (1<<role):
                oneform = s.kronecker_product(s.ones(2,1),I16[:,mask])
                eq('full16_coarse_constant_sector_%d_%d'%(role,mask),Dc*oneform)
                check('full16_fine_constant_sector_defect_%d_%d'%(role,mask),
                      ((Df*refinement*oneform).T*(Df*refinement*oneform))[0]==s.Rational(81,2))
    # Tensor-sector chain tests (32 grade-raising blocks), not a dense 1296-square surrogate.
    for mask in range(16):
        coarseP = P.tensor_sector_map(2,mask,s.Rational(3,2))
        expected_Gram = s.kronecker_product(*[
            s.Rational(9,4)*s.eye(2) if mask & (1<<r) else s.diag(2,1) for r in range(4)])
        eq('actual_all_sector_pullback_Gram_%d'%mask,coarseP.T*coarseP-expected_Gram)
        for role in range(4):
            if not mask & (1<<role):
                fineP = P.tensor_sector_map(2,mask|(1<<role),s.Rational(3,2))
                dc = s.kronecker_product(*[2*P.cycle_difference(2) if r==role else s.eye(2) for r in range(4)])
                df = s.kronecker_product(*[3*P.cycle_difference(3) if r==role else s.eye(3) for r in range(4)])
                eq('tensor_all_sector_chain_%d_%d'%(mask,role),df*coarseP-fineP*dc)
    B20,_ = P.refinement_maps(2)
    B30,_ = P.refinement_maps(3)
    twolevel = B30*B20
    eq('tower_first_vertex_mass',B20.T*B20-s.diag(2,1))
    eq('tower_next_pullback_vertex_mass',twolevel.T*twolevel-s.diag(3,1))
    reject('PAIRWISE_PULLBACK_GRAM_AUTOMATICALLY_COHERENT',zero(twolevel.T*twolevel-B20.T*B20))

    repairs = []
    for length,gamma in [(2,s.Rational(3,4)),(3,s.Integer(1)),(4,s.Rational(3,2))]:
        K = length+1
        data = P.nonlocal_repair(length,gamma,length,K)
        Gc,Gf,Dc,Df,refinement = [data[k] for k in ('Gc','Gf','Dc','Df','P')]
        coarse = P.rectangular_adjoint(refinement,Gc,Gf)
        eq('nonlocal_repair_isometric_L%d'%length,refinement.T*Gf*refinement-Gc)
        eq('nonlocal_repair_coisometry_L%d'%length,coarse*refinement-s.eye(2*length))
        eq('nonlocal_repair_adjoint_intertwiner_L%d'%length,data['af']*data['P1']-data['P0']*data['ac'])
        eq('nonlocal_repair_Dirac_intertwiner_L%d'%length,Df*refinement-refinement*Dc)
        eq('nonlocal_repair_square_intertwiner_L%d'%length,Df*Df*refinement-refinement*Dc*Dc)
        df = s.BlockMatrix([[s.zeros(K),s.zeros(K)],[data['df'],s.zeros(K)]]).as_explicit()
        dc = s.BlockMatrix([[s.zeros(length),s.zeros(length)],[data['dc'],s.zeros(length)]]).as_explicit()
        eq('nonlocal_repair_chain_retraction_L%d'%length,coarse*df-dc*coarse)
        v_unknown = s.Matrix(s.symbols('v0:'+str(length)))
        candidate_C1 = s.Rational(length,K)*s.eye(length).row_join(v_unknown)
        retraction_equations = candidate_C1*data['df']-data['dc']*data['Gc0'].inv()*data['P0'].T
        variables = list(v_unknown)
        system = s.Matrix(list(retraction_equations))
        jac = system.jacobian(variables)
        check('nonlocal_repair_complete_v_uniqueness_L%d'%length,jac.rank()==length)
        v_forced = (s.eye(length)[:,0]+s.eye(length)[:,-1])/2
        eq('nonlocal_repair_complete_v_solution_L%d'%length,system.subs(dict(zip(variables,v_forced))))
        for n in range(1,2*K+1):
            check('nonlocal_repair_positive_minor_L%d_%d'%(length,n),Gf[:n,:n].det()>0)
        v = (s.eye(length)[:,0]+s.eye(length)[:,-1])/2
        q = s.eye(K)[:,0]-s.eye(K)[:,-1]
        w = s.Matrix.vstack(-v,s.ones(1,1))
        eq('nonlocal_complement_differential_L%d'%length,data['df']*q-2*K*w)
        eq('nonlocal_complement_vertex_norm_L%d'%length,(q.T*q)[0]-2)
        eq('nonlocal_complement_edge_norm_L%d'%length,(w.T*data['Gf1']*w)[0]-(gamma-s.Rational(1,2)))
        complement = s.diag(q,w)
        eq('nonlocal_complement_orthogonal_L%d'%length,refinement.T*Gf*complement)
        eigenvalue = K*K*(2*gamma-1)
        eq('nonlocal_complement_tunable_square_L%d'%length,Df*Df*complement-eigenvalue*complement)
        repairs.append(dict(L=length,gamma=str(gamma),complement_square_eigenvalue=str(eigenvalue)))
    boundary = P.nonlocal_repair(2,s.Rational(1,2),2,3)
    eq('nonlocal_positivity_boundary_singular',boundary['Gf1'].det())
    reject('NONLOCAL_REPAIR_ALLOWS_GAMMA_HALF',boundary['Gf1'].det()>0)
    first,second = P.nonlocal_repair(2,1,2,3),P.nonlocal_repair(2,2,2,3)
    eq('different_repairs_same_coarse_Dirac',first['Dc']-second['Dc'])
    reject('EXACT_REFINEMENT_UNIQUELY_DETERMINES_FINE_HEAT',zero(first['Df']**2-second['Df']**2))
    # The nonlocal escape changes compatibility with original point observables.
    point0 = s.diag(1,0,0)
    reject('NONLOCAL_REPAIR_PRESERVES_POINT_STAR_REPRESENTATION',
           zero(first['Gf1']*point0-point0*first['Gf1']))
    gamma,beta,zc,k = s.symbols('gamma beta zc k',positive=True)
    lam = k*k*(2*gamma-1)
    zq = 2*s.exp(-beta*lam)
    heatfine = s.log(zc+zq)/beta
    eq('actual_complement_heat_gamma_derivative',s.diff(heatfine,gamma)+
       4*k*k*s.exp(-beta*lam)/(zc+2*s.exp(-beta*lam)))
    check('actual_complement_heat_gamma_derivative_strict_negative',
          s.diff(heatfine,gamma).is_negative)
    exact_family = P.nonlocal_repair(2,gamma,2,3)
    eigen = s.symbols('eigen')
    eq('actual_L2_coarse_full_square_characteristic',
       exact_family['Dc'].__pow__(2).charpoly(eigen).as_expr()-eigen**2*(eigen-27)**2)
    eq('actual_L2_fine_full_square_characteristic',
       exact_family['Df'].__pow__(2).charpoly(eigen).as_expr()-
       eigen**2*(eigen-27)**2*(eigen-9*(2*gamma-1))**2)
    actual_Zc = 2+2*s.exp(-27*beta)
    actual_Zf = actual_Zc+2*s.exp(-9*beta*(2*gamma-1))
    eq('actual_L2_Gibbs_full_price_derivative',s.diff(s.log(actual_Zf)/beta,gamma)+
       36*s.exp(-9*beta*(2*gamma-1))/actual_Zf)
    eq('actual_four_factor_heat_gamma_derivative',s.diff(4*heatfine,gamma)-4*s.diff(heatfine,gamma))
    xc,xq = s.symbols('xc xq',positive=True)
    Zc,Zq = 2+2*s.exp(-beta*xc),2*s.exp(-beta*xq)
    theta = Zc/(Zc+Zq)
    for variable in (xc,xq):
        eq('full_complement_heat_source_weight_'+str(variable),
           s.diff(s.log(Zc+Zq)/beta,variable)-theta*s.diff(s.log(Zc)/beta,variable)-
           (1-theta)*s.diff(s.log(Zq)/beta,variable))

    # Nonorthonormal complete fixture: moving G,d,P induce a genuine leak jet.
    fixture = J.covector_fixture()
    G,d,Pi,K,X,Z = [fixture[k] for k in ('G','d','P','K','X','Z')]
    adj = lambda M:J.dagger(M,G)
    D = d+adj(d)
    dotd = Z-J.comm(K,d)/2
    dotP = X-J.comm(K,Pi)/2
    dotD = dotd+adj(dotd)+J.comm(adj(d),K)
    leak = P.leak_data(D,G,Pi)
    Q,A,R,Gamma = [leak[k] for k in ('Q','A','R','compressed_square')]
    eq('forced_compressed_square_contains_leak',Gamma-A*A-adj(R)*R)
    reject('COMPRESSED_SQUARE_IS_SQUARE_OF_COMPRESSION',zero(adj(R)*R))
    dotR = P.moving_leak_jet(D,Pi,dotD,dotP)
    dotadjR = adj(dotR)+J.comm(adj(R),K)
    dotA = dotP*D*Pi+Pi*dotD*Pi+Pi*D*dotP
    dotGamma = dotP*D*D*Pi+Pi*dotD*D*Pi+Pi*D*dotD*Pi+Pi*D*D*dotP
    dotLeak = dotadjR*R+adj(R)*dotR
    eq('moving_compressed_square_first_jet',dotGamma-dotA*A-A*dotA-dotLeak)
    # Exact positive commuting surrogate on the moving P carrier, NOT Gibbs.
    W = Pi*(s.eye(4)+Gamma).inv()*Pi
    W = W/s.trace(W)
    eq('compressed_surrogate_supported',Pi*W*Pi-W)
    eq('compressed_surrogate_normalized',s.trace(W)-1)
    eq('compressed_surrogate_commutes_compressed_square',J.comm(W,Gamma))
    eq('compressed_surrogate_G_selfadjoint',adj(W)-W)
    supported_W = (fixture['T'].inv()*W*fixture['T'])[:2,:2]
    for minor in (1,2):
        check('compressed_surrogate_positive_on_image_minor%d'%minor,supported_W[:minor,:minor].det()>0)
    eq('moving_leak_source_cyclic_split',-s.trace(W*dotGamma)+
       s.trace(W*(dotA*A+A*dotA))+s.trace(W*dotLeak))
    reject('DROP_MOVING_LEAK_SOURCE',zero(s.trace(W*dotLeak)))
    wrongdotR = Q*dotD*Pi
    reject('DROP_MOVING_PROJECTOR_ENDPOINTS',zero(wrongdotR-dotR))
    reject('DROP_LEAK_ADJOINT_GRAM_JET',zero(dotLeak-(adj(dotR)*R+adj(R)*dotR)))
    # A moving basis changes all slots together and has zero cyclic source.
    V = s.Matrix(4,4,[2,-1,0,3,1,4,2,0,-2,1,3,1,0,2,-1,5])
    basisdotD,basisdotP = J.comm(V,D),J.comm(V,Pi)
    basisdotR = P.moving_leak_jet(D,Pi,basisdotD,basisdotP)
    eq('moving_leak_basis_covariance',basisdotR-J.comm(V,R))
    basisdotGamma = J.comm(V,Gamma)
    eq('moving_compressed_source_basis_Ward',s.trace(W*basisdotGamma))

    # Rectangular coarse/fine version, including independent Gram jets and
    # the actual induced moving inclusion/readback. This is a full algebraic
    # fixture; its rational commuting weights are explicitly not Gibbs.
    inclusion = fixture['T'][:,:2]
    Gc = s.eye(2)
    C = P.rectangular_adjoint(inclusion,Gc,G)
    eq('rectangular_inclusion_isometric',C*inclusion-s.eye(2))
    eq('rectangular_projection_matches_fixture',inclusion*C-Pi)
    Kc = s.Matrix([[2,1],[1,3]])
    omega = s.Matrix([[0,2],[-2,0]])
    nablaJ = X*inclusion+inclusion*omega
    dotJ = nablaJ-K*inclusion/2+inclusion*Kc/2
    dotC = P.rectangular_adjoint(dotJ,Gc,G)+C*K-Kc*C
    eq('rectangular_moving_isometry_constraint',dotC*inclusion+C*dotJ)
    eq('rectangular_moving_projection_matches',dotJ*C+inclusion*dotC-dotP)
    Dc = C*D*inclusion
    R = Q*D*inclusion
    Radj = P.rectangular_adjoint(R,Gc,G)
    A = C*D*D*inclusion
    delta = Dc*Dc
    eq('rectangular_compression_forced_reaction',A-delta-Radj*R)
    dotQ = -dotJ*C-inclusion*dotC
    dotR = dotQ*D*inclusion+Q*dotD*inclusion+Q*D*dotJ
    dotRadj = P.rectangular_adjoint(dotR,Gc,G)+Radj*K-Kc*Radj
    dotS = dotRadj*R+Radj*dotR
    dotDc = dotC*D*inclusion+C*dotD*inclusion+C*D*dotJ
    dotdelta = dotDc*Dc+Dc*dotDc
    dotA = dotC*D*D*inclusion+C*dotD*D*inclusion+C*D*dotD*inclusion+C*D*D*dotJ
    eq('rectangular_full_reaction_first_jet',dotA-dotdelta-dotS)
    nablaR = dotR+(K*R-R*Kc)/2
    nablaS = dotS+J.comm(Kc,Radj*R)/2
    eq('rectangular_balanced_reaction_jet',nablaS-
       P.rectangular_adjoint(nablaR,Gc,G)*R-Radj*nablaR)
    WA = (s.eye(2)+A).inv()
    WA = WA/s.trace(WA)
    Wc = (s.eye(2)+delta).inv()
    Wc = Wc/s.trace(Wc)
    eq('rectangular_surrogate_commutes_generator',J.comm(WA,A))
    eq('rectangular_surrogate_normalized',s.trace(WA)-1)
    for minor in (1,2):
        check('rectangular_surrogate_positive_minor%d'%minor,WA[:minor,:minor].det()>0)
    nabladelta = dotdelta+J.comm(Kc,delta)/2
    source = -s.trace(WA*dotA)
    eq('rectangular_balanced_source_reaction',source+s.trace(WA*nabladelta)+
       2*s.trace(WA*Radj*nablaR))
    eq('rectangular_source_difference_uses_both_densities',source+s.trace(Wc*nabladelta)+
       s.trace((WA-Wc)*nabladelta)+2*s.trace(WA*Radj*nablaR))
    reject('REPLACE_COMPRESSED_DENSITY_BY_COARSE_DENSITY',zero(s.trace((WA-Wc)*nabladelta)))
    reject('FREEZE_REFINEMENT_IN_REACTION_JET',zero(dotR-Q*dotD*inclusion))
    reject('DROP_RECTANGULAR_COARSE_GRAM_JET',zero(Kc*Radj*R))
    reject('DROP_RECTANGULAR_FINE_GRAM_JET',zero(Radj*K*R))
    Vc = s.Matrix([[1,2],[-1,3]])
    basisR = V*R-R*Vc
    basisKf,basisKc = -J.dagger(V,G)-V,-Vc.T-Vc
    basisRadj = P.rectangular_adjoint(basisR,Gc,G)+Radj*basisKf-basisKc*Radj
    eq('rectangular_reaction_basis_covariance',basisRadj*R+Radj*basisR-J.comm(Vc,Radj*R))
    eq('rectangular_full_source_basis_Ward',s.trace(WA*J.comm(Vc,A)))
    # Complement identity-unitary/zero-cut extension leaves feedback fixed.
    U,cut,z = [fixture[key] for key in ('U','P','z')]
    Gextended = s.diag(G,gamma,gamma)
    Uextended,cutextended = s.diag(U,s.eye(2)),s.diag(cut,s.zeros(2))
    Fcoarse = cut*J.dagger(U,G)*(s.eye(4)-cut)*U*cut
    Ffine = cutextended*J.dagger(Uextended,Gextended)*(s.eye(6)-cutextended)*Uextended*cutextended
    eq('feedback_reducing_complement_extension',Ffine-s.diag(Fcoarse,s.zeros(2)))
    eq('feedback_complement_determinant_unchanged',(s.eye(6)-z*Ffine).det()-(s.eye(4)-z*Fcoarse).det())

    if not include_receipt:
        return dict(exact_controls=len(checks),mutants=mutants,ranks=ranks,
                    refinements=refinement_records,repairs=repairs)
    receipt_path = BASE+'_lean_results.json'
    receipt = json.loads((ROOT/receipt_path).read_text())
    output = (ROOT/(BASE+'_lean_output.txt')).read_text()
    check('narrow_Lean_receipt_success',receipt['status']=='PASS' and receipt['compiler_exit_code']==0)
    check('Lean_capsule_fingerprint',receipt['capsule_sha256']==sha(BASE+'.lean'))
    check('Lean_actual_output_fingerprint',receipt['output_sha256']==sha(BASE+'_lean_output.txt'))
    axioms = {name:[a.strip() for a in body.split(',') if a.strip()]
        for name,body in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]",output)}
    check('Lean_actual_axiom_receipt',axioms==receipt['axioms'])
    check('Lean_declarations_resolved',set(axioms)==set(receipt['declarations']))
    printed = set(re.findall(r'^#print axioms ([A-Za-z0-9_.]+)',(ROOT/(BASE+'.lean')).read_text(),re.MULTILINE))
    check('Lean_every_axiom_request_resolved',set(axioms)==printed)
    capsule_text = (ROOT/(BASE+'.lean')).read_text()
    requested_checks = set(re.findall(r'^#check ([A-Za-z0-9_.]+)',capsule_text,re.MULTILINE))
    requested_prints = set(re.findall(r'^#print (?!axioms\b)([A-Za-z0-9_.]+)',capsule_text,re.MULTILINE))
    check('Lean_every_diagnostic_check_bound',requested_checks==set(receipt['diagnostic_checks']))
    check('Lean_every_diagnostic_print_bound',requested_prints==
          set(receipt['diagnostic_definitions'])|set(receipt['diagnostic_printed_propositions']))
    for name,dependencies in axioms.items():
        check('Lean_standard_axioms_'+name,set(dependencies)<={'propext','Classical.choice','Quot.sound'})
    for name in receipt.get('diagnostic_definitions',[]):
        check('Lean_actual_definition_'+name,('def '+name+' ') in output or ('theorem '+name+' ') in output)
    for name in receipt.get('diagnostic_checks',[]):
        check('Lean_actual_declaration_'+name,
              re.search(r'^'+re.escape(name)+r'(?:\.\{[^}]*\})?(?:\s|:)',output,re.MULTILINE) is not None)
    for name in receipt.get('diagnostic_printed_propositions',[]):
        check('Lean_actual_proposition_'+name,('theorem '+name+' ') in output)
    for path,fingerprint in receipt['input_sha256'].items():
        check('Lean_SOURCE_input_'+path,sha(path)==fingerprint)
    check('Lean_original_cache_preserved',receipt['original_cache_unchanged'])
    actual_closure = {path for path in source_closure([BASE+'.lean'])
                      if path.startswith('03_FORMALIZATION/D0/')}
    modules = {path[len('03_FORMALIZATION/'):-5].replace('/','.') for path in actual_closure}
    check('Lean_exact_actual_ten_module_closure',len(modules)==10 and
          set(receipt['cache_source_comparison'])==modules==set(receipt['current_overlay_reuse']))
    check('Lean_exact_SOURCE_receipt_closure',set(receipt['input_sha256'])==actual_closure|{
        '03_FORMALIZATION/lean-toolchain','03_FORMALIZATION/lake-manifest.json'})
    check('Lean_all_actual_dependencies_cache_source_MATCH',
          set(receipt['cache_source_comparison'].values())=={'MATCH'})
    check('Lean_ten_matching_source_cached_artifacts',
          receipt['matching_cache_source_reuse_count']==10 and receipt['copied_olean_file_count']==10)
    check('Lean_no_unclaimed_dependency_rebuilds',receipt['source_overlay_rebuilds']==[] and
          receipt['refreshed_source_module_count']==receipt['new_overlay_compilation_count']==
          receipt['verified_prior_source_rebuild_count']==0)
    for module,entry in receipt['current_overlay_reuse'].items():
        source_path='03_FORMALIZATION/'+module.replace('.','/')+'.lean'
        check('Lean_actual_cached_SOURCE_match_'+module,
              sha(source_path)==entry['source_sha256']==entry['cache_source_sha256'])
        check('Lean_actual_overlay_object_pin_'+module,
              receipt['actual_import_olean_sha256'][entry['overlay_olean']]==entry['olean_sha256'])
        check('Lean_original_object_pin_'+module,
              receipt['original_cache_olean_sha256']['.lake/build/lib/lean/'+module.replace('.','/')+'.olean']==entry['olean_sha256'])
    check('Lean_actual_object_pin_count_including_Init_and_Mathlib',len(receipt['actual_import_olean_sha256'])==12)
    source = re.search(r'Input SOURCE\s+`([0-9a-f]{40})`',(ROOT/PROOF).read_text()).group(1)
    check('proof_Lean_SOURCE_agree',source==receipt['source_commit'])
    inputs = source_closure(INPUTS+list(receipt['input_sha256']))
    return dict(schema='d0-native-pairing-refinement-source/1',
        verdict='WEIGHTED_STORED_CLASS_AND_PAIRING_REFINEMENT_OBSTRUCTION_WITH_NONLOCAL_REPAIR',
        input_source_sha=source,exact_controls=len(checks),controls=checks,
        executed_mathematical_mutants=mutants,weighted_tangent_patterns=ranks,
        constant_oneform_controls=refinement_records,nonlocal_repair_controls=repairs,
        scope='Exact full16 weighted edges; all 16 frequency patterns; finite symbolic diagonal obstruction corners; all tensor grade-raising blocks at L2; exact nonlocal repair and moving leak jets. Complete-class and thermal analytic statements remain in the pinned proof, not all in Lean.',
        compressed_fixture_weight='Normalized P(I+P D^2 P)^-1 P: exact positive commuting algebraic surrogate, not Gibbs.',
        weighted_pairing_native_admission='OPEN',nonlocal_repair_native_admission='OPEN',
        compatible_infinite_Gram_tower='OPEN',native_joint_preparation='OPEN',
        bootstrap_heat_identification='OPEN',source_Ward_GR='OPEN',original_parent_terminal='OPEN',
        input_sha256={path:sha(path) for path in inputs},proof_sha256=sha(PROOF),
        program_sha256=sha(BASE+'.py'),checker_sha256=sha(BASE+'_check.py'),
        Lean_capsule_sha256=sha(BASE+'.lean'),Lean_output_sha256=sha(BASE+'_lean_output.txt'),
        Lean_receipt_sha256=sha(receipt_path))


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--write',action='store_true')
    args=parser.parse_args()
    result=controls()
    target=ROOT/(BASE+'_certificate.json')
    if args.write:
        target.write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    else:
        assert json.loads(target.read_text())==result,'PAIRING_REFINEMENT_SOURCE_IMMUTABLE_LEDGER_MISMATCH'
    print('PASS_NATIVE_PAIRING_REFINEMENT_SOURCE controls=%d mutants=%d native_admission=OPEN'%
          (result['exact_controls'],len(result['executed_mathematical_mutants'])))


if __name__=='__main__':
    main()
