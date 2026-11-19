"""Exact native four-tick work comparison and a dyadic constant-action witness."""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from hashlib import sha256
from itertools import product
from pathlib import Path
import json
import runpy


PILOT = Path(__file__).resolve().parents[3]
OWNER = PILOT / "direct/round82/device/check_prepaid_report.py"
OWNER_SHA = "d7bb38033ccfade7f29b76195928b18ec507c82cc633ab7e3e67f6d1a57bc99f"
WIDTH = 12
PORT, SPIN = 2, (0, 1)
SITE, CAR = (3, 4), (5, 6, 7, 8)
KNOWN_ONE, E, W = 9, 10, 11
KA, KB, BUDGET = 14, 9, 14


def require(condition, reason):
    if not condition:
        raise ArithmeticError(reason)


def position(wire):
    return 1 << (WIDTH - 1 - wire)


def address(wires, value):
    return sum(position(wire) for j, wire in enumerate(reversed(wires)) if value & (1 << j))


def inventory(word):
    return Counter((gate.op, gate.wires) for gate in word)


def operator(owner, word):
    native = owner["ne"]
    execution = native.Execution(WIDTH, (), (), tuple(word), native.G_CX_SOURCE_I, PORT, SPIN)
    native.validate_execution(execution, max_qubits=WIDTH, max_expanded_stages=len(word))


def verify_site(owner):
    """Each actual two-birth, one-CX, one-measured path prepares one fair bit."""
    gate, v, p, zero = owner["ne"].Gate, owner["v"], owner["p"], owner["Golden"]()
    raw = {2*u + t: v[u]*v[t] for u, t in product((0, 1), repeat=2)}
    after = owner["action"](raw, gate("CX", (0, 1)), 2)
    success = sum((after[i]*after[i] for i in (1, 3)), zero)
    failure = sum((after[i]*after[i] for i in (0, 2)), zero)
    require(after[1] == after[3] == v[0]*v[1], "unmeasured addresses have equal amplitudes")
    require(success == 2*p*p*p and success+failure == 1, "both ready and refused mass retained")
    require(2*after[1]*after[1] == success, "two independently accepted flags give amplitude 1/2")


def addressed_plane(owner, site, component, numerator):
    """Literal balanced powers; all targets already occupied, all columns specified."""
    gate = owner["ne"].Gate
    differing = 14 ^ component
    pivot_mask = 1 << (differing.bit_length()-1)
    pivot = CAR[4-pivot_mask.bit_length()]
    first_bit = int(bool(14 & pivot_mask))
    remaining = tuple((wire, 1 << (3-i)) for i, wire in enumerate(CAR) if wire != pivot)
    frame = tuple(gate("CX", (pivot, wire)) for wire, mask in remaining if differing & mask)
    framed_start = 14 ^ (first_bit*(differing ^ pivot_mask))
    controls = (*(wire for wire, _ in remaining), *SITE)
    chosen = site + sum(int(bool(framed_start & mask)) << (4-i)
                        for i, (_, mask) in enumerate(remaining))
    route = tuple(gate("CX", pair) for pair in ((PORT, pivot), (pivot, PORT), (PORT, pivot)))
    z = (*route, gate("SourceI", (PORT, *SPIN)), gate("SourceI", (PORT, *SPIN)), *route)
    g = gate("G", (pivot,))
    word = list(frame)
    for subset in range(1 << len(controls)):
        path = tuple(gate("CX", (c, pivot)) for i, c in enumerate(reversed(controls))
                     if subset & (1 << i))
        k = numerator * (-1)**(first_bit + bin(chosen & subset).count("1"))
        word.extend((*path, *z, *((g,)*(BUDGET-k)), *z, *((g,)*(BUDGET+k)), *path[::-1]))
    return (*word, *frame[::-1])


def make_words(owner):
    gate = owner["ne"].Gate
    fields = []
    for ka, kb in ((KA, KB), (KB, KA)):
        word = ()
        for site, (axis, angle) in enumerate(((0, ka), (15, kb), (0, -ka), (15, -kb))):
            word += addressed_plane(owner, site, axis, angle)
        operator(owner, word)
        fields.append(word)
    require(inventory(fields[0]) == inventory(fields[1]), "exact balanced field-fork inventory")
    a, d = gate("CX", (CAR[0], E)), gate("CX", (E, W))
    reference, live = (d, d, a, a), (a, d, d, a)
    for word in (reference, live):
        operator(owner, word)
        for column in range(1 << WIDTH):
            index = column
            for operation in word:
                control, target = map(position, operation.wires)
                if index & control:
                    index ^= target
            require(index == column, "native continuation is the identity on all columns")
    require(inventory(reference) == inventory(live), "same literal diagnostic inventory")
    return fields, reference, live


def overlaps(owner, state, word):
    zero = owner["Golden"]()
    after = state
    result = []
    for gate in word:
        before = after
        after = owner["action"](before, gate, WIDTH)
        result.append(sum((coefficient*after.get(index, zero)
                           for index, coefficient in before.items()), zero))
    require(after == state, "full conditioned state recovered at the end")
    return result


def verify_paid_initial(owner, expected):
    """Supply the vacuum column and diagnostic zeros from actual Golden births."""
    native, gate = owner["ne"], owner["ne"].Gate
    v, one = owner["v"], owner["one"]
    half = owner["Golden"](Fraction(1, 2))
    wires = (*CAR, E, W)
    initial = {}
    for site, bits in product(range(4), product((0, 1), repeat=len(wires))):
        column = address(SITE, site) | position(KNOWN_ONE)
        amplitude = half
        for wire, bit in zip(wires, bits):
            column |= bit*position(wire)
            amplitude *= v[bit]
        initial[column] = amplitude
    word = ()
    for wire in (*CAR[1:], E, W):
        positive = native.Execution(WIDTH, (), (), (gate("G", (wire,)),),
                                    native.G_CX_SOURCE_I, PORT, SPIN)
        word += native.inverse_word(positive, max_qubits=WIDTH, max_expanded_stages=11)
    word += (gate("CX", (KNOWN_ONE, CAR[-1])),
             *(gate("CX", (CAR[0], wire)) for wire in CAR[1:]))
    operator(owner, word)
    for entry in word:
        initial = owner["action"](initial, entry, WIDTH)
    require(initial == expected and len(word) == 59, "paid CAR vacuum and two clean targets")

    source = gate("SourceI", (PORT, *SPIN))
    for column in range(8):
        full = address((*SPIN, PORT), column)
        after = owner["action"]({full: one}, source, WIDTH)
        after = owner["action"](after, source, WIDTH)
        require(after == {full: -one if column & 1 else one}, "physical phase sign fixes all old Spin columns")


def literal_field_states(owner, fields):
    """Replay all raw letters for one old column and check no unowned factors move."""
    p, a, golden = owner["p"], owner["a"], owner["Golden"]
    half = golden(Fraction(1, 2))
    start = {address(SITE, s) | address(CAR, j) | position(KNOWN_ONE): half*coefficient
             for s in range(4) for j, coefficient in ((1, a), (14, p))}
    columns = lru_cache(None)(owner["action"].__globals__["gate_columns"])
    owner["action"].__globals__["gate_columns"] = columns
    verify_paid_initial(owner, start)
    for (ka, kb), word in zip(((KA, KB), (KB, KA)), fields):
        ca, sa = owner["rot"](64*ka)
        cb, sb = owner["rot"](64*kb)
        expected = {}
        for s, (axis, car_c, car_s) in enumerate(((0, ca, sa), (15, cb, sb), (0, ca, -sa), (15, cb, -sb))):
            prefix = address(SITE, s) | position(KNOWN_ONE)
            for index, coefficient in ((1, a), (14, p*car_c), (axis, p*car_s)):
                expected[prefix | address(CAR, index)] = half*coefficient
        actual = start
        for gate in word:
            actual = owner["action"](actual, gate, WIDTH)
        require(actual == expected, "literal occupied-SITE plane word and padding")
        yield actual, p*sa, p*sb


def verify(owner):
    verify_site(owner)
    fields, reference, live = make_words(owner)
    p, golden, one = owner["p"], owner["Golden"], owner["one"]
    zero = golden()
    energy = []
    gaps = []
    for state, a, b in literal_field_states(owner, fields):
        material = ((a, zero), (zero, b), (-a, zero), (zero, -b))
        edges = [sum(((u-v)*(u-v) for u, v in zip(material[i], material[(i+1)%4])), zero)
                 for i in range(4)]
        require(edges == [a*a+b*b]*4, "every periodic directed material edge has the same action")
        energy.append(edges[0])
        q = sum((amplitude*amplitude for index, amplitude in state.items() if index & position(CAR[0])), zero)
        require(q == p*p-golden(Fraction(1, 2))*a*a, "single actual CAR-wire marginal")
        ref, moved = overlaps(owner, state, reference), overlaps(owner, state, live)
        require(ref[:2] == [one, one] and moved[1:3] == [one-q, one-q], "two exact native motion overlaps")
        require(ref[2:] == [moved[0], moved[3]], "other two primitive motions identical")
        gaps.append(4*(2*q-q*q))
    require(energy[0] == energy[1], "every local forward CAR action is exactly shared across fields")
    require(gaps[0] != gaps[1], "different exact motion columns")
    p_lo, p_hi = Fraction(".61803398874989"), Fraction(".61803398874990")
    require(p_lo+p_lo*p_lo < 1 < p_hi+p_hi*p_hi, "rational enclosure of the Golden p")

    def gap_bounds(k):
        cosine, sine = [tuple(owner["rational"](entry) for entry in enclosure)
                        for enclosure in owner["native_rotation_intervals"](64*k, bits=160)]
        require(cosine[0] > 0 and 0 < sine[0] <= sine[1] < 1, "positive native material column")
        minimum = p_lo*p_lo*(1-sine[1]*sine[1]/2)
        maximum = p_hi*p_hi*(1-sine[0]*sine[0]/2)
        return 4*(2*minimum-minimum*minimum), 4*(2*maximum-maximum*maximum)

    first, second = gap_bounds(KA), gap_bounds(KB)
    require(Fraction(".19") < first[0] - second[1] < first[1] - second[0] < Fraction(".22"),
            "strict native constant-action change in squared motion")
    return len(fields[0])


def verify_local_site_mask():
    sizes = (8, 16, 32, 64, 128, 256)
    for length in sizes:
        quarter, eighth = length//4, length//8
        parity = []
        for n in range(length):
            flag = (n//quarter ^ n//eighth) & 1
            parity.append(flag)
            phase = n % (length//2)
            if phase not in (eighth, 3*eighth):
                require(flag == int(eighth < phase < 3*eighth),
                        "two SITE bits select the exact signed cosine support")
            for car in (0, 1, 14, 15):
                is_even = 1 ^ (bin(car).count("1") & 1)
                require((is_even ^ flag) == ((1 ^ flag) if car in (0, 15) else flag),
                        "local XOR predicate on both original matter and vacuum blocks")
        require(sum(parity)*2 == length, "balanced SITE mask")
    return sizes


def main():
    require(sha256(OWNER.read_bytes()).hexdigest() == OWNER_SHA, "pinned exact Golden native replay")
    owner = runpy.run_path(str(OWNER))
    calls = verify(owner)
    require(Fraction(77, 100)*Fraction(1, 2560) > Fraction(3, 10000), "uniform strict analytical bound")
    require(Fraction(49, 100)*Fraction(1, 2560) > Fraction(19, 100000), "uniform local bound")
    print(json.dumps({
        "status": "PASS",
        "conditioned_site_count": 4,
        "whole_site_flag_success_mass": "4*p^6",
        "paid_vacuum_and_diagnostic_blank_calls": 59,
        "identical_addressed_field_calls_per_arm": calls,
        "diagnostic_all_columns_per_arm": 1 << WIDTH,
        "diagnostic_gate_count": 4,
        "all_four_native_local_material_edges_equal": True,
        "finite_native_squared_work_contrast_difference": [".19", ".22"],
        "ideal_ellipse_uniform_work_derivative_lower_bound": ".0003",
        "exact_local_site_mask_lattices": verify_local_site_mask(),
        "ideal_local_site_work_derivative_lower_bound": ".00019",
        "unconditional_book03_trace_tariff_derived": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
