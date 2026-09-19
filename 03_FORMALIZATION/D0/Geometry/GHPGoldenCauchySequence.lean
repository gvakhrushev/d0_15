import D0.Geometry.GHPGoldenCauchyBound
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Topology.MetricSpace.Cauchy

/-!
# Golden refinement towers are Cauchy in any pseudometric space

`D0-GHP-GOLDEN-CAUCHY-BOUND-001` owns the summability of the geometric
majorant `Σ C·δ₀^k`.

This module proves the exact abstract consequence: **any** sequence in **any**
pseudometric space whose consecutive steps are bounded by `C·δ₀^k` is Cauchy,
and in a complete ambient space it converges with the explicit tail bound
`dist (x k) (lim) ≤ C·δ₀^k / (1 − δ₀)`.

No specific D0 refinement-stage metric is constructed here.  In particular, this
module does not define compact quantum metric spaces or a quantum distance.  To use
the theorem in the external Rieffel/Latrémolière setting one must separately provide
a concrete metric realization of the stages and prove the required consecutive-step
estimate.  That datum remains under `ASSUMP-RIEFFEL-GHP`; smooth reconstruction also
requires `ASSUMP-CONNES-RECONSTRUCTION`.
-/

namespace D0.Geometry.GHPGoldenCauchySequence

open D0 D0.Geometry Filter Topology

variable {X : Type*} [PseudoMetricSpace X]

/-- A **golden refinement tower**: a sequence whose consecutive steps contract at the golden scale
`δ₀ = 1/(2φ³)` with some step constant `C`. -/
structure GoldenTower (x : ℕ → X) (C : ℝ) : Prop where
  step : ∀ k, dist (x k) (x (k + 1)) ≤ C * delta0 ^ k

/-- **Every golden refinement tower is a Cauchy sequence.** -/
theorem goldenTower_cauchySeq {x : ℕ → X} {C : ℝ} (h : GoldenTower x C) : CauchySeq x :=
  cauchySeq_of_le_geometric delta0 C delta0_lt_one h.step

/-- **Every golden refinement tower in a complete space converges.** -/
theorem goldenTower_converges [CompleteSpace X] {x : ℕ → X} {C : ℝ} (h : GoldenTower x C) :
    ∃ L : X, Tendsto x atTop (𝓝 L) :=
  cauchySeq_tendsto_of_complete (goldenTower_cauchySeq h)

/-- **Explicit convergence rate.** The distance from stage `k` to the limit is bounded by
`C·δ₀^k / (1 − δ₀)` — the golden geometric tail. -/
theorem goldenTower_dist_le_limit {x : ℕ → X} {C : ℝ} (h : GoldenTower x C) {L : X}
    (hL : Tendsto x atTop (𝓝 L)) (k : ℕ) :
    dist (x k) L ≤ C * delta0 ^ k / (1 - delta0) :=
  dist_le_of_le_geometric_of_tendsto delta0 C delta0_lt_one h.step hL k

/-- **Owner package (generic metric theorem).** For any golden refinement
tower in a complete pseudometric space: it is Cauchy, it converges, and the tail bound is the
golden geometric series. The smooth-manifold *identification* of the limit is not asserted. -/
theorem golden_tower_limit_owner [CompleteSpace X] {x : ℕ → X} {C : ℝ} (h : GoldenTower x C) :
    CauchySeq x ∧ ∃ L : X, Tendsto x atTop (𝓝 L) ∧
      ∀ k, dist (x k) L ≤ C * delta0 ^ k / (1 - delta0) := by
  refine ⟨goldenTower_cauchySeq h, ?_⟩
  obtain ⟨L, hL⟩ := goldenTower_converges h
  exact ⟨L, hL, goldenTower_dist_le_limit h hL⟩

end D0.Geometry.GHPGoldenCauchySequence
