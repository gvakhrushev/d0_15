import Mathlib.LinearAlgebra.Matrix.Trace
import D0.Interface.Poisson
import D0.Matter.RepresentationCarrier

open scoped BigOperators

namespace D0.Matter

def localTraceDensity {ι : Type} (Γ : Matrix ι ι ℝ) (i : ι) : ℝ :=
  Γ i i

theorem sum_localTraceDensity_eq_trace {ι : Type} [Fintype ι]
    (Γ : Matrix ι ι ℝ) :
    (∑ i : ι, localTraceDensity Γ i) = Matrix.trace Γ := by
  unfold localTraceDensity Matrix.trace Matrix.diag
  rfl

theorem localTraceDensity_neutral_of_trace_zero {n : Nat}
    (Γ : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ)
    (hΓ : Matrix.trace Γ = 0) :
    NeutralSource (localTraceDensity Γ) := by
  unfold NeutralSource
  rw [sum_localTraceDensity_eq_trace Γ, hΓ]

structure ArchiveMatterOperator (n : Nat) (R : MatterRep) where
  op : Matrix (archivePhaseIndex n) (archivePhaseIndex n) ℝ
  trace_eq_anomaly : Matrix.trace op = (R.anomalySum : ℝ)

theorem archiveMatterOperator_localTraceDensity_neutral_if_anomaly_free
    (n : Nat) (R : MatterRep)
    (A : ArchiveMatterOperator n R)
    (h : R.anomalySum = 0) :
    NeutralSource (localTraceDensity A.op) := by
  apply localTraceDensity_neutral_of_trace_zero
  simpa [h] using A.trace_eq_anomaly

end D0.Matter
