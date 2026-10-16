import D0.Representation.GoldenCoherentMemory
import D0.Representation.GoldenOrderInterferometer
import Mathlib.Data.Matrix.Block
import Mathlib.Tactic

/-! Research kernel: exact forward echo, complete switching block, fixed-word
Gram obstruction and composed feedback. Scene addressing and full spectral
binding are checked separately; no physical admission or supported CORE claim. -/
namespace D0.Research.AutonomousRecordProgram
noncomputable section
open Matrix
open D0.Representation.GoldenOrderInterferometer

def swapBit : Matrix (Fin 2) (Fin 2) ℝ := !![0,1; 1,0]

theorem forward_echo (a p : ℝ) :
    swapBit * gate a p * swapBit = (gate a p).transpose := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [swapBit, gate, Matrix.mul_apply, Fin.sum_univ_two]

theorem golden_both_orthogonal (a p : ℝ) (ha : a^2=p) (hp : p+p^2=1) :
    (gate a p).transpose * gate a p = 1 ∧
    gate a p * (gate a p).transpose = 1 := by
  refine ⟨gate_orthogonal a p ha hp, ?_⟩
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [gate, Matrix.mul_apply, Fin.sum_univ_two] <;> nlinarith

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The three chronological operations are f-echo, c-echo, then KG. -/
def wordBranch (K G : Matrix n n ℝ) (c f : Bool) : Matrix n n ℝ :=
  (K*G) * (if c then G.transpose else G) * (if f then G.transpose else G)

theorem full_four_branches (K G : Matrix n n ℝ)
    (hleft : G.transpose*G=1) (hright : G*G.transpose=1) :
    wordBranch K G true false = K*G ∧
    wordBranch K G true true = K*G.transpose ∧
    wordBranch K G false false = K*G^3 ∧
    wordBranch K G false true = K*G := by
  simp only [wordBranch, Bool.false_eq_true, ↓reduceIte]
  refine ⟨?_, ?_, ?_, ?_⟩
  · rw [Matrix.mul_assoc, hleft, Matrix.mul_one]
  · rw [Matrix.mul_assoc K G G.transpose, hright, Matrix.mul_one]
  · simp [pow_succ, Matrix.mul_assoc]
  · rw [Matrix.mul_assoc (K*G), hright, Matrix.mul_one]

/-- Both switch values are in the complete carrier. -/
def switchBlock (U V : Matrix n n ℝ) : Matrix (n ⊕ n) (n ⊕ n) ℝ :=
  Matrix.fromBlocks 0 V U 0

theorem complete_switch_orthogonal (U V : Matrix n n ℝ)
    (hU : U.transpose*U=1) (hV : V.transpose*V=1) :
    (switchBlock U V).transpose * switchBlock U V = 1 := by
  simp [switchBlock, Matrix.fromBlocks_transpose, Matrix.fromBlocks_multiply, hU, hV]

theorem complete_switch_two_ticks (U V : Matrix n n ℝ) :
    switchBlock U V * switchBlock U V = Matrix.fromBlocks (V*U) 0 0 (U*V) := by
  simp [switchBlock, Matrix.fromBlocks_multiply]

def x2 (a p : ℝ) : Fin 4 → ℝ := ![-2*a*p, 2*p-1, 0, 1]
def x3 (a p : ℝ) : Fin 4 → ℝ := ![5*p-4, a*(4*p-3), -p, -a]
def x4 (a p : ℝ) : Fin 4 → ℝ := ![-2*a*p, 2*p-1, -2*a*p, 2*p-1]

theorem consecutive_gram_gap (a p : ℝ) (hp : p+p^2=1) :
    dotProduct (x2 a p) (x3 a p) = 0 ∧
    dotProduct (x3 a p) (x4 a p) = 4*a*p^2 := by
  simp only [dotProduct, x2, x3, x4, Fin.sum_univ_succ, Fin.sum_univ_zero]
  constructor
  · dsimp; linear_combination -2*a*hp
  · dsimp; linear_combination -4*a*hp

theorem no_fixed_inner_product_preserver (a p : ℝ) (ha0 : 0<a)
    (hp0 : 0<p) (hp : p+p^2=1)
    (F : (Fin 4 → ℝ) → (Fin 4 → ℝ))
    (hF : ∀ u v, dotProduct (F u) (F v) = dotProduct u v) :
    ¬ (F (x2 a p) = x3 a p ∧ F (x3 a p) = x4 a p) := by
  intro h
  have hg := hF (x2 a p) (x3 a p)
  rw [h.1, h.2] at hg
  obtain ⟨h0,h1⟩ := consecutive_gram_gap a p hp
  rw [h0,h1] at hg
  have hpos : 0 < 4*a*p^2 := mul_pos (by positivity) (sq_pos_of_pos hp0)
  linarith

/-- Works in arbitrary finite dimension; the actual scene pairing determines
why its compression Gram is p*T*T, rather than p*T.transpose*T. -/
theorem golden_scene_feedback (p : ℝ) (hp : p+p^2=1) (T : Matrix n n ℝ) :
    1 - p • (T*T) = p^2 • (1 : Matrix n n ℝ) + p • (2 • (1-T) - (1-T)*(1-T)) := by
  have hid : 2 • (1-T) - (1-T)*(1-T) = (1 : Matrix n n ℝ)-T*T := by
    simp only [two_smul]
    noncomm_ring
  rw [hid, smul_sub, ← add_sub_assoc, ← add_smul]
  have hc : p^2+p=1 := by linarith
  rw [hc, one_smul]

theorem two_tick_golden_loss (p : ℝ) (hp : p+p^2=1) :
    1-(2*p-1)^2=4*p^3 := by
  linear_combination -4*p*hp

end
end D0.Research.AutonomousRecordProgram

#check D0.Research.AutonomousRecordProgram.full_four_branches
#check D0.Research.AutonomousRecordProgram.no_fixed_inner_product_preserver
#check D0.Research.AutonomousRecordProgram.golden_scene_feedback
#print axioms D0.Research.AutonomousRecordProgram.forward_echo
#print axioms D0.Research.AutonomousRecordProgram.golden_both_orthogonal
#print axioms D0.Research.AutonomousRecordProgram.full_four_branches
#print axioms D0.Research.AutonomousRecordProgram.complete_switch_orthogonal
#print axioms D0.Research.AutonomousRecordProgram.complete_switch_two_ticks
#print axioms D0.Research.AutonomousRecordProgram.consecutive_gram_gap
#print axioms D0.Research.AutonomousRecordProgram.no_fixed_inner_product_preserver
#print axioms D0.Research.AutonomousRecordProgram.golden_scene_feedback
#print axioms D0.Research.AutonomousRecordProgram.two_tick_golden_loss
#print axioms D0.Representation.GoldenCoherentMemory.fullStep_orthogonal
