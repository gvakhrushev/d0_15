#!/usr/bin/env python3
"""Exact certificate for the preregistered physical-redshift detection passport.

The certificate checks the algebra in Q(phi), validates the frozen protocol schema, and exercises
negative controls.  It does not compare D0 with astronomical data and does not call a raw detector
number a frequency.  Its subject is the conditional, falsifiable bridge:

    positive frequency readout + one fixed self-return-covariant protocol
        => nu_em / nu_obs = phi^(observer_depth-emitter_depth).

Raw positive double readout remains ratio-surjective; a non-D0 ratio is carried by an explicit
relative-calibration defect rather than hidden in a fitted redshift law.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class QPhi:
    """Exact a + b*phi arithmetic with phi^2 = phi + 1."""

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
        return self * other.inverse()

    def __pow__(self, exponent: int) -> "QPhi":
        assert exponent >= 0
        out = ONE
        base = self
        power = exponent
        while power:
            if power & 1:
                out = out * base
            base = base * base
            power //= 2
        return out

    def inverse(self) -> "QPhi":
        # Norm(a+b*phi) = (a+b*phi)(a+b-b*phi) = a^2+a*b-b^2.
        norm = self.a * self.a + self.a * self.b - self.b * self.b
        assert norm != 0
        return QPhi((self.a + self.b) / norm, -self.b / norm)


ZERO = QPhi(Fraction(0), Fraction(0))
ONE = QPhi(Fraction(1), Fraction(0))
PHI = QPhi(Fraction(0), Fraction(1))
PHI_INV = PHI - ONE


def q(value: int, denominator: int = 1) -> QPhi:
    return QPhi(Fraction(value, denominator), Fraction(0))


def ladder(depth: int) -> QPhi:
    return PHI_INV**depth


def frequency(calibration: QPhi, depth: int) -> QPhi:
    return calibration * ladder(depth)


def validate_preregistered_schema(model: dict) -> list[str]:
    reasons: list[str] = []
    required = {
        "protocol_version",
        "pre_registered_before_data",
        "readout",
        "tick_multiplier_source",
        "self_return_closure",
        "allowed_fit_parameters",
        "forbidden_fit_parameters",
    }
    for key in required:
        if key not in model:
            reasons.append(f"missing required key: {key}")
    if model.get("pre_registered_before_data") is not True:
        reasons.append("protocol must be preregistered before data")
    if model.get("readout") != "frequency_ratio_nu_em_over_nu_obs":
        reasons.append("readout must be the frozen emitted/observed frequency ratio")
    if model.get("tick_multiplier_source") != "self_return_p_plus_p_squared_eq_1":
        reasons.append("tick multiplier must come from self-return closure")
    if model.get("self_return_closure") != "p+p^2=1; 0<p<1":
        reasons.append("positive contracting root domain is missing")
    forbidden = model.get("forbidden_fit_parameters", [])
    for token in ("tick_multiplier", "redshift_generator", "depth_gap"):
        if token not in forbidden:
            reasons.append(f"{token} must remain forbidden to fit")
    allowed = model.get("allowed_fit_parameters", [])
    if any(token not in ("absolute_frequency_normalization",) for token in allowed):
        reasons.append("only absolute frequency normalization may be calibrated")
    return reasons


def clean_model() -> dict:
    return {
        "protocol_version": "1.0",
        "pre_registered_before_data": True,
        "readout": "frequency_ratio_nu_em_over_nu_obs",
        "tick_multiplier_source": "self_return_p_plus_p_squared_eq_1",
        "self_return_closure": "p+p^2=1; 0<p<1",
        "allowed_fit_parameters": ["absolute_frequency_normalization"],
        "forbidden_fit_parameters": [
            "tick_multiplier",
            "redshift_generator",
            "depth_gap",
        ],
    }


def main() -> int:
    model = clean_model()
    assert validate_preregistered_schema(model) == []

    # Preregistration controls: post-hoc selection, a fitted generator, or a renamed observable fail.
    assert validate_preregistered_schema({**model, "pre_registered_before_data": False})
    assert validate_preregistered_schema(
        {**model, "allowed_fit_parameters": ["redshift_generator"]}
    )
    assert validate_preregistered_schema(
        {**model, "forbidden_fit_parameters": ["depth_gap"]}
    )
    assert validate_preregistered_schema({**model, "readout": "arbitrary_detector_number"})
    print("PASS_PREREGISTERED_PROTOCOL_SCHEMA")

    # The positive contracting self-return root is exact and rejects free multipliers.
    assert PHI_INV + PHI_INV * PHI_INV == ONE
    wrong_half = q(1, 2)
    assert wrong_half + wrong_half * wrong_half != ONE
    negative_other_root = ZERO - PHI
    assert negative_other_root + negative_other_root * negative_other_root == ONE
    # The second algebraic root satisfies the equation but violates the preregistered positivity.
    assert float(negative_other_root.a) + float(negative_other_root.b) * 1.618 < 0
    print("PASS_SELF_RETURN_MULTIPLIER_UNIQUENESS")

    # Absolute calibration cancels for multiple independently chosen positive normalizations.
    for calibration in (q(1), q(3, 2), q(7, 5), PHI + q(2)):
        for emitter in range(8):
            for observer in range(emitter, 9):
                nu_em = frequency(calibration, emitter)
                nu_obs = frequency(calibration, observer)
                one_plus_z = PHI ** (observer - emitter)
                assert nu_em / nu_obs == one_plus_z
                assert nu_obs * one_plus_z == nu_em
                assert frequency(calibration, observer + 1) == nu_obs * PHI_INV
    print("PASS_ABSOLUTE_CALIBRATION_CANCELLATION")

    # The physical drift is inherited from the same generator; no second drift parameter exists.
    calibration = q(11, 7)
    for emitter in range(7):
        for observer in range(emitter, 8):
            z0 = frequency(calibration, emitter) / frequency(calibration, observer) - ONE
            z1 = frequency(calibration, emitter) / frequency(calibration, observer + 1) - ONE
            assert z1 - z0 == (PHI - ONE) * (ONE + z0)
    print("PASS_PHYSICAL_REDSHIFT_DRIFT_TRANSFER")

    # Exact universal defect factorization: unequal calibrations are the whole rival freedom.
    for emitter_cal, observer_cal in ((q(3, 2), q(1)), (q(5, 4), q(7, 6))):
        emitter, observer = 1, 5
        nu_em = frequency(emitter_cal, emitter)
        nu_obs = frequency(observer_cal, observer)
        d0_ratio = PHI ** (observer - emitter)
        assert nu_em / nu_obs == (emitter_cal / observer_cal) * d0_ratio
        assert (nu_em / nu_obs == d0_ratio) == (emitter_cal == observer_cal)
    print("PASS_RELATIVE_CALIBRATION_DEFECT_FACTORIZATION")

    # Raw two-readout protocols can realise every positive rational ratio at depths 0 and 1.
    for numerator in range(1, 10):
        for denominator in range(1, 8):
            rival = q(numerator, denominator)
            raw_emitted, raw_observed = rival, ONE
            assert raw_emitted / raw_observed == rival
    assert ONE != PHI
    assert ONE / ONE != PHI  # constant raw readout is the decisive first-step mutation.
    print("PASS_RAW_DOUBLE_DETECTION_RATIO_SURJECTIVITY_NOGO")

    print("PASS_PHYSICAL_REDSHIFT_DETECTION_PASSPORT")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
