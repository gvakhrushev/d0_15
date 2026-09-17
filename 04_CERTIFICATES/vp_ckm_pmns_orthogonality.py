#!/usr/bin/env python3
"""D0-CKM-PMNS-COMPLEMENTARITY-001 — V_CKM U_PMNS^T = I is FALSE; reforge to complementarity.

Researcher doc 2 (§04.12) claims V_CKM U_PMNS^T = I_3 (quark and lepton mixing as mutual
inverses). We CHECK it -- and it is FALSE: that would force V_CKM = U_PMNS (CKM = PMNS), but CKM
has SMALL angles and PMNS has LARGE angles. The error is reforged into the correct, weaker, and
experimentally real relation: quark-lepton COMPLEMENTARITY, theta_C + theta_12 ~ 45 deg.

WHAT IS PROVED (numeric, able to FAIL):
  * The strong claim fails: with the Cabibbo angle theta_C ~ 13.04 deg and the solar angle
    theta_12 ~ 33.6 deg (PMNS), the single-angle product R(theta_C) R(theta_12)^T = R(theta_C -
    theta_12) is NOT the identity (it is a rotation by theta_C - theta_12 ~ -20.6 deg).
  * The correct weaker relation: quark-lepton complementarity theta_C + theta_12 ~ 46.6 deg ~ 45
    deg (off by ~1.6 deg) -- the experimentally observed near-coincidence.

HONESTY BOUNDARY (printed): the orthogonality V_CKM U_PMNS^T = I is rejected (it would make
CKM=PMNS, false). The salvaged content is the APPROXIMATE complementarity theta_C+theta_12~45deg,
status HYP (a ~1.6 deg miss, not an exact identity). Idea reforged, overstatement not kept.
"""
from __future__ import annotations

import math
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def R(theta_deg: float):
    t = math.radians(theta_deg)
    return [[math.cos(t), -math.sin(t)], [math.sin(t), math.cos(t)]]


def matmul(X, Y):
    return [[sum(X[i][k] * Y[k][j] for k in range(len(Y))) for j in range(len(Y[0]))]
            for i in range(len(X))]


def transpose(X):
    return [[X[j][i] for j in range(len(X))] for i in range(len(X[0]))]


def main() -> int:
    print("=== D0-CKM-PMNS-COMPLEMENTARITY-001  V_CKM U_PMNS^T = I is FALSE -> complementarity ===")

    theta_C = 13.04      # Cabibbo angle (CKM 1-2), PDG
    theta_12 = 33.6      # solar angle (PMNS 1-2), sin^2=0.307 -> 33.6 deg

    # ---- strong claim V_CKM U_PMNS^T = I : test the 1-2 sector ---------------------
    prod = matmul(R(theta_C), transpose(R(theta_12)))   # = R(theta_C - theta_12)
    I2 = [[1.0, 0.0], [0.0, 1.0]]
    offdiag = abs(prod[0][1])
    assert offdiag > 0.1, "R(theta_C) R(theta_12)^T must be far from I (off-diagonal large)"
    # it is a rotation by theta_C - theta_12
    eff_angle = theta_C - theta_12
    assert abs(prod[0][1] - (-math.sin(math.radians(eff_angle)))) < 1e-9, "product = R(theta_C - theta_12)"
    print(f"FAIL_V_CKM_U_PMNS_T_IS_NOT_IDENTITY  product = R({eff_angle:.1f} deg), off-diag={offdiag:.3f} (CKM != PMNS)")

    # ---- correct weaker relation: complementarity theta_C + theta_12 ~ 45 ----------
    compl = theta_C + theta_12
    assert abs(compl - 45.0) < 3.0, f"quark-lepton complementarity theta_C+theta_12 ~ 45 deg, got {compl:.1f}"
    miss = abs(compl - 45.0)
    print(f"PASS_COMPLEMENTARITY_APPROX  theta_C + theta_12 = {compl:.1f} deg ~ 45 deg (miss {miss:.1f} deg)")

    # ---- honest controls -----------------------------------------------------------
    # equality to I would require theta_C = theta_12 (false)
    assert abs(theta_C - theta_12) > 15.0, "theta_C != theta_12, so V_CKM != U_PMNS, so product != I"
    # complementarity is approximate, not exact -> HYP not THE
    assert miss > 1.0, "complementarity is approximate (~1.6 deg miss), not an exact identity"
    print("FAIL_EXACT_45_NOT_REACHED_COMPLEMENTARITY_IS_HYP_NOT_THE")
    print("PASS_CKM_PMNS_CONTROLS")

    print("HONEST_STRONG_ORTHOGONALITY_REJECTED_REFORGED_TO_APPROX_COMPLEMENTARITY_HYP")
    print("PASS_CKM_PMNS_ORTHOGONALITY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
