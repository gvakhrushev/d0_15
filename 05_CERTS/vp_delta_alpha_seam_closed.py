#!/usr/bin/env python3
"""D0-DELTA-ALPHA-SEAM-CLOSED-001 - the gluing-anomaly seam invariant Delta_alpha (exact, bounded).

Delta_alpha := |alpha_top^-1 - alpha_alg^-1| is the exact finite seam between two independently closed
D0 canonizations: alpha_top^-1 = 726 - 364 phi (topological channel count) and alpha_alg^-1 =
159739/5 - (294902/15) phi (algebraic/archive). It is NOT a fitted residual:
    Delta_alpha = -156109/5 + (289442/15) phi   (exact in Q(phi)),   |Delta_alpha| ~ 4.152e-4 < phi^-16 ~ 4.531e-4.
No measured alpha is used. The neutrino/mass reading P_sterile = Delta_alpha^2 stays a passport
(D0-NEUTRINO-MASS-PASSPORT-001), not CORE.

CONSOLIDATION (honest): already Lean-CORE in D0.Spectral.DeltaAlphaExact.delta_alpha_exact
(D0-DELTA-ALPHA-EXACT-001: exact value + nonzero + phi^-16 bound). This row is the sprint's named
seam-invariant statement with controls.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0


def sub(x, y):
    return (x[0] - y[0], x[1] - y[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


def main() -> int:
    print("=== D0-DELTA-ALPHA-SEAM-CLOSED-001  Delta_alpha = |alpha_top^-1 - alpha_alg^-1| exact seam invariant ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: alpha_top^-1=726-364phi (channel count) and alpha_alg^-1=159739/5-294902/15 phi "
          "(archive) are independently closed Q(phi) forms; the seam is their exact difference, no measured alpha")
    a_top = (F(726), F(-364))
    a_alg = (F(159739, 5), F(-294902, 15))
    d = sub(a_top, a_alg)
    assert d == (F(-156109, 5), F(289442, 15)), f"Delta_alpha must be -156109/5 + 289442/15 phi: {d}"
    assert d[1] != 0, "Delta_alpha phi-coefficient must be nonzero (=> irrational => != 0, M1-forced)"
    phi_inv16 = 1597.0 - 987.0 * PHI   # phi^-16 = 1597 - 987 phi
    assert 0 < abs(val(d)) < phi_inv16, f"0 < |Delta_alpha| < phi^-16 must hold: {abs(val(d))} vs {phi_inv16}"
    print(f"PASS_SEAM_EXACT  Delta_alpha = {d} = {val(d):.3e}; nonzero (phi-coeff != 0); 0 < |Delta_alpha| < phi^-16={phi_inv16:.3e}")

    assert abs(abs(val(d)) - 3.71e-4) > 1e-5, "control: |Delta_alpha| is NOT the data residual ~3.71e-4 (must not be conflated)"
    print("FAIL_NOT_DATA_RESIDUAL  |Delta_alpha|~4.15e-4 != the data residual ~3.71e-4 (the seam is algebraic, not a data fit)")
    print("HONEST_CONSOLIDATION  already Lean-CORE (D0.Spectral.DeltaAlphaExact / D0-DELTA-ALPHA-EXACT-001: exact + nonzero + "
          "phi^-16 bound). The external profinite Dixmier residue-extraction REALIZATION stays D0-DIXMIER-RESIDUE-OWNER-001.")
    print("PASS_DELTA_ALPHA_SEAM_CLOSED")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
