<!-- AUTO-ASSEMBLED from 01_BOOKS/BOOK_07_GRAVITY_LIMIT_AND_FINITE_GEOMETRY/ by tools/assemble_books.py — edit the per-section files, never this generated book. -->
# BOOK 07 — Gravity Limit and Finite Geometry

> **[Standard Physics Isomorphism].** D0's coined terms in this book read, in mainstream physics, as:
>
> - archive → integrated-out environment / environment bath (open-system trace-out)
> - forgetting map / coarse-graining → Wilsonian coarse-graining / CPTP decoherence channel
> - archive pressure → trace anomaly / entropic backreaction
> - terminal (destructive) readout → projective (von Neumann) / POVM measurement
> - phason → Goldstone mode of broken translation symmetry
> - carrier → representation (state) space
> - readout → measurement outcome (POVM effect)
>
> Genuinely-D0 (kept, defined in-text against the standard notion): the scene `K(9,11,13)`, the M1 admissibility axiom (no obligatory external catalogue), `δ₀`, `φ`, and *forcing* (= reductio ad absurdum against M1). Full crosswalk: the language-normalization Rosetta (`00_LANGUAGE_NORMALIZATION/D0_STANDARD_LANGUAGE_ROSETTA.md`).


> Scope: Finite spectral geometry, horizon/seam law, spin-2 carrier, finite gravity limits, and laboratory channel-clearing bridges.
> Claim discipline: Gravity closure is internal; astrophysical and laboratory analogues remain bridges/passports unless separately certified.
> External bridges, laboratory analogues, LIGO/GWOSC searches and survey comparisons are not promoted to core closure unless a named theorem/certificate/passport owner is stated.


## 07.0 Active gravity/QG sector law

Book 07 synthesizes finite spectral geometry, heat trace, feedback pressure, boundary capacity, rank localization, and UV tail cut.

**Horizon Emission Law (closed).**
A nonzero \( QUP \) transition defines a local measurement seam. A macroscopic horizon is capacity-saturated seam aggregation. Horizon emission is archive-to-retained boundary leakage under capacity saturation. The conjugate archive-to-retained operator \( F_Q^{emit} = Q U^\dagger P U Q \) is positive semidefinite. Greybody candidates are certified at the finite operator level (HORIZON-EMISSION-LAW).

**Measurement-Horizon Equivalence & Unified Horizon Seam.**
A nonzero \( QUP \) transition defines a local measurement seam. A macroscopic horizon is capacity-saturated seam aggregation.

**Optical Jet Observable Target (open).**
The conjugate emission law is cert-closed (PSD F_Q^emit = Q U† P U Q verified by the finite certificate with valid P+Q=I, PQ=0, deterministic U, explicit capacity/saturation/axis/transverse masks orthogonal).

Jet collimation is a frozen finite observable inequality after capacity profile and axis/transverse projectors are specified (HORIZON-JET-OBSERVABLE-CERT-SCAFFOLD; toy model J_axis > J_transverse holds in cert).

Horizon emission PSD law is cert-closed.
Jet observable is finite and frozen by axis/transverse projectors and capacity profile.
No empirical astrophysical jet fit is claimed.

Jet collimation is a finite observable inequality after axial/transverse projectors and saturation profile are frozen (OPTICAL-JET-COLLIMATION-TARGET). Optical jet backreaction is a finite observable on the saturated archive seam after the projectors are frozen. Do not claim empirical astrophysical jets are already fit.

```text
\mathsf P_{fb}=\beta^{-1}\partial_V\log Z_N
\mathsf P_{cap}=\partial_V E_{\partial}
```

Regimes:

```text
\mathsf P_{fb}>\mathsf P_{cap} -> expansion/acceleration
\mathsf P_{fb}=\mathsf P_{cap} -> stationary horizon/boundary
\mathsf P_{fb}<\mathsf P_{cap} -> contraction/capacity saturation
```

UV/QG regime:

```text
|T_M(z(L),F_N(L))| >= delta0^12
```

means smooth gravity language stops and finite D0 algebra is used. This is the D0 quantum-gravity regime.

The section order is: archive variation and finite stress; graph Laplacian and heat trace; boundary capacity; finite Lorentz/tick carrier; TT projection; finite wave operator; gauge/trace quotient; higher-curvature finite cut; spectral A2 / Einstein-Hilbert bridge; macro Einstein interface theorem.

Finite spin-2 owner:

```text
D0.Geometry.finite_spin2_tt_carrier_closed
```

This passport remains an observable-transfer boundary. The D0 memory torus is a separate internal shell geometry and does not replace the terminal four-role TT projector. Active contraction and archive expansion are eigen-branches of one toral automorphism; determinant invariant gives exact phase-volume balance.

## 07.1 Standard reading of finite gravity language

D0 gravitational language is read as finite spectral geometry. `Line covariance` means covariance of a finite line/edge transport structure. `Length-depth` is a spectral-depth/scale-separation invariant. `Archive boundary` means a boundary of the traced-out complement in the finite geometric response system.

## 07.2 Role of this book

Book 07 is the finite-geometry book of D0. It follows the detector foundation, mathematical proof spine, action stack, matter selector/readout protocols, verification discipline and runtime/forgetting theory. It therefore does not introduce gravity as a primitive smooth field. It constructs the gravitational shadow of finite readout.

The canonical chain is

```math
\boxed{
\text{finite line covariance}
\rightarrow g_{ij}^{D0}
\rightarrow \text{geometric heat trace}
\rightarrow D_L
\rightarrow \ell_P^{D0}
\rightarrow G_N^{D0}
\rightarrow \text{Einstein limit}
}
```

### Why a metric at all (the forced first link)

The first arrow above is not a modeling choice; it is forced. Four forcing
steps, each a contradiction against M1 (no external catalog), carry "finite
graph" to "Riemannian metric" before any heat-trace machinery is invoked.

**(F1) Numbers in CORE are κ-equivalence classes, not ℝ.** Two level sequences
\(a_k,b_k\in\mathbb{Q}(\varphi)\) are *equal* iff \(|a_k-b_k|\le\varphi^{-k}\).
This is what replaces the real line: the \(\varphi^{-k}\) Cauchy bound is the
operational tolerance, and a "true point between nodes" that is indistinguishable
at every level \(k\) would require an external label not derivable from any test
— an external catalog, M1-forbidden. So the continuum is the limit of refinements,
not a bag of points [^b07-3].

**(F2) The interval is a discrete variational object.** On level \(k\) the scene
is a weighted graph \(G_k\) with edge costs \(J_k(e)\); the squared interval is
the minimum path-cost, not a postulated bilinear:

```math
\mathrm{s}^2_k(u,v) := \min_{\gamma:\,u\to v}\Big(\sum_{e\in\gamma} J_k(e)\Big)^2 .
```

This is the bridge from graph to \(ds^2\) [^b07-4].

**(F3) The quadratic form is unique — Finsler/non-symmetric/cubic are
M1-forbidden.** Why \(g_{\mu\nu}dx^\mu dx^\nu\) and not a Finsler norm \(F(x,dx)\),
a non-symmetric form, or a higher-order one? A non-symmetric form
\(g_{\mu\nu}\ne g_{\nu\mu}\) singles out an orientation per pair — a *catalog of
orientations* the isotropic graph cannot supply. A cubic/higher form needs a
tensor \(C_{\mu\nu\lambda}\) with new dimensionless coupling constants not
derivable from the scalar cost \(J\) — a *catalog of tensors*. Both are
M1-forbidden. The only admissible isotropic large-number limit is the symmetric
bilinear (Riemannian) form, fixed by a tangent-space inner product alone
[^b07-5]. [^b07-1].

**(F4) Curvature without derivatives, against a canonical flat reference.**
"Flat" = "simplest" = minimal canonical description length. Fixing level \(k\) and
node count \(m\), let \(\mathcal{U}_{k,m}\) be the connected \(m\)-node neighborhoods
and \(Inv(U):=|D_{\min}(U)|\) the canonical-code length; then

```math
U^{flat}_{k,m} := \arg\min_{U\in\mathcal{U}_{k,m}} Inv(U).
```

The reference is admissible only if the choice is **κ-stable across refinement**
\(k\to k+1\): the representatives \(U^{flat}_{k,m}\) must form a Cauchy sequence in
\(\equiv_\kappa\); otherwise "flattest" depends on level/procedure and becomes an
external catalog — M1-forbidden [^b07-6]. Existence
and uniqueness follow because \(\mathcal{U}_{k,m}\) is finite and \(D_{\min}\) is
canonical (GOLDEN LEM II.4.APPX5.16.3a′). Crucially the flat reference **adds no
new parameters**: it uses nothing beyond \((V_k,E_k,J_k,Enc,D_{\min})\); replacing
the selection rule by "any admissible reference" would itself require an external
catalog of choice ⇒ M1-violation [^b07-7]. Curvature
is then the **edge-density defect** against this reference,

```math
K_k(x) := \rho_k(U_k(x)) - \rho^{flat}_{k,m},
```

with \(\rho\) the edge-per-node density: \(K>0\) is contracted (sphere), \(K<0\) is
sparse (saddle). Curvature in D0 is a neighbor count, not an abstraction — which is
exactly what makes finite gravity computable [^b07-8]. [^b07-2].

This neighbor-counting \(K_k\) is the seam/trace-heat curvature of the later
sections viewed at its origin: the heat-trace carrier still *owns* finite gravity
(§07.5 onward), but \(K_k\) is what the trace is tracing.

### Dimension is computed, never tuned

The effective dimension \(D\) is a κ-stable characteristic *extracted* from the
corpus's admitted spectral/heat-trace tests, not a dial. Any reading in which
\(D\) is "chosen so it comes out right" is M1-forbidden: a tuned \(D\) is an
external catalog of dimension. Throughout this book "\(D\ge 6\)" denotes a
*computed structural fact* about the scene, never a postulate [^b07-9]. This is the dimension-specific instance of the corpus-wide
no-retuning discipline.

The book separates three things:

1. the internal finite-geometric construction;
2. the SI/metrological Newton shadow;
3. the traced-out complement/cosmology boundary cross-reference.

The finite TT gravity carrier is a symmetric projected sector built from finite
edge/line probes and is compatible with the finite Hodge complex.

Horizon capacity saturation and black-hole A/4 are pressure-capacity balance regimes of the same closed vacuum feedback equation of state (\(\mathsf P_{fb}\) vs \(\mathsf P_{cap}\)). The heat-trace carrier still owns finite gravity; feedback pressure supplies the source/regime selector and boundary capacity supplies the horizon condition:

```math
\mathsf P_{fb}>\mathsf P_{cap}\ \text{expansion/acceleration},\qquad
\mathsf P_{fb}=\mathsf P_{cap}\ \text{horizon balance},\qquad
\mathsf P_{fb}<\mathsf P_{cap}\ \text{contraction/capacity saturation}.
```

The boundary-local holographic rank lemma and greybody leakage formulas are
supporting proof targets, not replacements for the heat-trace gravity carrier.

Refined CVFT rank localization uses `rank(F)=rank(QUP)` and, when `QUP` factors
through a declared boundary-channel space, `rank(F)<=dim B_boundary(P,Q)`. This
supports boundary localization of feedback entropy; it does not replace the
terminal A/4 capacity witness.

The UV feedback-tail cut uses a = |z| rho(F) < 1 and the Neumann bound. δ_0^{12} is the finite readout noise-floor (Shannon readout noise-floor / finite readout tolerance) for macroscopic extraction, not the analytic convergence radius of the feedback-resolvent series.

|T_M(z(L), F_N(L))| < δ_0^{12} means smooth heat-trace / macroscopic interface valid.
|T_M(z(L), F_N(L))| >= δ_0^{12} means finite feedback algebra regime (readout tolerance forces the finite description).

Only the first two are normative Book 07 material. Survey-level archive pressure and BAO/S_DE remain Book 08 material.

## 07.3 Gravity as downstream geometry, not a primitive continuum

D0 starts from finite registration, not from a differentiable manifold. Geometry becomes available only after the detector has produced a stable line covariance. The metric is therefore a coarse-grained shadow of covariance among finite line probes:

```math
g_{ij}^{D0}=\operatorname{Cov}_{K_\varphi}(\ell_i,\ell_j).
```

The bridge to continuum geometry is a functorial/macroscopic shadow:

```math
g_{ij}^{D0}\xrightarrow{\mathcal F_{macro}} g_{\mu\nu}.
```

Definition. The D0 gravity construction is a finite-readout spectral geometry from which the metric description emerges as the stable large-scale language. It is not offered as a replacement for general relativity.

## 07.4 Causal section and metrological separation

The internal causal section is already fixed in the foundation:

```math
\ell_0^{D0}=1,\qquad \tau_0^{D0}=1,\qquad c_{D0}=1.
```

The normalization `c_{D0}=1` is not a unit convention bolted on after the fact: `C := lim C_k`
is the in-system limit speed of distinguishability propagation, so the CORE scale is *forced* to
the choice that makes it unit; any "c in m/s" lives in the BRIDGE export and is not a corpus
parameter [^b07-10]. This is why the causal section is a section and
not a tuning knob.

### What the causal section is a section *of*: the closed light-cycle

The lightlike scale `c_{D0}=1` is the maximal-speed transition budget, and that budget is exactly
what a *closed light-cycle* runs on. A closed light-cycle `P` is a path `γ` that is (1) closed
(`v_end = v_start`), (2) built from maximally-fast (lightlike) transitions, and (3) stable under
small graph variations — i.e. **topologically protected**. Its period `τ(P)` is the length of the
cycle in time, counted in `ν* = 1/9` steps [^b07-11]. The causal section
`ℓ_0^{D0}=τ_0^{D0}=1` is therefore the unit-period section against which every `τ(P)` is read off:
metrology here is the act of expressing `τ(P)` against this fixed lightlike section.

A massless line is the degenerate case: it has no internal closed cycle, hence no rest return and
no period to read against the section — its mass-square vanishes identically. The single-line /
photon-as-massless-line statement is owned upstream (`m_γ^2 ∝ ‖D_B^γ‖^2 = 0`, BOOK_01 §01.9); this
section only uses it as the `τ(P)→∞` boundary of the light-cycle picture.

### Mass is not exported as a parameter — it is *found* as a topological defect

Mass enters this book only through the causal section's metrology, and the reason it is legitimate
to treat it as metrology (not as a hidden gravity parameter) is structural: in CORE there is no
"mass" other than the density of stable closures. We do **not** introduce mass as a charge; we find
it as a topological effect [^b07-12].

```math
\varrho_k(x) := \frac{\sum_{P\in\mathrm{Cycles}(x)} \tau(P)^{-1}}{\mathrm{Vol}(U_k)}.
```

The forcing is a strict reduction-to-substance under M1: assume a "true mass" `M_true` irreducible
to cycles and geometry. It would need a coupling coefficient `α` to curve the graph and a separate
law of inertia — i.e. an **external catalog** of rest masses and charges not derivable from the
realization structure `Σ`. That catalog is exactly what M1 forbids. The only survivor is to build
matter from geometry: the unique stable localized structure in a dynamical graph is a
self-sustaining cycle (a soliton), its energy `E = hν` is proportional to its closure frequency
`ν ∼ 1/τ`, and its inertia is the topology's resistance to retrajectorying the cycle. "Mass" is the
self-linking of the causal net; a "particle" is a vortex in the history graph. Smaller cycle ⇒
higher frequency ⇒ heavier [^b07-13].

Status: CORE-FORCING [^b07-14].

This is what makes the electron terminal scale below an *honest* metrological bridge and not an
adjustable gravity dial: the scale it imports is the SI shadow of a closure period `τ(P)`, a counted
topological invariant, not a free coupling. The q-mass / residual-curvature realization of `τ(P)`
for concrete states is owned by BOOK_07 §07.12 (matter cross-reference) and the horizon mass-defect
passport by §07.48; this section cites them rather than re-deriving the defect.

### Operational curvature: gravity is neighbor-counting, hence computable

The same discipline applies to curvature. Curvature in D0 is not an abstraction added on top of the
section; it is the result of counting neighbors against the flat reference `U^flat` — the
density-defect `K_k(x) := ρ_k(U_k(x)) − ρ^flat_{k,m}`. Because that defect is a finite count, gravity
is **computable** [^b07-15]. Coupled with `K ∼ ϱ` (curvature
proportional to closure density, with `f(0)=0` forced by the vacuum/flat boundary condition), this is
the CORE statement whose covariant smooth shadow is the Einstein tensor; the numeric coefficient
`a_unit` is a unit choice fixed only at the BRIDGE step, never a new dimensionless physical constant
[^b07-16]. Book 07 keeps this as the *reason* the dimensionless
scale-separation invariant exported below is well-defined, not as a re-derivation of the field
equation (that smooth-limit bridge is owned downstream).

### SI export and the single-section discipline

The SI export of this section uses the terminal matter/readout bridge:

```math
\tau_0=\frac{h}{38m_ec^2},\qquad
\ell_0=c\tau_0=\frac{h}{38m_ec}.
```

Book 07 uses this only as metrology. It is forbidden to use the electron terminal scale as a hidden
adjustable gravity parameter — by the topological-defect forcing above, that scale is a counted
closure period in SI clothing, so promoting it to a free dial would smuggle in exactly the external
substance catalog M1 forbids. The single-section discipline is

```math
\Lambda_{act}=\frac{h}{\tau_0}=38m_ec^2,
```

with action-scale closure assigned to Book 03/04 (`Λ_act=38`) and dimensionless spectral
scale-separation invariant export assigned here.

Type safety: `D_L` is the dimensionless finite spectral scale-separation invariant.  The
Planck length `ell_P` and Newton coefficient `G_N` are SI-calibrated
single-section shadows obtained only after an `ExternalSICalibration` bridge is
declared through `derive_physical_observables`; they are not
`DimensionlessCoreTraces` outputs.
## 07.5 Finite line covariance and spin-2 carrier

The finite graph/cell support defines covariance of line probes. A spin-2 continuum field appears only after symmetric line-covariance readout stabilizes:

```math
g_{ab}^{runtime}\sim\langle \Pi_a\partial,\Pi_b\partial\rangle_{G^-1}.
```

The spin-2 structure is therefore not postulated as a primitive graviton field in the core. It is the continuum representation of quadratic covariance of finite geometric probes. In the external bridge this is the usual tensorial metric perturbation grammar.

### Why the carrier is a covariance readout and not a background field

The reason spin-2 enters as a *readout* of finite covariance rather than as a primitive field propagating on a fixed stage is forced one level up, in the field dynamics of the mechanism. M1 forbids an external catalog, and a fixed Minkowski background *is* such a catalog: it is geometry handed to the theory from outside the refinement that distinguishes itself. So the path integral over fields on a fixed stage cannot be the core object.

**CORE QFT partition sum (no path integral).** The continuum path integral is replaced by a finite diagram sum weighted by the spine constant `phi` [^b07-18]:

```math
\mathcal{Z}_k:=\sum_{\Gamma}\varphi^{-A(\Gamma)},
```

where `A(Gamma)` is the area/action of diagram `Gamma` in the graph. This is a distinct object from the feedback partition function `Z_N=Tr exp(-b Delta) det(I-zF)^-1` (the spectral/feedback partition owned by BOOK_05 via the `F_N` operator owned by BOOK_01 §01.0); `Z_k` is the diagram-sum over memory paths, not the spectral trace, and the two must not be collapsed.

**Loops are memory cycles.** Feynman loops in D0 are real physical cycles on the graph; "virtual particles" are circulation of information in the finite memory of the system (the internal count `N_int`), not excitations of an external vacuum [^b07-19]. This is what makes the line-covariance readout above an internal quadratic statistic rather than a propagator on a stage.

**Background independence (the forced step).** Because a fixed Minkowski background is forbidden by M1, the quantum-gravity partition sum ranges over the geometries themselves — the graphs `G` are summed, not assumed [^b07-20]:

```math
\mathcal{Z}^{\mathrm{QG}}_k:=\sum_{(G,J)\in\mathfrak{G}_k}\varphi^{-A(G,J)},
```

where `G_k` is the set of level-`k` geometries **generated by the refinement procedure `Sigma`** — a computable set, not an external measure "over all graphs". The theory is therefore background-independent by construction: no stage is supplied, only the refinement that builds the stages. The spin-2 carrier is the coarse-grained quadratic covariance read off *across* this sum over geometries, which is precisely why it cannot be a primitive field living on any one of them.

[^b07-17] — the identification of the finite TT carrier with the coarse limit of `Z^QG_k`'s quadratic covariance is a forcing claim awaiting its verification obligation; the finite carrier closure below is its existing partial anchor.

### Finite TT carrier closure

The finite carrier is explicit at the Lean owner.  A finite TT mode carries a symmetric response matrix, zero trace and a transverse condition.  This does not by itself prove the full smooth graviton QFT.  It closes the finite D0 carrier needed before the Einstein--Hilbert bridge is invoked, and supplies the partial anchor for the PROOF-TARGET above: it exhibits the symmetric, traceless, transverse finite object whose continuum representation is the spin-2 covariance readout.
## 07.6 Geometric heat trace and Einstein interface

The geometric operator `K_geometry^phi` carries the finite heat trace. The Einstein interface is the macro limit of the finite trace-heat/stress carrier. The heat expansion takes the form:

```math
\operatorname{Tr}K_{geometry}^\varphi
\longrightarrow
\int\sqrt{-g}\,(a_0+a_1R+\cdots).
```

Equivalently,

```math
\operatorname{Tr}e^{-u\Delta_g}
\sim (4\pi u)^{-2}\int d^4x\sqrt{g}\,(a_0+a_1uR+O(u^2)).
```

The Einstein--Hilbert shadow is

```math
S_{EH}=\frac{1}{16\pi G_D}\int d^4x\sqrt{-g}\,R.
```

The status of this statement is a carrier/bridge theorem: D0 fixes the finite support, heat-trace grammar and coefficient bridge; the continuum Einstein action is the stable large-scale language.

## 07.6a Trace–Heat geometry over the D0 tiling hull

Definition. The heat trace is the macro spectral shadow of finite operators over the D0 tiling hull. Curvature is the detector-visible response of this spectral shadow after finite coarse-graining.

This is closed by the Lean owner and confirmed by the finite verification certificate.

## 07.7 Length-depth theorem before Newton

The main gravity invariant is the dimensionless spectral scale-separation invariant factor:

```math
D_L=\Omega_8\varphi^{V_9V_{11}}\left(1+\frac{\delta_0}{V_{13}}\right).
```

In the active graph values used in the corpus,

```math
V_9V_{11}=99,\qquad V_{13}=13,
```

so the commonly used form is

```math
D_L=\Omega_8\varphi^{99}\left(1+\frac{\delta_0}{13}\right).
```

The Planck length shadow is not an input:

```math
\ell_P^{D0}=\frac{\ell_0}{D_L}.
```

Only after the SI export of `ell0` is attached does the Newton coefficient
appear as an SI-calibrated single-section shadow:

```math
G_N^{D0}=\frac{c^3(\ell_P^{D0})^2}{\hbar}.
```

`D_L` remains the dimensionless core/certificate invariant in this chain.
`ell_P` and `G_N` are downstream SI representatives and cannot be used to
repair the core dimensionless spectral scale-separation invariant value.  This ordering is non-negotiable:

```text
dimensionless spectral scale-separation invariant first; Newton coefficient second.
```

A script or derivation that starts from measured `G_N` to repair `D_L` violates the book.

## 07.8 Runtime gravity coefficient and area normalization

The finite area coefficient retained from the source gravity sector is

```math
\beta_{area}=\frac{3}{640\pi^2|E|\varphi^4}.
```

The runtime gravity coefficient is written as

```math
G_{runtime}=\frac{1}{16\pi\kappa_B\beta_{area}}.
```

This is not automatically the SI Newton constant. It is a finite runtime coefficient inside the geometric probe grammar. The SI bridge requires the dimensionless spectral scale-separation invariant and terminal metrology steps above.

The corresponding finite boundary entropy form is

```math
S_{D0}(R)=\frac{\beta_{area}R^2}{4}.
```

and the temperature scaling is

```math
T_{D0}(R)\propto R^{-1}.
```

## 07.9 Boundary, horizon and archive interpretation

At a finite boundary the detector can saturate:

```math
\sigma(R)\to1,\qquad \operatorname{Cost}_R(\partial)\to\infty.
```

The horizon statement is therefore a finite-readout statement before it becomes a spacetime ontology. A boundary map

```math
Y:\mathcal H_R(R)\to\mathcal H_N(R)
```

sends inaccessible active boundary information into the traced-out complement/null sector. Book 07 uses Book 06 forgetting theory here: loss of active readout is not deletion of total mathematical information. The correct statement is

```math
\text{loss of active readout}\neq\text{loss of total information}.
```

The horizon/archive interpretation is allowed only after the finite boundary quotient has been declared.

## 07.10 Higher-curvature finite cut

Near the boundary, higher-curvature terms must be controlled by finite resolution. The hard cut row is retained as

```math
\eta_{HC}(L)=\left(\frac{\ell_P^{D0}}{L}\right)^2.
```

with the cut condition

```math
\mathcal I_{12}=\delta_0^{12},
```

and

```math
\eta_{HC}(L)<\mathcal I_{12}
\quad\Longleftrightarrow\quad
L>\frac{\ell_P^{D0}}{\delta_0^6}.
```

The cut rule is not an arbitrary EFT cutoff. It is a finite-detector resolution rule expressed in gravity variables.

(The SI-calibrated representative values of `I_{12}`, `L_cut`, and `η_HC(L_cut)`, and the active cut certificate, are owned by §07.19.3; not restated here.)

### 07.10.1 Why the spatial cone is isotropic: Schur lock on the hull pushforward

The cut above bounds the *magnitude* of the higher-curvature row. A prior question is forced first: why is the residual spatial cone isotropic at all, so that a single scalar `η_HC(L)` (not a direction-dependent tensor) is the right carrier? The answer is not assumed — it is forced by the representation theory of the D0 hull symmetry.

Three roles must not be conflated [^b07-23]:

```text
Ω8 = ABCD × {+,−}  enforces central symmetry of the acceptance window
                    (removes the odd dispersion terms);
hull pushforward    controls the physical spatial cone;
SI calibration      is bridge-only, never a forcing input.
```

For the physical direction map `u : X → S²`, the hull-pushforward second moment is

```math
\Sigma=\int_{\mathcal X} u\otimes u\,d\mu .
```

When the physical momentum carrier is an **irreducible orthogonal representation** of the D0 hull symmetry, Schur's lemma forces `Σ` to commute with every group element, hence

```math
\Sigma=c\,I_3 .
```

The normalization `Tr Σ = 1` (the pushforward of the unique ergodic hull measure on `S²`) then pins the constant:

```math
\Sigma=\tfrac13 I_3 .
```

So isotropy of the residual cone is a *theorem*, not a symmetry ansatz: any anisotropic `Σ` would split the carrier into a proper invariant subspace, contradicting irreducibility. This is exactly what licenses the scalar finite cut `η_HC(L)` above — there is no preferred direction left for a tensor correction to live in.

**[^b07-21]** — the irreducibility of the physical momentum carrier under the hull symmetry, and the uniqueness/ergodicity of the hull measure whose pushforward gives `Tr Σ = 1`, are not yet discharged by a registered `vp_*` cert. (The hull objects `vp_d0_tiling_hull.py`, `vp_gap_labeling_d0_tiling_hull.py`, and the Lorentz-signature cert `vp_galois_lorentz_signature.py` are adjacent but do not yet close *this* Schur-isotropy obligation.)

### 07.10.2 The higher-curvature coefficient is derived, not fitted

With isotropy forced, the dimensionless higher-curvature finite-cut coefficient is bounded with no external input [^b07-24]:

```math
|c_4| \le \frac{5744}{33}\,\delta_0^{12}.
```

Every factor is structural:

```text
δ0^12  = the same finite-resolution power as the cut I_{12}=δ0^12 (12 = 2×6, the boundary readout depth);
33     = |V| total scene cardinality (the K(9,11,13) capacity ladder, 9+11+13 = 33);
5744   = 16 × 359,
  359  = total edge count of the holographic carrier (the minimal Q8~Ω8 / K(9,11,13) graph),
  16   = 4² = ABCD², the square of the 4-dimensional terminal quotient ABCD of Ω8.
```

The `16 = ABCD²` factor rests on the owned reading `ABCD = D2×D2 = 4` (BOOK_01 §01.7 owns the ABCD/Ω8 capacity alphabet, where `|V| = 33` is also fixed). The bound is therefore read off the symplectic structure and edge cardinality of the minimal carrier — `c_4` is a *derived* ceiling, not a tunable EFT Wilson coefficient. This is the higher-curvature analogue of the no-knob discipline the whole book runs on: the cut sets *where* the row dies, this coefficient sets *how large* it may be before it dies, and both are functions of the same finite carrier.

**[^b07-22]** — the edge tally `359` of the holographic carrier and the assembly `5744/33` into the `c_4` ceiling are not yet discharged by a registered `vp_*` cert. (`05_CERTS/higher_curvature_bound_report.json` records a *separate* trace-power floor check at curvature orders 3/4/5 and does not certify this `δ0^12` coefficient; do not conflate the two.)

### 07.10.3 The 12D→4D compactification fold and the 2⁶ = 64 degree-of-freedom difference

The finite cut is also a *dimensional* statement: it is the resolution at which the outer scene has already folded down to the observed 4D projection. That fold is carried by the compactification operator `Y` [^b07-25]:

```math
Y : 12D \to 4D \;(+\,6\ \text{bit}).
```

The `+6 bit` is **not new physics**. It is the bookkeeping label for the binary cascade

```math
2^{6}=64
```

read as the *difference of degrees of freedom* between the outer shell and the observable 4D projection — the information the fold `Y` traces out.

The status of `64` is the load-bearing point [^b07-26]. The number `64 = 2⁶` must appear as a **derived difference / convolution** — either as the `2⁶` information cascade, or as "outer shell capacity minus inner address capacity" in the concrete corpus formulas — and **never as a hand-tuned multiplier**. A postulated `64` would be exactly the kind of free knob the anti-numerology firewall (BOOK_00) rejects; the forcing is that it falls out of the fold `Y`, not that it is inserted to make a number work. This is why the `64` lands here, beside the derived `c_4` coefficient: both are quantities the dimension/finite-cut locus is allowed to *carry* only because the carrier *forces* their value.

**Status: forced definition (GOLDEN-owned)** — `Y` and the `2⁶ = 64` dof-difference reading are imported as the GOLDEN forcing for the 12D→4D fold; no D0 cert obligation is created by restating them, but any downstream claim that *uses* a numeric `64` must trace it back to this difference/convolution, not assume it.

## 07.11 pi0 is phase holonomy, not Newton repair

The finite-cycle phase generator appears in the gravity archive because it participates in holonomy and boundary normalization:

```math
\pi_0=\frac65\varphi^2.
```

It is not a license to tune Newton's constant. The allowed use is phase/holonomy accounting, for example

```math
\Delta\Phi_N=2N(\pi_0-\pi).
```

The forbidden use is

```text
choose a power of pi0/pi after seeing the target value of G_N.
```

This guardrail is essential because several corrected gravity bridges are audit trails. The normative path is dimensionless spectral scale-separation invariant before Newton.

## 07.12 q-mass, residual curvature and matter cross-reference

### Why mass is a closure density, not a substance (forcing)

Before the `q_mass`/`q_res` bookkeeping makes sense, the geometry side has to say what mass *is*. The forced answer is structural, not material: in CORE there is no mass-stuff, only the density of light-like cycles that close.

**[COR 07.12.M] Mass = cycle-closure density [^b07-28]. [^b07-27].** A light-like cycle `P` is a stable closure of the fastest transitions on a refinement level `k` [^b07-29]. Its period `τ(P)` is the cycle length in refinement ticks (DEF II.4.5). The closure density at `x` is the forced observable

```math
\varrho_k(x):=\frac{\sum_{P\in\mathrm{Cycles}(x)}\tau(P)^{-1}}{\mathrm{Vol}(U_k)}
```

(DEF II.4.6). The forcing-by-contradiction (DEF-0.2.2) runs: *any* "mass-substance" would require an external catalog of coupling parameters to fix its inertia ⇒ that catalog is exactly what M1 forbids ⇒ no mass-substance survives ⇒ mass in CORE is exhausted by `ρ`. Therefore

```math
\text{mass}\ \leftrightarrow\ \varrho\qquad(\text{closure-density identity, not a metaphor}).
```

"Looped light" is an intuitive image only; it is **not** a separate postulate and adds no parameter. Smaller `τ(P)` (faster closure) means larger mass — the triangular cycle `τ=3` contributing `~1/3` is the minimal worked instance (GOLDEN App. II.4.A).

This is the geometry-side root that the matter sector reads downstream: BOOK_04 (THE 04.6.π.D) takes the per-state rest frequency `ω₀:=τ(P)⁻¹` of a single light cycle and reads `E²−p²=ω₀²` off it rather than posting a free mass; the rest-mass-as-spectral-gap packaging (GOLDEN THE II.4.8, BRIDGE-tier) and the `K0` gap labels live there. BOOK_07 does **not** re-derive that spectrum — it only holds the closure-density origin so the gravity equation stays typed and the residual bookkeeping below stays a *cross-reference*, not a knob.

### q-mass and residual as cross-reference

The q-mass and boundary residual terms are cross-reference material, not independent gravity knobs:

```math
q_{mass}=(1+\delta_0^3)^{-1},
```

```math
q_{exact}=q_{mass}q_{res}.
```

Here `q_mass` is the closure-density identity above, re-marked in `δ_0` units; it carries no freedom beyond `ρ`. The interpretation belongs to the matter/EW boundary layer in Book 04 and to the residual cut discipline in Book 05/07. It is forbidden to use `q_res` as a scalar-curvature fit parameter.

The canonical gravity equation must remain typed:

```math
\text{closed dimensionless spectral scale-separation invariant}\rightarrow \ell_P^{D0}\rightarrow G_N^{D0},
```

not

```math
\text{residual mismatch}\rightarrow \text{new scalar repair}.
```

The closure-density identity is what makes this typing forced rather than stylistic: there is no mass-substance left over to soak up a "residual mismatch" into a new scalar, so `q_res` can only ever be a closed cross-reference back to `ρ` — never an Einstein-equation source term invented to repair a fit.
## 07.13 Einstein limit and carrier status

The finite support admits a Lorentz/Einstein carrier:

```math
\boxed{(1,3)}.
```

The continuum carrier statement is

```math
S_{D0}^{geom}\longrightarrow\frac{1}{16\pi G_N}\int R\sqrt{-g}\,d^4x.
```

This is a bridge theorem, not a claim that D0 begins with a smooth pseudo-Riemannian manifold. The manifold language is a stable external completion of finite geometric readout.

## 07.14 Cosmology and archive pressure cross-reference

Book 07 defines the geometric and boundary conditions that make an archive-pressure interpretation meaningful. It does not perform survey fitting and does not derive BAO parameters.

The archive-pressure operator preserved from the source gravity file is

```math
\mathsf P_{archive}^{D0}=-\frac{\delta_0^8}{30}\Pi_N,
```

with trace

```math
\operatorname{Tr}_N\mathsf P_{archive}^{D0}=-\delta_0^8.
```

Its cosmological use is handed to Book 08, where the allowed direction is

```math
\text{finite archive/boundary operator}
\rightarrow
\text{S_DE / survey transfer comparison protocol}.
```

The forbidden direction is

```math
\text{survey residual}
\rightarrow
\text{invent boundary/archive operator}.
```

## 07.15 Falsification rules for gravity claims

A gravity claim fails if it does any of the following:

1. starts from a smooth metric as primitive D0 input;
2. uses measured `G_N` to choose `D_L`;
3. uses `pi0` as a Newton repair parameter;
4. uses `q_res`, boundary residual eigenvalue r_∂ or boundary information as hidden scalar fitting;
5. collapses runtime `G_runtime` into SI `G_N` without dimensionless spectral scale-separation invariant and metrology;
6. imports cosmological survey residuals into the definition of the gravity operator;
7. treats terminal boundary quotient into the traced-out sector loss as literal deletion rather than loss of active readout.

The positive gravity chain is

```math
\text{finite line covariance}
\rightarrow g_{ij}^{D0}
\rightarrow \text{heat trace}
\rightarrow D_L
\rightarrow \ell_P^{D0}
\rightarrow G_N^{D0}
\rightarrow \text{Einstein bridge}.
```

## 07.16 Claims inherited from the theorem database

**Canonical source: the claim registry** (`09_LEAN_FORMALIZATION/docs/CLAIM_TO_LEAN_MAP.csv` / generated `03_THEORY_MAP/theory_status_map.csv`) is the single source of truth for claim IDs and `release_status`. This table is the **Book 07 sector view** — the `Book 07 role` column is its only sector-specific content; the statuses mirror the registry and are not edited here independently. The parallel evolution-sector view is §06.17.

| Claim ID | Status | Stage | Claim | Book 07 role |
|---|---|---|---|---|
| `D0-FOUND-003` | `CORE-FOUNDATION` | Foundation | Minimal continuum-measurement skeleton | reference to Books 01-04; used in gravity bridge |
| `D0-MATH-001` | `D0-RESOLUTION-EXACT` | Quotient/Resolution | Finite phi-runtime and stop ideal | reference to Books 01-04; used in gravity bridge |
| `D0-METRO-001` | `CORE-FOUNDATION` | Bridge/Dictionary | Single causal line/tick invariant | reference to Books 01-04; used in gravity bridge |
| `D0-METRO-002` | `SINGLE-SECTION-OUTPUT` | Single Section | Lambda_act single action section | reference to Books 01-04; used in gravity bridge |
| `D0-BOUND-001` | `D0-RESOLUTION-EXACT` | Quotient/Resolution | Boundary Residual Eigenvalue r_∂ and boundary curvature residual | reference to Books 01-04; used in gravity bridge |
| `D0-THERMO-001` | `CORE-MEASUREMENT` | Quadratic Readout | Finite-window entropy from archive forgetting | Book 06 runtime reference; boundary thermodynamics use |
| `D0-CARRIER-002` | `CORE-SUPPORT` | Finite Support | Lorentz and Einstein-Hilbert carrier | BOOK_07 normative |
| `D0-GRAV-001` | `SINGLE-SECTION-OUTPUT` | Bridge/Dictionary | Length-depth theorem and Planck/Newton shadow | BOOK_07 normative |
| `D0-GRAV-002` | `SINGLE-SECTION-OUTPUT` | Bridge/Dictionary | Newton coefficient finite-cycle holonomy closure | BOOK_07 normative |
| `D0-GRAV-003` | `D0-RESOLUTION-EXACT` | Quotient/Resolution | Higher-curvature finite cut rule | BOOK_07 normative |
| `D0-COSMO-001` | `CORE-MEASUREMENT` | Quadratic Readout | Archive-pressure operator | Book 08 cross-reference; gravity boundary only |
| `D0-COSMO-003` | `ACTIVE-PASSPORT` | External Comparison Protocol | Boundary dark survey-driver kernel | Book 08 cross-reference; gravity boundary only |
| `D0-COSMO-004` | `SINGLE-SECTION-OUTPUT` | Single Section | Cosmological archive-pressure coefficient closure | Book 08 cross-reference; gravity boundary only |
| `D0-COSMO-005` | `EMPIRICAL-PASSPORT` | External Comparison Protocol | S_DE finite-window BAO archive-transfer shape | Book 08 cross-reference; gravity boundary only |
| `D0-PI0-001` | `CORE-FOUNDATION` | Quotient/Resolution | pi0 finite-cycle versus pi continuum generator | BOOK_07 normative |

## 07.17 Cross-book boundary summary

| Topic | Book 07 treatment | Final proof/comparison protocol location |
|---|---|---|
| condensed support, `p+p^2`, `delta0`, ABCD | reference only | Books 01--02 |
| `Lambda_act`, action scale | metrological input discipline | Book 03 |
| electron terminal section, q-mass, EW residual | matter/metrology cross-reference | Book 04 |
| promotion, forbidden shortcuts, cert status | referenced | Book 05 |
| forgetting, entropy, active/archive quotient | boundary use | Book 06 |
| line covariance, heat trace, `D_L`, `G_N`, Einstein limit | normative | Book 07 |
| archive pressure as BAO/S_DE survey transfer | cross-reference | Book 08 |

## 07.18 Integrated continuum-division boundary-memory theorem and QG cut rule

Two gravity-side closures are normative here: the continuum-division boundary-memory theorem and the residual quantum-gravity cut rule.

The finite D0 geometry may be projected to a continuum heat-trace expansion only as a forgetting image:

```math
\operatorname{Tr}e^{-u\Delta_g}
\sim
(4\pi u)^{-2}\int\sqrt{-g}
\left(a_0+a_1uR+a_2u^2\mathcal I_2+\cdots\right).
```

The Einstein-Hilbert term is the retained large-scale readout.  Higher-curvature terms are governed by the dimensionless suppression

**EH macro-interface closure.**
Finite A2 variation + finite Bianchi + conserved stress pairing selects the unique Einstein tensor class as the macro response.
The EH macro-interface is therefore closed up to the standard smooth-limit dictionary: finite A2 variation + Bianchi selects the Einstein tensor class.
SI G_N remains the single-section metrological shadow.

```math
\eta_{HC}(L)=\left(\frac{\ell_P^{D0}}{L}\right)^2.
```

With the scalar stop ideal

```math
\mathcal I_{12}=\delta_0^{12},
```

D0 imposes the cut rule

```math
\eta_{HC}(L)<\mathcal I_{12}
\quad\Rightarrow\quad
\text{higher-curvature terms are below classical D0 readout resolution.}
```

Equivalently,

```math
L>L_{cut}=\frac{\ell_P^{D0}}{\delta_0^6}
```

is the Einstein-Hilbert readout domain, while for \(L\le L_{cut}\) the continuum correction language stops and the finite D0 support/readout algebra must be used directly.

This theorem is a domain split, not an added quantum-gravity coupling.  It prevents a residual ``higher-curvature'' phrase from becoming an open-ended parameter reservoir.
## 07.19 Integrated gravity and finite-cut closure cells

### 07.19.1 Dimensionless spectral scale-separation invariant theorem and Planck/Newton shadow

D0 derives a dimensionless spectral scale-separation invariant map before any Newton coefficient is named:

```math
D_L=\Omega_8\varphi^{V_9V_{11}}\left(1+{\delta_0\over V_{13}}\right).
```

The semantic factors are fixed:

```text
Ω8     = full-cycle multiplicity,
V9V11  = 99 witness-to-transport heat depth,
1+δ0/V13 = terminal-shell leakage.
```

The Planck/Newton quantities are SI-calibrated shadows of the same single
length section:

```math
\ell_P=\ell_0/D_L,
\qquad
G_N = \frac{c^3 \ell_P^2}{\hbar}.
```

The certificate records the SI representative values:

```text
D_L = 3.951771012845559e21,
ℓ_P^{D0} = 1.6157380866594502e-35 m,
G_N^{D0} = 6.670031309826955e-11.
```

**Closure.**  The gravity bridge now has its active proof-cell: dimensionless spectral scale-separation invariant first, typed SI calibration second.  `G_N` and `ell_P` are
single-section shadows, not independent anchors or core trace outputs.

This proof-cell is backed by the finite certificates.

### 07.19.2 Newton coefficient finite-cycle holonomy

The finite-cycle holonomy row is the same single-section completion read
through the Einstein/Planck dictionary.  It is not a separate fit to CODATA.
The gravity completion certificate gives the same `D_L`, `ell_P`, and `G_N`
after the external SI section is declared, and stress-tests nearby denominators
to show the chosen terminal leakage is not arbitrary.

**Closure.**  The Newton coefficient row is closed as an SI-calibrated
finite-cycle holonomy shadow of the dimensionless spectral scale-separation invariant theorem.  Comparison to CODATA
is a benchmark, not an input.

This row is backed by the finite gravity-completion certificates.

### 07.19.3 Higher-curvature finite cut rule

The higher-curvature language is cut off when the continuum correction falls below D0 readout resolution:

```math
I_{12}=\delta_0^{12},
\qquad
\eta_{HC}(L)=\left({\ell_P\over L}\right)^2.
```

The transition scale is

```math
L_{cut}={\ell_P\over\delta_0^6},
\qquad
\eta_{HC}(L_{cut})=\delta_0^{12}=I_{12}.
```

The certificate records

```text
I12 = 7.31282200941126e-12,
L_cut = 5.97487000645251e-30 m,
η_HC(L_cut) = 7.31282200941126e-12.
```

**Closure.**  Below this cut the active description is finite D0 support/readout algebra, not a new continuum higher-curvature sector.  No new gravitational anchor is introduced.

This cut rule is backed by the finite residual-targets certificate.

## 07.20 Gravity depth uniqueness closure

The gravitational line-depth exponent is not selected by numerical fit.  It is selected by the finite type of the map:

\[
\text{observed line sector}\times\text{comparison line sector}
\longrightarrow\text{dimensionless spectral scale-separation invariant covariance}.
\]

The only admissible bidegree using the finite carrier endpoints is

\[
D_L=V_9V_{11}=99.
\]

A sum `V9+V11`, a full carrier count `33`, or a rank/nullity expression changes the type of the map and therefore fails before numerical comparison.  This is the gravity version of stiffness closure: the large exponent is a finite map-degree, not a tuneable coefficient.

## 07.21 Terminal boundary of traced-out complement and the A/4 law

A D0 horizon is typed as a terminal boundary of traced-out complement. At finite stage the boundary is tiled by oriented readout quanta. The terminal four-role quotient `ABCD` groups four oriented boundary roles into one independent archive capacity unit. Therefore, for boundary area `A_{D0}` measured in D0/Planck area quanta,

```math
S_{D0}^{BH}=A_{D0}/4.
```

This is the D0 finite-channel version of the Bekenstein-Hawking area law. It does not import string microstates or continuum thermodynamics as primitive objects. Evaporation rates and greybody factors remain downstream external comparison protocols.

The factor `4` follows from the ABCD readout alphabet, and two forcing arguments make it *exactly* four and not a tuned normalization. Both are given below; the ABCD role alphabet itself is owned by BOOK_01 §01.7 and is cited, not re-derived.

**[THE 07.21.RT] Discrete Ryu-Takayanagi: horizon area = edge-cut rank, four edge units per resolvable bit [^b07-32].** On the minimal holographic carrier `K(9,11,13)` (rank 3 / nullity 30, BOOK_01) the horizon "area" is not a length — it is the *edge-cut rank* of the boundary seam: the min-cut separating the retained region `R` from its traced-out complement `R^c`. The discrete Ryu-Takayanagi reading is that boundary entanglement is carried by this cut. The forcing for the denominator: resolving one bit of boundary entanglement requires fixing the full symplectic phase, and symplectic phase resolution on `Omega8` consumes the entire four-dimensional terminal quotient `(A,B,C,D)`. So a single resolvable boundary bit costs exactly four geometric edge units, and

```math
C_{\partial}=A_{D0}/4
```

falls out as a finite topological count, not a thermodynamic fit. Cert status: the min-cut = 4 edge-cut structure is checked as a finite deterministic max-flow/min-cut object (cert: `vp_finite_mincut_holographic_entropy.py`, owned by §07.40 — cited, not duplicated here); the *identification* of that four-edge cut with the full `(A,B,C,D)` symplectic phase quotient is [^b07-30].

**[THE 07.21.4C] Four-Color boundary limit: exactly four identifiers so no adjacent boundary cell aliases [^b07-33].** A second, independent forcing fixes the same `4`. To distinguish itself without an external catalog (M1), the boundary automaton must assign each cell a phase identifier such that no two adjacent cells share a state — otherwise adjacent quantum domains alias and the boundary cannot tell them apart, ⊥M1. The boundary resolves its information on a planar-equivalent surface, so by the Four-Color Theorem any contiguous planar map needs *exactly four* distinct identifiers to guarantee no adjacent regions collide. The four terminal detector roles `ABCD` are precisely that minimal four-coloring. Hence the maximal resolvable capacity is one logical bit per four geometric cells, and the `A/4` law is the macroscopic shadow of the Four-Color Theorem applied to the holographic boundary graph. This is a forcing for *why exactly four* that is independent of the symplectic-quotient count above; the two agreeing on `4` is the cross-check. [^b07-31] — no Four-Color-boundary cert exists in `05_CERTS/`; do NOT cite a `vp_*` token for this claim.

The downstream `S_{D0}^{BH}=A_{D0}/4` witness (boundary cells × ABCD denominator, with negative controls A/2, A/8, volume entropy, singularity-as-deletion all rejected) is owned by §07.50 and cert-backed there (`vp_black_hole_capacity_a4_witness.py`); this section owns only the two forcing roots for the denominator `4` and defers the saturation witness to §07.50.
## 07.22 Gravity-depth hostile uniqueness: the exponent 99

The line-depth exponent is the active line-covariance channel count, not a fitted logarithm for Newton's constant.  The active propagation space before terminal readout is

```math
\mathcal{H}_{line}=\mathcal{H}_9\otimes\mathcal{H}_{11},
\qquad
\dim \mathcal{H}_{line}=9\cdot11=99.
```

Therefore

```math
D_L\propto \varphi^{99}.
```

The terminal shell `V13` is excluded from the exponent because it is the boundary/readout shell, not part of active line-covariant propagation.  Negative controls are structural: `98` removes one covariance channel; `100` adds an ambient line state; `117=9×13` incorrectly promotes the terminal shell to propagation duty.  Thus the exponent `99` is locked by active line covariance, not by a posteriori fitting of `G_N`.

## 07.23 Phase-unfolding master chain

**Canonical mechanism: §01.19** (phase-unfolding master chain — the map `U_τ(n)=(n, n mod τ)` turns an ordered finite registration into a branch foliation; residues mod `q` are the coherent branches). Owned there, not re-derived. This section carries the gravity/finite-geometry-sector content: the **M1-forcing** of the two return windows (the part not in §01.19).

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

**Why `20` is M1-forced (totient formulation).** The branch count `\varphi_E(44)=20` is not a tuned integer: it is the Euler totient `|(\mathbb{Z}/44)^\times| = 44(1-\tfrac12)(1-\tfrac1{11}) = 20`, which is also `|\mathrm{Aut}(\mathbb{Z}/44)|`. Any other count `k\neq20` would change the automorphism class of the window, producing a new admissibility class that can only be selected by an *external catalogue* — forbidden by M1. So `20` is forced, not chosen (claim `D0-WINDOW44-TOTIENT-M1-001`, cert `vp_window44_totient_m1.py`; neighbours `\varphi_E(43)=42`, `\varphi_E(45)=24` differ, confirming the window is sharp). This sharpens `D0-WINDOW44-GROUP-SPECTRUM-001`.

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

**The electroweak window `(q_EW, m_EW) = (710, 113)` is forced, not fitted.** Both numbers are closed expressions in the named scene invariants with zero free parameters — `710 = 2·D_Σ·(2|V|+D_Σ) = 2·5·71` (with `71 = 2·33+5`) and `113 = (|ABCD|+1)·d₁₃ + |V₁₃| = 5·20+13`. The window is the *ratio* `q/m ≈ τ = 2π` (the phase-circle period), and `710/113` is the **first** continued-fraction convergent of `2π` reaching ratio precision `|q/m − 2π| < 10⁻⁶` (the previous convergent `333/53` is `1.7·10⁻⁴`). By the best-approximation theorem no denominator below `113` can do better, and `113` is the minimal denominator the invariant grammar can write — so the window is the minimal coherent near-return the scene admits. This is forcing-minimality in a structural grammar, not a look-elsewhere count over arbitrary integers (the audit rule, BOOK_05 §05.8.R). Honest scope: the near-return is the ratio measure (`~5.3·10⁻⁷`); the absolute `|q − m·2π| ≈ 6·10⁻⁵` is denominator-scaled and is not the criterion.

## 07.24 Phase-unfolding capacity source for shell depth

The phase-unfolding theorem uses the capacity closure of `ABCD`, `Ω8`, and `V9`. The first stable terminal return modulus is

\[
q_T=|ABCD|\cdot |V_{11}|=4\cdot 11=44,
\]

and its admissible branch count is

\[
\varphi_{Euler}(44)=20.
\]

This identifies the terminal shell degree `d13` with the admissible branch count of the first terminal phase return. The next return window gives

\[
\varphi_{Euler}(710)=280=|\Omega_8|\cdot 35,
\]

so the electroweak radial depth is the per-oriented-terminal branch depth of the second unfolding window.

## 07.25 Hurwitz-rigid phase generator and non-resonant spatial unfolding

**Canonical derivation: §01.21** (Hurwitz-rigid phase generator — `α_D0 = p² = φ⁻²` is the maximally non-resonant rotation; `φ⁻²` irrational rotation ⇒ non-resonant archive smoothing, finite return modulus `q` ⇒ residue branch geometry). Owned there, not re-derived. The gravity/finite-geometry-sector consequence recorded here:

The active owner promotes this from prose to a finite information-quasicrystal
statement:

```text
D0.Geometry.HurwitzRigidPhaseGenerator
D0.Geometry.PhaseReturnBranchCount
D0.Geometry.PhaseUnfoldingQuasicrystal
```

The non-periodicity theorem says the `phi^-2` phase does not admit a
rational translational period.  By the Phase-Unfolding Theorem, visible arms
appear only when the finite quotient chooses q_T=44 or q_EW=710. Thus D0 geometry
is neither smooth primitive continuum nor periodic lattice: it is finite,
ordered, aperiodic and readout-generated.


## 07.26 Lorentz and smoothness transition theorem

The Lorentz carrier is induced by the terminal role capacity before any smooth geometry is introduced. The single runtime/normalization role and three comparison roles force signature `(1,3)`. A Lorentz-facing gravity claim must therefore pass through the Clifford carrier

```text
{γ^μ,γ^ν}=2η^{μν}I,
η=diag(+1,-1,-1,-1).
```

Smooth geometry is then a separate bridge. At finite stage `N`, line probes define a covariance matrix `G_N`; together with the finite incidence operator this determines a Laplacian-like operator `Δ_N` and heat trace

```text
Θ_N(u)=Tr exp(-uΔ_N).
```

The continuum metric is admissible only if the family is projectively compatible, uniformly non-degenerate on the retained sector, and has a stable four-dimensional Weyl heat-trace asymptotic. Thus D0 does not assume a smooth manifold; it specifies when a smooth manifold is a valid macro-shadow.

## 07.27 Canonical archive Laplacian and curvature obstruction

The finite archive is equipped with a canonical weighted graph Laplacian $L$ derived from the cyclic phase-distance metric. We prove in Lean that $L$ is symmetric, nonnegative, and has a row-sum zero constant mode. Projective compatibility of the Laplacian under refinement fails due to topological cycle splitting (no-go on projective compatibility), and a curvature obstruction skeleton prevents projection flatness on refined fibers (no-go on curvature flatness). This formalizes the non-triviality of the finite geometry.

## 07.28 Renormalized archive Laplacian / RG geometry

The local phase Laplacian is not required to commute strictly with archive pullback. The finite gravity operator is read through the effective coarse operator

```text
L_eff(n) = B^T L_{n+1} B,
```

where `B` is the matrix of the canonical phase coarse-graining projection. The Lean owner defines coarse graining, pullback energy, the operator residual, renormalized compatibility, and the theorem that zero RG residual is equivalent to exact flat compatibility. It also proves that strict pullback compatibility fails for the nearest-neighbor phase Laplacian.

The finite certificate confirms the flow: the projected effective operator has scale `c_n = 1` and zero residual for the canonical phase projection, while the strict pullback commutator is a stable rank-2 seam defect. Thus the curvature statement is RG-geometric: flatness means vanishing residual after the declared coarse-graining, not naive equality of local operators at different resolutions.

## 07.29 Seam curvature and archive action

The internal curvature object is the seam commutator

```text
C_n = L_{n+1} B_n - B_n L_n.
```

Lean defines the seam transport operator, the commutator, the curvature density

```text
rho_n = sum_{i,j} C_n(i,j)^2,
```

and the finite archive action

```text
S_N = sum_{n < N} rho_n.
```

The proved Lean facts are: `rho_n >= 0`, `rho_n = 0` iff operator transport is flat, `S_N >= 0`, and `S_N = 0` iff every included refinement step is flat. The Python seam certificate supplies the exact finite rank/support invariant: rank `2`, four seam entries, HS density `4`. This closes the internal action skeleton as accumulated seam curvature.

## 07.30 Seam-action variation and archive field equation

The seam action carries a finite variational layer.  Varying the coarse
archive Laplacian inside

```text
C_n = L_{n+1} B_n - B_n L_n
```

gives

```text
dC_n = -B_n dL_n,
d rho_n = 2 <C_n, dC_n> = <-2 B_n^T C_n, dL_n>.
```

Lean records this as an algebraic trace-square identity rather than relying on
an analytic derivative API.  The vacuum equation is stationarity of the seam
action against all admissible finite Laplacian variations; the sourced equation
is equality of the curvature-gradient pairing with the traced-out complement stress-source
pairing.

The row-sum identity for the canonical Laplacian and the lift gives the
discrete conservation statement

```text
archiveDivergence(archiveCurvatureGradient_n) = 0.
```

Consequently any source satisfying the traced-out complement field equation is conserved.
The finite certificate checks the finite
quadratic expansion, the gradient/source pairing, the conserved stress
representative, and negative controls for invalid variations, nonconserved
sources, and wrong projections.

### Why this variation *is* a field equation: the forced CORE law it shadows

The variational layer above is not a free Lagrangian we chose; it is the
finite, covariant shadow of the one CORE field law that M1 permits. That law is
`K(x) ~ ϱ(x)` — curvature-defect proportional to closure-density — and its
forced shape is owned upstream by §07.4: linearity from additivity of distant
masses, the vacuum boundary `f(0)=0 ⟹ b=0` because the flat reference `U^flat`
is the cycle-free minimum, and the coefficient `a_unit` fixed only as a unit
convention because M1 forbids introducing a *new* dimensionless physical
constant [^b07-34]. This section does not re-derive
that uniqueness; it carries its consequence: the seam-action vacuum equation is
exactly the discrete `K=0 ⟺ ϱ=0` statement (`b=0`, no closures ⇒ flat), and the
sourced equation is the discrete `K ~ ϱ` pairing written so that energy flux is
respected. The smooth, tensorial completion — the unique local-energy-conserving
tensor is `G_{μν}`, giving `G_{μν}+Λ g_{μν}=κ_GR T_{μν}` with `κ_GR=8πG/c⁴` a
pure BRIDGE unit factor — is the macro-shadow of this same finite equation
[^b07-35]. Status: CORE-FORCING for the discrete
law; the smooth-limit covariance is owned by the Einstein-interface sections
(§07.40, §07.13), which this section cites rather than re-deriving.

The scalar weak-field reduction of this field equation — the graph Poisson
problem `Lφ=ρ` with neutral-source solvability `Σ_i ρ_i = 0` and uniqueness
modulo the constant gauge mode — is owned by §07.32; this section supplies the full
curvature-gradient/stress-source pairing of which that Poisson skeleton is the
linearized scalar trace.

### The source `ϱ` is a frequency-density, and SR fixes the frequency

The traced-out complement stress-source in the sourced equation is not an
abstract density; it is the closure-frequency density

```math
\varrho_k(x) := \frac{\sum_{P\in\mathrm{Cycles}(x)} \tau(P)^{-1}}{\mathrm{Vol}(U_k)}
```

[^b07-36]. What §07.4 leaves to the dynamical layer — and what
this field equation needs in order to be Lorentz-honest — is *why* the weight in
`ϱ` is precisely the inverse period `τ(P)⁻¹` and how it transforms. That is the
forced special-relativity layer.

A massive state is a stable topological defect, so it carries an internal memory
cycle `P`. Each lightlike tick `Δ` (unit budget in the `C=1` normalization,
GOLDEN COR II.4.APPX5.21.C) splits into two orthogonal components: an external
transport `Δx` (change of address in the active scene) and an internal run `Δs`
(advance along `P`). External transport moves only the address; the internal run
moves only the cycle phase; cross terms vanish by definition of the observables
[^b07-37]. The unit budget is therefore partitioned as

```math
\|\Delta x\|^2 + \|\Delta s\|^2 = 1,
```

with `v := ‖Δx‖ ∈ [0,1]` the external velocity in units of `C`, and proper time
counted by internal runs `Δτ := ‖Δs‖`, `τ := Σ Δτ` [^b07-38]. Solving the budget gives `‖Δs‖ = √(1−v²)`, hence

```math
\frac{d\tau}{dt}=\sqrt{1-v^2},\qquad
\gamma:=\frac{dt}{d\tau}=\frac{1}{\sqrt{1-v^2}}.
```

Time dilation is thus *not* a postulated symmetry but the direct accounting of a
single causal tick's unit budget split between transport and internal run
[^b07-39]. The emergent Lorentz factor is a budget
identity, not an imposed group.

The rest frequency is the closure rate of the internal cycle,
`ω_0 := τ(P)^{-1}` — exactly the weight appearing in `ϱ`. Defining (CORE, no
external constants) `E := γ ω_0` and `p := γ ω_0 v` yields the discrete
dispersion invariant

```math
E^2 - p^2 = \omega_0^2,
```

the `C=1` analogue of relativistic energy–momentum, with the SI conversion
deferred to BRIDGE [^b07-40]. This closes the loop on the
field equation: the source `ϱ` is a Lorentz-covariant frequency density whose
rest weight `ω_0 = τ(P)⁻¹` is the same period the causal section of §07.4 reads
off, and `E²−p²=ω_0²` is the dispersion the traced-out complement stress-source
must respect frame-to-frame. Status: CORE-FORCING [^b07-41]. The pro-format caveat applies: each
`(v_k,τ_k,γ_k)` is defined at finite level `k` and the family is
projectively compatible, so no external limit term `c_n` is introduced
[^b07-42].
## 07.31 Admissible variation space and variational stress dual

The variational-dual algebra for the finite archive field equation is closed.  The raw curvature gradient

```text
G_n = -2 B_n^T C_n
```

is already row-conserved by the traced-out complement Bianchi identity, but it is not required to be symmetric.  The admissible Laplacian variation object carries the obligations used by the field equation:

```text
δL = δL^T,
δL · 1 = 0,
phase-local support obligation.
```

The formal result is not a prose identification of `G_n` with stress.  It is the theorem that the variation pairing only sees the symmetric component of any matrix:

```text
pairing(A, δL) = pairing(symPart(A), δL),
```

for every admissible variation `δL`.  Equivalently, skew-symmetric parts are in the annihilator of the admissible variation space.  Lean ownership:

```text
D0.pairing_depends_only_on_symmetric_part
D0.skew_part_annihilates_admissible_variations
D0.raw_gradient_equivalent_to_canonical_stress
D0.canonical_stress_symmetric
```

The canonical representative is therefore the variational representative

```text
canonicalStressRepresentative(G_n) = symPart(G_n),
VariationEquivalent(G_n, canonicalStressRepresentative(G_n)).
```

This does not by itself close the conservation of the symmetric representative.  The guardrail is

```text
NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION
```

which states that taking the symmetric part of an arbitrary matrix is not a conservation-preserving operation.  The constrained admissible projection is successfully constructed at its Lean owner using the projection:

```math
T = S - \frac{1}{N}\left(v\mathbf 1^T + \mathbf 1 v^T\right),
\qquad
S=\frac{G+G^T}{2},
\qquad
v=S\mathbf 1.
```

For raw gradients with `G · 1 = 0`, this projection is symmetric, row-conserved, and variation-equivalent to `G_n` for all admissible variations `δL` with `δL · 1 = 0`.

## 07.32 Discrete Poisson / weak-field equation

The finite weak-field skeleton is the graph Poisson problem on the canonical cycle Laplacian:

```math
L\phi = \rho.
```

Lean has closed the structural part of this finite equation:

```text
poisson_requires_neutral_source:
  ArchivePoissonEquation φ ρ → NeutralSource ρ

poisson_solution_unique_mod_constant:
  ArchivePoissonEquation φ₁ ρ →
  ArchivePoissonEquation φ₁ ρ →
  φ₁ - φ₂ is constant
```

The reason is the constant zero mode of the canonical Laplacian.  Thus solvability forces

```math
\sum_i \rho_i = 0,
```

and uniqueness is only modulo the constant gauge mode.

The finite certificate checks the finite-cycle Laplacian construction, a point-pair neutral source, zero-mean gauge fixing, residual control, positive energy, Green symmetry, uniqueness modulo constants and negative controls.

The non-vacuous scalar reduction is successfully closed at its Lean owner via the theorem:

```text
scalar_stationarity_implies_archive_poisson:
  ScalarSectorStationary n φ ρ → ArchivePoissonEquation φ ρ
```

The predicate `ScalarSectorStationary` is a non-vacuous point-test stationarity condition, completing the weak-field reduction proof.

## 07.33 Final finite-geometry theorem chain

The typed-closure finite-geometry chain is closed as a theorem/cert/no-go
sequence:

```text
finite variation
-> canonical stress representative
-> neutral-source Poisson equation
-> scalar/vector/edge stationarity equations
-> heat-trace A2 decomposition
-> finite spectral-action ladder
-> higher-curvature floor-bounded absolute control
-> continuum GR bridge status.
```

Machine ownership:

| statement | status | owner |
|---|---|---|
| first variation of trace-square action | `CORE-CLOSED` | `D0.first_variation_trace_square` |
| admissible variations see only the symmetric representative | `CORE-CLOSED` | `D0.pairing_depends_only_on_symmetric_part` |
| canonical stress representative is symmetric and variation-equivalent | `CORE-CLOSED` | `D0.raw_gradient_equivalent_to_canonical_stress`; `D0.canonical_stress_symmetric` |
| Poisson solvability requires neutral source and is unique modulo constants | `CORE-CLOSED` | `D0.poisson_requires_neutral_source`; `D0.poisson_solution_unique_mod_constant` |
| scalar stationarity implies archive Poisson | `CORE-CLOSED` | `D0.scalar_stationarity_implies_archive_poisson` |
| vector and edge equations have closed operator origins | `CORE-CLOSED` | `D0.Bridge.vector_operator_origin_closed`; `D0.Bridge.edge_stiffness_origin_closed` |
| finite TT representative is symmetric, trace-free and transverse | `CORE-CLOSED` | `D0.Geometry.finite_spin2_tt_carrier_closed` |
| weak-field gauge/trace quotient yields the TT representative | `CORE-CLOSED` | `D0.Geometry.finite_weak_field_quotient_yields_tt_representative` |
| conserved stress removes longitudinal and trace directions before spin-2 coupling | `CORE-CLOSED` | `D0.Geometry.finite_conserved_stress_spin2_coupling_closed` |
| heat trace square decomposes into diagonal term plus EH proxy | `CORE-CLOSED` | `D0.Geometry.HeatTraceA2Decomposition.heat_trace_sq_exact_decomposition` |
| higher curvature powers have floor-bounded absolute control | `CORE-CLOSED` | `D0.Geometry.HigherCurvatureSuppression.higher_curvature_suppression_by_floor` |
| continuum Einstein-Hilbert reading | `BRIDGE-CALIBRATION` | finite spectral ladder plus declared smooth/continuum bridge |

Thus the active scalar equation uses a point-test stationarity predicate with
direct Lean ownership, and the continuum Einstein language remains a bridge
calibration rather than a core smooth-manifold theorem.  The `a0/a2` trace
ratio is a dimensionless `CORE-CLOSED` finite spectral shape.  Any `c0/c2` SI
coefficient ratio belongs to `ExternalSICalibration`; `H0`, `G_N` and `Lambda`
are not outputs of `DimensionlessCoreTraces`.

### 07.33.1 Forced terminus 1: D0-sphericity (the finite Poincaré no-go)

The chain above closes the *local* finite geometry. Its *global* terminus is a
finite-resource sphericity theorem: the pro-limit of a constructively regular
3-geometry is forced to S^3, with no smooth-manifold input.

Objects (CORE-only; no infinite limit admitted as CORE — refinement tower plus
a κ-convergence criterion only):

- A **D0-3-manifold** `M` is a κ-stable inverse system of finite
  3-triangulations `M = {(T_k, π_{k→k-1})}`, each `T_k` a finite 3-complex,
  projections coherent (pro-model of continuum). Manifold equivalence is read
  as `≡_κ` (κ-equivalence, DEF 21.3.2).
- `M` is **D0-simply-connected** iff there is `k_0` such that for all `k ≥ k_0`
  every loop `γ` in the 1-skeleton of `T_k` carries a finite-resource
  contraction-verification packet `Cert(γ)`, and the contraction is
  `π`-compatible (κ-stable).

**THE 07.33.1 (D0-sphericity of the projective limit under constructive
regularity).** Let `M = (T_k, π_{k→k-1})` be a κ-stable inverse system of
finite simply-connected 3-triangulations satisfying the M1 physical-realizability
criterion (no non-constructive "thin" defect below the minimal scale). Then
`lim← M` is pro-homotopy equivalent to S^3; under additional PL-compatibility of
the bonding maps the limit object is homeomorphic to the sphere.
Status: **PROOF-TARGET (cert obligation open)** — scoped to the class of
constructively regularized 3-manifolds, not the full ZFC Poincaré statement.

Forcing (minimality + ⟂, strictly by M1) — [^b07-43]:

1. Fix level `k` and cell count `m`. The class `C_{k,m}` of connected closed
   3-complexes with `m` cells is **finite**.
2. By BOOK II there is a canonical "flat reference" `U^flat_{k,m}` as the
   minimizer of `|D_min(·)|`; its κ-stability is a hard admissibility condition.
3. For a D0-simply-connected `M` every loop has a verifiable contraction code,
   so there is **no κ-stable defect memory** — no mandatory loop that cannot be
   removed without external information.
4. Suppose `M ≢_κ S^3`. Then a κ-stable invariant-defect `Def(M)` distinguishes
   it from the sphere on infinitely many levels.
5. Any such defect must be **either** an irremovable loop/cut (contradicting
   D0-simple-connectivity) **or** "thin", appearing only on refinement — and
   then its specification requires an external catalog ("*which* thin defect")
   forbidden by M1.
6. Both horns contradict. Hence no defect; `M ≡_κ S^3`. □

Bridge [^b07-44]: the classical Poincaré conjecture is the
packaging of an inverse-system limit. In D0 "smoothness" is replaced by
κ-stability, and the statement becomes a strict distinguishability test rather
than a smooth-topology claim. This terminus is the global companion of the
local finite-geometry closures above: same M1 "no external catalog" forcing,
applied to the whole inverse system instead of a single point-test.

### 07.33.2 Forced terminus 2: minimal-plaquette mass-gap (finite spectral floor)

The finite spectral-action ladder and the higher-curvature floor of the table
above have a gauge-sector companion: on the same finite scenes the gauge
Hamiltonian's excitation spectrum is forced to have a strictly positive floor.

The **fact** of a finite gauge mass-gap is owned by the feedback sector, derived from the
F_N feedback-return / commutator obstruction (BOOK_05 `GAUGE-BOUNDARY-LAW`:
color confinement as the commutator obstruction preventing terminal stable poles
for non-singlet states, a finite lower-bound target on `F_N`; cf. BOOK_04 CVFT
gauge-boundary). That ownership is cited and **not** re-derived here. The §26
*minimal-plaquette* forcing of the same floor extends
the finite-spectral closure sequence directly and is given below.

Objects (CORE reformulation of Yang–Mills, by distinguishability):

- **Gauge** = local indistinguishability of an outgoing-edge permutation: if a
  permutation does not change the distinguishing tests, the node carries a local
  `S_N` symmetry.
- **Gauge field** = holonomy labelling `q(γ)` on paths, with `q(ℓ) ≠ 1` on
  closed contours `ℓ` as observable excitation memory.
- **Energy/mass** = cycle cost `ΔS := S(γ) − S(γ_vac)`; step cost is fixed by the
  corpus step-weights `W_ext = φ^-1`, `W_int = φ^-2`. Mass is the spectral/
  frequency reading of the minimal closure statistics (κ-density of closures).

**THE 07.33.2 (excitation-energy lower bound at fixed minimal cycle).** In D0 the
minimal elementary cycle (plaquette) has nonzero constructive cost
`ΔS_min > 0`, fixed by the corpus weights `W_ext = φ^-1`, `W_int = φ^-2`. Since
the UV cutoff forbids the limit `ΔS_min → 0` (that would be an exogenous
parametrization / hypercomputation), the excitation spectrum of the gauge
Hamiltonian is bounded below at every level:
```text
E_1 − E_0  ≥  c · ΔS_min  > 0.
```
Hence the "gapless" continuum limit is a mathematical abstraction not realizable
in the constructive D0 model.
Status: **PROOF-TARGET (cert obligation open)** — statement about the
regularized lattice theory at fixed UV cutoff, not the ZFC-form Clay statement;
consistent with the existing F_N `GAUGE-BOUNDARY-LAW` lower-bound fact.

Forcing (M1 + minimal loop) — [^b07-45]:

1. An excitation with no loop is indistinguishable from vacuum: with no stable
   closure `q(ℓ) ≠ 1` anywhere in the history there is no object memory, hence no
   physically distinguishable excitation (CORE distinguishability criterion).
2. At any level `k` the graph is finite, so the set of simple cycles is finite ⇒
   there is a minimal cycle length `L_min(k)` among those giving `q(ℓ) ≠ 1`.
3. κ-stability forbids "runaway" of the minimal cycle to ever-finer levels
   without a fixable class: if `L_min(k) → ∞` or `ΔS → 0` only by refinement,
   then specifying "*which* cycle is the excitation" needs exogenous
   branch/precision indices ⇒ M1 violation.
4. Each step cost is corpus-fixed (`W_ext = φ^-1`, `W_int = φ^-2`), so a minimal
   nonzero cycle cost `ΔS_min` exists and is positive.
5. Hence a minimal nonzero excitation frequency/mass exists:
   `m_gap ∼ ΔS_min > 0`. □

Bridge [^b07-46]: the classical "mass gap exists in 4D
Yang–Mills" is the packaging of a transfer-operator/Hamiltonian spectral gap. In
D0 the gap is unavoidable because "excitation" = "stable memory cycle" and a
cycle has a minimal cost with no external tuning. This is the same M1 "no
external catalog" forcing that closes 07.33.1, now read on the gauge spectrum:
the minimal-plaquette floor `ΔS_min > 0` is the gauge-sector analogue of the
higher-curvature floor closed at its Lean owner,
and it underwrites — rather than competes with — the F_N
`GAUGE-BOUNDARY-LAW` lower bound.

Both termini share the closure shape of the local table: a finite-resource
quantity (defect memory; cycle cost) cannot vanish or run away without an
external catalog M1 forbids, so the limit object is forced (S^3) and the spectrum
is forced gapped. The continuum GR / Clay readings remain bridge calibrations,
not core smooth-manifold theorems.
## 07.34 Cosmology boundary audit

Book 07 does not compute Hubble, matter-density, survey-redshift-center or BAO-amplitude values as internal gravity constants. It supplies the finite geometry side of the bridge:

```text
line covariance
-> archive Laplacian / heat trace
-> finite spectral ladder
-> density-floor higher-curvature absolute bound
-> bridge/comparison protocol handoff to Book 08.
```

The status boundary is:

| statement | status |
|---|---|
| finite heat-trace A0/A2 ladder | `CORE-CLOSED` |
| higher traces have floor-bounded absolute control | `CORE-CLOSED` |
| smooth Einstein-Hilbert language | `BRIDGE-CALIBRATION` |
| survey likelihood and cosmological parameter comparison | `EMPIRICAL-PASSPORT` / `EXTERNAL-DATA-REQUIRED` |

Any text that treats a survey value as a Book 07 internal theorem violates the final bridge index.


## 07.35 Finite spin-2 derivation theorem

Spin-2 is not a field tag. Poisson response plus a declared TT mode is not on its
own a derivation; the finite statement is a quotient chain.  A weak-field metric
response enters the GR bridge only after the following finite reduction has been
supplied:

```text
finite symmetric weak-field mode h
-> finite longitudinal/gauge representative
-> finite scalar trace representative
-> quotient reconstruction certificate
-> conserved-stress annihilation of longitudinal direction
-> conserved-stress annihilation of trace direction
-> transverse-traceless representative h_TT.
```

The Lean owner supplies an explicit finite reduction object in place of the weak
reading "there exists a TT-shaped mode".
The derived owners are:

```text
D0.Geometry.finite_weak_field_quotient_yields_tt_representative
D0.Geometry.finite_gauge_trace_quotient_closed
D0.Geometry.finite_conserved_stress_spin2_coupling_closed
D0.Geometry.finite_trace_mode_removed_from_spin2_carrier
```

Thus the active gravity chain is:

```text
archive variation
-> symmetric canonical stress representative
-> neutral-source Poisson response
-> finite weak-field gauge/trace quotient
-> conserved-stress elimination of non-TT directions
-> finite TT spin-2 representative
-> spectral A2 / Einstein--Hilbert bridge
-> SI calibration only after the internal dimensionless shape is fixed.
```

This is a theorem, not an analogy: Poisson response plus a declared TT mode would
not on its own be a derivation of the spin-2 carrier, so the quotient chain
forces the step to be a finite object with reconstruction and stress-annihilation
fields.  Smooth GR remains a bridge reading, but the finite carrier entering that
bridge is not a label or a primitive graviton import.

### 07.35.1 Rejected readings

The following readings are not valid D0 claims:

```text
Poisson equation alone => GR.
A symmetric matrix alone => spin-2 carrier.
Trace/scalar response can be promoted as the graviton carrier.
Longitudinal/gauge response can couple to conserved stress as physical spin-2.
Einstein--Hilbert action is a core smooth-manifold theorem without the spectral bridge.
```

Book 07 therefore has a sharper boundary: the finite theorem closes the D0
carrier; the continuum Einstein language remains the declared smooth/spectral
bridge.

## 07.36 Tick-gauge compatibility of the gravity bridge

The gravity bridge has an explicit tick-gauge prerequisite.  The weak-field spin-2 derivation closes the TT carrier; the tick/Lorentz layer closes the causal cone on which that carrier propagates.  The active finite owners are

```text
D0.Bridge.FiniteCausalTickSection
D0.Bridge.FiniteLorentzTickGaugeClosure
```

with closure theorems

```text
finite_causal_tick_section_cone_speed_eq_one
finite_lorentz_tick_gauge_cone_speed_closed
finite_lorentz_tick_gauge_signature_closed
finite_lorentz_tick_gauge_no_euclidean_export
finite_lorentz_tick_gauge_no_split_export
```

Therefore the GR-facing bridge has two separate finite gates:

```text
finite weak-field quotient -> TT spin-2 representative
finite tick/Lorentz closure -> one cone invariant and signature (1,3)
```

Only after both gates are closed may the smooth Einstein--Hilbert/Lorentz bridge be invoked.  A successful SI calibration of `c`, `G_N`, or macroscopic clock synchronization does not define the finite core and cannot alter the D0 cone invariant.

## 07.37 Finite spin-2 dynamics closure

The spin-2 layer closes the finite TT representative and a finite dynamics certificate over it.

The owner is

```text
D0.Geometry.FiniteSpin2Dynamics
```

with theorems

```text
finite_spin2_dynamics_propagates_tt
finite_spin2_dynamics_ghost_free
finite_spin2_dynamics_two_polarizations
finite_spin2_dynamics_closed
```

The active gravity chain is

```text
finite weak-field mode
-> gauge/trace quotient
-> TT representative
-> finite TT wave operator
-> propagation equation
-> conserved-stress coupling uniqueness
-> two-polarization readout
-> scalar/vector ghost exclusion
-> spectral A2 / EH bridge.
```

This does not claim that the smooth Einstein equations have been proved inside finite Lean.  It closes the finite carrier-plus-dynamics object required before the smooth GR bridge may be invoked.

## 07.38 Concrete finite TT wave operator

The TT projector is represented concretely, not by an abstract variable.  The concrete owner is

```text
D0.Geometry.FiniteSpin2WaveOperator
```

on the four-role terminal carrier with

```text
eta = diag(1,-1,-1,-1)
k = (1,1,0,0)
u = (1,0,0,0)
```

and the two explicit transverse polarizations `ePlus4` and `eCross4`.  The projector is

```text
PiTT4(h) =
  <ePlus,h>/<ePlus,ePlus> ePlus
+ <eCross,h>/<eCross,eCross> eCross
```

with `<A,B> = Tr(A eta B eta)`.  Lean proves that the projector is idempotent and TT, kills the trace and gauge directions, and that the wave operator preserves TT, has nonnegative energy, and couples only to the TT part of the stress.  The finite certificate checks the projector on all ten basis elements of `Sym(4)` and verifies rank 2.

The D0 memory torus is a separate internal shell geometry used by the
matter/flavour sectors.  It does not replace the terminal four-role TT
projector, does not derive Einstein equations, and does not assign Newton's
constant.  Spin-2 closure remains the finite TT projector, `WTT4` and conserved
stress coupling.

## 07.39 Spin-2 two-polarization arithmetic closure

The finite dynamics certificate is accompanied by an arithmetic readout for
the 4D Lorentz-facing spin-2 degree count.  The owner is

```text
D0.Geometry.FiniteSpin2DOF
```

with theorem owners

```text
massless_spin2_physical_dof_four_eq_two
spin2_component_reduction_four_dimensional
concrete_spin2_dynamics_two_polarizations_closed
```

The closure is deliberately finite:

```text
massless spin-2 physical dof in d dimensions = d(d-3)/2
for d = 4, this is 2
```

and, equivalently for the finite component bookkeeping,

```text
10 symmetric rank-2 components - 8 gauge/constraint removals = 2 TT polarizations.
```

This separates "TT carrier exists" from "the
Lorentz-facing spin-2 readout has the correct two physical polarizations".  The
smooth Einstein equation remains a bridge after TT dynamics, tick-gauge closure,
and spectral A2/EH proxy are all frozen.

## 07.40 Entropic archive to macro Einstein interface

D0 gravity is the finite archive macro-interface.  The continuum Einstein
equation is not inserted as a primitive.  It is the macro class compatible with
finite information conservation, symmetric stress readout, second-order finite
readout, TT spin-2 coupling and higher-curvature suppression.

The final gravity chain is:

```text
07.1 Archive variation and finite stress
07.2 Graph Laplacian and heat trace
07.3 Boundary capacity as finite holographic area

Finite min-cut entropy (terminal-normalized cut capacity / 4) extends the boundary-capacity witness for holographic entanglement.
07.4 Entropic surface tension
07.5 Conservation of archive flux
07.6 Symmetric stress representative
07.7 Terminal 4-role Lorentz/tick carrier
07.8 Explicit TT projector Pi_TT
07.9 Finite wave operator W_TT
07.10 Gauge/trace ghost annihilation
07.11 TT stress coupling
07.12 Higher-curvature finite cut
07.13 Spectral A2 / Einstein-Hilbert bridge
07.14 Macro Einstein interface theorem
```

The finite Lean owner carries the graph Laplacian,
boundary cut capacity, archive flux conservation and nonnegative entropic
surface tension.  The macro Lean owner packages a
finite witness for the traced-out complement conservation theorem, the explicit
`PiTT4/WTT4` carrier, higher-curvature terms below the finite readout cut, and
the spectral A2-is-EH-proxy theorem.

The active/archive split is not an extra matter component: active contraction and archive expansion are eigen-branches of one toral automorphism, and the determinant invariant gives exact phase-volume balance before the macro gravity interface is read.

**The `A/4` coefficient: a Four-Color forcing attempt, with the honest gap named.** A proposed route reads the horizon capacity `C_∂ = A/4` off the Four-Color theorem (4 horizon colors = 4 roles). The forcing attempt has a real half and an open half (claim `D0-FOURCOLOR-HORIZON-CAPACITY-001`, cert `vp_fourcolor_horizon_capacity.py`): the **"4" is forced** — four mutually-adjacent horizon cells form `K_4` with `\chi(K_4)=4`, and the Four-Color theorem caps any sphere map at 4, so the address-coloring uses exactly 4 colors `=` the 4 `ABCD` roles. But the **"1/4" is not derived**: the chromatic number `4` and the Bekenstein coefficient `1/4` are different objects (4 colors carry `\log_2 4 = 2` bits, neither `1/4` nor the `A/4` coefficient). So `C_∂ = A/4` is **not** declared from chromatics; the coefficient `1/4` stays a named gap whose owner is the Bekenstein/Jacobson thermodynamic route (§07.51.3), not the colouring. The Four-Color step fixes the role count, nothing more.

## 07.41 Trace-Heat-Capacity Gravity

Trace-Heat-Capacity Gravity refines the finite gravity entry point:

```text
Toral automorphism
-> Lucas trace levels
-> heat moments of T^2
-> Lefschetz scene counts
-> boundary capacity
-> black-hole capacity saturation
-> finite gravity witness
-> Einstein macro-interface.
```

The local black-hole reading is local information-capacity saturation, not a
core singularity.  For a finite graph region `S`, the admissible finite rule is:

```text
I(S,s) = Tr_S(exp(-s Delta_G))
C(boundary S) = BoundaryCutWeight(S)/4
horizon condition: I(S,s)=C(boundary S)
saturation condition: I(S,s)>=C(boundary S)
```

When saturation holds, extra local information must be boundary-encoded.  The
factor `A/4` is read as ABCD boundary capacity: four terminal detector roles
count boundary distinguishability in quarter-cut units.  The macro Einstein
interface remains the downstream bridge after this finite heat/capacity witness.

Higher-curvature terms are not forbidden metaphysically. They are below finite
D0 readout threshold in the macro interface and therefore cannot act as leading
gravity law.

The compact statement is:

```text
D0 gravity is the finite archive macro-interface.
At the finite level: graph Laplacian controls information diffusion; boundary
cut capacity is holographic area; entropic surface tension is nonnegative;
archive flux is conserved; stress readout is symmetric; TT projector and W_TT
give the finite spin-2 carrier.
At the macro level: any compatible gravity interface must be symmetric,
divergence-free, second-order under finite readout, and compatible with TT
stress coupling.
Therefore the Einstein-Hilbert / Einstein tensor class is the macro-interface (finite A2 variation + Bianchi selects the class; this is closed finite-response status, not bridge calibration).
```

## 07.49 Critical-collapse discrete self-similar log-time lattice and spacetime-crystal horizon

PRL 2026 (arXiv:2601.14358) constructs closed analytic large-D discretely self-similar solutions of the Einstein–massless-Klein–Gordon critical-collapse system.

D0 reads this as a gravity-side closure of the finite horizon transition: black-hole birth passes through a discrete log-scale discrete self-similar log-time lattice.

The self-similar horizon (SSH) is the null boundary where the echo-lattice vector becomes lightlike. In D0 this is the capacity-null boundary of the terminal horizon readout.

D0 chain (dynamic birth, not static saturation):

```text
trace-heat gravity
> capacity density growth
> critical echo-lattice phase
> self-similar null horizon
> terminal boundary of traced-out complement
> black-hole saturation
```

Typed owners:
- `D0.Gravity.CriticalCollapseDSS`
- `D0.Gravity.EchoCapacityHorizon`

Theorem block:
- D0-GRAV-DSS-001 Critical Collapse Echo-Lattice Closure
- D0-GRAV-DSS-002 Self-similar horizon is capacity-null boundary
- D0-GRAV-DSS-003 Echo admissibility constraint (NLO/convexity/SSH filtering)
- D0-GRAV-DSS-004 Spacetime Crystal Bridge
- D0-GRAV-DSS-NOGO-001 Smooth Monotone Collapse Failure

The echo-lattice closure is backed by a finite certificate and an external passport manifest.

The external analytic certificate owns the GR construction (closed DSS family + NLO filtering). D0 owns the finite log-time readout / capacity / admissibility interpretation.

Black-hole formation is a critical finite-readout phase transition through a spacetime-crystal echo horizon, not a purely smooth density-threshold singularity (while higher-curvature corrections are finite-cut suppressed).

## 07.50 Finite horizon capacity and A/4 witness

Finite boundary shell ∂R reaches capacity saturation σ(R) = 1.
Cost of external active extension → ∞.
Terminal archive quotient Y : H_R > H_N makes active information inaccessible, **not deleted**.
ABCD terminal alphabet supplies the factor of 4:

N_∂ = A / a_0 ,   S_∂^{D0} = N_∂ / 4 .

This is derived from four terminal readout roles per saturated boundary cell (not imported Bekenstein-Hawking normalization).
Negative controls (A/2, A/8, volume entropy, singularity-as-deletion) are rejected.

Typed owners:
- D0.Gravity.FiniteHorizonCapacity
- D0.Gravity.BlackHoleA4EntropyWitness

The A/4 witness is backed by a finite certificate and an external passport.

Cross-book:
- Book 06: saturation as runtime halt / active-archive quotient.
- Book 05: D0-BH-CAP-NOGO-001 (singularity-as-information-deletion rejected).
- Book 08: PBH formation must combine DSS echo-lattice birth + this finite A/4 capacity witness.

## 07.42 Phason/phonon split and dark metric response

The finite quasicrystal operator layer separates active visible strain from
archive phason strain.  Gravity sees both phonon and phason strain energy; EM
sees only active visible window; archive phason strain is a dark metric source.

The Lean owner carries:

```text
archive_phason_strain_is_dark_to_em
archive_phason_strain_can_source_metric_response
archive_phason_strain_em_dark_metric_visible
```

The finite certificate checks PSD archive strain
energy, zero EM archive coupling, positive heat/metric increment, and a
nonzero finite phason gradient sourced by a cluster.

## 07.47 Noncommutative solenoid gravity

The finite TT operator W_TT is the two-polarization sector of the D0 solenoid spectral geometry. The smooth Einstein interface is the macro shadow of heat-trace covariance over this noncommutative solenoid approximant.

### Why the solenoid geometry is noncommutative: the address-order forcing [J,Y]

The noncommutativity is not decorative — it is forced at the level of how a finite observer assembles a scene at all. Two operators act on the solenoid address book [^b07-47]:

- **Y (fold / compactify)** — the shell-convolution operator that folds the outer scene into the effective 4D representation, `Y: 12D -> 4D (+6 bit)`; the `+6 bit` is the binary cascade `2^6 = 64` read as the degree-of-freedom difference between shell and observed projection, not new physics [^b07-48]. Y is what fixes the boundary structure.
- **J (localize)** — pins a defect to an address.

The forcing claim: these do not commute, `[J,Y] != 0`, and the order is a physical selection rather than a bookkeeping convention.

- **Fold-then-localize (Y first, then J):** the defect is pinned *inside an already-given boundary structure*. The observer recovers reproducible "objects" — the localization inherits a context to be reproducible against.
- **Localize-then-fold (J first, then Y):** the defect is pinned *out of context* of any boundary, and the subsequent fold smears that context-free localization into a noise result.

So one operator order produces records that survive re-distinguishing and the reverse order produces noise. Under M1 (no external catalog to stabilize a context-free localization), only the reproducible order is admissible. Status: FORCED [^b07-49]. This is the book's natural home for the argument: it is the noncommutative-geometry locus where non-commuting structure on the solenoid spectral geometry already lives, and it is distinct from the torus-shell / CKM noncommutativity carried elsewhere (BOOK_01 §1305; BOOK_04 §04.4.4 own those) — here the non-commutation is the compactify-vs-localize order itself.

**Arrow of time as a corollary, not a postulate.** D0 does not insert a time arrow phenomenologically. The only reproducible scene-assembly procedure is the fold-then-localize order; the reverse collapses to noise. The directionality of "assemble an observable scene" is therefore a consequence of M1 acting through `[J,Y] != 0`, not an extra ingredient. Status: FORCED-COROLLARY [^b07-50].

The macro Einstein interface inherits this: W_TT, the two-polarization spin-2 sector, is read off the *folded* boundary structure, so the spin-2 carrier already presupposes the reproducible Y-then-J order. The noncommutative solenoid is the carrier of that order, not a free choice of presentation.

The Lean owners establish that the hull admits a noncommutative solenoid model and that the finite spin-2 operator is the TT sector of the solenoid spectral geometry, compatible with `WTT4`; this is confirmed by the finite verification certificate.
## 07.48 LIGO BBH mass-defect passport

$$\eta = \frac{M_1 M_2}{(M_1 + M_2)^2}$$

$$\Xi_{D0} = \eta \left[ \frac{3}{8} + \varphi^{-1}(4\eta - 1) + \frac{\chi_{eff}}{8} + \frac{\chi_{eff}^2}{3} \right]$$

$$\frac{\Delta M}{M_{raw}} = 1 - \sqrt{1 - \Xi_{D0}}$$

- **Status**: `EMPIRICAL-PASSPORT`.
- **Role in the chain**: LIGO compares the frozen horizon-capacity formula. LIGO does not choose the coefficients.

Passport inputs:

```text
M1, M2, chi_eff
```

Frozen D0 object:

```text
eta -> Xi_D0 -> Delta M / M_raw
```

Forbidden operations:

```text
retune 3/8;
retune phi^{-1};
choose a spin polynomial after seeing the event;
import a GR fitting coefficient into the D0 core.
```

Passport output:

```text
mass-defect fraction compared to the external LIGO event reconstruction.
```

The current-catalog comparison uses the pinned GWOSC/GWTC JSON table. The frozen D0 mass-defect formula is evaluated on complete BBH rows and compared against the mean-loss baseline; the LIGO passport records the exact events, RMSE, and negative-control numbers.

Events with neutron-star/mass-gap components or negative catalog mass defect are kept in the anomalies manifest, not used to retune the BBH horizon-capacity formula.

The finite D0 horizon-capacity mass-defect operator is the primary domain statement. External numerical comparison remains a passport protocol.

## 07.CVFT.Horizon emission as conjugate archive leakage

At boundary-capacity saturation the emission channel is the conjugate feedback operator
\[
F_Q^{emit}(R)=Q_RU_R^\dagger P_RU_RQ_R.
\]
For a boundary mode \(\psi_{\ell,\omega}\), the greybody candidate is the finite expectation value
\[
\Gamma_\ell(\omega)=
\langle\psi_{\ell,\omega},F_Q^{emit}(R)\psi_{\ell,\omega}\rangle.
\]
Horizon emission is archive-to-retained boundary leakage under capacity saturation. Thermal continuum descriptions are downstream passports of this finite operator law.

## 07.43 Measurement-Horizon Equivalence

A finite measurement seam is the support of a nonzero retained-to-archive transition:

\[
\mathcal S_N=\operatorname{supp}(Q_NU_NP_N).
\]

If \(Q_NU_NP_N\ne0\), some phase information is inaccessible to the retained sector and has crossed a local archive boundary. A macroscopic black-hole horizon is the capacity-saturated aggregate of such seams:

\[
\sigma(R)\to1,
\qquad
\operatorname{Cost}_R(\partial)\to\infty.
\]

Information is transferred into the archive complement, not deleted.

## 07.44 Unified Horizon Seam

The global complement \(Q_N=I-P_N\) defines a single archive interface. Local horizons are punctures of that interface:

\[
\partial(P,Q)=\bigcup_i\partial_i(P,Q).
\]

Rank localization supplies support; terminal capacity counting supplies the \(A/4\) normalization.

## 07.45 Optical Jet Backreaction

The conjugate archive-to-active emission operator is

\[
F_Q^{emit}=QU^\dagger PUQ=(PUQ)^\dagger(PUQ).
\]

At capacity saturation, archive pressure can discharge through this positive operator. With axial projector \(\Pi_{axis}\), the finite jet observable is

\[
J_{axis}=\operatorname{Tr}(\Pi_{axis}F_Q^{emit}).
\]

D0 defines relativistic jets internally as optical backreaction of a saturated horizon seam, collimated along the finite causal axis. Archive saturation corresponds to \(\mu\to1\) in informational mechanics.

----

## D0_v16 Dusty-plasma channel-clearing bridge

**Publication note on bridge material.** This section is a laboratory analogue/passport seed. It does not identify the experiment with astrophysical gravity; it records a channel-clearing and active-medium bridge that can be tested independently.


Status: `LAB-BRIDGE / TABLETOP-PASSPORT-SEED`.

Electron-beam dusty-plasma experiments provide a macroscopic laboratory bridge for D0 horizon/channel-clearing grammar. In the bridge dictionary, the electron beam is a directed readout puncture, dust grains are archive-capacity sinks, dust-free zones are channel-clearing events, and dust fly-out is a saturated-ejection analogue.

The useful horizon lesson is the sign switch: the periphery of a beam-plasma cloud can attract ordered dust structures, while the core can repel or clear grains. In D0 language this is a seam analogue: peripheral capture and core clearing are distinct finite regimes of the same active/archive interaction.

This paragraph is not a claim that electron-beam dust fly-out is literally an astrophysical black-hole jet. It is a typed bridge: the laboratory system supplies an experimentally accessible force-balance analogue for channel clearing and archive ejection. The core D0 horizon operators remain finite-algebraic objects; external dusty-plasma behavior is used only as a tabletop passport seed.
## 07.51 Horizonless arrest and the causal compactness ceiling

The horizon-as-seam picture of §07.43–§07.50 is a *static* statement: a black-hole horizon is a capacity-saturated aggregate, `σ(R) → 1`, `Cost → ∞`. §07.49 gave the *birth* of such a horizon by discrete self-similar collapse. What was missing is the **complementary dynamics** — the case where collapse is *arrested* and the seam stays open, never reaching saturation. An external result supplies exactly this counterpart, and reading it through the finite triple yields a sharp, falsifiable compactness ceiling.

### 07.51.1 Arrested collapse forms a horizonless seam (bridge)

The external anchor is the horizonless gravastar of Jampolski–Rezzolla (Phys. Rev. D **113**, L121502, 2026): a de Sitter core halts Oppenheimer–Snyder collapse *before* a horizon forms, leaving a compact object with no event horizon [^b07-51]. In the D0 reading the configuration is three regions — an interior de Sitter core `f_in(r) = 1 − (r/L)²`, a thin matching shell, and an exterior Schwarzschild region `f_out(r) = 1 − 2M/r` — joined by an Israel junction. A positive-energy shell requires `f_in(R) > f_out(R)`, and the object is horizonless on *both* sides precisely when

```math
2M < R < L,
```

so the exterior has no Schwarzschild horizon and the interior no de Sitter horizon. The collapse turns around; the measurement seam closes **without** the runaway saturation `σ(R) → 1` that a true horizon demands. This is the formation dynamics the seam picture lacked.

This step is a **bridge**: the general-relativistic arrest and junction construction are owned by the external result; D0 contributes only the finite-seam reading and the compactness at which the seam closes. It is not derived from M1 and is not a core claim.

### 07.51.2 The causal compactness ceiling `C_max = 3/8` (a named-gap lemma)

The compactness at which the seam closes is not free. Treat the photon orbit that just grazes the seam (`χ₂ = θ⋆`), the junction closure relating compactness to the interior opening angle (`2C = sin²χ₂`), and the holonomy/return condition of the seam cycle (`cos θ⋆ = 4C − 1`). Eliminating the two angles gives a single master equation [^b07-52]:

```math
2C = 1 - (4C-1)^2 \;\Longleftrightarrow\; -2C\,(8C-3) = 0 \;\Longrightarrow\; C \in \{0,\ 3/8\}.
```

Discarding the trivial root, the maximal causal compactness is `C_max = 3/8 = 0.375`. It sits strictly between the photon sphere `1/3` and the Buchdahl bound `4/9`, and strictly below the black-hole value `1/2` — a specific horizonless prediction, not a tuned number. Structurally it reads as

```math
C_{\max} = \frac{\mathrm{rank}}{|\Omega_8|} = \frac{3}{8},
```

with `rank = 3` the spatial-transport rank of the scene adjacency (owned by the signature split) and `|Ω₈| = 2³ = 8` the role-orientation octet.

The algebra of `3/8` is exact. Its *identification* with `rank/|Ω₈|` rests on one postulated bridge — that rank-3 transport is the causal light-cone on the 3-sphere seam — which is **not** forced from M1. Accordingly the result is a **lemma with a single named gap**, not a theorem: the master equation is closed, the structural reading is the open obligation.

### 07.51.3 The causal partition is forced (rank-3 = causal cone)

The identification of the three rank-3 transport modes with the spatial directions of a light-cone — the single Pisot modular flow supplying the time direction — is **forced**, not postulated (claim `D0-RANK3-CAUSAL-CONE-FORCING-001`, Lean `D0.Synthesis.RankCausalConeForcing`, cert `vp_rank3_causal_cone_forcing.py`). The closure is by **counting**, not by a smooth-manifold construction:

- The three rank-3 modes are **reversible**: the depressed cubic `λ³ − 359λ − 2574` has discriminant `−4(−359)³ − 27(−2574)² = 6\,185\,264 > 0`, so its three roots are *real* and distinct — the spatial modes carry no arrow.
- The single Pisot modular flow is **irreversible**: exactly one direction with `|ψ| < 1` (the time arrow; "arrow = Pisot contraction" is already **FORCED**, BOOK_06 §06.30a).
- A Lorentzian `(3,1)` form has exactly **one** timelike axis and **three** spacelike. The counts match — one arrow ↔ one timelike, three reversible ↔ three spacelike — and a Euclidean `(4,0)` is **excluded**, because the four directions are not alike (one carries an arrow, three do not), forcing the form *indefinite*. Since the timelike axis must be the arrow-direction (arrow = time), the timelike axis **is** the Pisot flow and the three spacelike axes **are** the reversible rank-3 modes.

So `rank-3 = the three spatial/causal directions of the cone` is forced, and `C_max = rank/|Ω₈| = 3/8` is structurally grounded (THE for the dimensionless ratio). **The only residual** is the cone-speed / smooth Lorentzian metric `g_{μν}` (the light-speed coefficient) — a *unit convention* whose smooth-manifold reconstruction is the **Connes-reconstruction** residual, owned by the cited edge `ASSUMP-CONNES-RECONSTRUCTION` (`D0.Bridge.ConnesReconstructionBridge`). The causal **structure** (signature + partition + null cone) is forced; the metric/cone-speed is the named Connes unit, not claimed here. The "static rank vs cone-speed/signature" gap is split: the *signature and partition* are forced; only the *cone-speed* remains, and it is a unit, not a derivation.

**The spatial metric form is realized, with a falsifiable anisotropy (`D0-RANK3-METRIC-TRANSPORT-001`).** The rank-3 spatial metric is the equitable-quotient transport quadratic form of `K(9,11,13)`, `B = [[0,11,13],[9,0,13],[9,11,0]]`, with characteristic polynomial `λ³ − 359λ − 2574` (`359 = |E|` the coupling): eigenvalues `≈ {−12.08, −9.76, +21.84}` — a non-degenerate `(1+,2−)` form, so the light cone is its null set `{x : Q(x)=0}` (cert `vp_rank3_metric_transport.py`). Because the zones `9 ≠ 11 ≠ 13` are unequal, the two negative eigenvalues **split** (`−12.08 ≠ −9.76`): the spatial transport metric is **anisotropic at the carrier level**, becoming isotropic only in the equal-zone limit `(n,n,n)` (spectrum `{2n,−n,−n}`). This is a finite **falsifier**: D0 predicts a Planck-level anisotropy of the spatial form. Honest scope: this realizes the spatial quadratic *form* and its null cone; it does **not** fix the overall cone-speed / dimensionful unit (still the `c=1`/Connes question), and it is a distinct object from the `(3,1)` Pisot-counting signature above — the two are not conflated.

**The cone-speed unit is `c=1=edge/tick`, internal — Connes is confirmation, not owner (`D0-CONNES-DISTANCE-GEODESIC-001`).** On the finite scene the Connes spectral distance `d_C(p,q)=sup{|f(p)−f(q)| : ‖[D,f]‖≤1}` **equals the graph geodesic** distance (the admissible `f` are exactly the 1-Lipschitz-per-edge functions; the sup is attained by `f=d_geo(·,p)` and bounded above by telescoping) — so the metric is an *internal* graph quantity, not an external input. And `‖[D,a]‖≤1` means a signal moves at most one edge per tick, so the cone speed is `c=1=edge/tick` — dimensionless, with **no external light-speed constant** (cert `vp_connes_distance_geodesic.py`). Therefore the last residual of §07.51.3 is internalized: the cone-speed unit is structural. `ASSUMP-CONNES-RECONSTRUCTION` is accordingly a **continuum-limit confirmation, not an owner**: the smooth-manifold (Connes 2008) reconstruction *confirms* that the internal geodesic metric converges to a Riemannian `g`, rather than *owning* the cone-speed gap. The single remaining external statement is the finite→smooth continuum limit itself, owned by the specific convergence framework — Rieffel compact quantum metric spaces + Gromov–Hausdorff(–Prokhorov) convergence (`D0-RIEFFEL-GHP-CONTINUUM-OWNER-001`, `ASSUMP-RIEFFEL-GHP`): each finite scene is an internal compact quantum metric space (Connes distance = geodesic), and the refinement sequence converges in quantum Gromov–Hausdorff distance to a smooth Riemannian limit. Connes reconstruction identifies the limit *object* (a commutative spectral triple is a spin manifold); Rieffel/GHP own the *convergence* to it. The named residual is exact: D0 does not prove the refinement sequence is GHP-Cauchy — that is not a finite computation — so the convergence is owned by Rieffel/GHP, not derived inside D0.

**Named external owner of the gap.** The classical theorem that *would* close "metric = spectrum" once the causal reading is supplied is the **Connes reconstruction theorem** (A. Connes, *On the spectral characterization of manifolds*, arXiv:0810.2088, 2008): a commutative real spectral triple satisfying the axioms is canonically the spectral triple of a compact oriented Riemannian spin manifold, with the metric recovered by the Connes distance. This is recorded as the forcing-owner edge `D0-CONNES-RECONSTRUCTION-OWNER-001` (assumption `ASSUMP-CONNES-RECONSTRUCTION`, Lean `D0.Bridge.ConnesReconstructionBridge`): naming the owner raises the gap from "asserted" to "owned by a cited classical theorem", without claiming D0 derives metric = spectrum and without closing the rank-3 = cone identification (BOOK_05 §05.8.R).

A complementary owner on the *thermodynamic* side is **Jacobson's derivation** (T. Jacobson, *Thermodynamics of spacetime: the Einstein equation of state*, Phys. Rev. Lett. **75**, 1260, 1995): the Einstein equation follows from the Clausius relation `δQ = T dS` together with the horizon entropy `S = A/4` imposed on every local Rindler horizon — i.e. gravity is an *equation of state*, emergent from the thermodynamics of information crossing causal horizons. In the D0 lens this is exactly "gravity emergent from the thermodynamics of recording": the same `A/4` capacity that bounds the archive (Bekenstein) yields the field equation by Jacobson's argument. This strengthens the Connes "metric = spectrum" owner with a second, thermodynamic external owner; both are cited, neither is re-derived inside D0, and neither closes the rank-3 = cone gap.

## Apparatus — sources & open obligations

_Traceability for the integrated forcing arguments and the open proof obligations. The body above reads as the monograph; these endnotes carry the GOLDEN/v17 provenance and cert/Lean status so nothing is lost._

[^b07-1]: open obligation — cert obligation open
[^b07-2]: open obligation — cert obligation open
[^b07-3]: forcing: GOLDEN DEF II.4.APPX5.14.0; THE II.4.APPX5.14.3
[^b07-4]: forcing: GOLDEN DEF II.4.APPX5.15
[^b07-5]: forcing: GOLDEN THE II.4.APPX5.15.0b
[^b07-6]: forcing: GOLDEN DEF II.4.APPX5.16.3
[^b07-7]: forcing: GOLDEN LEM II.4.APPX5.16.3b
[^b07-8]: forcing: GOLDEN DEF II.4.APPX5.16A;
THE II.4.APPX5.16A.4
[^b07-9]: forcing: GOLDEN
CHK 21.K.2; DEF 21.K.1
[^b07-10]: forcing: GOLDEN COR II.4.APPX5.21.C
[^b07-11]: forcing: GOLDEN DEF II.4.APPX5.21
[^b07-12]: forcing: GOLDEN THE II.4.APPX5.22.3
[^b07-13]: forcing: GOLDEN THE II.4.APPX5.22.3, micro-example II.4.APPX5.21.EX1
[^b07-14]: forcing: GOLDEN DEF II.4.APPX5.21, THE II.4.APPX5.22.3, COR II.4.APPX5.21.C
[^b07-15]: forcing: GOLDEN THE II.4.APPX5.16A.4
[^b07-16]: forcing: GOLDEN THE II.4.APPX5.23.1
[^b07-17]: open obligation — cert obligation open
[^b07-18]: forcing: GOLDEN DEF II.3.10
[^b07-19]: forcing: GOLDEN LEM II.3.12
[^b07-20]: forcing: GOLDEN DEF II.3.15
[^b07-21]: open obligation — cert obligation open
[^b07-22]: open obligation — cert obligation open
[^b07-23]: forcing: v17 IR-Lorentz Hull-Pushforward Lock, `SCHUR-LOCKED`
[^b07-24]: forcing: v17 IR-Lorentz Hull-Pushforward Lock
[^b07-25]: forcing: GOLDEN DEF 75.1, BOOK VI Extensions §75
[^b07-26]: forcing: GOLDEN LEM 75.2, BOOK VI Extensions §75
[^b07-27]: open obligation — cert obligation open
[^b07-28]: forcing: GOLDEN COR II.4.7, BOOK-II-MECHANISM
[^b07-29]: forcing: GOLDEN DEF II.4.4
[^b07-30]: open obligation — cert obligation open
[^b07-31]: open obligation — cert obligation open
[^b07-32]: forcing: GOLDEN THE 7.6, v17 BOOK_07 §07.8
[^b07-33]: forcing: GOLDEN THE 07.8B, v17 BOOK_07 §07.8B
[^b07-34]: forcing: GOLDEN THE II.4.APPX5.23.1
[^b07-35]: forcing: GOLDEN THE II.4.APPX5.23.B1
[^b07-36]: definition and its M1 reduction-to-substance forcing owned by §07.4; forcing:
GOLDEN THE II.4.APPX5.22.3
[^b07-37]: forcing: GOLDEN DEF II.4.SR.2
[^b07-38]: forcing: GOLDEN DEF
II.4.SR.3, DEF II.4.SR.4
[^b07-39]: forcing: GOLDEN THE II.4.SR.5
[^b07-40]: forcing: GOLDEN COR II.4.SR.6
[^b07-41]: forcing: GOLDEN DEF
II.4.SR.2–4, THE II.4.SR.5, COR II.4.SR.6
[^b07-42]: forcing: GOLDEN REM II.4.SR.1.PROSYS
[^b07-43]: forcing: GOLDEN THE 25.1.1
[^b07-44]: forcing: GOLDEN BRIDGE 25.B
[^b07-45]: forcing: GOLDEN THE 26.1.1
[^b07-46]: forcing: GOLDEN BRIDGE 26.B
[^b07-47]: forcing: GOLDEN THE 77.1, owner of the [J,Y] order argument
[^b07-48]: forcing: GOLDEN DEF 75.1 / LEM 75.2
[^b07-49]: forcing: GOLDEN THE 77.1
[^b07-50]: forcing: GOLDEN COR 77.2; arrow-of-time-from-M1
[^b07-51]: external anchor / bridge: Jampolski-Rezzolla PRD 113 L121502 (2026) arXiv:2509.15302 (horizonless gravastar, dS-core arrested OS collapse). cert vp_gravastar_os_arrest.py; claim D0-GRAVASTAR-FORMATION-BRIDGE-001 (BRIDGE, ASSUMP-GRAVASTAR-GR-EXTERNAL). GR junction physics owned externally; D0 owns the finite seam reading.
[^b07-52]: LEM: cert vp_gravastar_compactness.py derives C_max=3/8 from -2C(8C-3)=0 (exact). The former rank-3=causal-cone named gap is closed/re-scoped (Iter-21): the (3,1)+Pisot signature arithmetic is machine-checked CORE (claim D0-RANK3-CAUSAL-CONE-FORCING-001, Lean D0.Synthesis.RankCausalConeForcing), and the rank<->metric-cone identification is a named BRIDGE (CORE_BRIDGE_SPLIT), not over-claimed as M1-forced. Residual cone-speed/smooth metric owned by ASSUMP-CONNES-RECONSTRUCTION; claim D0-COMPACTNESS-LIMIT-001.
