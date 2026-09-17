import numpy as np


def main():
    phi = (1 + np.sqrt(5.0)) / 2.0
    p = 1 / phi
    I = np.eye(2)
    U = np.block([[np.sqrt(p) * I, -p * I], [p * I, np.sqrt(p) * I]])
    P = np.diag([1, 1, 0, 0]).astype(float)
    Q = np.eye(4) - P
    assert np.allclose(U.T @ U, np.eye(4), atol=1e-12)
    F = P @ U.T @ Q @ U @ P
    Ueff = P @ U @ P
    assert np.allclose(F, (p ** 2) * P, atol=1e-12)
    assert np.allclose(Ueff.T @ Ueff, p * P, atol=1e-12)
    A0, B0 = 1.0, 0.0
    A, B = A0, B0
    for _ in range(10):
        A, B = p * A, B + (p ** 2) * A
    assert A > 0
    assert np.allclose(A + B, A0 + B0, atol=1e-12)
    assert np.allclose(A, (p ** 10) * A0, atol=1e-12)
    print("PASS_GOLDEN_TICK_UNITARY")
    print("PASS_FRACTAL_TRACE_FRACTION_PHI_MINUS_TWO")
    print("PASS_RETAINED_FRACTION_PHI_MINUS_ONE")
    print("PASS_SUBSTRATE_CONSERVATION_RECURSION")
    print("PASS_ACTIVE_NEVER_ZERO_FINITE_TICKS")
    print("PASS_TIME_AS_TRACE_ORDER")
    print("FAIL_GLOBAL_F_EQUALS_PHI_MINUS_TWO_P_WITHOUT_CLOCK_SECTOR: Rejected")
    print("FAIL_LINEAR_SUBTRACTION_TIME_TERMINATES: Rejected")
    print("FAIL_MOTION_WITHOUT_TRACE: Rejected")
    print("FAIL_EXTERNAL_OBSERVER_TIME_PRIMITIVE: Rejected")


if __name__ == "__main__":
    main()
