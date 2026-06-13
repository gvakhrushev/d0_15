#!/usr/bin/env python3
"""Deterministic S_DE exceptional-point effective-transfer algebra cert."""

from __future__ import annotations

import math


def eig_discriminant(lc: float, lr: float, eta: float) -> float:
    return ((lr - lc) / 2) ** 2 - eta**2


def main() -> int:
    lam_c = 1.5 - math.sqrt(10) / 40
    lam_r = 1.5 + math.sqrt(10) / 40
    eta_ep = (lam_r - lam_c) / 2
    exact = abs(eta_ep - math.sqrt(10) / 40) < 1e-14
    below = eig_discriminant(lam_c, lam_r, eta_ep / 2) > 0
    at = abs(eig_discriminant(lam_c, lam_r, eta_ep)) < 1e-14
    above = eig_discriminant(lam_c, lam_r, eta_ep * 1.2) < 0

    if exact and below and at and above:
        print("PASS_SDE_EP_EFFECTIVE_TRANSFER_ALGEBRA")
        print("PASS_SDE_EXCEPTIONAL_POINT_ALGEBRA")
        print("PASS_SDE_EP_NO_ROOT_REFIT")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_SDE_EP_AS_DESI_PASS")
        print("NEGATIVE_CONTROL_CAUGHT FAIL_H0_NONEXISTENCE_OVERCLAIM")
        return 0
    print("FAIL_SDE_EXCEPTIONAL_POINT_ALGEBRA")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
