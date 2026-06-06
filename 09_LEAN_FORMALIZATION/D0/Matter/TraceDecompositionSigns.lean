import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

set_option linter.unusedSectionVars false

open scoped BigOperators

namespace D0.Matter

variable {n : Type} [Fintype n] [DecidableEq n]

noncomputable def diagPart (M : Matrix n n ℝ) : Matrix n n ℝ :=
  fun i j => if i = j then M i j else 0

noncomputable def symmOffDiagPart (M : Matrix n n ℝ) : Matrix n n ℝ :=
  fun i j => if i = j then 0 else (1 / 2 : ℝ) * (M i j + M j i)

noncomputable def skewPart (M : Matrix n n ℝ) : Matrix n n ℝ :=
  fun i j => if i = j then 0 else (1 / 2 : ℝ) * (M i j - M j i)

theorem matrix_decomposition (M : Matrix n n ℝ) :
    M = diagPart M + symmOffDiagPart M + skewPart M := by
  ext i j
  unfold diagPart symmOffDiagPart skewPart
  dsimp
  split_ifs with hij
  · subst j; ring
  · ring

theorem interaction_trace_sign_audit (Γ X : Matrix n n ℝ) :
    Matrix.trace (Γ * X) =
      Matrix.trace (diagPart Γ * diagPart X) +
      Matrix.trace (symmOffDiagPart Γ * symmOffDiagPart X) +
      Matrix.trace (skewPart Γ * skewPart X) := by
  unfold Matrix.trace Matrix.diag
  simp_rw [Matrix.mul_apply]
  -- Key symmetry lemma: swapping i↔j in the off-diagonal sum
  have h_comm : (∑ i : n, ∑ j : n, if i = j then 0 else Γ j i * X i j) =
      (∑ i : n, ∑ j : n, if i = j then 0 else Γ i j * X j i) := by
    rw [Finset.sum_comm]
    congr 1; ext x; congr 1; ext y
    by_cases h : x = y
    · subst h; rfl
    · rw [if_neg (ne_comm.mp h), if_neg h]
  -- Split LHS into diagonal + off-diagonal
  have h_split_lhs : (∑ i : n, ∑ j : n, Γ i j * X j i) =
      (∑ i : n, Γ i i * X i i) +
      (∑ i : n, ∑ j : n, if i = j then 0 else Γ i j * X j i) := by
    simp_rw [← Finset.sum_add_distrib]
    congr 1; ext i
    have : (∑ j : n, Γ i j * X j i) =
        (∑ j : n, if i = j then Γ i j * X j i else 0) +
        (∑ j : n, if i = j then 0 else Γ i j * X j i) := by
      rw [← Finset.sum_add_distrib]
      congr 1; ext j
      split_ifs <;> ring
    rw [this]
    congr 1
    rw [Finset.sum_eq_single i (fun j _ hne => by rw [if_neg hne.symm])
        (fun h => absurd (Finset.mem_univ i) h)]
    rw [if_pos rfl]
  -- RHS diagonal/symm/skew decomposition
  have h_diag_eq : ∀ i j : n,
      (diagPart Γ) i j * (diagPart X) j i = if i = j then Γ i i * X i i else 0 := by
    intro i j
    unfold diagPart
    by_cases h : i = j
    · subst h; simp
    · have hne : j ≠ i := ne_comm.mp h
      simp [h, hne]
  have h_symm_skew_eq : ∀ i j : n,
      (symmOffDiagPart Γ) i j * (symmOffDiagPart X) j i +
      (skewPart Γ) i j * (skewPart X) j i =
      if i = j then 0 else (1 / 2 : ℝ) * (Γ i j * X j i + Γ j i * X i j) := by
    intro i j
    unfold symmOffDiagPart skewPart
    by_cases h : i = j
    · subst h; simp
    · have hne : j ≠ i := ne_comm.mp h
      simp [h, hne]
      ring
  simp_rw [← Finset.sum_add_distrib]
  simp_rw [h_diag_eq]
  simp_rw [add_assoc]
  simp_rw [h_symm_skew_eq]
  -- Collapse the conditional diagonal sum
  have h_sum_diag : ∀ i : n,
      (∑ j : n, if i = j then Γ i i * X i i else 0) = Γ i i * X i i := fun i =>
    Finset.sum_eq_single i (fun j _ hne => by rw [if_neg hne.symm])
      (fun h => absurd (Finset.mem_univ i) h) |>.trans (by rw [if_pos rfl])
  simp_rw [Finset.sum_add_distrib]
  simp_rw [h_sum_diag]
  rw [h_split_lhs]
  congr 1
  -- Fold (1/2)*(A + B) symmetry using h_comm
  have h_S2_eq : (∑ i : n, ∑ j : n,
        if i = j then 0 else (1 / 2 : ℝ) * (Γ i j * X j i + Γ j i * X i j)) =
      ∑ i : n, ∑ j : n, if i = j then 0 else Γ i j * X j i := by
    have split2 : ∀ i j : n,
        (if i = j then (0 : ℝ) else (1/2) * (Γ i j * X j i + Γ j i * X i j)) =
        (1/2) * (if i = j then 0 else Γ i j * X j i) +
        (1/2) * (if i = j then 0 else Γ j i * X i j) := fun i j => by
      split_ifs <;> ring
    simp_rw [split2, Finset.sum_add_distrib, ← Finset.mul_sum, h_comm]
    ring
  exact h_S2_eq.symm
 
theorem frobenius_trace_sign_audit (Γ X : Matrix n n ℝ) :
    Matrix.trace (Γ.transpose * X) =
      Matrix.trace (diagPart Γ * diagPart X) +
      Matrix.trace (symmOffDiagPart Γ * symmOffDiagPart X) -
      Matrix.trace (skewPart Γ * skewPart X) := by
  rw [interaction_trace_sign_audit Γ.transpose X]
  have h_diag : diagPart (Γ.transpose) = diagPart Γ := by
    ext i j
    simp only [diagPart, Matrix.transpose_apply]
    by_cases h : i = j
    · subst h; rfl
    · rw [if_neg h, if_neg h]
  have h_symm : symmOffDiagPart (Γ.transpose) = symmOffDiagPart Γ := by
    ext i j
    simp only [symmOffDiagPart, Matrix.transpose_apply]
    by_cases h : i = j
    · subst h; rfl
    · rw [if_neg h, if_neg h]; ring
  have h_skew : skewPart (Γ.transpose) = - skewPart Γ := by
    ext i j
    simp only [skewPart, Matrix.neg_apply, Matrix.transpose_apply]
    by_cases h : i = j
    · subst h; simp
    · rw [if_neg h, if_neg h]; ring
  rw [h_diag, h_symm, h_skew]
  have h_skew_mul : (- skewPart Γ) * skewPart X = - (skewPart Γ * skewPart X) := by
    rw [Matrix.neg_mul]
  rw [h_skew_mul, Matrix.trace_neg]
  ring

end D0.Matter
