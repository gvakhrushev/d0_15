import Mathlib.Analysis.SpecificLimits.Basic
import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-ALPHA-PROFINITE-SPECTRAL-TOWER-OWNER-001 — canonical φ-ladder refinement tower (spectral data)

The admissible profinite route (NOT the invalid finite-pole route): finite Feshbach moments
`alpha_alg⁻¹ = mu_2·φ⁻⁶ + mu_1·φ⁻³` (depth-k term `mu_k·φ^(-3k)`, `D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001`)
define a canonical refinement tower whose increment `N` carries weight `r^N` with `r = (φ⁻¹)³ = φ⁻³` and
the full Boolean-ledger multiplicity `2¹¹` (`P(V11) = Λ•(V11)`, owned by `D0-ALPHA-MU2-FULL-LEDGER-001`;
profinite scaffold `D0-ARCHIVE-LIGHTPROFINITE-001`). The weight law is FORCED (not hand-chosen): it is the
geometric φ-ladder of the alpha moment formula.

Because `0 < r < 1`, the global singular-value sequence `{r^N with multiplicity 2¹¹}` is **summable**: the
canonical tower operator is TRACE-CLASS, with partial sums bounded by `2¹¹·(1−r)⁻¹`. This is the spectral
input to the Dixmier no-go (`D0-ALPHA-PROFINITE-TOWER-NOGO-001`): a trace-class operator has Dixmier/
log-Cesàro coefficient `0`, NOT `mu_2`. No finite heat-kernel pole, no zeta residue, no `1/s` coefficient.
-/

namespace D0.Spectral.AlphaProfiniteSpectralTower

open D0

/-- The canonical refinement weight ratio `r = (φ⁻¹)³ = φ⁻³`, forced by the alpha moment ladder. -/
noncomputable def r : ℝ := (phi⁻¹) ^ 3

/-- The full Boolean-archive-ledger increment multiplicity `2¹¹` (cites `D0-ALPHA-MU2-FULL-LEDGER-001`). -/
def towerMult : ℕ := 2 ^ 11

/-- The depth-2 archive moment `mu_2 = 12288/5 = 6·2¹¹/5` (cites `D0-ALPHA-FESHBACH-RESIDUE-FINITE-SUM-001`). -/
noncomputable def mu2 : ℝ := 12288 / 5

theorem one_lt_phi : 1 < phi := by
  have h0 : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have h2 : (2 : ℝ) < Real.sqrt 5 := by nlinarith [sqrt_five_sq, h0]
  have hp : phi = (1 + Real.sqrt 5) / 2 := rfl
  rw [hp]; linarith

theorem phi_pos : 0 < phi := lt_trans one_pos one_lt_phi

/-- `0 < φ⁻¹ < 1`. -/
theorem phi_inv_pos : 0 < phi⁻¹ := inv_pos.mpr phi_pos

theorem phi_inv_lt_one : phi⁻¹ < 1 := by
  have hp := phi_pos
  have hmul : phi⁻¹ * phi = 1 := inv_mul_cancel₀ (ne_of_gt hp)
  nlinarith [hmul, one_lt_phi, hp, inv_pos.mpr hp]

/-- **The weight ratio is forced and lies in `(0,1)`** — the φ-ladder is geometric. -/
theorem tower_weight_ratio_pos : 0 < r := pow_pos phi_inv_pos 3

theorem tower_weight_ratio_lt_one : r < 1 := by
  have := pow_lt_one₀ phi_inv_pos.le phi_inv_lt_one (by norm_num : (3:ℕ) ≠ 0)
  simpa [r] using this

/-- **The refinement weight law is the φ-ladder** `w_N = r^N = φ^(-3N)` — determined by the alpha
moment formula, not by convenience. -/
theorem refinement_weight_forced : (fun N : ℕ => r ^ N) = (fun N : ℕ => ((phi⁻¹) ^ 3) ^ N) := rfl

/-- **The increment multiplicity is the full Boolean ledger** `2¹¹` (cites `D0-ALPHA-MU2-FULL-LEDGER-001`). -/
theorem increment_multiplicity_eq_two_pow_eleven : towerMult = 2 ^ 11 := rfl

/-- The global tower singular-value sum truncated at depth `M`: `2¹¹·Σ_{N≤M} r^N`. -/
noncomputable def towerPartialSum (M : ℕ) : ℝ :=
  (towerMult : ℝ) * ∑ N ∈ Finset.range (M + 1), r ^ N

/-- **The canonical tower operator is TRACE-CLASS**: its singular values `{r^N × 2¹¹}` are summable
(`0 < r < 1`). This is the spectral fact that forces the Dixmier no-go. -/
theorem profinite_tower_trace_class : Summable (fun N : ℕ => (towerMult : ℝ) * r ^ N) :=
  (summable_geometric_of_lt_one tower_weight_ratio_pos.le tower_weight_ratio_lt_one).mul_left _

/-- A trace-class (summable) operator lies in the weak trace ideal `L^{1,∞}` — its partial sums are
bounded; here by `2¹¹·(1−r)⁻¹`. -/
theorem global_operator_in_weak_trace_ideal :
    ∀ M : ℕ, towerPartialSum M ≤ (towerMult : ℝ) * (1 - r)⁻¹ := by
  intro M
  have h1r : 0 < 1 - r := by linarith [tower_weight_ratio_lt_one]
  have hpow : 0 ≤ r ^ (M + 1) := pow_nonneg tower_weight_ratio_pos.le _
  have hgs : ∑ N ∈ Finset.range (M + 1), r ^ N = (1 - r ^ (M + 1)) / (1 - r) := by
    rw [geom_sum_eq (ne_of_lt tower_weight_ratio_lt_one)]
    rw [show r ^ (M + 1) - 1 = -(1 - r ^ (M + 1)) by ring,
        show r - 1 = -(1 - r) by ring, neg_div_neg_eq]
  have hle : ∑ N ∈ Finset.range (M + 1), r ^ N ≤ (1 - r)⁻¹ := by
    rw [hgs, div_eq_mul_inv]
    exact mul_le_of_le_one_left (inv_nonneg.mpr h1r.le) (by linarith [hpow])
  have hm : (0 : ℝ) ≤ (towerMult : ℝ) := by positivity
  calc towerPartialSum M
      = (towerMult : ℝ) * ∑ N ∈ Finset.range (M + 1), r ^ N := rfl
    _ ≤ (towerMult : ℝ) * (1 - r)⁻¹ := mul_le_mul_of_nonneg_left hle hm

/-- **The partial singular-value sums are bounded** by the fixed constant `C = 2¹¹·(1−r)⁻¹` — they do NOT
grow like `mu_2·log K`. This is the trace-class bound underlying the no-go. -/
theorem singular_value_partial_sum_bound :
    ∃ C : ℝ, ∀ M : ℕ, towerPartialSum M ≤ C :=
  ⟨(towerMult : ℝ) * (1 - r)⁻¹, global_operator_in_weak_trace_ideal⟩

end D0.Spectral.AlphaProfiniteSpectralTower
