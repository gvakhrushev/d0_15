import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchiveCurvatureDensity

open scoped BigOperators

namespace D0

def archiveCurvatureAction (N : Nat) : ℝ :=
  ∑ n ∈ Finset.range N, seamCurvatureDensity n

theorem archiveCurvatureAction_nonnegative (N : Nat) :
    0 ≤ archiveCurvatureAction N := by
  unfold archiveCurvatureAction
  apply Finset.sum_nonneg
  intro n _hn
  exact seamCurvatureDensity_nonnegative n

theorem archiveCurvatureAction_zero_iff_all_flat (N : Nat) :
    archiveCurvatureAction N = 0 ↔ ∀ n < N, OperatorTransportFlat n := by
  constructor
  · intro h n hn
    have h_nonneg :
        ∀ n ∈ Finset.range N, 0 ≤ seamCurvatureDensity n := by
      intro n _hn
      exact seamCurvatureDensity_nonnegative n
    have h_each :=
      (Finset.sum_eq_zero_iff_of_nonneg h_nonneg).mp (by
        simpa [archiveCurvatureAction] using h)
    exact (seamCurvatureDensity_zero_iff_flat n).mp
      (h_each n (Finset.mem_range.mpr hn))
  · intro h
    unfold archiveCurvatureAction
    apply Finset.sum_eq_zero
    intro n hn
    exact (seamCurvatureDensity_zero_iff_flat n).mpr
      (h n (Finset.mem_range.mp hn))

end D0
