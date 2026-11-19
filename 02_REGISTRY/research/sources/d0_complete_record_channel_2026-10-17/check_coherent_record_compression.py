#!/usr/bin/env python3
"""Bounded exact controls for complete-record coherent compression/source.

No old run(), Choi construction, spectral/rank census, or history enumeration.
The eight L4 momenta retain all16 CAR coordinates and reference128 in the
analytic consumer. The two-dimensional Gram/source controls below are
algebraic fixtures; their two operator combinations are not asserted to be
the entire native channel. Positivity of the full2048 support, the n>=22
statement, and fixed-positive-time C1 convergence are proved in the owner.
"""

from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
PRIOR = ('02_REGISTRY/research/sources/'
         'd0_complete_record_channel_2026-10-17/check_flat_relaxation.py')
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    PRIOR: '0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
}


def _definitions(repo):
    tree = ast.parse((repo / PRIOR).read_text())
    names = {'_creators', '_native_rows'}
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name in names]
    if len(nodes) != 2 or {node.name for node in nodes} != names:
        raise ArithmeticError('coherent_compression:definition_nodes')
    scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), PRIOR, 'exec'), scope)
    return scope['_creators'], scope['_native_rows']


def _sylvester(R, Y):
    """Exact row-major solve R X+X R=Y; no diagonalization is used."""
    n = R.rows
    coefficient = s.kronecker_product(R, s.eye(n)) + s.kronecker_product(s.eye(n), R.T)
    solution = coefficient.inv()*s.Matrix(list(Y))
    return s.Matrix(n, n, list(solution))


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('coherent_compression:' + name)
        checks.append(name)

    def zero(value):
        return s.simplify(s.expand(value)) == 0

    def eq(actual, expected, name):
        difference = actual-expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(zero(entry) for entry in entries), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    creators, native_rows = _definitions(repo)
    C, order = creators(repo)
    I, O = s.eye(16), s.zeros(16)
    require(order == (0, 2, 3, 1), 'literal_ACDB_full16_order')
    require(all(C[r]*C[t].H+C[t].H*C[r] == (I if r == t else O)
                and C[r]*C[t]+C[t]*C[r] == O
                for r in range(4) for t in range(4)),
            'all16_literal_CAR_no_grade_cut')
    xi = [item for r in range(4) for item in (C[r]+C[r].H, s.I*(C[r]-C[r].H))]
    eta = [xi[2*r+1] for r in range(4)]
    require(all(x.H == x and x*x == I for x in xi),
            'eight_actual_Hermitian_Majoranas')

    # Period1: theta=2*pi*h. Here h=1/4 gives theta=pi/2 exactly;
    # the anticommutator divisor is 2*nu*sin(theta)/h, not 2*nu*sin(h)/h.
    nu, b, h, theta = s.Rational(3, 5), s.Rational(4, 5), s.Rational(1, 4), s.pi/2
    eq(theta, 2*s.pi*h, 'period1_L4_theta_equals_two_pi_h')
    eq(nu**2+b**2, 1, 'strict_rational_Julia_margin')
    require(0 < nu < 1 and 0 < b < 1 and s.sin(theta) != 0,
            'nonzero_phase_and_positive_Julia_parameters')
    lam = 2*nu**2/h**2
    shell = [(role, sign) for role in range(4) for sign in (1, -1)]
    Ds = [nu/h*((sign*s.I-1)*C[role]+(-sign*s.I-1)*C[role].H)
          for role, sign in shell]
    require(all(all(zero(entry) for entry in list(D.H-D)+list(D*D-lam*I)) for D in Ds),
            'all8_axis_blocks_D_square_lambda_all16')
    divisor = 2*nu*s.sin(theta)/h
    require(all(all(zero(entry) for entry in
                    (D*eta[r]+eta[r]*D)/divisor-(sign*I if r == role else O))
                for D, (role, sign) in zip(Ds, shell) for r in range(4)),
            'actual_full16_anticommutators_give_four_central_Kr')

    # The central coordinate matrices are only8x8. Their full carrier lifts
    # are K tensor I16, as already checked in every block above.
    K = [s.diag(*(sign if role == r else 0 for role, sign in shell)) for r in range(4)]
    P = [(K[role]**2+sign*K[role])/2 for role, sign in shell]
    require(all(P[i][j, j] == (1 if i == j else 0)
                for i in range(8) for j in range(8)),
            'eight_central_momentum_projectors_are_the_named_shell_blocks')
    eq(sum(P, s.zeros(8)), s.eye(8), 'eight_projectors_resolve_full128_identity')
    require(all(P[i]*P[j] == (P[i] if i == j else s.zeros(8))
                for i in range(8) for j in range(8)),
            'eight_central_projectors_pairwise_orthogonal')

    # Actual Walsh inversion recovers the unshifted words from native rows.
    # Their jumps contain D and xi D. This is an operator-identity check, not
    # a numerical span/rank measurement or a change of recorded outcomes.
    rows, _, _ = native_rows(C, nu, b, (s.I, 1, 1, 1))
    D = Ds[0]
    jumps = {(label, coefficient): N.H*D for label, coefficient, N in rows}

    def word_jump(word_index, coefficient):
        return sum(((-1)**bin(label & word_index).count('1')*jumps[(label, coefficient)]
                    for label in range(32)), O.copy())

    jleft, jright = word_jump(4, 1), word_jump(6, 1)
    eq(-(jleft+jright)/(1+b), D, 'actual_Walsh_jump_span_contains_D')
    require(all(all(zero(entry) for entry in word_jump(8*r+4, 0)+nu*C[r].H*D)
                and all(zero(entry) for entry in word_jump(8*r+6, 0)+nu*C[r]*D)
                for r in range(4)),
            'actual_unshifted_words_give_all_eight_Majorana_times_D')
    eq(D*D/lam, I, 'identity_from_two_jump_words_no_adjoint_needed')
    require(all(all(zero(entry) for entry in (x*D)*D/lam-x) for x in xi),
            'Majoranas_from_two_jump_words_no_adjoint_needed')
    # Analytic counting: xi uses2 jump letters; K uses at most D*xi (3);
    # P uses at most K^2 (6). An eight-generator Clifford monomial uses at
    # most16 jump letters. Multiplying a central P yields at most22.
    word_bounds = {'D': 1, 'xi': 2, 'Kr': 3, 'P_plus_minus': 6,
                   'Clifford_monomial': 16, 'central_times_Clifford': 22}
    require(word_bounds['xi'] == 1+1
            and word_bounds['Kr'] == word_bounds['D']+word_bounds['xi']
            and word_bounds['P_plus_minus'] == 2*word_bounds['Kr']
            and word_bounds['Clifford_monomial'] == 8*word_bounds['xi']
            and word_bounds['central_times_Clifford']
                == word_bounds['P_plus_minus']+word_bounds['Clifford_monomial'],
            'analytic22_word_upper_bound_not_a_rank_census')

    # Full16 faithful complex preparation, with a moving normalizer.
    e01, P0 = O.copy(), O.copy()
    e01[0, 1], P0[0, 0] = 1, 1
    L = I+(1+s.I)*e01/3
    dL = P0
    normalizer = s.simplify(s.trace(L.H*L))
    dnormalizer = s.simplify(s.trace(dL.H*L+L.H*dL))
    rho = (L*L.H/normalizer).applyfunc(s.simplify)
    drho = ((dL*L.H+L*dL.H)/normalizer-rho*dnormalizer/normalizer).applyfunc(s.simplify)
    eq(s.trace(rho), 1, 'actual_complex_full16_preparation_normalized')
    eq(rho.H, rho, 'actual_complex_preparation_Hermitian')
    require(s.det(L) == 1 and normalizer > 0 and dnormalizer == 2,
            'faithful_preparation_invertible_and_normalizer_really_moves')
    eq(s.trace(drho), 0, 'normalized_preparation_source_trace_zero')
    require(s.im(rho[0, 1]) != 0, 'preparation_has_nonzero_complex_coherence')
    A = [I/4, xi[0]/4]
    eq(s.Matrix(2, 2, lambda i, j: s.trace(A[i].H*A[j])), s.eye(2),
       'two_actual_full16_form_operators_HS_orthonormal')
    Gactual = s.Matrix(2, 2, lambda i, j: s.trace(A[i].H*A[j]*rho))
    dGactual = s.Matrix(2, 2, lambda i, j: s.trace(A[i].H*A[j]*drho))
    eq(Gactual, s.Matrix([[1, s.Rational(3, 73)], [s.Rational(3, 73), 1]])/16,
       'exact_actual_complex_preparation_Gram')
    require(Gactual[0, 0] > 0 and s.det(Gactual) > 0,
            'two_operator_Gram_strict_positive_no_tomography')
    eq(dGactual[0, 0], 0, 'Gram_source_retains_preparation_normalizer')
    frozen_drho = (dL*L.H+L*dL.H)/normalizer
    require(s.trace(A[0].H*A[0]*frozen_drho) != dGactual[0, 0],
            'hostile_frozen_preparation_normalizer_source_rejected')

    # With complex Kraus coefficients, the physical record density is the
    # TRANSPOSE of the vector Gram (not the same matrix). These are only
    # two arbitrary combinations, not a complete native-channel fixture.
    coefficients = s.Matrix([[1, s.I/3], [(1+s.I)/2, s.Rational(2, 3)]])
    Kraus = [sum((A[i]*coefficients[i, j] for i in range(2)), O.copy()) for j in range(2)]
    vector_gram = s.Matrix(2, 2, lambda i, j: s.trace(Kraus[i].H*Kraus[j]*rho))
    record = s.Matrix(2, 2, lambda i, j: s.trace(Kraus[i]*rho*Kraus[j].H))
    eq(vector_gram, coefficients.H*Gactual*coefficients,
       'complex_Kraus_vector_Gram_coefficient_identity')
    eq(record, vector_gram.T, 'physical_record_density_is_complex_Gram_transpose')
    eq(record.H, record, 'record_Gram_transpose_is_Hermitian')
    require(any(not zero(entry) for entry in record-vector_gram),
            'hostile_omitted_Gram_transpose_rejected')

    # Generic Hermitian jets in a small strictly positive square-root
    # chart. This verifies the source identity without matrix logarithms.
    R = s.Matrix([[2, s.Rational(1, 3)], [s.Rational(1, 3), 1]])
    G = s.Matrix([[s.Rational(3, 2), s.Rational(1, 4)+s.I/3],
                  [s.Rational(1, 4)-s.I/3, 1]])
    H = s.Matrix([[2, s.I/5], [-s.I/5, 3]])
    require(R.H == R and R[0, 0] > 0 and R.det() > 0,
            'rational_square_root_fixture_strict_positive')
    require(G.H == G and H.H == H and H[0, 0] > 0 and H.det() > 0
            and any(not zero(entry) for entry in G*H-H*G)
            and any(not zero(entry) for entry in R*H-H*R),
            'source_covectors_Hermitian_and_noncommuting')
    ds0, ds1, ds2, ds3, dg0, dg1, dg2, dg3 = s.symbols('ds0 ds1 ds2 ds3 dg0 dg1 dg2 dg3', real=True)
    dS = s.Matrix([[ds0, ds2+s.I*ds3], [ds2-s.I*ds3, ds1]])
    dG = s.Matrix([[dg0, dg2+s.I*dg3], [dg2-s.I*dg3, dg1]])
    dR = _sylvester(R, dS)
    T = _sylvester(R, G*R*H+H*R*G)
    eq(R*dR+dR*R, dS, 'generic_square_root_derivative_Sylvester_equation')
    eq(R*T+T*R, G*R*H+H*R*G, 'generic_square_root_source_adjoint_Sylvester_equation')
    eq(dR.H, dR, 'generic_Hermitian_square_root_jet')
    dK = dR*G*R+R*dG*R+R*G*dR
    eq(s.trace(H*dK), s.trace(T*dS)+s.trace(R*H*R*dG),
       'complete_noncommuting_compressed_source_identity')
    forcing = 2*R*R
    source_from_root = s.simplify(s.trace(T*forcing))
    eq(source_from_root, 2*s.trace(H*R*G*R),
       'nonzero_square_root_source_has_exact_positive_control')
    require(source_from_root > 0,
            'hostile_frozen_square_root_loses_nonzero_source')

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks,
        'source_pins': PINS,
        'carrier': {'momenta': 8, 'forms': 16, 'system': 128, 'reference': 128},
        'phase_convention': 'period1, theta=2*pi*h; L4 theta=pi/2',
        'word_bounds': word_bounds,
        'analytic_consumer': {
            'jump_algebra': 'direct_sum_8 M16, dimension2048; proved structurally in owner',
            'finite_time': 'positive beta; finite n>=22 on isotropic positive first shell',
            'Gram': 'G_ij(rho)=Tr(A_i^* A_j rho)',
            'compressed': 'K=R G R, R=S^(1/2)',
            'source': 'Tr H dK=Tr T dS+Tr(R H R)dG; R T+T R=G R H+H R G',
            'support': 'vec(A C) for invertible purification C; equals vec(A) only if A C=A',
        },
        'scope': (
            'Bounded identities support the structural full2048 faithfulness and C1 proof; '
            'they do not infer it from a matrix rank fixture. No full Choi/history matrix, '
            'old run, spectrum census, changed record basis/price, physical preparation '
            'admission, pointer entropy convergence, arbitrary spatial-field source limit, '
            'or GR closure is supplied. Two Kraus combinations are an algebraic transpose '
            'control, not the full native channel.'
        ),
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
