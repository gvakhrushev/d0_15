"""Exact checks for occupied SER1 cleanup and the growing Book mixed contrast."""

from fractions import Fraction
from functools import reduce
from hashlib import sha256
from itertools import product
import json
from math import factorial
from operator import mul
from pathlib import Path
import subprocess

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[5]
PRIMARY = (
    "02_REGISTRY/research/"
    "A4D_NONVACUUM_SAME_REPRESENTATIVE_PAID_SOURCE_RESIDUAL_2026_10_20.md"
)
ZETA = Fraction(1, 2**20)


def require(condition, reason):
    if not condition:
        raise AssertionError(reason)


def check_cleanup():
    # The actual SER1 cursor is initialized to 0, copied with CX(r,c), then
    # cleaned by the same CX after both output times.
    cx = {(r, c): (r, c ^ r) for r, c in product(range(2), repeat=2)}
    flags = {}
    for bit in (0, 1):
        before = cx[bit, 0]
        after = cx[before]
        require(after == (bit, 0), "Final cleanup must restore the initialized cursor")
        flags[bit] = before != after
    require(flags == {0: False, 1: True}, "SER1 occupation is not the original record")
    require(all(cx[cx[state]] == state for state in cx),
            "Both CX calls must retain the full complementary columns")
    return {"occupied_cursor_changes": flags, "selected_stage": 57,
            "effect_on_root": "original Q", "mean_excess_response": "eta * Dq"}


def check_reordered_completion():
    states = tuple(product(range(2), repeat=3))
    tail = {x: (x[0], x[1], x[2] ^ x[0]) for x in states}
    cursor = {x: (x[0], x[1] ^ x[0], x[2]) for x in states}
    first = (tail, tail, cursor)
    second = (cursor, tail, tail)
    prefix_a = {x: x for x in states}
    prefix_b = prefix_a.copy()
    for gate_a, gate_b in zip(first, second):
        frame = {prefix_a[x]: prefix_b[x] for x in states}
        prefix_a = {x: gate_a[prefix_a[x]] for x in states}
        prefix_b = {x: gate_b[prefix_b[x]] for x in states}
        next_frame = {prefix_a[x]: prefix_b[x] for x in states}
        require(all(gate_b[frame[x]] == next_frame[gate_a[x]] for x in states),
                "The post-output stage frame does not intertwine")
    require(prefix_a == prefix_b == cursor, "The full endpoints must agree")

    def trajectory(bit, gates):
        current = (bit, bit, 0)
        path = [current]
        for gate in gates:
            current = gate[current]
            path.append(current)
        return ["".join(map(str, state)) for state in path]

    paths = [trajectory(1, gates) for gates in (first, second)]
    require(paths == [["110", "111", "110", "100"], ["110", "100", "101", "100"]],
            "The occupied histories changed")
    require(all(trajectory(0, gates) == ["000"]*4 for gates in (first, second)),
            "The inactive occupied history changed")
    return {"new_steps_total": 59, "active_paths": paths,
            "same_full_endpoint_and_declared_mark_effects": True}


def hot_bound(length):
    x = Fraction(2, 55)
    return (Fraction(176, 359) * x**length
            / (factorial(length) * (1 - x*x) * (1 - x/length)))


def test_mixed_sign(dimension, attenuation):
    # Rational internal examples. No rational endpoint is used in place of
    # an actual Golden compiled H.1 state.
    ends = [(Fraction(1, 10 + i), Fraction(1, 5 + i))
            for i in range(dimension)]
    variable_terms = {1: [], -1: []}
    for bits in product(range(2), repeat=dimension):
        parity = (-1)**(dimension - sum(bits))
        cold = attenuation * reduce(mul, (ends[i][b] for i, b in enumerate(bits)))
        variable_terms[parity].append(1 - ZETA + ZETA*cold)
    require(reduce(mul, variable_terms[1]) > reduce(mul, variable_terms[-1]),
            "The mixed difference of the negative log determinant has wrong sign")


def check_mixed_contrasts():
    # At the actual fixed SER1 q_ref, A71 proves 3/25 < q_ref < 7/50.
    # Use only these bounds and the exact phi range, not rounded q_ref.
    p_min, p_max = Fraction(3, 5), Fraction(5, 8)
    a_min, a_plus_p_max = Fraction(3, 4), Fraction(3, 2)
    q_lo, q_hi = Fraction(3, 25), Fraction(7, 50)
    require(p_min + p_min*p_min < 1 < p_max + p_max*p_max,
            "Golden root bracket failed")
    require(a_min*a_min < p_min and (a_plus_p_max - p_max)**2 > p_max,
            "Golden square-root bracket failed")
    low_w = p_min*p_min * (a_min - a_plus_p_max*q_hi)**2
    delta_w = 4*a_min*p_min**3*q_lo*(1-q_hi)
    require(low_w > Fraction(1, 10) and p_max**3 < Fraction(1, 4),
            "Absolute cold intervals failed")
    require(delta_w > Fraction(1, 16), "Actual literal phase contrast bracket failed")

    counts = {}
    for dimension in range(2, 13):
        spacer = 0
        while (ZETA / (1-ZETA)) * Fraction(1, 4)**spacer > Fraction(1, 2**(dimension+1)):
            spacer += 1
        nu_low = (ZETA / (1-ZETA)) * Fraction(1, 10)**spacer
        nu_hi = (ZETA / (1-ZETA)) * Fraction(1, 4)**spacer
        require(2**(dimension-1)*nu_hi <= Fraction(1, 4),
                "Higher terms no longer bounded by one third")
        gap = Fraction(1, 3)*4*nu_low * Fraction(1, 16)**dimension
        # Count from the conservative shortest genuine wrap length 1.
        pairs = 0
        while 2**dimension * hot_bound(1+2*pairs) >= gap:
            pairs += 1
        counts[dimension] = {"literal_common_spacer_blocks": spacer,
                             "sufficient_common_paid_CX_pairs": pairs}
        if dimension <= 8:
            test_mixed_sign(dimension, Fraction(1, 5)**spacer)
    return {"phase_fixture_weight_bounds": ["1/10", "1/4"],
            "phase_fixture_gap_lower": "1/16",
            "strict_rational_padding_bounds": counts}


def main():
    source_paths = [
        PRIMARY,
        "01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS.md",
        "03_FORMALIZATION/D0/Foundation/EndogenousActionQuantum.lean",
        "03_FORMALIZATION/D0/Foundation/ProspectiveExecution.lean",
    ]
    receipt = {
        "source_sha256": {path: sha256(subprocess.check_output([
            "git", "show", f"dc411daf01f697ec85dd22f28bfe124171796645:{path}"
        ], cwd=REPO) if path == PRIMARY
            else (REPO / path).read_bytes()).hexdigest()
                          for path in source_paths},
        "serializer": check_cleanup(),
        "reordered_completion": check_reordered_completion(),
        "Book_growing_clock_comparison": check_mixed_contrasts(),
        "physical_edge_tariff_selected": False,
        "full_Cost_minus_Info_bound_to_Book_master": False,
        "GR_closed": False,
        "status": "PASS",
    }
    print(json.dumps(receipt, indent=2))


if __name__ == "__main__":
    main()
