#!/usr/bin/env python3
"""Period-2 Lyapunov-Schmidt step for the upper-shear joint carrier.

The resonant ray is sigma(x)=(-1)^(x0+x2) times the integer witness of
a4d_joint_response_shear_witness_check.py. Quadratic self-interaction is
spatially constant. This certificate solves the resulting 24 constant link
equations at order u^2 and evaluates the cell metric Euler on that solution.

No torsion term or new action is introduced. A nonzero remaining metric
component is an obstruction to a joint vacuum, not a smooth-background NOGO.
"""

from __future__ import annotations

from itertools import combinations, product

import sympy as sp

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
Z4 = sp.zeros(4)
PAIRS = list(combinations(range(4), 2))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
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
SITES = list(product((0, 1), repeat=4))
SOURCE = [
    0, 24, 16, -24, -16, 0,
    -8, 0, -24, 16, -8, -16,
    0, -24, -16, 24, 16, 0,
    0, 0, 0, 0, 0, 0,
]
ZETA = [
    sp.Rational(-1, 2), sp.Rational(1, 2), sp.Rational(1, 2),
    sp.Rational(1, 2), sp.Rational(1, 2), 0,
    0, 0, 0, 0, 0, 0,
    sp.Rational(-1, 2), -1, sp.Rational(-1, 2), -1, sp.Rational(-1, 2), 0,
    -2, -1, 1, -1, 1, -2,
]


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def mul(left, right):
    return (
        left[0] * right[0],
        left[0] * right[1] + left[1] * right[0],
        left[0] * right[2] + left[1] * right[1] + left[2] * right[0],
    )


def smul(factor, jet):
    return tuple(factor * part for part in jet)


def inv(jet):
    return tuple(ETA * part.T * ETA for part in jet)


def eye():
    return (I4, Z4, Z4)


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


def link(site, role, zeta):
    generator = ROLES[role]
    shift_algebra = Z4
    for j in range(6):
        shift_algebra += zeta[6 * role + j] * GENERATORS[j]
    return (
        I4,
        sigma(site) * generator,
        sp.Rational(1, 2) * (generator * generator) + shift_algebra,
    )


def product(factors):
    out = eye()
    for factor in factors:
        out = mul(out, factor)
    return out


def plain_row(a, b):
    u, v = [j for j in range(4) if j not in (a, b)]
    return orientation(a, b) * wedge(SHEAR[:, u], SHEAR[:, v]).T * G2 * STAR


def varied_row(a, b, lift):
    u, v = [j for j in range(4) if j not in (a, b)]
    area = wedge(lift[:, u], SHEAR[:, v]) + wedge(SHEAR[:, u], lift[:, v])
    return orientation(a, b) * area.T * G2 * STAR


def factors_at(site, a, b, links):
    return [
        links[(site, a)],
        links[(shift(site, a), b)],
        inv(links[(shift(site, b), a)]),
        inv(links[(site, b)]),
    ]


def euler_jets(zeta):
    links = {(site, role): link(site, role, zeta) for site in SITES for role in range(4)}
    rows = [[0, 0, 0] for _ in range(24)]
    zero_gen = (I4 * 0, Z4, Z4)
    for site in SITES:
        for role in range(4):
            for j, generator in enumerate(GENERATORS):
                acc = [0, 0, 0]
                for a, b in PAIRS:
                    if role == a:
                        corners = [(site, 0), (shift(site, b), 2)]
                    elif role == b:
                        corners = [(shift(site, a), 1), (site, 3)]
                    else:
                        continue
                    row = plain_row(a, b)
                    for base, corner in corners:
                        facts = factors_at(base, a, b, links)
                        varied = list(facts)
                        gen = (generator, Z4, Z4)
                        if corner < 2:
                            varied[corner] = mul(facts[corner], gen)
                        else:
                            varied[corner] = mul(smul(-1, gen), facts[corner])
                        hol = product(facts)
                        dp = product(varied)
                        mid = mul(mul(inv(hol), dp), inv(hol))
                        for k in range(3):
                            curv = (dp[k] + mid[k]) / 2
                            acc[k] += (row * bivector(curv))[0]
                slot = 6 * role + j
                rows[slot] = [sp.expand(rows[slot][k] + acc[k]) for k in range(3)]
    return rows


def metric_u2(zeta):
    links = {(site, role): link(site, role, zeta) for site in SITES for role in range(4)}
    gram = SHEAR.T * ETA * SHEAR
    values = []
    for qa, qb in SYM:
        q = sp.zeros(4)
        q[qa, qb] = q[qb, qa] = 1
        lift = SHEAR * gram.inv() * q / 2
        total = 0
        for site in SITES:
            for a, b in PAIRS:
                row = varied_row(a, b, lift)
                facts = factors_at(site, a, b, links)
                hol = product(facts)
                curv = (hol[2] - inv(hol)[2]) / 2
                total += (row * bivector(curv))[0]
        values.append(sp.expand(total))
    return values


def main() -> None:
    pure = euler_jets([sp.Integer(0)] * 24)
    check("PURE_EULER_ORDERS_0_AND_1_VANISH", all(row[0] == 0 and row[1] == 0 for row in pure))
    check("PURE_QUADRATIC_SOURCE", [sp.Integer(row[2]) for row in pure] == [sp.Integer(x) for x in SOURCE])
    solved = euler_jets(ZETA)
    check("CONSTANT_CORRECTION_KILLS_QUADRATIC_EULER", all(row[2] == 0 for row in solved))
    pure_metric = metric_u2([sp.Integer(0)] * 24)
    corrected_metric = metric_u2(ZETA)
    expected = [0, 0, 0, 0, -16, 0, 0, 0, 0, 0]
    check("PURE_METRIC_JET", pure_metric == expected)
    check("REDUCED_METRIC_JET_UNCHANGED", corrected_metric == expected)
    check("VACUUM_CUTS_AMPLITUDE", corrected_metric[4] != 0 and all(
        corrected_metric[i] == 0 for i in range(10) if i != 4
    ))
    # Component 00 is the source fixed by the order already used in the memo.
    check("PREDECLARED_00_SOURCE_UNMATCHED", corrected_metric[0] == 0)
    print("RESULT_REDUCED_EQ_U2:", corrected_metric)
    print("RESULT_VACUUM: only u=0 solves E_K=O(u^3) and E_Q=O(u^4) together at this order")
    print("BOUNDARY: quadratic obstruction, not a smooth-background NOGO")


if __name__ == "__main__":
    main()
