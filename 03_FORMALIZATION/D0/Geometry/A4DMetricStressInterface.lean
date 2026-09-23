import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Geometry.A4DSymRoleCentralDifference

namespace D0.Geometry

open D0

noncomputable section

/-!
# 1+3+6 metric readout, conductance obstruction, lapse ordering

Role `A` is the time slot.  The Frobenius pairing of two symmetric role tensors
splits into the temporal diagonal, three spatial diagonals, and twice the three
mixed plus three spatial-shear coordinates.

A probe supported on one of those slots reads that slot of one supplied tensor.
An axis-diagonal spatial tensor cannot equal a pure shear.  For symmetric
matrices, `MH` is symmetric exactly when `M` and `H` commute.  The symmetrized
product is symmetric and is not selected as a physical coupling.
-/

def symFrobenius (S T : SymRoleTensor) : ℝ :=
  ∑ a : Role, ∑ b : Role, S.toMatrix a b * T.toMatrix a b

theorem sum_role_four (f : Role → ℝ) :
    (∑ r : Role, f r) = f A + f C + f D + f B := by
  have h : (∑ r : Role, f r) = ∑ a : Fin 2, ∑ b : Fin 2, f (a, b) :=
    Fintype.sum_prod_type f
  rw [h]
  simp only [Fin.sum_univ_two, A, C, D, B]
  ring

/-- Off-diagonal independent coordinates enter with factor two. -/
theorem symFrobenius_factor_two (S T : SymRoleTensor) :
    symFrobenius S T =
      S.toMatrix A A * T.toMatrix A A +
      S.toMatrix B B * T.toMatrix B B +
      S.toMatrix C C * T.toMatrix C C +
      S.toMatrix D D * T.toMatrix D D +
      2 * (S.toMatrix A B * T.toMatrix A B +
        S.toMatrix A C * T.toMatrix A C +
        S.toMatrix A D * T.toMatrix A D +
        S.toMatrix B C * T.toMatrix B C +
        S.toMatrix B D * T.toMatrix B D +
        S.toMatrix C D * T.toMatrix C D) := by
  unfold symFrobenius
  rw [sum_role_four (fun a => ∑ b, S.toMatrix a b * T.toMatrix a b)]
  simp_rw [sum_role_four (fun b => S.toMatrix _ b * T.toMatrix _ b)]
  rw [S.entry_symmetric B A, S.entry_symmetric C A, S.entry_symmetric D A,
    S.entry_symmetric C B, S.entry_symmetric D B, S.entry_symmetric D C,
    T.entry_symmetric B A, T.entry_symmetric C A, T.entry_symmetric D A,
    T.entry_symmetric C B, T.entry_symmetric D B, T.entry_symmetric D C]
  ring

def temporalProbe (t : ℝ) : SymRoleTensor where
  toMatrix := fun a b => if a = A ∧ b = A then t else 0
  symmetric := by
    intro a b
    by_cases ha : a = A <;> by_cases hb : b = A <;> simp [ha, hb]

theorem temporalVariation_reads_same_tensor (Lambda : SymRoleTensor) (t : ℝ) :
    symFrobenius Lambda (temporalProbe t) = t * Lambda.toMatrix A A := by
  unfold symFrobenius temporalProbe
  rw [sum_role_four (fun a => ∑ b, Lambda.toMatrix a b * _)]
  simp_rw [sum_role_four]
  simp [A, B, C, D]
  ring

def axisSpatial (wB wC wD : ℝ) : SymRoleTensor where
  toMatrix := fun a b =>
    if a ≠ b then 0
    else if a = B then wB
    else if a = C then wC
    else if a = D then wD
    else 0
  symmetric := by
    intro a b
    by_cases hab : a = b
    · subst b
      rfl
    · simp [hab, Ne.symm hab]

def pureShearBC : SymRoleTensor where
  toMatrix := fun a b =>
    if (a = B ∧ b = C) ∨ (a = C ∧ b = B) then 1 else 0
  symmetric := by
    intro a b
    by_cases h : (a = B ∧ b = C) ∨ (a = C ∧ b = B)
    · rcases h with h | h
      · simp [h.1, h.2]
      · simp [h.1, h.2]
    · have h' : ¬ ((b = B ∧ a = C) ∨ (b = C ∧ a = B)) := by
        intro hc
        apply h
        rcases hc with hc | hc
        · exact Or.inr ⟨hc.2, hc.1⟩
        · exact Or.inl ⟨hc.2, hc.1⟩
      simp [h, h']

/-- Three spatial axis weights do not reach a pure shear. -/
theorem axis_conductance_misses_shear (wB wC wD : ℝ) :
    axisSpatial wB wC wD ≠ pureShearBC := by
  intro h
  have hentry := congrArg (fun T : SymRoleTensor => T.toMatrix B C) h
  simp [axisSpatial, pureShearBC, B, C] at hentry

theorem mul_transpose_of_symmetric {n : Type*} [Fintype n] [DecidableEq n]
    (M H : Matrix n n ℝ) (hM : M.transpose = M) (hH : H.transpose = H) :
    (M * H).transpose = H * M := by
  rw [Matrix.transpose_mul, hH, hM]

theorem symmetric_mul_iff_commute {n : Type*} [Fintype n] [DecidableEq n]
    (M H : Matrix n n ℝ) (hM : M.transpose = M) (hH : H.transpose = H) :
    (M * H).transpose = M * H ↔ M * H = H * M := by
  rw [mul_transpose_of_symmetric M H hM hH]
  constructor <;> intro h <;> exact h.symm

def symmetrizedProduct {n : Type*} [Fintype n] (M H : Matrix n n ℝ) : Matrix n n ℝ :=
  M * H + H * M

theorem symmetrizedProduct_symmetric {n : Type*} [Fintype n] [DecidableEq n]
    (M H : Matrix n n ℝ) (hM : M.transpose = M) (hH : H.transpose = H) :
    (symmetrizedProduct M H).transpose = symmetrizedProduct M H := by
  unfold symmetrizedProduct
  rw [Matrix.transpose_add, mul_transpose_of_symmetric M H hM hH,
    mul_transpose_of_symmetric H M hH hM]
  abel

def lapseWitnessMul : Matrix (Fin 3) (Fin 3) ℝ :=
  Matrix.diagonal (fun i : Fin 3 => (i.val + 1 : ℝ))

def lapseWitnessHop : Matrix (Fin 3) (Fin 3) ℝ :=
  fun i j => if i = j then 0 else 1

theorem lapseWitnessMul_symmetric : lapseWitnessMul.transpose = lapseWitnessMul := by
  ext i j
  by_cases h : i = j
  · subst j
    simp [lapseWitnessMul, Matrix.diagonal]
  · simp [lapseWitnessMul, Matrix.diagonal, Matrix.transpose_apply, h, Ne.symm h]

theorem lapseWitnessHop_symmetric : lapseWitnessHop.transpose = lapseWitnessHop := by
  ext i j
  by_cases h : i = j
  · subst j
    simp [lapseWitnessHop]
  · simp [lapseWitnessHop, Matrix.transpose_apply, h, Ne.symm h]

theorem lapseWitness_fails_to_commute :
    lapseWitnessMul * lapseWitnessHop ≠ lapseWitnessHop * lapseWitnessMul := by
  intro h
  have h01 := congr_fun (congr_fun h (0 : Fin 3)) (1 : Fin 3)
  simp [Matrix.mul_apply, lapseWitnessMul, lapseWitnessHop, Matrix.diagonal,
    Fin.sum_univ_three] at h01

theorem lapseWitness_product_not_symmetric :
    (lapseWitnessMul * lapseWitnessHop).transpose ≠ lapseWitnessMul * lapseWitnessHop := by
  intro hsym
  exact lapseWitness_fails_to_commute
    ((symmetric_mul_iff_commute lapseWitnessMul lapseWitnessHop
      lapseWitnessMul_symmetric lapseWitnessHop_symmetric).mp hsym)

end

end D0.Geometry
