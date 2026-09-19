import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.Notation
import D0.Representation.TypedRepresentationFunctor
import D0.Extensions.RepresentationReadoutExtension
import D0.Synthesis.Z2SpinorCover

namespace D0.Representation.CompatibleInvolutionClassification

open Matrix
open D0.Representation.TypedRepresentationFunctor
open D0.Extensions.RepresentationReadoutExtension

abbrev M3 := Matrix (Fin 3) (Fin 3) ℚ

def gPPP : M3 := !![1,0,0; 0,1,0; 0,0,1]
def gPPM : M3 := !![1,0,0; 0,1,0; 0,0,-1]
def gPMP : M3 := !![1,0,0; 0,-1,0; 0,0,1]
def gPMM : M3 := !![1,0,0; 0,-1,0; 0,0,-1]
def gMPP : M3 := !![-1,0,0; 0,1,0; 0,0,1]
def gMPM : M3 := !![-1,0,0; 0,1,0; 0,0,-1]
def gMMP : M3 := !![-1,0,0; 0,-1,0; 0,0,1]
def gMMM : M3 := !![-1,0,0; 0,-1,0; 0,0,-1]

def CompatibleInvolution (X : M3) : Prop :=
  X * degreeOp = degreeOp * X ∧ X * X = (1 : M3)

def NonScalar (X : M3) : Prop :=
  X ≠ (1 : M3) ∧ X ≠ -(1 : M3)

private theorem rat_square_one_pm_one (x : ℚ) (h : x * x = 1) :
    x = 1 ∨ x = -1 := by
  have hf : (x - 1) * (x + 1) = 0 := by
    nlinarith
  rcases mul_eq_zero.mp hf with h1 | h1
  · left; linarith
  · right; linarith

theorem compatible_diagonal_signs
    (X : M3) (h : CompatibleInvolution X) :
    (X 0 0 = 1 ∨ X 0 0 = -1) ∧
    (X 1 1 = 1 ∨ X 1 1 = -1) ∧
    (X 2 2 = 1 ∨ X 2 2 = -1) := by
  rcases h with ⟨hcomm, hinv⟩
  have hoff := degree_commutant_diagonal X hcomm
  have h01 : X 0 1 = 0 := hoff 0 1 (by decide)
  have h02 : X 0 2 = 0 := hoff 0 2 (by decide)
  have h10 : X 1 0 = 0 := hoff 1 0 (by decide)
  have h12 : X 1 2 = 0 := hoff 1 2 (by decide)
  have h20 : X 2 0 = 0 := hoff 2 0 (by decide)
  have h21 : X 2 1 = 0 := hoff 2 1 (by decide)
  have h00 := congrArg (fun M : M3 => M 0 0) hinv
  have h11 := congrArg (fun M : M3 => M 1 1) hinv
  have h22 := congrArg (fun M : M3 => M 2 2) hinv
  simp [Matrix.mul_apply, Fin.sum_univ_three, h01, h02, h10, h12, h20, h21] at h00 h11 h22
  exact ⟨rat_square_one_pm_one _ h00,
    rat_square_one_pm_one _ h11,
    rat_square_one_pm_one _ h22⟩

theorem compatible_involution_eightfold
    (X : M3) (h : CompatibleInvolution X) :
    X = gPPP ∨ X = gPPM ∨ X = gPMP ∨ X = gPMM ∨
    X = gMPP ∨ X = gMPM ∨ X = gMMP ∨ X = gMMM := by
  rcases h with ⟨hcomm, hinv⟩
  have hoff := degree_commutant_diagonal X hcomm
  have h01 : X 0 1 = 0 := hoff 0 1 (by decide)
  have h02 : X 0 2 = 0 := hoff 0 2 (by decide)
  have h10 : X 1 0 = 0 := hoff 1 0 (by decide)
  have h12 : X 1 2 = 0 := hoff 1 2 (by decide)
  have h20 : X 2 0 = 0 := hoff 2 0 (by decide)
  have h21 : X 2 1 = 0 := hoff 2 1 (by decide)
  rcases compatible_diagonal_signs X ⟨hcomm, hinv⟩ with ⟨h0, h1, h2⟩
  rcases h0 with h0 | h0 <;>
    rcases h1 with h1 | h1 <;>
    rcases h2 with h2 | h2
  · left
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gPPP, h0, h1, h2, h01, h02, h10, h12, h20, h21]
  · right; left
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gPPM, h0, h1, h2, h01, h02, h10, h12, h20, h21]
  · right; right; left
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gPMP, h0, h1, h2, h01, h02, h10, h12, h20, h21]
  · right; right; right; left
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gPMM, h0, h1, h2, h01, h02, h10, h12, h20, h21]
  · right; right; right; right; left
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gMPP, h0, h1, h2, h01, h02, h10, h12, h20, h21]
  · right; right; right; right; right; left
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gMPM, h0, h1, h2, h01, h02, h10, h12, h20, h21]
  · right; right; right; right; right; right; left
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gMMP, h0, h1, h2, h01, h02, h10, h12, h20, h21]
  · right; right; right; right; right; right; right
    ext i j
    fin_cases i <;> fin_cases j <;>
      simp [gMMM, h0, h1, h2, h01, h02, h10, h12, h20, h21]

def positiveCount (X : M3) : ℕ :=
  (if X 0 0 = 1 then 1 else 0) +
  (if X 1 1 = 1 then 1 else 0) +
  (if X 2 2 = 1 then 1 else 0)

def negativeCount (X : M3) : ℕ := 3 - positiveCount X

def ncReadout (X : M3) : ℕ :=
  ncCount (positiveCount X) (negativeCount X)

theorem gPPP_eq_one : gPPP = (1 : M3) := by native_decide
theorem gMMM_eq_neg_one : gMMM = -(1 : M3) := by native_decide

theorem nonscalar_compatible_involution_nc
    (X : M3) (hcompat : CompatibleInvolution X) (hnon : NonScalar X) :
    ncReadout X = 8 := by
  rcases compatible_involution_eightfold X hcompat with
      h | h | h | h | h | h | h | h
  · exfalso
    exact hnon.1 (h.trans gPPP_eq_one)
  · rw [h]
    native_decide
  · rw [h]
    native_decide
  · rw [h]
    native_decide
  · rw [h]
    native_decide
  · rw [h]
    native_decide
  · rw [h]
    native_decide
  · exfalso
    exact hnon.2 (h.trans gMMM_eq_neg_one)

theorem compatible_involution_scalar_or_nc8
    (X : M3) (hcompat : CompatibleInvolution X) :
    X = (1 : M3) ∨ X = -(1 : M3) ∨ ncReadout X = 8 := by
  by_cases hp : X = (1 : M3)
  · exact Or.inl hp
  by_cases hm : X = -(1 : M3)
  · exact Or.inr (Or.inl hm)
  · exact Or.inr (Or.inr
      (nonscalar_compatible_involution_nc X hcompat ⟨hp, hm⟩))

theorem representation_residual_reduced_to_nonscalar :
    ∀ X : M3, CompatibleInvolution X → NonScalar X → ncReadout X = 8 :=
  nonscalar_compatible_involution_nc


/-- The direct scene-step orientation sign on the three zone addresses 9, 11, 13. -/
def sceneParitySign : Fin 3 → ℚ
  | 0 => ((Matrix.det (D0.Dynamics.T ^ 9) : ℤ) : ℚ)
  | 1 => ((Matrix.det (D0.Dynamics.T ^ 11) : ℤ) : ℚ)
  | 2 => ((Matrix.det (D0.Dynamics.T ^ 13) : ℤ) : ℚ)

/-- The grading obtained by using only the toral/address orientation parity. -/
def sceneParityGrading : M3 := Matrix.diagonal sceneParitySign

/-- The +2 address progression preserves the orientation sheet, so all three
generation-zone addresses carry the same odd sign. -/
theorem scene_parity_signs_all_negative :
    sceneParitySign 0 = -1 ∧ sceneParitySign 1 = -1 ∧ sceneParitySign 2 = -1 := by
  native_decide

/-- Therefore the direct scene-parity grading is scalar: it is exactly minus identity. -/
theorem sceneParityGrading_eq_neg_one :
    sceneParityGrading = -(1 : M3) := by
  native_decide


/-- The direct scene-parity operator is a perfectly valid compatible involution; its
failure is not algebraic admissibility but scalarity. -/
theorem sceneParityGrading_compatible :
    CompatibleInvolution sceneParityGrading := by
  rw [sceneParityGrading_eq_neg_one]
  constructor <;> native_decide

/-- Consequently the direct +2 scene parity gives the scalar nc=12 branch, not nc=8. -/
theorem scene_parity_nc_is_twelve :
    ncReadout sceneParityGrading = 12 := by
  rw [sceneParityGrading_eq_neg_one]
  native_decide

/-- Sharp route exclusion: the already-owned address parity cannot by itself be recycled
as the missing non-scalar generation grading. -/
theorem scene_parity_cannot_supply_nc8 :
    ncReadout sceneParityGrading ≠ 8 := by
  rw [scene_parity_nc_is_twelve]
  decide

end D0.Representation.CompatibleInvolutionClassification
