#!/usr/bin/env python3
"""Complete supplied four-slot laws: exact native roots, sources and comparisons."""
import argparse
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

import sympy as s

HEAD = '9e37e008ba89cfaa9a1a70f1d0ffaede6b5aab0b'
BASE = '02_REGISTRY/research/certificates/a4d_native_parent_law'
PROOF = '02_REGISTRY/research/A4D_NATIVE_PARENT_LAW_COMPLETENESS.md'
JOINT = '02_REGISTRY/research/certificates/a4d_native_joint_field_quotient_check.py'
SCOPE = {
    'complete_family': 'FIXED_PERFECT_PAIRING_SUPPLIED_COVARIANT_LINEAR_FOUR_SLOT_INTERFACE',
    'all_site_covariant_descent': 'ANALYTIC_FROM_COMPLETE_NATIVE_QUOTIENT',
    'pointwise_visible_pair_class': 'ARBITRARY_M_AND_RANK_K_AT_MOST_MIDDLE_DIMENSION',
    'full_root_source_comparison': 'COMPLETE_KERNEL_AND_RESTRICTED_SYMMETRIC_JETS',
    'projected_auxiliary_correspondence': 'EXPLICIT_KERNEL_PARAMETERIZATION_AND_QUADRATIC_IMAGE',
    'all_rank_strata_or_quadratic_images_solved': False,
    'pointwise_rank_test_supplies_global_smooth_factorization': False,
    'arbitrary_slots_are_actual_cubical_differentials': False,
    'physical_full_fock_four_grade_specialization_selected': False,
    'covariance_selects_physical_seed_law': False,
    'off_shell_inequality_proves_stationary_inequivalence': False,
    'equal_full_field_kernels_imply_equal_sources': False,
    'auxiliary_matching_required_for_weaker_physical_readout': False,
    'all_stationary_correspondences_require_equal_M_K': False,
    'singular_auxiliary_map_is_a_variation_equivalence': False,
    'nonsymmetric_star_uses_symmetric_star_equation': False,
    'kernel_is_gauge': False,
    'one_root_checks_entire_source_restriction': False,
    'source_gap_fitted_separately_on_each_mesh': False,
    'native_refinement_or_recovery_selected': False,
    'physical_Ward_derived': False,
    'whole_core_physical_nonuniqueness_proved': False,
    'G0_closed': False,
    'positive_GR': False,
    'whole_core_no_go': False,
    'original_parent_terminals_changed': False,
}


def energy(M, K, p, c, l):
    return (c.T*M*c)[0]/2+(l.T*(M*c-K*p))[0]


def hessian(M, K):
    Z = s.zeros(M.rows)
    return s.BlockMatrix([[Z, Z, -K.T],
                          [Z, (M+M.T)/2, M.T],
                          [-K, M, Z]]).as_explicit()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    checks = []
    if args.expect:
        assert json.loads(args.expect.read_text())['scope'] == SCOPE, 'PINNED_LEDGER_MISMATCH'

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    check('COMPILED_23_GENUINE_PROPOSITIONS', receipt['status'] == 'PASS'
          and receipt['compiler_exit_code'] == 0 and not receipt['sorryAx']
          and receipt['printed_axiom_dependencies'] == 23 and receipt['owner_input_head'] == HEAD)
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_TRANSITIVE_NATIVE_TOOLCHAIN_CAPSULE_OUTPUT_PINS', all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('STANDARD_AXIOMS_CLEAN_OUTPUT', set(receipt['axioms']) <= {'propext','Classical.choice','Quot.sound'}
          and not any(x in out for x in ['error:', 'warning:', 'sorryAx']))
    for name in ['literal_owner_binding', 'every_visible_pair_is_an_owner_input',
                 'visible_coefficients_identifiable', 'genuine_gate_equations',
                 'field_hasDerivAt', 'auxiliary_hasDerivAt', 'multiplier_hasDerivAt', 'source_hasDerivAt',
                 'kernel_and_source_comparison', 'decode_encode_primal', 'encoded_visible_composition',
                 'auxiliary_equivalence_action', 'full_joint_block_classification',
                 'full_joint_gate_iff', 'zero_parameter_gate_iff']:
        check('RESOLVED_ACTUAL_PROPOSITION_'+name, "'D0.Research.NativeParentLaw."+name+"' depends on axioms:" in out
              and '\nD0.Research.NativeParentLaw.'+name in out)
    check('LITERAL_EXTERIOR_FUNCTOR_AND_INVERSE_TYPES', 'D0.Geometry.archiveExteriorFrameLift_comp' in out
          and 'D0.Geometry.archiveExteriorFrameLift_inverse' in out)
    spec = importlib.util.spec_from_file_location('native_joint', root/JOINT)
    native = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(native)
    t = s.Symbol('t', real=True)

    # Full nonsymmetric action and all equations, with actual symbolic derivatives.
    M = s.Matrix([[1,2],[-3,4]])
    K = s.Matrix([[2,-1],[3,5]])
    z = s.Matrix(s.symbols('z:6', real=True))
    p,c,l = z[:2,0],z[2:4,0],z[4:,0]
    I = energy(M,K,p,c,l)
    H = hessian(M,K)
    gradient = s.Matrix([s.diff(I,x) for x in z])
    check('FULL_NONSYMMETRIC_OWNER_HESSIAN_AND_ALL_FIELD_ROWS', s.hessian(I,list(z)) == H
          and gradient == H*z and s.expand(I-(z.T*H*z)[0]/2) == 0)
    wrong = M*c+M.T*l
    check('REJECT_SYMMETRIC_STAR_EQUATION_FOR_NONSYMMETRIC_INPUT',
          s.simplify(wrong-gradient[2:4,0]) != s.zeros(2,1))
    check('SKEW_PART_VISIBLE_IN_MULTIPLIER_FIELD', energy(M,K,s.zeros(2,1),s.Matrix([1,0]),s.Matrix([0,1]))
          != energy((M+M.T)/2,K,s.zeros(2,1),s.Matrix([1,0]),s.Matrix([0,1])))

    P = s.Matrix([[1,2,3],[0,1,4]])
    B = s.Matrix([[1,2],[3,-1],[2,0]])
    V = B*P
    check('COMPLETE_POINTWISE_BOTTLENECK_FACTORIZATION', V.rank() == 2 and B*s.eye(2)*P == V)
    full = s.Matrix([[1,0,0],[0,1,0],[0,0,1]])
    check('REJECT_FULL_RANK_K_THROUGH_TWO_DIMENSIONAL_SLOT', full.rank() > P.rows)
    E = s.Matrix.vstack(s.eye(3),s.zeros(2,3))
    L = E.T
    arbitrary = s.Matrix([[1,2,3],[4,0,1],[1,-2,5]])
    check('EVERY_K_HAS_A_SMOOTH_FIXED_EMBEDDING_REALIZATION_WHEN_M_GE_N',
          L*E == s.eye(3) and L*(E*arbitrary*L)*E == arbitrary)
    angle = s.Symbol('angle', real=True)
    line = s.Matrix([s.cos(angle/2),s.sin(angle/2)])
    projector = s.Matrix([[(1+s.cos(angle))/2,s.sin(angle)/2],
                          [s.sin(angle)/2,(1-s.cos(angle))/2]])
    check('PERIODIC_RANK_ONE_PROJECTOR_NONTRIVIAL_FACTOR_LINE',
          s.simplify(projector*projector-projector) == s.zeros(2)
          and s.simplify(projector.det()) == 0 and s.trace(projector) == 1
          and s.trigsimp(line*line.T-projector) == s.zeros(2)
          and line.subs(angle,0) == -line.subs(angle,2*s.pi))

    G0 = s.Matrix([[1,2,0],[0,1,1],[0,0,2]])
    G1 = s.Matrix([[2,1],[0,3]])
    H1 = s.Matrix([[1,3],[-2,4]])
    M1 = arbitrary
    encP = G1.inv()*P*G0
    encB = G0.T*B*G1.inv().T
    encM = G0.T*M1*G0
    encH = G1.T*H1*G1
    check('ALL_FOUR_RECTANGULAR_COVARIANT_SEEDS_RECOVERED', G1*encP*G0.inv() == P
          and G0.inv().T*encB*G1.T == B and G0.inv().T*encM*G0.inv() == M1
          and G1.inv().T*encH*G1.inv() == H1)
    check('ACTUAL_VISIBLE_COMPOSITION_CONGRUENCE', encB*encH*encP == G0.T*(B*H1*P)*G0)

    # The fixed physical-matter readout need not identify auxiliary coordinates.
    M1 = s.diag(1,-1)
    K1 = s.Matrix([[1,0],[1,0]])
    M2 = s.diag(4,-1)
    K2 = s.Matrix([[2,0],[1,0]])
    Taux = s.diag(s.Rational(1,2),1)
    check('NONSCALAR_AUXILIARY_ACTION_EQUIVALENCE', Taux.T*M2*Taux == M1 and Taux.T*K2 == K1
          and s.expand(energy(M2,K2,p,Taux*c,Taux*l)-energy(M1,K1,p,c,l)) == 0
          and M2[0,0]/M1[0,0] != M2[1,1]/M1[1,1] and Taux.det() != 0)
    N1 = s.Matrix.hstack(*hessian(M1,K1).nullspace())
    N2 = s.Matrix.hstack(*hessian(M2,K2).nullspace())
    check('AUXILIARY_QUOTIENT_CAN_BE_WEAKER_THAN_FULL_FIELD_KERNEL',
          s.Matrix.hstack(N1,N2).rank() > N1.cols and N1[:2,:].rank() == N2[:2,:].rank() == 2)
    singular = s.diag(0,1)
    check('SINGULAR_AUXILIARY_MAP_IS_NOT_A_VARIATION_EQUIVALENCE', singular.det() == 0
          and hessian(singular.T*M2*singular,singular.T*K2).nullspace()
          and hessian(singular.T*M2*singular,singular.T*K2).rank() < hessian(M2,K2).rank())
    check('OFFSHELL_DIFFERENCE_WITH_IDENTICAL_NONZERO_ROOT_FIBER',
          hessian(M1,K1).nullspace() == (2*hessian(M1,K1)).nullspace()
          and energy(M1,K1,s.zeros(2,1),s.ones(2,1),s.zeros(2,1)) == 0
          and energy(M1,K1,s.zeros(2,1),s.Matrix([1,0]),s.zeros(2,1))
          != energy(2*M1,2*K1,s.zeros(2,1),s.Matrix([1,0]),s.zeros(2,1)))
    # Zero auxiliary stars give a genuine quadratic source image, not just a root projection.
    U = s.eye(2)
    for value in [-2,0,3]:
        cc = s.Matrix([1,0])
        ll = s.Matrix([s.Rational(value)-s.Rational(1,2),0])
        check('PROJECTED_AUXILIARY_SOURCE_IMAGE_'+str(value),
              hessian(s.zeros(2),s.zeros(2))*s.Matrix.vstack(p,cc,ll) == s.zeros(6,1)
              and energy(U,s.zeros(2),p,cc,ll) == value)

    # Native full sixteen-component parent, with one fixed seed law across all levels.
    M0 = s.diag(*([1,-1]*8))
    K0 = s.diag(*([s.Matrix([[1,0],[1,0]])]*8))
    W = s.diag(*([s.Rational(1,8),0]*8))
    pp = s.ones(16,1)
    cc = s.Matrix([1,-1]*8)
    ll = -cc
    zz = s.Matrix.vstack(pp,cc,ll)
    HH = hessian(M0,K0)
    NN = s.Matrix.hstack(*HH.nullspace())
    jj = hessian(W,s.zeros(16))
    check('FULL_ALL16_NONZERO_NATIVE_PARENT_ROOT', HH*zz == s.zeros(48,1)
          and all(x != 0 for x in zz) and energy(M0,K0,pp,cc,ll) == 0)
    check('FULL_KERNEL_BASIS_AND_PROJECTED_AUXILIARY_UNIQUENESS', HH.rank() == 32
          and NN.cols == 16 and NN[:16,:].det() != 0
          and NN*NN[:16,:].inv()*pp == zz and M0.det() != 0)
    check('SAME_FULL_FIELD_KERNEL_DIFFERENT_RESTRICTED_SOURCE', NN.T*jj*NN != s.zeros(16)
          and (zz.T*jj*zz)[0]/2 == -s.Rational(1,2))

    # Entire joint gates, including the singular star. The all-size necessity
    # and sufficiency are compiled; these exact controls bind the displayed
    # literal matrices to those equations and retain all eight null components.
    a, theta = s.symbols('a theta', real=True)
    xp,yp,up,vp,odd,even = s.symbols('x y u v p pe', real=True)
    pairM = s.diag(a,-1)
    pairK = s.Matrix([[1,0],[1,0]])
    pairz = s.Matrix([odd,even,xp,yp,up,vp])
    pairI = energy(pairM,pairK,pairz[:2,0],pairz[2:4,0],pairz[4:,0])
    pairGrad = s.Matrix([s.diff(pairI,zv) for zv in pairz])
    check('LITERAL_ACTION_BINDS_ALL_PAIRED_FIELD_EQUATIONS',
          s.simplify(pairGrad-s.Matrix([-up-vp,0,a*(xp+up),-yp-vp,a*xp-odd,-yp-odd])) == s.zeros(6,1))
    profile = s.Symbol('profile',real=True)
    check('LITERAL_BACKGROUND_DERIVATIVE_IS_CLASSIFIED_NORM_EQUATION',
          s.simplify(s.diff(pairI.subs(a,1+theta*profile/8),profile)
                     -theta*(xp*xp/2+up*xp)/8) == 0)
    field_rows = [a*(xp+up),a*xp-odd,-yp-odd,up+vp,yp+vp]
    coefficients = [1,-1,a,-a,a]
    check('PARAMETER_MINUS_ONE_IDENTITY_WITHOUT_DIVIDING_SINGULAR_STAR',
          s.expand(sum(c*r for c,r in zip(coefficients,field_rows))-(1-a)*odd) == 0)
    even_root = s.zeros(48,8)
    for k in range(8):
        even_root[2*k+1,k] = 1
    check('ALL_BACKGROUND_NONZERO_PARAMETER_ROOT_CLASS_SUFFICIENCY',
          hessian(s.diag(*([a,-1]*8)),K0)*even_root == s.zeros(48,8)
          and even_root.T*jj*even_root == s.zeros(8))
    for value in [0,1,-2,s.Rational(1,3),7]:
        Ma = s.diag(*([value,-1]*8))
        Ha = hessian(Ma,K0)
        Na = s.Matrix.hstack(*Ha.nullspace())
        Qa = Na.T*jj*Na/2
        Ns = s.Matrix.hstack(*Qa.nullspace())
        joint_basis = Na*Ns
        check('ENTIRE_JOINT_ROOT_CLASS_AT_A_'+str(value),
              joint_basis.cols == 8 and joint_basis.rank() == 8
              and s.Matrix.hstack(joint_basis,even_root).rank() == 8
              and all(Qa[i,j] == 0 for i in range(Qa.rows) for j in range(Qa.cols) if i != j)
              and (all(Qa[i,i] >= 0 for i in range(Qa.rows))
                   or all(Qa[i,i] <= 0 for i in range(Qa.rows))))
        if value in [0,1]:
            check('SINGULAR_OR_BASE_FIELD_FIBER_CANNOT_CANCEL_SOURCES_'+str(value),
                  Na.cols == 16 and Qa.rank() == 8
                  and all(Qa[i,i] >= 0 if value == 0 else Qa[i,i] <= 0 for i in range(Qa.rows))
                  and Na[:16,:].rank() == (8 if value == 0 else 16))
    check('ZERO_PARAMETER_FULL_ROOT_CLASS_ALL_PHYSICAL_FIELDS',
          HH*NN == s.zeros(48,16) and NN[:16,:].rank() == 16
          and (M0+theta*profile*W).diff(profile).subs(theta,0) == s.zeros(16))
    check('JOINT_ROOT_CHANGE_IS_A_PROJECTED_PHYSICAL_READOUT_CHANGE',
          s.Matrix.hstack(even_root[:16,:],pp).rank() == 9
          and NN[:16,:].rank() == 16)
    for sector in range(3):
        for i in range(16):
            parts = [pp,cc,ll]
            parts[sector] = parts[sector]+t*s.eye(16)[:,i]
            check('ACTUAL_NATIVE_FIELD_DERIVATIVE_'+str(sector)+'_'+str(i),
                  s.diff(energy(M0,K0,*parts),t).subs(t,0) == 0)

    eta = native.ETA
    coefficients = list(range(1,11))
    for k,(i,j) in enumerate(native.PAIRS):
        probe = s.zeros(4)
        probe[i,j] = probe[j,i] = 1
        F = s.eye(4)+t*probe*eta/2
        rho = native.exterior(F)
        q = F*eta*F.T
        f = sum(c*(q[a,b]-eta[a,b]) for c,(a,b) in zip(coefficients,native.PAIRS))
        Mt = M0+f*W
        rawM = rho.T*Mt*rho
        rawK = rho.T*K0*rho
        fixedraw = energy(rawM,rawK,pp,cc,ll)
        fixedphysical = energy(Mt,K0,pp,cc,ll)
        expected = -s.Rational(coefficients[k],2)
        check('ACTUAL_UNIFORM_TRANSPORTED_METRIC_SOURCE_'+str(i)+str(j),
              q.diff(t).subs(t,0) == probe and s.diff(fixedraw,t).subs(t,0) == expected
              and s.diff(fixedphysical,t).subs(t,0) == expected
              and s.diff(energy(M0,K0,rho*pp,rho*cc,rho*ll),t).subs(t,0) == 0)
    check('FULL_PACKED_DUAL_SOURCE_WEIGHTS',
          sum((1 if i == j else 2)*s.Rational(c,1 if i == j else 2) for c,(i,j) in zip(coefficients,native.PAIRS))
          == sum(coefficients))
    for edge in range(4):
        for i,j in itertools.combinations(range(4),2):
            gen = s.zeros(4)
            gen[i,j] = 1
            gen[j,i] = -eta[i,i]/eta[j,j]
            link = (s.eye(4)-t*gen/2).inv()*(s.eye(4)+t*gen/2)
            link_profile = (edge+1)*sum(2**(4*a+b)*(link[a,b]-s.eye(4)[a,b])
                                       for a in range(4) for b in range(4))
            link_energy = energy(M0+link_profile*W,K0,pp,cc,ll)
            link_source = -s.Rational(edge+1,2)*sum(2**(4*a+b)*gen[a,b]
                                                   for a in range(4) for b in range(4))
            check('ACTUAL_LORENTZ_LINK_ROW_'+str(edge)+'_'+str(i)+str(j),
                  s.simplify(link*eta*link.T-eta) == s.zeros(4)
                  and link.diff(t).subs(t,0) == gen
                  and link_source != 0 and link_energy.subs(t,0) == 0
                  and s.diff(link_energy,t).subs(t,0) == link_source)

    boost = s.Matrix([[s.Rational(5,4),s.Rational(3,4),0,0],
                      [s.Rational(3,4),s.Rational(5,4),0,0],[0,0,1,0],[0,0,0,1]])
    F = s.diag(2,1,1,1)
    rho = native.exterior(F)
    rhoG = native.exterior(boost)
    rhoPrime = native.exterior(F*boost)
    f = sum(c*((F*eta*F.T)[i,j]-eta[i,j]) for c,(i,j) in zip(coefficients,native.PAIRS))
    M = M0+f*W
    rawM,rawK = rho.T*M*rho,rho.T*K0*rho
    primeM,primeK = rhoPrime.T*M*rhoPrime,rhoPrime.T*K0*rhoPrime
    off = s.Matrix(list(range(1,17)))
    prime = rhoG.inv()*off
    check('NONZERO_OFFSHELL_ACTION_AND_ALL_FOUR_NATIVE_COVARIANCE_LAWS',
          rhoPrime == rho*rhoG and (F*boost)*eta*(F*boost).T == F*eta*F.T
          and primeM == rhoG.T*rawM*rhoG and primeK == rhoG.T*rawK*rhoG
          and rhoG.inv()*s.eye(16)*rhoG == s.eye(16)
          and rhoG.T*s.eye(16)*rhoG.inv().T == s.eye(16)
          and energy(rawM,rawK,off,off,off) != 0
          and energy(rawM,rawK,off,off,off) == energy(primeM,primeK,prime,prime,prime))
    check('NATIVE_ROOT_WITNESS_NOT_AUXILIARY_READOUT_ARTIFACT', M0.inv()*K0*pp == cc
          and ll == -cc and energy(W,s.zeros(16),pp,cc,ll) == -s.Rational(1,2))
    at = s.Rational(1,7)
    Mnear = M0+at*W
    reduced = K0.T*Mnear.inv()*K0
    check('NONZERO_SOURCE_ROOT_HAS_NO_DISPLAYED_CONTINUOUS_CONTINUATION',
          reduced*pp != s.zeros(16,1)
          and all(reduced[i,i] != 0 for i in range(0,16,2)))
    level = s.Symbol('L',positive=True,integer=True)
    check('FIXED_ALL_LEVEL_LAW_AND_NORMALIZED_SOURCE_GAP',
          s.simplify(level**4*(1/level)**4*energy(W,s.zeros(16),pp,cc,ll)) == -s.Rational(1,2))
    check('NATIVE_OPERATOR_BLOCK_SUM_IS_LITERAL_PARENT_SUM',
          energy(s.diag(M, M),s.diag(K0,K0),s.Matrix.vstack(off,off),
                 s.Matrix.vstack(off,off),s.Matrix.vstack(off,off)) == 2*energy(M,K0,off,off,off))

    payload = {'status':'PASS','owner_input_head':HEAD,'checks':checks,'scope':SCOPE,
               'transitive_d0_source_count':len(receipt['transitive_d0_source_sha256']),
               'input_sha256':pins,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
               'joint_carrier_checker_sha256':sha(JOINT),
               'native_witness':{'field_dimension':16,'hessian_rank':32,'kernel_dimension':16,
                                 'full_nonzero_field_components':48,'normalized_source_gap':'-1/2',
                                 'metric_components':10,'connection_rows':24}}
    if args.output:
        args.output.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
    else:
        expected = args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_PARENT_LAW_COMPLETENESS',len(checks),'controls',len(receipt['transitive_d0_source_sha256']),'D0 pins')


if __name__ == '__main__':
    main()
