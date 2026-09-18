import D0.Geometry.GHPGoldenCauchyBound
import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Topology.MetricSpace.Cauchy

/-!
# Golden refinement towers are Cauchy and converge in any complete (quantum) metric space

`D0-GHP-GOLDEN-CAUCHY-BOUND-001` owns the *summability* of the step-bound series `Σ C·δ₀^k`.
The Rieffel bridge (`D0.Bridge.RieffelGHPBridge`) states explicitly that "D0 does NOT prove
GHP-Cauchyness of the refinement sequence — that is the explicit named residual".

This module discharges that residual at the level of generality at which it is a theorem:
**any** sequence in **any** pseudometric space whose consecutive steps are bounded by `C·δ₀^k`
is a Cauchy sequence, and in a complete space it converges, with the explicit tail bound
`dist (x k) (lim) ≤ C·δ₀^k / (1 − δ₀)`.

Applied to the D0 refinement tower `(G_k)` seen as points of Rieffel's space of compact quantum
metric spaces under the quantum Gromov–Hausdorff (propinquity) distance — which is a *complete*
metric space (Latrémolière, Rieffel) — this yields existence of a limit compact quantum metric
space without any smooth-manifold hypothesis. The step bound `d_qGH(G_k, G_{k+1}) ≤ C·δ₀^k` for the
concrete D0 tower and the identification of the limit with a spin manifold remain the external
owners `ASSUMP-RIEFFEL-GHP` / `ASSUMP-CONNES-RECONSTRUCTION`; this module removes the *Cauchy*
and *existence-of-limit* steps from that list.
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

/-- **Owner package (internal half of the Rieffel/GHP residual).** For any golden refinement
tower in a complete pseudometric space: it is Cauchy, it converges, and the tail bound is the
golden geometric series. The smooth-manifold *identification* of the limit is not asserted. -/
theorem golden_tower_limit_owner [CompleteSpace X] {x : ℕ → X} {C : ℝ} (h : GoldenTower x C) :
    CauchySeq x ∧ ∃ L : X, Tendsto x atTop (𝓝 L) ∧
      ∀ k, dist (x k) L ≤ C * delta0 ^ k / (1 - delta0) := by
  refine ⟨goldenTower_cauchySeq h, ?_⟩
  obtain ⟨L, hL⟩ := goldenTower_converges h
  exact ⟨L, hL, goldenTower_dist_le_limit h hL⟩

end D0.Geometry.GHPGoldenCauchySequence
