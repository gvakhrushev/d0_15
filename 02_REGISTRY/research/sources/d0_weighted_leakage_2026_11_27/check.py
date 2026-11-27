#!/usr/bin/env python3
"""Check an exact finite weighted differential and a constant-weight control."""
from __future__ import annotations

SITES = range(4)


def shift_x(site: int) -> int:
    return site ^ 2


def shift_y(site: int) -> int:
    return site ^ 1


def dx(field: list[int]) -> list[int]:
    return [field[shift_x(i)] - field[i] for i in SITES]


def dy(field: list[int]) -> list[int]:
    return [field[shift_y(i)] - field[i] for i in SITES]


def weighted_square(field: list[int], weight: list[int]) -> list[int]:
    x = [weight[i] * value for i, value in enumerate(dx(field))]
    y = [weight[i] * value for i, value in enumerate(dy(field))]
    dx_y = dx(y)
    dy_x = dy(x)
    return [weight[i] * (dx_y[i] - dy_x[i]) for i in SITES]


def main() -> int:
    basis = [[int(i == j) for i in SITES] for j in SITES]
    constant = [1, 1, 1, 1]
    if any(weighted_square(field, constant) != [0, 0, 0, 0] for field in basis):
        raise ValueError("The constant-weight nilpotency control failed")

    weight = [1, 1, 2, 2]
    observed = [weighted_square(field, weight) for field in basis]
    expected = [[0, 0, 2, -2], [0, 0, -2, 2], [-1, 1, 0, 0], [1, -1, 0, 0]]
    if observed != expected:
        raise ValueError(f"The weighted square changed: {observed}")
    print("PASS: unweighted square is zero on a basis")
    print("PASS: varying-weight witness gives -1 at site 0 for basis vector 2")
    print("PASS: all four weighted square columns match exact integer values")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
