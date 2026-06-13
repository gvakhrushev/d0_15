import numpy as np


def main():
    P = np.diag([1, 1, 0, 0]).astype(float)
    Q = np.eye(4) - P
    theta = 0.37
    c, s = np.cos(theta), np.sin(theta)
    U = np.array([[c, 0, -s, 0], [0, c, 0, -s], [s, 0, c, 0], [0, s, 0, c]], dtype=float)
    A = Q @ U @ P
    F = A.T @ A
    assert np.allclose(F, P @ U.T @ Q @ U @ P)
    psi = np.array([2.0, -1.0, 0.0, 0.0])
    assert np.allclose(psi @ F @ psi, np.linalg.norm(A @ psi) ** 2)
    # Rank-one linear cut in a two-dimensional phase disk is not rotation invariant.
    linear_cut = np.diag([1.0, 0.0])
    rot = np.array([[0.0, -1.0], [1.0, 0.0]])
    assert not np.allclose(rot @ linear_cut @ rot.T, linear_cut)
    print("PASS_FEEDBACK_IS_GRAM_OPERATOR")
    print("PASS_TRACE_INTENSITY_IS_NORM_SQUARE")
    print("PASS_PHASE_BLIND_READOUT_QUADRATIC")
    print("PASS_LINEAR_CUT_BREAKS_PHASE_INVARIANCE")


if __name__ == "__main__":
    main()
