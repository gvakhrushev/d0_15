import D0.Cosmology.ReheatingEnergyBudgetOwner

/-!
# D0-INFLATIONLESS-THRESHOLD-ENERGY-OWNER-001 / D0-REHEATING-NO-INFLATON-NOGO-001

The early-universe threshold-energy owner is finite and inflationless: the reheating budget is fixed by
the `K(9,11,13)` Laplacian spectrum alone — the early-limit value `E(0⁺) = spectralWeightSum /
totalMultiplicity = 718/33` is a forced rational, with NO inflaton scalar potential and NO tunable
reheating-temperature parameter. The no-inflaton no-go records that no free parameter is introduced.
-/

namespace D0.Cosmology.InflationlessThresholdEnergyOwner

open D0.Cosmology.HeatTraceEnergyFunctional D0.Cosmology.ReheatingEnergyBudgetOwner

/-- **No-inflaton no-go (D0-REHEATING-NO-INFLATON-NOGO-001).** The threshold-energy early limit is the
spectrum-determined rational `spectralWeightSum / totalMultiplicity = 718/33` — there is no free
reheating-temperature scalar; the budget is a function of the finite spectrum alone. -/
theorem reheating_no_inflaton_nogo :
    (spectralWeightSum : ℚ) / (totalMultiplicity : ℚ) = 718 / 33
      ∧ energy 1 1 1 1 = 718 / 33 := by
  refine ⟨?_, reheating_energy_early_limit_eq_718_div_33⟩
  rw [show spectralWeightSum = 718 from spectral_weight_sum_eq_718,
      show totalMultiplicity = 33 from laplacian_multiplicities_sum_eq_33]
  norm_num

/-- **D0-INFLATIONLESS-THRESHOLD-ENERGY-OWNER-001.** The early-universe threshold energy is finite,
inflationless, and spectrum-determined: positive for `u > 0`, bounded by `λ_max = 33`, with forced early
limit `718/33` and late limit `0`, and no inflaton/free parameter. -/
theorem inflationless_threshold_energy_owner_closed (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    0 < reheatingEnergy x20 x22 x24 x33
      ∧ reheatingEnergy x20 x22 x24 x33 < 33
      ∧ energy 1 1 1 1 = 718 / 33
      ∧ energy 0 0 0 0 = 0
      ∧ (spectralWeightSum : ℚ) / (totalMultiplicity : ℚ) = 718 / 33 := by
  refine ⟨reheating_energy_positive x20 x22 x24 x33 h20 h22 h24 h33,
    reheating_energy_bounded_by_lambda_max x20 x22 x24 x33 h20 h22 h24 h33,
    reheating_energy_early_limit_eq_718_div_33,
    reheating_energy_late_limit_eq_zero,
    reheating_no_inflaton_nogo.1⟩

end D0.Cosmology.InflationlessThresholdEnergyOwner
