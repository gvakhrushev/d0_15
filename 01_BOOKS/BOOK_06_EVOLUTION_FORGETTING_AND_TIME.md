# BOOK 06 вЂ” Evolution, forgetting and time

## 06.1 Standard reading of evolution and forgetting

D0 `forgetting` is not a metaphor. In this book it means one of the following standard operations, depending on context: conditional expectation onto a retained algebra, partial trace over an environment, Wilsonian coarse-graining, or entropy-selected coupling. The D0 `archive` is the traced-out complement produced by that operation.

## 06.2 Role of this book

Book 06 is the runtime book of D0.  Books 01--02 define the condensed/profinite detector support and the finite proof calculus.  Book 03 defines the action gate and scene dynamics.  Book 04 defines matter and particle-sector finite readouts.  Book 05 defines the verification grammar.  Book 06 explains how a sequence of completed finite registrations becomes time, evolution, phase transport, entropy, classicality and runtime transfer.

The central rule is:

```math
\boxed{
\text{evolution is not a background flow; it is an ordered quotient of completed registrations.}
}
```

Equivalently,

```math
\text{time}=\text{ordered closure of registration events}.
```

This book therefore treats time as an invariant structure induced by finite detector completion, not as an external continuum parameter that precedes measurement.

## 06.3 Evolution cannot precede registration

A D0 event becomes eligible for evolution only after it has produced a finite record.  Before completion there is support, potential transport and unresolved comparison; after completion there is an ordered active state together with an archive remainder.  The primitive sequence is

```math
\text{support}\longrightarrow\text{finite detector channel}\longrightarrow
R=D^\dagger D\longrightarrow\text{halted record}\longrightarrow\text{ordered update}.
```

The first temporal object is not a smooth parameter `t`; it is the ordering relation on records that survive the halt quotient.

```math
r_i\prec r_j
\quad\Longleftrightarrow\quad
r_i\text{is registered before}\ r_j\text{inside the finite detector history}.
```

The continuum parameter of ordinary dynamics is integrated only after many such ordered records are coarse-grained through stable tick conventions.

## 06.4 Active/archive decomposition

The runtime state decomposes into an active component and an archive component:

```math
\mathcal H_{total}=\mathcal H_{active}\oplus\mathcal H_{archive}.
```

The active part contains the finite record capable of further transport.  The archive part contains information that has been resolved away by the detector quotient: phase metadata, unresolved address tails, null directions, inaccessible comparison data and dephased correlations.

A runtime state may be written schematically as

```math
\psi_{active}(P,u)=P\,H(u)\psi_{support},
```

where `P` is the active projector and `u` is the runtime/window parameter inherited from the finite detector depth.

Archive is not metaphysical non-existence.  It is the complement of active readout under a specified finite quotient:

```math
\Pi_{active}+\Pi_{archive}=I,
\qquad
\Pi_{active}\Pi_{archive}=0.
```

## 06.5 Forgetting maps as typed quotients

The D0 forgetting map is a typed quotient:

```math
\Delta:\rho_N\longmapsto\Delta(\rho_N).
```

It removes the information that is not stable under the declared finite readout while preserving the invariant needed for the next registration.

For a finite subsystem `A` the entropy assigned to the dephased finite-window state is

```math
S_A^{D0}=-\operatorname{Tr}_K\!\left(\rho_A^{fw}\log\rho_A^{fw}\right).
```

The classical limit is therefore not a primitive assumption.  It is the regime in which repeated typed quotients stabilize an effectively commuting record algebra.

```math
\Delta(\rho_N)\text{stable under repeated finite records}
\quad\Rightarrow\quad
\text{classical readout algebra}.
```

## 06.6 Finite phi-runtime and depth contraction

The foundational split `p+p^2=1` is proved in Books 01--02.  Book 06 uses it as a runtime contraction.  If a route or comparison chain has depth `N`, the finite continuation weight takes the form

```math
Q_N=Q_0\varphi^{-N}.
```

The runtime contraction is governed by the detector asymmetry quantum

```math
\delta_0=\frac{1}{2\varphi^3}.
```

A finite-depth update may therefore be represented as

```math
u_{k+1}=\delta_0 u_k,
```

or, for an error/tail amplitude,

```math
\delta^{(k+1)}=\delta_0\,\delta^{(k)}.
```

This does not introduce a new physical parameter.  It is the runtime use of the same finite-verification split that defines the detector foundation.

## 06.7 Time as invariant registration and the causal section

The D0 internal units may be represented by the normalized section

```math
\ell_0^{D0}=1,\qquad \tau_0^{D0}=1,\qquad c_{D0}=\frac{\ell_0^{D0}}{\tau_0^{D0}}=1.
```

This is not a claim that laboratory SI units are trivial.  It is the internal statement that one line-step and one tick-step form a single causal section before external metrology is attached.  The Lean owner is `D0.Bridge.internal_cone_speed_eq_one`: the internal cone speed is a dimensionless invariant of the normalized kinematic gauge.  SI light speed is therefore a metrological export, not a fitted D0 core parameter.

The physical export of the tick convention is handled by the matter/metrology books.  The old evolution material contains the terminal relation

```math
\tau_0=\frac{h}{38m_ec^2},
```

but Book 06 uses it only as a cross-reference: the coefficient `38` belongs to the terminal matter/readout analysis and the SI-length/Newton shadow belongs to Book 07.

## 06.8 Normalized tick operator

The finite time-transition operator has a separate integer toral-automorphism layer:

```text
T = [[0,1],[1,-1]]
chi_T(lambda)=lambda^2+lambda-1
spec(T)={phi^-1,-phi}
det(T)=-1
Tr(T^n)=(-1)^n L_n
```

The determinant-square theorem `toral_volume_conservation_square` records the finite volume-balance invariant, and `trace_T_pow_eq_signed_lucas` records the integer signed-Lucas trace law without importing analytic roots as Lean primitives.

For finite graph dynamics, background time is replaced by a normalized tick operator.  If `A` is the finite adjacency/action operator and `D` its degree/normalization operator, the canonical tick form is

```math
T_{tick}^{D0}=D^{-1/2}AD^{-1/2},\qquad \rho(T_{tick}^{D0})=1.
```

The condition `rho(T_tick)=1` is the finite stability condition for runtime propagation.  It prevents the tick from being either a hidden expansion parameter or an unbounded background evolution.

A witness transport along a finite route `gamma` is represented as

```math
\mathcal U_\gamma^{D0}:
\mathcal H_{active}(a)\longrightarrow\mathcal H_{active}(b),
```

and the corresponding transition probability takes the finite response form

```math
P(b|a,\gamma)=
\frac{\operatorname{Tr}(\Pi_b\,\mathcal U_\gamma R_a\mathcal U_\gamma^\dagger)}
{\operatorname{Tr}(R_a)}.
```

## 06.9 Phase transport and quantum emergence

Quantum evolution appears when the finite active record is transported without being immediately forced into a commuting classical quotient.  The finite-stage transport has the standard unitary-looking form

```math
\rho_N\mapsto U_N\rho_NU_N^\dagger,
```

but its interpretation is D0-specific: `U_N` is a finite transport of an already addressed detector support.  It does not presuppose an infinite background Hilbert space.

The bridge to quantum mechanics is therefore

```math
\mathcal F_Q:D0\to QM,
```

where the target quantum formalism is the continuum completion of finite detector transport.  The bridge is valid only when the D0 finite-window protocol has been declared.

## 06.9a Tiling-hull runtime

Time evolution over the D0 vacuum is represented as translation dynamics on the φ-quasicrystalline tiling hull. The ordered tick chain supplies the runtime order; the irrational φ phase supplies non-periodic transport; finite quotient windows produce stable detector-visible averages.

```text
fixed detector support
-> ordered tick transport
-> φ-quasicrystal hull translation
-> finite quotient window
-> smooth macro-runtime shadow
```

The Lean owner is `D0.Topology.TilingHull` (`d0_hull_has_phi_cut_project_origin`, `d0_hull_is_nonperiodic`, `d0_hull_supports_gap_labeling`). The certificate owner is `05_CERTS/vp_d0_tiling_hull.py` (`PASS_D0_TILING_HULL`).

## 06.10 Uncertainty as a finite-window protocol

Uncertainty is not imported as an independent metaphysical postulate.  It is the finite cost of resolving non-commuting readout channels inside one detector window.  The source notation records this as

```math
\Delta_J\Delta_\partial\ge 1.
```

Here `J` denotes action/scene resolution and `partial` denotes boundary/derivative resolution.  Book 06 reads this as a protocol inequality: increasing precision in one finite channel consumes the detector window available to the conjugate channel.

## 06.11 Evolution of scales: selection, not new knobs

Evolution may change which quotient is active, which transfer window is used, and which sector bridge is allowed.  It may not introduce a new scale by convenience.

The active scale discipline is inherited from Book 03:

```math
\Lambda_{act}
```

and sector consequences are downstream projections:

```math
\Lambda_{act}
\longrightarrow
\text{matter dressing},\text{runtime coefficients},\text{scattering windows},\text{archive pressure}.
```

This rule is essential.  Without it, evolution would become a place to hide fitted constants.

## 06.12 Runtime coefficient readout sequence

The source evolution book collects several runtime coefficient shadows.  In the new order they are not treated as independent derivations inside Book 06; they are read as a sequence of typed readouts from already-defined books:

```math
\pi_0\text{-holonomy}\to G_N,
```

```math
q_{res}\text{ electromagnetic runtime dressing}\to\alpha,
```

```math
T_W/T_Z\text{ runtime ratio}\to\theta_W,
```

```math
V_9\text{ two-way color holonomy}\to\alpha_s,
```

```math
\Lambda_{act}\varphi^5q_{mass}^{-(d_9+2Rank)}\to\Lambda_{QCD}.
```

The proof locations are Books 02--04 and the metrological export is Book 07.  Book 06 keeps the ordering principle: coefficients become observed through runtime quotients and transfer windows, not through free empirical anchoring.

## 06.13 Tick-to-scattering comparison protocol

Scattering is the experimental form of finite runtime.  The Book 06 contract is

```math
\text{finite support}\to T_{tick}^{D0}\to\mathcal U_\gamma^{D0}\to P(b|a,\gamma)\to\sigma_{exp}.
```

The source tick-to-scattering expression is preserved as

```math
\sigma_{D0\to exp}=\ell_0^2\,\mathcal J_{exp}\,P_{D0},\qquad
\ell_0=\frac{h}{38m_ec}.
```

The important discipline is that the finite transition probability `P_D0` must be fixed before the experimental Jacobian `J_exp` is attached.

## 06.14 Archive-pressure runtime kernel

Archive pressure is a runtime effect of the active/archive split.  The finite runtime space has the form

```math
\mathcal H_{runtime}=\mathcal H_A\oplus\mathcal H_N,
```

and the detector cut may be written schematically as

```math
\mathcal C_{det}=\delta_0^8I.
```

The archive-pressure operator belongs to Book 06 as a runtime kernel, but its cosmological empirical use belongs to Book 08.  This prevents a common error: using survey likelihoods to define the archive operator.

The allowed direction is

```math
\text{detector archive/runtime split}
\longrightarrow
\text{archive-pressure operator}
\longrightarrow
\text{S_DE or survey transfer comparison protocol}.
```

The forbidden direction is

```math
\text{survey residual}
\longrightarrow
\text{invent archive pressure}.
```

## 06.15 Saturation, horizons and the gravity cross-reference

Finite runtime can saturate.  In the source book this appears in horizon language and Einstein-side heat-trace language.  Book 06 records the runtime principle:

```math
\sigma(R)\to1
\quad\Rightarrow\quad
\text{saturated finite readout}.
```

Detailed gravity statements, including the length-depth theorem, Newton/Planck shadows, Einstein heat trace and horizon archive interpretation, are assigned to Book 07.  Book 06 only fixes the runtime boundary: saturation is a finite detector condition before it is a spacetime interpretation.

## 06.16 Falsification rules for evolution claims

An evolution claim fails if any of the following occurs:

1. it uses a background continuum time before finite registration;
2. it introduces a new scale outside the single-section discipline;
3. it hides a fitted coefficient in a runtime window;
4. it uses cosmological, scattering or matter data to define the operator that is later claimed to predict them;
5. it erases the distinction between active state and archive quotient;
6. it moves a gravity or cosmology result into Book 06 to avoid its sector comparison protocol.

The positive test is:

```math
\text{finite record}\to\text{typed forgetting}\to\text{normalized tick}\to
\text{sector transfer}\to\text{falsifiable comparison protocol}.
```

## 06.17 Claims inherited from the theorem database

| Claim ID | Domain | Status | Claim | Book 06 role |
|---|---|---|---|---|
| `D0-FOUND-002` | Foundation | `CORE-FOUNDATION` | Minimal addressable record split | foundation/metrology reference |
| `D0-FOUND-003` | Continuum Measurement | `CORE-FOUNDATION` | Minimal continuum-measurement skeleton | foundation/metrology reference |
| `D0-SCENE-002` | Detector Scene | `CORE-ACTION` | J_scene selects K(9,11,13) | action-ordering reference |
| `D0-ACTION-001` | Action Spine | `CORE-ACTION` | S_gate/J_scene backbone | action-ordering reference |
| `D0-METRO-001` | Metrology | `CORE-FOUNDATION` | Single causal line/tick invariant | foundation/metrology reference |
| `D0-METRO-002` | Metrology | `SINGLE-SECTION-OUTPUT` | Lambda_act single action section | foundation/metrology reference |
| `D0-QM-001` | Quantum Readout | `CORE-MEASUREMENT` | Born/Hilbert finite trace ratio | runtime/theorem use |
| `D0-THERMO-001` | Entropy | `CORE-MEASUREMENT` | Finite-window entropy from archive forgetting | runtime/theorem use |
| `D0-DYN-001` | Dynamics | `CORE-RUNTIME` | Normalized tick and witness transport | runtime/theorem use |
| `D0-VERTEX-001` | Vertex/Scattering | `CORE-RUNTIME` | Finite S-matrix registry | runtime/theorem use |
| `D0-LEPTON-002` | Charged Leptons | `ACTIVE-PASSPORT` | Charged-lepton generation action | matter evolution consequence |
| `D0-PHOTON-001` | Photon/Neutrino | `CORE-MEASUREMENT` | Photon massless carrier | matter evolution consequence |
| `D0-NEUTRINO-001` | Photon/Neutrino | `CORE-MEASUREMENT` | Neutrino neutral leakage mass-square pattern | matter evolution consequence |
| `D0-COEFF-003` | QCD | `CORE-RUNTIME` | QCD runtime and archive/confinement scale | matter evolution consequence |
| `D0-GRAV-001` | Gravity | `SINGLE-SECTION-OUTPUT` | Length-depth theorem and Planck/Newton shadow | gravity cross-reference |
| `D0-COSMO-001` | Cosmology/Archive | `CORE-MEASUREMENT` | Archive-pressure operator | archive-runtime cross-reference to cosmology |
| `D0-COSMO-003` | Dark/Archive | `ACTIVE-PASSPORT` | Boundary dark survey-driver kernel | archive-runtime cross-reference to cosmology |
| `D0-COLLIDER-001` | Collider | `EXTERNAL-BRIDGE` | Collider runtime typed bridge | runtime/theorem use |
| `D0-PI0-001` | Cycle/Holonomy | `CORE-FOUNDATION` | pi0 finite-cycle versus pi continuum generator | foundation/metrology reference |

## 06.18 Cross-book boundary summary

| Topic | Book 06 treatment | Final proof/comparison protocol location |
|---|---|---|
| `p+p^2=1`, `delta0`, `ABCD` | runtime use only | Books 01--02 |
| `S_gate`, `J_scene`, `Lambda_act` | ordering and scale discipline | Book 03 |
| photon/electron/neutrino/QCD coefficients | evolution consequences | Book 04 |
| verification and promotion statuses | referenced | Book 05 |
| tick, forgetting, entropy, phase transport | normative | Book 06 |
| `pi0`, SI length, Newton/Planck, Einstein heat trace | boundary cross-reference | Book 07 |
| archive pressure in BAO and survey likelihood | runtime kernel only | Book 08 |

## 06.19 Integrated causal-information invariants

The integrated source layer contains a compact causal-information invariant layer.  It belongs in the evolution book because it explains why time is not an external parameter but a stable ordering of finite records.

A D0 evolution step is admissible only if it preserves:

```text
addressability,
finite registration,
quadratic response,
causal ordering,
archive/active separation.
```

The invariant content of a finite history is therefore not the continuum path between records but the ordered class of registered transitions:

```math
\mathcal H_N=\big((a_0,R_{a_0}), (a_1,R_{a_1}),\ldots,(a_k,R_{a_k})\big)/\sim_{D0}.
```

Forgetting is a quotient on this history, not destruction of the finite event:

```math
\Delta(\rho_N)=\sum_a \Pi_a\rho_N\Pi_a,
```

with the discarded off-diagonal data entering the archive sector.  This integrated block is the evolution-side counterpart of Book 01's condensed detector halt.

## 06.20 Wilsonian RG as a typed forgetting map

The D0 forgetting map is not a metaphor for renormalization; it is the internal structure which allows a precise bridge to Wilsonian renormalization.

At the D0 level, forgetting is a typed quotient:

```math
\Delta_N:\rho_N \longmapsto \Delta_N(\rho_N),
```

where finite address, phase or high-depth metadata are moved from the active record to the archive complement.  At the QFT/EFT bridge level, Wilsonian coarse-graining integrates or quotients modes above a declared comparison scale.  The bridge dictionary is therefore:

```math
\Delta_N
\quad\leadsto\quad
\mathcal R_{\mathrm{SM}}^{\mathsf S}(\mu \leftarrow \Lambda_{\mathrm{act}}),
```

not as an identity of theories, but as a typed comparison map between the finite D0 active sector and the infrared scheme used by an experimental observable.

The admissible diagram is:

```math
O_{\mathrm{D0}}^{\mathrm{bare}}
\longrightarrow
O_{\mathrm{SM}}^{\mathsf S}(\Lambda_{\mathrm{act}})
\longrightarrow
O_{\mathrm{SM}}^{\mathsf S}(\mu),
```

with the first arrow being the declared dressing dictionary and the second arrow being the standard EFT/RG evolution in the declared scheme.

The guardrail is strict.  RG evolution is not allowed to repair a failed D0 invariant by adding new degrees of freedom.  It may only transport a fixed finite boundary object through an explicitly declared external evolution law.

## 06.21 Claim-level RG bridge guardrail

The RG/forgetting identification is a typed bridge, not a licence to import arbitrary continuum structure.  A Wilsonian step is admissible only when it is presented as a forgetting morphism from a declared finite D0 source object:

```math
O_{SM}^{\mathcal S}(\mu)
=\mathfrak D_{SM}^{D0}(\mathcal S,\mu,\Lambda_{act})[O_{D0}^{bare}].
```

The bridge must keep the field content, beta-functions, threshold conventions and scheme explicit.  A hidden new particle, new threshold, or scheme change is an external hypothesis and cannot repair a D0 residual.  This is the operational form of the archive/forgetting interpretation of RG flow.

## 06.22 RG/coarse-graining as typed forgetting

The Wilsonian interpretation of D0 is not a rhetorical analogy.  A typed forgetting map is a finite-to-effective comparison morphism:

\[
\Delta_{RG}:\operatorname{Obs}^{D0}_{active}\longrightarrow
\operatorname{Obs}^{scheme}_{IR}(\mu),
\]

where the target is scheme-labelled.  `О”_RG` may integrate out, trace out or coarse-grain finite metadata, but it may not introduce new fields, new scales or new beta functions unless the status is explicitly changed from D0 bridge to a different physical model.

Thus RG dressing is allowed only as external comparison calculus:

\[
O_{bare}^{D0}\neq O_{PDG},
\qquad
O_{PDG}=\Delta_{RG}^{scheme}(O_{bare}^{D0}).
\]

This prevents the Standard Model from being used as a hidden source of D0 invariants while still allowing it to be used as the correct infrared comparison engine.

---

## 06.23 Scheme-specific RG/PDG comparison protocol closure

Scheme-specific comparison with PDG or collider conventions is a typed bridge, not a core theorem.  The bridge file must declare:

```text
bare_d0_object
renormalization_scheme
scale_mu
matching_scale_Lambda_act
field_content
beta_functions
threshold_conventions
observable
external_table
forbidden_parameters
falsification_hook
```

A bridge comparison protocol is closed when these fields are fixed before numerical comparison.  It is not closed by reproducing a table after choosing a convenient scheme.  The release includes such comparison templates for the coefficient, lepton, CKM, QCD and BAO-facing rows.

## 06.24 Forgetting as entropy-selected coupling

The D0 forgetting map is upgraded from a metaphorical archive projection to a finite entropy-selected coupling. Given retained response tests `Test_D0(N)`, the forgetting bridge is the kernel

```math
K_N^* = \arg\max_{K_N}\ H(Y_N|X_N)
```

subject to the declared retained response constraints and loss quotient. This matches the Wilsonian intuition of coarse-graining: high-resolution metadata are not arbitrarily discarded, but are integrated out by the unique maximum-entropy representative compatible with retained finite responses.

Consequently, an RG bridge is closed only after specifying:

```text
retained response tests;
forgotten coordinates;
loss quotient;
entropy/gauge representative;
flow scheme.
```

This makes the RG/forgetting layer a constructive finite bridge rather than a continuum smoothing ansatz.

Terminology lock: RG/forgetting is a `convex-response` bridge and must expose a `coupling kernel` preserving retained response tests before loss quotient.

## 06.25 RG/forgetting as an executed finite entropy bridge

The forgetting map is not an informal loss of information.  At a finite stage it is represented by a conditional kernel selected by maximum entropy under retained D0 response constraints.  Given a finite response grid `Y` and retained response `r`, the forgetting channel is

```math
K^*(y_j\mid r)=\frac{\exp(\theta(r)y_j)}{\sum_k\exp(\theta(r)y_k)},
```

with `Оё(r)` uniquely fixed by `\sum_jK^*(y_j\mid r)y_j=r`.  This is the finite D0 analogue of Wilsonian coarse-graining: discarded metadata are not arbitrary; the retained response fixes the unique maximum-entropy representative in the quotient.

The executable finite-entropy certificate verifies this construction for the BAO/S_DE response windows and supplies the model for RG/PDG bridge kernels.

## 06.26 Executed macro-forgetting source

The archive-to-continuum bridge begins with a finite source. A unit archive act is represented by the bounded centered operator

```math
\mathsf A_k \in [-a,a],\qquad a=\delta_0^8/30,
```

after active-sector centering. The normalized archive atom `Z_k=\mathsf A_k/a` obeys

```math
\mathbb E\exp(tZ_k)\le \exp(t^2/2).
```

Therefore

```math
X_N=N^{-1/2}\sum_{k=1}^N Z_k
```

is a finite subgaussian archive vector before any continuum Gaussian comparison is made. This supplies the D0 side of the HST-style macro bridge. The bridge is a comparison functor from finite archive statistics to macro Gaussian modelling, not an ambient-continuum primitive.

## 06.27 Lepton magnetic moment as RG/forgetting bridge

In standard QFT, the anomalous magnetic moment is scheme-dependent and receives QED, electroweak, hadronic vacuum-polarization and hadronic light-by-light contributions. In D0 this is represented as an external RG/forgetting bridge from a finite ABCD holonomy in the lepton support shell to a continuum comparison scheme:

\[
a_\ell^{D0,S}(\mu)=a_\ell^{S,baseline}(\mu)+K_{g-2}^{D0}(\mu)\mathcal R_{residual}^{D0,S}.
\]

The term \(K_{g-2}^{D0}\) is finite and single-section locked. The residual trace \(\mathcal R_{residual}^{D0,S}\) is not allowed to introduce new fields or modified beta functions. This turns `gв€’2` into a scheme comparison protocol rather than a free new-physics knob.

## 06.28 Tick-to-space unfolding

The runtime tick does not merely order events. When paired with a cyclic phase quotient it generates a branch foliation. A near-return modulus `q` turns the one-dimensional tick line into residue branches; admissibility filters select which branches survive as observable geometry. This is the finite mechanism by which ordered registration can unfold into spatial structure before any smooth manifold is invoked.

## 06.29 Phase-unfolding master chain

D0 no longer treats spatial branching as a primitive geometric background.  An ordered finite registration can generate visible geometry through a phase quotient.  For a phase circumference \(\tau\), the map

\[
U_\tau(n)=(n,n\bmod \tau)
\]

turns the one-dimensional tick sequence into a branch foliation whenever an integer pair \((q,m)\) satisfies \(|q-m\tau|\ll 1\).  The residue classes modulo \(q\) are the coherent branches.  An admissibility filter selects the branches visible to the detector.

The time operator supplies the non-periodic ordered runtime.  The integer toral
automorphism `T=[[0,1],[1,-1]]` orders the active/archive ladder through
`Tr(T^n)=(-1)^n L_n`, while the phase owner fixes the return increment
`alpha_D0=phi^-2`.  Tick order is therefore not a periodic clock embedded in a
background lattice; it is an ordered runtime whose detector-visible branches are
created only by finite return quotients.

The D0 structural return

\[
q_T=|ABCD|\,|V_{11}|=4\cdot11=44,
\qquad
m_T=|ABCD|+\operatorname{rank}(A_K)=4+3=7
\]

is the first terminal phase-return window.  Its admissible coprime branch count is

\[
\varphi_E(44)=20=d_{13}.
\]

Thus the terminal shell degree is the branch count of the first stable phase unfolding.

The second return is

\[
q_{EW}=2(|ABCD|+1)(2|V|+|ABCD|+1)=710,
\qquad
m_{EW}=(|ABCD|+1)d_{13}+|V_{13}|=113.
\]

Since \(710/113\) is a near-return for the Euclidean phase circumference, and

\[
\varphi_E(710)=280=|\Omega_8|\cdot 35,
\]

the electroweak radial depth is the per-\(\Omega_8\)-sector branch depth:

\[
D_{EW}=35.
\]

This section upgrades phase unfolding from an illustration to a structural theorem: later scale depths are repeated applications of the same finite tick \(\to\) phase quotient \(\to\) return modulus \(\to\) residue branch \(\to\) quotient mechanism.

## 06.30 Hurwitz-rigid phase generator and non-resonant spatial unfolding

The normalized D0 phase generator is not an arbitrary irrational angle.  The
primitive positive-response theorem gives `p+pВІ=1`, hence the return branch is

```math
\alpha_{D0}=p^2=\varphi^{-2}.
```

The physical phase increment is therefore `2ПЂ/П†ВІ`.  By the Hurwitz/continued-
fraction extremality of the `П†` class, this rotation is maximally resistant to
low-denominator rational locking.  In D0 terminology, it is the admissible phase
increment that suppresses uncontrolled metric arms in the unresolved complement.

This does not eliminate finite branches.  Branches appear only after a finite
readout quotient chooses a return modulus.  Thus the same chain has two layers:

```text
П†вЃ»ВІ irrational rotation  в†’ non-resonant archive smoothing;
finite return modulus q  в†’ residue branch geometry.
```

This closes the compatibility between macroscopic smoothness and finite branch
unfolding.

The combined owner is now `D0.Geometry.PhaseUnfoldingQuasicrystal`:

```text
toral_runtime_supplies_quasicrystal_order;
quasicrystal_order_not_periodic_lattice.
```

## 06.30a Time evolution over the П†-quasicrystalline hull

Time evolution over the D0 vacuum is represented as translation dynamics on the $\varphi$-quasicrystalline tiling hull. The continuous flow on this hull projects the discrete phase steps into smooth invariant averages under the cut-and-project setup. The formal Lean owner is `D0.Topology.TilingHull` (`d0_hull_has_phi_cut_project_origin`, `d0_hull_is_nonperiodic`, `d0_hull_supports_gap_labeling`). Verification is performed by `05_CERTS/vp_d0_tiling_hull.py` (`PASS_D0_TILING_HULL`).

## 06.31 П†-discrete RG as a typed forgetting step

The renormalization bridge is a typed forgetting map over the D0 scale ladder. At level `k`, the comparison scale is

```text
Ој_k = О›_act П†^{-k}.
```

A coupling `g_k` is transported by a finite-difference beta operator

```text
ОІ_П†(g_k) = (g_{k+1}-g_k)/(-log П†).
```

The continuous RG equation is the interpolation shadow of this ladder. The bridge is valid only relative to an explicitly declared scheme, threshold convention and field content. Changing the beta coefficients or thresholds after comparison is a hidden external repair and invalidates the comparison protocol.

## 06.31a Gap-labeled RG bands

The П†-discrete RG ladder may be read as a sequence of frozen operator bands. Spectral gaps in these bands are admissible only when they carry hull/K0 labels.

The formal Lean owner is `D0.Matter.KTheoryGapLabeling` (`gap_labeling_requires_frozen_operator` and `d0_gap_labels_are_countable`), and the verification certificate is `05_CERTS/vp_gap_labeling_d0_tiling_hull.py` (`PASS_D0_GAP_LABELING_TILING_HULL`).

## 06.32 Canonical cyclic phase distance and forgetting geometry

The forgetting geometry on finite fibers of size $N$ is equipped with a canonical cyclic phase distance:
\[
d_{phase}(i, j) = \frac{\min((i - j) \bmod N, (j - i) \bmod N)}{N}.
\]
This cyclic distance defines the metric on finite archive fibers, ensuring nonnegativity, symmetry, and identity of indiscernibles. It is verified in Lean core, providing the structural basis for forgetting phase transport without relying on ambient-continuum coordinates.

## 06.32.1 Boundary status for Hurwitz, Bianchi and gauge transformations

The local D0 phase class and the D0 internal dimensions 1/2/4/8 are Lean-owned through `D0.Algebra.D0InternalDimensionSelector`. Global Hurwitz exhaustion is external mathematical background, not an active core dependency for forgetting/phase transport.

The non-abelian layer is also a boundary layer. The flat tensor no-go shows that a naive tensor product of two skew sectors leaves the skew/vector sector, the non-abelian curvature module records the corrected finite skew-preserving construction, and the Bianchi module records the residual expansion only:

```text
D0.Gauge.FlatTensorNoGo
D0.Gauge.NonAbelianDiscreteCurvature
D0.Gauge.BianchiResidual
D0.Gauge.YangMillsKillingPositivity
D0.Gauge.MatrixRepGaugeTransform
```

The exact Bianchi statement is now closed on the graded incidence complex by `D0.Gauge.GradedBianchiIdentity`; the flat ungraded matrix residual remains a `NO-GO`. Finite gauge covariance is closed on the Wilson-link model by `D0.Gauge.WilsonLinkGaugeCovariance`. This closure is group-level and requires an associative `[Group G]` link carrier. Octonions are non-associative and cannot serve directly as the connection group; D0 uses the GaugeGroupDerivable boundary, meaning a derived associative automorphism group or matrix representation group.

## 06.33 Renormalized archive Laplacian as finite forgetting

The phase-canonical archive Laplacian is local on each cyclic fiber, but strict pullback compatibility under refinement is too strong. The correct finite forgetting statement is RG-type:

```text
L_{n+1}
  -> coarse-grain by the archive phase projection B
  -> B^T L_{n+1} B
  -> compare with L_n by scale plus residual.
```

Lean records the strict operator no-go, while the RG certificate `vp_archive_laplacian_rg_flow.py` checks the effective quadratic-form flow. For the canonical phase projection the projected residual is zero with scale `1`; the strict pullback commutator remains a rank-2 seam defect. This is now the runtime meaning of archive curvature in the forgetting layer: not deletion, but the measured failure of strict flat pullback transport.

## 06.34 Refinement seam as archive forgetting boundary

The current seam layer makes the forgetting boundary explicit. Energy descends exactly across the archive phase projection, but the lifted operator transport has a localized commutator:

```text
C_n = L_{n+1} B_n - B_n L_n.
```

The seam is the finite boundary where one additional refined phase point is folded back into the coarser archive cycle. The certificate `vp_archive_seam_curvature_action.py` verifies that this defect is rank `2`, supported on four seam entries, and has HS density `4`. Thus the archive forgetting boundary is not an uncontrolled loss term; it is the finite seam where curvature is measured.


## 06.35 Internal cone speed and the role of time

c_D0 = 1 is the invariant causal propagation bound of finite hull dynamics. It means one admissible tick cannot cross more than one finite adjacency layer. The SI value of light speed is unit printing, not the invariant.

The current edition separates three statements that were previously too easy to conflate:

1. D0 internal length tick: the primitive finite propagation section has one line unit and one tick unit.
2. Internal cone invariant: `internal_cone_speed_eq_one` states `c_D0 = 1` as a dimensionless cone-speed normalization.
3. SI metrology: `299792458 m/s` is the external unit conversion fixed by the SI definition of metre and second.

Therefore D0 does not fit the speed of light.  It fixes the internal causal cone before SI units are attached.  Any later physical comparison must preserve this separation; changing a unit convention cannot change the D0 causal section.

This also sharpens the time claim: time is not an extra continuum substance added to the graph.  It is the invariant registration order of finite propagation, and the smooth time coordinate is a large-scale language for that order.

## 06.36 Finite tick-gauge closure
Sync token: 06.36 v14 tick-gauge closure.

The active formulation replaces the shorthand `length tick = time tick` with a finite causal section. The owner is

```text
D0.Bridge.FiniteCausalTickSection
```

A finite record is admissible as an internal kinematic gauge only when the line tick and the time tick are two readouts of one common section tick.  Lean owners:

```text
D0.Bridge.finite_causal_tick_section_forces_same_tick
D0.Bridge.finite_causal_tick_section_cone_speed_eq_one
D0.Bridge.common_tick_rescaling_preserves_internal_cone_speed
D0.Bridge.asymmetric_ticks_not_internal_gauge
```

Thus `c_D0=1` is a theorem-level finite section invariant.  It is not the SI number `299792458 m/s`; that number belongs to external metrology and fixes the human unit convention.  Common rescaling of line and tick units preserves the invariant; asymmetric rescaling is an SI/export operation and cannot become a D0 core gauge.

The Lorentz-facing owner

```text
D0.Bridge.FiniteLorentzTickGaugeClosure
```

adds the terminal role signature `(1,3)` through

```text
D0.Bridge.finite_lorentz_tick_gauge_signature_closed
D0.Bridge.finite_lorentz_tick_gauge_no_euclidean_export
D0.Bridge.finite_lorentz_tick_gauge_no_split_export
```

The macroscopic Lorentz bridge may integrate this finite carrier into smooth spacetime kinematics, but it may not change the core cone speed, add a second elementary speed, or export Euclidean/split signature as the D0 internal geometry.

The spin-2 wave operator uses the same terminal tick/Lorentz carrier in concrete
finite form:

```text
eta4 = diag(1,-1,-1,-1)
k4   = (1,1,0,0)
u4   = (1,0,0,0)
```

This is a dimensionless `c_D0=1` carrier.  No SI calibration of `G_N` is
introduced here.

Gravity runtime exports remain internal until a bridge is declared:

```text
c_D0 = 1 tick gauge
eta4 terminal signature
delta0 finite readout cut
heat trace scale is internal, not SI time
```

## 06.37 П†вЃµ torus invariant and runtime quasicrystal geometry (Phi^5 Torus Invariant)

The D0 memory torus uses a dimensionless internal geometry invariant:

```text
a = phi^5
xi5 = phi^-5
R/r = (1 + xi5) / (1 - xi5)
```

The shell normalization is

```text
R-r = 1
R+r = a
```

so the three shell boundaries are `R-r`, `R`, and `R+r`. This runtime quasicrystal geometry is connected with the cut-and-project vacuum support and noncommuting torus shells. This introduces no SI length scale and no external mass unit; SI calibration remains a bridge layer.

### 06.37.1 Trace-heat time ladder

The same fixed time matrix controls the trace-heat runtime:

```text
Tr(T^n)=(-1)^n L_n
Delta_T = T^2
Tr((Delta_T)^m)=Tr(T^(2m))=L_(2m)
```

Thus heat moments of T^2 are even Lucas traces. A fixed detector reads T^n layers while the detector itself is unchanged; the changing object is the finite time-ladder state, not a retuned observer.

## 06.39 Phason flips and finite rewrite inertia

The runtime transport layer now has an operator-origin reading inside the
phi-quasicrystalline support.  Runtime transport through aperiodic support
requires phason flips under acceleration; inertia is the finite rewrite cost of
maintaining admissible support.

The finite owner is `D0.Physics.PhasonFlipInertia`:

```text
PhasonFlipCount
InertialCost
phason_flip_drag_positive_cost
```

The certificate `vp_phason_flip_inertia.py` checks that uniform admissible
phase transport has the minimal flip count, acceleration increases
window-crossing events, and the excess flip count is a scale-free rewrite cost
before any SI calibration.
