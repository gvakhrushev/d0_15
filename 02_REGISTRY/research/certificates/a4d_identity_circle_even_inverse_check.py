#!/usr/bin/env python3
"""Exact all-frequency inverse for the even output of a resonance circle.

Two-sided coefficient identities, not sampled ranks, certify the inverse.
This is the flat (b,b,-1,-1) connection block, not the full curved Hessian.
"""
from fractions import Fraction as F
from pathlib import Path
import argparse
import json
import numpy as np
import a4d_identity_physical_resonance_circles_check as P
from a4d_warped_designated_normal_rescue_check import interpolate, inverse


def compose(a, b):
    out = np.zeros((len(a)+len(b)-1, 24, 24), dtype=object)
    for j, x in enumerate(a):
        for k, y in enumerate(b):
            out[j+k] += x@y
    return out


def ledger(blocks, radius):
    return [{'power': j-radius, 'entries': [[r, c, str(block[r, c])]
                for r in range(24) for c in range(24) if block[r, c]]}
            for j, block in enumerate(blocks) if np.any(block)]


def build_inverse():
    h = []
    for b in (1, -1, P.Q):
        a, _ = P.flat_symbols([b, b, -1, -1])
        h.append(np.array(a, dtype=object).T)
    zero = (h[0]+h[1])/2
    positive = (h[0]-zero+(h[2]-zero)/P.Q)/2
    negative = h[0]-zero-positive
    assert all(not x.im for block in (negative, zero, positive) for row in block for x in row)
    H = np.array([[[x.re for x in row] for row in block]
                  for block in (negative, zero, positive)], dtype=object)
    radius = 3
    values = []
    for b in map(F, range(1, 2*radius+2)):
        matrix = sum(block*b**(j-1) for j, block in enumerate(H))
        values.append(b**radius*inverse(matrix))
    B = np.array(interpolate(values))
    expected = np.zeros((9, 24, 24), dtype=object)
    expected[4] = np.eye(24, dtype=object)
    assert np.array_equal(compose(H, B), expected)
    assert np.array_equal(compose(B, H), expected)
    return H, B


def run_checks():
    H, B = build_inverse()
    print('PASS_TWO_SIDED_RADIUS3_LAURENT_INVERSE_ALL_COMPLEX_B', flush=True)
    polynomial = [[P.tr([(int(2*x[r, c]), 0) for x in H]) for c in range(24)]
                  for r in range(24)]
    determinant = P.determinant(polynomial)
    assert determinant == [(0, 0)]*24+[(2**32, 0)]
    print('PASS_PHYSICAL_CONNECTION_DETERMINANT_CONSTANT256', flush=True)
    def bounds(weight):
        rows = [sum(abs(block[r, c])*weight(j-3) for j, block in enumerate(B)
                    for c in range(24)) for r in range(24)]
        cols = [sum(abs(block[r, c])*weight(j-3) for j, block in enumerate(B)
                    for r in range(24)) for c in range(24)]
        return max(rows), max(cols)
    norm = bounds(lambda j: 1)
    moment = bounds(abs)
    assert norm == (F(9, 2), F(9, 2))
    assert sum(np.count_nonzero(block) for block in B) == 852
    bad = H.copy()
    entry = next((j, r, c) for j, block in enumerate(H) for r in range(24)
                 for c in range(24) if block[r, c])
    bad[entry] = -bad[entry]
    assert not np.array_equal(compose(bad, B), compose(H, B))
    print('PASS_ALL_LP_KERNEL_BOUND_FIRST_MOMENT_AND_SIGN_MUTATION', flush=True)
    return {'schema': 'a4d-identity-circle-even-inverse-v1',
            'input_head': 'de71bf30e9cfd34614fc8178255d456c49ebb8b1',
            'operator': 'literal connection H(b) at lambda=(b,b,-1,-1)',
            'identity': 'H(b)B(b)=B(b)H(b)=I24 for every b in C*',
            'determinant': '256', 'inverse_radius': 3, 'inverse_nonzero_coefficients': 852,
            'H': ledger(H, 1), 'B': ledger(B, 3),
            'operator_1_2_infinity_inverse_bound': '9/2',
            'inverse_first_moment_row_column_bounds': list(map(str, moment)),
            'all_periods': 'periodized finite Laurent convolution; every 1<=p<=infinity, including unweighted owner1',
            'nonclaims': ['not the odd physical circle-center inverse',
                          'not an arbitrary curved-coframe inverse or a full torus theorem',
                          'does not yet bound the nonlinear response of arbitrary circle envelopes'],
            'verdict': 'ALL_FREQUENCY_CIRCLE_EVEN_RANGE_INVERSE_CERTIFIED; TASK_TERMINAL_OPEN'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name('a4d_identity_circle_even_inverse_results.json')
                               if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print('PASS_PINNED_LEDGER', flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('VERDICT', report['verdict'])
