#!/usr/bin/env python3
"""Bounded exact first-source inputs for the full native record instrument.

Only the pinned creator and native-row definitions execute.  The fixture
keeps all16 forms, all64 Julia rows and both golden ports (128 outcomes).
It verifies the tangent isometry, its orthogonal innovation decomposition,
and the derivative of the SAME finite native channel.  It is not a proof
of whole-grid moment estimates, C1 process convergence, entropy/source
convergence, physical Info selection, or an Einstein field equation.
"""

from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CURVED = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PRIOR = ('02_REGISTRY/research/sources/'
         'd0_complete_record_channel_2026-10-17/check_flat_relaxation.py')
PINS = {
    CURVED: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    PRIOR: '0dcb79f0959ecd4f4484a500ef1c0e53e47d95b4a95feb874d16840f56cc9ec9',
}


def _definitions(repo):
    tree = ast.parse((repo / PRIOR).read_text())
    names = {'_creators', '_native_rows'}
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name in names]
    if len(nodes) != 2 or {node.name for node in nodes} != names:
        raise ArithmeticError('first_source_inputs:definition_nodes')
    scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), PRIOR, 'exec'), scope)
    return scope['_creators'], scope['_native_rows']


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('first_source_inputs:' + name)
        checks.append(name)

    # p is the positive golden root, a=sqrt(p).  Polynomial reduction
    # retains exact signs/adjoints without nested radical expressions.
    p, a = s.symbols('p a', positive=True)

    def reduce(value):
        expanded = s.expand(value)
        if expanded == 0:
            return s.S.Zero
        return s.expand(s.rem(s.rem(expanded, a*a-p, a), p*p+p-1, p))

    def clean(matrix):
        return s.SparseMatrix(matrix).applyfunc(reduce)

    def eq(actual, expected, name):
        difference = actual-expected
        if isinstance(difference, s.MatrixBase):
            entries = s.SparseMatrix(difference).todok().values()
        else:
            entries = [difference]
        require(all(reduce(entry) == 0 for entry in entries), name)

    def nonzero(matrix):
        return any(reduce(entry) != 0
                   for entry in s.SparseMatrix(matrix).todok().values())

    def witness(matrix):
        return next(({'row': row, 'column': column,
                      'value': str(reduce(value))}
                     for (row, column), value
                     in sorted(s.SparseMatrix(matrix).todok().items())
                     if reduce(value) != 0), None)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    creators, native_rows = _definitions(repo)
    C, order = creators(repo)
    C = [s.SparseMatrix(c) for c in C]
    I = s.SparseMatrix(s.eye(16))
    O = s.SparseMatrix(16, 16, {})
    require(order == (0, 2, 3, 1), 'literal_ACDB_full16_exterior_order')
    require(all(C[r]*C[j].H+C[j].H*C[r] == (I if r == j else O)
                and C[r]*C[j]+C[j]*C[r] == O
                for r in range(4) for j in range(4)),
            'all16_CAR_all_four_roles_no_grade_cut')
    nu, b, h = s.Rational(3, 5), s.Rational(4, 5), s.Rational(1, 4)
    eq(nu*nu+b*b, 1, 'strict_rational_345_Julia_margin')
    eq(p+p*p, 1, 'positive_golden_probability_quotient')
    eq(a*a, p, 'literal_second_port_amplitude_a_squared_equals_p')
    phases = (s.I, s.S.One, s.S.One, s.S.One)
    require(all(phase*s.conjugate(phase) == 1 for phase in phases),
            'actual_four_role_unit_Fourier_phases')

    # c0*cos(t)+c1*sin(t) is an exactly normalized creator.  Its first
    # jet c0+t*c1 gives the TRUE first jets of both positive Julia roots.
    # The linear expression is not asserted to be normalized at order2.
    t = s.Symbol('t', real=True)
    rotated = C[0]+t*C[1]
    eq((rotated*rotated.H+rotated.H*rotated).diff(t).subs(t, 0), O,
       'actual_normalized_rotating_creator_CAR_first_jet')
    Cjet = list(C)
    Cjet[0] = rotated
    rows, left, right = native_rows(Cjet, nu, b, phases)
    jets = [(label, coefficient, s.SparseMatrix(N.subs(t, 0)),
             s.SparseMatrix(N.diff(t).subs(t, 0)))
            for label, coefficient, N in rows]
    require(len(jets) == 64, 'all32_labels_times_two_coefficients_retained')
    njet = rotated*rotated.H
    for root_name, root, target in (
            ('left', left[0], s.eye(16)-nu*nu*njet),
            ('right', right[0], s.eye(16)-nu*nu*(s.eye(16)-njet))):
        eq((root*root).subs(t, 0), target.subs(t, 0),
           'actual_positive_' + root_name + '_Julia_root_square_base')
        eq((root*root).diff(t).subs(t, 0), target.diff(t).subs(t, 0),
           'actual_positive_' + root_name + '_Julia_root_square_first_jet')
    eq(sum((N*N.H for _, _, N, _ in jets), O.copy()), I,
       'full64_Julia_rows_base_isometry')
    eq(sum((dN*N.H+N*dN.H for _, _, N, dN in jets), O.copy()), O,
       'full64_Julia_rows_first_tangent_isometry')
    A, dA = jets[0][2], jets[0][3]
    eq(A.H, A, 'actual_blank_A_Hermitian')
    eq(dA.H, dA, 'actual_blank_first_jet_Hermitian')
    D, dD = 16*A/h, 16*dA/h
    Delta, dDelta = D*D, dD*D+D*dD
    eq(Delta, 2*nu*nu*I/(h*h),
       'actual_nonzero_Fourier_D_square_all16')
    eq(dDelta, O, 'normalized_row_rotation_Delta_first_jet_zero')
    require(nonzero(dD), 'actual_D_first_jet_nonzero')

    kraus = []
    for label, coefficient, N, dN in jets:
        for port in range(2):
            if label == coefficient == port == 0:
                K = I-2*p*p*A*A
                dK = -2*p*p*(dA*A+A*dA)
            else:
                weight = -2*p*p if port == 0 else -2*a*p
                K = weight*N.H*A
                dK = weight*(dN.H*A+N.H*dA)
            kraus.append((label, coefficient, port, clean(K), clean(dK)))
    require(len(kraus) == 128, 'all128_literal_outcomes_both_golden_ports')
    require(any(label == coefficient == 0 and port == 1 and nonzero(K)
                for label, coefficient, port, K, _ in kraus),
            'special_blank_label_port1_outcome_retained')
    eq(sum((K.H*K for _, _, _, K, _ in kraus), O.copy()), I,
       'full128_native_Stinespring_exact_isometry')
    eq(sum((dK.H*K+K.H*dK for _, _, _, K, dK in kraus), O.copy()), O,
       'full128_native_Stinespring_tangent_isometry')
    connection = clean(sum((K.H*dK for _, _, _, K, dK in kraus), O.copy()))
    eq(connection.H, -connection,
       'actual_Stinespring_connection_skew_Hermitian')
    require(nonzero(connection), 'actual_connection_not_zero_or_frozen')
    innovation = [(label, coefficient, port, K, dK,
                   clean(dK-K*connection))
                  for label, coefficient, port, K, dK in kraus]
    eq(sum((K.H*R for _, _, _, K, _, R in innovation), O.copy()), O,
       'exact_innovation_sum_Kadjoint_R_zero')
    jet_norm = clean(sum((dK.H*dK for _, _, _, _, dK in kraus), O.copy()))
    innovation_norm = clean(sum((R.H*R for _, _, _, _, _, R in innovation),
                               O.copy()))
    eq(innovation_norm, jet_norm-connection.H*connection,
       'exact_innovation_quadratic_variation_identity')
    require(nonzero(innovation_norm),
            'actual_orthogonal_innovation_is_nonzero')
    require(nonzero(connection.H*connection),
            'hostile_omitting_connection_fails_innovation_quadratic_identity')
    # Taking R=K' without subtracting KA would give sum K*R=A !=0.
    require(nonzero(sum((K.H*dK for _, _, _, K, dK in kraus), O.copy())),
            'hostile_raw_Kprime_is_not_orthogonal_innovation')

    # Fully generic Hermitian input on all16 forms.  This is one
    # universal matrix identity, not a basis/rank/spectrum enumeration.
    X = s.MutableSparseMatrix(16, 16, {})
    for row in range(16):
        X[row, row] = s.Symbol('x_' + str(row), real=True)
        for column in range(row+1, 16):
            real, imag = s.symbols('x_' + str(row) + '_' + str(column)
                                  + ' y_' + str(row) + '_' + str(column),
                                  real=True)
            X[row, column], X[column, row] = real+s.I*imag, real-s.I*imag
    eq(X.H, X, 'generic_full16_Hermitian_input')
    require(nonzero(D*X-X*D), 'generic_input_really_noncommutes_with_D')
    exact_base = sum((K*X*K.H for _, _, _, K, _ in kraus), O.copy())
    exact_first = sum((dK*X*K.H+K*X*dK.H
                       for _, _, _, K, dK in kraus), O.copy())
    epsilon = p*p*h*h/64
    DXD = D*X*D
    dDXD = dD*X*D+D*X*dD
    T_DXD = sum((N.H*DXD*N for _, _, N, _ in jets), O.copy())
    dT_DXD = sum((dN.H*DXD*N+N.H*dDXD*N+N.H*DXD*dN
                  for _, _, N, dN in jets), O.copy())
    expected_base = X+epsilon*(T_DXD-(Delta*X+X*Delta)/2)
    expected_first = epsilon*(dT_DXD-(dDelta*X+X*dDelta)/2)
    eq(exact_base, expected_base,
       'actual_full128_channel_equals_64_row_native_GKSL_formula')
    eq(exact_first, expected_first,
       'actual_full128_channel_first_jet_equals_64_row_GKSL_derivative')
    eq(s.trace(exact_first), 0, 'actual_channel_derivative_trace_zero')
    require(nonzero(expected_first), 'actual_channel_first_jet_nonzero')

    # Analytic rank-birth control only, not another native fixture.
    # The third zero entry records that support may change; the signed
    # pure lift (sqrt(1-t^2),t,0) is smooth across t=0.
    z = s.Symbol('z', positive=True)
    birth_entropy = -(1-z*z)*s.log(1-z*z)-z*z*s.log(z*z)
    birth_source = s.diff(birth_entropy, z)
    require(s.limit(birth_source, z, 0, dir='+') == 0,
            'rank_birth_entropy_first_source_continuous_zero')
    require(s.limit(s.diff(birth_source, z)+2*s.log(z*z),
                    z, 0, dir='+') == -4,
            'rank_birth_entropy_second_jet_has_positive_log_divergence')

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks,
        'source_pins': PINS,
        'fixture': {'forms': 16, 'roles': 4, 'Julia_rows': len(jets),
                    'golden_outcomes': len(kraus), 'nu': str(nu), 'b': str(b),
                    'h': str(h), 'phases': [str(x) for x in phases],
                    'rotation': 'c0*cos(t)+c1*sin(t), first jet c0+t*c1',
                    'golden_quotient': 'p>0, p^2+p=1, a>0, a^2=p'},
        'exact_formulae': {
            'connection': 'Aconn=sum K_alpha^* K_alpha_prime, Aconn^*=-Aconn',
            'innovation': 'R_alpha=K_alpha_prime-K_alpha Aconn; sum K_alpha^* R_alpha=0',
            'quadratic_variation': 'sum R_alpha^* R_alpha=sum K_alpha_prime^* K_alpha_prime-Aconn^* Aconn',
            'finite_channel': 'Phi(X)=X+epsilon*(sum_64 N^* D X D N-{D^2,X}/2)',
            'clock': 'epsilon=p^2*h^2/64 fixed in this fixture',
            'rank_birth': 'S_prime(t)->0; S_second(t)=-2log(t^2)-4+o(1)'},
        'nonzero_connection_entry': witness(connection),
        'nonzero_innovation_norm_entry': witness(innovation_norm),
        'scope': (
            'Exact full16 finite native instrument first-jet inputs at one '
            'Fourier phase. All64 Julia rows, all128 literal outcomes and '
            'the special blank-label/port1 outcome are kept. The GKSL '
            'comparison uses the64 N rows, not an uncorrected127-jump sum. '
            'Orthogonality of insertions at different record times and '
            'uniform whole-grid energy/source bounds are analytic consumers, '
            'not proved by this one-step matrix fixture. No old entrypoint, '
            'lattice/spectral/rank census, physical Info or altered action '
            'is used. The optional qutrit rank-birth entropy identity is '
            'elementary scalar analysis only.'),
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
