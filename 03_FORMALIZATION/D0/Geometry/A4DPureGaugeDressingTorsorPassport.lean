import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic

/-!
# Pure-gauge dressing torsor passport

Algebraic owner for the finite right-isotropy and infinitesimal skew boundaries
isolated by `MEMO_A4D_FINITE_GRADED_COFRAME_DRESSING.md`.

The finite and infinitesimal freedoms are kept separate:

* in any group, a commuting right factor `R` does not change the conjugated
  horizontal letter `F U F⁻¹`;
* for square matrices, a right orthogonal factor does not change
  `F⁻ᵀ F⁻¹`;
* at first order, adding a skew matrix does not change
  `-(Gᵀ + G)`.

The explicit 2×2 control shows why orthogonality alone is insufficient for
horizontal descent: an orthogonal factor that does not commute with the
translation changes it by conjugation.

No arbitrary-background dressing, resolution datum, crossed `T_kappa`,
stress tensor, continuum limit, or preferred representative is introduced.
-/

namespace D0.Geometry.A4DPureGaugeDressingTorsorPassport

/-! ## Finite torsor algebra -/

section GroupCore

variable {G : Type*} [Group G]

/-- Conjugated horizontal letter carried by a dressing representative. -/
def horizontalLetter (F U : G) : G :=
  F * U * F⁻¹

theorem conjugate_self_of_commute (R U : G) (hRU : Commute R U) :
    R * U * R⁻¹ = U := by
  calc
    R * U * R⁻¹ = U * R * R⁻¹ := by rw [hRU.eq]
    _ = U := by simp [mul_assoc]

/-- A commuting right-isotropy factor is invisible to the horizontal letter. -/
theorem horizontalLetter_right_commuting (F R U : G) (hRU : Commute R U) :
    horizontalLetter (F * R) U = horizontalLetter F U := by
  calc
    horizontalLetter (F * R) U
        = F * (R * U * R⁻¹) * F⁻¹ := by
            simp [horizontalLetter, mul_assoc]
    _ = F * U * F⁻¹ := by rw [conjugate_self_of_commute R U hRU]
    _ = horizontalLetter F U := rfl

theorem horizontalLetter_one (U : G) :
    horizontalLetter 1 U = U := by
  simp [horizontalLetter]

/-- Conversely, conjugation fixes `U` only if the right factor commutes with it. -/
theorem commute_of_conjugate_self (R U : G)
    (h : R * U * R⁻¹ = U) :
    Commute R U := by
  show R * U = U * R
  have h' := congrArg (fun x : G => x * R) h
  simpa [mul_assoc] using h'

/-- Exact necessity/sufficiency boundary for right-isotropy horizontal descent. -/
theorem horizontalLetter_right_eq_base_iff_commute (R U : G) :
    horizontalLetter R U = horizontalLetter 1 U ↔ Commute R U := by
  rw [horizontalLetter_one]
  constructor
  · intro h
    exact commute_of_conjugate_self R U (by simpa [horizontalLetter] using h)
  · intro h
    simpa [horizontalLetter] using conjugate_self_of_commute R U h

/-- Nontrivial commuting right factors give distinct representatives with the
same horizontal output. -/
theorem distinct_representatives_same_horizontal
    (F R U : G) (hR : R ≠ 1) (hRU : Commute R U) :
    F * R ≠ F ∧
      horizontalLetter (F * R) U = horizontalLetter F U := by
  constructor
  · intro h
    have h' : F * R = F * 1 := by simpa using h
    exact hR (mul_left_cancel h')
  · exact horizontalLetter_right_commuting F R U hRU

end GroupCore

/-! ## Matrix constitutive shadow -/

section MatrixCore

open Matrix

variable {n K : Type*} [Fintype n] [DecidableEq n] [Field K]

abbrev Mat := Matrix n n K

/-- Two-sided orthogonality, stated without choosing a preferred basis beyond
the matrix transpose already present in the carrier. -/
def RightOrthogonal (R : Mat) : Prop :=
  R.transpose * R = 1 ∧ R * R.transpose = 1

/-- Constitutive shadow of an invertible dressing representative. Matrix
nonsingular inverse is used so the statement remains in the repository matrix
carrier. -/
def constitutiveShadow (F : Mat) : Mat :=
  (F⁻¹).transpose * F⁻¹

theorem RightOrthogonal.inv_eq_transpose {R : Mat} (hR : RightOrthogonal R) :
    R⁻¹ = R.transpose := by
  exact Matrix.inv_eq_right_inv hR.2

/-- Orthogonal right-isotropy drops out of `F⁻ᵀ F⁻¹`. -/
theorem constitutiveShadow_right_orthogonal
    (F R : Mat) (hR : RightOrthogonal R) :
    constitutiveShadow (F * R) = constitutiveShadow F := by
  have hRinv : R⁻¹ = R.transpose := hR.inv_eq_transpose
  unfold constitutiveShadow
  rw [Matrix.mul_inv_rev F R, Matrix.transpose_mul, hRinv, Matrix.transpose_transpose]
  calc
    (F⁻¹).transpose * R * (R.transpose * F⁻¹)
        = (F⁻¹).transpose * (R * R.transpose) * F⁻¹ := by
            simp only [Matrix.mul_assoc]
    _ = (F⁻¹).transpose * F⁻¹ := by rw [hR.2]; simp

/-! ## Infinitesimal skew freedom -/

/-- First constitutive derivative associated with a dressing tangent. -/
def tangentConstitutive (G : Mat) : Mat :=
  -(G.transpose + G)

/-- Matrix skewness, kept separate from the finite right-isotropy predicate. -/
def IsSkew (A : Mat) : Prop :=
  A.transpose = -A

/-- A skew tangent is invisible to the first constitutive derivative. -/
theorem tangentConstitutive_add_skew
    (G A : Mat) (hA : IsSkew A) :
    tangentConstitutive (G + A) = tangentConstitutive G := by
  unfold tangentConstitutive
  rw [Matrix.transpose_add, hA]
  abel

/-- Equality of first constitutive derivatives is exactly skew difference. -/
theorem tangentConstitutive_eq_iff_sub_skew (G₁ G₂ : Mat) :
    tangentConstitutive G₁ = tangentConstitutive G₂ ↔
      IsSkew (G₁ - G₂) := by
  constructor
  · intro h
    unfold IsSkew
    ext i j
    have hij := congrArg (fun M : Mat => M i j) h
    simp only [tangentConstitutive, Matrix.neg_apply, Matrix.add_apply,
      Matrix.transpose_apply] at hij
    simp only [Matrix.transpose_apply, Matrix.sub_apply, Matrix.neg_apply]
    linarith
  · intro h
    have h0 := tangentConstitutive_add_skew G₂ (G₁ - G₂) h
    have hsum : G₂ + (G₁ - G₂) = G₁ := by
      abel
    rw [hsum] at h0
    exact h0

end MatrixCore

/-! ## Exact finite hostile controls -/

section Controls

open Matrix

abbrev M2 := Matrix (Fin 2) (Fin 2) ℚ

/-- Nontrivial orthogonal right factor. -/
def swap2 : M2 :=
  !![0, 1; 1, 0]

/-- A translation/operator not commuting with `swap2`. -/
def sign2 : M2 :=
  !![1, 0; 0, -1]

/-- Nonzero skew tangent. -/
def skew2 : M2 :=
  !![0, 1; -1, 0]

theorem swap2_rightOrthogonal :
    RightOrthogonal swap2 := by
  native_decide

theorem swap2_nontrivial :
    swap2 ≠ (1 : M2) := by
  native_decide

/-- Constitutive output descends even though the representative changes. -/
theorem constitutive_torsor_nonidentification_control :
    swap2 ≠ (1 : M2) ∧
      constitutiveShadow swap2 = constitutiveShadow (1 : M2) := by
  refine ⟨swap2_nontrivial, ?_⟩
  simpa using
    (constitutiveShadow_right_orthogonal (F := (1 : M2))
      (R := swap2) swap2_rightOrthogonal)

theorem skew2_isSkew :
    IsSkew skew2 := by
  native_decide

theorem skew2_nonzero :
    skew2 ≠ (0 : M2) := by
  native_decide

/-- Nonzero skew tangent with unchanged first constitutive response. -/
theorem tangent_skew_nonidentification_control :
    skew2 ≠ (0 : M2) ∧
      tangentConstitutive skew2 = tangentConstitutive (0 : M2) := by
  refine ⟨skew2_nonzero, ?_⟩
  simpa using
    (tangentConstitutive_add_skew (G := (0 : M2)) (A := skew2) skew2_isSkew)

/-- Mandatory negative firewall: orthogonality alone does not make a right
factor invisible to a horizontal operator. -/
theorem orthogonality_without_commutation_does_not_descend :
    RightOrthogonal swap2 ∧
      swap2 * sign2 ≠ sign2 * swap2 ∧
      swap2 * sign2 * swap2.transpose ≠ sign2 := by
  native_decide

end Controls

end D0.Geometry.A4DPureGaugeDressingTorsorPassport
