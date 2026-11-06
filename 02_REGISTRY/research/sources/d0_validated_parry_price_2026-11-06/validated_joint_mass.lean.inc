open D0.Analysis.RetainedRecordSurprisal

#print axioms moment_eq_tariff_sum
#print axioms hasFDerivAt_moment
#print axioms hasFDerivAt_moment_fixed

namespace D0.Research.NativeCodePriceResolution

theorem validated_joint_mass (mass : Fin 3 → ℝ) (hp : ∀ i, 0 < mass i) :
    moment Finset.univ (Real.log D0.phi) mass ![2,3,3] = 1 - (D0.phi⁻¹)^4 := by
  have hφ : 1 < D0.phi := by
    unfold D0.phi
    nlinarith [Real.sq_sqrt (show (0:ℝ) ≤ 5 by norm_num), Real.sqrt_nonneg 5]
  have powers (n : ℕ) : Real.exp (-Real.log D0.phi * n) = (D0.phi⁻¹)^n := by
    rw [mul_comm, Real.exp_nat_mul, Real.exp_neg, Real.exp_log (lt_trans zero_lt_one hφ)]
  rw [moment_eq_tariff_sum _ (Real.log_pos hφ).ne' _ _ fun i _ => hp i, Fin.sum_univ_three]
  change Real.exp (-Real.log D0.phi * 2) + Real.exp (-Real.log D0.phi * 3) +
    Real.exp (-Real.log D0.phi * 3) = 1 - (D0.phi⁻¹)^4
  rw [show Real.exp (-Real.log D0.phi * 2) = (D0.phi⁻¹)^2 from powers 2,
      show Real.exp (-Real.log D0.phi * 3) = (D0.phi⁻¹)^3 from powers 3,
      ← golden_two_tick_event_mass]
  ring

#print axioms validated_joint_mass
end D0.Research.NativeCodePriceResolution
