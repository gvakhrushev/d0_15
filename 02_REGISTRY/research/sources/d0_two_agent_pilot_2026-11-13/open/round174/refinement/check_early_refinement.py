"""Recompute the physical first-digit weights and the exact SC1 moments."""

from fractions import Fraction
from math import comb
from pathlib import Path
import json


DENOMINATOR = 705600
SETTINGS = range(1, 9)


def require(condition, label):
    if not condition:
        raise ValueError(label)


def exact_prefix_counts(price):
    counts = [1, 1]
    for budget in range(2, price + 1):
        counts.append(counts[budget - 1] + counts[budget - 2])
    return counts


def main():
    counts = exact_prefix_counts(36)
    zero_prefixes = counts[35]
    start = 0
    first_counts = [[], []]
    for j in SETTINGS:
        n_j = Fraction(DENOMINATOR * comb(8, j), j**2)
        require(n_j.denominator == 1, f"native count for j={j}")
        end = start + int(n_j)
        zero = max(0, min(end, zero_prefixes) - start)
        first_counts[0].append(zero)
        first_counts[1].append(int(n_j) - zero)
        start = end
    require(start <= counts[36], "all active intervals fit the native tree")
    require(
        first_counts[0] == [5644800, 4939200, 4346352, 0, 0, 0, 0, 0],
        "native first digit zero",
    )
    require(
        first_counts[1] == [0, 0, 44048, 3087000, 1580544, 548800, 115200, 11025],
        "native first digit one",
    )
    moments = [
        [
            sum(
                count * (-1) ** (j - 1) * j ** degree
                for j, count in zip(SETTINGS, column)
            )
            for degree in range(2, 10)
        ]
        for column in first_counts
    ]
    require(
        [left + right for left, right in zip(*moments)] == [DENOMINATOR] + [0] * 7,
        "native all-address interpolation",
    )
    require(moments[0][:2] == [25005168, 83482704], "first two zero-sector moments")

    ell_upper = Fraction("0.482")
    gap_factor = Fraction("0.32")
    a2, a3 = [Fraction(value, DENOMINATOR) for value in moments[0][:2]]
    require((a2 - 1) * gap_factor / ell_upper > 22, "first digit leading slope")
    require(a3 * gap_factor / ell_upper > 78, "first digit cubic slope")

    owner_receipt_path = (
        Path(__file__).resolve().parents[2] / "round173" / "FIRST_DIGIT_SOURCE_RESULT.json"
    )
    owner_receipt = json.loads(owner_receipt_path.read_text())
    require(
        owner_receipt["first_digit_split_of_the_actual_selector36"]
        == [list(pair) for pair in zip(*first_counts)],
        "physical first digit in B173",
    )
    print(json.dumps({"first_digit_counts": first_counts, "signed_moments": moments}))


if __name__ == "__main__":
    main()
