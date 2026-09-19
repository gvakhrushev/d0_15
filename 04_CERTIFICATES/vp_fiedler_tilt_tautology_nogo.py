#!/usr/bin/env python3
"""D0-FIEDLER-TILT-TAUTOLOGY-NOGO-001 exact arithmetic certificate."""

from fractions import Fraction


def tilt(q: Fraction, lam: Fraction) -> Fraction:
    return -2 * q / (q + lam)


def main() -> int:
    # Universal matched-scale identity on representative nonzero rationals.
    for lam in [Fraction(1), Fraction(2), Fraction(20), Fraction(-3, 2)]:
        assert lam != 0
        assert tilt(lam, lam) == -1

    # The D0 Fiedler mode does not select the evaluation scale.
    assert tilt(Fraction(20), Fraction(20)) == -1
    assert tilt(Fraction(40), Fraction(20)) == Fraction(-4, 3)
    assert tilt(Fraction(20), Fraction(20)) != tilt(Fraction(40), Fraction(20))

    # Negative control: changing lambda does not change the matched-scale answer.
    assert tilt(Fraction(7), Fraction(7)) == tilt(Fraction(20), Fraction(20)) == -1

    print("PASS_FIEDLER_TILT_TAUTOLOGY_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
