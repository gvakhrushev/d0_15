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
3. **Endogenous Scene Genesis:** Independent line filling, toral return sterility in $\mathrm{GL}_2(\mathbb{Z})$, and minimal zone capacity uniquely weld the parameters $(|\mathrm{Role}|, \Delta, |\Omega_8|, m, q_T) = (4, 2, 8, 11, 44)$ into the bipartite/tripartite scene $K(9,11,13)$ with $N=33$ and collision invariant $P_2 = 371/1089$.
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

## 3. The Three Layers

The repository strictly separates internal theorems, mathematical operators, and external phenomenological passports:

| Layer | Scientific Role | Core Locations | Epistemic Status |
|:------|:----------------|:---------------|:-----------------|
| **I. Epistemic Foundation (Core)** | Conditions of distinguishability, Popperian bootstrap, self-reading functor, finite scene birth | `01_BOOKS/BOOK_00`, `BOOK_01`<br>`03_FORMALIZATION/D0/Foundation/`<br>`03_FORMALIZATION/D0/Core/` | **Lean 4 verified (0 sorry)**.<br>No external physical assumptions. |
| **II. Algebraic Spine** | Operator algebras, top-Hodge rigidity, spectral geometry, No-Go theorems | `01_BOOKS/BOOK_02`, `BOOK_03`<br>`03_FORMALIZATION/D0/Geometry/`<br>`03_FORMALIZATION/D0/Topology/` | **Lean 4 verified**.<br>Continuum bridge assumptions isolated in `Bridge/Assumptions/`. |
| **III. Readout / Phenomenology** | Mass selectors, gauge decompositions, cosmological SDE, empirical stress-tests | `01_BOOKS/BOOK_04`–`BOOK_08`<br>`04_CERTIFICATES/`<br>`05_EXPERIMENTS/` | **Executable Python certificates & observational data**.<br>Passports do not promote core theorems. |

> **Reading Rule:** Do not evaluate Layer III before understanding Layer I. Numerical agreements without the detection contract are merely numbers; their physical meaning exists solely as shadows of the underlying verification structure.

---

## 4. Why This Cannot Be Dismissed Casually

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

## 5. Non-Trivial Theorems in the Corpus

- **Popperian Bootstrap Equivalence (`D0-POPPERIAN-BOOTSTRAP-001`):** Proof that $\operatorname{KillingTest}(P) \iff \operatorname{VerificationContract}(P)$, turning empirical falsifiability into a constructive mathematical constraint on detector state spaces.
- **Exact Support Orthogonality (`D0-VERIFIABLE-REGISTRATION-ORTHOGONALITY-001`):** An exact verification contract $\operatorname{compare}(x,y) = [x \neq y]$ on physical states forces strictly orthogonal density supports: $\operatorname{supp}(\tau_x) \perp \operatorname{supp}(\tau_y)$. Exact distinguishability cannot be implemented over non-orthogonal states.
- **Top-Hodge Inverse Spectral Rigidity (`D0-TOP-HODGE-INVERSE-SPECTRAL-RIGIDITY-001`):** Equality of top-Hodge data $(D, H, M_2)$ for positive complete tripartite scenes uniquely forces equality of the unlabelled part-size multisets.
- **Dense Operator Scene Rigidity (`D0-DENSE-OPERATOR-SCENE-RIGIDITY-001`):** Any finite simple rational adjacency matrix on 33 vertices with rank $\le 3$ and $\mathrm{tr}(A^2)=718$ is recovered as the complete tripartite graph $K(9,11,13)$ without assuming partitions, triangles, or connectedness.
- **No-Go on Non-Quadratic Measures (`BornAreaPreservationNoGo`):** Symplectic area preservation on finite state carriers forces power $p=2$, deriving Born's rule from cyclic measurement consistency.
- **Explicit Bridge Quarantine (`D0-BRIDGE-COMPRESSION-001`):** Conjectured continuum limits (such as `HeatTraceWeyl.lean` or `SmoothInterpolation.lean`) are strictly quarantined in `03_FORMALIZATION/D0/Bridge/Assumptions/` and never masquerade as core Lean theorems.

---

## 6. How to Read (Short Paths)

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

## 7. Canonical Repository Layout & Sources of Truth

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

## 8. Local Verification & Reproducibility

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

## 9. Epistemic Guardrails (What D0 Is Not Claiming)

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
