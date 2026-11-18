"""Same native marginals, distinct two-record scores, and a finite extension bound."""
from fractions import Fraction
from itertools import product
from math import comb
import json

from check_event_information import logarithm
from check_extra_work import centre, check, span


def meet(first, second, label):
    check(max(first.lo, second.lo) <= min(first.hi, second.hi), label)


def native_pair(a, p, nested, q, ell):
    # Integrate the two queries on precisely the same four registered coins.
    masses = {key: span(0) for key in product((0, 1), repeat=2)}
    for x, z, c, d in product((0, 1), repeat=4):
        ones = x + z + c + d
        weight = a**ones * p**(4 - ones)
        reuse = c == 1 and (not nested or d == 0)
        masses[x, x if reuse else z] += weight
    eta = a*p if nested else a
    m00, m01, m10, m11 = masses.values()
    meet(m01, m10, "pair is exchangeable")
    meet(m10+m11, a, "first golden marginal")
    meet(m01+m11, a, "second golden marginal")
    meet(m11 - a*a, eta*a*p, "measurable excess of joint clicks")
    meet(m00, p*(p+a*eta), "00 table")
    low = logarithm(m10/m00)
    high = logarithm(m11/m01)
    slope = 1+((1-q)*low+q*high)/ell
    return slope, {
        "copy_probability": eta.fmt(), "pair_excess": (m11-a*a).fmt(),
        "response_per_independent_q": slope.fmt(),
        "mixed_response": ((high-low)/ell).fmt(),
        "zero_at_other_q": ((-ell-low)/(high-low)).fmt()
    }


def adjacent_slopes(a, p, q, ell):
    result = {}
    for n in (1, 2, 3, 4, 5, 8, 16):
        mean = span(0)
        for k in range(n):
            mass = comb(n-1, k)*q**k*(1-q)**(n-1-k)
            mean += mass*logarithm((k+a)/(n-1-k+p))
        slope = 1+mean/ell
        if n == 1:
            meet(slope, span(0), "one-record score")
        elif n in (2, 3, 4):
            check(slope.hi < 0, "strictly negative short score")
        else:
            check(slope.lo > 0, "positive longer score")
        result[str(n)] = slope.fmt()
    return result


def bounded_count_reference(a, p, q, ell, n=5):
    # One attempt per stage. Unsuccessful selection has its own fallback law.
    increments = {}
    for i in range(1, n+1):
        select = i*a*p**(i-1)
        for k in range(i):
            prob = select*(k+a)/i + (1-select)*a
            increments[i, k] = (logarithm(1-prob), logarithm(prob))
    log_weights = {}
    normalize = span(0)
    for word in product((0, 1), repeat=n):
        k = 0
        weight = span(1)
        score = span(0)
        for i, bit in enumerate(word, 1):
            select = i*a*p**(i-1)
            prob = select*(k+a)/i + (1-select)*a
            weight *= prob if bit else 1-prob
            score += increments[i, k][bit]
            k += bit
        normalize += weight
        log_weights[word] = score
    meet(normalize, span(1), "bounded reference includes every outcome")
    slopes = []
    for j in range(n):
        diff = span(0)
        for other in product((0, 1), repeat=n-1):
            k = sum(other)
            probability = q**k*(1-q)**(n-1-k)
            low = other[:j]+(0,)+other[j:]
            high = other[:j]+(1,)+other[j:]
            diff += probability*(log_weights[high]-log_weights[low])
        slope = 1+diff/ell
        check(slope.lo > Fraction(47, 1000), "positive on each independent coordinate")
        slopes.append(slope.fmt())
    return slopes


def finite_exchangeability():
    # Exactly symmetric non-product triple with every two positions independent.
    a = Fraction(2, 5)
    delta = Fraction(1, 125)
    triple = {word: a**sum(word)*(1-a)**(3-sum(word)) + (-1)**sum(word)*delta
              for word in product((0, 1), repeat=3)}
    check(min(triple.values()) > 0 and sum(triple.values()) == 1, "positive law")
    for j in range(3):
        for pair in product((0, 1), repeat=2):
            mass = sum(weight for w, weight in triple.items() if w[:j]+w[j+1:] == pair)
            check(mass == a**sum(pair)*(1-a)**(2-sum(pair)), "independent pairs")
    check(triple[1, 1, 1] != a**3, "nonproduct triple")
    # Direct finite count on a nontrivial mixture of urns, including negative
    # pair covariance possibilities in the general bound.
    for L, counts in ((9, (2, 5)), (15, (6, 6)), (18, (0, 10))):
        mean = Fraction(sum(counts), 2*L)
        second = Fraction(sum(k*(k-1) for k in counts), 2*L*(L-1))
        variance = mean*(1-mean)/L + (1-Fraction(1, L))*(second-mean**2)
        check(variance == sum((Fraction(k,L)-mean)**2 for k in counts)/2, "count variance")
        for m in range(1, 5):
            bound = comb(m, 2)*(Fraction(1,L)+variance)
            for k in range(m+1):
                actual = Fraction(sum(comb(s,k)*comb(L-s,m-k) for s in counts),
                                  2*comb(L,m)*comb(m,k))
                check(abs(actual-mean**k*(1-mean)**(m-k)) <= bound, "word-mass bound")


def main():
    q, ell = centre()
    p = (span(5).sqrt()-1)/2
    a = p**2
    small, data_small = native_pair(a, p, True, q, ell)
    large, data_large = native_pair(a, p, False, q, ell)
    check(small.lo > 0 and large.hi < 0, "opposite same-history score responses")
    finite_exchangeability()
    L, m = 10**6, 5
    error = comb(m, 2)*(1+a*p)/L
    slope_error = 2*error/(ell*(a**m-error))
    check(slope_error.hi < Fraction(64, 10000), "finite five-coordinate source bound")
    print(json.dumps({
        "centre": q.fmt(), "nested_selector": data_small, "single_selector": data_large,
        "five_records_zero_pair_covariance_extension": {
            "length": L, "word_error": error.fmt(), "source_error_per_slot": slope_error.fmt()},
        "causal_count_reference": adjacent_slopes(a, p, q, ell),
        "bounded_five_report_score_per_slot": bounded_count_reference(a, p, q, ell),
        "finite_exchangeability_counterexample": "all three pair marginals exactly product"
    }, indent=2))


if __name__ == "__main__":
    main()
