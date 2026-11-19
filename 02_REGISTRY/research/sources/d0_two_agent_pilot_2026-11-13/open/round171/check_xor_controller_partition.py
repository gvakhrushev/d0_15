"""Check conditional partitions of the fixed XOR bank with paid gate motion."""

from collections import Counter
from itertools import product
import json

import mpmath as mp


def require(predicate, reason):
    if not predicate:
        raise ArithmeticError(reason)


def verify_symbolic_event_partitions():
    # A formal monomial is (NC1 control state, exponent of u, exponent of p^nu).
    banks = []
    for old_bit in (0, 1):
        ledger = Counter()
        for selector, report in product((0, 1), repeat=2):
            control = old_bit ^ selector
            net_length = report - (report ^ control)
            ledger[control, old_bit + selector, net_length] += 1
        banks.append(ledger)
    banks[0].subtract(banks[1])
    require({key: value for key, value in banks[0].items() if value}
            == {(0, 0, 0): 2, (0, 2, 0): -2}, "literal event partitions differ by A0(1-u²)")


def motion(probability, p):
    one = mp.iv.mpf(1)
    flip_overlap = 2 * p * mp.iv.sqrt(p)
    first = mp.iv.sqrt(one - (one - (one - flip_overlap) * probability)**2)
    third = mp.iv.sqrt(one - (one - probability)**2)
    return first + p + third


def check_intervals(nu):
    one = mp.iv.mpf(1)
    p = (mp.iv.sqrt(5) - one) / 2
    r, s = p**2, p**3
    work = [motion(value, p) for value in (r, p)]
    require((work[1] - work[0]).a > 0, "motion strictly increases for the actual control")
    u, literal = p**(nu*s), p**nu
    intervals = {}
    for name in ("event", "drop"):
        if name == "event":
            conditional = [2 * p**(nu*work[0]),
                           (literal + one/literal) * p**(nu*work[1])]
            selector_weights = (one, one)
        else:
            common = literal + literal**2
            conditional = [common * p**(nu*value) for value in work]
            selector_weights = (one, literal)
        z0 = selector_weights[0]*conditional[0] + selector_weights[1]*u*conditional[1]
        z1 = u*selector_weights[0]*conditional[1] + u**2*selector_weights[1]*conditional[0]
        ratio = z1/z0
        require(ratio.a > 0 and ratio.b < 1, "positive rate gives strict sector gap")
        # Independent enumeration of one pair's four joint outcomes.
        concrete = []
        for bit in (0, 1):
            value = mp.iv.mpf(0)
            for selector, report in product((0, 1), repeat=2):
                control = bit ^ selector
                if name == "event":
                    literal_charge = report - (report ^ control)
                else:
                    literal_charge = selector + 1 + report
                value += p**(nu*(literal_charge + s*(bit+selector) + work[control]))
            concrete.append(value)
        difference = concrete[1]/concrete[0] - ratio
        require(difference.a <= 0 <= difference.b, "full retained leaf enumeration")
        # Pick candidate endpoints and certify them by outward intervals.
        lower = int(float(ratio.a) * 10**6)
        require(ratio.a > mp.iv.mpf(lower) / 10**6
                and ratio.b < mp.iv.mpf(lower+1) / 10**6, "rational endpoints")
        intervals[name] = [lower, lower+1]
    return intervals


def main():
    mp.iv.dps = 60
    verify_symbolic_event_partitions()
    print(json.dumps({
        "status": "PASS",
        "scope": "full retained XOR bank, gate-motion coefficient one in numerical fixture",
        "formal_event_gap": "A0(1-u^2)",
        "one_pair_ratio_bounds_in_millionths": {
            str(nu): check_intervals(nu) for nu in (1, 2)
        },
        "physical_universal_price_selected": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
