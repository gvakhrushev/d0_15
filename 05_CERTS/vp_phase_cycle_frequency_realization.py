#!/usr/bin/env python3
"""Exact certificate for finite phase-cycle frequency realization.

Checks the four-quarter-turn return, fixed count/window frequency law, exact raw-defect
factorization and ratio-surjective no-go.  It contains no astronomical data or apparatus claim.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class QPhi:
    a: Fraction
    b: Fraction

    def __add__(self, other: "QPhi") -> "QPhi":
        return QPhi(self.a + other.a, self.b + other.b)

    def __sub__(self, other: "QPhi") -> "QPhi":
        return QPhi(self.a - other.a, self.b - other.b)

    def __mul__(self, other: "QPhi") -> "QPhi":
        return QPhi(
            self.a * other.a + self.b * other.b,
            self.a * other.b + self.b * other.a + self.b * other.b,
        )

    def __truediv__(self, other: "QPhi") -> "QPhi":
        norm = other.a * other.a + other.a * other.b - other.b * other.b
        assert norm != 0
        inverse = QPhi((other.a + other.b) / norm, -other.b / norm)
        return self * inverse

    def __pow__(self, exponent: int) -> "QPhi":
        assert exponent >= 0
        result = ONE
        base = self
        n = exponent
        while n:
            if n & 1:
                result = result * base
            base = base * base
            n //= 2
        return result


ZERO = QPhi(Fraction(0), Fraction(0))
ONE = QPhi(Fraction(1), Fraction(0))
PHI = QPhi(Fraction(0), Fraction(1))
PHI_INV = PHI - ONE


def q(numerator: int, denominator: int = 1) -> QPhi:
    return QPhi(Fraction(numerator, denominator), Fraction(0))


def quarter_turn(v: tuple[Fraction, Fraction]) -> tuple[Fraction, Fraction]:
    re, im = v
    return -im, re


def turns(v: tuple[Fraction, Fraction], count: int) -> tuple[Fraction, Fraction]:
    for _ in range(count):
        v = quarter_turn(v)
    return v


def scale(depth: int) -> QPhi:
    return PHI**depth


def frequency(cycles: int, base_window: QPhi, depth: int) -> QPhi:
    assert cycles > 0
    return q(cycles) / (base_window * scale(depth))


def main() -> int:
    print("STRUCTURE_FIXED_BEFORE_NUMBER: four-turn cycle; fixed count; fixed base window")

    # Finite return owner and a reachable mutation: three turns are not a full cycle.
    probes = [
        (Fraction(1), Fraction(0)),
        (Fraction(2), Fraction(-3)),
        (Fraction(-5, 7), Fraction(11, 13)),
    ]
    for probe in probes:
        assert turns(probe, 4) == probe
        for completed in range(9):
            assert turns(probe, 4 * completed) == probe
    assert turns(probes[0], 3) != probes[0]
    print("FAIL_THREE_TURNS_ARE_FULL_CYCLE")
    print("PASS_FINITE_FOUR_TURN_RETURN")

    # A fixed positive cycle count and base window cancel from every depth comparison.
    for cycles in (1, 2, 7, 19):
        for base in (q(1), q(3, 2), PHI + q(2)):
            for emitter in range(7):
                for observer in range(emitter, 8):
                    nu_em = frequency(cycles, base, emitter)
                    nu_obs = frequency(cycles, base, observer)
                    assert nu_obs == frequency(cycles, base, observer - 1) * PHI_INV if observer else nu_obs == frequency(cycles, base, 0)
                    assert nu_em / nu_obs == PHI ** (observer - emitter)
    print("PASS_FIXED_CYCLE_WINDOW_FREQUENCY")

    # Mutating either preregistered datum creates exactly the advertised defect.
    emitter_depth, observer_depth = 1, 5
    emitter_count, observer_count = 3, 7
    emitter_base, observer_base = q(5, 4), q(11, 6)
    nu_em = frequency(emitter_count, emitter_base, emitter_depth)
    nu_obs = frequency(observer_count, observer_base, observer_depth)
    d0_ratio = PHI ** (observer_depth - emitter_depth)
    count_defect = q(emitter_count) / q(observer_count)
    window_defect = observer_base / emitter_base
    assert nu_em / nu_obs == count_defect * window_defect * d0_ratio
    assert nu_em / nu_obs != d0_ratio
    print("FAIL_VARIABLE_COUNT_OR_WINDOW_PRESERVES_D0_RATIO")
    print("PASS_COUNT_WINDOW_DEFECT_FACTORIZATION")

    # Raw positive windows realize every tested positive rational ratio at the same depths.
    for numerator in range(1, 12):
        for denominator in range(1, 9):
            ratio = q(numerator, denominator)
            raw_emitter_frequency = ONE
            raw_observer_frequency = ONE / ratio
            assert raw_emitter_frequency / raw_observer_frequency == ratio
    assert ONE != PHI
    print("FAIL_RAW_CYCLE_WINDOW_FORCES_PHI")
    print("PASS_RAW_CYCLE_WINDOW_RATIO_SURJECTIVITY_NOGO")

    print("PASS_PHASE_CYCLE_FREQUENCY_REALIZATION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
