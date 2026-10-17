import D0.Core.Phi
import D0.Algebra.FibonacciAFTower
import Mathlib.Tactic

/-! Scalar backbone of the literal phi-martingale heat / scene comparison.
The operator-norm and semigroup applications are analytic in the companion proof.
No physical admission, new heat law or native field preparation is assumed here. -/
namespace D0.Research.AFSceneHeatComparison

theorem phi_squared_gap : (64 / 25 : ℝ) ≤ D0.phi ^ 2 := by
  have hs := D0.sqrt_five_sq
  have hn := Real.sqrt_nonneg (5 : ℝ)
  have hl : (11 / 5 : ℝ) < Real.sqrt 5 := by nlinarith
  have hp : (8 / 5 : ℝ) < D0.phi := by unfold D0.phi; linarith
  nlinarith [D0.phi_sq]

theorem successive_ladder_gap (c b : ℝ) (hc : 0 < c)
    (hb : (64 / 25 : ℝ) ≤ b) (i j : ℕ) (hij : i < j) :
    (64 / 25 : ℝ) * (c * b ^ i) ≤ c * b ^ j := by
  have hb1 : 1 ≤ b := by linarith
  have hbi : 0 ≤ c * b ^ i := mul_nonneg hc.le (pow_nonneg (by linarith) _)
  calc
    (64 / 25 : ℝ) * (c * b ^ i) ≤ b * (c * b ^ i) :=
      mul_le_mul_of_nonneg_right hb hbi
    _ = c * b ^ (i + 1) := by rw [pow_succ]; ring
    _ ≤ c * b ^ j := mul_le_mul_of_nonneg_left
      (pow_le_pow_right₀ hb1 (Nat.succ_le_of_lt hij)) hc.le

theorem ladder_separated (c b : ℝ) (hc : 0 < c)
    (hb : (64 / 25 : ℝ) ≤ b) (i j : ℕ) :
    c * b ^ i = c * b ^ j ∨
      (64 / 25 : ℝ) * (c * b ^ i) ≤ c * b ^ j ∨
      (64 / 25 : ℝ) * (c * b ^ j) ≤ c * b ^ i := by
  rcases lt_trichotomy i j with h | h | h
  · exact Or.inr (Or.inl (successive_ladder_gap c b hc hb i j h))
  · exact Or.inl (by rw [h])
  · exact Or.inr (Or.inr (successive_ladder_gap c b hc hb j i h))

theorem three_bands_incompatible (x y z : ℝ)
    (hxy : x = y ∨ (64 / 25 : ℝ) * x ≤ y ∨ (64 / 25 : ℝ) * y ≤ x)
    (hyz : y = z ∨ (64 / 25 : ℝ) * y ≤ z ∨ (64 / 25 : ℝ) * z ≤ y)
    (hx : |x - 20| < (13 / 2 : ℝ))
    (hy : |y - 22| < (13 / 2 : ℝ))
    (hz : |z - 33| < (13 / 2 : ℝ)) : False := by
  rcases abs_lt.mp hx with ⟨hxl,hxu⟩
  rcases abs_lt.mp hy with ⟨hyl,hyu⟩
  rcases abs_lt.mp hz with ⟨hzl,hzu⟩
  have he1 : x = y := by
    rcases hxy with h | h | h
    · exact h
    · linarith
    · linarith
  have he2 : y = z := by
    rcases hyz with h | h | h
    · exact h
    · linarith
    · linarith
  linarith

theorem no_phi_squared_triple_approximation (c : ℝ) (hc : 0 < c)
    (i j k : ℕ) :
    ¬ (|c * (D0.phi ^ 2) ^ i - 20| < (13 / 2 : ℝ) ∧
       |c * (D0.phi ^ 2) ^ j - 22| < (13 / 2 : ℝ) ∧
       |c * (D0.phi ^ 2) ^ k - 33| < (13 / 2 : ℝ)) := by
  rintro ⟨hx,hy,hz⟩
  exact three_bands_incompatible _ _ _
    (ladder_separated c _ hc phi_squared_gap i j)
    (ladder_separated c _ hc phi_squared_gap j k) hx hy hz

theorem sharp_common_level_error :
    max |(53 / 2 : ℝ) - 20|
      (max |(53 / 2 : ℝ) - 22|
        (max |(53 / 2 : ℝ) - 24| |(53 / 2 : ℝ) - 33|)) = 13 / 2 := by
  norm_num

noncomputable def mixingWeight (lo hi target : ℝ) : ℝ :=
  (target - lo) / (hi - lo)

theorem mixing_weight_between (lo hi target : ℝ) (hl : lo < target)
    (hh : target < hi) : 0 < mixingWeight lo hi target ∧
      mixingWeight lo hi target < 1 := by
  have hden : 0 < hi - lo := by linarith
  constructor
  · exact div_pos (sub_pos.mpr hl) hden
  · unfold mixingWeight
    exact (div_lt_one hden).mpr (by linarith)

theorem mixing_first_moment (lo hi target : ℝ) (hne : hi - lo ≠ 0) :
    (1 - mixingWeight lo hi target) * lo +
      mixingWeight lo hi target * hi = target := by
  unfold mixingWeight
  field_simp [hne]
  ring

theorem mixing_second_moment_defect (lo hi target : ℝ) (hne : hi - lo ≠ 0) :
    (1 - mixingWeight lo hi target) * lo ^ 2 +
      mixingWeight lo hi target * hi ^ 2 - target ^ 2 =
        (target - lo) * (hi - target) := by
  unfold mixingWeight
  field_simp [hne]
  ring

theorem mixing_defect_positive (lo hi target : ℝ) (hl : lo < target)
    (hh : target < hi) : 0 < (target - lo) * (hi - target) :=
  mul_pos (sub_pos.mpr hl) (sub_pos.mpr hh)

theorem actual_AF_room :
    D0.Algebra.FibonacciAFTower.dimA 3 = 34 ∧
    D0.Algebra.FibonacciAFTower.dimA 4 = 89 ∧
    D0.Algebra.FibonacciAFTower.dimA 5 = 233 ∧
    D0.Algebra.FibonacciAFTower.dimA 4 - D0.Algebra.FibonacciAFTower.dimA 3 = 55 ∧
    D0.Algebra.FibonacciAFTower.dimA 5 - D0.Algebra.FibonacciAFTower.dimA 4 = 144 := by
  decide

end D0.Research.AFSceneHeatComparison

#check D0.Research.AFSceneHeatComparison.phi_squared_gap
#check D0.Research.AFSceneHeatComparison.successive_ladder_gap
#check D0.Research.AFSceneHeatComparison.ladder_separated
#check D0.Research.AFSceneHeatComparison.three_bands_incompatible
#check D0.Research.AFSceneHeatComparison.no_phi_squared_triple_approximation
#check D0.Research.AFSceneHeatComparison.sharp_common_level_error
#check D0.Research.AFSceneHeatComparison.mixing_weight_between
#check D0.Research.AFSceneHeatComparison.mixing_first_moment
#check D0.Research.AFSceneHeatComparison.mixing_second_moment_defect
#check D0.Research.AFSceneHeatComparison.mixing_defect_positive
#check D0.Research.AFSceneHeatComparison.actual_AF_room
#print axioms D0.Research.AFSceneHeatComparison.phi_squared_gap
#print axioms D0.Research.AFSceneHeatComparison.successive_ladder_gap
#print axioms D0.Research.AFSceneHeatComparison.ladder_separated
#print axioms D0.Research.AFSceneHeatComparison.three_bands_incompatible
#print axioms D0.Research.AFSceneHeatComparison.no_phi_squared_triple_approximation
#print axioms D0.Research.AFSceneHeatComparison.sharp_common_level_error
#print axioms D0.Research.AFSceneHeatComparison.mixing_weight_between
#print axioms D0.Research.AFSceneHeatComparison.mixing_first_moment
#print axioms D0.Research.AFSceneHeatComparison.mixing_second_moment_defect
#print axioms D0.Research.AFSceneHeatComparison.mixing_defect_positive
#print axioms D0.Research.AFSceneHeatComparison.actual_AF_room
