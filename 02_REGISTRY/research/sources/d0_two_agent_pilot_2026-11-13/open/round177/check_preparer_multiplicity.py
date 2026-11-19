"""Certified passive return of the existing and refined B174 material word."""

from ast import Assign, Name, literal_eval, parse
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path
import sys

from mpmath import iv, mp

HERE = Path(__file__).resolve().parent
PILOT = HERE.parents[1]
SOURCE = PILOT / "open/round174/material/RESULT.json"
A85_SOURCE = PILOT / "direct/round85/clock/check_cycle_feedback.py"
sys.path.insert(0, str(PILOT / "open/round175/center"))
from check_centered_motion import interval_rotation, require, signs

L = 8
FIELDS = (Fraction(3, 8), Fraction(5, 8))


def interval(x):
    return iv.mpf(x.numerator) / x.denominator


def asin(x):
    return iv.atan2(x, iv.sqrt(1 - x*x))


def average(values):
    return sum(values) / len(values)


def field_targets(p):
    amplitude = iv.mpf(1) / (128 * iv.sin(iv.pi / 8))
    sites = [(t, 2 * iv.pi * n / L) for t in map(interval, FIELDS) for n in range(L)]
    target = []
    overlaps = []
    for t, phase in sites:
        x = amplitude * iv.sqrt(1+t) * iv.cos(phase)
        y = amplitude * iv.sqrt(1-t) * iv.sin(phase)
        target.append((asin(x / iv.sqrt(p*p-y*y)), asin(y/p)))
        overlaps.append(p + p * iv.sqrt(p*p - x*x - y*y))
    return target, overlaps


def refine_powers(theta, targets, denominator_limit, column_error):
    alpha = 16 * mp.mpf(theta.mid) / (2*mp.pi)
    rational = Fraction(str(alpha)).limit_denominator(denominator_limit)
    q = rational.denominator
    inv = pow(rational.numerator, -1, q)

    def select(target):
        grid = int(mp.nint(q * mp.mpf(target.mid) / (2*mp.pi)))
        k = (grid * inv + q//2) % q - q//2
        if abs(mp.mpf(target.mid)) < mp.mpf("1e-50"):
            k = 0
        angle = 16 * k * theta
        wrap = int(mp.nint(mp.mpf((angle-target).mid)/(2*mp.pi)))
        defect = abs(angle-target-2*wrap*iv.pi)
        return k, defect

    anchor, defect = select(theta)
    error = defect
    powers = []
    for axis in range(2):
        current = []
        for mask in range(2*L):
            coefficient = average([signs(mask, n)*x[axis] for n, x in enumerate(targets)])
            k, defect = select(coefficient)
            current.append(k)
            error += defect
        powers.append(current)
    require((2*error).b < iv.mpf(column_error), "Refined all-column operator bound")
    return anchor, powers


def native_overlaps(p, anchor, powers):
    a = iv.sqrt(p)
    overlaps = []
    for site in range(2*L):
        x, y = [16*sum(k*signs(mask, site) for mask, k in enumerate(axis))
                for axis in powers]
        state = [iv.mpf(0), a, p, iv.mpf(0)]
        for i, j, exponent in ((1, 2, -16*anchor), (2, 0, -x), (2, 3, -y),
                               (1, 2, 16*anchor), (2, 3, y), (2, 0, x)):
            c, s = interval_rotation(p, exponent)
            u, v = state[i], state[j]
            state[i], state[j] = c*u-s*v, s*u+c*v
        overlaps.append(a*state[1] + p*state[2])
    return overlaps


def two_ends(overlaps):
    result = []
    for k in (0, L):
        sites = overlaps[k:k+L]
        one = average(sites)**2
        independent_two = one**2
        shared_two = average([d*d for d in sites])**2
        require((shared_two-independent_two).a > 0, "Common SITE is not an independent tensor")
        result.append((one, shared_two-independent_two))
    return result


def inside(value, lo, hi):
    require(value.a > iv.mpf(lo) and value.b < iv.mpf(hi), f"Not in ({lo}, {hi}): {value}")
    return [lo, hi]


def existing_a85_slots(p):
    a = iv.sqrt(p)
    records = []
    assignments = [node for node in parse(A85_SOURCE.read_text()).body if isinstance(node, Assign)]
    modes = next(literal_eval(node.value) for node in assignments
                 if any(isinstance(target, Name) and target.id == "modes" for target in node.targets))
    checks = (("0.00237107", "0.00237108"), ("0.02607157", "0.02607158"))
    require(len(modes) == len(checks), "A85 names changed")
    for powers, bounds in zip(modes, checks):
        angles = [interval_rotation(p, 4*m) for m in powers]
        require(all(abs(v).a > 0 for pair in angles for v in pair), "Every copied slot outcome is active")
        c = p*angles[0][0] + p**2*angles[1][0]
        s = p*angles[0][1] + p**2*angles[1][1]
        records.append(inside((a*c+p*s)**2, *bounds))
    return {
        "passive_square_by_A85_name": records,
        "read_second_slot_four_outcomes_passive_square": "(p^2+p^4)^2",
        "retained_second_slot_to_read_second_slot_ratio": "p^2 xi/(p^2+p^4)^2",
        "design_uses_both_bank_requests_before_flag": True,
    }


def main():
    iv.dps = 76
    mp.dps = 78
    p = (iv.sqrt(5)-1)/2
    a = iv.sqrt(p)
    born = [p, p*p]
    passive_early = [(a*a*a)**2, (p*p*a)**2]
    passive_late = [(a*a)**2, (p*a)**2]
    for actual, exact in ((passive_early, (p**3, p**5)), (passive_late, (p**2, p**3))):
        require(all((val-ref).a <= 0 <= (val-ref).b for val, ref in zip(actual, exact)),
                "Passive flag powers")
    require((sum(born)-1).a <= 0 <= (sum(born)-1).b, "All raw exits retained")

    original = json.loads(SOURCE.read_text())
    require(original["dyadic_L"] == L and original["field_endpoints"] == [float(t) for t in FIELDS],
            "Pinned B174 preparation changed")
    targets, exact = field_targets(p)
    anchor, powers = refine_powers(asin(p), targets, 10**9, "8e-8")
    short_anchor, short_powers = refine_powers(asin(p), targets, 3*10**6, "4.2e-5")
    left, right = two_ends(native_overlaps(p, short_anchor, short_powers))
    short_s = 4*(right[0]-left[0])
    ideal, native, fine = [two_ends(values) for values in
                           (exact, native_overlaps(p, 7596, original["cartesian_walsh_powers"]),
                            native_overlaps(p, anchor, powers))]
    exact_s, native_s, fine_s = [4*(right[0]-left[0]) for left, right in (ideal, native, fine)]
    data = {
        "status": "PASS",
        "pinned_material_receipt_sha256": sha256(SOURCE.read_bytes()).hexdigest(),
        "L": L,
        "fields": ["3/8", "5/8"],
        "A85_literal_source_sha256": sha256(A85_SOURCE.read_bytes()).hexdigest(),
        "return_square_secants": {
            "ideal": inside(exact_s, "-5.693e-8", "-5.692e-8"),
            "actual_B174": inside(native_s, "-1.189e-5", "-1.188e-5"),
            "refined_native_plan": inside(fine_s, "-5.673e-8", "-5.672e-8"),
            "shorter_native_plan": inside(short_s, "-5.841e-8", "-5.840e-8"),
            "actual_relative_to_ideal": inside(native_s/exact_s, "208", "210"),
        },
        "shared_SITE_minus_independent_return_square": {
            "ideal": [inside(ideal[0][1], "6.110e-9", "6.112e-9"),
                      inside(ideal[1][1], "1.697e-8", "1.698e-8")],
            "actual_B174": [inside(native[0][1], "8.637e-9", "8.638e-9"),
                             inside(native[1][1], "1.855e-8", "1.856e-8")],
        },
        "flags": {
            "each_Born_masses": ["p", "p^2", "0"],
            "RI4_copied_flag_after_NC1_passive_squares": ["p^3", "p^5"],
            "material_flag_NC1_passive_squares": ["p^2", "p^3"],
        },
        "same_prefix_cold_count_test": existing_a85_slots(p),
        "refinement": {
            "common_anchor_power": anchor,
            "cartesian_walsh_powers": powers,
            "square_word_G_count": 32*(abs(anchor)+sum(abs(k) for axis in powers for k in axis)),
            "all_column_analytic_error_upper_bound": "8e-8",
            "literal_expansion_run": False,
        },
        "shorter_refinement": {
            "common_anchor_power": short_anchor,
            "cartesian_walsh_powers": short_powers,
            "square_word_G_count": 32*(abs(short_anchor)+sum(abs(k) for axis in short_powers for k in axis)),
            "all_column_analytic_error_upper_bound": "4.2e-5",
            "literal_expansion_run": False,
        },
        "new_combined_paid_carrier_executed": False,
        "book_cost_minus_info_identified": False,
        "GR_closed": False,
    }
    print(json.dumps(data, indent=2))


if __name__ == "__main__":
    main()
