"""Exact deterministic T copy on the fixed controller, and absolute-sector bounds."""
from collections import Counter, defaultdict
from fractions import Fraction
from importlib.util import module_from_spec, spec_from_file_location
from itertools import product
import json
from pathlib import Path

import sympy as sp


def require(condition, label):
    if not condition:
        raise AssertionError(label)


def previous_controller():
    directory = Path(__file__).resolve().parents[2] / "round171" / "controller"
    path = directory / "check_fixed_retained_controller.py"
    spec = spec_from_file_location("fixed_controller", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, module.owner()


def copying_word(arithmetic, base):
    native = arithmetic.ne
    gate = native.Gate
    block = (gate("CX", (0, 9)), gate("G", (9,)), gate("CX", (0, 9)))
    gates = base + block
    execution = native.Execution(10, (), (), gates, native.G_CX, report_bits=(1, 3, 5, 7, 0))
    native.execution_from_json(native.canonical_json(execution), max_qubits=10, max_expanded_stages=19)
    require(Counter(stage.op for stage in gates) == {"CX": 14, "G": 5}, "19 literal native gates")
    return block, gates


def exact_columns_and_marks(arithmetic, base, block, gates):
    a, p, G, one, v = arithmetic.a, arithmetic.p, arithmetic.Golden, arithmetic.one, arithmetic.v

    def run(state, word, width):
        for letter in word:
            state = arithmetic.action(state, letter, width)
        return state

    matrices = (((a, -p), (p, a)), ((a, p), (-p, a)))
    for column in range(1024):
        t = column >> 9
        initial_nine, new_raw = column >> 1, column & 1
        old_end = run({initial_nine: one}, base, 9)
        expected = {2 * row + tail: amplitude * matrices[t][tail][new_raw]
                    for row, amplitude in old_end.items() for tail in (0, 1)}
        exact = run({column: one}, gates, 10)
        require(exact == expected, "full fixed word at all raw columns")

    retained = []
    for t in (0, 1):
        joint_input = {}
        bare_input = {}
        for old_work in product((0, 1), repeat=8):
            index = t
            amplitude = one
            for bit in old_work:
                index = 2 * index + bit
                amplitude *= v[bit]
            bare_input[index] = amplitude
            for tail in (0, 1):
                joint_input[2 * index + tail] = amplitude * v[tail]
        bare_end = run(bare_input, base, 9)
        end = run(joint_input, gates, 10)
        copy_tail = (arithmetic.p3, 2 * a * p) if t == 0 else (one, G())
        require(end == {2 * row + b: alpha * amplitude for row, alpha in bare_end.items()
                        for b, amplitude in enumerate(copy_tail) if amplitude != 0}, "pure conditional new tail")

        def old_marks(row):
            return tuple((row >> (8 - wire)) & 1 for wire in (1, 3, 5, 7))

        old_mass = defaultdict(G)
        actual_mass = defaultdict(G)
        for row, amplitude in bare_end.items():
            old_mass[old_marks(row)] += amplitude * amplitude
        for row, amplitude in end.items():
            old = row >> 1
            head, tail = row >> 9, row & 1
            require(head == t and not (head and tail), "deterministic LC1 copy; no dark 11")
            # LC1 outcome 0 does not disclose the tail. Outcome 1 is 10.
            actual_mass[(old_marks(old), head)] += amplitude * amplitude
        require(actual_mass == {(w, t): value for w, value in old_mass.items()}, "no new probability or Info")
        require(len(old_mass) == 16 and all(value != 0 for value in old_mass.values()), "all old outcomes retained")
        powers = [one]
        for _ in range(8):
            powers.append(powers[-1] * p)
        require(all(any(value == power for power in powers[4:]) for value in old_mass.values()) and
                all(any(value == power for value in old_mass.values()) for power in (powers[4], powers[-1])),
                "unchanged conditional event information ranges from 4 to 8")
        retained.append(len(actual_mass))

        old = t << 9
        state = {old: a, old + 1: p}
        aggregate_motion = arithmetic.interval(0)
        for gate in block:
            moved = arithmetic.action(state, gate, 10)
            overlap = sum((amp * moved.get(row, G()) for row, amp in state.items()), G())
            aggregate_motion = arithmetic.plus(aggregate_motion, arithmetic.trace_distance(overlap))
            state = moved
        expected_work = arithmetic.enclosure(p if t == 0 else p + one + arithmetic.p3)
        require(max(aggregate_motion[0], expected_work[0]) <= min(aggregate_motion[1], expected_work[1]),
                "same actual deterministic copy motion as A82")
    return retained


def confirmation_contrasts(arithmetic):
    r, p = arithmetic.enclosure(arithmetic.p * arithmetic.p), arithmetic.enclosure(arithmetic.p)

    def coherent(q):
        return arithmetic.plus(arithmetic.sqrtiv(q), arithmetic.sqrtiv(arithmetic.times(3, arithmetic.minus(1, q))))

    registered = arithmetic.minus(p, r)
    full = arithmetic.minus(coherent(r), coherent(p))
    state_jump = arithmetic.minus(arithmetic.sqrtiv(arithmetic.minus(1, r)),
                                  arithmetic.sqrtiv(arithmetic.minus(1, p)))
    for bound in (registered, full, state_jump):
        require(bound[0] > 0, "rare outcome is more costly in the declared confirmation")
    return [float(sum(bound) / 2) for bound in (registered, full, state_jump)]


def exact_sector_proofs():
    p_symbols = (sp.sqrt(5) - 1) / 2
    field = sp.QQ.algebraic_field(p_symbols)
    p = field.convert(p_symbols)
    one = field.one
    low_p, high_p = Fraction("0.6180339887498948482"), Fraction("0.6180339887498948483")
    require(low_p + low_p**2 < 1 < high_p + high_p**2, "rational golden enclosure")

    def positive(value):
        lo, hi = Fraction(0), Fraction(0)
        for coefficient in value.to_list():
            term = Fraction(int(coefficient.numerator), int(coefficient.denominator))
            endpoints = [x * y + term for x, y in product((lo, hi), (low_p, high_p))]
            lo, hi = min(endpoints), max(endpoints)
        return lo > 0

    bounds, endpoints, reversed_maximum = {}, {}, {}
    for nu in (1, 2):
        w = p**nu
        limit = (one + w * w)**2 / (4 * w)
        require(limit == (5 * p if nu == 1 else 9 * p * p) / 4, "exact uniform sector bound")
        require(positive(one - limit), "uniform bound is strictly below one")
        bounds[str(nu)] = float(field.to_sympy(limit).evalf(25))
        zero_meter = []
        for drop in (0, 1):
            z = w**drop
            a0, a1 = one + z, z / w + w
            old_0, old_1 = a0 + z * a1, a1 + z * a0
            require(old_0 == old_1, "endpoint literal XOR ties before copy")
            require(w * (old_1 / old_0)**2 == w, "deterministic literal copy separates sectors")
            zero_meter.append(float(field.to_sympy(w)))
        endpoints[str(nu)] = zero_meter

        # Pure event Info. Pay the rare D=1 two extra units and give
        # the report read no corresponding confirmation charge.
        d_weight = w**2
        a0_max, a1_max = one, one / w
        require(positive(a0_max - d_weight * a1_max) and
                positive(a1_max - d_weight * a0_max), "maximum leaves selected under declared D meter")
        max_ratio = w * (a1_max / a0_max)**2
        require(max_ratio == one / w and positive(max_ratio - one), "minimum reverses under separate meters")
        reversed_maximum[str(nu)] = float(field.to_sympy(max_ratio))
        shared_weight_squared, a1_max_squared = w, one / w
        require(shared_weight_squared * a1_max_squared == one and
                w * a1_max_squared == one, "exact minimum tie under a common meter")

    # Deliberately outside A82: charge six for common D=0 and six for
    # a rare R branch. These are positive but invert the D confirmation order.
    w = p
    rare = w**6
    inverted_d = one / rare
    a0, a1 = one + rare, rare / w + w
    reversed_ratio = w * ((a1 + inverted_d * a0) / (a0 + inverted_d * a1))**2
    require(positive(reversed_ratio - field.convert(sp.Rational(5, 4))),
            "counterexample beyond outcome monotonicity")
    return bounds, endpoints, reversed_maximum, float(field.to_sympy(reversed_ratio).evalf(25))


def main():
    controller, arithmetic = previous_controller()
    base = controller.fixed_word(arithmetic.ne)
    block, gates = copying_word(arithmetic, base)
    retained = exact_columns_and_marks(arithmetic, base, block, gates)
    meters = confirmation_contrasts(arithmetic)
    bounds, endpoints, reversed_maximum, counterexample = exact_sector_proofs()
    print(json.dumps({
        "status": "PASS",
        "B171_commit": "c3e3eb04e",
        "fixed_word": {"CX": 14, "G": 5, "fresh_golden_births": 9, "physical_LC1_readings": 5},
        "exact_raw_columns": 1024,
        "positive_conditional_marks_each_old_T": retained,
        "deterministic_copy_literal_lengths": [1, 2],
        "extra_conditional_event_drop_and_CQ_information": [0, 0, 0],
        "rare_minus_common_confirmation_registered_coherent_jump": meters,
        "upper_sector_ratios_nu_1_2": bounds,
        "zero_rate_ratios_event_and_drop": endpoints,
        "maximum_leaf_weight_ratio_with_D_only_registered_meter": reversed_maximum,
        "maximum_leaf_weight_ratio_at_common_meter_tie": 1,
        "arbitrary_inverted_D_price_ratio_counterexample": counterexample,
        "absolute_old_input_mass_assumed_as_separate_condition": True,
        "full_physical_Cost_minus_Info_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
