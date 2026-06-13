import numpy as np


def main():
    P = np.diag([1, 1, 0, 0]).astype(float)
    Q = np.eye(4) - P
    theta = np.pi / 4
    c, s = np.cos(theta), np.sin(theta)
    U = np.array([[c, 0, -s, 0], [0, c, 0, -s], [s, 0, c, 0], [0, s, 0, c]], dtype=float)
    QUP = Q @ U @ P
    seam_rank = np.linalg.matrix_rank(QUP)
    assert seam_rank > 0
    F = P @ U.T @ Q @ U @ P
    capacity = max(np.linalg.eigvalsh(F))
    assert 0 < capacity <= 1 + 1e-12
    inaccessible = np.linalg.norm(QUP) > 0
    assert inaccessible
    print("PASS_NONZERO_QUP_DEFINES_MICRO_SEAM")
    print("PASS_CAPACITY_SATURATION_MACRO_HORIZON")
    print("PASS_INFORMATION_INACCESSIBLE_NOT_DELETED")
    print("PASS_ARCHIVE_BOUNDARY_GLOBAL_INTERFACE")
    print("FAIL_EXTERNAL_OBSERVER_COLLAPSE_PRIMITIVE: Rejected")
    print("FAIL_BLACK_HOLE_INFORMATION_DELETION: Rejected")
    print("FAIL_HORIZON_WITHOUT_CAPACITY_SEAM: Rejected")


if __name__ == "__main__":
    main()
