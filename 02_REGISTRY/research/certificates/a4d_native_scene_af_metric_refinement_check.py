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
from fractions import Fraction as Q
from math import comb, factorial

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_scene_af_metric_refinement'
PROOF = '02_REGISTRY/research/A4D_NATIVE_SCENE_AF_METRIC_REFINEMENT.md'
PRIMARY = '04_CERTIFICATES/vp_verifiable_registration_metric_closure.py'
INPUT = '812abc87da9c494d14d4b8549b2b219b88c60f86'
HEAT_INPUT = '43fc7657d88d50f390b72b52e86317e98e1f5974'
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
    'full_heat_operator': 'D_b_SQUARED_WITH_ALL_ACTUAL_GNS_MULTIPLICITIES_AND_ZERO_MODE',
    'positive_finite_four_dimensional_small_time_heat_coefficient_for_any_fixed_b_gt_one': False,
    'whole_b_family_heat_obstruction': 'ANALYTIC_ALL_LEVEL_PROOF_NOT_FINITE_EXTRAPOLATION',
    'sqrt_33_scale_selected_as_native': False,
    'fixed_phase_geometric_heat_subsequence_excluded': False,
    'full_bootstrap_price_identified_with_AF_heat_trace': False,
    'all_native_F_or_other_physical_readouts_excluded': False,
    'normalized_GNS_trace_substituted_for_operator_heat_trace': False,
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


def load_composition():
    spec = importlib.util.spec_from_file_location('native_scene_composition_primary',
        ROOT / '04_CERTIFICATES/vp_compositional_closure_spectral_limit.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def heat_dimension(n, counts, group_order):
    value = sum(c * f ** (2*n) for f, c in counts.items())
    assert value % group_order == 0
    return value // group_order


def heat_layer(n, dims):
    return dims[n] - dims[n-1]


def phase_tail_bounds():
    critical_B = 33
    R = critical_B ** 2
    taylor_tail_coefficient = factorial(4)
    return dict(critical_B=critical_B,
                negative=Q(1, 9*(R-1)), center=Q(1, 12),
                next=121*Q(3, 8)**11,
                positive=Q(taylor_tail_coefficient*9, R*(R-1)))


def heat_controls():
    composition = load_composition()
    counts, g = composition.compute_fixed_counts()
    checks = {}
    def require(name, value):
        assert value, name
        checks[name] = 1
    require('full_group_order', g == factorial(9)*factorial(11)*factorial(13))
    require('all_permutations_retained', sum(counts.values()) == g)
    require('single_identity', counts[33] == 1)
    require('no_one_point_move', 32 not in counts)
    require('next_stratum_transpositions', counts[31] == sum(comb(d, 2) for d in (9,11,13)) == 169)
    dims = [heat_dimension(n, counts, g) for n in range(21)]
    dimension_zero = 1
    require('scalar_zero_mode', dims[0] == dimension_zero == 1)
    require('first_two_actual_algebras', dims[1:3] == [12,309])
    stirling = composition.stirling_table(20)
    for n in range(11):
        require('independent_partition_dimension_'+str(n),
                dims[n] == composition.orbit_count_by_partitions(2*n, stirling))
    R, S = 33**2, 31**2
    coefficient = Q(R-1, R*g)
    require('positive_identity_coefficient', coefficient > 0)
    layers = [heat_layer(n, dims) for n in range(1,21)]
    require('first_layer_keeps_scalar_separate', layers[0] == 11)
    for n in range(1,21):
        m = layers[n-1]
        require('positive_full_layer_'+str(n), m > 0)
        require('full_layers_telescope_'+str(n), 1+sum(layers[:n]) == dims[n])
        residual = Q(m)-coefficient*R**n
        actual_residual = Q(sum(c*(f*f-1)*f**(2*n-2)
                                for f,c in counts.items() if f != 33), g)
        require('all_nonidentity_residual_'+str(n), residual == actual_residual)
        require('uniform_subleading_bound_'+str(n), abs(residual) <= Q(g-1,g)*S**n)
    bounds = phase_tail_bounds()
    require('four_dimensional_critical_exponent', bounds['critical_B']**2 == R)
    require('negative_geometric_tail_exact', bounds['negative'] == Q(1,9)*Q(1,R)/(1-Q(1,R)))
    require('positive_geometric_tail_exact', bounds['positive'] == Q(24*9,R**2)/(1-Q(1,R)))
    require('center_exponential_bound', bounds['center'] == Q(1,9)/Q(4,3))
    require('next_exponential_bound', bounds['next'] == Q(11**2)/Q(8,3)**11)
    lower_taylor = sum(Q(1,factorial(n)) for n in range(4))
    upper_taylor = lower_taylor + Q(1,factorial(4))/(1-Q(1,5))
    require('e_lower_finite_taylor', lower_taylor == Q(8,3))
    require('e_upper_controlled_tail', upper_taylor == Q(87,32) < 3)
    require('phase_one_strict_lower', 1/upper_taylor > Q(1,3))
    upper = sum(bounds[k] for k in ('negative','center','next','positive'))
    require('phase_third_exact_upper', upper == Q(13694175177875,159025459101696))
    require('phase_third_below_tenth', upper < Q(1,10))
    require('phase_gap_strict_separation', Q(1,3)-upper > Q(7,30))
    # Whole geometric tails, not numerical exp evaluations, bound the omitted levels.
    for end in (1,2,3,6,12):
        require('negative_partial_within_tail_'+str(end),
                sum(Q(1,9*R**j) for j in range(1,end+1)) < bounds['negative'])
        require('positive_partial_within_tail_'+str(end),
                sum(Q(24*9,R**j) for j in range(2,end+2)) < bounds['positive'])
    return dict(checks=checks, exact_controls=len(checks), group_order=g,
                dimensions={str(n):d for n,d in enumerate(dims)},
                identity_leading_coefficient=str(coefficient),
                critical_heat_ratio=33, critical_Dirac_scale='sqrt(33)_NECESSARY_NOT_SELECTED',
                phase_one_lower='1/3', phase_third_upper=str(upper),
                phase_separation_lower='7/30 times identity_leading_coefficient',
                all_b_and_all_level_asymptotics='ANALYTIC_PROOF',
                fixed_phase_geometric_subsequence_retained=True)


def hostile_heat_mutations():
    code = (ROOT / (BASE+'_check.py')).read_text()
    mutations = [
        ('matrix_index_exponent_halved', 'c * f ** (2*n)', 'c * f ** n'),
        ('nonidentity_archives_deleted',
         'for f, c in counts.items())', 'for f, c in counts.items() if f == 33)'),
        ('layers_replaced_by_total_dimensions',
         '    return dims[n] - dims[n-1]', '    return dims[n]'),
        ('scalar_zero_mode_deleted', '    dimension_zero = 1', '    dimension_zero = 0'),
        ('Dirac_square_scale_confused', '    critical_B = 33', '    critical_B = 1089'),
        ('positive_infinite_tail_wrong_Taylor_order',
         '    taylor_tail_coefficient = factorial(4)', '    taylor_tail_coefficient = factorial(3)'),
    ]
    rejected = []
    with tempfile.TemporaryDirectory(prefix='d0-native-af-heat-mutations-') as directory:
        for name, before, after in mutations:
            # Replacement strings are also quoted inside this mutation table.
            assert code.count(before) == 2, (name, code.count(before))
            path = Path(directory) / (name+'.py')
            path.write_text(code.replace(before,after,1))
            p = subprocess.run([sys.executable,str(path),'--repo',str(ROOT),'--heat-only'],
                               cwd=ROOT,text=True,capture_output=True)
            assert p.returncode != 0 and 'AssertionError' in p.stderr, (name,p.stdout,p.stderr)
            rejected.append(dict(name=name,rejection=p.stderr.strip().splitlines()[-1]))
    return rejected


def make_ledger():
    primary = load_primary()
    checks = primary.metric_controls()
    assert sum(checks.values()) == 195
    composition = load_composition()
    fixed_counts, group_order = composition.compute_fixed_counts()
    owned_dimensions = {str(n): composition.orbit_count(2*n, fixed_counts, group_order) for n in [1, 2]}
    assert owned_dimensions == {'1': 12, '2': 309}
    inputs = [PRIMARY, PROOF, BASE + '_check.py',
              '04_CERTIFICATES/vp_compositional_closure_spectral_limit.py',
              '01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md']
    heat = heat_controls()
    return dict(status='PASS_NATIVE_SCENE_AF_METRIC_AND_HEAT_BOUNDARY', input_head=INPUT,
                heat_continuation_input_head=HEAT_INPUT,
                original_primary_blob=OLD_PRIMARY_BLOB, original_primary_sha256=OLD_PRIMARY_SHA256,
                scope=SCOPE, checks=checks, metric_exact_controls=sum(checks.values()),
                heat_boundary=heat, exact_controls=sum(checks.values())+heat['exact_controls'],
                actual_composition_owner_dimensions=owned_dimensions,
                mathematical_mutations_rejected=hostile_mutations()+hostile_heat_mutations(),
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
    ap.add_argument('--heat-only', action='store_true')
    args = ap.parse_args()
    if args.repo:
        ROOT = args.repo.resolve()
    if args.heat_only:
        print('PASS_AF_HEAT_CONTROLS',heat_controls()['exact_controls'])
        return
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
