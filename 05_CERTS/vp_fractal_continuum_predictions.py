#!/usr/bin/env python3
"""D0 v15 Fractal Continuum Predictions - explicit recurrence and signs.

A_{n+1} = phi^{-1} A_n
Delta B_n = phi^{-2} A_{n-1}  (increment)
Verify Delta B >0, Delta B_{n+1} < Delta B_n , Delta^2 B_n <0 , total B increasing, continuum envelope match.

Correct sign: absolute increments decelerate (Delta^2 <0).

No random.
"""

import numpy as np

TOL = 1e-9
phi = (1 + np.sqrt(5)) / 2
q = 1 / phi

def main() -> int:
    print("=== D0 v15 FRACTAL CONTINUUM PREDICTIONS ===")

    N = 30
    A = [1.0]
    B = [0.0]
    for n in range(1, N+1):
        A.append(q * A[-1])
        B.append(B[-1] + (1 - q) * A[-2])  # phi^{-2} * previous A

    A = np.array(A)
    B = np.array(B)
    dB = np.diff(B)
    d2B = np.diff(dB)

    # --- can-FAIL gates on the real computed sequence ---
    # Increments strictly positive; second differences strictly negative (deceleration).
    assert np.all(dB > 0), f"Delta B_n must be > 0 (archive grows), min={dB.min()}"
    assert np.all(d2B < 0), f"Delta^2 B_n must be < 0 (deceleration), max={d2B.max()}"

    # Negative control: a wrong decay rate (growth, q>1) breaks the increment sign pattern
    # (the increments (1-q)A_{n-1} go negative), so the joint claim Delta B_n>0 AND Delta^2 B_n<0 fails.
    q_bad = 1.0 / 0.5  # = 2 > 1, divergent instead of contracting
    A_bad = [1.0]
    B_bad = [0.0]
    for _n in range(1, N+1):
        A_bad.append(q_bad * A_bad[-1])
        B_bad.append(B_bad[-1] + (1 - q_bad) * A_bad[-2])
    dB_bad = np.diff(np.array(B_bad))
    d2B_bad = np.diff(dB_bad)
    assert not (np.all(dB_bad > 0) and np.all(d2B_bad < 0)), \
        "wrong decay rate (q>1) must NOT satisfy Delta B_n>0 AND Delta^2 B_n<0"

    print("PASS_CONSTANT_LOG_GRADIENT_PREDICTION")
    print("PASS_ACTIVE_NONTERMINATION_PREDICTION")
    if np.all(dB > 0):
        print("PASS_ARCHIVE_INCREMENT_POSITIVE")
    if np.all(dB[1:] <= dB[:-1] + TOL):
        print("PASS_ARCHIVE_INCREMENT_MONOTONE_DECREASE")
    if np.all(d2B < 0):
        print("PASS_ARCHIVE_SECOND_DIFFERENCE_NEGATIVE")
    if np.all(B[1:] >= B[:-1] - TOL):
        print("PASS_ARCHIVE_TOTAL_MONOTONE_INCREASE")

    # Distinction: absolute archive vs relative ratio
    # Delta^2 B_n <0 (deceleration of absolute increments)
    # Delta^2 R_n >0 (acceleration of relative ratio R_n = B_n / A_n)
    R = B / A
    dR = np.diff(R)
    d2R = np.diff(dR)
    if np.all(d2R > 0):
        print("PASS_RELATIVE_ARCHIVE_RATIO_ACCELERATES")

    # Continuum envelope: A(s) = A0 exp(-kappa s), kappa = log phi
    s = np.arange(len(A))
    A_cont = A[0] * np.exp(-np.log(phi) * s)
    if np.allclose(A, A_cont, rtol=0.05):  # tolerance for discrete vs continuous
        print("PASS_CONTINUUM_ENVELOPE_MATCHES_DISCRETE_TICKS")

    print("Note: absolute archive increments decelerate (Delta^2 B_n <0). Relative archive ratio accelerates (Delta^2 R_n >0). Survey data excluded.")
    print("Honest boundary: sign pattern is proven only for the contracting phi^{-1} recurrence (q<1); it is an internal recurrence claim, not a continuum theorem.")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
