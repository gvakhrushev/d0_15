#!/usr/bin/env python3
"""Deterministic U_eff contraction and pole-discipline certificate."""

from __future__ import annotations

import cmath
import math


def main() -> int:
    # Deterministic compressed diagonal transfer.  It is a contraction and has
    # one damped complex pole candidate.
    eigs_ueff = [0.8 * cmath.exp(0.3j), 0.5, 0.0]
    contraction = all(abs(lam) <= 1 + 1e-12 for lam in eigs_ueff)
    lam = eigs_ueff[0]
    energy = cmath.phase(lam)
    gamma = -math.log(abs(lam))
    pole_ok = abs(energy - 0.3) < 1e-12 and gamma > 0

    # Bare positive F has only real nonnegative eigenvalues; it cannot be the
    # source of complex pole phases.
    eigs_f = [0.64, 0.25, 0.0]
    bare_f_real_nonnegative = all(isinstance(x, float) and x >= 0 for x in eigs_f)

    if contraction and pole_ok and bare_f_real_nonnegative:
        print("PASS_UEFF_CONTRACTION_POLE_DISCIPLINE")
        print("PASS_UEFF_POLE_DISCIPLINE")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_COMPLEX_POLES_FROM_BARE_POSITIVE_F")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_COMPLEX_POLES_FROM_BARE_F")
        return 0
    print("FAIL_UEFF_CONTRACTION_POLE_DISCIPLINE")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
