"""Outward verification of a strict two-block Golden parity source witness."""
import hashlib
import json
import math
import sys
from fractions import Fraction
from pathlib import Path

import numpy as np

PILOT = Path(__file__).resolve().parents[2]
PINS = {
    'direct/round76/record/check_noisy_site_price.py':
        '170f1b51e3f3cb1625c062b658e95782380a1a054328a921549df337b1838123',
    'direct/round75/history/TWO_SITE_SOURCE_RU.md':
        'b22c08ca55b1c6996fa58066b01b178f175c6db2ee1ddbceb0ae8ed945bdd29c',
}


sys.path.insert(0, str(PILOT / "open/round153"))
import check_positive_gain_site_bound as strong

I, O, source = strong.I, strong.O, strong.source


def site_data():
    p, q, dq, multiplicity, _, _ = strong.physical_site()
    masks = I(np.array([[((x >> 7) & 1) == first and ((x >> 6) & 1) == second
                         for x in range(256)]
                        for first in (0, 1) for second in (0, 1)]))
    mass = strong.parity_sum(q[:, None, :], masks)*multiplicity[:, None]
    slope = strong.parity_sum(dq[:, None, :], masks)*multiplicity[:, None]
    O.require(np.all(mass.lo > 0), "four actual SITE groups per old mark")
    return p, mass, slope


def probabilities(n, powers, interval):
    weights = [interval.rational(math.comb(n, k)) for k in range(n+1)]
    return (strong.stack([weights[k]*powers[n+k] for k in range(n+1)]),
            strong.stack([weights[k]*powers[2*n-k] for k in range(n+1)]))


def finite_weights(n, cut, powers, interval):
    weights = []
    for j in range(min(cut, n-1)+1):
        weight = interval(0.)
        for level in range(j, n, 2):
            coefficient = math.comb(level, (level+j)//2)
            weight = weight+interval.rational(coefficient)*powers[3+(3*level+j)//2]
        weights.append(weight)
    return weights


def negative_cone(source, p, powers, finite, a, b, da, db):
    """A lower certificate for magnitude of the negative GAIN extremum.

    Restricting the walk index omits only nonnegative terms. Every prefix
    included in the sum is a prefix of the prescribed finite horizon.
    """
    interval = source.I
    ell = -source.ln(p)
    signed = a*db-b*da
    positive = interval(np.maximum(0., signed.lo), np.maximum(0., signed.hi))
    negative = interval(np.maximum(0., -signed.hi), np.maximum(0., -signed.lo))
    total = interval(0.)
    for j, weight in enumerate(finite):
        rows = ((a+b, b),) if j == 0 else ((a*powers[j]+b, b),
                                         (a+b*powers[j], b*powers[j]))
        for denominator, one_mass in rows:
            r = p.square()+powers[3]*one_mass/denominator
            complement = interval(1.)-r
            negative_g = -source.ln(r)/(complement*ell)
            positive_g = -source.ln(complement)/(r*ell)
            total = total+source.O.reduce_sum(
                weight*(positive*negative_g+negative*positive_g)/denominator)
    return total


def certify(first_count, second_count, cut):
    for relative, expected in {**strong.PINS, **PINS}.items():
        O.require(hashlib.sha256((PILOT / relative).read_bytes()).hexdigest() == expected,
                  f"pinned input {relative}")
    interval = I
    p, mass, slope = site_data()
    powers = [interval(1.)]
    for _ in range(2*max(first_count, second_count)+4):
        powers.append(powers[-1]*p)
    u, v = probabilities(first_count, powers, interval)
    first_weights = finite_weights(first_count, cut, powers, interval)
    second_weights = finite_weights(second_count, cut, powers, interval)
    first = negative_cone(source, p, powers, first_weights,
                          mass[:,0]+mass[:,1], mass[:,2]+mass[:,3],
                          slope[:,0]+slope[:,1], slope[:,2]+slope[:,3])
    second = negative_cone(source, p, powers, second_weights,
        mass[:,0,None]*u+mass[:,2,None]*v, mass[:,1,None]*u+mass[:,3,None]*v,
        slope[:,0,None]*u+slope[:,2,None]*v, slope[:,1,None]*u+slope[:,3,None]*v)
    total = first+second
    # Mix the zero-source surprisal assignment into the extremal one to
    # make every genuinely random edge strictly positive.
    strict_total = interval.rational(Fraction(99,100))*total
    a_lower = Fraction('0.043528211786661')
    b_lower = Fraction('0.098704349262786')
    depth_one_upper = interval.rational(Fraction('0.00009473')/(a_lower*b_lower))
    result = {'sequence': [7, 6], 'block_lengths': [first_count, second_count],
              'walk_index_cut': cut, 'first_certified_truncated_gain': source.O.bounds(first),
              'second_certified_truncated_gain': source.O.bounds(second),
              'total_certified_truncated_gain': source.O.bounds(total),
              'strict_positive_gain_witness': source.O.bounds(strict_total),
              'normalized_depth_one_geometric_upper': source.O.bounds(depth_one_upper),
              'strict_witness_dominates_depth_one': bool(strict_total.lo > depth_one_upper.hi),
              'recover_DATA': False, 'physical_tariff_compiled': False, 'GR_closed': False}
    margin = strict_total-depth_one_upper
    O.require(margin.lo > .00104554, "selected strict tariff exceeds the depth-one source")
    result["margin_over_A75_depth_one"] = O.bounds(margin)
    result["depth_one_exact_scalar_interpolation_allowed"] = True
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


if __name__ == "__main__":
    certify(96, 96, 27)
