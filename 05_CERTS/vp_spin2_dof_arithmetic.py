#!/usr/bin/env python3
"""4D spin-2 two-polarization arithmetic certificate."""
from __future__ import annotations

d = 4
physical = d * (d - 3) // 2
symmetric = 10
removed = 8
assert physical == 2
assert symmetric - removed == 2
print("SPIN2_DOF_ARITHMETIC")
print(f"dimension={d}, massless_spin2_dof={physical}")
print(f"symmetric_components={symmetric}, removed={removed}, residual={symmetric-removed}")
print("PASS_SPIN2_DOF_ARITHMETIC")
