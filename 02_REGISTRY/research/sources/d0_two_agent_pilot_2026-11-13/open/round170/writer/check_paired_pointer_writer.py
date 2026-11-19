"""Exact A82 second-pointer terminal writer and the last-read rectangle."""
from collections import Counter
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def import_a82():
    pilot = Path(__file__).resolve().parents[3]
    path = pilot / "direct" / "round82" / "device" / "check_prepaid_report.py"
    spec = spec_from_file_location("a82_terminal_writer_inputs", path)
    owner = module_from_spec(spec)
    spec.loader.exec_module(owner)
    return owner


def run_word(owner, state, word, width):
    for gate in word:
        state = owner.action(state, gate, width)
    return state


def check_w3(owner):
    gate = owner.ne.Gate
    width = 10
    new = (7, 8, 9)
    port, spin = 2, (0, 1)

    def clear(wire):
        instruction = (gate("G", (wire,)),)
        context = owner.ne.Execution(width, (), (), instruction, owner.ne.G_CX_SOURCE_I, port, spin)
        result = owner.ne.inverse_word(context, max_qubits=width, max_expanded_stages=11)
        require(len(result) == 11, "actual routed positive inverse")
        return result

    preparations = tuple(clear(wire) for wire in new)
    prep = tuple(letter for word in preparations for letter in word)
    copies = (gate("CX", (owner.PTR_Q, new[0])), gate("CX", (owner.PTR_Q, new[2])))
    inventory = Counter(letter.op for letter in prep + copies)
    require(inventory == {"CX": 20, "SourceI": 12, "G": 3}, "fixed 35-gate inventory")

    for wire, word in zip(new, preparations):
        require(all(set(letter.wires) <= {*spin, port, wire} for letter in word), "actual preparation support")
        target_mask = 1 << (width - 1 - wire)
        for source_spin, old_port, old_target in product(range(4), range(2), range(2)):
            even = (source_spin << 8) + (old_port << 7)
            start = even + old_target * target_mask
            coeffs = (owner.a, -owner.p) if old_target == 0 else (owner.p, owner.a)
            expected = {even: coeffs[0], even + target_mask: coeffs[1]}
            require(run_word(owner, {start: owner.one}, word, width) == expected,
                    "complete routed inverse on all active and uninitialized columns")

    # Replay the native writer on every raw column, even when the container
    # has not been initialized. The middle cell never receives a gate here.
    for column in range(1 << width):
        old = column >> 3
        target_flip = 5 if old & 1 else 0
        result = run_word(owner, {column: owner.one}, copies, width)
        require(result == {column ^ target_flip: owner.one}, "all raw reversible writer columns")

    # Clear actual Golden births (not supplied zeros), on every old Spin,
    # PORT, Y, U and pair-of-pointers column.
    for old in range(1 << 7):
        input_state = {8 * old + 4 * a + 2 * b + c: owner.v[a] * owner.v[b] * owner.v[c]
                       for a, b, c in product(range(2), repeat=3)}
        prepared = run_word(owner, input_state, prep, width)
        require(prepared == {8 * old: owner.one}, "physical blank preparation preserves old column")
        result = run_word(owner, prepared, copies, width)
        require(result == {8 * old + (5 if old & 1 else 0): owner.one}, "actual 000/101 copy")

    # Independently verify the two observed movement steps in each known
    # control sector. Spectators factor out of every overlap.
    for bit in (0, 1):
        old = bit
        state = {8 * old: owner.one}
        for letter in copies:
            next_state = owner.action(state, letter, width)
            overlap = sum((value * next_state.get(key, owner.Golden()) for key, value in state.items()),
                          owner.Golden())
            require(overlap == (owner.Golden() if bit else owner.one), "literal W3 motion")
            state = next_state
    return dict(inventory)


def check_nc1(owner):
    gate = owner.ne.Gate
    repetitions = (gate("CX", (owner.PTR_Q, 7)), gate("G", (7,)), gate("CX", (owner.PTR_Q, 7)))
    expected = ((owner.p3, 2 * owner.a * owner.p), (owner.one, owner.Golden()))
    for old in range(1 << 7):
        state = {2 * old: owner.a, 2 * old + 1: owner.p}
        actual = run_word(owner, state, repetitions, 8)
        desired = {2 * old + t: amplitude for t, amplitude in enumerate(expected[old & 1]) if amplitude != 0}
        require(actual == desired, "all old columns of live NC1")
    movement = (owner.p, owner.p + owner.one + owner.p3)
    for bit in (0, 1):
        state = {2 * bit: owner.a, 2 * bit + 1: owner.p}
        calculated = owner.interval(0)
        for letter in repetitions:
            next_state = owner.action(state, letter, 8)
            overlap = sum((value * next_state.get(key, owner.Golden()) for key, value in state.items()),
                          owner.Golden())
            calculated = owner.plus(calculated, owner.trace_distance(overlap))
            state = next_state
        interval = owner.enclosure(movement[bit])
        require(max(calculated[0], interval[0]) <= min(calculated[1], interval[1]), "live NC1 work replay")
        passive = sum((owner.v[t] * amplitude for t, amplitude in enumerate(expected[bit])), owner.Golden())
        require(passive * passive == owner.p, "unchanged passive square for each branch")


def last_read_rectangle(owner):
    # The A82 native 90-stage detector, before the new post-read writer,
    # gives precisely 00 and (01 or 10) on each already known old U.
    gates = owner.word(1)
    cosine, sine = owner.rot(4)
    require(len(gates) == 90, "actual last A82 read")
    for bit, spin, port in product((0, 1), range(4), (0, 1)):
        old = ((2 * spin + port) * 2 + 1) * 2 + bit  # Y=1, U=bit.
        born = {4 * old + 2 * a + b: owner.v[a] * owner.v[b] for a, b in product((0, 1), repeat=2)}
        read = run_word(owner, born, gates, 7)
        require(read == {4 * old: cosine, 4 * old + 1 + bit: sine}, "known U on original last read")

    pairs = ((0, 0), (0, 1), (1, 0))
    lengths = {f"{a}{b}": [3 + 2 * a + b, 1 + b, 4 + 2 * (a + b)] for a, b in pairs}
    require(lengths["10"][0] - lengths["01"][0] == 1, "original last rectangle")
    require(lengths["10"][1] - lengths["01"][1] == -1, "one literal countercharge")
    require(lengths["10"][2] == lengths["01"][2], "paired last success lengths")
    return lengths, sine * sine


def mean_source(owner, eta):
    add, sub, mul = owner.plus, owner.minus, owner.times
    r = owner.enclosure(owner.p * owner.p)
    eta = owner.enclosure(eta)
    h = add(1, r)
    failure = sub(1, eta)
    survival = owner.interval(1)
    floors = {}
    for index in range(1, 19):
        survival = mul(survival, failure)
        gain = sub(mul(index - 1, mul(eta, r)), mul(sub(1, survival), h))
        if index == 17:
            require(gain[1] < 0, "paired writer loses the 17-read literal certificate")
        if index == 18:
            require(gain[0] > Fraction("0.004"), "18 reads is already positive")
        if index in (17, 18):
            floors[str(index)] = [float(x) for x in gain]
    require(sub(r, mul(survival, h))[0] > 0, "all later increments positive")
    nc1_motion = mul(mul(eta, r), add(1, owner.enclosure(owner.p3)))
    w3_motion = mul(2, mul(eta, r))
    require(nc1_motion[1] < Fraction("0.10") and w3_motion[1] < Fraction("0.161"),
            "both new terminal contrasts fit inside the proved first motion margin")
    return floors


def main():
    owner = import_a82()
    inventory = check_w3(owner)
    check_nc1(owner)
    lengths, eta = last_read_rectangle(owner)
    floors = mean_source(owner, eta)
    print(json.dumps({
        "status": "PASS",
        "A82_commit": "75d4da9ef",
        "actual_last_detector_square_commands": 90,
        "old_live_second_pointer_wire": 6,
        "additional_W3_clearing_and_copy_inventory": inventory,
        "additional_W3_births": 3,
        "exact_routed_inverse_compact_columns": 48,
        "additional_W3_raw_columns": 1024,
        "old_columns_with_actually_prepared_W3": 128,
        "old_columns_with_live_NC1": 128,
        "lengths_original_extra_total": lengths,
        "last_literal_rectangle_before_after": [1, 0],
        "last_W3_movement_rectangle_before_after": [2, 0],
        "last_live_NC1_movement_rectangle_before_after": ["1+p^3", 0],
        "paired_literal_slope_intervals": floors,
        "latent_conditional_entropy_added": 0,
        "full_physical_Cost_minus_Info_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
