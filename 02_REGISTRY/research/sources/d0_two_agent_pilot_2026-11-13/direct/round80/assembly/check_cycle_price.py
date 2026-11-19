"""Rational stopped weights, gauge and a hidden conditional-entropy witness."""
from fractions import Fraction as F
from math import log, sqrt


def first_return(stay, outward, inward, other_stay, cap):
    return [stay] + [outward*inward*other_stay**k for k in range(cap)]


def normalization(stay, outward, inward, other_stay):
    return stay + outward*inward/(1-other_stay)


def entropy(probabilities):
    return -sum(p*log(p, (1+sqrt(5))/2) for p in probabilities if p)


def check(u, scale, gauge):
    a, d = scale*u, u
    b, c = gauge*(1-u), scale*(1-u)/gauge
    z = normalization(a, b, c, d)
    assert z == scale
    observed = first_return(u, 1-u, 1-u, u, 8)
    assert [w/z for w in first_return(a, b, c, d, 8)] == observed
    assert d == u and b*c/a == (1-u)**2/u
    # Opposite initial sector with identical transition weights, when summable.
    assert a < 1
    z_b = normalization(d, c, b, a)
    matched_b = [w/z_b for w in first_return(d, c, b, a, 8)] == observed
    assert matched_b == (scale == 1)
    if matched_b:
        assert z == z_b == 1 and b*c == (1-u)**2
        cap = 8
        overflow = b*d**cap
        assert overflow == gauge*(1-u)*u**cap
        assert (overflow + sum(observed) == 1) == (gauge == 1)

    # The first retained word has mass u even with a finite cap. Split just its microhistories.
    capped = observed + [(1-u)*u**8]
    for split in [F(1, 2), F(1, 5), F(2, 7)]:
        fine = [u*split, u*(1-split), *capped[1:]]
        assert sum(fine) == sum(capped) == 1
        difference = entropy(fine) - entropy(capped)
        assert abs(difference - u*entropy([split, 1-split])) < 1e-12


if __name__ == "__main__":
    for u in [F(3, 50), F(1, 8), F(1, 5), F(7, 25)]:
        for scale in [F(1, 2), F(1), F(3, 2)]:
            for gauge in [F(2, 3), F(1), F(5, 3)]:
                check(u, scale, gauge)
    print("PASS 36 rational stopped networks, two return tasks, overflow and hidden prices")
