#!/usr/bin/env python3
"""Preparation-information source of the literal complete record programme.

Only two pinned function definitions from check_flat_relaxation.py and the
literal creator definitions execute; its run() is never imported or called.
The event below is a grouping of the full retained tape, not a replacement
of its pointer entropy, coherent state, or code cost. All16 form coordinates,
all8 first-shell momenta, and reference128 remain in the preparation family.

The role1 one-form e_1 has mask2. Mask1 is the time-role one-form e_0;
substituting mask1 would give a different preparation derivative.
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
    """Execute the two small pinned definitions, never an old entrypoint."""
    tree = ast.parse((repo / PRIOR).read_text())
    names = {'_creators', '_native_rows'}
    nodes = [node for node in tree.body
             if isinstance(node, ast.FunctionDef) and node.name in names]
    if {node.name for node in nodes} != names or len(nodes) != 2:
        raise ArithmeticError('preparation_information:definition_nodes')
    scope = {'s': s, 'ast': ast, 'lru_cache': lru_cache, 'CURVED': CURVED}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), PRIOR, 'exec'), scope)
    return scope['_creators'], scope['_native_rows']


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('preparation_information:' + name)
        checks.append(name)

    p = s.Symbol('p', positive=True)

    def red(value):
        numerator, denominator = s.fraction(s.cancel(s.expand(value)))
        numerator = s.rem(numerator, p*p+p-1, p)
        denominator = s.rem(denominator, p*p+p-1, p)
        if denominator == 0:
            raise ArithmeticError('preparation_information:zero_denominator')
        return s.cancel(numerator / denominator)

    def eq(actual, expected, name):
        difference = actual - expected
        entries = list(difference) if isinstance(difference, s.MatrixBase) else [difference]
        require(all(red(entry) == 0 for entry in entries), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    creators, native_rows = _definitions(repo)
    C, order = creators(repo)
    I, O = s.eye(16), s.zeros(16)
    require(order == (0, 2, 3, 1), 'literal_ACDB_full16_exterior_order')
    require(all(C[r]*C[t].H+C[t].H*C[r] == (I if r == t else O)
                and C[r]*C[t]+C[t]*C[r] == O
                for r in range(4) for t in range(4)),
            'literal_all16_CAR_no_grade_cut')

    nu, b, h = s.Rational(3, 5), s.Rational(4, 5), s.Rational(1, 4)
    eq(nu**2+b**2, 1, 'strict_rational_native_Julia_margin')
    require(0 < nu < 1 and 0 < b < 1 and h > 0,
            'strict_positive_parameters')
    number = [c*c.H for c in C]
    parity = [I-2*n for n in number]
    Zsum = sum(parity, O.copy())
    phases = (s.I, s.S.One, s.S.One, s.S.One)
    rows, left, right = native_rows(C, nu, b, phases)
    require(len(rows) == 64 and len(left) == len(right) == 4,
            'all32_labels_two_coefficients_four_roles_retained')
    row_dict = {(label, coefficient): N for label, coefficient, N in rows}
    N = row_dict[(6, 1)]
    eq(N, (1-b)*Zsum/8,
       'actual_label6_coefficient1_defect_row_from_literal_words')
    eq(N.H, N, 'selected_actual_row_Hermitian')

    # The coefficient1 words are L_r,R_r,-L_r,-R_r and contain no Fourier
    # phase. The SAME N is therefore used for all8 momenta, not refitted.
    eps = p**2*h**2/64
    lam = 2*nu**2/h**2
    c = eps*lam*(1-b)**2/16
    Dblocks, Eblocks = [], []
    for role in range(4):
        for sign in (1, -1):
            phase = sign*s.I
            D = nu/h*((phase-1)*C[role]
                       +(s.conjugate(phase)-1)*C[role].H)
            A = h*D/16
            E = 4*p**2*A*N.H*N*A
            Dblocks.append(D)
            Eblocks.append(E)
    require(all(all(red(entry) == 0 for entry in list(D.H-D)+list(D*D-lam*I))
                for D in Dblocks),
            'all8_actual_L4_axis_D_blocks_full16_same_lambda')
    require(all(all(red(entry) == 0 for entry in
                   E-c*(Zsum-2*parity[role])**2/4)
                for role in range(4) for E in Eblocks[2*role:2*role+2]),
            'all8_exact_effects_from_same_literal_row_not_an_ancillary_probe')
    eq(sum(s.trace(E) for E in Eblocks)/128, c,
       'faithful128_event_average_c_with_all8_momenta')
    eq(c, 9*p**2/320000, 'exact_rational_control_event_coefficient')

    D, E = Dblocks[0], Eblocks[0]
    A = h*D/16
    # This nonblank label has both actual golden ports. No sum over an
    # unrecorded substitute outcome is introduced.
    K0 = -2*p**2*N.H*A
    K1 = -2*p*s.sqrt(p)*N.H*A
    E0, E1 = K0.H*K0, K1.H*K1
    eq(E0+E1, E, 'both_actual_golden_ports_effect_union')
    eq(E0, p**2*E, 'actual_port0_effect_retained_separately')
    eq(E1, p*E, 'actual_port1_effect_retained_separately')

    Pvac, Pe1, Ptime = O.copy(), O.copy(), O.copy()
    Pvac[0, 0], Pe1[2, 2], Ptime[1, 1] = 1, 1, 1
    eq(number[0]*Ptime, Ptime, 'mask1_is_time_role0_not_spatial_e1')
    eq(number[1]*Pe1, Pe1, 'spatial_role1_e1_is_mask2')
    eq(s.trace(E*Pvac), c, 'actual_union_vacuum_probability_c')
    eq(s.trace(E*Pe1), 0, 'actual_union_spatial_e1_probability_zero')
    eq(s.trace(E*Ptime), 4*c, 'hostile_time_oneform_changes_the_source')
    eq(s.trace(E0*Pvac), p**2*c, 'actual_port0_vacuum_probability')
    eq(s.trace(E0*Pe1), 0, 'actual_port0_spatial_e1_probability_zero')

    # Eight16 blocks refer to eight disjoint16-dimensional reference
    # sectors. They are an exact representation of system128/reference128;
    # no reference dimension or momentum sector has been discarded.
    t = s.Symbol('t', real=True)
    X = Pvac-Pe1
    rho_blocks = [I/128+t*X]+[I/128 for _ in range(7)]
    eq(sum(s.trace(rho) for rho in rho_blocks), 1,
       'full_faithful128_linear_preparation_normalized')
    eq(s.trace(X), 0, 'preparation_tangent_trace_zero')
    eq(sum(s.trace(rho*lam*I) for rho in rho_blocks), lam,
       'normalized_Rayleigh_source_lambda_unchanged_exactly')
    q = sum(s.trace(rho*effect) for rho, effect in zip(rho_blocks, Eblocks))
    eq(q, c*(1+t), 'literal_full_preparation_event_q_equals_c_times_one_plus_t')
    q0 = sum(s.trace(rho*p**2*effect) for rho, effect in zip(rho_blocks, Eblocks))
    eq(q0, p**2*c*(1+t), 'same_preparation_derivative_also_visible_in_actual_port0')
    require(rho_blocks[0].is_diagonal()
            and rho_blocks[0][0, 0] == s.Rational(1, 128)+t
            and rho_blocks[0][2, 2] == s.Rational(1, 128)-t
            and all(rho_blocks[0][mask, mask] == s.Rational(1, 128)
                    for mask in range(16) if mask not in (0, 2))
            and rho_blocks[0][2, 2].subs(t, s.Rational(1, 128)) == 0
            and rho_blocks[0][0, 0].subs(t, -s.Rational(1, 128)) == 0
            and rho_blocks[0][2, 2].subs(t, s.Rational(1, 64)) < 0,
            'full_rank_domain_abs_t_less_than_one_over128_sharp_endpoints')

    # Exact normalized square-root purification, not a formal density jet.
    # All126 spectator amplitudes remain 1/sqrt128, including all7 other
    # momentum blocks and all other14 grades of the selected block.
    fplus, fminus = s.sqrt(s.Rational(1, 128)+t), s.sqrt(s.Rational(1, 128)-t)
    eq(fplus**2+fminus**2+s.Rational(126, 128), 1,
       'actual_diagonal_sqrt_family_norm_one_full_reference128')
    C0 = I/s.sqrt(128)
    dC = s.sqrt(128)*X/2
    ddC = -128**s.Rational(3, 2)*(Pvac+Pe1)/4
    eq(s.diff(fplus, t).subs(t, 0), dC[0, 0],
       'actual_sqrt_amplitude_vacuum_first_derivative')
    eq(s.diff(fminus, t).subs(t, 0), dC[2, 2],
       'actual_sqrt_amplitude_spatial_e1_first_derivative')
    eq(dC*C0.H+C0*dC.H, X,
       'actual_full_reference_amplitude_first_jet_gives_X')
    eq(2*s.re(s.trace(C0.H*dC)), 0,
       'actual_normalized_amplitude_first_norm_source_zero')
    eq(ddC*C0.H+2*dC*dC.H+C0*ddC.H, O,
       'sqrt_amplitude_second_jet_gives_affine_density_not_extra_source')
    eq(s.diff(fplus, t, 2).subs(t, 0), ddC[0, 0],
       'actual_sqrt_amplitude_second_derivative_checked')

    # Native complete-blank survival has scalar B on this entire shell.
    # The event is the FIRST selected nonblank mark after complete blanks;
    # all subsequent outputs are unrestricted and still retained.
    B = 1-eps*lam/2
    e = eps*lam-eps**2*lam**2/4
    eq(1-B**2, e, 'native_shell_total_exit_probability_e')
    eq(eps*lam, p**2*nu**2/32,
       'native_shell_exit_clock_parameter_no_recalibration')
    golden = (s.sqrt(5)-1)/2
    require(0 < golden < 1 and nu**2/32 < 1,
            'strict_native_survival_zero_less_than_B_less_than_one')
    z = s.Symbol('z', real=True)
    require(all(s.expand((1-z)*sum(z**j for j in range(n))-(1-z**n)) == 0
                for n in (1, 2, 3, 5)),
            'finite_first_exit_geometric_sum_identity_not_history_census')
    require(all(red(sum(c*(1+t)*B**(2*j) for j in range(n))
                    -(1-(1-e)**n)*c*(1+t)/e) == 0
                for n in (1, 2, 3)),
            'actual_first_exit_mark_probability_C_h_times_one_plus_t')

    # Strict information curvature follows without evaluating any log.
    # Identically zero outcome effects have zero derivative and are omitted
    # from Fisher sums. Full-rank rho keeps the other effects on fixed support.
    x, y = s.symbols('x y', positive=True)
    u, v = s.symbols('u v', real=True)
    eq(u*u/x+v*v/y-(u+v)**2/(x+y),
       (u*y-v*x)**2/(x*y*(x+y)),
       'exact_positive_Fisher_grouping_identity_per_bin')
    Ch = s.Symbol('C_h', positive=True)
    Q = Ch*(1+t)
    eq(Ch**2/Q+Ch**2/(1-Q), Ch**2/(Q*(1-Q)),
       'two_bin_Fisher_lower_bound_for_complete_pointer')
    eq((Ch**2/(Q*(1-Q))).subs(t, 0), Ch/(1-Ch),
       'strict_pointer_information_curvature_at_faithful_preparation')
    require(s.simplify(s.diff(-Q*s.log(Q)-(1-Q)*s.log(1-Q), t, 2)
                       +Ch**2/(Q*(1-Q))) == 0,
            'grouped_pointer_entropy_second_derivative_negative_Fisher')
    weights = s.symbols('ell_0:4', real=True)
    qbase = s.symbols('q_0:4', real=True)
    qdot = s.symbols('dq_0:4', real=True)
    code_cost = sum(weight*(prob+t*derivative)
                    for weight, prob, derivative in zip(weights, qbase, qdot))
    eq(s.diff(code_cost, t, 2), 0,
       'any_fixed_full_code_expected_cost_affine_in_preparation')

    return {
        'status': 'PASS',
        'exact_checks': len(checks),
        'checks': checks,
        'source_pins': PINS,
        'event': {'label': 6, 'coefficient': 1, 'ports': [0, 1],
                  'spatial_e1_mask': 2, 'momentum': '+e0 on L4'},
        'carrier': {'form': 16, 'shell_momenta': 8, 'system': 128,
                    'reference': 128, 'spectator_amplitudes': 126},
        'exact_formulae': {
            'epsilon': 'p^2*h^2/64', 'lambda': '2*nu^2/h^2',
            'c': 'epsilon*lambda*(1-b)^2/16',
            'rational_control_c': str(c),
            'rho': 'I128/128+t*(P_(+e0) tensor (P_vac-P_spatial_e1))',
            'domain': '|t|<1/128',
            'q_kappa': 'c*(1+t)', 'q_port0': 'p^2*c*(1+t)',
            'R': 'lambda',
            'first_exit_e': 'epsilon*lambda-epsilon^2*lambda^2/4',
            'C_h': '(1-(1-e)^n)*c/e',
            'first_exit_q_kappa': 'C_h*(1+t)',
            'pointer_Fisher_at_zero_lower_bound': 'C_h/(1-C_h)>0',
            'fixed_code_cost_second_derivative': '0',
        },
        'scope': (
            'A readout event of the literal full tape, not an entropy or price replacement. '
            'Pointer probabilities, hence retained record states, distinguish a full-rank '
            'preparation family on the same lambda shell. Fixed full-code expected cost is '
            'affine; pointer entropy has a strictly negative Fisher second derivative. '
            'The coherent fixed-reference relative entropy is strictly convex on this '
            'nonconstant record-state family, by its BKM Hessian on the common support. '
            'No physical preparation/admission, complete native action selection, '
            'stationarity, continuum limit, or GR closure follows from these finite checks.'
        ),
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
