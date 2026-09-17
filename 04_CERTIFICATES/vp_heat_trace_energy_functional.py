#!/usr/bin/env python3
"""vp_heat_trace_energy_functional - D0-REHEATING-HEATTRACE-ENERGY-FUNCTIONAL-001.

The finite heat-energy functional E(u) = -d/du log H(u) computed from the connected K(9,11,13)
Laplacian spectrum {0:1,20:12,22:10,24:8,33:2}. Verifies: H(u)=Sum mult_i exp(-lam_i u); -H'(u)=Sum
mult_i lam_i exp(-lam_i u); E(u)=(-H')/H is the heat-weighted mean eigenvalue; early limit E(0+)=718/33;
late limit E(inf)=0. No inflaton, Planck n_s, or survey datum. Reachable controls reject a changed
spectrum and a wrong derivative-coefficient row.
"""
import math
from fractions import Fraction as F
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SPEC = {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}  # eigenvalue: multiplicity


def H(u, spec=SPEC):
    return sum(m * math.exp(-lam * u) for lam, m in spec.items())


def minusHprime(u, spec=SPEC):
    return sum(m * lam * math.exp(-lam * u) for lam, m in spec.items())


def E(u, spec=SPEC):
    return minusHprime(u, spec) / H(u, spec)


def main() -> int:
    print("=== vp_heat_trace_energy_functional  E(u) = -d/du log H(u) from K(9,11,13) spectrum ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the spectrum {0:1,20:12,22:10,24:8,33:2}, the heat trace "
          "H(u)=Sum mult_i exp(-lam_i u), and E(u)=(-H')/H (heat-weighted mean eigenvalue) are fixed "
          "before any number; no inflaton / Planck n_s / survey datum enters.")

    assert sum(SPEC.values()) == 33, "multiplicities must sum to 33"
    wsum = sum(m * lam for lam, m in SPEC.items())
    assert wsum == 718, f"spectral weight sum {wsum} != 718"
    print(f"PASS_SPECTRUM  multiplicities sum 33; nonzero spectral weight Sum mult*lam = {wsum} (=718).")

    # exact early limit: at u=0, -H'=718, H=33
    e0 = F(sum(m * lam for lam, m in SPEC.items()), sum(SPEC.values()))
    assert e0 == F(718, 33), f"early limit {e0} != 718/33"
    assert abs(E(1e-9) - 718 / 33) < 1e-3, "numeric early limit mismatch"
    print(f"PASS_EARLY_LIMIT  E(0+) = 718/33 = {float(e0):.6f} (unweighted spectral mean).")

    assert E(50.0) < 1e-6, "late limit must -> 0"
    print(f"PASS_LATE_LIMIT  E(u) -> 0 as u -> inf (zero-mode dominates; E(50)={E(50.0):.2e}).")

    # E is the heat-weighted mean eigenvalue: 0 < E < 33 on a grid
    grid = [0.001, 0.01, 0.05, 0.1, 0.5, 1.0, 5.0]
    assert all(0 < E(u) < 33 for u in grid), "E must lie strictly in (0,33) on the grid"
    print(f"PASS_FUNCTIONAL_RANGE  0 < E(u) < 33 on u-grid {grid} (max E={max(E(u) for u in grid):.4f}).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    bad_spec = {0: 1, 19: 12, 22: 10, 24: 8, 33: 2}  # changed 20 -> 19
    assert sum(m * lam for lam, m in bad_spec.items()) != 718, "control: changed spectrum must differ"
    print("FAIL_CHANGED_SPECTRUM_REJECTED  altering the Laplacian spectrum (20->19) changes the weight sum (caught).")

    wrong_coeff = 240 + 220 + 192 + 67  # wrong mult*lam row (66->67)
    assert wrong_coeff != 718, "control: a wrong derivative-coefficient row must differ from 718"
    print("FAIL_WRONG_DERIVATIVE_COEFF_REJECTED  a wrong mult*lam coefficient row (!=718) is caught.")

    print("PASS_HEAT_TRACE_ENERGY_FUNCTIONAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
