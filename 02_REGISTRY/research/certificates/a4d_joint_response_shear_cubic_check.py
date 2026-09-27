#!/usr/bin/env python3
"""Higher-order Euler jet of the period-2 shear ansatz.

The constant correction that kills the order-u^2 connection Euler is kept.
The resonant kernel projection of the resulting Euler vanishes through order
u^5, while the odd range at order u^3 and the even range at order u^4 do not.
Those range sources cannot change the already computed order-u^2 metric jet.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
Z4 = sp.zeros(4)
N = 6
PAIRS = list(combinations(range(4), 2))
GENERATORS = []
for j in (1, 2, 3):
    matrix = sp.zeros(4)
    matrix[0, j] = matrix[j, 0] = 1
    GENERATORS.append(matrix)
for a, b in list(PAIRS)[3:]:
    matrix = sp.zeros(4)
    matrix[a, b], matrix[b, a] = 1, -1
    GENERATORS.append(matrix)
G2 = sp.diag(*(ETA[a, a] * ETA[b, b] for a, b in PAIRS))
STAR = sp.zeros(6)
for col, (row, sign) in enumerate([(5, -1), (4, 1), (3, -1), (2, 1), (1, -1), (0, 1)]):
    STAR[row, col] = sign
SHEAR = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
ROLES = [
    GENERATORS[5],
    Z4,
    -GENERATORS[2] - GENERATORS[4] + GENERATORS[5],
    2 * GENERATORS[0] + GENERATORS[1] + GENERATORS[3],
]
WITNESS = [
    [0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0],
    [0, 0, -1, 0, -1, 1],
    [2, 1, 0, 1, 0, 0],
]
ZETA = [
    sp.Rational(-1, 2), sp.Rational(1, 2), sp.Rational(1, 2),
    sp.Rational(1, 2), sp.Rational(1, 2), 0,
    0, 0, 0, 0, 0, 0,
    sp.Rational(-1, 2), -1, sp.Rational(-1, 2), -1, sp.Rational(-1, 2), 0,
    -2, -1, 1, -1, 1, -2,
]
SITES = list(product((0, 1), repeat=4))


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def mul(left, right):
    out = []
    for i in range(N):
        acc = sp.zeros(4)
        for j in range(i + 1):
            acc += left[j] * right[i - j]
        out.append(acc)
    return tuple(out)


def smul(factor, jet):
    return tuple(factor * part for part in jet)


def inv(jet):
    return tuple(ETA * part.T * ETA for part in jet)


def eye():
    return (I4,) + tuple(Z4 for _ in range(N - 1))


def bivector(matrix):
    dressed = matrix * ETA
    return sp.Matrix([dressed[i, j] for i, j in PAIRS])


def wedge(left, right):
    return sp.Matrix([left[i] * right[j] - left[j] * right[i] for i, j in PAIRS])


def orientation(a, b):
    rest = [j for j in range(4) if j not in (a, b)]
    seq = [a, b] + rest
    return (-1) ** sum(seq[i] > seq[j] for i, j in combinations(range(4), 2))


def shift(site, role):
    out = list(site)
    out[role] ^= 1
    return tuple(out)


def sigma(site):
    return 1 if (site[0] + site[2]) % 2 == 0 else -1


def algebra(coeffs):
    out = Z4
    for coeff, generator in zip(coeffs, GENERATORS):
        out += coeff * generator
    return out


def link(site, role):
    generator = ROLES[role]
    sign = sigma(site)
    zed = algebra(ZETA[6 * role: 6 * role + 6])
    series = [Z4] * N
    series[1] = sign * generator
    series[2] = zed
    step = eye()
    out = eye()
    for k in range(1, N):
        step = smul(sp.Rational(1, k), mul(step, tuple(series)))
        out = tuple(out[i] + step[i] for i in range(N))
    return out


def product(factors):
    out = eye()
    for factor in factors:
        out = mul(out, factor)
    return out


def plain_row(a, b):
    u, v = [j for j in range(4) if j not in (a, b)]
    return orientation(a, b) * wedge(SHEAR[:, u], SHEAR[:, v]).T * G2 * STAR


def euler_parities():
    links = {(site, role): link(site, role) for site in SITES for role in range(4)}
    even = [[0] * N for _ in range(24)]
    odd = [[0] * N for _ in range(24)]
    for site in SITES:
        sign = sigma(site)
        for role in range(4):
            for j, generator in enumerate(GENERATORS):
                acc = [0] * N
                for a, b in PAIRS:
                    if role == a:
                        corners = [(site, 0), (shift(site, b), 2)]
                    elif role == b:
                        corners = [(shift(site, a), 1), (site, 3)]
                    else:
                        continue
                    row = plain_row(a, b)
                    for base, corner in corners:
                        facts = [
                            links[(base, a)],
                            links[(shift(base, a), b)],
                            inv(links[(shift(base, b), a)]),
                            inv(links[(base, b)]),
                        ]
                        varied = list(facts)
                        gen = (generator,) + tuple(Z4 for _ in range(N - 1))
                        if corner < 2:
                            varied[corner] = mul(facts[corner], gen)
                        else:
                            varied[corner] = mul(smul(-1, gen), facts[corner])
                        hol = product(facts)
                        dp = product(varied)
                        mid = mul(mul(inv(hol), dp), inv(hol))
                        for k in range(N):
                            curv = (dp[k] + mid[k]) / 2
                            acc[k] += (row * bivector(curv))[0]
                slot = 6 * role + j
                for k in range(N):
                    even[slot][k] += acc[k]
                    odd[slot][k] += sign * acc[k]
    return even, odd


def main() -> None:
    even, odd = euler_parities()
    kernel = []
    for k in range(N):
        value = 0
        for role in range(4):
            for j in range(6):
                value += WITNESS[role][j] * odd[6 * role + j][k]
        kernel.append(sp.expand(value))
    check("KERNEL_PROJECTION_VANISHES_THROUGH_U5", kernel == [0] * N)
    check("ODD_ORDER_3_RANGE_IS_REAL", sp.expand(odd[1][3]) == 32)
    check("EVEN_ORDER_4_RANGE_IS_REAL", sp.expand(even[1][4]) == sp.Rational(-4, 3))
    check("QUADRATIC_EVEN_EULER_STAYS_ZERO", all(sp.expand(row[2]) == 0 for row in even))
    print("RESULT_KERNEL_EULER: 0 through u^5")
    print("RESULT_RANGE: odd u^3 and even u^4 sources remain")
    print("BOUNDARY: higher range is unsolved; it cannot cancel the order-u^2 metric defect")


if __name__ == "__main__":
    main()
