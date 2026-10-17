import D0.Representation.GoldenCoherentMemory
import Mathlib.Tactic

/-! The literal golden apparatus commutant and a necessary observer-domain
test. No operation admission, physical heat law or supported CORE owner. -/
namespace D0.Research.FockRecordBinding
noncomputable section
open Matrix D0.Representation.GoldenCoherentMemory

def priceCut : Matrix (Fin 4) (Fin 4) ℝ := !![1,0,0,0;0,1,0,0;0,0,0,0;0,0,0,0]
def blankCut : Matrix (Fin 4) (Fin 4) ℝ := !![1,0,0,0;0,0,0,0;0,0,1,0;0,0,0,0]

theorem literal_apparatus_commutant_scalar (a p : ℝ) (hp : p ≠ 0)
    (X : Matrix (Fin 4) (Fin 4) ℝ)
    (hU : X * fullStep a p = fullStep a p * X)
    (hP : X * priceCut = priceCut * X)
    (hB : X * blankCut = blankCut * X) :
    ∃ c : ℝ, X = c • (1 : Matrix (Fin 4) (Fin 4) ℝ) := by
  have hd : ∀ i j, i ≠ j → X i j = 0 := by
    intro i j hij
    have hpij := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M i j) hP
    have hbij := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M i j) hB
    fin_cases i <;> fin_cases j <;> try contradiction
    all_goals
      simp [priceCut, blankCut, Matrix.mul_apply, Fin.sum_univ_succ] at hpij hbij
      first | exact hpij | exact hpij.symm | exact hbij | exact hbij.symm
  have hd02 : X 0 2 = 0 := hd 0 2 (by decide)
  have hd03 : X 0 3 = 0 := hd 0 3 (by decide)
  have hd21 : X 2 1 = 0 := hd 2 1 (by decide)
  have hd31 : X 3 1 = 0 := hd 3 1 (by decide)
  have hd12 : X 1 2 = 0 := hd 1 2 (by decide)
  have hd13 : X 1 3 = 0 := hd 1 3 (by decide)
  have h02 : X 0 0 = X 2 2 := by
    have h := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 0 2) hU
    simp [fullStep, Matrix.mul_apply, Fin.sum_univ_succ, hd02, hd03] at h
    apply mul_left_cancel₀ hp
    nlinarith [h]
  have h21 : X 2 2 = X 1 1 := by
    have h := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 2 1) hU
    simp [fullStep, Matrix.mul_apply, Fin.sum_univ_succ, hd21, hd31] at h
    apply mul_left_cancel₀ hp
    nlinarith [h]
  have h13 : X 1 1 = X 3 3 := by
    have h := congrArg (fun M : Matrix (Fin 4) (Fin 4) ℝ => M 1 3) hU
    simp [fullStep, Matrix.mul_apply, Fin.sum_univ_succ, hd12, hd13] at h
    apply mul_left_cancel₀ hp
    nlinarith [h]
  have h11 : X 1 1 = X 0 0 := h21.symm.trans h02.symm
  have h22 : X 2 2 = X 0 0 := h02.symm
  have h33 : X 3 3 = X 0 0 := h13.symm.trans h11
  refine ⟨X 0 0, ?_⟩
  ext i j
  by_cases hij : i = j
  · subst j
    fin_cases i <;> simp [Matrix.smul_apply, h11, h22, h33]
  · simp [Matrix.smul_apply, hij, hd i j hij]

theorem golden_root_gt_half (p : ℝ) (hp : p+p^2=1) (hp0 : 0<p) :
    (1:ℝ)/2 < p := by
  by_contra h
  have hle : p ≤ (1:ℝ)/2 := le_of_not_gt h
  have hm := mul_nonneg hp0.le (sub_nonneg.mpr hle)
  nlinarith

theorem golden_full_gate_spacelike_first_grade (a p : ℝ)
    (ha : a^2=p) (hp : p+p^2=1) (hp0 : 0<p) :
    a^2-(2*p)^2 < 0 := by
  have hh := golden_root_gt_half p hp hp0
  have hn : 1-4*p < 0 := by linarith
  have h := mul_neg_of_pos_of_neg hp0 hn
  nlinarith

end
end D0.Research.FockRecordBinding

#check D0.Research.FockRecordBinding.literal_apparatus_commutant_scalar
#check D0.Research.FockRecordBinding.golden_full_gate_spacelike_first_grade
#print axioms D0.Research.FockRecordBinding.literal_apparatus_commutant_scalar
#print axioms D0.Research.FockRecordBinding.golden_root_gt_half
#print axioms D0.Research.FockRecordBinding.golden_full_gate_spacelike_first_grade
#print axioms D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
#print axioms D0.Representation.GoldenCoherentMemory.blank_record_evolution
