import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchiveSeamCurvature

open scoped BigOperators

namespace D0

def seamCurvatureDensity (n : Nat) : ℝ :=
  ∑ i : archivePhaseIndex (n+1), ∑ j : archivePhaseIndex n,
    (seamCommutator n i j)^2

theorem seamCurvatureDensity_nonnegative (n : Nat) :
    0 ≤ seamCurvatureDensity n := by
  unfold seamCurvatureDensity
  apply Finset.sum_nonneg
  intro i _hi
  apply Finset.sum_nonneg
  intro j _hj
  positivity

theorem seamCurvatureDensity_zero_iff_flat (n : Nat) :
    seamCurvatureDensity n = 0 ↔ OperatorTransportFlat n := by
  constructor
  · intro h
    unfold OperatorTransportFlat
    ext i j
    have h_outer_nonneg :
        ∀ i ∈ (Finset.univ : Finset (archivePhaseIndex (n+1))),
          0 ≤ ∑ j : archivePhaseIndex n, (seamCommutator n i j)^2 := by
      intro i _hi
      apply Finset.sum_nonneg
      intro j _hj
      positivity
    have h_outer :=
      (Finset.sum_eq_zero_iff_of_nonneg h_outer_nonneg).mp (by
        simpa [seamCurvatureDensity] using h)
    have h_inner_sum :
        ∑ j : archivePhaseIndex n, (seamCommutator n i j)^2 = 0 := by
      exact h_outer i (Finset.mem_univ i)
    have h_inner_nonneg :
        ∀ j ∈ (Finset.univ : Finset (archivePhaseIndex n)),
          0 ≤ (seamCommutator n i j)^2 := by
      intro j _hj
      positivity
    have h_inner :=
      (Finset.sum_eq_zero_iff_of_nonneg h_inner_nonneg).mp h_inner_sum
    have h_sq : (seamCommutator n i j)^2 = 0 :=
      h_inner j (Finset.mem_univ j)
    exact sq_eq_zero_iff.mp h_sq
  · intro h
    unfold OperatorTransportFlat at h
    unfold seamCurvatureDensity
    rw [h]
    simp

end D0
