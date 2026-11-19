#!/usr/bin/env python3
"""Exact nonlinear test of the SAME retained three-label coherent reading.

Pinned definitions and one owned local matrix assignment are extracted.
No previous run(), root, spectrum, receipt or field-dependent detector runs.
"""
from pathlib import Path
import ast
import hashlib
import importlib.util
import json

import sympy as s

ROOT = Path(__file__).resolve().parents[4]
PRINCIPAL = '02_REGISTRY/research/sources/d0_retained_causal_principal_2026-10-17/check_principal.py'
HISTORY = '02_REGISTRY/research/sources/d0_retained_history_causal_source_2026-10-16/check_retained_history.py'
CREATORS = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
PINS = {
    PRINCIPAL: '7f57f6e325defd8fda3e85667cf040f061ef8dba6a0897a127385ed8de49380d',
    HISTORY: '6be5d31fc2b5a2d2f75b54071720b03c6bbebc30356260b5c823c3ef8ef88d92',
    CREATORS: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
}


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('retained_nonlinear:' + name)
        checks.append(name)

    def eq(actual, expected, name, reduce=s.expand):
        values = list(actual-expected) if isinstance(actual, s.MatrixBase) else [actual-expected]
        require(all(reduce(value) == 0 for value in values), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo/path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    spec = importlib.util.spec_from_file_location('retained_principal_defs', repo/PRINCIPAL)
    principal = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(principal)
    C, order = principal.creators(repo)  # Definition API only, never run().
    require(order == (0, 2, 3, 1), 'actual_ACDB_all16_creator_order')
    O = s.zeros(16)

    def elementary(i, j):
        matrix = s.zeros(4)
        matrix[i, j] = 1
        return matrix

    # Execute only the literal owned all-angle matrix assignment, not its
    # enclosing run() or any of its checks/outputs.
    tree = ast.parse((repo/HISTORY).read_text())
    function = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == 'run')
    assignments = [n for n in function.body if isinstance(n, ast.Assign)
                   and any(isinstance(t, ast.Name) and t.id == 'mr' for t in n.targets)]
    require(len(assignments) == 1, 'owned_all_angle_matrix_assignment_identity')
    x, y, q = s.symbols('sin2theta cos2theta theta_prime', real=True)
    scope = {'q': q, 'x': x, 'y': y, 'e': elementary, 's': s}
    exec(compile(ast.Module(body=assignments, type_ignores=[]), HISTORY, 'exec'), scope)
    M = scope['mr']
    def lift(matrix):
        return sum((matrix[i, j]*C[i]*C[j].T for i in range(4)
                    for j in range(4)), O.copy())
    L = [C[r]*lift(M[r]) for r in range(4)]
    J = [value+value.T for value in L]
    eq(sum(L, O.copy()), O, 'owned_all_angle_forward_Cartan_identity')
    chi_J = [sum((chi[r]*J[r] for r in range(4)), O.copy())
             for chi in principal.CHARS]
    eq(sum(chi_J, O.copy()), 4*J[0], 'same_coherent_projector_extracts_four_J0_all_angles')
    circle = lambda value: s.rem(s.expand(value), x*x+y*y-1, x)
    eq(s.trace(J[0]*J[0]), 4*(1+y*y)*q*q,
       'independent_full16_all_angle_J0_norm', circle)
    jv = sum(chi_J, O.copy())/s.sqrt(3)
    eq(s.trace(jv*jv)/16, s.Rational(4, 3)*(1+y*y)*q*q,
       'same_coherent_readout_all_angle_potential_norm', circle)

    theta, velocity, acceleration = s.symbols('theta theta_prime theta_second', real=True)
    survival, scale = s.symbols('one_minus_exp_beta_lambda scale', positive=True)
    f = 1+s.cos(2*theta)**2
    density = survival*f*velocity**2/(192*scale**2)
    from_history = survival*(s.trace(jv*jv)/16).subs(
        {x: s.sin(2*theta), y: s.cos(2*theta), q: velocity})/(256*scale**2)
    eq(from_history, density, 'actual_clock_gives_nonlinear_density_not_fitted_weight', s.trigsimp)
    eq(density-survival*velocity**2/(96*scale**2),
       -survival*s.sin(2*theta)**2*velocity**2/(192*scale**2),
       'exact_action_discrepancy_is_negative_square_not_boundary', s.trigsimp)
    amplitude, u, du = s.symbols('epsilon u du', real=True)
    gap = (density-survival*velocity**2/(96*scale**2)).subs(
        {theta: amplitude*u, velocity: amplitude*du})
    eq(s.diff(gap, amplitude, 4).subs(amplitude, 0)/s.factorial(4),
       -survival*u**2*du**2/(48*scale**2), 'first_discrepancy_is_quartic')
    angle = s.Symbol('y', real=True)
    eq(s.integrate(s.cos(angle)**2*s.sin(angle)**2, (angle, 0, 2*s.pi))/(2*s.pi),
       s.Rational(1, 8), 'periodic_cosine_quartic_mean_exact_one_eighth')
    euler = s.diff(density, theta)-(s.diff(density, velocity, theta)*velocity
                                   +s.diff(density, velocity, 2)*acceleration)
    expected = -survival*((1+s.cos(2*theta)**2)*acceleration
                          -s.sin(4*theta)*velocity**2)/(96*scale**2)
    eq(euler, expected, 'full_nonlinear_Euler_includes_weight_derivative', s.trigsimp)
    flat = euler.subs({theta: 0, velocity: 0})
    quarter = euler.subs({theta: s.pi/4, velocity: 0})
    eq(flat, -survival*acceleration/(48*scale**2), 'flat_principal_matches_previous_three_field_result')
    eq(quarter, flat/2, 'constant_pi_over_four_cone_has_half_principal_coefficient')
    # The exact existing single-cone EH action is -2s^2(theta')^2.
    eh_euler = 4*scale**2*acceleration
    witness = {theta: s.pi/8, acceleration: 0}
    eq(euler.subs(witness), survival*velocity**2/(96*scale**2),
       'same_coherent_readout_has_nonzero_source_at_linear_theta_germ', s.trigsimp)
    eq(eh_euler.subs(witness), 0, 'exact_single_cone_EH_source_vanishes_at_that_germ')
    require(s.trigsimp(euler+survival*eh_euler/(192*scale**4)) != 0,
            'no_automatic_nonlinear_EH_promotion_of_principal_comparison')

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks, 'source_pins': PINS,
        'carrier': {'Fock': 16, 'reference': 128, 'occupied_momenta': 8,
                    'retained_labels': [16, 8, 24], 'golden_ports': 'both'},
        'detector_unchanged': '(|16>+|8>+|24>)(<16|+<8|+<24|)/3',
        'cone': 'e=s O01(theta(y)), y=x2; same true LC links and fixed positive G=s^2 I',
        'nonlinear_readout_contrast': '(1-exp(-beta/s^2))/(192*s^2) * mean((1+cos(2theta)^2)*(theta_prime)^2)',
        'nonlinear_Euler': '-(1-exp(-beta/s^2))/(96*s^2) * [(1+cos(2theta)^2)*theta_second-sin(4theta)*(theta_prime)^2]',
        'principal_coefficient_ratio_pi_over_four_vs_zero': '1/2',
        'EH_mismatch_germ': 'theta=pi/8, theta_second=0: history source=(1-exp(-beta/s^2))*(theta_prime)^2/(96*s^2), EH source=0',
        'scope': {'old_run_entrypoints_executed': False,
                  'prior_principal_results_modified': False,
                  'new_field_dependent_detector_or_price_selected': False,
                  'same_fixed_coherent_detector_is_full_nonlinear_EH': False,
                  'all_detectors_or_native_actions_excluded': False,
                  'physical_detector_or_preparation_admission_proved': False},
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
