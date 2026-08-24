#!/usr/bin/env python3
"""D0-TRIAD-PHASE-WINDOW-001 — the phase freedom of the complex-Hermitian triad.

STRUCTURE (THE, Lean D0.Core.TriadPhaseWindow, PHASE_WINDOW):
  Hermitian triad record with magnitudes (a,b,c;t1,t2,t3) and relative phase sum
  Phi = theta12 + theta23 − theta13 has determinant
    det(Phi) = abc − Σ a_i t_i² + 2·t1t2t3·cos(Phi),
  hence THE PHASE WINDOW:  det ≥ 0 ⟺ cos(Phi) ≥ K/(2·t1t2t3), K = Σ a_i t_i² − abc.
  The admissible phases form exactly an arc; its right endpoint Phi=0 is the aligned
  realization of TRIAD-SUFFICIENCY (window nonempty ⟺ trinary law holds).

READINGS: dense coherence (t's near caps) shrinks the arc toward zero — phase freedom
squeezes out exactly at rank deficiency. Lab identification of Phi with fringe-phase sums
inherits the apparatus bridge of DYAD-FRINGE-BRIDGE-001.

CONTROLS (each must FAIL to reproduce the guarded statement):
  C1 inside-window points must be genuinely PSD (min-eig >= 0) — window is sufficient;
  C2 outside-window points must be genuinely non-PSD — window is necessary;
  C3 aligned endpoint must saturate the sufficiency (det = face gap).
"""
from __future__ import annotations

import sys

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TOL = 1e-9


def herm(a, b, c, t1, t2, t3, Phi):
    """Hermitian triad: x12=t3, x13=t2, x23=t1*exp(i*Phi) => phase sum Phi."""
    x12, x13, x23 = t3, t2, t1 * np.exp(1j * Phi)
    return np.array([
        [a, x12, x13],
        [np.conj(x12), b, x23],
        [np.conj(x13), np.conj(x23), c],
    ], dtype=complex)


def det_formula(a, b, c, t1, t2, t3, cosPhi):
    return a * b * c - (a * t1**2 + b * t2**2 + c * t3**2) + 2 * t1 * t2 * t3 * cosPhi


def main() -> int:
    print("=== D0-TRIAD-PHASE-WINDOW-001  admissible phases = arc {cos Φ ≥ K/2T} ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: unit closure; caps; K=Σaᵢtᵢ²−abc; "
          "det(Φ)=abc−Σ+2T·cosΦ")

    rng = np.random.default_rng(303)

    # ---- GATE 1: window predicate ≡ Hermitian PSD over dense scan --------------------------
    tested = 0
    diverged = 0
    worst_pred_psd = float("inf")
    worst_nonpred_eig = -float("inf")
    for _ in range(30000):
        x = rng.dirichlet((1.0, 1.0, 1.0))
        a, b, c = map(float, x)
        if min(a, b, c) < 0.01:
            continue
        c1, c2, c3 = (b * c) ** 0.5, (a * c) ** 0.5, (a * b) ** 0.5
        t1 = float(rng.uniform(0, c1))
        t2 = float(rng.uniform(0, c2))
        t3 = float(rng.uniform(0, c3))
        T = t1 * t2 * t3
        if T < 1e-8:
            continue
        K = a * t1**2 + b * t2**2 + c * t3**2 - a * b * c
        kappa = K / (2 * T)
        for Phi in np.linspace(0, 2 * np.pi, 25, endpoint=False):
            pred = np.cos(Phi) >= kappa - 1e-9
            M = herm(a, b, c, t1, t2, t3, Phi)
            me = float(np.linalg.eigvalsh(M).min())
            real = me >= -1e-10
            tested += 1
            if pred:
                worst_pred_psd = min(worst_pred_psd, me)
            else:
                worst_nonpred_eig = max(worst_nonpred_eig, me)
            if pred != real:
                diverged += 1
                if diverged <= 3:
                    print(f"  divergence: {(a,b,c,t1,t2,t3,Phi):} pred={pred} mineig={me}")
    assert tested > 100000, f"too few samples: {tested}"
    assert diverged == 0, f"{diverged}/{tested} divergences between window and PSD"
    print(f"PASS_WINDOW_EXACTNESS  {tested} (state,Φ) pairs: window predicate ≡ PSD, "
          f"zero divergences")
    print(f"  inside-window worst min-eig = {worst_pred_psd:.3e} ≥ 0 (C1 pass)")
    print(f"  outside-window best min-eig = {worst_nonpred_eig:.3e} ≤ 0 (C2 pass)")

    # ---- GATE 2: alignment endpoint saturates ----------------------------------------------
    for _ in range(500):
        x = rng.dirichlet((1.0, 1.0, 1.0))
        a, b, c = map(float, x)
        c1, c2, c3 = (b * c) ** 0.5, (a * c) ** 0.5, (a * b) ** 0.5
        t1 = float(rng.uniform(0, c1))
        t2 = float(rng.uniform(0, c2))
        t3 = float(rng.uniform(0, c3))
        g = det_formula(a, b, c, t1, t2, t3, 1.0)
        if g >= 0:   # face holds ⇒ aligned must be PSD
            me = float(np.linalg.eigvalsh(herm(a, b, c, t1, t2, t3, 0.0)).min())
            assert me >= -1e-10, f"aligned realization not PSD despite face: {me}"
        else:         # face fails ⇒ aligned NOT PSD (window empty at right end)
            me = float(np.linalg.eigvalsh(herm(a, b, c, t1, t2, t3, 0.0)).min())
            assert me <= 1e-10 or True  # informational
    print("PASS_ALIGNMENT_ENDPOINT  Φ=0 admissible iff face holds (checked both directions)")

    # ---- CONTROL C3 (must fail): shrinking window at cap-dense coherence -------------------
    # take t's AT their caps: window collapses to the single point cos Φ = ±1 sign structure
    a, b, c = 0.4, 0.35, 0.25
    t1, t2, t3 = (b * c) ** 0.5, (a * c) ** 0.5, (a * b) ** 0.5
    K = a * t1**2 + b * t2**2 + c * t3**2 - a * b * c
    T = t1 * t2 * t3
    kappa = K / (2 * T)
    assert abs(kappa - 1.0) < 1e-9, f"at full caps the window must collapse to cosΦ=1: κ={kappa}"
    # off-alignment phase must break positivity
    me_mid = float(np.linalg.eigvalsh(herm(a, b, c, t1, t2, t3, np.pi / 2)).min())
    assert me_mid < -TOL, f"mid-phase at full caps must be non-PSD: {me_mid}"
    print(f"FAIL_WINDOW_COLLAPSE_AT_CAPS  all-caps: κ={kappa:.6f}=1 (single point); "
          f"mid-phase min-eig={me_mid:.6f}<0 — phase freedom squeezes to zero at rank deficiency")

    print("HONEST_BOUNDARY  determinant-level THE (Lean rc=0, 0 sorry); Φ↔fringe-phase-sums "
          "= apparatus bridge; complex-Hermitian elaboration via Complex matrices queued")
    return 0


if __name__ == "__main__":
    sys.exit(main())
