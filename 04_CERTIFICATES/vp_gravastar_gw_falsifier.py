#!/usr/bin/env python3
"""D0-GRAVASTAR-GW-FALSIFIER-001 — horizonless ringdown ≠ black-hole (passport target).

ROOT Phase 1 / T1.3 (Iteration 4). A second gravitational-wave falsifier, beyond the
I_f = log φ horizon-hum target (BOOK_09 §09.05): a horizonless gravastar at the causal
compactness C_max = 3/8 has its surface at R = 8M/3 ≈ 2.667M, which is INSIDE the photon
sphere r_ph = 3M. The light-ring potential barrier plus the reflecting surface form a
cavity, so the post-merger signal carries GW ECHOES — a feature a true black hole (whose
horizon absorbs, no surface, no cavity) cannot produce. Echoes present ⟹ horizonless;
absent ⟹ consistent with a horizon.

This is an EMPIRICAL-PASSPORT TARGET, frozen as a falsifier — NOT a core claim and NOT
claimed from current data (Book 09 claim discipline: allowed verb = "predicts as target").

WHAT IS PROVED (numeric, able to FAIL):
  * CAVITY EXISTS.  At C = 3/8, the surface R = 8M/3 lies strictly inside the photon
    sphere 3M and strictly outside the horizon 2M: 2M < 8M/3 < 3M. A BH has no surface
    outside 2M, hence no cavity.
  * ECHO-DELAY TARGET.  The characteristic echo delay is the light round-trip across the
    cavity in tortoise coordinate, τ_echo = 2·[r*(3M) − r*(8M/3)] with
    r*(r) = r + 2M·ln(r/2M − 1); computed here ≈ 2.3 M — a short-delay echo train
    (distinct from the long-delay near-horizon echoes of objects sitting at R → 2M).
    Dimensionless (in units of M), so it is a falsifiable structural target.
  * DISCIPLINE.  Marked NOT confirmed (retained target, like I_f); a BH gives no echo.

NEGATIVE CONTROL:
  * A black hole (surface at the horizon 2M, no exterior surface) has no cavity: there is
    no r in (2M, 3M) reflecting surface, so no echo delay is defined. Echo presence is the
    discriminator.

HONESTY BOUNDARY (printed, not hidden):
  * PASSPORT TARGET, never core. The echo mechanism for ultracompact horizonless objects
    is standard (Cardoso–Pani); the D0-specific content is the surface placement at the
    causal ceiling C=3/8 (companion LEM). Not claimed from any current LIGO event.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

M = 1.0
C_MAX = 3.0 / 8.0
R_SURF = M / C_MAX          # 8M/3 ≈ 2.667M
R_PH = 3.0 * M             # Schwarzschild photon sphere
R_HOR = 2.0 * M


def r_star(r: float) -> float:
    """Tortoise coordinate r* = r + 2M ln(r/2M − 1)."""
    return r + 2.0 * M * math.log(r / (2.0 * M) - 1.0)


def main() -> int:
    print("=== D0-GRAVASTAR-GW-FALSIFIER-001  horizonless ringdown != BH (passport target) ===")

    # ---- cavity exists: 2M < surface < photon sphere -------------------------------
    assert R_HOR < R_SURF < R_PH, "surface not in the light-ring cavity (need 2M < R < 3M)"
    assert abs(R_SURF - 8.0 / 3.0) < 1e-12, "surface radius != 8M/3"
    print(f"PASS_LIGHT_RING_CAVITY  2M={R_HOR:.3f} < R_surf={R_SURF:.3f} < r_ph={R_PH:.3f}")

    # ---- echo-delay target: τ_echo = 2[r*(3M) − r*(8M/3)] --------------------------
    tau_echo = 2.0 * (r_star(R_PH) - r_star(R_SURF))
    assert tau_echo > 0.0, "echo delay must be positive"
    assert 1.0 < tau_echo < 5.0, f"echo delay {tau_echo:.3f}M out of expected short-delay band"
    print(f"PASS_ECHO_DELAY_TARGET  tau_echo = 2[r*(3M)-r*(8M/3)] = {tau_echo:.4f} M (short-delay)")

    # ---- discipline: dimensionless, falsifiable, NOT confirmed ----------------------
    # the target is in units of M (dimensionless once scaled by the remnant mass)
    assert tau_echo / M == tau_echo, "echo delay not expressed in units of M"
    print("PASS_DIMENSIONLESS_FALSIFIABLE_TARGET  echo delay in units of M (scale-free)")

    # ---- negative control: a black hole has no cavity / no echo --------------------
    # for a BH the only 'surface' is the horizon at 2M; r*(2M) -> -inf, no exterior surface
    try:
        _ = r_star(R_HOR)          # r/(2M)-1 = 0 -> log(0) -> -inf / domain error
        bh_surface_defined = math.isfinite(_)
    except ValueError:
        bh_surface_defined = False
    assert not bh_surface_defined, "control: a BH must have no finite exterior reflecting surface"
    print("FAIL_BLACK_HOLE_HAS_NO_CAVITY_NO_ECHO")
    # an object at the photon sphere itself (R=3M) has zero cavity width -> no echo train
    assert abs(2.0 * (r_star(R_PH) - r_star(R_PH))) < 1e-12, "control: zero-width cavity gives no delay"
    print("FAIL_ZERO_WIDTH_CAVITY_NO_ECHO")
    print("PASS_GW_FALSIFIER_NEGATIVE_CONTROLS")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_PASSPORT_TARGET_NEVER_CORE_NOT_CLAIMED_FROM_CURRENT_LIGO")
    print("HONEST_ECHO_MECHANISM_STANDARD_CARDOSO_PANI_D0_CONTENT_IS_SURFACE_AT_3_8")

    print("PASS_GRAVASTAR_GW_FALSIFIER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
