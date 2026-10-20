import D0.Core.Phi
import Mathlib.Algebra.Order.Round
import Mathlib.Tactic

/-! Exact finite lemmas for literal integer code prices. The all-probe
normalization theorem has a separate analytic proof. No action is selected. -/
namespace D0.Research.NativeCodePriceResolution
noncomputable section

theorem code_half_contrast_lattice (a nu : ℝ) (np nm : ℕ) :
    (nu * (np : ℝ) - nu * (nm : ℝ)) / (2 * a) =
      (nu / (2 * a)) * (((np : ℤ) - (nm : ℤ) : ℤ) : ℝ) := by
  push_cast
  ring

theorem nonzero_integer_abs_at_least_one (k : ℤ) (hk : k ≠ 0) :
    (1 : ℝ) ≤ |(k : ℝ)| := by
  exact_mod_cast Int.one_le_abs hk

theorem fixed_lattice_nearest_zero (s b : ℝ) (k : ℤ)
    (hgap : 2 * |b| ≤ |s|) :
    |b| ≤ |s * (k : ℝ) - b| := by
  by_cases hk : k = 0
  · simp [hk]
  · have habs := nonzero_integer_abs_at_least_one k hk
    have hmul : |s| ≤ |s * (k : ℝ)| := by
      rw [abs_mul]
      nlinarith [abs_nonneg s]
    have htriangle : |s * (k : ℝ)| ≤ |s * (k : ℝ) - b| + |b| := by
      simpa only [sub_add_cancel] using abs_add_le (s * (k : ℝ) - b) b
    linarith

theorem recording_error_keeps_gap (s b r e : ℝ) (k : ℤ)
    (hgap : 2 * |b| ≤ |s|) (hrecord : |r - s * (k : ℝ)| ≤ e) :
    |b| - e ≤ |r - b| := by
  have hlow := fixed_lattice_nearest_zero s b k hgap
  have htriangle : |s * (k : ℝ) - b| ≤
      |s * (k : ℝ) - r| + |r - b| := by
    simpa only [sub_add_sub_cancel] using
      abs_add_le (s * (k : ℝ) - r) (r - b)
  rw [abs_sub_comm (s * (k : ℝ)) r] at htriangle
  linarith

theorem integer_endpoint_recording_gap (a nu b r e : ℝ) (np nm : ℕ)
    (hgap : 2 * |b| ≤ |nu / (2 * a)|)
    (hrecord : |r - (nu * (np : ℝ) - nu * (nm : ℝ)) / (2 * a)| ≤ e) :
    |b| - e ≤ |r - b| := by
  rw [code_half_contrast_lattice] at hrecord
  exact recording_error_keeps_gap (nu / (2 * a)) b r e
    ((np : ℤ) - (nm : ℤ)) hgap hrecord

theorem lattice_rounding_sufficient (s b : ℝ) (hs : 0 < s) :
    ∃ k : ℤ, |s * (k : ℝ) - b| ≤ s / 2 := by
  refine ⟨round (b / s), ?_⟩
  have hr := abs_sub_round (b / s)
  have hm := mul_le_mul_of_nonneg_left hr hs.le
  have heq : s * |b / s - (round (b / s) : ℝ)| =
      |s * (round (b / s) : ℝ) - b| := by
    calc
      s * |b / s - (round (b / s) : ℝ)| =
          |s * (b / s - (round (b / s) : ℝ))| := by
            rw [abs_mul, abs_of_pos hs]
      _ = |b - s * (round (b / s) : ℝ)| := by
            congr 1
            field_simp
      _ = |s * (round (b / s) : ℝ) - b| := abs_sub_comm _ _
  rw [heq] at hm
  linarith

theorem action_lower_bound_not_difference_quantization (e : ℝ)
    (he0 : 0 < e) (he1 : e < 1) :
    (1 : ℝ) ≤ 1 + e ∧ (1 : ℝ) ≤ 1 ∧
      (1 + e) - 1 = e ∧ 0 < |(1 + e) - 1| ∧ |(1 + e) - 1| < 1 := by
  rw [show (1 + e) - 1 = e by ring, abs_of_pos he0]
  constructor
  · linarith
  · exact ⟨le_rfl, rfl, he0, he1⟩

theorem owned_golden_binary_partition (n : ℕ) :
    (D0.phi⁻¹ + (D0.phi⁻¹)^2)^n = (1 : ℝ) := by
  rw [D0.phi_inv_satisfies_primitive, one_pow]

theorem golden_two_tick_event_mass :
    (D0.phi⁻¹)^2 + 2 * (D0.phi⁻¹)^3 = 1 - (D0.phi⁻¹)^4 := by
  have h := congrArg (fun x : ℝ => x^2) D0.phi_inv_satisfies_primitive
  nlinarith

#check code_half_contrast_lattice
#print axioms code_half_contrast_lattice
#check nonzero_integer_abs_at_least_one
#print axioms nonzero_integer_abs_at_least_one
#check fixed_lattice_nearest_zero
#print axioms fixed_lattice_nearest_zero
#check recording_error_keeps_gap
#print axioms recording_error_keeps_gap
#check integer_endpoint_recording_gap
#print axioms integer_endpoint_recording_gap
#check lattice_rounding_sufficient
#print axioms lattice_rounding_sufficient
#check action_lower_bound_not_difference_quantization
#print axioms action_lower_bound_not_difference_quantization
#check owned_golden_binary_partition
#print axioms owned_golden_binary_partition
#check golden_two_tick_event_mass
#print axioms golden_two_tick_event_mass
#check D0.phi_inv_satisfies_primitive
#print axioms D0.phi_inv_satisfies_primitive

end
end D0.Research.NativeCodePriceResolution
