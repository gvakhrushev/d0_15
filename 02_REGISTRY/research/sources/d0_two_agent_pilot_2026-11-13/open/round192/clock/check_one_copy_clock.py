"""Verify the Golden 0/1 fork, shared-SITE bias and native-clock scale."""

from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys

import mpmath as mp

PILOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PILOT / "direct/round80/price"))
sys.path.insert(0, str(PILOT / "open/round181"))
from check_fixed_positive_reader import nc1, one, p, power, require, with_births
from check_parity_price import action

G = type(one)


def fork():
    # The first real flag is the depth, the second the STOP/GO decision.
    # Every old wire is a spectator, including any external reference.
    state = with_births({0: one}, 4)
    gates = nc1(0, 1) + nc1(2, 3)
    for gate in gates:
        state = action(state, gate, 4)
    measured = {(d,r): one*0 for d,r in product(range(2), repeat=2)}
    for index, amp in state.items():
        d, tail_d, r, tail_r = ((index >> bit) & 1 for bit in (3,2,1,0))
        require(not (d and tail_d) and not (r and tail_r), "Unexpected dark NC1 leaf")
        measured[d,r] += amp*amp
    require(measured == {(d,r): power(p, 2+d+r) for d,r in measured},
            "Actual native 0/1 fork masses changed")

    def positive_masses(acceptance, extra=(F(1),F(1)), zero=F(1)):
        depths = F(3,7), F(2,9)
        stop, go = F(5,11), F(7,13)
        masses = [[
            depths[d]*stop,
            depths[d]*go*extra[d]*q,
        ] for d,q in enumerate((zero,acceptance))]
        # Keep two unrelated rejection masses in the normalization.
        total = sum(sum(row) for row in masses) + F(3,19) + F(5,23)
        return tuple(tuple(m/total for m in row) for row in masses)

    def odds(masses):
        (p00,p01),(p10,p11) = masses
        return p11*p00/(p10*p01)

    q, known_reference = F(11,29), F(4,5)
    clean = positive_masses(q)
    require(odds(clean) == q, "The one-copy cross odds lost the reference")
    require(known_reference*odds(positive_masses(q, zero=known_reference)) == q,
            "A known non-unit absolute reference must be carried")
    extra = F(17,12), F(11,10)
    skew = positive_masses(q, extra)
    require(odds(skew) == q*extra[1]/extra[0], "Wrong clock/route bias")
    changed = F(5,4)
    require(positive_masses(q*changed, (extra[0],extra[1]/changed)) == skew,
            "Absolute calibration degeneracy not seen on the same masses")

    # Make both GO routes execute two copies, ignoring the second mark on d=1.
    # Its total absolute mass T remains, even though the route is now matched.
    t = F(7,10)
    go_one, go_two = q*t, q*q
    require(go_two/go_one == q/t and go_two/go_one != q, "Padding lost its extra mass")

    return {
        "actual_Golden_fork": ["p^2", "p^3", "p^3", "p^4"],
        "actual_NC1_gates": len(gates),
        "actual_fresh_births": 4,
        "one_copy_target": str(q),
        "cross_odds_with_matched_ratio": str(odds(clean)),
        "cross_odds_with_unmatched_ratio": str(odds(skew)),
        "raw_nonidentifiability_witness": True,
        "fixed_two_copy_run_returns_normalized_q_over_t": str(go_two/go_one),
    }


def site_bias():
    mp.mp.dps = 80
    # For all actual |y|<=1/64, the interval for u and the polynomial signs
    # prove strict increase of the report, independent of any chosen Lambda.
    p_lo, p_hi = F(618,1000), F(619,1000)
    require(p_lo*p_lo+p_lo-1 < 0 < p_hi*p_hi+p_hi-1 and 4*p_hi**3 < 1,
            "Wrong p enclosure or feedback bound")
    ulo, uhi = p_lo-p_hi*p_hi/64, p_hi+p_hi*p_hi/64
    require(ulo > F(612,1000) and uhi < F(5,8) and 2*uhi*uhi < 1,
            "Genuine report factor can change sign")
    # A^2 from the exact Chebyshev calculation on the actual 712-G radius.
    u = power(p, 3)
    t0,t1 = one,u
    for _ in range(2, 713):
        t0,t1 = t1,2*u*t1-t0
    amp2 = p*p*(one-t1)*G(F(1,2))
    b = amp2*G(F(1,32))  # diagnostic Lambda=1; not an H_q norm calibration
    z = G(F(1,2**20))
    l0 = 4*power(p,3)

    def report(y):
        w = p+p*p*y
        g = 4*w*w*(one-w*w)
        return one-(one-z*g)*(one-z*(l0+(one-l0)*g))

    a,b0,c = (report(y) for y in (-b, one*0, b))
    require(a != b0 and b0 != c and a != c, "Exact native phase sectors collapsed")
    mean = (a+2*b0+c)*G(F(1,4))
    second = (a*a+2*b0*b0+c*c)*G(F(1,4))
    variance = second-mean*mean
    squares = (2*power(a-b0,2)+2*power(c-b0,2)+power(a-c,2))*G(F(1,16))
    require(variance == squares and variance != 0,
            "Shared SITE must have exact nonzero variance")
    require(amp2 != 0 and all(x.coefficients[1::2] == (0,0) for x in (a,b0,c,variance)),
            "Literal A^2 and acceptance coefficients must lie in Q(p)")

    pp, zz = (mp.sqrt(5)-1)/2, mp.mpf(2)**-20
    theta = mp.asin(pp)
    bb = (pp*mp.sin(712*theta))**2/32
    ll = 4*pp**3

    def numeric_report(y):
        w = pp+pp*pp*y
        g = 4*w*w*(1-w*w)
        return 1-(1-zz*g)*(1-zz*(ll+(1-ll)*g))

    ra,r0,rc = (numeric_report(y) for y in (-bb,0,bb))
    m = (ra+2*r0+rc)/4
    v = (2*(ra-r0)**2+2*(rc-r0)**2+(ra-rc)**2)/16
    require(ra < r0 < rc and v > 0, "Numerical report order mismatch")
    require(abs((ra*ra+2*r0*r0+rc*rc)/(4*m)-m-v/m) < mp.mpf("1e-75"),
            "Shared 1/2 cross odds not size-biased")
    return {
        "actual_local_field_reference": "L=4, descriptors 00 and 01, A=p sin(712 theta)",
        "site_multiplicities_for_minus_zero_plus": [64,128,64],
        "diagnostic_Lambda_one_not_a_norm_calibration": True,
        "mean_local_acceptance": mp.nstr(m,23),
        "positive_shared_site_variance": mp.nstr(v,23),
        "shared_site_cross_odds_minus_mean": mp.nstr(v/m,23),
        "exact_nonzero_sum_of_squares_in_Qp": True,
    }


def clock_scale():
    # Each real pair adds two square stages of occupied ambient dimension d.
    # See the original Hodge formula, not a cost tariff.
    d, horizon, pairs = 16, 128, 64
    first = horizon*d
    padded = first+2*pairs*d
    require(padded == 2*first, "Example must double the actual clock dimension")
    lower_partition_ratio = F(359*padded,425*first)
    require(lower_partition_ratio > 1, "Absolute heat example lacks a strict bound")
    beta = 2*((mp.sqrt(5)-1)/2)**2
    return {
        "dimension_before": first,
        "dimension_after": padded,
        "lower_partition_ratio_using_both_degrees": str(lower_partition_ratio),
        "lower_heat_difference_diagnostic": mp.nstr(mp.log(mp.mpf(
            lower_partition_ratio.numerator)/lower_partition_ratio.denominator)/beta,18),
        "unchanged_terminal_action_requires_actual_common_RC3_cut": True,
    }


def main():
    print(json.dumps({
        "native_fork": fork(), "shared_SITE": site_bias(), "clock_padding": clock_scale(),
        "same_execution_Book03_ratio_identified": False, "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
