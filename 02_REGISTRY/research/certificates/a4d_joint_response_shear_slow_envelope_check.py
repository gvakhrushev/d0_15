#!/usr/bin/env python3
"""First lattice derivative of the order-3 shear resonant projection.

The solved period-2 jet is transported by a sitewise amplitude
A(x)=1+epsilon*ell(x). Shifts are the genuine lattice steps x |-> x+e_r.
Bookkeeping stops at order 3, which is the first order whose resonant
projection sees a gradient. The constant mode has slope 0. The gradient
is (72, -872/59, -144, 72).
"""
from __future__ import annotations

import importlib.util
import math
from fractions import Fraction
from itertools import product
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


cubic = load("a4d_joint_response_shear_cubic_check")
order5 = load("a4d_joint_response_shear_order5_check")

N = 4  # bookkeeping orders 0..3; order 3 is closed under this truncation
NVAR = 5  # 0: constant, 1..4: coordinate directions
ETA_SIGN = (1, -1, -1, -1)
PAIRS = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
SITES = list(product((0, 1), repeat=4))


def check(name, condition):
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def frac(expr):
    rational = cubic.sp.Rational(expr)
    return Fraction(int(rational.p), int(rational.q))


def reduce_mat(den, nums):
    g = den
    for value in nums:
        g = math.gcd(g, value)
    if g > 1:
        den //= g
        nums = [value // g for value in nums]
    if den < 0:
        den = -den
        nums = [-value for value in nums]
    return (den, tuple(nums))


def to_matrix(source):
    rats = [frac(source[i, j]) for i in range(4) for j in range(4)]
    den = 1
    for rat in rats:
        den = math.lcm(den, rat.denominator)
    nums = [rat.numerator * (den // rat.denominator) for rat in rats]
    return reduce_mat(den, nums)


def mat_zero():
    return (1, (0,) * 16)


def mat_eye():
    return (1, (1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1))


def mat_add(left, right):
    left_den, left_nums = left
    right_den, right_nums = right
    if left_den == right_den:
        return reduce_mat(left_den, [a + b for a, b in zip(left_nums, right_nums)])
    g = math.gcd(left_den, right_den)
    den = left_den // g * right_den
    left_factor = right_den // g
    right_factor = left_den // g
    return reduce_mat(den, [
        a * left_factor + b * right_factor
        for a, b in zip(left_nums, right_nums)
    ])


def as_rat(factor):
    if isinstance(factor, Fraction):
        return factor.numerator, factor.denominator
    return int(factor), 1


def mat_scale(factor, source):
    numer, denom = as_rat(factor)
    den, nums = source
    return reduce_mat(den * denom, [numer * value for value in nums])


def mat_mul(left, right):
    left_den, left_nums = left
    right_den, right_nums = right
    nums = [0] * 16
    for i in range(4):
        row = i * 4
        for j in range(4):
            total = 0
            for k in range(4):
                total += left_nums[row + k] * right_nums[k * 4 + j]
            nums[row + j] = total
    return reduce_mat(left_den * right_den, nums)


def lorentz_inv(source):
    den, nums = source
    out = [0] * 16
    for i in range(4):
        for j in range(4):
            out[i * 4 + j] = ETA_SIGN[i] * nums[j * 4 + i] * ETA_SIGN[j]
    return (den, tuple(out))


ZERO = mat_zero()
EYE = mat_eye()
ROLES = [to_matrix(cubic.ROLES[role]) for role in range(4)]
ZETA = [
    to_matrix(cubic.algebra(cubic.ZETA[6 * role: 6 * role + 6]))
    for role in range(4)
]
ETA = [
    to_matrix(cubic.algebra(order5.ETA_CLEAN[6 * role: 6 * role + 6]))
    for role in range(4)
]
GEN_MATS = [to_matrix(generator) for generator in cubic.GENERATORS]
ROWS = {}
for a, b in cubic.PAIRS:
    row = cubic.plain_row(a, b)
    ROWS[(a, b)] = tuple(frac(row[0, j]) for j in range(6))


def zero_slopes():
    return tuple(ZERO for _ in range(NVAR))


def element_zero():
    return (ZERO, zero_slopes())


def element_add(left, right):
    return (
        mat_add(left[0], right[0]),
        tuple(mat_add(left[1][i], right[1][i]) for i in range(NVAR)),
    )


def element_scale(factor, source):
    return (
        mat_scale(factor, source[0]),
        tuple(mat_scale(factor, source[1][i]) for i in range(NVAR)),
    )


def element_mul(left, right):
    base = mat_mul(left[0], right[0])
    slopes = []
    for i in range(NVAR):
        slopes.append(mat_add(
            mat_mul(left[0], right[1][i]),
            mat_mul(left[1][i], right[0]),
        ))
    return (base, tuple(slopes))


def element_inv(source):
    return (
        lorentz_inv(source[0]),
        tuple(lorentz_inv(source[1][i]) for i in range(NVAR)),
    )


def jet_zero():
    return [element_zero() for _ in range(N)]


def jet_eye():
    out = jet_zero()
    out[0] = (EYE, zero_slopes())
    return out


def jet_add(left, right):
    return [element_add(left[i], right[i]) for i in range(N)]


def jet_scale(factor, source):
    return [element_scale(factor, source[i]) for i in range(N)]


def jet_mul(left, right):
    out = jet_zero()
    for i in range(N):
        for j in range(N - i):
            out[i + j] = element_add(out[i + j], element_mul(left[i], right[j]))
    return out


def variation(site):
    return (Fraction(1),) + tuple(Fraction(site[r]) for r in range(4))


def powered(prefactor, matrix, site, power):
    lam = variation(site)
    base = mat_scale(prefactor, matrix)
    slopes = tuple(
        mat_scale(prefactor * power * lam[i], matrix)
        for i in range(NVAR)
    )
    return (base, slopes)


def sigma(site):
    return 1 if (site[0] + site[2]) % 2 == 0 else -1


def shift(site, role):
    out = list(site)
    out[role] += 1
    return tuple(out)


def link(site, role):
    sign = sigma(site)
    series = jet_zero()
    series[1] = powered(sign, ROLES[role], site, 1)
    series[2] = powered(1, ZETA[role], site, 2)
    series[3] = powered(sign, ETA[role], site, 3)
    step = jet_eye()
    out = jet_eye()
    for k in range(1, N):
        step = jet_scale(Fraction(1, k), jet_mul(step, series))
        out = jet_add(out, step)
    return out


def bivector(matrix):
    den, nums = matrix
    return den, tuple(nums[i * 4 + j] * ETA_SIGN[j] for i, j in PAIRS)


def dot_row(row, packed):
    den, comps = packed
    total = Fraction(0)
    for j in range(6):
        total += row[j] * Fraction(comps[j], den)
    return total


def scalar(row, source):
    value = dot_row(row, bivector(source[0]))
    slope = tuple(dot_row(row, bivector(source[1][i])) for i in range(NVAR))
    return value, slope


def resonant_linear():
    cache = {}

    def get_link(site, role):
        key = (site, role)
        found = cache.get(key)
        if found is None:
            found = link(site, role)
            cache[key] = found
        return found

    total = [(Fraction(0), tuple(Fraction(0) for _ in range(NVAR))) for _ in range(N)]
    for site in SITES:
        sign = sigma(site)
        for role in range(4):
            for j, generator in enumerate(cubic.GENERATORS):
                weight = cubic.WITNESS[role][j]
                if weight == 0:
                    continue
                gen = (GEN_MATS[j], zero_slopes())
                acc = [(Fraction(0), tuple(Fraction(0) for _ in range(NVAR))) for _ in range(N)]
                for a, b in cubic.PAIRS:
                    if role == a:
                        corners = [(site, 0), (shift(site, b), 2)]
                    elif role == b:
                        corners = [(shift(site, a), 1), (site, 3)]
                    else:
                        continue
                    row = ROWS[(a, b)]
                    for base, corner in corners:
                        facts = [
                            get_link(base, a),
                            get_link(shift(base, a), b),
                            element_inv_jet(get_link(shift(base, b), a)),
                            element_inv_jet(get_link(base, b)),
                        ]
                        varied = list(facts)
                        if corner < 2:
                            varied[corner] = jet_mul(facts[corner], [gen] + [element_zero() for _ in range(N - 1)])
                        else:
                            varied[corner] = jet_mul(
                                jet_scale(-1, [gen] + [element_zero() for _ in range(N - 1)]),
                                facts[corner],
                            )
                        hol = jet_eye()
                        dp = jet_eye()
                        for factor, varied_factor in zip(facts, varied):
                            hol = jet_mul(hol, factor)
                            dp = jet_mul(dp, varied_factor)
                        mid = jet_mul(jet_mul(element_inv_jet(hol), dp), element_inv_jet(hol))
                        for k in range(N):
                            curv = element_scale(Fraction(1, 2), element_add(dp[k], mid[k]))
                            piece = scalar(row, curv)
                            acc[k] = (
                                acc[k][0] + piece[0],
                                tuple(acc[k][1][i] + piece[1][i] for i in range(NVAR)),
                            )
                for k in range(N):
                    total[k] = (
                        total[k][0] + sign * weight * acc[k][0],
                        tuple(
                            total[k][1][i] + sign * weight * acc[k][1][i]
                            for i in range(NVAR)
                        ),
                    )
    print("LINK_CACHE", len(cache), flush=True)
    return total


def element_inv_jet(jet):
    return [element_inv(part) for part in jet]


def main():
    values = resonant_linear()
    frozen = [values[k][0] for k in range(N)]
    slopes = [values[k][1] for k in range(N)]
    print("FROZEN", frozen, flush=True)
    for k in range(N):
        print("SLOPE_ORDER", k, list(slopes[k]), flush=True)
    check("FROZEN_THROUGH_ORDER3_VANISHES", all(item == 0 for item in frozen))
    check(
        "ORDERS_BELOW_3_HAVE_NO_LINEAR_RESPONSE",
        all(all(item == 0 for item in slopes[k]) for k in range(3)),
    )
    order3 = slopes[3]
    expected = (
        Fraction(0),
        Fraction(72),
        Fraction(-872, 59),
        Fraction(-144),
        Fraction(72),
    )
    check("ORDER3_CONSTANT_RESPONSE_VANISHES", order3[0] == expected[0])
    check("ORDER3_GRADIENT", tuple(order3[1:]) == expected[1:])
    # Coordinate s dual to S=(72,-872/59,-144,72), so d/ds = S·∇.
    # The competing balance S·∇v = 432 v^3 becomes dv/ds = 432 v^3.
    # Then d/ds (v^{-2}) = -864, so a nonzero value reaches a pole in finite s.
    a, s = cubic.sp.symbols("a s", positive=True)
    v = a / cubic.sp.sqrt(1 - 864 * a**2 * s)
    residual = cubic.sp.simplify(cubic.sp.diff(v, s) - 432 * v**3)
    check("ODE_SEPARATION", residual == 0)
    _, denom = cubic.sp.fraction(cubic.sp.together(v**2))
    pole = cubic.sp.solve(denom, s)[0]
    check("ODE_POLE_AT_FINITE_DISTANCE", cubic.sp.simplify(pole - 1 / (864 * a**2)) == 0)
    check("GRADIENT_NOT_ZERO", any(item != 0 for item in expected[1:]))
    print("RESULT_SLOW_ENVELOPE: order-3 gradient competes with -432 U^5 at U=h^(1/2)")
    print("BOUNDARY: frozen shear profile; the only bounded solution is zero amplitude")


if __name__ == "__main__":
    main()
