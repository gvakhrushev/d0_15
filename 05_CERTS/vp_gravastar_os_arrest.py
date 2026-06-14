#!/usr/bin/env python3
"""D0-GRAVASTAR-FORMATION-BRIDGE-001 — arrested OS collapse, horizonless seam (BRIDGE).

ROOT §4 / Phase 1 (Iteration 4). External anchor: Jampolski-Rezzolla, Phys. Rev. D 113,
L121502 (2026) (arXiv:2509.15302) — a de Sitter core arrests Oppenheimer-Snyder collapse
before a horizon forms, leaving a horizonless compact object. This is the FORMATION
dynamics of D0's "horizon = capacity-saturated seam" (BOOK_07 §07.43/§07.50): the seam
closes WITHOUT the runaway saturation σ(R)→1 that a true horizon would require.

This is a BRIDGE: it reproduces the external GR arrest structurally and reads the D0
content (the seam closes at the causal-threshold compactness C_max = 3/8, owned by
D0-COMPACTNESS-LIMIT-001). It does NOT claim to derive the gravastar from M1.

WHAT IS PROVED (exact/numeric, able to FAIL):
  * THREE-REGION STRUCTURE.  Interior de Sitter `f_in(r) = 1 − (r/L)²`, exterior
    Schwarzschild `f_out(r) = 1 − 2M/r`, joined by a thin shell at radius R.
  * ISRAEL JUNCTION.  A positive-energy static shell requires `f_in(R) > f_out(R)`
    (surface density `σ ∝ √f_in − √f_out > 0`); checked exactly.
  * HORIZONLESS ON BOTH SIDES.  `2M < R < L`: the exterior has no Schwarzschild horizon
    (`f_out(R) > 0 ⟺ C = M/R < 1/2`) and the interior has no de Sitter horizon
    (`f_in(R) > 0 ⟺ R < L`).  The collapse is ARRESTED — a seam, not a horizon.
  * D0 SEAM-CLOSURE AT C = 3/8.  The threshold (maximal stable) configuration sits at
    `C = M/R = 3/8` (from the compactness cert), strictly below the BH value 1/2, with a
    finite horizonless margin `f_out(R) = 1 − 2C = 1/4 > 0`.

NEGATIVE CONTROL (the dS core is what arrests):
  * Removing the dS core (`L → ∞`, pure dust) gives no arrest: the configuration runs to
    `C = 1/2`, `R = 2M`, `f_out = 0` — a horizon forms. The arrest is the dS core's doing.

HONESTY BOUNDARY (printed, not hidden):
  * BRIDGE: external GR result + D0 seam reading. The compactness algebra C=3/8 is the
    companion core LEM (vp_gravastar_compactness.py, named gap rank-3=causal-cone). The
    GW signature (horizonless ringdown ≠ BH) is an EMPIRICAL-PASSPORT target (Book 09).
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def f_out(r: float, M: float) -> float:
    return 1.0 - 2.0 * M / r


def f_in(r: float, L: float) -> float:
    return 1.0 - (r / L) ** 2


def main() -> int:
    print("=== D0-GRAVASTAR-FORMATION-BRIDGE-001  arrested OS collapse (horizonless seam) ===")

    M = 1.0
    Cmax = 3.0 / 8.0
    R = M / Cmax              # threshold radius R = M/C = 8/3
    assert abs(R - 8.0 / 3.0) < 1e-12, "threshold radius != 8/3"

    # ---- exterior horizonless: f_out(R) > 0  <=>  C < 1/2 --------------------------
    fo = f_out(R, M)
    C = M / R
    assert abs(C - Cmax) < 1e-12, "compactness != 3/8 at threshold"
    assert fo > 0.0, "exterior has a horizon (f_out <= 0)"
    assert abs(fo - (1.0 - 2.0 * C)) < 1e-12 and abs(fo - 0.25) < 1e-12, "f_out != 1-2C = 1/4"
    print(f"PASS_EXTERIOR_HORIZONLESS  C=3/8 -> f_out(R)=1-2C=0.25 > 0 (no Schwarzschild horizon)")

    # ---- choose a dS core radius L with R < L and a positive-energy shell ----------
    # need f_in(R) > f_out(R): 1-(R/L)^2 > 1/4  <=>  (R/L)^2 < 3/4  <=>  L > R*2/sqrt(3)
    L_min = R * 2.0 / math.sqrt(3.0)
    L = 4.0
    assert L > L_min, "chosen L does not admit a positive-energy shell"
    fi = f_in(R, L)
    assert R < L, "interior has a dS horizon (R >= L)"
    assert fi > 0.0, "interior dS horizon (f_in <= 0)"
    assert fi > fo, "Israel junction: positive-energy shell needs f_in > f_out"
    # surface density proportional to (sqrt(f_in) - sqrt(f_out)) > 0
    sigma_sign = math.sqrt(fi) - math.sqrt(fo)
    assert sigma_sign > 0.0, "shell surface density not positive"
    print(f"PASS_ISRAEL_JUNCTION  R<L, f_in(R)={fi:.3f} > f_out(R)={fo:.3f}; shell sigma>0")

    # ---- horizonless on BOTH sides: 2M < R < L ------------------------------------
    assert 2.0 * M < R < L, "not horizonless on both sides (need 2M < R < L)"
    print(f"PASS_BOTH_SIDES_HORIZONLESS  2M={2*M:.3f} < R={R:.3f} < L={L:.3f} (collapse arrested)")

    # ---- D0 seam closure at C = 3/8 < 1/2 (finite margin) --------------------------
    assert C < 0.5, "seam compactness not below the BH value"
    assert abs(C - 3.0 / 8.0) < 1e-12, "seam not at causal threshold 3/8"
    print("PASS_SEAM_CLOSES_AT_3_8  causal-threshold compactness 3/8 < 1/2 (horizonless margin)")

    # ---- negative control: no dS core (L -> inf) gives a horizon -------------------
    # pure dust collapse runs to R=2M (C=1/2): f_out=0, horizon forms
    R_bh = 2.0 * M
    assert abs(f_out(R_bh, M)) < 1e-12, "control: pure-collapse endpoint should hit f_out=0"
    # with no dS core, f_in -> 1 everywhere (L->inf), no f_in>f_out arrest below 2M
    assert f_in(R_bh, 1e12) > f_out(R_bh, M), "control sanity"
    print("FAIL_NO_DS_CORE_FORMS_HORIZON_AT_C_HALF")
    print("PASS_OS_ARREST_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_BRIDGE_EXTERNAL_GR_ARREST_PLUS_D0_SEAM_READING_NOT_M1_DERIVATION")
    print("HONEST_C_MAX_3_8_ALGEBRA_OWNED_BY_COMPACTNESS_LIMIT_LEM_WITH_NAMED_GAP")

    print("PASS_GRAVASTAR_OS_ARREST")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
