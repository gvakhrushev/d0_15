# D0 — Finite Verification Theory

> **How can a closed finite system produce reproducible facts without an external classical observer?**

D0 is a mathematical and physical research programme that inverts the traditional foundational order: instead of postulating a smooth space-time continuum, background fields, and an external measuring apparatus, D0 begins from the **operational preconditions of verifiable detection** inside a closed finite system.

Discrete scene structure, registration channels, and (conditionally) continuum limits are derived as consequences of this operational contract. High-energy spectra, gauge structures, and cosmological evolutions are downstream readouts, not independent starting hypotheses.

---

## 1. The Core Inversion (Read This First)

Standard physics proceeds from geometry to observation:
$$\text{Smooth Space-Time } \mathcal{M} \;\longrightarrow\; \text{Lagrangian / Fields } \psi \;\longrightarrow\; \text{External Measurement / Projection}$$

D0 inverts this hierarchy:
$$\text{Verifiability Contract (M1)} \;\longrightarrow\; \text{Functional Tuple} \;\longrightarrow\; \text{Finite Scene } K(9,11,13) \;\longrightarrow\; \text{Readout Spectrum}$$

### The Foundational Premise

> Any process claiming to produce objectively reproducible distinctions between independent runs must already possess the internal means of **distinction**, **retention**, and **independent comparison** — and cannot outsource these operations to an obligatory external catalogue.

From this operational contract (the **M1 condition** + finite realizability), the programme derives:

1. **The Functional Tuple:** distinction ($x \neq y$), persistent record ($x \mapsto \text{rec}(x)$ injective), and independent comparison lines ($l_0 \neq l_1$) are forced as the minimal requirements for empirical verifiability.
2. **The Popperian Bootstrap (`D0-POPPERIAN-BOOTSTRAP-001`):** A theory can be falsified by a "killing test" if and only if it admits a verification contract ($\text{KillingTest}(P) \iff \text{VerificationContract}(P)$). The bare possibility of refutation strictly forces the entire functional tuple. Solitary-witness systems are non-falsifiable.
3. **Endogenous Scene Genesis:** Independent line filling, toral return sterility in $\mathrm{GL}_2(\mathbb{Z})$, and minimal zone capacity uniquely weld the parameters $(|\mathrm{Role}|, \Delta, |\Omega_8|, m, q_T) = (4, 2, 8, 11, 44)$ into the tripartite scene $K(9,11,13)$ with $N=33$ and collision invariant $P_2 = 371/1089$.
4. **The Born Rule as Consistency:** Quadratic detector response ($P \propto |\psi|^2$) is not an arbitrary quantum postulate, but a mathematical consequence of symplectic area preservation on finite carriers; non-quadratic powers destroy unitarity under cyclic independent readout.

The foundational derivation is proved in **BOOK_00** and **BOOK_01** and formalized in Lean 4. Everything else in the repository builds upon this layer.

---

## 2. Architecture & Flow of Forcing

```text
[ Operational Requirements of Verification ]
  - M1: No obligatory external catalogue
  - Finite realizability (no infinite preparation reservoir)
  - Non-solipsism: >= 2 independent checking lines
                         │
                         ▼
[ Popperian Bootstrap & Functional Tuple ]
  - Distinction: x ≠ y
  - Retention: injective record map
  - Comparison: invariant across background catalogues
  - Falsifiability ⟺ VerificationContract (D0-POPPERIAN-BOOTSTRAP-001)
                         │
                         ▼
[ Two-Channel Algebraic Weld ]
  - Toral channel: GL_2(Z) return sterility forces golden class φ
  - Typed channel: binary 2-line preparation (q=2, r=2)
  - Agreement on (4, 2, 8, 11, 44) without external inputs
                         │
                         ▼
[ Canonical Scene K(9,11,13) on N=33 ]
  - Three zones: V_9, V_11, V_13 (sum = 33, inventory = 44)
  - Graph invariant moments: tr(A^2) = 718, tr(A^3) = 7722
  - Topological dimension bounded: no 3-simplices (tetrahedra)
                         │
         ┌───────────────┴───────────────┐
         ▼                               ▼
[ Layer II: Algebraic Spine ]   [ Layer III: Downstream Readout ]
  - Top-Hodge inverse rigidity    - Gauge group decomposition (SU(3)xSU(2)xU(1))
  - Commutant AF-algebra tower    - Puiseux branchings & mass hierarchies
  - Discrete Dirac & Laplacians   - CKM/PMNS phason holonomies
  - Isolated bridge assumptions   - Dynamic cosmological SDE w(z) != -1
    (HeatTraceWeyl, etc.)         - Pre-registered empirical passports
```

---

## 3. The 10-Book Derivation Chain (From Admissibility to Interferometry)

The research corpus is structured into 10 sequential books (`01_BOOKS/BOOK_00` .. `BOOK_09`). Each book solves a concrete mathematical stage and passes its certified invariants to the next:

```text
[ BOOK 00: Admissibility Contract & M1 ]
                 │
                 ▼
[ BOOK 01: Condensed Vacuum & 3-Partite Graph K(n1,n2,n3) ]
                 │
                 ▼
[ BOOK 02: Operator Algebra (F_N, Born Rule R_N = D^†D, Scene Rigidity) ]
                 │
                 ▼
[ BOOK 03: Variational Action S_fb = -log det(I-z F_N) & Conserved Stress ]
                 │
                 ▼
[ BOOK 04: Matter Resonance, Gauge SU(3)xSU(2)xU(1), Puiseux Mass Hierarchy ]
                 │
                 ▼
[ BOOK 05: Verification Audit & Centralized No-Go Ledger ]
                 │
                 ▼
[ BOOK 06: Markov Forgetting Channels, Entropy Monotonicity & Arrow of Time ]
                 │
                 ▼
[ BOOK 07: Noncommutative Spectral Gravity, Heat Trace a_2 ~ R-2Λ, Horizons ]
                 │
                 ▼
[ BOOK 08: Dynamic Cosmology SDE, LambdaCDM Exclusion (w ≠ -1), DESI Drift ]
                 │
                 ▼
[ BOOK 09: Apple Torus, Spin-2 Quadrupole, GW Horizon Capacity (LIGO/GWOSC) ]
```

### BOOK 00: Entry Contract and Admissibility
- **Endogenous Observer:** Theory of a closed system of finite capacity. The apparatus is built from the same discrete elements as the system; no external classical observer is postulated.
- **Admissibility Criterion:** Physical status is granted solely to properties addressable and verifiable in finitely many discrete steps (`DiscriminationKinds.lean`). Unbounded continua and uncomputable infinities are eliminated.
- **The $M_1$ Equivalence Class:** Any data array claiming inter-subjective reproducibility under independent cycles must factor through the canonical quotient $M_1$ (`M1Predicate.lean`, `M1Universality.lean`).
- **Independent Relational Calibration:** Phase drift and detector noise are compensated internally without external length or time standards (`IndependentDetectionRepairGrammar.lean`, `RelationalRepairClosure.lean`).
- **Popperian Bootstrap:** Verifiability requires empirical refutability; `KillingTest P ↔ VerificationContract P` proves that falsifiability forces the functional tuple (`PopperianBootstrap.lean`).
- **Core No-Go Theorems:** `M1CascadeSceneNoGo` (cascade models without unitarity loss are impossible outside $M_1$), `CanonicalSelectorNoGo` (no basis choice without topological support), `SceneCountRouteNoGo` (continuous phase integrals fail on discrete pregeometry).

### BOOK 01: Condensed Foundations and Graph Birth
- **Condensed Pregeometry:** Space-time manifold topology is replaced by condensed sets (covariant functors from compact totally disconnected profinite sets) (`ProfiniteSupport.lean`, `ProjectiveSystem.lean`).
- **Condensed Vacuum:** Projective limit of discrete spectral layers scaled by the golden ratio $\varphi$ (`CondensedPhiVacuum.lean`), with natural intertwining operators (`OperatorNaturality.lean`).
- **Emergence of the Tripartite Scene:** A discrete graph is not embedded into space; it emerges as the combinatorial compatibility skeleton of phase projections (`RawSceneGraph.lean`). Minimality of non-trivial automorphism cycles forces a 3-partite structure $K(n_1,n_2,n_3)$ (`CompleteTripartite.lean`).
- **Absence of 3-Simplices (Tetrahedra):** Theorem `NoThreeSimplices.lean` proves the clique complex is strictly 2-dimensional, cutting off Planck-scale ultraviolet divergence.
- **Discrete Time (The Tick):** Physical time is generated by cyclic phase transitions (`FixedDetectorTimeLadder.lean`, `PhaseTower.lean`). The witness halting theorem (`WitnessHalting.lean`) guarantees finite termination of measurement cycles.
- **Homology & Hodge Spectrum:** Exact rings $H_0, H_1, H_2$ (`GenericTripartiteHomology.lean`) and top-Hodge Laplacian spectra (`GenericTripartiteTopHodgeSpectrum.lean`) fix the channel capacity Euler characteristic $\chi = |V| - |E| + |F|$.

### BOOK 02: Mathematical Proof Spine and Invariant Calculus
- **Feedback Operator Algebra:** The unitary defect operator $F_N = P_N U_N^\dagger Q_N U_N P_N \ge 0$ ($0 \le F_N \le P_N$) on retained ($P_N$) and archive ($Q_N = I - P_N$) subspaces, with resolvent $G_N(z) = (I - z F_N)^{-1}$.
- **Born Rule Derivation:** Quadratic readout response $R_N = D_N^\dagger D_N$ is derived from symplectic area preservation under cyclic phase reading (`finite_effect_born_readout_unique`). Any power $p \neq 2$ violates measure conservation (`BornAreaPreservationNoGo`).
- **Spectral Scene Rigidity:** Unlabelled multiset $\{9, 11, 13\}$ on $N=33$ is uniquely recovered from rational adjacency with $\mathrm{rank} \le 3$ and $\mathrm{tr}(A^2)=718$ without assuming partitions or triangles (`DenseOperatorSceneRigidity.lean`). Top-Hodge data $(D, H, M_2)$ rigidly force the scene (`TopHodgeInverseSpectralRigidity.lean`).

### BOOK 03: Finite Action Operators and Scene Dynamics
- **Finite Log-Det Action:** Logarithmic action $S_\mathrm{fb} = -\log\det(I - z F_N)$, inherently finite and free of continuum ultraviolet infinities.
- **Variation & Universal Source:** $\delta S_\mathrm{fb} = \mathrm{Tr}[(I - z F_N)^{-1} z\,\delta F_N]$; universal feedback source operator $\Pi_\mathrm{fb} = z(I - z F_N)^{-1}$.
- **Conserved Stress on the Boundary Seam:** Boundary stress conservation between retained sector and environment bath (`ConservedStressProjection.lean`), yielding discrete equations of motion.

### BOOK 04: Spectrum, Matter, and Finite Selector Theory
- **Matter as Resonant Modes:** Particles are terminally projected near-critical feedback modes ($F_N \psi_j = r_j \psi_j$ with $|z r_j| \approx 1$ and $P_\mathrm{term} \psi_j = \psi_j$).
- **Gauge Group Decomposition:** $\mathrm{SU}(3)\times\mathrm{SU}(2)\times\mathrm{U}(1)$ arises as the automorphism algebra of 3-partite boundary cycles and $4\times 4$ window selectors (`SMGaugeDecomposition.lean`, `BraidValence.lean`).
- **Hypercharge Quantization:** Anomaly cancellation sums on the discrete lattice force hypercharge denominators to be quantized in multiples of $1/6$ (`SMCharges.lean`, `AnomalySums.lean`, `HyperchargeMinimalDenominator.lean`).
- **Mass Hierarchy via Puiseux Series:** Lepton and quark mass eigenvalues expand in Puiseux series in deformation parameter $\varepsilon = \varphi^{-n}$ on Riemann–Hurwitz branched coverings (`LeptonRiemannHurwitzBranchIndex.lean`, `LeptonGreenPuiseuxOwner.lean`), removing arbitrary Yukawa couplings.
- **CKM & PMNS Phason Holonomies:** Flavour mixing matrices are computed as topological holonomies of phason displacement waves around scene boundary singularities (`CKMPhasonHolonomy.lean`, `PMNSSeamTopology.lean`).

### BOOK 05: Verification Status and Certificate Discipline
- **Status Classification:** Rigorous stratification of all claims into `CORE-FORMALIZED` (Lean 4, zero axioms), `OPERATOR-SCAFFOLD-CERTIFIED`, `PASSPORT-CLOSED`, and `PROOF-TARGET`.
- **Centralized No-Go Ledger:** Complete catalog of forbidden shortcuts (`D0_NOGO_LEDGER`) — forbidding flat tensors, non-topological selectors, non-quadratic measures, and ad-hoc continuum field substitutions.
- **Phase-Unfolding Theorem:** Proof that irrational $\varphi^{-2}$ phase rotation on discrete lattices generates the exact return modulus $q_T = 44$ and electroweak modulus $q_\mathrm{EW} = 710$ (`PhaseUnfoldingQuasicrystal.lean`).

### BOOK 06: Evolution, Forgetting, and Time
- **The Arrow of Time as a CPTP Channel:** Time direction is the ordering induced by normalized Markovian coarse-graining channels $\hat{\Phi}_N(\rho) = \Phi_N(\rho)/\mathrm{Tr}\Phi_N(\rho)$.
- **Entropy Monotonicity:** Monotone information loss and entropy growth are proved on the finite carrier, providing an irreversible thermodynamic arrow from terminal readout.
- **Seam Fluctuation Relaxation:** Renormalization-group flow and dissipation of boundary defect noise across coarse-graining scales.

### BOOK 07: Gravity Limit and Finite Geometry
- **Noncommutative Spectral Geometry:** Connes spectral triple $(\mathcal{A}, \mathcal{H}, \mathcal{D})$ over the scene complex; discrete Dirac operator $\mathcal{D}$ with Hodge boundary weights (`CanonicalDiracCovariance.lean`).
- **Heat Trace & Einstein–Hilbert Action:** Asymptotic heat trace $\mathrm{Tr}(e^{-t\mathcal{D}^2}) \sim \sum t^{(k-d)/2} a_k$; coefficient $a_2$ recovers the scalar curvature $R - 2\Lambda$ via the Dixmier trace (`ArchiveHeatTrace.lean`, `DixmierTraceBridge.lean`). Higher curvature terms ($R^2, R_{\mu\nu}R^{\mu\nu}$) are exponentially suppressed at the lattice scale.
- **Horizon Emission Law:** A macroscopic horizon is capacity-saturated seam aggregation; horizon emission $F_Q^\mathrm{emit} = Q U^\dagger P U Q \ge 0$ is archive-to-retained boundary leakage under capacity saturation (`HORIZON-EMISSION-LAW`).
- **Quarantined Bridge Interface:** Assumptions of continuum limit existence (`HeatTraceWeyl.lean`, `SmoothInterpolation.lean`) are strictly quarantined in `Bridge/Assumptions/`.

### BOOK 08: Cosmology, Archive, and SDE Transfer
- **Exclusion of Strict $\Lambda\mathrm{CDM}$:** Theorem `LambdaCDMExcluded.lean` proves that $w = -1$ is impossible in an open graph with unitary dissipation; dark energy density must dynamically relax.
- **Cosmological SDE & $w(z)$ Drift:** Vacuum energy evolution obeys a stochastic differential equation (SDE) of phason-archive interaction, predicting a thawing/freezing deviation from $w=-1$ tested against DESI BAO and Planck CMB data (`DarkArchiveTransfer.lean`, `vp_phason_thawing.py`).
- **Sandage–Loeb Redshift Drift:** Cosmic acceleration drift $\dot{v} = c \frac{\dot{z}}{1+z} + \Delta_\mathrm{phason}(z)$ derived from the desynchronization rate between detector and source discrete ticks (`RedshiftExpansionArchiveCoupling.lean`).

### BOOK 09: Gravitational Waves and Quantum Interferometry
- **Apple/Spindle Torus Horizon Geometry:** Binary merger boundary modeled as a finite toroidal readout geometry with two axial release lobes and an equatorial capacity belt.
- **Spin-2 Quadrupole Carrier:** Volume-preserving quadrupole deformations and phason strain tensors on the boundary seam.
- **Horizon Capacity Quantization:** Step-like quantum capacity anomalies in final black hole mass $M_f$ and spin $a_f$ (`BlackHoleCapacityA4.lean`, tested in GWOSC/LIGO MERS_V10 protocols).
- **Epistemic Discovery Guardrails:** Strict prohibition against claiming observational "proof" from current detector noise; pre-registered $5\sigma$ protocols for upcoming observational runs.

---

## 4. The Three Architecture Layers

The repository strictly separates internal theorems, mathematical operators, and external phenomenological passports:

| Layer | Scientific Role | Core Locations | Epistemic Status |
|:------|:----------------|:---------------|:-----------------|
| **I. Epistemic Foundation (Core)** | Conditions of distinguishability, Popperian bootstrap, self-reading functor, finite scene birth | `01_BOOKS/BOOK_00`, `BOOK_01`<br>`03_FORMALIZATION/D0/Foundation/`<br>`03_FORMALIZATION/D0/Core/` | **Lean 4 verified (0 sorry)**.<br>No external physical assumptions. |
| **II. Algebraic Spine** | Operator algebras, top-Hodge rigidity, spectral geometry, No-Go theorems | `01_BOOKS/BOOK_02`, `BOOK_03`<br>`03_FORMALIZATION/D0/Geometry/`<br>`03_FORMALIZATION/D0/Topology/` | **Lean 4 verified**.<br>Continuum bridge assumptions isolated in `Bridge/Assumptions/`. |
| **III. Readout / Phenomenology** | Mass selectors, gauge decompositions, cosmological SDE, empirical stress-tests | `01_BOOKS/BOOK_04`–`BOOK_09`<br>`04_CERTIFICATES/`<br>`05_EXPERIMENTS/` | **Executable Python certificates & observational data**.<br>Passports do not promote core theorems. |

> **Reading Rule:** Do not evaluate Layer III before understanding Layer I. Numerical agreements without the detection contract are merely numbers; their physical meaning exists solely as shadows of the underlying verification structure.

---

## 5. Why This Cannot Be Dismissed Casually

Superficial critics often label the appearance of the golden ratio $\varphi = \frac{1+\sqrt{5}}{2}$ or Lucas numbers as "numerological curve fitting". Within D0, this dismissive response is intellectually invalid:

1. **Global Toral Forcing:** The matrix class of $T = \begin{pmatrix} 0 & 1 \\ 1 & -1 \end{pmatrix}$ is the *unique* unimodular integral class in $\mathrm{GL}_2(\mathbb{Z})$ whose first two returns are sterile ($\#\mathrm{Fix}_1 = \#\mathrm{Fix}_2 = 1$). Orientation-preserving classes ($\det = +1$) have zero integer solutions. Thus, $\varphi$ is the unique non-trapped dynamic memory eigenvalue (`D0-GLOBAL-RETURN-STERILITY-GOLDEN-FORCING-001`).
2. **Step Rigidity:** Constant arithmetic zone step $\Delta$ requires $q = q(q-1)$, which uniquely forces the binary alphabet $q=2$ and $\Delta=2$. Any alphabet $q \ge 3$ causes exponential step blowup (`D0-STEP-TWO-AND-LINE-COUNT-NOGO-001`).
3. **The Asymmetric Burden of Proof (`alternative_burden`):**
   To dispute the foundational layer, a critic cannot simply demand "prove that no other exotic models exist in the universe". Under `D0-POPPERIAN-BOOTSTRAP-001`, any claimed alternative realization that supports a falsifiable killing test **must itself carry the functional tuple** (distinction, retention, comparison, multi-witness, catalogue invariance).

To substantively challenge D0's foundation, an opponent must do one of four concrete things:
- Point out an internal mathematical contradiction in the repair and distinction grammar (`IndependentDetectionRepairGrammar.lean`).
- Construct a non-quadratic probability response law on a finite carrier that preserves measure and unitarity under cyclic independent readout (overcoming `BornAreaPreservationNoGo.lean`).
- Construct an endogenous readout functor that does not factor through the $M_1$ quotient and does not require infinite preparation memory (`PrimitiveMinimalityFromRawFunctor.lean`).
- Exhibit a viable physical alternative that admits a Popperian killing test without satisfying the M1 verification contract.

---

## 6. Non-Trivial Theorems in the Corpus

- **Popperian Bootstrap Equivalence (`D0-POPPERIAN-BOOTSTRAP-001`):** Proof that $\operatorname{KillingTest}(P) \iff \operatorname{VerificationContract}(P)$, turning empirical falsifiability into a constructive mathematical constraint on detector state spaces.
- **Exact Support Orthogonality (`D0-VERIFIABLE-REGISTRATION-ORTHOGONALITY-001`):** An exact verification contract $\operatorname{compare}(x,y) = [x \neq y]$ on physical states forces strictly orthogonal density supports: $\operatorname{supp}(\tau_x) \perp \operatorname{supp}(\tau_y)$. Exact distinguishability cannot be implemented over non-orthogonal states.
- **Top-Hodge Inverse Spectral Rigidity (`D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001`):** Equality of top-Hodge data $(D, H, M_2)$ for positive complete tripartite scenes uniquely forces equality of the unlabelled part-size multisets.
- **Dense Operator Scene Rigidity (`D0-DENSE-OPERATOR-SCENE-RIGIDITY-001`):** Any finite simple rational adjacency matrix on 33 vertices with rank $\le 3$ and $\mathrm{tr}(A^2)=718$ is recovered as the complete tripartite graph $K(9,11,13)$ without assuming partitions, triangles, or connectedness.
- **No-Go on Non-Quadratic Measures (`BornAreaPreservationNoGo`):** Symplectic area preservation on finite state carriers forces power $p=2$, deriving Born's rule from cyclic measurement consistency.
- **Explicit Bridge Quarantine (`D0-BRIDGE-COMPRESSION-001`):** Conjectured continuum limits (such as `HeatTraceWeyl.lean` or `SmoothInterpolation.lean`) are strictly quarantined in `03_FORMALIZATION/D0/Bridge/Assumptions/` and never masquerade as core Lean theorems.

---

## 7. How to Read (Short Paths)

Depending on your background, choose one of three entry paths:

```text
Path A: Foundations & Epistemology (Recommended First Pass)
  └─► BOOK_00 (Entry Contract & Admissibility)
  └─► BOOK_01 (Condensed Foundations & Scene Birth)
  └─► Lean: D0.Foundation.PopperianBootstrap, VerifiabilityNecessity, M1Universality

Path B: Discrete Geometry & Spectral Operators
  └─► BOOK_02 & BOOK_03 (Scene Operators, Graph Rigidity)
  └─► Certificates: vp_spectral_scene_rigidity.py, vp_toral_return_group_origin_of_scene.py
  └─► Lean: D0.Synthesis.DenseOperatorSceneRigidity, D0.Synthesis.TopHodgeInverseSpectralRigidity

Path C: Phenomenology & Stress-Tests (Only after A/B)
  └─► BOOK_04 (Matter Spectrum) & BOOK_08 (Cosmology)
  └─► 05_EXPERIMENTS/ (DESI BAO fitting, LIGO horizon capacity, Sandage-Loeb drift)
  └─► Verification of passports in 02_REGISTRY/claims.csv
```

---

## 8. Canonical Repository Layout & Sources of Truth

```text
01_BOOKS/           Narrative derivation (read BOOK_00 -> BOOK_09)
02_REGISTRY/        Single canonical source of truth for all claims, assumptions, and proofs
03_FORMALIZATION/   Machine-checked Lean 4 library (0 sorry in core)
04_CERTIFICATES/    Self-contained, executable numerical/combinatorial certificates
05_EXPERIMENTS/     Empirical observational passports, pinned survey data, and likelihoods
tools/              Repository validator, Lean view generator, and test runners
```

### Source-of-Truth Rules

- **Books explain; they do not define release status.** Formal claim status and proof ownership are governed strictly by `02_REGISTRY/claims.csv`.
- **Lean ownership is explicit.** `D0.All` and `ClaimMap.lean` are machine-generated from registered claims and audited in CI. Hand edits are rejected.
- **Certificates are reachable evidence.** Every python certificate in `04_CERTIFICATES` must be referenced by an active claim in `claims.csv`.
- **The release tree is immutable under verification.** Executing certificates writes only to temporary `.build/cert_outputs/`; the git working tree remains clean.
- **Empirical results never silently promote a core theorem.** External data comparisons stay in `05_EXPERIMENTS/` as `PASSPORT-CLOSED` or `PROOF-TARGET`.

---

## 9. Local Verification & Reproducibility

### Fast Structural & Integrity Validation

```bash
# Validate CSV registry integrity, imports, and lack of orphan Lean modules
python tools/validate_repo.py

# Verify machine-generated Lean views are up to date
python tools/generate_lean_views.py --check

# Syntax check all certificate scripts
python -m compileall -q tools 04_CERTIFICATES
```

### Running Executable Certificates

```bash
# Run the fast suite of registered mathematical certificates (timeout 90s)
python tools/run_registered_certs.py --timeout 90 --exclude vp_scene_bartholdi_typed.py

# Run the intensive Bartholdi scene certificate separately
python 04_CERTIFICATES/vp_scene_bartholdi_typed.py
```

### Formal Lean 4 Build

```bash
cd 03_FORMALIZATION
lake build D0.All
```

*(The Lean toolchain version is pinned in `03_FORMALIZATION/lean-toolchain`)*.

---

## 10. Epistemic Guardrails (What D0 Is Not Claiming)

To maintain scientific integrity, D0 explicitly records what has **not** been achieved:

- **Continuum Limit as Theorem:** D0 does **not** claim that the Einstein–Hilbert action or smooth Yang–Mills theory has been proved as an unconditional mathematical theorem from the graph. They are conditioned on explicitly quarantined bridge assumptions (`HeatTraceWeyl`, `SmoothInterpolation`).
- **Empirical Confirmation:** D0 does **not** claim that observational hints (e.g. DESI $w(z)$ dynamical dark energy or LIGO black hole horizon step features) constitute verified empirical discoveries. They are structured, pre-registered falsification tests.
- **Universal Metaphysical Uniqueness:** D0 does **not** claim that no other mathematical universe could ever be conceived. It claims that *within the regime of finite, catalogue-free, endogenous verifiability*, the canonical scene and functional tuple are mathematically forced.

---

## Citation & Status

D0 is an open, actively developed research corpus. The state of any claim is determined by the registry, not by narrative prose.

```text
Repository: https://github.com/gvakhrushev/d0_15
Registry:   02_REGISTRY/claims.csv
Contact:    grigorijvahrusev@gmail.com
```
