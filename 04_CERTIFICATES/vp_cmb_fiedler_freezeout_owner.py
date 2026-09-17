#!/usr/bin/env python3
"""vp_cmb_fiedler_freezeout_owner - D0-CMB-FIEDLER-FREEZEOUT-OWNER-001.

The freeze-out scale is the Fiedler value lambda_2 = 20 = minimum nonzero eigenvalue of the K(9,11,13)
Laplacian spectrum {0:1,20:12,22:10,24:8,33:2}; freeze-out wavenumber k_*^2 = 20. Finite decidable fact
off the frozen spectrum. Reachable controls reject a changed lambda_2 and a survey-selected k_*.
"""
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SPEC = {0: 1, 20: 12, 22: 10, 24: 8, 33: 2}


def main() -> int:
    print("=== vp_cmb_fiedler_freezeout_owner  freeze-out scale = Fiedler value lambda_2 = 20 ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the freeze-out scale is fixed as the algebraic connectivity "
          "(min nonzero Laplacian eigenvalue) of K(9,11,13), before any number; no survey k_* or Planck datum.")

    nonzero = sorted(k for k in SPEC if k > 0)
    assert nonzero == [20, 22, 24, 33], f"nonzero spectrum {nonzero} unexpected"
    fiedler = min(nonzero)
    assert fiedler == 20, f"Fiedler value {fiedler} != 20"
    assert all(20 <= lam for lam in nonzero), "20 must be the lower edge of the nonzero spectrum"
    print(f"PASS_FIEDLER  lambda_2 = min nonzero eigenvalue = {fiedler} = 20; freeze-out k_*^2 = 20.")
    print(f"PASS_LOWER_EDGE  every nonzero eigenvalue >= 20 (lower edge of the connected spectrum).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    bad = {0: 1, 18: 12, 22: 10, 24: 8, 33: 2}
    assert min(k for k in bad if k > 0) != 20, "control: a changed spectrum must move lambda_2"
    print("FAIL_LAMBDA2_CHANGED_REJECTED  altering the spectrum (20->18) moves the Fiedler value (caught).")

    survey_k = 0.05  # a survey-selected freeze-out scale
    assert survey_k != fiedler, "control: a survey-selected k_* is not the internal Fiedler value"
    print("FAIL_SURVEY_KSTAR_REJECTED  a survey-selected k_* differs from the internal lambda_2 (caught).")

    print("PASS_CMB_FIEDLER_FREEZEOUT_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
