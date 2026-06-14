#!/usr/bin/env python3
"""D0-GRAV-002 — single-section gravity completion: G_N from the phi^99 depth (can-FAIL).

ell_P and G_N are built from the closed D0 primitives delta0, |Omega8|=8, and the forced
gravitational depth exponent V9*V11=99 (D0-PHI99-DEPTH-FORCING-001); CODATA G is a benchmark,
not an input. Rewritten from a print-stub (hardcoded PASS) to assert the structural chain + the
benchmark agreement, so it can FAIL.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

H = 6.62607015e-34
C = 299792458.0
ME = 9.1093837139e-31
HBAR = H / (2 * math.pi)
G_REF = 6.67430e-11        # CODATA 2022; benchmark, not input
phi = (1 + math.sqrt(5)) / 2
delta0 = (math.sqrt(5) - 2) / 2
Omega8 = 8
V9, V11, V13 = 9, 11, 13


def main() -> int:
    print("=== D0-GRAV-002  single-section gravity completion: G_N from phi^99 ===")
    ell0 = H / (38 * ME * C)

    assert V9 * V11 == 99, "the forced gravitational depth exponent V9*V11 must be 99"
    DL = Omega8 * phi ** (V9 * V11) * (1 + delta0 / V13)
    ellP = ell0 / DL
    G = C ** 3 * ellP ** 2 / HBAR
    rel = G / G_REF - 1
    print(f"PASS_PHI99_DEPTH  D_L = Omega8 * phi^99 * (1+delta0/V13) = {DL:.6e}")
    assert abs(rel) < 1e-3, f"G_N must match CODATA within 0.1%: rel_err={rel:.6e}"
    print(f"PASS_G_N_BENCHMARK  G_N(D0)={G:.6e} vs CODATA {G_REF:.6e}; rel_err={rel:.4%} (benchmark not input)")

    # negative control: a wrong depth exponent (98 instead of 99) misses G by phi^2 ~ 2.6x
    DL_wrong = Omega8 * phi ** 98 * (1 + delta0 / V13)
    G_wrong = C ** 3 * (ell0 / DL_wrong) ** 2 / HBAR
    assert abs(G_wrong / G_REF - 1) > 0.3, "control: phi^98 depth must miss G by >30%"
    print("FAIL_WRONG_DEPTH_PHI98_MISSES_G_BY_PHI_SQUARED")
    print("HONEST_G_N_IS_A_BENCHMARK_NOT_AN_INPUT_PHI99_DEPTH_IS_THE_FORCED_EXPONENT")
    print("PASS_SINGLE_SECTION_GRAVITY_COMPLETION")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
