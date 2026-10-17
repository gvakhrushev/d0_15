#!/usr/bin/env python3
"""Bounded reproducible controls for the actual golden AF information/source gate.

Runs only standard-library finite calculations. Does not execute the original v8
instrument, prove Book physical Info selection, verify the full AF regular GNS,
or substitute for the original all-ten raw h^-2 Euler target.
"""
from collections import Counter
from decimal import Decimal, getcontext
from fractions import Fraction
from itertools import product
from math import comb, factorial, log, sqrt, prod

getcontext().prec = 90
PHI_D = (Decimal(1) + Decimal(5).sqrt()) / 2
P_D = 1 / PHI_D
PHI = float(PHI_D)
P = float(P_D)
ELL = log(PHI)
BPHI = 2 + log(2) / ELL
E0 = P * P


def family(e: float):
    w = P ** 1.5
    a = w * sqrt(1 - e)
    b = sqrt(e / 2)
    da = -w / (2 * sqrt(1 - e))
    db = 1 / (2 * sqrt(2 * e))
    q = [(a + b) ** 2, (a - b) ** 2, P**3 * (1 - e),
         P**4 * (1 - e), P**4 * (1 - e)]
    dq = [2 * (a + b) * (da + db), 2 * (a - b) * (da - db),
          -P**3, -P**4, -P**4]
    return q, dq


def scalar_metrics(q, dq):
    mu = [P**3] * 3 + [P**4] * 2
    cost = -sum(x * log(m) for x, m in zip(q, mu)) / ELL
    h = -sum(x * log(x) for x in q) / ELL
    d = cost - h
    costprime = -sum(x * log(m) for x, m in zip(dq, mu)) / ELL
    hprime = -sum(x * log(y) for x, y in zip(dq, q)) / ELL
    dprime = costprime - hprime
    return cost, h, d, costprime, hprime, dprime


def golden_encoder(start: Fraction, mass: Fraction):
    """Find native F/R cylinder around the assigned midpoint.

    Decimal arithmetic at 90 significant digits is more than sufficient
    for N<=5 in this bounded checker. The mathematical theorem is exact.
    """
    mid = start + mass / 2
    midpoint = Decimal(mid.numerator) / Decimal(mid.denominator)
    lower = Decimal(start.numerator) / Decimal(start.denominator)
    upper = Decimal((start + mass).numerator) / Decimal((start + mass).denominator)
    target = (upper - lower) / 2
    lo, width = Decimal(0), Decimal(1)
    word = []
    cost = 0
    for _ in range(250):
        if width <= target:
            assert lo >= lower - Decimal("1e-70")
            assert lo + width <= upper + Decimal("1e-70")
            return "".join(word), cost
        lf = P_D * width
        if midpoint < lo + lf:
            word.append("F")
            cost += 1
            width = lf
        else:
            word.append("R")
            cost += 2
            lo += lf
            width *= P_D * P_D
    raise AssertionError("golden encoder failed to terminate")


def universal_prob(seq: tuple[int, ...], k: int):
    N = len(seq)
    n = Counter(seq)
    M = factorial(N) // prod(factorial(n[i]) for i in range(k))
    T = comb(N + k - 1, k - 1)
    return Fraction(1, T * M)


def test_one_length(N: int, q, dq):
    K = len(q)
    codes = []
    integral = Fraction(0)
    expected = 0.0
    derivative = 0.0
    mass = 0.0
    max_overhead = 0.0
    for tup in product(range(K), repeat=N):
        Q = universal_prob(tup, K)
        code, cost = golden_encoder(integral, Q)
        qseq = 1.0
        score = 0.0
        for y in tup:
            qseq *= q[y]
            score += dq[y] / q[y]
        expected += qseq * cost
        derivative += qseq * score * cost
        mass += qseq
        max_overhead = max(max_overhead, cost + log(float(Q)) / ELL)
        codes.append(code)
        integral += Q

    assert integral == 1
    assert abs(mass - 1) < 1e-11
    codes.sort()
    assert all(not right.startswith(left) for left, right in zip(codes, codes[1:]))
    assert max_overhead <= BPHI + 1e-10

    _, H, _, _, Hp, _ = scalar_metrics(q, dq)
    assert 0 <= expected / N - H < (log(comb(N + K - 1, K - 1)) / ELL + BPHI) / N + 1e-10
    return {
        "N": N,
        "codewords": len(codes),
        "cost_per_symbol": expected / N,
        "cost_source_per_symbol": derivative / N,
        "Shannon": H,
        "Shannon_source": Hp,
        "source_gap": derivative / N - Hp,
        "max_prefix_overhead": max_overhead,
    }


def test_native_one_way_obstruction():
    """Exact symbolic formula plus bounded numerical normalized-source control."""
    last_lower = 0.0
    for t in (0.1, 0.03, 0.01, 0.001):
        e_a = P * P
        e_b = e_a * (1 + t * t)
        diff = sqrt((sqrt(1 - e_a) - sqrt(1 - e_b)) ** 2
                    + (sqrt(e_a) - sqrt(e_b)) ** 2)
        lower = 0.5 * diff / (t * t)
        assert lower + 1e-9 >= P / 4
        assert lower < 0.2
        last_lower = lower
    assert abs(last_lower - sqrt(P)/4) < 1e-6
    assert abs(sqrt(P)/4 - 0.19653784443935582) < 1e-12


def main():
    q, dq = family(E0)
    assert abs(sum(q) - 1.0) < 1e-12
    assert abs(sum(dq)) < 1e-12
    C, H, D, Cp, Hp, Dp = scalar_metrics(q, dq)
    assert abs(Dp - 0.5848452975169395) < 1e-10
    assert abs(Hp + 0.8766413650175716) < 1e-10
    assert abs(Dp - Hp - 1.461486662534511) < 1e-10
    assert abs(Cp + 2 * P**4) < 1e-11
    assert abs(D - (C-H)) < 1e-12
    print("AF GOLDEN ORIGINAL e=p^2")
    print(f"C={C:.12f}; H={H:.12f}; D={D:.12f}")
    print(f"dC={Cp:+.12f}; dH={Hp:+.12f}; dD={Dp:+.12f}")
    print(f"ACTUAL BRANCH LIKELIHOOD SOURCE MISMATCH={Dp-Hp:+.12f}")
    results = [test_one_length(N, q, dq) for N in (1, 2, 3, 4, 5)]
    for x in results:
        print("N={N} words={codewords} rate={cost_per_symbol:.12f} "
              "source={cost_source_per_symbol:+.12f} "
              "source_gap={source_gap:+.12f}".format(**x))
    assert abs(results[-1]["source_gap"]) < abs(results[0]["source_gap"])
    assert results[-1]["cost_per_symbol"] > H
    test_native_one_way_obstruction()
    print("PASS: complete golden coding, prefix, normalization, C1 source and direct one-way gate obstruction")
    print("SCOPE: no native AF gate admission, Info-law selection, full Lorentz or exact GR roots")


if __name__ == "__main__":
    main()
