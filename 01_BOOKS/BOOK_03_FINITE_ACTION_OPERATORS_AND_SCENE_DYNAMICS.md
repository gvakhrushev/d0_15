<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_03_FINITE_ACTION_OPERATORS_AND_SCENE_DYNAMICS/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 03 — Finite Action Operators and Scene Dynamics

> **Publication status — v16 publication-proofread draft.**
> Scope: Finite action/variation language, scene dynamics, and admissible finite equations of motion.
> Claim discipline: This book supplies operator dynamics, not standalone empirical claims.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 03.v15 Active action/variation layer

Book 03 supplies the finite action and variation language for the feedback operator. It does not make empirical claims.

```text
S_fb = -log det(I - z F_N)
```

For an admissible finite variation `delta F_N`:

```text
delta S_fb
= Tr[(I - z F_N)^(-1) z delta F_N]
```

The universal feedback source is:

```text
Pi_fb = z(I - z F_N)^(-1)
```

Book 03 supplies the response source used by matter, gravity and cosmology sector reductions. Physical meaning is assigned only after sector projection and bridge/passport boundary.

## 03.1 Standard reading of action and finite incidence/clique complex terminology

The D0 `finite incidence/clique complex` is a finite incidence/clique complex with cochains and boundary/coboundary operators. The D0 `finite variational operator stack` is a finite variational functional on this complex. A `tick` is a discrete evolution endomorphism, and a `single dimensional calibration section` is a single scale-section fixing dimensionalization without introducing a second mass anchor.

## 03.2 Role and boundary of this book

Book 03 contains the finite action mechanism. It does not re-prove the condensed/profinite detector object, and it does not complete the particle, gravity or cosmology comparison protocols. Those are adjacent books.

The boundary rule is:

```math
S_{D0}^\varphi\ \text{and the response theorem} \in Books 01--02,
\qquad
S_{finite variational test functional},J_{finite incidence/clique complex},\Lambda_{act},S_\partial\in\text{Book 03},
```

```math
\text{particle/coefficient comparison protocols}\in\text{Book 04},
\qquad
\text{gravity and cosmology transfers}\in\text{Books 07--08}.
```

Thus this book is a bridge from invariant finite registration to finite dynamics.

## 03.3 Action as a finite admissible operator stack

Once a finite incidence/clique complex has been constructed, D0 does not introduce a continuum Lagrangian and then regulate it. The action is a finite admissible stack of operators, projectors, spectra, boundary terms and quadratic responses:

```math
\mathcal S_{stack}=J_{finite incidence/clique complex}+S_{coeff}+S_\Lambda+S_\partial+S_{heat}+S_{terminal}.
```

The order is not cosmetic. Scene selection comes first; finite variational test functional coefficients follow; the full-cycle action section fixes the single dimensional dictionary; the boundary block fixes the non-diagonal curvature residual; heat depth controls the length map; terminal terms record the final charged or leaking shell.

The admissibility condition is:

```math
\text{new sector scale}=\varnothing
\quad\text{after}\quad
\Lambda_{act}\ \text{has been chosen}.
```

A sector formula that requires a new GeV, metre, second, Planck, nucleon, collider, or dark-sector anchor is not an action theorem.

The closed feedback action component is `S_fb = -log det(I - z F_N)`, where `F_N=P_N U_N^dagger Q_N U_N P_N` is feedback-return, not positive response. The source is

```math
\Pi_{fb}=z(I-zF_N)^{-1},\qquad dS_{fb}=\operatorname{Tr}(\Pi_{fb}\,dF_N).
```

The log/Neumann expansion is allowed only under `|z|\rho(F_N)<1`; the resolvent itself only requires `z^{-1}` outside the spectrum. Its variation is represented by the finite feedback source owner `D0.Cosmology.FeedbackPartitionFunction`; pressure and finite PVT are owned by `D0.Cosmology.FiniteFeedbackEquationOfState`. The ideal-gas postulate is a no-go core shortcut, not the D0 pressure law.

## 03.4 Scene/finite variational test functional backbone

The finite incidence/clique complex is not background spacetime. It is the finite register on which action can be evaluated. The active action spine is:

```math
K(9,11,13)
\to
S_{finite variational test functional},J_{finite incidence/clique complex}
\to
\mathcal G_{spec}
\to
\Lambda_{act}
\to
\text{quadratic readout}.
```

The finite incidence/clique complex action is the finite selector of persistent records, unlocks, decays, bridges and readouts. It is therefore closer to a variational detector functional than to a continuum field postulate.

The finite variational test functional stack is allowed to use finite matrices, graph degrees, projectors, Hessians, spectra, finite differences and positive quadratic penalties. It is not allowed to use a sector target table as an input.

## 03.5 Internal action gauge

Let the length-depth map selected by finite incidence/clique complex, heat and terminal terms be

```math
D_L=\Omega_8\varphi^{V_9V_{11}}\left(1+\frac{\delta_0}{V_{13}}\right).
```

The normalized internal cell density is

```math
\rho_{cell}^{D0}=D_L^{-2}.
```

The internal gauge block is

```math
S_{gauge}^{D0}(\lambda,\rho)=
(\lambda-1)^2+(\rho-D_L^{-2})^2+
(\lambda^2\rho-D_L^{-2})^2.
```

Its positive stationary solution is

```math
\lambda_*=1,
\qquad
\rho_*=D_L^{-2}.
```

This is an internal action class and density class. It is not a kilogram, joule or electronvolt.

## 03.6 Single full-cycle action section

The physical SI section is chosen once, through the minimal charged terminal full-cycle:

```math
S_\Lambda(\tau,\Lambda)=
(\Lambda\tau/h-1)^2+
\left(38\tau/(h/(m_ec^2))-1\right)^2.
```

The Euler point is

```math
\tau_0=\frac{h}{38m_ec^2},
\qquad
\ell_0=c\tau_0=\frac{h}{38m_ec},
\qquad
\Lambda_{act}=\frac{h}{\tau_0}=38m_ec^2.
```

D0 does not fail to derive kilograms or joules. Kilogram, joule, metre and second are external unit sections, not invariants. D0 derives the invariant finite action-section structure. The electron terminal record prints this structure into the SI convention. Once this section is chosen, every later mass or rate readout must use the same section.

The mass map is therefore

```math
M_a^2=(\Lambda_{act}^{SI})^2\lambda_a.
```

The single dimensional calibration section rank rule is:

```text
mass, Q_beta, rate        : Lambda_act^(+1)
time, length, ellP        : Lambda_act^(-1)
G_N, cross-section area   : Lambda_act^(-2)
Born/entropy probabilities: Lambda_act^(0)
```

## 03.6a Gap labels do not create action sections

K-theory / K0 Gap Labeling records spectral gap ownership for frozen operators on the tiling hull. It does not introduce a second action section, a tunable scalar parameter, or a new mass anchor.

The allowed order is:

```text
single action section
-> frozen operator
-> spectral gap
-> K0 gap label
-> sector readout/passport
```

The forbidden shortcut is:

```text
gap label -> new action scale.
```

## 03.7 Boundary curvature and interaction-information cell

The scalar boundary residual is fixed by a non-diagonal boundary block, not by a free correction series. Define

```math
r=\frac{c_\partial^2}{\delta_0^6},
\qquad
r_0=\frac{13}{8}\frac{1+\delta_0^3/38}{1+\delta_0/9},
\qquad
d_9=\deg(V_9)=24.
```

The finite boundary action is

```math
S_\partial(r,I)=
\left(r-r_0\left(1+{I}\over d_9}\right)\right)^2+
\left(I-\Delta_\lambda^2\delta_0^3\right)^2.
```

Its stationary solution is

```math
I_*=\Delta_\lambda^2\delta_0^3,
\qquad
r_*=r_0\left(1+\frac{\Delta_\lambda^2\delta_0^3}{d_9}\right),
\qquad
c_\partial^2=\delta_0^6r_*.
```

The interaction-information cell used later is

```math
I_B=\frac{\Delta_\lambda^2\delta_0^3}{24}.
```

Book 04 may use this cell in hadron or coefficient comparison protocols, but Book 03 owns the variational reason that the cell is non-diagonal and finite.

## 03.8 Finite equations of motion

The D0 equation of motion is not a continuum Euler-Lagrange equation at fundamental level. It is a finite stationarity condition on the finite incidence/clique complex variables:

```math
\nabla_{x\in\mathcal X_N}\left(J_{finite incidence/clique complex}+S_{finite variational test functional}+S_\Lambda+S_\partial+S_{heat}+S_{terminal}\right)=0.
```

After the halt quotient and forgetting map, continuum equations may appear as limits or bridge dictionaries. They are not the primitive input.

The generic action-to-readout form is:

```math
\text{finite operator}\ Q
\quad\mapsto\quad
Q^\dagger Q
\quad\mapsto\quad
{\operatorname{Tr}(\Pi_aQ^\dagger Q)}\over{\operatorname{Tr}(Q^\dagger Q)}.
```

The proof of the trace law is in Book 02; Book 03 uses it as the admissible dynamics-to-readout finite variational test functional.

## 03.9 Runtime, forgetting and witness transport

The runtime stack consists of finite tick/witness transport followed by active/archive forgetting. The action consequence is that a record may persist, unlock or decay only through an operator that has a quadratic readout and a finite quotient.

The normalized witness transport is schematically

```math
\text{tick}\rightarrow\text{witness transport}\rightarrow\text{active/archive split}\rightarrow\text{quadratic readout}.
```

Finite-window entropy and dynamic witness transport are proof-referenced to Book 02. Book 03 uses them to control when an action block is a real runtime mechanism and when it is only a formal expression.

## 03.10 Vertex registry and finite scattering discipline

The vertex registry belongs here as action infrastructure. The finite S-matrix is not a complete collider simulator, but a registry of admissible transition operators:

```math
\mathcal S_{finite}: \mathcal H_{in}\to\mathcal H_{out},
\qquad
P(i\to f)=|\langle f|\mathcal S_{finite}|i\rangle|^2
```

provided the states are finite detector states and the bridge to external kinematics is typed. Collider and scattering comparison protocols are handed to Book 04.

## 03.11 Electroweak and photon channels as action layers

The electroweak material is retained as an action-layer owner block. Book 03 owns the action layer:

```math
\text{EW channel}=\text{single dimensional calibration section action layer}+\text{finite radial depth}+\text{typed weak unlock}.
```

Particle masses, charged-lepton generation, CKM orientation and gauge coefficient normalization are Book 04 matters. Book 03 only states the admissibility rule: the electroweak formulas must use the single action section and may not import an independent `M_Z`, `M_W`, proton or collider anchor.

The photon channel is the straight transit/phase channel of the terminal section. It is admissible as a benchmark action channel only because it preserves the invariant causal section and does not introduce a rest-return mass section.

## 03.12 Proton, neutron and beta/archive blocks as action mechanisms

The proton terminal-destructive readout and neutron beta/archive split blocks are not full hadron theory. They are action mechanisms handed to Book 04.

Book 03 keeps only the generic operator form:

```math
\text{terminal destructive readout}:
\quad
\lambda_{support}\rightarrow\lambda_{active}-\Delta_{readout},
```

and

```math
\text{beta/archive unlock}:
\quad
\text{finite active support}\rightarrow\text{weak unlock}\rightarrow\text{archive leakage/rate}.
```

The exact proton/neutron numerical comparison protocols remain in the matter book.

## 03.13 Gravity and cosmology cross-reference

The finite variational operator stack supplies one-section metrology and length-depth action. Gravity receives this in Book 07. Cosmology receives the finite-window archive-transfer mechanism in Book 08.

The S_DE insertion is therefore not a cosmology derivation inside Book 03. It is the action-side rule:

```math
\text{closed static coefficient}\rightarrow\text{finite spectrum}\rightarrow\text{finite window}\rightarrow\text{typed transfer}.
```

The actual BAO/archive pressure derivation belongs to Book 08.

## 03.14 Guardrails

Book 03 rejects the following moves:

1. adding a second dimensional anchor after `Lambda_act`;
2. reading a support eigenvalue directly as a particle mass without terminal/runtime transfer;
3. using a continuum action as primitive input before the finite halt quotient;
4. fitting bridge coefficients after seeing target data;
5. moving sector formulas from Book 04/07/08 back into the action book as if they were action proofs.

## 03.15 Claims covered or handed off

| Claim | Status | Canonical placement | Name | Forbidden shortcut | Falsification hook |
|---|---|---|---|---|---|
| `D0-SCENE-002` | CORE-ACTION | BOOK_03 | J_finite incidence/clique complex selects K(9,11,13) | Do not read J_finite incidence/clique complex as fitted polynomial for later constants. | Different admissible zero of the same typed obligations or wrong graph invariants. |
| `D0-MATH-001` | D0-RESOLUTION-EXACT | BOOK_03 | Finite phi-runtime and stop ideal | Do not add infinite correction layers below I12. | A physical scalar claim requires distinguishing below I12 inside D0 grammar. |
| `D0-ACTION-001` | CORE-ACTION | BOOK_03 | S_finite variational test functional/J_finite incidence/clique complex backbone | Do not close Born, entropy, leptons, or dynamics by unrelated formulas. | Mismatch between books or failure of Boundary Residual Eigenvalue r_∂ / I_B / action-spine consistency. |
| `D0-METRO-002` | SINGLE-SECTION-OUTPUT | BOOK_03 | Lambda_act single action section | No proton, W/Z, Planck, G_N, H0, or dark anchor as second scale. | Any closed prediction requiring an independent sector scale. |
| `D0-BOUND-001` | D0-RESOLUTION-EXACT | BOOK_03 | Boundary Residual Eigenvalue r_∂ and boundary curvature residual | Do not fit q_res with arbitrary scalar factor or reopen an infinite residual spiral. | Boundary residual cannot be produced below I12 by admissible cell. |
| `D0-QM-001` | CORE-MEASUREMENT | BOOK_02/BOOK_03 | Born/Hilbert finite trace ratio | Do not postulate continuum Hilbert space before finite trace. | Negative or unnormalized probabilities from finite Hessian readout. |
| `D0-VERTEX-001` | CORE-RUNTIME | BOOK_03 | Finite S-matrix registry | Do not compare raw graph amplitude directly to event count. | Failure of finite amplitude normalization or type split. |
| `D0-GAUGE-001` | CORE-RUNTIME | BOOK_04 via BOOK_03 operator mechanism | U(1) topological normalization and photon benchmark | Do not treat gamma/Z interference or event counts as closed by photon-only cert. | Failure of whitening identity or photon benchmark arithmetic. |
| `D0-EW-001` | CORE-RUNTIME | BOOK_03 | W/Z runtime ratio and on-shell angle | Do not use 3/13 or common-kernel variants as physical angle. | Failure to derive asymmetric kernels or trace ratio. |

## 03.16 Integrated calibration DAG and single action-section power matrix

The single dimensional calibration section rule is stated as an active action theorem, not as an index note.

D0 does not fail to derive kilograms or joules. Kilogram, joule, metre and second are external unit sections, not invariants. D0 derives the invariant finite action-section structure. The electron terminal record prints this structure into the SI convention. Once the external SI realization of the terminal charged cycle is chosen, all dimensional readouts must use the same section:

```math
C_e=\frac1{2(2\gamma-1)}=\frac1{38},
\qquad
\Lambda_{act}=38m_ec^2,
```

```math
\tau_0=\frac{h}{\Lambda_{act}},
\qquad
\ell_0=c\tau_0.
```

The integrated calibration DAG is

```text
finite verification algebra
  -> delta0, Omega8, K(9,11,13), rank/nullity data
  -> S_finite variational test functional / J_finite incidence/clique complex
  -> spectral and boundary invariants
  -> single action section Lambda_act
  -> matter, weak-rate, gravity, entropy, dynamics and survey readouts.
```

The power matrix is the operational content of the single dimensional calibration section theorem:

| object | D0 form | \(\Lambda_{act}\) power |
|---|---|---:|
| rest energy | \(M_a=\Lambda_{act}\mu_a\) | +1 |
| beta Q-value | \(Q_\beta=\Lambda_{act}\epsilon_\beta\) | +1 |
| decay rate | \(\Gamma=(\Gamma\tau_0)/\tau_0\) | +1 |
| tick/time | \(\tau_0=h/\Lambda_{act}\) | -1 |
| line length | \(\ell_0=ch/\Lambda_{act}\) | -1 |
| Planck length from depth | \(\ell_P=\ell_0/D_L\) | -1 |
| Newton bridge | \(G\sim\ell_P^2c^3/\hbar\) | -2 |
| cross-section area | \(\sigma\sim \ell_0^2\times\) dimensionless factor | -2 |
| trace probabilities and entropy weights | finite ratios | 0 |

Equivalently, the metrological DAG has one nonzero scale column.  Adding a proton, neutron, electroweak, Planck, dark-sector, collider or survey mass anchor raises the rank of the section matrix and is forbidden.

The section constraint may be represented in the finite variational operator stack by

```math
S_\Lambda(\tau,\Lambda)
=
(\Lambda\tau/h-1)^2
+
\left(38\tau/(h/(m_ec^2))-1\right)^2,
```

whose Euler point is

```math
\tau_0=\frac{h}{38m_ec^2},
\qquad
\Lambda_{act}=\frac h{\tau_0}=38m_ec^2.
```

This integrated block makes explicit that the single dimensional calibration section rule is a typed
metrology theorem, not a stylistic guardrail.  The Lean bridge types are
`DimensionlessCoreTraces` for the core trace shapes, `ExternalSICalibration`
for the SI dictionary, `SIMacroscopicPhysics` for SI outputs, and
`derive_physical_observables` for the typed bridge map.  The core trace object
does not produce SI constants by itself.

## 03.17 Integrated beta/scattering comparison protocol as finite transition discipline

The old beta-operator and scattering-comparison protocol notes clarify that collider or scattering formulas are downstream finite-transition comparison protocols, not raw event-count or continuum-field oracles.

A scattering comparison must declare

```math
P(a\to b)=\frac{|S_{ba}|^2}{\sum_c |S_{ca}|^2},
```

with the finite transition operator typed by the detector/finite variational operator stack and the external detector cuts placed only in the comparison protocol layer.  The allowed chain is

```text
finite variational operator stack -> finite transition operator -> quadratic transition weights -> detector comparison protocol.
```

Forbidden shortcuts are: collider normalization as a second action scale, post-hoc channel relabelling, and treating a finite D0 transition registry as a full detector simulator.

## 03.18 Terminal-cycle derivation of the `38` action section

The action section `Λ_act=38m_ec^2` is not a definition of the electron mass and not a fit to electron data.  The dimensionless coefficient `38` is fixed before SI units enter.

The graph-birth carrier has

```math
|V|=9+11+13=33,
\qquad Rank=3,
\qquad nullity=|V|-Rank=30.
```

The reduced terminal echo depth is therefore

```math
\gamma={nullity\over Rank}=10.
```

The primitive weak/terminal unlock uses a forward-return audit with the halt section counted once:

```math
N_{unlock}=2\gamma-1=19.
```

The full terminal action section has two orientation sides, hence

```math
N_{act}=2N_{unlock}=2(2\gamma-1)=38.
```

Only after this dimensionless finite-cycle number is fixed is the SI electron rest-energy used as a section dictionary:

```math
\Lambda_{act}=N_{act}m_ec^2=38m_ec^2.
```

Thus the electron mass is not predicted from itself.  The finite theorem predicts the dimensionless full-cycle action coefficient `38`; the external electron rest energy supplies the SI unit section used to express the D0 action scale in joules or MeV.

## 03.19 Integrated single dimensional calibration section and boundary-residual closure cells

This section closes the action/metrology rows that cannot remain as ledger-only claims.  The active theorem text now carries the proof-cell content required for release status.

### 03.19.1 `D0-METRO-002`: Lambda action-section rigidity

**Theorem.**  All dimensionful mass/action readouts in D0 factor through one and only one action section.  The finite theory determines the admissible section type and slot-count; SI units supply only the external representative.

The electron full-cycle section is

```math
C_e={1\over 2(2\gamma-1)}={1\over 38},
\qquad
\Lambda_{act}=38m_ec^2.
```

The causal line/tick dictionary is

```math
\ell_0^{D0}=1,
\qquad
\tau_0^{D0}=1,
\qquad
c_{D0}=\ell_0^{D0}/\tau_0^{D0}=1.
```

In SI representatives the same section is

```math
\tau_0={h\over 38m_ec^2},
\qquad
\ell_0=c\tau_0={h\over 38m_ec},
\qquad
\Lambda_{act}={h\over\tau_0}=38m_ec^2.
```

The active certificate records

```text
τ0 = 2.1298157324596072e-22 s,
ℓ0 = 6.3850269352113602e-14 m,
ℓ0/τ0 = 299792458 m/s,
Λ_act = 19.417960126286623 MeV.
```

**Closure.**  This closes the quotient/resolution field missing in the earlier review pass: the quotient is not another sector scale, but the equivalence class of all dimensionful readouts under the single action section.  A second proton, W/Z, Planck, Hubble or dark-sector anchor falsifies the claim.

Primary certs: `vp_calibration_dag_and_lambda_section_rigidity_20260522.py`, `vp_c_time_length_single_section_closure.py`.

### 03.19.2 `D0-BOUND-001`: q-mass and boundary curvature residual

The boundary residual is not a fitted scalar.  It is the stationary solution of the boundary block of the finite variational test functional action:

```math
S_\partial(r,I)=\left(r-r_0(1+I/d_9)\right)^2+
\left(I-\Delta_\lambda^2\delta_0^3\right)^2.
```

The Euler equations select

```math
I_* = \Delta_\lambda^2\delta_0^3,
\qquad
r_* = r_0(1+I_*/d_9),
\qquad
c_\partial^2=\delta_0^6r_*.
```

The same action-gauge closure fixes

```math
S_\Lambda(\tau,\Lambda)=
(\Lambda\tau/h-1)^2+
\left(38\tau/(h/(m_ec^2))-1\right)^2,
```

hence

```math
\tau_0=h/(38m_ec^2),
\qquad
\Lambda_{act}=h/\tau_0=38m_ec^2.
```

**Closure.**  The linear/operator field is now explicit: the boundary residual comes from the finite boundary Euler block of the global action, not from a post-hoc scalar correction.  The retired `q_mass` bridge remains a quotient dictionary only after the stationary residual has been fixed.

Primary certs: `vp_action_gauge_and_boundary_curvature_closure.py`, `vp_derivation_boundary_curvature_stationarity.py`.

## 03.20 Single-section hostile uniqueness: the integer 38

The action section uses the finite graph finite variational operator stack before particle-sector finite readouts.  Let

```math
|V|=33,
\qquad \operatorname{rank}(A)=3,
\qquad \nu=|V|-\operatorname{rank}(A)=30.
```

Then the terminal coefficient is

```math
\gamma=\nu/\operatorname{rank}(A)=10,
\qquad
N_{unlock}=2\gamma-1=19,
\qquad
N_{act}=2N_{unlock}=38.
```

The dimensionful section is therefore

```math
\Lambda_{act}=38m_ec^2.
```

The electron unit is a section for comparison, not the source of the integer.  Nearest-neighbour controls fail as follows: `37` leaves one half-cycle channel missing; `39` adds a non-D0 channel; `40` double-counts the fixed witness endpoint.  Thus `38` is an operator lock of the closed two-direction action section, not a fitted electroweak coefficient.

## 03.21 Finite spectral-action ladder

The primary D0 gravity/action statement is finite spectral algebra, not a continuum Einstein-Hilbert integral. The continuum integral is a later bridge reading after finite heat-trace support has been declared.

For a density floor `rho` and finite Laplacian `L`, the active ladder is:

```text
W L W = conformalLaplacian L rho
Tr(W L W) = a0 volume proxy
Tr((W L W)^2) = diagonal square term + 2 * discreteEHActionProxy
|Tr((W L W)^k)| has floor-bounded absolute control for higher powers.
```

The off-diagonal action proxy carries a factor `1/2` because the double sum counts both orientations of an undirected edge:

```text
2 * discreteEHActionProxy
  = sum_i sum_j if i != j then L_ij^2 / (rho_i rho_j) else 0.
```

Lean ownership:

```text
D0.Geometry.HeatTraceA2Decomposition.heat_trace_sq_exact_decomposition
D0.Geometry.HeatTraceA2Decomposition.double_count_factor_guard
D0.Geometry.HigherCurvatureSuppression.higher_curvature_suppression_by_floor
D0.Geometry.SpectralActionLadder.a0_is_volume_proxy
D0.Geometry.SpectralActionLadder.a2_is_eh_proxy
D0.Geometry.SpectralActionLadder.higher_powers_floor_bounded
```


## 03.21a Gap labels do not create new action sections

The topological gap labels assigned to spectral gaps do not introduce new action sections or ad-hoc scalar field parameters. They serve as discrete indices of existing sectors on the tiling hull rather than defining new energy anchors. All calculations remain strictly constrained by the single metrological section $\Lambda_{act} = 38 m_e c^2$. The formal Lean owner is `D0.Matter.KTheoryGapLabeling` (`gap_labeling_requires_frozen_operator`), and the integration is checked by `D0.Bridge.FinalBridgeIndex`.

## 03.22 Action-to-selector closure rule

An action operator becomes a particle-sector statement only after it induces a finite selector or a finite response readout.  The finite variational operator stack alone is not enough.  The required chain is:

```text
finite action support
→ response / score functional
→ strict selector certificate or normalized response theorem
→ observable transfer only after the internal object is fixed.
```

This removes the previous bridge-only reading in which a large action number could be quoted as if it directly selected a particle mass. The active theory requires the intermediate operator: response for probability claims, strict selector for particle identity claims, and transfer operator for mass/comparison claims.
## 03.23 K(9,11,13) Torus Shell Interpretation

The preceding dynamic source is the D0 time-transition matrix:

```text
T time evolution
-> |Tr(T^2)|=3 generation carrier
-> |Tr(T^3)|=4 ABCD capacity
-> |Tr(T^5)|=11 memory torus
-> K(9,11,13) torus shell geometry
```

The finite action/topology spine now gives the structural home for the D0 memory
torus:

```text
D=9  puncture/interface shell  = R-r = 1
D=11 memory torus core shell   = R
D=13 outer shell               = R+r
```

The dimensionless torus aspect is frozen as

```text
(R+r)/(R-r) = phi^5
```

with the algebraic core owner `D0.Geometry.TorusCore13GeometryOrigin`.  Book 03
does not use PDG data to create this geometry; PDG Core-13 is an external
embedding passport.

## 03.24 Lefschetz finite incidence/clique complex counts from the time ladder

The anti-periodic finite incidence/clique complex count is read as
`NFermion(n)=|det(T^n+I)|`.  The first active closure checks are:

```text
NFermion(3)=4
NFermion(4)=9
NFermion(5)=11
NFermion(3)+NFermion(4)=13
NFermion(6)=20
```

These are finite trace/automorphism counts.  They are not empirical particle
multiplicities and do not replace downstream selector or passport protocols.

## 03.v15 CVFT master bootstrap action

The D0 action layer uses a single finite bootstrap functional:
\[
\mathcal B_N
=
\beta^{-1}\log\operatorname{Tr}(e^{-\beta\Delta_N(V)})
-
\log\det(I-zF_N(V)).
\]
The stationarity condition \(\delta\mathcal B_N=0\) locks finite spectral geometry to feedback-return thermodynamics. The discrete derivative \(\partial_V A_N=A_{N+1}-A_N\) acts over rank evolution \(V_N=\operatorname{rank}(P_N)\). The single action section is unchanged by this rank step; no second mass anchor is introduced.

## 03.v15 Golden tick gate

Let \(p=\varphi^{-1}\). The detector-clock fixed point is realized by the finite active/archive splitter

\[
U_\varphi=
\begin{pmatrix}
\sqrt p\,I&-pI\\
pI&\sqrt p\,I
\end{pmatrix}.
\]

Since \(p+p^2=1\), this block is unitary. It yields

\[
F_N=p^2P_N=\varphi^{-2}P_N,
\qquad
U_{\rm eff}^\dagger U_{\rm eff}=pP_N=\varphi^{-1}P_N
\]

on the declared detector-clock block. This construction supplies the finite action-level gate for informational mechanics.
