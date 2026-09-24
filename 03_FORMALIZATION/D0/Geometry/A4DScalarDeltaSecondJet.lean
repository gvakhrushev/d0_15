import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Geometry.A4DSecondOrderCartanCongruence

/-!
# Scalar cycle second jet

On the cycle of length `L ≥ 3`, with `U f(x) = f(x+1)`,
`D = L/2 (U - U⁻¹)`, `Δ = L (U - I)` and `G = M_ξ D`, the delta field
`ξ = δ₀` has `G² = (Gᵀ)² = 0` and a completely determined symmetric block.
The numbers `25/4`, `-25 c` and `-25/2` are the `L = 5` case.

`diag H₀(a) = 0` for every acceleration, and for `L ≥ 4` the distance-two
entries `H₀(a)_{1,-1}` vanish as well. The exponential law and the zero second
jet therefore fail for every rational coefficient `c`, including `c = 0`.
Under the explicit hypothesis that the quadratic form of the constant vector
is fixed, both reference coefficients `c = 1` and `c = 2` fail, and the
diagonal ansatz forces `c = 0`. That value is not a completed physical action.

No canonical `K` is chosen. The antisymmetric part stays free.
-/

namespace D0.Geometry

open Matrix
open scoped BigOperators
open TwoJet

set_option linter.unusedSimpArgs false
set_option linter.unusedSectionVars false

variable {n : ℕ} [NeZero n]

/-- Cycle shift `(U f)(x) = f(x+1)`. -/
def scalarCycleShift (n : ℕ) [NeZero n] : Matrix (Fin n) (Fin n) ℚ :=
  fun i j => if j = i + 1 then 1 else 0

/-- Skew difference `D = L/2 (U - U⁻¹)`. -/
def scalarCycleD (n : ℕ) [NeZero n] : Matrix (Fin n) (Fin n) ℚ :=
  ((n : ℚ) / 2) • (scalarCycleShift n - (scalarCycleShift n)ᵀ)

/-- Forward difference `Δ = L (U - I)`. -/
def scalarCycleDelta (n : ℕ) [NeZero n] : Matrix (Fin n) (Fin n) ℚ :=
  (n : ℚ) • (scalarCycleShift n - 1)

/-- Pointwise multiplication `M_v`. -/
def scalarCycleMul (v : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  diagonal v

/-- Cartan tangent `G = M_ξ D`. -/
def scalarCycleG (v : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  scalarCycleMul v * scalarCycleD n

/-- Scalar first jet `H₀(a) = (M_a U + U⁻¹ M_a) / 2`. -/
def scalarCycleH0 (a : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  (1 / 2 : ℚ) •
    (scalarCycleMul a * scalarCycleShift n + (scalarCycleShift n)ᵀ * scalarCycleMul a)

/-- Site indicator. -/
def scalarSite (k : Fin n) : Fin n → ℚ :=
  fun i => if i = k then 1 else 0

/-- `h = Δ ξ`. -/
def scalarDisplacement (v : Fin n → ℚ) : Fin n → ℚ :=
  fun i => (n : ℚ) * (v (i + 1) - v i)

def scalarOnes (n : ℕ) : Fin n → ℚ := fun _ => 1

def scalarConstantForm (M : Matrix (Fin n) (Fin n) ℚ) : ℚ :=
  ∑ i, ∑ j, M i j

private lemma val_one_ge_two (hn : 2 ≤ n) : ((1 : Fin n).val) = 1 := by
  have hlt : 1 < n := by omega
  change (1 % n) = 1
  exact Nat.mod_eq_of_lt hlt

private lemma val_neg_one (hn : 1 ≤ n) : ((-1 : Fin n).val) = n - 1 := by
  obtain ⟨k, hk⟩ : ∃ k, n = k + 1 := ⟨n - 1, by omega⟩
  subst hk
  simpa using (Fin.coe_neg_one (n := k))

private lemma zero_ne_one (hn : 2 ≤ n) : (0 : Fin n) ≠ 1 := by
  intro h
  have := congrArg Fin.val h
  rw [val_one_ge_two hn] at this
  simp at this

private lemma zero_ne_neg_one (hn : 2 ≤ n) : (0 : Fin n) ≠ -1 := by
  intro h
  have := congrArg Fin.val h
  rw [val_neg_one (by omega : 1 ≤ n)] at this
  simp at this
  omega

private lemma one_ne_neg_one (hn : 3 ≤ n) : (1 : Fin n) ≠ -1 := by
  intro h
  have := congrArg Fin.val h
  rw [val_one_ge_two (by omega), val_neg_one (by omega : 1 ≤ n)] at this
  omega

private lemma two_ne_zero (hn : 3 ≤ n) : (2 : Fin n) ≠ 0 := by
  intro h
  have hdiv : n ∣ 2 := (Fin.natCast_eq_zero (n := n) (a := 2)).mp h
  have : n ≤ 2 := Nat.le_of_dvd (by omega) hdiv
  omega

private lemma one_add_one (hn : 2 ≤ n) : (1 + 1 : Fin n) = 2 := by
  apply Fin.ext
  rw [Fin.val_add, val_one_ge_two hn]
  exact congrArg (fun k : ℕ => k % n) (show (1 + 1) = 2 from rfl)

private lemma two_add_one (hn : 3 ≤ n) : ((2 : Fin n) + 1) = 3 := by
  apply Fin.ext
  rw [Fin.val_add, val_one_ge_two (Nat.le_trans (by decide) hn)]
  have h2 : 2 < n := Nat.lt_of_succ_le hn
  change (2 % n + 1) % n = 3 % n
  rw [Nat.mod_eq_of_lt h2]

private lemma not_two_step (hn : 3 ≤ n) (i : Fin n) : (i + 1) + 1 ≠ i := by
  intro h
  have hleft : ((i + 1) + 1) - i = (1 + 1 : Fin n) := by abel
  have hsub : ((i + 1) + 1) - i = 0 := by rw [h]; simp
  have : (1 + 1 : Fin n) = 0 := by rw [← hleft, hsub]
  rw [one_add_one (by omega)] at this
  exact two_ne_zero hn this

private lemma pred_of_succ_zero {i : Fin n} (h : i + 1 = 0) : i = -1 := by
  calc
    i = (i + 1) + (-1 : Fin n) := by abel
    _ = 0 + (-1 : Fin n) := by rw [h]
    _ = -1 := by simp

private lemma one_succ_ne_zero (hn : 3 ≤ n) : (1 : Fin n) + 1 ≠ 0 := by
  intro h
  exact two_ne_zero hn (by rw [← one_add_one (by omega)]; exact h)

private lemma neg_one_ne_two (hn : 4 ≤ n) : (-1 : Fin n) ≠ (1 : Fin n) + 1 := by
  intro h
  have h2 : (2 : Fin n) = -1 := by
    rw [← one_add_one (by omega)]
    exact h.symm
  have h3 : (3 : Fin n) = 0 := by
    calc
      (3 : Fin n) = (2 : Fin n) + 1 := (two_add_one (by omega)).symm
      _ = (-1 : Fin n) + 1 := by rw [h2]
      _ = 0 := by simp
  have hdiv : n ∣ 3 := (Fin.natCast_eq_zero (n := n) (a := 3)).mp h3
  have : n ≤ 3 := Nat.le_of_dvd (by omega) hdiv
  omega

private lemma one_ne_neg_one_succ (hn : 2 ≤ n) : (1 : Fin n) ≠ -1 + 1 := by
  intro h
  exact (zero_ne_one hn).symm (by simpa using h)

private lemma shift_apply (i j : Fin n) :
    scalarCycleShift n i j = if j = i + 1 then (1 : ℚ) else 0 := by
  simp [scalarCycleShift]

private lemma diagonal_mul_apply (v : Fin n → ℚ) (M : Matrix (Fin n) (Fin n) ℚ)
    (i j : Fin n) : (diagonal v * M) i j = v i * M i j := by
  rw [Matrix.mul_apply, Finset.sum_eq_single i]
  · simp [Matrix.diagonal]
  · intro k _ hk
    simp [Matrix.diagonal, hk.symm]
  · intro h
    exact absurd (Finset.mem_univ _) h

private lemma mul_diagonal_apply (M : Matrix (Fin n) (Fin n) ℚ) (v : Fin n → ℚ)
    (i j : Fin n) : (M * diagonal v) i j = M i j * v j := by
  rw [Matrix.mul_apply, Finset.sum_eq_single j]
  · simp [Matrix.diagonal]
  · intro k _ hk
    simp [Matrix.diagonal, hk]
  · intro h
    exact absurd (Finset.mem_univ _) h

private lemma transpose_shift_apply (i j : Fin n) :
    (scalarCycleShift n)ᵀ i j = if i = j + 1 then (1 : ℚ) else 0 := by
  simp [Matrix.transpose_apply, shift_apply]

lemma D_apply (i j : Fin n) :
    scalarCycleD n i j =
      ((n : ℚ) / 2) * (scalarCycleShift n i j - scalarCycleShift n j i) := by
  simp [scalarCycleD, Matrix.smul_apply, Matrix.sub_apply, Matrix.transpose_apply]

private lemma shift_diagonal_zero (hn : 2 ≤ n) (i : Fin n) :
    scalarCycleShift n i i = 0 := by
  rw [shift_apply]
  simp only [ite_eq_right_iff]
  intro h
  have : (0 : Fin n) = 1 := by
    calc
      (0 : Fin n) = i - i := by simp
      _ = (i + 1) - i := by rw [← h]
      _ = 1 := by abel
  exact (zero_ne_one hn this).elim

lemma D_diagonal (hn : 2 ≤ n) (i : Fin n) : scalarCycleD n i i = 0 := by
  rw [D_apply]
  simp [shift_diagonal_zero hn]

lemma D_forward (hn : 3 ≤ n) (i : Fin n) :
    scalarCycleD n i (i + 1) = (n : ℚ) / 2 := by
  rw [D_apply]
  have hfwd : scalarCycleShift n i (i + 1) = 1 := by simp [shift_apply]
  have hrev : scalarCycleShift n (i + 1) i = 0 := by
    rw [shift_apply]
    simp only [ite_eq_right_iff]
    intro h
    exact (not_two_step hn i h.symm).elim
  simp [hfwd, hrev]

lemma D_backward (hn : 3 ≤ n) (i : Fin n) :
    scalarCycleD n i (i - 1) = -((n : ℚ) / 2) := by
  rw [D_apply]
  have hrev : scalarCycleShift n (i - 1) i = 1 := by
    have hstep : i = (i - 1) + 1 := by simp
    rw [shift_apply, if_pos hstep]
  have hfwd : scalarCycleShift n i (i - 1) = 0 := by
    rw [shift_apply]
    simp only [ite_eq_right_iff]
    intro h
    have hstep : (i + 1) + 1 = i := by
      have : i + 1 = i - 1 := h.symm
      calc
        (i + 1) + 1 = (i - 1) + 1 := by rw [this]
        _ = i := by simp
    exact (not_two_step hn i hstep).elim
  simp [hfwd, hrev]

lemma D_backward_succ (hn : 3 ≤ n) (i : Fin n) :
    scalarCycleD n (i + 1) i = -((n : ℚ) / 2) := by
  simpa [add_sub_cancel_right] using D_backward hn (i + 1)

lemma D_forward_pred (hn : 3 ≤ n) (i : Fin n) :
    scalarCycleD n (i - 1) i = (n : ℚ) / 2 := by
  simpa [sub_add_cancel] using D_forward hn (i - 1)

lemma neighbor_exclusive (hn : 3 ≤ n) (i : Fin n) : i + 1 ≠ i - 1 := by
  intro h
  have hstep : (i + 1) + 1 = i := by
    calc
      (i + 1) + 1 = (i - 1) + 1 := by rw [h]
      _ = i := by simp
  exact not_two_step hn i hstep

lemma D_off (hn : 3 ≤ n) (i j : Fin n) (hf : j ≠ i + 1) (hb : j ≠ i - 1) :
    scalarCycleD n i j = 0 := by
  rw [D_apply]
  have h1 : scalarCycleShift n i j = 0 := by simp [shift_apply, hf]
  have h2 : scalarCycleShift n j i = 0 := by
    rw [shift_apply]
    simp only [ite_eq_right_iff]
    intro h
    have hj : j = i - 1 := by
      calc
        j = (j + 1) - 1 := by simp
        _ = i - 1 := by rw [h]
    exact (hb hj).elim
  simp [h1, h2]

private lemma D_zero_one (hn : 3 ≤ n) :
    scalarCycleD n (0 : Fin n) 1 = (n : ℚ) / 2 := by
  simpa using D_forward hn (0 : Fin n)

private lemma D_one_zero (hn : 3 ≤ n) :
    scalarCycleD n (1 : Fin n) 0 = -((n : ℚ) / 2) := by
  simpa using D_backward_succ hn (0 : Fin n)

private lemma D_zero_neg_one (hn : 3 ≤ n) :
    scalarCycleD n (0 : Fin n) (-1) = -((n : ℚ) / 2) := by
  have h : (-1 : Fin n) = (0 : Fin n) - 1 := by simp
  rw [h]
  exact D_backward hn 0

lemma scalarCycleG_apply (v : Fin n → ℚ) (i j : Fin n) :
    scalarCycleG v i j = v i * scalarCycleD n i j := by
  rw [scalarCycleG, scalarCycleMul, diagonal_mul_apply]

lemma scalarCycleH0_diagonal (hn : 2 ≤ n) (a : Fin n → ℚ) (i : Fin n) :
    scalarCycleH0 a i i = 0 := by
  have hU : scalarCycleShift n i i = 0 := shift_diagonal_zero hn i
  have hleft : (scalarCycleMul a * scalarCycleShift n) i i = 0 := by
    rw [scalarCycleMul, diagonal_mul_apply, hU]
    ring
  have hright : ((scalarCycleShift n)ᵀ * scalarCycleMul a) i i = 0 := by
    rw [scalarCycleMul, mul_diagonal_apply, Matrix.transpose_apply, hU]
    ring
  simp [scalarCycleH0, Matrix.smul_apply, Matrix.add_apply, hleft, hright]

private lemma scalarCycleH0_off (a : Fin n → ℚ) (i j : Fin n)
    (hf : j ≠ i + 1) (hb : i ≠ j + 1) : scalarCycleH0 a i j = 0 := by
  have hL : (scalarCycleMul a * scalarCycleShift n) i j = 0 := by
    rw [scalarCycleMul, diagonal_mul_apply, shift_apply, if_neg hf]
    ring
  have hR : ((scalarCycleShift n)ᵀ * scalarCycleMul a) i j = 0 := by
    rw [scalarCycleMul, mul_diagonal_apply, transpose_shift_apply, if_neg hb]
    ring
  simp [scalarCycleH0, Matrix.smul_apply, Matrix.add_apply, hL, hR]

/-- For `L ≥ 4` the distance-two entries of every acceleration jet vanish. -/
theorem scalarCycleH0_distanceTwo (hn : 4 ≤ n) (a : Fin n → ℚ) :
    scalarCycleH0 a 1 (-1) = 0 ∧ scalarCycleH0 a (-1) 1 = 0 := by
  have hfar := neg_one_ne_two hn
  have hnear := one_ne_neg_one_succ (Nat.le_trans (by decide) hn)
  exact ⟨scalarCycleH0_off a 1 (-1) hfar hnear,
    scalarCycleH0_off a (-1) 1 hnear hfar⟩

/-- `H₀(Δξ) = -(G_ξ + G_ξᵀ)` on every scalar field, for `L ≥ 3`. -/
theorem scalarCycle_firstJet_eq_negative_symmetrized
    (hn : 3 ≤ n) (v : Fin n → ℚ) :
    scalarCycleH0 (scalarDisplacement v) = -(scalarCycleG v + (scalarCycleG v)ᵀ) := by
  ext i j
  by_cases hfwd : j = i + 1
  · subst hfwd
    have hL : (scalarCycleMul (scalarDisplacement v) * scalarCycleShift n) i (i + 1) =
        scalarDisplacement v i := by
      rw [scalarCycleMul, diagonal_mul_apply]
      simp [shift_apply]
    have hR : ((scalarCycleShift n)ᵀ * scalarCycleMul (scalarDisplacement v)) i (i + 1) = 0 := by
      rw [scalarCycleMul, mul_diagonal_apply, transpose_shift_apply, if_neg (not_two_step hn i).symm]
      ring
    have hGij : scalarCycleG v i (i + 1) = v i * ((n : ℚ) / 2) := by
      simp [scalarCycleG_apply, D_forward hn]
    have hGji : scalarCycleG v (i + 1) i = v (i + 1) * (-((n : ℚ) / 2)) := by
      simp [scalarCycleG_apply, D_backward_succ hn]
    simp only [scalarCycleH0, Matrix.smul_apply, Matrix.add_apply, Matrix.neg_apply,
      Matrix.transpose_apply, hL, hR, hGij, hGji, scalarDisplacement]
    ring
  · by_cases hbwd : j = i - 1
    · subst hbwd
      have hL : (scalarCycleMul (scalarDisplacement v) * scalarCycleShift n) i (i - 1) = 0 := by
        rw [scalarCycleMul, diagonal_mul_apply, shift_apply,
          if_neg (neighbor_exclusive hn i).symm]
        ring
      have hR : ((scalarCycleShift n)ᵀ * scalarCycleMul (scalarDisplacement v)) i (i - 1) =
          scalarDisplacement v (i - 1) := by
        rw [scalarCycleMul, mul_diagonal_apply, transpose_shift_apply]
        simp
      have hGij : scalarCycleG v i (i - 1) = v i * (-((n : ℚ) / 2)) := by
        simp [scalarCycleG_apply, D_backward hn]
      have hGji : scalarCycleG v (i - 1) i = v (i - 1) * ((n : ℚ) / 2) := by
        simp [scalarCycleG_apply, D_forward_pred hn]
      have hdisp : scalarDisplacement v (i - 1) = (n : ℚ) * (v i - v (i - 1)) := by
        simp [scalarDisplacement]
      simp only [scalarCycleH0, Matrix.smul_apply, Matrix.add_apply, Matrix.neg_apply,
        Matrix.transpose_apply, hL, hR, hGij, hGji, hdisp]
      ring
    · have hL : (scalarCycleMul (scalarDisplacement v) * scalarCycleShift n) i j = 0 := by
        rw [scalarCycleMul, diagonal_mul_apply, shift_apply, if_neg hfwd]
        ring
      have hR : ((scalarCycleShift n)ᵀ * scalarCycleMul (scalarDisplacement v)) i j = 0 := by
        rw [scalarCycleMul, mul_diagonal_apply, transpose_shift_apply, if_neg]
        · ring
        · intro h
          apply hbwd
          calc
            j = (j + 1) - 1 := by simp
            _ = i - 1 := by rw [h]
      have hDij : scalarCycleD n i j = 0 := D_off hn i j hfwd hbwd
      have hDji : scalarCycleD n j i = 0 := by
        have hf : i ≠ j + 1 := by
          intro h
          apply hbwd
          calc
            j = (j + 1) - 1 := by simp
            _ = i - 1 := by rw [h]
        have hb : i ≠ j - 1 := by
          intro h
          apply hfwd
          calc
            j = (j - 1) + 1 := by simp
            _ = i + 1 := by rw [h]
        exact D_off hn j i hf hb
      simp [scalarCycleH0, Matrix.smul_apply, Matrix.add_apply, Matrix.neg_apply,
        Matrix.transpose_apply, scalarCycleG_apply, hL, hR, hDij, hDji]

theorem scalarCycleG_sq_transpose (v : Fin n → ℚ) :
    (scalarCycleG v)ᵀ * (scalarCycleG v)ᵀ = (scalarCycleG v * scalarCycleG v)ᵀ := by
  simp [Matrix.transpose_mul]

theorem scalarDelta_G_sq (hn : 3 ≤ n) :
    scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleG (scalarSite 0) = 0 := by
  ext i j
  rw [Matrix.mul_apply, Matrix.zero_apply]
  refine Finset.sum_eq_zero ?_
  intro k _
  simp only [scalarCycleG_apply, scalarSite]
  by_cases hk : k = 0
  · subst hk
    by_cases hi : i = 0
    · simp [hi, D_diagonal (Nat.le_trans (by decide) hn)]
    · simp only [if_neg hi]
      ring
  · simp only [if_neg hk]
    ring

theorem scalarDelta_Gt_sq (hn : 3 ≤ n) :
    (scalarCycleG (scalarSite (0 : Fin n)))ᵀ *
      (scalarCycleG (scalarSite 0))ᵀ = 0 := by
  rw [scalarCycleG_sq_transpose, scalarDelta_G_sq hn, Matrix.transpose_zero]

theorem scalarDelta_GtG_apply (hn : 3 ≤ n) (i j : Fin n) :
    (((scalarCycleG (scalarSite (0 : Fin n)))ᵀ * scalarCycleG (scalarSite (0 : Fin n)) :
        Matrix (Fin n) (Fin n) ℚ) i j) =
      scalarCycleD n 0 i * scalarCycleD n 0 j := by
  rw [Matrix.mul_apply, Finset.sum_eq_single (0 : Fin n)]
  · simp [Matrix.transpose_apply, scalarCycleG_apply, scalarSite]
  · intro k _ hk
    simp only [Matrix.transpose_apply, scalarCycleG_apply, scalarSite, if_neg hk]
    ring
  · intro h
    exact absurd (Finset.mem_univ _) h

theorem scalarDelta_displacement_zero (hn : 2 ≤ n) :
    scalarDisplacement (scalarSite (0 : Fin n)) 0 = - (n : ℚ) := by
  have hstep : (0 : Fin n) + 1 ≠ 0 := by simpa using (zero_ne_one hn).symm
  simp only [scalarDisplacement, scalarSite, if_neg hstep, if_true]
  ring

theorem scalarDelta_displacement_minus (hn : 2 ≤ n) :
    scalarDisplacement (scalarSite (0 : Fin n)) (-1) = (n : ℚ) := by
  have hm : (-1 : Fin n) ≠ 0 := (zero_ne_neg_one hn).symm
  have hstep : (-1 : Fin n) + 1 = 0 := by simp
  simp only [scalarDisplacement, scalarSite, if_neg hm, hstep, if_true]
  ring

theorem scalarDelta_displacement_one (hn : 3 ≤ n) :
    scalarDisplacement (scalarSite (0 : Fin n)) 1 = 0 := by
  have h1 : (1 : Fin n) ≠ 0 := (zero_ne_one (by omega)).symm
  have h2 : (1 : Fin n) + 1 ≠ 0 := one_succ_ne_zero hn
  simp only [scalarDisplacement, scalarSite, if_neg h1, if_neg h2]
  ring

theorem scalarDelta_displacement_off (hn : 2 ≤ n) (i : Fin n) (hi : i ≠ 0) (hm : i ≠ -1) :
    scalarDisplacement (scalarSite (0 : Fin n)) i = 0 := by
  have hstep : i + 1 ≠ 0 := by
    intro h
    exact hm (pred_of_succ_zero h)
  simp only [scalarDisplacement, scalarSite, if_neg hi, if_neg hstep]
  ring

theorem scalarDelta_displacement_sq_sum (hn : 2 ≤ n) :
    (∑ i, scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2) = 2 * (n : ℚ) ^ 2 := by
  classical
  let f : Fin n → ℚ := fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2
  have hne := zero_ne_neg_one hn
  have hsup : ∀ i, i ≠ 0 → i ≠ -1 → f i = 0 := by
    intro i hi hm
    simp [f, scalarDelta_displacement_off hn i hi hm]
  have hsplit := Finset.sum_filter_add_sum_filter_not (s := Finset.univ)
    (p := fun i : Fin n => i = 0 ∨ i = -1) f
  have hrest : ∑ i ∈ Finset.univ.filter (fun i => ¬ (i = 0 ∨ i = -1)), f i = 0 := by
    apply Finset.sum_eq_zero
    intro i hi
    simp only [Finset.mem_filter, Finset.mem_univ, true_and, not_or] at hi
    exact hsup i hi.1 hi.2
  have hset : Finset.univ.filter (fun i : Fin n => i = 0 ∨ i = -1) = {0, -1} := by
    ext i
    simp [Finset.mem_filter]
  have htwo : ∑ i ∈ Finset.univ.filter (fun i => i = 0 ∨ i = -1), f i = f 0 + f (-1) := by
    rw [hset, Finset.sum_pair hne]
  have hz : f 0 = (n : ℚ) ^ 2 := by
    simp [f, scalarDelta_displacement_zero hn]
  have hm : f (-1) = (n : ℚ) ^ 2 := by
    simp [f, scalarDelta_displacement_minus hn]
  have hpair : ∑ i, f i = f 0 + f (-1) := by
    rw [← hsplit, hrest, htwo, add_zero]
  rw [hpair, hz, hm]
  ring

/-- On the delta orbit the symmetric jet required by covariance is
`GᵀG - c M_{h²} - H₀(a)/2`, because `G² = (Gᵀ)² = 0`. -/
theorem delta_kSym_of_covariance (hn : 3 ≤ n) (c : ℚ) (a : Fin n → ℚ)
    (K : Matrix (Fin n) (Fin n) ℚ)
    (hcov : scalarCycleH0 a + ((2 : ℚ) * c) •
        diagonal (fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2) =
      (TwoJet.mk (scalarCycleG (scalarSite 0)) K).secondOrderCongruenceCoefficient) :
    (1 / 2 : ℚ) • (Kᵀ + K) =
      (scalarCycleG (scalarSite 0))ᵀ * scalarCycleG (scalarSite 0) -
        c • diagonal (fun i => scalarDisplacement (scalarSite 0) i ^ 2) -
        (1 / 2 : ℚ) • scalarCycleH0 a := by
  set GtG : Matrix (Fin n) (Fin n) ℚ :=
    (scalarCycleG (scalarSite (0 : Fin n)))ᵀ * scalarCycleG (scalarSite (0 : Fin n))
  set H0 := scalarCycleH0 a
  set Dg := diagonal (fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2)
  have hcov' : H0 + ((2 : ℚ) * c) • Dg = (2 : ℚ) • GtG - (Kᵀ + K) := by
    simpa [GtG, H0, Dg, secondOrderCongruenceCoefficient_formula, scalarDelta_G_sq hn,
      scalarDelta_Gt_sq hn, mul_zero, zero_mul, smul_zero, add_zero] using hcov
  have hsum : H0 + ((2 : ℚ) * c) • Dg + (Kᵀ + K) = (2 : ℚ) • GtG := by
    rw [hcov']
    abel
  have hsym : Kᵀ + K = (2 : ℚ) • GtG - (H0 + ((2 : ℚ) * c) • Dg) := by
    have hsub := congrArg (fun M => M - (H0 + ((2 : ℚ) * c) • Dg)) hsum
    dsimp at hsub
    rw [add_sub_cancel_left] at hsub
    exact hsub
  have hc : (1 / 2 : ℚ) * ((2 : ℚ) * c) = c := by ring
  have h2 : (1 / 2 : ℚ) * 2 = 1 := by norm_num
  calc
    (1 / 2 : ℚ) • (Kᵀ + K) =
        (1 / 2 : ℚ) • ((2 : ℚ) • GtG - (H0 + ((2 : ℚ) * c) • Dg)) := by rw [hsym]
    _ = GtG - c • Dg - (1 / 2 : ℚ) • H0 := by
      simp only [smul_sub, smul_add, smul_smul, hc, h2, one_smul]
      abel

private def deltaHsq : Fin n → ℚ :=
  fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2

private def deltaKSym (c : ℚ) (a : Fin n → ℚ) : Matrix (Fin n) (Fin n) ℚ :=
  (scalarCycleG (scalarSite 0))ᵀ * scalarCycleG (scalarSite 0) -
    c • diagonal deltaHsq - (1 / 2 : ℚ) • scalarCycleH0 a

private lemma deltaKSym_a0 (hn : 3 ≤ n) (c : ℚ) (i j : Fin n) :
    deltaKSym c (0 : Fin n → ℚ) i j =
      scalarCycleD n 0 i * scalarCycleD n 0 j -
        c * (if i = j then deltaHsq i else 0) := by
  have hH : scalarCycleH0 (0 : Fin n → ℚ) = 0 := by
    ext a b
    simp [scalarCycleH0, scalarCycleMul, diagonal_zero, Matrix.zero_apply]
  by_cases hij : i = j
  · rw [hij]
    simp only [deltaKSym, hH, smul_zero, sub_zero, Matrix.sub_apply, Matrix.smul_apply,
      Matrix.zero_apply, Matrix.diagonal_apply, if_true, deltaHsq]
    rw [scalarDelta_GtG_apply hn]
    ring
  · simp only [deltaKSym, hH, smul_zero, sub_zero, Matrix.sub_apply, Matrix.smul_apply,
      Matrix.zero_apply, Matrix.diagonal_apply, if_neg hij, deltaHsq]
    rw [scalarDelta_GtG_apply hn]
    ring

theorem delta_Ksym_diag_plus (hn : 3 ≤ n) (c : ℚ) :
    deltaKSym c (0 : Fin n → ℚ) 1 1 = (n : ℚ) ^ 2 / 4 := by
  rw [deltaKSym_a0 hn]
  simp [D_zero_one hn, deltaHsq, scalarDelta_displacement_one hn]
  field_simp
  ring

theorem delta_Ksym_diag_zero (hn : 3 ≤ n) (c : ℚ) :
    deltaKSym c (0 : Fin n → ℚ) 0 0 = -c * (n : ℚ) ^ 2 := by
  rw [deltaKSym_a0 hn]
  simp [D_diagonal (Nat.le_trans (by decide) hn), deltaHsq, scalarDelta_displacement_zero (Nat.le_trans (by decide) hn)]

theorem delta_Ksym_diag_minus (hn : 3 ≤ n) (c : ℚ) :
    deltaKSym c (0 : Fin n → ℚ) (-1) (-1) = (n : ℚ) ^ 2 * (1 / 4 - c) := by
  rw [deltaKSym_a0 hn]
  simp [D_zero_neg_one hn, deltaHsq, scalarDelta_displacement_minus (Nat.le_trans (by decide) hn)]
  field_simp
  ring

theorem delta_Ksym_mixed (hn : 4 ≤ n) (c : ℚ) (a : Fin n → ℚ) :
    deltaKSym c a (1 : Fin n) (-1) = - (n : ℚ) ^ 2 / 4 ∧
      deltaKSym c a (-1) (1 : Fin n) = - (n : ℚ) ^ 2 / 4 := by
  obtain ⟨h1, h2⟩ := scalarCycleH0_distanceTwo hn a
  have h3 : 3 ≤ n := Nat.le_trans (by decide) hn
  constructor
  · have hdiag : (diagonal deltaHsq) (1 : Fin n) (-1) = 0 := by
      simp [Matrix.diagonal, one_ne_neg_one h3]
    simp only [deltaKSym, Matrix.sub_apply, Matrix.smul_apply, scalarDelta_GtG_apply h3,
      D_zero_one h3, D_zero_neg_one h3, hdiag, h1]
    field_simp
    ring
  · have hdiag : (diagonal deltaHsq) (-1) (1 : Fin n) = 0 := by
      simp [Matrix.diagonal, (one_ne_neg_one h3).symm]
    simp only [deltaKSym, Matrix.sub_apply, Matrix.smul_apply, scalarDelta_GtG_apply h3,
      D_zero_one h3, D_zero_neg_one h3, hdiag, h2]
    field_simp
    ring

theorem delta_Ksym_zero_cross (hn : 3 ≤ n) (c : ℚ) :
    deltaKSym c (0 : Fin n → ℚ) 0 1 = 0 ∧
      deltaKSym c (0 : Fin n → ℚ) 1 0 = 0 ∧
      deltaKSym c (0 : Fin n → ℚ) 0 (-1) = 0 ∧
      deltaKSym c (0 : Fin n → ℚ) (-1) 0 = 0 := by
  have hn1 : n ≠ 1 := by omega
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [deltaKSym_a0 hn, D_diagonal (Nat.le_trans (by decide) hn)]
    simp [zero_ne_one (Nat.le_trans (by decide) hn), hn1]
  · rw [deltaKSym_a0 hn, D_diagonal (Nat.le_trans (by decide) hn)]
    simp [(zero_ne_one (Nat.le_trans (by decide) hn)).symm, hn1]
  · rw [deltaKSym_a0 hn, D_diagonal (Nat.le_trans (by decide) hn)]
    simp [zero_ne_neg_one (Nat.le_trans (by decide) hn), hn1]
  · rw [deltaKSym_a0 hn, D_diagonal (Nat.le_trans (by decide) hn)]
    simp [(zero_ne_neg_one (Nat.le_trans (by decide) hn)).symm, hn1]

private lemma deltaHsq_outside (hn : 2 ≤ n) {i : Fin n} (hi : i ≠ 0) (hm : i ≠ -1) :
    deltaHsq i = 0 := by
  simp [deltaHsq, scalarDelta_displacement_off hn i hi hm]

private lemma D_outside (hn : 3 ≤ n) {j : Fin n} (hp : j ≠ 1) (hm : j ≠ -1) :
    scalarCycleD n (0 : Fin n) j = 0 := by
  have hf : j ≠ (0 : Fin n) + 1 := by simpa using hp
  have hb : j ≠ (0 : Fin n) - 1 := by simpa using hm
  exact D_off hn 0 j hf hb

theorem delta_Ksym_block_zero (hn : 3 ≤ n) (c : ℚ) (i j : Fin n)
    (hi : i ≠ 0 ∧ i ≠ 1 ∧ i ≠ -1) :
    deltaKSym c (0 : Fin n → ℚ) i j = 0 := by
  rw [deltaKSym_a0 hn]
  have hDi : scalarCycleD n 0 i = 0 := D_outside hn hi.2.1 hi.2.2
  have hsq : deltaHsq i = 0 :=
    deltaHsq_outside (Nat.le_trans (by decide) hn) hi.1 hi.2.2
  simp [hDi, hsq]

theorem delta_Ksym_block_zero_col (hn : 3 ≤ n) (c : ℚ) (i j : Fin n)
    (hj : j ≠ 0 ∧ j ≠ 1 ∧ j ≠ -1) :
    deltaKSym c (0 : Fin n → ℚ) i j = 0 := by
  rw [deltaKSym_a0 hn]
  have hDj : scalarCycleD n 0 j = 0 := D_outside hn hj.2.1 hj.2.2
  have hsq : i = j → deltaHsq i = 0 := by
    intro hij
    simpa [hij] using deltaHsq_outside (Nat.le_trans (by decide) hn) hj.1 hj.2.2
  by_cases hij : i = j
  · rw [hDj, hsq hij, hij]
    simp
  · rw [hDj]
    simp [hij]

/-- `L = 5` diagonal and mixed conditions. The mixed sum is `-25/2`. -/
theorem delta_L5_necessary_entries (c : ℚ) :
    deltaKSym (n := 5) c 0 1 1 = (25 : ℚ) / 4 ∧
      deltaKSym (n := 5) c 0 0 0 = -25 * c ∧
      deltaKSym (n := 5) c 0 (-1) (-1) = 25 * (1 / 4 - c) ∧
      deltaKSym (n := 5) c 0 1 (-1) + deltaKSym (n := 5) c 0 (-1) 1 = -25 / 2 := by
  have hn : 4 ≤ 5 := by omega
  have h3 : 3 ≤ 5 := by omega
  refine ⟨?_, ?_, ?_, ?_⟩
  · have h := delta_Ksym_diag_plus (n := 5) h3 c
    norm_num at h
    exact h
  · rw [delta_Ksym_diag_zero (n := 5) h3 c]
    ring
  · have h := delta_Ksym_diag_minus (n := 5) h3 c
    norm_num at h
    exact h
  · obtain ⟨h1, h2⟩ := delta_Ksym_mixed (n := 5) hn c 0
    rw [h1, h2]
    norm_num

/-- Every rational coefficient and every acceleration fails the exponential
second jet on the delta cycle. The site `+1` diagonal is `L²/2` on the right
and `0` on the left. -/
theorem deltaCartan_exponentialSecondOrder_noCellDiagonalCompletion
    (hn : 3 ≤ n) (c : ℚ) (a : Fin n → ℚ) :
    scalarCycleH0 a + ((2 : ℚ) * c) •
        diagonal (fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2) ≠
      (scalarCycleG (scalarSite 0))ᵀ * (scalarCycleG (scalarSite 0))ᵀ +
        (2 : ℚ) • ((scalarCycleG (scalarSite 0))ᵀ * scalarCycleG (scalarSite 0)) +
        scalarCycleG (scalarSite 0) * scalarCycleG (scalarSite 0) := by
  intro h
  have hentry := congr_fun (congr_fun h (1 : Fin n)) (1 : Fin n)
  have h2 : 2 ≤ n := Nat.le_trans (by decide) hn
  have hH : scalarCycleH0 a (1 : Fin n) (1 : Fin n) = 0 := scalarCycleH0_diagonal h2 a 1
  have hM : (diagonal (fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2))
      (1 : Fin n) (1 : Fin n) = 0 := by
    simp [Matrix.diagonal, scalarDelta_displacement_one hn]
  have hgtg := scalarDelta_GtG_apply hn (1 : Fin n) (1 : Fin n)
  rw [D_zero_one hn] at hgtg
  simp only [Matrix.add_apply, Matrix.smul_apply, hH, hM, scalarDelta_G_sq hn,
    scalarDelta_Gt_sq hn, Matrix.zero_apply, hgtg, add_zero, zero_add, smul_zero] at hentry
  have hn0 : (n : ℚ) ≠ 0 := by
    exact_mod_cast (Nat.ne_of_gt (Nat.zero_lt_of_lt (Nat.lt_of_succ_le hn)))
  have hsq : (n : ℚ) ^ 2 = 0 := by
    have := hentry.symm
    simp only [smul_eq_mul] at this
    field_simp at this
    simpa [mul_zero] using this
  exact hn0 (sq_eq_zero_iff.mp hsq)

theorem deltaCartan_zeroSecondJet_noCellDiagonalCompletion
    (hn : 3 ≤ n) (c : ℚ) (a : Fin n → ℚ) :
    scalarCycleH0 a + ((2 : ℚ) * c) •
        diagonal (fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2) ≠
      (TwoJet.mk (scalarCycleG (scalarSite (0 : Fin n))) 0).secondOrderCongruenceCoefficient := by
  rw [secondOrderCongruenceCoefficient_formula]
  simpa [scalarDelta_G_sq hn, scalarDelta_Gt_sq hn, mul_zero, zero_mul, smul_zero, add_zero,
    sub_zero] using deltaCartan_exponentialSecondOrder_noCellDiagonalCompletion hn c a

/-- Nondelta field `ξ = δ₀ + 2 δ₁`. Its square does not vanish. -/
def scalarNondelta : Fin n → ℚ :=
  fun i => if i = 0 then 1 else if i = 1 then 2 else 0

theorem nondelta_G_sq_entry (hn : 3 ≤ n) :
    ((scalarCycleG scalarNondelta * scalarCycleG scalarNondelta : Matrix (Fin n) (Fin n) ℚ)
        (0 : Fin n) (2 : Fin n)) =
      (n : ℚ) ^ 2 / 2 := by
  rw [Matrix.mul_apply, Finset.sum_eq_single (1 : Fin n)]
  · simp only [scalarCycleG_apply, scalarNondelta, D_zero_one hn]
    have h12 : scalarCycleD n (1 : Fin n) (2 : Fin n) = (n : ℚ) / 2 := by
      have htwo : (2 : Fin n) = (1 : Fin n) + 1 :=
        (one_add_one (Nat.le_trans (by decide) hn)).symm
      rw [htwo]
      exact D_forward hn 1
    have hn1 : n ≠ 1 := by omega
    simp [h12, hn1]
    ring_nf
  · intro k _ hk
    simp only [scalarCycleG_apply, scalarNondelta]
    by_cases hk0 : k = 0
    · simp [hk0, D_diagonal (Nat.le_trans (by decide) hn)]
    · simp [hk0, hk]
  · intro h
    exact absurd (Finset.mem_univ _) h

theorem nondelta_G_sq_ne_zero (hn : 3 ≤ n) :
    (scalarCycleG scalarNondelta * scalarCycleG scalarNondelta : Matrix (Fin n) (Fin n) ℚ) ≠ 0 := by
  intro h
  have hentry := congr_fun (congr_fun h (0 : Fin n)) (2 : Fin n)
  rw [nondelta_G_sq_entry hn, Matrix.zero_apply] at hentry
  have hn0 : n ≠ 0 := Nat.ne_of_gt (Nat.zero_lt_of_lt (Nat.lt_of_succ_le hn))
  have hne : (n : ℚ) ^ 2 / 2 ≠ 0 :=
    div_ne_zero (pow_ne_zero 2 (Nat.cast_ne_zero.mpr hn0)) (by norm_num)
  exact hne hentry

/-- Generic symmetric jet, including the nondelta terms `(Gᵀ)²` and `G²`. -/
theorem genericKSym_from_congruence (G K H B : Matrix (Fin n) (Fin n) ℚ) (c : ℚ)
    (hB : B = ((2 : ℚ) * c) • diagonal (fun i =>
      scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2))
    (hcov : H + B = (TwoJet.mk G K).secondOrderCongruenceCoefficient) :
    (1 / 2 : ℚ) • (Kᵀ + K) =
      Gᵀ * Gᵀ + Gᵀ * G + G * G - c • diagonal (fun i =>
        scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2) - (1 / 2 : ℚ) • H := by
  rw [secondOrderCongruenceCoefficient_formula] at hcov
  set Dg := diagonal (fun i => scalarDisplacement (scalarSite (0 : Fin n)) i ^ 2)
  have hcov' : H + B = (2 : ℚ) • (Gᵀ * Gᵀ) + (2 : ℚ) • (Gᵀ * G) + (2 : ℚ) • (G * G) -
      (Kᵀ + K) := hcov
  have hsum : H + B + (Kᵀ + K) =
      (2 : ℚ) • (Gᵀ * Gᵀ) + (2 : ℚ) • (Gᵀ * G) + (2 : ℚ) • (G * G) := by
    rw [hcov']
    abel
  have hsym : Kᵀ + K =
      (2 : ℚ) • (Gᵀ * Gᵀ) + (2 : ℚ) • (Gᵀ * G) + (2 : ℚ) • (G * G) - (H + B) := by
    have hsub := congrArg (fun M => M - (H + B)) hsum
    dsimp at hsub
    rw [add_sub_cancel_left] at hsub
    exact hsub
  have hc : (1 / 2 : ℚ) * ((2 : ℚ) * c) = c := by ring
  have h2 : (1 / 2 : ℚ) * 2 = 1 := by norm_num
  rw [hsym, hB]
  simp only [Dg, smul_sub, smul_add, smul_smul, hc, h2, one_smul]
  abel

private lemma shift_row_sum (i : Fin n) : (∑ j, scalarCycleShift n i j) = 1 := by
  rw [Finset.sum_eq_single (i + 1)]
  · simp [shift_apply]
  · intro j _ hj
    simp [shift_apply, hj]
  · intro h
    exact absurd (Finset.mem_univ _) h

private lemma shiftT_row_sum (i : Fin n) : (∑ j, (scalarCycleShift n)ᵀ i j) = 1 := by
  rw [Finset.sum_eq_single (i - 1)]
  · have h : i = (i - 1) + 1 := by simp
    rw [Matrix.transpose_apply, shift_apply, if_pos h]
  · intro j _ hj
    simp only [Matrix.transpose_apply, shift_apply]
    split_ifs with h
    · have : j = i - 1 := by
        calc
          j = (j + 1) - 1 := by simp
          _ = i - 1 := by rw [← h]
      exact absurd this hj
    · rfl
  · intro h
    exact absurd (Finset.mem_univ _) h

private lemma D_row_sum (i : Fin n) : (∑ j, scalarCycleD n i j) = 0 := by
  have h2 : (∑ j, scalarCycleShift n j i) = 1 := by
    simpa [Matrix.transpose_apply] using shiftT_row_sum i
  calc
    (∑ j, scalarCycleD n i j) =
        ∑ j, ((n : ℚ) / 2) * (scalarCycleShift n i j - scalarCycleShift n j i) := by
          simp [D_apply]
    _ = ((n : ℚ) / 2) * ∑ j, (scalarCycleShift n i j - scalarCycleShift n j i) := by
          rw [Finset.mul_sum]
    _ = ((n : ℚ) / 2) * ((∑ j, scalarCycleShift n i j) - ∑ j, scalarCycleShift n j i) := by
          rw [Finset.sum_sub_distrib]
    _ = ((n : ℚ) / 2) * (1 - 1) := by rw [shift_row_sum, h2]
    _ = 0 := by ring

theorem scalarCycleG_kills_ones (v : Fin n → ℚ) (i : Fin n) :
    (∑ j, scalarCycleG v i j * scalarOnes n j) = 0 := by
  simp only [scalarCycleG_apply, scalarOnes, mul_one]
  rw [← Finset.mul_sum, D_row_sum]
  ring

theorem scalarCycleG_constantForm (v : Fin n → ℚ) :
    scalarConstantForm (scalarCycleG v) = 0 := by
  classical
  simp only [scalarConstantForm]
  have h (i : Fin n) : (∑ j, scalarCycleG v i j) = 0 := by
    simpa [scalarOnes] using scalarCycleG_kills_ones v i
  simp [h]

private lemma constantForm_one : scalarConstantForm (1 : Matrix (Fin n) (Fin n) ℚ) = n := by
  classical
  simp only [scalarConstantForm, Matrix.one_apply]
  have h (i : Fin n) : (∑ j, if i = j then (1 : ℚ) else 0) = 1 := by
    rw [Finset.sum_eq_single i]
    · simp
    · intro j _ hj
      simp [if_neg (Ne.symm hj)]
    · intro hmem
      exact absurd (Finset.mem_univ _) hmem
  simp [h, Finset.sum_const, Finset.card_univ, Fintype.card_fin]

private lemma constantForm_smul (r : ℚ) (M : Matrix (Fin n) (Fin n) ℚ) :
    scalarConstantForm (r • M) = r * scalarConstantForm M := by
  simp only [scalarConstantForm, Matrix.smul_apply, smul_eq_mul]
  rw [Finset.mul_sum]
  refine Finset.sum_congr rfl ?_
  intro i _
  rw [Finset.mul_sum]

private lemma constantForm_diagonal (v : Fin n → ℚ) :
    scalarConstantForm (diagonal v) = ∑ i, v i := by
  classical
  simp only [scalarConstantForm, Matrix.diagonal_apply]
  have h (i : Fin n) : (∑ j, if i = j then v i else 0) = v i := by
    rw [Finset.sum_eq_single i]
    · simp
    · intro j _ hj
      simp [if_neg (Ne.symm hj)]
    · intro hmem
      exact absurd (Finset.mem_univ _) hmem
  simp [h]

private lemma constantForm_add (A B : Matrix (Fin n) (Fin n) ℚ) :
    scalarConstantForm (A + B) = scalarConstantForm A + scalarConstantForm B := by
  simp only [scalarConstantForm, Matrix.add_apply, Finset.sum_add_distrib]

private lemma constantForm_neg (A : Matrix (Fin n) (Fin n) ℚ) :
    scalarConstantForm (-A) = -scalarConstantForm A := by
  simp only [scalarConstantForm, Matrix.neg_apply, Finset.sum_neg_distrib]

private lemma constantForm_transpose (M : Matrix (Fin n) (Fin n) ℚ) :
    scalarConstantForm Mᵀ = scalarConstantForm M := by
  simp only [scalarConstantForm, Matrix.transpose_apply]
  rw [Finset.sum_comm]

/-- Reference scalar shadow `W_c(th) = I + t H(h) + c t² M_{h²}`. -/
def scalarReferenceWeight (c t : ℚ) (H : Matrix (Fin n) (Fin n) ℚ) (h : Fin n → ℚ) :
    Matrix (Fin n) (Fin n) ℚ :=
  1 + t • H + (c * t ^ 2) • diagonal (fun i => h i * h i)

theorem scalarReferenceWeight_quadraticCoefficient
    (c t : ℚ) (H : Matrix (Fin n) (Fin n) ℚ) (h : Fin n → ℚ) :
    scalarReferenceWeight c t H h =
      1 + t • H + (t ^ 2 / 2) • (((2 : ℚ) * c) • diagonal (fun i => h i * h i)) := by
  simp only [scalarReferenceWeight, smul_smul]
  have hcoeff : t ^ 2 / 2 * ((2 : ℚ) * c) = c * t ^ 2 := by ring
  simp [hcoeff]

theorem scalarReference_constantForm (hn : 3 ≤ n) (c t : ℚ) :
    scalarConstantForm (scalarReferenceWeight c t
        (-(scalarCycleG (scalarSite (0 : Fin n)) + (scalarCycleG (scalarSite 0))ᵀ))
        (scalarDisplacement (scalarSite 0))) =
      (n : ℚ) + c * t ^ 2 * (2 * (n : ℚ) ^ 2) := by
  have hsq := scalarDelta_displacement_sq_sum (Nat.le_trans (by decide) hn)
  simp only [scalarReferenceWeight]
  rw [constantForm_add, constantForm_add, constantForm_smul, constantForm_smul, constantForm_one,
    constantForm_neg, constantForm_add, scalarCycleG_constantForm, constantForm_transpose,
    scalarCycleG_constantForm, constantForm_diagonal]
  have hsq' : (∑ i, scalarDisplacement (scalarSite (0 : Fin n)) i *
      scalarDisplacement (scalarSite 0) i) = 2 * (n : ℚ) ^ 2 := by
    simpa [pow_two] using hsq
  rw [hsq']
  ring

theorem constantsPreservation_rejects_nonzero_c (hn : 3 ≤ n) {c : ℚ} (hc : c ≠ 0) :
    ¬ (∀ t : ℚ,
        scalarConstantForm (scalarReferenceWeight c t
          (-(scalarCycleG (scalarSite (0 : Fin n)) + (scalarCycleG (scalarSite 0))ᵀ))
          (scalarDisplacement (scalarSite 0))) = n) := by
  intro h
  have ht := h 1
  rw [scalarReference_constantForm hn] at ht
  have hn0 : (n : ℚ) ≠ 0 := by exact_mod_cast (by omega : n ≠ 0)
  have : c * (2 * (n : ℚ) ^ 2) = 0 := by linarith
  have hpow : (2 : ℚ) * (n : ℚ) ^ 2 ≠ 0 :=
    mul_ne_zero (by norm_num) (pow_ne_zero 2 hn0)
  exact hc ((mul_eq_zero.mp this).resolve_right hpow)

theorem constantsPreservation_rejects_displayed_coefficients (hn : 3 ≤ n) :
    ¬ (∀ t, scalarConstantForm (scalarReferenceWeight 1 t
        (-(scalarCycleG (scalarSite (0 : Fin n)) + (scalarCycleG (scalarSite 0))ᵀ))
        (scalarDisplacement (scalarSite 0))) = n) ∧
    ¬ (∀ t, scalarConstantForm (scalarReferenceWeight (2 : ℚ) t
        (-(scalarCycleG (scalarSite (0 : Fin n)) + (scalarCycleG (scalarSite 0))ᵀ))
        (scalarDisplacement (scalarSite 0))) = n) := by
  constructor
  · exact constantsPreservation_rejects_nonzero_c hn (by norm_num)
  · exact constantsPreservation_rejects_nonzero_c hn (by norm_num)

theorem diagonalAnsatz_constants_force_c_zero (hn : 3 ≤ n) (c : ℚ)
    (hpres : ∀ t, scalarConstantForm (scalarReferenceWeight c t
        (-(scalarCycleG (scalarSite (0 : Fin n)) + (scalarCycleG (scalarSite 0))ᵀ))
        (scalarDisplacement (scalarSite 0))) = n) : c = 0 := by
  by_contra hc
  exact constantsPreservation_rejects_nonzero_c hn hc hpres

/-- `c = 0` matches the constant-vector test and still fails the exponential jet. -/
theorem zeroCoefficient_is_not_exponential_completion (hn : 3 ≤ n) (a : Fin n → ℚ) :
    scalarCycleH0 a ≠
      (scalarCycleG (scalarSite (0 : Fin n)))ᵀ * (scalarCycleG (scalarSite 0))ᵀ +
        (2 : ℚ) • ((scalarCycleG (scalarSite 0))ᵀ * scalarCycleG (scalarSite 0)) +
        scalarCycleG (scalarSite 0) * scalarCycleG (scalarSite 0) := by
  simpa [zero_smul, add_zero] using
    deltaCartan_exponentialSecondOrder_noCellDiagonalCompletion hn (0 : ℚ) a

theorem delta_commutator_entry (hn : 3 ≤ n) :
    (((scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleG (scalarSite (1 : Fin n)) -
        scalarCycleG (scalarSite (1 : Fin n)) * scalarCycleG (scalarSite (0 : Fin n))) :
        Matrix (Fin n) (Fin n) ℚ) (0 : Fin n) (0 : Fin n)) =
      - (n : ℚ) ^ 2 / 4 := by
  have h01 : ((scalarCycleG (scalarSite (0 : Fin n)) * scalarCycleG (scalarSite (1 : Fin n)) :
        Matrix (Fin n) (Fin n) ℚ) (0 : Fin n) (0 : Fin n)) =
      - (n : ℚ) ^ 2 / 4 := by
    rw [Matrix.mul_apply, Finset.sum_eq_single (1 : Fin n)]
    · have hn1 : n ≠ 1 := by omega
      simp only [scalarCycleG_apply, scalarSite, D_zero_one hn, D_one_zero hn, hn1, if_true]
      ring_nf
    · intro k _ hk
      simp only [scalarCycleG_apply, scalarSite, if_neg hk]
      ring
    · intro h
      exact absurd (Finset.mem_univ _) h
  have h10 : ((scalarCycleG (scalarSite (1 : Fin n)) * scalarCycleG (scalarSite (0 : Fin n)) :
        Matrix (Fin n) (Fin n) ℚ) (0 : Fin n) (0 : Fin n)) = 0 := by
    rw [Matrix.mul_apply, Finset.sum_eq_single (0 : Fin n)]
    · have hn1 : n ≠ 1 := by omega
      simp [scalarCycleG_apply, scalarSite, (zero_ne_one (Nat.le_trans (by decide) hn)).symm,
        D_diagonal (Nat.le_trans (by decide) hn), hn1]
    · intro k _ hk
      simp only [scalarCycleG_apply, scalarSite, if_neg hk]
      ring
    · intro h
      exact absurd (Finset.mem_univ _) h
  simp [Matrix.sub_apply, h01, h10]

end D0.Geometry
