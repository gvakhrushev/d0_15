"""Exact finite checks for scene-free class selection by comparison statistics.

Uses only the Python standard library.
Checks:
1. Enumeration of all 17 integer partitions of N=33 with sum of squares C=371.
2. Unique minimizer of cubic moment P3 is (9, 11, 13) with sum of cubes 4257 (P3 = 43/363).
3. Next partition has sum of cubes 4617 (or 4797 with all parts >= 2).
4. Parametric certificate identity for all m >= 9, showing (m-2, m, m+2) is the unique minimizer
   for total 3m and squares 3m^2 + 8.
"""

from collections import Counter
from fractions import Fraction


def constrained_partitions(total, squares, lower=1):
    """Enumerate every nondecreasing positive integer partition with two moments."""
    if total == 0:
        if squares == 0:
            yield ()
        return
    for first in range(lower, total + 1):
        if first * first > squares:
            break
        for rest in constrained_partitions(total - first, squares - first * first, first):
            yield (first,) + rest


def cube_sum(partition):
    return sum(n**3 for n in partition)


def certificate(m, t):
    return (3 * m - t) * (3 * m**3 + 24 * m - t**3) - (3 * m * m + 8 - t * t) ** 2


def main():
    partitions = sorted(constrained_partitions(33, 371), key=cube_sum)
    assert len(partitions) == 17
    assert partitions[0] == (9, 11, 13)
    assert cube_sum(partitions[0]) == 4257
    assert partitions[1] == (1, 8, 9, 15)
    assert cube_sum(partitions[1]) == 4617
    assert [p for p in partitions if cube_sum(p) <= 4257] == [(9, 11, 13)]
    archives = [p for p in partitions if p[0] >= 2]
    assert set(archives) == {
        (9, 11, 13),
        (3, 4, 11, 15),
        (3, 5, 9, 16),
        (2, 2, 5, 7, 17),
        (2, 3, 3, 3, 4, 18),
    }
    assert [p for p in archives if len(set(p)) == len(p)] == [
        (9, 11, 13),
        (3, 4, 11, 15),
        (3, 5, 9, 16),
    ]

    # Exact checks of polynomial identities; universal signs are proved analytically.
    for m in range(9, 31):
        for t in range(1, 3 * m):
            expanded = (
                -3 * m * t**3
                + (6 * m * m + 16) * t * t
                - (3 * m**3 + 24 * m) * t
                + 24 * m * m
                - 64
            )
            assert certificate(m, t) == expanded
            if t <= m - 3:
                secant = certificate(m, 1) + Fraction(t - 1, m - 4) * (
                    certificate(m, m - 3) - certificate(m, 1)
                )
                remainder = (t - 1) * (t - m + 3) * (-3 * m * t + 3 * m * m + 6 * m + 16)
                assert certificate(m, t) - secant == remainder
                assert certificate(m, t) < 0
            if t >= m + 3:
                z = t - m - 3
                upper = (
                    -11 * m * m
                    - 57 * m
                    + 80
                    + (96 - 18 * m * m - 73 * m) * z
                    + (16 - 3 * m * m - 27 * m) * z * z
                    - 3 * m * z**3
                )
                assert certificate(m, t) == upper < 0

    # Independent finite instances of the family theorem.
    for m in range(9, 13):
        candidates = list(constrained_partitions(3 * m, 3 * m * m + 8))
        optimum = min(map(cube_sum, candidates))
        assert optimum == 3 * m**3 + 24 * m
        assert [p for p in candidates if cube_sum(p) == optimum] == [
            (m - 2, m, m + 2)
        ]

    assert Fraction(4257, 33**3) == Fraction(43, 363)
    assert 33**2 - 371 == 718
    assert 6 * 9 * 11 * 13 == 7722

    print("PASS: scene-free class selection certificate verified.")
    print("Unique minimum: (9, 11, 13), P3 = 43/363.")


if __name__ == "__main__":
    main()
