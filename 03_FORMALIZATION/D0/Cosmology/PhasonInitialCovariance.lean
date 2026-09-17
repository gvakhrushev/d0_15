import Mathlib.Tactic

/-!
# D0-REHEATING-PHASON-INITIAL-DATA-OWNER-001 / D0-PHASON-INITIAL-COVARIANCE-OWNER-001

The post-threshold phason initial state is the normalized heat-kernel covariance on the NONZERO
connected modes (the zero mode is projected out by `Π_phason`). Its energy
`ρ_φ(u) = Σ_{nz} mult_k λ_k e^{−u λ_k} / Σ_{nz} mult_k e^{−u λ_k}` is the heat-weighted mean of the
nonzero eigenvalues `{20,22,24,33}`, hence `20 ≤ ρ_φ ≤ 33` and `ρ_φ > 0` for every `u > 0`. The state
is sourced by the reheating heat trace and carries no independent inflaton amplitude.

HONEST SCOPE. The covariance and its positivity/bounds are CERT-CLOSED for **every** heat window
`u > 0`; a uniquely-FORCED threshold window `u_*` is NOT supplied by the reheating owner (its energy
`E(u)` is a curve, not a point), so the forced-`u_*` selection stays the named PROOF-TARGET. Parametrise
by the heat-decay variables `x_k = e^{−u λ_k} > 0`; no transcendental analysis.
-/

namespace D0.Cosmology.PhasonInitialCovariance

/-- Normalization trace `Σ_{nz} mult_k x_k` (the zero mode is excluded — `Π_phason`). -/
def covTrace (x20 x22 x24 x33 : ℝ) : ℝ := 12 * x20 + 10 * x22 + 8 * x24 + 2 * x33

/-- Phason energy numerator `Σ_{nz} mult_k λ_k x_k` (coefficients `mult_k·λ_k`: 240,220,192,66). -/
def covEnergyNum (x20 x22 x24 x33 : ℝ) : ℝ := 240 * x20 + 220 * x22 + 192 * x24 + 66 * x33

/-- Phason initial energy `ρ_φ = (Σ mult λ x)/(Σ mult x)` — the heat-weighted mean nonzero eigenvalue. -/
noncomputable def rhoPhi (x20 x22 x24 x33 : ℝ) : ℝ :=
  covEnergyNum x20 x22 x24 x33 / covTrace x20 x22 x24 x33

theorem covTrace_pos (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    0 < covTrace x20 x22 x24 x33 := by unfold covTrace; positivity

/-- **The phason covariance is normalized**: the nonzero-mode weights sum to one (`trace/trace = 1`). -/
theorem phason_initial_covariance_normalized (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    covTrace x20 x22 x24 x33 / covTrace x20 x22 x24 x33 = 1 :=
  div_self (covTrace_pos x20 x22 x24 x33 h20 h22 h24 h33).ne'

/-- **`ρ_φ > 0`** for every `u > 0` (positive numerator and denominator). -/
theorem phason_initial_energy_positive (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    0 < rhoPhi x20 x22 x24 x33 := by
  apply div_pos
  · unfold covEnergyNum; positivity
  · exact covTrace_pos x20 x22 x24 x33 h20 h22 h24 h33

/-- **Lower edge `ρ_φ ≥ 20 = λ₂`** (Fiedler value): the weighted mean of `{20,22,24,33}` is ≥ the min. -/
theorem rhoPhi_ge_fiedler (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    20 ≤ rhoPhi x20 x22 x24 x33 := by
  rw [rhoPhi, le_div_iff₀ (covTrace_pos x20 x22 x24 x33 h20 h22 h24 h33)]
  unfold covEnergyNum covTrace; nlinarith [h22, h24, h33]

/-- **Upper edge `ρ_φ ≤ 33 = λ_max`**: the weighted mean of `{20,22,24,33}` is ≤ the max. -/
theorem rhoPhi_le_lambda_max (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    rhoPhi x20 x22 x24 x33 ≤ 33 := by
  rw [rhoPhi, div_le_iff₀ (covTrace_pos x20 x22 x24 x33 h20 h22 h24 h33)]
  unfold covEnergyNum covTrace; nlinarith [h20, h22, h24]

/-- **D0-PHASON-INITIAL-COVARIANCE-OWNER-001 / D0-REHEATING-PHASON-INITIAL-DATA-OWNER-001.** For every
`u > 0` the post-threshold phason initial state is a normalized covariance on the nonzero connected
modes with energy `ρ_φ ∈ [λ₂, λ_max] = [20, 33]`, strictly positive — sourced by the reheating heat
trace, with no independent inflaton amplitude (the bounds hold for ALL `x_k > 0`, so no tunable
amplitude can move `ρ_φ` out of the spectral band). -/
theorem phason_initial_data_owner (x20 x22 x24 x33 : ℝ)
    (h20 : 0 < x20) (h22 : 0 < x22) (h24 : 0 < x24) (h33 : 0 < x33) :
    0 < rhoPhi x20 x22 x24 x33
      ∧ 20 ≤ rhoPhi x20 x22 x24 x33
      ∧ rhoPhi x20 x22 x24 x33 ≤ 33
      ∧ covTrace x20 x22 x24 x33 / covTrace x20 x22 x24 x33 = 1 := by
  exact ⟨phason_initial_energy_positive x20 x22 x24 x33 h20 h22 h24 h33,
    rhoPhi_ge_fiedler x20 x22 x24 x33 h20 h22 h24 h33,
    rhoPhi_le_lambda_max x20 x22 x24 x33 h20 h22 h24 h33,
    phason_initial_covariance_normalized x20 x22 x24 x33 h20 h22 h24 h33⟩

end D0.Cosmology.PhasonInitialCovariance
