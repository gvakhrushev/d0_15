"""Finite witnesses for A73. Run with the Python standard library."""
from fractions import Fraction as F
from itertools import product
from math import isclose, log, sqrt


def check(ok, description):
    if not ok:
        raise ValueError(description)


def dot(xs, ys):
    check(len(xs) == len(ys), "matching vector lengths")
    return sum(x * y for x, y in zip(xs, ys))


def enumerate_trials(prob, weights, horizon, prices):
    """Enumerate every finite physical word, including unused suffix draws."""
    result = elapsed = work = F(0)
    for first, *fresh in product(range(len(prob)), repeat=horizon + 1):
        mass = prob[first]
        for y in fresh:
            mass *= prob[y]
        used = fresh[:fresh.index(first) + 1] if first in fresh else fresh
        result += mass * weights[first] * len(used)
        elapsed += mass * len(used)
        work += mass * sum(prices[first][y] for y in used)
    return result, elapsed, work


def test_return_price():
    prob = [F(1, 2), F(1, 3), F(1, 6)]
    weights = [F(1, 4), F(1, 5), F(1, 2)]
    prices = [[x + 3 * y + 1 for y in range(3)] for x in range(3)]
    for n in (1, 2, 5):
        recorded, elapsed, work = enumerate_trials(prob, weights, n, prices)
        factors = [1 - (1 - q) ** n for q in prob]
        check(recorded == dot(weights, factors), "counting measure")
        check(elapsed == sum(factors), "actual clock")
        check(work == dot(factors, [dot(row, prob) for row in prices]), "each paid comparison")
    check(dot(prob, weights) != sum(weights), "naive Born average must differ")
    # Even histories with the same printed tag can have different actual weights.
    coarse_weight = (prob[0] * weights[0] + prob[1] * weights[1]) / (prob[0] + prob[1])
    check(coarse_weight + weights[2] != sum(weights), "unresolved fine histories matter")
    dprob = [F(1, 10), F(-1, 7), F(3, 70)]
    dweights = [F(2, 9), F(1, 11), F(-3, 8)]
    check(sum(dprob) == 0, "smooth normalized tangent")
    for n in (1, 6, 25, 100):
        factors = [1 - (1 - q) ** n for q in prob]
        df = [n * (1 - q) ** (n - 1) * dq for q, dq in zip(prob, dprob)]
        truncated = dot(dweights, factors) + dot(weights, df)
        b = 1 - min(prob)
        bound = b ** n * sum(map(abs, dweights)) + n * max(weights) * b ** (n-1) * sum(map(abs, dprob))
        check(abs(sum(dweights) - truncated) <= bound, "field derivative error")
    # A common field scale changes the source while preserving the odds.
    check([w / sum(weights) for w in weights] ==
          [2 * w / sum(2 * u for u in weights) for w in weights], "invisible common scale")


def gram_by_actual_events(prob, weights):
    twice = sum(p * w * w for p, w in zip(prob, weights))
    thrice = pair_filter = F(0)
    for i, j, k in product(range(len(prob)), repeat=3):
        mass = prob[i] * prob[j] * prob[k]
        thrice += mass * (i == j == k)
        pair_filter += mass * (i == j) * weights[i]
    return twice * thrice - pair_filter ** 2


def test_collision_jet():
    prob = [F(2, 7), F(4, 7), F(1, 7)]
    dp = [F(1, 8), F(-1, 6), F(1, 24)]
    dw = [F(1, 5), F(2, 9), F(-1, 8)]
    scale = F(3, 4)
    w = [scale * p for p in prob]
    check(gram_by_actual_events(prob, w) == 0, "single-point calibration")
    check(gram_by_actual_events(prob, dw) > 0, "nonproportional weight motion")
    recip = sum(p * p / a for p, a in zip(prob, w))
    drecip = sum(2*p*v/a - p*p*u/a**2 for p, v, a, u in zip(prob, dp, w, dw))
    check(drecip / recip == -sum(dw) / sum(w), "absolute jet")
    entropy_derivative = -sum(v * (1 + log(p)) for v, p in zip(dp, prob))
    price_derivative = -sum(v * log(a) + p * u / a for v, p, a, u in zip(dp, prob, w, dw))
    check(isclose(price_derivative, entropy_derivative + drecip / recip, abs_tol=1e-14),
          "cost, moving records, inverse collision jet")
    for w in ([F(3, 8), F(1, 4), F(2, 3)], w):
        z = sum(w)
        recip = sum(p*p/a for p, a in zip(prob, w))
        pi = [a / z for a in w]
        r = [p*p/(a*recip) for p, a in zip(prob, w)]
        kl = sum(p * log(p/u) for p, u in zip(prob, r))
        chi = sum((p-u)**2/u for p, u in zip(prob, pi))
        gap = sum(p*log(a/p) for p, a in zip(prob, w)) + log(recip)
        check(z * recip - 1 == chi and isclose(gap, kl, abs_tol=1e-14), "two exact gaps")


def test_native_scalar():
    p = (sqrt(5)-1)/2
    z = 2**-20
    q = p**2 + p**3 * 0.13
    prob = [1-q, q]
    check(gram_by_actual_events(prob, [p, p*p]) > 1e-6, "literal output tariffs fail calibration")
    gamma = (2*p**3)**20
    s, ds, c0, dc0 = .77, .39, .62, -.18
    cold = 1-z+z*s*c0
    dcold = z*(ds*c0+s*dc0)
    dq = 0.35
    w = [gamma*cold*v for v in prob]
    dp = [-dq, dq]
    dw = [gamma*(dcold*v+cold*t) for v, t in zip(prob, dp)]
    price = -sum(t*log(a)+v*u/a for v, t, a, u in zip(prob, dp, w, dw))
    check(isclose(price, dq*log((1-q)/q)-dcold/cold, abs_tol=3e-14),
          "golden diluted cold source with moving prior")


if __name__ == "__main__":
    test_return_price()
    test_collision_jet()
    test_native_scalar()
    print("PASS counting weights, first-record repetitions, paid comparisons, absolute field jets and native scalar check")
