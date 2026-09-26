import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.LinearAlgebra.Matrix.Nondegenerate
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
Review scope: candidate-class / first Cartan–Hodge translation correction only.

# Scoped first Cartan–Hodge translation-rescue obstruction

This module formalizes the exact rational linear-algebra obstruction from merged
PR #181 / certificate
`a4d_star_translation_onshell_constraint_symmetry_check.py`.

On the all-site nondegenerate solder sector the six-parameter first Cartan–Hodge
correction class is

\[
(a_0,a_1,b_{00},b_{01},b_{10},b_{11})\in\mathbb{Q}^6
\]

encoding the solder-nonparallelism channels \(i_\alpha T\), \(i_\alpha \star_{\mathrm{base}} T\)
and the four curvature connection channels
\(i_\alpha F\), \(i_\alpha \star_{\mathrm{int}} F\),
\(i_\alpha \star_{\mathrm{base}} F\), \(i_\alpha \star_{\mathrm{int}}\star_{\mathrm{base}} F\).

Seven exact homogeneous L=2 controls give a \(7\times 6\) matrix of rank 6
(explicit invertible \(6\times 6\) minor). The hostile curved translation witness
then has bare forward variation \(c=-5/3\) and incompatible correction row, so

\[
\operatorname{rank} A = 6,\qquad
\operatorname{rank}[A\mid -c]=7.
\]

Hence no coefficient vector in this declared six-parameter class solves all
controls.

**Out of scope (explicit):** higher-curvature / longer-path laws, observer-dependent
channels, non-polynomial holonomy laws, and Euler/Hessian-dependent
transformations. This is **not** a universal affine-translation no-go.
-/

namespace D0.Geometry

open Matrix

set_option linter.unusedSimpArgs false
set_option linter.unnecessarySimpa false

noncomputable section

/-! ## 1. Six-parameter first Cartan–Hodge coefficient space -/

/-- Index of the six first Cartan–Hodge correction coefficients:
`0↦a₀`, `1↦a₁`, `2↦b₀₀`, `3↦b₀₁`, `4↦b₁₀`, `5↦b₁₁`. -/
abbrev FirstCartanHodgeCoeffIndex := Fin 6

/-- Rational coefficient vectors of the first Cartan–Hodge correction class. -/
abbrev FirstCartanHodgeCoeff := FirstCartanHodgeCoeffIndex → ℚ

/-- Named projections (documentation / readability). -/
def FirstCartanHodgeCoeff.a0 (x : FirstCartanHodgeCoeff) : ℚ := x 0
def FirstCartanHodgeCoeff.a1 (x : FirstCartanHodgeCoeff) : ℚ := x 1
def FirstCartanHodgeCoeff.b00 (x : FirstCartanHodgeCoeff) : ℚ := x 2
def FirstCartanHodgeCoeff.b01 (x : FirstCartanHodgeCoeff) : ℚ := x 3
def FirstCartanHodgeCoeff.b10 (x : FirstCartanHodgeCoeff) : ℚ := x 4
def FirstCartanHodgeCoeff.b11 (x : FirstCartanHodgeCoeff) : ℚ := x 5

/-! ## 2. Exact homogeneous control matrix (certificate `HOMOGENEOUS_ROWS`) -/

/-- Seven homogeneous curved L=2 control rows in coefficient order
`(a₀,a₁,b₀₀,b₀₁,b₁₀,b₁₁)`, copied verbatim from the #181 certificate. -/
def firstCartanHodgeHomogeneous :
    Matrix (Fin 7) FirstCartanHodgeCoeffIndex ℚ :=
  ![![0, (-1 : ℚ) / 25, 1, 1 / 20, (-107 : ℚ) / 75, 7 / 75],
    ![0, 1 / 3, -1, 0, 0, 11 / 18],
    ![(-4 : ℚ) / 15, (-16 : ℚ) / 3, (-2 : ℚ) / 3, (-29 : ℚ) / 30, (-19 : ℚ) / 9, 4 / 15],
    ![(-14 : ℚ) / 3, 20 / 21, (-7 : ℚ) / 3, (-4 : ℚ) / 7, (-1 : ℚ) / 3, 0],
    ![0, 0, 5, 5 / 3, -1, 0],
    ![7 / 165, (-6209 : ℚ) / 6050, 7 / 165, (-1 : ℚ) / 6, 7 / 15, 299 / 363],
    ![0, 0, 0, 0, 1 / 3, 0]]

/-- Row selector for the invertible `6×6` minor (omit homogeneous row 5). -/
def firstCartanHodgeMinorRow : Fin 6 → Fin 7
  | ⟨0, _⟩ => 0
  | ⟨1, _⟩ => 1
  | ⟨2, _⟩ => 2
  | ⟨3, _⟩ => 3
  | ⟨4, _⟩ => 4
  | ⟨5, _⟩ => 6

/-- Explicit invertible `6×6` minor of the homogeneous controls. -/
def firstCartanHodgeHomogeneousMinor :
    Matrix (Fin 6) FirstCartanHodgeCoeffIndex ℚ :=
  firstCartanHodgeHomogeneous.submatrix firstCartanHodgeMinorRow id

/-! ## 3. Homogeneous rank 6 / trivial kernel -/

/-- The selected `6×6` minor has nonzero determinant. -/
theorem firstCartanHodge_homogeneous_minor_det_ne_zero :
    firstCartanHodgeHomogeneousMinor.det ≠ 0 := by
  native_decide

theorem firstCartanHodge_homogeneous_minor_isUnit_det :
    IsUnit firstCartanHodgeHomogeneousMinor.det :=
  isUnit_iff_ne_zero.mpr firstCartanHodge_homogeneous_minor_det_ne_zero

theorem firstCartanHodge_homogeneous_minor_isUnit :
    IsUnit firstCartanHodgeHomogeneousMinor :=
  firstCartanHodgeHomogeneousMinor.isUnit_iff_isUnit_det.mpr
    firstCartanHodge_homogeneous_minor_isUnit_det

/-- Kernel of the invertible minor is trivial. -/
theorem firstCartanHodge_homogeneous_minor_ker_trivial
    (x : FirstCartanHodgeCoeff)
    (hx : firstCartanHodgeHomogeneousMinor *ᵥ x = 0) : x = 0 :=
  eq_zero_of_mulVec_eq_zero firstCartanHodge_homogeneous_minor_det_ne_zero hx

/-- Homogeneous `7×6` control matrix has trivial coefficient kernel. -/
theorem firstCartanHodge_homogeneous_ker_trivial
    (x : FirstCartanHodgeCoeff)
    (hx : firstCartanHodgeHomogeneous *ᵥ x = 0) : x = 0 := by
  refine firstCartanHodge_homogeneous_minor_ker_trivial x ?_
  ext i
  change (firstCartanHodgeHomogeneous *ᵥ x) (firstCartanHodgeMinorRow i) = 0
  simp [hx]

/-- Rank of the homogeneous control matrix equals 6. -/
theorem firstCartanHodge_homogeneous_rank :
    firstCartanHodgeHomogeneous.rank = 6 := by
  have hminor : firstCartanHodgeHomogeneousMinor.rank = 6 := by
    simpa using
      (rank_of_isUnit (R := ℚ) firstCartanHodgeHomogeneousMinor
        firstCartanHodge_homogeneous_minor_isUnit)
  have hle : firstCartanHodgeHomogeneous.rank ≤ 6 := by
    simpa using (Matrix.rank_le_card_width (R := ℚ) firstCartanHodgeHomogeneous)
  have hge : 6 ≤ firstCartanHodgeHomogeneous.rank := by
    have : firstCartanHodgeHomogeneousMinor.rank ≤ firstCartanHodgeHomogeneous.rank := by
      simpa [firstCartanHodgeHomogeneousMinor] using
        (Matrix.rank_submatrix_le (R := ℚ) firstCartanHodgeHomogeneous
          firstCartanHodgeMinorRow
          (id : FirstCartanHodgeCoeffIndex → FirstCartanHodgeCoeffIndex))
    simpa [hminor] using this
  exact le_antisymm hle hge

/-! ## 4. Hostile inhomogeneous row -/

/-- Hostile curved translation witness: bare forward variation. -/
def firstCartanHodgeHostileBare : ℚ := -5 / 3

/-- Hostile correction row
`(-68/27, 64/45, 70/81, -109/45, -10/9, 293/135)`. -/
def firstCartanHodgeHostileRow : FirstCartanHodgeCoeff :=
  ![(-68 : ℚ) / 27, 64 / 45, 70 / 81, (-109 : ℚ) / 45, (-10 : ℚ) / 9, 293 / 135]

/-- Full coefficient matrix: seven homogeneous rows plus the hostile row. -/
def firstCartanHodgeFull :
    Matrix (Fin 8) FirstCartanHodgeCoeffIndex ℚ :=
  fun i j =>
    if h : (i : ℕ) < 7 then
      firstCartanHodgeHomogeneous ⟨i, h⟩ j
    else
      firstCartanHodgeHostileRow j

/-- Right-hand side for the Noether system: zeros on homogeneous controls,
`-c = 5/3` on the hostile witness. -/
def firstCartanHodgeRHS : Fin 8 → ℚ :=
  fun i => if (i : ℕ) < 7 then 0 else -firstCartanHodgeHostileBare

/-- Augmented matrix `[A | -c]` as an `8×7` rational matrix. -/
def firstCartanHodgeAugmented : Matrix (Fin 8) (Fin 7) ℚ :=
  fun i j =>
    if h : (j : ℕ) < 6 then firstCartanHodgeFull i ⟨j, h⟩
    else firstCartanHodgeRHS i

/-- Explicit invertible `7×7` witness minor of the augmented system:
the homogeneous invertible minor together with the hostile inhomogeneous row. -/
def firstCartanHodgeAugmentedMinor : Matrix (Fin 7) (Fin 7) ℚ :=
  ![![0, (-1 : ℚ) / 25, 1, 1 / 20, (-107 : ℚ) / 75, 7 / 75, 0],
    ![0, 1 / 3, -1, 0, 0, 11 / 18, 0],
    ![(-4 : ℚ) / 15, (-16 : ℚ) / 3, (-2 : ℚ) / 3, (-29 : ℚ) / 30, (-19 : ℚ) / 9, 4 / 15, 0],
    ![(-14 : ℚ) / 3, 20 / 21, (-7 : ℚ) / 3, (-4 : ℚ) / 7, (-1 : ℚ) / 3, 0, 0],
    ![0, 0, 5, 5 / 3, -1, 0, 0],
    ![0, 0, 0, 0, 1 / 3, 0, 0],
    ![(-68 : ℚ) / 27, 64 / 45, 70 / 81, (-109 : ℚ) / 45, (-10 : ℚ) / 9, 293 / 135, 5 / 3]]

theorem firstCartanHodge_augmented_minor_det_ne_zero :
    firstCartanHodgeAugmentedMinor.det ≠ 0 := by
  native_decide

/-- Row embedding of the augmented invertible minor into the full augmented matrix. -/
def firstCartanHodgeAugmentedMinorRow : Fin 7 → Fin 8
  | ⟨0, _⟩ => 0
  | ⟨1, _⟩ => 1
  | ⟨2, _⟩ => 2
  | ⟨3, _⟩ => 3
  | ⟨4, _⟩ => 4
  | ⟨5, _⟩ => 6
  | ⟨6, _⟩ => 7

theorem firstCartanHodge_augmented_minor_eq_submatrix :
    firstCartanHodgeAugmentedMinor =
      firstCartanHodgeAugmented.submatrix firstCartanHodgeAugmentedMinorRow id := by
  ext i j
  fin_cases i <;> fin_cases j <;> native_decide

/-! ## 5. Augmented inconsistency / rank 7 -/

theorem firstCartanHodge_full_eq_homogeneous_on_prefix
    (x : FirstCartanHodgeCoeff) (i : Fin 7) :
    (firstCartanHodgeFull *ᵥ x) ⟨i.val, by omega⟩ =
      (firstCartanHodgeHomogeneous *ᵥ x) i := by
  simp [firstCartanHodgeFull, mulVec, dotProduct]

theorem firstCartanHodge_rhs_prefix_zero (i : Fin 7) :
    firstCartanHodgeRHS ⟨i.val, by omega⟩ = 0 := by
  simp [firstCartanHodgeRHS]

/-- The augmented system is inconsistent. -/
theorem firstCartanHodge_augmented_inconsistent :
    ¬ ∃ x : FirstCartanHodgeCoeff,
      firstCartanHodgeFull *ᵥ x = firstCartanHodgeRHS := by
  rintro ⟨x, hx⟩
  have hHom : firstCartanHodgeHomogeneous *ᵥ x = 0 := by
    ext i
    have := congrFun hx ⟨i.val, by omega⟩
    rw [firstCartanHodge_full_eq_homogeneous_on_prefix, firstCartanHodge_rhs_prefix_zero] at this
    exact this
  have hx0 := firstCartanHodge_homogeneous_ker_trivial x hHom
  have h7 := congrFun hx 7
  subst hx0
  change (firstCartanHodgeFull *ᵥ (0 : FirstCartanHodgeCoeff)) 7 = firstCartanHodgeRHS 7 at h7
  have hL : (firstCartanHodgeFull *ᵥ (0 : FirstCartanHodgeCoeff)) 7 = 0 := by
    simp [mulVec, dotProduct]
  have hR : firstCartanHodgeRHS 7 = -firstCartanHodgeHostileBare := by
    simp [firstCartanHodgeRHS, firstCartanHodgeHostileBare]
  rw [hL, hR] at h7
  norm_num [firstCartanHodgeHostileBare] at h7

theorem firstCartanHodge_augmented_minor_isUnit :
    IsUnit firstCartanHodgeAugmentedMinor :=
  firstCartanHodgeAugmentedMinor.isUnit_iff_isUnit_det.mpr
    (isUnit_iff_ne_zero.mpr firstCartanHodge_augmented_minor_det_ne_zero)

/-- Equivalent rank form: `rank[A|-c] = 7`. -/
theorem firstCartanHodge_augmented_rank :
    firstCartanHodgeAugmented.rank = 7 := by
  have hminor : firstCartanHodgeAugmentedMinor.rank = 7 := by
    simpa using
      (rank_of_isUnit (R := ℚ) firstCartanHodgeAugmentedMinor
        firstCartanHodge_augmented_minor_isUnit)
  have hle : firstCartanHodgeAugmented.rank ≤ 7 := by
    simpa using (Matrix.rank_le_card_width (R := ℚ) firstCartanHodgeAugmented)
  have hge : 7 ≤ firstCartanHodgeAugmented.rank := by
    have : firstCartanHodgeAugmentedMinor.rank ≤ firstCartanHodgeAugmented.rank := by
      simpa [firstCartanHodge_augmented_minor_eq_submatrix] using
        (Matrix.rank_submatrix_le (R := ℚ) firstCartanHodgeAugmented
          firstCartanHodgeAugmentedMinorRow (id : Fin 7 → Fin 7))
    simpa [hminor] using this
  exact le_antisymm hle hge

/-! ## 6. Scoped no-solution theorem -/

/-- No coefficient vector in the declared six-parameter first Cartan–Hodge class
solves all homogeneous controls together with the hostile translation witness.

Scoped statement only — not a universal translation no-go. Higher-curvature/path,
observer-dependent, non-polynomial and Euler-dependent laws remain outside scope. -/
theorem firstCartanHodge_no_coefficient_solution :
    ¬ ∃ x : FirstCartanHodgeCoeff,
      (∀ i : Fin 7, (firstCartanHodgeHomogeneous *ᵥ x) i = 0) ∧
        (firstCartanHodgeHostileRow ⬝ᵥ x) = -firstCartanHodgeHostileBare := by
  rintro ⟨x, hHom, hHost⟩
  have hx0 : x = 0 :=
    firstCartanHodge_homogeneous_ker_trivial x (by ext i; exact hHom i)
  subst hx0
  change firstCartanHodgeHostileRow ⬝ᵥ (0 : FirstCartanHodgeCoeff) =
      -firstCartanHodgeHostileBare at hHost
  have : (0 : ℚ) = -firstCartanHodgeHostileBare := by
    simpa [dotProduct] using hHost
  norm_num [firstCartanHodgeHostileBare] at this

/-- Convenience package: homogeneous rank 6, augmented rank 7, and scoped
no-solution. Out-of-scope note is in the module docstring above. -/
theorem firstCartanHodge_translation_obstruction_package :
    firstCartanHodgeHomogeneous.rank = 6 ∧
      firstCartanHodgeAugmented.rank = 7 ∧
      (¬ ∃ x : FirstCartanHodgeCoeff,
        firstCartanHodgeFull *ᵥ x = firstCartanHodgeRHS) :=
  ⟨firstCartanHodge_homogeneous_rank, firstCartanHodge_augmented_rank,
    firstCartanHodge_augmented_inconsistent⟩

#print axioms firstCartanHodge_homogeneous_rank
#print axioms firstCartanHodge_augmented_rank
#print axioms firstCartanHodge_augmented_inconsistent
#print axioms firstCartanHodge_no_coefficient_solution

end

end D0.Geometry
