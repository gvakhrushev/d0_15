"""Check all raw leaves, literal CNOT printing, and the two price bases."""

from collections import Counter
from hashlib import sha256
from itertools import product
import json
from pathlib import Path

import sympy as sp


ROOT = Path(__file__).resolve().parents[6]
RESEARCH = "02_REGISTRY/research/"
PILOT = RESEARCH + "sources/d0_two_agent_pilot_2026-11-13/"
SOURCES = (
    "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
    RESEARCH + "A4D_BOOK03_GOLDEN_NO_POLAR_FINITE_NATIVE_STOP_COMPILER_2026_10_22.md",
    RESEARCH + "sources/d0_paid_moment_field_writer_2026-10-21/book/"
    "COMPLETE_CODE_WRITER_BOOK_PRICE.md",
    PILOT + "open/round149/RESULT.json",
    PILOT + "direct/round75/history/TWO_SITE_SOURCE_RU.md",
)
p = sp.Symbol("p")
RELATION = p**2 + p - 1
EXACT_P = (sp.sqrt(5)-1)/2


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def equivalent(actual, expected, message):
    numerator = sp.together(actual-expected).as_numer_denom()[0]
    require(sp.rem(sp.expand(numerator), RELATION, p) == 0, message)


def execute(state, word):
    result = list(state)
    for control, target in word:
        result[target] ^= result[control]
    return tuple(result)


def check_serializer():
    c, d = (0, 1), (1, 0)
    words = ((c, c, d, d), (d, c, d, c), (c, d, c, d))
    for r, s, bit in product(range(2), repeat=3):
        word = words[0 if not r else 1+s]
        final = execute((r, s, bit), word)
        require(final[0] == 0 and final[2] == bit, "Actual second symbol is zero")
        require(Counter(word) == {c: 2, d: 2}, "Same addressed printing inventory")
        require(execute(final, reversed(word)) == (r, s, bit), "Restore old print work")


def check_gain(states, extra_price, multiplicity):
    # Check two different raw read orders. The proof uses a conditional cost
    # bound independent of the order and includes the full canonical raw code.
    raw_count = len(states[0])
    raw_orders = (tuple(range(raw_count)), tuple(reversed(range(raw_count))))
    bound = 1-multiplicity*p**2
    h = p+2*p**2
    for order in raw_orders:
        for depth, coordinate in enumerate(order):
            for previous in product(range(2), repeat=depth):
                parent = [state for state in states
                          if tuple(state[index] for index in order[:depth]) == previous]
                children = []
                for read_bit in (0, 1):
                    children.append(sp.rem(sum(
                        extra_price[state] * p**sum(1+state[index]
                                                     for index in order[depth+1:])
                        for state in parent if state[coordinate] == read_bit),
                        RELATION, p))
                mean = p*children[0] + p**2*children[1]
                for child_cost in children:
                    difference = sp.rem(h + child_cost - mean - bound, RELATION, p)
                    require(bool(difference.subs(p, EXACT_P) >= 0), "Strict raw Info margin")


def check_cell(parity_length, copies, raw_count):
    states = list(product(range(2), repeat=raw_count))
    u, b = raw_count-2, raw_count-1
    a = tuple((index, u) for index in range(parity_length))
    B = (u, b)
    before, after = (B, B)+a, (B,)+a+(B,)
    require(Counter(before) == Counter(after), "Equal gate inventory per physical cell")
    costs = ({}, {})
    for state in states:
        parity = sum(state[:parity_length]) % 2
        low, high = execute(state, before), execute(state, after)
        require(low[:-1] == high[:-1] and low[u] == state[u] ^ parity, "Same work output")
        require(low[b] == state[b] and high[b] == state[b] ^ parity, "Printed bit truth table")
        for slot, (final, word) in enumerate(((low, before), (high, after))):
            require(execute(final, reversed(word)) == state, "Full deterministic state return")
            costs[slot][state] = copies*(1+state[b]) + 1+final[b]
    average = sum(p**(raw_count+sum(state))*(costs[1][state]-costs[0][state])
                  for state in states)
    price_step = p**3*(1-p**(3*parity_length))/2
    equivalent(average, price_step, "Exact Born price step, full raw probabilities")
    z = [sum(p**cost for cost in tariff.values()) for tariff in costs]
    ratio = 2*(1+p**(copies+1))/((1+p**copies)*(1+p))
    equivalent(z[0]/z[1], ratio, "Absolute local-surprise sum, all raw leaves")
    for tariff in costs:
        check_gain(states, tariff, copies)
    return price_step, ratio


def main():
    check_serializer()
    check_cell(1, 1, 4)
    check_cell(2, 1, 4)
    cells = ((1, 1), (2, 1), (3, 1), (1, 2))
    steps = {cell: check_cell(*cell, raw_count=5) for cell in cells}
    price_1, r1 = steps[1, 1]
    price_2, _ = steps[2, 1]
    price_3, _ = steps[3, 1]
    _, r2 = steps[1, 2]
    equivalent(price_1, p**5, "First native coefficient")
    equivalent(price_2, 2*p**6, "Second native coefficient")
    equivalent(price_2-price_1, p**8, "First horizontal step")
    equivalent(price_3-price_2, p**11, "Second horizontal step")
    equivalent(r1*r1.subs(p, -1-p), 20, "First log coefficient field norm")
    equivalent(r2*r2.subs(p, -1-p), sp.Rational(16, 5), "Second log coefficient field norm")
    for a, b in ((1, 0), (0, 1), (-5, 7)):
        equivalent((16*a+10*b)*p**5+(5*a+3*b)*2*p**6, 2*(a+b*p),
                   "Exact finite Golden code formula")
    equivalent(16*p**5+5*2*p**6-2, 0, "Conditional old-Bellman neutrality relation")
    print(json.dumps({
        "GR_closed": False,
        "full_physical_class_map_and_price_proved": False,
        "raw_outcomes_per_general_cell": 32,
        "actual_CNOT_print_cycle_and_inverse": 8,
        "Bellman_positive_bound_for_cells_with_two_prior_prints": "p^3",
        "unit_preserving_pair_of_prices_is_dense": True,
        "Bellman_horizontal_steps": ["p^8", "p^11"],
        "local_surprise_field_norms": ["20", "16/5"],
        "source_sha256": {path: sha256((ROOT / path).read_bytes()).hexdigest()
                          for path in SOURCES},
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
