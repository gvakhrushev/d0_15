import Mathlib.Tactic
import D0.Geometry.A4DScalarDeltaSecondJet
import D0.Geometry.ArchivePathWordAlgebra

/-!
# Scalar background action mixes spatial word length

On the cycle, `G_ξ = M_ξ D` and `h_ξ = Δ ξ` satisfy

`G_ξ U - U G_ξ = -½ M_{h_ξ} (U² - I)`.

The right-hand side is a site multiplier times the empty word plus a site
multiplier times the length-two word `U²`. The one-letter shift sector does
not contain the delta commutator. This is not a crossed constitutive law.
-/

namespace D0.Geometry

open Matrix
open scoped BigOperators

variable {n : ℕ} [NeZero n]

lemma shift_mul_shiftT : scalarCycleShift n * (scalarCycleShift n)ᵀ = 1 := by
  ext i j
  rw [Matrix.mul_apply, Finset.sum_eq_single (i + 1)]
  · simp only [scalarCycleShift, Matrix.transpose_apply, Matrix.one_apply]
    by_cases hij : i = j
    · simp [hij]
    · have hstep : i + 1 ≠ j + 1 := fun h => hij (add_right_cancel h)
      simp [hij, hstep]
  · intro k _ hk
    simp [scalarCycleShift, hk]
  · intro h
    exact absurd (Finset.mem_univ _) h

lemma shiftT_mul_shift : (scalarCycleShift n)ᵀ * scalarCycleShift n = 1 :=
  (mul_eq_one_comm).mp shift_mul_shiftT

lemma shift_sq_apply (i j : Fin n) :
    (scalarCycleShift n * scalarCycleShift n) i j =
      if j = i + 1 + 1 then (1 : ℚ) else 0 := by
  rw [Matrix.mul_apply, Finset.sum_eq_single (i + 1)]
  · simp [scalarCycleShift]
  · intro k _ hk
    simp [scalarCycleShift, hk]
  · intro h
    exact absurd (Finset.mem_univ _) h

lemma D_mul_shift :
    scalarCycleD n * scalarCycleShift n =
      ((n : ℚ) / 2) • (scalarCycleShift n * scalarCycleShift n - 1) := by
  rw [scalarCycleD, Matrix.smul_mul, sub_mul, shiftT_mul_shift]

lemma shift_mul_D :
    scalarCycleShift n * scalarCycleD n =
      ((n : ℚ) / 2) • (scalarCycleShift n * scalarCycleShift n - 1) := by
  rw [scalarCycleD, Matrix.mul_smul, mul_sub, shift_mul_shiftT]

lemma shift_mul_diagonal (v : Fin n → ℚ) :
    scalarCycleShift n * diagonal v =
      diagonal (fun i => v (i + 1)) * scalarCycleShift n := by
  ext i j
  simp only [Matrix.mul_diagonal, Matrix.diagonal_mul, scalarCycleShift]
  by_cases h : j = i + 1
  · simp [h]
  · simp [h]

lemma displacement_diagonal (v : Fin n → ℚ) :
    diagonal (fun i => v i - v (i + 1)) =
      (-(1 / (n : ℚ))) • diagonal (scalarDisplacement v) := by
  have hn0 : (n : ℚ) ≠ 0 := by exact_mod_cast (NeZero.ne n)
  ext i j
  by_cases hij : i = j
  · subst hij
    simp [Matrix.diagonal, scalarDisplacement, smul_eq_mul]
    field_simp
    ring
  · simp [Matrix.diagonal, hij]

lemma scaled_diagonal_mul_entry (c : ℚ) (v : Fin n → ℚ)
    (A : Matrix (Fin n) (Fin n) ℚ) (i j : Fin n) :
    (c • (diagonal v * A)) i j = c * v i * A i j := by
  rw [Matrix.smul_apply, Matrix.mul_apply, Finset.sum_eq_single i]
  · simp [Matrix.diagonal, mul_assoc]
  · intro k _ hk
    simp [Matrix.diagonal, hk.symm]
  · intro h
    exact absurd (Finset.mem_univ _) h

/-- Exact scalar word-length identity. `n` is the cycle length. -/
theorem scalarBackground_wordMixing (v : Fin n → ℚ) :
    scalarCycleG v * scalarCycleShift n - scalarCycleShift n * scalarCycleG v =
      (-(1 / 2 : ℚ)) •
        (scalarCycleMul (scalarDisplacement v) *
          (scalarCycleShift n * scalarCycleShift n - 1)) := by
  have hDU : scalarCycleD n * scalarCycleShift n = scalarCycleShift n * scalarCycleD n := by
    rw [D_mul_shift, shift_mul_D]
  rw [scalarCycleG, scalarCycleMul]
  have hleft :
      (diagonal v * scalarCycleD n) * scalarCycleShift n =
        diagonal v * (scalarCycleD n * scalarCycleShift n) := by
    rw [mul_assoc]
  have hright :
      scalarCycleShift n * (diagonal v * scalarCycleD n) =
        diagonal (fun i => v (i + 1)) * (scalarCycleShift n * scalarCycleD n) := by
    calc
      scalarCycleShift n * (diagonal v * scalarCycleD n) =
          (scalarCycleShift n * diagonal v) * scalarCycleD n := by rw [← mul_assoc]
      _ = (diagonal (fun i => v (i + 1)) * scalarCycleShift n) * scalarCycleD n := by
          rw [shift_mul_diagonal]
      _ = diagonal (fun i => v (i + 1)) * (scalarCycleShift n * scalarCycleD n) := by
          rw [mul_assoc]
  rw [hleft, hright, hDU, ← sub_mul, Matrix.diagonal_sub, ← hDU, displacement_diagonal,
    D_mul_shift, Matrix.smul_mul, Matrix.mul_smul, smul_smul]
  congr 1
  have hn0 : (n : ℚ) ≠ 0 := by exact_mod_cast (NeZero.ne n)
  field_simp [hn0]

theorem scalarBackground_wordMixing_split (v : Fin n → ℚ) :
    scalarCycleG v * scalarCycleShift n - scalarCycleShift n * scalarCycleG v =
      (1 / 2 : ℚ) • scalarCycleMul (scalarDisplacement v) +
        (-(1 / 2 : ℚ)) •
          (scalarCycleMul (scalarDisplacement v) *
            (scalarCycleShift n * scalarCycleShift n)) := by
  rw [scalarBackground_wordMixing, scalarCycleMul, mul_sub, Matrix.mul_one, smul_sub,
    sub_eq_add_neg]
  simp only [neg_smul, neg_neg]
  exact add_comm _ _

/-- Empty word and length-two word. Their maximum length is two. -/
def wordMixingExpression : PathExpr Unit :=
  .add (.word []) (.word [(), ()])

theorem wordMixingExpression_maxLength :
    (pathExprCost wordMixingExpression).maxWordLength = 2 := by
  simp [wordMixingExpression, pathExprCost]

theorem wordMixingExpression_not_single_word :
    ∀ w : List Unit, wordMixingExpression ≠ PathExpr.word w := by
  intro w
  simp [wordMixingExpression]

def oneLetterSector (M : Matrix (Fin n) (Fin n) ℚ) : Prop :=
  ∀ i j, M i j ≠ 0 → j = i + 1 ∨ i = j + 1

private lemma zero_ne_one_word (hn : 2 ≤ n) : (0 : Fin n) ≠ 1 := by
  intro h
  have hval := congrArg Fin.val h
  change 0 = 1 % n at hval
  rw [Nat.mod_eq_of_lt (by omega : 1 < n)] at hval
  omega

private lemma delta_displacement_at_zero (hn : 2 ≤ n) :
    scalarDisplacement (scalarSite (0 : Fin n)) (0 : Fin n) = - (n : ℚ) := by
  have h1 : (1 : Fin n) ≠ 0 := (zero_ne_one_word hn).symm
  simp [scalarDisplacement, scalarSite, h1]

private lemma shift_sq_zero_zero (hn : 3 ≤ n) :
    (scalarCycleShift n * scalarCycleShift n) (0 : Fin n) (0 : Fin n) = 0 := by
  rw [shift_sq_apply, ite_eq_right_iff]
  intro h
  have hval := congrArg Fin.val h
  have h0 : ((0 : Fin n).val) = 0 := rfl
  have h1 : ((1 : Fin n).val) = 1 := Nat.mod_eq_of_lt (by omega : 1 < n)
  have step1 : (((0 : Fin n) + 1).val) = 1 := by
    rw [Fin.val_add, h0, h1]
    exact Nat.mod_eq_of_lt (by omega : 1 < n)
  have step2 : (((0 : Fin n) + 1 + 1).val) = 2 := by
    rw [Fin.val_add, step1, h1]
    exact Nat.mod_eq_of_lt (by omega : 2 < n)
  rw [step2, h0] at hval
  omega

theorem delta_wordMixing_diagonal (hn : 3 ≤ n) :
    (scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleShift n -
        scalarCycleShift n * scalarCycleG (scalarSite (0 : Fin n)))
        (0 : Fin n) (0 : Fin n) = - (n : ℚ) / 2 := by
  rw [scalarBackground_wordMixing, scalarCycleMul]
  rw [scaled_diagonal_mul_entry]
  rw [delta_displacement_at_zero (Nat.le_trans (by decide) hn)]
  have hsq := shift_sq_zero_zero hn
  simp only [Matrix.sub_apply, Matrix.one_apply, hsq, if_true]
  ring

/-- The delta commutator has a nonzero on-site entry, so it is not a one-letter shift. -/
theorem delta_wordMixing_not_oneLetter (hn : 3 ≤ n) :
    ¬ oneLetterSector
        (scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleShift n -
          scalarCycleShift n * scalarCycleG (scalarSite (0 : Fin n))) := by
  intro hsec
  have hdiag := delta_wordMixing_diagonal hn
  have hn0 : (n : ℚ) ≠ 0 := by exact_mod_cast (NeZero.ne n)
  have hne : - (n : ℚ) / 2 ≠ 0 := div_ne_zero (neg_ne_zero.mpr hn0) (by norm_num)
  have hentry := hne
  rw [← hdiag] at hentry
  have hsup := hsec (0 : Fin n) (0 : Fin n) hentry
  rcases hsup with h | h
  · exact zero_ne_one_word (Nat.le_trans (by decide) hn) (by simpa using h)
  · exact zero_ne_one_word (Nat.le_trans (by decide) hn) (by simpa using h)

private lemma two_as_double_step (hn : 3 ≤ n) : (2 : Fin n) = (0 : Fin n) + 1 + 1 := by
  apply Fin.ext
  have hL : ((2 : Fin n).val) = 2 := Nat.mod_eq_of_lt (by omega : 2 < n)
  have h1 : ((1 : Fin n).val) = 1 := Nat.mod_eq_of_lt (by omega : 1 < n)
  have hR : (((0 : Fin n) + 1 + 1).val) = 2 := by
    rw [Fin.val_add, Fin.val_add, show ((0 : Fin n).val) = 0 from rfl, h1]
    rw [Nat.mod_eq_of_lt (by omega : 1 < n)]
    exact Nat.mod_eq_of_lt (by omega : 2 < n)
  rw [hL, hR]

theorem delta_wordMixing_lengthTwo (hn : 4 ≤ n) :
    (scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleShift n -
        scalarCycleShift n * scalarCycleG (scalarSite (0 : Fin n)))
        (0 : Fin n) (2 : Fin n) = (n : ℚ) / 2 := by
  have h3 : 3 ≤ n := Nat.le_trans (by decide) hn
  rw [scalarBackground_wordMixing, scalarCycleMul, scaled_diagonal_mul_entry,
    delta_displacement_at_zero (Nat.le_trans (by decide) hn)]
  have hsq : (scalarCycleShift n * scalarCycleShift n) (0 : Fin n) (2 : Fin n) = 1 := by
    rw [two_as_double_step h3, shift_sq_apply]
    simp
  have hdiag : (1 : Matrix (Fin n) (Fin n) ℚ) (0 : Fin n) (2 : Fin n) = 0 := by
    have hne : (0 : Fin n) ≠ 2 := by
      intro h
      have hval := congrArg Fin.val h
      rw [show ((0 : Fin n).val) = 0 from rfl,
        show ((2 : Fin n).val) = 2 from Nat.mod_eq_of_lt (by omega : 2 < n)] at hval
      omega
    simp [hne]
  simp [Matrix.sub_apply, hsq, hdiag]
  ring

theorem delta_lengthTwo_outside_oneLetter (hn : 4 ≤ n) :
    ¬ ((2 : Fin n) = (0 : Fin n) + 1 ∨ (0 : Fin n) = (2 : Fin n) + 1) := by
  intro h
  rcases h with h | h
  · have hval := congrArg Fin.val h
    have h2 : ((2 : Fin n).val) = 2 := Nat.mod_eq_of_lt (by omega : 2 < n)
    have h1 : ((1 : Fin n).val) = 1 := Nat.mod_eq_of_lt (by omega : 1 < n)
    have h0 : ((0 : Fin n).val) = 0 := rfl
    have hstep : (((0 : Fin n) + 1).val) = 1 := by
      rw [Fin.val_add, h0, h1]
      exact Nat.mod_eq_of_lt (by omega : 1 < n)
    rw [h2, hstep] at hval
    omega
  · have hval := congrArg Fin.val h
    have h0 : ((0 : Fin n).val) = 0 := rfl
    have h2 : ((2 : Fin n).val) = 2 := Nat.mod_eq_of_lt (by omega : 2 < n)
    have h1 : ((1 : Fin n).val) = 1 := Nat.mod_eq_of_lt (by omega : 1 < n)
    have hstep : (((2 : Fin n) + 1).val) = 3 := by
      rw [Fin.val_add, h2, h1]
      exact Nat.mod_eq_of_lt (by omega : 3 < n)
    rw [h0, hstep] at hval
    omega

/-- On the delta orbit the diagonal comes from the empty word and the `(0,2)`
entry comes from the length-two word. -/
theorem delta_wordMixing_empty_and_lengthTwo (hn : 4 ≤ n) :
    (scalarCycleShift n * scalarCycleShift n) (0 : Fin n) (0 : Fin n) = 0 ∧
      (1 : Matrix (Fin n) (Fin n) ℚ) (0 : Fin n) (0 : Fin n) = 1 ∧
      (scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleShift n -
          scalarCycleShift n * scalarCycleG (scalarSite (0 : Fin n)))
          (0 : Fin n) (0 : Fin n) = - (n : ℚ) / 2 ∧
      (scalarCycleShift n * scalarCycleShift n) (0 : Fin n) (2 : Fin n) = 1 ∧
      (1 : Matrix (Fin n) (Fin n) ℚ) (0 : Fin n) (2 : Fin n) = 0 ∧
      (scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleShift n -
          scalarCycleShift n * scalarCycleG (scalarSite (0 : Fin n)))
          (0 : Fin n) (2 : Fin n) = (n : ℚ) / 2 ∧
      ¬ ((2 : Fin n) = (0 : Fin n) + 1 ∨ (0 : Fin n) = (2 : Fin n) + 1) := by
  have h3 : 3 ≤ n := Nat.le_trans (by decide) hn
  refine ⟨shift_sq_zero_zero h3, ?_, delta_wordMixing_diagonal h3, ?_, ?_,
    delta_wordMixing_lengthTwo hn, delta_lengthTwo_outside_oneLetter hn⟩
  · simp
  · rw [two_as_double_step h3, shift_sq_apply]
    simp
  · have hne : (0 : Fin n) ≠ 2 := by
      intro h
      have hval := congrArg Fin.val h
      rw [show ((0 : Fin n).val) = 0 from rfl,
        show ((2 : Fin n).val) = 2 from Nat.mod_eq_of_lt (by omega : 2 < n)] at hval
      omega
    simp [hne]

/-- Nondelta control: the same identity holds where `G²` does not vanish. -/
theorem nondelta_wordMixing (hn : 3 ≤ n) :
    scalarCycleG (scalarNondelta (n := n)) * scalarCycleShift n -
        scalarCycleShift n * scalarCycleG (scalarNondelta (n := n)) =
      (-(1 / 2 : ℚ)) •
        (scalarCycleMul (scalarDisplacement (scalarNondelta (n := n))) *
          (scalarCycleShift n * scalarCycleShift n - 1)) ∧
      scalarCycleG (scalarNondelta (n := n)) *
          scalarCycleG (scalarNondelta (n := n)) ≠ 0 :=
  ⟨scalarBackground_wordMixing (scalarNondelta (n := n)),
    nondelta_G_sq_ne_zero (n := n) hn⟩

end D0.Geometry
