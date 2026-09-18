import D0.Spectral.AlphaProfiniteTowerNoGo
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# The Perron-φ³ carrier lands on the Dixmier critical line

`D0-ALPHA-PROFINITE-TOWER-NOGO-001` proves that every present-core profinite tower (block growth
`a ≤ 2`, weight decay `φ⁻³ᴺ`) is trace-class, hence its log-Cesàro limit is `0 ≠ μ₂`. Its
"EXACT MISSING ARTIFACT" is *a canonical refinement carrier with Perron eigenvalue φ³ whose
multiplicity growth `~φ^{3N}` exactly cancels the `φ^{-3N}` weight decay onto the critical line*.

This module supplies the analytic half of that artifact. For the **Perron-φ³ carrier** —
level `N` carries `α^N` singular values of size `c·α^{-N}` with `α = φ³` (the cube of the
golden Bratteli rate, i.e. the three-step Fibonacci AF refinement) — we prove:

* the level sums are constant (`c` per level), so the tower is **not** trace-class;
* the singular-value count `M_K = Σ_{N≤K} α^N` satisfies `α^K ≤ 1 + M_K ≤ C₀·α^{K+1}`;
* hence `log(1 + M_K)/(K+1) → log α = 3·log φ`;
* hence the **log-Cesàro ratio converges to `c / (3·log φ) ≠ 0`** — the carrier sits exactly in
  `L^{1,∞} ∖ L¹` with a nonzero Dixmier coefficient;
* choosing the level constant `c₂ := 3·μ₂·log φ` gives log-Cesàro limit exactly `μ₂ = 12288/5`.

HONESTY BOUNDARY. What is proved: the φ³-carrier has a nonzero, computable log-Cesàro limit and
can be normalised to `μ₂`. What is NOT proved: that the D0 scene *forces* the φ³ carrier (i.e.
that the three-step AF refinement is the canonical archive tower) and that the level constant is
internally `3·μ₂·log φ`. Those remain `PRIM-PERRON-PHI3-CARRIER` (closure_frontier lane E).
This module converts the no-go's missing artifact from "unknown analytic object" into "a
specific, explicitly verified carrier awaiting a canonicity proof".
-/

namespace D0.Spectral.PerronPhi3Carrier

open D0 D0.Spectral.AlphaProfiniteSpectralTower D0.Spectral.AlphaProfiniteTowerNoGo
open Filter Topology Finset

/-- The Perron growth ratio `α = φ³`. -/
noncomputable def alpha : ℝ := phi ^ 3

theorem alpha_gt_one : 1 < alpha := by
  unfold alpha; exact one_lt_pow₀ one_lt_phi (by norm_num)

theorem alpha_pos : 0 < alpha := lt_trans one_pos alpha_gt_one

theorem log_alpha_pos : 0 < Real.log alpha := Real.log_pos alpha_gt_one

theorem log_alpha_eq : Real.log alpha = 3 * Real.log phi := by
  unfold alpha; rw [Real.log_pow]; norm_num

/-- Number of singular values through level `K`: `M_K = Σ_{N≤K} α^N`. -/
noncomputable def count (K : ℕ) : ℝ := ∑ N ∈ range (K + 1), alpha ^ N

/-- Level-`K` partial singular-value sum for level constant `c`: each of the `α^N` values at level
`N` has size `c·α^{-N}`, so each level contributes exactly `c`. -/
noncomputable def partialSum (c : ℝ) (K : ℕ) : ℝ := c * ((K : ℝ) + 1)

/-- The level sum identity: `α^N · (c·α^{-N}) = c`. -/
theorem level_sum (c : ℝ) (N : ℕ) : alpha ^ N * (c * (alpha ^ N)⁻¹) = c := by
  have h : alpha ^ N ≠ 0 := pow_ne_zero _ (ne_of_gt alpha_pos)
  field_simp

/-- **Not trace-class:** the partial sums are unbounded for `c > 0`. -/
theorem partialSum_unbounded {c : ℝ} (hc : 0 < c) :
    Tendsto (partialSum c) atTop atTop := by
  unfold partialSum
  apply Tendsto.const_mul_atTop hc
  exact tendsto_atTop_add_const_right atTop 1 tendsto_natCast_atTop_atTop

theorem count_nonneg (K : ℕ) : 0 ≤ count K :=
  sum_nonneg fun _ _ => pow_nonneg alpha_pos.le _

/-- Lower bound: the top term alone gives `α^K ≤ M_K`. -/
theorem count_ge (K : ℕ) : alpha ^ K ≤ count K := by
  unfold count
  exact single_le_sum (fun i _ => pow_nonneg alpha_pos.le i) (mem_range.mpr (Nat.lt_succ_self K))

/-- Geometric closed form `M_K = (α^{K+1} − 1)/(α − 1)`. -/
theorem count_eq (K : ℕ) : count K = (alpha ^ (K + 1) - 1) / (alpha - 1) := by
  unfold count
  exact geom_sum_eq (ne_of_gt alpha_gt_one) (K + 1)

/-- Upper bound: `M_K ≤ α^{K+1}/(α − 1)`. -/
theorem count_le (K : ℕ) : count K ≤ alpha ^ (K + 1) / (alpha - 1) := by
  rw [count_eq]
  have h : 0 < alpha - 1 := by linarith [alpha_gt_one]
  apply div_le_div_of_nonneg_right _ h.le
  linarith

/-- The upper-bound constant `C₀ = 1/(α−1) + 1 ≥ 1`. -/
noncomputable def C0 : ℝ := 1 / (alpha - 1) + 1

theorem C0_ge_one : 1 ≤ C0 := by
  unfold C0
  have h : 0 < alpha - 1 := by linarith [alpha_gt_one]
  have : 0 ≤ 1 / (alpha - 1) := by positivity
  linarith

theorem C0_pos : 0 < C0 := lt_of_lt_of_le one_pos C0_ge_one

/-- `α^K ≤ 1 + M_K`. -/
theorem one_add_count_ge (K : ℕ) : alpha ^ K ≤ 1 + count K := by
  linarith [count_ge K]

/-- `1 + M_K ≤ C₀·α^{K+1}`. -/
theorem one_add_count_le (K : ℕ) : 1 + count K ≤ C0 * alpha ^ (K + 1) := by
  have hpow : 1 ≤ alpha ^ (K + 1) := one_le_pow₀ alpha_gt_one.le
  have hc := count_le K
  unfold C0
  have h : 0 < alpha - 1 := by linarith [alpha_gt_one]
  have : alpha ^ (K + 1) / (alpha - 1) = 1 / (alpha - 1) * alpha ^ (K + 1) := by ring
  nlinarith [this, hc, hpow]

theorem one_add_count_pos (K : ℕ) : 0 < 1 + count K := by linarith [count_nonneg K]

/-- Log lower bound: `K·log α ≤ log(1 + M_K)`. -/
theorem log_lower (K : ℕ) : (K : ℝ) * Real.log alpha ≤ Real.log (1 + count K) := by
  have := Real.log_le_log (pow_pos alpha_pos K) (one_add_count_ge K)
  rwa [Real.log_pow] at this

/-- Log upper bound: `log(1 + M_K) ≤ (K+1)·log α + log C₀`. -/
theorem log_upper (K : ℕ) :
    Real.log (1 + count K) ≤ ((K : ℝ) + 1) * Real.log alpha + Real.log C0 := by
  have h := Real.log_le_log (one_add_count_pos K) (one_add_count_le K)
  rw [Real.log_mul (ne_of_gt C0_pos) (pow_ne_zero _ (ne_of_gt alpha_pos)), Real.log_pow] at h
  push_cast at h
  linarith

/-- The normalised log-count `log(1 + M_K)/(K+1)`. -/
noncomputable def normLog (K : ℕ) : ℝ := Real.log (1 + count K) / ((K : ℝ) + 1)

theorem normLog_pos (K : ℕ) : 0 < normLog K := by
  unfold normLog
  apply div_pos _ (by positivity)
  have := log_lower K
  rcases Nat.eq_zero_or_pos K with h | h
  · subst h
    have : count 0 = 1 := by simp [count]
    rw [this]; exact Real.log_pos (by norm_num)
  · have hK : (0 : ℝ) < K := Nat.cast_pos.mpr h
    exact lt_of_lt_of_le (mul_pos hK log_alpha_pos) this

/-- `K/(K+1) → 1`. -/
private lemma tendsto_ratio : Tendsto (fun K : ℕ => (K : ℝ) / ((K : ℝ) + 1)) atTop (𝓝 1) := by
  have h : (fun K : ℕ => (K : ℝ) / ((K : ℝ) + 1)) = fun K : ℕ => 1 - 1 / ((K : ℝ) + 1) := by
    funext K; field_simp; ring
  rw [h]
  have := tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ)
  simpa using (tendsto_const_nhds (x := (1 : ℝ))).sub this

/-- **`log(1 + M_K)/(K+1) → log α`** (squeeze between the two log bounds). -/
theorem normLog_tendsto : Tendsto normLog atTop (𝓝 (Real.log alpha)) := by
  have hlow : Tendsto (fun K : ℕ => (K : ℝ) / ((K : ℝ) + 1) * Real.log alpha) atTop
      (𝓝 (Real.log alpha)) := by
    simpa using tendsto_ratio.mul_const (Real.log alpha)
  have hup : Tendsto (fun K : ℕ => Real.log alpha + Real.log C0 * (1 / ((K : ℝ) + 1))) atTop
      (𝓝 (Real.log alpha)) := by
    have := (tendsto_one_div_add_atTop_nhds_zero_nat (𝕜 := ℝ)).const_mul (Real.log C0)
    simpa using (tendsto_const_nhds (x := Real.log alpha)).add this
  refine tendsto_of_tendsto_of_tendsto_of_le_of_le hlow hup ?_ ?_
  · intro K
    show (K : ℝ) / ((K : ℝ) + 1) * Real.log alpha ≤ normLog K
    unfold normLog
    have hK : (0 : ℝ) < (K : ℝ) + 1 := by positivity
    rw [div_mul_eq_mul_div, div_le_div_iff_of_pos_right hK]
    exact log_lower K
  · intro K
    show normLog K ≤ Real.log alpha + Real.log C0 * (1 / ((K : ℝ) + 1))
    unfold normLog
    have hK : (0 : ℝ) < (K : ℝ) + 1 := by positivity
    rw [div_le_iff₀ hK]
    have := log_upper K
    have e : (Real.log alpha + Real.log C0 * (1 / ((K : ℝ) + 1))) * ((K : ℝ) + 1)
        = ((K : ℝ) + 1) * Real.log alpha + Real.log C0 := by field_simp
    linarith

/-- The log-Cesàro ratio of the φ³ carrier at level `K`. -/
noncomputable def logCesaroPhi3 (c : ℝ) (K : ℕ) : ℝ := partialSum c K / Real.log (1 + count K)

theorem logCesaroPhi3_eq (c : ℝ) (K : ℕ) : logCesaroPhi3 c K = c / normLog K := by
  unfold logCesaroPhi3 partialSum normLog
  have hK : ((K : ℝ) + 1) ≠ 0 := by positivity
  field_simp

/-- **CRITICAL LINE.** The φ³ carrier's log-Cesàro ratio converges to `c / log α = c/(3 log φ)`. -/
theorem logCesaroPhi3_tendsto (c : ℝ) :
    Tendsto (logCesaroPhi3 c) atTop (𝓝 (c / Real.log alpha)) := by
  have h : logCesaroPhi3 c = fun K => c / normLog K := funext (logCesaroPhi3_eq c)
  rw [h]
  exact tendsto_const_nhds.div normLog_tendsto (ne_of_gt log_alpha_pos)

/-- **Nonzero Dixmier coefficient** for any `c ≠ 0`: the carrier is in `L^{1,∞} ∖ L¹`. -/
theorem dixmier_coefficient_ne_zero {c : ℝ} (hc : c ≠ 0) : c / Real.log alpha ≠ 0 :=
  div_ne_zero hc (ne_of_gt log_alpha_pos)

/-- The level constant that normalises the carrier onto `μ₂`: `c₂ = 3·μ₂·log φ = μ₂·log α`. -/
noncomputable def c2 : ℝ := mu2 * Real.log alpha

/-- **μ₂-normalised carrier:** with `c = c₂` the log-Cesàro limit is exactly `μ₂ = 12288/5`. -/
theorem logCesaroPhi3_c2_tendsto_mu2 : Tendsto (logCesaroPhi3 c2) atTop (𝓝 mu2) := by
  have h := logCesaroPhi3_tendsto c2
  have e : c2 / Real.log alpha = mu2 := by
    unfold c2; exact mul_div_cancel_right₀ mu2 (ne_of_gt log_alpha_pos)
  rwa [e] at h

/-- **Contrast with the present-core no-go.** The forced present-core tower has log-Cesàro limit
`0`, the φ³ carrier has limit `μ₂`: the two towers are analytically distinct, and only the
φ³ growth reaches the critical line. -/
theorem carrier_vs_present_core :
    Tendsto logCesaro atTop (𝓝 0) ∧ Tendsto (logCesaroPhi3 c2) atTop (𝓝 mu2) ∧ mu2 ≠ 0 :=
  ⟨log_cesaro_tendsto_zero, logCesaroPhi3_c2_tendsto_mu2, mu2_ne_zero⟩

/-- **Owner package.** (i) φ³ carrier not trace-class; (ii) `log(1+M_K)/(K+1) → 3 log φ`;
(iii) log-Cesàro limit `c/(3 log φ)`, nonzero for `c ≠ 0`; (iv) `c₂` normalises it to `μ₂`. -/
theorem perron_phi3_carrier_owner :
    (∀ c, 0 < c → Tendsto (partialSum c) atTop atTop)
      ∧ Tendsto normLog atTop (𝓝 (3 * Real.log phi))
      ∧ (∀ c, Tendsto (logCesaroPhi3 c) atTop (𝓝 (c / (3 * Real.log phi))))
      ∧ Tendsto (logCesaroPhi3 c2) atTop (𝓝 mu2) := by
  refine ⟨fun c hc => partialSum_unbounded hc, ?_, ?_, logCesaroPhi3_c2_tendsto_mu2⟩
  · rw [← log_alpha_eq]; exact normLog_tendsto
  · intro c; rw [← log_alpha_eq]; exact logCesaroPhi3_tendsto c

end D0.Spectral.PerronPhi3Carrier
