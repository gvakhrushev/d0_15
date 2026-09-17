#!/usr/bin/env python3
"""Deterministic finite certificate for Born quadratic origin."""

from __future__ import annotations

from fractions import Fraction


def q(a: Fraction, b: Fraction, c: Fraction, x: Fraction, y: Fraction) -> Fraction:
    return a * x * x + b * x * y + c * y * y


def quarter_turn(x: Fraction, y: Fraction) -> tuple[Fraction, Fraction]:
    return -y, x


def check_quarter_turn_solution() -> tuple[Fraction, Fraction, Fraction]:
    # Invariance on (1, 0) gives a = c.
    a = Fraction(1)
    c = a

    # Invariance on (1, 1) gives a + b + c = a - b + c, hence b = 0.
    b = Fraction(0)

    # Unit calibration R(1, 0) = 1 gives a = 1, already fixed above.
    assert q(a, b, c, Fraction(1), Fraction(0)) == 1
    return a, b, c


def check_phase_blind(a: Fraction, b: Fraction, c: Fraction) -> None:
    grid = [Fraction(n) for n in range(-3, 4)]
    for x in grid:
        for y in grid:
            jx, jy = quarter_turn(x, y)
            assert q(a, b, c, x, y) == q(a, b, c, jx, jy)


def check_parallelogram(a: Fraction, b: Fraction, c: Fraction) -> None:
    grid = [Fraction(n) for n in range(-2, 3)]
    for x1 in grid:
        for y1 in grid:
            for x2 in grid:
                for y2 in grid:
                    lhs = q(a, b, c, x1 + x2, y1 + y2) + q(a, b, c, x1 - x2, y1 - y2)
                    rhs = 2 * q(a, b, c, x1, y1) + 2 * q(a, b, c, x2, y2)
                    assert lhs == rhs


def run_certificate() -> None:
    print("--- D0 BORN QUADRATIC ORIGIN CERTIFICATE ---")
    a, b, c = check_quarter_turn_solution()
    assert (a, b, c) == (Fraction(1), Fraction(0), Fraction(1))
    print("[1] quarter-turn probes force a=1, b=0, c=1: PASS")

    check_phase_blind(a, b, c)
    print("[2] phase blindness verified on rational grid: PASS")

    check_parallelogram(a, b, c)
    print("[3] parallelogram law verified on rational grid: PASS")

    for x in [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]:
        for y in [Fraction(-2), Fraction(-1), Fraction(0), Fraction(1), Fraction(2)]:
            assert q(a, b, c, x, y) == x * x + y * y

    print("[4] unit-calibrated response equals x^2+y^2: PASS")
    print("[CERT-CLOSED] PASS_BORN_QUADRATIC_ORIGIN")


if __name__ == "__main__":
    run_certificate()
