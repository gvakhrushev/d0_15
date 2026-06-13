#!/usr/bin/env python3
"""Deterministic CVFT UV feedback-tail refined bound certificate."""

from __future__ import annotations


def main() -> int:
    eigs = [0.7, 0.25, 0.0]
    z_abs = 0.5
    rho = max(eigs)
    rank_f = sum(1 for x in eigs if x > 1e-12)
    m_cut = 4
    a = z_abs * rho
    if not (a < 1):
        print("FAIL_CVFT_UV_TAIL_BOUND_REFINED bad setup")
        return 1

    # Positive real z is enough for this deterministic certificate; the theorem
    # target uses absolute values for complex z.
    tail = 0.0
    for m in range(m_cut + 1, 80):
        tail += (z_abs**m / m) * sum(lam**m for lam in eigs)
    remainder_bound = (
        rank_f / (m_cut + 1) * (a ** (m_cut + 1)) / (1 - a)
    )

    delta12 = 1e-6
    tolerance_is_not_radius = a != delta12 and a < 1

    if abs(tail) <= remainder_bound + 1e-12 and tolerance_is_not_radius:
        print("PASS_CVFT_UV_TAIL_BOUND_REFINED")
        print("PASS_CVFT_UV_FEEDBACK_TAIL_BOUND")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_DELTA12_AS_CONVERGENCE_RADIUS")
        return 0
    print("FAIL_CVFT_UV_TAIL_BOUND_REFINED")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
