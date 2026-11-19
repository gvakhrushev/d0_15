"""Exact A82 mask support, causal tariff contrasts, and two positive slopes."""

from fractions import Fraction
from hashlib import sha256
from itertools import product
from math import isqrt
from pathlib import Path
import json

import sympy as sp


PILOT = Path(__file__).resolve().parents[3]
GOLDEN = (sp.sqrt(5)-1)/2
FIELD = sp.QQ.algebraic_field(GOLDEN)
P = FIELD.from_sympy(GOLDEN)
R = P**2


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def source_pins():
    pins = {
        "direct/round82/assembly/REUSED_BIT_RU.md":
            "d3a3d58e7eb85a956ac20489c28ee6b8c3d18f5da3163d0875829ac6f9e78188",
        "direct/round82/device/PREPAID_REPORT_RU.md":
            "7f6c1d4386af55e9d2a2a1a3998aee3150da2046686a2329c23530c2531582fc",
    }
    for name, expected in pins.items():
        require(sha256((PILOT/name).read_bytes()).hexdigest() == expected, name)
    return len(pins)


def golden_interval(value):
    resolution = 10**400
    low = Fraction(isqrt(5*resolution**2)-resolution, 2*resolution)
    high = low+Fraction(1, 2*resolution)
    require(low**2+low < 1 < high**2+high, "wrong Golden constant interval")
    coefficients = [Fraction(c.numerator, c.denominator) for c in value.to_list()]
    coefficients = [Fraction(0)]*(2-len(coefficients)) + coefficients
    slope, constant = coefficients
    endpoints = (constant+slope*low, constant+slope*high)
    return min(endpoints), max(endpoints)


def inside(value, lower, upper, reason):
    low, high = golden_interval(value)
    require(Fraction(lower) < low <= high < Fraction(upper), reason)


def measurement_probability(k):
    # cos(8 k theta)=T_{4k}(cos(2 theta)) and cos(2 theta)=p^3.
    previous = FIELD.one
    current = P**3
    for _ in range(2, 4*k+1):
        previous, current = current, 2*(P**3)*current-previous
    return (1-current)/2


def record(field, mask, colour, late_zero):
    disclosed = False
    serial = []
    for success in mask:
        active_colour = colour if field and (not disclosed or not late_zero) else 0
        first = int(success and active_colour == 1)
        second = int(success and not first)
        head = field ^ first ^ second
        serial.append((first, second, head))
        disclosed = disclosed or bool(success)
    return tuple(serial)


def check_support(eta, horizon, late_zero):
    wait = 1-eta
    masked_unresolved = P**4/wait
    masked_resolve = P**4/eta
    term_0 = P**3/wait + P**5/eta
    totals = [FIELD.zero, FIELD.zero]
    means = [FIELD.zero, FIELD.zero]
    weights = [FIELD.zero, FIELD.zero]
    distinct = [set(), set()]
    for mask in product((0, 1), repeat=horizon):
        hits = sum(mask)
        mask_mass = eta**hits * wait**(horizon-hits)
        for field in (0, 1):
            by_colour = []
            colours = ((0, P), (1, R)) if field and hits else ((0, FIELD.one),)
            for u, colour_mass in colours:
                bits = record(field, mask, u, late_zero)
                require(bits not in distinct[field], "erased or duplicated raw leaf")
                distinct[field].add(bits)
                length = sum(3+sum(read) for read in bits) + 2*u
                mass = mask_mass * colour_mass
                cost_weight = P**length / mass
                totals[field] += mass
                means[field] += mass * length
                weights[field] += cost_weight
                by_colour.append((length, mass, cost_weight))
            if len(by_colour) == 2:
                (len0, mass0, weight0), (len1, mass1, weight1) = by_colour
                require(len1-len0 == 2 and mass1 == P*mass0 and weight1 == P*weight0,
                        "lost mixed cancellation or true colour odds")
    require(totals == [FIELD.one, FIELD.one], "lost Born normalization")
    require([len(keys) for keys in distinct] == [2**horizon, 2**(horizon+1)-1],
            "wrong physical support size")
    expected_field = horizon*(1-2*eta)+2*R*(1-wait**horizon)
    require(means[1]-means[0] == expected_field, "wrong mean billed source")

    sigma = P**(-2)
    pending = settled = FIELD.one
    for _ in range(horizon):
        pending = masked_unresolved*pending+masked_resolve*sigma*settled
        settled = (masked_unresolved+masked_resolve)*settled
    require(weights == [term_0**horizon, pending], "wrong exact positive recursion")
    return sum(len(keys) for keys in distinct)


def check_causal_constraints(horizon):
    # Columns: d_tau, a_(j,0/1), d_end. All constraints compare
    # actual nonempty masks with one fixed nonempty reference mask.
    masks = [mask for mask in product((0, 1), repeat=horizon) if any(mask)]
    rows = []
    for mask in masks:
        tau = mask.index(1)
        row = [0]*(horizon+2*(horizon-1)+1)
        row[tau] = row[-1] = 1
        for j in range(tau+1, horizon):
            row[horizon+2*(j-1)+mask[j]] = 1
        rows.append(sp.Matrix([row]))
    terminal = sp.Matrix.vstack(*(row-rows[0] for row in rows))
    local = []
    for j in range(1, horizon):
        row = sp.zeros(1, terminal.cols)
        row[horizon+2*(j-1)+1] = 1
        row[horizon+2*(j-1)] = -1
        local.append(row)
    for tau in range(horizon-1):
        row = sp.zeros(1, terminal.cols)
        row[tau], row[horizon-1] = 1, -1
        for j in range(tau+1, horizon):
            row[horizon+2*(j-1)] = 1
        local.append(row)
    comparison = sp.Matrix.vstack(*local)
    expected_rank = 2*horizon-2
    require(terminal.rank() == comparison.rank() == expected_rank
            and sp.Matrix.vstack(terminal, comparison).rank() == expected_rank,
            "local causal requirements do not recover all terminal equalities")
    return expected_rank


def candidate_bounds():
    eta = measurement_probability(5)
    inside(eta, "0.4730329632", "0.4730329633", "wrong native k=5")
    inside(eta-R, "0.0910", "0.0911", "missing upper-sum direction")
    wait = 1-eta
    slope = 12*(1-2*eta)-P*(1-wait**12)
    inside(slope, "0.02945830", "0.02945831", "wrong source sign")
    denominator = eta + R*wait
    s = P/denominator
    d = P*eta/denominator
    sigma = P**(-2)
    ratio = sigma*s**12+(1-sigma)*d**12
    inside(ratio, "0.91986643", "0.91986645", "wrong conditional partition ratio")

    low = measurement_probability(1)
    inside(1-(3+R)*low, "0.2881", "0.2882", "lost low-power mean positivity")
    inside(P/(low+R*(1-low)), "1.2069", "1.2070",
           "missed low-power conditional sum reversal")
    return {"k": 5, "n": 12, "resolved_colour_price_gap": 2,
            "mean_slope": ["0.02945830", "0.02945831"],
            "conditional_partition_ratio": ["0.91986643", "0.91986645"]}


def main():
    scanned = sum(check_support(measurement_probability(k), horizon, switch)
                  for k in (1, 5) for horizon in range(1, 7)
                  for switch in (False, True))
    ranks = [check_causal_constraints(n) for n in range(2, 7)]
    print(json.dumps({
        "candidate": candidate_bounds(),
        "exact_terminal_records_scanned": scanned,
        "causal_constraint_ranks": ranks,
        "source_pins": source_pins(),
        "full_book_price_selected": False,
        "GR_closed": False,
        "status": "PASS",
    }, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
