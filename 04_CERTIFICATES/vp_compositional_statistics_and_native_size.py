"""Exact checks for compositional statistics, U-statistic variance, and native size limits.

Uses only the Python standard library.
Checks:
1. Exact unbiased U-statistic variance formula matches sample enumeration for L=2..5.
2. Invariance of all moments and adaptive experiment distributions under scale multiplication.
3. Primitive 231-atom source has identical P2 = 371/1089 and strictly smaller P3.
4. Tensor product K(9,11,13) x K(9,11,13) has competitor partition with identical N=1089,
   C=137641, but strictly smaller sum of cubes (by 110592), proving P3 minimization is not
   automatically tensor-compositional without preparation factorization.
"""

from fractions import Fraction as F
from functools import reduce
from itertools import combinations, product
from math import comb, gcd


def probabilities(parts):
    return tuple(F(n, sum(parts)) for n in parts)


def moment(weights, k):
    return sum(w**k for w in weights)


def predicted_variance(weights, sample_size):
    p2, p3 = moment(weights, 2), moment(weights, 3)
    L = sample_size
    return F(2, L * (L - 1)) * p2 * (1 - p2) + F(4 * (L - 2), L * (L - 1)) * (
        p3 - p2 * p2
    )


def exact_sample_variance(weights, sample_size):
    L = sample_size
    pairs = tuple(combinations(range(L), 2))
    mean = square_mean = F(0)
    for sample in product(range(len(weights)), repeat=L):
        chance = F(1)
        for x in sample:
            chance *= weights[x]
        estimate = F(sum(sample[a] == sample[b] for a, b in pairs), comb(L, 2))
        mean += chance * estimate
        square_mean += chance * estimate**2
    assert mean == moment(weights, 2)
    return square_mean - mean**2


def main():
    core = (9, 11, 13)
    w = probabilities(core)
    kappa = F(371, 1089)
    assert moment(w, 2) == kappa
    assert moment(w, 3) - kappa * kappa == F(2840, 1185921)

    checks = 0
    for parts in [(1, 1), (1, 2, 3), core, (3, 4, 11, 15)]:
        p = probabilities(parts)
        for L in range(2, 6):
            assert exact_sample_variance(p, L) == predicted_variance(p, L)
            checks += 1

    for scale in (1, 2, 3, 7):
        assert probabilities(tuple(scale * n for n in core)) == w
    for N in range(1, 200):
        assert ((kappa * N * N).denominator == 1) == (N % 33 == 0)
    assert sum(n * n for n in (3, 4, 11, 15)) == 371

    larger = (61, 83, 87)
    assert reduce(gcd, larger) == 1
    assert sum(larger) == 231
    assert moment(probabilities(larger), 2) == kappa
    assert moment(w, 3) - moment(probabilities(larger), 3) == F(320, 1369599)
    for L in (3, 4, 10, 100):
        assert predicted_variance(probabilities(larger), L) < predicted_variance(
            w, L
        )

    for t in (F(0), F(-1), F(-2), F(-3), F(-4), F(-11, 3), F(-37, 10)):
        D = 1 + t + t * t
        x, y, z = 2 * (1 - t * t) / D, 2 * t * (t + 2) / D, -2 * (1 + 2 * t) / D
        assert x + y + z == 0
        assert x * x + y * y + z * z == 8
        weights = tuple((11 + a) / 33 for a in (x, y, z))
        assert all(a > 0 for a in weights)
        assert moment(weights, 2) == kappa

    tensor = tuple(sorted(a * b for a in core for b in core))
    competitor = (73, 99, 99, 117, 117, 143, 143, 145, 153)
    assert sum(tensor) == sum(competitor) == 1089
    assert sum(n * n for n in tensor) == sum(n * n for n in competitor) == 137641
    assert sum(n**3 for n in tensor) == 18122049
    assert sum(n**3 for n in competitor) == 18011457
    assert sum(n**3 for n in tensor) - sum(n**3 for n in competitor) == 110592
    assert reduce(gcd, tensor) == reduce(gcd, competitor) == 1
    assert (kappa * kappa).denominator == 33**4
    for k in range(2, 6):
        assert moment(probabilities(tensor), k) == moment(w, k) ** 2
    ratio = moment(w, 3) / moment(w, 2) ** 2
    assert (
        moment(probabilities(tensor), 3) / moment(probabilities(tensor), 2) ** 2
        == ratio**2
    )

    print(f"Passed {checks} exact sample-enumeration variance checks.")
    print("Rational parametrization, refinement and denominator checks passed.")
    print("Primitive 231-atom source has the same P2 and strictly smaller P3.")
    print("Tensor competitor: same N=1089 and C=137641; cube sum improves by 110592.")


if __name__ == "__main__":
    main()
