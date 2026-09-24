import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Geometry.A4DScalarComparisonPatch

/-!
# Comparison-jet nonselection by nearest-neighbor edge Laplacian freedom

Memo (5.10)–(5.11): the one-parameter family
`S_lam = S_patch + lam T_edge` preserves constants and mandatory distance-two entries,
so the stated scalar support/composition constraints do not select a unique `S`.

This is nonselection inside the stated family, not universal nonuniqueness.
-/

namespace D0.Geometry

open Matrix
open scoped BigOperators

set_option linter.unusedSimpArgs false

variable {n : ℕ} [NeZero n]

/-- Edge weight `w_i(h,k) = h_i k_i`. -/
def scalarEdgeWeight (h k : Fin n → ℚ) (i : Fin n) : ℚ :=
  h i * k i

/-- Symmetric weighted nearest-neighbor edge Laplacian (5.10). -/
def scalarEdgeLaplacian (h k : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  fun i j =>
    if j = i + 1 then scalarEdgeWeight h k i
    else if i = j + 1 then scalarEdgeWeight h k j
    else if i = j then
      - (scalarEdgeWeight h k i + scalarEdgeWeight h k (i - 1))
    else
      0

/-- One-parameter family `S_lam = S_patch + lam T_edge` (5.11). -/
def scalarComparisonFamily (lam : ℚ) (h k : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  scalarComparisonPatch h k + lam • scalarEdgeLaplacian h k

theorem scalarEdgeLaplacian_comm (h k : Fin n → ℚ) :
    scalarEdgeLaplacian h k = scalarEdgeLaplacian k h := by
  ext i j
  simp [scalarEdgeLaplacian, scalarEdgeWeight, mul_comm]

theorem scalarEdgeLaplacian_delta_L5 :
    scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 =
      !![(-50), 25, 0, 0, 25;
         25, (-25), 0, 0, 0;
         0, 0, 0, 0, 0;
         0, 0, 0, 0, 0;
         25, 0, 0, 0, (-25)] := by
  native_decide

theorem scalarEdgeLaplacian_delta_L5_symmetric :
    (scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5)ᵀ =
      scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 := by
  rw [scalarEdgeLaplacian_delta_L5]; native_decide

theorem scalarEdgeLaplacian_delta_L5_rowSumZero (i : Fin 5) :
    ∑ j : Fin 5, scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 i j = 0 := by
  fin_cases i <;> native_decide

theorem scalarEdgeLaplacian_delta_L5_no_distanceTwo :
    scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 (0 : Fin 5) (2 : Fin 5) = 0 ∧
      scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 (1 : Fin 5) (-1) = 0 := by
  native_decide

theorem scalarComparisonFamily0_eq_patch :
    scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5 =
      scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5 := by
  simp [scalarComparisonFamily]

theorem scalarComparisonFamily1_eq :
    scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5 =
      scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5 +
        scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 := by
  simp [scalarComparisonFamily]

theorem scalarComparisonFamily0_rowSumZero (i : Fin 5) :
    ∑ j : Fin 5, scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5 i j = 0 := by
  simpa [scalarComparisonFamily0_eq_patch] using scalarComparisonPatch_delta_L5_rowSumZero i

theorem scalarComparisonFamily1_rowSumZero (i : Fin 5) :
    ∑ j : Fin 5, scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5 i j = 0 := by
  fin_cases i <;> native_decide

/-- Constants preserved for every rational parameter (via bilinearity of row sums). -/
theorem scalarComparisonFamily_delta_L5_rowSumZero (lam : ℚ) (i : Fin 5) :
    ∑ j : Fin 5, scalarComparisonFamily lam scalarPatchDeltaH5 scalarPatchDeltaH5 i j = 0 := by
  have hp := scalarComparisonPatch_delta_L5_rowSumZero i
  have he := scalarEdgeLaplacian_delta_L5_rowSumZero i
  simp only [scalarComparisonFamily, Matrix.add_apply, Matrix.smul_apply, smul_eq_mul,
    Finset.sum_add_distrib]
  have hmul : ∑ j, lam * scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 i j =
      lam * ∑ j, scalarEdgeLaplacian scalarPatchDeltaH5 scalarPatchDeltaH5 i j := by
    simp [Finset.mul_sum]
  rw [hmul, hp, he, mul_zero, add_zero]

theorem scalarComparisonFamily0_sameAxis :
    (scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5 +
        (scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5)ᵀ)
      (1 : Fin 5) (-1) = (-25 / 2 : ℚ) := by
  simpa [scalarComparisonFamily0_eq_patch] using scalarComparisonPatch_delta_L5_sameAxis

theorem scalarComparisonFamily1_sameAxis :
    (scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5 +
        (scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5)ᵀ)
      (1 : Fin 5) (-1) = (-25 / 2 : ℚ) := by
  native_decide

theorem scalarComparisonFamily0_zeroPlusTwo :
    (scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5 +
        (scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5)ᵀ)
      (0 : Fin 5) (2 : Fin 5) = (-25 / 4 : ℚ) := by
  simpa [scalarComparisonFamily0_eq_patch] using scalarComparisonPatch_delta_L5_zeroPlusTwo

theorem scalarComparisonFamily1_zeroPlusTwo :
    (scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5 +
        (scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5)ᵀ)
      (0 : Fin 5) (2 : Fin 5) = (-25 / 4 : ℚ) := by
  native_decide

/-- At least two parameter values give distinct comparison jets. -/
theorem scalarComparisonFamily_distinct_jets :
    scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5 ≠
      scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5 := by
  intro h
  have hentry := congr_fun (congr_fun h (0 : Fin 5)) (0 : Fin 5)
  have h0 : scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5 (0 : Fin 5) 0 =
      (25 / 4 : ℚ) := by
    simp [scalarComparisonFamily0_eq_patch, scalarComparisonPatch_delta_L5]
  have h1 : scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5 (0 : Fin 5) 0 =
      (25 / 4 : ℚ) + (-50 : ℚ) := by
    simp [scalarComparisonFamily1_eq, scalarComparisonPatch_delta_L5,
      scalarEdgeLaplacian_delta_L5, Matrix.add_apply]
  rw [h0, h1] at hentry
  norm_num at hentry

/-- Capstone nonselection inside the stated family. -/
theorem scalarComparison_constraints_do_not_select_unique_S :
    ∃ S₀ S₁ : Matrix (Fin 5) (Fin 5) ℚ,
      (∀ i, ∑ j, S₀ i j = 0) ∧
      (∀ i, ∑ j, S₁ i j = 0) ∧
      (S₀ + S₀ᵀ) (1 : Fin 5) (-1) = (-25 / 2 : ℚ) ∧
      (S₁ + S₁ᵀ) (1 : Fin 5) (-1) = (-25 / 2 : ℚ) ∧
      (S₀ + S₀ᵀ) (0 : Fin 5) (2 : Fin 5) = (-25 / 4 : ℚ) ∧
      (S₁ + S₁ᵀ) (0 : Fin 5) (2 : Fin 5) = (-25 / 4 : ℚ) ∧
      S₀ ≠ S₁ := by
  refine ⟨scalarComparisonFamily 0 scalarPatchDeltaH5 scalarPatchDeltaH5,
    scalarComparisonFamily 1 scalarPatchDeltaH5 scalarPatchDeltaH5,
    scalarComparisonFamily0_rowSumZero, scalarComparisonFamily1_rowSumZero,
    scalarComparisonFamily0_sameAxis, scalarComparisonFamily1_sameAxis,
    scalarComparisonFamily0_zeroPlusTwo, scalarComparisonFamily1_zeroPlusTwo,
    scalarComparisonFamily_distinct_jets⟩

end D0.Geometry
