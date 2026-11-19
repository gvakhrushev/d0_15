"""Actual descriptor/reader and interval checks for a conditional ledger.

No claim is made that the two devices have been physically composed, that
their success is certain, or that Book03 selects BORN+GAIN.
"""
from collections import Counter
from itertools import product
from mpmath import iv

from check_fresh_guard_reader import golden_tables, native_columns
from check_native_golden_descriptor_secants import add, check_columns, mul, power
from check_source_price import need


def main():
    rows, *_ = golden_tables()
    native = native_columns(rows)
    need(native["total_stages"] == 35, "full fresh reader")
    count, ops = check_columns(8)  # existing exact column verifier
    need(count == 2048 and ops == Counter({"T": 17, "CX": 18}),
         "actual n=8 descriptor word and every logical column")
    for row in rows:
        t, h, e = row["T"], row["H"], row["E"]
        d = t ^ e
        need(row["literal_length"] == 4+d+(h ^ d)+e+t, "literal four codes")
        need(row["conditional_info_phi"] == 2+h+e, "canonical complete H,E mass")

    # Exact Q(p) calculation of the complete seed-record law, with no
    # postselection among its bit strings. The conditional successful
    # logical seed itself is not a complete physical factory execution.
    pp, rr = (0, 1), (1, -1)  # p, p^2
    totals = [(0, 0), (0, 0)]
    for seed_h, z, guard_h, e in product(range(2), range(256), range(2), range(2)):
        ones = bin(z).count("1")
        seed_weight = mul(rr if seed_h else pp,
                          mul(power(rr, ones), power(pp, 8-ones)))
        weight = mul(seed_weight, power(pp, 2+guard_h+e))
        for k in (0, 1):
            t = int(bool(seed_h or (k and z == 0)))
            d = t ^ e
            length = 4+d+(guard_h ^ d)+e+t
            totals[k] = add(totals[k], mul(weight, (length, 0)))
    difference = add(totals[1], (-totals[0][0], -totals[0][1]))
    need(difference == mul((5, -6), power(pp, 9)),
         "all seed/H/E columns give exact paid-code contrast c p^9")

    iv.dps = 60
    one = iv.mpf(1)
    p = (iv.sqrt(5)-one)/2
    ell = iv.log(one/p)
    kap = one/iv.sqrt(5)
    c = 5-6*p
    q0 = p*p
    delta = p**9
    q1 = q0+delta
    entropy = lambda q: -(q*iv.log(q)+(one-q)*iv.log(one-q))/ell
    f = lambda q: 2*entropy(q)+2*(one+p*p)-4*p-c*q
    a = lambda q: -iv.log(one-kap*q)/ell
    s_bell = (f(q0)-f(q1))/delta
    s_fresh = (a(q1)-a(q0))/delta
    needed = s_fresh-s_bell
    remainder_cost = s_fresh-c
    need(q1 < iv.mpf('0.4'), "real finite descriptor endpoint")
    # The derivative of -f is increasing; checking its upper endpoint
    # proves negativity on the entire actual interval.
    upper_derivative = c-2*iv.log((one-q1)/q1)/ell
    need(upper_derivative < 0, "Bellman declared-record secant is negative")
    need(s_bell > iv.mpf('-0.592887') and s_bell < iv.mpf('-0.592886'),
         "conditional Bellman secant interval")
    need(s_fresh > iv.mpf('1.124800') and s_fresh < iv.mpf('1.124801'),
         "conditional fresh secant interval")
    need(needed > iv.mpf('1.717686') and needed < iv.mpf('1.717688'),
         "diagnostic required additional ledger interval")
    need(remainder_cost > iv.mpf('-0.166996') and remainder_cost < iv.mpf('-0.166995'),
         "diagnostic required other cost after full seed entropy cancellation")
    print("Actual reader: 35 stages; descriptor n=8: 2048 logical columns")
    print("q0 = p^2; q1 = p^2 + p^9 on the stated successful branches")
    print("Bellman registered-code secant:", s_bell)
    print("Fresh conditional factor secant:", s_fresh)
    print("Required extra ledger in the explicitly ideal diagnostic:", needed)
    print("Exact full seed record: Delta expected LC1 code = (5-6p) p^9")
    print("Required other cost in the same ideal diagnostic:", remainder_cost)
    print("Full success/failure and source/lift remain physical obligations; GR open")


if __name__ == "__main__":
    main()
