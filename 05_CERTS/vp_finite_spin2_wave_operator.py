#!/usr/bin/env python3
"""Public v14 finite spin-2 wave-operator certificate name."""

from __future__ import annotations

from vp_finite_spin2_wave_operator_concrete import run_certificate


EXPECTED_TOKEN = "PASS_FINITE_SPIN2_WAVE_OPERATOR_CONCRETE"


if __name__ == "__main__":
    run_certificate()
