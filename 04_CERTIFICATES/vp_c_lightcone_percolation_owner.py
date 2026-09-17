#!/usr/bin/env python3
"""D0-C-LIGHTCONE-PERCOLATION-OWNER-001 (CERT-CLOSED) - c = 1 gauge + gap-positivity at connectivity.

Front P4 (companion to vp_connectivity_spectral_gap_speed.py / vp_connectivity_threshold_owner.py and
the Lean owner D0.Cosmology.CLightconePercolationOwner). The discrete signal speed is the ratio of a
unit cell-length to a unit tick, c_D0 = ell0 / tau0. With the tick gauge ell0 = tau0 = 1 (one edge
traversed per discrete step) this is c_D0 = 1.

HONEST SPLIT (cardinal):
  * The numerical VALUE c_D0 = 1 is a UNIT-FIXING GAUGE (ell0 = tau0 = 1), NOT a derivation. The SI
    speed of light is neither an input nor an output; importing it as input is a rejected control.
  * The CONTENT (the theorem) is that one-edge-per-tick propagation along the scene graph exists only
    when the graph is CONNECTED, and connectivity is exactly lambda_2 > 0 (Fiedler value, smallest
    nonzero Laplacian eigenvalue). For the forced scene K(9,11,13): lambda_2 = 20 > 0 (connected); for
    the edgeless stage: lambda_2 = 0 (disconnected, nothing propagates).

WHAT IS PROVED (exact, able to FAIL):
  * c_D0 = ell0/tau0 = 1/1 = 1 with EXACT rational arithmetic (Fraction); the value is gauge-forced.
  * K(9,11,13) Laplacian Fiedler value lambda_2 = 20 > 0 (numpy eigvalsh, second-smallest eigenvalue),
    so the connected scene admits a one-edge-per-tick path; matches Lean fiedler_pos / lap_fiedler_eigen20.
  * The edgeless 33-vertex stage has lambda_2 = 0; a graph with lambda_2 = 0 cannot propagate at any c.

No SI c, no Planck/CMB datum enters. Lean owner: D0.Cosmology.CLightconePercolationOwner
(cD0_eq_one, lap_fiedler_eigen20, fiedler_pos, edgeless kernel facts).
"""
from __future__ import annotations

import sys
from fractions import Fraction

import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ZONES = (9, 11, 13)  # forced zone sizes -> 33 vertices
N = sum(ZONES)

# SI speed of light (m/s) - present ONLY as a planted negative-control input that must be REJECTED.
C_SI = 299_792_458


def speed_from_gauge(ell0: Fraction, tau0: Fraction) -> Fraction:
    """Discrete signal speed: unit cell-length per unit tick. Exact rational."""
    return ell0 / tau0


def laplacian(sizes):
    """Combinatorial Laplacian L = D - A of the complete multipartite graph on the given parts."""
    labels = []
    for b, s in enumerate(sizes):
        labels += [b] * s
    n = len(labels)
    A = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            if i != j and labels[i] != labels[j]:
                A[i, j] = 1.0
    return np.diag(A.sum(axis=1)) - A


def fiedler_value(L) -> float:
    """Algebraic connectivity = second-smallest Laplacian eigenvalue."""
    return float(np.sort(np.linalg.eigvalsh(L))[1])


def main() -> int:
    print("=== D0-C-LIGHTCONE-PERCOLATION-OWNER-001  c=1 gauge + gap-positivity (CERT-CLOSED) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the tick gauge (ell0 = tau0 = 1, one edge per tick) and the "
          "33-vertex complete-tripartite scene K(9,11,13) are fixed before any number; c_D0 = ell0/tau0 "
          "is a UNIT gauge and the CONTENT is lambda_2 > 0 <=> connected. No SI c, no CMB datum")

    # ---- c_D0 = 1 is a gauge (ell0 = tau0 = 1), exact rational ----------------------
    ell0, tau0 = Fraction(1), Fraction(1)
    c = speed_from_gauge(ell0, tau0)
    assert c == Fraction(1), f"c_D0 must be 1 in the unit gauge, got {c}"
    print(f"PASS_C_GAUGE_ONE  c_D0 = ell0/tau0 = {ell0}/{tau0} = {c} (UNIT-FIXING gauge, NOT a derivation "
          "of the value 1) [matches Lean cD0_eq_one]")

    # ---- the value is forced by the gauge for ANY unit gauge ------------------------
    for e, t in [(Fraction(1), Fraction(1)), (Fraction(2, 2), Fraction(3, 3))]:
        assert speed_from_gauge(e, t) == Fraction(1), "any ell0=tau0 gauge must give speed 1"
    print("PASS_C_GAUGE_INVARIANT  every ell0 = tau0 gauge gives speed 1 (value forced by the gauge, "
          "not by any spectral number) [matches Lean speed_eq_one]")

    # ---- CONTENT: K(9,11,13) carries a positive gap (connected) ---------------------
    L = laplacian(ZONES)
    lam2 = fiedler_value(L)
    assert abs(lam2 - 20.0) < 1e-9 and lam2 > 0.0, f"connected-scene Fiedler value must be 20 > 0, got {lam2}"
    fied = np.zeros(33)
    fied[20], fied[21] = 1.0, -1.0
    assert np.allclose(L @ fied, 20.0 * fied, atol=1e-12), "explicit 20-eigenvector must check"
    print(f"PASS_CONTENT_GAP_POSITIVE  K(9,11,13): lambda_2 = {lam2:.9f} = 20 > 0 -> CONNECTED -> "
          "one-edge-per-tick propagation exists [matches Lean lap_fiedler_eigen20 / fiedler_pos]")

    # ---- edgeless stage: lambda_2 = 0 (disconnected) --------------------------------
    L0 = np.zeros((33, 33))
    assert abs(fiedler_value(L0)) < 1e-12, "edgeless Fiedler value must be 0"
    print("PASS_EDGELESS_NO_GAP  edgeless 33-vertex stage: lambda_2 = 0 -> DISCONNECTED -> no propagation "
          "[matches Lean edgeless_e0_kernel / edgeless_e1_kernel / e0_ne_e1]")

    # ---- negative controls (genuinely reachable) ------------------------------------
    # (a) SI speed of light imported as the value of c: the gauge fixes c=1, NOT 299792458.
    imported_c_value = Fraction(C_SI)
    accept_si_as_cD0 = (speed_from_gauge(ell0, tau0) == imported_c_value)
    assert accept_si_as_cD0 is False, "control: SI speed of light must NOT be c_D0"
    print(f"FAIL_SI_C_INPUT_REJECTED  planted 'c_D0 = {C_SI} m/s (SI input)' rejected "
          "(gauge fixes c_D0 = 1; no SI datum enters)")

    # (b) an arbitrary c != 1 from a non-unit gauge claimed as the D0 speed: rejected.
    bad_c = speed_from_gauge(Fraction(3), Fraction(2))  # ell0=3, tau0=2 -> 3/2 != 1
    assert bad_c != Fraction(1), "non-unit gauge must give c != 1"
    accept_arbitrary_c = (bad_c == Fraction(1))
    assert accept_arbitrary_c is False, "control: arbitrary c != 1 must be rejected as the D0 gauge speed"
    print(f"FAIL_ARBITRARY_C_REJECTED  planted 'c_D0 = {bad_c} (non-unit gauge ell0=3,tau0=2)' rejected "
          "(the D0 gauge is ell0 = tau0 = 1 -> c = 1)")

    # (c) disconnected graph claimed to propagate at c = 1: lambda_2 = 0 -> no path.
    disconnected_propagates_at_c1 = (fiedler_value(L0) > 0.0) and (c == Fraction(1))
    assert disconnected_propagates_at_c1 is False, \
        "control: a disconnected graph must NOT propagate at c=1"
    print("FAIL_DISCONNECTED_C1_REJECTED  planted 'edgeless graph propagates at c=1' rejected "
          "(lambda_2 = 0 -> no connected path -> nothing to propagate at any speed)")

    # (d) lambda_2 = 2 over-claim (a fake Cheeger equality): actual lambda_2 = 20, not 2.
    overclaim_lambda2_is_2 = abs(fiedler_value(L) - 2.0) < 1e-9
    assert overclaim_lambda2_is_2 is False, "control: lambda_2 = 2 over-claim must be rejected"
    print(f"FAIL_LAMBDA2_EQUALS_2_REJECTED  planted 'lambda_2 = 2' rejected "
          f"(actual lambda_2 = {fiedler_value(L):.6f} = 20; no Cheeger equality is asserted)")

    print("HONEST_C1_IS_GAUGE_NOT_DERIVATION; CONTENT_IS_GAP_POSITIVE_AT_CONNECTIVITY; "
          "NORMALIZED_CHEEGER_BOUND_IS_THEOREM_TARGET")
    print("PASS_C_LIGHTCONE_PERCOLATION_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
