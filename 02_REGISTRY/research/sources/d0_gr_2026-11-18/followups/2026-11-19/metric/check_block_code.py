"""Minimum Golden-prefix report prices at the source-certified noisy H.1 centre."""
from functools import lru_cache
from fractions import Fraction
from itertools import combinations
from math import comb
import json

from check_extra_work import centre, check, span


def best_two_profiles(m, q):
    """Return the two cheapest distinct sorted cost profiles (including ties)."""
    n = 2**m
    a, b = q.denominator - q.numerator, q.numerator
    masses = [a**(m-k)*b**k for k in range(m+1) for _ in range(comb(m, k))]
    tail = [0]*(n+1)
    for i in reversed(range(n)):
        tail[i] = tail[i+1] + masses[i]

    @lru_cache(None)
    def best(i, now, next_level):
        if i == n:
            return [(0, ())]
        candidates = []
        for leaves in range(now+1):
            branches = now-leaves
            placed = i+leaves
            if placed+next_level+2*branches > n:
                continue
            if placed < n and next_level+branches == 0:
                continue
            for cost, profile in best(placed, next_level+branches, branches):
                candidates.append((cost+tail[placed], (leaves,)+profile))
        return sorted(candidates)[:2]

    return [(Fraction(v, q.denominator**m), h) for v,h in best(0,1,0)]


def main():
    q, ell = centre()
    a = 1-q
    midpoint = Fraction("0.412469880568555")
    radius = max(abs(q.lo-midpoint), abs(q.hi-midpoint))
    p_prime = 1-(a/q).log_positive()/ell
    blocks = {}
    for m in range(1,6):
        leading = best_two_profiles(m, midpoint)
        price, profile = leading[0]
        unit_profile = (0,)*m + tuple(comb(m,k) for k in range(m+1))
        expected = unit_profile if m < 5 else (0,)*6 + (6,11,11,4)
        check(profile == expected, "exact minimizing leaf histogram")
        gap = None
        if len(leading) > 1:
            gap = leading[1][0]-price
            check(gap > 4*m*(2**m-1)*radius, "strict optimality on true centre enclosure")
        blocks[m] = {"leaves_by_golden_cost_from_zero":profile,
                     "second_profile_gap_at_rational_midpoint":str(gap) if gap is not None else None}
    savings = q**3-a**5
    check(savings.lo>0, "physical-centre code saving")
    # Per-record perturbation at the common field. The three-element and four-
    # element sets are precisely the assignments that can tie in a weight class.
    pos = set(range(5))
    triples = list(map(frozenset, combinations(pos,3)))
    quads = list(map(frozenset, combinations(pos,4)))
    slopes, norms = [], []
    for triple in triples:
        for left, right in combinations(quads, 2):
            gradient = []
            common_in_quads = left & right
            for j in range(5):
                slope = p_prime-a**4
                for marked in (triple,left,right,pos):
                    k = len(marked)
                    if j in marked:
                        slope -= q**(k-1)*a**(5-k)
                    else:
                        slope += q**k*a**(4-k)
                compact = p_prime-a**4
                if j in triple:
                    compact -= q**2*a
                if j in common_in_quads:
                    compact -= q**3
                check(abs(slope.lo-compact.lo)<Fraction(1,10**28)
                      and abs(slope.hi-compact.hi)<Fraction(1,10**28), "two triple indicators")
                gradient.append(slope)
            slopes.append(gradient[0])
            check(all(v.lo*v.hi > 0 for v in gradient), "resolved five row signs")
            norms.append(sum((v if v.lo>0 else -v for v in gradient), span(0)))
    lo = min(slopes, key=lambda x:x.lo)
    hi = max(slopes, key=lambda x:x.hi)
    symmetric = (lo+hi)/2
    swap_first = p_prime-a**4-q**2
    swap_last = p_prime-a**4
    diagonal = 5*p_prime-5*a**4-3*q**2
    norm = max(norms, key=lambda x:x.hi)
    check(all(v.hi <= norm.hi for v in norms), "uniform gradient norm upper bound")
    sharp_radius = diagonal/norm
    check(len(slopes)==100 and lo.hi<0<hi.lo, "opposite one-record sources")
    check(symmetric.lo>0 and diagonal.lo>0 and swap_first.hi<0<swap_last.lo,
          "coordinate finite-difference and common-field signs")
    check(abs(swap_first.lo-lo.lo)<Fraction(1,10**28) and abs(swap_first.hi-lo.hi)<Fraction(1,10**28),
          "subtree swap attains lower active directional response")
    zero_sum_direction = [1,1,1,Fraction(-3,2),Fraction(-3,2)]
    ordered = sorted(zero_sum_direction)
    central_zero_sum = -(q**2)*(sum(ordered[:3])+sum(ordered[-3:]))/2
    check(sum(ordered)==0 and central_zero_sum.hi<0, "nonlinear symmetric comparison")
    print(json.dumps({
        "scope":"fixed Golden letter costs and a freely recoded terminal lossless classical block",
        "centre_interval":q.fmt(14), "blocks":blocks,
        "block5_cost_saving":savings.fmt(14),
        "native_net_slope_per_record":p_prime.fmt(13),
        "fixed_subtree_swap_per_coordinate":{"in_first_three":swap_first.fmt(13),"other":swap_last.fmt(13)},
        "number_of_active_length_assignments":len(slopes),
        "median_counterexample_central_zero_sum_direction":central_zero_sum.fmt(13),
        "optimized_one_coordinate":{"right":lo.fmt(13),"left":hi.fmt(13),"symmetric":symmetric.fmt(13)},
        "optimized_common_field_all_five":diagonal.fmt(13),
        "sum_of_five_coordinate_symmetric_slopes":(5*symmetric).fmt(13),
        "max_gradient_l1":norm.fmt(13),
        "sharp_relative_radius_around_shared_field_direction":sharp_radius.fmt(13)
    },indent=2))


if __name__ == "__main__":
    main()
