#!/usr/bin/env python3
"""Replay the actual scene-AF metric controls, inputs and hostile mutations."""
from __future__ import annotations
import argparse
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_scene_af_metric_refinement'
PROOF = '02_REGISTRY/research/A4D_NATIVE_SCENE_AF_METRIC_REFINEMENT.md'
PRIMARY = '04_CERTIFICATES/vp_verifiable_registration_metric_closure.py'
INPUT = '812abc87da9c494d14d4b8549b2b219b88c60f86'
OLD_PRIMARY_BLOB = '383c449af69e8005b329e515baa9c344ea9d0142'
OLD_PRIMARY_SHA256 = '203e112d202e521606fb32b8bb0d451d445b2adce3c978d4f479556f8c764a18'
SCOPE = {
    'interface': 'FULL_SCENE_DIAGONAL_GROUP_FIXED_POINT_TENSOR_REGISTER_AF_TOWER',
    'scene_size': 33,
    'first_algebra_GNS_dimension': 12,
    'pairing': 'NORMALIZED_33_DIMENSIONAL_SCENE_TRACE',
    'all_archive_sectors_and_scalar_zero_mode_retained': True,
    'old_constant_two_operator_tail_bound_valid': False,
    'corrected_tail_bound': '33*b^(1-n)/(b-1)^2 * norm([D_b,L_a])',
    'operator_bound_and_weak_star_topology_for_all_fixed_b_gt_one': 'ANALYTIC_PROOF_NOT_LEAN_OR_FINITE_SAMPLE_EXTRAPOLATION',
    'one_step_norm_factor_33_is_sharp_in_the_actual_second_algebra': True,
    'same_bound_claimed_for_arbitrary_AF_filtrations': False,
    'scale_b_or_temperature_selected': False,
    'register_refinement_identified_with_archiveProjection': False,
    'spectral_resolution_identified_with_physical_mesh_h': False,
    'four_dimensional_field_readout_or_own_full_price_preparation_derived': False,
    'own_source_Ward_or_stationarity_derived': False,
    'T0_T3_GR_global_or_original_parent_terminals_closed': False,
    'other_registration_claims_proved_by_the_retained_count_arithmetic': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def load_primary():
    spec = importlib.util.spec_from_file_location('native_scene_metric_primary', ROOT / PRIMARY)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def hostile_mutations():
    code = (ROOT / PRIMARY).read_text()
    mutations = [
        ('algebra_dimension_substituted_for_scene_trace', '    normalization = Q(1, 33)', '    normalization = Q(1, 12)'),
        ('middle_archive_deleted', '    archive_dims = (8, 10, 12)', '    archive_dims = (8, 0, 12)'),
        ('variance_factor_discarded', '    return b * b * t * (1 - t)', '    return b * b * t'),
        ('unnormalized_partial_trace', 'for j in range(d)) / Q(d**2))', 'for j in range(d)) / Q(d))'),
        ('false_sqrt_register_constant', '    return sp.Integer(d)', '    return sp.sqrt(d)'),
        ('geometric_tail_factor_b_lost', '    return d * b ** (1 - n) / (b - 1) ** 2', '    return d * b ** (-n) / (b - 1) ** 2'),
        ('scalar_zero_mode_erased', '        D = b * (sp.eye(12) - P0)', '        D = b * sp.eye(12)'),
    ]
    rejected = []
    with tempfile.TemporaryDirectory(prefix='d0-native-af-metric-mutations-') as directory:
        for name, before, after in mutations:
            expected = 2 if name == 'middle_archive_deleted' else 1
            assert code.count(before) == expected, (name, code.count(before))
            path = Path(directory) / (name + '.py')
            path.write_text(code.replace(before, after, 1))
            p = subprocess.run([sys.executable, str(path)], cwd=ROOT, text=True, capture_output=True)
            assert p.returncode != 0 and 'AssertionError' in p.stderr, (name, p.stdout, p.stderr)
            rejected.append(dict(name=name, rejection=p.stderr.strip().splitlines()[-1]))
    return rejected


def make_ledger():
    primary = load_primary()
    checks = primary.metric_controls()
    assert sum(checks.values()) == 195
    spec = importlib.util.spec_from_file_location('native_scene_composition_primary',
        ROOT / '04_CERTIFICATES/vp_compositional_closure_spectral_limit.py')
    composition = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(composition)
    fixed_counts, group_order = composition.compute_fixed_counts()
    owned_dimensions = {str(n): composition.orbit_count(2*n, fixed_counts, group_order) for n in [1, 2]}
    assert owned_dimensions == {'1': 12, '2': 309}
    inputs = [PRIMARY, PROOF, BASE + '_check.py',
              '04_CERTIFICATES/vp_compositional_closure_spectral_limit.py',
              '01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md']
    return dict(status='PASS_NATIVE_SCENE_AF_METRIC_REFINEMENT', input_head=INPUT,
                original_primary_blob=OLD_PRIMARY_BLOB, original_primary_sha256=OLD_PRIMARY_SHA256,
                scope=SCOPE, checks=checks, exact_controls=sum(checks.values()),
                actual_composition_owner_dimensions=owned_dimensions,
                mathematical_mutations_rejected=hostile_mutations(),
                analytic_proof=PROOF, new_Lean_propositions=0,
                old_bound_counterexample=dict(b='2', observable_trace='1/33',
                    full_commutator_norm_squared='128/1089', left_squared='1024/1089',
                    claimed_right_squared='512/1089', squared_violation_ratio='2'),
                inputs_sha256={p: sha(p) for p in inputs},
                native_F_or_positive_GR_derived=False)


def main():
    global ROOT
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repo', type=Path)
    ap.add_argument('--write', action='store_true')
    args = ap.parse_args()
    if args.repo:
        ROOT = args.repo.resolve()
    actual = make_ledger()
    path = ROOT / (BASE + '_certificate.json')
    if args.write:
        path.write_text(json.dumps(actual, indent=2, sort_keys=True) + '\n')
    saved = json.loads(path.read_text())
    assert saved == actual, 'STALE_OR_FALSE_LEDGER'
    rejected = 0
    for key, value in SCOPE.items():
        false = copy.deepcopy(saved)
        false['scope'][key] = not value if isinstance(value, bool) else 'FALSE_SCOPE'
        try:
            assert false == actual, 'STALE_OR_FALSE_LEDGER'
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError('ACCEPTED_FALSE_SCOPE: ' + key)
    print(actual['status'], actual['exact_controls'], 'CONTROLS',
          len(actual['mathematical_mutations_rejected']), 'MATH_MUTATIONS_REJECTED',
          rejected, 'FALSE_SCOPE_LEDGERS_REJECTED')


if __name__ == '__main__':
    main()
