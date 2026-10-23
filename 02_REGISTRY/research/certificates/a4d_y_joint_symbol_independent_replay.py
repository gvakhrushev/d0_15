#!/usr/bin/env python3
"""Exact independent replay of the finite-amplitude Y Laurent stencil.

Corrects the attached replay's metric-row covariance offset. Uses rational
coefficient identities and good-prime minor witnesses; no SymPy dependency.
This certifies finite facts, not H_TORUS or nonlinear curved continuation.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import hashlib
import json
import numpy as np
import a4d_y_curved_joint_rational_stencil as S

PRIME = 65521
INPUT_HEAD = 'de71bf30e9cfd34614fc8178255d456c49ebb8b1'
ATTACHED_INPUT_HEAD = '43f2a33096a85c5576fd7fcafa1cf0f09703cfee'


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print('PASS_'+name, flush=True)


def is_prime(p):
    return p >= 2 and all(p % q for q in range(2, int(p**.5)+1))


def mod_fraction(x):
    x = F(x)
    return (x.numerator*pow(x.denominator, -1, PRIME)) % PRIME


def joint_mod(phases):
    matrix = np.zeros((136, 96), dtype=np.int64)
    for offset, terms in ((0, S.ATERMS), (96, S.QTERMS)):
        for shift, entries in terms.items():
            phase = 1
            for z, n in zip(phases, shift):
                phase = phase*pow(int(z), n, PRIME) % PRIME
            for (r, c), value in entries.items():
                matrix[offset+r, c] = (int(matrix[offset+r, c])+phase*mod_fraction(value)) % PRIME
    return matrix


def rank_minor(matrix):
    a = matrix.copy()
    row_ids = list(range(len(a)))
    rows, cols = [], []
    rank = 0
    determinant = 1
    for col in range(a.shape[1]):
        candidates = np.flatnonzero(a[rank:, col])
        if not len(candidates):
            continue
        pivot = rank+int(candidates[0])
        if pivot != rank:
            a[[rank, pivot]] = a[[pivot, rank]]
            row_ids[rank], row_ids[pivot] = row_ids[pivot], row_ids[rank]
            determinant = -determinant
        value = int(a[rank, col])
        determinant = determinant*value % PRIME
        rows.append(row_ids[rank])
        cols.append(col)
        a[rank, col:] = a[rank, col:]*pow(value, -1, PRIME) % PRIME
        factors = a[rank+1:, col].copy()
        a[rank+1:, col:] = (a[rank+1:, col:]-factors[:, None]*a[rank, col:]) % PRIME
        rank += 1
        if rank == min(a.shape):
            break
    # A square minor is checked independently, including row permutation.
    if rows:
        minor = matrix[np.ix_(rows, cols)].copy()
        d = 1
        for col in range(rank):
            candidates = np.flatnonzero(minor[col:, col])
            assert len(candidates)
            pivot = col+int(candidates[0])
            if pivot != col:
                minor[[col, pivot]] = minor[[pivot, col]]
                d = -d
            value = int(minor[col, col])
            d = d*value % PRIME
            if col+1 < rank:
                factors = minor[col+1:, col]*pow(value, -1, PRIME) % PRIME
                minor[col+1:, col:] = (minor[col+1:, col:]-factors[:, None]*minor[col, col:]) % PRIME
        assert d % PRIME
    else:
        d = 1
    return rank, rows, cols, int(d % PRIME)


def covariance_failures(terms, metric, wrong_metric_offset=False):
    failures = []
    for shift, entries in terms.items():
        for (r, c), value in entries.items():
            if not value:
                continue
            phase = S.LABELS[r][0] if not metric or wrong_metric_offset else r//10
            if (sum(shift)+phase-S.LABELS[c][0]) % 4:
                failures.append((shift, r, c, str(value)))
    return failures


def exact_common_action(vector, metric_terms=None):
    result = [F(0)]*136
    for offset, terms in ((0, S.ATERMS), (96, S.QTERMS if metric_terms is None else metric_terms)):
        for entries in terms.values():
            for (r, c), value in entries.items():
                result[offset+r] += value*vector[c]
    return result


def run_checks():
    check('GOOD_PRIME', is_prime(PRIME))
    check('EXACT_STENCIL_COUNTS',
          len(S.ATERMS) == 21 and sum(map(len, S.ATERMS.values())) == 1944
          and len(S.QTERMS) == 5 and sum(map(len, S.QTERMS.values())) == 1044)
    check('CONNECTION_RECIPROCITY', all(
        S.ATERMS.get(tuple(-x for x in shift), {}).get((c, r), F(0)) == value
        for shift, entries in S.ATERMS.items() for (r, c), value in entries.items()))
    check('CONNECTION_FOURTH_ROOT_COVARIANCE', not covariance_failures(S.ATERMS, False))
    check('METRIC_FOURTH_ROOT_COVARIANCE_WITH_CORRECT_OFFSET', not covariance_failures(S.QTERMS, True))
    wrong = covariance_failures(S.QTERMS, True, wrong_metric_offset=True)
    check('ATTACHED_INDEXING_BUG_DETECTED', len(wrong) == 783)

    vector = [F(0)]*96
    for generator, value in ((3, 1), (4, -1), (5, 1)):
        vector[S.LABELS.index((0, 0, generator))] = F(value)
        vector[S.LABELS.index((2, 0, generator))] = F(-value)
    check('Y_KERNEL_EXACT_OVER_Q', not any(exact_common_action(vector)))
    check('Y_KERNEL_NONZERO', any(vector))
    square_root = next(pow(a, (PRIME-1)//4, PRIME) for a in range(2, 100)
                       if pow(pow(a, (PRIME-1)//4, PRIME), 2, PRIME) == PRIME-1)
    folds = {}
    for name, rho in [('1', 1), ('-1', PRIME-1), ('i', square_root), ('-i', PRIME-square_root)]:
        matrix = joint_mod([rho]*4)
        rank, rows, cols, determinant = rank_minor(matrix)
        transformed = np.array([mod_fraction(x)*pow(rho, -S.LABELS[j][0], PRIME) % PRIME
                                for j, x in enumerate(vector)], dtype=np.int64)
        check('FOLDED_COVARIANT_KERNEL_'+name, not np.any(matrix@transformed % PRIME))
        check('FOLDED_RANK95_'+name, rank == 95)
        folds[name] = {'rank_over_Q_or_Qi': 95, 'nullity': 1,
                       'lower_bound_prime': PRIME, 'minor_rows': rows,
                       'minor_columns': cols, 'minor_residue': determinant}
    # Covariance and the exact nonzero Q-kernel give the characteristic-zero
    # upper bound 95. These nonzero 95-minors prove the matching lower bound.

    controls = []
    for phases in [(2, 3, 5, 7), (F(1, 2), F(2, 3), F(3, 5), F(5, 7)),
                   (F(3, 7), F(7, 3), F(5, 11), F(11, 5))]:
        rank, rows, cols, determinant = rank_minor(joint_mod(list(map(mod_fraction, phases))))
        check('RATIONAL_CONTROL_FULL_COLUMN_'+str(len(controls)), rank == 96)
        controls.append({'lambda': list(map(str, phases)), 'rank_over_Q': 96,
                         'lower_bound_prime': PRIME, 'minor_rows': rows,
                         'minor_columns': cols, 'minor_residue': determinant})

    axes = []
    for axis in range(4):
        rows, columns = [F(0)]*136, [F(0)]*96
        for offset, terms in ((0, S.ATERMS), (96, S.QTERMS)):
            for shift, entries in terms.items():
                for (r, c), value in entries.items():
                    bound = abs(shift[axis])*abs(value)
                    rows[offset+r] += bound
                    columns[c] += bound
        check('EXACT_DERIVATIVE_ENVELOPE_'+str(axis), max(rows) == max(columns) == F(22, 7))
        axes.append({'axis': axis, 'max_row_sum': str(max(rows)), 'max_column_sum': str(max(columns)),
                     'operator_1_2_infinity_bound': '22/7'})

    # A metric-coefficient sign mutation destroys the exact kernel, even
    # though changing the row-offset in the old test never changed the matrix.
    bad = {shift: dict(entries) for shift, entries in S.QTERMS.items()}
    shift, key, value = next((d, (r, c), value)
                            for d, entries in bad.items() for (r, c), value in entries.items()
                            if value and vector[c])
    bad[shift][key] = -value
    check('METRIC_SIGN_MUTATION_REJECTED', any(exact_common_action(vector, bad)))
    normalized = [[name, list(shift), r, c, str(value)]
                  for name, terms in [('A', S.ATERMS), ('C', S.QTERMS)]
                  for shift, entries in sorted(terms.items())
                  for (r, c), value in sorted(entries.items())]
    digest = hashlib.sha256(json.dumps(normalized, separators=(',', ':')).encode()).hexdigest()
    return {
        'schema': 'a4d-y-joint-symbol-independent-replay-v2',
        'repository': 'gvakhrushev/d0_15', 'pr': 310,
        'input_head': INPUT_HEAD, 'attached_report_input_head': ATTACHED_INPUT_HEAD,
        'operator': 'finite-amplitude z=1 Y, 136x96; distinct from identity-sheet 34x24',
        'arithmetic': 'exact Fraction identities; good-prime nonzero minors lift lower bounds to Q or Q(i)',
        'coefficient_sha256': digest,
        'exact_stencil': {'connection_shifts': 21, 'connection_nonzeros': 1944,
                          'metric_shifts': 5, 'metric_nonzeros': 1044},
        'connection_reciprocity': 'coefficientwise A(lambda^-1)=A(lambda)^T',
        'folded_covariance': 'Q(rho*lambda)=D_rows(rho^-phase) Q(lambda) D_cols(rho^phase), rho^4=1',
        'attachment_bug': {'wrong_metric_row_phase_failures': len(wrong),
                           'correct_metric_row_phase_failures': 0,
                           'first_failure': [list(wrong[0][0]), wrong[0][1], wrong[0][2], wrong[0][3]]},
        'folded_exact_ranks': folds, 'rational_exact_rank_controls': controls,
        'unit_torus_derivative_envelopes': axes,
        'all_torus_rank_theorem': False,
        'nonlinear_curved_continuation': False,
        'verdict': 'FINITE_OWNER_REPLAY_PASS; TASK_TERMINAL_OPEN'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name('a4d_y_joint_symbol_independent_replay_results.json') if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print('PASS_PINNED_LEDGER', flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('VERDICT', report['verdict'])
