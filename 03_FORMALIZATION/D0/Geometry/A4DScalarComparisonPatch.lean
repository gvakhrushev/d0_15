import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Geometry.A4DScalarAdvectiveGroupoidObstruction
import D0.Geometry.A4DScalarDeltaSecondJet

/-!
# Scalar two-edge comparison patch `S_patch`

Exact bilinear witness from
`MEMO_A4D_ENDPOINT_COMPARISON_JET_OVERLAP_LAW` (5.3)–(5.9).

This is an algebraic constants-preserving two-edge patch. It is not a geometrically
selected D0 law and does not claim uniqueness of `S`.
-/

namespace D0.Geometry

open Matrix
open scoped BigOperators

set_option linter.unusedSimpArgs false

variable {n : ℕ} [NeZero n]

/-- Directed distance-two contribution at base index `i` (memo (5.3)). -/
def scalarComparisonPatchWeight (h k : Fin n → ℚ) (i : Fin n) : ℚ :=
  - (h i * k i + h (i + 1) * k (i + 1)) / 8

/-- Symmetric off-diagonal two-edge support before diagonal repair. -/
def scalarComparisonPatchOffDiag (h k : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  fun i j =>
    if j = i + 2 then scalarComparisonPatchWeight h k i
    else if i = j + 2 then scalarComparisonPatchWeight h k j
    else 0

/-- Row-sum zero diagonal completion (5.4). -/
def scalarComparisonPatch (h k : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  fun i j =>
    if i = j then
      - ∑ t : Fin n, if t = i then (0 : ℚ) else scalarComparisonPatchOffDiag h k i t
    else
      scalarComparisonPatchOffDiag h k i j

theorem scalarComparisonPatchWeight_comm (h k : Fin n → ℚ) (i : Fin n) :
    scalarComparisonPatchWeight h k i = scalarComparisonPatchWeight k h i := by
  simp [scalarComparisonPatchWeight, mul_comm]

theorem scalarComparisonPatchOffDiag_comm (h k : Fin n → ℚ) :
    scalarComparisonPatchOffDiag h k = scalarComparisonPatchOffDiag k h := by
  ext i j
  simp only [scalarComparisonPatchOffDiag, scalarComparisonPatchWeight_comm]

theorem scalarComparisonPatch_comm (h k : Fin n → ℚ) :
    scalarComparisonPatch h k = scalarComparisonPatch k h := by
  ext i j
  simp only [scalarComparisonPatch, scalarComparisonPatchOffDiag_comm]

theorem scalarComparisonPatchWeight_add_left (h₁ h₂ k : Fin n → ℚ) (i : Fin n) :
    scalarComparisonPatchWeight (h₁ + h₂) k i =
      scalarComparisonPatchWeight h₁ k i + scalarComparisonPatchWeight h₂ k i := by
  simp [scalarComparisonPatchWeight, Pi.add_apply]; ring

theorem scalarComparisonPatchWeight_smul_left (a : ℚ) (h k : Fin n → ℚ) (i : Fin n) :
    scalarComparisonPatchWeight (a • h) k i = a * scalarComparisonPatchWeight h k i := by
  simp [scalarComparisonPatchWeight, Pi.smul_apply, smul_eq_mul]; ring

/-- Support is restricted to the diagonal and distance-two pairs. -/
theorem scalarComparisonPatch_support_twoEdge (h k : Fin n → ℚ) (i j : Fin n)
    (hij : i ≠ j) (hfwd : j ≠ i + 2) (hbwd : i ≠ j + 2) :
    scalarComparisonPatch h k i j = 0 := by
  simp [scalarComparisonPatch, scalarComparisonPatchOffDiag, hij, hfwd, hbwd]

/-- L = 5 displacement of `δ₀`. -/
def scalarPatchDeltaH5 : Fin 5 → ℚ :=
  fun i => if i = 0 then (-5 : ℚ) else if i = 4 then 5 else 0

/-- L = 5 displacement of `δ₀ + 2δ₁`. -/
def scalarPatchNondeltaH5 : Fin 5 → ℚ :=
  fun i => if i = 0 then (5 : ℚ) else if i = 1 then -10 else if i = 4 then 5 else 0

theorem scalarPatchDeltaH5_eq_displacement :
    scalarPatchDeltaH5 = scalarDisplacement (scalarSite (0 : Fin 5)) := by
  native_decide

theorem scalarPatchNondeltaH5_eq_displacement :
    scalarPatchNondeltaH5 = scalarDisplacement (scalarNondelta : Fin 5 → ℚ) := by
  native_decide

/-- Complete L = 5 delta comparison matrix (5.5). -/
theorem scalarComparisonPatch_delta_L5 :
    scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5 =
      !![(25 / 4), 0, (-25 / 8), (-25 / 8), 0;
         0, (25 / 4), 0, 0, (-25 / 4);
         (-25 / 8), 0, (25 / 8), 0, 0;
         (-25 / 8), 0, 0, (25 / 8), 0;
         0, (-25 / 4), 0, 0, (25 / 4)] := by
  native_decide

theorem scalarComparisonPatch_delta_L5_symmetric :
    (scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5)ᵀ =
      scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5 := by
  rw [scalarComparisonPatch_delta_L5]; native_decide

theorem scalarComparisonPatch_delta_L5_rowSumZero (i : Fin 5) :
    ∑ j : Fin 5, scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5 i j = 0 := by
  fin_cases i <;> native_decide

/-- Mandatory same-axis distance-two entry after doubling (5.6). -/
theorem scalarComparisonPatch_delta_L5_sameAxis :
    let S := scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5
    (S + Sᵀ) (1 : Fin 5) (-1) = (-25 / 2 : ℚ) := by
  simp only [scalarComparisonPatch_delta_L5_symmetric]; native_decide

/-- Mandatory `(0,+2)` distance-two entry after doubling (5.6). -/
theorem scalarComparisonPatch_delta_L5_zeroPlusTwo :
    let S := scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5
    (S + Sᵀ) (0 : Fin 5) (2 : Fin 5) = (-25 / 4 : ℚ) := by
  simp only [scalarComparisonPatch_delta_L5_symmetric]; native_decide

/-- Effective Hessian after subtracting `2 S_patch` (5.7). -/
theorem scalarComparisonPatch_delta_L5_effHessian :
    advectiveEnergyHessian (scalarSite (0 : Fin 5)) -
        (2 : ℚ) • scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5 =
      !![(25 / 2), 0, 0, 0, 0;
         0, 0, 0, 0, 0;
         0, 0, (-25 / 4), 0, 0;
         0, 0, 0, (-25 / 4), 0;
         0, 0, 0, 0, 0] := by
  native_decide

theorem scalarComparisonPatch_delta_L5_cancels_sameAxis :
    (advectiveEnergyHessian (scalarSite (0 : Fin 5)) -
        (2 : ℚ) • scalarComparisonPatch scalarPatchDeltaH5 scalarPatchDeltaH5)
      (1 : Fin 5) (-1) = 0 := by
  rw [scalarComparisonPatch_delta_L5_effHessian]; native_decide

/-- Complete L = 5 nondelta comparison matrix with `G² ≠ 0` (5.8). -/
theorem scalarComparisonPatch_nondelta_L5 :
    scalarComparisonPatch scalarPatchNondeltaH5 scalarPatchNondeltaH5 =
      !![(75 / 4), 0, (-125 / 8), (-25 / 8), 0;
         0, (75 / 4), 0, (-25 / 2), (-25 / 4);
         (-125 / 8), 0, (125 / 8), 0, 0;
         (-25 / 8), (-25 / 2), 0, (125 / 8), 0;
         0, (-25 / 4), 0, 0, (25 / 4)] := by
  native_decide

theorem scalarComparisonPatch_nondelta_L5_symmetric :
    (scalarComparisonPatch scalarPatchNondeltaH5 scalarPatchNondeltaH5)ᵀ =
      scalarComparisonPatch scalarPatchNondeltaH5 scalarPatchNondeltaH5 := by
  rw [scalarComparisonPatch_nondelta_L5]; native_decide

theorem scalarComparisonPatch_nondelta_L5_rowSumZero (i : Fin 5) :
    ∑ j : Fin 5, scalarComparisonPatch scalarPatchNondeltaH5 scalarPatchNondeltaH5 i j =
      0 := by
  fin_cases i <;> native_decide

/-- Nondelta effective Hessian display (5.9). -/
theorem scalarComparisonPatch_nondelta_L5_effHessian :
    advectiveEnergyHessian (scalarNondelta : Fin 5 → ℚ) -
        (2 : ℚ) • scalarComparisonPatch scalarPatchNondeltaH5 scalarPatchNondeltaH5 =
      !![(-25 / 2), 0, 0, 0, 0;
         0, 25, 0, 0, 0;
         0, 0, (75 / 4), 0, 0;
         0, 0, 0, (-125 / 4), 0;
         0, 0, 0, 0, 0] := by
  native_decide

/-- Cancellation is not an artifact of delta nilpotence `G² = 0`. -/
theorem scalarComparisonPatch_nondelta_L5_uses_nonzero_Gsq :
    (scalarCycleG (scalarNondelta : Fin 5 → ℚ) *
        scalarCycleG (scalarNondelta : Fin 5 → ℚ)) ≠ 0 :=
  nondelta_G_sq_ne_zero (n := 5) (by decide)

/-- Translation covariance witness: shifting the delta input yields the cyclically
shifted patch matrix (exact `native_decide` certification). -/
theorem scalarComparisonPatch_delta_L5_shift1_exists :
    ∃ M : Matrix (Fin 5) (Fin 5) ℚ,
      M = scalarComparisonPatch (fun i => scalarPatchDeltaH5 (i + 1))
        (fun i => scalarPatchDeltaH5 (i + 1)) ∧
      (∀ i, ∑ j, M i j = 0) ∧ Mᵀ = M := by
  refine ⟨scalarComparisonPatch (fun i => scalarPatchDeltaH5 (i + 1))
      (fun i => scalarPatchDeltaH5 (i + 1)), rfl, ?_, ?_⟩
  · intro i; fin_cases i <;> native_decide
  · native_decide

end D0.Geometry
