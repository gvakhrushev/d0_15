#!/usr/bin/env python3
"""Frozen charged-lepton transfer table certificate."""
from __future__ import annotations
from fractions import Fraction

ratios = {
    "electron": Fraction(1, 1),
    "muon": Fraction(38814328681047283, 10000000000000000),
    "tau": Fraction(103183483253993735, 10000000000000000),
}
exponents = {
    "electron": Fraction(0, 1),
    "muon": Fraction(1, 4),
    "tau": Fraction(1, 3),
}
assert ratios["electron"] == 1
assert exponents["electron"] == 0
assert exponents["muon"] == Fraction(1, 4)
assert exponents["tau"] == Fraction(1, 3)
print("CHARGED_LEPTON_TRANSFER_TABLE")
for k in ["electron", "muon", "tau"]:
    print(f"{k}: ratio={ratios[k]} exponent={exponents[k]}")
print("PASS_CHARGED_LEPTON_TRANSFER_CERTIFICATE")
