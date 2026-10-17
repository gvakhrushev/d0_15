#!/usr/bin/env python3
"""Exact scene, retained AF and moment controls; scalar universal gap is Lean."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

import sympy as s

STEM = '02_REGISTRY/research/certificates/a4d_native_af_scene_heat_comparison'
PROOF = '02_REGISTRY/research/A4D_NATIVE_AF_SCENE_HEAT_COMPARISON.md'
INPUT = '833372049d1cbde14f51bcbc3ca06bb017025cb8'
SCOPE = {
    'actual_combinatorial_scene_graph_and_all_projectors_checked': True,
    'degree_normalized_scene_operator_included_in_obstruction': False,
    'uniform_all_level_all_scale_intertwining_gap': True,
    'actual_AF_89_dimensional_sharpness_witness': True,
    'actual_AF_233_dimensional_exact_weak_compression': True,
    'every_AF_mode_retained_in_both_witnesses': True,
    'dimension_inequality_excludes_rectangular_compression': False,
    'weak_Laplacian_compression_implies_heat_compression': False,
    'exact_heat_semigroup_compression_on_literal_ladder_exists': False,
    'literal_martingale_scale_derived_as_native_heat_law': False,
    'comparison_basis_and_scale_declared_native_preparation': False,
    'operator_norm_gap_is_physical_action_contrast_gap': False,
    'arbitrary_AF_scales_or_normalized_scene_excluded': False,
    'operator_norm_and_heat_semigroup_proofs_new_Lean_theorems': False,
    'native_F_source_Ward_or_GR_closed': False,
    'T0_T3_or_original_310_202_317_terminals_closed': False,
    'heat_gap_excludes_Feshbach_elimination_with_memory': False,
    'fixed_spectrum_coupled_block_heat_derivative_is_zero': True,
    'coupled_spectral_block_is_derived_native_F': False,
}
ROOT = None
Q = None


def load_field(root):
    global Q
    path = root / '02_REGISTRY/research/certificates/a4d_native_golden_cost_refinement_check.py'
    spec = importlib.util.spec_from_file_location('golden_field_for_scene_comparison', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    Q = module.Q


def inverse(x):
    x = Q.co(x)
    norm = x.a*x.a - x.a*x.b - x.b*x.b
    assert norm != 0
    return Q((x.a-x.b)/norm, -x.b/norm)


def sign(x):
    """Sign of a+b*p, using p=(sqrt(5)-1)/2 and rational comparisons."""
    x = Q.co(x)
    a, b = 2*x.a-x.b, x.b
    if b == 0:
        return (a > 0)-(a < 0)
    if a == 0:
        return (b > 0)-(b < 0)
    if a > 0 and b > 0:
        return 1
    if a < 0 and b < 0:
        return -1
    gap = a*a-5*b*b
    return ((gap > 0)-(gap < 0))*(1 if a > 0 else -1)


def mathematics():
    checks = Counter()

    def ck(name, condition):
        assert bool(condition), name
        checks[name] += 1

    p = Q(0, 1)
    phi = 1+p
    b = phi**2
    ck('literal_heat_ratio', b == 2+p and sign(b-F(64, 25)) > 0)
    for x in [p, phi, b, 13*(b-1), b**4]:
        ck('exact_field_inverse', x*inverse(x) == 1)
    for x, expected in [(Q(0), 0), (p, 1), (-p, -1), (p-1, -1),
                        (3-5*p, -1), (phi-1, 1), (5-8*p, 1)]:
        ck('exact_field_order', sign(x) == expected)

    zones = [0]*9+[1]*11+[2]*13
    adjacency = s.Matrix(33, 33, lambda i, j: int(zones[i] != zones[j]))
    degree = [sum(adjacency.row(i)) for i in range(33)]
    ck('actual_scene_adjacency', adjacency == adjacency.T and sum(adjacency) == 718)
    ck('actual_scene_degrees', degree == [24]*9+[22]*11+[20]*13)
    laplacian = s.diag(*degree)-adjacency
    zero = s.zeros(33)
    identity = s.eye(33)
    p0 = s.ones(33)/33
    pzone = s.diag(s.ones(9)/9, s.ones(11)/11, s.ones(13)/13)
    projectors = {
        0: p0,
        20: s.diag(s.zeros(20), s.eye(13)-s.ones(13)/13),
        22: s.diag(s.zeros(9), s.eye(11)-s.ones(11)/11, s.zeros(13)),
        24: s.diag(s.eye(9)-s.ones(9)/9, s.zeros(24)),
        33: pzone-p0,
    }
    ranks = {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}
    ck('actual_scene_resolution', sum(projectors.values(), zero) == identity)
    ck('actual_scene_spectral_reconstruction',
       sum((a*P for a, P in projectors.items()), zero) == laplacian)
    for a, P in projectors.items():
        ck('actual_scene_selfadjoint_projectors', P.T == P and P*P == P)
        ck('actual_scene_projector_ranks', s.trace(P) == ranks[a])
        ck('actual_scene_eigenspaces', laplacian*P == a*P)
        for aa, PP in projectors.items():
            if a != aa:
                ck('actual_scene_orthogonality', P*PP == zero)
    vectors = {
        20: s.Matrix([int(i == 20)-int(i == 21) for i in range(33)]),
        22: s.Matrix([int(i == 9)-int(i == 10) for i in range(33)]),
        24: s.Matrix([int(i == 0)-int(i == 1) for i in range(33)]),
        33: s.Matrix([11]*9+[-9]*11+[0]*13),
    }
    for a, v in vectors.items():
        ck('literal_scene_eigenvectors', v != s.zeros(33, 1) and laplacian*v == a*v)

    # These rational strict inequalities are used by the all-index Lean proof.
    # No bounded scan is represented as a proof over all levels or scales.
    for ratio in [F(57, 27), F(53, 31), F(79, 31), F(57, 53)]:
        ck('three_band_ratio_separation', ratio < F(64, 25))
    ck('first_third_open_bands_disjoint', F(20)+F(13, 2) == F(33)-F(13, 2))
    ck('zero_outside_three_bands', all(a > F(13, 2) for a in [20, 22, 33]))

    counts = [(1, 1)]
    for _ in range(5):
        a, aa = counts[-1]
        counts.append((a+aa, a))
    dimensions = [a*a+aa*aa for a, aa in counts]
    increments = [dimensions[j]-dimensions[j-1] for j in range(1, 6)]
    ck('actual_AF_dimensions', dimensions == [2, 5, 13, 34, 89, 233])
    ck('actual_AF_increments', increments == [3, 8, 21, 55, 144])

    def full_spectrum(level, scale):
        levels = [Q(0)]*2
        for j in range(1, level+1):
            levels += [scale*b**j]*increments[j-1]
        ck('all_AF_modes_retained', len(levels) == dimensions[level])
        ck('all_AF_levels_retained',
           sum(increments[:level])+2 == dimensions[level] and sign(scale) > 0)
        return levels

    sharp_energy = F(53, 2)
    sharp = full_spectrum(4, Q(sharp_energy)*inverse(b**4))
    ck('sharp_full_89_model', len(sharp) == 89 and sharp[:2] == [Q(0), Q(0)])
    ck('sharp_increment_55', all(x == sharp_energy for x in sharp[34:]) and len(sharp[34:]) == 55)
    ck('sharp_embed_all_scene_modes', sum(ranks.values()) == 33 and 32 <= 55)
    # Constant maps to one zero vector; all 32 remaining vectors to the last
    # increment. The other 56 AF directions remain in the full spectrum.
    ck('sharp_unused_directions_retained', len(sharp)-33 == 56)
    sharp_error = max(abs(sharp_energy-a) for a in [20, 22, 24, 33])
    ck('sharp_uniform_bound', sharp_error == F(13, 2))

    lo, hi = Q(13), 13*b
    weak = full_spectrum(5, lo*inverse(b**4))
    ck('weak_full_233_model', len(weak) == 233)
    ck('weak_two_existing_increments',
       all(x == lo for x in weak[34:89]) and all(x == hi for x in weak[89:]))
    ck('weak_embedding_dimension', 32 <= increments[3] and 32 <= increments[4])
    ck('weak_unused_coordinates_retained', len(weak)-65 == 168)
    ck('weak_orthogonal_complement_retained', len(weak)-33 == 200)
    first = {}
    second_defects = {}
    for a in [20, 22, 24, 33]:
        w = (a-lo)*inverse(hi-lo)
        ck('mixing_positive_weights', sign(w) > 0 and sign(1-w) > 0)
        ck('mixing_Gram_isometry', (1-w)+w == 1)
        moment = (1-w)*lo+w*hi
        defect = (1-w)*lo**2+w*hi**2-a*a
        ck('mixing_exact_first_moment', moment == a)
        ck('mixing_exact_second_defect', defect == (a-lo)*(hi-a))
        ck('mixing_strict_second_defect', sign(defect) > 0)
        first[a], second_defects[a] = moment, defect
        d = lo+hi-a
        k2 = (a-lo)*(hi-a)
        ck('coupled_block_fixed_spectrum', a+d == lo+hi and a*d-k2 == lo*hi)
        ck('nonzero_retained_Feshbach_memory', sign(k2) > 0 and sign(d) > 0)
        # Negative spectral parameter -1 is away from both positive poles
        # and from the positive archive block, so all inverses exist.
        schur = inverse(a+1-k2*inverse(d+1))
        ck('coupled_block_exact_compressed_resolvent', schur == (d+1)*inverse((lo+1)*(hi+1)))
    # Projector reconstruction verifies the full scene first moment. The
    # square-root embedding itself is analytic, not rational matrix entries.
    ck('weak_full_scene_first_moment',
       sum((s.Rational(first[a].a)*projectors[a] for a in first), zero) == laplacian
       and all(x.b == 0 for x in first.values()))
    ck('weak_defect_rank_32_and_constant_zero',
       sum(ranks[a] for a in second_defects) == 32 and projectors[0]*laplacian == zero)

    # Generic coupled two-mode identities over polynomial/rational functions.
    # They apply to the full self-adjoint spectral fiber; a phase of the
    # complex off-diagonal coefficient is not set to zero as a physical law.
    al, ell, upper, spectral = s.symbols('a l u spectral')
    archive = ell+upper-al
    coupling_squared = (al-ell)*(upper-al)
    ck('generic_coupled_trace', s.expand(al+archive-ell-upper) == 0)
    ck('generic_coupled_characteristic',
       s.expand((al-spectral)*(archive-spectral)-coupling_squared-(ell-spectral)*(upper-spectral)) == 0)
    ck('generic_Feshbach_identity', s.cancel(
        1/(al-spectral-coupling_squared/(archive-spectral))
        -(archive-spectral)/((ell-spectral)*(upper-spectral))) == 0)
    ck('generic_archive_tangent', s.diff(archive, al) == -1)
    ck('generic_coupling_tangent', s.expand(s.diff(coupling_squared, al)-(ell+upper-2*al)) == 0)
    ck('memory_changes_on_fixed_spectral_fiber',
       s.cancel(s.diff(coupling_squared/archive, al)-(1-ell*upper/archive**2)) == 0
       and s.diff(coupling_squared/archive, al) != 0)

    # An independent rational 2x2 example executes the second-derivative
    # failure and the exact residual Gram identity without square roots.
    H = s.diag(1, 4)
    J = s.Matrix([s.Rational(3, 5), s.Rational(4, 5)])
    L = s.Matrix([[s.Rational(73, 25)]])
    ck('rational_hostile_first_moment', J.T*J == s.eye(1) and J.T*H*J == L)
    residual = H*J-J*L
    variance = J.T*H*H*J-L*L
    ck('rational_residual_Gram_identity', residual.T*residual == variance)
    ck('rational_heat_second_derivative_fails', variance[0] == s.Rational(1296, 625) > 0)
    return dict(sorted(checks.items()))


MUTATIONS = {
    'omit_scene_edges': ("int(zones[i] != zones[j])", "int(zones[i] < zones[j])", 'actual_scene_adjacency'),
    'wrong_scene_degree': ("[24]*9+[22]*11+[20]*13", "[24]*9+[20]*11+[22]*13", 'actual_scene_degrees'),
    'unsquared_Dirac_used_as_heat': ("b = phi**2", "b = phi", 'literal_heat_ratio'),
    'discard_unused_AF_increment': ("[scale*b**j]*increments[j-1]", "[scale*b**j]*min(32, increments[j-1])", 'all_AF_modes_retained'),
    'overstate_uniform_bound': ("sharp_error == F(13, 2)", "sharp_error >= F(7)", 'sharp_uniform_bound'),
    'wrong_mixing_weight': ("w = (a-lo)*inverse(hi-lo)", "w = F(1, 2)*(a-lo)*inverse(hi-lo)", 'mixing_exact_first_moment'),
    'erase_second_moment_defect': ("defect = (1-w)*lo**2+w*hi**2-a*a", "defect = Q(0)", 'mixing_exact_second_defect'),
    'independently_freeze_archive_block': ("d = lo+hi-a", "d = hi", 'coupled_block_fixed_spectrum'),
    'omit_Feshbach_memory': ("schur = inverse(a+1-k2*inverse(d+1))", "schur = inverse(a+1)", 'coupled_block_exact_compressed_resolvent'),
}


def validate(ledger):
    assert ledger['input_head'] == INPUT
    assert ledger['scope'] == SCOPE
    assert all(hashlib.sha256((ROOT/p).read_bytes()).hexdigest() == h
               for p, h in ledger['inputs'].items())
    receipt = json.loads((ROOT/(STEM+'_results.json')).read_text())
    assert receipt['input_head'] == INPUT and receipt['returncode'] == 0
    assert receipt['new_declarations'] == 11
    assert receipt['axiom_union'] == ['Classical.choice', 'Quot.sound', 'propext']
    capsule = (ROOT/(STEM+'.lean')).read_text()
    names = re.findall(r'^#check (D0\.Research\.AFSceneHeatComparison\.\w+)$', capsule, re.M)
    assert len(names) == len(set(names)) == 11 and names == receipt['declarations']
    output = (ROOT/(STEM+'_output.txt')).read_text()
    assert not any(x in output for x in ['error:', 'warning:', 'sorryAx'])
    assert hashlib.sha256(capsule.encode()).hexdigest() == receipt['capsule_sha256']
    assert hashlib.sha256(output.encode()).hexdigest() == receipt['output_sha256']
    reports = dict(re.findall(r"'([^']+)' depends on axioms: \[(.*?)\]", output, re.S))
    assert set(reports) == set(names)
    assert sorted({a.strip() for v in reports.values() for a in v.split(',')}) == receipt['axiom_union']
    for path, digest in receipt['transitive_d0_source_sha256'].items():
        assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest


def main():
    global ROOT
    ap = argparse.ArgumentParser()
    ap.add_argument('--repo', type=Path)
    ap.add_argument('--math-only', action='store_true')
    ap.add_argument('--write-certificate', action='store_true')
    args = ap.parse_args()
    ROOT = args.repo.resolve() if args.repo else Path(__file__).resolve().parents[3]
    load_field(ROOT)
    if args.math_only:
        print(json.dumps(mathematics(), sort_keys=True))
        return
    path = ROOT/(STEM+'_certificate.json')
    if args.write_certificate:
        assert not path.exists(), 'refuse to overwrite existing expectations'
        receipt = json.loads((ROOT/(STEM+'_results.json')).read_text())
        pins = set(receipt['transitive_d0_source_sha256']) | {
            PROOF, STEM+'.lean', STEM+'_check.py', STEM+'_output.txt', STEM+'_results.json',
            '03_FORMALIZATION/lean-toolchain', '03_FORMALIZATION/lake-manifest.json',
            '03_FORMALIZATION/D0/VNext2/SceneSpectralFingerprint.lean',
            '03_FORMALIZATION/D0/Synthesis/SceneHeatKernel.lean',
            '03_FORMALIZATION/D0/VNext/CanonicalMartingaleDiracScale.lean',
            '03_FORMALIZATION/D0/VNext/AFMartingaleDiracScaleNoGo.lean',
            '03_FORMALIZATION/D0/VNext/AFD0LaplacianComparisonNoGo.lean',
            '03_FORMALIZATION/D0/VNext/AFD0SpectralInvariantComparison.lean',
            '03_FORMALIZATION/D0/Spectral/CanonicalRefinementScaleFlow.lean',
            '03_FORMALIZATION/D0/Spectral/DarkArchiveStructure.lean',
            '03_FORMALIZATION/D0/VNext/FibonacciAFAlgebra.lean',
            '04_CERTIFICATES/vp_vnext_af_feshbach_compatibility.py',
            '04_CERTIFICATES/vp_vnext_dirac_laplacian_compatibility.py',
            '02_REGISTRY/research/A4D_NATIVE_GOLDEN_COST_REFINEMENT.md',
            '02_REGISTRY/research/A4D_NATIVE_AF_TRACE_PREPARATION.md',
        }
        for stem in ['a4d_native_golden_cost_refinement', 'a4d_native_af_trace_preparation']:
            pins.update(str(p.relative_to(ROOT)) for p in
                        (ROOT/'02_REGISTRY/research/certificates').glob(stem+'*') if p.is_file())
        ledger = dict(input_head=INPUT, scope=SCOPE,
                      inputs={p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in sorted(pins)},
                      checks=mathematics(), math_mutants=list(MUTATIONS))
        path.write_text(json.dumps(ledger, indent=2)+'\n')
    ledger = json.loads(path.read_text())
    validate(ledger)
    checks = mathematics()
    assert checks == ledger['checks'] and ledger['math_mutants'] == list(MUTATIONS)
    text = Path(__file__).read_text()
    prefix, suffix = text.split('\nMUTATIONS =', 1)
    for name, (old, new, expected) in MUTATIONS.items():
        assert prefix.count(old) == 1, (name, prefix.count(old))
        with tempfile.TemporaryDirectory(prefix='d0-af-scene-') as folder:
            temp = Path(folder)/'mutant.py'
            temp.write_text(prefix.replace(old, new)+'\nMUTATIONS ='+suffix)
            r = subprocess.run([sys.executable, str(temp), '--repo', str(ROOT), '--math-only'],
                               text=True, capture_output=True, timeout=120)
            assert r.returncode != 0 and 'AssertionError' in r.stderr and expected in r.stderr, (name, r.stderr[-700:])
    rejected = 0
    for key, value in SCOPE.items():
        bad = json.loads(json.dumps(ledger))
        bad['scope'][key] = not value
        try:
            validate(bad)
        except AssertionError:
            rejected += 1
        else:
            raise AssertionError(('false_scope_accepted', key))
    print(json.dumps(dict(verdict='PASS_LITERAL_AF_SCENE_COMPRESSION_AND_HEAT_GAP',
                          exact_controls=sum(checks.values()), groups=len(checks),
                          executed_math_mutants_rejected=len(MUTATIONS),
                          false_scope_ledgers_rejected=rejected, new_Lean_propositions=11,
                          native_F_T0_T3_or_GR_closed=False), sort_keys=True))


if __name__ == '__main__':
    main()
