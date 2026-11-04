import D0.Research.TaskFaithfulReporterAffineTransfer
import D0.Research.TaskFaithfulRepeatedReporterDerivative

/-!
# Transfer for a repeated tied reporter

The local affine-effect binding and equality of all unit-input statistics are
assumptions on the same word and a neighbourhood of zero. A shared typed label
uses the same preparation, effect and direction at every occurrence. Neither
physical admission nor effect bounds, changing preparation, nonradial source,
heat, clock or work follow from this transfer.
-/

noncomputable section
namespace D0.Research

open Filter
open scoped Topology

variable {J I M O X V : Type*} [DecidableEq J]
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I] [CompleteSpace I]
  [NormedAddCommGroup M] [InnerProductSpace ℂ M] [FiniteDimensional ℂ M]
  [NormedAddCommGroup O] [InnerProductSpace ℂ O] [FiniteDimensional ℂ O]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X] [CompleteSpace X]
  [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]

/-- Transfer the exact multiplicity derivative to an actual reporter family
when its unit-input statistics match a locally affine-effect reference family. -/
theorem actualReporter_price_repeated_affine_derivative
    {n : Type*} [Fintype n] [DecidableEq n]
    (inputPrepare : J → I →ₗ[ℂ] M) (readout : J → O →ₗ[ℂ] O)
    (returnPrepare : J → X →ₗᵢ[ℂ] I)
    (referenceReport actualReport : ℝ → J → M →ₗ[ℂ] O)
    (reference : J → I →ₗ[ℂ] I) (direction : I →ₗ[ℂ] I) (corners : J → ℝ)
    (w : List J) (j : J)
    (hpos : ∀ k ∈ w, 0 < corners k) (hcj : 0 < corners j)
    (hcorner : ∀ k ∈ w,
      taskReturnCompression (returnPrepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (alpha : ℝ)
    (hscalar : (returnPrepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (returnPrepare j).toContinuousLinearMap) =
        (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
    (affineEffect : ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k ∈ w,
      reporterEffectFamily inputPrepare (referenceReport t) readout k =
        Function.update reference j (reference j + (t : ℂ) • direction) k)
    (sameTask : ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k ∈ w,
      sameUnitReporterStatistics (inputPrepare k)
        (referenceReport t k) (actualReport t k) (readout k)) :
    let S : Matrix n n ℂ := ((z * (w.map corners).prod ^ 2 : ℝ) : ℂ) •
      D0.Analysis.gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t => actualReporterReturnPrice inputPrepare (actualReport t) readout returnPrepare
        w K basis z)
      ((4 * (w.count j : ℝ) * alpha / corners j) *
        D0.Analysis.regularizedReturnGain (1-z) S) 0 := by
  have h := taskReturnProduct_price_repeated_affine returnPrepare reference direction corners w j
    hpos hcj hcorner alpha hscalar K basis z hz hzOne
  apply h.congr_of_eventuallyEq
  filter_upwards [affineEffect, sameTask] with t ha hb
  have hprod :
      taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare (referenceReport t) readout) w =
        taskReturnProduct returnPrepare
          (Function.update reference j (reference j + (t : ℂ) • direction)) w := by
    unfold taskReturnProduct
    apply congrArg List.prod
    apply List.map_congr_left
    intro k hk
    rw [ha k hk]
  change D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) • D0.Analysis.gramMatrix
      (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare (actualReport t) readout)
        w ∘L K).toLinearMap basis) = _
  calc
    _ = D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) • D0.Analysis.gramMatrix
      (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare (referenceReport t) readout)
        w ∘L K).toLinearMap basis) :=
        (taskReturnProduct_price_eq_of_sameUnitStatistics inputPrepare (referenceReport t)
          (actualReport t) readout returnPrepare w K basis z hb).symm
    _ = _ := by rw [hprod]

end D0.Research
end
