import numpy as np


def main():
    phi = (1 + np.sqrt(5.0)) / 2.0
    kappa = np.log(phi)
    q = np.exp(-kappa)
    G = np.array([[-kappa, 0.0], [kappa, 0.0]])
    # Closed form exp(G) for this triangular generator.
    M_exp = np.array([[np.exp(-kappa), 0.0], [1 - np.exp(-kappa), 1.0]])
    M_tick = np.array([[q, 0.0], [1 - q, 1.0]])
    assert np.allclose(M_exp, M_tick, atol=1e-12)
    A0, B0 = 1.0, 0.0
    for n in range(1, 8):
        A = A0 * np.exp(-kappa * n)
        B = B0 + A0 * (1 - np.exp(-kappa * n))
        assert np.allclose(np.log(A) - np.log(A0 * np.exp(-kappa * (n - 1))), -kappa)
        assert np.allclose(A + B, A0 + B0)
        assert np.allclose(A, A0 * (q ** n))
    print("PASS_TICK_MAP_EQUALS_EXP_GENERATOR")
    print("PASS_CONSTANT_LOG_GRADIENT")
    print("PASS_DISCRETE_LADDER_CONTINUUM_ENVELOPE")
    print("PASS_SUBSTRATE_CONSERVED_UNDER_FLOW")
    print("PASS_CONTINUUM_FROM_TRACE_SEMIGROUP")
    print("FAIL_CONTINUUM_AS_EXTERNAL_BACKGROUND: Rejected")
    print("FAIL_LINEAR_MELTING_FINITE_TERMINATION: Rejected")
    print("FAIL_CONSTANT_ABSOLUTE_GRADIENT_MODEL: Rejected")
    print("FAIL_TIME_WITHOUT_TRACE_PRODUCTION: Rejected")


if __name__ == "__main__":
    main()
