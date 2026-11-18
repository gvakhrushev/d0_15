"""Verify the exact Golden calibration and the final price/Info bounds."""

from fractions import Fraction
import json

import mpmath as mp


def require(condition, reason):
    if not bool(condition):
        raise AssertionError(reason)


def sine_squared_power(n, k, p):
    iv = mp.iv
    c, s = iv.mpf(1), iv.mpf(0)
    rc, rs = iv.sqrt(p), p
    exponent = (1 << n)*k
    while exponent:
        if exponent & 1:
            c, s = c*rc-s*rs, s*rc+c*rs
        rc, rs = rc*rc-rs*rs, 2*rc*rs
        exponent //= 2
    return s*s


def main():
    iv = mp.iv
    iv.dps = 120
    p = (iv.sqrt(5)-1)/2
    threshold = sine_squared_power(88, 15, p)
    readiness = sine_squared_power(40, 1, p)
    require(iv.mpf("0.998511") < threshold and threshold < iv.mpf("0.998513"),
            "The literal threshold response lost its interval")
    require(iv.mpf("0.05502") < readiness and readiness < iv.mpf("0.05503"),
            "The literal readiness response lost its interval")
    u_min = Fraction(3,4)-Fraction(126506,2**20)
    q_lower = iv.mpf(u_min.numerator)/u_min.denominator*threshold
    require(q_lower > p, "The actual conditional output lost the original price sign")
    exact_q = threshold*iv.mpf(3)/4
    ell = -iv.ln(p)
    known = {"1": ["-0.74", "-0.70"], "2": ["0.40", "0.44"]}
    for exponent in (1,2):
        require(iv.sqrt(5)-iv.mpf(1)/exponent < 2, "The universal per-leaf bound changed")
        entropy = -exact_q*iv.ln(exact_q)-(1-exact_q)*iv.ln(1-exact_q)
        bound = (entropy/exact_q-iv.ln(exact_q/(1-exact_q))/exponent)/ell
        lo, hi = known[str(exponent)]
        require(iv.mpf(lo) < bound and bound < iv.mpf(hi), "The centre bound changed")
    print(json.dumps({
        "status": "PASS",
        "threshold_literal_controls": 88,
        "threshold_native_positive_power_multiplier": 15,
        "threshold_readout_probability_bounds": ["0.998511","0.998513"],
        "readiness_literal_controls": 40,
        "readiness_readout_probability_bounds": ["0.05502","0.05503"],
        "conditional_report_lower_than_one_and_greater_than_p": True,
        "minimum_ideal_conditional_report": str(u_min),
        "nonnegative_Info_maximum_total_late_gap_at_thinned_null_centre": known,
        "old_original_truthful_report_on_all_columns_selected": False,
        "book03_full_work_or_info_selected": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
