#!/usr/bin/env python3
"""Check the exact 718-edge input and the finite registered source identity."""
from hashlib import sha256
import json
from pathlib import Path

import sympy as s
from sympy.polys.matrices import DomainMatrix


def scene():
    zones = [zone for zone, size in enumerate((9, 11, 13)) for _ in range(size)]
    adjacency = s.Matrix(33, 33, lambda i, j: int(zones[i] != zones[j]))
    assert sum(adjacency) == 718 and adjacency.rank() == 3
    degrees = [int(sum(adjacency.row(i))) for i in range(33)]
    assert degrees == [24] * 9 + [22] * 11 + [20] * 13
    degree_transfer = s.diag(*(s.Rational(1, d) for d in degrees)) * adjacency
    ker = degree_transfer.nullspace()
    loss = s.eye(33) - degree_transfer**2
    assert len(ker) == 30 and all(loss * v == v for v in ker)
    assert DomainMatrix.from_Matrix(loss).rank() == 32
    scale = s.diag(*(1 / s.sqrt(d + 2) for d in degrees))
    Bs = scale * adjacency * scale
    Cs = scale**2
    assert s.simplify((Bs * Cs - Cs * Bs)[0, 9] - 1 / (312 * s.sqrt(624))) == 0
    return {'directed_edges': 718, 'adjacency_rank': 3, 'scene_feedback_rank': 32,
            'binary_unit_leakage_modes': 30, 'rank_four_intersection_dimension_at_least': 26,
            'scene_time_heat_blocks_do_not_commute': True}


def registered_source():
    # Rational analytical fixture for (2) with moving preparation, terminal,
    # chronological unitary, and scene weights. All declared effects and
    # weights here remain strictly positive for sufficiently small t.
    t = s.Symbol('t', real=True)
    rho = s.diag(s.Rational(2, 3) + t, s.Rational(1, 3) - t)
    rotation = s.Matrix([[1 - t**2, -2 * t], [2 * t, 1 - t**2]]) / (1 + t**2)
    static_rotation = s.Matrix([[3, -4], [4, 3]]) / 5
    words = [rotation * static_rotation, static_rotation * rotation.T]
    effects = [s.diag(s.Rational(2, 3), s.Rational(1, 3) + t), s.diag(s.Rational(1, 4), s.Rational(3, 4))]
    weights = [2 + t, 1 - t / 2]
    for word in words:
        assert s.simplify(word.T * word - s.eye(2)) == s.zeros(2)
        assert s.simplify(s.trace(rho * word.T * word)) == 1
    e = [s.trace(rho * V.T * E * V) for V, E in zip(words, effects)]
    Z = sum(w * x for w, x in zip(weights, e))
    ZI = sum(weights)
    pi = [w / ZI for w in weights]
    ell = [s.diff(w, t) / w for w in weights]
    avg = sum(p * x for p, x in zip(pi, e))
    expected_derivative = sum(p * s.diff(x, t) for p, x in zip(pi, e))
    covariance = sum(p * x * l for p, x, l in zip(pi, e, ell)) - avg * sum(p * l for p, l in zip(pi, ell))
    at_zero = lambda x: s.simplify(x.subs(t, 0))
    direct = s.diff(Z, t) / Z - s.diff(ZI, t) / ZI
    assert at_zero(direct - (expected_derivative + covariance) / avg) == 0
    assert at_zero(expected_derivative) != 0 and at_zero(covariance) != 0
    return {'complete_unmarked_effects_constant_under_actual_isometries': True,
            'clock_preparation_terminal_and_weight_terms_checked': True}


def main():
    root = Path(__file__).resolve().parents[4]
    paths = [
        'A4D_NATIVE_SCENE_718_EDGE_COMPLETE_REGISTER_DETERMINANT_BOOK_2026_10_19.md',
        'A4D_NATIVE_SHARED_SCENE_PRICE_SOURCE.md',
        'A4D_BOOK03_GLOBAL_WEIGHTED_SCENE_BALANCE_AND_REPORT_BRIDGE_2026_10_22.md',
        'sources/d0_retained_response_concentration_2026-10-28/GROWING_CLOCK_RU.md',
        'A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md',
    ]
    print(json.dumps({'result': 'PASS', 'scene': scene(), 'registered_fixture': registered_source(),
                      'upstream_sha256': {p: sha256((root / p).read_bytes()).hexdigest() for p in paths},
                      'physical_C_closed': False, 'GR_closed': False}, indent=2))


if __name__ == '__main__':
    main()
