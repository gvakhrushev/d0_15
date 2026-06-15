# D0 formalization asset map (Iter-18) — reuse existing math, don't reinvent

Method: mined all 10 books for the external mathematical theories D0 *synthesizes from* (**307 anchors,
277 distinct theory clusters**), then mapped the top 26 + the 19 ledger assumptions to existing
formalization — our pinned Mathlib, the wider Lean ecosystem, or not-yet — so closures reuse work
instead of reinventing it (36-agent workflow). This is the answer to "what else can close the
formalization" beyond condensed math, and it is grounded in what the books actually cite (e.g. the
§04.2 "theorem owners used by this book" table, §02.K K-theory gap-labeling, §01.21 the φ-network).

## Headline — the earlier "external owner" picture was too pessimistic
The pinned Mathlib has grown: it now carries **differential-geometry connections (covariant
derivatives, torsion, parallel transport), Riemannian manifolds, Delone sets / aperiodic order,
condensed math / profinite, quadratic Galois theory, Lie/Killing forms, spectral graph Laplacians,
and braided monoidal categories**. Several D0 gaps the Lean-only audit filed under "external owner"
are in fact **formalizable from the pin today**.

---

## ✅ READY_IN_PIN — formalizable now, no new dependency (5 clusters)

| theory | Mathlib pin | D0 gap it closes | action |
|---|---|---|---|
| **Quadratic Galois theory** | `FieldTheory/Galois/Basic` (`IsQuadraticExtension.isGalois/isCyclic`), `FieldTheory/Fixed` | the φ↔ψ Galois pair: `D0-Z2-SPINOR-COVER-001` `galois_z2_order_two` (currently a `decide` stub), Vieta §02.34, §01.14 φ-rigidity | replace the decide-stub with real `Gal(ℚ(√5)/ℚ)` = ℤ₂ on `x²−x−1` |
| **Spectral graph theory (normalized Laplacian)** | `Combinatorics/SimpleGraph/LapMatrix`, `AdjMatrix`; `LinearAlgebra/Eigenspace`; `Analysis/InnerProductSpace/Spectrum` | §04.2 the `1⊕30⊕(1+1)` split of `L_sym(K(9,11,13))`; the two **active eigenvalues** flagged "numerical, do not cite" are roots of `160λ²−480λ+359` ⇒ exact quadratic surds | promote the active eigenvalues from numeric to **exact algebraic theorem**; ground the 30-fold band in `lapMatrix` rank |
| **Differential-geometry connections** | `Geometry/Manifold/VectorBundle/CovariantDerivative.{Basic,Torsion}`, `…/Tangent`, `Riemannian.Basic` | `D0-ARCHIVE-BIANCHI-001`, `D0-SMOOTH-001` holonomy/parallel-transport (§02.41, §07/§08.35) | port the Bianchi/holonomy content onto Mathlib connections instead of `:= {…}` structural stubs |
| **Condensed math / profinite** | `Condensed.*`, `Topology/Category/Profinite.AsLimit`, `LightProfinite.*` | `archive_tower_defines_profinite_object : True` (§ArchiveTower); the no-hidden-points THE 01.4.0 (PROOF-TARGET); the cut-project support | build the `ℕᵒᵖ ⥤ FintypeCat` limit → real `LightProfinite` (replaces the `: True`) |
| **Linear algebra / spectral decomposition** | `LinearAlgebra/Eigenspace/*`, `Matrix/Spectrum`, `InnerProductSpace/Spectrum` | scene-operator eigen-analysis §04.2/§04.4 generally | instantiate Mathlib spectral theory on the concrete scene operators |

---

## ➕ PORTABLE_NEEDS_DEP — Lean-formalized (often partly in pin), needs a bridge/dep (10)

- **Cut-and-project / Meyer / Delone sets** → `Analysis/AperiodicOrder/Delone/Basic` is **in the pin**.
  Closes the tiling-hull cut-project (`D0-HULL-001`, §02.34, §04.4): import `Delone`, write a Meyer-set
  closure cert, keep the D0 hull modules as the D0-side anchor.
- **Aperiodic order / Sturmian / symbolic dynamics** → `Analysis/AperiodicOrder/Delone`,
  `Dynamics/SymbolicDynamics/Basic` (shift spaces) in pin — the Fibonacci/Sturmian (§05.8) + golden-mean
  SFT (the I_f closure) can sit on real shift-space machinery.
- **TQFT / fusion categories (Fibonacci)** → `CategoryTheory/Monoidal/{Braided,Rigid,Symmetric}` in pin
  — a `Fusion` module would deepen `D0-FIBONACCI-IF-FORCING-001` (the fusion-matrix side) beyond the
  cert.
- **Open quantum systems / CPTP (forgetting map)** → `Analysis/CStarAlgebra/CompletelyPositiveMap` in
  pin — bundle a trace-preserving CPTP channel type to back "forgetting = CPTP decoherence".
- **Quantum measurement / Born / Gleason** → `VonNeumannAlgebra/Basic`, `CStarAlgebra/Projection` in
  pin — write a Gleason-on-PVM module for `D0-GLEASON-LOOPHOLE-CLOSURE`.
- **Gauge theory / Lie reps / Killing** → `Algebra/Lie/*` (65 modules incl. `Killing.lean`) in pin —
  **directly closes `ASSUMP-COMPACT-LIE-KILLING-NEGATIVE`** (the audit's "should-be-internal" flag).
- **Einstein–Hilbert / GR** → `Geometry/Manifold/Riemannian.*` in pin — conditional bridge module for
  the EH interface (`D0-GEOM-HEAT-TRACE-A2-DECOMP-001`).
- **Algebraic topology (genus, homology, π₁(T²)=ℤ²)** → `AlgebraicTopology/*` in pin — §03.23.
- **Braid groups** → `CategoryTheory/Monoidal/Braided` + `FreeGroup` quotient — braid-valence gauge
  forcing (THE 04.6.M1.gauge).
- **K-theory gap-labeling (Bellissard)** → C*-basics in pin, but the **Bellissard K₀-trace identity is
  NOT formalized anywhere** → keep external owner (record `ASSUMP-BELLISSARD-K0-TRACE`); D0's finite
  shadow (`countable gap labels`) stays the D0-side.

---

## 🛠 NEEDS_NEW_FORMALIZATION (6)
- **Pisot numbers / Sturmian substitutions** — not in Mathlib (foundations `NumberField.Norm`,
  `Minpoly` exist); `D0-PISOT-CONTRACTION-TIME-ARROW` (§06.36) would need a new `PisotNumbers` module
  (algebraic integer with all conjugates `|·|<1`). High value (the time-arrow), medium effort.
- **Tomita–Takesaki modular theory** — only `VonNeumannAlgebra/Basic` in pin; **partial in Mathlib
  2026 (Tanimoto `StandardSubspace`)** — extendable later; keep `ASSUMP-TOMITA-TAKESAKI` for now.
- **Heat-kernel expansion / spectral action** — `InnerProductSpace/Laplacian` in pin but no Seeley–
  DeWitt expansion → keep external owner; D0's finite spectral-action stubs stay finite.
- **Noether's theorem (finite cochain Ward)** — formalizable internally with diff-forms/Lie-derivative.
- **RG / Wilsonian EFT** — keep `ASSUMP-RG-SMOOTH-INTERP` (continuum limit, external).
- **Kolmogorov / Solomonoff (M1 ground)** — `Computability` in pin but no algorithmic-complexity layer
  → keep `ASSUMP-M1-KOLMOGOROV`/`SOLOMONOFF` external.

---

## 🌐 STAYS_EXTERNAL_OWNER — genuinely beyond current formalization (correct as honest bridges) (5)
Operational QM reconstruction (Hardy/Masanes–Müller), Jones subfactor *obstruction*, QM experimental
no-go (Renou et al.), Bekenstein/Jacobson horizon thermodynamics, Wilson lattice-gauge continuum
limit. D0 already records all five as `BRIDGE-ASSUMPTIONS-EXPLICIT` owner-edges — keep as-is.

---

## Prioritized reuse plan (highest value × READY_IN_PIN first)
1. **Lie/Killing → close `ASSUMP-COMPACT-LIE-KILLING-NEGATIVE` internally** (`Algebra/Lie/Killing`).
   Removes a questionable ledger assumption with a real Mathlib proof. Clean, high-value.
2. **Quadratic Galois → upgrade `D0-Z2-SPINOR-COVER-001` `galois_z2_order_two`** from `decide`-stub to
   real `Gal(ℚ(√5)/ℚ)≅ℤ₂` on `x²−x−1`. Foundational φ↔ψ pair.
3. **Spectral graph Laplacian → promote the §04.2 active eigenvalues** from "numerical, do not cite" to
   exact quadratic-surd theorems (roots of `160λ²−480λ+359`) + ground the 30-band in `lapMatrix` rank.
4. **Condensed/profinite → real `archive_tower_defines_profinite_object`** via `LightProfinite`/
   `Profinite.AsLimit` (replaces the `: True` marker).
5. **Delone/aperiodic order → the tiling-hull cut-project** (`D0-HULL-001`) on `AperiodicOrder/Delone`.
6. **Differential-geometry connections → Bianchi/holonomy** onto Mathlib `CovariantDerivative` (retire
   the `:= {…}` structural stubs in the Gravity interface).

Items 1–3 are the cleanest first wave (decidable/algebraic, small, each removes a flagged weakness).
Items 4–6 are larger (categorical / manifold API) but use real Mathlib. Everything in NEEDS_NEW /
STAYS_EXTERNAL is honestly out of reach now and correctly recorded as owner-edges or proof-targets.
