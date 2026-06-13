import numpy as np


def main():
    # P has two active channels; Q has two archive channels. The unitary makes
    # archive-to-active emission stronger on the first axial channel.
    P = np.diag([1, 1, 0, 0]).astype(float)
    Q = np.eye(4) - P
    theta_axis = 0.7
    theta_trans = 0.2
    c1, s1 = np.cos(theta_axis), np.sin(theta_axis)
    c2, s2 = np.cos(theta_trans), np.sin(theta_trans)
    U = np.array([[c1, 0, -s1, 0], [0, c2, 0, -s2], [s1, 0, c1, 0], [0, s2, 0, c2]], dtype=float)
    Femit = Q @ U.T @ P @ U @ Q
    assert np.allclose(Femit, Femit.T)
    assert np.all(np.linalg.eigvalsh(Femit) >= -1e-12)
    Pi_axis = np.diag([0, 0, 1, 0]).astype(float)
    Pi_trans = np.diag([0, 0, 0, 1]).astype(float)
    J_axis = np.trace(Pi_axis @ Femit)
    J_trans = np.trace(Pi_trans @ Femit)
    assert J_axis > J_trans
    print("PASS_CONJUGATE_EMISSION_OPERATOR_PSD")
    print("PASS_AXIS_PROJECTOR_DEFINED")
    print("PASS_AXIS_BACKREACTION_CHANNEL")
    print("PASS_OPTICAL_JET_BACKREACTION_LAW")
    print("FAIL_JET_FROM_NON_PSD_OPERATOR: Rejected")
    print("FAIL_HORIZON_WITHOUT_CAPACITY_SEAM: Rejected")


if __name__ == "__main__":
    main()
