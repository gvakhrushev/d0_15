# Next front — five campaigns for breakthrough synthesis (2026-08)

Built from a three-agent reviewer survey (matter / gravity-time / α-line). Ordered by dependency:
Campaign 0 unblocks citation of the entire session layer; Campaign 2 carries the largest
breakthrough potential; 1 is the sharpest positive fit; 3–4 convert the layer's negative power
into registered theorems.

---

## Campaign 0 — Registration and desync repair (mandatory first; ~1 session)

**Problem.** ~20 session modules (`TransportClosedForm`, `DarkArchiveStructure`, `JointCommutant`,
`EquivariantSeamNoGo`, `HodgeThreeLevelSpectrum`, `GenericSceneCalculus`, the dark-EOS chain, …)
are not imported in `D0/All.lean`, have no registry rows, and are git-untracked. Under the corpus's
closure contract **no row may cite them** — every later campaign is blocked on this.

**Work.**
1. Import all session modules into `09_LEAN_FORMALIZATION/D0/All.lean`; full `lake build`.
2. Draft registry rows (owner-gated: prepare the row texts, statuses proposed as
   certificate/formal_core; the owner decides mints).核心 rows: spectral resolution, archive
   structure, joint commutant, equivariant seam no-go, Hodge three-level, generic calculus,
   dark-EOS chain (with the |w|=φ conditionality stated).
3. Repair live desyncs found by survey:
   - row 583 (`D0-ALPHA-SEAM-FORM-FORCED-001`) still says FIVE fork doors; collapse to four is
     Lean-only. Update memo + `transport_twelve_check.py` (`distinct_objects = 5` stale).
   - `vp_alpha_seam_form_forced.py:124` still declares (ii) unowned; row says ADOPTED.
   - row 583's internal row references are uniformly +19 stale.
4. Log the discovered conflict: `YukawaShellOverlapMatrix.yukawaShellOverlap ∉ ℚ[Q]`
   (computed: fitting `aI+bQ+cQ²` fails) — the CERT-CLOSED scaffold is not equivariant-compatible.

**Exit criterion:** all modules build from `All.lean`; desync list empty; conflict logged.

---

## Campaign 1 — Trace-heat capacity gravity: fill the book/Lean gap (sharpest positive fit)

**Finding.** BOOK_07:1751 states the rule `I(S,s) = Tr_S(exp(−s Δ_G))`, horizon condition
`I(S,s) = C(∂S) = BoundaryCutWeight/4`. The Lean (`TraceHeatCapacityGravity.lean`) implements
`localHeatContent` as a **free `Rat`** (cert hardcodes `5/2`), `TraceHeatDefect` is dead code, and
`heat_trace_entropy_gradient_admits_gravity_interface` ignores its saturation hypothesis (`_hsat`
unused — vacuous). The book demands object A (scene Laplacian heat trace); the Lean delivers
object B (Lucas moments of `T²`, divergent, not a heat trace) plus an invented number.

**Work.**
1. New module `SceneTraceHeatCapacity`: instantiate `I(S,s)` from the closed forms — global
   `P0(e^{−s})`, per-zone sectors from the spectral resolution. `TraceHeatDefect` becomes
   computable for the first time; the horizon/saturation conditions become decidable arithmetic
   (both sides scene-computable: `BoundaryCutWeight({j}) = deg(j) ∈ {20,22,24}`).
2. Replace the vacuous theorem with a non-vacuous saturation statement (or record its vacuity as a
   named defect if the owner prefers).
3. Promote `ζ_L` from docstring to `def zetaL` with evaluation lemmas.
4. Instantiate the generic A0/A2 spectral-action ladder (`SpectralActionLadder.lean`, currently
   never applied to any scene) at the scene: `Tr Δ₀ = 718`, `Tr Δ₀² `, `M₂ = 50193` slots.

**Trap register (from survey):** six distinct objects are all called "heat trace" in the corpus
(scene L / toral Lucas / 4-D archive tower / index-placeholder / generic `Tr L²` / Feshbach block).
Every statement must name its operator. BOOK_06 §06.1.1 says "scene Laplacian" but its cert checks
the archive tower — do not conflate.

**Exit criterion:** `D0-TRACE-HEAT-CAPACITY-GRAVITY-001`'s heat side computed, not free;
saturation decidable; zeta defined; ladder instantiated.

---

## Campaign 2 — α-line obligation (i): the endgame (largest breakthrough potential)

**State.** Row 583: obligation (ii) adopted at ceiling, (iii) decomposed and reduced to (i); (i) is
the **single live obligation** of the flagship α dressing `α_top⁻¹ + φ⁻¹⁷(1 + h_KS sinθ_seam)`,
`φ⁻¹⁷ = ξ₅·φ⁻¹²`. The 5 is owned (`Xi5TorusDefect`: fifth toral return, `L₅ = 11 = |V₁₁|`,
`Tr(T⁵) = −11`). The 12 is a four-door fork with zero in-print bindings.

**Step 1 (free kill).** Door #5 (commutant 12) is now closable-negative: `EquivariantSeamNoGo`
proves the equivariant class has **zero seam**, so a seam depth cannot be the dimension of that
algebra; `JointCommutant` halves the 12 to 6 under the scene's own dynamics. Mint the no-go; fork
4 → 3.

**Step 2 (one-line no-go, trap-(d) vaccination).** `g_light ≠ Aut-commutant` as Lie algebras:
`𝔰𝔩₃ ⊕ ℚ⁴-centre` (rank 2, centre 4) vs `𝔰𝔲(3)⊕𝔰𝔲(2)⊕𝔲(1)` (rank 3, centre 1); partitions
`9+1+1+1` vs `8+3+1`. The two 12s of doors #1/#5 cannot be merged. Unexamined in the corpus.

**Step 3 (the decisive attempt).** Door #2 (`|V₁₁|+1`) is closest to bindable — the only door
sharing an owned object with the 5 (both from the fifth toral return). The binding statement:
  (a) an owned bijection {sectors crossed by one seam closure} ≅ `V₁₁ ⊔ {ω₀}` — the `+1` is the
      witness, the same `+1` that identified doors 3=4 (`witness_removal_identity`);
  (b) a **per-crossing φ⁻¹ contraction theorem** — the single missing mechanism (the parabolic law
      owns additivity of the parameter, not a per-step gain).
Binding criterion assembled from the corpus: §05.19 isolation cell (door 1 only), trap (d) — the
12 must be *produced as a crossing count*, and `transport_twelve_check.py` T2/T4/T5 flip on mint.

**Both outcomes are large.** If (b) succeeds → the transport factor is bound, obligation (i)
closes, and (iii) with it — the α-line ladder completes. If (b) is impossible — and
`TransportNotGolden` (no transport eigenvalue in ℚ(φ)) points that way — the honest outcome is a
**depth-axis no-go**, which settles (iii) closed-negative and forces a re-grade of the whole
02.13.h ladder. Run the full adversarial loop (memo with pre-registered attack surface, skeptic)
either way; the survey's preflight is done.

---

## Campaign 3 — Matter front: register the layer's negative power (three no-gos + one big positive)

1. **Hypercharge** (`D0-HYPERCHARGE-GRAPH-FLOW-OWNER-001`): an equivariant zone-normalised
   holonomy trace sees ≤ 3 numbers (the zone sums — `no_invariant_vector_in_archive` +
   `no_equivariant_seam`), hence cannot yield a 6-entry Weyl row. The flow→Weyl map Φ necessarily
   breaks the scene symmetry. Mint as a structural sharpening of the row's hedge.
2. **Higgs M3** (`D0-HIGGS-PHASON-CONDENSATION-OWNER-001`): the required non-commuting
   `(U, Q₀, Π_H)` provably does not exist in the equivariant class (joint commutant = 6,
   block-diagonal) — widen the blocker from "not present-core" to "not Aut-equivariant".
3. **Unified edge spine** (`D0-UNIFIED-EDGE-SPINE-001`): `PRIM-EDGE-HOLONOMY-SELECTOR` is not
   realizable equivariantly — a whole candidate family excluded.
4. **The big positive candidate — Yukawa from the transport cubic.** The logged conflict (overlap
   scaffold ∉ ℚ[Q]) has two resolutions; the interesting one: replace the scaffold by an element of
   `ℚ[Q]` — then its eigenvalues are forced to be the roots of `λ³ − 359λ − 2574`, and the charged
   -lepton hierarchy would be built from the transport spectrum with **no free matrix**. Explore;
   if the numerics are wrong, record the honest negative (the ratios are fixed, so this is
   immediately falsifiable — trap-(f)-clean by construction).
5. **Winding metric** (`D0-PRIM-WINDING-METRIC-001`): register `P₂ = (8+x⁹)(10+x¹¹)(12+x¹³)` as an
   internal candidate gap-size source (one factor per generation), honestly labelled candidate —
   the row's non-uniqueness objection survives.

**Do not attack:** the Puiseux cluster (rows 1–3 of the survey) — rational layer cannot produce
ramification indices 1/4, 1/3; carrier is a different 7-point object.

---

## Campaign 4 — Time front (exploratory): the Lefschetz–Hodge bridge

`lefschetz_spectrum_unfolds_scene` (owned): `|det(Tⁿ + I)| = 4, 9, 11, 20` for `n = 3,4,5,6`, with
`4 + 9 = 13` — the zone sizes and λ = 20 appear as anti-periodic Lefschetz counts of the **toral**
operator. The top Hodge factorisation's exponents are the same `9, 11, 13`. Nothing in the corpus
states a bridge. Investigate whether an owned identity (not an intertwiner — the field-disjointness
no-go `ℚ(√5) vs ℚ(√10)` forbids carrier intertwiners) connects the toral return ladder to the Hodge
exponents. Honest outcomes: a numeric-mechanism theorem, or a recorded near-miss (trap-(d) entry).
Low cost, high upside for the "time = toral flow / space = scene" unification.

---

## Execution order and verification

`0 → 1 → 2 (steps 1–2) → 3 (items 1–3) → 2 (step 3, the decisive attempt) → 3 (item 4) → 4`.

Every module: `lake build` + `#print axioms` (no `sorryAx`, no unnecessary `native_decide`);
numeric claims cross-checked by `tools/d0_scene_invariants.py` or a dedicated cert; every mint
candidate goes through the d0-adversarial-forcing-loop (preflight → memo with pre-registered
attack surface → independent skeptic → accept/repair). Registry mints are prepared as proposals —
status decisions stay with the owner.
