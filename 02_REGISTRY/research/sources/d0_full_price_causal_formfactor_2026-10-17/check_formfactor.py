#!/usr/bin/env python3
"""Full16 transverse proper-link vertex and the full-price formfactor interface.

Only frozen creator definitions and the literal owned LC matrix assignment
are extracted by AST. No previous checker or module entrypoint executes.
The new finite checks concern CAR identities, all symbolic momenta, the
complete H+J divided difference, and exact finite-boundary reindexing.
General nonrationality, infinite-moment growth, and the actual matter Schur
consumer are analytic obligations of the accompanying owner, not conclusions
of a finite set of checks below.
"""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CREATORS = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
LC_SOURCE = ('02_REGISTRY/research/sources/'
             'd0_retained_history_causal_source_2026-10-16/check_retained_history.py')
PINS = {
    CREATORS: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    LC_SOURCE: '6be5d31fc2b5a2d2f75b54071720b03c6bbebc30356260b5c823c3ef8ef88d92',
}


def _definitions(repo):
    tree = ast.parse((repo / CREATORS).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
              and t.id == 'EXTERIOR_ORDER' for t in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('formfactor:literal_creator_definition_nodes')
    scope = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, 'exec'), scope)
    creators = [scope['creator'](r) for r in range(4)]

    lc_tree = ast.parse((repo / LC_SOURCE).read_text())
    assignments = [node for node in ast.walk(lc_tree)
                   if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name)
                      and t.id == 'mr' for t in node.targets)]
    if len(assignments) != 1:
        raise ArithmeticError('formfactor:owned_LC_assignment_count')

    def elementary(a, b):
        return s.Matrix(4, 4, lambda i, j: int(i == a and j == b))

    # In the pinned assignment q means theta_prime, x=sin(2theta),
    # y=cos(2theta). This evaluation takes its exact flat first coefficient.
    lc_scope = {'s': s, 'q': s.S.One, 'x': s.S.Zero, 'y': s.S.One,
                'e': elementary}
    exec(compile(ast.Module(body=assignments, type_ignores=[]), LC_SOURCE, 'exec'), lc_scope)
    return creators, scope['EXTERIOR_ORDER'], lc_scope['mr'], elementary


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('formfactor:' + name)
        checks.append(name)

    def eq(actual, expected, name, reduce=s.expand):
        values = list(actual - expected) if isinstance(actual, s.MatrixBase) else [actual - expected]
        require(all(reduce(value) == 0 for value in values), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    C, order, M, elementary = _definitions(repo)
    I, O = s.eye(16), s.zeros(16)
    require(order == (0, 2, 3, 1), 'literal_ACDB_order_all16_grades')
    for r in range(4):
        for t in range(4):
            eq(C[r]*C[t].T+C[t].T*C[r], I if r == t else O,
               'full16_CAR_' + str(r)+str(t))
    annihilator = [c.T for c in C]
    beta = [C[r]+annihilator[r] for r in range(4)]
    gamma = [C[r]-annihilator[r] for r in range(4)]

    def lift(matrix):
        return sum((matrix[a, b]*C[a]*annihilator[b]
                    for a in range(4) for b in range(4)), O.copy())

    R12 = elementary(1, 2)-elementary(2, 1)
    B02 = elementary(0, 2)+elementary(2, 0)
    R01 = elementary(0, 1)-elementary(1, 0)
    for r, expected in enumerate((-R12, -B02, R01, s.zeros(4))):
        eq(M[r], expected, 'owned_actual_flat_LC_connection_' + str(r))
    H = [lift(matrix) for matrix in M]
    eq(sum((C[r]*H[r] for r in range(4)), O.copy()), O,
       'full16_torsionfree_Cartan_cancellation')
    B = [C[r]*H[r]-H[r].T*annihilator[r] for r in range(4)]
    for r, expected in enumerate((-beta[0]*lift(R12), -gamma[1]*lift(B02),
                                  beta[2]*lift(R01), O)):
        eq(B[r], expected, 'true_adjoint_D1_connection_coefficient_' + str(r))
        eq(B[r].T, -B[r], 'D1_coefficient_antiadjoint_' + str(r))

    k0, k1, u, k3, q = s.symbols('k0 k1 u k3 q', real=True)
    nu = s.Symbol('nu', positive=True)
    average = (k0, k1, u, k3)
    incoming = (k0, k1, u-q/2, k3)
    outgoing = (k0, k1, u+q/2, k3)
    Baverage = sum((B[r]*average[r] for r in range(4)), O.copy())

    # For theta=exp(i q x2), p=theta_prime=i q theta. In L1=(nu/2)
    # sum c_r nabla_r^2, the two derivative legs give (k_r+l_r)/2.
    # Form the reverse block before its adjoint; do not adjoint a single
    # complex Fourier coefficient as if it had the same q.
    forward_plus = -q*sum((C[r]*H[r]*average[r] for r in range(4)), O.copy())
    forward_reverse = q*sum((C[r]*H[r]*average[r] for r in range(4)), O.copy())
    D1_vertex_over_nu = forward_plus + forward_reverse.T
    eq(D1_vertex_over_nu, -q*Baverage,
       'proper_link_L1_plus_true_reverse_block_adjoint')
    wrong = -q*sum((B[r]*incoming[r] for r in range(4)), O.copy())
    require(D1_vertex_over_nu != wrong,
            'hostile_omit_moving_endpoint_half_q_changes_actual_vertex')

    gl = sum((gamma[r]*outgoing[r] for r in range(4)), O.copy())
    gk = sum((gamma[r]*incoming[r] for r in range(4)), O.copy())
    Y = gl*Baverage+Baverage*gk
    X = -s.I*nu**2*q*Y
    eq(X, (s.I*nu*gl)*(nu*D1_vertex_over_nu)
       +(nu*D1_vertex_over_nu)*(s.I*nu*gk),
       'actual_full16_A1_vertex_D0out_D1_plus_D1_D0in')

    norm_reduced = s.expand(sum((entry**2 for entry in Y), s.S.Zero))
    norm_expected = 16*((k0-k1)**2*(k1*k1+u*u)
                        +(k1-u)**2*(k0*k0+k1*k1)
                        +(q*q/4)*((u-k0)**2+(k1-u)**2))
    eq(norm_reduced, norm_expected, 'full16_unaveraged_symbolic_HS_norm')
    even_norm = s.expand(sum((norm_reduced.subs({k0: sign0*k0, k1: sign1*k1},
                             simultaneous=True)
                             for sign0 in (-1, 1) for sign1 in (-1, 1)), s.S.Zero)/4)
    Aperp = k0*k0+k1*k1
    P0 = Aperp*(2*k1*k1+q*q/4)
    P2 = 2*Aperp+q*q/2
    eq(even_norm, 16*(P0+u*u*P2), 'parity_even_full_thermal_vertex_norm')
    eq(norm_reduced.subs({k0: 0, k1: 1, u: 0, k3: 0}), 16*(2+q*q/4),
       'nonzero_equal_energy_vertex_not_a_polynomial_commutator')
    eq((s.Rational(1, 2))*(2*s.Rational(1, 2)**2), s.Rational(1, 4),
       'real_cosine_two_edges_and_half_Hessian_normalization')

    # Complete H+J divided difference, keeping Z inside the heat term.
    ek, el, Z, mass, temperature, z, lk, ll = s.symbols(
        'E_k E_l Z M beta z lambda_k lambda_l', real=True)
    ak, al = 1-z+z*ek, 1-z+z*el
    kappak = -ek/Z+mass*temperature*z*ek/ak
    kappal = -el/Z+mass*temperature*z*el/al
    dd = (kappal-kappak)/(ll-lk)
    exact_weight = (ek-el)/(ll-lk)*(1/Z-mass*temperature*z*(1-z)/(ak*al))
    eq(dd, exact_weight, 'complete_HJ_divided_difference_heat_feedback_global_Z', s.cancel)
    fixed_Z_derivative = -temperature*ek*s.diff(kappak, ek)
    eq(fixed_Z_derivative, temperature*ek/Z
       -mass*temperature**2*z*(1-z)*ek/ak**2,
       'equal_feature_branch_exact_derivative_at_fixed_Z', s.cancel)
    a1 = -1/Z+mass*temperature*z/(1-z)
    a2 = -mass*temperature*z*z/(1-z)**2
    eq(s.diff(kappak, ek).subs(ek, 0), a1,
       'first_exponential_tail_coefficient', s.cancel)
    eq(s.diff(kappak, ek, 2).subs(ek, 0)/2, a2,
       'second_exponential_tail_coefficient_if_first_cancels', s.cancel)

    # Exact reindexing before an infinite sum. For fixed positive odd q
    # and N>=q, the finite-cutoff identity has the boundary printed below.
    j, t = s.symbols('j t', integer=True)
    f = s.Function('f')
    eq((f(j+q)/(nu**2*q*(2*j+q))).subs(j, t-q),
       f(t)/(nu**2*q*(2*t-q)), 'Stieltjes_first_numerator_exact_index_shift', s.cancel)
    eq((1/(2*j-q)-1/(2*j+q))/(nu**2*q),
       2/(nu**2*(4*j*j-q*q)), 'Stieltjes_shifted_partial_fraction_identity', s.cancel)
    for qvalue, cutoff in ((1, 2), (3, 4)):
        finite = sum(((f(n+qvalue)-f(n))/(qvalue*(2*n+qvalue))
                      for n in range(-cutoff, cutoff+1)), s.S.Zero)
        stieltjes = sum((2*f(n)/(4*n*n-qvalue*qvalue)
                         for n in range(-cutoff, cutoff+1)), s.S.Zero)
        boundary = (sum((f(n)/(2*n-qvalue)
                         for n in range(cutoff+1, cutoff+qvalue+1)), s.S.Zero)
                    -sum((f(n)/(2*n-qvalue)
                          for n in range(-cutoff, -cutoff+qvalue)), s.S.Zero))/qvalue
        eq(finite-stieltjes, boundary,
           'formal_sequence_finite_boundary_identity_q' + str(qvalue), s.cancel)
    eq(((j-q/2)-(j+q/2))/(2*nu**2*q), -1/(2*nu**2),
       'u_squared_divided_difference_sum_is_exact_local_moment', s.cancel)

    # The q^2 and q^4 prefactors must be combined before claiming an
    # irreducible tail. This is an identity for every integer r>=1; it is
    # not a finite-check proof of nonrationality or Gaussian moment growth.
    r = s.Symbol('r', integer=True, positive=True)
    combined_tail = (-16*nu**2*4**r*Aperp*k1*k1*j**(2*r)
                     -8*nu**2*4**r*Aperp*j**(2*r+2))
    target_tail = -8*nu**2*4**r*Aperp*j**(2*r)*(2*k1*k1+j*j)
    eq(combined_tail, target_tail, 'combined_nonlocal_prefactors_all_tail_orders', s.simplify)

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks,
        'source_pins': PINS,
        'carrier': {'Fock': 16, 'reference_retained': 128,
                    'incoming_preparation_shell_momenta': 8,
                    'thermal_momenta': 'all Z^4; no finite thermal census'},
        'vertex': {
            'polarization': 'theta_1=epsilon cos(q x2), theta_2=theta_3=0',
            'D1_unit_complex_mode': '-nu*q*(B0*k0+B1*k1+B2*(k2+q/2))',
            'B': ['-beta0 Gamma(R12)', '-gamma1 Gamma(B02)', 'beta2 Gamma(R01)', '0'],
            'Xq': 'D0(k+q e2) D1q + D1q D0(k)',
            'parity_even_HS_squared': '16 nu^4 q^2 [A(2k1^2+q^2/4)+(k2+q/2)^2(2A+q^2/2)], A=k0^2+k1^2',
            'real_cosine_susceptibility_factor': '1/4 sum_k kappa^[1](lambda_k,lambda_k+q) ||Xq(k)||_HS^2',
        },
        'full_price': {
            'kappa': '-E/Z+M beta z E/(1-z+zE)',
            'divided_difference': '(E_k-E_l)/(lambda_l-lambda_k) [1/Z-M beta z(1-z)/(A_k A_l)]',
            'global_normalizer_quadratic_term': 'zero for this nonzero Fourier transfer by trace orthogonality; not frozen',
            'clock_cone_term': 'Delta0^2 is cone-independent only on the fixed-positive-G LC graph',
        },
        'formfactor': {
            'definition': 'F_kappa(q;c)=sum_j [kappa(nu^2((j+q)^2+c))-kappa(nu^2(j^2+c))]/[nu^2((j+q)^2-j^2)]',
            'odd_positive_integer_q_identity': 'F_kappa(q;c)=(2/nu^2) sum_j kappa(nu^2(j^2+c))/(4j^2-q^2)',
            'finite_boundary': '[sum_(j=N+1)^(N+q) f_j/(2j-q)-sum_(j=-N)^(-N+q-1) f_j/(2j-q)]/(nu^2 q), N>=q',
            'infinite_sum_assumptions': 'fixed beta>0, nu>0, Z>0, 0<z<1 and finite M; kappa has exponential spectral decay, so polynomially weighted sums converge absolutely and the fixed-q boundary vanishes',
            'bubble_decomposition': '4nu^4 q^2 sum_kperp A(2k1^2+q^2/4) F_kappa(q;kperp^2) -2nu^2 q^2 sum_k (2A+q^2/2) kappa(lambda_k)',
            'combined_q_minus_2r_tail': '-8nu^2 4^r sum_k A k2^(2r)(2k1^2+k2^2) kappa(lambda_k), r>=1',
        },
        'scope': {
            'old_checkers_or_module_entrypoints_executed': False,
            'numerical_q_or_eigenspectrum_scan': False,
            'all16_symbolic_vertex_and_finite_boundary_checked': True,
            'general_infinite_moment_or_nonrationality_proved_by_finite_checks': False,
            'actual_matter_EL_or_joint_branch_solved': False,
            'finite_shell_Schur_cancellation_excluded_by_this_checker': False,
            'physical_action_admission_or_universal_GR_no_go': False,
        },
    }


if __name__ == '__main__':
    print(json.dumps(run(), sort_keys=True, ensure_ascii=False, indent=2))
