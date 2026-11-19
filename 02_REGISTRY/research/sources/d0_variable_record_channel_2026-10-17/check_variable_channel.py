#!/usr/bin/env python3
"""Bounded full16 controls for the variable native record channel.

Only pinned creator/native-row definitions execute; no previous run(), grid,
Choi construction, spectral/rank census, or PDE solver is called. The first
fixture is a first jet of the actual normalized rotating creator. The second
is an actual constant proper-boost connection, not a fitted source. These
identities support, rather than substitute for, the analytic variable-field
Lyapunov/conservativity proof in the owner.
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
    tree = ast.parse((repo/PRIOR).read_text())
    names = {'_creators', '_native_rows'}
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name in names]
    if len(nodes) != 2 or {node.name for node in nodes} != names:
        raise ArithmeticError('variable_channel:definition_nodes')
    scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), PRIOR, 'exec'), scope)
    return scope['_creators'], scope['_native_rows']


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('variable_channel:' + name)
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
    beta = [c+c.H for c in C]
    eta = [s.I*(c-c.H) for c in C]
    xi = [item for pair in zip(beta, eta) for item in pair]
    nu, b = s.Rational(3, 5), s.Rational(4, 5)
    eq(nu**2+b**2, 1, 'strict_rational_native_Julia_margin')
    require(0 < nu < 1 and 0 < b < 1, 'positive_strict_Julia_parameters')

    # The actual blank and nonblank maps give a POSITIVE Dyson split,
    # including the special blank-label/port1 outcome. This is not an
    # arbitrary positive Euler prescription for an unbounded generator.
    p = (s.sqrt(5)-1)/2
    h, z = s.symbols('h z', positive=True)
    epsilon = p**2*h**2/64
    eq(p+p**2, 1, 'original_golden_probability_identity')
    eq(epsilon*(1-p)*h**2/256, epsilon**2/4,
       'special_blank_jump_weight_matches_exact_Delta_rho_Delta_subtraction')
    eq((1-epsilon*z/2)**2
       +epsilon*(z-(1-p)*h**2*z**2/256), 1,
       'exact_nojump_and_jump_effects_telescope_to_identity')
    require(0 < 4*p**2 < 2 and 1-2*p**2 > 0,
            'literal_native_CFL_makes_B_a_positive_contraction')

    # The genuine normalized creator is c0*cos(t)+c1*sin(t). Its first
    # jet is c0+t*c1. Substituting that jet into the pinned row formula
    # gives the exact first jet; no assertion at order t^2 is made.
    t = s.Symbol('t', real=True)
    Cjet = list(C)
    Cjet[0] = C[0]+t*C[1]
    rows, _, _ = native_rows(Cjet, nu, b, (1, 1, 1, 1))
    jets = [(label, coefficient, N.subs(t, 0), N.diff(t).subs(t, 0))
            for label, coefficient, N in rows]
    require(len(jets) == 64, 'all32_labels_two_coefficients_retained')
    require(all(N.H == ((-1)**((label >> 1) & 1))*N
                and dN.H == ((-1)**((label >> 1) & 1))*dN
                for label, coefficient, N, dN in jets if coefficient == 0),
            'coefficient0_fixed_adjoint_phase_is_label_bit1')
    require(all(N.H == N and dN.H == dN
                for _, coefficient, N, dN in jets if coefficient == 1),
            'coefficient1_roots_have_fixed_Hermitian_phase')
    eq(sum((N*N.H for _, _, N, _ in jets), O.copy()), I,
       'actual_local_rows_sum_N_Nadjoint_identity')
    eq(sum((dN*N.H+N*dN.H for _, _, N, dN in jets), O.copy()), O,
       'actual_local_row_unitarity_first_derivative')
    connection = sum((N*dN.H for _, _, N, dN in jets), O.copy())
    rotation01 = C[0]*C[1].H-C[1]*C[0].H
    eq(connection, (1-b)*rotation01/4,
       'actual_Julia_connection_nonzero_even_though_its_trace_vanishes')
    eq(s.trace(connection), 0, 'actual_derivative_trace_sum_N_dNadjoint_zero')
    require(connection != O and connection.H == -connection,
            'actual_nonzero_antiHermitian_connection_not_dropped')

    # A moving Kraus phase leaves the POINTWISE channel unchanged, but
    # changes its action on differential operators. This is why the
    # literal fixed phases above, not CP/TP alone, enter the trace proof.
    phase_N = s.exp(s.I*t)*I
    eq(phase_N*phase_N.H, I, 'hostile_phase_family_still_pointwise_unital')
    phase_connection = (phase_N*phase_N.H.diff(t)).subs(t, 0)
    eq(phase_connection, -s.I*I, 'hostile_phase_has_nonzero_trace_connection')
    require(s.trace(phase_connection) != 0,
            'pointwise_channel_normalization_alone_does_not_imply_trace_cancellation')

    # Constant coframe u_r=nu*e_r, n=e0 and the genuine proper Lorentz
    # connection Omega_2=B01. Its exterior generator is Hermitian.
    Gamma = C[0]*C[1].H+C[1]*C[0].H
    k = s.Symbol('k', real=True)
    D = nu*(k*eta[0]+beta[2]*Gamma)
    Delta = (D*D).applyfunc(s.expand)
    eq(Gamma.H, Gamma, 'actual_full16_exterior_boost_generator_Hermitian')
    eq(D.H, D, 'actual_constant_boost_native_D_Hermitian')
    A = s.I*beta[2]*beta[1]
    eq(Delta, nu**2*(k*k*I+k*A+Gamma*Gamma),
       'actual_boost_D_square_retains_matrix_first_order_term')
    number = [c*c.H for c in C]
    left = [I+(b-1)*n for n in number]
    right = [b*I+(1-b)*n for n in number]

    def T0(X):
        return sum((nu**2*(C[r].H*X*C[r]+C[r]*X*C[r].H)
                    +left[r]*X*left[r]+right[r]*X*right[r]
                    for r in range(4)), O.copy())/8

    base_rows = [N for _, _, N, _ in jets]
    eq(sum((N.H*Delta*N for N in base_rows), O.copy()), T0(Delta),
       'actual_Walsh_rows_equal_paired_Julia_recycling_on_full_Delta')
    eq(T0(I), I, 'paired_Julia_recycling_unital')
    eq(T0(A), (1+b)*A/2,
       'actual_degree2_two_role_recycling_factor')
    defect = (D*(T0(Delta)-Delta)*D).applyfunc(s.expand)
    F3 = defect.applyfunc(lambda value: s.expand(value).coeff(k, 3))
    coefficient = (1-b)*nu**4/2
    eq(F3, -coefficient*A, 'bare_native_energy_has_nonzero_signed_cubic_symbol')
    eq(F3.H, F3, 'bare_energy_cubic_symbol_Hermitian')
    eq(s.trace(F3), 0, 'bare_energy_cubic_symbol_traceless')
    eq(F3*F3, coefficient**2*I, 'bare_energy_cubic_symbol_square_scalar_positive')
    require(coefficient > 0 and F3 != O,
            'bare_energy_cannot_have_uniform_quadratic_upper_bound')

    # The exact first-order cell corrector is not a new action or channel.
    # It is an auxiliary reference-energy correction for the Lyapunov proof.
    principal_D = nu*k*eta[0]
    principal_lambda = nu**2*k*k
    b1 = -nu**2*k*A
    M_b1 = principal_D*T0(b1)*principal_D-principal_lambda*b1
    eq(M_b1, -k**3*F3, 'corrector_cell_operator_cancels_entire_cubic_symbol')

    def Lstar(X):
        return (D*T0(X)*D-(Delta*X+X*Delta)/2).applyfunc(s.expand)

    corrected = Lstar(Delta+b1)
    require(all(s.Poly(entry, k).degree() <= 2
                for entry in corrected if entry != 0),
            'corrected_native_energy_has_order_at_most_two_all16')
    wrong = Lstar(Delta-b1)
    eq(wrong.applyfunc(lambda value: s.expand(value).coeff(k, 3)), 2*F3,
       'hostile_wrong_sign_corrector_leaves_nonzero_cubic')

    # The full Clifford decomposition gives the generic count formula.
    # This is eight scalar degree classes and one actual saturation witness,
    # not enumeration/rank computation of256 matrices.
    degree = s.Symbol('degree', integer=True)
    eq(2*(8-(8-2*degree)), 4*degree,
       'generic_even_Clifford_commutator_factor')
    eq(2*(8+(8-2*degree)), 32-4*degree,
       'generic_odd_Clifford_commutator_factor')
    require(4*2 >= 4 and 32-4*7 == 4,
            'generic_nonidentity_degree_cases_have_commutator_gap_four')
    grade7 = I
    for generator in xi[1:]:
        grade7 = grade7*generator
    eq(grade7.H*grade7, I, 'actual_grade7_gap_witness_unitary')
    eq(s.trace(grade7), 0, 'actual_grade7_gap_witness_traceless')
    commutator_mass = sum((s.trace((x*grade7-grade7*x).H*(x*grade7-grade7*x))
                           for x in xi), s.S.Zero)
    eq(commutator_mass, 4*s.trace(grade7.H*grade7),
       'actual_full16_grade7_saturates_generic_commutator_gap')
    wI = (1+b)**2/4
    require(wI >= s.Rational(1, 4) and nu**2/8 < s.Rational(1, 2),
            'identity_weight_and_CAR_gap_control_both_spectral_sides')
    require((3+b)/4 <= 1-nu**2/8,
            'actual_sharp_flat_factor_respects_general_traceless_gap')

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks,
        'source_pins': PINS,
        'fixture': {'forms': 16, 'nu': str(nu), 'b': str(b),
                    'connection': 'Omega_2=B01, all other Omega_r=0',
                    'variable_jet': 'u0=nu*(e0*cos(t)+e1*sin(t)); other ur=nu*er'},
        'exact_formulae': {
            'sum_N_dNadjoint': '(1-b)/4 * Gamma(e0 e1^T-e1 e0^T)',
            'F3': '-(1-b)*nu^4/2 * i*beta2*beta1',
            'F3_coefficient': str(coefficient),
            'b1': '-nu^2*k*i*beta2*beta1',
            'generic_traceless_gap': 'sigma_min(U)^2/8',
        },
        'scope': (
            'Exact full16 algebraic input controls only. Bare Delta energy fails, '
            'while the indicated auxiliary cell corrector cancels the cubic symbol. '
            'The Lyapunov construction, CF core conditions and conservative QDS, '
            'then the first-jump Stinespring proof of actual finite-grid marginal '
            'trajectory convergence, are analytic owner results rather than '
            'consequences of a rank/spectrum fixture. No entropy/source convergence, '
            'physical admission, new action, matter restriction or GR closure '
            'is claimed.'
        ),
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
