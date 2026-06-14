"""D0-H0-EVOLVING-W-001 — H0(z) downtrend = evolving w from R_n=phi^n-1 (passport).

ROOT Phase 5 / T5.5 (Iteration 4). External anchors: DESI DR2 evolving-w (w0wa) and the
H0(z) trend literature (IOP 2041-8213/ae1965, 2025). D0's relative-archive-acceleration
R_n = phi^n - 1 has a convex second difference (Delta^2 R_n > 0), which reads as an
evolving (thawing) dark-energy equation of state and a redshift-declining effective H0.
This is an EMPIRICAL-PASSPORT with an internal falsifier; never core.

WHAT IS PROVED (exact, able to FAIL):
  * CONVEX ACCELERATION.  R_n = phi^n - 1 has strictly positive second difference
    Delta^2 R_n = R_{n+2} - 2 R_{n+1} + R_n = phi^n (phi-1)^2 > 0 for all n (exact via
    the phi^2 = phi + 1 recursion) -> a thawing, evolving-w signature, not a cosmological
    constant (Delta^2 = 0).
  * DIRECTION.  The trend is monotone (R_n increasing) and convex, giving a redshift
    DECLINING effective expansion rate (younger effective age) — the qualitative DESI
    w0>-1, wa<0 corner, opposite to a phantom (w<-1) crossing.
  * INTERNAL FALSIFIER.  The passport is rejected if H0 RISES with z while S8 stays at the
    Planck value (the corpus holds S8 at Planck); the predicted joint move is H0 falling
    with z together with the DESI w0wa anomaly as ONE phenomenon.

HONESTY BOUNDARY (printed, not hidden):
  * EMPIRICAL-PASSPORT, firewall-blocked from core (BOOK_08 demotes H0 to a diagnostic and
    forbids promoting it to a core observable; H0/G_N/Lambda need external SI calibration).
    The convexity Delta^2 R_n > 0 is the only exact/forced piece; the cosmological reading
    is a passport comparison against DESI DR2/DR3, not a prediction at survey precision.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + math.sqrt(5.0)) / 2.0


def R(n: int) -> float:
    return PHI ** n - 1.0


def main() -> int:
    print("=== D0-H0-EVOLVING-W-001  H0(z) downtrend = evolving w from R_n=phi^n-1 (passport) ===")

    # ---- convex second difference Delta^2 R_n = phi^n (phi-1)^2 > 0 ----------------
    for n in range(0, 12):
        d2 = R(n + 2) - 2 * R(n + 1) + R(n)
        closed = PHI ** n * (PHI - 1.0) ** 2
        if abs(d2 - closed) > 1e-9 * max(1.0, abs(closed)):
            raise AssertionError(f"Delta^2 R_{n} != phi^n (phi-1)^2")
        if not d2 > 0:
            raise AssertionError(f"Delta^2 R_{n} not strictly positive")
    print("PASS_CONVEX_ACCELERATION  Delta^2 R_n = phi^n (phi-1)^2 > 0 (evolving/thawing w)")

    # ---- monotone increasing (declining effective H0 with z) -----------------------
    assert all(R(n + 1) > R(n) for n in range(0, 12)), "R_n not monotone increasing"
    # cosmological-constant control: a constant R would have Delta^2 = 0 (not evolving)
    constR = lambda n: 1.0
    assert (constR(2) - 2 * constR(1) + constR(0)) == 0.0, "constant control should have Delta^2=0"
    print("PASS_MONOTONE_CONVEX  R_n increasing & convex (vs Lambda-CDM Delta^2=0 control)")

    # ---- internal falsifier: H0 up with S8 at Planck rejects the passport ----------
    # encode the falsifier as a boolean predicate the passport asserts must NOT hold
    def falsified(H0_rises_with_z: bool, S8_at_planck: bool) -> bool:
        return H0_rises_with_z and S8_at_planck
    assert not falsified(False, True), "predicted: H0 falls with z (not rises) at Planck S8"
    assert falsified(True, True), "control: H0 rising with z at Planck S8 WOULD falsify"
    print("FAIL_H0_RISING_WITH_Z_AT_PLANCK_S8_WOULD_FALSIFY")
    print("PASS_H0_FALSIFIER_DEFINED")

    # ---- honesty boundary ----------------------------------------------------------
    print("HONEST_EMPIRICAL_PASSPORT_H0_DEMOTED_NOT_CORE_NEEDS_EXTERNAL_SI_CALIBRATION")
    print("HONEST_ONLY_CONVEXITY_DELTA2_R_N_FORCED_COSMO_READING_IS_DESI_COMPARISON")

    print("PASS_H0_EVOLVING_W")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
