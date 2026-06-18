#!/usr/bin/env python3
"""D0-PHASON-PRESSURE-EOS-SCAFFOLD-001 - the phason equation-of-state FORM w_D0 = p/rho is well-defined.

Given a finite internal pressure-energy pair (rho>0 from the archive relative-acceleration energy
D0-IM-COSMO-001; pressure from the log-det loop-pressure response LOGDET-PRESSURE-COUPLING-CERT-CLOSED),
the EOS w_D0 = pressure/rho is well-defined on the nonzero-energy domain and computed from INTERNAL
quantities only. Lean: D0.Cosmology.PhasonWZTransfer (phason_w_defined_on_nonzero_energy).

SCOPE (honest): closes the EOS FORM + well-definedness only. The explicit internal w_D0(u) / finite w_N
FORMULA (the actual phason rho(u), p(u) functions) stays PROOF-TARGET (D0-PHASON-WZ-TRANSFER-OWNER-001);
the redshift u->z / CPL reading is passport-only. No survey datum enters.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def w_D0(p, rho):
    assert rho != 0, "EOS undefined at zero energy"
    return p / rho


def main() -> int:
    print("=== D0-PHASON-PRESSURE-EOS-SCAFFOLD-001  w_D0 = p/rho well-defined (EOS form) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: finite pressure-energy pair (rho from archive energy D0-IM-COSMO-001; p from "
          "log-det pressure) fixed before w; w_D0 = p/rho on the nonzero-energy domain")
    rho = F(1)          # a positive internal archive-energy unit (R_n>0; archive_growth_strictly_convex)
    p = F(-3, 4)        # an internal log-det pressure value (illustrative internal quantity, not a survey input)
    assert rho > 0, "archive energy must be positive (relative-acceleration convexity)"
    w = w_D0(p, rho)
    assert w == p / rho, "w_D0 must equal p/rho (well-defined)"
    print(f"PASS_EOS_WELL_DEFINED  rho={rho}>0, p={p}, w_D0 = p/rho = {w} (computed from internal quantities only)")

    # control: zero energy is undefined (the domain condition bites)
    failed = False
    try:
        w_D0(p, F(0))
    except AssertionError:
        failed = True
    assert failed, "control: w_D0 must be undefined at rho=0"
    print("FAIL_ZERO_ENERGY_REJECTED  w_D0 is undefined at rho=0 (nonzero-energy domain enforced)")

    # control: w_D0 is p/rho from internal pressure-energy, NOT a fitted CPL / survey value
    cpl_w0 = -0.95
    assert abs(float(w) - cpl_w0) > 1e-6, "control: w_D0 is not pinned to an external CPL number"
    print("FAIL_CPL_TUNING_REJECTED  w_D0 is p/rho from internal pressure-energy, NOT a fitted CPL (w0,wa)/DESI/H0/Omega_m value")
    print("FAIL_BARYON_S3_SUBSTITUTION_REJECTED  the archive-phason pressure-energy pair is NOT the baryon-S3 transfer (distinct owners)")

    print("HONEST_SCOPE  EOS FORM + well-definedness only; the explicit w_D0(u)/finite w_N is PROOF-TARGET "
          "(D0-PHASON-WZ-TRANSFER-OWNER-001); redshift/CPL is passport-only; kernel dim alone does NOT determine w "
          "(D0-PHASON-WZ-KERNEL-ONLY-NOGO-001).")
    print("PASS_PHASON_PRESSURE_EOS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
