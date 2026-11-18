#!/usr/bin/env python3
"""Rational verification of the owned J2 coefficient and the null witness."""
from fractions import Fraction
from hashlib import sha256
from pathlib import Path
import json

import sympy as sym


class Interval:
    def __init__(self, lo, hi=None):
        self.lo = Fraction(lo)
        self.hi = Fraction(lo if hi is None else hi)
        assert self.lo <= self.hi

    @staticmethod
    def coerce(value):
        return value if isinstance(value, Interval) else Interval(value)

    def __add__(self, other):
        other = self.coerce(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + (-self.coerce(other))

    def __rsub__(self, other):
        return self.coerce(other) + (-self)

    def __mul__(self, other):
        other = self.coerce(other)
        ends = [a * b for a in (self.lo, self.hi) for b in (other.lo, other.hi)]
        return Interval(min(ends), max(ends))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = self.coerce(other)
        assert not other.lo <= 0 <= other.hi
        return self * Interval(1 / other.hi, 1 / other.lo)

    def __rtruediv__(self, other):
        return self.coerce(other) / self

    def __pow__(self, n):
        assert n >= 0
        result = Interval(1)
        for _ in range(n):
            result *= self
        return result


def coefficient_bounds():
    p = Interval(Fraction(618033988749, 10**12), Fraction(618033988750, 10**12))
    assert p.lo**2 + p.lo < 1 < p.hi**2 + p.hi
    z = Fraction(1, 2**20)
    L0 = 4 * p**2 * (1 - p**2)
    Q0 = 1 - z * L0
    R0 = 1 - z * (L0 + (1 - L0) * L0)
    assert min(Q0.lo, R0.lo) > 0
    curvature_slope = 4 * p**2 * (1 - 2 * p**2)
    curvature_second = -8 * p**4
    # Set T=1. Each slope is proportional to T and each second jet to T^2.
    c = z * curvature_slope * (1 - L0) / R0
    rr = z * (1 - L0) * curvature_second / R0
    rr += (z * (1 - L0) * curvature_slope / R0)**2
    for orientation in (-1, 1):
        matter_slope = 8 * orientation * p**3 * (1 - 2 * p**2)
        matter_second = 8 * p**4 * (1 - 2 * p**2) - 32 * p**6
        d = z * matter_slope * (1 / Q0 + (1 - L0) / R0)
        rX = -z * (1 - z) * curvature_slope * matter_slope / R0**2
        XX = z * matter_second * (1 / Q0 + (1 - L0) / R0)
        XX += z**2 * matter_slope**2 * (1 / Q0**2 + (1 - L0)**2 / R0**2)
        ratio = d / c
        C2 = XX - 2 * ratio * rX + ratio**2 * rr
        cone_coefficient = -orientation * 2 * C2 / d
        assert c.lo > 0 and rr.hi < 0
        assert 23 < (orientation * ratio).lo < (orientation * ratio).hi < 24
        assert C2.hi < 0
        assert -1479 < (C2 / c).lo < (C2 / c).hi < -1478
        assert 126 < cone_coefficient.lo < cone_coefficient.hi < 127


def verify_symbol():
    H, alpha, amplitude = sym.symbols('H alpha A', real=True)
    metric_inverse = sym.Matrix([[0, 1, 0, 0], [1, -H, 0, 0],
                                 [0, 0, -1, 0], [0, 0, 0, -1]])
    raised_gradient = sym.Matrix([0, amplitude, 0, 0])
    scalar_inverse = metric_inverse + alpha * raised_gradient * raised_gradient.T
    assert scalar_inverse.det() == metric_inverse.det() == -1
    shifted_covector = sym.Matrix([(H - alpha * amplitude**2) / 2, 1, 0, 0])
    assert sym.expand((shifted_covector.T * scalar_inverse * shifted_covector)[0]) == 0
    assert sym.expand((shifted_covector.T * metric_inverse * shifted_covector)[0]) == -alpha * amplitude**2


def verify_original_metric_control():
    X, p, T, z, k, orientation = sym.symbols('X p T z k orientation')
    E = p**2 * (1 - T * k * X)
    probability = (p + orientation * p**2 * T * X)**2
    geometric = 4 * E * (1 - E)
    matter = 4 * probability * (1 - probability)
    Q = sym.Poly(1 - z * matter, X)
    R = sym.Poly(1 - z * (geometric + (1 - geometric) * matter), X)
    assert Q.degree() == 4 and R.degree() == 6
    for sign in (-1, 1):
        leading = (Q.LC() * R.LC()).subs(orientation, sign)
        assert leading == 64 * z**2 * p**20 * T**10 * k**2


def main():
    root = Path(__file__).resolve().parents[4]
    owner = root / 'A4D_SINGLE_J2_EXACT_EINSTEIN_FRAME_AND_KESSENCE_2026_10_18.md'
    digest = sha256(owner.read_bytes()).hexdigest()
    assert digest == '6429169d276aa0b580c1ee9327f3f1549d545ce1a2996291e30c182b5b1bd2dc'
    coefficient_bounds()
    verify_symbol()
    verify_original_metric_control()
    print(json.dumps({
        'status': 'PASS',
        'upstream_owner_sha256': digest,
        'physical_feedback_z': '2^-20',
        'C2_over_c_over_T_open_interval': [-1479, -1478],
        'absolute_cone_shift_over_T_open_interval': [126, 127],
        'orientations_checked': [-1, 1],
        'distinct_scalar_and_metric_characteristics_at_nonzero_null_gradient': True,
        'original_metric_nonconstant_X_polynomial_degree': 10,
        'physical_cost_info_binding': False,
        'GR_closed': False,
    }, indent=2))


if __name__ == '__main__':
    main()
