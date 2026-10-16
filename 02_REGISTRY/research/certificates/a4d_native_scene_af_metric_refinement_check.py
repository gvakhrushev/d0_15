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

# Mutant scripts may live directly below /tmp. Resolve a supplied --repo
# before consulting the script depth; the default applies only to this file.
ROOT = None
BASE = '02_REGISTRY/research/certificates/a4d_native_scene_af_metric_refinement'
PROOF = '02_REGISTRY/research/A4D_NATIVE_SCENE_AF_METRIC_REFINEMENT.md'
PRIMARY = '04_CERTIFICATES/vp_verifiable_registration_metric_closure.py'
INPUT = '812abc87da9c494d14d4b8549b2b219b88c60f86'
HEAT_INPUT = '43fc7657d88d50f390b72b52e86317e98e1f5974'
PHASE_INPUT = 'cad6f9a3168d26c72a72a98a71d737e470bac508'
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
    'ordinary_second_heat_coefficient_exists_on_some_fixed_phase': False,
    'all_intermediate_archive_heat_orders_retained': True,
    'fixed_phase_leading_heat_error_rate': '(961/1089)^N_WITH_POSITIVE_COEFFICIENT',
    'phase_decomposition_and_second_coefficient_proof': 'ANALYTIC_ALL_LEVEL_ALL_FIXED_PHASES',
    'formal_subtraction_of_intermediate_orders_admitted_as_native': False,
    'vanishing_full_bootstrap_metric_stress_derived': False,
    'heat_rate_promoted_to_physical_action_contrast_obstruction': False,
    'fixed_point_strata_declared_independent_native_heat_blocks': False,
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


def phase_strata(counts):
    return [f for f in sorted(counts) if f >= 2]


def stratum_kappa(f, count, group_order):
    return Q(count,group_order)*(1-Q(1,f*f))


def zero_stratum_contribution(n, count, group_order):
    return -Q(count,group_order)*0**(2*n-2)


def curvature_strata(strata):
    return [f for f in strata if f >= 6]


def bounded_remainder_limit(counts, group_order):
    return Q(counts[1],group_order)


def leading_error_ratio():
    return Q(31**2,33**2)


def phase_controls():
    counts,g = load_composition().compute_fixed_counts()
    checks = {}
    def require(name, value):
        assert value,name
        checks[name] = 1
    strata = phase_strata(counts)
    require('complete_actual_fixed_point_support', set(counts)==set(range(32))|{33})
    require('complete_positive_increment_strata', strata==list(range(2,32))+[33])
    require('actual_31_stratum_retained', counts[31]==169 and 31 in strata)
    kappas = {f:stratum_kappa(f,counts[f],g) for f in strata}
    for f in strata:
        require('positive_stratum_'+str(f), kappas[f]>0)
        require('negative_level_tail_mass_'+str(f), kappas[f]/(1-Q(1,f*f))==Q(counts[f],g))
    for n in range(1,7):
        require('zero_fixed_point_term_'+str(n),
                zero_stratum_contribution(n,counts[0],g)==(-Q(counts[0],g) if n==1 else 0))
        require('one_fixed_point_increment_'+str(n), counts[1]*(1**2-1)*1**(2*n-2)==0)
    constant = bounded_remainder_limit(counts,g)
    require('bounded_remainder_limit_exact',
            1-Q(counts[0],g)-sum(kappas[f]/(1-Q(1,f*f)) for f in strata)==constant)
    require('bounded_remainder_nonnegative', 0<constant<1)
    require('all_remainder_weights_retained',
            Q(counts[0],g)+constant+sum(Q(counts[f],g) for f in strata)==1)
    strong = curvature_strata(strata)
    weak = [f for f in strata if f not in strong]
    require('all_stronger_than_curvature_strata', strong==list(range(6,32))+[33])
    require('all_weaker_than_curvature_strata', weak==[2,3,4,5])
    for f in strong:
        require('strictly_above_curvature_order_'+str(f), f*f>33)
    for f in weak:
        require('strictly_below_curvature_order_'+str(f), f*f<33)
    require('no_exact_curvature_power', all(f*f!=33 for f in strata))
    require('unique_leading_stratum', [f for f in strata if f*f==1089]==[33])
    require('unique_next_stratum', max(f for f in strata if f<33)==31)
    require('next_order_strictly_intermediate', 33<961<1089)
    uniform_lower = kappas[31]*Q(1,3*31**2)
    require('uniform_phase_lower_bound', uniform_lower==Q(169*320,g*961**2)>0)
    ratio = leading_error_ratio()
    require('leading_error_exact_ratio', ratio==Q(961,1089))
    require('leading_error_decays_but_slower_than_curvature', Q(1,33)<ratio<1)
    require('second_coefficient_growth_factor', Q(961,33)>1)
    require('formal_full_strong_order_subtraction_control', max(Q(f*f,33) for f in weak)==Q(25,33)<1)
    for n in range(7):
        require('all_level_ratio_identity_'+str(n), ratio**n*1089**n==961**n)
        require('retained_next_increment_'+str(n),
                kappas[31]*961**(n+1)==Q(169*960,g)*961**n)
    return dict(checks=checks,exact_controls=len(checks),
                positive_strata=strata,intermediate_strata=list(range(6,32)),
                subcurvature_strata=weak,scalar_remainder_limit=str(constant),
                uniform_next_profile_lower_bound=str(uniform_lower),
                fixed_phase_leading_error_ratio=str(ratio),
                proof='ANALYTIC_FULL_DECOMPOSITION_AND_ALL_FIXED_PHASE_LIMITS',
                leading_fixed_phase_limit_preserved=True,
                second_coefficient_diverges_positive_infinity=True,
                formal_subtraction_control_is_not_native=True)


def hostile_phase_mutations():
    code = (ROOT/(BASE+'_check.py')).read_text()
    mutations = [
        ('next_archive_stratum_deleted',
         '    return [f for f in sorted(counts) if f >= 2]',
         '    return [f for f in sorted(counts) if f >= 2 and f != 31]'),
        ('increment_coefficient_replaced_by_dimension',
         '    return Q(count,group_order)*(1-Q(1,f*f))', '    return Q(count,group_order)'),
        ('zero_fixed_point_sign_reversed',
         '    return -Q(count,group_order)*0**(2*n-2)', '    return Q(count,group_order)*0**(2*n-2)'),
        ('curvature_order_threshold_shifted',
         '    return [f for f in strata if f >= 6]', '    return [f for f in strata if f >= 5]'),
        ('one_fixed_point_remainder_deleted',
         '    return Q(counts[1],group_order)', '    return Q(0)'),
        ('matrix_pair_power_lost_in_level_rate',
         '    return Q(31**2,33**2)', '    return Q(31,33)'),
    ]
    rejected=[]
    with tempfile.TemporaryDirectory(prefix='d0-native-af-phase-mutations-') as directory:
        for name,before,after in mutations:
            assert code.count(before)==2,(name,code.count(before))
            path=Path(directory)/(name+'.py');path.write_text(code.replace(before,after,1))
            p=subprocess.run([sys.executable,str(path),'--repo',str(ROOT),'--phase-only'],
                             cwd=ROOT,text=True,capture_output=True)
            assert p.returncode!=0 and 'AssertionError' in p.stderr,(name,p.stdout,p.stderr)
            rejected.append(dict(name=name,rejection=p.stderr.strip().splitlines()[-1]))
    return rejected


def shallow_path_replays():
    """Exercise explicit --repo before default-path indexing, as on Linux CI."""
    launcher = '''from pathlib import Path
import sys
source, root, mode = sys.argv[1:]
code = Path(source).read_text()
sys.argv = ['/checker.py', '--repo', root, mode]
exec(compile(code, '/checker.py', 'exec'), {'__name__':'__main__', '__file__':'/checker.py'})
'''
    outputs = {}
    for mode, expected in [('--heat-only','PASS_AF_HEAT_CONTROLS 121'),
                           ('--phase-only','PASS_AF_PHASE_CONTROLS 136')]:
        p = subprocess.run([sys.executable,'-c',launcher,str(ROOT/(BASE+'_check.py')),str(ROOT),mode],
                           cwd=ROOT,text=True,capture_output=True)
        assert p.returncode==0 and p.stdout.strip()==expected,(mode,p.stdout,p.stderr)
        outputs[mode]=p.stdout.strip()
    return dict(simulated_script_path='/checker.py', explicit_repo_resolved_first=True,
                outputs=outputs, legacy_failure='IndexError before --repo parsing in shallow Linux mutation paths')


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
    phase = phase_controls()
    return dict(status='PASS_NATIVE_SCENE_AF_METRIC_AND_FULL_HEAT_BOUNDARY', input_head=INPUT,
                heat_continuation_input_head=HEAT_INPUT,
                phase_continuation_input_head=PHASE_INPUT,
                original_primary_blob=OLD_PRIMARY_BLOB, original_primary_sha256=OLD_PRIMARY_SHA256,
                scope=SCOPE, checks=checks, metric_exact_controls=sum(checks.values()),
                heat_boundary=heat, phase_curvature_boundary=phase,
                exact_controls=sum(checks.values())+heat['exact_controls']+phase['exact_controls'],
                actual_composition_owner_dimensions=owned_dimensions,
                mathematical_mutations_rejected=hostile_mutations()+hostile_heat_mutations()+hostile_phase_mutations(),
                shallow_path_portability_replays=shallow_path_replays(),
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
    ap.add_argument('--phase-only', action='store_true')
    args = ap.parse_args()
    ROOT = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[3]
    if args.heat_only:
        print('PASS_AF_HEAT_CONTROLS',heat_controls()['exact_controls'])
        return
    if args.phase_only:
        print('PASS_AF_PHASE_CONTROLS',phase_controls()['exact_controls'])
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
