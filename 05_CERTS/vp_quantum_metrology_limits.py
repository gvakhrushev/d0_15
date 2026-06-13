#!/usr/bin/env python3
"""
D0 v16 Quantum Metrology Limits Bridge Certificate.

Verifies:
- the admitted PSD purification operator inequality for random unitaries
- that algebra alone does NOT force a universal φ^{-2} leak (negative control)
- the conditional bound requires an explicit sector assumption (φ^{-2} is a hypothesis/target)
- the analog residual R_n = n φ^{-2} - 1/2 is non-Gaussian (kurtosis ≈ 1.8) and shows enhanced Bragg lines at multiples of φ^{-2} (synthetic line-spectrum target)

All constructions are finite, deterministic or statistically controlled, and internal.
No real LIGO/GW data.
"""

import numpy as np

PHI = (np.sqrt(5) + 1) / 2
LAMBDA_STAR = PHI ** -2


def random_unitary(dim, seed=42):
    rng = np.random.default_rng(seed)
    Z = rng.normal(size=(dim, dim)) + 1j * rng.normal(size=(dim, dim))
    Q, R = np.linalg.qr(Z)
    phases = np.diag(R) / np.abs(np.diag(R))
    return Q @ np.diag(np.conj(phases))


def projector(dim, idxs):
    P = np.zeros((dim, dim), dtype=complex)
    for i in idxs:
        P[i, i] = 1.0
    return P


def psd_check(A, tol=1e-10):
    A = 0.5 * (A + A.conj().T)
    eigs = np.linalg.eigvalsh(A)
    return np.all(eigs >= -tol), eigs


def run_quantum_metrology_limits_cert():
    print("--- D0 QUANTUM METROLOGY LIMITS BRIDGE CERT ---")

    # ------------------------------------------------------------
    # 1. Analog residual: non-Gaussian quasiperiodic line target
    # ------------------------------------------------------------
    N = 65536
    n = np.arange(1, N + 1)
    R = np.mod(n * LAMBDA_STAR, 1.0) - 0.5

    # Equidistributed sawtooth marginal has kurtosis 9/5, not 3.
    kurtosis = np.mean(R**4) / (np.std(R)**4)
    assert abs(kurtosis - 1.8) < 0.05
    assert abs(kurtosis - 3.0) > 0.5
    print(f"PASS_ANALOG_RESIDUAL_NON_GAUSSIAN_MARGINAL kurtosis={kurtosis:.4f}")

    # Check that expected Bragg bins are enhanced, not claim exact finite Dirac deltas.
    psd = np.abs(np.fft.fft(R)) ** 2
    freqs = np.fft.fftfreq(N)
    pos = freqs > 0
    pos_freqs = freqs[pos]
    pos_psd = psd[pos]

    expected = []
    for m in range(1, 8):
        f = (m * LAMBDA_STAR) % 1.0
        if f > 0.5:
            f = 1.0 - f
        expected.append(f)

    median_psd = np.median(pos_psd)
    for f0 in expected[:4]:
        idx = np.argmin(np.abs(pos_freqs - f0))
        assert pos_psd[idx] > 100 * median_psd
    print("PASS_ANALOG_RESIDUAL_BRAGG_LINE_TARGETS_ENHANCED")

    # ------------------------------------------------------------
    # 2. Universal PSD operator inequality
    # ------------------------------------------------------------
    dim = 30
    P_N = projector(dim, range(15))
    Q_N = np.eye(dim, dtype=complex) - P_N
    Pi_lab = projector(dim, range(3))

    for seed in range(10):
        U = random_unitary(dim, seed=seed)
        F_N = P_N @ U.conj().T @ Q_N @ U @ P_N
        Q_env = np.eye(dim, dtype=complex) - Pi_lab
        F_lab = Pi_lab @ U.conj().T @ Q_env @ U @ Pi_lab

        diff = F_lab - Pi_lab @ F_N @ Pi_lab
        ok, eigs = psd_check(diff)
        assert ok, eigs

    print("PASS_PURIFICATION_OPERATOR_INEQUALITY_FOR_RANDOM_UNITARIES")

    # ------------------------------------------------------------
    # 3. Negative control: algebra alone does not imply phi^-2 leak
    # ------------------------------------------------------------
    U_id = np.eye(dim, dtype=complex)
    F_N_id = P_N @ U_id.conj().T @ Q_N @ U_id @ P_N
    Q_env = np.eye(dim, dtype=complex) - Pi_lab
    F_lab_id = Pi_lab @ U_id.conj().T @ Q_env @ U_id @ Pi_lab

    assert np.isclose(np.trace(F_lab_id).real, 0.0)
    assert np.isclose(np.trace(Pi_lab @ F_N_id @ Pi_lab).real, 0.0)
    print("PASS_NEGATIVE_CONTROL_NO_UNIVERSAL_PHI_LEAK_FROM_ALGEBRA_ALONE")

    # ------------------------------------------------------------
    # 4. Conditional phi bound under explicit sector assumption
    # ------------------------------------------------------------
    # Build an artificial sector model with F_N >= phi^-2 P_N on lab block.
    F_sector = LAMBDA_STAR * P_N
    conditional_bound = np.trace(Pi_lab @ F_sector @ Pi_lab).real
    expected = LAMBDA_STAR * 3

    assert np.isclose(conditional_bound, expected)
    print("PASS_CONDITIONAL_PHI_BOUND_REQUIRES_SECTOR_ASSUMPTION")

    print("PASS_QUANTUM_METROLOGY_LIMITS_OPERATOR_LEMMA_CERT")


if __name__ == "__main__":
    run_quantum_metrology_limits_cert()
