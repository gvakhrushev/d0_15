import D0.Geometry.Archive1DCochainRefinement
import D0.Geometry.ArchiveSeamCurvature
import D0.Geometry.ArchiveCubicalDifferential

namespace D0.Geometry

/-!
The supported one-dimensional cochain maps are bound here to the existing
archive projection, lift matrix and forward scale. These are migrations of
the corresponding proofs in the preserved research capsule
`a4d_native_cochain_refinement.lean`. The all-role `dForward` transport and
physical refinement/readout are separate obligations.
-/

/-- The vertex cochain lift is the literal frozen archive projection. -/
theorem archive_b0_literal_projection (N : ℕ) (f : D0.archivePhaseIndex N → ℝ) :
    archiveCochainB0 (N + 1) f = fun i => f (D0.archiveRGPhaseProjection N i) := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · have hp : D0.archiveRGPhaseProjection N (Fin.last (N + 2)) = 0 := by
      apply Fin.ext
      simp [D0.archiveRGPhaseProjection, D0.archiveFibers]
    simp only [archiveCochainB0, Fin.lastCases_last, hp]
    rfl
  · have hp : D0.archiveRGPhaseProjection N j.castSucc = j := by
      apply Fin.ext
      exact Nat.mod_eq_of_lt j.isLt
    simp [archiveCochainB0, hp]

/-- The same vertex lift is the existing archive lift matrix acting on a
vector. -/
theorem archive_b0_literal_matrix (N : ℕ) (f : D0.archivePhaseIndex N → ℝ) :
    archiveCochainB0 (N + 1) f = (D0.archiveLiftOperator N).mulVec f := by
  rw [archive_b0_literal_projection]
  funext i
  simp [D0.archiveLiftOperator, Matrix.mulVec, dotProduct]

/-- The standard-basis cochain matrix is the existing literal archive lift. -/
theorem archive_b0_matrix_eq_archive_lift (N : ℕ) :
    archiveCochainB0Matrix (N + 1) = D0.archiveLiftOperator N := by
  ext i j
  have h := congrFun
    (archive_b0_literal_matrix N (fun k => if k = j then 1 else 0)) i
  simpa [archiveCochainB0Matrix, Matrix.mulVec, dotProduct] using h

/-- The actual archive lift has vertex Gram matrix `I + E₀₀`. -/
theorem archive_lift_operator_gram (N : ℕ) :
    (D0.archiveLiftOperator N).transpose * D0.archiveLiftOperator N =
      1 + Matrix.single 0 0 1 := by
  simpa only [archive_b0_matrix_eq_archive_lift N] using
    archive_b0_matrix_gram (N + 1)

/-- The scale in the existing forward-difference owner is the cycle size. -/
theorem archive_forward_scale (N : ℕ) : forwardDifferenceScale N = (N + 2 : ℝ) := by
  simp [forwardDifferenceScale, D0.archiveFibers]

/-- The degree-corrected one-dimensional chain block at the actual archive
forward scales. This does not by itself construct the full 4D `dForward` map. -/
theorem archive_scaled_block_with_owner_scale (N k : ℕ)
    (f : D0.archivePhaseIndex N → ℝ) (i : D0.archivePhaseIndex (N + 1)) :
    forwardDifferenceScale (N + 1) * archiveCycleIncidence (N + 2)
        (fun j => archiveCochainScaleRatio (N + 1) ^ k * archiveCochainB0 (N + 1) f j) i =
      archiveCochainScaleRatio (N + 1) ^ (k + 1) * archiveCochainB1 (N + 1)
        (fun j => forwardDifferenceScale N * archiveCycleIncidence (N + 1) f j) i := by
  convert archive_scaled_incidence_chain (N + 1) k f i using 1 <;>
    simp [archive_forward_scale, Nat.cast_add, add_assoc]
  all_goals norm_num

/-- At the first archive level the uncorrected maps do not intertwine the
level-scaled differences: the first edge gives `3 ≠ 2`. -/
theorem archive_unscaled_chain_fails_owner_scales :
    let f : Fin 2 → ℝ := fun i => (i.val : ℝ)
    forwardDifferenceScale 1 * archiveCycleIncidence 2 (archiveCochainB0 1 f) 0 ≠
      archiveCochainB1 1 (fun j => forwardDifferenceScale 0 * archiveCycleIncidence 1 f j) 0 := by
  let f : Fin 2 → ℝ := fun i => (i.val : ℝ)
  change forwardDifferenceScale 1 * archiveCycleIncidence 2 (archiveCochainB0 1 f) 0 ≠
    archiveCochainB1 1 (fun j => forwardDifferenceScale 0 * archiveCycleIncidence 1 f j) 0
  have hdiff : archiveCycleIncidence 1 f (0 : Fin 2) = 1 := by
    change (Fin.lastCases (motive := fun _ : Fin 2 => ℝ) (f 0 - f (Fin.last 1))
      (fun j : Fin 1 => f j.succ - f j.castSucc)) ((0 : Fin 1).castSucc) = 1
    rw [Fin.lastCases_castSucc]
    norm_num [f]
  have hedge : archiveCochainB1 1 (archiveCycleIncidence 1 f) (0 : Fin 3) = 1 := by
    change archiveCochainB1 1 (archiveCycleIncidence 1 f) ((0 : Fin 2).castSucc) = 1
    simpa [archiveCochainB1] using hdiff
  have hfine : archiveCycleIncidence 2 (archiveCochainB0 1 f) (0 : Fin 3) = 1 := by
    rw [intertwining_d_b0_eq_b1_d]
    exact hedge
  have hcoarse : archiveCochainB1 1
      (fun j => forwardDifferenceScale 0 * archiveCycleIncidence 1 f j) (0 : Fin 3) = 2 := by
    change (Fin.lastCases (motive := fun _ : Fin 3 => ℝ) 0
      (fun j : Fin 2 => forwardDifferenceScale 0 * archiveCycleIncidence 1 f j))
      ((0 : Fin 2).castSucc) = 2
    rw [Fin.lastCases_castSucc, archive_forward_scale, hdiff]
    norm_num
  rw [hfine, hcoarse, archive_forward_scale]
  norm_num

end D0.Geometry
