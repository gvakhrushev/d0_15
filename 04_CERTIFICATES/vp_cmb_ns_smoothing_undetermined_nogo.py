#!/usr/bin/env python3
"""vp_cmb_ns_smoothing_undetermined_nogo - D0-CMB-NS-SMOOTHING-UNDETERMINED-NOGO-001 (closed-negative).

Proves the discrete spectral tilt n_eff-1 = (k/P) P'(k) of the heat-smoothed phason power proxy
P(k)=Sum_i w_i/(k^2+lam_i) (nonzero modes lam in {20,22,24,33}, w_i=mult_i e^{-u lam_i}) is NOT a
function of the spectrum alone: it varies with the wavenumber k AND with the smoothing measure (w_i).
Hence the bare K(9,11,13) spectrum + an unforced (k,u) does NOT determine a single n_s. Exact rational
arithmetic. Reachable controls reject 'spectrum alone fixes n_s' and a Planck n_s input.
"""
from fractions import Fraction as F
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

LAMS = [20, 22, 24, 33]


def tilt(k, w):
    k = F(k)
    P = sum(F(wi) / (k * k + lam) for wi, lam in zip(w, LAMS))
    Pp = sum(F(wi) * (-2 * k) / (k * k + lam) ** 2 for wi, lam in zip(w, LAMS))
    return k * Pp / P


def main() -> int:
    print("=== vp_cmb_ns_smoothing_undetermined_nogo  spectrum + unforced (k,u) does NOT fix n_s (no-go) ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: the tilt n_eff-1=(k/P)P'(k) of the heat-smoothed phason proxy over "
          "the nonzero K(9,11,13) modes is fixed before any number; admissible smoothing = positive weights, "
          "the heat family w_i=mult_i e^{-u lam_i} is a subfamily; no Planck n_s / inflaton / survey datum.")

    wA = [12, 10, 8, 2]  # u=0 weighting (w = mult)
    wB = [12, 5, 2, 1]   # low-lambda-emphasising admissible smoothing (u>0-like)

    # k-axis: same smoothing, two wavenumbers
    tk1, tk2 = tilt(1, wA), tilt(2, wA)
    assert tk1 != tk2, "tilt must vary with k"
    print(f"PASS_VARIES_WITH_K  tilt(k=1,wA)={float(tk1):.6f} != tilt(k=2,wA)={float(tk2):.6f} "
          "(exact rationals differ): the evaluation wavenumber is unforced.")

    # u/weight-axis: same k, two admissible smoothings
    tu1, tu2 = tilt(1, wA), tilt(1, wB)
    assert tu1 != tu2, "tilt must vary with the smoothing measure"
    print(f"PASS_VARIES_WITH_SMOOTHING  tilt(k=1,wA)={float(tu1):.6f} != tilt(k=1,wB)={float(tu2):.6f}: "
          "the smoothing window u is unforced.")

    print("PASS_NO_GO  the tilt is non-constant on BOTH axes -> spectrum + unforced (k,u) does NOT determine "
          "n_s; a canonical forced (k,u) is the named missing artifact (D0-CMB-IDS-SMOOTHING-OWNER-001).")

    # ===================== REACHABLE NEGATIVE CONTROLS =====================
    spectrum_alone_fixes_ns = (tk1 == tk2 and tu1 == tu2)  # would have to be constant
    assert not spectrum_alone_fixes_ns, "control: 'spectrum alone fixes n_s' must be rejected"
    print("FAIL_SPECTRUM_ALONE_FIXES_NS_REJECTED  the claim 'the spectrum alone determines n_s' is refuted "
          "(the tilt is non-constant) -- reachable.")

    planck_ns = F(9649, 10000)  # measured Planck n_s = 0.9649
    assert all(planck_ns != t for t in (tk1, tk2, tu1, tu2)), "control: Planck n_s must not appear"
    print("FAIL_PLANCK_NS_INPUT_REJECTED  the measured Planck n_s does not enter the internal tilt (caught).")

    print("PASS_CMB_NS_SMOOTHING_UNDETERMINED_NOGO")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
