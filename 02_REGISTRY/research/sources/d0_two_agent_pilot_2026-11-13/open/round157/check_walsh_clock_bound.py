"""Outward clock lower bound for direct Walsh compilation of the B155 tariff."""
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
    'open/round155/RESULT.json':
        'fba45d4f8752cfb2a651856cde7b728db96d7c750d912562524394eba6447c36',
}
PREFIX = 95
DEGREE = 47
EPSILON = Fraction(1, 10**10)


def load_sources():
    sys.path.insert(0, str(PILOT / 'direct/round76/record'))
    import check_noisy_site_price
    for relative, digest in PINS.items():
        fixture = PILOT / relative
        check_noisy_site_price.O.require(hashlib.sha256(fixture.read_bytes()).hexdigest() == digest,
                                         f"pinned source {relative}")

    fixture = PILOT / 'open/round155/RESULT.json'
    with fixture.open() as stream:
        return check_noisy_site_price, json.load(stream)


def old_zero(source):
    p, state, weights, dweights, forward, backward, u, du, _ = source.owner.site_vector()
    values, tangents = source.owner.actions(0, weights, dweights, forward, backward, u, du)
    # The actual old y=0 is coefficient=0, Walsh index=0, port=0.
    z = state-2*p.square()*values[0]
    dz = -2*p.square()*tangents[0]
    q = source.sum_at_site(z.square())
    v = 2*source.sum_at_site(z*dz)
    bit_six = ((np.arange(256) >> 6) & 1).astype(bool)
    masses = [source.O.reduce_sum(q[mask]) for mask in (~bit_six, bit_six)]
    slopes = [source.O.reduce_sum(v[mask]) for mask in (~bit_six, bit_six)]
    determinant = masses[0]*slopes[1]-masses[1]*slopes[0]
    source.O.require(determinant.lo > 0, 'B155 b=0 is the actual negative-source extremum')
    return p, masses, slopes, determinant


def exact_alpha(source, certificate):
    interval = source.I
    a = interval(interval.rational(Fraction('0.043528211786661')).lo,
                 interval.rational(Fraction('0.043528211786664')).hi)
    b = interval(interval.rational(Fraction('0.098704349262786')).lo,
                 interval.rational(Fraction('0.098704349262792')).hi)
    native = interval(interval.rational(Fraction('0.00009472')).lo,
                      interval.rational(Fraction('0.00009473')).hi)
    magnitude = interval(*certificate['total_certified_truncated_gain'])
    alpha = native/(a*b*magnitude)
    source.O.require(alpha.lo > 0 and alpha.hi < .99, 'B155 exact scalar cancellation interval')
    return alpha


def last_charge_parts(source, p, mass, confirmation):
    interval = source.I
    powers = [interval(1.)]
    for _ in range(PREFIX):
        powers.append(powers[-1]*p)
    ell = -source.ln(p)
    offset, scaled = [], []
    for count in range(PREFIX+1):
        walk = 2*count-PREFIX
        a, b = mass
        if walk < 0:
            b = b*powers[-walk]
        else:
            a = a*powers[walk]
        r = p.square()+powers[3]*b/(a+b)
        r0 = interval(1.)-r
        h = -(r0*source.ln(r0)+r*source.ln(r))/ell
        surprisal_delta = (source.ln(r0)-source.ln(r))/ell
        # Keep the common alpha outside cancellation in the transform.
        offset.append(2*surprisal_delta-1-confirmation(r0,r))
        scaled.append(-h/r0-surprisal_delta if abs(walk) <= 27 else interval(0.))
    return offset, scaled


def common_coefficient(source, vals, degree):
    total = source.I(0.)
    for count, value in enumerate(vals):
        low = max(0, count-(PREFIX-degree))
        high = min(count, degree)
        signed_count = sum((-1)**j*math.comb(degree,j)*math.comb(PREFIX-degree,count-j)
                           for j in range(low, high+1))
        total = total+source.I.rational(Fraction(signed_count, 2**PREFIX))*value
    return total


def report_mode(source, name, p, mass, alpha, confirmation):
    offset, scaled = last_charge_parts(source,p,mass,confirmation)
    coefficients = {
        d:common_coefficient(source,offset,d)+alpha*common_coefficient(source,scaled,d)
        for d in range(38,60)
    }
    coefficient = coefficients[DEGREE]
    source.O.require(coefficient.lo > 0 or coefficient.hi < 0, "strict degree-47 coefficient")
    floor = Fraction.from_float(float(max(coefficient.lo,-coefficient.hi)))
    missing = (2*EPSILON/floor)**2
    support = math.comb(PREFIX,DEGREE)-missing.numerator//missing.denominator
    max_coeff = max(max(-x.lo,x.hi) for x in coefficients.values())
    energy = sum((source.I.rational(math.comb(PREFIX,d))*c.square()
                  for d,c in coefficients.items()),source.I(0.))
    remaining = energy-source.I.rational(Fraction(1,2500))
    cell_count = remaining/source.I(float(max_coeff)).square()
    source.O.require(cell_count.lo > 5*10**27, "clock lower bound also at tariff error .01")
    return {'given_last_charge': name, 'common_degree_47_coefficient': source.O.bounds(coefficient),
            'minimum_distinct_print_characters_error_1e_10':support,
            'degree_38_to_59_energy':source.O.bounds(energy),
            'max_abs_coefficient_in_band_upper':float(max_coeff),
            'minimum_distinct_print_characters_error_0_01_lower':float(cell_count.lo)}


def main():
    source, certificate = load_sources()
    p, mass, slopes, determinant = old_zero(source)
    alpha = exact_alpha(source, certificate)
    interval = source.I
    root22 = interval(22.).sqrt()
    def reg(a,b):
        return a-b
    def coh(a,b):
        return b.sqrt()+(3*a).sqrt()-a.sqrt()-(3*b).sqrt()
    modes = [('literal', lambda a,b: interval(0.)), ('registered',reg),
             ('registered_sqrt22',lambda a,b:root22*reg(a,b)), ('coherent',coh),
             ('coherent_sqrt22',lambda a,b:root22*coh(a,b))]
    output = {'old_tag': 0, 'first_block_fixed_count': 48, 'second_prefix_bits': PREFIX,
              'walsh_degree': DEGREE, 'walsh_families': math.comb(PREFIX,DEGREE),
              'old_masses': [source.O.bounds(q) for q in mass],
              'old_mass_jets': [source.O.bounds(dq) for dq in slopes],
              'old_posterior_sign': source.O.bounds(determinant),
              'alpha': source.O.bounds(alpha),
              'given_last_charge_scenarios': [report_mode(source,name,p,mass,alpha,fn) for name,fn in modes],
              'bounds_only_fixed_linear_print_architecture': True, 'GR_closed': False}
    print(json.dumps(output, indent=2, sort_keys=True))


if __name__=='__main__':
    main()
