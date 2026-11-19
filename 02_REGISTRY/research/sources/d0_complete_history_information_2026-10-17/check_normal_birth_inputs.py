#!/usr/bin/env python3
"""Exact inputs to the complete-record normal-birth consumer.

Only the pinned full16 creator/order AST definitions execute.  The literal
duplicated-word/32 projection and the owned all-angle coordinate LC matrices
are reconstructed below.  This checks their algebra, not a Stinespring
Schur limit, entropy expansion, field equation or physical admission.
"""
from pathlib import Path
from functools import lru_cache
import ast
import hashlib
import json

import sympy as s


ROOT = Path(__file__).resolve().parents[4]
CREATORS = '02_REGISTRY/research/certificates/a4d_native_curved_soldered_heat.py'
HISTORY = ('02_REGISTRY/research/sources/'
           'd0_retained_history_causal_source_2026-10-16/check_retained_history.py')
PINS = {
    CREATORS: 'bf13f57c902da0005634ae6834c0b4e3ffd2df1aa196a61ebc0ff3dc0351c7da',
    HISTORY: '6be5d31fc2b5a2d2f75b54071720b03c6bbebc30356260b5c823c3ef8ef88d92',
}
LABELS = (16, 8, 24)
CHARS = ((1, 1, -1, -1), (1, -1, 1, -1), (1, -1, -1, 1))


def creators(repo):
    tree = ast.parse((repo / CREATORS).read_text())
    nodes = [node for node in tree.body if
             (isinstance(node, ast.FunctionDef) and node.name == 'creator') or
             (isinstance(node, ast.Assign) and any(isinstance(target, ast.Name)
              and target.id == 'EXTERIOR_ORDER' for target in node.targets))]
    if len(nodes) != 2:
        raise ArithmeticError('normal_birth_inputs:creator_definition_nodes')
    namespace = {'s': s, 'lru_cache': lru_cache}
    exec(compile(ast.Module(body=nodes, type_ignores=[]), CREATORS, 'exec'), namespace)
    return [namespace['creator'](r) for r in range(4)], namespace['EXTERIOR_ORDER']


def run(repo=None):
    repo = ROOT if repo is None else Path(repo).resolve()
    checks = []

    def require(condition, name):
        if not bool(condition):
            raise ArithmeticError('normal_birth_inputs:' + name)
        checks.append(name)

    def equal(actual, expected, name, reduce=s.expand):
        differences = list(actual - expected) if isinstance(actual, s.MatrixBase) else [actual - expected]
        require(all(reduce(value) == 0 for value in differences), name)

    for path, digest in PINS.items():
        require(hashlib.sha256((repo / path).read_bytes()).hexdigest() == digest,
                'source_pin_' + Path(path).name)
    C, order = creators(repo)
    I, O = s.eye(16), s.zeros(16)
    require(order == (0, 2, 3, 1), 'actual_ACDB_order_all16')
    require(all(C[i] * C[j].H + C[j].H * C[i] == (I if i == j else O)
                for i in range(4) for j in range(4)), 'full16_CAR_without_grade_restriction')

    def elementary(i, j):
        value = s.zeros(4)
        value[i, j] = 1
        return value

    def lift(value):
        return sum((value[i, j] * C[i] * C[j].H
                    for i in range(4) for j in range(4)), O.copy())

    x, y, velocity = s.symbols('sin2theta cos2theta theta_prime', real=True)
    e = elementary
    # Same literal all-angle Mr as the pinned original owner (no old run).
    Mr = [velocity * (x * e(0, 2) - y * e(1, 2) + e(2, 1)),
          velocity * (-y * e(0, 2) - x * e(1, 2) - e(2, 0)),
          velocity * (e(0, 1) - e(1, 0)), s.zeros(4)]
    forward = [C[r] * lift(Mr[r]) for r in range(4)]
    J = [value + value.H for value in forward]
    Aforward, Bforward, Cforward = C[0] * C[1] * C[2].H, C[0] * C[2] * C[1].H, C[1] * C[2] * C[0].H
    A, B, Cc = Aforward + Aforward.H, Bforward + Bforward.H, Cforward + Cforward.H
    expected = [velocity * (B - y * A), velocity * (y * A - Cc),
                velocity * (Cc - B), O]
    require(all(s.expand(v) == 0 for r in range(4) for v in J[r] - expected[r]),
            'actual_Mr_true_adjoint_gives_three_constant_CAR_components')
    require(all(value.H == value for value in (A, B, Cc)) and
            all(s.trace(value * value) == 4 for value in (A, B, Cc)) and
            all(s.trace(left * right) == 0 for left, right in ((A, B), (A, Cc), (B, Cc))),
            'three_full16_Hermitian_components_norm4_mutually_HS_orthogonal')
    equal(sum(forward, O.copy()), O, 'full16_Cartan_forward_sum_zero')
    equal(sum(J, O.copy()), O, 'full16_positive_D_connection_sum_zero')

    # Original role-major SELECT: four Julia words, each duplicated.
    # Only coefficient0/top-left is needed, so no defect root is substituted.
    # For arbitrary P these tops are P,P*, -C,-C*, exactly as in the owner.
    h, nu = s.symbols('h nu', real=True)
    scaled = [nu * value for value in C]
    P = [scaled[r] + h * nu * forward[r] for r in range(4)]
    tops = []
    for r in range(4):
        for value in (P[r], P[r].H, -scaled[r], -scaled[r].H):
            tops.extend((value, value))
    require(len(tops) == 32, 'literal_four_roles_four_words_two_duplicates')
    role_J = []
    for label, chi in zip(LABELS, CHARS):
        literal = sum((((-1) ** bin(label & word).count('1')) * tops[word]
                       for word in range(32)), O.copy()) / 32
        Dchi = nu * sum((chi[r] * J[r] for r in range(4)), O.copy())
        equal(literal, h * Dchi / 16, 'literal_rare_Walsh_coefficient0_label_' + str(label))
        equal(literal.subs(h, 0), O, 'literal_rare_baseline_zero_label_' + str(label))
        role_J.append(Dchi / nu)
    require(any(s.expand(v) != 0 for v in role_J[0] / 16 - role_J[0] / 32),
            'hostile_wrong_Walsh_factor_rejected')
    # A complex first jet makes .H and .T distinct; it is a control of the
    # coefficient0 projection, not another physical coframe or gate.
    complex_jet = s.I * forward[0]
    require(complex_jet + complex_jet.H != complex_jet + complex_jet.T and
            forward[0] != forward[0] + forward[0].H,
            'hostile_transpose_or_dropped_adjoint_changes_actual_row')

    direct_roles = [2 * velocity * (B - Cc), 2 * velocity * (Cc - y * A),
                    2 * velocity * (B - y * A)]
    require(all(s.expand(v) == 0 for index in range(3)
                for v in role_J[index] - direct_roles[index]),
            'all_three_literal_role_potentials_in_constant_component_basis')
    norms = [s.expand(s.trace(value.H * value)) for value in role_J]
    expected_norms = [32 * velocity ** 2, 16 * velocity ** 2 * (1 + y ** 2),
                      16 * velocity ** 2 * (1 + y ** 2)]
    require(all(s.expand(actual - expected) == 0
                for actual, expected in zip(norms, expected_norms)),
            'three_full16_role_norms_exact_all_angles')

    p = s.Symbol('p', real=True)
    golden = lambda value: s.rem(s.expand(value), p * p + p - 1, p)
    equal(p * p + p, 1, 'both_actual_golden_port_weights_sum_one', golden)
    require(golden(p * p - 1) != 0 and golden(p - 1) != 0,
            'hostile_single_port_does_not_have_union_weight')

    # Periodic angle: mean(theta' cos(2theta)) is a boundary difference.
    theta0, theta1, length = s.symbols('theta0 theta1 period', real=True, nonzero=True)
    theta = s.Symbol('theta', real=True)
    equal(s.integrate(s.cos(2 * theta), (theta, theta0, theta1)),
          (s.sin(2 * theta1) - s.sin(2 * theta0)) / 2,
          'periodic_cosine_weighted_velocity_is_exact_boundary')
    w, E, F = s.symbols('mean_theta_prime mean_theta_prime_squared mean_cos2theta_squared_theta_prime_squared', real=True)
    mean_roles = [2 * w * (B - Cc), 2 * w * Cc, 2 * w * B]
    mean_squares = [32 * E, 16 * (E + F), 16 * (E + F)]
    variances = [s.expand(mean_squares[index] - s.trace(mean_roles[index].H * mean_roles[index]))
                 for index in range(3)]
    equal(sum(variances), 32 * (2 * E + F) - 64 * w ** 2,
          'complete_three_row_periodic_variance_including_winding_mean')
    angle = s.Symbol('angle', real=True)
    winding_rows = [value.subs({velocity: 1, y: s.cos(2 * angle)}) for value in role_J]
    winding_means = [value.applyfunc(lambda entry: s.integrate(entry, (angle, 0, 2 * s.pi)) / (2 * s.pi))
                     for value in winding_rows]
    winding_variances = [s.simplify(s.integrate(s.trace(value.H * value), (angle, 0, 2 * s.pi)) / (2 * s.pi)
                                  - s.trace(mean.H * mean))
                         for value, mean in zip(winding_rows, winding_means)]
    require(winding_variances == [0, 8, 8],
            'literal_nonzero_winding_has_positive_variance_in_other_two_rows')
    equal(sum(winding_variances), 16, 'all_three_rows_nonzero_winding_variance_total16')

    return {
        'status': 'PASS', 'exact_checks': len(checks), 'checks': checks,
        'source_pins': PINS,
        'carrier': {'Fock': 16, 'reference': 128, 'occupied_momenta': 8,
                    'literal_labels': 32, 'coefficient_outputs': 2, 'golden_ports': 2},
        'role_rows': {'labels': list(LABELS), 'coefficient': 0,
                      'literal_normalization': 'N_kappa=h*D_chi/16',
                      'baseline': 'N_kappa,0=0 identically when P_r=C_r'},
        'all_angle_components': ['J0=theta_prime*(B-cos(2theta)*A)',
                                 'J1=theta_prime*(cos(2theta)*A-C)',
                                 'J2=theta_prime*(C-B)', 'J3=0'],
        'periodic_variance': 'sum_chi mean||J_chi-mean J_chi||HS^2 = 32*(2*mean(theta_prime^2)+mean(cos(2theta)^2*theta_prime^2))-64*mean(theta_prime)^2',
        'unit_winding_theta_y_variances': [0, 8, 8],
        'scope': {'old_entrypoints_executed': False,
                  'spectral_or_rank_census_performed': False,
                  'new_detector_gate_price_or_action_added': False,
                  'full_Stinespring_Schur_or_entropy_limit_proved_by_this_helper': False,
                  'all10_Einstein_or_joint_stationarity_claimed': False,
                  'physical_preparation_or_matrix_program_admission_claimed': False},
    }


if __name__ == '__main__':
    print(json.dumps(run(), ensure_ascii=False, sort_keys=True, indent=2))
