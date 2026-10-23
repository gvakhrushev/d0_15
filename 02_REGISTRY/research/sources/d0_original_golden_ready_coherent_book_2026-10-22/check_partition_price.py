#!/usr/bin/env python3
"""Narrow same-carrier Book partition comparison; standard library only.

This checks NEW algebra and its native coefficient application. It consumes the
owned n=20 outcome multiplicities, not the full128 instrument or geometry suite.
No files are written. Decimal logarithms are evaluations, not interval proofs;
the uniform rational lower bound is separately certified in Q(p), p^2+p=1.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
import json


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def padd(a, b):
    c = dict(a)
    for key, value in b.items():
        c[key] = c.get(key, 0) + value
    return {key: value for key, value in c.items() if value}


def pscale(a, n):
    return {key: value * n for key, value in a.items() if value * n}


def pmul(a, b):
    c = {}
    for ka, va in a.items():
        for kb, vb in b.items():
            key = tuple(x + y for x, y in zip(ka, kb))
            c[key] = c.get(key, 0) + va * vb
    return {key: value for key, value in c.items() if value}


def psub(a, b):
    return padd(a, pscale(b, -1))


class Golden:
    """Exact a+b*p, with its positive real embedding p=(sqrt(5)-1)/2."""
    def __init__(self, a=0, b=0):
        self.a, self.b = F(a), F(b)

    @staticmethod
    def cast(x):
        return x if isinstance(x, Golden) else Golden(x)

    def __add__(self, other):
        o = self.cast(other)
        return Golden(self.a + o.a, self.b + o.b)

    __radd__ = __add__

    def __neg__(self):
        return Golden(-self.a, -self.b)

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        o = self.cast(other)
        return Golden(self.a * o.a + self.b * o.b,
                      self.a * o.b + self.b * o.a - self.b * o.b)

    __rmul__ = __mul__

    def __truediv__(self, other):
        o = self.cast(other)
        norm = o.a * o.a - o.a * o.b - o.b * o.b
        require(norm != 0, "zero Golden denominator")
        return self * Golden((o.a - o.b) / norm, -o.b / norm)

    def __pow__(self, n):
        require(isinstance(n, int) and n >= 0, "nonnegative integer power")
        result, base = Golden(1), self
        while n:
            if n % 2:
                result = result * base
            base = base * base
            n //= 2
        return result

    def sign(self):
        x, y = 2 * self.a - self.b, self.b
        sign = lambda q: (q > 0) - (q < 0)
        if not y:
            return sign(x)
        if not x or sign(x) == sign(y):
            return sign(y)
        return sign(x) * sign(x * x - 5 * y * y)

    def __eq__(self, other):
        o = self.cast(other)
        return self.a == o.a and self.b == o.b


def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]


def mm(a, b):
    return [[sum(x * y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def transpose(a):
    return list(map(list, zip(*a)))


def msub(a, b):
    return [[x - y for x, y in zip(ra, rb)] for ra, rb in zip(a, b)]


def blocks(bs):
    return [[bs[i // 3][i % 3][j % 3] if i // 3 == j // 3 else F(0)
             for j in range(3 * len(bs))] for i in range(3 * len(bs))]


def determinant(a):
    a = [row[:] for row in a]
    result = F(1)
    for j in range(len(a)):
        pivot = next((i for i in range(j, len(a)) if a[i][j]), None)
        if pivot is None:
            return F(0)
        if pivot != j:
            a[j], a[pivot] = a[pivot], a[j]
            result = -result
        v = a[j][j]
        result *= v
        for i in range(j + 1, len(a)):
            ratio = a[i][j] / v
            for k in range(j + 1, len(a)):
                a[i][k] -= ratio * a[j][k]
    return result


def partitions(n):
    if n == 0:
        yield []
    else:
        for old in partitions(n - 1):
            for i in range(len(old)):
                yield old[:i] + [old[i] + [n - 1]] + old[i + 1:]
            yield old + [[n - 1]]


def jadd(a, b):
    return tuple(x + y for x, y in zip(a, b))


def jmul(a, b):
    return (a[0] * b[0], a[1] * b[0] + a[0] * b[1],
            a[2] * b[0] + a[0] * b[2],
            a[3] * b[0] + a[1] * b[2] + a[2] * b[1] + a[0] * b[3])


def run():
    z = F(1, 2 ** 20)
    one, aa, bb, zz = ({(0, 0, 0): 1}, {(1, 0, 0): 1},
                       {(0, 1, 0): 1}, {(0, 0, 1): 1})
    dp = lambda q: psub(one, pscale(pmul(zz, pmul(q, psub(one, q))), 4))
    lhs = psub(dp(padd(aa, bb)), pmul(dp(aa), dp(bb)))
    rhs = pscale(pmul(pmul(pmul(zz, aa), bb),
                     psub(one, pscale(pmul(zz, pmul(psub(one, aa), psub(one, bb))), 2))), 8)
    require(lhs == rhs, "general merge identity")
    nk = pscale(pmul(zz, psub(one, pscale(aa, 2))), 4)
    derivative_num = padd(pscale(pmul(zz, dp(aa)), -8), pmul(nk, nk))
    derivative_expected = pscale(pmul(zz, padd(psub(one, pscale(zz, 2)),
                                pscale(pmul(zz, pmul(aa, psub(one, aa))), 4))), -8)
    require(derivative_num == derivative_expected, "general decreasing-source identity")

    d = lambda q: 1 - 4 * z * q * (1 - q)
    k = lambda q: 4 * z * (1 - 2 * q) / d(q)
    kp = lambda q: -8 * z * (1 - 2 * z + 4 * z * q * (1 - q)) / d(q) ** 2
    omega = [F(1, 3), F(2, 3), F(2, 3)]
    p0 = [[a * b for b in omega] for a in omega]
    proj = blocks([p0, p0, p0])
    require(mm(proj, proj) == proj and sum(proj[i][i] for i in range(9)) == 3, "common projector")
    reflection = lambda inds: [[F((1 - 2 * (i in inds)) if i == j else 0)
                               for j in range(3)] for i in range(3)]
    programmes = [(blocks([reflection([0]), reflection([1]), reflection([2])]),
                   [F(1, 9), F(4, 9), F(4, 9)]),
                  (blocks([reflection([0, 1]), reflection([2]), eye(3)]),
                   [F(5, 9), F(4, 9), F(0)])]
    dets = []
    for unitary, qs in programmes:
        require(mm(transpose(unitary), unitary) == eye(9), "all nine unitary columns")
        feedback = mm(mm(mm(mm(proj, transpose(unitary)), msub(eye(9), proj)), unitary), proj)
        expected = blocks([[[4 * q * (1 - q) * x for x in row] for row in p0] for q in qs])
        require(feedback == expected, "literal complete complement")
        dets.append(determinant(msub(eye(9), [[z * x for x in row] for row in feedback])))
        product = F(1)
        for q in qs:
            product *= d(q)
        require(dets[-1] == product, "full determinant including six zero modes")
    require(dets[1] > dets[0], "same-carrier strict price ordering")

    weights = [F(1, 12), F(1, 6), F(1, 8), F(1, 8), F(1, 5), F(3, 10)]
    category = [0, 0, 1, 1, 2, 2]
    all_partitions = list(partitions(6))
    valid = [part for part in all_partitions
             if all(len({category[i] for i in block}) == 1 for block in part)]
    products = []
    for part in valid:
        product = F(1)
        for block in part:
            product *= d(sum(weights[i] for i in block))
        products.append(product)
    best = max(products)
    minimizers = [part for part, product in zip(valid, products) if product == best]
    require(len(all_partitions) == 203 and len(valid) == 8, "complete small partition fixture")
    require(minimizers == [[[0, 1], [2, 3], [4, 5]]], "unique task-preserving minimum")
    require(best < d(sum(weights)) == 1, "dropping task is a different cheaper programme")

    aj = tuple(map(F, [F(1, 5), F(1, 11), F(-2, 13), F(3, 17)]))
    bj = tuple(map(F, [F(2, 7), F(-3, 19), F(5, 23), F(-7, 29)]))
    def minus_log_jet(q):
        iq = (1 - q[0], -q[1], -q[2], -q[3])
        dd = jadd((F(1), F(0), F(0), F(0)), tuple(-4 * z * x for x in jmul(q, iq)))
        return (-dd[1] / dd[0], -dd[3] / dd[0] + dd[1] * dd[2] / dd[0] ** 2)
    ja, jb, js = minus_log_jet(aj), minus_log_jet(bj), minus_log_jet(jadd(aj, bj))
    a, b, s = aj[0], bj[0], aj[0] + bj[0]
    first = (k(a) - k(s)) * aj[1] + (k(b) - k(s)) * bj[1]
    mixed = ((kp(a) - kp(s)) * aj[1] * aj[2] + (kp(b) - kp(s)) * bj[1] * bj[2]
             - kp(s) * (aj[1] * bj[2] + bj[1] * aj[2])
             + (k(a) - k(s)) * aj[3] + (k(b) - k(s)) * bj[3])
    require(ja[0] + jb[0] - js[0] == first, "independent exact first chain rule")
    require(ja[1] + jb[1] - js[1] == mixed, "independent exact mixed chain rule")
    require(2 * kp(F(1, 4)) < 0 < 2 * kp(F(1, 4)) - 4 * kp(F(1, 2)), "indefinite field Hessian")
    require(F(2, 7) * (k(0) - k(F(1, 3))) > 0, "dark probability birth has second source")

    p = Golden(0, 1)
    require(p * p + p == 1 and (2 * p * p - p).sign() > 0, "Golden recurrence interval")
    require(p ** 2 * (2 * p ** 2) * (1 - 2 * p ** 2) == 2 * p ** 7, "uniform merged mass bound")
    pi = p ** 23
    ready = 2 * 10946 * pi
    require(6765 * p ** 21 + 10946 * (p ** 22 + p ** 24 + 2 * pi) == 1, "owned complete native mass")
    require(6765 + 6 * 10946 == 72441, "owned complete fine label count")
    radius = 16 * z * p ** 7 * (1 - 2 * z)
    rational_lower = F(6726908, 10 ** 11)
    require((128 * radius / (1 + radius) - rational_lower).sign() > 0, "rigorous rational uniform price bound")
    ell = 4 * p ** 3
    r0 = 1 - (1 - z * ell) * (1 - z * ell * (1 + p ** 6))
    g_fine = ready / 2 * (k(pi * r0) - k(pi * (1 - r0)))
    g_three = ready / 2 * (k(ready * r0) - k(ready * (1 - r0)))
    require(g_fine.sign() > 0 and (g_three - g_fine).sign() > 0, "exact native all42 gain ordering")

    values = []
    for precision in (80, 100):
        with localcontext() as ctx:
            ctx.prec = precision
            pd, zd = (Decimal(5).sqrt() - 1) / 2, Decimal(2) ** -20
            q, ad, ld = pd ** 23, 2 * 10946 * pd ** 23, 4 * pd ** 3
            rd = 1 - (1 - zd * ld) * (1 - zd * ld * (1 + pd ** 6))
            j = lambda t: -(1 - 4 * zd * t * (1 - t)).ln()
            kd = lambda t: 4 * zd * (1 - 2 * t) / (1 - 4 * zd * t * (1 - t))
            fine = 128 * (6765 * j(pd ** 21) + 10946 * (j(pd ** 22) + j(pd ** 24)
                          + 2 * j(q * rd) + 2 * j(q * (1 - rd))))
            three = 128 * (j(1 - ad) + j(ad * (1 - rd)) + j(ad * rd))
            lower = 128 * (1 + 16 * zd * pd ** 7 * (1 - 2 * zd)).ln()
            values.append([fine, three, fine - three, lower,
                           ad / 2 * (kd(q * rd) - kd(q * (1 - rd))),
                           ad / 2 * (kd(ad * rd) - kd(ad * (1 - rd)))])
    require(all(abs(a - b) < Decimal('1e-70') for a, b in zip(*values)), "Decimal precision stability")
    return {
        "scope": "exact finite same-carrier partition comparison; conditional physical application",
        "exact_checks": {
            "merge_polynomial_and_source_derivative": True,
            "common_9d_carrier_all_columns_and_full_determinants": True,
            "coarse_to_fine_determinant_ratio": str(dets[1] / dets[0]),
            "all_fixture_partitions": len(all_partitions), "task_preserving_partitions": len(valid),
            "unique_task_preserving_minimum": True, "first_and_mixed_source_chain_rule": True,
            "field_hessian_indefinite": True, "dark_birth_second_source": True,
            "native_mass_and_gain_order_in_Qp": True,
            "uniform_gap_strict_rational_lower": str(rational_lower),
        },
        "decimal_evaluation_not_interval_certificate": dict(zip(
            ["J_FINE_n20", "J3_n20", "gap_n20", "uniform_symbolic_log_bound", "g_FINE", "g3"],
            [format(value, '.65g') for value in values[1]])),
        "retained_open_conditions": ["native task and active cut", "actual marking programme valuation",
                                     "complete Info and clock/work", "independent input equations",
                                     "full source and refinement"],
        "GR_closed": False,
    }


if __name__ == '__main__':
    print(json.dumps(run(), indent=2, sort_keys=True))
