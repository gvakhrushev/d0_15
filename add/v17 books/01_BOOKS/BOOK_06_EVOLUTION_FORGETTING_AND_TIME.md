# BOOK 06: Evolution, Forgetting, and Time

**D0 Theory — Finite Readout Information Mechanics**  
**Version 16 — publication draft**

> **Publication status.** Book 06 defines time as ordered finite registration, forgetting as typed active-to-archive quotient, and archive evolution as the accumulation of completed trace. It uses the core operator calculus of Books 01--03 and does not introduce an independent background time continuum.
>
> **Claim discipline.** Entropy, RG, laboratory analogues, and metrological exports are admissible only after the relevant finite channel, quotient, bridge, or passport target has been declared. External bridges are not promoted to core closure in this book.

---

## 06.1 Purpose and dependencies

Book 06 supplies the temporal layer of D0. Its role is not to add a new background parameter. Its role is to specify how completed finite registrations become an ordered history and how discarded degrees of freedom become archive trace.

The dependency chain is:

| Input | Owner | Use in Book 06 |
|---|---|---|
| Terminal role space and phase-unfolding chain | Book 01 | ordered non-periodic support |
| Feedback-return operator \(F_N\) and invariant calculus | Book 02 | active/archive leakage and pressure |
| Finite scene update | Book 03 | tick-level scene dynamics |
| Claim and certificate discipline | Book 05 | admissibility of evolution and bridge claims |
| Relative archive acceleration and cosmological transfer | Book 08 | continuum envelope and export |

Book 06 therefore treats time as an internal order relation on finite records.

---

## 06.2 Tomita-Takesaki Modular Time and the Entanglement Flow

D0 strictly rejects the existence of a background temporal parameter t. Time emerges algebraically through the **Tomita-Takesaki Modular Flow**.

Whenever the holographic carrier is partitioned into a Retained (Active) sector P_N and a Traced (Archive) sector Q_N, the restriction of the pure topological state to the active boundary generates a highly entangled thermal density matrix ρ_active. By the Tomita-Takesaki theorem of von Neumann algebras, this state uniquely defines a modular operator Δ, which intrinsically generates a one-parameter group of automorphisms:

σ_s(O) = Δ^{is} O Δ^{-is}.

In D0, **Time is exactly this Modular Flow**. Ordered finite registration is merely the discrete spectrum of Δ. The fractal tick decay rule (A_{n+1} = φ^{-1} A_n) is the rigorous algebraic consequence of the modular operator transporting symplectic area into the Archive. Time does not "pass"; Time is the thermodynamic effort required to maintain the holographic boundary against the growing entanglement entropy of the Bulk.

---

## 06.3 Active/archive decomposition

At each finite registration depth there is an active/archive split

\[
\mathcal H_{total}=\mathcal H_{active}\oplus\mathcal H_{archive},
\qquad
P_N+Q_N=I,
\qquad
P_NQ_N=0.
\]

The active sector contains the retained finite state capable of further readout. The archive sector contains degrees of freedom removed from active comparison by the declared quotient: dephased phase data, unresolved address tails, null directions, inaccessible comparison data, and discarded correlations.

A finite readout state may be represented schematically as

\[
\psi_{active}(N)=P_N\,\psi_{support}(N).
\]

The archive is not non-existence. It is the complement of retained readout under a specified finite split.

## 06.2B KMS Duality and the Natural Obstruction to Perturbative Quantization of Gravity (Core Theorem)

Time is the Tomita-Takesaki modular flow \(\Delta^{is}\), which uniquely defines a KMS thermal state. Geometry emerges from the heat-trace of the Master Bootstrap Functional \(\mathcal B_N\) at inverse temperature \(\beta\).

By the KMS condition, imaginary time \(\beta\) is exactly dual to the modular flow. Therefore spacetime geometry and Time are dual representations of the same thermal KMS state of the Fibonacci fusion algebra. Gravity is the thermodynamic equation of state of this flow. Attempting to quantize the metric tensor (postulating a graviton) is a category error equivalent to attempting to construct a coherent quantum superposition of a purely thermal temperature.

Certificate: `vp_kms_duality_gravity_thermal.py`

## 06.2E Relational Time as the Feshbach-Schur Delay (Core Theorem)

Recent empirical and theoretical advances in relational quantum dynamics (e.g., "Toy Universe" entanglement models, 2026) strongly indicate that global time does not exist. D0 Theory formalizes this illusion algebraically via the Schur Complement.

**Theorem 06.2E (Time as Archive Circulation Delay, D0.Core).**
The global state of the finite holographic carrier is static under the unitary evolution $U_N$. Time emerges exclusively for an observer restricted to the Active Transport boundary ($P_N$). 
Evaluating the effective evolution operator $\mathcal{W}_{eff}$ for the Active sector necessitates tracing over the 30-dimensional Sterile Archive ($Q_N$). The solution is strictly the Feshbach-Schur complement:
\[ \mathcal{W}_{eff} = P_N U_N P_N + P_N U_N Q_N (I - Q_N U_N Q_N)^{-1} Q_N U_N P_N. \]
Expanding the Archive resolvent via the Neumann series reveals the discrete structure of temporal flow:
\[ \mathcal{W}_{eff} = P_N U_N P_N + \sum_{k=0}^{\infty} (P_N U_N Q_N)(Q_N U_N Q_N)^k (Q_N U_N P_N). \]
The phenomenological "passage of time" is algebraically identical to the discrete index $k$. Time is the algorithmic delay caused by quantum phase information circulating within the Sterile Archive ($(Q U Q)^k$) before its eventual observable return to the Active Boundary.

---

## 06.4 Forgetting maps

**Definition 6.3 (Forgetting map).**  
A forgetting map is a typed quotient from active comparison data to retained record data, together with an archive complement. Depending on the declared sector it may be a conditional expectation, a partial trace, a Wilsonian coarse-graining map, or an entropy-selected coupling.

The generic form is

\[
\Delta_N:\rho_N\longmapsto\Delta_N(\rho_N),
\]

where \(\Delta_N(\rho_N)\) preserves the invariant required for the next finite registration and removes the information that is not stable under the declared readout.

For a finite subsystem \(A\), entropy may be assigned only after the finite-window dephasing/coarse-graining map has been declared:

\[
S_A^{D0}=-\operatorname{Tr}\!\left(\rho_A^{fw}\log \rho_A^{fw}\right).
\]

The classical regime is the regime in which repeated typed quotients stabilize an effectively commuting record algebra:

\[
\Delta_N(\rho_N)\text{ stable under repeated finite records}
\quad\Rightarrow\quad
\text{classical readout algebra}.
\]

---

## 06.5 Normalized feedback channels and entropy arrow

The raw feedback update may be non-trace-preserving. Entropy monotonicity is therefore not a property of an unnormalized raw operator.

When the positive denominator exists, the normalized channel form is

\[
\widehat\Phi_N(\rho)=
\frac{\Phi_N(\rho)}{\operatorname{Tr}\Phi_N(\rho)}.
\]

**Rule 6.4 (Entropy discipline).**  
An entropy-arrow statement is admissible only when the channel is normalized, the dephasing or coarse-graining map is declared, and the entropy functional is evaluated on the resulting finite-window state.

Thus:

\[
\text{time}\ne\text{entropy}.
\]

Time is ordered registration. Entropy is a functional of a declared coarse-grained record state.

---

## 06.6 Fractal tick evolution

The decay law \(A_{n+1} = \varphi^{-1} A_n\) follows directly from the detector asymmetry derived in Book 01 §01.5: the retained fraction per tick is exactly \(p = \varphi^{-1}\), as required by the positive self-return condition \(p + p^2 = 1\). Thus the fractal tick envelope is not postulated but inherited from the primitive detector.

Let \(A_n\) denote the active retained component and \(B_n\) the accumulated archive component after \(n\) ticks. The D0 fractal tick envelope is

\[
A_{n+1}=\varphi^{-1}A_n,
\]

so the per-tick archive increment is

\[
B_{n+1}=B_n+\left(1-\varphi^{-1}\right)A_n
      =B_n+\varphi^{-2}A_n.
\]

With \(A_0>0\) and \(B_0=0\), the closed forms are

\[
A_n=A_0\varphi^{-n},
\qquad
B_n=A_0(1-\varphi^{-n}).
\]

The relative archive ratio is

\[
R_n=\frac{B_n}{A_n}=\varphi^n-1.
\]

In a continuum envelope parameter \(s\), this becomes

\[
A(s)=A_0e^{-s\log\varphi},
\qquad
R(s)=e^{s\log\varphi}-1.
\]

Consequently,

\[
R''(s)=(\log\varphi)^2e^{s\log\varphi}>0.
\]

**Interpretation.**  
The active component decays exponentially in finite tick depth. The relative archive ratio accelerates because the denominator is the shrinking retained component. This is the time-layer form of active/archive evolution; Book 08 handles its continuum and cosmological transfer.

---

The relative archive acceleration derived here is the direct source of the internal cosmological mechanism in Book 08; external survey comparison remains strictly passport work.

## 06.7 Phase-unfolding inheritance

The full Phase-Unfolding Master Chain is owned by Book 01. Book 06 uses only its temporal consequence: the ordered runtime is a non-periodic finite return structure generated by irrational \(\varphi\)-support.

The key return moduli inherited from Book 01 are

\[
q_T=44,
\qquad
q_{EW}=710.
\]

These values are not re-derived in Book 06. They are referenced as phase-return data for downstream evolution, bridge, and passport layers.

---

## 06.8 Archive evolution and finite scene update

A finite scene update has two components:

1. active transport inside the retained sector;
2. archive production through the complement.

The active transport step is represented by the unitary tick operator followed by the active projector,

\[
\psi_{n+1}^{active}=P_{N+1}U_N\psi_n^{active}.
\]

The archive production is measured by the positive feedback-return operator owned by Book 02,

\[
F_N=(Q_NU_NP_N)^\dagger(Q_NU_NP_N).
\]

Book 06 uses this operator to define the time direction of trace accumulation: completed readout increases the archive ledger associated with the declared split.

## 06.8a The Toral Automorphism as the Modular Time Generator

The Tomita-Takesaki modular flow is generated explicitly by the integer toral automorphism matrix:
\[ T = \begin{pmatrix} 0 & 1 \\ 1 & -1 \end{pmatrix}. \]
Its characteristic polynomial is \(\chi_T(\lambda) = \lambda^2 + \lambda - 1\), yielding the exact symplectic spectrum \(\{ \varphi^{-1}, -\varphi \}\). 
Time evolution is the action of \(T^n\) upon the finite state. The fractal decay of the active sector and the accumulation of the archive trace are exact eigenvectors of this discrete automorphism. Time is therefore the invariant trace sequence of a deterministic, non-invertible Fibonacci fusion process.

The archive increment of a finite state \(\rho_N\) is measured schematically by

\[
\Delta B_N(\rho_N)=\operatorname{Tr}(F_N\rho_N),
\]

subject to the sector-specific normalization and quotient rules of Book 05.

---

## 06.9 RG as typed bridge

Renormalization-group language is admissible in D0 only as a typed bridge. It must specify:

| Required item | Meaning |
|---|---|
| retained algebra | what is kept active |
| quotient map | what is archived or coarse-grained |
| scale parameter | finite depth, window, or bridge scale |
| invariant | what is preserved under transfer |
| loss rule | what is discarded into archive |

A continuous RG flow is not a primitive D0 object. It is an envelope or bridge description of a finite sequence of typed quotients.

The admissible schematic form is

\[
\mathcal A_{N+1}=\mathcal R_N(\mathcal A_N),
\]

where \(\mathcal R_N\) is a declared retained/archive transfer map. Any continuum beta function is a bridge export of this finite sequence, not a core replacement for it.

---

## 06.10 Active-medium laboratory bridge

Dusty-plasma and beam-plasma systems provide a laboratory bridge for the active-medium principle. In that bridge, the readout source and the trace medium co-produce the observed channel: dust can absorb beam energy, contract the active plasma volume, clear channels, and exhibit core/periphery sign-switch behavior.

This bridge supports the following D0 time-layer lesson:

\[
\text{detector medium is active, not a passive coordinate background.}
\]

The bridge remains external. Golden mass-loss and acoustic \(\log\varphi\) claims are prediction targets requiring separate laboratory protocols. They are not promoted to core time theorems in Book 06.

---

## 06.11 Interface to later books

| Downstream layer | Interface from Book 06 |
|---|---|
| Book 07 gravity/seams | archive accumulation and active-medium channel clearing |
| Book 08 cosmology | continuum envelope of fractal tick and archive ratio |
| Book 09 gravitational waves | finite registration, detector-frame transfer, negative-control discipline |
| external laboratory bridges | active-medium trace production and falsifiable prediction targets |

Book 06 therefore supplies the temporal grammar needed by the later physical books, while leaving their bridge and passport claims to their own owners.

---

## 06.12 Time-layer summary

| Concept | Formula / definition | Status | Owner |
|---|---:|---|---|
| finite registration time | \(t_n=n\) | core definition | Book 06 |
| record order | \(r_i\prec r_j\) | core definition | Book 06 |
| active/archive split | \(P_N+Q_N=I\) | inherited core split | Books 02, 06 |
| forgetting map | \(\Delta_N:\rho_N\mapsto\Delta_N(\rho_N)\) | typed quotient | Book 06 |
| normalized feedback channel | \(\widehat\Phi_N=\Phi_N/\operatorname{Tr}\Phi_N\) | admissibility rule | Books 05, 06 |
| fractal active tick | \(A_{n+1}=\varphi^{-1}A_n\) | invariant time envelope | Books 06, 08 |
| archive increment | \(B_{n+1}=B_n+\varphi^{-2}A_n\) | invariant time envelope | Books 06, 08 |
| relative archive ratio | \(R_n=\varphi^n-1\) | archive acceleration | Book 08 |
| phase return moduli | \(q_T=44,\ q_{EW}=710\) | inherited reference | Book 01 |
| RG | typed retained/archive bridge | bridge only | Books 06, 08 |
| dusty-plasma active medium | channel-clearing laboratory bridge | passport seed | Books 06, 07 |

---

## 06.13 Closing statement

Book 06 closes the internal time grammar of D0: time is the order of completed finite registrations; forgetting is a typed quotient; archive evolution is the accumulation of trace; and continuum time is a stable envelope of finite tick depth.

No external laboratory, cosmological, or interferometric claim is closed by this book alone. Those claims require their own bridge maps, certificates, data manifests, and falsification rules.

## 06.14 Time as the Ordering Principle of the Entire D0 Corpus

Finite registration time is the ordering rule that prevents later books from reversing proof direction. A bridge or passport may test a downstream observable, but it cannot move backward and redefine the support, operator or action objects owned by Books 01--03. In this sense, Book 06 supplies the temporal hygiene of the monograph: construction comes before transfer, and negative controls come before evidence language.

## 06.15 Interface to Other Books

| Book | Object received from Book 06 | Role |
|---|---|---|
| Book 07 | finite tick and archive boundary language | horizon seam and emission update |
| Book 08 | \(A_{n+1}=arphi^{-1}A_n\), \(B_{n+1}=B_n+arphi^{-2}A_n\), \(R_n=arphi^n-1\) | internal archive acceleration |
| Book 09 | ordered finite windows and no-retuning time discipline | blind-run residual protocol |

## 06.36A Emergent Lorentz Symmetry from the Discrete Causal Budget

Special Relativity in D0 is not a postulate of an ambient Minkowski manifold. It is an exact algebraic consequence of the finite information budget of the holographic readout tick.

**Theorem 06.36A (Discrete Lorentz Factor).** 
By the Holographic Self-Reading Principle, a fundamental causal tick possesses a normalized unit budget of symplectic area (\(C=1\)). For a massive state (a stable topological memory cycle), this budget is partitioned into two orthogonal actions:
1. External transport \(\Delta x\) (changing address on the active boundary).
2. Internal holonomy \(\Delta s\) (advancing the phase of the internal memory cycle).
Orthogonality enforces the Pythagorean budget constraint:
\[ \|\Delta x\|^2 + \|\Delta s\|^2 = 1. \]
Defining the external transport velocity \(v := \|\Delta x\| \in [0,1]\), the proper time \(\Delta \tau\) experienced by the internal memory cycle is exactly the remaining budget:
\[ \Delta \tau := \|\Delta s\| = \sqrt{1 - v^2}. \]
The Lorentz factor \(\gamma = \frac{dt}{d\tau} = \frac{1}{\sqrt{1-v^2}}\) emerges automatically. Time dilation is therefore not geometric curvature, but the strict thermodynamic rationing of a finite computational readout cycle.

## 06.36B Emergent Lorentz Symmetry from the Symplectic Area Budget (Core Theorem)

Special Relativity is not a geometric postulate of an ambient Minkowski manifold. It is an exact algebraic consequence of the finite computational budget enforced by the Finite Holographic Self-Reading Principle (Book 00 §00.2).

**Theorem 06.36B (Discrete Lorentz Factor, D0.Core).**  
A fundamental causal tick possesses a normalized unit budget of symplectic area \(C=1\). For any massive topological memory cycle this budget partitions orthogonally into:
- external transport \(\Delta x\) (address change on the active boundary),
- internal holonomy \(\Delta s\) (phase advance inside the memory cycle).

Orthogonality (symplectic area preservation) enforces the Pythagorean identity
\[
\|\Delta x\|^2 + \|\Delta s\|^2 = 1.
\]
Defining the macroscopic transport velocity \(v := \|\Delta x\|\in[0,1]\), the proper time experienced by the cycle is the residual budget:
\[
\Delta\tau := \|\Delta s\| = \sqrt{1-v^2}.
\]
The Lorentz factor \(\gamma=1/\sqrt{1-v^2}\) emerges deterministically. Time dilation is the strict thermodynamic rationing of a finite symplectic computational cycle.

Owner: Book 06 / D0.Core. Certificate: `vp_symplectic_budget_lorentz.py`. Negative control: any model violating area preservation immediately loses relativistic invariance.

## 06.16 Publication Boundary Statement

Book 06 closes the finite time and archive-evolution layer. It does not close empirical cosmology, RG phenomenology, plasma experiments or GW signals. Those are downstream bridges/passports.

## 06.17 Cross-Reference Summary

- Book 00: Self-Reading Principle + 00.19-00.20 R ≡ Λ_N Grand Singularity.
- Book 01: support + 01.11C Pointer Machine (EPR as archive aliasing; Schur substrate here).
- Book 02/03: operator/action spine (02.19B homological forces; 03 action for scene updates).
- Book 05: 05.10 manifest (vp_schur...); central certs.
- Book 07: horizon seam for measurement micro-horizons (ties to 06.2E + 01.11C P->NP flush).
- Book 08: archive pressure / S_DE from forgetting + tick.
- New Core: 06.2E Relational Time as Feshbach-Schur Delay (D0-CORE-SCHUR-TIME-001): time = Neumann depth k in W_eff for P_N observer; static global U_N. See cert + CSV.

- Book 01 owns the phase-unfolding derivation.
- Book 02 owns the feedback operator and log-det calculus.
- Book 08 receives the archive-ratio theorem for cosmological transfer.
- Book 09 receives ordered-window discipline for blind tests.

Book 06 closes finite registration time and prepares the archive/cosmology layer. All time claims derive from the retained/archive split of the Self-Reading Principle.
