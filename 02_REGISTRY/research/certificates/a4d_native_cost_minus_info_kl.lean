import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Tactic

/-!
Conditional finite-record lemma: a golden prefix-code cost minus the Shannon
entropy of its actual binary record is the KL divergence to the golden law.
This does not identify the D0-native `Info` term with Shannon entropy.
-/

namespace D0.Research.CostMinusInfoKL

noncomputable section

def expectedCodeLength (r : ℝ) : ℝ := 1 + r

def binaryShannonPhi (p r : ℝ) : ℝ :=
  -((1 - r) * Real.log (1 - r) + r * Real.log r) / Real.log (1 / p)

def binaryGoldenKL (p r : ℝ) : ℝ :=
  ((1 - r) * Real.log ((1 - r) / p) +
    r * Real.log (r / p^2)) / Real.log (1 / p)

/-- For the direct/return code with lengths 1 and 2, the expected code length
minus the actual Bernoulli Shannon information equals KL to the golden
reference `(p,p^2)`, whenever `p+p^2=1`. -/
theorem code_minus_info_eq_golden_kl
    (p r : ℝ) (hp : 0 < p) (hp1 : p < 1) (hr : 0 < r) (hr1 : r < 1) :
    expectedCodeLength r - binaryShannonPhi p r = binaryGoldenKL p r := by
  have hphi : 1 < 1 / p := by
    apply (lt_div_iff₀ hp).2
    nlinarith
  have hlogphi : 0 < Real.log (1 / p) := Real.log_pos hphi
  have hlogp : Real.log (1 / p) = -Real.log p := by
    rw [Real.log_div (by norm_num : (1 : ℝ) ≠ 0) (ne_of_gt hp), Real.log_one]
    ring
  have hlogp_ne : Real.log p ≠ 0 := by
    intro h
    rw [h] at hlogp
    have hz : Real.log (1 / p) = 0 := by simpa using hlogp
    exact (ne_of_gt hlogphi) hz
  have hlog_noerror : Real.log ((1 - r) / p) =
      Real.log (1 - r) - Real.log p := by
    rw [Real.log_div (by linarith : 1 - r ≠ 0) (ne_of_gt hp)]
  have hlog_error : Real.log (r / p^2) =
      Real.log r - 2 * Real.log p := by
    rw [Real.log_div (ne_of_gt hr) (pow_ne_zero 2 (ne_of_gt hp)), Real.log_pow]
    norm_num
  unfold expectedCodeLength binaryShannonPhi binaryGoldenKL
  rw [hlog_noerror, hlog_error, hlogp]
  field_simp [hlogp_ne]
  ring

/-- The same identity summed over three independent QND ticks. -/
theorem three_round_code_minus_info_eq_golden_kl
    (p r : ℝ) (hp : 0 < p) (hp1 : p < 1) (hgolden : p + p^2 = 1)
    (hr : 0 < r) (hr1 : r < 1) :
    p + p^2 = 1 ∧
      3 * (expectedCodeLength r - binaryShannonPhi p r) =
        3 * binaryGoldenKL p r := by
  refine ⟨hgolden, ?_⟩
  rw [code_minus_info_eq_golden_kl p r hp hp1 hr hr1]

#check code_minus_info_eq_golden_kl
#check three_round_code_minus_info_eq_golden_kl
#print axioms code_minus_info_eq_golden_kl
#print axioms three_round_code_minus_info_eq_golden_kl

end
end D0.Research.CostMinusInfoKL
