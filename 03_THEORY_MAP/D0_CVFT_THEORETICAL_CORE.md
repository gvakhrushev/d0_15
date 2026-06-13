# D0 CVFT Theoretical Core

This note is the internal spine layer for closed vacuum feedback thermodynamics.
It sits after the finite proof/operator spine and before sector projections in
matter, time, gravity and cosmology.

## 1. Standard-Language Setup

D0 is treated as a finite observable system with a retained sector and a
traced-out complement. The vacuum is not an external mirror or empty medium; it
is the finite retained/traced split induced by bounded observation.

## 2. Retained/Traced Finite System

For a finite support:

```text
H_N = H_N^ret + H_N^tr
P_N + Q_N = I
P_N Q_N = 0
```

`P_N` is the terminally addressable sector. `Q_N` is the unresolved complement.
The positive readout/response operator remains `R_resp = D_N^dagger D_N`.

## 3. Feedback-Return Operator

The feedback-return operator is named `F_N`, not `R_N`, to avoid conflict with
positive response:

```text
F_N = P_N U_N^dagger Q_N U_N P_N
```

Assuming `P_N=P_N^dagger=P_N^2`, `Q_N=I-P_N`, and `U_N^dagger U_N=I`, the
unitarity-defect identities are:

```text
F_N = (Q_N U_N P_N)^dagger (Q_N U_N P_N)
F_N = P_N - (P_N U_N P_N)^dagger (P_N U_N P_N)
```

Consequences:

```text
F_N >= 0
F_N = 0 iff Q_N U_N P_N = 0
```

Do not infer `F_N != 0` from `Q_N != 0` alone.  Non-Hermitian behavior belongs
only to effective projected transfer reductions such as `U_eff=P_N U_N P_N` or a
declared Feshbach-Schur operator.

## 4. Resolvent and Determinant

The finite feedback resolvent is:

```text
(I - z F_N)^(-1)
```

It exists when `z^(-1)` is not in the finite spectrum of `F_N`.  The Neumann and
log-det expansions are valid only in the subcritical regime:

```text
|z| rho(F_N) < 1
(I - z F_N)^(-1) = sum_{m>=0} z^m F_N^m
-log det(I - z F_N) = sum_{m>=1} z^m/m * Tr(F_N^m)
```

Near-critical behavior is a pole/saturation regime, not the same theorem as the
regular loop expansion.  The determinant itself is not expanded as
`sum (-z)^m Tr(F_N^m)`.

## 5. Feedback Free Energy and Finite Volume Derivative

The partition function is:

```text
Z_N(beta,z,V) = Tr exp(-beta Delta_N(V)) det(I - z F_N(V))^(-1)
```

The finite pressure split is:

```text
P_fb = P_heat + P_loop
P_heat = beta^(-1) d_V log Tr exp(-beta Delta_N(V))
P_loop = beta^(-1) d_V log det(I - z F_N(V))^(-1)
```

`d_V` is a declared finite deformation derivative: graph-volume, boundary-cut,
spectral-window, terminal-capacity or survey-transfer coordinate.  It must be
one of:

```text
finite difference: (A(V+epsilon_N)-A(V))/epsilon_N
smooth finite matrix family: V -> A_N(V), entrywise differentiable
```

## 6. Variational Susceptibility

The feedback action component is:

```text
S_fb = -log det(I - z F_N)
Pi_fb = z(I - z F_N)^(-1)
dS_fb = Tr(Pi_fb dF_N)
```

`Pi_fb` is susceptibility. Pressure, stress, decay width and cosmology transfer
are sector projections of it.

## 7. Pole Classification and Matter

Matter candidates are terminally stabilized feedback poles:

```text
F_N psi_j = r_j psi_j
lambda_j = z r_j
|lambda_j| near 1 and P_term psi_j = psi_j
```

Finite pole data are internal. External particle masses require a transfer map
from finite pole/action data into an SI or PDG convention.

Complex resonance data are not read from bare positive `F_N`.  They require
compressed/effective dynamics:

```text
U_eff = P_N U_N P_N
U_eff psi_j = lambda_j psi_j
lambda_j = exp(-Gamma_j + i E_j)
E_j = arg(lambda_j)
Gamma_j = -log |lambda_j|
```

## 8. Feedback Entropy Channel and Time Arrow

Time is not entropy itself. The time arrow is the ordering induced by repeated
feedback/coarse-grained updates when the update is normalized or embedded in an
admissible channel and entropy is assigned to the dephased finite-window state.

## 9. Pressure-Capacity Gravity

Finite spectral geometry gives the gravity carrier. Feedback pressure gives the
source/regime selector. Boundary capacity gives the horizon/collapse condition:

```text
P_fb > P_cap : expansion/acceleration regime
P_fb = P_cap : stationary boundary or horizon balance
P_fb < P_cap : contraction/collapse/local capacity saturation
```

## 10. Two-Mode S_DE Reduction

`S_DE` is the two-mode reduction of the feedback-pressure transfer operator, not
a fitted polynomial. The frozen characteristic is:

```text
160 lambda^2 - 480 lambda + 359
```

## 11. Boundary-Derivative Correction

DESI/SPARC failures do not authorize root, window or arbitrary-kernel refits.
The theorem-grade diagnostic is:

```text
F_N^(partial) = F_N^(2) + eta_N d_V F_N
eta_N = d_V Tr(F_N^2) / d_V Tr(F_N)
```

The missing term is boundary-derivative feedback.

## 12. Exceptional-Point Transfer

Exceptional-point language belongs to effective two-mode pressure-transfer
reductions only. It is a transfer-regime diagnostic, not a claim that a global
external parameter literally does not exist.

## 13. Feedback Halo-Response Candidate

SPARC-style halo response is a non-terminal feedback-pressure response candidate.
The allowed object is a boundary-deformation pressure gradient, not a fitted dark
particle catalogue and not a fitted halo kernel.

## 14. Finite Scattering Resolvent

The finite scattering kernel is:

```text
S_fi^D0(z) = <f|(I - z F_N)^(-1)|i>
```

Continuum perturbative loops are bridge representatives of repeated finite
complement-return amplitudes when the QFT bridge exists.

## 15. No-Overclaim Rules

Core theorem statements stay in finite operators. RG, spectral action,
cosmology, gauge readouts and external data comparisons are assembled only in
`D0.Bridge.InterpretationSpine.InterpretationPackage` or in empirical passport
rows.
