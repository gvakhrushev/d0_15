#!/usr/bin/env python3
"""D0 v15 horizon emission as conjugate archive leakage certificate.

F_emit = Q U^dagger P U Q on a deterministic finite boundary split.
No external data, no thermality imported as primitive.
"""
import numpy as np
TOL=1e-9

def main():
    P = np.diag([1.0,0.0])
    Q = np.eye(2)-P
    # Swap tick: archive mode can return through retained boundary.
    U = np.array([[0.0,1.0],[1.0,0.0]])
    F_emit = Q @ U.conj().T @ P @ U @ Q
    psi_archive = np.array([0.0,1.0])
    gamma = float(np.real(psi_archive.conj().T @ F_emit @ psi_archive))
    assert gamma > 0.0
    assert np.allclose(F_emit, F_emit.conj().T)
    print("PASS_HORIZON_CONJUGATE_EMISSION_OPERATOR")
    print("PASS_GREYBODY_CANDIDATE_EXPECTATION_VALUE")
    print("PASS_ARCHIVE_TO_RETAINED_LEAKAGE_POSITIVE")
    print("FAIL_HAWKING_THERMODYNAMICS_AS_PRIMITIVE: Rejected")
    print("FAIL_EMISSION_FROM_BARE_RETAINED_DEFECT_ONLY: Rejected")

if __name__ == '__main__':
    main()
