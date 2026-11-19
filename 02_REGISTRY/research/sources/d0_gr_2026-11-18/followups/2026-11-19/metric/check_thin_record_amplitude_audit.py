"""Exact native branch effects and a conservative thermal amplitude test.

This is not a test of the unknown full physical Cost-Info and does not
establish the same-execution source or GR closure. It replays the original
35-stage reader on all 16 old columns, using its existing exact checker.
"""
from fractions import Fraction
from math import exp, log, sqrt

from check_fresh_guard_reader import golden_tables, native_columns
from check_source_price import need


def main():
    rows, *_ = golden_tables()
    native = native_columns(rows)
    need(native["old_input_dimension"] == 16, "all 16 old columns")
    need(native["total_stages"] == 35, "all 35 physical stages")
    branch = {(r["T"], r["H"], r["E"]): r for r in rows}
    zero, one = branch[0, 0, 0], branch[0, 1, 0]
    need((zero["literal_length"], one["literal_length"]) == (4, 5), "full literal code")
    need((zero["conditional_info_phi"], one["conditional_info_phi"]) == (2, 3), "declared conditional information")
    need((zero["declared_net_price"], one["declared_net_price"]) == (2, 2), "same declared price")

    # For beta <= 1, L >= 2, the full scene bound is at most 3/352.
    # e < 11/4 and e^2 < 8 give s >= exp(-2 beta) > 1/8.
    epsilon = Fraction(3, 352)
    minimum_s = Fraction(1, 8)
    chi = (minimum_s + epsilon) / (minimum_s - epsilon)
    need(chi == Fraction(47, 41), "exact heat ratio upper bound")
    # p < 5/8 and (47/41)^2 * 5/8 < 1 establish chi < 1/sqrt(p)
    # without relying on floating-point roots.
    need(chi * chi * Fraction(5, 8) < 1, "exact thermal amplitude obstruction")
    p = (sqrt(5) - 1) / 2
    need(2*p*p < 1, "the example beta is below one")
    need(exp(-2) > float(minimum_s), "numerical cross-check of thermal lower bound")
    need(2*(exp(1/11) - 1 - 1/11) < float(epsilon), "numerical cross-check of thermal tail")
    need(float(chi) < 1/sqrt(p), "numerical cross-check of amplitude threshold")
    gap = 0.5 - log(float(chi))/log(1/p)
    need(gap > 0.216, "strict positive branch-price gap")
    print("Native reader: 35 stages, all 16 old input columns verified")
    print("Two declared prices: s_000 = s_010 = 2")
    print("Born ratio = p; positive amplitude ratio = sqrt(p)")
    print(f"Conservative thermal ratio upper bound = {chi}")
    print(f"Positive branch-price gap > {gap:.12f} phi-units")
    print("Status: direct component identification excluded under stated conditions; GR open")


if __name__ == "__main__":
    main()
