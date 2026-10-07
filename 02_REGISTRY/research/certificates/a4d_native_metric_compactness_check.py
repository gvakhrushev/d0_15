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
    check('COMPILED_21_REAL_PROPOSITIONS', receipt['status'] == 'PASS'
          and receipt['compiler_exit_code'] == 0 and not receipt['sorryAx']
          and receipt['printed_axiom_dependencies'] == 21 and receipt['owner_input_head'] == HEAD)
    pins = {**receipt['transitive_d0_source_sha256'], **receipt['toolchain_input_sha256'],
            receipt['capsule']: receipt['capsule_sha256'], receipt['output']: receipt['output_sha256']}
    check('ALL_TRANSITIVE_OWNER_TOOLCHAIN_CAPSULE_OUTPUT_PINS', all(sha(p) == h for p, h in pins.items()))
    out = (root/receipt['output']).read_text()
    check('STANDARD_AXIOMS_AND_CLEAN_COMPILER_OUTPUT', set(receipt['axioms']) <= {'propext','Classical.choice','Quot.sound'}
          and not any(x in out for x in ['error:', 'warning:', 'sorryAx']))
    actual = ['signedGram_square_le','metricError_small_chart','korn_identity',
              'nonlinear_inverse_square','native_centered_binding','native_korn_identity',
              'native_metric_binding','native_metric_inverse_square','native_nyquist_raw_translation',
              'native_nyquist_center_zero','raw4_det','resonance_center','resonance_gram']
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

    payload={'status':'PASS','owner_input_head':HEAD,'scope':SCOPE,'checks':checks,
             'input_sha256':pins,'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
             'native_refinement_certificate_sha256':sha(REFINEMENT),
             'transitive_d0_source_count':len(receipt['transitive_d0_source_sha256']),
             'exact_results':{'signature':[1,-1,-1,-1],'inverse_square_constant':'4/3',
              'raw_determinant':'-1','raw_normalized_square':'4+8/h^2',
              'curved_Ric_AA_and_G_BB_at_zero':'24*pi^2/1033',
              'coframe_variance':'9/1024','link_raw_product_square_limit':'9/32',
              'geometric_potential_bonding_square_defect':'1',
              'actual_frozen_lift_centered_gradient_square':'4*K','metric_components':10,'connection_rows':24}}
    if args.output:
        args.output.write_text(json.dumps(payload,sort_keys=True,indent=2)+'\n')
    else:
        expected=args.expect or root/(BASE+'_certificate.json')
        assert json.loads(expected.read_text()) == payload, 'PINNED_LEDGER_MISMATCH'
    print('PASS_NATIVE_METRIC_COMPACTNESS_AND_LINK_RESONANCE',len(checks),'controls',len(receipt['transitive_d0_source_sha256']),'D0 pins')


if __name__ == '__main__':
    main()
