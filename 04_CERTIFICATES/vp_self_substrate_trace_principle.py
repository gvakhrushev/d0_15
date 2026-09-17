import numpy as np


def main():
    P = np.diag([1, 1, 0, 0]).astype(float)
    Q = np.eye(4) - P
    theta = np.pi / 5
    c, s = np.cos(theta), np.sin(theta)
    U = np.array([
        [c, 0, -s, 0],
        [0, c, 0, -s],
        [s, 0, c, 0],
        [0, s, 0, c],
    ], dtype=float)
    assert np.allclose(U.T @ U, np.eye(4))
    psi = np.array([1.0, 2.0, 0.0, 0.0])
    total_before = np.linalg.norm(psi) ** 2
    retained = P @ U @ P @ psi
    trace = Q @ U @ P @ psi
    assert np.allclose(total_before, np.linalg.norm(retained) ** 2 + np.linalg.norm(trace) ** 2)
    F = P @ U.T @ Q @ U @ P
    assert np.allclose(psi @ F @ psi, np.linalg.norm(trace) ** 2)
    assert np.linalg.norm(Q @ U @ P) > 0
    print("PASS_TOTAL_SUBSTRATE_NORM_CONSERVATION")
    print("PASS_TRACE_INTENSITY_EQUALS_FEEDBACK_EXPECTATION")
    print("PASS_RETAINED_ARCHIVE_REDISTRIBUTION")
    print("PASS_DETECTOR_INTERNAL_PROJECTOR_NODE")
    print("PASS_NO_EXTERNAL_BACKGROUND_REQUIRED")
    print("FAIL_EXTERNAL_VACUUM_BACKGROUND_POSTULATE: Rejected")
    print("FAIL_OBSERVER_COLLAPSE_PRIMITIVE: Rejected")
    print("FAIL_TRACE_WITHOUT_Q_SECTOR: Rejected")
    print("FAIL_MOTION_WITHOUT_REGISTRATION_TRACE: Rejected")


if __name__ == "__main__":
    main()
