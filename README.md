# D0 — Finite Verification Theory

> **How can a closed finite system produce reproducible facts without an external classical observer?**

D0 is a mathematical and physical research programme that inverts the traditional foundational order: instead of postulating a smooth space-time continuum, background fields, and an external measuring apparatus, D0 begins from the **operational preconditions of verifiable detection** inside a closed finite system.

Discrete scene structure, registration channels, and (conditionally) continuum limits are derived as consequences of this operational contract. High-energy spectra, gauge structures, and cosmological evolutions are downstream readouts, not independent starting hypotheses.

---

## Table of Contents

- [1. The Core Inversion (Read This First)](#1-the-core-inversion-read-this-first)
  - [The Foundational Premise](#the-foundational-premise)
- [2. Architecture & Flow of Forcing](#2-architecture--flow-of-forcing)
- [3. The 10-Book Derivation Chain (From Admissibility to Interferometry)](#3-the-10-book-derivation-chain-from-admissibility-to-interferometry)
  - [BOOK 00: Entry Contract and Admissibility](#book-00-entry-contract-and-admissibility)
  - [BOOK 01: Condensed Foundations and Graph Birth](#book-01-condensed-foundations-and-graph-birth)
  - [BOOK 02: Mathematical Proof Spine and Invariant Calculus](#book-02-mathematical-proof-spine-and-invariant-calculus)
  - [BOOK 03: Finite Action Operators and Scene Dynamics](#book-03-finite-action-operators-and-scene-dynamics)
  - [BOOK 04: Spectrum, Matter, and Finite Selector Theory](#book-04-spectrum-matter-and-finite-selector-theory)
  - [BOOK 05: Verification Status and Certificate Discipline](#book-05-verification-status-and-certificate-discipline)
  - [BOOK 06: Evolution, Forgetting, and Time](#book-06-evolution-forgetting-and-time)
  - [BOOK 07: Gravity Limit and Finite Geometry](#book-07-gravity-limit-and-finite-geometry)
  - [BOOK 08: Cosmology, Archive, and SDE Transfer](#book-08-cosmology-archive-and-sde-transfer)
  - [BOOK 09: Gravitational Waves and Quantum Interferometry](#book-09-gravitational-waves-and-quantum-interferometry)
- [4. The Three Architecture Layers](#4-the-three-architecture-layers)
- [5. Spectral Rigidity: The Golden Ratio φ and Zero-Parameter Mass Sectors](#5-spectral-rigidity-the-golden-ratio-varphi-and-zero-parameter-mass-sectors)
  - [Audited Mathematical Routes to φ](#audited-mathematical-routes-to-varphi)
  - [Scientific Falsifiability](#scientific-falsifiability)
- [6. Non-Trivial Theorems in the Corpus](#6-non-trivial-theorems-in-the-corpus)
- [7. How to Read (Short Paths)](#7-how-to-read-short-paths)
- [8. Canonical Repository Layout & Sources of Truth](#8-canonical-repository-layout--sources-of-truth)
  - [Source-of-Truth Rules](#source-of-truth-rules)
- [9. Local Verification & Reproducibility](#9-local-verification--reproducibility)
- [10. Epistemic Guardrails & Frontier Resolution Strategy](#10-epistemic-guardrails--frontier-resolution-strategy)
- [Citation & Status](#citation--status)

---

## 1. The Core Inversion (Read This First)

Standard physics proceeds from geometry to observation:
$$\text{Smooth Space-Time } \mathcal{M} \;\longrightarrow\; \text{Lagrangian / Fields } \psi \;\longrightarrow\; \text{External Measurement / Projection}$$

D0 inverts this hierarchy:
$$\text{Verifiability Contract (M1)} \;\longrightarrow\; \text{Functional Tuple} \;\longrightarrow\; \text{Finite Scene } K(9,11,13) \;\longrightarrow\; \text{Readout Spectrum}$$

### The Foundational Premise

> Any process claiming to produce objectively reproducible distinctions between independent runs must already possess the internal means of **distinction**, **retention**, and **independent comparison** — and cannot outsource these operations to an obligatory external catalogue.

Within the repository's **currently formalized admissibility architecture** (the M1 condition + finite realizability), the programme derives the following registered results. These premises do not classify every finite catalogue-free carrier: a killing test also exists for a three-line protocol and for a protocol whose record type has an unused coordinate (`M1-UNIVERSALITY-COUNTEREXAMPLE`).

1. **The Functional Tuple:** distinction ($x \neq y$), persistent record ($x \mapsto \text{rec}(x)$ injective), and independent comparison lines ($l_0 \neq l_1$) are forced as the minimal requirements for empirical verifiability.
2. **The Popperian Bootstrap (`D0-POPPERIAN-BOOTSTRAP-001`):** A theory can be falsified by a "killing test" if and only if it admits a verification contract ($\text{KillingTest}(P) \iff \text{VerificationContract}(P)$). The bare possibility of refutation strictly forces the entire functional tuple. Solitary-witness systems are non-falsifiable. The tuple does not fix the carrier: `Bool` is not equivalent to `Fin 3`, and a record type may contain an unused coordinate.
3. **Endogenous Scene Genesis (inside the registered forcing architecture):** Independent line filling, toral return sterility in $\mathrm{GL}_2(\mathbb{Z})$, and minimal zone capacity weld the parameters $(|\mathrm{Role}|, \Delta, |\Omega_8|, m, q_T) = (4, 2, 8, 11, 44)$ into the tripartite scene $K(9,11,13)$ with $N=33$ and collision invariant $P_2 = 371/1089$. This is a strong internal uniqueness statement inside that forcing architecture. It is not a classification of every contract carrier.
4. **Quadratic Born readout inside the phase-response class:** the finite response is quadratic, and uniqueness of the phase quadratic is owned under quarter-turn phase blindness (`QuarterTurnInvariant`). Generic symplectic-area preservation alone is explicitly **insufficient** (`BornAreaPreservationNoGo`).

The registered functional-tuple and scene-forcing results are developed in **BOOK_00** and **BOOK_01** and formalized in Lean 4 within their stated candidate/admissibility classes. The external-review P1 lane audits the stronger completeness claim rather than treating it as already proved. Everything downstream builds on the registered finite architecture, not on an unqualified universal-classification assertion.

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
  - Top-Hodge inverse rigidity    - Frozen SM factor/Weyl ledger + representation target
  - Commutant AF-algebra tower    - Puiseux mass-hierarchy passports
  - Discrete Dirac & Laplacians   - CKM/PMNS phason-holonomy passports
  - Isolated bridge assumptions   - Conditional dark-EOS / cosmology passports
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
[ BOOK 04: Matter Resonance, Frozen SM Ledger, Gauge-Representation Target, Puiseux Passports ]
                 │
                 ▼
[ BOOK 05: Verification Audit & Centralized No-Go Ledger ]
                 │
                 ▼
[ BOOK 06: Markov Forgetting Channels, Entropy Monotonicity & Arrow of Time ]
                 │
                 ▼
[ BOOK 07: Finite/Spectral Gravity Operators, Quarantined EH Bridge, Horizons ]
                 │
                 ▼
[ BOOK 08: Conditional Dark-EOS/Cosmology Passports, SDE Tests, DESI Drift ]
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
- **Discrete Time (The Tick):** Physical time is generated by cyclic phase transitions (`FixedDetectorTimeLadder.lean`, `PhaseTower.lean`). The witnesshalting theorem (`WitnessHalting.lean`) guarantees finite termination of measurement cycles.
- **Homology & Hodge Spectrum:** Exact rings $H_0, H_1, H_2$ (`GenericTripartiteHomology.lean`) and top-Hodge Laplacian spectra (`GenericTripartiteTopHodgeSpectrum.lean`) fix the channel capacity Euler characteristic $\chi = |V| - |E| + |F|$.

PLACEHOLDER_ABORT
