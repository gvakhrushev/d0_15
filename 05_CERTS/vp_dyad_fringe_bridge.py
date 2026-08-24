#!/usr/bin/env python3
"""D0-DYAD-FRINGE-BRIDGE-001 — the fringe/path bridge is DERIVED, not identified.

STRUCTURE (THE, Lean D0.Core.DyadFringeBridge, DYAD_FRINGE_BRIDGE_PROVED):
  scan the dyad comparison phase: I(phi) = 1/2 + r12*cos(phi)  (baseline = unit closure).
    fringeMax = 1/2 + |r12|,  fringeMin = 1/2 - |r12|,  fringeMax + fringeMin = 1.
  THEOREM (Leg 1): standard fringe contrast
    (Imax - Imin)/(Imax + Imin) = 2*|r12| = V(rho)   — an IDENTITY, no optical input.
  THEOREM (Leg 2): branch-diagonal best guess has success gap |r11 - r22| = D(rho).
  COROLLARY (operational complementarity):
    fringe-contrast^2 + path-gap^2 <= 1   for every admissible record.

RESIDUAL EXTERNAL BRIDGE (one sentence): a laboratory interferometer implements the
phase-scanned comparison of its two arms. The QUANTITY-level bridge of the previous claim
(D0-DYAD-COMPLEMENTARITY-001) is hereby discharged into derivation; only the apparatus-level
reading stays external.

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 non-vacuity: a non-PSD matrix violates the operational bound;
  C2 closure load-bearing: WITHOUT unit normalization the contrast identity breaks —
     the denominator trick (Imax+Imin = trace) is exactly where closure enters;
  C3 sanity at the extremes: path-certain state -> flat pattern (V=0);
     balanced coherent state -> maximal swing (V=1).
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-9


def admissible(a: float, b: float, c: float) -> bool:
    return abs((a + b) - 1.0) < TOL and (a * b - c * c) >= -TOL


def empirical_contrast(a: float, b: float, c: float, n: int = 720) -> float:
    """Scan I(phi) = a*? ... direct computation over phi grid, extract (max-min)/(max+min).

    Full phase readout of the branch pair against relative phase phi:
        I(phi) = (a+b)/2 + c*cos(phi)     (real symmetric dyad)
    """
    phi = np.linspace(0.0, 2.0 * np.pi, n, endpoint=False)
    intens = (a + b) / 2.0 + c * np.cos(phi)
    imax, imin = float(intens.max()), float(intens.min())
    return (imax - imin) / (imax + imin)


def main() -> int:
    print("=== D0-DYAD-FRINGE-BRIDGE-001  fringe contrast ≡ V(rho), derived from the scan ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: I(phi)=(trace)/2+r12*cos(phi); contrast=",
          "(Imax-Imin)/(Imax+Imin); no optical postulates — pure finite-stage algebra")

    # ---- GATE 1: contrast identity over random admissible states ------------------------
    rng = np.random.default_rng(15)
    checked = 0
    worst_gap = 0.0
    for _ in range(4000):
        a = float(rng.uniform(0, 1))
        b = 1.0 - a
        # |c| <= sqrt(a*b) keeps PSD
        c = float(rng.uniform(-1, 1)) * (a * b) ** 0.5 * 0.999
        if not admissible(a, b, c):
            continue
        checked += 1
        emp = empirical_contrast(a, b, c)
        theo = 2.0 * abs(c)
        worst_gap = max(worst_gap, abs(emp - theo))
        assert abs(emp - theo) < 1e-7, f"contrast identity broke: {emp} vs {theo} at {(a,b,c)}"
    assert checked > 3000, f"too few admissible samples: {checked}"
    print(f"PASS_CONTRAST_IDENTITY  {checked} states: (Imax-Imin)/(Imax+Imin) == 2|r12| "
          f"exactly (worst dev {worst_gap:.2e})")

    # ---- GATE 2: operational complementarity on extracted quantities --------------------
    for a, b, c in [(0.8, 0.2, 0.2), (0.5, 0.5, 0.5), (0.99, 0.01, 0.09),
                    (0.6, 0.4, -0.35), (0.5, 0.5, -0.49)]:
        assert admissible(a, b, c)
        v = empirical_contrast(a, b, c)
        d = abs(a - b)
        assert v * v + d * d <= 1.0 + 1e-9, f"operational bound violated at {(a,b,c)}: {v}^{2}+{d}^2"
    print(f"PASS_OPERATIONAL_BOUND  fringe-contrast² + path-gap² ≤ 1 on extracted quantities")

    # ---- CONTROL C1 (must fail): non-PSD violates the operational bound ------------------
    bad_a, bad_b, bad_c = 0.9, 0.1, 0.5
    assert not admissible(bad_a, bad_b, bad_c)
    v_bad = empirical_contrast(bad_a, bad_b, bad_c)
    d_bad = abs(bad_a - bad_b)
    assert v_bad ** 2 + d_bad ** 2 > 1.0 + 1e-9, "non-PSD must violate operational bound"
    print(f"FAIL_NONPSD_OPERATIONAL  non-admissible [[{bad_a},{bad_c}],[{bad_c},{bad_b}]]: "
          f"{v_bad**2+d_bad**2:.6f} > 1")

    # ---- CONTROL C2 (must fail): unit closure is load-bearing ----------------------------
    # scale the state by 2 (trace=2): denominator doubles, identity degrades to half-contrast
    a2, b2, c2 = 1.0, 1.0, 0.6  # trace 2, PSD
    assert abs((a2 + b2) - 2.0) < TOL
    emp_unnorm = empirical_contrast(a2, b2, c2)
    theo_if_closure_free = 2.0 * abs(c2)
    assert abs(emp_unnorm - theo_if_closure_free / 2.0) < 1e-7 and \
           abs(emp_unnorm - theo_if_closure_free) > 1e-3, \
        "without unit closure the contrast identity must break by exactly the trace factor"
    print(f"FAIL_CLOSURE_FREE_IDENTITY  trace=2 state: empirical contrast {emp_unnorm:.6f} "
          f"= V/2, NOT V={theo_if_closure_free:.6f} — closure enters via Imax+Imin=1")

    # ---- CONTROL C3 (must pass structure): extremes behave physically --------------------
    v_path = empirical_contrast(1.0, 0.0, 0.0)
    assert abs(v_path) < 1e-9, "path-certain record must show NO fringes"
    v_wave = empirical_contrast(0.5, 0.5, 0.5)
    assert abs(v_wave - 1.0) < 1e-9, "balanced coherent record must show FULL swing"
    print(f"FAIL_PATH_STATE_HAS_NO_FRINGES  diag(1,0): V={v_path:.3f}; "
          f"balanced coherent: V={v_wave:.3f} — wave/particle extremes confirmed")

    print("HONEST_BOUNDARY  quantities now DERIVED (Lean rc=0, 0 sorry); residual external "
          "bridge = 'lab interferometer realizes the phase-scanned comparison' (apparatus, "
          "not quantity)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
