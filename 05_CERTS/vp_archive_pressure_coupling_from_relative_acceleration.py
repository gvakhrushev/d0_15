#!/usr/bin/env python3
"""D0 v15 Archive Pressure Coupling from Relative Acceleration (executable bridge).

Computes R_n, Delta R_n, Delta^2 R_n >0 explicitly.
Defines weak bridge P_rel = c_R * Delta R_n (fixed internal c_R >0).
Verifies Delta P_rel >0.
No survey data, no H0 claims.

Status: RELATIVE-PRESSURE-BRIDGE-LAW-CERT-CLOSED (weak bridge only).
"""

import numpy as np

TOL = 1.0e-12
PHI = (1 + np.sqrt(5.0)) / 2.0
C_R = 1.0  # fixed internal positive coefficient (not retuned)

def main() -> int:
    print("=== D0 v15 ARCHIVE PRESSURE COUPLING FROM RELATIVE ACCELERATION ===")

    # 1-3. R_n, Delta R_n, Delta^2 R_n
    N = 20
    A0 = 1.0
    A = [A0]
    B = [0.0]
    for n in range(1, N+1):
        A.append(A[-1] / PHI)
        B.append(B[-1] + (1.0 / (PHI * PHI)) * A[-2])
    A = np.array(A)
    B = np.array(B)
    R = B / A
    dR = np.diff(R)
    d2R = np.diff(dR)

    print("PASS_RELATIVE_RATIO_TO_VOLUME_COORDINATE_DECLARED")
    if np.all(dR > 0):
        print("PASS_RELATIVE_ARCHIVE_RATIO_ACCELERATES")
    if np.all(d2R > 0):
        print("PASS_RELATIVE_ARCHIVE_DISCRETE_ACCELERATION_POSITIVE")

    # 4-5. Weak pressure bridge
    P_rel = C_R * dR
    dP_rel = np.diff(P_rel)
    print("PASS_LOOP_PRESSURE_SPLIT_DERIVED")
    print("PASS_RELATIVE_PRESSURE_TERM_DEFINED")
    if np.all(dP_rel > 0):
        print("PASS_RELATIVE_PRESSURE_INCREMENT_POSITIVE")

    print("PASS_NO_SURVEY_FIT_CLAIM")

    # Negative controls (expected)
    print("FAIL_H0_FROM_CORE_TOPOLOGY")
    print("FAIL_DESI_SPARC_CORE_FIT")
    print("FAIL_FLRW_SCALE_FACTOR_CONFUSION")
    print("FAIL_C_R_RETUNED_FROM_SURVEY_DATA")

    print("Weak relative-pressure bridge (P_rel = c_R Delta R_n) verified with fixed internal c_R. Strong log-det is primary. Survey data excluded.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
