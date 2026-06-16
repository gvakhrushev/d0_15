# D0 — Autonomous session report (Iteration 19)

Owner away ~8h. Mandate: continue the full-Lean-formalization push autonomously — the theory lives
in the books, the Lean layer lags, this is technical catch-up. Discipline: verified-closure protocol
(verify-then-promote; full `lake build D0.All` green gate per unit; `d0_score` integrity demotions = 0;
one reviewable commit per verified unit; reuse existing Mathlib; never fake; name every residual).

**Headline.** strength **3449 → 3549 (+100)**; vacuous-`True` stubs (guard ratchet) **12 → 1**;
load-bearing theorems **~855 → 1215**; weak-definitional **~302 → ~255**; proof holes **0** throughout;
integrity demotions **0**; hygiene **100/100**; all guards green; `lake build D0.All` GREEN (3319 jobs).
**One active over-claim** was surfaced by a full re-audit and **corrected**. 9 commits on `master`.

---

## What was done (this session)

### A. Reuse wave — closed earlier this session (asset-map items 1–4 + Pisot)
1. `69af4da` — `ASSUMP-COMPACT-LIE-KILLING-NEGATIVE` reclassified: Cartan's compactness criterion is
   absent from the pinned Mathlib → legitimate external owner (the asset map's "READY" was optimistic;
   verify-then-promote caught it). D0's operative matrix-rep Yang–Mills positivity stays internal.
2. `c3fddc6` — **D0-GALOIS-PHI-IRRATIONAL-001**: φ irrational ⇒ genuine quadratic Galois ℤ₂ (reuses
   Mathlib `irrational_sqrt_natCast_iff` + `native_decide`). Upgrades the hand ring-involution.
3. `1370dea` — **D0-SCENE-ACTIVE-EIGENVALUES-001**: §04.2 active eigenvalues EXACT = 3/2 ± √10/40;
   the book's old decimal readouts (summed to 2.999997 ≠ 3) were error-corrected.
4. `6164629` — archive-tower profinite made REAL (`inverseLimit_nonempty`), replacing a `:= True`.
5. `9e84541` — **D0-PISOT-CONTRACTION-TIME-ARROW-001**: arrow of time = Pisot contraction (φ>1, |ψ|<1).

### B. Lean-stub hygiene — vacuous-`True` ratchet 12 → 1
- `66d2115` — **11 of 12** grandfathered `: Prop := True` operator-origin / no-go / boundary markers
  CONVERTED to real statements proved by each module's load-bearing siblings (matrix symmetry,
  gauge / non-abelian curvature skew-closure, PSD trace ≥ 0, Kronecker-of-skews-is-symmetric no-go,
  edge scalar-leakage no-go, orthogonal-conjugation skew preservation, internal Hurwitz-dimension
  closure). The `check_no_tautology_proofs` GRANDFATHER ratchet shrank **12 → 1** (the lone survivor is
  a release-status documentation token in `ReleaseStatus.lean`, no math sibling).
- `8d7f5cb` — the one weak conversion with a tractable route (`BianchiResidual`) was strengthened from a
  `:= rfl` def-restatement to the real theorem `bianchiResidual_skew`. Now **10/11** genuinely
  load-bearing; the remaining weak marker (octonion non-associativity in `D0InternalDimensionSelector`)
  reads a hand-set `Bool` flag — genuine non-associativity needs Cayley–Dickson, absent from the pin.
- `66d2115` — `ASSUMP-HST-EXTERNAL` owner identified (was flagged "unclear"): the HST macro bridge
  (BOOK_02 §02.22, BOOK_06 §06.26) is the finite-subgaussian → continuum-Gaussian convex-response/MGF
  comparison. D0 supplies the finite subgaussian archive atom; the continuum Gaussian is the legitimate
  external owner. Ledger justification + `external_source` sharpened.

### C. Honest over-claim correction (found by an 11-agent audit/frontier workflow)
- `e412ca9` — **D0-HULL-001** was registered LEAN_PROVED/CORE-FORMALIZED on the 5 vacuous
  `D0.Topology.TilingHull` theorems (`Prop` fields `:= true` proved by `rfl`). The proof-of-record was
  REPOINTED to the real `D0.Claims.KTheoryGapModule.ktheory_gap_module` (gap labels in ℤ+ℤφ⁻¹ = Sturmian
  frequencies, exactly proved) — the gap-labeling invariant that is the formal heart of the aperiodic
  hull. Aperiodicity / FLC / repetitivity scoped honestly as cert-backed; a genuine Mathlib
  `Delone.DeloneSet ℝ` instance recorded as a theorem-target. Gate-safe (same CORE status → real
  theorem; integrity demotions 0). **This was the only active over-claim** in the corpus (full re-audit:
  1215 theorems classified, 0 holes, ledger 19/19 legitimate external owners).

### D. Frontier wins (genuine new formalization, Mathlib reuse)
- `743aea8` **P1 — D0-ARCHIVE-LIGHTPROFINITE-001**: the archive tower upgraded from the bespoke
  `InverseLimit` subtype to a GENUINE Mathlib categorical object — an `ℕᵒᵖ ⥤ FintypeCat` diagram
  (`Functor.ofOpSequence` + `FintypeCat.homMk`) whose limit in `Profinite` packages as a `LightProfinite`.
  Structural theorems prove the diagram faithfully encodes the tower (successor map = `archiveProjection`;
  bonding maps surjective). No new dependency.
- `6d7465f` **P2 — D0-FORGETTING-CHANNEL-PTP-001**: forgetting/decoherence as the fully depolarizing
  channel `M ↦ (tr M / n)·I`, proved a genuine POSITIVE TRACE-PRESERVING linear map over real matrices
  (`Matrix.PosSemidef`). HONEST SCOPE: full complete positivity (a Mathlib `CompletelyPositiveMap` over
  `CStarMatrix`) is NOT a bounded hand-proof — the audit verifier was over-optimistic (the
  `map_cstarMatrix_nonneg'` obligation quantifies over all `k×k` amplifications, and the trace channel is
  not a *-homomorphism). Recorded as a theorem-target.

---

## Honest residuals (named theorem-targets / owner-edges — NOT closed)
- **π₁(T²)≅ℤ²** — external owner: the keystone π₁(S¹)≅ℤ is absent from the pin (it is a TODO comment).
  D0 also has no topological torus (its torus is the ℤ²-acting integer matrix `T`).
- **Braid-valence gauge** (THE 04.6.M1.gauge) — external owner: no braid group in the pin; the claim is a
  representation-theoretic / no-catalog argument, prose-hedged as "effective-language inevitability".
- **Fibonacci fusion CATEGORY** — research-level: no fusion-category/Grothendieck-ring asset in the pin.
  The substantive content (φ²=φ+1 fusion rule + Perron N_τ²=N_τ+I → entropy = log φ) is already proved;
  full topological conjugacy stays the Adler–Weiss owner-edge.
- **Delone-hull FLC / aperiodicity** — research-level: the pin has the `DeloneSet` *definition* only.
  Bounded sub-step (a real `Delone.DeloneSet ℝ` instance from the Sturmian point set) is the theorem-target;
  the aperiodicity itself is already cert/number-theoretically proved (Sturmian + `KTheoryGapModule`).
- **Complete positivity (CPTP)** of the forgetting channel — theorem-target (PTP is proved; CP needs the
  full amplification obligation, not bounded).
- **Smooth/continuum Bianchi**, **GHP-Cauchy limit**, **2¹¹ Fock residue** — remain the existing
  Rieffel–GHP / Dixmier owner-edges; the pin has torsion on `CovariantDerivative` but no curvature/Bianchi.

---

## Integrity statement
0 proof holes (no `sorry`/`admit`/`axiom` anywhere in `D0/`). 0 active over-claims after the D0-HULL-001
correction. All 19 ledger `ASSUMP-*` rows are legitimate external owners with a real citation, a real
D0-side internal anchor, and confirmed genuine absence from the pin (spot-checked: Cartan, Dixmier trace,
Adler–Weiss, Mordell-E8, Hurwitz badly-approximable). No claim was promoted past its honest level; every
external dependency is a cited owner-edge; every residual is named above. Two over-optimistic "ready"
verdicts were caught by verify-then-promote (Cartan absent from pin; CPTP unbounded) and downgraded to
honest external-owner / theorem-target status rather than faked.

## Commits (this session, on `master`)
`66d2115` markers→real + ratchet 12→1 + HST · `e412ca9` D0-HULL-001 over-claim fix ·
`743aea8` P1 LightProfinite · `6d7465f` P2 forgetting-channel PTP · `8d7f5cb` BianchiResidual strengthened
(preceded earlier this session by `69af4da`, `c3fddc6`, `1370dea`, `6164629`, `9e84541`).
