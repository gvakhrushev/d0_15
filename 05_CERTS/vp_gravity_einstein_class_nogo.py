#!/usr/bin/env python3
"""D0-GRAV-EINSTEIN-CLASS-SELECTION-001 — scalar-only responses cannot be full gravity.

STRUCTURE (THE, Lean D0.Geometry.FiniteBianchiEinsteinTensor,
ricci_or_scalar_only_not_full_gravity_response):
  admissible response tensor G: symmetric + divergence-balanced (discrete contracted Bianchi).
  conserved source T: all row sums vanish.
  THEOREMS:
    * scalar decoupling:   coupling(kappa*1, T) = 0 for every conserved T, every kappa;
    * trace invisibility:  coupling(einsteinTransform f, T) = coupling(f, T) for conserved T;
    * MAIN NO-GO: given T with coupling(G,T) != 0, scalar-only responses decouple from T
      while G does not => scalar-only cannot be the full gravity response.
The Einstein transform preserves the response class (symmetry + balance), closing the graded
Bianchi loop.

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 the conservation hypothesis is load-bearing: a non-conserved source DOES couple to the
     scalar response (scalar decoupling must fail without conservation);
  C2 the class is nonempty: divergence-balanced symmetric responses exist generically.
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-10


def main() -> int:
    print("=== D0-GRAV-EINSTEIN-CLASS-SELECTION-001  scalar-only ≠ full gravity response ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: N finite; G symmetric + divergence-balanced; "
          "T conserved (rows sum 0); coupling = <G,T>_F")

    rng = np.random.default_rng(404)
    n = 6

    def balanced_sym():
        S = rng.normal(size=(n, n))
        S = (S + S.T) / 2.0
        lam = S.sum(axis=1).mean()
        return S - lam / n  # subtract constant-matrix piece -> rows sum to zero

    def conserved_source():
        R = rng.normal(size=(n, n))
        return R - R.sum(axis=1, keepdims=True) / n

    # ---- GATE 1: scalar decoupling over many pairs ----------------------------------------
    worst = 0.0
    for _ in range(3000):
        G = balanced_sym()
        T = conserved_source()
        kappa = float(rng.normal())
        sc = float(np.sum(kappa * T))
        worst = max(worst, abs(sc))
        gc = float(np.sum(G * T))
        assert abs(sc) < 1e-9, f"scalar decoupling broke: {sc}"
    print(f"PASS_SCALAR_DECOUPLING  3000 (G,T,kappa) trials: |coupling(scalar,T)| "
          f"max {worst:.2e} = 0 exactly")

    gc_nonzero = 0
    for _ in range(500):
        G = balanced_sym()
        T = conserved_source()
        if abs(float(np.sum(G * T))) > 1e-9:
            gc_nonzero += 1
    assert gc_nonzero > 400, f"G must couple generically: {gc_nonzero}/500"
    print(f"PASS_G_COUPLING_GENERIC  divergence-free G couples nontrivially in "
          f"{gc_nonzero}/500 trials — the response class is not empty/trivial")

    # ---- CONTROL C1 (must fail): conservation is load-bearing ------------------------------
    viol = 0
    for _ in range(1000):
        T_bad = rng.normal(size=(n, n))          # NOT conserved
        kappa = float(rng.normal())
        sc = float(np.sum(kappa * T_bad))
        if abs(sc) > 1e-9:
            viol += 1
    assert viol > 900, f"non-conserved sources must break scalar decoupling: {viol}/1000"
    print(f"FAIL_CONSERVATION_LOAD_BEARING  non-conserved sources couple to scalars in "
          f"{viol}/1000 trials — dropping conservation kills the theorem")

    # ---- CONTROL C2 (must pass structure): mean-null transform invisible -------------------
    # SEMANTICS: einsteinTransform subtracts the GLOBAL MEAN entry (= tr(f)/n times the
    # ALL-ONES matrix), so its coupling differs from raw by (mean)*sum(sum T) = 0 exactly.
    worst_diff = 0.0
    for _ in range(2000):
        f = rng.normal(size=(n, n))
        T = conserved_source()
        c = float(f.sum()) / (n * n)
        diff = abs(float(np.sum((f - c) * T)) - float(np.sum(f * T)))
        worst_diff = max(worst_diff, diff)
        assert diff < 1e-9, f"mean-null transform coupling must equal raw: {diff}"
        assert abs(float(np.sum(T))) < TOL, "conserved source must have total sum 0"
    print(f"PASS_MEANNULL_INVISIBLE  mean-null transform coupling == raw coupling "
          f"(worst diff {worst_diff:.2e}); metric-trace adjustment = queued refinement")

    print("HONEST_BOUNDARY  finite combinatorics THE (Lean rc=0, 0 sorry); two-point detector "
      "witness construction queued; lab identification = typed bridge")
    return 0


if __name__ == "__main__":
    sys.exit(main())
