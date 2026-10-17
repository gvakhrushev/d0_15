#!/usr/bin/env python3
"""Role-indexed coframe induction on one pp-wave family.

Consumer of the reconstruction pinned at
e92d4714183aec5b8838906be1dfd23844178042, checker blob
0b11d34f2f982a62616722feeb110f10fa55f2e6.
The curvature below is recomputed. It is not assigned from the
Einstein expression. This module does not identify the native price
with the geometric action.
"""
from __future__ import annotations

from itertools import combinations

import sympy as S

ETA = S.diag(1, -1, -1, -1)
SIG = (1, -1, -1, -1)
PAIRS = list(combinations(range(4), 2))
PIN = "e92d4714183aec5b8838906be1dfd23844178042"
CHECKER_BLOB = "0b11d34f2f982a62616722feeb110f10fa55f2e6"


def clean(value):
    if isinstance(value, S.MatrixBase):
        return value.applyfunc(S.cancel)
    return S.cancel(value)


def nilpotent():
    generator = S.zeros(4)
    generator[0, 0] = generator[0, 3] = S.Rational(1, 2)
    generator[3, 0] = generator[3, 3] = -S.Rational(1, 2)
    return generator


def wave_family(height, hx, hy, hxx, hxy, hyy):
    """Coordinate coframe of the pinned pp-wave. Rows are indexed 0..3.

    These rows are not the native solder legs eta F_r^T.
    """
    generator = nilpotent()
    if generator * generator != S.zeros(4):
        raise ArithmeticError("nilpotent_generator")
    frame_inverse = S.eye(4) + height * generator
    frame = S.eye(4) - height * generator
    metric = clean(frame_inverse.T * ETA * frame_inverse)
    first = [S.zeros(4), hx * generator, hy * generator, S.zeros(4)]
    second = [[S.zeros(4) for _ in range(4)] for _ in range(4)]
    second[1][1] = hxx * generator
    second[1][2] = hxy * generator
    second[2][1] = hxy * generator
    second[2][2] = hyy * generator
    return {
        "e": frame_inverse,
        "F": frame,
        "g": metric,
        "de": first,
        "dde": second,
        "N": generator,
        "k": S.Matrix([1, 0, 0, 1]),
    }


def induce_coframe(frame_inverse, variation):
    """Symmetric Role variation to coordinate-coframe variation.

    delta e = e g^{-1} V / 2, with g = e^T eta e.
    """
    metric = frame_inverse.T * ETA * frame_inverse
    return S.simplify(frame_inverse * metric.inv() * variation / 2)


def recovered_metric_variation(frame_inverse, delta_frame):
    return S.simplify(
        delta_frame.T * ETA * frame_inverse + frame_inverse.T * ETA * delta_frame
    )


def _torsion(frame_inverse, first, connection):
    return {
        (left, right): clean(
            first[left][:, right]
            - first[right][:, left]
            + connection[left] * frame_inverse[:, right]
            - connection[right] * frame_inverse[:, left]
        )
        for left, right in PAIRS
    }


def _absorb(frame_inverse, torsion):
    """Unique metric-compatible contorsion, component formula (4) of the pin."""
    frame = frame_inverse.inv()
    lowered = [
        [
            [
                sum(
                    SIG[row]
                    * frame[left, mid]
                    * frame[right, last]
                    * (
                        torsion[left, right][row]
                        if left < right
                        else -torsion[right, left][row]
                    )
                    for left in range(4)
                    for right in range(4)
                    if left != right
                )
                for last in range(4)
            ]
            for mid in range(4)
        ]
        for row in range(4)
    ]
    contorsion = [
        [
            [
                clean(
                    (
                        lowered[row][mid][last]
                        + lowered[mid][last][row]
                        - lowered[last][row][mid]
                    )
                    / 2
                )
                for last in range(4)
            ]
            for mid in range(4)
        ]
        for row in range(4)
    ]
    return [
        S.Matrix(
            4,
            4,
            lambda row, mid: clean(
                SIG[row]
                * sum(
                    contorsion[row][mid][last] * frame_inverse[last, direction]
                    for last in range(4)
                )
            ),
        )
        for direction in range(4)
    ]


def _connection_jet(frame_inverse, connection, delta_frame, delta_first):
    return _absorb(frame_inverse, _torsion(delta_frame, delta_first, connection))


def curvature_source(frame_inverse, first, second):
    """Ricci and scalar density from torsion absorption, not from a pasted formula."""
    connection = _absorb(frame_inverse, _torsion(frame_inverse, first, [S.zeros(4) for _ in range(4)]))
    derivative = [
        _connection_jet(frame_inverse, connection, first[direction], second[direction])
        for direction in range(4)
    ]
    curvature = {
        (left, right): clean(
            derivative[left][right]
            - derivative[right][left]
            + connection[left] * connection[right]
            - connection[right] * connection[left]
        )
        for left, right in PAIRS
    }
    frame = frame_inverse.inv()
    converted = {
        pair: clean(frame * block * frame_inverse) for pair, block in curvature.items()
    }

    def component(left, right):
        if left < right:
            return converted[left, right]
        if right < left:
            return -converted[right, left]
        return S.zeros(4)

    ricci = S.Matrix(
        4,
        4,
        lambda down, across: clean(
            sum(component(row, across)[row, down] for row in range(4))
        ),
    )
    metric = frame_inverse.T * ETA * frame_inverse
    density = clean(S.trace(metric.inv() * ricci) * frame_inverse.det())
    raised = clean(metric.inv() * ricci * metric.inv())
    return {
        "Ric": ricci,
        "scalar_density": density,
        "Gup": raised,
        "connection": connection,
        "forms": curvature,
    }


def metric_probe(raised, variation):
    return S.simplify(S.trace(raised * variation))


def row_support(matrix):
    return tuple(
        index
        for index in range(4)
        if any(S.simplify(matrix[index, column]) != 0 for column in range(4))
    )


def native_leg(frame, role):
    """v_r = eta F_r^T. Not the coordinate coframe row."""
    return S.simplify(ETA * frame[role, :].T)
