"""Exact native router, cold cross difference, and registered A86 accounting."""

from collections import Counter
from hashlib import sha256
from math import factorial
from pathlib import Path
from runpy import run_path
import json

from mpmath import iv

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
A85 = PILOT / "direct/round85/clock/check_cycle_feedback.py"
A86 = PILOT / "direct/round86/recovery/check_writer_history.py"


def require(value, message):
    if not value:
        raise ArithmeticError(message)


def enclosed(value, lower, upper):
    require(value.a > iv.mpf(lower) and value.b < iv.mpf(upper),
            f"outside ({lower}, {upper}): {value}")
    return [lower, upper]


def router():
    # Wires 0,1 are the field bank, 2,3 the dummy and 4,5 the same receiver.
    swap = tuple(edge for j in range(2) for edge in ((j, j+2), (j+2, j), (j, j+2)))
    copy = ((2, 4), (3, 5))
    read_bank = swap + copy + swap
    read_dummy = copy + swap + swap
    require(Counter(read_bank) == Counter(read_dummy) and len(read_bank) == 14,
            "Comparison must use the same literal gate addresses")

    def evaluate(word, column):
        state = column
        for control, target in word:
            if (state >> control) & 1:
                state ^= 1 << target
        return state

    for column in range(64):
        require(evaluate(read_bank, column) == column ^ ((column & 3) << 4),
                "Bank must be restored, including all receiver input columns")
        require(evaluate(read_dummy, column) == column ^ (((column >> 2) & 3) << 4),
                "Dummy must be restored, including all receiver input columns")
    return {"CX_per_slot": len(read_bank), "all_raw_columns_per_setting": 64}


def spectral_test(owner):
    p, a, z = owner["P"], owner["A"], owner["z"]
    sigma = (p**2+p**4)**2
    diagnostics = (
        (("-5.294e-10", "-5.293e-10"), ("5.306e-10", "5.307e-10"), ("1.258e-12", "1.259e-12")),
        (("-1.258e-11", "-1.257e-11"), ("1.291e-11", "1.292e-11"), ("3.366e-13", "3.367e-13")),
    )

    beta = 2*p**2
    x = beta/11
    cap = 16
    one_log_heat_error = iv.mpf(132)/359*x**cap/factorial(cap)/(1-x/(cap+1))
    require((4*one_log_heat_error).b < iv.mpf("2.067e-32"),
            "Complete heat cannot reverse either cross sign")
    records = []
    marked_cross_bounds = (("-1.645e-12", "-1.643e-12"), ("-3.906e-14", "-3.904e-14"))
    marked_first_bounds = (("2.668e-12", "2.670e-12"), ("6.552e-14", "6.553e-14"))
    for name, (cross_bounds, first_bounds, last_bounds) in enumerate(diagnostics):
        _, c, s = owner["lane"](name, 1)
        _, initial_marked, _ = owner["feedback"](name, 1, 1)
        xi = (a*c+p*s)**2
        A = 1-z+z*p**2
        B = z*p**6*initial_marked*sigma**2
        cross = -8*iv.log1p(A*B*(1-xi)**2/(A+B*xi)**2)
        first = 8*iv.log1p(B*(1-xi)/(A+B*xi))
        last = 8*iv.log1p(B*xi*(1-xi)/(A+B*xi**2))
        require((first-2*one_log_heat_error).a > 0 and (last-2*one_log_heat_error).a > 0
                and (cross+4*one_log_heat_error).b < 0, "All full spectral signs")
        read_sigma = p**2*sigma
        s0 = read_sigma*(p**3+p**5*xi)
        s1 = read_sigma*(p**5+p**3*xi)
        rho = s1/s0
        B_marked = z*p**6*initial_marked*s0**2
        marked_cross = -8*iv.log1p(A*B_marked*(1-rho)**2/(A+B_marked*rho)**2)
        marked_first = 8*iv.log1p(B_marked*(1-rho)/(A+B_marked*rho))
        require((marked_cross+4*one_log_heat_error).b < 0
                and (marked_first-2*one_log_heat_error).a > 0,
                "Retaining both count flags must preserve the full signs")
        records.append({
            "name": name,
            "cold_cross_log": enclosed(cross, *cross_bounds),
            "cold_first_log_increment": enclosed(first, *first_bounds),
            "cold_last_log_increment": enclosed(last, *last_bounds),
            "all_count_flags_included_cold_cross_log": enclosed(marked_cross, *marked_cross_bounds[name]),
            "all_count_flags_included_first_increment": enclosed(marked_first, *marked_first_bounds[name]),
            "full_spectral_vs_independent_tariff_sup_log_error_lower_bound":
                "1.323e-10" if name == 0 else "3.142e-12",
        })
    return {
        "router": router(),
        "unchanged_reporter": "A85 fixed-port mark",
        "index_settings": ["00", "01", "10", "11"],
        "even_terminal_CX_tail": cap,
        "max_error_in_full_cross_log_from_heat": "2.067e-32",
        "names": records,
        "composite_clock_executed": False,
    }


def printed_service_test(owner):
    p, ell, theta = owner["p"], owner["ell"], owner["theta"]
    s0, s2, s3 = 2*p**3, 4*p**3, 16*p**9
    ready, weight = owner["ready"], owner["reg_weight"]
    b = weight(s0, 1, 16)
    success = b**86 * weight(s2, 1, 32)**86 * weight(s2, 2, 32)**86 * weight(s3, 1, 32)**46
    ordinary_abort = ((1-s0)*p)**16*(1-b**86)/(1-b)
    extra_abort = b**86
    abort = iv.mpf([ordinary_abort.a, (ordinary_abort+extra_abort).b])
    relative_at_zero = abort/(p*success)

    gamma = ready(s0, 16)**86 * ready(s2, 32)**172 * ready(s3, 32)**46
    r = 4*p**3*(p*iv.sin(712*theta))**2

    def paid_success_fraction(padding):
        return 1/(1+relative_at_zero*p**padding)

    def difference(fraction):
        return -iv.log1p(-fraction*(1-p)*r)/ell

    pass_half = 818
    pass_ninety_nine = 827
    require(paid_success_fraction(pass_half-1).b < iv.mpf(".5") <
            paid_success_fraction(pass_half).a, "Smallest half threshold")
    require(paid_success_fraction(pass_ninety_nine-1).b < iv.mpf(".99") <
            paid_success_fraction(pass_ninety_nine).a, "Smallest 99 percent threshold")

    cap = 32
    x_code = 2*p**2*(1-p**(2*cap))+p**(2*cap)
    one_flag_success_kraft = (1-p**16)**86*(1-p**32)**132
    ready_kraft = one_flag_success_kraft*(2*p**2*(1-p**64))**86
    complete_ternary = p+p**3+p**4
    require(complete_ternary.a <= 1 <= complete_ternary.b, "Complete recoding weights")
    prefix_free = ("0", "100", "1010")
    require(not any(left != right and right.startswith(left)
                    for left in prefix_free for right in prefix_free), "Prefix code")

    width = 86*(16+1)+86*(32+1)+86*(2*32+1)+46*(32+1)
    return {
        "normalization_at_fixed_zero_click_in_report": {
            "ready_fraction_after_817_real_failure_zeros":
                enclosed(paid_success_fraction(817), ".461", ".462"),
            "ready_fraction_after_818_real_failure_zeros":
                enclosed(paid_success_fraction(818), ".580", ".581"),
            "first_padding_for_half_ready_weight": pass_half,
            "first_padding_for_99_percent_ready_weight": pass_ninety_nine,
            "log_price_difference_with_827_zeros":
                enclosed(difference(paid_success_fraction(827)), "9.20e-5", "9.24e-5"),
            "service_record_width_for_equal_padding": width,
            "equal_width_log_price_difference":
                enclosed(difference(gamma), "9.04262e-5", "9.04264e-5"),
        },
        "printed_Kraft": {
            "Kraft_tree_upper_bound": enclosed(1-(1-x_code)*one_flag_success_kraft,
                                                ".77296210504772", ".77296210504774"),
            "two_flag_X_retry_Kraft": enclosed(x_code, ".76393202250021", ".76393202250023"),
            "F6_minus_F5_support_Kraft": enclosed(p**2*ready_kraft, "3.21952e-11", "3.21953e-11"),
            "alternative_ternary_words": prefix_free,
        },
        "price_of_added_record_devices_is_included_in_known_ledger": False,
        "padded_composite_executed": False,
    }


def material_anchor():
    # Two CX copy the CAR low and high into their own physical cleared heads.
    def code(raw, prior):
        low, high = raw & 1, (raw >> 3) & 1
        return prior ^ ((high << 1) | low)

    for raw in range(16):
        require(len({code(raw, prior) for prior in range(4)}) == 4,
                "Both pointer operations are reversible on all columns")
    occupied = (0, 1, 14, 15)
    require([code(raw, 0) for raw in occupied] == list(range(4)), "Four CAR masks")
    return {
        "logical_car_head_columns": 64,
        "marked_car_basis_labels": list(occupied),
        "occupied_anchor": "e1 at mark 01",
        "conditional_ready_anchor_probability": "p",
        "material_moment_reads_only": ["00", "11"],
        "markers_given_known_positive_bit": {"births": 4, "G": 4, "CX": 10},
        "composite_executed": False,
    }


def main():
    clock = run_path(str(A85))
    history = run_path(str(A86))
    history["iv"].dps = 90
    data = {
        "status": "PASS",
        "owner_checksums": {
            str(path.relative_to(PILOT)): sha256(path.read_bytes()).hexdigest()
            for path in (A85, A86)
        },
        "matched_slot_spectral_obstruction": spectral_test(clock),
        "written_service_prices": printed_service_test(history),
        "ready_material_anchor": material_anchor(),
        "full_book03_valuation_identified": False,
        "GR_closed": False,
    }
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
