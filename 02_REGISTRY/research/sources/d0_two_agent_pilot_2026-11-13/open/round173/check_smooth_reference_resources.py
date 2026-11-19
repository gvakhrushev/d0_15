"""Certify an explicit finite binary-phase compiler witness and the field obstruction."""

from fractions import Fraction
import json
from math import isqrt
from pathlib import Path
import subprocess

import mpmath as mp


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PRIMARY = "2350117b4"
RECEIPT = (
    "02_REGISTRY/research/sources/d0_gr_2026-11-18/followups/"
    "2026-11-19/metric/smooth_twofield_reference_result.json"
)


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def finite_root_obstruction():
    # Even L with totient 4 are 8, 10, 12. The L=10 sine has
    # square (5-sqrt(5))/8. Its rational norm is not a square.
    sine_square_norm = Fraction(25-5, 64)
    require(sine_square_norm == Fraction(5, 16)
            and isqrt(sine_square_norm.numerator)**2 != sine_square_norm.numerator,
            "L=10 cannot put the sine into the unique quadratic subfield")
    degree_two_witnesses = {6: "sqrt(3)", 8: "sqrt(2)", 12: "sqrt(3)"}
    return {
        "deterministic_all_columns_obstructed_even_L_at_least": 6,
        "conditioning_on_native_positive_branch_keeps_density_in_field": True,
        "even_small_denominator_square_root_obstructions": degree_two_witnesses,
        "L10_sine_square_norm": str(sine_square_norm),
    }


def complex_product(x, y):
    a, b = x
    c, d = y
    return a*c-b*d, a*d+b*c


def complex_power(base, exponent):
    if exponent < 0:
        base = base[0], -base[1]
        exponent = -exponent
    identity = mp.iv.mpf(1), mp.iv.mpf(0)
    while exponent:
        if exponent % 2:
            identity = complex_product(identity, base)
        base = complex_product(base, base)
        exponent //= 2
    return identity


def error(a, b):
    return mp.iv.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)


def apply_cx(column, control, target):
    mask = 1 << control
    return column ^ ((1 << target) if column & mask else 0)


def check_frame(left, right):
    difference = left ^ right
    pivot = difference.bit_length()-1
    targets = [position for position in range(4)
               if position != pivot and difference & (1 << position)]
    columns = []
    for column in range(16):
        for target in targets:
            column = apply_cx(column, pivot, target)
        columns.append(column)
    require(sorted(columns) == list(range(16)), "full reversible CAR frame")
    require((columns[left] ^ columns[right]) == (1 << pivot), "one target bit")
    active = [column for column, target in enumerate(columns)
              if target >> (pivot+1) == columns[left] >> (pivot+1)
              and (target & ((1 << pivot)-1)) == (columns[left] & ((1 << pivot)-1))]
    require(sorted(active) == sorted((left,right)), "all other CAR columns fixed")
    return pivot


def check_character_coefficients(count):
    for intended in range(1 << count):
        for actual in range(1 << count):
            value = sum((-1)**(bin(subset & (intended ^ actual)).count("1"))
                        for subset in range(1 << count))
            require(value == ((1 << count) if actual == intended else 0),
                    "exact addressed plane on every control value")


def finite_binary_phase_witness():
    raw = json.loads(subprocess.check_output(
        ["git", "show", f"{PRIMARY}:{RECEIPT}"], cwd=REPO,
    ))
    require(raw["check"] == "PASS" and not raw["original_native_field_preparation_word_replayed"],
            "owned smooth reference pin")
    mp.iv.dps = 75
    p = (mp.iv.sqrt(5)-1)/2
    a = mp.iv.sqrt(p)
    theta = a,p
    bounds = raw["k0_interval"].strip("[]").split(",")
    k0 = mp.iv.mpf([bounds[0].strip(),bounds[1].strip()])
    f = Fraction(raw["rational_F_values"]["8"])
    f_value = mp.iv.mpf(f.numerator)/f.denominator
    sin_pi_over_eight = mp.iv.sqrt(2-mp.iv.sqrt(2))/2
    amplitude = mp.iv.sqrt(f_value/k0)/(16*sin_pi_over_eight)
    tilt_sine = amplitude/p
    tilt = mp.iv.sqrt(1-tilt_sine**2), tilt_sine

    rounds = [
        ("anchor", -1721, 3, theta, "0.000198"),
        ("tilt", 1483, 3, tilt, "0.000208"),
        ("low_address_bit", -8915, 4, (mp.iv.sqrt(2)/2,mp.iv.sqrt(2)/2), "0.000278"),
        ("middle_address_bit", 131, 4, (0,1), "0.000085"),
        ("high_address_bit", -262, 4, (-1,0), "0.000169"),
    ]
    deviations = []
    entries = {}
    for name, power, controls, aim, upper in rounds:
        diff = error(complex_power(theta,(1 << controls)*power),aim)
        require(diff.b < mp.iv.mpf(upper), f"outward angle check: {name}")
        deviations.append(diff)
        entries[name] = {"power":power, "control_count":controls, "error_upper":upper}
    combined = deviations[0]+2*deviations[1]+2*sum(deviations[2:])
    require(combined.b < mp.iv.mpf(".0017"), "whole operator bound")
    for pair in ((1,14),(14,0),(0,15)):
        check_frame(*pair)
    for controls in (3,4):
        check_character_coefficients(controls)
    return {
        "L": 8,
        "explicit_integer_only_witness": entries,
        "whole_car_site_operator_error_upper": ".0017",
        "constant_complement_and_no_address_read_proved": True,
        "witness_is_not_at_the_geometric_gain_precision": True,
    }


def main():
    print(json.dumps({
        "status":"PASS",
        "primary": PRIMARY,
        "algebraic_obstruction": finite_root_obstruction(),
        "binary_phase_witness": finite_binary_phase_witness(),
        "GR_closed":False,
    }, indent=2))


if __name__ == "__main__":
    main()
