# D0 v16 Quantum Metrology Limits

**Status:** THEOREM-TARGET / OPERATOR-LEMMA-CERT

**Claim class:** conditional metrology extension

## Admitted operator lemma

Let (P_N + Q_N = I), (P_N Q_N = 0), and let the laboratory projector satisfy (Π_lab ≤ P_N). Define

\[
Q_{env} = I - \Pi_{lab} = Q_N + (P_N - \Pi_{lab})
\]

and

\[
F_{lab} = \Pi_{lab} U^\dagger Q_{env} U \Pi_{lab}.
\]

Then

\[
F_{lab} \succeq \Pi_{lab} F_N \Pi_{lab},
\qquad
F_N = P_N U^\dagger Q_N U P_N.
\]

The difference is positive semidefinite because

\[
\Pi_{lab} U^\dagger (P_N - \Pi_{lab}) U \Pi_{lab} = K^\dagger K.
\]

## Conditional purification bound

If a D0 clock/metrology sector (C ⊆ P_N) satisfies

\[
F_N \vert_{\mathcal C} \succeq \lambda_* P_{\mathcal C},
\]

then every laboratory projector (Π_lab ≤ P_C) obeys

\[
\operatorname{Tr}(F_{lab}) \ge \lambda_* \operatorname{rank}(\Pi_{lab}).
\]

The special value (λ_* = ϕ^{-2}) is a D0 sector hypothesis / prediction target, not a consequence of the PSD lemma alone.

## Analog residual prediction

The residual

\[
R_n = n \varphi^{-2} - \frac12
\]

is non-Gaussian in its marginal distribution and quasiperiodic in time. Its idealized line spectrum is pure point, with Bragg frequencies

\[
f_m = m \varphi^{-2} \pmod{1}.
\]

This is a metrological prediction target. Instrumental aliasing, finite sampling, damping, and calibration lines must be controlled before any physical claim is made.

## Integration notes

- PSD purification inequality → OPERATOR-LEMMA-CERT
- φ^{-2} purification flux → CONDITIONAL-THEOREM-TARGET
- phason Bragg line spectrum → METROLOGY-PREDICTION-TARGET

See executable certificate `05_CERTS/vp_quantum_metrology_limits.py` for the finite verification of the operator inequality and the negative control showing that algebra alone does not force the φ^{-2} leak. The conditional bound and the Bragg-line target require the additional D0 sector hypothesis.