import D0.Cosmology.HeatTraceEnergyFunctional

/-!
# D0-REHEATING-ENERGY-BUDGET-OWNER-001 — positive finite reheating budget from the heat-trace jump

The reheating budget is `E_reheat = E_connected − E_pre`. The pre-threshold disconnected stage has heat
trace `H_pre = 33` (all 33 vertices isolated, Laplacian `0`), so its heat-energy functional is `E_pre = 0`.
Hence `E_reheat = E_connected`, and for `u > 0` (decay variables `x_k > 0`) it is strictly positive and
bounded above by the maximal scene eigenvalue `λ_max = 33`. This is the finite heat-energy release at
connectivity onset — not an inflaton potential, not a fitted CMB scalar.
-/

namespace D0.Cosmology.ReheatingEnergyBudgetOwner

open D0.Cosmology.HeatTraceEnergyFunctional

/-- Pre-threshold disconnected heat trace: all 33 vertices isolated, Laplacian `0`, so `H_pre = 33`. -/
def preThresholdHeatTrace : ℝ := 33

/-- **Pre-threshold heat trace = 33** (the edgeless 33-vertex baseline). -/
theorem prethreshold_heat_trace_eq_33 : preThresholdHeatTrace = 33 := rfl

/-- Pre-threshold heat-energy functional: a constant heat trace has `−∂_u log H = 0`. -/
def preThresholdEnergy : ℝ := 0

/-- **The reheating budget** `E_reheat = E_connected − E_pre`. (`noncomputable`: depends on `energy`.) -/
noncomputable def reheatingEnergy (x20 x22 x24 x33 : ℝ) : ℝ :=
  energy x20 x22 x24 x33 - preThresholdEnergy

/-- **`E_reheat = E_connected`** (the pre-threshold baseline contributes `0`). -/
theorem reheating_energy_eq_connected_heat_energy (x20 x22 x24 x33 : ℝ) :
    reheatingEnergy x20 x22 x24 x33 = energy x20 x22 x24 x33 := by
  unfold reheatingEnergy preThresholdEnergy; ring

/-- **Positivity**: for `u > 0` (all `x_k > 0`) the reheating budget is strictly positive. -/
theorem reheating_energy_positive (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    0 < reheatingEnergy x20 x22 x24 x33 := by
  rw [reheating_energy_eq_connected_heat_energy, energy]
  apply div_pos
  · unfold heatTraceMinusDeriv; positivity
  · exact heatTrace_pos x20 x22 x24 x33 h20.le h22.le h24.le h33.le

/-- **Upper bound by the maximal eigenvalue**: `E_reheat < 33 = λ_max`. The energy is a heat-weighted
mean of `{0,20,22,24,33}`; the zero-mode and sub-maximal modes keep it strictly below `λ_max`. -/
theorem reheating_energy_bounded_by_lambda_max (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    reheatingEnergy x20 x22 x24 x33 < 33 := by
  rw [reheating_energy_eq_connected_heat_energy, energy]
  rw [div_lt_iff₀ (heatTrace_pos x20 x22 x24 x33 h20.le h22.le h24.le h33.le)]
  unfold heatTraceMinusDeriv heatTrace
  -- 33*H − (−H') = 33 + 156 x20 + 110 x22 + 72 x24 + 0·x33 > 0
  nlinarith [h20, h22, h24, h33]

/-- **D0-REHEATING-ENERGY-BUDGET-OWNER-001.** For `u > 0`: the reheating budget equals the connected
heat-energy functional, is strictly positive, and is bounded above by `λ_max = 33`; with early limit
`718/33` and late limit `0` (Functional module). The pre-threshold baseline is `0`. -/
theorem reheating_energy_budget_owner_closed (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    reheatingEnergy x20 x22 x24 x33 = energy x20 x22 x24 x33
      ∧ 0 < reheatingEnergy x20 x22 x24 x33
      ∧ reheatingEnergy x20 x22 x24 x33 < 33
      ∧ preThresholdEnergy = 0 := by
  refine ⟨reheating_energy_eq_connected_heat_energy x20 x22 x24 x33,
    reheating_energy_positive x20 x22 x24 x33 h20 h22 h24 h33,
    reheating_energy_bounded_by_lambda_max x20 x22 x24 x33 h20 h22 h24 h33, rfl⟩

end D0.Cosmology.ReheatingEnergyBudgetOwner
