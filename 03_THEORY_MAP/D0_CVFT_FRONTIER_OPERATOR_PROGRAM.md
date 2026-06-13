# D0 CVFT Frontier Operator Program

This file is not a closure ledger.  It lists operator programs that are allowed
as frontier work only.  New rows from this file must enter the status map as
`FRONTIER`, `OPEN`, or `PROOF-TARGET` until the required Lean theorem,
certificate, or external runner exists.

## F0 — Operator Hardening

Core feedback-return notation:

```text
F_N = P_N U_N^dagger Q_N U_N P_N
Q_N = I - P_N
R_N^resp = D_N^dagger D_N
P_fb = beta^(-1) d_V log Z_N
```

Required identities:

```text
F_N = (Q_N U_N P_N)^dagger (Q_N U_N P_N)
F_N = P_N - (P_N U_N P_N)^dagger (P_N U_N P_N)
F_N >= 0
F_N != 0 iff Q_N U_N P_N != 0
```

Forbidden shortcut:

```text
Q_N != 0 => F_N != 0
```

## F1 — Coefficient-Origin Trace/Residue Program

Target, not theorem:

```text
F_E = P_E U_E^dagger Q_E U_E P_E
Tr(F_E) ?= 359 / phi^2 - phi^(-5)
```

Required before promotion:

- define `P_E`, `Q_E`, `U_E`;
- prove why each edge contributes `phi^(-2)`;
- derive `phi^(-5)` as boundary leakage from an operator;
- run negative controls: `358`, `360`, `phi^(-4)`, `phi^(-6)`;
- separate `alpha_top`, `alpha_D0`, and external QED scheme.

Status: `PROOF-TARGET`.

## F2 — Horizon Emission / Greybody Leakage Program

Forward emission operator:

```text
F_Q^emit(R) = Q_R U_R^dagger P_R U_R Q_R
Gamma_l(omega) = <psi_l,omega | F_Q^emit(R) | psi_l,omega>
```

Still required:

- horizon projection `P_R`, `Q_R`;
- finite capacity-saturated state;
- frequency/angular mode dictionary;
- finite temperature or KMS-like weighting;
- external greybody comparison convention.

Status: `FRONTIER`.  Do not claim the Hawking spectrum is closed.

## F3 — Hadron Resonance Pole Transfer Program

Use compressed/effective dynamics:

```text
U_eff^B = Pi_S3 P U P Pi_S3
```

or Feshbach-Schur form:

```text
H_eff^B(E) = H_PP^B + H_PQ^B (E - H_QQ^B)^(-1) H_QP^B
```

Resonance conditions:

```text
det(I - zeta U_eff^B) = 0
det(E - H_eff^B(E)) = 0
```

Pole interpretation:

```text
lambda_j = exp(-Gamma_j + i E_j)
E_j = arg(lambda_j)
Gamma_j = -log |lambda_j|
```

Status: `FRONTIER`.  Do not replace the baryon/multiplet no-go until the
actual `S3`, spin/flavour, transfer, and passport operators exist.

## F4 — UV Feedback-Tail Cut

Unresolved loop tail:

```text
T_M(z,F_N) = sum_{m>M} z^m/m * Tr(F_N^m)
```

Continuum-safe heat-trace use:

```text
|T_M(z(L),F_N(L))| < delta0^12
```

Finite-algebra regime:

```text
|T_M(z(L),F_N(L))| >= delta0^12
```

Status: `PROOF-TARGET`.  `delta0^12` is a finite readout tolerance for
neglected feedback loops, not a radius of convergence.

## F5 — Dynamic Neutrino Decoherence Candidate

Candidate:

```text
F_nu(V) = F_N + eta_N d_V F_N
```

This remains an external IceCube-passport candidate until:

- the energy scaling is declared before data;
- exposure/flux baseline is fixed;
- no bin/window retuning is used;
- the same IceCube runner is executed.

Status: `FRONTIER`.

## F6 — Gauge-Boundary Commutator Obstruction

Target, not theorem:

```text
<psi,F_N psi> = |Q_N U_N P_N psi|^2 >= m_gap^2 |psi|^2
```

Required:

- non-singlet color states must be explicitly defined;
- boundary projection must be shown not to preserve the isolated color sector;
- prove `m_gap > 0`.

Status: `PROOF-TARGET`.  Do not claim the Yang-Mills mass gap is solved without
this lower-bound theorem.

## F7 — Boundary-Local Holographic Rank Lemma

If `U_N` is local with respect to the finite incidence graph and only
boundary-crossing matrix entries connect `P_N` to `Q_N`, then:

```text
rank(F_N) = rank(Q_N U_N P_N) <= |boundary(P_N,Q_N)|
```

Status: `PROOF-TARGET`.  This supports boundary localization of feedback
entropy, but it does not replace the existing finite `A/4` capacity witness.
