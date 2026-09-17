#!/usr/bin/env python3
"""Certificate for the internal self-unfolding observable-elimination laws."""

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class QPhi:
    """Exact element a + b*phi with phi^2 = phi + 1."""

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

    def __pow__(self, exponent: int) -> "QPhi":
        assert exponent >= 0
        result = ONE
        base = self
        power = exponent
        while power:
            if power & 1:
                result = result * base
            base = base * base
            power //= 2
        return result


ZERO = QPhi(Fraction(0), Fraction(0))
ONE = QPhi(Fraction(1), Fraction(0))
PHI = QPhi(Fraction(0), Fraction(1))
PHI_INV = PHI - ONE


def one_plus_redshift(observer_depth: int, emitter_depth: int) -> QPhi:
    assert emitter_depth <= observer_depth
    return PHI ** (observer_depth - emitter_depth)


def redshift(observer_depth: int, emitter_depth: int) -> QPhi:
    return one_plus_redshift(observer_depth, emitter_depth) - ONE


def archive_growth(depth: int) -> QPhi:
    return PHI**depth - ONE


def main() -> int:
    print(
        "STRUCTURE_FIXED_BEFORE_NUMBER: one refinement index feeds the registered time, "
        "depth-comparison, scale, and relative-archive readouts."
    )

    # Exact cocycle for every tested composable triple; the Lean theorem is universal.
    for emitter in range(9):
        for middle in range(emitter, 9):
            for observer in range(middle, 9):
                assert one_plus_redshift(observer, emitter) == (
                    one_plus_redshift(observer, middle)
                    * one_plus_redshift(middle, emitter)
                )
    print("PASS_RELATIVE_DEPTH_COCYCLE: transport depends only on composable depth differences")

    for emitter in range(8):
        for observer in range(emitter, 8):
            z = redshift(observer, emitter)
            drift = redshift(observer + 1, emitter) - z
            assert one_plus_redshift(observer + 1, emitter) == PHI * (ONE + z)
            assert drift == (PHI - ONE) * (ONE + z)
    print("PASS_REDSHIFT_DRIFT_ELIMINATION: delta-z=(phi-1)(1+z) with no free drift law")

    for depth in range(9):
        scale_increment = PHI ** (depth + 1) - PHI**depth
        archive_increment = archive_growth(depth + 1) - archive_growth(depth)
        origin_drift = redshift(depth + 1, 0) - redshift(depth, 0)
        assert redshift(depth, 0) == archive_growth(depth)
        assert origin_drift == scale_increment == archive_increment
    print("PASS_SHARED_INCREMENT: origin drift, metric-scale increment, and archive growth coincide")

    for depth in range(9):
        dynamic_visible = PHI_INV**depth
        dynamic_archive = ONE - dynamic_visible
        z = redshift(depth, 0)
        assert dynamic_visible + dynamic_archive == ONE
        # Division-free certificate of darkDynamic = z/(1+z).
        assert dynamic_archive * (ONE + z) == z
    first_dynamic_archive = ONE - PHI_INV
    static_dimension_share = QPhi(Fraction(10, 11), Fraction(0))
    assert first_dynamic_archive == PHI_INV * PHI_INV == QPhi(Fraction(2), Fraction(-1))
    assert first_dynamic_archive != static_dimension_share
    print(
        "PASS_DYNAMIC_MEASURE_RELATION: darkDynamic=z/(1+z), while first-step golden share "
        "differs from static 10/11 dimension share"
    )

    assert PHI * PHI_INV == ONE
    for depth in range(9):
        active_now = PHI_INV**depth
        active_next = PHI_INV ** (depth + 1)
        assert active_next == active_now * PHI_INV
        assert one_plus_redshift(depth + 1, 0) == PHI * one_plus_redshift(depth, 0)
    print("PASS_TICK_EXPANSION_RECIPROCITY: time retention and depth expansion use inverse generators")

    # Mutation controls: an integer-tick coordinate is monotone but does not satisfy the phi law,
    # and a free multiplier different from phi already fails at the zeroth comparison.
    integer_z0 = QPhi(Fraction(0), Fraction(0))
    integer_z1 = QPhi(Fraction(1), Fraction(0))
    assert integer_z1 - integer_z0 != (PHI - ONE) * (ONE + integer_z0)
    wrong_generator = QPhi(Fraction(2), Fraction(0))
    assert one_plus_redshift(1, 0) != wrong_generator * one_plus_redshift(0, 0)
    print("FAIL_MUTATION_CONTROLS: integer coordinate and free multiplier violate the shared law")

    print("PASS_SELF_UNFOLDING_OBSERVABLE_RELATIONS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
