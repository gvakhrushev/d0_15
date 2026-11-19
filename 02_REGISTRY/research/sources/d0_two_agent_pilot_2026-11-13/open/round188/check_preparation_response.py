"""Exact receipts for the occupied clock, coherent price and shared SITE tests."""

from collections import Counter
from fractions import Fraction
from itertools import product
import json
from pathlib import Path
import sys

PILOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PILOT / "open/round182"))
from check_serial_book03 import a, actual_words, one, overlap, p, prefixes, require


def clock_and_work():
    words = actual_words()
    w0, w1 = words["CX_18"], words["G_Z_G_Z"]
    occupied = tuple({spin: a, spin + 4: p} for spin in range(4))
    for word, first, second in ((w0 + w1, 3, 19), (w1 + w0, 1, 33)):
        states = prefixes(word, occupied)
        require(first % 16 == second % 16, "The clock slots must coincide")
        require(states[first - 1] == states[second - 1] == occupied,
                "The full occupied input must coincide")
        for u, v in zip(states[first], states[second]):
            inner = overlap(u, v)
            require(inner == a and one - inner*inner == p*p,
                    "The requested pure outputs must be trace distance p apart")

    g, z = w1[:1], w1[1:9]
    identity = g + z + g + z
    inverse_square = z + g + g + z
    blank = tuple({spin: one} for spin in range(4))
    require(Counter(identity) == Counter(inverse_square) and len(identity) == 18,
            "Use the same complete gate inventory for preparing both inputs")
    work0 = prefixes(inverse_square + g, occupied)[-1]
    work2 = prefixes(identity + g, occupied)[-1]
    require(work0 == blank and work2 == prefixes(g + g, blank)[-1],
            "The two preparations must give rotation angles 0 and 2 theta")
    contrasts = []
    for initial in (work0, work2):
        first0 = prefixes(w0[:1], initial)[-1]
        first1 = prefixes(w1[:1], initial)[-1]
        contrast = [sum(x*x for k, x in v.items() if k & 4) -
                    sum(x*x for k, x in u.items() if k & 4)
                    for u, v in zip(first0, first1)]
        require(all(c == contrast[0] for c in contrast), "Protected Spin dependence")
        contrasts.append(contrast[0])
        require(prefixes(w0 + w1, initial)[-1] == prefixes(w1 + w0, initial)[-1]
                == initial, "The serial endpoints must agree")
    delta = contrasts[1] - contrasts[0]
    require(contrasts[0] == p*p and delta == 44*one - 72*p and delta != 0,
            "Wrong first-tick occupancy contrast")
    return {"same_work_input_trace_distance": "p",
            "minimum_history_tag_distance_for_output_error_epsilon": "max(0,p-2 epsilon)",
            "same_inventory_first_tick_double_difference": "44-72p"}


def coherent_roles():
    bright_i = p + p*p
    bright_z = p - p*p
    require(bright_i == one and bright_z == p*p*p, "Native bright-port amplitudes")
    require(bright_z * (p + 2) == p and bright_z * (p*p - 2) == -p*p,
            "The change of normalized coefficients must be (+2,-2)")
    require(bright_z*bright_z + 4*p*p*p == one, "Both detector outputs must normalize")
    return {"native_bright_port_weights_I": ["p", "p^2"],
            "native_bright_port_weights_Z": ["p+2", "p^2-2"],
            "absolute_common_prefix_coefficient": 1,
            "bright_port_relative_preparation_row": "2*(D S_pre(0)-D S_pre(1))"}


def site_test():
    rotor = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def material(site, v):
        return rotor[(site[1] + v * site[2]) % 4]

    def differences(site, axis, v):
        next_site = list(site)
        next_site[axis] += 1
        return tuple(b - a for a, b in zip(material(site, v), material(next_site, v)))

    local = []
    for site in product(range(4), repeat=4):
        moment = sum((1 if axis == 0 else -1) *
                     sum(x*y for x, y in zip(differences(site, axis, 0),
                                            differences(site, axis, 1)))
                     for axis in range(4))
        local.append(Fraction(moment, 2))
    require(Counter(local) == {-1: 64, 0: 128, 1: 64}, "Wrong SITE moments")
    mean = sum(local) / len(local)
    variance = sum(value*value for value in local) / len(local)
    require(mean == 0 and variance == Fraction(1, 2), "Wrong SITE moment laws")
    # At t=0, packet weights are (1+tF)/256 and effects are (1 +/- eF)/2.
    # Expected masses are 1/2, so their log-ratio slope divided by e is 2 E[F^2].
    relative_slope = 2 * variance
    require(relative_slope == 1, "The shared SITE source survives at equal masses")
    return {"comparison_descriptors": ["00", "01"],
            "site_mean": str(mean), "site_second_moment": str(variance),
            "relative_log_slope_divided_by_epsilon": str(relative_slope)}


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "clock": clock_and_work(),
                      "coherent_preparation": coherent_roles(), "shared_site": site_test(),
                      "absolute_Cost_minus_Info_cancellation_proved": False,
                      "GR_closed": False}, indent=2))
