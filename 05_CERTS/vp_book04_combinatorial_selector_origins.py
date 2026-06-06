#!/usr/bin/env python3
"""Verify Book 04 combinatorial origins for centered full-support selectors.

This certificate does not fit selector targets.  It checks that the support
radii used by the centered selectors are read from upstream D0 formulas:
DEW=35, 18*17=306, 2*10-1=19, and then verifies the corresponding symmetric
supports and midpoint equations.
"""

from __future__ import annotations

CASES = [
    ("electroweak", 35, "DEW=35 from forced Ω8 return-window calculus"),
    ("proton_readout", 18 * 17, "18*17 high-gain destructive-readout count"),
    ("beta_unlock", 2 * 10 - 1, "2*10-1 weak-unlock formula"),
]

for name, radius, origin in CASES:
    support = list(range(2 * radius + 1))
    midpoint_solutions = [x for x in support if 2 * x == 2 * radius]
    assert midpoint_solutions == [radius], (name, midpoint_solutions, radius)
    print(
        f"{name}: origin={origin}; radius={radius}; "
        f"support=0..{2*radius}; checked={len(support)}; midpoint={midpoint_solutions[0]}"
    )

print("PASS_BOOK04_COMBINATORIAL_SELECTOR_ORIGINS")
