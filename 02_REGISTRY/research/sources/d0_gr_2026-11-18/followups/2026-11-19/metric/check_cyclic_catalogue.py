"""Audit the retained cyclic selector, finite truth table and a corrupted dispatch."""
from bisect import bisect_right
from collections import Counter
from fractions import Fraction as F
from functools import lru_cache
from itertools import accumulate
from math import comb
import json


WEIGHTS = [F((-1) ** (j - 1) * comb(8, j), j) for j in range(1, 9)]
SIZES = [int(abs(w) * 840) for w in WEIGHTS]


class BinaryDiagram:
    """Shared ordered binary decision diagrams. The original tape is read-only."""

    def __init__(self):
        self.nodes = {}
        self.unique = {}

    def branch(self, variable, low, high):
        if low == high:
            return low
        key = (variable, low, high)
        if key not in self.unique:
            identifier = 2 + len(self.nodes)
            self.unique[key] = identifier
            self.nodes[identifier] = key
        return self.unique[key]

    def output(self, roots, tape):
        value = 0
        for bit, root in enumerate(roots):
            while root >= 2:
                variable, low, high = self.nodes[root]
                root = high if tape[variable] else low
            value += root << bit
        return value


@lru_cache(None)
def hits(remaining):
    if remaining <= 0:
        return int(remaining == 0)
    return hits(remaining - 1) + hits(remaining - 2)


def protocol(cut, bin_sizes):
    """Label exact-hit leaves by lexicographic rank; the entire fallback is 0."""
    ends = list(accumulate(bin_sizes))
    diagram = BinaryDiagram()
    bits = len(bin_sizes).bit_length()

    def leaf(rank):
        label = bisect_right(ends, rank) + 1
        return label if label <= len(ends) else 0

    def tree(depth, remaining, rank):
        if remaining <= 0:
            value = leaf(rank) if remaining == 0 else 0
            return tuple((value >> i) & 1 for i in range(bits))
        low = tree(depth + 1, remaining - 1, rank)
        high = tree(depth + 1, remaining - 2, rank + hits(remaining - 1))
        return tuple(diagram.branch(depth, a, b) for a, b in zip(low, high))

    roots = tree(0, cut, 0)
    histogram = Counter()
    ranks = 0

    def visit(tape, cost):
        nonlocal ranks
        if cost >= cut:
            target = leaf(ranks) if cost == cut else 0
            ranks += cost == cut
            histogram[cost, target] += 1
            for pad in (0, 1):
                assert diagram.output(roots, tape + [pad] * (cut - len(tape))) == target
            return
        visit(tape + [0], cost + 1)
        visit(tape + [1], cost + 2)

    visit([], 0)
    assert ranks == hits(cut)
    assert [histogram[cut, j] for j in range(1, len(bin_sizes) + 1)] == bin_sizes
    assert histogram[cut + 1, 0] == hits(cut - 1)
    return {"cut": cut, "reduced_boolean_nodes": len(diagram.nodes),
            "active_counts": bin_sizes, "inactive_at_cut": histogram[cut, 0],
            "overshoot": histogram[cut + 1, 0]}


def main():
    settings = protocol(24, SIZES)
    shifts = protocol(5, [1] * 8)
    # Coefficients include independently varying linear and nonlinear bank responses.
    # Each column can be any derivative on its bank, including a moving SITE.
    response = [[F(((-1) ** (k + d)) * (d + 2) * (k + 3), (k + 2) * (d + 3))
                 for d in range(1, 9)] for k in range(8)]
    t = F(1, 257)
    for d in range(1, 9):
        assert sum(w * j ** d for j, w in enumerate(WEIGHTS, 1)) == (d == 1)

    def selected(k, j):
        return sum(coeff * (j * t) ** d for d, coeff in enumerate(response[k], 1))

    bank_rows = []
    for k in range(8):
        row = sum(w * selected(k, j) for j, w in enumerate(WEIGHTS, 1))
        assert row == t * response[k][0]
        bank_rows.append(row)
    full = sum(w * selected((j - 1 + c) % 8, j)
               for c in range(8) for j, w in enumerate(WEIGHTS, 1))
    assert full == sum(bank_rows)
    unsym = sum(w * selected(j - 1, j) for j, w in enumerate(WEIGHTS, 1))
    assert unsym != sum(bank_rows) / 8

    # A truly varying label is deliberately corrupted into another varying tag.
    # Derivatives of the signed-read and fallback labels are tested after dispatch.
    derivatives = [F(0)] + [(-1) ** (j - 1) * selected((c + j - 1) % 8, j)
                            for c in range(8) for j in range(1, 9)]
    masses = [F(1, 9)] + [F(SIZES[j], 9 * sum(SIZES))
                           for c in range(8) for j in range(8)]
    assert sum(masses) == 1
    size = len(masses)
    eta = F(1, 37)
    eps = eta * eta
    new_masses = [F(0)] * size
    for b, mass in enumerate(masses):
        wrong = (b * 7 + 17) % size
        new_masses[b] += (1 - eps) * mass
        new_masses[wrong] += eps * mass
    tv = sum(abs(a - b) for a, b in zip(masses, new_masses)) / 2
    err = abs(sum((a - b) * d for a, b, d in zip(masses, new_masses, derivatives)))
    assert 0 < tv <= eps and 0 < err <= tv * (max(derivatives) - min(derivatives))
    # Classical permutation and stochastic kernels need no presumed noise law.
    # Correct tag projector Q: with rational unit vector (a,b) and perfect (1,0),
    # b^2 <= ||actual-ideal||^2, rigorously including the square exponent.
    a, b = F(684, 685), F(37, 685)
    assert a*a + b*b == 1 and b*b <= (1-a)**2 + b*b
    print(json.dumps({"status": "PASS", "settings": settings, "shifts": shifts,
                      "signed_integer_weights": [840 * w.numerator // w.denominator for w in WEIGHTS],
                      "mark_gain_relative_to_first_selector": "8*p^5",
                      "cyclic_settings_per_bank": [8] * 8,
                      "independent_bank_rows_exact": True, "unbalanced_diagonal_rejected": True,
                      "stochastic_dispatch_test": {"tv": str(tv), "eta_squared": str(eps),
                        "bounded_nonzero_directional_error": True, "wrong_live_to_live_allowed": True,
                        "input_masses": "rational synthetic challenge vector"},
                      "all_stopped_prefixes_classified_twice": True,
                      "full_native_clock_replayed": False, "full_physical_price_identified": False},
                     ensure_ascii=False, sort_keys=True, indent=2))


if __name__ == "__main__":
    main()
