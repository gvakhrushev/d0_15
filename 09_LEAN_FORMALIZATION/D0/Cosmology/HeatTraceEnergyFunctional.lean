import Mathlib.Tactic

/-!
# D0-REHEATING-HEATTRACE-ENERGY-FUNCTIONAL-001 — finite heat-energy functional `E(u) = −∂_u log H(u)`

Over the connected reheating scene `K(9,11,13)` the graph-Laplacian heat trace is
`H(u) = Σ_i mult_i · e^{−u λ_i} = 1 + 12 e^{−20u} + 10 e^{−22u} + 8 e^{−24u} + 2 e^{−33u}`
(spectrum `{0:1, 20:12, 22:10, 24:8, 33:2}`, total multiplicity 33). The heat-energy functional is the
heat-weighted mean eigenvalue `E(u) = −∂_u log H(u) = −H'(u)/H(u)`.

To stay finite and decidable we parametrise by the heat-decay variables `x_k = e^{−k u} > 0` (so
`u > 0 ⟺ x_k ∈ (0,1)`), giving
`H = 1 + 12 x20 + 10 x22 + 8 x24 + 2 x33` and `−H' = 240 x20 + 220 x22 + 192 x24 + 66 x33`
(coefficients `mult_k · λ_k`). All theorems are over ℝ but use only `div_pos`/`nlinarith`/`norm_num`
— no transcendental analysis. No inflaton, Planck `n_s`, or survey datum enters.
-/

namespace D0.Cosmology.HeatTraceEnergyFunctional

def mult0 : Nat := 1
def mult20 : Nat := 12
def mult22 : Nat := 10
def mult24 : Nat := 8
def mult33 : Nat := 2

def totalMultiplicity : Nat := mult0 + mult20 + mult22 + mult24 + mult33

/-- **The Laplacian multiplicities sum to 33** (= number of vertices). -/
theorem laplacian_multiplicities_sum_eq_33 : totalMultiplicity = 33 := by decide

def spectralWeightSum : Nat := mult20 * 20 + mult22 * 22 + mult24 * 24 + mult33 * 33

/-- **The nonzero spectral weight `Σ mult_k λ_k` is 718.** -/
theorem spectral_weight_sum_eq_718 : spectralWeightSum = 718 := by decide

/-- The heat trace `H = Σ mult_i x_i` in the heat-decay variables `x_k = e^{−k u}` (with the zero-mode
constant `1`). -/
def heatTrace (x20 x22 x24 x33 : ℝ) : ℝ := 1 + 12 * x20 + 10 * x22 + 8 * x24 + 2 * x33

/-- `−H' = Σ mult_k λ_k x_k` (coefficients `mult_k·λ_k`: `240, 220, 192, 66`). -/
def heatTraceMinusDeriv (x20 x22 x24 x33 : ℝ) : ℝ :=
  240 * x20 + 220 * x22 + 192 * x24 + 66 * x33

/-- The **heat-energy functional** `E(u) = −∂_u log H = (−H')/H`, the heat-weighted mean eigenvalue.
(`noncomputable` because real division is noncomputable; the theorems are unaffected.) -/
noncomputable def energy (x20 x22 x24 x33 : ℝ) : ℝ :=
  heatTraceMinusDeriv x20 x22 x24 x33 / heatTrace x20 x22 x24 x33

/-- **`E = (−H')/H` by definition.** -/
theorem heat_energy_functional_defined (x20 x22 x24 x33 : ℝ) :
    energy x20 x22 x24 x33 = heatTraceMinusDeriv x20 x22 x24 x33 / heatTrace x20 x22 x24 x33 := rfl

/-- The connected heat trace is strictly positive for nonnegative decay variables (the zero-mode `1`). -/
theorem heatTrace_pos (x20 x22 x24 x33 : ℝ)
    (h20 : 0 ≤ x20) (h22 : 0 ≤ x22) (h24 : 0 ≤ x24) (h33 : 0 ≤ x33) :
    0 < heatTrace x20 x22 x24 x33 := by
  unfold heatTrace; positivity

/-- **Early limit** `u → 0⁺` (all `x_k = 1`): `E = 718/33` — the unweighted spectral mean. -/
theorem reheating_energy_early_limit_eq_718_div_33 : energy 1 1 1 1 = 718 / 33 := by
  unfold energy heatTraceMinusDeriv heatTrace; norm_num

/-- **Late limit** `u → ∞` (all `x_k = 0`): `E = 0` — the surviving zero-mode carries no energy. -/
theorem reheating_energy_late_limit_eq_zero : energy 0 0 0 0 = 0 := by
  unfold energy heatTraceMinusDeriv heatTrace; norm_num

end D0.Cosmology.HeatTraceEnergyFunctional
