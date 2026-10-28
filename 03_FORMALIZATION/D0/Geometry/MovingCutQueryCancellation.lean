import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic

/-!
# Moving-cut cancellation in a finite QUERY control

The pinned PR #334 source at commit `172876cdf38bfce6f87fdd4a059d524b60c10eb9`
contains the exact rational rank-one control `+16/35`, `-16/35`, and `0`
for QUERY-only, cut-only, and joint conjugation source rows. This module
formalizes its generic two-dimensional matrix identity over `ℚ`.

It does not prove that either tangent is an admitted D0 variation, transport
the thermal operator, or identify this chart with the original 42-field
execution. It is a finite algebraic control only.
-/

namespace D0.Geometry.MovingCutQueryCancellation

abbrev M2 := Matrix (Fin 2) (Fin 2) ℚ

def P : M2 := !![(1 : ℚ), 0; 0, 0]

def U (c u : ℚ) : M2 := !![c, u; u, -c]

def K (u : ℚ) : M2 := !![0, -u; u, 0]

theorem K_eq_unitary_projector_commutator (c u : ℚ) :
    K u = U c u * P - P * U c u := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [K, U, P]

def escape (c u : ℚ) : M2 := (1 - P) * U c u * P

def queryVelocity (c u : ℚ) : M2 := K u * U c u - U c u * K u

def cutVelocity (u : ℚ) : M2 := K u * P - P * K u

def escapeVelocity (c u : ℚ) (dU dP : M2) : M2 :=
  -(dP * U c u * P) + (1 - P) * dU * P + (1 - P) * U c u * dP

def resolvent (u z : ℚ) : M2 := !![1 / (1 - z * u ^ 2), 0; 0, 1]

def escapeGram (c u : ℚ) : M2 :=
  Matrix.transpose (escape c u) * escape c u

def source (c u z : ℚ) (dU dP : M2) : ℚ :=
  2 * z * Matrix.trace
    (resolvent u z * Matrix.transpose (escape c u) * escapeVelocity c u dU dP)

theorem escape_eq (c u : ℚ) :
    escape c u = !![(0 : ℚ), 0; u, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [escape, P, U, Matrix.mul_apply]

theorem escape_transpose_eq (c u : ℚ) :
    Matrix.transpose (escape c u) = !![(0 : ℚ), u; 0, 0] := by
  rw [escape_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp

theorem escape_gram_eq (c u : ℚ) :
    escapeGram c u = !![u ^ 2, 0; 0, 0] := by
  unfold escapeGram
  rw [escape_transpose_eq, escape_eq]
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply] <;> ring

theorem resolvent_is_two_sided_inverse
    (c u z : ℚ) (hden : 1 - z * u ^ 2 ≠ 0) :
    resolvent u z * (1 - z • escapeGram c u) = 1 ∧
    (1 - z • escapeGram c u) * resolvent u z = 1 := by
  have hleft : resolvent u z * (1 - z • escapeGram c u) = 1 := by
    unfold resolvent
    rw [escape_gram_eq]
    ext i j
    fin_cases i <;> fin_cases j
    · simp [Matrix.mul_apply]
      field_simp [hden]
    · simp [Matrix.mul_apply]
    · simp [Matrix.mul_apply]
    · simp [Matrix.mul_apply]
  have hright : (1 - z • escapeGram c u) * resolvent u z = 1 := by
    unfold resolvent
    rw [escape_gram_eq]
    ext i j
    fin_cases i <;> fin_cases j
    · simp [Matrix.mul_apply]
      field_simp [hden]
    · simp [Matrix.mul_apply]
    · simp [Matrix.mul_apply]
    · simp [Matrix.mul_apply]
  exact ⟨hleft, hright⟩

theorem query_velocity_source_term_eq (c u : ℚ) :
    escapeVelocity c u (queryVelocity c u) 0 = !![(0 : ℚ), 0; 2 * c * u, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [escapeVelocity, queryVelocity, K, P, U, Matrix.mul_apply] <;> ring

theorem cut_velocity_source_term_eq (c u : ℚ) :
    escapeVelocity c u 0 (cutVelocity u) = !![-u ^ 2, 0; -2 * c * u, u ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [escapeVelocity, cutVelocity, K, P, U, Matrix.mul_apply] <;> ring

theorem joint_velocity_source_term_eq (c u : ℚ) :
    escapeVelocity c u (queryVelocity c u) (cutVelocity u) =
      !![-u ^ 2, 0; 0, u ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [escapeVelocity, queryVelocity, cutVelocity, K, P, U, Matrix.mul_apply] <;> ring

theorem moving_cut_query_source_rows_cancel
    (c u z : ℚ) (hunit : c ^ 2 + u ^ 2 = 1) (hden : 1 - z * u ^ 2 ≠ 0) :
    U c u * U c u = 1 ∧
    source c u z (queryVelocity c u) 0 = 4 * z * c * u ^ 2 / (1 - z * u ^ 2) ∧
    source c u z 0 (cutVelocity u) = -(4 * z * c * u ^ 2 / (1 - z * u ^ 2)) ∧
    source c u z (queryVelocity c u) (cutVelocity u) = 0 := by
  have hquery :
      source c u z (queryVelocity c u) 0 = 4 * z * c * u ^ 2 / (1 - z * u ^ 2) := by
    rw [source, escape_transpose_eq, query_velocity_source_term_eq]
    simp [resolvent, Matrix.trace, Matrix.diag, Matrix.mul_apply]
    field_simp [hden]
    ring
  have hcut :
      source c u z 0 (cutVelocity u) = -(4 * z * c * u ^ 2 / (1 - z * u ^ 2)) := by
    rw [source, escape_transpose_eq, cut_velocity_source_term_eq]
    simp [resolvent, Matrix.trace, Matrix.diag, Matrix.mul_apply]
    field_simp [hden]
    ring
  have hjoint :
      source c u z (queryVelocity c u) (cutVelocity u) = 0 := by
    rw [source, escape_transpose_eq, joint_velocity_source_term_eq]
    simp [resolvent, Matrix.trace, Matrix.diag, Matrix.mul_apply]
  refine ⟨?_, hquery, hcut, hjoint⟩
  ext i j
  fin_cases i <;> fin_cases j
  · simp [U, Matrix.mul_apply]
    nlinarith [hunit]
  · simp [U, Matrix.mul_apply]
    ring
  · simp [U, Matrix.mul_apply]
    ring
  · simp [U, Matrix.mul_apply]
    nlinarith [hunit]

theorem rational_query_cut_source_control :
    U (3 / 5) (4 / 5) * U (3 / 5) (4 / 5) = 1 ∧
    source (3 / 5) (4 / 5) (1 / 4)
      (queryVelocity (3 / 5) (4 / 5)) 0 = 16 / 35 ∧
    source (3 / 5) (4 / 5) (1 / 4) 0 (cutVelocity (4 / 5)) = -(16 / 35) ∧
    source (3 / 5) (4 / 5) (1 / 4)
      (queryVelocity (3 / 5) (4 / 5)) (cutVelocity (4 / 5)) = 0 := by
  have hunit : (3 / 5 : ℚ) ^ 2 + (4 / 5 : ℚ) ^ 2 = 1 := by norm_num
  have hden : (1 : ℚ) - (1 / 4) * (4 / 5) ^ 2 ≠ 0 := by norm_num
  have h := moving_cut_query_source_rows_cancel (3 / 5 : ℚ) (4 / 5) (1 / 4) hunit hden
  norm_num at h ⊢
  exact h

end D0.Geometry.MovingCutQueryCancellation
