import Mathlib.Data.Real.Basic
import Mathlib.Tactic

/-!
# D0.Cosmology.FiedlerRelaxationLimit

Theoretical owner: `D0-FIEDLER-RELAXATION-LIMIT-001`.

Formalization of the dynamical origin of the Hodge-Fiedler spectral projection:
The Fiedler projector $\Pi_F$ is not an ad-hoc choice, but the unique slow-mode
attractor of the continuous heat / SDE relaxation flow on $K(9,11,13)$ in the
long-time limit.

The nonzero Laplacian spectrum of $K(9,11,13)$ consists of:
- $\lambda_2 = 20$ (multiplicity 12, Fiedler mode)
- $\lambda_3 = 22$ (multiplicity 10)
- $\lambda_4 = 24$ (multiplicity 8)
- $\lambda_5 = 33$ (multiplicity 2)

Under heat kernel evolution $e^{-u L}$, factoring out the overall decay $e^{-20u}$
leaves relative relaxation weights $e^{-u(\lambda - 20)}$:
- $\lambda = 20 \implies 1$
- $\lambda = 22 \implies e^{-2u}$
- $\lambda = 24 \implies e^{-4u}$
- $\lambda = 33 \implies e^{-13u}$

Setting $t = e^{-u}$ for $t \in (0, 1]$ (where $t \to 0^+$ corresponds to $u \to \infty$):
- Normalized heat partition function on the nonzero spectrum:
  $$Z(t) = 12 + 10 t^2 + 8 t^4 + 2 t^{13}$$
- Fraction of heat weight in the Fiedler subspace:
  $$F(t) = \frac{12}{12 + 10 t^2 + 8 t^4 + 2 t^{13}}$$
- Heat-weighted effective relaxation energy:
  $$\rho(t) = \frac{240 + 220 t^2 + 192 t^4 + 66 t^{13}}{12 + 10 t^2 + 8 t^4 + 2 t^{13}}$$

Quantitative Bounds (for $t \in [0, 1]$):
1. Fiedler share deficit bound:
   $$0 \le 1 - F(t) \le \frac{5}{3} t^2$$
2. Effective energy excess bound:
   $$0 \le \rho(t) - 20 \le \frac{13}{2} t^2$$

Consequently, as $t \to 0^+$ ($u \to \infty$), $F(t) \to 1$ and $\rho(t) \to 20$:
the Fiedler eigenspace is the unique asymptotic survivor of intrinsic SDE relaxation.
-/

namespace D0.Cosmology.FiedlerRelaxationLimit

/-- Nonzero heat trace denominator $Z(t) = 12 + 10 t^2 + 8 t^4 + 2 t^{13}$. -/
def relHeatDenom (t : ℝ) : ℝ :=
  12 + 10 * t ^ 2 + 8 * t ^ 4 + 2 * t ^ 13

/-- Relative Fiedler subspace share $F(t) = \frac{12}{Z(t)}$. -/
noncomputable def fiedlerShare (t : ℝ) : ℝ :=
  12 / relHeatDenom t

/-- Nonzero heat-weighted energy $\rho(t) = \frac{240 + 220 t^2 + 192 t^4 + 66 t^{13}}{Z(t)}$. -/
noncomputable def relHeatEnergy (t : ℝ) : ℝ :=
  (240 + 220 * t ^ 2 + 192 * t ^ 4 + 66 * t ^ 13) / relHeatDenom t

/-- $Z(t) \ge 12$ for all $t \ge 0$. -/
theorem relHeatDenom_ge_twelve {t : ℝ} (ht : 0 ≤ t) : 12 ≤ relHeatDenom t := by
  unfold relHeatDenom
  have h1 : 0 ≤ 10 * t ^ 2 := by positivity
  have h2 : 0 ≤ 8 * t ^ 4 := by positivity
  have h3 : 0 ≤ 2 * t ^ 13 := by positivity
  linarith

/-- $Z(t) > 0$ for all $t \ge 0$. -/
theorem relHeatDenom_pos {t : ℝ} (ht : 0 ≤ t) : 0 < relHeatDenom t := by
  have := relHeatDenom_ge_twelve ht
  linarith

/-- For $t \in [0, 1]$, $t^4 \le t^2$. -/
theorem pow_four_le_pow_two {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : t ^ 4 ≤ t ^ 2 := by
  have ht2 : t ^ 2 ≤ 1 := by
    nlinarith
  calc t ^ 4 = t ^ 2 * t ^ 2 := by ring
  _ ≤ t ^ 2 * 1 := by nlinarith
  _ = t ^ 2 := mul_one _

/-- For $t \in [0, 1]$, $t^{13} \le t^2$. -/
theorem pow_thirteen_le_pow_two {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) : t ^ 13 ≤ t ^ 2 := by
  have ht_le : t ≤ 1 := ht1
  have ht2_pos : 0 ≤ t ^ 2 := by positivity
  have ht11_le_one : t ^ 11 ≤ 1 := by
    have h_pow : ∀ n : ℕ, t ^ n ≤ 1 := by
      intro n
      induction n with
      | zero => simp
      | succ n ih =>
        calc t ^ (n + 1) = t ^ n * t := by ring
        _ ≤ 1 * 1 := by nlinarith
        _ = 1 := by norm_num
    exact h_pow 11
  calc t ^ 13 = t ^ 2 * t ^ 11 := by ring
  _ ≤ t ^ 2 * 1 := mul_le_mul_of_nonneg_left ht11_le_one ht2_pos
  _ = t ^ 2 := mul_one _

/-- For $t \in [0, 1]$, the higher-mode numerator polynomial $10 t^2 + 8 t^4 + 2 t^{13} \le 20 t^2$. -/
theorem higher_mode_sum_le {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    10 * t ^ 2 + 8 * t ^ 4 + 2 * t ^ 13 ≤ 20 * t ^ 2 := by
  have h4 := pow_four_le_pow_two ht0 ht1
  have h13 := pow_thirteen_le_pow_two ht0 ht1
  linarith

/-- **Quantitative Fiedler Share Bound**:
For $0 \le t \le 1$, the Fiedler subspace share deficit is bounded:
$$0 \le 1 - F(t) \le \frac{5}{3} t^2.$$ -/
theorem fiedler_share_error_bound {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    0 ≤ 1 - fiedlerShare t ∧ 1 - fiedlerShare t ≤ (5 / 3 : ℝ) * t ^ 2 := by
  have hZ_pos := relHeatDenom_pos ht0
  have hZ_ge12 := relHeatDenom_ge_twelve ht0
  have h_diff : 1 - fiedlerShare t = (10 * t ^ 2 + 8 * t ^ 4 + 2 * t ^ 13) / relHeatDenom t := by
    unfold fiedlerShare relHeatDenom
    have h_ne : 12 + 10 * t ^ 2 + 8 * t ^ 4 + 2 * t ^ 13 ≠ 0 := ne_of_gt hZ_pos
    field_simp
    ring
  refine ⟨?_, ?_⟩
  · rw [h_diff]
    have h_num_nonneg : 0 ≤ 10 * t ^ 2 + 8 * t ^ 4 + 2 * t ^ 13 := by positivity
    exact div_nonneg h_num_nonneg (le_of_lt hZ_pos)
  · rw [h_diff]
    have h_num_le := higher_mode_sum_le ht0 ht1
    have h_num_nonneg : 0 ≤ 10 * t ^ 2 + 8 * t ^ 4 + 2 * t ^ 13 := by positivity
    -- (A / B) ≤ (5/3) t^2 ↔ A ≤ (5/3) t^2 * B
    rw [div_le_iff₀ hZ_pos]
    have h_mult : 20 * t ^ 2 ≤ (5 / 3 : ℝ) * t ^ 2 * relHeatDenom t := by
      calc 20 * t ^ 2 = (5 / 3 : ℝ) * t ^ 2 * 12 := by ring
      _ ≤ (5 / 3 : ℝ) * t ^ 2 * relHeatDenom t := by
        have ht2_nonneg : 0 ≤ (5 / 3 : ℝ) * t ^ 2 := by positivity
        exact mul_le_mul_of_nonneg_left hZ_ge12 ht2_nonneg
    linarith

/-- For $t \in [0, 1]$, the energy excess numerator $20 t^2 + 32 t^4 + 26 t^{13} \le 78 t^2$. -/
theorem energy_excess_numerator_le {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    20 * t ^ 2 + 32 * t ^ 4 + 26 * t ^ 13 ≤ 78 * t ^ 2 := by
  have h4 := pow_four_le_pow_two ht0 ht1
  have h13 := pow_thirteen_le_pow_two ht0 ht1
  linarith

/-- **Quantitative Effective Energy Bound**:
For $0 \le t \le 1$, the deviation of the heat-weighted energy from the Fiedler scale 20 is bounded:
$$0 \le \rho(t) - 20 \le \frac{13}{2} t^2.$$ -/
theorem fiedler_energy_error_bound {t : ℝ} (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    0 ≤ relHeatEnergy t - 20 ∧ relHeatEnergy t - 20 ≤ (13 / 2 : ℝ) * t ^ 2 := by
  have hZ_pos := relHeatDenom_pos ht0
  have hZ_ge12 := relHeatDenom_ge_twelve ht0
  have h_diff : relHeatEnergy t - 20 = (20 * t ^ 2 + 32 * t ^ 4 + 26 * t ^ 13) / relHeatDenom t := by
    unfold relHeatEnergy relHeatDenom
    have h_ne : 12 + 10 * t ^ 2 + 8 * t ^ 4 + 2 * t ^ 13 ≠ 0 := ne_of_gt hZ_pos
    field_simp
    ring
  refine ⟨?_, ?_⟩
  · rw [h_diff]
    have h_num_nonneg : 0 ≤ 20 * t ^ 2 + 32 * t ^ 4 + 26 * t ^ 13 := by positivity
    exact div_nonneg h_num_nonneg (le_of_lt hZ_pos)
  · rw [h_diff]
    have h_num_le := energy_excess_numerator_le ht0 ht1
    rw [div_le_iff₀ hZ_pos]
    have h_mult : 78 * t ^ 2 ≤ (13 / 2 : ℝ) * t ^ 2 * relHeatDenom t := by
      calc 78 * t ^ 2 = (13 / 2 : ℝ) * t ^ 2 * 12 := by ring
      _ ≤ (13 / 2 : ℝ) * t ^ 2 * relHeatDenom t := by
        have ht2_nonneg : 0 ≤ (13 / 2 : ℝ) * t ^ 2 := by positivity
        exact mul_le_mul_of_nonneg_left hZ_ge12 ht2_nonneg
    linarith

/-- Complete theoretical owner for `D0-FIEDLER-RELAXATION-LIMIT-001`. -/
theorem fiedler_relaxation_limit_owner :
    (∀ t : ℝ, 0 ≤ t → t ≤ 1 → 0 ≤ 1 - fiedlerShare t ∧ 1 - fiedlerShare t ≤ (5 / 3 : ℝ) * t ^ 2) ∧
    (∀ t : ℝ, 0 ≤ t → t ≤ 1 → 0 ≤ relHeatEnergy t - 20 ∧ relHeatEnergy t - 20 ≤ (13 / 2 : ℝ) * t ^ 2) := by
  exact ⟨fun t ht0 ht1 => fiedler_share_error_bound ht0 ht1,
         fun t ht0 ht1 => fiedler_energy_error_bound ht0 ht1⟩

end D0.Cosmology.FiedlerRelaxationLimit
