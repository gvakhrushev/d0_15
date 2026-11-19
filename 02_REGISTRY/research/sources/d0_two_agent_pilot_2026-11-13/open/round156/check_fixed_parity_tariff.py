"""Exact fixed-word tariff compiler and outward A76/B155 admissibility margins."""
import hashlib
import json
import sys
from fractions import Fraction as Q
from pathlib import Path

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "open/round153"))
import check_positive_gain_site_bound as strong

I, O = strong.I, strong.O
PINS = {
    "open/round153/check_positive_gain_site_bound.py":
        "5c5f1257327de26ae0022e683441596858aa90ff77deef45db9583b57ae48d0c",
    "open/round155/RESULT.json":
        "fba45d4f8752cfb2a651856cde7b728db96d7c750d912562524394eba6447c36",
    "open/round152/RESULT.json":
        "eaf0ff8edfa931b7a672b270c813870d26db91b96263506035d79342fc468fb2",
}
DELTA_ONE = (-1, 2)
DELTA_SIX = (46921, -75920)
PRECISION = Q(1, 10**10)


def add(left, right, multiplier=1):
    return left[0]+multiplier*right[0], left[1]+multiplier*right[1]


def scale(value, multiplier):
    return multiplier*value[0], multiplier*value[1]


def sign(value):
    """Exact comparison in Q(p), p=(sqrt(5)-1)/2."""
    a, b = value
    r = 2*a-b
    if r >= 0 and b >= 0:
        return int(r > 0 or b > 0)
    if r <= 0 and b <= 0:
        return -1
    return (1 if r > 0 else -1) if r*r > 5*b*b else (1 if b > 0 else -1)


def floor_ratio(numerator, denominator):
    O.require(sign(numerator) >= 0 and sign(denominator) > 0, "positive division")
    lo, hi = 0, 1
    while sign(add(numerator, denominator, -hi)) >= 0:
        lo, hi = hi, 2*hi
    while hi-lo > 1:
        middle = (lo+hi)//2
        if sign(add(numerator, denominator, -middle)) >= 0:
            lo = middle
        else:
            hi = middle
    return lo


def delta(counts):
    return add(scale(DELTA_ONE, counts[0]), DELTA_SIX, counts[1])


def grid(tolerance):
    """Find a certified convergent u/v to positive delta / negative magnitude."""
    alpha, beta = DELTA_ONE, scale(DELTA_SIX, -1)
    a, b = alpha, beta
    previous, current = (0, 1), (1, 0)
    while True:
        quotient = floor_ratio(a,b)
        a, b = b, add(a,b,-quotient)
        previous, current = current, add(previous,current,quotient)
        u, v = current
        if v > 1 and sign(add((v*tolerance,0),beta,-2)) > 0:
            residual = add(scale(alpha,v),beta,-u)
            O.require(sign(add(scale(residual,sign(residual)*v),beta,-1)) < 0,
                      "certified grid error")
            return u, v


def round_positive_counts(coefficient, pair):
    alpha, beta = DELTA_ONE, scale(DELTA_SIX,-1)
    u, v = pair
    # First translate a positive objective to a nonpositive one. Then a
    # modular inverse finds the requested residue without a scan.
    n0 = floor_ratio((coefficient,0),alpha)+1 if coefficient > 0 else 0
    negative_remainder = add(scale(alpha,n0),(coefficient,0),-1)
    j = -floor_ratio(scale(negative_remainder,v),beta)
    n = (j*pow(u,-1,v)) % v
    m = (n*u-j)//v
    return n+n0,m


def parity(mask, word):
    return bin(mask & word).count("1") % 2


def compile_table(target, tolerance):
    """Return fixed counts (mask, G or G^6 banks) for a rational target table."""
    size = len(target)
    O.require(size >= 2 and size & (size-1) == 0 and tolerance > 0, "binary table")
    pair = grid(tolerance/(size-1))
    plan = []
    for mask in range(1, size):
        coefficient = -2*sum((Q(v)*(1-2*parity(mask, word))
                              for word, v in enumerate(target)), Q(0))/size
        if coefficient:
            plan.append((mask, *round_positive_counts(coefficient,pair)))
    return plan


def realized_relative(plan, word):
    value = (0, 0)
    for mask, count_one, count_six in plan:
        if parity(mask, word):
            value = add(value, delta((count_one, count_six)))
    return value


def check_short_words(p):
    # cos(2 theta) = 2p-1; verify its sixth Chebyshev polynomial in Q(p).
    def times_delta_one(value):
        a, b = value
        return 2*b-a, 2*a-3*b

    previous, current = (1, 0), DELTA_ONE
    for _ in range(5):
        previous, current = current, add(scale(times_delta_one(current), 2), previous, -1)
    O.require(current == DELTA_SIX and sign(DELTA_ONE) == 1 and sign(DELTA_SIX) == -1,
              "exact two short rotation contrasts and their signs")
    # DELTA_SIX/DELTA_ONE = -11077+17922p.
    O.require(times_delta_one((-11077, 17922)) == DELTA_SIX, "irrational ratio")
    c, s = I(1.), I(0.)
    for k in range(1, 7):
        c, s = c*p.sqrt()-s*p, c*p+s*p.sqrt()
        if k not in (1, 6):
            continue
        rate = s.square()
        contrast = c.square()-rate
        exact = DELTA_ONE if k == 1 else DELTA_SIX
        p_form = I(exact[0])+exact[1]*p
        O.require(max(contrast.lo,p_form.lo) <= min(contrast.hi,p_form.hi),
                  "actual pointer agrees with exact contrast")
        yield rate


def minimum_gain(rate, logphi):
    lower = 100.
    for r in (rate, I(1.)-rate):
        r0 = I(1.)-r
        h = -(r*O.logarithm(r)+r0*O.logarithm(r0))/logphi
        lower = min(lower,float((O.logarithm(r0)/logphi-r+2*h).lo),
                    float((O.logarithm(r)/logphi+r0+2*h).lo))
    return lower


def main():
    for path, digest in PINS.items():
        O.require(hashlib.sha256((PILOT/path).read_bytes()).hexdigest() == digest, "source pin")
    p, _, _, _, qy, _ = strong.physical_site()
    logphi = -O.logarithm(p)
    rates = list(check_short_words(p))
    min_gains = [minimum_gain(r,logphi) for r in rates]
    O.require(min_gains[0] > .1458 and min_gains[1] > .5146, "strict on all bank symbols")

    # Min sibling probability in ANY deterministic serialization of the full old mark.
    # From -ln(1-r)>=r, its realized surprisal is at least q_min/ln(phi).
    old = I(float(qy.lo.min()),float(qy.hi.min()))/logphi
    O.require(old.lo > float(I.rational(4*PRECISION).hi), "old Info margin under price error")
    raw_tv = json.loads((PILOT/"open/round152/RESULT.json").read_text())
    tv_hi = raw_tv["actual_outward_scores"]["D_old_and_sharp_site_TV"][1]
    error = 2*I(tv_hi)*I.rational(PRECISION)
    margin = json.loads((PILOT/"open/round155/RESULT.json").read_text())
    margin_lo = margin["margin_over_A75_depth_one"][0]
    gap = I(margin_lo)-error
    O.require(gap.lo > .00104554, "compiled price still crosses the A75 depth-one row")

    # Mixed positive and negative high-order coefficients exercise an actual
    # fixed program: no live branch selector in the generated tuple stream.
    target = [Q(7,8)+3*((x&3)==3)-2*((x&6)==6)+Q(11,7)*(x==5) for x in range(8)]
    demo = compile_table(target, PRECISION)
    for word, price in enumerate(target):
        diff = add(realized_relative(demo, word), (price-target[0], 0), -1)
        O.require(sign(add(diff,(PRECISION,0),-1)) < 0
                  and sign(add(diff,(PRECISION,0))) > 0, "exact tariff approximation")
    # This tests precision selection in the full table dimension without
    # falsely claiming to enumerate the 2^199 branches.
    wide = grid(PRECISION/(2*(2**199-1)))
    print(json.dumps({
        "round": "B156",
        "pinned_source_hashes": PINS,
        "pointer_one_probability": [O.bounds(rate) for rate in rates],
        "info_on_every_new_bank_symbol_lower": min_gains,
        "old_surprisal_lower_for_any_deterministic_serialization": float(old.lo),
        "raw_A76_moving_probability_l1_upper": 2*tv_hi,
        "per_complete_old_and_B155_path_relative_tariff_error": str(PRECISION),
        "B155_source_error_upper": float(error.hi),
        "B155_crossing_margin_lower_for_compiled_literal_price": float(gap.lo),
        "truth_table_example_bank_count": sum(n1+n6 for _, n1, n6 in demo),
        "example_fixed_plan_mask_one_six": demo,
        "full_199_bit_convergent_denominator_bit_length": wide[1].bit_length(),
        "full_199_bit_program_expanded": False,
        "book_direct_clock_source_and_class_bound": False,
        "GR_closed": False,
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
