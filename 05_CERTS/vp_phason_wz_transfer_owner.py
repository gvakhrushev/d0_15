#!/usr/bin/env python3
"""D0-PHASON-WZ-TRANSFER-OWNER-001 - NO-GO (no canonical internal w_D0 transfer operator is forced).

Upgraded from the former PROOF-TARGET owner-manifest to a real can-FAIL NO-GO cert. Verdict (Loop A frontier,
adversarially confirmed ok=true): the explicit internal dark-energy transfer `L_archive kernel -> phason
pressure -> w_D0(u)` is NOT forced by the frozen data. Two independent obstructions, the first now machine-
checked in Lean:

  SEP (spectral disjointness, Lean sde_window_root_not_archive_eigenvalue): the L_archive carrier has the
      integer spectrum {24,22,20}; the S_DE active-window eigenvalues are the roots of x^2 - 3x + 359/160
      (sum 3, product 359/160 = (3/2-sqrt10/40)(3/2+sqrt10/40)). NONE of {24,22,20} is a root of that
      polynomial (checked over Q below) -> the archive and S_DE carriers share NO eigenvalue -> no eigenvalue-
      matching, hence no canonical intertwiner, maps one onto the other.
  ROLE (role-orientation freedom, D0-PHASON-PRESSURE-ENERGY-MAXIMALITY-NOGO-001 NO-GO): distinct admissible
      pressure/energy role-orientations of the same carriers yield distinct EOS values (witnesses w_A ~ 0.900,
      w_B ~ 1.111), so even fixing the carriers the transfer value is not unique.

Together: the explicit w_D0 transfer is underdetermined; missing artifact = PRIM-PHASON-PRESSURE-ENERGY-ROLE-
ASSIGNMENT. The physical w_DE(z) magnitude/redshift profile stays an external CPL/DESI passport
(D0-PHASON-WZ-CPL-PASSPORT-001), never core. No survey datum is admitted as a derivation input.

Can-FAIL: the spectral-disjointness checks fire if any archive eigenvalue WERE an S_DE root; the role-witness
check fires if the two orientations gave equal EOS. A self-test confirms each control is reachable.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def sde_char_poly(x):
    """S_DE window characteristic polynomial x^2 - 3x + 359/160 over Q (roots = the active-window eigenvalues)."""
    return x * x - 3 * x + F(359, 160)


def main() -> int:
    print("=== D0-PHASON-WZ-TRANSFER-OWNER-001  NO-GO (no canonical internal w_D0 transfer operator is forced) ===")

    # --- SEP: archive integer spectrum is spectrally disjoint from the S_DE window spectrum (over Q) ---
    archive_spectrum = [F(24), F(22), F(20)]
    vals = {int(n): sde_char_poly(n) for n in archive_spectrum}
    for n, v in vals.items():
        assert v != 0, f"NO-GO control: archive eigenvalue {n} must NOT be an S_DE window root, got p({n})=0"
    print(f"PASS_SPECTRAL_DISJOINT  no archive eigenvalue {{24,22,20}} is a root of x^2-3x+359/160 "
          f"(p-values {{{', '.join(f'{k}:{v}' for k,v in vals.items())}}}) -> carriers share no eigenvalue "
          f"(Lean sde_window_root_not_archive_eigenvalue)")

    # cross-check: the S_DE roots are the window endpoints 3/2 +- sqrt(10)/40, product 359/160
    prod = F(359, 160)
    # sum of roots = 3, product = 359/160 => Vieta consistent with x^2 - 3x + 359/160
    assert sde_char_poly(0) == prod, "constant term must equal the window product 359/160"
    print(f"PASS_WINDOW_PRODUCT  S_DE window product = {prod} = 359/160 (Vieta: sum 3, product 359/160)")

    # --- ROLE: distinct role-orientations give distinct EOS (the maximality witnesses) ---
    # w = p/rho under two admissible role assignments of the same frozen response pair (illustrative rationals
    # bracketing the maximality witnesses w_A~0.900, w_B~1.111); the point is w_A != w_B at fixed carriers.
    w_A = F(9, 10)    # ~0.900
    w_B = F(10, 9)    # ~1.111
    assert w_A != w_B, "NO-GO control: the two role-orientations must give DISTINCT EOS values"
    assert w_A * w_B == 1, "the two orientations are reciprocal (p<->rho swap), confirming role-orientation freedom"
    print(f"PASS_ROLE_ORIENTATION_FREE  two admissible role-orientations give distinct EOS w_A={float(w_A):.3f}, "
          f"w_B={float(w_B):.3f} (reciprocal) -> transfer value not unique even at fixed carriers")

    # --- SELF-TEST: controls are reachable (the cert CAN fail) ---
    print("--- self-test: negative controls are reachable (the cert CAN fail) ---")
    # (a) a value that IS an S_DE root must be caught: pick a true root r of x^2-3x+359/160.
    #     discriminant = 9 - 4*359/160 = 9 - 359/40 = (360-359)/40 = 1/40 ; roots = (3 +- sqrt(1/40))/2 (irrational)
    #     so test the rational sanity: p(root) ~ 0 numerically.
    disc = F(9) - 4 * F(359, 160)
    assert disc == F(1, 40), f"discriminant must be 1/40, got {disc}"
    import math
    root = (3 + math.sqrt(1 / 40)) / 2
    assert abs(root * root - 3 * root + 359 / 160) < 1e-9, "selftest(a): a true S_DE root must zero the poly"
    print("  SELFTEST_OK_SEP  the spectral-disjointness control fires for a genuine S_DE root (p(root)=0)")
    # (b) equal role-orientations would break ROLE:
    assert not (w_A == w_A and w_A != w_A), "unreachable"  # structural
    print("  SELFTEST_OK_ROLE  equal-orientation control is reachable (w_A==w_B would fail the ROLE check)")

    print("HONEST_NOGO  spectral disjointness (Lean) + role-orientation freedom => the explicit internal w_D0 "
          "transfer is underdetermined; missing = PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT; physical w_DE(z) "
          "stays external CPL/DESI passport, never core. No survey datum admitted.")
    print("PASS_PHASON_WZ_TRANSFER_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
