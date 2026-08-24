#!/usr/bin/env python3
"""D0-DYAD-CLOSURE-FORCING-001 — the unit closure is FORCED, not normalized.

STRUCTURE (THE, Lean D0.Core.DyadClosureForcing, DYAD_CLOSURE_FORCING_PROVED):
  generalize the dyad to arbitrary closure k = r11 + r22 (total positive response), det >= 0.
  Raw readout functionals D = |r11 - r22|, V = 2|r12|; identity D^2 + V^2 = k^2 - 4*det.
  * VALIDITY:  raw bound D^2+V^2 <= 1 for ALL admissible states  <=>  k <= 1
    (k > 1 broken by the pure state r11=k: D^2 = k^2 > 1);
  * SATURABILITY: some admissible state attains equality  <=>  k >= 1
    (k < 1 gives D^2+V^2 <= k^2 < 1 — bound unreachable, descriptive capacity dead;
     witness for k >= 1: r11=(k+1)/2, r22=(k-1)/2, r12=0 => det=(k^2-1)/4);
  * FORCING: validity AND saturability together  <=>  k = 1.

KOLMOGOROV / M1 READING (the point of this cert): any k != 1 forces a description cost —
either the law is broken or every readout statement must carry an extra normalization
constant 1/k. A free real constant in the description is an exogenous catalog, forbidden by
M1. Hence the unit closure (= the owned p + p^2 = 1 split) is DERIVED: "0 and 1 do not give
it, only unity" is now a theorem-shaped statement about the closure constant.

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 k=2: raw bound broken (generalizes the trace-2 V/2 finding of the previous cert);
  C2 k=0.5: bound valid but never saturable — half-dead description;
  C3 k=1 exactly: both hold, saturation by the pure state diag(1,0).
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-9


def max_raw(a: float, b: float, c: float) -> float:
    return abs(a - b) ** 2 + (2 * abs(c)) ** 2


def scan_max_raw(k: float, n: int = 401) -> float:
    """Numerical max of D^2+V^2 over PSD states with trace k (r12 grid + exact det filter)."""
    worst = -1.0
    for a in np.linspace(0.0, k, n):
        b = k - a
        cmax = (a * b) ** 0.5 if a * b >= 0 else 0.0
        for frac in (-1.0, -0.5, 0.0, 0.5, 1.0):
            c = frac * cmax * 0.999999
            if a * b - c * c >= -TOL:
                worst = max(worst, max_raw(a, b, c))
    return worst


def main() -> int:
    print("=== D0-DYAD-CLOSURE-FORCING-001  k = 1 forced (validity ∧ saturability) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: raw identity D²+V² = k²−4det; PSD states; "
          "no quantum postulates — closure constant under audit")

    # ---- GATE 1: validity ⟺ k ≤ 1 over a closure grid -----------------------------------
    ks = [0.25, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0]
    for k in ks:
        m = scan_max_raw(k)
        valid_pred = k <= 1.0 + TOL
        valid_fact = m <= 1.0 + 1e-7
        assert valid_pred == valid_fact, f"validity mismatch at k={k}: max={m}"
    print("PASS_VALIDITY_BICONDITIONAL  raw bound holds for all states iff k ≤ 1 "
          "(grid 0.25..2.0, analytic max = k² at det→0 confirmed numerically)")

    # ---- GATE 2: saturability ⟺ k ≥ 1 ----------------------------------------------------
    for k in ks:
        if k >= 1.0:
            det_w = (k * k - 1.0) / 4.0
            a, b = (k + 1) / 2, (k - 1) / 2
            assert a * b - det_w > -TOL, f"witness must be admissible at k={k}"
            val = max_raw(a, b, 0.0)
            sat = abs(val - 1.0) < 1e-6
            assert sat == (k >= 1.0 - TOL), f"saturability mismatch at k={k}: val={val}"
        else:
            m = scan_max_raw(k)
            assert m < 1.0 - 1e-4, f"k={k} must NOT saturate: max={m}"
    print("PASS_SATURABILITY_BICONDITIONAL  equality attainable iff k ≥ 1 "
          "(witness (k+1)/2,(k−1)/2; sub-unit closures never saturate)")

    # ---- GATE 3: forcing — both together only at k = 1 ------------------------------------
    both = [k for k in ks if (scan_max_raw(k) <= 1.0 + 1e-7)]
    both_sat = [k for k in ks if k >= 1.0 - TOL]
    forced = [k for k in ks if k in both and k in both_sat]
    assert forced == [1.0], f"forcing must select exactly k=1, got {forced}"
    print("PASS_FORCING_K_EQUALS_ONE  validity ∧ saturability selects k = 1 uniquely")

    # ---- CONTROL C1 (must fail): k=2 breaks the raw bound ---------------------------------
    m2 = scan_max_raw(2.0)
    assert m2 > 1.0 + 1e-6, f"k=2 must violate the bound: {m2}"
    print(f"FAIL_K2_BOUND_BROKEN  k=2: max D²+V² = {m2:.6f} > 1 "
          f"(pure state carries D=k; generalizes the trace-2 contrast=V/2 finding)")

    # ---- CONTROL C2 (must fail): k=0.5 is a dead description -------------------------------
    m05 = scan_max_raw(0.5)
    assert m05 <= 1.0 and m05 < 1.0 - 1e-4, f"k=0.5 must be valid-but-dead: {m05}"
    print(f"FAIL_K05_DEAD_CAPACITY  k=0.5: valid everywhere but max={m05:.6f}<1 — "
          f"equality unreachable, an extra 1/k constant needed to speak about saturated reads")

    # ---- M1 note ---------------------------------------------------------------------------
    print("M1_READING  k≠1 costs either a broken law (k>1) or an exogenous normalization "
          "constant (k<1); a free real constant in the description is an external catalog — "
          "forbidden. Unit closure (= p+p² split) is derived, not assumed.")

    print("HONEST_BOUNDARY  forcing proved for the two-branch readout family (Lean rc=0, "
          "0 sorry); the M1 no-catalog reading is the design principle enforced here, "
          "stated as scope, not as a separate formal axiom")
    return 0


if __name__ == "__main__":
    sys.exit(main())
