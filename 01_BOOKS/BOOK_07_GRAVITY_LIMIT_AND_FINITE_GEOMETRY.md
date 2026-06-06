# BOOK 07 — Gravity limit and finite geometry

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

The book separates three things that were interleaved in earlier gravity drafts:

1. the internal finite-geometric construction;
2. the SI/metrological Newton shadow;
3. the traced-out complement/cosmology boundary cross-reference.

The finite TT gravity carrier is a symmetric projected sector built from finite
edge/line probes and is compatible with the finite Hodge complex.


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

This is not a replacement for general relativity. It is a finite-readout construction of the data from which the metric description becomes the stable large-scale language.

## 07.4 Causal section and metrological separation

The internal causal section is already fixed in the foundation:

```math
\ell_0^{D0}=1,\qquad \tau_0^{D0}=1,\qquad c_{D0}=1.
```

The SI export of this section uses the terminal matter/readout bridge:

```math
\tau_0=\frac{h}{38m_ec^2},\qquad
\ell_0=c\tau_0=\frac{h}{38m_ec}.
```

Book 07 uses this only as metrology. It is forbidden to use the electron terminal scale as a hidden adjustable gravity parameter. The single-section discipline is

```math
\Lambda_{act}=\frac{h}{\tau_0}=38m_ec^2,
```

with action-scale closure assigned to Book 03/04 and dimensionless spectral scale-separation invariant export assigned here.

Type safety: `D_L` is the dimensionless finite dimensionless spectral scale-separation invariant invariant.  The
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

The finite carrier is now explicit in Lean as `D0.Geometry.finite_spin2_tt_carrier_closed`.  A finite TT mode carries a symmetric response matrix, zero trace and a transverse condition.  This does not by itself prove the full smooth graviton QFT.  It closes the finite D0 carrier needed before the Einstein--Hilbert bridge is invoked.

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

The heat trace is not a continuum primitive. It is the macro spectral shadow of finite operators over the D0 tiling hull. Curvature is the detector-visible response of this spectral shadow after finite coarse-graining.

The formal Lean owner is `D0.Geometry.NonCommutativeSolenoidGravity` (`d0_heat_trace_admits_solenoid_spectral_triple_approx`), and the verification certificate is `05_CERTS/vp_noncommutative_solenoid_gravity.py` (`PASS_NONCOMMUTATIVE_SOLENOID_GRAVITY`).

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

The q-mass and boundary residual terms are retained as cross-reference material, not as independent gravity knobs:

```math
q_{mass}=(1+\delta_0^3)^{-1},
```

```math
q_{exact}=q_{mass}q_{res}.
```

The interpretation belongs to the matter/EW boundary layer in Book 04 and to the residual cut discipline in Book 05/07. It is forbidden to use `q_res` as a scalar-curvature fit parameter.

The canonical gravity equation must remain typed:

```math
\text{closed dimensionless spectral scale-separation invariant}\rightarrow \ell_P^{D0}\rightarrow G_N^{D0},
```

not

```math
\text{residual mismatch}\rightarrow \text{new scalar repair}.
```

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
4. uses `q_res`, `q_mass` or boundary information as hidden scalar fitting;
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

| Claim ID | Status | Stage | Claim | Book 07 role |
|---|---|---|---|---|
| `D0-FOUND-003` | `CORE-FOUNDATION` | Foundation | Minimal continuum-measurement skeleton | reference to Books 01-04; used in gravity bridge |
| `D0-MATH-001` | `D0-RESOLUTION-EXACT` | Quotient/Resolution | Finite phi-runtime and stop ideal | reference to Books 01-04; used in gravity bridge |
| `D0-METRO-001` | `CORE-FOUNDATION` | Bridge/Dictionary | Single causal line/tick invariant | reference to Books 01-04; used in gravity bridge |
| `D0-METRO-002` | `SINGLE-SECTION-OUTPUT` | Single Section | Lambda_act single action section | reference to Books 01-04; used in gravity bridge |
| `D0-BOUND-001` | `D0-RESOLUTION-EXACT` | Quotient/Resolution | q_mass and boundary curvature residual | reference to Books 01-04; used in gravity bridge |
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

**EH macro-interface status update (D0-GRAV-EH closure):**  
Finite A2 variation + finite Bianchi + conserved stress pairing selects the unique Einstein tensor class as the macro response.  
The previous “EH bridge calibration” language is replaced by:  
“EH macro-interface closed up to standard smooth-limit dictionary: finite A2 variation + Bianchi selects Einstein tensor class.”  
SI G_N remains single-section metrological shadow (no change).

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

### 07.19.1 `D0-GRAV-001`: dimensionless spectral scale-separation invariant theorem and Planck/Newton shadow

D0 derives a dimensionless spectral scale-separation invariant map before any Newton coefficient is named:

```math
D_L=\Omega_8\varphi^{V_9V_{11}}\left(1+{\delta_0\over V_{13}}\right).
```

The semantic factors are fixed:

```text
О©8     = full-cycle multiplicity,
V9V11  = 99 witness-to-transport heat depth,
1+Оґ0/V13 = terminal-shell leakage.
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

Primary certs: `vp_final_terminal_scale_depth_theorem.py`, `vp_gravity_metric_heat_kernel_two_part.py`.

### 07.19.2 `D0-GRAV-002`: Newton coefficient finite-cycle holonomy

The finite-cycle holonomy row is the same single-section completion read
through the Einstein/Planck dictionary.  It is not a separate fit to CODATA.
The gravity completion certificate gives the same `D_L`, `ell_P`, and `G_N`
after the external SI section is declared, and stress-tests nearby denominators
to show the chosen terminal leakage is not arbitrary.

**Closure.**  The Newton coefficient row is closed as an SI-calibrated
finite-cycle holonomy shadow of the dimensionless spectral scale-separation invariant theorem.  Comparison to CODATA
is a benchmark, not an input.

Primary certs: `vp_single_section_gravity_completion.py`, `vp_gravity_gn_bridge_demo.py`.

### 07.19.3 `D0-GRAV-003`: higher-curvature finite cut rule

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
О·_HC(L_cut) = 7.31282200941126e-12.
```

**Closure.**  Below this cut the active description is finite D0 support/readout algebra, not a new continuum higher-curvature sector.  No new gravitational anchor is introduced.

Primary cert: `vp_residual_targets_qg_cut_closure.py`.

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

The terminal shell `V13` is excluded from the exponent because it is the boundary/readout shell, not part of active line-covariant propagation.  Negative controls are structural: `98` removes one covariance channel; `100` adds an ambient line state; `117=9Г—13` incorrectly promotes the terminal shell to propagation duty.  Thus the exponent `99` is locked by active line covariance, not by a posteriori fitting of `G_N`.

## 07.23 Phase-unfolding master chain

D0 no longer treats spatial branching as a primitive geometric background.  An ordered finite registration can generate visible geometry through a phase quotient.  For a phase circumference \(\tau\), the map

\[
U_\tau(n)=(n,n\bmod \tau)
\]

turns the one-dimensional tick sequence into a branch foliation whenever an integer pair \((q,m)\) satisfies \(|q-m\tau|\ll 1\).  The residue classes modulo \(q\) are the coherent branches.  An admissibility filter selects the branches visible to the detector.

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

## 07.24 Phase-unfolding capacity source for shell depth

The phase-unfolding theorem uses the capacity closure of `ABCD`, `О©8`, and `V9`. The first stable terminal return modulus is

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

The normalized D0 phase generator is not an arbitrary irrational angle.  The
primitive positive-response theorem gives `p+pВІ=1`, hence the return branch is

```math
\alpha_{D0}=p^2=\varphi^{-2}.
```

The physical phase increment is therefore `2ПЂ/φВІ`.  By the Hurwitz/continued-
fraction extremality of the `φ` class, this rotation is maximally resistant to
low-denominator rational locking.  In D0 terminology, it is the admissible phase
increment that suppresses uncontrolled metric arms in the unresolved complement.

This does not eliminate finite branches.  Branches appear only after a finite
readout quotient chooses a return modulus.  Thus the same chain has two layers:

```text
φвЃ»ВІ irrational rotation  → non-resonant archive smoothing;
finite return modulus q  → residue branch geometry.
```

This closes the compatibility between macroscopic smoothness and finite branch
unfolding.

The active owner promotes this from prose to a finite information-quasicrystal
statement:

```text
D0.Geometry.HurwitzRigidPhaseGenerator
D0.Geometry.PhaseReturnBranchCount
D0.Geometry.PhaseUnfoldingQuasicrystal
```

The theorem `phi_phase_is_nonperiodic` says the `phi^-2` phase does not admit a
rational translational period.  The theorem
`finite_return_modulus_unfolds_branches` says that visible arms are generated
only when the finite quotient chooses `q_T=44` or `q_EW=710`.  Thus D0 geometry
is neither smooth primitive continuum nor periodic lattice: it is finite,
ordered, aperiodic and readout-generated.


## 07.26 Lorentz and smoothness transition theorem

The Lorentz carrier is induced by the terminal role capacity before any smooth geometry is introduced. The single runtime/normalization role and three comparison roles force signature `(1,3)`. A Lorentz-facing gravity claim must therefore pass through the Clifford carrier

```text
{Оі^Ој,Оі^ОЅ}=2О·^{ОјОЅ}I,
О·=diag(+1,-1,-1,-1).
```

Smooth geometry is then a separate bridge. At finite stage `N`, line probes define a covariance matrix `G_N`; together with the finite incidence operator this determines a Laplacian-like operator `О”_N` and heat trace

```text
О_N(u)=Tr exp(-uО”_N).
```

The continuum metric is admissible only if the family is projectively compatible, uniformly non-degenerate on the retained sector, and has a stable four-dimensional Weyl heat-trace asymptotic. Thus D0 does not assume a smooth manifold; it specifies when a smooth manifold is a valid macro-shadow.

## 07.27 Canonical archive Laplacian and curvature obstruction

The finite archive is equipped with a canonical weighted graph Laplacian $L$ derived from the cyclic phase-distance metric. We prove in Lean that $L$ is symmetric, nonnegative, and has a row-sum zero constant mode. Projective compatibility of the Laplacian under refinement fails due to topological cycle splitting (no-go on projective compatibility), and a curvature obstruction skeleton prevents projection flatness on refined fibers (no-go on curvature flatness). This formalizes the non-triviality of the finite geometry.

## 07.28 Renormalized archive Laplacian / RG geometry

The current refinement is that the local phase Laplacian is not required to commute strictly with archive pullback. The finite gravity operator is read through the effective coarse operator

```text
L_eff(n) = B^T L_{n+1} B,
```

where `B` is the matrix of the canonical phase coarse-graining projection. The Lean module `D0.Geometry.ArchiveLaplacianRG` defines coarse graining, pullback energy, the operator residual, renormalized compatibility, and the theorem that zero RG residual is equivalent to exact flat compatibility. It also proves that strict pullback compatibility fails for the nearest-neighbor phase Laplacian.

The certificate `vp_archive_laplacian_rg_flow.py` confirms the finite flow: the projected effective operator has scale `c_n = 1` and zero residual for the canonical phase projection, while the strict pullback commutator is a stable rank-2 seam defect. Thus the curvature statement is RG-geometric: flatness means vanishing residual after the declared coarse-graining, not naive equality of local operators at different resolutions.

## 07.29 Seam curvature and archive action

The internal curvature object is now the seam commutator

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

The seam action now has a finite variational layer.  Varying the coarse
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
The certificate `vp_archive_variational_field_equation.py` checks the finite
quadratic expansion, the gradient/source pairing, the conserved stress
representative, and negative controls for invalid variations, nonconserved
sources, and wrong projections.

## 07.31 Admissible variation space and variational stress dual

The current Lean layer closes the variational-dual algebra for the finite archive field equation.  The raw curvature gradient

```text
G_n = -2 B_n^T C_n
```

is already row-conserved by the traced-out complement Bianchi identity, but it is not required to be symmetric.  The admissible Laplacian variation object carries the obligations used by the field equation:

```text
ОґL = ОґL^T,
ОґL В· 1 = 0,
phase-local support obligation.
```

The formal result is not a prose identification of `G_n` with stress.  It is the theorem that the variation pairing only sees the symmetric component of any matrix:

```text
pairing(A, ОґL) = pairing(symPart(A), ОґL),
```

for every admissible variation `ОґL`.  Equivalently, skew-symmetric parts are in the annihilator of the admissible variation space.  Lean ownership:

```text
D0.pairing_depends_only_on_symmetric_part
D0.skew_part_annihilates_admissible_variations
D0.raw_gradient_equivalent_to_canonical_stress
D0.canonical_stress_symmetric
```

The currently proved canonical representative is therefore the variational representative

```text
canonicalStressRepresentative(G_n) = symPart(G_n),
VariationEquivalent(G_n, canonicalStressRepresentative(G_n)).
```

This does not by itself close the conservation of the symmetric representative.  Lean currently records the guardrail

```text
NO_GO_CANONICAL_STRESS_CONSERVATION_PROJECTION
```

which states that taking the symmetric part of an arbitrary matrix is not a conservation-preserving operation.  The constrained admissible projection is successfully constructed as `constrained_stress_projection_symmetric_conserved_equivalent` (claim ID `D0-ARCHIVE-STRESS-CONSERVATION-001`) using the projection:

```math
T = S - \frac{1}{N}\left(v\mathbf 1^T + \mathbf 1 v^T\right),
\qquad
S=\frac{G+G^T}{2},
\qquad
v=S\mathbf 1.
```

For raw gradients with `G В· 1 = 0`, this projection is symmetric, row-conserved, and variation-equivalent to `G_n` for all admissible variations `ОґL` with `ОґL В· 1 = 0`.

## 07.32 Discrete Poisson / weak-field equation

The finite weak-field skeleton is now the graph Poisson problem on the canonical cycle Laplacian:

```math
L\phi = \rho.
```

Lean has closed the structural part of this finite equation:

```text
poisson_requires_neutral_source:
  ArchivePoissonEquation φ ПЃ → NeutralSource ПЃ

poisson_solution_unique_mod_constant:
  ArchivePoissonEquation φв‚Ѓ ПЃ →
  ArchivePoissonEquation φв‚‚ ПЃ →
  φв‚Ѓ - φв‚‚ is constant
```

The reason is the constant zero mode of the canonical Laplacian.  Thus solvability forces

```math
\sum_i \rho_i = 0,
```

and uniqueness is only modulo the constant gauge mode.

The Python certificate `vp_archive_weak_field_poisson.py` checks the finite-cycle Laplacian construction, a point-pair neutral source, zero-mean gauge fixing, residual control, positive energy, Green symmetry, uniqueness modulo constants and negative controls.

The non-vacuous scalar reduction is successfully closed under claim ID `D0-ARCHIVE-SCALAR-REDUCTION-001` via the theorem:

```text
scalar_stationarity_implies_archive_poisson:
  ScalarSectorStationary n φ ПЃ → ArchivePoissonEquation φ ПЃ
```

The predicate `ScalarSectorStationary` is a non-vacuous point-test stationarity condition, completing the weak-field reduction proof.

## 07.33 Final finite-geometry theorem chain

The typed-closure finite-geometry chain is now closed as a theorem/cert/no-go
sequence rather than an informal gravity analogy:

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

The gravity book no longer treats spin-2 as a field tag. Poisson response plus
a declared TT mode was not yet a derivation. The active finite statement is now
a quotient chain.  A weak-field metric response enters the GR
bridge only after the following finite reduction has been supplied:

Poisson response plus a declared TT mode was not yet a derivation.

```text
finite symmetric weak-field mode h
-> finite longitudinal/gauge representative
-> finite scalar trace representative
-> quotient reconstruction certificate
-> conserved-stress annihilation of longitudinal direction
-> conserved-stress annihilation of trace direction
-> transverse-traceless representative h_TT.
```

The Lean owner is `D0.Geometry.FiniteWeakFieldQuotient`.  It replaces the weak
reading "there exists a TT-shaped mode" with an explicit finite reduction object.
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

The improvement is theoretical, not editorial.  Earlier text could be attacked as
an analogy: Poisson response plus a declared TT mode was not a derivation of
the spin-2 carrier. The active replacement forces the missing step to be a
finite object with reconstruction and stress-annihilation fields.  Smooth GR is
still a bridge reading, but the finite carrier entering that bridge is no longer
a label or a primitive graviton import.

### 07.35.1 Rejected readings

The following readings are no longer active D0 claims:

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

The gravity bridge now has an explicit tick-gauge prerequisite.  The weak-field spin-2 derivation closes the TT carrier; the tick/Lorentz layer closes the causal cone on which that carrier propagates.  The active finite owners are

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

The previous spin-2 layer closed the finite TT representative. The active closure adds the next missing object: a finite dynamics certificate over the TT representative.

The new owner is

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

The active gravity chain is now

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

The TT projector is no longer represented by an abstract variable.  The concrete owner is

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

with `<A,B> = Tr(A eta B eta)`.  Lean proves `PiTT4_idempotent`, `PiTT4_is_tt`, `PiTT4_kills_trace`, `PiTT4_kills_gauge`, `WTT4_preserves_tt`, `WTT4_energy_nonnegative` and `spin2_coupling_depends_only_on_tt_stress`.  The public certificate `vp_finite_spin2_wave_operator.py` checks the projector on all ten basis elements of `Sym(4)`, verifies rank 2 and removes the previous random `h_test` style of evidence; its concrete backend is `vp_finite_spin2_wave_operator_concrete.py`.

The D0 memory torus is a separate internal shell geometry used by the
matter/flavour sectors.  It does not replace the terminal four-role TT
projector, does not derive Einstein equations, and does not assign Newton's
constant.  Spin-2 closure remains the finite TT projector, `WTT4` and conserved
stress coupling.

## 07.39 Spin-2 two-polarization arithmetic closure

The finite dynamics certificate is now accompanied by an arithmetic readout for
the 4D Lorentz-facing spin-2 degree count.  The new owner is

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

This removes the previous ambiguity between "TT carrier exists" and "the
Lorentz-facing spin-2 readout has the correct two physical polarizationsвЂќ.  The
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

The finite owner is `D0.Gravity.EntropicArchiveInterface`: graph Laplacian,
boundary cut capacity, archive flux conservation and nonnegative entropic
surface tension.  The macro owner is `D0.Gravity.MacroEinsteinInterface`: a
finite witness packages the traced-out complement conservation theorem, the explicit
`PiTT4/WTT4` carrier, `higher_curvature_terms_below_finite_readout_cut` and
the spectral `a2_is_eh_proxy` theorem.

The active/archive split is not an extra matter component: active contraction and archive expansion are eigen-branches of one toral automorphism, and the determinant invariant gives exact phase-volume balance before the macro gravity interface is read.

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
Therefore the Einstein-Hilbert / Einstein tensor class is the macro-interface (finite A2 variation + Bianchi selects the class; previous loose "EH bridge calibration" language is replaced by closed finite-response status).

## 07.49 Critical-collapse discrete self-similar log-time lattice and spacetime-crystal horizon

PRL 2026 (arXiv:2601.14358) constructs closed analytic large-D discretely self-similar solutions of the Einstein–massless-Klein–Gordon critical-collapse system.

D0 reads this as a gravity-side closure of the finite horizon transition: black-hole birth passes through a discrete log-scale discrete self-similar log-time lattice.

The self-similar horizon (SSH) is the null boundary where the echo-lattice vector becomes lightlike. In D0 this is the capacity-null boundary of the terminal horizon readout.

New D0 chain (dynamic birth, not static saturation):

```text
trace-heat gravity
→ capacity density growth
→ critical echo-lattice phase
→ self-similar null horizon
→ terminal boundary of traced-out complement
→ black-hole saturation
```

New typed owners:
- `D0.Gravity.CriticalCollapseDSS`
- `D0.Gravity.EchoCapacityHorizon`

New theorem block:
- D0-GRAV-DSS-001 Critical Collapse Echo-Lattice Closure
- D0-GRAV-DSS-002 Self-similar horizon is capacity-null boundary
- D0-GRAV-DSS-003 Echo admissibility constraint (NLO/convexity/SSH filtering)
- D0-GRAV-DSS-004 Spacetime Crystal Bridge
- D0-GRAV-DSS-NOGO-001 Smooth Monotone Collapse Failure

Certificate: `05_CERTS/vp_critical_collapse_dss_echo_lattice.py`
Passport manifest: `08_PASSPORTS/CriticalCollapseDSS/dss_prl2026_manifest.json`

The external analytic certificate owns the GR construction (closed DSS family + NLO filtering). D0 owns the finite log-time readout / capacity / admissibility interpretation.

Black-hole formation is a critical finite-readout phase transition through a spacetime-crystal echo horizon, not a purely smooth density-threshold singularity (while higher-curvature corrections are finite-cut suppressed).

## 07.50 Finite horizon capacity and A/4 witness

Finite boundary shell ∂R reaches capacity saturation σ(R) = 1.  
Cost of external active extension → ∞.  
Terminal archive quotient Y : H_R → H_N makes active information inaccessible, **not deleted**.  
ABCD terminal alphabet supplies the factor of 4:

N_∂ = A / a_0 ,   S_∂^{D0} = N_∂ / 4 .

This is derived from four terminal readout roles per saturated boundary cell (not imported Bekenstein-Hawking normalization).  
Negative controls (A/2, A/8, volume entropy, singularity-as-deletion) are rejected.

New typed owners:
- D0.Gravity.FiniteHorizonCapacity
- D0.Gravity.BlackHoleA4EntropyWitness

Certificates: 05_CERTS/vp_black_hole_capacity_a4_witness.py  
Passports: 08_PASSPORTS/BlackHoleCapacity/

Cross-book:
- Book 06: saturation as runtime halt / active-archive quotient.
- Book 05: D0-BH-CAP-NOGO-001 (singularity-as-information-deletion rejected).
- Book 08: PBH formation must combine DSS echo-lattice birth + this finite A/4 capacity witness.

## 07.42 Phason/phonon split and dark metric response

The finite quasicrystal operator layer separates active visible strain from
archive phason strain.  Gravity sees both phonon and phason strain energy; EM
sees only active visible window; archive phason strain is a dark metric source.

The owner is `D0.Physics.ArchivePhasonDarkMatter`:

```text
archive_phason_strain_is_dark_to_em
archive_phason_strain_can_source_metric_response
archive_phason_strain_em_dark_metric_visible
```

The certificate `vp_archive_phason_dark_matter.py` checks PSD archive strain
energy, zero EM archive coupling, positive heat/metric increment, and a
nonzero finite phason gradient sourced by a cluster.

## 07.47 Noncommutative solenoid gravity

The finite TT operator W_TT is the two-polarization sector of the D0 solenoid spectral geometry. The smooth Einstein interface is the macro shadow of heat-trace covariance over this noncommutative solenoid approximant.

The Lean owners are `D0.Geometry.NonCommutativeSolenoid` (`d0_hull_admits_noncommutative_solenoid_model`) and `D0.Geometry.NonCommutativeSolenoidGravity` (`finite_spin2_operator_is_tt_sector_of_solenoid_spectral_geometry`, `wtt4_is_compatible_with_noncommutative_solenoid_geometry`), and the verification certificate is `05_CERTS/vp_noncommutative_solenoid_gravity.py` (`PASS_NONCOMMUTATIVE_SOLENOID_GRAVITY`).

## 07.48 LIGO BBH mass-defect external comparison protocol

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

Current external-data runner result:

```text
PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT
PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_ALL
PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_CLEAN_BBH
```

The current-catalog comparison uses the pinned GWOSC/GWTC JSON table.  The
frozen D0 mass-defect formula was evaluated on complete BBH rows and compared
against the mean-loss baseline.

Current machine metrics:

```text
primary clean_BBH_run:
  result = PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_CLEAN_BBH
  events_used = 271
  rmse_d0 = 0.00687416
  rmse_mean_baseline = 0.00898949
  rmse_spin_only_negative_control = 0.00868605

all_catalog_run:
  result = PASS_LIGO_D0_MERGER_MASS_DEFECT_CURRENT_ALL
  events_used = 276
  rmse_d0 = 0.00966751
  rmse_mean_baseline = 0.0118123
  rmse_spin_only_negative_control = 0.011562
```

Events with neutron-star/mass-gap components or negative catalog mass defect are
kept in `08_PASSPORTS/GWOSC/ligo_current_mass_defect_anomalies.csv`, not used to
retune the BBH horizon-capacity formula.

Meaning: the clean-BBH run is the primary domain test. The finite D0
horizon-capacity mass-defect operator beats the mean baseline and the spin-only
negative control, so spin-only mass loss is insufficient.
