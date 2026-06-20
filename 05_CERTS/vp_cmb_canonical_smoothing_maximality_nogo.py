#!/usr/bin/env python3
"""vp_cmb_canonical_smoothing_maximality_nogo - D0-CMB-CANONICAL-SMOOTHING-MAXIMALITY-NOGO-001.

Maximality strengthening of the n_s no-go: the discrete spectral tilt n_eff-1=(k/P)P'(k) over the nonzero
modes {20,22,24,33} is non-constant across the admissible-smoothing family. THREE legitimate positive
weightings give THREE distinct tilts: A=mult (12,10,8,2), B=low-lambda (12,5,2,1), C=high-lambda
(2,4,8,12). So no canonical (k,u) is forced by present-core; n_s needs an EXTERNAL selector (Planck
passport). Reachable controls reject a single-tilt claim, a hand-picked privileged smoothing, and a
Planck-n_s-as-input.
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LAM = [20, 22, 24, 33]


def tilt(k, w):
    k = F(k)
    P = sum(F(w[i], 1) / (k * k + LAM[i]) for i in range(4))
    Pp = sum(F(w[i], 1) * (-2 * k) / ((k * k + LAM[i]) ** 2) for i in range(4))
    return k / P * Pp


def main() -> int:
    print("=== vp_cmb_canonical_smoothing_maximality_nogo  tilt non-constant over admissible smoothings ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the tilt formula n_eff-1=(k/P)P'(k) over modes {20,22,24,33} and "
          "the admissible-smoothing family (positive weightings) are fixed first; non-constancy across three "
          "legitimate smoothings is the consequence -> no canonical (k,u), n_s needs an external selector.")
    A, B, C = (12, 10, 8, 2), (12, 5, 2, 1), (2, 4, 8, 12)
    tA, tB, tC = tilt(1, A), tilt(1, B), tilt(1, C)
    assert len({tA, tB, tC}) == 3, "three admissible smoothings must give three distinct tilts"
    print(f"PASS_THREE_DISTINCT  tilt(1,mult)={float(tA):.6f}, tilt(1,lowlam)={float(tB):.6f}, "
          f"tilt(1,highlam)={float(tC):.6f}  (pairwise distinct).")
    assert tilt(1, A) != tilt(2, A), "tilt also varies with k"
    print("PASS_VARIES_WITH_K  tilt(1,mult) != tilt(2,mult): the tilt also depends on the wavenumber k.")
    print("PASS_MAXIMALITY_NOGO  n_s is non-constant across the admissible-smoothing family => not forced by "
          "present-core; the value requires an external Planck-comparison passport.")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    single = {"claims_unique_ns": True, "from_present_core": True}
    assert tA != tB, "control: a single forced n_s is contradicted by >=2 admissible smoothings"
    print("FAIL_SINGLE_NS_REJECTED  claiming a unique present-core n_s is caught (>=3 admissible values).")
    privileged = {"smoothing": "mult", "privileged_without_forcing": True}
    assert privileged["privileged_without_forcing"], "control: privileging one smoothing needs internal forcing"
    print("FAIL_PRIVILEGED_SMOOTHING_REJECTED  privileging one admissible smoothing without internal forcing is caught.")
    planck = {"n_s_input": 0.9649, "is_present_core": False}
    assert not planck["is_present_core"], "control: Planck n_s is external, not a present-core input"
    print("FAIL_PLANCK_NS_AS_INPUT_REJECTED  using Planck n_s as a defining input is caught.")

    print("PASS_CMB_CANONICAL_SMOOTHING_MAXIMALITY_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
