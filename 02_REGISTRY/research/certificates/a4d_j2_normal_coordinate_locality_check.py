#!/usr/bin/env python3
"""Combinatorial certificate for WRK-A4D-J2-NORMAL-COORDINATE-LOCALITY.

Enumerates derivative-order compositions of total order 0, 1 and 2 and
evaluates them on the normal-coordinate jet q = 0, dq = 0, with a nonzero
second-derivative sentinel. Checks the exact scaling

    h^{-2} * |h n|^3 = h |n|^3

that turns a uniform cubic symbol remainder into an O(h) majorant when the
third Fourier moment does not depend on h.

No star-symbol coefficient is computed. No resonance orbit is classified.
No shrinking-bump family is used as a hypothesis.
"""

from __future__ import annotations

from fractions import Fraction
from itertools import product


def fail(name: str) -> None:
    raise SystemExit(f"FAIL {name}")


def check(name: str, cond: bool) -> None:
    if not cond:
        fail(name)
    print(f"PASS {name}")


def compositions(m: int, degree: int) -> list[tuple[int, ...]]:
    return [orders for orders in product(range(degree + 1), repeat=m) if sum(orders) == degree]


def schematic(orders: tuple[int, ...]) -> str:
    degree = sum(orders)
    if degree == 0:
        return "constant"
    if degree == 1 and orders.count(1) == 1 and orders.count(0) == len(orders) - 1:
        return "q^{m-1} dq"
    if degree == 2 and orders.count(2) == 1 and orders.count(0) == len(orders) - 1:
        return "q^{m-1} d2q"
    if degree == 2 and orders.count(1) == 2 and orders.count(0) == len(orders) - 2:
        return "q^{m-2} (dq)(dq)"
    fail(f"unclassified composition {orders}")
    return ""


def jet_product(orders: tuple[int, ...], jet: dict[int, int]) -> int:
    value = 1
    for order in orders:
        value *= jet[order]
    return value


# Normal-coordinate center: undifferentiated and once-differentiated factors vanish.
# The second derivative is a nonzero sentinel, so survival is visible.
NORMAL = {0: 0, 1: 0, 2: 1}
# The same monomials away from that center, used only as a negative control.
AWAY = {0: 1, 1: 1, 2: 1}
# Flat-branch input: every zero-momentum symbol coefficient vanishes.
FLAT_CONSTANT = 0

EXPECTED_KIND = {
    0: {"constant"},
    1: {"q^{m-1} dq"},
    2: {"q^{m-1} d2q", "q^{m-2} (dq)(dq)"},
}


def expected_count(m: int, degree: int) -> int:
    if degree == 0:
        return 1
    if degree == 1:
        return m
    return m + (m * (m - 1)) // 2


for m in range(1, 9):
    for degree in (0, 1, 2):
        rows = compositions(m, degree)
        kinds = {schematic(row) for row in rows}
        check(f"count m={m} d={degree}", len(rows) == expected_count(m, degree))
        if degree == 2 and m == 1:
            check(f"kinds m={m} d={degree}", kinds == {"q^{m-1} d2q"})
        else:
            check(f"kinds m={m} d={degree}", kinds == EXPECTED_KIND[degree])
        for row in rows:
            if degree == 0:
                check(f"flat-branch kills {row}", FLAT_CONSTANT == 0)
                continue
            at_center = jet_product(row, NORMAL)
            if m >= 2 or degree == 1:
                check(f"center zero {row}", at_center == 0)
            else:
                check(f"linear second jet survives {row}", at_center == 1)

# Degree 1 is not identically zero. Vanishing uses the normal jet.
check("degree 1 survives away from the center", jet_product((1, 0), AWAY) == 1)
check("degree 1 vanishes at the center", jet_product((1, 0), NORMAL) == 0)

# The degree cutoff is sharp: two second derivatives need total degree 4.
check("sharp (2, 2) survives the sentinel", jet_product((2, 2), NORMAL) == 1)
for m in range(2, 9):
    check(f"all factors of order >=2 need degree >=4 when m={m}", 2 * m >= 4)

# Index permutation stays inside one schematic class.
double = {(2, 0, 0), (0, 2, 0), (0, 0, 2)}
check("permutation class", {schematic(row) for row in double} == {"q^{m-1} d2q"})

# A tensor contraction is a coefficient times the same derivative monomial.
coefficient = Fraction(3, 7) - Fraction(11, 5)
check("nonzero contraction coefficient", coefficient != 0)
check(
    "contraction vanishes with the monomial",
    coefficient * jet_product((1, 0, 1), NORMAL) == 0,
)

# Cubic majorant. |hn| = h|n| for h > 0, any absolutely homogeneous norm.
def cubic_majorant(h: Fraction, weights: tuple[tuple[int, Fraction], ...], constant: Fraction) -> Fraction:
    total = Fraction(0)
    for abs_n, amplitude in weights:
        total += constant * (h * abs_n) ** 3 * amplitude
    return h ** (-2) * total


def third_moment(weights: tuple[tuple[int, Fraction], ...]) -> Fraction:
    return sum((Fraction(abs_n) ** 3) * amplitude for abs_n, amplitude in weights)


WEIGHTS = (
    (0, Fraction(1)),
    (1, Fraction(2)),
    (3, Fraction(1, 4)),
    (5, Fraction(1, 8)),
)
CONSTANT = Fraction(7, 3)
MOMENT = third_moment(WEIGHTS)
check("fixed third moment is finite", MOMENT > 0)

# Euclidean norm on a lattice vector: |n|^2 = 25, so |n| = 5 and |hn| = 5h.
VECTOR = (1, 2, 2, 4)
vector_square = sum(Fraction(component) ** 2 for component in VECTOR)
check("euclidean square", vector_square == 25)
for raw_h in (Fraction(1, 2), Fraction(3, 7)):
    scaled_square = sum((raw_h * Fraction(component)) ** 2 for component in VECTOR)
    check(f"euclidean homogeneity h={raw_h}", scaled_square == raw_h**2 * vector_square)
    check(f"euclidean cubic majorant h={raw_h}", raw_h ** (-2) * (5 * raw_h) ** 3 == raw_h * 125)

ratios = []
for raw_h in (Fraction(1, 2), Fraction(1, 10), Fraction(3, 7), Fraction(1, 100)):
    got = cubic_majorant(raw_h, WEIGHTS, CONSTANT)
    expect = CONSTANT * raw_h * MOMENT
    check(f"scaling identity h={raw_h}", got == expect)
    ratios.append(got / raw_h)
check("O(h) ratio independent of h", len(set(ratios)) == 1)

# Negative control: an h-dependent third moment of size h^{-2} is not O(h).
shrinking = [CONSTANT * raw_h * (1 / raw_h**2) for raw_h in (Fraction(1, 2), Fraction(1, 10), Fraction(1, 100))]
check("shrinking moment is not O(h)", shrinking[0] < shrinking[1] < shrinking[2])

# Homogeneous degree d >= 3 normalizes to O(h^{d-2}), hence O(h) for 0 < h <= 1.
for degree in range(3, 8):
    for raw_h in (Fraction(1, 2), Fraction(1, 10)):
        normalized = raw_h ** (-2) * raw_h**degree
        check(f"degree {degree} exponent h={raw_h}", normalized == raw_h ** (degree - 2))
        check(f"degree {degree} is O(h) h={raw_h}", normalized <= raw_h)

# Conditional arithmetic of the recorded inputs. This does not derive either input.
check("T1 = (1/4) E_eta and E_eta = -2 G give -1/2 G", Fraction(1, 4) * Fraction(-2) == Fraction(-1, 2))

print("RESULT J2-NONLINEAR-DEGREE-LE2-VANISHES-IN-NORMAL-COORDINATES")
print("RESULT J2-IR-POSTQUADRATIC-REMAINDER-O-H")
