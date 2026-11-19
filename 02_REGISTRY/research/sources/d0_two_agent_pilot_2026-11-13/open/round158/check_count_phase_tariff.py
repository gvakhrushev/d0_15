"""Exact phase and resource bounds for the count-form B155 tariff."""

import hashlib
import json
import sys
from fractions import Fraction as Q
from math import gcd, isqrt
from pathlib import Path

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "direct/round76/record"))
import check_complete_tariffs as record

O, I = record.O, record.I
PINS = {
    "direct/round76/record/check_complete_tariffs.py":
        "213739c2ed2abf6a378781ec561b6984db7c4a8937bb9940490ecedc62e5ffa0",
    "open/round155/RESULT.json":
        "fba45d4f8752cfb2a651856cde7b728db96d7c750d912562524394eba6447c36",
    "open/round157/RESULT.json":
        "77e920d03f9ea7914825839a625cafa6ce7dc9d635e5e4494dc994deeee7e6a0",
}
GRID_NUM = 175_623_544_141
GRID_DEN = 414_068_583_427
PHASE_NODES = 6
LAST_RADIX_LEVEL = 13
EPSILON = Q(9,1000)


def arcsine_partial(argument, terms):
    total = term = argument
    for index in range(1, terms):
        term *= argument ** 2 * Q(
            (2 * index - 1) ** 2, (2 * index) * (2 * index + 1)
        )
        total += term
    return total


def arctangent_bounds(argument, terms):
    partial = sum(
        (-1) ** index * argument ** (2 * index + 1) / (2 * index + 1)
        for index in range(terms)
    )
    remainder = argument ** (2 * terms + 1) / (2 * terms + 1)
    return partial - remainder, partial + remainder


def golden_phase_fraction_bounds():
    scale = 2 ** 180
    root_lower = isqrt(5 * scale ** 2)
    p_lower = Q(root_lower - scale, 2 * scale)
    p_upper = Q(root_lower + 1 - scale, 2 * scale)
    O.require(p_lower**2+p_lower < 1 < p_upper**2+p_upper, "Golden root")
    first_low, first_high = arctangent_bounds(Q(1, 5), 100)
    last_low, last_high = arctangent_bounds(Q(1, 239), 100)
    pi_lower = 16 * first_low - 4 * last_high
    pi_upper = 16 * first_high - 4 * last_low
    O.require(pi_upper < Q(22,7), "pi upper bound")
    arcsine_lower = arcsine_partial(p_lower, 110)
    arcsine_upper = (
        arcsine_partial(p_upper, 110)
        + p_upper ** 221 / (1 - p_upper ** 2)
    )
    # This fraction turns controlled G^(2m) into phase 2*pi*m*xi.
    return 2 * arcsine_lower / pi_upper, 2 * arcsine_upper / pi_lower


def rational_ceiling(value):
    return -(-value.numerator//value.denominator)


def phase_grid_error():
    lower, upper = golden_phase_fraction_bounds()
    ratio = Q(GRID_NUM,GRID_DEN)
    radius = Q(1,GRID_DEN**2)
    O.require(gcd(GRID_NUM,GRID_DEN) == 1 and ratio-radius < lower <= upper < ratio+radius,
              "permutation grid of original positive G powers")
    return Q(66,7*GRID_DEN)


def actual_old_tags(p):
    _, masses = record.full_jets()
    active = [n for n,q in enumerate(masses) if q.lo > 0]
    O.require(active == [i for i in range(128) if not i&4], "six varying bits, full archive retained")
    smallest = min(masses[i].lo for i in active)
    p50 = I(1.)
    for _ in range(50):
        p50 = p50*p
    O.require(smallest > p50.hi, "old surprisal below 50 Golden units")
    return len(active)


def mode_budget(old_labels):
    width = 2*old_labels  # The current actual outcome is included separately.
    block = 96
    counts = [width*(n+1)*first_count
              for first_count in (1,block+1) for n in range(block)]
    self_conjugate = 2*width*sum(1+(n%2) for n in range(block))
    total = sum(counts)
    modes = (total+self_conjugate)//2
    # Each value is bounded by 5. Parseval + Cauchy over the 192 steps.
    squared = 25*len(counts)*total
    l1 = isqrt(squared)+1
    O.require((l1-Q(1,2000))**2 > squared, "reserve for rounded coefficients")
    return total,modes,l1


def resources(modes, l1, attenuation_low):
    groups = rational_ceiling(Q(l1)/attenuation_low+Q(modes,2)+2*LAST_RADIX_LEVEL*modes)
    meters = groups*PHASE_NODES
    # 192 exact zero-controlled positive words, one global phase, four
    # readout CXs, births and the addressed raw XORs. The explicit count
    # includes literal print slots but not independent physical mount work.
    per_meter = 192*(2*GRID_DEN+2)+2*GRID_DEN+128
    primitives = meters*per_meter+groups*(64*LAST_RADIX_LEVEL)+10**7
    return groups,meters,primitives


def price_errors(modes,l1,groups,meters,d,eta,phase):
    # Real coefficients are fixed at the reference field. This allowance
    # includes 64 old names priced with the B157 digits.
    calibration = Q(1,2000)+Q(1,4000)
    roundoff = Q(1,2)*modes*eta*d**(LAST_RADIX_LEVEL+1)
    magnitude = (2+4*d/(1-d))*l1
    angle = magnitude*192*phase
    literal_offset = magnitude*PHASE_NODES*phase/2
    nonlinear_offset = meters*24*eta**2*phase/(1-eta**2)**2
    # Even entropy/confirmation tails. The registered mean is quadratic.
    ell = Q(48,100)
    entropy_gain = groups*2*eta**PHASE_NODES/(ell*(PHASE_NODES-1)*(1-eta**2))
    coherent_confirm = groups*Q(47,10)*2*PHASE_NODES*eta**PHASE_NODES/(1-eta**2)
    result = dict(calibration=calibration,balanced_golden_rounding=roundoff,
                  basis_phase=angle,literal_offset=literal_offset,
                  entropy_and_confirm_offset=nonlinear_offset,
                  entropy_quadrature=entropy_gain,coherent_confirm_quadrature=coherent_confirm)
    O.require(sum(result.values()) < EPSILON,"full conditional tariff uniform error")
    return result


def main():
    for name,digest in PINS.items():
        O.require(hashlib.sha256((PILOT/name).read_bytes()).hexdigest()==digest, "exact owner pin")
    p = (-I(1.)+I(5.).sqrt())/2
    ell = -O.logarithm(p)
    d = p*p.square()
    d_lo,d_hi = Q(2360679,10**7),Q(2360680,10**7)
    O.require(d.lo > I.rational(d_lo).hi and d.hi < I.rational(d_hi).lo and ell.lo > .48,
              "elementary bounds on p and ln phi")
    phase = phase_grid_error()
    total,modes,l1 = mode_budget(actual_old_tags(p))
    groups,meters,primitives = resources(modes,l1,d_lo**4)
    errors = price_errors(modes,l1,groups,meters,d_hi,d_hi**4,phase)
    O.require(primitives < 10**24,"explicit elementary schedule upper")

    # Actual gains for all r in the broad interval [p²,p], including
    # both registered and coherent branch confirmation cases.
    minimum_literal = (1-3*d_hi)/2
    high_probability = 2+(1-d_hi)-Q(694,480)-Q(1,2)-Q(47,20)*d_hi
    O.require(minimum_literal > Q(1458,10000) and high_probability > minimum_literal,
              "all continuous pointer states remain positive")
    eta = d_hi**4
    future_scratch = 2*eta*(1+PHASE_NODES*phase/2)
    base = json.loads((PILOT/"open/round157/RESULT.json").read_text())
    minimum_scratch_before_future = (
        min(row["scratch_lower"] for row in base["full_raw_confirmed_gain_bounds"].values())
        + float((1+d_lo)**2/2)
    )
    O.require(minimum_scratch_before_future > .95, "same actual scratch branch cost from B157")
    scratch_lower = Q(95,100)-Q(619,1000)*future_scratch
    O.require(scratch_lower > Q(94,100),"shared measured scratch bound")

    old_gain = I.rational(Q(1,100))/ell-I.rational(2*EPSILON)
    # Use an explicit conservative interval rather than an unrounded
    # decimal obtained by division of two outward endpoints.
    residual = I.rational(Q(104554,10**8))-I.rational(Q(1526809,10**9)*EPSILON)
    O.require(old_gain.lo > .00278 and residual.lo > .0010317, "strict A76 price crossing")
    O.require(base["B155_crossing_margin_lower_under_literal_and_symmetric_bank_confirmation"] > .00103027,
              "B157 baseline")
    print(json.dumps({
        "round":"B158",
        "old_tags":64,
        "scope":"fixed reference tariff on 192 actually retained B155 bits",
        "phase_grid":[GRID_NUM,GRID_DEN],
        "phase_error_upper":float(phase),
        "count_table_domain_total":total,
        "real_count_fourier_terms_upper":modes,
        "coefficient_absolute_sum_upper":l1,
        "independent_quadrature_groups_upper":groups,
        "terminal_meters_upper":meters,
        "explicit_addressed_letters_and_literal_slots_upper":primitives,
        "uniform_fixed_tariff_error_upper":float(sum(errors.values())),
        "uniform_fixed_tariff_error_allowed":float(EPSILON),
        "error_components_upper":{name:float(x) for name,x in errors.items()},
        "terminal_realized_Info_lower":float(minimum_literal),
        "scratch_realized_Info_lower":float(scratch_lower),
        "B155_Info_lower_as_factor_of_1_minus_q":float(old_gain.lo),
        "crossing_margin_against_old_G1_lower":float(residual.lo),
        "full_bank_expanded":False,
        "same_physical_clock_and_full_class_verified":False,
        "GR_closed":False,
        "pinned_inputs":PINS,
    },sort_keys=True,indent=2))


if __name__=="__main__":
    main()
