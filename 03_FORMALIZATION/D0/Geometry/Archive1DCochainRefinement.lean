import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Matrix.Basis
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring
import D0.Core.FiniteTypes

namespace D0.Geometry

open scoped BigOperators
noncomputable section

/-!
# D0.Geometry.Archive1DCochainRefinement

Owner: `D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001`.

The one-dimensional definitions and proofs below are migrated from the
preserved research capsule `a4d_native_cochain_refinement.lean`, section 1
of `A4D_NATIVE_COCHAIN_REFINEMENT.md`. Here `m + 1` is the coarse cycle size.
The unscaled cycle incidence, vertex and edge maps, Gram identities, and
degree-dependent scale correction are proved for every `m`. The fixed trace
constants below remain separate arithmetic and do not define any matrices.
The full four-dimensional `dForward` application is not proved in this file.
-/

/-- Duplicate the first coarse vertex at the new final fine vertex. -/
def archiveCochainB0 (m : ℕ) (f : Fin (m + 1) → ℝ) : Fin (m + 2) → ℝ :=
  Fin.lastCases (f 0) f

/-- Copy the coarse edges and assign zero to the collapsed final edge. -/
def archiveCochainB1 (m : ℕ) (f : Fin (m + 1) → ℝ) : Fin (m + 2) → ℝ :=
  Fin.lastCases 0 f

/-- Oriented cyclic incidence, including the wrap edge. -/
def archiveCycleIncidence (m : ℕ) (f : Fin (m + 1) → ℝ) : Fin (m + 1) → ℝ :=
  Fin.lastCases (f 0 - f (Fin.last m))
    (fun j => f j.succ - f j.castSucc)

/-- The vertex lift's exact counting Gram form. -/
theorem archive_b0_gram (m : ℕ) (f g : Fin (m + 1) → ℝ) :
    (∑ i, archiveCochainB0 m f i * archiveCochainB0 m g i) =
      (∑ i, f i * g i) + f 0 * g 0 := by
  rw [Fin.sum_univ_castSucc]
  simp [archiveCochainB0]

/-- Matrix of the vertex lift in the standard coordinate bases. -/
def archiveCochainB0Matrix (m : ℕ) : Matrix (Fin (m + 2)) (Fin (m + 1)) ℝ :=
  fun i j => archiveCochainB0 m (fun k => if k = j then 1 else 0) i

/-- The vertex matrix acts as the original cochain lift. -/
theorem archive_b0_matrix_mulVec (m : ℕ) (f : Fin (m + 1) → ℝ) :
    (archiveCochainB0Matrix m).mulVec f = archiveCochainB0 m f := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simp [Matrix.mulVec, dotProduct, archiveCochainB0Matrix, archiveCochainB0]
  · simp [Matrix.mulVec, dotProduct, archiveCochainB0Matrix, archiveCochainB0]

/-- The vertex Gram matrix is the identity plus the `(0,0)` matrix unit. -/
theorem archive_b0_matrix_gram (m : ℕ) :
    (archiveCochainB0Matrix m).transpose * archiveCochainB0Matrix m =
      1 + Matrix.single 0 0 1 := by
  ext j k
  have h := archive_b0_gram m
    (fun i : Fin (m + 1) => if i = j then 1 else 0)
    (fun i : Fin (m + 1) => if i = k then 1 else 0)
  by_cases hj : j = 0 <;> by_cases hk : k = 0 <;>
    simpa [Matrix.mul_apply, Matrix.one_apply, Matrix.single_apply,
      Matrix.transpose_apply, archiveCochainB0Matrix, eq_comm, hj, hk,
      mul_ite, ite_mul] using h

/-- The vertex Gram diagonal is 2 at the repeated vertex and 1 elsewhere. -/
theorem archive_b0_matrix_gram_diagonal (m : ℕ) (j : Fin (m + 1)) :
    ((archiveCochainB0Matrix m).transpose * archiveCochainB0Matrix m) j j =
      if j = 0 then 2 else 1 := by
  rw [archive_b0_matrix_gram]
  by_cases hj : j = 0 <;>
    simp [Matrix.single_apply, hj, eq_comm] <;> norm_num

/-- Edge refinement preserves the real counting inner product. -/
theorem b1_isometry (m : ℕ) (f g : Fin (m + 1) → ℝ) :
    (∑ i, archiveCochainB1 m f i * archiveCochainB1 m g i) =
      ∑ i, f i * g i := by
  rw [Fin.sum_univ_castSucc]
  simp [archiveCochainB1]

/-- Matrix of the edge lift in the standard coordinate bases. -/
def archiveCochainB1Matrix (m : ℕ) : Matrix (Fin (m + 2)) (Fin (m + 1)) ℝ :=
  fun i j => archiveCochainB1 m (fun k => if k = j then 1 else 0) i

/-- The literal coordinate matrix has identity Gram matrix. -/
theorem archive_b1_matrix_gram (m : ℕ) :
    (archiveCochainB1Matrix m).transpose * archiveCochainB1Matrix m = 1 := by
  ext j k
  simp [Matrix.mul_apply, Matrix.one_apply, archiveCochainB1Matrix,
    archiveCochainB1, Fin.sum_univ_castSucc, eq_comm]

/-- The matrix and function definitions act identically on every edge
cochain. -/
theorem archive_b1_matrix_mulVec (m : ℕ) (f : Fin (m + 1) → ℝ) :
    (archiveCochainB1Matrix m).mulVec f = archiveCochainB1 m f := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · simp [Matrix.mulVec, dotProduct, archiveCochainB1Matrix, archiveCochainB1]
  · simp [Matrix.mulVec, dotProduct, archiveCochainB1Matrix, archiveCochainB1]

/-- Exact chain map for unscaled cyclic incidence, including wrap and
collapsed edges. -/
theorem intertwining_d_b0_eq_b1_d (m : ℕ) (f : Fin (m + 1) → ℝ) :
    archiveCycleIncidence (m + 1) (archiveCochainB0 m f) =
      archiveCochainB1 m (archiveCycleIncidence m f) := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i
  · have hz : Fin.lastCases (f 0) f (0 : Fin (m + 2)) = f 0 := by
      change Fin.lastCases (f 0) f (0 : Fin (m + 1)).castSucc = f 0
      simp only [Fin.lastCases_castSucc]
    simp only [archiveCycleIncidence, archiveCochainB0, archiveCochainB1,
      Fin.lastCases_last]
    rw [hz]
    ring
  · refine Fin.lastCases ?_ (fun k => ?_) j
    · simp [archiveCycleIncidence, archiveCochainB0, archiveCochainB1]
    · simp [archiveCycleIncidence, archiveCochainB0, archiveCochainB1,
        Fin.succ_castSucc, -Fin.castSucc_succ]

theorem archive_incidence_smul (m : ℕ) (c : ℝ) (f : Fin (m + 1) → ℝ) :
    archiveCycleIncidence m (fun i => c * f i) =
      fun i => c * archiveCycleIncidence m f i := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i <;> simp [archiveCycleIncidence, mul_sub]

theorem archive_b1_smul (m : ℕ) (c : ℝ) (f : Fin (m + 1) → ℝ) :
    archiveCochainB1 m (fun i => c * f i) = fun i => c * archiveCochainB1 m f i := by
  funext i
  refine Fin.lastCases ?_ (fun j => ?_) i <;> simp [archiveCochainB1]

/-- Adjacent-cycle degree correction for the level-scaled forward derivative. -/
def archiveCochainScaleRatio (m : ℕ) : ℝ := (m + 2 : ℝ) / (m + 1 : ℝ)

theorem archive_scaled_incidence_chain (m k : ℕ) (f : Fin (m + 1) → ℝ)
    (i : Fin (m + 2)) :
    (m + 2 : ℝ) * archiveCycleIncidence (m + 1)
        (fun j => archiveCochainScaleRatio m ^ k * archiveCochainB0 m f j) i =
      archiveCochainScaleRatio m ^ (k + 1) *
        archiveCochainB1 m (fun j => (m + 1 : ℝ) * archiveCycleIncidence m f j) i := by
  rw [archive_incidence_smul, intertwining_d_b0_eq_b1_d, archive_b1_smul, pow_succ]
  have h : (m + 1 : ℝ) ≠ 0 := by positivity
  simp only [archiveCochainScaleRatio]
  field_simp

/-- The incidence energy pulls back exactly; this is not a Laplacian
intertwining statement. -/
theorem archive_incidence_energy_pullback (m : ℕ) (f g : Fin (m + 1) → ℝ) :
    (∑ i, archiveCycleIncidence (m + 1) (archiveCochainB0 m f) i *
      archiveCycleIncidence (m + 1) (archiveCochainB0 m g) i) =
      ∑ i, archiveCycleIncidence m f i * archiveCycleIncidence m g i := by
  rw [intertwining_d_b0_eq_b1_d, intertwining_d_b0_eq_b1_d, b1_isometry]

/-- Recorded vertex-mass trace value at the fixed L = 2 comparison. No matrix
is defined by this scalar. -/
def massMatrixTrace1D : ℕ := 3

/-- Recorded edge-Gram trace value at the fixed L = 2 comparison. No refinement
map or Gram matrix is defined by this scalar. -/
def edgeGramMatrixTrace1D : ℕ := 2

theorem mass_trace_ne_edge_trace : massMatrixTrace1D ≠ edgeGramMatrixTrace1D := by
  unfold massMatrixTrace1D edgeGramMatrixTrace1D
  decide

/-- **D0-ARCHIVE-1D-COCHAIN-REFINEMENT-001 (Owner, scalar scope)**:
Records only the two fixed trace values and their inequality. It does not prove
an isometry or a chain-map identity. -/
theorem archive_1d_cochain_refinement_owner :
    (massMatrixTrace1D = 3) ∧
    (edgeGramMatrixTrace1D = 2) ∧
    (massMatrixTrace1D ≠ edgeGramMatrixTrace1D) :=
  ⟨rfl, rfl, mass_trace_ne_edge_trace⟩

end
end D0.Geometry
