import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import D0.Geometry.A4DPrimalDualCellPairing
import D0.Geometry.A4DSolderMetricCompletion

/-!
# Flat Lorentz metric star: signature and pointwise boundary

These coefficients live on one Lorentz fibre.  They are distinct from the
located, two-colour primal/dual placement `J`.
-/

namespace D0.Geometry

open D0
open scoped BigOperators

noncomputable section

/-- Product of the diagonal Lorentz signs on an occupied subset, in an
integer shadow suitable for exhaustive four-role proofs. -/
def flatLorentzSubsetWeightInt (S : ArchiveFockState) : ℤ :=
  ∏ r ∈ Finset.univ.filter (fun r : Role => S r),
    (if r = A then (1 : ℤ) else -1)

def flatLorentzSubsetWeight (S : ArchiveFockState) : ℝ :=
  (flatLorentzSubsetWeightInt S : ℝ)

theorem flatLorentzSubsetWeight_eq_sign_product (S : ArchiveFockState) :
    flatLorentzSubsetWeight S =
      ∏ r ∈ Finset.univ.filter (fun r : Role => S r), roleLorentzSign r := by
  simp only [flatLorentzSubsetWeight, flatLorentzSubsetWeightInt, Int.cast_prod]
  apply Finset.prod_congr rfl
  intro r hr
  fin_cases r <;>
    norm_num [roleLorentzSign, roleRoleSigEquiv, roleSign, A, B, C, D]

theorem flatLorentzSubsetWeightInt_singleton : ∀ r : Role,
    flatLorentzSubsetWeightInt (fockSingletonState r) =
      if r = A then 1 else -1 := by
  native_decide

/-- Degree-one Jacobi/cofactor identity for an invertible four-dimensional
common fibre.  The complementary determinant is the ordered `3 × 3` minor.
It is an algebraic same-fibre identity and carries no located site shift. -/
theorem commonFiber_four_cofactor_inverse (L : Matrix (Fin 4) (Fin 4) ℝ)
    (hdet : L.det ≠ 0) (i j : Fin 4) :
    L.det * (L⁻¹) i j =
      (-1 : ℝ) ^ ((j : ℕ) + (i : ℕ)) *
        (L.submatrix j.succAbove i.succAbove).det := by
  rw [Matrix.inv_def, Matrix.smul_apply, smul_eq_mul,
    Matrix.adjugate_fin_succ_eq_det_submatrix]
  simp [hdet]

/-- Lexicographic 2-subsets of `Fin 4`: low index, then high index. -/
def fin4TwoLow : Fin 6 → Fin 4
  | 0 => 0 | 1 => 0 | 2 => 0 | 3 => 1 | 4 => 1 | 5 => 2

def fin4TwoHigh : Fin 6 → Fin 4
  | 0 => 1 | 1 => 2 | 2 => 3 | 3 => 2 | 4 => 3 | 5 => 3

/-- Complement in lexicographic order: `{0,1}↔{2,3}`, `{0,2}↔{1,3}`, `{0,3}↔{1,2}`. -/
def fin4TwoComplement : Fin 6 → Fin 6
  | 0 => 5 | 1 => 4 | 2 => 3 | 3 => 2 | 4 => 1 | 5 => 0

/-- Diagonal Lorentz fibre `diag(+1,-1,-1,-1)` on `Fin 4`. -/
def flatLorentzFin4 : Matrix (Fin 4) (Fin 4) ℝ :=
  Matrix.diagonal (fun i => if i = 0 then 1 else -1)

/-- Principal 2×2 compound minor. -/
def fin4PrincipalTwoMinor (M : Matrix (Fin 4) (Fin 4) ℝ) (i : Fin 6) : ℝ :=
  M (fin4TwoLow i) (fin4TwoLow i) * M (fin4TwoHigh i) (fin4TwoHigh i) -
    M (fin4TwoLow i) (fin4TwoHigh i) * M (fin4TwoHigh i) (fin4TwoLow i)

theorem flatLorentzFin4_sq : flatLorentzFin4 * flatLorentzFin4 = 1 := by
  rw [flatLorentzFin4, Matrix.diagonal_mul_diagonal]
  ext i j
  by_cases h : i = j
  · subst h
    fin_cases i <;> simp [Matrix.diagonal_apply, Matrix.one_apply]
  · simp [Matrix.diagonal_apply, Matrix.one_apply, h, Ne.symm h]

theorem flatLorentzFin4_inv : flatLorentzFin4⁻¹ = flatLorentzFin4 :=
  Matrix.inv_eq_right_inv flatLorentzFin4_sq

theorem flatLorentzFin4_det : flatLorentzFin4.det = -1 := by
  rw [flatLorentzFin4, Matrix.det_diagonal]
  simp [Fin.prod_univ_succ, Fin.prod_univ_zero]
  norm_num

/-- On the nondegenerate flat Lorentz fibre, the determinant times a principal
middle minor of the inverse equals the principal minor of the complementary
pair.  The cofactor identity above is the generic codimension-one Jacobi law. -/
theorem flatLorentz_middle_complementary_minor (i : Fin 6) :
    flatLorentzFin4.det * fin4PrincipalTwoMinor flatLorentzFin4⁻¹ i =
      fin4PrincipalTwoMinor flatLorentzFin4 (fin4TwoComplement i) := by
  rw [flatLorentzFin4_inv, flatLorentzFin4_det]
  fin_cases i <;>
    simp [fin4PrincipalTwoMinor, fin4TwoLow, fin4TwoHigh, fin4TwoComplement,
      flatLorentzFin4, Matrix.diagonal_apply] <;>
    norm_num

/-- A one-fibre Lorentz exterior-star coefficient in the ordered subset basis.
The orientation is the algebraic complement sign, while the metric factor is
the product of the Lorentz signs of the occupied roles. -/
def flatLorentzStarCoeff (S : ArchiveFockState) : ℝ :=
  complementOrientation S * flatLorentzSubsetWeight S

theorem flatLorentzSubsetWeightInt_complement : ∀ S : ArchiveFockState,
    flatLorentzSubsetWeightInt S *
      flatLorentzSubsetWeightInt (occupationComplement S) = -1 := by
  native_decide

/-- The additional minus sign comes from the three negative directions of
`eta=(+---)`. -/
theorem flatLorentzStarCoeff_double (S : ArchiveFockState) :
    flatLorentzStarCoeff S * flatLorentzStarCoeff (occupationComplement S) =
      if (fockDegree S * (4 - fockDegree S)) % 2 = 0 then -1 else 1 := by
  have hw := congrArg (fun z : ℤ => (z : ℝ))
    (flatLorentzSubsetWeightInt_complement S)
  have he := epsilon_complement_sign S
  unfold flatLorentzStarCoeff flatLorentzSubsetWeight
  simp only [Int.cast_mul, Int.cast_neg, Int.cast_one] at hw
  by_cases hp : (fockDegree S * (4 - fockDegree S)) % 2 = 0
  · rw [if_pos hp] at he ⊢
    nlinarith [mul_assoc (complementOrientation S)
      (flatLorentzSubsetWeightInt S : ℝ)
      (complementOrientation (occupationComplement S))]
  · rw [if_neg hp] at he ⊢
    nlinarith [mul_assoc (complementOrientation S)
      (flatLorentzSubsetWeightInt S : ℝ)
      (complementOrientation (occupationComplement S))]

theorem neg_one_pow_two_mul_add_three (n : ℕ) :
    (-1 : ℝ) ^ (2 * n + 3) = -1 := by
  rw [pow_add, pow_mul, pow_succ, pow_succ, pow_succ, pow_zero]
  norm_num

theorem neg_one_pow_even (n : ℕ) : (-1 : ℝ) ^ (2 * n) = 1 := by
  rw [pow_mul]
  norm_num

/-- Double application has sign `(-1)^{k(4-k)+3}`. -/
theorem flatLorentzStarCoeff_double_exponent (S : ArchiveFockState) :
    flatLorentzStarCoeff S * flatLorentzStarCoeff (occupationComplement S) =
      (-1 : ℝ) ^ (fockDegree S * (4 - fockDegree S) + 3) := by
  rw [flatLorentzStarCoeff_double]
  set k : ℕ := fockDegree S * (4 - fockDegree S)
  have hk : k = 2 * (k / 2) + k % 2 := (Nat.div_add_mod k 2).symm
  by_cases hp : k % 2 = 0
  · rw [if_pos hp]
    have hk' : k + 3 = 2 * (k / 2) + 3 := by omega
    rw [hk', neg_one_pow_two_mul_add_three]
  · have h1 : k % 2 = 1 := by
      have hmod := Nat.mod_two_eq_zero_or_one k
      cases hmod with
      | inl h0 => exact absurd h0 hp
      | inr h1 => exact h1
    rw [if_neg hp]
    have hk' : k + 3 = 2 * ((k / 2) + 2) := by omega
    rw [hk', neg_one_pow_even]

/-- On degree one the flat metric pairing is `eta`, not the positive counting
form.  In particular the B direction has norm `-1`. -/
theorem flatLorentz_degreeOne_B_negative : roleLorentzMetric B B = -1 := by
  simp [roleLorentzMetric]

theorem flatLorentz_degreeOne_not_counting :
    roleLorentzMetric ≠ (1 : Matrix Role Role ℝ) := by
  intro h
  have hB := congrArg (fun M : Matrix Role Role ℝ => M B B) h
  norm_num [flatLorentz_degreeOne_B_negative] at hB

/-- A pointwise scalar coefficient rule is blind to a change at the next
site, whereas the accepted forward scalar derivative detects it. -/
theorem pointwiseCoefficient_cannot_equal_neighborDerivative
    (K : ArchiveRolePhaseGroup 1 → ℝ → ℝ)
    (hK : ∀ f : ArchiveRolePhaseGroup 1 → ℝ,
      ∀ x, K x (f x) = forwardDifference 1 A f x) : False := by
  let y : ArchiveRolePhaseGroup 1 := roleStep 1 A
  have hy : y ≠ 0 := by
    intro h
    have hA := congrFun h A
    have hne : (1 : ZMod 3) ≠ 0 := by decide
    change (1 : ZMod 3) = 0 at hA
    exact hne hA
  let f : ArchiveRolePhaseGroup 1 → ℝ := fun x => if x = y then 1 else 0
  have h0 : f 0 = 0 := by simp [f, Ne.symm hy]
  have h1 : f y = 1 := by simp [f]
  have hzero := hK (fun _ => 0) 0
  have hf := hK f 0
  simp [forwardDifference, forwardDifferenceScale, archiveFibers,
    roleTranslatePlus, roleTranslate, h0, h1, y] at hzero hf
  linarith

end

end D0.Geometry
