#!/usr/bin/env python3
"""Independent exact controls for Structural.lean's scoped weighted examples."""
from itertools import product


def two_shift_square(field, weight, x):
    sx, sy = lambda p: p ^ 2, lambda p: p ^ 1
    xpart = weight[sx(x)] * (field[sy(sx(x))] - field[sx(x)])
    xpart -= weight[x] * (field[sy(x)] - field[x])
    ypart = weight[sy(x)] * (field[sx(sy(x))] - field[sy(x)])
    ypart -= weight[x] * (field[sx(x)] - field[x])
    return weight[x] * (xpart - ypart)


def two_shift_formula(field, weight, x):
    sx, sy = lambda p: p ^ 2, lambda p: p ^ 1
    return weight[x] * (
        (weight[sx(x)] - weight[sy(x)]) * field[sx(sy(x))]
        + (weight[sy(x)] - weight[x]) * field[sy(x)]
        + (weight[x] - weight[sx(x)]) * field[sx(x)]
    )


def exterior(field, multiplier, *, jordan_wigner=True):
    """Four directions on (Z/2)^4 with integer Jordan-Wigner CAR creation."""
    out = [[0] * 16 for _ in range(16)]
    for x in range(16):
        for ket in range(16):
            for role in range(4):
                bit = 1 << role
                if ket & bit:
                    continue
                bra = ket | bit
                sign = (-1) ** bin(ket & (bit - 1)).count("1") if jordan_wigner else 1
                out[x][bra] += multiplier[x] * sign * (
                    field[x ^ bit][ket] - field[x][ket]
                )
    return out


def main():
    checks = 0
    for weight in product((1, 2, 3), repeat=4):
        for point in range(4):
            for basis_index in range(4):
                field = [int(i == basis_index) for i in range(4)]
                if two_shift_square(field, weight, point) != two_shift_formula(field, weight, point):
                    raise ValueError("Two-shift expansion disagrees with direct composition")
                checks += 1
    if checks != 1296:
        raise ValueError("Unexpected number of two-shift checks")

    # Role order A,B,C,D is bits 0,1,2,3, matching the Lean CAR owner.
    probe = [[0] * 16 for _ in range(16)]
    probe[1][0] = 1  # shift A of the origin, vacuum
    multiplier = [2 if x & 1 else 1 for x in range(16)]
    weighted = exterior(exterior(probe, multiplier), multiplier)
    if weighted[0][3] != -1:  # origin; A and B occupied
        raise ValueError("Four-role CAR square did not produce the stated leakage")
    mutant = exterior(exterior(probe, multiplier, jordan_wigner=False), multiplier,
                      jordan_wigner=False)
    if mutant[0][3] == weighted[0][3]:
        raise ValueError("Jordan-Wigner sign mutation was not detected")
    plain = exterior(exterior(probe, [1] * 16), [1] * 16)
    if any(value for site in plain for value in site):
        raise ValueError("The unweighted exterior differential did not square to zero")
    print(f"PASS: {checks} exact two-shift formula controls")
    print("PASS: full four-role weighted CAR square has 0-to-2 element -1")
    print("PASS: Jordan-Wigner sign mutation changes the checked element")
    print("PASS: full unweighted square vanishes on the probe")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
