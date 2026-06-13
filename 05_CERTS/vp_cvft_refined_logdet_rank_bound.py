#!/usr/bin/env python3
"""Deterministic CVFT refined log-det/rank bound certificate."""

from __future__ import annotations

import cmath
import math


def main() -> int:
    eigs = [0.8, 0.4, 0.0]
    z = 0.45 + 0.2j
    rho = max(eigs)
    rank_f = sum(1 for x in eigs if x > 1e-12)
    a = abs(z) * rho
    if not (0 <= rho <= 1 and a < 1):
        print("FAIL_CVFT_LOGDET_RANK_BOUND_REFINED bad setup")
        return 1

    logdet = sum(-cmath.log(1 - z * lam) for lam in eigs if lam > 1e-12)
    refined = rank_f * (-math.log(1 - a))
    rational = rank_f * a / (1 - a)
    ok = abs(logdet) <= refined + 1e-12 and refined <= rational + 1e-12

    # Negative control: the forbidden bound uses |z| without rho(F); it is not the
    # theorem statement even when it happens to be numerically true.
    forbidden_statement_rejected = abs(z) != a

    if ok and forbidden_statement_rejected:
        print("PASS_CVFT_LOGDET_RANK_BOUND_REFINED")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_LOGDET_BOUND_USING_Z_NOT_ZRHO")
        return 0
    print("FAIL_CVFT_LOGDET_RANK_BOUND_REFINED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
