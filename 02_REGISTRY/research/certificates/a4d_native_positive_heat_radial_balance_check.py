#!/usr/bin/env python3
"""Exact full-carrier controls for positive Hodge heat; no preparation is selected."""
import argparse
import copy
import hashlib
import itertools
import json
import os
import re
import shutil
import subprocess
import tempfile
from collections import Counter
from fractions import Fraction
from pathlib import Path

import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_positive_heat_radial_balance'
PROOF = '02_REGISTRY/research/A4D_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE.md'
INPUT = 'eeab0de21ee704794e291434e6ae0b65fdb360d6'
PRIOR = ['a4d_native_composed_feedback_dynamics', 'a4d_native_weighted_dirac_boundary']
PREFIX = 'D0.Research.NativePositiveHeatRadialBalance.'
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}
PRIMARY_GRADE_AXIOM = 'D0.Geometry.carCreateInt_degree_raise._native.native_decide.ax_1_1'
SCOPE = {
    'class': 'POSITIVE_GRADED_HODGE_WITH_ADMITTED_FULL_JOINT_RADIAL_PATH_AND_FIXED_BETA',
    'price': 'LITERAL_EXISTING_FULL_BOOTSTRAP_HEAT_PLUS_ALL_REMAINING_TERMS',
    'actual_genuine_radial_heat_HasDerivAt_compiled': True,
    'all_new_propositions_standard_axioms_only': True,
    'actual_curved_coefficient_degree_proof_rebuilt_by_kernel_decide': True,
    'printed_prior_degree_owner_retains_its_explicit_native_decide_leaf': True,
    'requires_positive_pairing_nonzero_d_and_owned_scaling_admission': True,
    'flatness_or_d_squared_zero_required_for_similarity': False,
    'retained_zero_modes_or_other_archive_rows_deleted': False,
    'full_moving_graded_spectral_argument_and_uniform_L_contrast_bound': 'ANALYTIC_NOT_FULL_LEAN',
    'radial_contraction_determines_all_ten_source_components_or_pure_trace': False,
    'native_joint_preparation_or_constitutive_uniqueness_derived': False,
    'all_positive_pairings_or_all_coupled_bootstraps_excluded': False,
    'all_nearby_corrected_roots_or_recovery_excluded': False,
    'native_h_squared_normalization_or_temperature_law_installed': False,
    'compensating_source_or_stationarity_gate_selected': False,
    'coupled_one_direction_control_is_admitted_full_joint_root': False,
    'whole_core_F_absence_GR_or_original_parent_terminal_closed': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def compile_capsule():
    formal = ROOT / '03_FORMALIZATION'
    lean = subprocess.check_output(['lake', 'env', 'which', 'lean'], cwd=formal, text=True).strip()
    leanpath = subprocess.check_output(['lake', 'env', 'printenv', 'LEAN_PATH'], cwd=formal, text=True).strip()
    stem = Path(BASE).name
    with tempfile.TemporaryDirectory(prefix='d0-positive-heat-') as directory:
        directory = Path(directory)
        env = dict(os.environ, LEAN_PATH=str(directory) + ':' + leanpath)
        for mod in PRIOR + [stem]:
            source = ROOT / ('02_REGISTRY/research/certificates/' + mod + '.lean')
            target = directory / (mod + '.lean')
            shutil.copyfile(source, target)
            proc = subprocess.run([lean, '--root=' + str(directory), '-o', str(directory / (mod + '.olean')), str(target)],
                                  cwd=formal, env=env, text=True, capture_output=True)
            output = proc.stdout + proc.stderr
            assert proc.returncode == 0, output
            if mod == stem:
                assert ': warning' not in output and 'sorryAx' not in output, output
                (ROOT / (BASE + '_output.txt')).write_text(output)
    write_receipt()


def write_receipt():
    source = (ROOT / (BASE + '.lean')).read_text()
    output = (ROOT / (BASE + '_output.txt')).read_text()
    names = re.findall(r'^#check ([\w.]+)', source, re.M)
    assert len(names) == len(set(names)) == 22
    assert ': error' not in output and ': warning' not in output and 'sorryAx' not in output
    axioms = {name: [a.strip() for a in items.split(',') if a.strip()]
              for name, items in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)}
    axioms.update({name: [] for name in re.findall(r"'([^']+)' does not depend on any axioms", output)})
    assert set(axioms) == set(names)
    declarations = [name for name in names if name.startswith(PREFIX)]
    owners = [name for name in names if name not in declarations]
    assert len(declarations) == 19 and len(owners) == 3
    for name in names:
        extra = set(axioms[name]) - STANDARD
        assert extra == ({PRIMARY_GRADE_AXIOM} if name == 'D0.Geometry.dConn_raises_degree' else set())
    printed = {}
    for name in names:
        found = re.search(r'^' + re.escape(name) + r'(?:\.\{[^\n]*\})?[\s\S]*?(?=\n\x27' + re.escape(name) + r'\x27)', output, re.M)
        assert found, name
        printed[name] = found.group().strip()
    transitive = {}
    def walk(path):
        if path in transitive:
            return
        transitive[path] = sha(path)
        for name in re.findall(r'^import\s+(D0\.[\w.]+)', (ROOT / path).read_text(), re.M):
            walk('03_FORMALIZATION/' + name.replace('.', '/') + '.lean')
    capsules = ['02_REGISTRY/research/certificates/' + mod + '.lean' for mod in PRIOR] + [BASE + '.lean']
    for path in capsules:
        for name in re.findall(r'^import\s+(D0\.[\w.]+)', (ROOT / path).read_text(), re.M):
            walk('03_FORMALIZATION/' + name.replace('.', '/') + '.lean')
    old = json.loads((ROOT / '02_REGISTRY/research/certificates/a4d_native_weighted_dirac_boundary_results.json').read_text())
    tool = old['toolchain_input_sha256']
    inputs = ['01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
              '02_REGISTRY/research/A4D_NATIVE_COMPOSED_FEEDBACK_DYNAMICS.md',
              '02_REGISTRY/research/A4D_NATIVE_WEIGHTED_DIRAC_BOUNDARY.md',
              '02_REGISTRY/research/A4D_NATIVE_CONSTRAINED_PRICE_SOURCE.md',
              '02_REGISTRY/research/A4D_NATIVE_HODGE_CONNES_METRIC.md']
    for mod in PRIOR:
        inputs.extend('02_REGISTRY/research/certificates/' + mod + suffix for suffix in ['.lean', '_results.json', '_output.txt'])
    result = {
        'status': 'PASS', 'input_head': INPUT, 'compiler_exit_code': 0,
        'supported_D0_tree': subprocess.check_output(['git', 'rev-parse', 'HEAD:03_FORMALIZATION/D0'], cwd=ROOT, text=True).strip(),
        'command': ['python3', BASE + '_check.py', '--compile'],
        'compiler_procedure': 'Use lake env to resolve the pinned Lean executable and dependency path. Copy the two unchanged research capsules and this capsule into a fresh temporary root; compile each in dependency order with --root and -o. Only then compile and audit this capsule.',
        'capsule': BASE + '.lean', 'capsule_sha256': sha(BASE + '.lean'),
        'output': BASE + '_output.txt', 'output_sha256': sha(BASE + '_output.txt'),
        'declarations': declarations, 'primary_owner_propositions': owners,
        'printed_propositions': {n: printed[n] for n in declarations},
        'printed_primary_owner_propositions': {n: printed[n] for n in owners},
        'axioms': axioms, 'inherited_primary_degree_axioms': [PRIMARY_GRADE_AXIOM],
        'transitive_d0_source_sha256': dict(sorted(transitive.items())),
        'primary_and_prior_input_sha256': {p: sha(p) for p in inputs},
        'toolchain_input_sha256': {p: sha(p) for p in tool},
        'full_graded_spectral_and_uniform_L_bound_kernel_formalized': False,
        'native_preparation_source_or_GR_derived': False,
    }
    (ROOT / (BASE + '_results.json')).write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')


def zero(matrix):
    return matrix == sp.zeros(*matrix.shape)


def compound_weight(F):
    Q = F * F.T
    M = Q.inv()
    mu = F.det()
    assert mu > 0
    masks = [[r for r in range(4) if mask & (1 << r)] for mask in range(16)]
    def entry(a, b):
        if len(masks[a]) != len(masks[b]):
            return 0
        return mu * (M.extract(masks[a], masks[b]).det() if masks[a] else 1)
    W = sp.Matrix(16, 16, entry)
    E = sp.Matrix(16, 16, lambda a, b: F.inv().extract(masks[a], masks[b]).det()
                  if len(masks[a]) == len(masks[b]) and masks[a] else int(a == b == 0))
    return Q, mu, W, E


def covariant_d(curved=False):
    L = 2
    points = list(itertools.product(range(L), repeat=4))
    index = {p: i for i, p in enumerate(points)}
    rows = {}
    for x in points:
        site = index[x]
        for ket in range(16):
            for r in range(4):
                if ket & (1 << r):
                    continue
                bra = ket | (1 << r)
                sign = (-1) ** bin(ket & ((1 << r) - 1)).count('1')
                y = list(x)
                y[r] = (y[r] + 1) % L
                coefficient = 2 if curved and x == (0, 0, 0, 0) and r == 0 else 1
                for col, value in [(16 * index[tuple(y)] + ket, L * sign * coefficient),
                                   (16 * site + ket, -L * sign)]:
                    key = (16 * site + bra, col)
                    rows[key] = rows.get(key, 0) + value
    return points, sp.SparseMatrix(256, 256, rows)


def rational_energy(spectrum, beta_multiple=1):
    Z = sum((Fraction(2) ** (-beta_multiple * value) * multiplicity for value, multiplicity in spectrum.items()), Fraction(0))
    numerator = sum((value * Fraction(2) ** (-beta_multiple * value) * multiplicity for value, multiplicity in spectrum.items()), Fraction(0))
    return numerator / Z


def controls():
    checks = {}
    def ck(name, condition, count=1):
        assert bool(condition), name
        checks[name] = checks.get(name, 0) + count
    receipt = json.loads((ROOT / (BASE + '_results.json')).read_text())
    output = (ROOT / (BASE + '_output.txt')).read_text()
    ck('actual_compiler_and_input', receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0 and receipt['input_head'] == INPUT)
    ck('actual_declaration_counts', len(receipt['declarations']) == 19 and len(receipt['primary_owner_propositions']) == 3)
    ck('no_sorry_error_warning', ': error' not in output and ': warning' not in output and 'sorryAx' not in output)
    for name in receipt['declarations'] + receipt['primary_owner_propositions']:
        extra = set(receipt['axioms'][name]) - STANDARD
        ck('resolved_proposition_and_transitive_axioms', name in output and extra ==
           ({PRIMARY_GRADE_AXIOM} if name == 'D0.Geometry.dConn_raises_degree' else set()))
    ck('genuine_derivative_not_totalized_deriv', 'HasDerivAt' in receipt['printed_propositions'][PREFIX + 'actual_heat_radial_derivative'])
    ck('curved_degree_has_no_nilpotency_premise', 'dConn U' in receipt['printed_propositions'][PREFIX + 'actual_covariant_d_raises_degree'] and
       'HasDerivAt' not in receipt['printed_propositions'][PREFIX + 'actual_covariant_d_raises_degree'])
    for group in ['transitive_d0_source_sha256', 'primary_and_prior_input_sha256', 'toolchain_input_sha256']:
        for path, digest in receipt[group].items():
            ck('source_pin_' + group, sha(path) == digest)
    ck('new_capsule_and_output_hashes', sha(BASE + '.lean') == receipt['capsule_sha256'] and sha(BASE + '_output.txt') == receipt['output_sha256'])
    ck('analytic_formal_boundary', not receipt['full_graded_spectral_and_uniform_L_bound_kernel_formalized'] and not receipt['native_preparation_source_or_GR_derived'])

    F = sp.Matrix([[1, sp.Rational(1, 2), sp.Rational(1, 3), sp.Rational(1, 7)], [0, 1, sp.Rational(1, 4), sp.Rational(1, 5)],
                   [0, 0, 1, sp.Rational(1, 6)], [0, 0, 0, sp.Rational(3, 2)]])
    Fs = [F, F * sp.diag(2, 1, 1, 1)]
    weights = []
    for frame in Fs:
        Q, mu, W, E = compound_weight(frame)
        ck('positive_full_compound_factorization', W == mu * E.T * E and E.det() != 0 and mu > 0)
        ck('mixed_metric_retained', all(Q[i, j] != 0 for i in range(4) for j in range(4)))
        ck('all_sixteen_graded_weights', W.shape == (16, 16) and W.det() != 0)
        weights.append(W)
        for c in [sp.Rational(3, 2), sp.Rational(2)]:
            qc, muc, wc, ec = compound_weight(c * frame)
            T = sp.diag(*[c ** (4 - 2 * bin(k).count('1')) for k in range(16)])
            ck('literal_geometric_homogeneity_all_degrees', qc == c**2 * Q and muc == c**4 * mu and wc == T * W)
    for signature in [sp.eye(4), sp.diag(1, -1, -1, -1)]:
        qt = F * signature * F.T
        D = sp.eye(4)
        D[0, 1] = sp.Rational(2, 3)
        D[2, 3] = sp.Rational(1, 5)
        qs = D * qt * D.T
        ck('both_endpoints_full_joint_radial_tangent', D * (2 * qt) * D.T == 2 * qs)
        ck('frozen_endpoint_is_rejected', D * (2 * qt) * D.T != sp.zeros(4))
        for v in [sp.eye(4), qt]:
            A = sp.Matrix([[1, 2, 3, 4], [2, 5, 6, 7], [3, 6, 8, 9], [4, 7, 9, 10]])
            packed = sum(A[i, i] * v[i, i] for i in range(4)) + 2 * sum(A[i, j] * v[i, j] for i in range(4) for j in range(i + 1, 4))
            ck('packed_dual_trace_uses_all_ten_slots', packed == sp.trace(A.T * v))

    full_cases = []
    for curved in [False, True]:
        points, d = covariant_d(curved)
        ck('all_native_sites_and_grades_retained', d.shape == (256, 256))
        ck('coefficient_curvature_control', (not zero(d * d)) if curved else zero(d * d))
        blocks = [weights[x[0]] for x in points]
        W = sp.SparseMatrix(sp.diag(*blocks))
        WI = sp.SparseMatrix(sp.diag(*[block.inv() for block in blocks]))
        delta = WI * d.T * W
        D0 = d + delta
        ck('full_weighted_adjoint', d.T * W == W * delta)
        ck('full_dirac_weighted_symmetry', D0.T * W == W * D0)
        c = sp.Rational(2)
        J = sp.diag(*[c ** bin(k).count('1') for x in points for k in range(16)])
        JI = sp.diag(*[c ** (-bin(k).count('1')) for x in points for k in range(16)])
        T = sp.diag(*[c ** (4 - 2 * bin(k).count('1')) for x in points for k in range(16)])
        TI = sp.diag(*[c ** (-4 + 2 * bin(k).count('1')) for x in points for k in range(16)])
        wc = T * W
        wci = WI * TI
        deltac = wci * d.T * wc
        Dc = d + deltac
        ck('actual_full_coupled_codifferential_scale', deltac == delta / c**2)
        ck('full_dirac_similarity_not_constant_pairing', Dc == J * D0 * JI / c)
        ck('full_squared_similarity_with_curvature_retained', Dc * Dc == J * (D0 * D0) * JI / c**2)
        ck('freezing_the_adjoint_is_wrong', Dc != D0)
        full_cases.append({'curved_coefficient_links': curved, 'dimension': 256,
                           'd_squared_nonzero': not zero(d * d), 'dirac_nonzero': not zero(D0)})
    points, d = covariant_d(False)
    lap = (d + d.T) ** 2
    spectral_results = []
    for L, one_axis in [(2, [0, 16]), (4, [0, 32, 64, 32])]:
        spectrum = Counter()
        for x in itertools.product(one_axis, repeat=4):
            spectrum[sum(x)] += 16
        ck('literal_flat_full_spectrum_cardinality', sum(spectrum.values()) == 16 * L**4 and spectrum[0] == 16)
        energy = rational_energy(spectrum)
        ck('literal_flat_thermal_energy_strict', energy > 0)
        if L == 2:
            ck('actual_flat_operator_spectral_first_moment', sp.trace(lap) == sum(k * v for k, v in spectrum.items()))
            ck('actual_flat_operator_spectral_second_moment', sp.trace(lap * lap) == sum(k*k*v for k, v in spectrum.items()))
        for zeros in [1, 65, 653]:
            extended = spectrum.copy()
            extended[0] += zeros
            ee = rational_energy(extended)
            ck('every_added_zero_mode_retained_sign_survives', 0 < ee < energy)
        spectral_results.append({'L': L, 'full_spectrum': {str(k): v for k, v in sorted(spectrum.items())},
                                 'energy_at_beta_log2': str(energy)})
    ck('zero_operator_is_excluded_hypothesis_control', rational_energy(Counter({0: 256})) == 0)
    ck('indefinite_spectrum_sign_control', rational_energy(Counter({-1: 1, 0: 1, 1: 1})) == -Fraction(3, 7))
    ck('temperature_scale_not_silently_fixed', rational_energy(Counter({0: 1, 1: 1}), 2) < rational_energy(Counter({0: 1, 1: 1}), 1))
    u = sp.Symbol('u', real=True)
    d_control = sp.zeros(4)
    d_control[1, 0] = 1
    grades_control = [0, 1, 0, 1]
    ck('coupled_control_is_actual_positive_graded_dirac_square',
       (d_control + d_control.T)**2 == sp.diag(1, 1, 0, 0) and
       all(grades_control[i] == grades_control[j] + 1
           for i in range(4) for j in range(4) if d_control[i, j] != 0))
    cayley = sp.Matrix([[1-u**2, -2*u], [2*u, 1-u**2]]) / (1+u**2)
    U_control = sp.diag(cayley, sp.eye(2))
    P_control = sp.diag(1, 0, 0, 0)
    ck('coupled_control_complete_orthogonal_operation',
       (U_control.T * U_control - sp.eye(4)).applyfunc(sp.factor) == sp.zeros(4))
    feedback = 4*u**2/(1+u**2)**2
    ck('coupled_control_same_full_carrier_feedback',
       (P_control * U_control.T * (sp.eye(4)-P_control) * U_control * P_control -
        sp.diag(feedback, 0, 0, 0)).applyfunc(sp.factor) == sp.zeros(4))
    sqrtW_control = sp.diag(4, 2, 4, 2)
    W_control = sqrtW_control**2
    U_scaled = sqrtW_control.inv() * U_control * sqrtW_control
    adjoint_scaled = W_control.inv() * U_scaled.T * W_control
    ck('coupled_control_respects_moving_positive_pairing',
       (adjoint_scaled * U_scaled - sp.eye(4)).applyfunc(sp.factor) == sp.zeros(4))
    ck('coupled_control_feedback_survives_orthonormal_frame_transport',
       (P_control * adjoint_scaled * (sp.eye(4)-P_control) * U_scaled * P_control -
        sp.diag(feedback, 0, 0, 0)).applyfunc(sp.factor) == sp.zeros(4))
    price_jet = sp.diff(feedback, u)/(2*(1-feedback/2))
    at = sp.factor(price_jet.subs(u, sp.Rational(1, 3)))
    thermal_jet = sp.Rational(2, 3)
    ck('coupled_control_full_paired_spectrum_thermal_jet',
       2 * rational_energy(Counter({0: 2, 1: 2})) == thermal_jet)
    parameter_jet = -sp.Rational(205, 324)
    ck('same_bootstrap_cayley_derivative_exact', at == sp.Rational(216, 205))
    ck('coupled_radial_cancellation_not_universal_no_go', thermal_jet + at*parameter_jet == 0)
    ck('strict_operator_domain_at_cancellation_control', 1-feedback.subs(u, sp.Rational(1, 3))/2 == sp.Rational(41, 50))
    for n in [2, 3, 5, 10]:
        h = Fraction(1, n**3)
        epsilon = Fraction(1, n)
        ck('fixed_price_contrast_has_wrong_h_order', epsilon/h == n**2)
        ck('h_squared_normalization_changes_bound', h*h*epsilon/h == Fraction(1, n**4))
    return {'checks': checks, 'total_controls': sum(checks.values()), 'full_matrix_cases': full_cases,
            'flat_spectral_controls': spectral_results,
            'radial_cancellation_control': {'full_spectrum': [0, 0, 1, 1],
                                            'positive_graded_dirac_square': True,
                                            'thermal': '2/3', 'feedback_parameter_derivative': str(parameter_jet),
                                            'feedback_price_parameter_derivative': str(at), 'total': '0',
                                            'is_native_full_joint_root': False}}


def make_ledger():
    result = controls()
    result.update(schema='d0-native-positive-heat-radial-balance-v1', input_head=INPUT, scope=SCOPE,
                  input_sha256={p: sha(p) for p in [PROOF, BASE + '.lean', BASE + '_output.txt', BASE + '_results.json', BASE + '_check.py']})
    return result


def validate_ledger(candidate, actual):
    assert candidate == actual


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compile', action='store_true')
    parser.add_argument('--receipt-only', action='store_true')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    if args.compile:
        compile_capsule()
    if args.receipt_only:
        write_receipt()
        print('RADIAL_RECEIPT_PASS')
        return
    actual = make_ledger()
    path = ROOT / (BASE + '_certificate.json')
    if args.write:
        path.write_text(json.dumps(actual, indent=2, sort_keys=True) + '\n')
    saved = json.loads(path.read_text())
    validate_ledger(saved, actual)
    rejected = 0
    for key, value in SCOPE.items():
        false = copy.deepcopy(saved)
        false['scope'][key] = not value if isinstance(value, bool) else 'FALSE_SCOPE'
        try:
            validate_ledger(false, actual)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('accepted false scope ' + key)
    print('PASS_NATIVE_POSITIVE_HEAT_RADIAL_BALANCE', actual['total_controls'], 'CONTROLS', rejected, 'FALSE_LEDGERS_REJECTED')


if __name__ == '__main__':
    main()
