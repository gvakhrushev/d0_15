#!/usr/bin/env python3
"""Exact finite inputs to warped-quarter nonlinear isolation.

Rebuilds the literal shared-link first-slow compatibility and the quadratic
metric gate on its entire compatible plane. A rational quartic identity
certifies coercivity. The all-frequency compactness proof is in
A4D_WARPED_QUARTER_NONREGULAR_ISOLATION.md, not in this finite calculation.
"""
from fractions import Fraction as F
from itertools import combinations_with_replacement as cr
from pathlib import Path
import argparse
import json
import numpy as np
from a4d_designated_full_gap_check import QI, elimination
from a4d_warped_quarter_regular_response_check import (
    setup, reduced_first_slow, independent_rows, qi_inverse)
from a4d_identity_quarter_nonlinear_response_check import quadratic


def rref_tracked(matrix):
    a = [[F(x) for x in row] for row in matrix]
    n = len(a)
    transform = [[F(i == j) for j in range(n)] for i in range(n)]
    rank = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(rank, n) if a[j][col]), None)
        if pivot is None:
            continue
        a[rank], a[pivot] = a[pivot], a[rank]
        transform[rank], transform[pivot] = transform[pivot], transform[rank]
        value = a[rank][col]
        a[rank] = [x/value for x in a[rank]]
        transform[rank] = [x/value for x in transform[rank]]
        for j in range(n):
            if j != rank and a[j][col]:
                value = a[j][col]
                a[j] = [x-value*y for x, y in zip(a[j], a[rank])]
                transform[j] = [x-value*y for x, y in zip(transform[j], transform[rank])]
        rank += 1
        if rank == n:
            break
    return np.array(a[:rank], dtype=object), np.array(transform[:rank], dtype=object)


def ideal_identity(forms, degree_two, degree_four):
    rows = []
    for form in forms:
        for monomial in degree_two:
            row = [F(0)]*len(degree_four)
            for pair, coefficient in zip(degree_two, form):
                row[degree_four.index(tuple(sorted(monomial+pair)))] += coefficient
            rows.append(row)
    matrix = np.array(rows, dtype=object)
    reduced, transform = rref_tracked(matrix)
    assert np.array_equal(reduced, np.eye(35, dtype=object))
    target = np.zeros(35, dtype=object)
    for i in range(4):
        for j in range(4):
            target[degree_four.index(tuple(sorted((i, i, j, j))))] += 1
    multipliers = target@transform
    assert np.array_equal(multipliers@matrix, target)
    return multipliers.reshape(5, 10), target


def strings(a):
    return [[str(F(x)) for x in row] for row in a]


def run_checks():
    coframe, envelope = reduced_first_slow(setup())
    rows = independent_rows(envelope)
    assert rows == [1, 3, 9, 11]
    compat = coframe-envelope@qi_inverse(envelope[rows])@coframe[rows]
    real = np.array(
        [[x.re for x in row]+[x.im for x in row] for row in compat]
        + [[x.im for x in row]+[-x.re for x in row] for row in compat], dtype=object)
    assert elimination(real.tolist())[0] == 4
    # x=Re(alpha0), y=Re(alpha1), z=-Im(alpha0), t=-Im(alpha1).
    mapping = np.array([
        [1, 0, 0, 0], [0, 1, 0, 0],
        [F(1, 2), F(-1, 2), F(1, 2), F(1, 2)],
        [F(-1, 2), F(1, 2), F(-1, 2), F(-1, 2)],
        [0, 0, 1, 0], [0, 0, 0, 1],
        [F(-1, 2), F(-1, 2), F(1, 2), F(-1, 2)],
        [F(1, 2), F(1, 2), F(-1, 2), F(1, 2)]], dtype=object)
    assert not np.any(real@mapping)
    assert elimination(mapping.tolist())[0] == 4
    gram = mapping.T@mapping
    eye = np.eye(4, dtype=object)
    assert not np.any((gram-eye)@(gram-3*eye))
    print('PASS_LITERAL_FIRSTSLOW_ENTIRE_COMPATIBLE_PLANE_AND_NORM', flush=True)

    monomials = list(cr(range(4), 2))
    diagonal = [quadratic(mapping[:, i])[1] for i in range(4)]
    coefficients = []
    for i, j in monomials:
        coefficients.append(diagonal[i] if i == j else
                            quadratic(mapping[:, i]+mapping[:, j])[1]-diagonal[i]-diagonal[j])
    coefficients = np.array(coefficients, dtype=object).T
    forms, transform = rref_tracked(coefficients)
    expected = np.array([
        [1, 0, 0, 0, 0, 0, 0, -1, 0, 0],
        [0, 1, 0, 0, 0, 0, -3, 0, -1, 0],
        [0, 0, 1, 0, 0, 0, -1, 0, 0, 0],
        [0, 0, 0, 1, 0, 1, -1, 0, 0, 0],
        [0, 0, 0, 0, 1, 0, -6, 0, 0, -1]], dtype=object)
    assert np.array_equal(forms, expected)
    assert np.array_equal(transform@coefficients, forms)
    print('PASS_QUADRATIC_GATE_REBUILT_ON_ALL_FOUR_REAL_COMPATIBLE_COORDINATES', flush=True)

    degree_four = list(cr(range(4), 4))
    multipliers, target = ideal_identity(forms, monomials, degree_four)
    identity_bound = sum(abs(x) for x in multipliers.flat)
    readout_bound = max(sum(abs(x) for x in row) for row in transform)
    assert identity_bound == F(707, 3)
    # |c|^2 <= 3|v|^2, |v|^4 <= identity_bound |v|^2 max|forms(v)|.
    coercivity = 1/(3*identity_bound*readout_bound)
    assert coercivity > 0
    print('PASS_EXACT_QUARTIC_IDEAL_IDENTITY_AND_POSITIVE_COERCIVITY', flush=True)

    # An independent dense evaluation checks phase order, polarization and
    # the output-slot convention, without loading either older ledger.
    dense = np.array([F(2), F(-1), F(3), F(1, 2)], dtype=object)
    _, literal = quadratic(mapping@dense)
    products = np.array([dense[i]*dense[j] for i, j in monomials], dtype=object)
    assert np.array_equal(literal, coefficients@products)
    assert sum((dense[i]**2 for i in range(4)))**2 == sum(
        (multipliers@products)[i]*(forms@products)[i] for i in range(5))
    # A sign mutation of the first quartic coefficient is detected as a
    # polynomial identity failure, not just by this dense evaluation.
    bad = multipliers.copy()
    bad[0, 0] = -bad[0, 0]
    assert bad[0, 0] != multipliers[0, 0]
    wrong = np.zeros(35, dtype=object)
    for row, form in zip(bad, forms):
        for a, ca in zip(monomials, row):
            for b, cb in zip(monomials, form):
                wrong[degree_four.index(tuple(sorted(a+b)))] += ca*cb
    assert not np.array_equal(wrong, target)
    print('PASS_DENSE_LITERAL_CONTROL_AND_SIGN_MUTATION', flush=True)
    return {
        'arithmetic': 'Q and Q(i); exact finite-stencil jets, no floating ranks',
        'scope': 'finite compatibility/coercivity inputs to the separate analytic nonregular-isolation proof',
        'center_convention': 'alpha=a-i*b; c=(a0,a1,a2,a3,b0,b1,b2,b3)',
        'compatible_coordinates': ['Re alpha0', 'Re alpha1', '-Im alpha0', '-Im alpha1'],
        'compatibility_real_rank': 4,
        'compatible_plane_map': strings(mapping),
        'compatible_plane_gram_minpoly': '(G-I)(G-3I)=0',
        'quadratic_monomials': [list(m) for m in monomials],
        'literal_restricted_metric_gate': strings(coefficients),
        'gate_to_five_forms': strings(transform),
        'five_form_coefficients': strings(forms),
        'degree_four_ideal_rank': 35,
        'quartic_identity': '(x^2+y^2+z^2+t^2)^2=sum_i P_i F_i',
        'quadratic_multipliers_P': strings(multipliers),
        'sum_P_coefficient_absolute_values': str(identity_bound),
        'gate_to_forms_max_row_sum': str(readout_bound),
        'coercivity': '||Q2(c)||_infinity >= constant*||c||_2^2 for K alpha(c)=0 at f=1',
        'coercivity_constant': str(coercivity),
        'nonclaims': ['finite certificate alone is not a refinement-uniform theorem',
                      'no numerical curved coframe radius',
                      'no arbitrary four-dimensional metric closure',
                      'no independent-source existence assertion']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    report = run_checks()
    if args.expect:
        assert json.loads(args.expect.read_text()) == report
        print('PASS_PINNED_LEDGER', flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('RESULT: exact warped-quarter compatibility-plane quadratic coercivity.', flush=True)
