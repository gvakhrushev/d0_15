import Mathlib.Topology.MetricSpace.Basic
import Mathlib.Tactic
import D0.Geometry.GHPGoldenCauchyBound
import D0.Geometry.GHPGoldenCauchySequence

/-!
# D0.Bridge.GromovHausdorff — honest metric boundary

Historical versions of this file described the result below as a formalization of
Rieffel compact quantum metric spaces and quantum propinquity.  The Lean object was
never that: the proof used only an arbitrary `PseudoMetricSpace` plus a geometric
bound on consecutive distances.

This file now states exactly what is owned.

* `LipNormCandidate` records only a nonnegative real-valued functional.  It is
  deliberately NOT called a compact quantum metric space: no C*-algebra/order-unit
  structure, state space, weak-* metricization, Leibniz property, tunnel, bridge or
  quantum distance is constructed here.
* `MetricStageRealization` is the first concrete datum required to apply the golden
  Cauchy theorem to any intended refinement tower: actual stages in an actual
  pseudometric space, together with the stage-to-stage bound.
* From that datum, the already-owned generic theorem proves Cauchyness (and, in a
  complete space, convergence).

The identification of a D0 finite-stage tower with a genuine compact quantum metric
space and a Rieffel/Latrémolière distance remains the explicit external bridge
`ASSUMP-RIEFFEL-GHP`.  This module does not define or claim such a distance.
-/

namespace D0.Bridge.GromovHausdorff

open D0 D0.Geometry D0.Geometry.GHPGoldenCauchySequence

/-- A minimal nonnegative Lip-functional candidate.

This is intentionally weaker than a compact quantum metric space.  The name makes the
honesty boundary type-visible instead of hiding missing C*-algebra/state-space axioms. -/
structure LipNormCandidate (A : Type*) where
  lipNorm : A → ℝ
  lip_nonneg : ∀ a, 0 ≤ lipNorm a

/-- The owned golden geometric step majorant.  It is a real bound, not the definition
of any particular Gromov-Hausdorff or quantum distance. -/
noncomputable def goldenStepBound (C : ℝ) (k : ℕ) : ℝ :=
  C * delta0 ^ k

/-- **First missing concrete object for a D0 metric-limit application.**
A proposed stage tower must first be realized as points of an actual pseudometric space
and must satisfy the golden stage-to-stage estimate in that metric.

A future Rieffel/Latrémolière bridge may instantiate this structure, but doing so is
external to the present core. -/
structure MetricStageRealization (X : Type*) [PseudoMetricSpace X] where
  stage : ℕ → X
  C : ℝ
  step : ∀ k, dist (stage k) (stage (k + 1)) ≤ goldenStepBound C k

/-- The strongest unconditional theorem owned here: any sequence in any pseudometric
space satisfying the golden step estimate is Cauchy. -/
theorem metric_sequence_cauchy {X : Type*} [PseudoMetricSpace X]
    (x : ℕ → X) (C : ℝ)
    (hstep : ∀ k, dist (x k) (x (k + 1)) ≤ goldenStepBound C k) :
    CauchySeq x := by
  have htower : GoldenTower x C := by
    refine ⟨?_⟩
    intro k
    simpa [goldenStepBound] using hstep k
  exact goldenTower_cauchySeq htower

/-- A typed stage realization immediately supplies the generic Cauchy conclusion. -/
theorem metric_stage_realization_cauchy {X : Type*} [PseudoMetricSpace X]
    (R : MetricStageRealization X) :
    CauchySeq R.stage := by
  exact metric_sequence_cauchy R.stage R.C R.step

/-- In a complete ambient metric space the same typed realization converges. -/
theorem metric_stage_realization_converges {X : Type*}
    [PseudoMetricSpace X] [CompleteSpace X]
    (R : MetricStageRealization X) :
    ∃ L : X, Filter.Tendsto R.stage Filter.atTop (nhds L) := by
  apply cauchySeq_tendsto_of_complete
  exact metric_stage_realization_cauchy R

/-- **D0-GROMOV-HAUSDORFF-DEQUARANTINE-001, honesty-repaired owner.**

The legacy claim ID is retained for traceability, but the machine content is exactly a
generic metric theorem.  It does not assert that D0 stages have been embedded into a
Gromov-Hausdorff/quantum-metric space. -/
theorem golden_metric_cauchy_boundary_owner :
    delta0 < 1 ∧
    (∀ (X : Type*) [PseudoMetricSpace X] (x : ℕ → X) (C : ℝ),
      GoldenTower x C → CauchySeq x) := by
  refine ⟨delta0_lt_one, ?_⟩
  intro X _ x C h
  exact goldenTower_cauchySeq h

end D0.Bridge.GromovHausdorff
