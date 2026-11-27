#!/usr/bin/env python3
"""Enumerate intertwiners for natural and trivial S3 actions on three labels."""
from itertools import permutations, product


def main() -> int:
    group = list(permutations(range(3)))
    maps = list(product(range(3), repeat=3))
    if len(group) != 6 or len(maps) != 27:
        raise ValueError("The finite carriers have unexpected sizes")

    equivariant = [
        f for f in maps
        if all(f[sigma[x]] == f[x] for sigma in group for x in range(3))
    ]
    injective = [f for f in equivariant if len(set(f)) == 3]
    natural_to_natural = [
        f for f in maps
        if len(set(f)) == 3
        and all(f[sigma[x]] == sigma[f[x]] for sigma in group for x in range(3))
    ]

    if len(equivariant) != 3 or injective:
        raise ValueError("The natural-to-trivial action comparison failed")
    if natural_to_natural != [(0, 1, 2)]:
        raise ValueError("The natural-to-natural identity control failed")
    print("PASS: all three natural-to-trivial intertwiners are constant")
    print("PASS: no injective natural-to-trivial intertwiner exists")
    print("PASS: the natural-to-natural identity is an equivariant bijection")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
