import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.LinearAlgebra.Matrix.Kronecker
import Mathlib.LinearAlgebra.Matrix.Vec
import Mathlib.Tactic
import D0.Geometry.A4DMetricStarSignatureBoundary

/-!
# Regular nondegenerate relative A/e passport

Lean owner for the restricted invertible branch isolated by PR #120 / memo
`MEMO_A4D_DIAGONAL_JUNCTION_OVERLAP_LAW` §§30–31 and Theorem L.

Matrix-level theorem over `4×4` matrices with the repository Lorentz signature
`η = diag(+1,-1,-1,-1)`. The algebraic core is stated over `ℚ` so that exact
rational controls are `native_decide`-checkable; the signature matches
`flatLorentzFin4` after the canonical cast `ℚ → ℝ`.

On invertible raw solder `B_e`, the ratio `K = B_e⁻¹ C_A` is frame-invariant.
In the translation chart `B = I + η D`, `C = D` one has the reconstruction
identity `D - η D K = K`, equivalently `B - η B K = I`, unique under
injectivity/invertibility of `L_K(X) = X - η X K`.

This is **not** a global selector: the singular/degenerate locus is left open.
No generalized inverse, observer patch, finite E dressing, or `A = A(e)` is
introduced here.
-/

namespace D0.Geometry.A4DRegularAEPassport

open Matrix
open scoped BigOperators Kronecker

noncomputable section

set_option linter.unusedSimpArgs false

/-! ## Carriers and η convention -/

/-- Local 4×4 rational matrix carrier (exact controls; same algebra as ℝ). -/
abbrev M4 := Matrix (Fin 4) (Fin 4) ℚ

/-- Repository Lorentz signature on `Fin 4`: `diag(+1,-1,-1,-1)`. -/
def passportEta : M4 :=
  diagonal ![1, -1, -1, -1]

theorem passportEta_sq : passportEta * passportEta = 1 := by
  native_decide

theorem passportEta_matches_flatLorentzFin4 :
    passportEta.map (Rat.cast : ℚ → ℝ) = flatLorentzFin4 := by
  ext i j
  simp only [passportEta, flatLorentzFin4, diagonal, map_apply]
  fin_cases i <;> fin_cases j <;> norm_num

/-! ## Mandatory definitions -/

/-- Regular passport ratio `K = B_e⁻¹ C_A` on the invertible-`B_e` branch
(memo (30.3)). Matrix-level owner of `B_e(x)e_s = v_s(e,x)` and
`C_A(x)e_s = b_{x,s}` after choosing fibre bases. -/
def regularPassportK (B_e C_A : M4) : M4 :=
  B_e⁻¹ * C_A

/-- Translation-chart solder `B = I + η D` (memo (30.4)). -/
def translationChartB (η D : M4) : M4 :=
  1 + η * D

/-- Translation-chart shift `C = D` (memo (30.4)). -/
def translationChartC (D : M4) : M4 :=
  D

/-- Reconstruction operator `L_K(X) = X - η X K` (memo (30.7)). -/
def reconstructionLK (η K : M4) (X : M4) : M4 :=
  X - η * X * K

/-- Candidate right-inverse companion `R_K(X) = X + η X K`. -/
def reconstructionRK (η K : M4) (X : M4) : M4 :=
  X + η * X * K

theorem reconstructionLK_add (η K X Y : M4) :
    reconstructionLK η K (X + Y) =
      reconstructionLK η K X + reconstructionLK η K Y := by
  simp only [reconstructionLK, mul_add, add_mul]
  abel

/-! ## 5. Explicit regularity boundary (packaged separately) -/

/-- Invertibility of the raw solder / coframe map `B_e`. -/
def BInvertible (B_e : M4) : Prop :=
  IsUnit B_e.det

/-- Invertibility of the reconstruction operator `L_K`. -/
def LKInvertible (η K : M4) : Prop :=
  Function.Bijective (reconstructionLK η K)

/-- Regular-branch hypotheses: both invertibility boundaries, kept unbundled. -/
structure RegularAEPassportBoundary (B_e C_A η : M4) : Prop where
  B_e_invertible : BInvertible B_e
  L_K_invertible : LKInvertible η (regularPassportK B_e C_A)

theorem BInvertible.nonsing_inv_mul {B_e : M4} (h : BInvertible B_e) :
    B_e⁻¹ * B_e = 1 :=
  Matrix.nonsing_inv_mul B_e h

theorem BInvertible.mul_nonsing_inv {B_e : M4} (h : BInvertible B_e) :
    B_e * B_e⁻¹ = 1 :=
  Matrix.mul_nonsing_inv B_e h

/-! ## 1. Pure-linear transformation (frame invariance) -/

/-- Under `B'_e = g B_e` and `C'_A = g C_A` with invertible `g` and `B_e`,
one has `K' = K` (memo (30.2)–(30.3)). -/
theorem regularPassportK_pureLinear (g B_e C_A : M4)
    (hg : BInvertible g) (hB : BInvertible B_e) :
    regularPassportK (g * B_e) (g * C_A) = regularPassportK B_e C_A := by
  have hinv : (g * B_e)⁻¹ = B_e⁻¹ * g⁻¹ := by
    refine Matrix.inv_eq_right_inv ?_
    calc
      (g * B_e) * (B_e⁻¹ * g⁻¹)
          = g * (B_e * B_e⁻¹) * g⁻¹ := by simp [mul_assoc]
      _ = g * (1 : M4) * g⁻¹ := by rw [hB.mul_nonsing_inv]
      _ = 1 := by simp [hg.mul_nonsing_inv]
  calc
    regularPassportK (g * B_e) (g * C_A)
        = (g * B_e)⁻¹ * (g * C_A) := rfl
    _ = B_e⁻¹ * g⁻¹ * (g * C_A) := by rw [hinv]
    _ = B_e⁻¹ * (g⁻¹ * g) * C_A := by simp [mul_assoc]
    _ = B_e⁻¹ * (1 : M4) * C_A := by rw [hg.nonsing_inv_mul]
    _ = regularPassportK B_e C_A := by simp [regularPassportK]

/-! ## 2–3. Translation-chart identities -/

theorem translationChart_BK (η D : M4)
    (hB : BInvertible (translationChartB η D)) :
    translationChartB η D *
        regularPassportK (translationChartB η D) (translationChartC D) = D := by
  calc
    _ = translationChartB η D * ((translationChartB η D)⁻¹ * D) := by
      simp [regularPassportK, translationChartC]
    _ = (translationChartB η D * (translationChartB η D)⁻¹) * D := by
      simp [mul_assoc]
    _ = (1 : M4) * D := by rw [hB.mul_nonsing_inv]
    _ = D := by simp

/-- Translation-chart identity `D - η D K = K` (memo (30.5)). -/
theorem translation_chart_identity (η D : M4)
    (hB : BInvertible (translationChartB η D)) :
    let K := regularPassportK (translationChartB η D) (translationChartC D)
    D - η * D * K = K := by
  intro K
  have hBK : translationChartB η D * K = D := translationChart_BK η D hB
  have hlin : K + η * D * K = D := by
    calc
      K + η * D * K = (1 + η * D) * K := by
        simp [add_mul, one_mul, mul_assoc]
      _ = translationChartB η D * K := rfl
      _ = D := hBK
  -- From `K + ηDK = D` rearrange to `D - ηDK = K`.
  exact (eq_sub_of_add_eq hlin).symm

/-- Equivalent B-hat identity `B - η B K = I` (memo (30.6)). -/
theorem translation_chart_B_hat_identity (η D : M4)
    (hB : BInvertible (translationChartB η D)) :
    let B := translationChartB η D
    let K := regularPassportK B (translationChartC D)
    B - η * B * K = 1 := by
  intro B K
  have hBK : B * K = D := translationChart_BK η D hB
  calc
    B - η * B * K = B - η * D := by rw [← hBK]; simp [mul_assoc]
    _ = (1 + η * D) - η * D := rfl
    _ = 1 := by abel

/-! ## Nilpotent-shear reconstruction invertibility helper -/

theorem reconstructionLK_nilpotent_inverse (η K : M4)
    (hη : η * η = 1) (hK : K * K = 0) (X : M4) :
    reconstructionLK η K (reconstructionRK η K X) = X ∧
      reconstructionRK η K (reconstructionLK η K X) = X := by
  constructor
  · simp only [reconstructionLK, reconstructionRK]
    have h1 : η * (X + η * X * K) * K =
        η * X * K + (η * η) * X * (K * K) := by
      simp [mul_add, add_mul, mul_assoc]
    simp [h1, hη, hK]
  · simp only [reconstructionLK, reconstructionRK]
    have h1 : η * (X - η * X * K) * K =
        η * X * K - (η * η) * X * (K * K) := by
      simp [mul_sub, sub_mul, mul_assoc]
    simp [h1, hη, hK]

theorem LKInvertible_of_nilpotent (η K : M4)
    (hη : η * η = 1) (hK : K * K = 0) :
    LKInvertible η K := by
  refine Function.bijective_iff_has_inverse.mpr ⟨reconstructionRK η K, ?_, ?_⟩
  · intro X; exact (reconstructionLK_nilpotent_inverse η K hη hK X).2
  · intro X; exact (reconstructionLK_nilpotent_inverse η K hη hK X).1

/-! ## 4. Reconstruction uniqueness -/

theorem reconstruction_solution_D (η D : M4)
    (hB : BInvertible (translationChartB η D)) :
    reconstructionLK η
        (regularPassportK (translationChartB η D) (translationChartC D)) D =
      regularPassportK (translationChartB η D) (translationChartC D) := by
  simpa [reconstructionLK] using translation_chart_identity η D hB

theorem reconstruction_unique_of_injective (η K : M4)
    (hinj : Function.Injective (reconstructionLK η K))
    (X₁ X₂ : M4)
    (h₁ : reconstructionLK η K X₁ = K)
    (h₂ : reconstructionLK η K X₂ = K) :
    X₁ = X₂ :=
  hinj (h₁.trans h₂.symm)

theorem reconstruction_unique_eq_D (η D : M4)
    (hB : BInvertible (translationChartB η D))
    (hinj : Function.Injective
      (reconstructionLK η
        (regularPassportK (translationChartB η D) (translationChartC D))))
    (X : M4)
    (hX : reconstructionLK η
        (regularPassportK (translationChartB η D) (translationChartC D)) X =
      regularPassportK (translationChartB η D) (translationChartC D)) :
    X = D :=
  reconstruction_unique_of_injective η _ hinj X D hX
    (reconstruction_solution_D η D hB)

theorem reconstruction_exists_unique_of_bijective (η K : M4)
    (hbij : LKInvertible η K) :
    ∃! X : M4, reconstructionLK η K X = K := by
  obtain ⟨X, hX⟩ := hbij.2 K
  refine ⟨X, hX, fun Y hY => hbij.1 (hY.trans hX.symm)⟩

theorem regular_passport_unique_D (η D : M4)
    (hB : BInvertible (translationChartB η D))
    (hL : LKInvertible η
      (regularPassportK (translationChartB η D) (translationChartC D))) :
    ∃! X : M4,
      reconstructionLK η
          (regularPassportK (translationChartB η D) (translationChartC D)) X =
        regularPassportK (translationChartB η D) (translationChartC D) := by
  refine ExistsUnique.intro D (reconstruction_solution_D η D hB) ?_
  intro X hX
  exact reconstruction_unique_eq_D η D hB hL.1 X hX

/-! ## 6. Singular-locus firewall -/

/-- Outside `L_K`-injectivity the reconstruction equation is non-unique.
Does **not** claim the singular locus is physically excluded. -/
theorem singular_LK_nonunique (η K N : M4) (hN : N ≠ 0)
    (hker : reconstructionLK η K N = 0) :
    ¬ Function.Injective (reconstructionLK η K) ∧
      ∀ X : M4, reconstructionLK η K X = K →
        reconstructionLK η K (X + N) = K ∧ X + N ≠ X := by
  refine ⟨?_, ?_⟩
  · intro hinj
    exact hN (hinj (by simpa [reconstructionLK] using hker))
  · intro X hX
    refine ⟨?_, by simpa using hN⟩
    calc
      reconstructionLK η K (X + N)
          = reconstructionLK η K X + reconstructionLK η K N :=
            reconstructionLK_add η K X N
      _ = K + 0 := by rw [hX, hker]
      _ = K := by simp

/-- Singular `B_e` blocks the two-sided inverse identity used by `K = B⁻¹ C`. -/
theorem singular_B_blocks_passport_inverse (B_e : M4) (hSing : ¬ BInvertible B_e) :
    ¬ (B_e * B_e⁻¹ = 1) := by
  intro h
  have : IsUnit B_e.det := by
    have hdet : B_e.det * (B_e⁻¹).det = (1 : M4).det := by
      simpa [det_mul] using congrArg Matrix.det h
    simp only [det_one] at hdet
    exact isUnit_iff_exists_inv.mpr ⟨(B_e⁻¹).det, hdet⟩
  exact hSing this

theorem singular_B_blocks_passport_left_inverse (B_e : M4) (hSing : ¬ BInvertible B_e) :
    ¬ (B_e⁻¹ * B_e = 1) := by
  intro h
  have : IsUnit B_e.det := by
    have hdet : (B_e⁻¹).det * B_e.det = (1 : M4).det := by
      simpa [det_mul] using congrArg Matrix.det h
    simp only [det_one] at hdet
    exact isUnit_iff_exists_inv.mpr ⟨(B_e⁻¹).det, by simpa [mul_comm] using hdet⟩
  exact hSing this

/-! ## Exact controls -/

theorem flat_D_zero_K_zero (η : M4) :
    regularPassportK (translationChartB η 0) (translationChartC 0) = 0 := by
  have hB : translationChartB η 0 = (1 : M4) := by simp [translationChartB]
  simp [regularPassportK, translationChartC, hB]

theorem flat_LK_id (η : M4) :
    reconstructionLK η 0 = id := by
  funext X; simp [reconstructionLK]

theorem flat_LK_invertible (η : M4) : LKInvertible η 0 := by
  change Function.Bijective (reconstructionLK η 0)
  rw [flat_LK_id]
  exact Function.bijective_id

/-- Nonzero rational shear `D = E_{0,1}` (entry `(0,1) = 1`). -/
def exampleRegularD : M4 :=
  !![0, 1, 0, 0; 0, 0, 0, 0; 0, 0, 0, 0; 0, 0, 0, 0]

def exampleRegularB : M4 :=
  translationChartB passportEta exampleRegularD

theorem exampleRegularB_eq :
    exampleRegularB = !![1, 1, 0, 0; 0, 1, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1] := by
  native_decide

theorem exampleRegularB_det : exampleRegularB.det = 1 := by
  rw [exampleRegularB_eq]; native_decide

theorem exampleRegularB_invertible : BInvertible exampleRegularB := by
  simp [BInvertible, exampleRegularB_det]

theorem exampleRegularD_sq : exampleRegularD * exampleRegularD = 0 := by
  native_decide

theorem exampleRegularK_eq_D :
    regularPassportK exampleRegularB (translationChartC exampleRegularD) =
      exampleRegularD := by
  have hInv : exampleRegularB⁻¹ =
      !![1, -1, 0, 0; 0, 1, 0, 0; 0, 0, 1, 0; 0, 0, 0, 1] := by
    refine Matrix.inv_eq_left_inv ?_
    rw [exampleRegularB_eq]; native_decide
  simp only [regularPassportK, translationChartC, hInv, exampleRegularD]
  native_decide

theorem exampleRegular_translation_identity :
    exampleRegularD - passportEta * exampleRegularD *
        regularPassportK exampleRegularB (translationChartC exampleRegularD) =
      regularPassportK exampleRegularB (translationChartC exampleRegularD) :=
  translation_chart_identity passportEta exampleRegularD exampleRegularB_invertible

theorem exampleRegular_B_hat_identity :
    exampleRegularB - passportEta * exampleRegularB *
        regularPassportK exampleRegularB (translationChartC exampleRegularD) = 1 :=
  translation_chart_B_hat_identity passportEta exampleRegularD exampleRegularB_invertible

theorem exampleRegular_LK_invertible :
    LKInvertible passportEta
      (regularPassportK exampleRegularB (translationChartC exampleRegularD)) := by
  rw [exampleRegularK_eq_D]
  exact LKInvertible_of_nilpotent passportEta exampleRegularD passportEta_sq
    exampleRegularD_sq

theorem exampleRegular_boundary :
    RegularAEPassportBoundary exampleRegularB (translationChartC exampleRegularD)
      passportEta where
  B_e_invertible := exampleRegularB_invertible
  L_K_invertible := exampleRegular_LK_invertible

/-- Singular `K = η`: `L_η(η) = 0`. -/
def exampleSingularK : M4 := passportEta

theorem exampleSingular_ker :
    reconstructionLK passportEta exampleSingularK passportEta = 0 := by
  simp only [reconstructionLK, exampleSingularK]
  have h : passportEta * passportEta * passportEta = passportEta := by
    rw [passportEta_sq, one_mul]
  rw [h, sub_self]

theorem exampleSingular_nonunique :
    ¬ Function.Injective (reconstructionLK passportEta exampleSingularK) ∧
      ∀ X : M4, reconstructionLK passportEta exampleSingularK X = exampleSingularK →
        reconstructionLK passportEta exampleSingularK (X + passportEta) =
          exampleSingularK ∧ X + passportEta ≠ X :=
  singular_LK_nonunique passportEta exampleSingularK passportEta
    (by native_decide) exampleSingular_ker

theorem exampleSingularB_zero_blocks :
    ¬ BInvertible (0 : M4) ∧ ¬ ((0 : M4) * (0 : M4)⁻¹ = 1) := by
  have hSing : ¬ BInvertible (0 : M4) := by
    simp [BInvertible, Matrix.det_zero]
  exact ⟨hSing, singular_B_blocks_passport_inverse 0 hSing⟩

/-! ## 7. Optional vectorization -/

/-- `vec(L_K(X)) = (I - Kᵀ ⊗ η) vec(X)` (memo (30.8)). -/
theorem reconstructionLK_vectorize (η K X : M4) :
    vec (reconstructionLK η K X) =
      (1 - Kᵀ ⊗ₖ η) *ᵥ vec X := by
  have hηXK : vec (η * X * K) = (Kᵀ ⊗ₖ η) *ᵥ vec X := by
    -- `(B ⊗ₖ A) *ᵥ vec X = vec (A * X * Bᵀ)` with `A = η`, `B = Kᵀ`
    simpa using (kronecker_mulVec_vec (A := η) (B := Kᵀ) (X := X)).symm
  simp only [reconstructionLK, vec_sub, hηXK, sub_mulVec, one_mulVec]

end
end D0.Geometry.A4DRegularAEPassport
