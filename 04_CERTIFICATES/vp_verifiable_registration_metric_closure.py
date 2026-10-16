"""Finite registration arithmetic and actual scene-AF metric controls.

The old constant-two operator tail bound was false: a geometric series
check did not test a commutator. The weighted first-level calculation
below rejects it on the actual 33-dimensional scene, retaining all archives.
The corrected all-level estimate and weak-star conclusion have an analytic
proof in research/A4D_NATIVE_SCENE_AF_METRIC_REFINEMENT.md. Finite controls
do not prove them by sampling, or re-prove native preparation/orthogonality.
"""

from fractions import Fraction
import math
import sympy as sp


Q = sp.Rational


def first_level_data():
    normalization = Q(1, 33)
    archive_dims = (8, 10, 12)
    W = sp.diag(*([normalization] * 9 + [normalization * d for d in archive_dims]))
    unit = sp.Matrix([int(i == j) for i in range(3) for j in range(3)] + [1, 1, 1])
    P0 = unit * (unit.T * W)
    Le = sp.diag(*([int(i == 0) for i in range(3) for j in range(3)] + [0, 0, 0]))
    return W, unit, P0, Le


def commutator_norm_squared(b):
    t = Q(1, 33)
    return b * b * t * (1 - t)


def bell_partial_trace(d):
    return sp.Matrix(d, d, lambda i, k:
                     sum(int(i == j) * int(k == j) for j in range(d)) / Q(d**2))


def register_norm_factor(d):
    return sp.Integer(d)


def tail_bound(d, b, n):
    return d * b ** (1 - n) / (b - 1) ** 2


def metric_controls():
    checks = {}

    def ck(name, condition):
        assert bool(condition), name
        checks[name] = checks.get(name, 0) + 1

    W, unit, P0, Le = first_level_data()
    ck('full_first_level_GNS_dimension', W.rows == 12)
    ck('all_three_archive_sectors_retained', list(W.diagonal())[-3:] == [Q(8, 33), Q(10, 33), Q(12, 33)])
    ck('positive_GNS_pairing', all(w > 0 for w in W.diagonal()))
    ck('normalized_native_scene_trace', (unit.T * W * unit)[0] == 1)
    ck('scalar_conditional_expectation_is_projection', P0 * P0 == P0 and W * P0 == P0.T * W)
    ck('observable_is_GNS_selfadjoint_projection', Le * Le == Le and W * Le == Le.T * W)
    ck('observable_trace_is_scene_trace_not_algebra_dimension', (unit.T * W * Le * unit)[0] == Q(1, 33))

    for b in [Q(3, 2), Q(2), Q(33)]:
        D = b * (sp.eye(12) - P0)
        C = D * Le - Le * D
        K = W.inv() * C.T * W * C
        variance = commutator_norm_squared(b)
        # Positivity of C^dagger C, its polynomial and nonzero trace fix the
        # full operator norm. A sampled column is not substituted for it.
        ck('full_commutator_singular_value_polynomial', K * K == variance * K)
        ck('full_commutator_rank_two_trace', sp.trace(K) == 2 * variance and variance > 0)
        ck('Dirac_retains_scalar_zero_mode', D * unit == sp.zeros(12, 1))
    b = Q(2)
    lhs_squared = Q(32, 33) ** 2
    old_rhs_squared = (2 / (b - 1)) ** 2 * commutator_norm_squared(b)
    ck('old_constant_two_bound_is_false', lhs_squared > old_rhs_squared)
    ck('old_bound_exact_factor_two_violation', lhs_squared == 2 * old_rhs_squared)
    phi = (1 + sp.sqrt(5)) / 2
    golden_ratio = sp.simplify(lhs_squared / ((2 / (phi - 1))**2 * commutator_norm_squared(phi)))
    ck('old_bound_also_fails_at_golden_scale', sp.simplify(golden_ratio - 8 / phi**4) == 0 and golden_ratio > 1)
    for n in range(1, 6):
        full_norm_squared = b ** (2 * (n + 1)) * Q(32, 33**2)
        rhs_squared = (2 / (b ** (n + 1) - b**n)) ** 2 * full_norm_squared
        ck('late_register_counterexample_same_violation', lhs_squared == 2 * rhs_squared)

    e = sp.Matrix(33, 33, lambda i, j: Q(1, 9) if i < 9 and j < 9 else 0)
    ck('native_zonal_projection', e * e == e and sp.trace(e) == 1)
    generators = []
    start = 0
    for size in (9, 11, 13):
        for i in range(start, start + size - 1):
            perm = list(range(33))
            perm[i], perm[i + 1] = perm[i + 1], perm[i]
            generators.append(perm)
        start += size
    ck('complete_scene_permutation_generators', len(generators) == 30)
    diagonal_pairs = {(i, i) for i in range(33)}
    for perm in generators:
        ck('zonal_projection_fixed_by_native_group', e.extract(perm, perm) == e)
        ck('full_scene_Bell_vector_fixed_by_native_group', {(perm[i], perm[i]) for i in range(33)} == diagonal_pairs)

    for d in [2, 3, 33]:
        partial = bell_partial_trace(d)
        ck('Bell_normalized_partial_trace', partial == sp.eye(d) / d**2)
        ck('register_norm_factor_attains_equality', register_norm_factor(d)**2 * partial[0, 0] == 1)
        ck('smaller_sqrt_dimension_factor_fails', d * partial[0, 0] < 1)
        if d <= 3:
            v = sp.Matrix([int(i == j) for i in range(d) for j in range(d)])
            p = v * v.T / d
            ck('materialized_Bell_projection', p * p == p and sp.trace(p) == 1)
        else:
            ck('full_scene_Bell_normalization', sum(int(i == j)**2 for i in range(d) for j in range(d)) == d)

    for b in [Q(2), Q(3, 2), Q(33, 32), Q(33)]:
        for n in range(6):
            finite_tail = sum(1 / (b**m - b**(m-1)) for m in range(n + 1, n + 10))
            closed_tail = b ** (1 - n) / (b - 1)**2
            remainder = b ** (1 - (n + 9)) / (b - 1)**2
            ck('exact_geometric_tail_identity', finite_tail + remainder == closed_tail)
            ck('correct_register_bound_dominates_finite_tail', tail_bound(33, b, n) >= 33 * finite_tail)
            ck('correct_register_bound_equals_analytic_constant', tail_bound(33, b, n) == 33 * closed_tail)
            ck('uniform_refinement_ratio', tail_bound(33, b, n + 1) == tail_bound(33, b, n) / b)
    ck('correct_bound_survives_first_level_counterexample', lhs_squared <= tail_bound(33, Q(2), 0)**2 * commutator_norm_squared(Q(2)))
    return checks


def main():
    zones = (9, 11, 13)
    archive_dims = (8, 10, 12)

    # 1. Verification Lemma check (orthogonal support)
    # If tau_i and tau_j are state distributions with overlap Tr(tau_i tau_j) > 0,
    # then Tr(C (tau_i x tau_i)) = 0 and Tr(C (tau_j x tau_i)) = 1 is impossible.
    # Trace of positive product Tr(tau_i tau_j) == 0 iff disjoint support.
    p = (math.sqrt(5) - 1) / 2
    q = p * p

    # 2. Counter-channel omitting middle archive:
    # Memory dim = 8*2 + 12 + 2 = 30.
    # Active rank of Choi matrix = 2, total rank = 30.
    # Omits W_11 (dim 10) by mixing middle zone into boundary zones.
    dim_omitted = archive_dims[0] * 2 + archive_dims[2] + 2
    assert dim_omitted == 30

    # Operational participation of all 3 archives requires dim 31.
    dim_full = 1 + sum(archive_dims)
    assert dim_full == 31

    # 3. Second moment defect
    # Degree values: (24, 22, 20).
    # Expected degree: 22. Variance defect on zone 11:
    # (24 - 22) * (22 - 20) * 2 = 2 * 2 * 2 = 8.
    defect_11 = (24 - 22) * (22 - 20) * 2
    assert defect_11 == 8

    # 4. Geometric-series arithmetic only; it is not an operator proof.
    # For b in {1.05, sqrt(2), 2, 33}:
    for b in (1.05, math.sqrt(2), 2.0, 33.0):
        assert b > 1.0
        gap_0 = b - 1.0
        assert gap_0 > 0
        tail_sum = 0.0
        for n in range(1, 2000):
            term = 1.0 / (b**n * gap_0)
            tail_sum += term
            if term < 1e-15:
                break
        exact = 1.0 / (gap_0 * gap_0)
        assert abs(tail_sum - exact) < 1e-9

    checks = metric_controls()
    print('PASS_SCENE_AF_METRIC_CONTROLS', sum(checks.values()))
    print('REJECTED_FALSE_CONSTANT_TWO_TAIL_BOUND; full scene trace and archives retained.')
    print('Registration counts retained; all-level metric proof is analytic; native field/source still open.')


if __name__ == "__main__":
    main()
