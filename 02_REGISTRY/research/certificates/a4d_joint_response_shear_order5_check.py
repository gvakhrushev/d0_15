#!/usr/bin/env python3
"""Order-u^5 resonant coefficient of the period-2 shear connection equation.

The order-u^3 odd Euler is solvable. Its linearization has rank 20 and a
four-dimensional kernel containing the resonant witness. After the
order-u^4 constant correction that kills the even Euler, the witness
projection of the order-u^5 connection Euler equals -432 on a basis of the
witness-orthogonal kernel complement. The witness lies in the left kernel,
so this projection is a Fredholm obstruction and forces amplitude zero.

The order-u^2 metric jet stays the single point -16 e_q11. This is not a
smooth-background response NOGO.
"""
from __future__ import annotations

import importlib.util
from itertools import combinations, product
from pathlib import Path

import sympy as sp

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "cubic", HERE / "a4d_joint_response_shear_cubic_check.py"
)
cubic = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cubic)

ETA = sp.diag(1, -1, -1, -1)
I4 = sp.eye(4)
Z4 = sp.zeros(4)
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
SITES = list(product((0, 1), repeat=4))
SYM = [(a, b) for a in range(4) for b in range(a, 4)]
WITNESS = [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 0, -1, 1, 2, 1, 0, 1, 0, 0]
SOURCE = [
    0, 24, 16, -24, -16, 0,
    -8, 0, -24, 16, -8, -16,
    0, -24, -16, 24, 16, 0,
    0, 0, 0, 0, 0, 0,
]
ZETA = sp.sympify(
    "[-1/2, 1/2, 1/2, 1/2, 1/2, 0, 0, 0, 0, 0, 0, 0,"
    " -1/2, -1, -1/2, -1, -1/2, 0, -2, -1, 1, -1, 1, -2]"
)
S3 = sp.sympify(
    "[0, 32, -256/3, -32, 256/3, 0, 32, -4, 20/3, -60, 44/3, 32/3,"
    " 0, -32, 256/3, 32, -256/3, 0, 0, 0, 0, 0, 0, 0]"
)
S4 = sp.sympify(
    "[48, -3064/177, -7044/59, -1184/177, 2796/59, 0, 5864/177, -7784/177,"
    " 1812/59, -8132/177, -2392/177, -196/177, -84, 15056/177, 7136/177,"
    " -10808/177, -19880/177, -72, -48, 3196/59, 1468/177, 5300/59, 4904/177, 36]"
)
ETA_CLEAN = sp.sympify(
    "[96/59, 231/236, -911/708, 231/236, 151/708, 689/354, 0, 0, 3/2, 0, 3/2,"
    " -9/2, 101/118, 153/236, -1529/708, 153/236, 595/708, 175/118, -73/59,"
    " -1199/354, -22/59, 197/177, -22/59, 179/118]"
)
XI_CLEAN = sp.sympify(
    "[-1057/708, -452/177, -805/236, -983/177, -157/59, 47/118, -6, -9/4,"
    " -15/4, -21/4, -15/4, 9, -5305/708, 1013/236, 625/236, 32/59, 112/59,"
    " 979/236, 1259/708, 1033/354, -191/236, -280/177, -1253/236, 2927/708]"
)
K0 = sp.Matrix([0, 0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 0])
K1 = sp.Matrix([0, 0, 2, 0, 2, 1, 0, 0, 0, 0, 0, 0, 0, 0, -3, 0, -3, -1, 0, 1, 0, 1, 0, 0])
K2 = sp.Matrix([1, -2, 0, -2, 0, 0, 0, 0, 0, 0, 0, 0, -1, 3, 0, 3, 0, 0, 0, 0, 1, 0, 1, 0])
K3 = sp.Matrix([0, -1, 0, -1, 0, 0, 0, 0, 0, 0, 0, 0, -1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1])
XI_V = sp.Matrix([11, -6, -11, -6, -11, 0, 0, 0, 0, 0, 0, 0, 11, 12, 11, 12, 11, 0, -16, -3, -2, -3, -2, 14])
XI_K2 = sp.Matrix([0, -3, 2, -3, 2, 3, 0, 0, 0, 0, 0, 0, 0, 3, -4, 3, -4, 3, -6, -2, -1, -2, -1, 0])
XI_K3 = sp.Matrix(sp.sympify(
    "[0, -1, 1/2, -1, 1/2, 1, 0, 0, 0, 0, 0, 0, 0, 1, -1, 1, -1, 1, -1, 0, 1/2, 0, 1/2, -2]"
))
ACTIVE_ETA = [sp.Integer(0)] * 24
ACTIVE_XI = [sp.Integer(0)] * 24


def check(name: str, condition: bool) -> None:
    if not condition:
        raise AssertionError(name)
    print("PASS_" + name, flush=True)


def mul(left, right):
    n = len(left)
    out = []
    for i in range(n):
        acc = Z4 * 0
        for j in range(i + 1):
            acc += left[j] * right[i - j]
        out.append(acc)
    return tuple(out)


def smul(factor, jet):
    return tuple(factor * part for part in jet)


def inv(jet):
    return tuple(ETA * part.T * ETA for part in jet)


def eye(n):
    return (I4,) + tuple(Z4 for _ in range(n - 1))


def bivector(matrix):
    dressed = matrix * ETA
    return sp.Matrix([dressed[i, j] for i, j in PAIRS])


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
    out = Z4 * 0
    for coeff, generator in zip(coeffs, GENERATORS):
        out += coeff * generator
    return out


def plain_row(a, b):
    u, v = [j for j in range(4) if j not in (a, b)]
    area = sp.Matrix([
        SHEAR[i, u] * SHEAR[j, v] - SHEAR[j, u] * SHEAR[i, v] for i, j in PAIRS
    ]).T
    return orientation(a, b) * area * G2 * STAR


def euler_linear(coeffs, weighted):
    links = {}
    for site in SITES:
        for role in range(4):
            amp = algebra(coeffs[6 * role: 6 * role + 6])
            if weighted:
                amp *= sigma(site)
            links[(site, role)] = (I4, amp)
    even = [0] * 24
    odd = [0] * 24
    for site in SITES:
        sign = sigma(site)
        for role in range(4):
            for j, generator in enumerate(GENERATORS):
                acc = 0
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
                        gen = (generator, Z4)
                        if corner < 2:
                            varied[corner] = mul(facts[corner], gen)
                        else:
                            varied[corner] = mul(smul(-1, gen), facts[corner])
                        hol = eye(2)
                        dp = eye(2)
                        for factor, varied_factor in zip(facts, varied):
                            hol = mul(hol, factor)
                            dp = mul(dp, varied_factor)
                        mid = mul(mul(inv(hol), dp), inv(hol))
                        curv = (dp[1] + mid[1]) / 2
                        acc += (row * bivector(curv))[0]
                slot = 6 * role + j
                even[slot] += acc
                odd[slot] += sign * acc
    rows = odd if weighted else even
    return [sp.expand(entry) for entry in rows]


def full_link(site, role):
    generator = cubic.ROLES[role]
    sign = cubic.sigma(site)
    zed = cubic.algebra(cubic.ZETA[6 * role: 6 * role + 6])
    series = [cubic.Z4 for _ in range(cubic.N)]
    series[1] = sign * generator
    series[2] = zed
    series[3] = sign * cubic.algebra(ACTIVE_ETA[6 * role: 6 * role + 6])
    series[4] = cubic.algebra(ACTIVE_XI[6 * role: 6 * role + 6])
    step = cubic.eye()
    out = cubic.eye()
    for k in range(1, cubic.N):
        step = cubic.smul(sp.Rational(1, k), cubic.mul(step, tuple(series)))
        out = tuple(out[i] + step[i] for i in range(cubic.N))
    return out


def resonant(odd, order):
    value = 0
    for role in range(4):
        for j in range(6):
            value += cubic.WITNESS[role][j] * odd[6 * role + j][order]
    return sp.expand(value)


def metric_component(links, order, qa, qb):
    gram = cubic.SHEAR.T * cubic.ETA * cubic.SHEAR
    q = sp.zeros(4)
    q[qa, qb] = q[qb, qa] = 1
    lift = cubic.SHEAR * gram.inv() * q / 2
    total = 0
    for site in cubic.SITES:
        for a, b in cubic.PAIRS:
            u, v = [j for j in range(4) if j not in (a, b)]
            area = cubic.wedge(lift[:, u], cubic.SHEAR[:, v]) + cubic.wedge(
                cubic.SHEAR[:, u], lift[:, v]
            )
            row = cubic.orientation(a, b) * area.T * cubic.G2 * cubic.STAR
            facts = [
                links[(site, a)],
                links[(cubic.shift(site, a), b)],
                cubic.inv(links[(cubic.shift(site, b), a)]),
                cubic.inv(links[(site, b)]),
            ]
            hol = cubic.eye()
            for factor in facts:
                hol = cubic.mul(hol, factor)
            dual = cubic.inv(hol)
            curv = (hol[order] - dual[order]) / 2
            total += (row * cubic.bivector(curv))[0]
    return sp.expand(total)


def solved_jet(label, eta, xi, metric4):
    global ACTIVE_ETA, ACTIVE_XI
    ACTIVE_ETA = list(eta)
    ACTIVE_XI = list(xi)
    cubic.link = full_link
    even, odd = cubic.euler_parities()
    odd3 = [sp.expand(odd[slot][3]) for slot in range(24)]
    even4 = [sp.expand(even[slot][4]) for slot in range(24)]
    check(label + "_ODD3_ZERO", all(entry == 0 for entry in odd3))
    check(label + "_EVEN4_ZERO", all(entry == 0 for entry in even4))
    check(label + "_KERNEL5_MINUS_432", resonant(odd, 5) == -432)
    links = {(site, role): full_link(site, role) for site in cubic.SITES for role in range(4)}
    metric2 = [metric_component(links, 2, a, b) for a, b in SYM]
    metric4_values = [metric_component(links, 4, a, b) for a, b in SYM]
    check(label + "_METRIC2_FROZEN", metric2 == [0, 0, 0, 0, -16, 0, 0, 0, 0, 0])
    expected4 = [0, 0, 0, 0, metric4, 0, 0, 0, 0, 0]
    check(label + "_METRIC4", metric4_values == expected4)


def main():
    witness = sp.Matrix(WITNESS)
    check("WITNESS_IS_KERNEL_COMBINATION", sp.Matrix(2 * K0 + K1) == witness)
    zeta_even = euler_linear(list(ZETA), False)
    check("EVEN_OPERATOR_MATCHES_ZETA", zeta_even == [-sp.Integer(x) for x in SOURCE])
    check("ODD_WITNESS_IN_RIGHT_KERNEL", euler_linear(WITNESS, True) == [0] * 24)
    for name, vector in (("K0", K0), ("K1", K1), ("K2", K2), ("K3", K3)):
        check(name + "_IN_ODD_KERNEL", euler_linear(list(vector), True) == [0] * 24)
    eta_image = euler_linear(list(ETA_CLEAN), True)
    check("ETA_SOLVES_ORDER3", eta_image == [-entry for entry in S3])
    check(
        "ETA_ORTHOGONAL_TO_KERNEL",
        all(sp.Matrix(ETA_CLEAN).dot(vector) == 0 for vector in (K0, K1, K2, K3)),
    )
    pairings = []
    for index in range(24):
        direction = [0] * 24
        direction[index] = 1
        pairings.append(sp.Matrix(euler_linear(direction, True)).dot(witness))
    check("WITNESS_IN_LEFT_KERNEL", pairings == [0] * 24)
    xi_image = euler_linear(list(XI_CLEAN), False)
    check("XI_SOLVES_RECORDED_ORDER4", xi_image == [-entry for entry in S4])
    even_columns = []
    for index in range(24):
        direction = [0] * 24
        direction[index] = 1
        even_columns.append(euler_linear(direction, False))
    check("EVEN_OPERATOR_RANK_24", sp.Matrix(even_columns).rank() == 24)

    step = 8 * K0 - K1
    solved_jet("CLEAN", ETA_CLEAN, XI_CLEAN, sp.Rational(-7040, 177))
    solved_jet("V", sp.Matrix(ETA_CLEAN) + step, sp.Matrix(XI_CLEAN) + XI_V, sp.Rational(55264, 177))
    solved_jet("K2", sp.Matrix(ETA_CLEAN) + K2, sp.Matrix(XI_CLEAN) + XI_K2, sp.Rational(-7040, 177))
    solved_jet("K3", sp.Matrix(ETA_CLEAN) + K3, sp.Matrix(XI_CLEAN) + XI_K3, sp.Rational(-7040, 177))
    print("RESULT_REDUCED_KERNEL5: -432")
    print("RESULT_AMPLITUDE: the order-u^5 connection equation forces u=0")
    print("BOUNDARY: period-2 shear ansatz only; not a smooth-background response NOGO")


if __name__ == "__main__":
    main()
