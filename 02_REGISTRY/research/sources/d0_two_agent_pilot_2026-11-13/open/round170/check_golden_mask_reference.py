"""Replay the exact full Golden-record reference for the measured A82 mask law."""

from itertools import product
import json
from typing import NamedTuple


ONE = (1, 0)
P = (0, 1)
ZERO = (0, 0)


class Leaf(NamedTuple):
    word: str
    mark: int


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def subtract(x, y):
    return (x[0] - y[0], x[1] - y[1])


def multiply(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c - b * d)


def sign(x):
    # The sign of (2a-b) + b sqrt(5) is the sign of a+bp.
    a, b = x
    rational = 2 * a - b
    if rational >= 0 and b >= 0:
        return int(x != ZERO)
    if rational <= 0 and b <= 0:
        return -int(x != ZERO)
    comparison = rational * rational - 5 * b * b
    return 1 if (comparison > 0) == (rational > 0) else -1


def require(condition, context):
    if not condition:
        raise ArithmeticError(context)


def efficiency(angle_multiple):
    # cos(2theta)=2p-1 for sin(theta)=p. The doubled-angle recurrence
    # computes sin²(m theta) using only the original Golden integer ring.
    previous = ONE
    cosine_twice = current = (-1, 2)
    doubled_cosine = add(cosine_twice, cosine_twice)
    for _ in range(1, angle_multiple):
        previous, current = current, subtract(multiply(doubled_cosine, current), previous)
    total = subtract(ONE, current)
    require(all(value % 2 == 0 for value in total), "Golden integer efficiency")
    return (total[0] // 2, total[1] // 2)


def code_length(word):
    return len(word) + word.count("1")


def golden_sampler(target):
    require(sign(target) >= 0 and sign(subtract(ONE, target)) >= 0, "probability")
    prefix = ""
    leaves = []
    while target not in (ZERO, ONE):
        if sign(subtract(target, P)) < 0:
            leaves.append(Leaf(prefix + "1", 0))
            prefix += "0"
            target = multiply(target, (1, 1))  # divide by p
        else:
            leaves.append(Leaf(prefix + "0", 1))
            prefix += "1"
            target = multiply(subtract(target, P), (2, 1))  # divide by p²
    leaves.append(Leaf(prefix, target[0]))
    return leaves


def power_table(last):
    values = [ONE]
    for _ in range(last):
        values.append(multiply(values[-1], P))
    return values


def check_compact_cut():
    # Cost 8 or 9 uses the existing complete Fibonacci partition.
    frontier = [""]
    terminal = []
    while frontier:
        word = frontier.pop()
        if code_length(word) < 8:
            frontier.extend((word + "1", word + "0"))
        else:
            terminal.append(word)
    lengths = [code_length(word) for word in terminal]
    require(lengths.count(8) == 34 and lengths.count(9) == 21, "native cost cut")
    success_at_nine = [word for word in terminal if code_length(word) == 9][:16]
    powers = power_table(9)
    require(multiply((len(success_at_nine), 0), powers[9]) == efficiency(4),
            "native efficiency allocated to actual prefixes")
    require(multiply((16, 0), subtract(powers[7], powers[8])) == efficiency(4),
            "unique two-length coordinates exclude a positive representation through cost 8")
    return success_at_nine


def check_full_record(leaves, target, cycles):
    # Decode all raw sampler histories and the one actual payload read.
    # Each fine record contributes the single monomial p^(printed length).
    max_length = cycles * max(code_length(leaf.word) for leaf in leaves) + 2
    powers = power_table(max_length)
    observed = {}
    counts = [0, 0]
    for choices in product(leaves, repeat=cycles):
        mask = tuple(leaf.mark for leaf in choices)
        length = sum(code_length(leaf.word) for leaf in choices)
        cases = [(0, None)]
        cases += [(1, 0), (1, 1)] if any(mask) else [(1, None)]
        for prior, payload in cases:
            counts[prior] += 1
            letter = 0 if payload is None else 1 + payload
            key = (prior, mask, payload)
            observed[key] = add(observed.get(key, ZERO), powers[length + letter])
    for (prior, mask, payload), mass in observed.items():
        expected = ONE
        for success in mask:
            expected = multiply(expected, target if success else subtract(ONE, target))
        if payload is not None:
            require(prior == 1 and any(mask), "branch reveals the bit only on first success")
            expected = multiply(expected, powers[1 + payload])
        require(mass == expected, "coarse mask and payload probabilities")
    all_masks = len(leaves) ** cycles
    all_fail = sum(leaf.mark == 0 for leaf in leaves) ** cycles
    require(counts == [all_masks, 2 * all_masks - all_fail], "complete fine support")
    return counts


def check_sampler(angle_multiple, expected_leaves, expected_marks, expected_longest):
    target = efficiency(angle_multiple)
    leaves = golden_sampler(target)
    lengths = [code_length(leaf.word) for leaf in leaves]
    words = [leaf.word for leaf in leaves]
    require(len(set(words)) == len(words), "distinct raw records")
    require(not any(a != b and b.startswith(a) for a in words for b in words),
            "prefix-free records")
    require(len(leaves) == expected_leaves and sum(leaf.mark for leaf in leaves) == expected_marks
            and max(lengths) == expected_longest, "explicit sampler size")
    powers = power_table(max(lengths))
    normalizer, success = ZERO, ZERO
    for leaf, length in zip(leaves, lengths):
        normalizer = add(normalizer, powers[length])
        if leaf.mark:
            success = add(success, powers[length])
    require(normalizer == ONE and success == target, "mass of full stopped raw sampler")
    return {
        "angle_multiple": angle_multiple,
        "efficiency_in_1_p_basis": list(target),
        "leaves": [list(leaf) for leaf in leaves],
        "maximum_code_length": max(lengths),
        "full_records_Y0_then_Y1": [check_full_record(leaves, target, n) for n in range(1, 4)],
    }



def check_paid_refinements():
    target = efficiency(4)
    leaves = golden_sampler(target)
    counts = []
    for mark, expected in ((0, [14, 18]), (1, [14, 19])):
        index = next(i for i, leaf in enumerate(leaves) if leaf.mark == mark)
        parent = leaves[index]
        whole = leaves[:index] + [Leaf(parent.word + bit, mark) for bit in "01"] + leaves[index + 1:]
        refined = check_full_record(whole, target, 1)
        require(refined == expected, "complete paid refinement preserves the coarse law")
        counts.append(refined)
    return counts


def main():
    print(json.dumps({
        "status": "PASS",
        "sources": "A82 two-control instrument and canonical Golden cost cut",
        "literal_cost_9_success_prefixes_k1": check_compact_cut(),
        "exact_sparse_samplers": [check_sampler(4, 13, 4, 16), check_sampler(12, 35, 18, 52)],
        "counts_after_one_failure_then_one_success_refined_separately": check_paid_refinements(),
        "physical_full_cost_identified": False,
        "GR_closed": False,
    }, indent=2))


if __name__ == "__main__":
    main()
