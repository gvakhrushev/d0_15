"""Static native controller on retained T and finite-field obstruction to the old mux."""
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


def owner():
    pilot = Path(__file__).resolve().parents[3]
    path = pilot / "direct" / "round82" / "device" / "check_prepaid_report.py"
    spec = spec_from_file_location("native_work", path)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixed_word(native):
    gate = native.Gate
    controls, reports = ((1, 2), (5, 6)), ((3, 4), (7, 8))

    def nc1(head, tail):
        return (gate("CX", (head, tail)), gate("G", (tail,)), gate("CX", (head, tail)))

    gates = ()
    for (d, d_tail), (r, r_tail) in zip(controls, reports):
        gates += nc1(d, d_tail) + (gate("CX", (0, r)), gate("CX", (d, r))) + nc1(r, r_tail)
    execution = native.Execution(9, (), (), gates, native.G_CX, None, None,
                                 report_bits=(1, 3, 5, 7))
    native.execution_from_json(native.canonical_json(execution), max_qubits=9, max_expanded_stages=16)
    require(Counter(letter.op for letter in gates) == {"CX": 12, "G": 4}, "fixed native inventory")
    return gates


def check_columns_and_born(module, gates):
    a, p, v = module.a, module.p, module.v
    zero, one = module.Golden(), module.one
    G = ((a, -p), (p, a))
    Gi = ((a, p), (-p, a))

    def run(state):
        for letter in gates:
            state = module.action(state, letter, 9)
        return state

    def index(bits):
        total = 0
        for bit in bits:
            total = 2 * total + bit
        return total

    for raw in product(range(2), repeat=9):
        terminal = list(raw)
        terminal[3] ^= raw[0] ^ raw[1]
        terminal[7] ^= raw[0] ^ raw[5]
        expected = {}
        for bits in product(range(2), repeat=4):
            amplitude = one
            for tail, digit in zip((2, 4, 6, 8), bits):
                block = Gi if terminal[tail - 1] else G
                amplitude *= block[digit][raw[tail]]
                terminal[tail] = digit
            if amplitude != zero:
                expected[index(terminal)] = amplitude
        require(run({index(raw): one}) == expected, "exact static word on all raw columns")

    r, s = p * p, p * p * p
    source_prices = []
    for t in (0, 1):
        initial = {}
        for rest in product(range(2), repeat=8):
            amplitude = one
            for bit in rest:
                amplitude *= v[bit]
            initial[index((t,) + rest)] = amplitude
        final = run(initial)
        mass = defaultdict(module.Golden)
        for row, amplitude in final.items():
            bits = tuple((row >> (8 - wire)) & 1 for wire in range(9))
            require(bits[0] == t, "retained T")
            for head in (1, 3, 5, 7):
                require(not (bits[head] and bits[head + 1]), "NC1 dark 11 on canonical tail")
            mass[tuple(bits[j] for j in (1, 3, 5, 7))] += amplitude * amplitude

        for d1, r1, d2, r2 in product(range(2), repeat=4):
            q1, q2 = r + s * (t ^ d1), r + s * (t ^ d2)
            expected = ((r if d1 else p) * (q1 if r1 else one - q1) *
                        (r if d2 else p) * (q2 if r2 else one - q2))
            require(mass[d1, r1, d2, r2] == expected and expected != zero, "all 16 retained marks")
        total = sum((weight for weight in mass.values()), zero)
        require(total == one, "Born full mass")
        expected_length = sum((weight * (4 + sum(heads)) for heads, weight in mass.items()), zero)
        # All four marginal/conditional NC1 entropies equal 1+r in Golden units.
        price = expected_length - 4 * (one + r)
        require(price == 2 * s * (r + s * t), "exact registered fixed-controller source")
        source_prices.append(price)
    require(source_prices[1] - source_prices[0] == 2 * s * s, "same source as #334")
    return len(mass)


def certify_motion(module):
    p, a, zero, one = module.p, module.a, module.Golden(), module.one
    r, s = p * p, p * p * p
    overlap_toggle = 2 * a * p
    require(one - overlap_toggle * overlap_toggle == s * s, "true CX motion")
    require(one - a * a == p * p, "true middle G motion")

    def report_motion(q):
        overlaps = (one - (one - overlap_toggle) * q, a, one - q)
        return sum_interval(module, [module.trace_distance(item) for item in overlaps])

    delta = module.minus(report_motion(p), report_motion(r))
    coefficient = module.times(module.enclosure(2 * s), module.plus(1, delta))
    require(delta[0] > Fraction("0.17"), "strict NC1 movement contrast")
    require(coefficient[0] > Fraction("0.55"), "strict total work source")
    return tuple(float(sum(bound) / 2) for bound in (delta, coefficient))


def sum_interval(module, items):
    total = module.interval(0)
    for item in items:
        total = module.plus(total, item)
    return total


def finite_field_obstruction(native):
    # 0,1,a,a+1 as F4 encoded in the binary polynomial basis.
    def mul(a, b):
        value = 0
        for bit in range(2):
            if b >> bit & 1:
                value ^= a << bit
        return value ^ 7 if value & 4 else value

    def plus_many(entries):
        value = 0
        for item in entries:
            value ^= item
        return value

    def affine(row, wires):
        base = row[0]
        terms = [(1 << (wires - 1 - j), row[1 << (wires - 1 - j)] ^ base)
                 for j in range(wires)]
        return all(value == base ^ plus_many(term for mask, term in terms if index & mask)
                   for index, value in enumerate(row))

    cx = sp.eye(4)[:, [0, 1, 3, 2]]
    symbols = {0: 0, 1: 1, -1: 1, native.A: 2, -native.A: 2,
               native.P: 3, -native.P: 3}
    for matrix, size in ((native.G_LOCAL, 1), (cx, 2), (native.SOURCE_I_LOCAL, 3)):
        weights = [[mul(symbols[matrix[i, j]], symbols[matrix[i, j]])
                    for j in range(2**size)] for i in range(2**size)]
        for mask in (0, *(1 << i for i in range(size))):
            f = [1 if not mask or i & mask else 0 for i in range(2**size)]
            back = [plus_many(mul(f[i], weights[i][j]) for i in range(2**size)) for j in range(2**size)]
            require(affine(back, size), "each actual primitive preserves affine rows")
            if mask == 0:
                require(back == f, "total mod-2 mass")

    # The original selection with T=0 has X=D*N. The output-head bit
    # probability is p²+p³*X; its mixed difference reduces to 1.
    p2 = mul(3, 3)
    p3 = mul(p2, 3)
    require(p2 == 2 and p3 == 1, "Golden field reduction")
    square = [[p2 ^ mul(p3, d * n) for n in range(2)] for d in range(2)]
    mixed = plus_many(entry for row in square for entry in row)
    require(mixed == 1, "original selector is not an affine registered probability")
    return square


def main():
    module = owner()
    gates = fixed_word(module.ne)
    mark_count = check_columns_and_born(module, gates)
    delta, motion = certify_motion(module)
    square = finite_field_obstruction(module.ne)
    print(json.dumps({
        "status": "PASS",
        "PR334_source_pin": "a3ef80fffd9bd5c4786e033e7233c8fd638e07c7",
        "fixed_native_gates": {"CX": 12, "G": 4},
        "fresh_golden_births": 8,
        "physical_NC1_reads": 4,
        "raw_word_columns_checked": 512,
        "positive_new_retained_marks_per_T": mark_count,
        "conditional_registered_price": "2*p^5 + 2*p^6*T",
        "same_field_source_as_PR334": "2*p^6 DPr(T=1)",
        "strict_NC1_movement_contrast": delta,
        "strict_mean_native_gate_movement_source_coefficient": motion,
        "symmetric_confirmation_source_coefficients": [0, 0],
        "original_mux_Born_field_square": square,
        "original_mux_nonlinear_mixed_difference_F4": 1,
        "implements_original_full_mux_tree": False,
        "full_physical_Cost_minus_Info_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
