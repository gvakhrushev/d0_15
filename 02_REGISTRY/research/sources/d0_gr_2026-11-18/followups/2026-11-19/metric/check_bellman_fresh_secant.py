"""Actual descriptor/reader and interval checks for a conditional ledger.

No claim is made that the two devices have been physically composed, that
their success is certain, or that Book03 selects BORN+GAIN.
"""
from collections import Counter
from itertools import product
from mpmath import iv

from check_fresh_guard_reader import golden_tables, native_columns
from check_native_golden_descriptor_secants import check_columns
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
    print("Actual reader: 35 stages; descriptor n=8: 2048 logical columns")
    print("q0 = p^2; q1 = p^2 + p^9 on the stated successful branches")
    print("Bellman registered-code secant:", s_bell)
    print("Fresh conditional factor secant:", s_fresh)
    print("Required extra ledger in the explicitly ideal diagnostic:", needed)
    print("Full success/failure and source/lift remain physical obligations; GR open")


if __name__ == "__main__":
    main()
