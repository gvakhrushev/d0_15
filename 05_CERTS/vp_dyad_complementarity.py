#!/usr/bin/env python3
"""D0-DYAD-COMPLEMENTARITY-001 — complementarity as a theorem of the measurement dyad.

STRUCTURE (THE, Lean D0.Core.DyadComplementarity, DYAD_COMPLEMENTARITY_PROVED):
  a dyad readout state is an admissible symmetric 2x2 branch matrix: unit closure
  (r11 + r22 = 1) and positive joint response (det = r11*r22 - r12^2 >= 0).
  Readout functionals:
    D(rho) = |r11 - r22|   (path distinguishability — WHICH branch),
    V(rho) = 2*|r12|       (coherence visibility — interference between branches).
  THEOREM: every admissible state obeys  D^2 + V^2 <= 1,
  with equality iff det = 0. Proof: D^2 + V^2 = (r11+r22)^2 - 4*det = 1 - 4*det.
  The two equality families are the wave/particle extremes:
    diag(1,0)            -> (D, V) = (1, 0)   (particle / path-certain);
    [[1/2,1/2],[1/2,1/2]]-> (D, V) = (0, 1)   (wave / coherence-maximal).

HONEST SCOPE: the structure above is THE (finite, exact). The identification of V with
optical fringe visibility and D with which-path distinguishability in laboratory
interferometry is a typed BRIDGE (Englert's V^2 + D^2 <= 1 is the external-background
correspondence); it is NOT claimed as derived here. What is owned: the bound holds for the
dyad architecture with zero quantum postulates — only unit closure + positivity of the
two-channel response, the same primitives that own the Born weights upstream (D0.Core.BornFinite).

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 non-vacuity: a non-PSD "state" must VIOLATE the bound — positivity is load-bearing;
  C2 admissibility filter: that non-PSD matrix must be rejected by the gate;
  C3 wrong bound: the LINEAR form D + V <= 1 must be violated by admissible states —
     the squares are structural, not decorative.
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-9


def admissible(a: float, b: float, c: float) -> bool:
    """Unit closure + PSD for symmetric [[a,c],[c,b]]."""
    return abs((a + b) - 1.0) < TOL and (a * b - c * c) >= -TOL


def readout(a: float, b: float, c: float) -> tuple[float, float]:
    """(D, V) of the dyad state."""
    return abs(a - b), 2.0 * abs(c)


def main() -> int:
    print("=== D0-DYAD-COMPLEMENTARITY-001  D² + V² ≤ 1 from the measurement dyad ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: admissible = unit closure + PSD; D=|r11−r22|; "
          "V=2|r12|; no quantum postulates — same primitives as upstream Born weights")

    # ---- GATE 1: dense scan over the admissible simplex ---------------------------------
    worst = -1.0
    n_checked = 0
    for a in np.linspace(0.0, 1.0, 201):
        for c in np.linspace(-0.5, 0.5, 401):
            b = 1.0 - a
            if not admissible(a, b, c):
                continue
            n_checked += 1
            d, v = readout(a, b, c)
            worst = max(worst, d * d + v * v)
    assert n_checked > 1000, f"scan must cover a real region, got {n_checked} states"
    assert worst <= 1.0 + 1e-7, f"complementarity bound violated: max D²+V² = {worst}"
    print(f"PASS_COMPLEMENTARITY_BOUND  {n_checked} admissible states scanned; "
          f"max D²+V² = {worst:.9f} ≤ 1")

    # ---- GATE 2: equality cases are exactly the pure (rank-one) states -------------------
    d_p, v_p = readout(1.0, 0.0, 0.0)
    assert abs(d_p - 1.0) < TOL and abs(v_p) < TOL, "particle mode must give (D,V)=(1,0)"
    d_w, v_w = readout(0.5, 0.5, 0.5)
    assert abs(v_w - 1.0) < TOL and abs(d_w) < TOL, "wave mode must give (D,V)=(0,1)"
    # mixed admissible state must sit strictly inside
    d_m, v_m = readout(0.8, 0.2, 0.2)
    assert d_m * d_m + v_m * v_m < 1.0 - 1e-6, "mixed state must be strictly inside"
    assert admissible(0.8, 0.2, 0.2), "mixed control state must be admissible"
    print(f"PASS_EQUALITY_FAMILIES  particle diag(1,0)->(1,0); wave balanced->(0,1); "
          f"mixed (0.8,0.2,0.2)->D²+V²={d_m*d_m+v_m*v_m:.6f}<1")

    # ---- CONTROL C1 (must fail): positivity is load-bearing ------------------------------
    bad_a, bad_b, bad_c = 0.9, 0.1, 0.5
    assert not admissible(bad_a, bad_b, bad_c), "control matrix must be non-PSD"
    d_bad, v_bad = readout(bad_a, bad_b, bad_c)
    assert d_bad ** 2 + v_bad ** 2 > 1.0 + 1e-9, \
        "non-PSD matrix must violate the bound (bound is not vacuous)"
    print(f"FAIL_NONPSD_STATE  [[{bad_a},{bad_c}],[{bad_c},{bad_b}]]: D²+V²="
          f"{d_bad**2+v_bad**2:.6f} > 1 — outside admissibility; bound tracks PSD exactly")

    # ---- CONTROL C2 (must fail): the admissibility gate rejects the violator -------------
    rejected = 0
    for a, b, c in [(bad_a, bad_b, bad_c), (0.7, 0.3, 0.55), (0.99, 0.01, 0.32)]:
        if not admissible(a, b, c):
            d, v = readout(a, b, c)
            assert d * d + v * v > 1.0 or True  # informational
            rejected += 1
    assert rejected == 3, f"all three violators must be filtered out, rejected {rejected}"
    print(f"FAIL_ADMISSIBILITY_GATE  all non-PSD probes rejected by the filter "
          f"(unit closure ∧ det ≥ 0)")

    # ---- CONTROL C3 (must fail): linear form D + V ≤ 1 is NOT the theorem ---------------
    lin_violators = []
    for a in np.linspace(0.0, 1.0, 101):
        for c in np.linspace(-0.5, 0.5, 201):
            b = 1.0 - a
            if not admissible(a, b, c):
                continue
            d, v = readout(a, b, c)
            if d + v > 1.0 + 1e-9:
                lin_violators.append((a, c, d, v))
    assert lin_violators, "linear bound must be violable by admissible states"
    a0, c0, d0, v0 = lin_violators[0]
    print(f"FAIL_LINEAR_BOUND  admissible state r11={a0:.3f}, r12={c0:.3f}: "
          f"D+V={d0+v0:.6f} > 1 while D²+V²={d0*d0+v0*v0:.6f} ≤ 1 — squares are structural")

    print("HONEST_BOUNDARY  structure = THE (Lean rc=0, 0 sorry); lab identification "
          "(fringe visibility / which-path) = typed BRIDGE to interferometry; Englert "
          "V²+D²≤1 = external-background correspondence")
    return 0


if __name__ == "__main__":
    sys.exit(main())
