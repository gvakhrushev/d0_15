"""Exact native finite CAR fork and vacuum motion on a coherent SITE."""
from collections import Counter
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from pathlib import Path
import json
import runpy


SOURCES = Path("02_REGISTRY/research/sources")
PILOT = SOURCES / "d0_two_agent_pilot_2026-11-13"
PINS = {
    PILOT / "direct/round82/device/check_prepaid_report.py": "d7bb38033ccfade7f29b76195928b18ec507c82cc633ab7e3e67f6d1a57bc99f",
    SOURCES / "d0_native_readiness_amplification_2026-10-24/native_phase.py": "c9b764111a88d440cb76d6215de1f687713ae6c1a336768ce2bd37898fcfc98d",
    SOURCES / "d0_native_execution_domain_2026-10-24/native_execution.py": "222eafaffa4b30f175919a32c940534b82f3a2b9af89c7897d318dd004a2007c",
    Path("01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md"): "dfa47d91c4994fa8eea64cda67115590056d8aaf48605daf61a1750aaaf0646d",
}
WIDTH = 11
SITE = 3
CAR = (4, 5, 6, 7)
KNOWN_ONE, PARITY, WORK = 8, 9, 10
PHASE_INDEX = 28


def require(condition, label):
    if not condition:
        raise ArithmeticError(label)


def bit_position(wire):
    return 1 << (WIDTH - wire - 1)


def inventory(word):
    return Counter((gate.op, gate.wires) for gate in word)


def apply_word(owner, state, word):
    for gate in word:
        state = owner["action"](state, gate, WIDTH)
    return state


def incoming_basis(owner, old):
    fresh = (SITE, *CAR, PARITY, WORK)
    v, one = owner["v"], owner["one"]
    initial = (old << (WIDTH - 3)) | bit_position(KNOWN_ONE)
    state = {}
    for bits in product((0, 1), repeat=len(fresh)):
        column = initial
        amplitude = one
        for wire, bit in zip(fresh, bits):
            column |= bit*bit_position(wire)
            amplitude *= v[bit]
        state[column] = amplitude
    return state


def native_programs(owner):
    native = owner["ne"]
    gate = native.Gate
    def cx(control, target):
        return gate("CX", (control, target))

    def make_zero(wire):
        forward = native.Execution(WIDTH, (), (), (gate("G", (wire,)),), native.G_CX_SOURCE_I, 2, (0, 1))
        result = native.inverse_word(forward, max_qubits=WIDTH, max_expanded_stages=11)
        require(len(result) == 11, "actual source-port inverse")
        return result

    prep = tuple(entry for wire in (*CAR[1:], PARITY, WORK) for entry in make_zero(wire))
    prep += (cx(KNOWN_ONE, CAR[-1]), *(cx(CAR[0], wire) for wire in CAR[1:]))
    frame = (cx(CAR[0], CAR[1]), cx(CAR[0], CAR[2]))
    controls = (*CAR[1:], SITE)
    plane_calls = []
    for size in range(5):
        for subset in combinations(controls, size):
            path = tuple(cx(wire, CAR[0]) for wire in subset)
            plane_calls.extend((*path, *((gate("G", (CAR[0],)),)*PHASE_INDEX), *path[::-1]))
    plane = tuple(plane_calls)
    compiled = native.Execution(WIDTH, (), (), plane, native.G_CX_SOURCE_I, 2, (0, 1))
    native.validate_execution(compiled, max_qubits=WIDTH, max_expanded_stages=512)
    require(len(plane) == 512, "four-control literal field word")
    route = (cx(2, CAR[0]), cx(CAR[0], 2), cx(2, CAR[0]))
    z = (*route, owner["ne"].Gate("SourceI", (2, 0, 1)), owner["ne"].Gate("SourceI", (2, 0, 1)), *route)
    fields = {1: (*frame, *z, *plane, *plane, *z, *frame[::-1]),
              -1: (*frame, *z, *z, *plane, *plane, *frame[::-1]),
              0: (*frame, *plane, *z, *plane, *z, *frame[::-1])}
    require(inventory(fields[0]) == inventory(fields[1]) == inventory(fields[-1]), "same field fork inventory")
    parity = tuple(cx(wire, PARITY) for wire in (*CAR, KNOWN_ONE))
    diagnostic = (cx(PARITY, WORK),)*2
    baseline = (*diagnostic, *parity, *parity[::-1])
    live = (*parity, *diagnostic, *parity[::-1])
    require(inventory(baseline) == inventory(live), "same old-field diagnostic inventory")
    for column in range(1 << WIDTH):
        for word in (baseline, live):
            shifted = column
            for entry in word:
                control, target = entry.wires
                if shifted & bit_position(control):
                    shifted ^= bit_position(target)
            require(shifted == column, "full-column identity for both source-order variants")
    return prep, fields, baseline, live


def expected_field(owner, old, sign, cosine, sine):
    a, p, v = owner["a"], owner["p"], owner["v"]
    prefix = (old << (WIDTH - 3)) | bit_position(KNOWN_ONE)
    result = {}
    for site, weight in enumerate(v):
        for car, coefficient in ((1, a), (14, p if site or sign == 0 else p*cosine)):
            result[prefix | (site*bit_position(SITE)) | (car << (WIDTH - CAR[-1] - 1))] = weight*coefficient
        if not site and sign:
            result[prefix] = weight*p*sine*sign
    return result


def trace_overlaps(owner, starts, word):
    after = starts
    overlaps = []
    zero = owner["Golden"]()
    for gate in word:
        before = after
        after = owner["action"](before, gate, WIDTH)
        overlaps.append(sum((value*after.get(index, zero) for index, value in before.items()), zero))
    require(after == starts, "all old and new terminal factors restored")
    return overlaps


def verify_angle(sine_interval):
    lo, hi = sine_interval
    angle_lo, angle_hi = Fraction("0.0479273"), Fraction("0.0479274")
    sin_at_lo_upper = angle_lo - angle_lo**3/6 + angle_lo**5/120
    sin_at_hi_lower = angle_hi - angle_hi**3/6
    require(sin_at_lo_upper < lo <= hi < sin_at_hi_lower, "rational enclosure of the actual two-sided angle")


def main():
    for path, expected in PINS.items():
        require(sha256(path.read_bytes()).hexdigest() == expected, f"pinned input {path}")
    owner = runpy.run_path(str(PILOT / "direct/round82/device/check_prepaid_report.py"))
    cosine, sine = owner["rot"](32*PHASE_INDEX)
    cosine_interval, sine_interval = [tuple(owner["rational"](entry) for entry in bounds)
                                      for bounds in owner["native_rotation_intervals"](32*PHASE_INDEX, bits=160)]
    require(cosine_interval[0] > 0, "positive material filler")
    verify_angle(sine_interval)
    p = owner["p"]
    one = owner["one"]
    prep, fields, baseline, live = native_programs(owner)
    mass = p*(p*sine)*(p*sine)
    for old in range(8):
        start = apply_word(owner, incoming_basis(owner, old), prep)
        for sign in (-1, 0, 1):
            after = apply_word(owner, start, fields[sign])
            require(after == expected_field(owner, old, sign, cosine, sine), "literal native material fork, all old columns")
            ref_overlaps = trace_overlaps(owner, after, baseline)
            live_overlaps = trace_overlaps(owner, after, live)
            q = mass if sign else owner["Golden"]()
            require(ref_overlaps[:2] == [one, one], "uncomputed parity target is stationary")
            require(live_overlaps[5:7] == [one-q, one-q], "two paid field-sensitive CX overlaps")
            require(ref_overlaps[2:] == live_overlaps[:5] + live_overlaps[7:], "all other motions coincide exactly")
    p_low, p_high = Fraction("0.61803398874989"), Fraction("0.61803398874990")
    require(p_low+p_low**2 < 1 < p_high+p_high**2, "exact p enclosure")
    mass_lo = p_low**3 * sine_interval[0]**2
    mass_hi = p_high**3 * sine_interval[1]**2
    lo, hi = 4*(2*mass_lo-mass_lo**2), 4*(2*mass_hi-mass_hi**2)
    require(Fraction("0.004") < lo <= hi < Fraction("0.005"), "positive finite squared trace-motion contrast")
    print(json.dumps({
        "status": "PASS",
        "old_spin_port_columns_per_field_arm": 8,
        "physical_diagnostic_all_columns": 1 << WIDTH,
        "field_arms": ["minus", "vacuum", "plus"],
        "addressed_field_calls_per_arm": len(fields[0]),
        "addressed_diagnostic_calls_per_arm": len(baseline),
        "phase_index": PHASE_INDEX,
        "centered_angle_interval": ["0.0479273", "0.0479274"],
        "finite_motion_gap_squared_interval": ["0.004", "0.005"],
        "GR_closed": False,
        "source_sha256": {str(path): value for path, value in PINS.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
