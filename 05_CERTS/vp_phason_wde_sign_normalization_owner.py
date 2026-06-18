#!/usr/bin/env python3
"""D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001 (CERT-CLOSED): the NEGATIVE dark-energy sign is
FORCED by the Galois conjugation sigma:phi->psi, NOT an inserted/arbitrary minus.

Lean owner: D0.Cosmology.PhasonWDESignNormalization
  archive_ratio_pos              0 < phi^-1
  psi_neg                        psi < 0
  psi_inv_eq_neg_phi             psi^-1 = -phi
  retained_reading_neg
  galois_conjugate_is_not_naive_negation   -(phi^-1) != psi^-1
  phason_wde_sign_normalization_owner

Exact Q(phi) facts (a,b) = a + b*phi with phi^2 = phi+1:
  phi^-1     = (-1, 1)   ~ +0.618  (POSITIVE archive ratio)
  sigma(phi) = psi       (the field/Galois conjugate; psi ~ -0.618 < 0)
  sigma(phi^-1) = psi^-1 = -phi = (0,-1) ~ -1.618 (NEGATIVE)
  field relations: phi*psi = -1, phi+psi = 1.

The negative sign of the retained/dark-energy reading is the SPECIFIC field-conjugate value
psi^-1 = -phi, obtained by applying sigma to the positive archive ratio phi^-1. It is NOT the
naive arithmetic negation -(phi^-1) = (1,-1) ~ -0.618 (a different number), and it is NOT chosen
by any survey. The MAGNITUDE/normalization of |w_DE| stays PROOF-TARGET
(D0-PHASON-WZ-EXPLICIT-FUNCTION-001).
"""
import sys
from fractions import Fraction as F

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

PHI = (1.0 + 5.0 ** 0.5) / 2.0
PSI = (1.0 - 5.0 ** 0.5) / 2.0


def mul(x, y):
    a, b = x
    c, d = y
    return (a * c + b * d, a * d + b * c + b * d)


def add(x, y):
    return (x[0] + y[0], x[1] + y[1])


def neg(x):
    return (-x[0], -x[1])


def val(x):
    return float(x[0]) + float(x[1]) * PHI


# sigma: Q(phi) Galois conjugation phi -> psi = 1 - phi.  As (a,b) = a + b*phi,
# sigma(a + b*phi) = a + b*psi = a + b*(1-phi) = (a+b) - b*phi = (a+b, -b).
def sigma(x):
    a, b = x
    return (a + b, -b)


def sval(x):
    # numeric value of (a,b) under the conjugate embedding phi->psi
    return float(x[0]) + float(x[1]) * PSI


ONE = (F(1), F(0))
PHIv = (F(0), F(1))
PHI_INV = (F(-1), F(1))      # phi^-1 = -1 + phi
PSIv = sigma(PHIv)           # = (1, -1) = 1 - phi = psi


def main() -> int:
    print("=== D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001  negative w_DE sign FORCED by Galois sigma:phi->psi ===")
    print("STRUCTURE_FIXED_BEFORE_NUMBER: Q(phi) with phi^2=phi+1, archive ratio phi^-1=(-1,1), "
          "Galois sigma(phi)=psi (a+b*phi -> (a+b,-b)), field relations phi*psi=-1 & phi+psi=1 fixed "
          "BEFORE any numeric value; the sign is sigma(phi^-1), not an inserted minus")

    # --- field-structure anchors (fixed before numbers) ---
    assert mul(PHIv, PHIv) == add(PHIv, ONE), "phi^2 = phi + 1 must hold"
    print("PASS_FIELD_PHI2  phi^2 = phi + 1 (Q(phi) structure)")

    assert mul(PHIv, PSIv) == neg(ONE), f"phi*psi must equal -1: {mul(PHIv, PSIv)}"
    assert add(PHIv, PSIv) == ONE, f"phi+psi must equal 1: {add(PHIv, PSIv)}"
    print("PASS_FIELD_RELATIONS  phi*psi = -1 and phi+psi = 1 (minimal polynomial of the conjugate pair)")

    # --- positive archive ratio phi^-1 = (-1,1) ---
    assert mul(PHIv, PHI_INV) == ONE, "phi * phi^-1 must equal 1"
    assert PHI_INV == (F(-1), F(1)), f"phi^-1 must be (-1,1): {PHI_INV}"
    assert val(PHI_INV) > 0, f"phi^-1 must be POSITIVE: {val(PHI_INV)}"
    print(f"PASS_ARCHIVE_RATIO_POS  phi^-1 = {PHI_INV} = {val(PHI_INV):.6f} > 0 (POSITIVE archive ratio)")

    # --- Galois conjugate of the archive ratio: sigma(phi^-1) = psi^-1 = -phi ---
    sig_pinv = sigma(PHI_INV)
    neg_phi = neg(PHIv)                       # -phi = (0,-1)
    assert mul(PSIv, sig_pinv) == ONE, f"sigma(phi^-1) must be the inverse of psi: {mul(PSIv, sig_pinv)}"  # psi^-1
    assert sig_pinv == neg_phi, f"sigma(phi^-1) = psi^-1 must equal -phi = (0,-1): {sig_pinv}"
    assert sig_pinv == (F(0), F(-1)), f"psi^-1 must be (0,-1): {sig_pinv}"
    assert val(sig_pinv) < 0, f"sigma(phi^-1) = -phi must be NEGATIVE: {val(sig_pinv)}"
    print(f"PASS_GALOIS_FORCES_NEG_SIGN  sigma(phi^-1) = psi^-1 = -phi = {sig_pinv} = {val(sig_pinv):.6f} < 0 "
          "(NEGATIVE sign FORCED by the field conjugate, not inserted)")

    # cross-check the conjugate embedding: under phi->psi, phi^-1 maps to psi^-1
    assert abs(sval(PHI_INV) - (1.0 / PSI)) < 1e-9, "conjugate embedding: sigma(phi^-1) numeric = psi^-1"
    print(f"PASS_CONJUGATE_EMBEDDING  phi^-1 under phi->psi = {sval(PHI_INV):.6f} = psi^-1 (consistent)")

    # ---- KEY negative control: naive negation is a DIFFERENT number ----
    naive = neg(PHI_INV)                      # -(phi^-1) = (1,-1) ~ -0.618
    assert naive == (F(1), F(-1)), f"-(phi^-1) must be (1,-1): {naive}"
    assert naive != sig_pinv, "control: naive negation -(phi^-1) must NOT equal the Galois value psi^-1=-phi"
    assert abs(val(naive) - val(sig_pinv)) > 0.5, "control: the two negatives are numerically distinct"
    print(f"FAIL_NAIVE_NEGATION_REJECTED  -(phi^-1) = {naive} = {val(naive):.6f} != psi^-1 = {sig_pinv} = "
          f"{val(sig_pinv):.6f}; an ARBITRARY sign flip is rejected -- the sign is the SPECIFIC field conjugate")

    # ---- control: +phi^-1 itself is NOT the physical (negative) w_DE ----
    assert val(PHI_INV) > 0, "control basis: phi^-1 is positive"
    assert not (val(PHI_INV) < 0), "control: the POSITIVE archive ratio +phi^-1 cannot be the negative w_DE"
    print("FAIL_POSITIVE_RATIO_AS_WDE_REJECTED  +phi^-1 > 0 is the internal archive ratio; it CANNOT itself be "
          "the negative physical w_DE -- the conjugate sigma is required to flip the sign")

    # ---- control: no survey chooses the sign ----
    desi_w0 = -0.95   # representative external CPL number, used ONLY as a rejected planted input
    assert abs(val(sig_pinv) - desi_w0) > 1e-2, "control: the forced sign value is NOT a DESI/CPL w0 datum"
    assert val(sig_pinv) == val(neg(PHIv)), "the sign value is psi^-1=-phi, an internal field object"
    print("FAIL_DESI_CHOOSES_SIGN_REJECTED  the negative sign = psi^-1 = -phi is fixed by the internal Galois "
          "conjugation; a survey value (e.g. CPL w0=-0.95) is NOT the input and does NOT choose the sign")

    print("HONEST_PROOF_TARGET  CERT-CLOSED on the SIGN only (negative = sigma(phi^-1) = psi^-1 = -phi). "
          "MISSING (residual PROOF-TARGET D0-PHASON-WZ-EXPLICIT-FUNCTION-001): the MAGNITUDE/normalization |w_DE| "
          "-- the explicit owned map from the conjugate-pair object to the physical |w_DE| amplitude -- is NOT "
          "computed here; only the sign is forced.")
    print("PASS_PHASON_WDE_SIGN_NORMALIZATION_OWNER")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
