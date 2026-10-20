#!/usr/bin/env python3
"""Exact changed-composition checks; no old geometry or gate-factory replay.

stdlib only. Checks remain active under -O. The proof, not this finite
calculation, supplies every-state and every-mesh quantifiers and admission.
"""

from collections import Counter, defaultdict
from dataclasses import dataclass
from fractions import Fraction as F
from itertools import product
from math import lcm


def need(ok, message):
    if not ok:
        raise RuntimeError(message)


@dataclass(frozen=True)
class Qp:
    a: F = F(0)
    b: F = F(0)

    def __post_init__(self):
        object.__setattr__(self, "a", F(self.a))
        object.__setattr__(self, "b", F(self.b))

    @staticmethod
    def lift(x):
        return x if isinstance(x, Qp) else Qp(x)

    def __add__(self, other):
        y = self.lift(other)
        return Qp(self.a + y.a, self.b + y.b)

    __radd__ = __add__

    def __neg__(self):
        return Qp(-self.a, -self.b)

    def __sub__(self, other):
        return self + -self.lift(other)

    def __rsub__(self, other):
        return self.lift(other) + -self

    def __mul__(self, other):
        y = self.lift(other)
        return Qp(self.a * y.a + self.b * y.b,
                  self.a * y.b + self.b * y.a - self.b * y.b)

    __rmul__ = __mul__

    def __truediv__(self, other):
        return Qp(self.a / F(other), self.b / F(other))

    def __pow__(self, n):
        need(isinstance(n, int) and n >= 0, "nonnegative integer power")
        out, base = Qp(1), self
        while n:
            if n & 1:
                out = out * base
            base = base * base
            n //= 2
        return out


P = Qp(0, 1)
ONE = Qp(1)
ZERO = Qp()


def poly_add(a, b):
    out = [ZERO] * max(len(a), len(b))
    for i, x in enumerate(a):
        out[i] = out[i] + x
    for i, x in enumerate(b):
        out[i] = out[i] + x
    return out


def poly_mul(a, b):
    out = [ZERO] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] = out[i + j] + x * y
    return out


def poly_scale(a, x):
    return [v * x for v in a]


def poly_pow(a, n):
    out = [ONE]
    for _ in range(n):
        out = poly_mul(out, a)
    return out


def neg(k):
    return tuple((-x) % 4 for x in k)


COS4 = (1, 0, -1, 0)
SIN4 = (0, 1, 0, -1)
E = [tuple(int(i == j) for i in range(4)) for j in range(4)]
DIFF = E + [tuple(E[j][r] - E[i][r] for r in range(4))
            for j in range(1, 4) for i in range(j)]


def dot4(x, y):
    return sum(a * b for a, b in zip(x, y)) % 4


PAIRS = [k for k in product(range(4), repeat=4) if k < neg(k)]


def score(k):
    return sum(COS4[dot4(k, d)] for d in DIFF)


FRAME = sorted(PAIRS, key=lambda k: (-score(k), k))[:64]


def gamma(x, y):
    d = tuple(a - b for a, b in zip(x, y))
    return F(sum(COS4[dot4(k, d)] for k in FRAME), 64)


def frame_check():
    need(len(PAIRS) == 120, "original order-four conjugate pairs")
    need(Counter(map(score, PAIRS)) == {6: 5, 4: 10, 2: 10, 0: 50, -2: 45},
         "deterministic frame score distribution")
    nums = [sum(COS4[dot4(k, d)] for k in FRAME) for d in DIFF]
    need(nums == [20, 10, 10, 9, 8, 8, 6, 9, 5, 5], "all stencil overlaps")
    # Full original reference128: integer characters before division by 8.
    rows = [[v for k in FRAME for v in (COS4[dot4(k, x)], SIN4[dot4(k, x)])]
            for x in product(range(4), repeat=4)]
    need(all(sum(v * v for v in row) == 64 for row in rows), "site norms")
    cols = list(zip(*rows))
    for i in range(128):
        for j in range(i, 128):
            actual = sum(x * y for x, y in zip(cols[i], cols[j]))
            need(actual == (128 if i == j else 0), "full reference128 Gram")
    return nums


def observable_check():
    sites = [(0, 0, 0, 0)] + E
    size, h, rho, scale, height = 256, F(1, 4), F(3, 2), F(2, 3), F(5, 7)
    g = [[F(0) for _ in range(4)] for _ in range(4)]
    g[0][1] = g[1][0] = scale**2
    g[1][1] = -scale**2 * height
    g[2][2] = g[3][3] = -scale**2
    m = [[F(0) for _ in range(10)] for _ in range(10)]
    for offset in (0, 5):
        for r in range(4):
            for t in range(4):
                for i, vi in ((offset + r + 1, 1), (offset, -1)):
                    for j, vj in ((offset + t + 1, 1), (offset, -1)):
                        m[i][j] += vi * vj * g[r][t]
    qop = [[F(size) * m[i][j] / (rho * h**2 * gamma(sites[i % 5], sites[j % 5]))
            for j in range(10)] for i in range(10)]
    psi = [F(1, 32), F(3, 64), F(1, 16), F(5, 64), F(3, 32),
           -F(1, 20), F(1, 30), F(1, 40), -F(1, 50), F(1, 60)]
    need(all(psi[i]**2 + psi[5 + i]**2 < 1 - F(619, 1000)
             for i in range(5)), "strict full CAR slack exists")
    expected = sum(g[r][t] * (psi[o+r+1]-psi[o]) * (psi[o+t+1]-psi[o])
                   for o in (0, 5) for r in range(4) for t in range(4)) / (rho*h*h)
    density = [[psi[i]*psi[j]*gamma(sites[i % 5], sites[j % 5])/size
                for j in range(10)] for i in range(10)]
    actual = sum(density[i][j] * qop[j][i] for i in range(10) for j in range(10))
    need(actual == expected, "LEFT-only live material observable with full PF/h/s")
    wrong = sum(density[i][j] * size * m[j][i] / (rho*h*h)
                for i in range(10) for j in range(10))
    need(wrong != expected, "hostile omitted-reference-overlap control")
    need(actual*rho != expected, "hostile omitted-inverse-PF control")
    need(all(qop[i][j] == qop[j][i] for i in range(10) for j in range(10)),
         "Hermitian LEFT observable")
    terms = []
    for i in range(10):
        terms += [qop[i][i]/2, -qop[i][i]/2]
        for j in range(i+1, 10):
            terms += [qop[i][j], -qop[i][j]/2, -qop[i][j]/2]
    l1 = sum(map(abs, terms))
    bound = F(512*size, 5) * sum(abs(x) for row in g for x in row) / (rho*h*h)
    need(l1 <= bound, "actual signed-involution L1 bound")
    den = lcm(*(x.denominator for x in terms))
    exponent = 0
    while 2**exponent < den*l1:
        exponent += 1
    normalization = F(2**exponent, den)
    weights = [abs(x)/normalization for x in terms]
    weights += [(1-sum(weights))/2]*2
    need(sum(weights) == 1 and min(weights) >= 0, "complete padded selector weights")
    need(all(x.denominator & (x.denominator-1) == 0 for x in weights),
         "fixture selector weights have common dyadic denominator")
    # Verify transposition/sign identity on active and two external labels.
    a, b, n = 2, 7, 12
    for i in range(n):
        for j in range(n):
            swap = int(i == (b if j == a else a if j == b else j))
            za = int(i == j) * (-1 if j == a else 1)
            zb = int(i == j) * (-1 if j == b else 1)
            desired = int((i, j) in ((a, b), (b, a)))
            need(swap-F(za+zb, 2) == desired, "full-space involution decomposition")
    return expected, normalization


TABLE = {
    (0, 0): (83349760, 49790975), (0, 1): (82325376, 49291265),
    (0, 2): (81285120, 48775167), (1, 0): (84922240, 50847745),
    (1, 1): (83881984, 50331647), (1, 2): (82825344, 49799169),
    (2, 0): (86528000, 51920895), (2, 1): (85471360, 51388417),
    (2, 2): (84397824, 50839551),
}


def beta(flags, sign=1):
    c = sign * P**2 / 64
    r = [P+c*x for x in flags]
    return 4*r[0]*r[1]*(ONE-r[2]*r[3])


def prefix_and_polynomial_check():
    l, u = F(309, 500), F(619, 1000)
    need(l*l+l-1 < 0 < u*u+u-1, "exact p enclosure")
    lo, hi = l-u*u/64, u+u*u/64
    need(0 < lo < hi < 1 and 0 < 4*lo*lo*(1-hi*hi), "lower beta interval")
    need(4*hi*hi*(1-lo*lo) < 1, "upper beta interval")
    leaves = defaultdict(lambda: ZERO)
    for word in product((0, 1), repeat=7):
        weight = 0
        for length, bit in enumerate(word, 1):
            weight += 1+bit
            if weight >= 7:
                break
        leaves[word[:length]] += P**(7+sum(word))
    counts = Counter(sum(1+x for x in word) for word in leaves)
    need(counts == {7: 21, 8: 13}, "all first-passage leaves, including weight8")
    need(sum(leaves.values(), ZERO) == ONE, "complete prefix partition")
    for word, probability in leaves.items():
        need(probability == P**sum(1+x for x in word), "coherent unused suffix summed")
    for flags in product((-1, 1), repeat=4):
        i, j = sum(x == 1 for x in flags[:2]), sum(x == 1 for x in flags[2:])
        a, b = TABLE[i, j]
        need(0 < a < 88080384 and 0 < b < 54525952, "strict complete capacities")
        compiled = (a*P**7+b*P**8)/2**22
        need(compiled == beta(flags), "exact four-bit coefficient table")
        ar, br = TABLE[2-i, 2-j]
        need((ar*P**7+br*P**8)/2**22 == beta(flags, -1), "opposite native sign")
    for sign in (-1, 1):
        actual = [ZERO]*5
        for flags in product((-1, 1), repeat=4):
            k = sum(x == 1 for x in flags)
            law = poly_mul(poly_pow([ZERO, ONE], k), poly_pow([ONE, -ONE], 4-k))
            actual = poly_add(actual, poly_scale(law, beta(flags, sign)))
        c = sign * P**2/64
        r = [P-c, 2*c]
        target = poly_add(poly_scale(poly_pow(r, 2), 4), poly_scale(poly_pow(r, 4), -4))
        need(actual == target, "exact full four-copy response polynomial")
    return len(leaves)


def source_and_degree_check(normalization):
    for sign in (-1, 1):
        eta2 = 1/(64*normalization)
        kappa = sign * P**2 * eta2
        r = [P, kappa]
        b = poly_add(poly_scale(poly_pow(r, 2), 4), poly_scale(poly_pow(r, 4), -4))
        need(b[0] == 4*P**3 and ONE-b[0] == P**6, "original null response")
        need(b[1] == 8*sign*P**6*eta2, "actual normalization in first material source")
        aa, bb, cc = F(5, 13), F(-2, 7), F(3, 11)
        q = [Qp(cc), Qp(bb), Qp(aa)]
        rq = poly_add([P], poly_scale(q, kappa))
        response = poly_add(poly_scale(poly_pow(rq, 2), 4),
                            poly_scale(poly_pow(rq, 4), -4))
        need(len(response) == 9 and response[8] == -4*kappa**4*aa**4,
             "nonzero eighth scalar power on actual top/slack curve")
        need(response[8]/256 == -(kappa**4)*aa**4/64 and response[8] != ZERO,
             "exact nonzero eighth Fourier coefficient")


def main():
    overlaps = frame_check()
    response, normalization = observable_check()
    leaves = prefix_and_polynomial_check()
    source_and_degree_check(normalization)
    print("PASS original Fourier128 frame, all10 nonzero overlaps:", overlaps)
    print("PASS LEFT-only overlap/PF/h/s normalization and hostile omissions; q =", response)
    print("PASS coherent full prefix partition:", leaves, "leaves; all16 exact coefficients and response")
    print("PASS exact null source factor and eighth-harmonic copy-order coefficient")
    print("Scope: changed algebra only; no native input, Book binding or full42 admission inferred.")


if __name__ == "__main__":
    main()
