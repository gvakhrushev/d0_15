import D0.Research.TaskFaithfulReturnPrice

/-!
# Exact same-task reporter transport through an ordered return product

For each listed reporter, equality of the output statistic on *every* unit
input implies equality of the complete pulled-back effect.  The existing
compression theorem then gives equality of each actual return block.  This
module transports that equality through the original list order, the same
retained-history map, its Gram matrix, and the return price.  No commutativity,
scalar corner, gain positivity, invertibility, or physical admission follows.
-/

noncomputable section
namespace D0.Research

variable {J I M O X : Type*}
  [NormedAddCommGroup I] [InnerProductSpace ℂ I] [FiniteDimensional ℂ I]
  [NormedAddCommGroup M] [InnerProductSpace ℂ M] [FiniteDimensional ℂ M]
  [NormedAddCommGroup O] [InnerProductSpace ℂ O] [FiniteDimensional ℂ O]
  [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]

/-- Each actual source reporter has its own fixed input preparation and readout. -/
def reporterEffectFamily (prepare : J → I →ₗ[ℂ] M)
    (report : J → M →ₗ[ℂ] O) (readout : J → O →ₗ[ℂ] O) : J → I →ₗ[ℂ] I :=
  fun j => taskReporterEffect (prepare j) (report j) (readout j)

/-- Equality of all unit-input reporter statistics makes the two actual ordered
return products equal. Reporter actions may differ, and labels may repeat. -/
theorem taskReturnProduct_eq_of_sameUnitStatistics
    (inputPrepare : J → I →ₗ[ℂ] M) (report₁ report₂ : J → M →ₗ[ℂ] O)
    (readout : J → O →ₗ[ℂ] O) (returnPrepare : J → X →ₗᵢ[ℂ] I)
    (w : List J)
    (same : ∀ j ∈ w, sameUnitReporterStatistics (inputPrepare j)
      (report₁ j) (report₂ j) (readout j)) :
    taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare report₁ readout) w =
      taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare report₂ readout) w := by
  unfold taskReturnProduct
  apply congrArg List.prod
  apply List.map_congr_left
  intro j hj
  have heffect := (taskReporterEffect_eq_iff_sameUnitStatistics
    (inputPrepare j) (report₁ j) (report₂ j) (readout j)).mpr (same j hj)
  have hblock := taskReturnCompression_eq_of_effect_eq (returnPrepare j).toLinearMap _ _ heffect
  exact congrArg LinearMap.toContinuousLinearMap hblock

/-- The common retained history produces the same Gram matrix, including when
that history is singular or zero. -/
theorem taskReturnProduct_gram_eq_of_sameUnitStatistics
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    {n : Type*} [Fintype n] [DecidableEq n]
    (inputPrepare : J → I →ₗ[ℂ] M) (report₁ report₂ : J → M →ₗ[ℂ] O)
    (readout : J → O →ₗ[ℂ] O) (returnPrepare : J → X →ₗᵢ[ℂ] I)
    (w : List J) (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V)
    (same : ∀ j ∈ w, sameUnitReporterStatistics (inputPrepare j)
      (report₁ j) (report₂ j) (readout j)) :
    D0.Analysis.gramMatrix
        (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare report₁ readout) w ∘L K).toLinearMap basis =
      D0.Analysis.gramMatrix
        (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare report₂ readout) w ∘L K).toLinearMap basis := by
  rw [taskReturnProduct_eq_of_sameUnitStatistics inputPrepare report₁ report₂ readout returnPrepare w same]

/-- The two actual return prices are exactly equal for the same `z`, full `K`,
and input basis. Equality here does not require log-domain, gain, or scalar
corner hypotheses: the two price arguments are definitionally the same. -/
theorem taskReturnProduct_price_eq_of_sameUnitStatistics
    {V : Type*} [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    {n : Type*} [Fintype n] [DecidableEq n]
    (inputPrepare : J → I →ₗ[ℂ] M) (report₁ report₂ : J → M →ₗ[ℂ] O)
    (readout : J → O →ₗ[ℂ] O) (returnPrepare : J → X →ₗᵢ[ℂ] I)
    (w : List J) (K : V →L[ℂ] X) (basis : OrthonormalBasis n ℂ V) (z : ℝ)
    (same : ∀ j ∈ w, sameUnitReporterStatistics (inputPrepare j)
      (report₁ j) (report₂ j) (readout j)) :
    D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
      D0.Analysis.gramMatrix
        (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare report₁ readout) w ∘L K).toLinearMap basis) =
    D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
      D0.Analysis.gramMatrix
        (taskReturnProduct returnPrepare (reporterEffectFamily inputPrepare report₂ readout) w ∘L K).toLinearMap basis) := by
  rw [taskReturnProduct_gram_eq_of_sameUnitStatistics inputPrepare report₁ report₂ readout returnPrepare w K basis same]

omit [FiniteDimensional ℂ I] [FiniteDimensional ℂ M] [FiniteDimensional ℂ O] in
/-- A full sign change in a reporter leaves the selected quadratic statistics
unchanged; no assumption is made about other unselected observations. -/
theorem neg_reporter_sameUnitStatistics (prepare : I →ₗ[ℂ] M)
    (report : M →ₗ[ℂ] O) (readout : O →ₗ[ℂ] O) :
    sameUnitReporterStatistics prepare report (-report) readout := by
  intro ψ hψ
  simp

/-- The equality condition is nonvacuous: identity and its negation are
distinct complex-linear reporters with the same selected statistics. -/
theorem distinct_reporters_same_statistics :
    let idc : ℂ →ₗ[ℂ] ℂ := LinearMap.id
    idc ≠ -idc ∧ sameUnitReporterStatistics idc idc (-idc) idc := by
  dsimp
  constructor
  · intro h
    have h1 := congrArg (fun f : ℂ →ₗ[ℂ] ℂ => f 1) h
    norm_num at h1
  · exact neg_reporter_sameUnitStatistics LinearMap.id LinearMap.id LinearMap.id


/-- A nonempty actual return word uses distinct identity and negative-identity
reporters. Their selected return price is equal for every common isometric
return preparation and retained history. No nonzero gain is asserted. -/
theorem distinct_reporters_same_ordered_price
    {X V : Type*} [NormedAddCommGroup X] [InnerProductSpace ℂ X] [FiniteDimensional ℂ X]
    [NormedAddCommGroup V] [InnerProductSpace ℂ V] [FiniteDimensional ℂ V]
    {n : Type*} [Fintype n] [DecidableEq n]
    (returnPrepare : X →ₗᵢ[ℂ] ℂ) (K : V →L[ℂ] X)
    (basis : OrthonormalBasis n ℂ V) (z : ℝ) :
    let idc : ℂ →ₗ[ℂ] ℂ := LinearMap.id
    idc ≠ -idc ∧
    D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
      D0.Analysis.gramMatrix
        (taskReturnProduct (fun _ : Unit => returnPrepare)
          (reporterEffectFamily (fun _ : Unit => idc) (fun _ => idc) (fun _ => idc)) [()] ∘L K).toLinearMap basis) =
    D0.Analysis.regularizedReturnPrice (1-z) ((z : ℂ) •
      D0.Analysis.gramMatrix
        (taskReturnProduct (fun _ : Unit => returnPrepare)
          (reporterEffectFamily (fun _ : Unit => idc) (fun _ => -idc) (fun _ => idc)) [()] ∘L K).toLinearMap basis) := by
  dsimp
  constructor
  · exact distinct_reporters_same_statistics.1
  · apply taskReturnProduct_price_eq_of_sameUnitStatistics
    intro j hj
    exact neg_reporter_sameUnitStatistics LinearMap.id LinearMap.id LinearMap.id

end D0.Research
end
