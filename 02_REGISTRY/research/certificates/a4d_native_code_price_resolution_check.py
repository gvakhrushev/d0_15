#!/usr/bin/env python3
"""Literal code-price resolution: exact controls and compiled finite inequalities."""
from __future__ import annotations
import argparse
import copy
import hashlib
import itertools
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as Q
import sympy as sp

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_code_price_resolution'
PROOF = '02_REGISTRY/research/A4D_NATIVE_CODE_PRICE_RESOLUTION.md'
INPUT = 'f55bea04beed7aab18141e4284e49fe66cd397ed'
PREFIX = 'D0.Research.NativeCodePriceResolution.'
STANDARD = {'propext', 'Classical.choice', 'Quot.sound'}
PRIMARY = [
    '01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md',
    '03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean',
    '02_REGISTRY/research/A4D_NATIVE_COUPLED_HODGE_SCALE_BOUNDARY.md',
]
SCOPE = {
    'price_class': 'LITERAL_INTEGER_CODE_PRICE_WITH_OWN_LEVEL_UNIT_AND_COMMON_LEVEL_OFFSET',
    'all_state_spaces_grammars_readouts_and_endpoint_pairs_in_that_class': True,
    'fixed_nonzero_calibration_required': True,
    'all_scalar_probes_with_nonzero_linear_response_required_for_unit_bound': True,
    'probe_constants_must_be_uniform_in_scalar_parameter': False,
    'measurable_or_continuous_native_preparation_choice_required': False,
    'all_probe_unit_bound': 'ANALYTIC_MEASURE_PROOF_NOT_FULL_LEAN',
    'finite_lattice_error_and_rounding_inequalities_kernel_checked': True,
    'integer_prices_follow_from_ActionProtocol_lower_bound_alone': False,
    'whole_heat_feedback_bootstrap_is_identified_with_code_length': False,
    'log_sum_and_shrinking_native_units_are_excluded': False,
    'rounding_constructs_admitted_codes_or_respects_native_level_budgets': False,
    'physical_homothetic_test_is_a_native_sourced_solution': False,
    'golden_event_comparison_deletes_a_history_or_archive_mode': False,
    'golden_event_readout_actuation_or_geometric_admission_derived': False,
    'native_normalization_temperature_or_action_selected': False,
    'joint_preparation_full_source_Ward_or_stationarity_derived': False,
    'T0_T3_GR_global_closure_or_original_parents_closed': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def half_contrast(nu, a, np, nm):
    return nu * (np - nm) / (2 * a)


def lattice_distance(b, delta):
    k = b // delta
    return min(abs(b - delta * k), abs(b - delta * (k + 1)))


def nearest_index(b, delta):
    return (b / delta + Q(1, 2)) // 1


def record_lower_bound(b, e):
    return abs(b) - e


def band_bound(B, delta, radius):
    return 2 * radius / delta + 6 * radius / B


def band_measure(B, delta, radius):
    assert B > 0 and delta > 2 * radius > 0
    lo = -(radius // delta)  # exact ceiling of -radius/delta
    hi = (B + radius) // delta
    intervals = []
    for k in range(lo, hi + 1):
        left, right = max(Q(0), k * delta - radius), min(B, k * delta + radius)
        if left <= right:
            intervals.append((left, right))
    # delta > 2*radius makes the interiors disjoint, including clipped ends.
    return sum((right - left for left, right in intervals), Q(0)) / B


def golden_event_mass(p, n):
    return 1 - p ** (2 * n)


def math_controls():
    checks = {}
    def ck(name, condition):
        assert bool(condition), name
        checks[name] = checks.get(name, 0) + 1
    for nu, a in [(Q(1), Q(1)), (Q(-3, 2), Q(2)), (Q(3, 7), Q(-2))]:
        for np, nm in [(0, 0), (7, 1), (1, 7), (2, 1)]:
            value = half_contrast(nu, a, np, nm)
            ck('exact_endpoint_half_contrast', value == nu * Q(np - nm, 2) / a)
            ck('integer_lattice_membership', value / (nu / (2 * a)) == np - nm)
    for n in [4, 8, 16, 32, 64]:
        h, epsilon, delta = Q(1, n**3), Q(1, n), Q(1, 2)
        b = Q(3, 7) * epsilon
        ck('probe_mesh_is_in_four_N', n**3 % 4 == 0 and epsilon**3 == h)
        ck('fixed_gap_nearest_zero', 2 * abs(b) < delta and lattice_distance(b, delta) == abs(b))
        for k in [-5, -1, 0, 1, 7]:
            ck('signed_integer_gap_control', abs(delta * k - b) >= abs(b))
        r = h  # k=0 with a positive recording error exactly h
        ck('recording_error_is_retained', abs(r - b) >= record_lower_bound(b, h))
        ck('recording_error_can_make_unreduced_bound_false', abs(r - b) < abs(b))
        for delta_small in [h, h*h]:
            for t in [Q(-1), Q(1, 3), Q(1, 2), Q(5, 7), Q(1)]:
                target = Q(3, 7) * epsilon * t
                k = nearest_index(target, delta_small)
                ck('shrinking_unit_rounding_control', abs(delta_small * k - target) <= delta_small / 2)
        for t in [Q(0), Q(1, 2), Q(1)]:
            ck('finite_probe_list_is_insufficient', lattice_distance(epsilon*t, epsilon/2) == 0)
        ck('fixed_missing_probe_detects_coarse_spacing',
           lattice_distance(epsilon/3, epsilon/2) == epsilon/6)
        ck('fixed_missing_probe_error_over_h', (epsilon/6)/h == Q(n*n, 6))
        ck('zero_response_exception', lattice_distance(Q(0), delta) == 0)
        ck('unit_lower_bound_not_gap', 1 + epsilon >= 1 and (1 + epsilon) - 1 == epsilon < 1)
        varying_delta = Q(1, n*n)
        measure = band_measure(epsilon, varying_delta, h)
        ck('exact_covering_measure_bound', 0 < measure <= band_bound(epsilon, varying_delta, h))
        ck('covering_measure_subsequence_bound', band_bound(epsilon, varying_delta, h) == Q(2, n) + Q(6, n*n))
    ck('covering_bound_lattice_count_term_is_required',
       band_measure(Q(1), Q(1, 10), Q(1, 1000)) <= band_bound(Q(1), Q(1, 10), Q(1, 1000)))
    p = (sp.sqrt(5) - 1) / 2
    ck('actual_golden_root', sp.simplify(p + p*p - 1) == 0 and p > 0 and p < 1)
    for n in [1, 2, 3, 4, 5]:
        costs = [sum(word) for word in itertools.product([1, 2], repeat=n)]
        ck('all_golden_records_retained', len(costs) == 2**n)
        weights = [p**cost for cost in costs]
        ck('golden_full_partition', sp.simplify(sum(weights) - 1) == 0)
        # A query on a retained event; the complementary word remains in costs.
        event_weight = sum(p**cost for cost in costs if cost != 2*n)
        ck('golden_event_weight_exact', sp.simplify(event_weight - golden_event_mass(p, n)) == 0)
        if n >= 2:
            ck('log_event_price_strictly_between_zero_and_one',
               sp.simplify(event_weight - p) > 0 and sp.simplify(1-event_weight) > 0)
    return checks


def math_mutation_controls():
    """Exercise the numerical controls after changing six mathematical rules."""
    source = Path(__file__).read_text()
    mutations = [
        ('missing_half_contrast_factor',
         '    return nu * (np - nm) / (2 * a)', '    return nu * (np - nm) / a'),
        ('all_lattice_distances_falsely_zero',
         '    return min(abs(b - delta * k), abs(b - delta * (k + 1)))', '    return Q(0)'),
        ('floor_substituted_for_nearest_integer',
         '    return (b / delta + Q(1, 2)) // 1', '    return (b / delta) // 1'),
        ('recording_error_discarded',
         '    return abs(b) - e', '    return abs(b)'),
        ('lattice_density_term_discarded',
         '    return 2 * radius / delta + 6 * radius / B', '    return 6 * radius / B'),
        ('wrong_golden_event_exponent',
         '    return 1 - p ** (2 * n)', '    return 1 - p ** n'),
    ]
    rejected = []
    with tempfile.TemporaryDirectory(prefix='d0-code-price-mutations-') as directory:
        for name, before, after in mutations:
            # Match only the actual function line, not the mutation's string.
            needle = '\n' + before + '\n'
            assert source.count(needle) == 1, name
            path = Path(directory) / 'research/certificates' / (name + '.py')
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(source.replace(needle, '\n' + after + '\n', 1))
            proc = subprocess.run([sys.executable, str(path), '--repo', str(ROOT), '--math-only'],
                                  cwd=ROOT, text=True, capture_output=True)
            assert proc.returncode != 0 and 'AssertionError' in proc.stderr, (name, proc.stdout, proc.stderr)
            rejected.append(name)
    return rejected


def compile_capsule():
    formal = ROOT / '03_FORMALIZATION'
    lean = subprocess.check_output(['lake', 'env', 'which', 'lean'], cwd=formal, text=True).strip()
    leanpath = subprocess.check_output(['lake', 'env', 'printenv', 'LEAN_PATH'], cwd=formal, text=True).strip()
    stem = Path(BASE).name
    with tempfile.TemporaryDirectory(prefix='d0-code-price-') as directory:
        directory = Path(directory)
        target_phi = directory / 'D0/Core/Phi.lean'
        target_phi.parent.mkdir(parents=True)
        shutil.copyfile(ROOT / '03_FORMALIZATION/D0/Core/Phi.lean', target_phi)
        target = directory / (stem + '.lean')
        shutil.copyfile(ROOT / (BASE + '.lean'), target)
        env = dict(os.environ, LEAN_PATH=str(directory) + ':' + leanpath)
        for source in [target_phi, target]:
            proc = subprocess.run([lean, '--root=' + str(directory), '-o', str(source.with_suffix('.olean')), str(source)],
                                  cwd=formal, env=env, text=True, capture_output=True)
            output = proc.stdout + proc.stderr
            assert proc.returncode == 0 and 'sorryAx' not in output and ': warning' not in output, output
            if source == target:
                (ROOT / (BASE + '_output.txt')).write_text(output)
    write_receipt()


def write_receipt():
    source = (ROOT / (BASE + '.lean')).read_text()
    output = (ROOT / (BASE + '_output.txt')).read_text()
    short_names = re.findall(r'^#check ([\w.]+)', source, re.M)
    names = [name if name.startswith('D0.') else PREFIX + name for name in short_names]
    assert len(names) == len(set(names)) == 10
    assert not any(x in output for x in [': error', ': warning', 'sorryAx'])
    axioms = {name: [a.strip() for a in items.split(',') if a.strip()]
              for name, items in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", output)}
    axioms.update({name: [] for name in re.findall(r"'([^']+)' does not depend on any axioms", output)})
    assert set(axioms) == set(names)
    props = {}
    for name in names:
        assert set(axioms[name]) <= STANDARD
        found = re.search(r'^' + re.escape(name) + r'(?:\.\{[^\n]*\})?[\s\S]*?(?=\n\x27' + re.escape(name) + r'\x27)', output, re.M)
        assert found, name
        props[name] = found.group().strip()
    receipt = dict(status='PASS', input_head=INPUT, compiler_exit_code=0,
                   command='lake env lean, with literal D0.Core.Phi rebuilt in a temporary module root before the capsule',
                   literal_primary_phi_compiled=True, declarations=names[:-1], primary_owner_propositions=names[-1:],
                   printed_propositions=props, axioms=axioms, capsule_sha256=sha(BASE + '.lean'),
                   output_sha256=sha(BASE + '_output.txt'),
                   transitive_d0_source_sha256={'03_FORMALIZATION/D0/Core/Phi.lean': sha('03_FORMALIZATION/D0/Core/Phi.lean')},
                   primary_input_sha256={path: sha(path) for path in PRIMARY},
                   toolchain_input_sha256={path: sha(path) for path in
                       ['03_FORMALIZATION/lean-toolchain', '03_FORMALIZATION/lake-manifest.json']},
                   all_probe_analytic_theorem_fully_Lean_formalized=False,
                   native_preparation_source_or_GR_derived=False)
    (ROOT / (BASE + '_results.json')).write_text(json.dumps(receipt, indent=2, sort_keys=True) + '\n')


def make_ledger():
    receipt = json.loads((ROOT / (BASE + '_results.json')).read_text())
    assert receipt['status'] == 'PASS' and receipt['compiler_exit_code'] == 0 and receipt['input_head'] == INPUT
    assert receipt['literal_primary_phi_compiled'] and len(receipt['declarations']) == 9
    assert len(receipt['primary_owner_propositions']) == 1
    assert not receipt['all_probe_analytic_theorem_fully_Lean_formalized']
    assert not receipt['native_preparation_source_or_GR_derived']
    for group in ['transitive_d0_source_sha256', 'primary_input_sha256', 'toolchain_input_sha256']:
        for path, digest in receipt[group].items():
            assert sha(path) == digest, ('CHANGED_INPUT', path)
    assert sha(BASE + '.lean') == receipt['capsule_sha256']
    assert sha(BASE + '_output.txt') == receipt['output_sha256']
    assert set(receipt['axioms']) == set(receipt['printed_propositions']) == set(receipt['declarations'] + receipt['primary_owner_propositions'])
    assert all(set(a) <= STANDARD for a in receipt['axioms'].values())
    checks = math_controls()
    return dict(status='PASS_NATIVE_CODE_PRICE_RESOLUTION', input_head=INPUT, scope=SCOPE,
                checks=checks, total_controls=sum(checks.values()), compiled_propositions=9,
                rejected_mathematical_mutations=math_mutation_controls(),
                printed_primary_propositions=1, transitive_d0_pins=1,
                all_probe_proof='Analytic fixed-probe countable-cover measure argument in the proof; finite controls do not prove it.',
                inputs_sha256={path: sha(path) for path in PRIMARY + [PROOF, BASE+'.lean', BASE+'_results.json', BASE+'_output.txt', BASE+'_check.py']},
                native_T0_T3_GR_or_parent_terminal_closed=False)


def validate_ledger(candidate, actual):
    assert candidate == actual, 'STALE_OR_FALSE_LEDGER'


def main():
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path)
    ap.add_argument('--compile', action='store_true')
    ap.add_argument('--receipt-only', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--math-only', action='store_true')
    args = ap.parse_args()
    if args.repo:
        ROOT = args.repo.resolve()
    if args.math_only:
        checks = math_controls()
        print('MATH_CONTROLS_PASS', sum(checks.values()))
        return
    if args.compile:
        compile_capsule()
    if args.receipt_only:
        write_receipt()
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
            raise AssertionError('ACCEPTED_FALSE_SCOPE: ' + key)
    print(actual['status'], actual['total_controls'], 'CONTROLS',
          len(actual['rejected_mathematical_mutations']), 'MATH_MUTATIONS_REJECTED',
          rejected, 'FALSE_LEDGERS_REJECTED')


if __name__ == '__main__':
    main()
