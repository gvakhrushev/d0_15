"""
D0 CORE CONSTANTS (single source of truth)

Contract:
- This module contains ONLY canonically-derived constants.
- No SI anchors, no dataset knobs, no "fits".
"""

from __future__ import annotations

import math

# --- Golden canon (BOOK I) ---
sqrt5: float = math.sqrt(5.0)
phi: float = (1.0 + sqrt5) / 2.0
psi: float = (1.0 - sqrt5) / 2.0  # = -1/phi

# δ0 = 1/(2 φ^3)  (matches your scripts and BOOK III convention)
delta0: float = 1.0 / (2.0 * (phi ** 3))

# ε = φ^-8 ; ε² = φ^-16  (CERT tolerance)
eps: float = phi ** (-8)
eps2: float = eps * eps

# ξ5 = φ^-5
xi5: float = phi ** (-5)

# --- Structural circle holonomy (BOOK III) ---
# π0 = (6/5)·φ^2   (structural; NOT transcendental π)
pi0: float = (6.0 / 5.0) * (phi ** 2)

# memory mass quantum
m0: float = 2.0 * pi0

# base period in D0-time units
tau0_D0: float = 1.0 / m0
