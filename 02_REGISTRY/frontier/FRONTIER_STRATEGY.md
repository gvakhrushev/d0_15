# D0 Frontier Strategy: Resolving the Interface Crisis

> **Current semantic/remediation roadmap:** [REVIEW_REMEDIATION_ROADMAP.md](REVIEW_REMEDIATION_ROADMAP.md).  It records the external-review repairs, universal-carrier and gauge-representation research lanes, and the rule that public prose may not exceed literal owner strength.

> **HISTORICAL EXPLORATION — NOT THE ACTIVE DEFINITION OF DONE.**  This document
> records an earlier research strategy and intentionally contains conjectural positive
> routes.  It must not be read as saying that the four vectors below are current
> load-bearing blockers or already-proved replacements for registered NO-GOs.
> The authoritative closure rule is [CLOSURE_CONTRACT.md](CLOSURE_CONTRACT.md):
> a proved NO-GO or explicit BRIDGE/PASSPORT is terminal, and optional continuation
> does not count against theory closure.

> **The four remaining hard frontiers of D0 do not represent incompleteness in the discrete operator core; they represent the crisis of the interface between an endogenous discrete system and legacy continuum language.**

A superficial reading of the project's open boundaries treats them as "gaps on the road to a smooth field theory." In truth, the development path of D0 is not to stretch the discrete skeleton into classical continuous equations, but to **systematically dismantle the remaining continuum crutches** within the formalism.

---

## 1. Architectural Diagnosis of the Four Frontiers

| Frontier & Target | Orthodox / Continuum Reading | Endogenous D0 Reality |
|:------------------|:-----------------------------|:----------------------|
| **1. AlphaDixmierFrontier**<br>`AlphaProfiniteTowerNoGo`<br>`DeltaAlphaNormalizationNoGo` | Dixmier trace cannot be normalized on a projective tower without external Feshbach cutoff. | Artificial attempt to impose continuous scale integrals onto a discrete projective tower of profinite sets. |
| **2. Metric Scale Underdetermination**<br>`MassSectorMetricUnderdetermination`<br>`RedshiftSITickCalibrationNoGo` | Scene algebra yields only dimensionless eigenvalue ratios; absolute eV/SI mass scale requires external calibration. | Conflation of the detector's endogenous discrete information capacity with historically contingent external SI artifacts. |
| **3. Smooth Interpolation Bridge**<br>`Bridge/Assumptions/SmoothInterpolation` | Lack of a proven isomorphism between the graph Laplacian on $K(9,11,13)$ and the Laplace–Beltrami operator on $\mathcal{M}$. | **Redundant concession to the continuum:** trying to prove diffeomorphism to a smooth manifold where Rieffel spectral convergence suffices. |
| **4. CMB SDE Smoothing Ambiguity**<br>`CMBNsSmoothingUndeterminedNoGo` | Spectral tilt $n_s$ depends on the chosen continuous smoothing kernel $\sigma$ under stochastic relaxation. | Artificially convolving purely combinatorial graph spectra with continuous spatial kernels to match angular multipoles $\ell$. |

---

## 2. Four Strategic Vectors of Resolution

### Vector 1. Closing the Dixmier Trace via Fibonacci $AF$-Algebras and the Perron–Frobenius Tower
*Instead of seeking an external regulator for projective limits of sets, the tower must be cast as an inductive limit of $C^*$-algebras.*

- **Problem:** `DixmierFeshbachFiniteHeatTrace.lean` arises because the Dixmier trace is applied over an infinite-dimensional Hilbert space where each discrete level requires an ad-hoc normalization weight.
- **Solution:** Transition to the Fibonacci $AF$-algebra (already prepared in `D0/VNext/FibonacciAFAlgebra.lean` and `PerronGNSTower.lean`). An inductive limit of finite-dimensional $C^*$-algebras with Bratteli transition matrix $\begin{pmatrix} 1 & 1 \\ 1 & 0 \end{pmatrix}$ possesses a **unique canonical tracial state**.
- **Result:** Each level's weight is strictly governed by the maximal Perron–Frobenius eigenvector component, scaling exactly as $\varphi^{-k}$. This dissolves `AlphaProfiniteTowerNoGo.lean`: the Cesàro residue is normalized by the internal trace state of the $AF$-algebra without external cutoff scales.

### Vector 2. Endogenous Scale Calibration via Information Capacity Saturation
*Absolute energy scale emerges not from arbitrary meters or seconds, but from the saturation limit of discrete detector memory.*

- **Bremermann–Bekenstein Bound:** Modules `PreparationMemoryBound.lean` and `CapacityRawScene.lean` prove that an endogenous detector has a finite distinguishability capacity per discrete tick.
- **Dimensionless Action Quantum:** Instead of fitting electron mass in grams or eV, calibration is defined by fixing the fundamental action quantum per tick:
  $$S_{\mathrm{min}} = \frac{1}{2} \hbar_{\mathrm{endogenous}} \equiv 1$$
- **Resolution:** The mass sector is calibrated through the ratio of the scene's total topological capacity to the elementary entropy dissipation step of the archive (`LogdetSecondResponse.lean`, `ArchiveVolumeBounds.lean`). Energy is local edge-tension density relative to the detector's information boundary, not an extrinsic dimensional constant.

### Vector 3. Eliminating `SmoothInterpolation.lean`: Rieffel Quantum Metric Spaces
*The attempt to prove that a discrete graph "becomes" a smooth $C^\infty$ manifold is mathematically misguided and physically unnecessary.*

- **From Riemannian Manifolds to CQMS:** In Connes' noncommutative geometry, a smooth manifold is merely a special commutative case of a Compact Quantum Metric Space (CQMS). The apparatus is already present in `D0/Bridge/RieffelGHPBridge.lean`.
- **Dismantling the Axiom:** Instead of postulating an ad-hoc diffeomorphism (`SmoothInterpolation.lean`), the theory proves convergence of the sequence of graph spectral triples $(\mathcal{A}_n, \mathcal{H}_n, \mathcal{D}_n)$ in the quantum Gromov–Hausdorff distance (Rieffel propinquity):
  $$\operatorname{dist}_{\mathrm{QGH}}\big((\mathcal{A}_n, \mathcal{D}_n), (\mathcal{A}_\infty, \mathcal{D}_\infty)\big) \longrightarrow 0 \quad \text{as } n \to \infty$$
- **Result:** The Einstein–Hilbert action is generated directly by the Chamseddine–Connes spectral action on $\mathcal{D}_\infty$. The smooth manifold is entirely bypassed as an ontological intermediary.

### Vector 4. Spectral Algebraicization of Cosmological SDE (Fiedler Projectors)
*Replace continuous spatial kernel convolutions with canonical spectral Hodge projectors.*

- **The Kernel Artifact:** `CMBNsSmoothingUndeterminedNoGo.lean` shows that convolving discrete archive relaxation noise with a continuous Gaussian kernel introduces unphysical dependence on the kernel width $\sigma$.
- **Canonical Projection via the Fiedler Vector:** In `CMBFiedlerFreezeout.lean`, the lowest non-trivial relaxation mode of the graph is proved to be discrete and unique. Continuous smoothing is replaced by a spectral projector onto graph Laplacian eigenspaces $\lambda \le \lambda_{\mathrm{Fiedler}}$.
- **Result:** Cosmological perturbations become invariant under coordinate interpolations: the spectral index $n_s$ is fixed by the combinatorial ratio of Hodge projector ranks.

---

## 3. Structural Refactoring Roadmap

```text
[ 02_REGISTRY ]
      │
      ├─► Update no_go_atlas.md: document continuum-interface boundaries
      ├─► Close paths in forcing_routes.json via inductive AF-algebra traces
      └─► Reclassify closure_frontier.csv lanes from external passports to core algebraic limits

[ 03_FORMALIZATION ]
      │
      ├─► [ Core Promotion of VNext / VNext2 ]:
      │      * Promote FibonacciAFAlgebra and PerronGNSTower to D0/Algebra/
      │      * Promote CanonicalDiracCovariance to D0/Geometry/
      │
      ├─► [ Bridge Demolition ]:
      │      * RETIRE: SmoothInterpolation.lean (superseded by RieffelGHPBridge.lean)
      │      * RESOLVE: AlphaProfiniteTowerNoGo (closed via AF tracial state)
      │
      └─► [ Scale Foundation in D0/Foundation/ ]:
             * Formalize endogenous action quantum S_min = 1
             * Link mass ratios directly to capacity saturation bounds
```

---

## 4. Active Search Architecture: Select Before You Build

This section is an **operational research method**, not a scientific claim and
not a replacement for `CLOSURE_CONTRACT.md`.

The current frontier is no longer served well by accumulating candidate
structures and formalizing them one by one. New lanes should use a selective
search architecture.

### 4.1 KILL-FIRST gates

A candidate progresses only while it survives:

```text
TYPE
→ REPRESENTATION / Hom-space
→ SYMMETRY
→ MODULI DIMENSION
→ FLAT LIMIT
→ VARIATION
→ GAUGE / CONSTRAINT QUOTIENT
→ EXACT FINITE SPECTRUM
→ PHYSICAL INTERPRETATION
```

A failure at an early gate terminates that branch. Do not pay for later
research/Lean work on a candidate already killed by typing, representation
theory, or symmetry.

### 4.2 Backward mathematics before forward guessing

Prefer established classification mathematics, invariant theory, representation
theory, cohomology, spectral theory, and exact finite normal forms to blind
forward construction.

The admissible backward question is:

> What mathematical structure would be necessary for the target phenomenon, and
> which of those structures are already owned or forced by D0?

The forbidden shortcut is importing the desired physical equation as an axiom.

### 4.3 Do not confuse action freedom with physical freedom

Track three different dimensions:

[
d_A=dim(mathcal A_{mathrm{action}}),
qquad
d_E=dim(mathcal A_{mathrm{EL}}),
qquad
d_P=dim(mathcal A_{mathrm{physical}}).
]

Here (d_E) is counted after deriving independent Euler--Lagrange equations,
and (d_P) after gauge reduction, algebraic constraints, and elimination of
auxiliary fields.

A selector is not required merely because (d_A>1). First test whether

[
d_A>d_E
quad	ext{or}quad
d_E>d_P.
]

In particular, a multi-parameter first-order action family may collapse to a
unique physical operator after connection elimination. The selector question is
therefore asked at the **latest level where the parameter still changes
physical output**.

### 4.4 Classify once, specialize late

When a finite invariant space has basis (T_1,ldots,T_n), write the generic
object

[
T(alpha)=sum_i alpha_i T_i
]

and carry (alpha) through variation, quotient, and spectrum.

Do not create separate theory/Lean branches for each numerical choice of
(alpha) unless the generic theorem has already shown that specialization is
mathematically meaningful.

### 4.5 Search engine versus proof boundary

Use exact Python/rational certificates for:

- rank/nullity;
- commutants and invariant Hom-spaces;
- finite Fourier symbols;
- Schur complements/range checks;
- hostile witnesses and mutations;
- rapid enumeration of finite candidate families.

Use Lean for the surviving universal statement:

- typing;
- equivariance;
- classification theorem;
- exact quotient/no-go;
- parameterized variation identity;
- theorem that a physical operator is or is not parameter-independent.

The intended loop is:

```text
known mathematics
→ reverse target fingerprint
→ invariant/Hom classification
→ finite candidate basis
→ exact hostile certificates
→ generic parameter family
→ variation
→ gauge/constraint quotient
→ physical Hessian
→ only then ask for a selector
→ Lean owner for the surviving theorem
```

This is the default strategy for new frontier work unless a CONTROL task
explicitly justifies a different search mode.

