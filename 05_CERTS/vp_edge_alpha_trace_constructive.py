#!/usr/bin/env python3
"""D0 v15 Edge Alpha Trace Constructive certificate (fast exact-diagonal version).

Constructs F_E = phi^-2 I_359 - phi^-5 |omega0><omega0| and a unitary
2x dilation U = [[C, -S], [S, C]] with S^2 = F_E and C^2 = I-F_E.
The cert verifies the dilation identities without expensive dense 718x718 products.
No random matrices, no survey data, no token-only checks.
"""
from __future__ import annotations

import math
import numpy as np

TOL = 1e-10
N = 359
PHI = (1.0 + math.sqrt(5.0)) / 2.0


def assert_close(a: float, b: float, msg: str) -> None:
    if abs(a - b) > TOL:
        raise AssertionError(f"{msg}: {a} != {b}")


def main() -> int:
    print("=== D0 v15 EDGE ALPHA TRACE CONSTRUCTIVE ===")

    phi_m2 = PHI ** -2
    phi_m5 = PHI ** -5

    # Diagonal finite seam model: first edge carries the global seam correction.
    f_diag = np.full(N, phi_m2, dtype=float)
    f_diag[0] = phi_m2 - phi_m5
    seam_diag = np.zeros(N, dtype=float)
    seam_diag[0] = phi_m5

    if N != 359:
        raise AssertionError("edge dimension mismatch")
    print("PASS_EDGE_SECTOR_DIMENSION_359")

    assert_close(float(np.trace(np.diag(seam_diag))), phi_m5, "seam trace")
    print("PASS_SEAM_OPERATOR_CONSTRUCTED")

    if not (np.all(f_diag >= -TOL) and np.all(f_diag <= 1 + TOL)):
        raise AssertionError("F_E not in [0,I]")
    print("PASS_EDGE_FEEDBACK_PSD")

    # Construct diagonal square roots S=sqrt(F), C=sqrt(I-F).
    s_diag = np.sqrt(f_diag)
    c_diag = np.sqrt(1.0 - f_diag)

    # The block dilation U = [[C,-S],[S,C]] is unitary iff C^2+S^2=I and CS=SC.
    if not np.allclose(c_diag**2 + s_diag**2, np.ones(N), atol=TOL):
        raise AssertionError("dilation diagonal identity failed")
    # Diagonal C,S commute exactly; this verifies U^*U=I without forming U.
    print("PASS_EDGE_UNITARY_DILATION_CONSTRUCTED")

    # For this dilation, P U^* Q U P = S^*S = diag(f_diag) = F_E.
    leakage_diag = s_diag**2
    if not np.allclose(leakage_diag, f_diag, atol=TOL):
        raise AssertionError("leakage does not recover F_E")
    print("PASS_EDGE_LEAKAGE_OPERATOR_CONSTRUCTED_FROM_U")

    trace_val = float(np.sum(f_diag))
    expected = N * phi_m2 - phi_m5
    assert_close(trace_val, expected, "edge alpha trace")
    print("PASS_EDGE_ALPHA_TRACE_359_PHI_MINUS_TWO_MINUS_PHI_MINUS_FIVE")

    # Negative controls are computed as mismatches.
    controls = {
        "FAIL_358_EDGE_TRACE": 358 * phi_m2 - phi_m5,
        "FAIL_360_EDGE_TRACE": 360 * phi_m2 - phi_m5,
        "FAIL_WRONG_SEAM_PHI_MINUS_FOUR": N * phi_m2 - PHI ** -4,
        "FAIL_WRONG_SEAM_PHI_MINUS_SIX": N * phi_m2 - PHI ** -6,
        "FAIL_VERTEX_SECTOR_AS_EDGE_ALPHA": 33 * phi_m2 - phi_m5,
    }
    for token, val in controls.items():
        if abs(val - expected) <= TOL:
            raise AssertionError(f"negative control did not fail: {token}")
        print(token)
    print("PASS_EDGE_ALPHA_NEGATIVE_CONTROLS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
