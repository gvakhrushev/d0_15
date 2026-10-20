#!/usr/bin/env python3
"""Exact cyclic-history preparation; no physical heat/metric admission claim.

Analytic all-size proofs are in the companion memo. This replay checks actual
ordered scene words and full finite operators, not only supplied eigenvalues.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

import sympy as s

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_cyclic_history_price'
PROOF = '02_REGISTRY/research/A4D_NATIVE_CYCLIC_HISTORY_PRICE_PREPARATION.md'
HEAD = '5a4c5eacec603d04b2b5e6e73ce9ba2aab8d119d'
INPUTS = [
    '03_FORMALIZATION/D0/Claims/Signature31Split.lean',
    '03_FORMALIZATION/D0/VNext2/ScenePathHistoryCanonicity.lean',
    '03_FORMALIZATION/D0/VNext2/SceneEndpointReynoldsExpectation.lean',
    '03_FORMALIZATION/D0/Geometry/ArchivePhaseShift.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveRefinementTower.lean',
    '03_FORMALIZATION/D0/Geometry/ArchivePhaseDistance.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveWeightedGraph.lean',
    '03_FORMALIZATION/D0/Geometry/ArchiveCanonicalLaplacian.lean',
    '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
    '02_REGISTRY/research/A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md',
    '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md',
    '02_REGISTRY/research/A4D_NATIVE_HISTORY_ACTION_BOUNDARY.md',
]
SCOPE = {
    'history_admission': 'LITERAL_COMPOSITION_COMPLETE_ALL_WALKS_INTERFACE',
    'record_retained': 'WHOLE_ORDERED_CLOSED_SCENE_WORD',
    'common_heat_binding': 'DECLARED_OWNED_UNSCALED_CYCLE_LAPLACIAN',
    'projection': 'CONDITIONAL_AVERAGE_ON_VISIT_FIBERS',
    'all_positive_integer_reversible_frequencies': 'ANALYTIC_EULER_TRAIL_CONSTRUCTION',
    'paired_price_error': '33*z/((1-z)*m)_TO_WEIGHTED_RETURN_OBSERVABLE',
    'repetition': 'ACTUAL_WORD_REPETITION_AND_EXPLICIT_CYCLIC_COVERING',
    'one_step_frequency_readout_suffices_for_two_step_price': False,
    'memory_fiber': 'ACTUAL_PATH_CONCATENATIONS_WITH_FIXED_WHOLE_ONE_STEP_COUNTS',
    'memory_fiber_full_price': 'STRICT_DECREASE_ON_COMPLETE_THETA_INTERVAL_AT_z_HALF',
    'memory_fiber_secant_error': '(1/120)*n^(-2/3)_FOR_epsilon=n^(-1/3)',
    'additive_edge_action_detects_this_memory_fiber': False,
    'all_D0_action_stack_terms_evaluated': False,
    'finite_words_are_a_smooth_variation_space': False,
    'cycle_binding_is_forced_physical_heat': False,
    'all_M1_catalogues_or_core_preparations_classified': False,
    'physical_q_D_b_m_readout_constructed': False,
    'golden_or_physical_mesh_refinement_identified': False,
    'full_matter_source_Ward_or_native_stationarity': False,
    'Einstein_contrast_or_curved_joint_roots': False,
    'soundness_recovery_T0_T3_or_parent_terminals_closed': False,
    'new_supported_Lean_theorem': False,
    'new_action_or_physical_selection_postulate': False,
}


def sha(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()


def zone(i):
    return 0 if i < 9 else 1 if i < 20 else 2


def euler_word(m, r=0):
    """All directed native edges, integer multiplicity m plus r at two edges."""
    adj = [[] for _ in range(33)]
    for i in range(33):
        for j in range(33):
            if zone(i) == zone(j):
                continue
            edge = {i, j}
            n = m + (r if edge == {0, 9} else -r if edge == {0, 20} else 0)
            assert n > 0
            adj[i].extend([j]*n)
    stack, reverse = [0], []
    while stack:
        v = stack[-1]
        if adj[v]:
            stack.append(adj[v].pop())
        else:
            reverse.append(stack.pop())
    assert not any(adj)
    return reverse[::-1]


def valid_word(word):
    return (len(word) >= 4 and word[0] == word[-1]
            and all(0 <= x < 33 for x in word)
            and all(zone(i) != zone(j) for i, j in zip(word, word[1:])))


def counts(word, k, labels=None):
    body = word[:-1]
    labels = sorted(set(body)) if labels is None else list(labels)
    index = {v:i for i, v in enumerate(labels)}
    masses = Counter(body)
    D = s.diag(*[masses[v] for v in labels])
    N = s.zeros(len(labels))
    for t, v in enumerate(body):
        N[index[v], index[body[(t+k) % len(body)]]] += 1
    assert all(D[i, i] > 0 for i in range(len(labels)))
    one = s.ones(len(labels), 1)
    assert N*one == D*one and N.T*one == D*one
    return D, N


def pencil_det(D, N, z=s.Rational(1, 2)):
    return s.cancel(((1-z)*D+z*N.T*D.inv()*N).det(method='domain-ge')/D.det())


def full_operators(word, k):
    body = word[:-1]
    labels = sorted(set(body))
    L = len(body)
    J = s.Matrix(L, len(labels), lambda t, i: int(body[t] == labels[i]))
    D, N = counts(word, k, labels)
    C = D.inv()*J.T
    P = J*C
    U = s.Matrix(L, L, lambda i, j: int(j == (i+1) % L))
    Delta = 2*s.eye(L)-U-U.T
    UK = U**k
    F = P*UK.T*(s.eye(L)-P)*UK*P
    return D, N, J, C, P, U, Delta, F


def controls():
    checks, mutants = [], []

    def check(name, condition):
        assert bool(condition), name
        checks.append(name)

    def reject(name, actual, altered):
        check('REJECT_'+name, actual != altered)
        mutants.append(name)

    A = s.Matrix(33, 33, lambda i, j: int(zone(i) != zone(j)))
    E = s.zeros(33)
    E[0,9] = E[9,0] = 1
    E[0,20] = E[20,0] = -1
    D0 = s.diag(*list(A*s.ones(33,1)))
    check('LITERAL_SCENE_718_DIRECTED_EDGES', sum(A) == 718)
    for m, r in [(2,0), (4,-1), (4,1), (8,-3), (8,3)]:
        word = euler_word(m,r)
        DD, NN = counts(word,1,range(33))
        check('ACTUAL_CLOSED_WORD_%s_%s' % (m,r), valid_word(word)
              and len(word)-1 == 718*m and (len(word)-1)%4 == 0)
        check('REALIZED_ALL_718_COUNTS_%s_%s' % (m,r), NN == m*A+r*E
              and DD == s.diag(*list((m*A+r*E)*s.ones(33,1))))

    # Unequal visit masses are necessary to test the weighted adjoint.
    small = [0,9,0,20,9,20,0,9,0]
    for k in [1,2,3]:
        D,N,J,C,P,U,Delta,F = full_operators(small,k)
        L, n = J.shape
        T = D.inv()*N
        FT = s.eye(n)-D.inv()*T.T*D*T
        check('WHOLE_MATRIX_PROJECTION_%s' % k, J.T*J == D and C*J == s.eye(n)
              and P.T == P and P*P == P)
        check('WHOLE_SHIFT_AND_COMPRESSION_%s' % k, U.T*U == s.eye(L)
              and C*(U**k)*J == T)
        check('WHOLE_FEEDBACK_%s' % k, F == J*FT*C)
        check('FULL_DETERMINANT_%s' % k,
              (s.eye(L)-F/2).det() == pencil_det(D,N))
        check('FULL_CYCLE_HEAT_%s' % k, Delta == (U-s.eye(L)).T*(U-s.eye(L))
              and Delta*s.ones(L,1) == s.zeros(L,1)
              and Delta.trace() == 2*L and (Delta**2).trace() == 6*L)
    D,N,J,C,P,U,Delta,F = full_operators(small,2)
    T = D.inv()*N
    reject('FREEZE_PAIRING', J*(s.eye(D.rows)-T.T*T)*C, F)
    reject('REPLACE_RETAINED_SHIFT_SQUARED_BY_IDENTITY', F, s.zeros(F.rows))
    reject('DELETE_FULL_HEAT_MODES', Delta.trace(), (s.eye(D.rows)-T).trace())

    repeated = small[:-1]*2+[small[0]]
    d,n,j,c,p,u,delta,f = full_operators(repeated,2)
    L = len(small)-1
    B = s.Matrix(2*L,L,lambda i,j: int(i%L == j))/s.sqrt(2)
    check('REPETITION_COMPLETE_MAPS', B.T*B == s.eye(L) and u*B == B*U
          and delta*B == B*Delta and p == B*P*B.T and f == B*F*B.T)
    check('REPETITION_DETERMINANT_WITH_FULL_COMPLEMENT',
          (s.eye(2*L)-f/2).det() == (s.eye(L)-F/2).det())
    reject('REPLICATE_ACTIVE_PROJECTION_INSTEAD_OF_READOUT',
           (s.eye(2*L)-f/2).det(), (s.eye(L)-F/2).det()**2)
    check('RETAIN_EXTRA_HEAT_MODES', delta.rows == 2*Delta.rows
          and delta.trace() == 2*Delta.trace())

    # This is the literal shared-scene first jet, with changing degrees retained.
    DI = D0.inv()
    T0 = DI*A
    dD = s.diag(*list(E*s.ones(33,1)))
    V = DI*(E-dD*T0)
    kappa = 1-s.trace(T0*T0)/2
    dkappa = -s.trace(T0*V)
    FF = s.eye(33)-T0*T0
    dF = -(T0*V+V*T0)
    z = s.Rational(1,2)
    derivative = s.trace(z*(s.eye(33)-z*FF).inv()*dF)
    check('ACTUAL_ALL_COMPONENT_FIRST_JET', kappa == s.Rational(39,160)
          and dkappa == s.Rational(359,1161600)
          and derivative == s.Rational(359,1207230))
    reject('FREEZE_DEGREE_DERIVATIVE', V*s.ones(33,1), DI*E*s.ones(33,1))
    zz = s.symbols('z')
    q = 1-zz-2*zz*(1-zz)*kappa+zz**2*kappa**2
    coefficient = 2*zz*(1-zz*(1+kappa))/q
    check('PROTECTED_FUGACITY_EXCEPTION', coefficient.subs(zz,s.Rational(160,199)) == 0
          and coefficient.subs(zz,z)*dkappa == derivative)
    check('UNIFORM_OPERATOR_LIPSCHITZ_ARITHMETIC', s.Rational(2,19)+s.Rational(25,361)<1)
    for t,m in [(s.Rational(1,3),4), (s.Rational(-1,7),8), (s.Rational(1,2),4)]:
        r = int(s.floor(m*t+s.Rational(1,2)))
        check('EXACT_ROUNDING_%s_%s' % (str(t),m), abs(s.Rational(r,m)-t)<=s.Rational(1,2*m)
              and abs(r)<m and valid_word(euler_word(m,r)))

    base = euler_word(2)
    wa = base+[9,0,10,0,20,0,21,0]
    wb = base+[9,0,20,0,10,0,21,0]
    check('FULL_ORDERED_HOSTILE_WORDS_ADMITTED', valid_word(wa) and valid_word(wb)
          and len(wa)==len(wb)==1445 and len(set(wa))==len(set(wb))==33)
    da,n1a=counts(wa,1,range(33))
    db,n1b=counts(wb,1,range(33))
    da2,n2a=counts(wa,2,range(33))
    db2,n2b=counts(wb,2,range(33))
    qa,qb=pencil_det(da2,n2a),pencil_det(db2,n2b)
    ratio=s.cancel(qb/qa)
    check('EXACT_ONE_STEP_FIBER', da==db==da2==db2 and n1a==n1b)
    check('EXACT_TWO_STEP_PRICE_GAP', n2a!=n2b and qa>0 and qb>qa)
    reject('MARKOVIZE_THE_RETAINED_TWO_STEP_HISTORY', n2a, n1a*da.inv()*n1a)
    reject('DESCEND_COMPOSED_PRICE_THROUGH_ONE_STEP_FIBER', ratio, s.Integer(1))

    # Composition uses the literal shared endpoint once. Common incoming and
    # outgoing boundary labels make the lag-two counts additive as well.
    check('COMMON_TWO_STEP_BLOCK_JUNCTION', wa[:2]==wb[:2]==[0,32]
          and wa[-2:]==wb[-2:]==[21,0])
    for pattern in [(0,1),(1,0),(0,0,1),(1,0,1)]:
        word=[0]
        for bit in pattern:
            word += (wb if bit else wa)[1:]
        dm,nm=counts(word,2,range(33))
        _,nm1=counts(word,1,range(33))
        n=len(pattern); a=sum(pattern)
        check('ACTUAL_FIXED_ONE_STEP_MEMORY_FIBER_'+str(pattern), valid_word(word)
              and len(word)-1==1444*n and dm==n*da and nm1==n*n1a
              and nm==(n-a)*n2a+a*n2b)
    X=s.zeros(33,2); Y=s.zeros(2,33)
    X[20,0]=1; X[9,0]=-1; X[9,1]=1; X[10,1]=-1
    Y[0,10]=1; Y[0,21]=-1; Y[1,20]=1; Y[1,21]=-1
    check('LITERAL_ORDER_MEMORY_RANK_TWO', X*Y==n2b-n2a and X.rank()==Y.rank()==2)
    theta=s.symbols('theta')
    M0=(da+n2a.T*da.inv()*n2a)/2
    VV=(n2a.T*da.inv()*X).row_join(Y.T)
    KK=s.zeros(2).row_join(theta*s.eye(2)).col_join(
        (theta*s.eye(2)).row_join(theta**2*X.T*da.inv()*X))
    NN=n2a+theta*X*Y
    check('WHOLE_MATRIX_DETERMINANT_LEMMA_INPUT',
          s.simplify((da+NN.T*da.inv()*NN)/2-M0-VV*KK*VV.T/2)==s.zeros(33))
    poly=s.Poly(s.cancel((s.eye(4)+KK*VV.T*M0.inv()*VV/2).det()),theta)
    coefficients=list(reversed(poly.all_coeffs()))
    check('ALL_THETA_POSITIVE_QUARTIC_COEFFICIENTS', poly.degree()==4
          and coefficients[0]==1 and all(c>0 for c in coefficients[1:]))
    for t in [s.Integer(0),s.Rational(1,3),s.Rational(1,2),s.Integer(1)]:
        check('FULL_33_VERSUS_REDUCED_PENCIL_'+str(t),
              poly.eval(t)==pencil_det(da,n2a+t*(n2b-n2a))/qa)
    check('UNIFORM_MEMORY_PRICE_DESCENT', coefficients[1]/poly.eval(1)>s.Rational(1,1000)
          and all(poly.diff((theta,k)).eval(1)<s.Rational(1,100) for k in [1,2,3]))
    check('THIRD_DERIVATIVE_AND_SECANT_BOUND',
          s.Rational(1,100)+s.Rational(3,10000)+s.Rational(2,1000000)<s.Rational(1,50)
          and s.Rational(1,300)+s.Rational(1,200)==s.Rational(1,120))
    mid=s.Rational(1,2)
    gm=-poly.diff().eval(mid)/poly.eval(mid)
    nmid=n2a+mid*(n2b-n2a)
    mmid=(da+nmid.T*da.inv()*nmid)/2
    gm_full=-s.trace(mmid.inv()*((n2b-n2a).T*da.inv()*nmid
                    +nmid.T*da.inv()*(n2b-n2a))/2)
    check('FULL_MEMORY_FIBER_FIRST_VARIATION', gm==gm_full
          and -s.Rational(3,1000)<gm<-s.Rational(2,1000))
    reject('ADDITIVE_EDGE_ACTION_OR_ONE_STEP_QUOTIENT_RESPONSE',gm,s.Integer(0))
    for r in [2,3]:
        dra,nra=counts(wa[:-1]*r+[wa[0]],2,range(33))
        drb,nrb=counts(wb[:-1]*r+[wb[0]],2,range(33))
        check('PERSISTENT_FULL_ORDERED_COUNTS_%s'%r,
              dra==r*da and drb==r*db and nra==r*n2a and nrb==r*n2b)
    body=wa[:-1]
    shifted=body[17:]+body[:17]
    check('INTERNAL_ORIGIN_CHANGE', counts(shifted+[shifted[0]],2,range(33))==(da,n2a))
    sigma=list(range(33)); sigma[0],sigma[1]=1,0
    relabeled=[sigma[v] for v in small]
    check('CATALOGUE_RELABELING_PRESERVES_FULL_PROJECTION',
          valid_word(relabeled) and full_operators(relabeled,2)[4]==P)
    reverse_bad=wa.copy(); reverse_bad[2]=reverse_bad[1]
    reject('INVALID_NATIVE_STEP', valid_word(wa), valid_word(reverse_bad))
    return {
        'checks':checks, 'executed_mutants_rejected':mutants,
        'symbolic_frequency_jet':str(derivative),
        'memory_fiber':{
            'det_ratio_polynomial_constant_first':[str(c) for c in coefficients],
            'midpoint_first_variation':str(gm),
            'uniform_first_variation_bounds':['-1/100','-1/1000'],
            'uniform_third_derivative_bound':'1/50',
            'secant_error_at_epsilon_n_minus_third':'(1/120)*n^(-2/3)',
            'actual_finite_block_change_price_drop_lower_bound':'1/(1000*n)',
        },
        'ordered_counterexample':{
            'length':1444, 'word_a':wa, 'word_b':wb,
            'det_a':str(qa), 'det_b':str(qb), 'det_b_over_a':str(ratio),
            'price_a_minus_b':'log(det_b_over_a)',
        },
    }


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path)
    parser.add_argument('--expect',type=Path)
    args=parser.parse_args()
    header={'schema':'d0-cyclic-history-price/1','input_head':HEAD,'scope':SCOPE,
            'proof_sha256':sha(PROOF),'checker_sha256':sha(BASE+'_check.py'),
            'inputs_sha256':{p:sha(p) for p in INPUTS}}
    expected=None
    if not args.output:
        expected=json.loads((args.expect or ROOT/(BASE+'_certificate.json')).read_text())
        assert all(expected.get(k)==v for k,v in header.items()), 'SOURCE_SCOPE_OR_INPUT_MISMATCH'
    result={**header,**controls()}
    if args.output:
        args.output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    else:
        assert result==expected,'EXACT_CERTIFICATE_MISMATCH'
    print('PASS_CYCLIC_HISTORY_PRICE_PREPARATION',len(result['checks']),'controls;',
          len(result['executed_mutants_rejected']),'executed mutants rejected')


if __name__=='__main__':
    main()
