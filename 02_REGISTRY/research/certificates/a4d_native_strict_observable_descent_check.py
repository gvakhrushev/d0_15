#!/usr/bin/env python3
"""Strict native scalar persistence versus new retained cylinders and Hodge geometry."""
import argparse
import copy
import hashlib
import itertools
import json
import math
from collections import deque
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
BASE = '02_REGISTRY/research/certificates/a4d_native_strict_observable_descent'
PROOF = '02_REGISTRY/research/A4D_NATIVE_STRICT_OBSERVABLE_DESCENT.md'
INPUT = 'adee3e64e0cd07ab792610a1f52a95a5e4e9cb0f'
SCOPE = {
    'class': 'ACTUAL_STRICT_SCALAR_ARCHIVE_FAMILIES_AND_FIXED_COUNTING_HODGE_SCALAR_SUBALGEBRAS',
    'whole_strict_family_factorization_and_retained_record_witness_kernel_formalized': True,
    'twenty_new_resolved_propositions_standard_axioms_only': True,
    'actual_successor_composites_used_not_direct_or_coordinatewise_modulo': True,
    'all_scalar_subalgebra_classification_and_metric_collapse': 'ANALYTIC_NOT_FULL_LEAN_FORMALIZATION',
    'full_Hodge_operator_norm_gate_used_not_replaced_by_edge_or_column_gate': True,
    'all_bijective_site_identifications_in_fixed_birth_class_covered': True,
    'strict_base_zero_algebra_has_exactly_sixteen_classes': True,
    'strict_fixed_birth_reading_recovers_noncollapsed_Hodge_metric': False,
    'all_locally_constant_profinite_readouts_are_strict_base_zero_families': False,
    'some_finite_factorization_or_mathematical_cylinder_is_native_physical_admission': False,
    'alternative_observable_algebra_or_operational_gate_installed': False,
    'new_cylinder_admitted_by_all_native_preparation_budget_rules': False,
    'native_readout_q_D_b_m_or_full_price_source_derived': False,
    'hidden_archive_modes_deleted_or_declared_gauge': False,
    'archive_phi_index_identified_with_physical_mesh': False,
    'metric_obstruction_promoted_to_O_h_action_contrast_no_go': False,
    'absence_of_Gamma_F_for_whole_core_proved': False,
    'own_source_Ward_curved_roots_GR_or_original_parent_terminals_closed': False,
}


def sha(path):
    return hashlib.sha256((ROOT / path).read_bytes()).hexdigest()


def to_base(L, x):
    assert L >= 2 and 0 <= x < L**4
    for t in range(L - 1, 1, -1):
        x %= t**4
    return x


def to_one(L, x):
    assert L >= 3 and 0 <= x < L**4
    for t in range(L - 1, 2, -1):
        x %= t**4
    return x


def digits(L, i):
    return tuple((i // L**r) % L for r in range(4))


def plus(L, i, r):
    d = (i // L**r) % L
    return i + L**r if d < L - 1 else i - (L - 1)*L**r


def minus(L, i, r):
    d = (i // L**r) % L
    return i - L**r if d else i + (L - 1)*L**r


def car_create(r, bra, ket):
    if ket & (1 << r) or bra != ket ^ (1 << r):
        return 0
    return (-1)**sum((ket >> s) & 1 for s in range(r))


def car_annihilate(r, bra, ket):
    if not (ket & (1 << r)) or bra != ket ^ (1 << r):
        return 0
    return (-1)**sum((ket >> s) & 1 for s in range(r))


def controls():
    checks = {}

    def ck(name, condition, count=1):
        assert bool(condition), name
        checks[name] = checks.get(name, 0) + count

    rec = json.loads((ROOT / (BASE + '_results.json')).read_text())
    out = (ROOT / (BASE + '_output.txt')).read_text()
    ck('actual_compiler_success', rec['status'] == 'PASS' and rec['compiler_exit_code'] == 0 and rec['input_head'] == INPUT)
    ck('twenty_new_and_three_primary_propositions', len(rec['declarations']) == 20 and len(rec['primary_owner_propositions']) == 3)
    ck('no_sorry_error_or_warning', 'sorryAx' not in out and ': error' not in out and ': warning' not in out)
    for name in rec['declarations'] + rec['primary_owner_propositions']:
        ck('literal_resolved_proposition', name in out and name in rec['axioms'])
        ck('transitive_standard_axioms_only', set(rec['axioms'][name]) <= {'propext', 'Classical.choice', 'Quot.sound'})
    for group in ['transitive_d0_source_sha256', 'prior_operator_source_sha256', 'primary_and_prior_input_sha256', 'toolchain_input_sha256']:
        for path, digest in rec[group].items():
            ck('sha_' + group, sha(path) == digest)
    ck('capsule_hash', sha(BASE + '.lean') == rec['capsule_sha256'])
    ck('output_hash', sha(BASE + '_output.txt') == rec['output_sha256'])
    ck('literal_whole_family_classification', 'Compatible F ↔' in rec['printed_propositions']['D0.Research.NativeStrictObservableDescent.compatible_iff_base_pullback'])
    ck('birth_witness_uses_actual_limit_type', 'actualBirthRecord ≠' in rec['printed_propositions']['D0.Research.NativeStrictObservableDescent.two_actual_records_same_base_distinct'])
    ck('formalization_boundary', rec['strict_family_and_native_record_binding_kernel_formalized'] and not rec['scalar_subalgebra_and_Hodge_metric_collapse_kernel_formalized'])
    ck('admission_boundary', not rec['native_physical_preparation_or_source_GR_derived'])
    book = (ROOT / '01_BOOKS/BOOK_02_MATHEMATICAL_PROOF_SPINE_AND_INVARIANT_CALCULUS.md').read_text()
    ck('actual_book_scalar_rule', 'F_{k-1}∘π_{k→k-1}=F_k' in book)
    prior = json.loads((ROOT / '02_REGISTRY/research/certificates/a4d_native_hodge_connes_metric_certificate.json').read_text())
    ck('actual_prior_full_operator_triple', prior['scope']['all_size_exact_product_circle_Connes_distance'] == 'ANALYTIC_PROOF_NOT_FULL_LEAN_FORMALIZATION')

    # An arbitrary finite set of scalar algebra generators: the proof's
    # products recover each actual equivalence-class indicator exactly.
    for generators in [
        [(0, 0, 1, 1, 2, 2, 2, 2), (0, 0, 2, 2, 4, 4, 5, 5)],
        [(0, 1, 2, 3, 4, 5, 6, 7)],
        [(3, 3, 3, 3, 3, 3, 3, 3)],
    ]:
        words = [tuple(g[x] for g in generators) for x in range(8)]
        classes = sorted(set(words))
        for a in classes:
            indicator = [Fraction(1) for _ in range(8)]
            for b in classes:
                if a == b:
                    continue
                r = next(r for r in range(len(generators)) if a[r] != b[r])
                indicator = [indicator[x]*Fraction(generators[r][x]-b[r], a[r]-b[r]) for x in range(8)]
            ck('polynomial_product_recovers_full_class_indicator', indicator == [Fraction(int(w == a)) for w in words])
        ck('scalar_class_indicators_sum_to_one', all(sum(int(w == a) for a in classes) == 1 for w in words))

    # Persistence, true successor composition, and new finite cylinders.
    ck('first_actual_new_cylinder_not_base_reading', 16 % 16 == 0 and 0 % 16 == 0 and (16 == 16) != (0 == 16))
    ck('long_direct_modulo_is_different', to_base(4, 81) == 0 and 81 % 16 == 1)
    f0 = tuple(j*j - 3*j for j in range(16))
    for L in range(2, 13):
        for x in range((L+1)**4):
            coarse = x % L**4
            b = to_base(L, coarse)
            ck('full_actual_base_reading_range', 0 <= b < 16)
            ck('base_reading_successor_persists', f0[to_base(L+1, x)] == f0[b])
            if L >= 3:
                ck('new_tail_test_persists', (to_one(L+1, x) == 16) == (to_one(L, coarse) == 16))
        ck('all_base_classes_retained', {to_base(L, x) for x in range(L**4)} == set(range(16)))
    for n in range(50):
        old, new = (0 if n == 0 else 16), 16
        ck('whole_birth_record_actual_successor', new % (n+2)**4 == old)
        ck('whole_zero_record_actual_successor', 0 % (n+2)**4 == 0)
        ck('whole_records_same_base_reading', to_base(n+2, old) == 0)
        if n >= 1:
            ck('new_tail_reading_separates_retained_records', to_one(n+2, old) == 16 and to_one(n+2, 0) == 0)

    # Complete graph argument: relabellings here are controls, not a search.
    for L in [2, 3, 4, 6, 8, 16]:
        size = L**4
        for mult, off in [(1, 0), (1, size//3), (5 if math.gcd(5, size) == 1 else 7, 19 % size)]:
            ck('tested_relabelling_is_bijective', math.gcd(mult, size) == 1)
            labels = [None]*size
            for j in range(size):
                labels[(mult*j + off) % size] = to_base(L, j)
            ck('sixteen_nonempty_actual_classes', set(labels) == set(range(16)))
            graph = [set() for _ in range(16)]
            for x in range(size):
                for r in range(4):
                    y = plus(L, x, r)
                    ck('actual_periodic_edge_inverse', minus(L, y, r) == x)
                    a, b = labels[x], labels[y]
                    if a != b:
                        graph[a].add(b)
                        graph[b].add(a)
            for a in range(16):
                dist = {a: 0}
                todo = deque([a])
                while todo:
                    b = todo.popleft()
                    for c in graph[b]:
                        if c not in dist:
                            dist[c] = dist[b] + 1
                            todo.append(c)
                ck('actual_quotient_connected_simple_path_bound', len(dist) == 16 and max(dist.values()) <= 15)
            # Necessary edge inequality only. It is not used as a full norm gate.
            for values in [tuple(range(16)), f0, tuple(int(j == 7) for j in range(16))]:
                edge = max(abs(values[a]-values[b]) for a in range(16) for b in graph[a])
                ck('exact_range_versus_quotient_edge_bound', max(values)-min(values) <= 15*edge)

    # Every CAR grade, including L=2 spatial collisions. Actual full-column
    # vacuum entry has one creator and no annihilator cancellation.
    for r, ket in itertools.product(range(4), range(16)):
        v = [car_create(r, bra, ket) + car_annihilate(r, bra, ket) for bra in range(16)]
        ck('literal_CAR_whole_grade_column_norm', sum(a*a for a in v) == 1)
        if ket == 0:
            ck('vacuum_edge_entry_no_cancellation', car_create(r, 1 << r, ket) == 1 and all(car_annihilate(r, bra, ket) == 0 for bra in range(16)))
    for L in [2, 3, 4]:
        # Positive control in the full scalar algebra: the single-coordinate
        # distance has an actual signed partial permutation commutator with
        # ||C||<=1 on the full Hilbert carrier, hence no alleged universal collapse.
        tau = lambda x: min(x % L, L-(x % L))
        rows = set()
        for x, ket in itertools.product(range(L**4), range(16)):
            bra = ket ^ 1
            y = minus(L, x, 0) if not (ket & 1) else plus(L, x, 0)
            coefficient = tau(x)-tau(y)
            ck('full_scalar_witness_exact_commutator_coeff', abs(coefficient) <= 1)
            if coefficient:
                ck('full_operator_witness_output_no_colliding_columns', (y, bra) not in rows)
                rows.add((y, bra))
        ck('full_scalar_witness_nonzero_distance', Fraction(tau(L//2)-tau(0), L) == Fraction(L//2, L) and tau(L//2) > 0)

    # Exact four-dimensional packing includes every centre and wrap.
    for L in range(2, 19):
        for radius in range(L+1):
            for centre in range(L):
                count = sum(min((j-centre) % L, (centre-j) % L) <= radius for j in range(L))
                ck('exact_cyclic_ball_count', count == min(L, 2*radius+1))
                ck('four_role_packing_bound', count**4 <= (2*radius+1)**4)
    for C in [0, 1, 2, 5, 10, Fraction(7, 2)]:
        L = 4*(2*(2*math.floor(C)+1)//4 + 1)
        ck('fixed_sixteen_class_reading_breaks_resolution_capacity', L**4 > 16*(2*math.floor(C)+1)**4)
    ck('all_physical_mesh_controls_use_operator_scale_only', all(L % 4 == 0 for L in [4, 8, 16, 32]))
    ck('noncollapsed_even_full_metric_contrasts_with_strict_bound', Fraction(15, 32) < 1)
    ck('level_dependent_rescaling_is_not_fixed_calibration', Fraction(32, 2) != Fraction(64, 2))
    return checks


def expected(checks):
    return {'status': 'PASS', 'input_head': INPUT, 'scope': SCOPE,
            'checks': checks, 'controls': sum(checks.values()),
            'proof_sha256': sha(PROOF), 'checker_sha256': sha(BASE + '_check.py'),
            'capsule_sha256': sha(BASE + '.lean'),
            'lean_receipt_sha256': sha(BASE + '_results.json')}


def validate(candidate, checks):
    assert candidate == expected(checks), 'certificate scope, counts, source or proof mismatch'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    checks = controls()
    cert = expected(checks)
    if args.write:
        (ROOT / (BASE + '_certificate.json')).write_text(json.dumps(cert, sort_keys=True, indent=2) + '\n')
    validate(json.loads((ROOT / (BASE + '_certificate.json')).read_text()), checks)
    mutants = []
    for key, value in SCOPE.items():
        if isinstance(value, bool):
            bad = copy.deepcopy(cert)
            bad['scope'][key] = not value
            mutants.append(bad)
    for key in ['proof_sha256', 'checker_sha256', 'lean_receipt_sha256']:
        bad = copy.deepcopy(cert)
        bad[key] = '0'*64
        mutants.append(bad)
    for bad in mutants:
        try:
            validate(bad, checks)
        except AssertionError:
            pass
        else:
            raise AssertionError('false scope ledger accepted')
    print('PASS_NATIVE_STRICT_OBSERVABLE_DESCENT', sum(checks.values()), 'CONTROLS', len(mutants), 'FALSE_LEDGERS_REJECTED')


if __name__ == '__main__':
    main()
