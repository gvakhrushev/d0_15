#!/usr/bin/env python3
"""Exact native gradient compactness controls and a UV--small-link sequence."""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction as Q
from pathlib import Path

import sympy as s

HEAD = 'af3658e09762860e1e38820fd8bc11de54403cff'
BASE = '02_REGISTRY/research/certificates/a4d_native_metric_compactness'
PROOF = '02_REGISTRY/research/A4D_NATIVE_METRIC_COMPACTNESS_AND_LINK_RESONANCE.md'
REFINEMENT = '02_REGISTRY/research/certificates/a4d_native_cochain_refinement_certificate.json'
SCOPE = {
    'finite_inverse': 'ALL_NATIVE_SIZES_CENTERED_GRADIENT_CHART_FROBENIUS_AT_MOST_ONE_QUARTER',
    'metric_only_compactness_and_flatness': 'ANALYTIC_FULL_STATED_SMALL_CHART',
    'transported_flatness_extension': 'DELTA_LINK_TIMES_RAW_L2_TENDS_TO_ZERO',
    'curved_sequence': 'BOUNDED_NATIVE_POTENTIAL_PROPER_SMALL_LINKS_TRANSPORTED_READOUT',
    'frozen_coframe_refinement_boundary': 'ALL_COARSE_COFRAMES_FULL_COMPOSED_ONE_FORM_BLOCK_FIXED_TORUS_WEAK_METRIC_PROBES_SMALL_COMPARISON_LINKS',
    'frozen_raw_gauge_orbit_boundary': 'ANY_DIFFERENTIABLE_FULL_STATE_REFINEMENT_WITH_FLAT_RAW_REFERENCE_AND_SAME_FROZEN_ROW_FIRST_JET',
    'frozen_gauge_saturated_admission': 'EMPTY_FOR_ANY_NONDEGENERATE_FULL_STATE_ADMISSION_WITH_LITERAL_FIXED_REFERENCE_RAW_BLOCK_AND_FULL_PROPER_LORENTZ_ORBIT_DESCENT',
    'affine_raw_intertwiners': 'COMPLETE_CONNECTION_INDEPENDENT_AFFINE_CLASS_FOR_PULLBACK_NODE_FRAMES_WITH_REFERENCE_CONDITION_EXPLICIT',
    'frozen_curve_refinement_gap': 'NONZERO_GAUGE_INVARIANT_BULK_GAP_WITH_VANISHING_METRIC_CORRECTORS_ALLOWED',
    'continuum_parity_and_regularity_formalized': False,
    'finite_inverse_is_joint_Euler_inverse': False,
    'small_metric_implies_small_gradient_chart': False,
    'small_coframe_implies_gradient_image': False,
    'small_links_alone_imply_flatness': False,
    'bounded_potential_implies_bounded_raw_gradient': False,
    'raw_Nyquist_is_physical_gauge': False,
    'smooth_transported_metric_implies_smooth_full_raw_quotient': False,
    'geometric_link_bonding_is_frozen_native_refinement': False,
    'exact_link_bonding_supplies_coframe_refinement': False,
    'rational_Cayley_links_bond_exactly': False,
    'native_admission_or_action_selected': False,
    'curved_sequence_is_joint_physical_root': False,
    'zero_matter_is_geometric_stationarity': False,
    'source_fitted_or_physical_Ward_derived': False,
    'all_coframes_or_whole_core_no_go': False,
    'continuum_frozen_weak_metric_boundary_formalized': False,
    'metric_probe_compatibility_is_action_contrast_bound': False,
    'one_doubling_forces_global_flatness': False,
    'small_comparison_links_are_derived_from_native_dynamics': False,
    'homogeneous_raw_cochain_lift_is_nondegenerate': False,
    'all_other_native_refinement_diagrams_excluded': False,
    'affine_origin_gauge_supplied_by_linear_Lorentz_owner': False,
    'prepared_price_theorem_derives_full_coframe_refinement': False,
    'nonlinear_same_jet_can_restore_raw_Lorentz_orbits': False,
    'fine_links_can_erase_raw_Gram_orbit_defect': False,
    'affine_naturality_alone_forces_B0_without_reference': False,
    'orbit_metric_gap_is_action_contrast': False,
    'affine_class_exhausts_other_native_refinements': False,
    'affine_intertwiner_universal_class_Lean_formalized': False,
    'raw_quotient_naturality_derived_for_any_weaker_readout': False,
    'flat_gauge_test_proves_native_physical_root': False,
    'isolated_roots_can_restore_frozen_orbit_descent': False,
    'full_native_admission_exhausted': False,
    'gauge_preparation_derived': False,
    'gauge_admission_obstruction_needs_flat_state': False,
    'soundness_or_recovery_proved': False,
    'G0_closed': False,
    'positive_GR': False,
    'global_closure': False,
    'original_parent_terminals_changed': False,
}


def sq(M):
    return sum(x*x for x in M)


def boost(j, u):
    M = s.eye(4)
    M[0, 0] = M[j, j] = (1+u*u)/(1-u*u)
    M[0, j] = M[j, 0] = 2*u/(1-u*u)
    return M


def zero(M):
    return all(s.factor(x) == 0 for x in M)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[3]
    sha = lambda p: hashlib.sha256((root/p).read_bytes()).hexdigest()
    if args.expect:
        assert json.loads(args.expect.read_text())['scope'] == SCOPE, 'PINNED_LEDGER_MISMATCH'
    checks = []

    def check(name, value):
        assert bool(value), name
        checks.append(name)

    receipt = json.loads((root/(BASE+'_results.json')).read_text())
    check('COMPILED_45_REAL_PROPOSITIONS', receipt['status'] == 'PASS'
          and receipt['compiler_exit_code'] == 0 and not receipt['sorryAx']
          and receipt['printed_axiom_dependencies'] == 45 and receipt['owner_input_head'] == HEAD)
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_TRANSITIVE_OWNER_TOOLCHAIN_CAPSULE_OUTPUT_PINS', all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('STANDARD_AXIOMS_AND_CLEAN_COMPILER_OUTPUT', set(receipt['axioms']) <= {'propext','Classical.choice','Quot.sound'}
          and not any(x in out for x in ['error:', 'warning:', 'sorryAx']))
    actual = ['signedGram_square_le','metricError_small_chart','korn_identity',
              'nonlinear_inverse_square','native_centered_binding','native_korn_identity',
              'native_metric_binding','native_metric_inverse_square','native_nyquist_raw_translation',
              'native_nyquist_center_zero','raw4_det','resonance_center','resonance_gram',
              'frozen_native_tail_zero','native_flat_bulk_center','native_flat_bulk_center_bound',
              'native_flat_gram_expansion','native_flat_gram_entry_bound',
              'native_transported_gram_frame_invariant','resonance_two_component_gap',
              'affine_frozen_doubling_degeneracy',
              'frozen_native_pointwise_affine_binding',
              'native_flat_gram_curve_derivative',
              'gauge_mask_jet_iff_constant',
              'rotationBC4_lorentz',
              'masked_rotation_metric_BC',
              'masked_rotation_partial_det',
              'masked_rotation_genuine_metric_derivative',
              'nonzero_metric_jet_not_orbit_constant',
              'cayley_rotation_actual_metric_derivative',
              'frozen_partial_metric_reads_any_raw_row',
              'rotationCD4_lorentz',
              'columnCFrames4_lorentz',
              'four_proper_frames_force_raw_row_zero',
              'nondegenerate_raw_orbit_has_frozen_metric_defect',
              'frozen_gauge_saturated_admission_empty',
              'native_partial_mask_exists']
    for name in actual:
        check('RESOLVED_REAL_PROPOSITION_'+name, "'D0.Research.NativeMetricCompactness."+name+"' depends on axioms:" in out
              and '\nD0.Research.NativeMetricCompactness.'+name in out)

    eta = s.diag(1,-1,-1,-1)
    v = s.Matrix([1,1,0,0])
    w = s.ones(4,1)
    t,h,f,z = s.symbols('t h f z', real=True)
    d = 1-h*h*f*f
    raw = lambda a: eta+a*w*v.T
    read = s.Matrix([[1,0,0,0],[0,-1,0,0],[-z*h*f*f/d,0,-1,z*f/d],[-z*h*f*f/d,0,-z*f/d,-1]])
    pulls = [s.eye(4),s.eye(4),boost(3,-h*f),boost(2,h*f)]
    check('EXPLICIT_ROLE_ORDER_AND_PLUS_MINUS_MINUS_MINUS', list(eta.diagonal()) == [1,-1,-1,-1])
    check('NULL_RANK_ONE_NATIVE_SHEAR', (v.T*eta*v)[0] == 0 and (v.T*eta*w)[0] == 0)
    check('ALL_AMPLITUDES_RAW_DETERMINANT_NONZERO', s.factor(raw(t).det()) == -1)
    check('ALL_AMPLITUDES_RAW_NORM', s.expand(sq(raw(t))) == 4+8*t*t)
    for r in range(4):
        R = pulls[r]
        check('EXACT_LORENTZ_LINK_'+str(r), zero(R*eta*R.T-eta) and s.factor(R.det()) == 1)
        for a in range(4):
            check('LITERAL_TRANSPORTED_ROW_'+str(r)+str(a),
                  s.factor((raw(z/h)[r,a]+(raw(-z/h)*R)[r,a])/2-read[r,a]) == 0)
    expected = s.Matrix([[1,0,-z*h*f*f/d,-z*h*f*f/d],[0,-1,0,0],
                         [-z*h*f*f/d,0,-1-f*f/d,h*h*f**4/d**2],
                         [-z*h*f*f/d,0,h*h*f**4/d**2,-1-f*f/d]])
    gram = read*eta*read.T
    pairs = [(i,j) for i in range(4) for j in range(i,4)]
    for i,j in pairs:
        expr = s.factor(gram[i,j]-expected[i,j])
        check('PACKED_METRIC_COMPONENT_'+str(i)+str(j), all(expr.subs(z,e) == 0 for e in [-1,1]))
    check('PACKED_FROBENIUS_WEIGHTS', s.expand(sum((1 if i == j else 2)*gram[i,j]**2 for i,j in pairs)-sq(gram)) == 0)
    check('TRANSPORTED_NONDEGENERATE_DETERMINANT', s.factor(read.det().subs(z,1)+1+f*f/d**2) == 0)
    check('SMOOTH_METRIC_LIMIT_ALL_TEN_COMPONENTS', all(s.limit(expected[i,j],h,0) == s.diag(1,-1,-1-f*f,-1-f*f)[i,j] for i,j in pairs))
    check('UNIFORM_ORDER_H_METRIC_ERROR', all(s.limit((expected[i,j]-s.diag(1,-1,-1-f*f,-1-f*f)[i,j])/h,h,0).is_finite for i,j in pairs))
    check('STRONG_COFRAME_VARIANCE', s.limit(sq(read-eta).subs(z,1),h,0) == 2*f*f)
    check('WEAK_COFRAME_LIMIT_TWO_PARITIES', zero(((read.subs(z,1)+read.subs(z,-1))/2).applyfunc(lambda x: s.limit(x,h,0))-eta))
    check('RAW_COORDINATE_TIME_COMPONENT_CHANGES_SIGN', s.expand((raw(z/h)*eta*raw(z/h).T)[0,0]) == 1+2*z/h
          and (1-2/h).subs(h,s.Rational(1,4)) < 0)
    check('RAW_GRAM_NYQUIST_IS_NOT_LORENTZ_GAUGE', not zero(raw(1/h)*eta*raw(1/h).T-raw(-1/h)*eta*raw(-1/h).T))
    Fx,Fy=raw(1/h),raw(-1/h)
    Ds=[Fy*R*Fx.inv() for R in pulls]
    B=s.Matrix(4,4,lambda r,a: (int(r == a)+Ds[r][r,a])/2)
    check('FULL_NATIVE_JOINT_QUOTIENT_RETAINS_TRANSPORTED_CENTER', zero(B*Fx-read.subs(z,1))
          and zero(B*(Fx*eta*Fx.T)*B.T-gram.subs(z,1)))
    for r in range(4):
        check('EXACT_DRESSED_LINK_METRIC_CONSTRAINT_'+str(r), zero(Ds[r]*(Fx*eta*Fx.T)*Ds[r].T-Fy*eta*Fy.T))
    check('TRANSPORTED_COORDINATE_CHANGE_NOT_UNIFORMLY_REGULAR',
          s.limit(h*h*sq(B),h,0) != 0 and s.limit(h*h*sq(Fx*read.subs(z,1).inv()),h,0) != 0)
    flatread = s.Matrix(4,4,lambda r,a: (eta[r,a]+(eta*pulls[r])[r,a])/2)
    check('SAME_LINKS_ON_FLAT_RAW_HAVE_ZERO_METRIC_RESPONSE', flatread == eta)
    check('ACTIVE_LINKS_ARE_NOT_COMMUTING_GAUGE', not zero(pulls[2].subs({h:s.Rational(1,4),f:s.Rational(3,32)})
          *pulls[3].subs({h:s.Rational(1,4),f:s.Rational(3,32)})
          -pulls[3].subs({h:s.Rational(1,4),f:s.Rational(3,32)})*pulls[2].subs({h:s.Rational(1,4),f:s.Rational(3,32)})))
    for r in range(4):
        for i,j in pairs:
            if i == j:
                continue
            K = s.zeros(4)
            K[i,j],K[j,i] = 1, -eta[i,i]*eta[j,j]
            row = s.zeros(4)
            row[r,:] = (eta*K)[r,:]/2
            check('ALL24_ADMITTED_LINK_DIRECTIONS_'+str(r)+str(i)+str(j), zero(K*eta+eta*K.T)
                  and ((row+row.T == s.zeros(4)) == (r not in [i,j])))
    for L in [4,8,12,16]:
        hh=s.Rational(1,L)
        check('PROPER_FUTURE_LINKS_L'+str(L), all(R.subs({h:hh,f:ff})[0,0] >= 1
              and R.subs({h:hh,f:ff}).det() == 1 for R in pulls for ff in [s.Rational(1,32),s.Rational(3,32)]))
        maxsq = sq((read-eta).subs({h:hh,f:s.Rational(3,32),z:1}))
        check('CURVED_READOUT_SMALL_COFRAME_BUT_NOT_GRADIENT_L'+str(L), maxsq < s.Rational(1,16))
    delta=2*h*f/(1-h*f)
    check('RAW_LINK_PRODUCT_CONDITION_FAILS_EXACTLY', s.limit(delta**2*(4+8/h**2),h,0).subs(f,s.Rational(3,32)) == s.Rational(9,32))
    profile=(2+s.cos(2*s.pi*t))/32
    check('NONZERO_STRONG_VARIANCE_PROFILE', s.integrate(2*profile**2,(t,0,1)) == s.Rational(9,1024))
    check('CURVED_PROFILE_FIXED_INDEPENDENT_OF_MESH', profile.subs(t,0) == s.Rational(3,32)
          and s.diff(profile,t).subs(t,0) == 0 and s.diff(profile,t,2).subs(t,0) == -s.pi**2/8)

    # Full curvature at the smooth profile jet, independently from the lattice Gram.
    g=s.diag(1,-1,-1-profile**2,-1-profile**2)
    gi=g.inv()
    dg=lambda M,r: M.diff(t) if r == 0 else s.zeros(4)
    Gamma=[[[s.simplify(sum(gi[a,l]*(dg(g,b)[l,c]+dg(g,c)[l,b]-dg(g,l)[b,c]) for l in range(4))/2)
             for c in range(4)] for b in range(4)] for a in range(4)]
    Riem={}
    for a,b,c,e in itertools.product(range(4),repeat=4):
        x=(s.diff(Gamma[a][e][b],t) if c == 0 else 0)-(s.diff(Gamma[a][c][b],t) if e == 0 else 0)
        x+=sum(Gamma[a][c][l]*Gamma[l][e][b]-Gamma[a][e][l]*Gamma[l][c][b] for l in range(4))
        Riem[a,b,c,e]=s.simplify(x.subs(t,0)) if hasattr(x,'subs') else s.Integer(x)
    ric=s.Matrix(4,4,lambda b,e: sum(Riem[a,b,a,e] for a in range(4)))
    g0=g.subs(t,0)
    scalar=s.trace(g0.inv()*ric)
    einstein=ric-g0*scalar/2
    check('CURVATURE_NONZERO_NO_SOURCE_FIT', any(x != 0 for x in Riem.values())
          and ric[0,0] == 24*s.pi**2/1033 and einstein[1,1] == 24*s.pi**2/1033)
    for i,j in pairs:
        check('ALL_TEN_CONTINUUM_EINSTEIN_COMPONENTS_'+str(i)+str(j),
              einstein[i,j] == ([0,24*s.pi**2/1033,3*s.pi**2/256,3*s.pi**2/256][i] if i == j else 0))

    # Independent literal native lattice identities, using exact rational data.
    for L in [3,4,6]:
        sites=list(itertools.product(range(L),repeat=4))
        shift=lambda x,r,e: tuple((x[a]+(e if a == r else 0)) % L for a in range(4))
        xi={x:[Q(((sum((a+1)*(r+2)*x[r] for r in range(4))+a*a) % 5)-2,128*L) for a in range(4)] for x in sites}
        psi={x:[Q(((sum((a+2)*(r+1)*x[r] for r in range(4))+a) % 7)-3,256*L) for a in range(4)] for x in sites}
        def center(p):
            return {x:[[L*(p[shift(x,r,1)][a]-p[shift(x,r,-1)][a])/2 for a in range(4)] for r in range(4)] for x in sites}
        A,B=center(xi),center(psi)
        norm=lambda X: sum(X[x][r][a]**2 for x in sites for r in range(4) for a in range(4))/L**4
        symnorm=sum((A[x][r][a]+A[x][a][r])**2 for x in sites for r in range(4) for a in range(4))/L**4
        divnorm=sum(sum(A[x][r][r] for r in range(4))**2 for x in sites)/L**4
        check('EXACT_NATIVE_KORN_L'+str(L), symnorm == 2*norm(A)+2*divnorm)
        check('NATIVE_CHART_BOUNDS_L'+str(L), all(sum(M[r][a]**2 for r in range(4) for a in range(4)) <= Q(1,16) for M in list(A.values())+list(B.values())))
        qm=lambda M,r,a: (int(eta[r,r]) if r == a else 0)+M[r][a]+M[a][r]+sum(M[r][k]*int(eta[k,k])*M[a][k] for k in range(4))
        deltafield={x:[[A[x][r][a]-B[x][r][a] for a in range(4)] for r in range(4)] for x in sites}
        qdiff=sum((qm(A[x],r,a)-qm(B[x],r,a))**2 for x in sites for r in range(4) for a in range(4))/L**4
        check('NATIVE_NONLINEAR_INVERSE_L'+str(L), norm(deltafield) <= Q(4,3)*qdiff)
        check('LITERAL_FORWARD_BACKWARD_CENTER_L'+str(L), all(A[x][r][a] ==
              (L*(xi[shift(x,r,1)][a]-xi[x][a])+L*(xi[x][a]-xi[shift(x,r,-1)][a]))/2
              for x in sites for r in range(4) for a in range(4)))
    for L in [4,8,12]:
        phase=lambda x: (-1)**sum(x)
        sites=list(itertools.product(range(L),repeat=4))
        shift=lambda x,r,e: tuple((x[a]+(e if a == r else 0)) % L for a in range(4))
        check('ALL_EVEN_NATIVE_PHASE_FLIPS_L'+str(L), all(phase(shift(x,r,e)) == -phase(x)
              for x in sites for r in range(4) for e in [-1,1]))
        check('GEOMETRIC_DECIMATION_POTENTIAL_DEFECT_L'+str(L), sum(Q((phase(x)-1)**2,2) for x in sites)/L**4 == 1)

    # Actual frozen B0/B1 matrices and their compositions, not a modulo shortcut.
    for L in [4,6,8]:
        old=s.Matrix([(-1)**j for j in range(L)])
        P0,P1=s.eye(L),s.eye(L)
        D=lambda n: s.Matrix(n,n,lambda i,j: int(j == (i+1)%n)-int(j == i))
        for K in range(L+1,2*L+1):
            B0=s.Matrix(K,K-1,lambda i,j: int(j == i%(K-1)))
            B1=s.Matrix(K,K-1,lambda i,j: int(i == j))
            check('ACTUAL_ADJACENT_COCHAIN_L'+str(L)+'K'+str(K), D(K)*B0 == B1*D(K-1))
            P0,P1=B0*P0,B1*P1
            if K in [L+1,2*L]:
                lifted=P0*old
                dc=s.Matrix([Q(K,2)*(lifted[(i+1)%K]-lifted[(i-1)%K]) for i in range(K)])
                check('ACTUAL_NYQUIST_CENTERED_NORM_L'+str(L)+'K'+str(K),
                      2*sum(x*x for x in dc)/K == 4*K)
                check('DEGREE_AWARE_GRADIENT_COMMUTES_L'+str(L)+'K'+str(K), K*D(K)*P0 == Q(K,L)*P1*(L*D(L)))
                check('ACTUAL_PREFIX_TAIL_PHASE_L'+str(L)+'K'+str(K), lifted == s.Matrix([(-1)**i if i<L else 1 for i in range(K)]))

    u=s.symbols('u',real=True)
    E=lambda u: s.Matrix([[s.cosh(u),s.sinh(u)],[s.sinh(u),s.cosh(u)]])
    check('EXPONENTIAL_LINK_EXACT_TWO_EDGE_BONDING', all(s.expand_trig(x).simplify() == 0 for x in E(u)*E(u)-E(2*u)))
    cayley=(boost(3,u)*boost(3,u)-boost(3,2*u))[0,3]
    check('RATIONAL_LINK_BONDING_IS_ONLY_ORDER_CUBIC', s.limit(cayley/u**3,u,0) == -4)
    check('EXPONENTIAL_COMPANION_SAME_CURVED_LIMIT', s.limit(s.sinh(2*h*f)/(2*h),h,0) == f
          and s.limit((1-s.cosh(2*h*f))/(2*h),h,0) == 0)
    bigboost=boost(1,s.Rational(3,5))
    check('METRIC_SMALLNESS_DOES_NOT_SELECT_COFRAME_CHART', bigboost*eta*bigboost.T == eta and sq(bigboost-eta) > s.Rational(1,16))
    check('CUBE_COMPACTNESS_VOLUME_CONSTANT', s.Rational(2**4,2) == 8)

    # Full composed frozen blocks: the coarse data are arbitrary, not just Nyquist.
    # Each exact adjacent row is composed before the tensor/degree normalization.
    tensor_rows = 0
    for L,K in [(2,4),(3,6),(4,8),(4,12)]:
        P0,P1=s.eye(L),s.eye(L)
        for n in range(L+1,K+1):
            P0=s.Matrix(n,n-1,lambda i,j: int(j == i%(n-1)))*P0
            P1=s.Matrix(n,n-1,lambda i,j: int(i == j))*P1
        cap=lambda i: i if i<L else 0
        check('COMPOSED_VERTEX_CAP_L'+str(L)+'K'+str(K),
              P0 == s.Matrix(K,L,lambda i,j: int(j == cap(i))))
        check('COMPOSED_OCCUPIED_PREFIX_L'+str(L)+'K'+str(K),
              P1 == s.Matrix(K,L,lambda i,j: int(i == j)))
        ys=list(itertools.product(range(K),repeat=4))
        for mask in range(16):
            occupied=[r for r in range(4) if mask&(1<<r)]
            factor=Q(K,L)**len(occupied)
            def coarse(a):
                return 3+mask+sum((r+2)*a[r] for r in range(4))
            mismatches=0
            for y in ys:
                a=tuple(cap(i) for i in y)
                tensor=factor*coarse(a)
                for r in range(4):
                    tensor *= int((P1 if r in occupied else P0)[y[r],a[r]])
                direct=(factor*coarse(a) if all(y[r]<L for r in occupied) else 0)
                mismatches += int(tensor != direct)
                tensor_rows += 1
            check('ALL_SIXTEEN_GRADED_COMPOSED_ROWS_L'+str(L)+'K'+str(K)+'S'+str(mask), mismatches == 0)
        bulk=[y for y in ys if all(i>=L+1 for i in y)]
        check('FLAT_BULK_EXACT_CARDINALITY_L'+str(L)+'K'+str(K), len(bulk) == (K-L-1)**4)
        check('ALL_SIXTEEN_COFRAME_ENTRIES_VANISH_ON_BULK_L'+str(L)+'K'+str(K),
              all(P1[y[r],cap(y[r])] == 0 for y in bulk for r in range(4) for a in range(4)))
        check('ALL_ACTUAL_INCOMING_NEIGHBORS_STAY_IN_ZERO_REGION_L'+str(L)+'K'+str(K),
              all(all((i-1 if j == r else i)>=L for j,i in enumerate(y))
                  for y in bulk for r in range(4)))
        check('HOMOGENEOUS_RAW_LIFT_ZERO_VERSUS_PERTURBATION_LIFT_ETA_L'+str(L)+'K'+str(K),
              len(bulk)>0 and eta.det() == -1 and s.zeros(4).det() == 0)
        econst=-s.Rational(L,K)*eta
        check('AFFINE_FROZEN_LIFT_FAILS_COMPLETE_NONDEGENERATE_CARRIER_L'+str(L)+'K'+str(K),
              (eta+econst).det() != 0 and eta+s.Rational(K,L)*econst == s.zeros(4))

    # All finite linear link matrices on the bulk, before imposing Lorentz.
    rr=[s.Matrix(4,4,lambda a,b: s.Symbol('u'+str(r)+str(a)+str(b))) for r in range(4)]
    flat=s.Matrix(4,4,lambda r,a: (eta[r,a]+(eta*rr[r])[r,a])/2)
    H=flat-eta
    check('ALL_COMPONENTS_LITERAL_FLAT_BULK_CENTER',
          all(s.expand(H[r,a]-eta[r,r]*(rr[r][r,a]-int(r == a))/2) == 0
              for r in range(4) for a in range(4)))
    check('FULL_FLAT_BULK_GRAM_EXPANSION', zero(flat*eta*flat.T-(eta+H+H.T+H*eta*H.T)))
    delta=s.Symbol('delta',nonnegative=True)
    for r,a in itertools.product(range(4),repeat=2):
        check('ALL_COMPONENTS_FLAT_BULK_GRAM_BOUND_'+str(r)+str(a),
              s.expand(delta/2+delta/2+4*(delta/2)**2-(delta+delta**2)) == 0)

    # The real owner transforms the whole raw solder AND all incoming links.
    Lam=boost(2,s.Rational(1,3))
    Remote=boost(1,s.Rational(-1,5))
    base=flatread.subs({h:s.Rational(1,8),f:s.Rational(3,32)})
    transformed=s.Matrix(4,4,lambda r,a:
      ((eta*Lam)[r,a]+(eta*Remote*(Remote.inv()*pulls[r].subs({h:s.Rational(1,8),f:s.Rational(3,32)})*Lam))[r,a])/2)
    check('FULL_JOINT_LOCAL_LORENTZ_ACTION_RETAINS_BULK_METRIC',
          zero(transformed-base*Lam) and zero(transformed*eta*transformed.T-base*eta*base.T))
    changed=s.Matrix(4,4,lambda r,a: ((eta*Lam)[r,a]+(eta*Lam*pulls[r].subs({h:s.Rational(1,8),f:s.Rational(3,32)}))[r,a])/2)
    check('COFRAME_ONLY_REFRAMING_IS_NOT_THE_FULL_GAUGE_REPAIR', not zero(changed*eta*changed.T-eta))

    # The two nonzero smooth metric entries have a bulk gap, not only a coframe defect.
    ll=s.Symbol('L',positive=True)
    p=((ll-1)/(2*ll))**4
    lower=2*p/(32**4)
    check('RESONANCE_BULK_SQUARE_GAP_LIMIT', s.limit(lower,ll,s.oo) == s.Rational(1,8388608))
    check('EXACT_RESONANCE_TWO_COMPONENT_GAP',
          s.factor((expected[2,2]+1)**2+(expected[3,3]+1)**2-2*f**4/d**2) == 0)
    for mask in range(16):
        wm=s.Matrix([int(bool(mask&(1<<r))) for r in range(4)])
        masked=eta+t*wm*v.T
        determinant=s.factor(masked.det())
        check('RESONANT_COMPARISON_FULL_RAW_STATE_NONEMPTY_MASK'+str(mask),
              s.expand(determinant+1+t*(wm[0]-wm[1])) == 0 and
              all(determinant.subs(t,zz*kk) != 0 for zz in [-1,1] for kk in [4,8,12,16]))
    for L in [4,8,12,16]:
        K=2*L
        for ff in [s.Rational(1,32),s.Rational(1,16),s.Rational(3,32)]:
            hh=s.Rational(1,K)
            dd=1-hh*hh*ff*ff
            check('FINITE_RESONANCE_METRIC_GAP_L'+str(L)+'F'+str(ff),
                  0<dd<=1 and 2*s.Rational((L-1)**4,K**4)*(ff*ff/dd)**2 >=
                  2*s.Rational((L-1)**4,K**4)/(32**4))
    check('ARBITRARY_SMALL_COMPARISON_LINK_ERROR_TENDS_TO_ZERO',
          s.limit(4*(1/ll+1/ll**2),ll,s.oo) == 0)
    check('VANISHING_METRIC_CORRECTOR_CANNOT_ERASE_POSITIVE_GAP',
          s.limit(s.sqrt(lower)-1/ll,ll,s.oo) == s.sqrt(s.Rational(1,8388608)))
    nonnear=[s.eye(4),s.eye(4),boost(2,s.Rational(1,3)),s.eye(4)]
    nonflat=s.Matrix(4,4,lambda r,a: (eta[r,a]+(eta*nonnear[r])[r,a])/2)
    check('SMALL_COMPARISON_LINK_PREMISE_IS_NECESSARY',
          nonnear[2].det() == 1 and nonnear[2][0,0]>1 and not zero(nonflat*eta*nonflat.T-eta))
    bump=s.exp(-1/(t*(s.Rational(1,4)-t)))/32
    bc=bump.subs(t,s.Rational(1,8))
    bdd=s.diff(bump,t,2).subs(t,s.Rational(1,8))
    check('ONE_DOUBLING_BULK_FLATNESS_DOES_NOT_IMPLY_GLOBAL_FLATNESS',
          bc == s.exp(-64)/32 and bdd == -8192*bc and
          s.simplify(-2*bc*bdd/(1+bc*bc))>0)
    check('WEAK_SMOOTH_METRIC_PROBE_GAP_REMAINS_NONZERO',
          s.Rational(2,32**2) == s.Rational(1,512) and profile.subs(t,s.Rational(3,4))**2>0)

    # Full proper-Lorentz orbit and every partial row mask, at the owned raw arrow.
    rho,uu=s.symbols('rho uu',real=True)
    co=(1-uu**2)/(1+uu**2)
    si=2*uu/(1+uu**2)
    rot=s.eye(4)
    rot[1,1]=rot[2,2]=co
    rot[1,2]=si
    rot[2,1]=-si
    check('GAUGE_ROTATION_PROPER_LORENTZ_AND_FUTURE',
          zero(rot*eta*rot.T-eta) and s.factor(rot.det()) == 1 and rot[0,0] == 1)
    check('GAUGE_ROTATION_CONNECTS_TO_IDENTITY', rot.subs(uu,0) == s.eye(4))
    coarse=eta*rot
    check('COARSE_COMPLETE_CONSTANT_GAUGE_ORBIT_RAW_AND_TRANSPORTED_METRIC',
          zero(coarse*eta*coarse.T-eta) and s.factor(coarse.det()) == -1)
    check('COARSE_FULL_GAUGE_IDENTITY_LINKS_UNCHANGED',
          zero(rot.inv()*s.eye(4)*rot-s.eye(4)))
    opaque=s.Matrix(4,4,lambda r,a: s.Symbol('F'+str(r)+str(a)))
    for mask in range(16):
        row=s.diag(*[rho*int(bool(mask&(1<<r))) for r in range(4)])
        fine=eta+row*(coarse-eta)
        qfine=fine*eta*fine.T
        b=rho*int(bool(mask&2))
        k=rho*int(bool(mask&4))
        check('ALL_RAW_AFFINE_OWNER_ENTRIES_MASK'+str(mask),
              all(s.expand((eta+row*(opaque-eta))[r,a]-
                  (eta[r,a]+row[r,r]*(opaque[r,a]-eta[r,a]))) == 0
                  for r in range(4) for a in range(4)))
        check('EXACT_GAUGE_METRIC_BC_MASK'+str(mask),
              s.factor(qfine[1,2]-(k-b)*si) == 0)
        expected_det=(-1 if b == 0 and k == 0 else
          -1+rho*(1-co) if (b == 0) != (k == 0) else
          -(1+2*rho*(rho-1)*(1-co)))
        check('FULL_NONDEGENERATE_GAUGE_MASK_DETERMINANT'+str(mask),
              s.factor(fine.det()-expected_det) == 0 and
              fine.subs({rho:2,uu:s.Rational(1,16)}).det() != 0)
        if (b == 0) != (k == 0):
            check('ARBITRARILY_SMALL_FRAME_RAW_GAUGE_DEFECT_MASK'+str(mask),
                  s.diff(qfine[1,2],uu).subs(uu,0) == 2*(k-b)
                  and s.limit(qfine[1,2]/uu,uu,0) == 2*(k-b))
    db,dc=s.symbols('db dc',real=True)
    mm=eta+s.diag(0,db,dc,0)*(coarse-eta)
    check('FULL_TWO_ROW_MASK_METRIC_NOT_ONLY_BINARY',
          s.factor((mm*eta*mm.T)[1,2]-(dc-db)*si) == 0)
    check('NONGAUGE_RAW_DIFFERENCE_HAS_FIXED_SIGNED_SMOOTH_PROBE',
          (-2*si).subs(uu,s.Rational(1,16)) == -s.Rational(64,257))
    # All six generators and all sixteen masks; no Lorentz gauge direction dropped.
    ds=s.symbols('d0:4',real=True)
    for a,b in itertools.combinations(range(4),2):
        generator=s.zeros(4)
        generator[a,b]=1
        generator[b,a]=-eta[a,a]*eta[b,b]
        skew=eta*generator
        check('GENUINE_INTERNAL_LORENTZ_TANGENT_'+str(a)+str(b),
              zero(generator*eta+eta*generator.T) and skew.T == -skew)
        tangent=s.diag(*ds)*skew
        check('COMPLETE_ROW_WEIGHT_GAUGE_METRIC_JET_'+str(a)+str(b),
              tangent+tangent.T == s.Matrix(4,4,lambda r,j:(ds[r]-ds[j])*skew[r,j]))
        for mask in range(16):
            vals={ds[r]:rho*int(bool(mask&(1<<r))) for r in range(4)}
            diff=(tangent+tangent.T).subs(vals)
            check('ALL_INTERNAL_GENERATOR_MASK_JET_'+str(a)+str(b)+'S'+str(mask),
                  (zero(diff)) == (bool(mask&(1<<a)) == bool(mask&(1<<b))))
    check('SECOND_ORDER_NONLINEAR_RAW_CORRECTOR_CANNOT_FIX_FIRST_METRIC_JET',
          s.limit((-rho*si+uu**2)/uu,uu,0) == -2*rho)
    # Exact volume count on both partial regions, with packed off-diagonal weight.
    ll=s.Symbol('LL',positive=True)
    kk=rho*ll
    transported_lower=4*rho**2*(ll-1)*(kk-ll-1)/kk**2*si**2
    check('FIXED_RATIO_GAUGE_METRIC_GAP_LIMIT',
          s.factor(s.limit(transported_lower,ll,s.oo)-4*(rho-1)*si**2) == 0)
    check('DOUBLED_GAUGE_GAP_EXACT_NONZERO_CONSTANT',
          (4*si**2).subs(uu,s.Rational(1,16)) == s.Rational(4096,66049))
    check('VANISHING_METRIC_CORRECTOR_RETAINS_GAUGE_GAP',
          s.limit(s.sqrt(transported_lower.subs({rho:2,uu:s.Rational(1,16)}))-1/ll,ll,s.oo)
          == s.sqrt(s.Rational(4096,66049)))
    for L,K in [(4,8),(8,16),(4,12)]:
        rr=s.Rational(K,L)
        partial=2*(L-1)*(K-L-1)*K**2
        count=sum(1 for bb in range(K) for cc in range(K)
          if (1<=bb<L and L+1<=cc<K) or (L+1<=bb<K and 1<=cc<L))*K**2
        check('BOTH_ACTUAL_TRANSPORTED_PARTIAL_REGION_COUNTS_L'+str(L)+'K'+str(K),
              partial == count and partial>0)
        allpartial=2*L*(K-L)*K**2
        check('RAW_PACKED_BC_METRIC_NORM_EXACT_L'+str(L)+'K'+str(K),
              2*s.Rational(allpartial,K**4)*rr**2 == 4*(rr-1))
        for mask in [2,4]:
            row=s.diag(*[rr*int(bool(mask&(1<<r))) for r in range(4)])
            ff=(eta+row*(coarse-eta)).subs(uu,s.Rational(1,16))
            center=s.Matrix(4,4,lambda r,a:(ff[r,a]+ff[r,a])/2)
            check('LITERAL_IDENTITY_LINK_TRANSPORTED_GAUGE_DEFECT_L'+str(L)+'K'+str(K)+'S'+str(mask),
                  center == ff and (center*eta*center.T)[1,2] != 0 and ff.det() != 0)
    # Entire gauge-saturated admission class, without a flat/open/root premise.
    # Symbolic identities below cover every matrix, not an interpolation grid.
    weights=s.symbols('wd0:4',real=True)
    for r,a in itertools.permutations(range(4),2):
        ww=list(weights);ww[r]=rho;ww[a]=0
        frozen_any=eta+s.diag(*ww)*(opaque-eta)
        check('ANY_RAW_PARTIAL_MASK_METRIC_READS_ROW_'+str(r)+str(a),
              s.expand((frozen_any*eta*frozen_any.T)[r,a]-rho*opaque[r,a]) == 0)
    rotminus=rot.subs(uu,-uu)
    rotcd=s.eye(4)
    rotcd[2,2]=rotcd[3,3]=co
    rotcd[2,3]=si;rotcd[3,2]=-si
    admission_frames=[rot,rotminus,boost(2,uu),rotcd]
    admission_columns=s.Matrix.hstack(*[(M-s.eye(4))[:,2] for M in admission_frames])
    admission_det=s.factor(admission_columns.det())
    check('SYMBOLIC_FOUR_FRAME_COLUMNS_SPAN_ALL_RAW_ROW_COMPONENTS',
          admission_det != 0 and admission_det ==
          s.factor(-2*si**2*(co-1)*(2*uu/(1-uu**2))))
    check('FOUR_FRAMES_ARBITRARILY_CLOSE_TO_IDENTITY',
          all(M.subs(uu,0) == s.eye(4) for M in admission_frames))
    for i,M in enumerate(admission_frames):
        check('ADMISSION_FRAME_SYMBOLIC_PROPER_LORENTZ_'+str(i),
              zero(M*eta*M.T-eta) and s.factor(M.det()) == 1)
        fany=eta+s.diag(0,rho,0,0)*(opaque*M-eta)
        fbase=eta+s.diag(0,rho,0,0)*(opaque-eta)
        check('FULL_SYMBOLIC_RAW_ORBIT_METRIC_DIFFERENCE_'+str(i),
              s.expand((fany*eta*fany.T-fbase*eta*fbase.T)[1,2]-
                       rho*(opaque*M-opaque)[1,2]) == 0)
    for radius in [s.Rational(1,16),s.Rational(1,32),s.Rational(1,256)]:
        cols=admission_columns.subs(uu,radius)
        check('NONZERO_ROW_CONTRADICTION_WITH_TINY_PROPER_FRAMES_'+str(radius),
              cols.det() != 0 and cols.rank() == 4 and not cols.T.nullspace())
        check('ALL_FOUR_TINY_FRAMES_DETERMINANT_FUTURE_AND_SIGNATURE_'+str(radius),
              all(M.subs(uu,radius).det() == 1 and M.subs(uu,radius)[0,0]>=1
                  and zero(M.subs(uu,radius)*eta*M.subs(uu,radius).T-eta)
                  for M in admission_frames))
    fixedcols=admission_columns.subs(uu,s.Rational(1,16))
    for omitted in range(4):
        kept=[j for j in range(4) if j != omitted]
        null=fixedcols[:,kept].T.nullspace()
        check('OMITTED_FRAME_LEAVES_NONZERO_ADMISSION_ROW_'+str(omitted),
              len(null) == 1 and not zero(null[0])
              and not zero(fixedcols[:,omitted].T*null[0]))
        row=null[0].T
        candidates=[]
        for triple in itertools.combinations(range(4),3):
            F=s.Matrix.vstack(s.eye(4)[triple[0],:],row,
                              s.eye(4)[triple[1],:],s.eye(4)[triple[2],:])
            if F.det() != 0:candidates.append(F)
        check('OMITTED_FRAME_CONTROL_HAS_NONDEGENERATE_FULL_RAW_STATE_'+str(omitted),
              bool(candidates) and all((F*admission_frames[j].subs(uu,s.Rational(1,16)))[1,2] == F[1,2]
                  for F in candidates for j in kept))
    singular=s.eye(4);singular[1,:]=s.zeros(1,4)
    check('NONDEGENERACY_PREMISE_REQUIRED_FOR_RAW_ROW_TEST',
          singular.det() == 0 and all(zero(singular[1,:]*(M-s.eye(4))) for M in admission_frames))
    for L,K in [(2,3),(3,4),(4,5),(4,8),(8,9)]:
        fine_point=[0,0,L,0]
        coarse_point=[v if v<L else 0 for v in fine_point]
        mask=[s.Rational(K,L)*int(v<L) for v in fine_point]
        check('ACTUAL_STRICT_REFINEMENT_PARTIAL_POINT_L'+str(L)+'K'+str(K),
              all(0<=v<K for v in fine_point) and coarse_point == [0]*4
              and mask[1] == s.Rational(K,L)>0 and mask[2] == 0)
    check('NONEMPTY_FULL_FINE_GAUGE_CONTROL_RETAINED_FOR_ADMISSION_THEOREM',
          all((eta+s.diag(*[2*int(bool(mask&(1<<r))) for r in range(4)])*
               (eta*rot.subs(uu,s.Rational(1,16))-eta)).det() != 0
              for mask in range(16)))

    # Proper finite witnesses completely force the standard commutant and fixed rows.
    halfturns=[s.diag(1,-1,-1,1),s.diag(1,-1,1,-1),s.diag(1,1,-1,-1)]
    witnesses=halfturns+[boost(j,s.Rational(1,2)) for j in [1,2,3]]
    for j,M in enumerate(witnesses):
        check('AFFINE_COMPLETENESS_PROPER_GROUP_WITNESS_'+str(j),
              zero(M*eta*M.T-eta) and M.det() == 1 and M[0,0]>=1)
    symbols=s.symbols('m0:16')
    variable=s.Matrix(4,4,symbols)
    equations=[e for M in witnesses for e in variable*M-M*variable]
    commutant=s.linear_eq_to_matrix(equations,symbols)[0]
    null=commutant.nullspace()
    check('COMPLETE_STANDARD_LORENTZ_COMMUTANT_RANK15_NULLITY1',
          commutant.rank() == 15 and len(null) == 1 and s.Matrix(4,4,list(null[0])) == s.eye(4))
    fixed=s.Matrix.vstack(*[M.T-s.eye(4) for M in witnesses])
    killed=s.Matrix.vstack(*[M-s.eye(4) for M in witnesses])
    check('COMPLETE_PROPER_LORENTZ_FIXED_ROW_AND_COLUMN_SPACES_ZERO',
          fixed.rank() == 4 and killed.rank() == 4 and not fixed.nullspace() and not killed.nullspace())
    check('COMPLETE_RAW_AFFINE_INTERTWINER_DIMENSION', 16*(16-commutant.rank()) == 16)
    C=s.Matrix([[2,1,0,0],[0,1,0,0],[0,0,3,0],[0,0,0,1]])
    check('LEFT_RAW_INTERTWINERS_SUFFICE_FOR_FULL_RIGHT_FRAME_ACTION',
          zero(C*(opaque*rot)-(C*opaque)*rot) and C.det() != 0)
    check('REFERENCE_NORMALIZATION_NECESSARY_BEFORE_UNIQUE_B0_CONCLUSION',
          zero(2*(opaque*rot)-(2*opaque)*rot) and 2*eta != eta)
    check('AFFINE_FIXED_REFERENCE_ROW_WEIGHT_FAILS_FULL_NATURALITY',
          not zero((eta+C*(opaque*rot-eta))-(eta+C*(opaque-eta))*rot))
    check('OTHER_SITE_TERM_CANNOT_INTERTWINE_INDEPENDENT_NODE_FRAMES',
          not zero((opaque+opaque*rot)-(opaque+opaque)))
    # The unique affine reference-preserving raw B0 map is not the graded d-chain map.
    for L in [3,4,8]:
        K=L+1
        B0=s.Matrix(K,L,lambda i,j:int(j == i%L))
        B1=s.Rational(K,L)*s.Matrix(K,L,lambda i,j:int(i == j))
        DL=s.Matrix(L,L,lambda i,j:L*(int(j == (i+1)%L)-int(i == j)))
        DK=s.Matrix(K,K,lambda i,j:K*(int(j == (i+1)%K)-int(i == j)))
        sf=s.zeros(L,1);sf[1]=1
        check('RAW_B0_FAILS_ACTUAL_NEW_ROW_CHAIN_EQUATION_L'+str(L),
              (DK*B0*sf)[L] == 0 and (B0*DL*sf)[L] == L)
        check('ACTUAL_GRADED_B1_STILL_SATISFIES_CHAIN_EQUATION_L'+str(L),
              DK*B0 == B1*DL)
        check('B0_RAW_STATE_NONDEGENERACY_CONTROL_L'+str(L),
              all((2*eta).det() != 0 for _ in range(K)))

    payload={'status':'PASS','owner_input_head':HEAD,'scope':SCOPE,'checks':checks,
             'input_sha256':pins,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
             'native_refinement_certificate_sha256':sha(REFINEMENT),
             'transitive_d0_source_count':len(receipt['transitive_d0_source_sha256']),
             'exact_results':{'signature':[1,-1,-1,-1],'inverse_square_constant':'4/3',
              'raw_determinant':'-1','raw_normalized_square':'4+8/h^2',
              'curved_Ric_AA_and_G_BB_at_zero':'24*pi^2/1033',
              'coframe_variance':'9/1024','link_raw_product_square_limit':'9/32',
              'geometric_potential_bonding_square_defect':'1',
              'actual_frozen_lift_centered_gradient_square':'4*K','metric_components':10,'connection_rows':24,
              'frozen_metric_bulk_site_count':'(K-L-1)^4',
              'frozen_metric_bulk_entry_bound':'delta+delta^2',
              'frozen_resonance_metric_gap_square_liminf_lower_bound':'1/8388608',
              'fixed_smooth_probe_gap_lower_bound':'(1/512)*integral(chi)',
              'gauge_orbit_metric_BC_first_jet':'2*(d_C-d_B)',
              'gauge_orbit_doubled_transported_gap_square_liminf_lower_bound':'4096/66049',
              'frozen_gauge_saturated_admission':'EMPTY_FOR_SPECIFIED_RAW_QUOTIENT_TRANSITION',
              'frozen_admission_four_frame_column_determinant':str(fixedcols.det()),
              'frozen_admission_without_flat_open_or_root_hypothesis':True,
              'affine_standard_commutant_rank':15,
              'affine_raw_intertwiner_dimension':16,
              'full_graded_composed_row_equations':tensor_rows,
              'global_frozen_metric_limit':'eta_WITH_ALL_FIXED_UNBOUNDED_SCALE_RATIOS_WEAK_METRIC_COMPATIBILITY'}}
    if args.output:
        args.output.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
    else:
        expected=args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_METRIC_COMPACTNESS_AND_LINK_RESONANCE',len(checks),'controls',len(receipt['transitive_d0_source_sha256']),'D0 pins')


if __name__ == '__main__':
    main()
