"""Exact address and full-archive tests for one fresh common SITE centre."""

from collections import Counter
from fractions import Fraction as F
from itertools import product
import json
from pathlib import Path
import sys

import numpy as np

PILOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PILOT / "open/round189"))
from check_absolute_interference import Interval, report_coefficients, require


def add_coordinates(left, right):
    value = np.zeros_like(left, dtype=np.uint32)
    for shift in range(0, 8, 2):
        value |= (((left >> shift) + (right >> shift)) & 3) << shift
    return value


def coordinate_translation():
    pair = np.arange(256 * 256, dtype=np.uint32)
    x, tau = pair >> 8, pair & 255
    low_mask = 0b01010101
    # Four parallel in-place two-bit additions:
    # high ^= X.low & tau.low; high ^= X.high; low ^= X.low.
    shifted = tau ^ (((x & tau) & low_mask) << 1) ^ (x & ~np.uint32(low_mask))
    shifted ^= x & low_mask
    inverse = shifted ^ (x & low_mask) ^ (x & ~np.uint32(low_mask))
    inverse ^= ((x & inverse) & low_mask) << 1
    require(np.array_equal(shifted, add_coordinates(x, tau)), "Wrong mod-four recoding")
    require(np.array_equal(inverse, tau), "The relabelling must be reversible")
    ordered = np.sort(shifted.reshape(256, 256), axis=1)
    require(np.array_equal(ordered, np.tile(np.arange(256), (256, 1))),
            "No old SITE may change the fresh uniform plus state")
    return {"translated_columns": len(pair), "routing_CX": 8, "routing_Toffoli": 4}


def comparator(offset, centres, resources):
    registers = {}
    for name, values in (("k", centres), ("y", resources)):
        for index in range(8):
            registers[name, index] = ((values >> index) & 1).astype(np.uint8)
    for name, width in (("d", 8), ("a", 7)):
        for index in range(width):
            registers[name, index] = np.zeros(len(centres), dtype=np.uint8)
    registers["h", 0] = np.ones(len(centres), dtype=np.uint8)
    original = {key: values.copy() for key, values in registers.items()}

    gates = []
    if offset is not None:
        low, high = ("k", 2*offset), ("k", 2*offset+1)
        gates.extend(((low, high), (("h", 0), low)))
    for i in range(8):
        gates.extend(((("k", i), ("d", i)), (("y", i), ("d", i)),
                      (("h", 0), ("d", i))))
    gates.append((("d", 0), ("d", 1), ("a", 0)))
    for i in range(1, 7):
        gates.append((("a", i-1), ("d", i+1), ("a", i)))

    def apply(gate):
        if len(gate) == 2:
            registers[gate[-1]] ^= registers[gate[0]]
        else:
            registers[gate[-1]] ^= registers[gate[0]] & registers[gate[1]]

    for gate in gates:
        apply(gate)
    translated = centres
    if offset is not None:
        translated = add_coordinates(centres, np.full_like(centres, 1 << (2*offset)))
    desired = (translated == resources).astype(np.uint8)
    require(np.array_equal(registers["a", 6], desired), "Wrong NC1 head on a real column")
    for gate in reversed(gates):
        apply(gate)
    require(all(np.array_equal(registers[key], value) for key, value in original.items()),
            "Comparator must restore the centre, resource and scratch")

    counts = Counter(len(gate) for gate in gates)
    with_read = (2*counts[2]+2, 2*counts[3])
    require(with_read == ((50 if offset is None else 54), 14), "Wrong count with NC1")
    return with_read


def check_address():
    pair = np.arange(256 * 256, dtype=np.uint32)
    centre, resource = pair >> 8, pair & 255
    zero = comparator(None, centre, resource)
    shifted = [comparator(j, centre, resource) for j in range(4)]
    cx = 8*(2*zero[0] + 2*sum(count[0] for count in shifted))
    toffoli = 8*(2*zero[1] + 2*sum(count[1] for count in shifted))
    require((cx, toffoli) == (4256, 1120), "Wrong 80-comparator inventory")
    return {"columns_per_offset": len(pair), "offsets": 5, "comparators": 80,
            "CX_with_NC1": cx, "logical_Toffoli": toffoli,
            "fewer_CX_than_shifted_comparators": 6816-cx,
            "fewer_Toffoli_than_shifted_comparators": 1760-toffoli,
            "additional_NC1_births_and_G": [80, 80]}


def check_coherent_records():
    # Two old SITE values with arbitrary reference amplitudes represented by
    # independent, nonzero symbolic coefficients; three actual distinct
    # environment labels can include admitted successes or preserved failures.
    old = {1: (F(2, 3), F(3, 5)), 195: (F(5, 7), F(7, 11))}

    def label(k):
        return ("STOP" if k % 3 else "READY", (5*k+2) % 257)

    after = {}
    for (x, right), tau in product(product(old, range(2)), range(256)):
        k = int(add_coordinates(np.array([x], dtype=np.uint32),
                                np.array([tau], dtype=np.uint32))[0])
        after[x, right, k, label(k)] = old[x][right]/16

    direct = {(x, right, k, label(k)): old[x][right]/16
              for x, right, k in product(old, range(2), range(256))}
    require(after == direct, "Coherent output and all retained labels must factor")

    # A phase keyed by original X preserves every probability on a basis
    # column but acts nontrivially on superposed old X (the |+> overlap is zero).
    phase = {1: 1, 195: -1}
    signed = {key: value*phase[key[0]] for key, value in direct.items()}
    require(signed != direct and all(signed[key]**2 == v*v for key, v in direct.items()),
            "Equal effects must not be confused with equal isometries")
    return {"retained_coefficients_compared": len(after),
            "basis_effects_do_not_detect_x_phase": True}


def check_local_nonlinear_derivative():
    rotor = ((1, 0), (0, 1), (-1, 0), (0, -1))

    def difference(x, axis, descriptor_v):
        y = list(x)
        y[axis] += 1
        before = rotor[(x[1] + descriptor_v*x[2]) % 4]
        after = rotor[(y[1] + descriptor_v*y[2]) % 4]
        return [later - early for early, later in zip(before, after)]

    local = []
    for x in product(range(4), repeat=4):
        local.append(F(sum((1 if axis == 0 else -1) * sum(a*b for a,b in zip(
            difference(x, axis, 0), difference(x, axis, 1)))
            for axis in range(4)), 2))
    counts = Counter(local)
    require(counts == {-1: 64, 0: 128, 1: 64}, "Wrong actual descriptor moment")

    # Evaluate the published polynomial with an illustrative b = 1/512,
    # enclose p exactly and prove the signs of the observed source and TV gap.
    p = (Interval.cast(5).sqrt()-1)/2
    coeff = report_coefficients(p)

    def report(y):
        result = Interval.cast(0)
        # report_coefficients uses the input t=64*y.
        for c in reversed(coeff):
            result = result*(64*y)+c
        return result

    minus, zero, plus = [report(F(f, 512)) for f in (-1, 0, 1)]
    old_average = (minus+2*zero+plus)/4
    new_average = sum((counts[f]*report(F(f, 512)) for f in counts), Interval.cast(0))/256
    local_source = (plus-minus)/4
    require(old_average == new_average, "One shared centre must preserve the uniform nonlinear report")
    require(old_average.hi < zero.lo, "Independent centres should preserve the distinct Jensen gap")
    require(local_source.lo > 0, "A genuine conditional old SITE tangent cannot disappear")
    require(minus.hi < old_average.lo and old_average.hi < zero.lo < plus.lo,
            "Wrong ordered probabilities in the exact TV expression")
    total_variation = local_source + (zero - old_average)/2
    require(total_variation.lo > local_source.hi, "Joint archive separation must be strict")
    return {"sites": len(local), "conditional_uniform_report_preserved": True,
            "nonzero_old_SITE_jet": "(R(b)-R(-b))/4",
            "fresh_centre_old_SITE_jet": 0,
            "TV_joint_old_SITE_record_at_least_local_slope": True,
            "illustration_b": "1/512", "illustrative_old_SITE_jet": float(local_source.lo)}


if __name__ == "__main__":
    print(json.dumps({"status": "PASS", "translation": coordinate_translation(),
                      "literal_direct_comparator": check_address(),
                      "coherent_archive": check_coherent_records(),
                      "nonlinear_source": check_local_nonlinear_derivative(),
                      "physical_complete_Hq_and_Book03_ledger_proved": False,
                      "GR_closed": False}, indent=2))
