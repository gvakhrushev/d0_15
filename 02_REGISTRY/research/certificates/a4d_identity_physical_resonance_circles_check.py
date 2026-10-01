#!/usr/bin/env python3
"""Literal Euler placement and continuous identity-sheet resonance circles.

Independent 4x4 face Hessians determine the physical stack (A^T;C). Exact
Gaussian-integer polynomial minors then classify three complex lines and
conjugation gives six physical unit circles. This supersedes the physical
interpretations of the wrong-placement first-slow/parabolic controls.
"""
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path
import argparse
import json
import numpy as np
import a4d_y_curved_joint_rational_stencil as S
from a4d_designated_full_gap_check import QI, flat_symbols, elimination
from a4d_warped_quarter_regular_response_check import COLS, qi_inverse, independent_rows
from a4d_identity_fourphase_circle_check import determinant, tr, qpoly, qgcd, evaluate, exact_strings

Q = QI(0, 1)
TC = [[0, 0, 0, 1, -1, 1], [0, 1, -1, 0, 0, 1],
      [1, 0, -1, 0, 1, 0], [1, -1, 0, 1, 0, 0]]


def literal_stencil():
    """Direct Hessian of odd plaquette curvature; input-minus-output shifts."""
    h, c = {}, {}
    def add(terms, shift, row, col, value):
        if value:
            entries = terms.setdefault(tuple(shift), {})
            entries[row, col] = entries.get((row, col), F(0))+value
    for r, s in S.PAIRS:
        roles = [r, s, r, s]
        signs = [1, 1, -1, -1]
        offsets = [(0, 0, 0, 0), tuple(int(j == r) for j in range(4)),
                   tuple(int(j == s) for j in range(4)), (0, 0, 0, 0)]
        u, v = [j for j in range(4) if j not in (r, s)]
        area = S.wedge(S.basis(u), S.basis(v))
        for a, b in combinations(range(4), 2):
            for i, xi in enumerate(S.GEN):
                for j, xj in enumerate(S.GEN):
                    d2p = S.mscale(signs[a]*signs[b], S.mm(xi, xj))
                    d2f = S.mscale(F(1, 2), S.msub(d2p, S.linv(d2p)))
                    value = S.orient(r, s)*S.pair_star(area, S.biv(d2f))
                    shift = tuple(x-y for x, y in zip(offsets[b], offsets[a]))
                    add(h, shift, 6*roles[a]+i, 6*roles[b]+j, value)
                    add(h, tuple(-x for x in shift), 6*roles[b]+j, 6*roles[a]+i, value)
        for metric, (a, b) in enumerate(S.SYM):
            ds = S.metric_lift(a, b)
            da = S.madd([S.wedge([ds[i][u] for i in range(4)], S.basis(v))],
                        [S.wedge(S.basis(u), [ds[i][v] for i in range(4)])])[0]
            for slot, role in enumerate(roles):
                for generator, x in enumerate(S.GEN):
                    value = signs[slot]*S.orient(r, s)*S.pair_star(da, S.biv(x))
                    add(c, offsets[slot], metric, 6*role+generator, value)
    return ({d: {rc: x for rc, x in entries.items() if x} for d, entries in h.items()},
            {d: {rc: x for rc, x in entries.items() if x} for d, entries in c.items()})


H_LITERAL, C_LITERAL = literal_stencil()


def literal_joint(phases):
    out = np.array([[QI() for _ in range(24)] for _ in range(34)], dtype=object)
    for offset, terms in ((0, H_LITERAL), (24, C_LITERAL)):
        for shift, entries in terms.items():
            phase = QI.of(1)
            for z, power in zip(phases, shift):
                if power == 1:
                    phase *= QI.of(z)
                elif power == -1:
                    phase /= QI.of(z)
                else:
                    assert power == 0
            for (r, c), value in entries.items():
                out[offset+r, c] += phase*value
    return out


def joint(phases, wrong=False):
    a, c = flat_symbols(phases)
    a = np.array(a, dtype=object)
    return np.concatenate([a if wrong else a.T, np.array(c, dtype=object)])


def line_coefficients(spatial_role):
    def at(a):
        phases = [Q]*4
        phases[0] = phases[spatial_role] = a
        return joint(phases)
    plus, minus, quarter = [at(z) for z in (1, -1, Q)]
    zero = (plus+minus)/2
    positive = (plus-zero+(quarter-zero)/Q)/2
    negative = plus-zero-positive
    polynomial = []
    for r in range(34):
        row = []
        for c in range(24):
            values = [2*x[r, c] for x in (negative, zero, positive)]
            assert all(x.re.denominator == x.im.denominator == 1 for x in values)
            row.append(tr([(int(x.re), int(x.im)) for x in values]))
        polynomial.append(row)
    held = QI(F(3, 5), F(4, 5))
    assert np.array_equal(at(held), negative/held+zero+positive*held)
    return (negative, zero, positive), polynomial, at


def transform(vector, spatial_role):
    permutation = list(range(4))
    permutation[1], permutation[spatial_role] = permutation[spatial_role], permutation[1]
    out = np.array([QI() for _ in range(24)], dtype=object)
    gens = np.array(S.GEN, dtype=object)
    for role in range(4):
        matrix = sum((gens[j]*vector[6*role+j] for j in range(6)), np.zeros((4, 4), dtype=object))
        matrix = matrix[np.ix_(permutation, permutation)]
        coords = [matrix[0, j] for j in (1, 2, 3)]+[matrix[1, 2], matrix[1, 3], matrix[2, 3]]
        out[6*permutation[role]:6*permutation[role]+6] = coords
    return out


def circle_kernel(spatial_role):
    constant = np.array([QI() for _ in range(24)], dtype=object)
    linear = constant.copy()
    constant[0] = constant[6] = Q
    linear[0] = linear[6] = QI.of(-1)
    for role in (2, 3):
        for j, x in enumerate(TC[role]):
            constant[6*role+j] = (1-Q)*x
    free = np.array([QI() for _ in range(24)], dtype=object)
    free[21] = QI.of(1)
    mapped = transform(free, spatial_role)
    coordinate = next(j for j, x in enumerate(mapped) if x)
    return transform(constant, spatial_role), transform(linear, spatial_role), coordinate


def reduce_gamma(base, centers, complement, wrong=False):
    j0 = joint(base, wrong)
    rows = independent_rows(j0[:, complement])
    inverse = qi_inverse(j0[np.ix_(rows, complement)])
    rest = [r for r in range(34) if r not in rows]
    gammas = []
    for axis in range(4):
        values = []
        for z in (1, -1, Q):
            point = list(base)
            point[axis] = z
            values.append(joint(point, wrong))
        plus, minus, quarter = values
        zero = (plus+minus)/2
        derivative = quarter-zero if base[axis] == QI.of(1) else -(plus-minus)/2
        assert base[axis] in (QI.of(1), Q)
        source = derivative@centers
        gammas.append((source-j0[:, complement]@inverse@source[rows])[rest])
    return j0, rows, rest, gammas


def run_checks():
    # Both symbols have Laurent radius <=1 in each variable. The tensor
    # product of three nonzero evaluation nodes therefore proves equality
    # coefficientwise, rather than sampling a rank or extrapolating a gap.
    for phases in product((QI.of(1), QI.of(-1), Q), repeat=4):
        assert np.array_equal(literal_joint(phases), joint(phases))
    print('PASS_LITERAL_FACE_HESSIAN_FULL_LAURENT_INTERPOLATION_81', flush=True)
    control = [QI(F(3, 5), F(4, 5))]*2+[Q]*2
    assert np.array_equal(literal_joint(control), joint(control))
    assert not np.array_equal(literal_joint(control), joint(control, wrong=True))
    assert elimination(joint(control).tolist())[0] == 23
    assert elimination(joint(control, wrong=True).tolist())[0] == 24
    print('PASS_MIXED_PLACEMENT_CONTROL_PHYSICAL23_WRONG24', flush=True)

    circles = []
    for spatial in (1, 2, 3):
        coefficients, polynomial, at = line_coefficients(spatial)
        constant, linear, coordinate = circle_kernel(spatial)
        assert constant[coordinate] and not linear[coordinate]
        for degree in range(-1, 3):
            value = np.array([QI() for _ in range(34)], dtype=object)
            for power, matrix in zip((-1, 0, 1), coefficients):
                if power == degree:
                    value += matrix@constant
                if power+1 == degree:
                    value += matrix@linear
            assert not np.any(value)
        columns = [j for j in range(24) if j != coordinate]
        charts, gcd = [], None
        for order in (list(range(34)), list(range(24, 34))+list(range(24))):
            rows = [order[j] for j in independent_rows(at(1)[np.ix_(order, columns)])]
            assert len(rows) == 23
            determinant_poly = determinant([[polynomial[r][c] for c in columns] for r in rows])
            assert determinant_poly
            qp = qpoly(determinant_poly)
            gcd = qp if gcd is None else qgcd(gcd, qp)
            held = QI(F(3, 5), F(4, 5))
            rank, value = elimination(at(held)[np.ix_(rows, columns)].tolist())
            assert rank == 23
            scale = QI.of(1)
            for _ in range(23):
                scale *= 2*held
            assert evaluate(qp, held) == scale*value
            charts.append({'rows': rows, 'columns': columns, 'degree': len(qp)-1,
                           'determinant': [list(x) for x in determinant_poly]})
        expected = [(1, 0)]
        from a4d_identity_fourphase_circle_check import pm
        for _ in range(4):
            expected = pm(expected, [(0, -1), (1, 0)])
        # The selected row charts differ under a spatial permutation.
        # Their harmless clearing-denominator power at a=0 can differ;
        # on C* each chart gcd has exactly the same root a=i.
        zero_order = next(j for j, x in enumerate(gcd) if x)
        assert gcd == [QI()]*zero_order+qpoly(expected)
        assert elimination(at(Q).tolist())[0] == 20
        circles.append({'variable_roles': [0, spatial], 'fixed_other_phases': 'i',
                        'kernel_constant': exact_strings(constant), 'kernel_linear': exact_strings(linear),
                        'nonzero_constant_coordinate': coordinate,
                        'rank_off_a_i': 23, 'rank_at_a_i': 20,
                        'minor_charts': charts, 'monic_gcd': exact_strings(gcd),
                        'excluded_a_zero_multiplicity': zero_order})
        print('PASS_CONTINUOUS_COMPLEX_RESONANCE_CIRCLE_0_'+str(spatial), flush=True)

    centers = np.array([[QI() for _ in range(4)] for _ in range(24)], dtype=object)
    for role in range(4):
        for j, x in enumerate(TC[role]):
            centers[6*role+j, role] = QI.of(x)
    j0, rows, rest, gamma = reduce_gamma([Q]*4, centers, COLS)
    assert elimination(j0.tolist())[0] == 20
    assert all(elimination(g.tolist())[0] == 4 for g in gamma)
    direction = [1, 1, 0, 0]
    reduced = sum((x*g for x, g in zip(direction, gamma)), np.zeros((14, 4), dtype=object))
    null = np.array([QI(), QI(), QI.of(1), QI.of(1)], dtype=object)
    assert not np.any(reduced@null)
    assert elimination(reduced.tolist())[0] == 3
    _, _, _, wrong_gamma = reduce_gamma([Q]*4, centers, COLS, wrong=True)
    wrong_reduced = wrong_gamma[0]+wrong_gamma[1]
    assert elimination(wrong_reduced.tolist())[0] == 4
    print('PASS_PHYSICAL_QUARTER_FIRSTSLOW_CHARACTERISTIC_AND_FALSE_INJECTIVITY_CONTROL', flush=True)

    constant, linear, coordinate = circle_kernel(1)
    n = ((constant+linear)/(constant[coordinate])).reshape(24, 1)
    mixed_point = [QI.of(1), QI.of(1), Q, Q]
    assert not np.any(joint(mixed_point)@n)
    # Face (0,2): dF=(1-lambda2)u0+(lambda0-1)u2.
    # Here u0=-K1, so dF=(i-1)K1 !=0. A pure gauge at I
    # has u_r=(lambda_r-1)theta and zero linear plaquette curvature.
    assert n[0, 0] == QI.of(-1)
    linear_curvature_coefficient = (1-Q)*n[0, 0]
    assert linear_curvature_coefficient == Q-1 and linear_curvature_coefficient
    assert mixed_point not in ([Q]*4, [-Q]*4)
    print('PASS_NONGAUGE_EXACT_KERNEL_OUTSIDE_DIAGONAL_QUARTER_FIBERS', flush=True)
    complement = [j for j in range(24) if j != coordinate]
    _, r23, rest23, g23 = reduce_gamma([QI.of(1), QI.of(1), Q, Q], n, complement)
    real = np.array([[g[row, 0].re for g in g23] for row in range(11)]
                    + [[g[row, 0].im for g in g23] for row in range(11)], dtype=object)
    assert elimination(real.tolist())[0] == 2
    assert not np.any(real@np.array(direction, dtype=object))
    second_direction = [0, 0, 1, -1]
    assert not np.any(real@np.array(second_direction, dtype=object))
    print('PASS_RANK23_TANGENT_IS_CONTINUOUS_CIRCLE_NOT_PARABOLIC_ISOLATED_POINT', flush=True)
    return {
        'schema': 'a4d-identity-physical-resonance-circles-v1',
        'input_head': 'de71bf30e9cfd34614fc8178255d456c49ebb8b1',
        'arithmetic': 'Q(i) identities; exact Gaussian-integer polynomial Bareiss and Q(i) gcd',
        'physical_symbol': 'literal Euler J=(A^T;C), 34x24',
        'literal_interpolation_nodes': ['1', '-1', 'i'], 'literal_interpolation_count': 81,
        'placement_control': {'phases': exact_strings(control), 'physical_rank': 23, 'wrong_placement_rank': 24},
        'complex_line_certificates': circles,
        'conjugate_circles': 'all real Laurent coefficients; replace i by -i and conjugate kernels',
        'quarter_range_rows': rows, 'quarter_reduced_rows': rest,
        'quarter_gamma': [[exact_strings(row) for row in g] for g in gamma],
        'quarter_characteristic_direction': direction,
        'quarter_reduced_rank_on_direction': 3,
        'quarter_reduced_kernel_amplitudes': exact_strings(null),
        'wrong_placement_reduced_rank_on_same_direction': 4,
        'rank23_range_rows': r23, 'rank23_reduced_rows': rest23,
        'rank23_firstslow_real_rank': 2, 'rank23_circle_tangent': direction,
        'rank23_other_firstslow_null_direction': second_direction,
        'rank23_firstslow_real_matrix': [[str(x) for x in row] for row in real],
        'rank23_schur_along_circle': 'identically zero, by the global polynomial kernel with a nonzero constant center coordinate',
        'quarter_only_complement_counterexample': {
            'metric': 'eta; smooth comparator I', 'periods': 'every L divisible by 4',
            'real_field': 'Re(i^(x2+x3) v(1))',
            'characters': ['(1,1,i,i)', '(1,1,-i,-i)'],
            'connection_and_metric_linear_residual': 'exactly zero',
            'diagonal_quarter_projection': 'exactly zero by distinct discrete Fourier characters',
            'linear_plaquette_curvature_face_0_2': '(i-1)K1 !=0',
            'nongauge_reason': 'pure gauge at I has zero linear plaquette curvature',
            'consequence': 'no inverse with any finite h loss on a complement that removes only the diagonal quarter fibers',
            'scope': 'refutes that linear range-inverse premise, not existence of the designated flat root or continuum response universality'},
        'superseded_physical_claims': ['full first-slow injectivity of the quarter center for all real k !=0',
                                       'isolated parabolic rank23 points and an eight-point physical torus premise'],
        'one_coordinate_owners': 'unchanged: their physical (A^T;C) circle is different and has only the two quarter folds',
        'nonclaims': ['does not classify all remaining physical torus zeros',
                      'does not construct a nonlinear stationary branch or independent-source counterexample',
                      'does not prove continuum response failure or closure'],
        'verdict': 'CONTINUOUS_PHYSICAL_RESONANCE_CIRCLES_CERTIFIED; TASK_TERMINAL_OPEN'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--expect', type=Path)
    args = parser.parse_args()
    report = run_checks()
    expected = args.expect or (Path(__file__).with_name('a4d_identity_physical_resonance_circles_results.json') if args.output is None else None)
    if expected:
        assert json.loads(expected.read_text()) == report
        print('PASS_PINNED_LEDGER', flush=True)
    if args.output:
        args.output.write_text(json.dumps(report, indent=2)+'\n')
    print('VERDICT', report['verdict'])
