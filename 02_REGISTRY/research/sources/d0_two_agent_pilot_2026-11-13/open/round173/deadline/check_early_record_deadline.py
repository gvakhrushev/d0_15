"""Rational enclosures for the native A83 and A80 early-record bounds."""

from dataclasses import dataclass
from fractions import Fraction
from math import isqrt


SCALE = 10**75


@dataclass(frozen=True)
class Interval:
    """Closed interval with endpoints in SCALE^{-1} Z."""

    lower: int
    upper: int

    def __sub__(self, other):
        return Interval(self.lower - other.upper, self.upper - other.lower)

    def __mul__(self, other):
        products = (
            self.lower * other.lower,
            self.lower * other.upper,
            self.upper * other.lower,
            self.upper * other.upper,
        )
        return Interval(min(products) // SCALE, -(-max(products) // SCALE))

    def square(self):
        products = (self.lower**2, self.upper**2)
        lower = 0 if self.lower <= 0 <= self.upper else min(products)
        return Interval(lower // SCALE, -(-max(products) // SCALE))

    def sqrt(self):
        if self.lower < 0:
            raise ValueError("square root of an interval with a negative endpoint")
        return Interval(
            isqrt(self.lower * SCALE),
            isqrt(self.upper * SCALE) + 1,
        )

    def strictly_between(self, low, high):
        return (
            Fraction(self.lower, SCALE) > Fraction(low)
            and Fraction(self.upper, SCALE) < Fraction(high)
        )

    def display(self):
        return f"{(self.lower + self.upper) / (2 * SCALE):.12f}"


def const(a, b=1):
    quotient, remainder = divmod(a * SCALE, b)
    return Interval(quotient, quotient + bool(remainder))


def require(condition, label):
    if not condition:
        raise ValueError(label)


def golden_power(p, exponent):
    value = const(1)
    for _ in range(exponent):
        value = value * p
    return value


def detector_eta(p_cubed, exponent):
    """sin^2(2^exponent θ) from cos(2 θ) = p^3."""
    cosine = p_cubed
    for _ in range(exponent - 1):
        cosine = const(2) * cosine.square() - const(1)
    return const(1) - cosine.square()


def main():
    golden_floor = (isqrt(5 * SCALE**2) - SCALE) // 2
    p = Interval(golden_floor, golden_floor + 1)
    p_cubed = golden_power(p, 3)
    for length, exponent, eta_range, obstruction_range in (
        (24, 25, ("0.982170151702", "0.982170151704"), ("0.00866", "0.00867")),
        (36, 39, ("0.986049140797", "0.986049140799"), ("0.00677", "0.00679")),
    ):
        eta = detector_eta(p_cubed, exponent)
        obstruction = (const(1) - eta) * p_cubed.sqrt()
        require(eta.strictly_between(*eta_range), f"A83 L={length}: native eta")
        require(
            obstruction.strictly_between(*obstruction_range),
            f"A83 L={length}: first retained digit obstruction",
        )
        print(f"A83 L={length}: eta={eta.display()} trace_bound={obstruction.display()}")

    eta = detector_eta(p_cubed, 4)
    require(eta.strictly_between("0.891448779058", "0.891448779060"), "A80 eta")
    for active, return_range in (
        (2, ("0.4443", "0.4444")),
        (3, ("0.4456", "0.4457")),
    ):
        c = golden_power(p, 3 * active)
        one_minus_c_squared = const(1) - c.square()
        commutator = const(1, 2) * one_minus_c_squared.sqrt()
        defect = const(1, 2) * eta * one_minus_c_squared
        require(commutator.strictly_between("0.4992", "0.5"), "A80 commutator")
        require(defect.strictly_between(*return_range), "A80 late report probability")
        print(
            f"A80 s={active}: eta={eta.display()} commutator={commutator.display()} "
            f"return_defect={defect.display()}"
        )


if __name__ == "__main__":
    main()
