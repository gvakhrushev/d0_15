import D0.Research.TaskFaithfulReporterProductEquality
import D0.Research.TaskFaithfulAffineReporterDerivative

/-!
# Reporter-level transfer of an affine return-price derivative

The reference reporter family is supplied with a local, exact affine effect
binding. The actual reporter has the same selected all-unit-input statistics
locally. Both bindings are explicit hypotheses, not physical admission or a
claim that a compiler is differentiable. Existing ordered-product equality
then transfers the owned affine derivative to the actual reporter family.
Independent heat, clock, work, changing preparation and other reports remain
outside this result. No normalized gain or physical positive gain is inferred.
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

/-- The existing total regularized price of the actual ordered reporter product,
with its unchanged history and basis. -/
def actualReporterReturnPrice {n : Type*} [Fintype n] [DecidableEq n]
    (inputPrepare : J → I →ₗ[ℂ] M) (report : J → M →ₗ[ℂ] O)
    (readout : J → O →ₗ[ℂ] O) (returnPrepare : J → X →ₗᵢ[ℂ] I)
    (w : List J) (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V) (z : ℝ) : ℝ :=
  D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) • D0.Analysis.gramMatrix
    (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare report readout) w ∘L K).toLinearMap basis)

/-- The claimed derivative holds for an actual reporter family when its selected
statistics agree locally with a supplied affine-effect reporter family. The
one-label affine law is required only for labels in the actual word, and no
smoothness assumption is placed on either reporter family. -/
theorem actualReporter_price_one_affine_derivative
    {n : Type*} [Fintype n] [DecidableEq n]
    (inputPrepare : J → I →ₗ[ℂ] M) (readout : J → O →ₗ[ℂ] O)
    (returnPrepare : J → X →ₗᵢ[ℂ] I)
    (referenceReport actualReport : ℝ → J → M →ₗ[ℂ] O)
    (reference : J → I →ₗ[ℂ] I) (direction : I →ₗ[ℂ] I) (corners : J → ℝ)
    (left right : List J) (j : J) (hleft : j ∉ left) (hright : j ∉ right)
    (hpos : ∀ k ∈ left ++ j :: right, 0 < corners k)
    (hcorner : ∀ k ∈ left ++ j :: right,
      taskReturnCompression (returnPrepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (alpha : ℝ)
    (hscalar : (returnPrepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (returnPrepare j).toContinuousLinearMap) =
        (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
    (affineEffect : ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k ∈ left ++ j :: right,
      reporterEffectFamily inputPrepare (referenceReport t) readout k =
        Function.update reference j (reference j + (t : ℂ) • direction) k)
    (sameTask : ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k ∈ left ++ j :: right,
      sameUnitReporterStatistics (inputPrepare k)
        (referenceReport t k) (actualReport t k) (readout k)) :
    let other := (left.map corners).prod * (right.map corners).prod
    let S : Matrix n n ℂ := ((z * other ^ 2 : ℝ) : ℂ) •
      D0.Analysis.gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t => actualReporterReturnPrice inputPrepare (actualReport t) readout returnPrepare
        (left ++ j :: right) K basis z)
      ((4 * alpha / corners j) * D0.Analysis.regularizedReturnGain (1-z)
        (((corners j ^ 2 : ℝ) : ℂ) • S)) 0 := by
  have h := taskReturnProduct_price_one_affine_reporter returnPrepare reference direction corners
    left right j hleft hright hpos hcorner alpha hscalar K basis z hz hzOne
  apply h.congr_of_eventuallyEq
  filter_upwards [affineEffect, sameTask] with t ha hb
  have hprod :
      taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare (referenceReport t) readout)
          (left ++ j :: right) =
        taskReturnProduct returnPrepare
          (Function.update reference j (reference j + (t : ℂ) • direction))
          (left ++ j :: right) := by
    unfold taskReturnProduct
    apply congrArg List.prod
    apply List.map_congr_left
    intro k hk
    rw [ha k hk]
  change D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) • D0.Analysis.gramMatrix
      (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare (actualReport t) readout)
        (left ++ j :: right) ∘L K).toLinearMap basis) = _
  calc
    _ = D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) • D0.Analysis.gramMatrix
      (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare (referenceReport t) readout)
        (left ++ j :: right) ∘L K).toLinearMap basis) :=
        (taskReturnProduct_price_eq_of_sameUnitStatistics inputPrepare (referenceReport t)
          (actualReport t) readout returnPrepare (left ++ j :: right) K basis z hb).symm
    _ = _ := by rw [hprod]

/-- A nonempty word whose actual reporter family is the negative of its reference
consumes the previous theorem. The affine effect binding and all original
corner hypotheses remain explicit; the sign gives no physical distinction. -/
theorem negReporter_price_one_affine_derivative
    {n : Type*} [Fintype n] [DecidableEq n]
    (inputPrepare : J → I →ₗ[ℂ] M) (readout : J → O →ₗ[ℂ] O)
    (returnPrepare : J → X →ₗᵢ[ℂ] I) (referenceReport : ℝ → J → M →ₗ[ℂ] O)
    (reference : J → I →ₗ[ℂ] I) (direction : I →ₗ[ℂ] I) (corners : J → ℝ)
    (left right : List J) (j : J) (hleft : j ∉ left) (hright : j ∉ right)
    (hpos : ∀ k ∈ left ++ j :: right, 0 < corners k)
    (hcorner : ∀ k ∈ left ++ j :: right,
      taskReturnCompression (returnPrepare k).toLinearMap (reference k) = (corners k : ℂ) • 1)
    (alpha : ℝ)
    (hscalar : (returnPrepare j).toContinuousLinearMap.adjoint ∘L
      (direction.toContinuousLinearMap ∘L (returnPrepare j).toContinuousLinearMap) =
        (alpha : ℂ) • 1)
    (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (z : ℝ) (hz : 0 ≤ z) (hzOne : z < 1)
    (affineEffect : ∀ᶠ t in 𝓝 (0 : ℝ), ∀ k ∈ left ++ j :: right,
      reporterEffectFamily inputPrepare (referenceReport t) readout k =
        Function.update reference j (reference j + (t : ℂ) • direction) k) :
    let other := (left.map corners).prod * (right.map corners).prod
    let S : Matrix n n ℂ := ((z * other ^ 2 : ℝ) : ℂ) •
      D0.Analysis.gramMatrix K.toLinearMap basis
    HasDerivAt
      (fun t => actualReporterReturnPrice inputPrepare (fun k => -(referenceReport t k))
        readout returnPrepare (left ++ j :: right) K basis z)
      ((4 * alpha / corners j) * D0.Analysis.regularizedReturnGain (1-z)
        (((corners j ^ 2 : ℝ) : ℂ) • S)) 0 := by
  apply actualReporter_price_one_affine_derivative inputPrepare readout returnPrepare
    referenceReport (fun t k => -(referenceReport t k)) reference direction corners
    left right j hleft hright hpos hcorner alpha hscalar K basis z hz hzOne affineEffect
  filter_upwards [] with t
  intro k hk
  exact neg_reporter_sameUnitStatistics (inputPrepare k) (referenceReport t k) (readout k)

end D0.Research
end
