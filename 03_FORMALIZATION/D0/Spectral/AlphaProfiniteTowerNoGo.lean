import D0.Spectral.AlphaProfiniteSpectralTower

/-!
# D0-ALPHA-PROFINITE-TOWER-NOGO-001 — Outcome B (trace-class ⇒ Dixmier coefficient 0 ≠ mu_2)

The canonical φ-ladder refinement tower (`D0-ALPHA-PROFINITE-SPECTRAL-TOWER-OWNER-001`) is trace-class:
its singular-value partial sums are bounded by a fixed constant `C = 2¹¹·(1−r)⁻¹`. Hence the ordinary
logarithmic Cesàro coefficient `Σ_K / log(1+K) → 0`, NOT `mu_2 = 12288/5 > 0`. The canonical tower
therefore CANNOT realize `mu_2` as a Dixmier-type logarithmic trace coefficient (**Outcome B**).

This is NOT the invalid finite-pole route (the finite heat trace is analytic at 0 with no `1/s`
coefficient — `D0-DIXMIER-FESHBACH-FINITE-HEATTRACE-001`). It is the profinite complement: even the
infinite pro-object built from the canonical stages is trace-class, so its Dixmier coefficient is `0`.

SHARPER MECHANISM (independently re-derived by adversarial scout): D0 freezes weight decay `φ^(-3N)`
AND the golden carrier growth `φ^(+N)` (Perron eigenvalue `φ` of `[[1,1],[1,0]]`, forced by 5-fold
symmetry + M1). Their product `φ^(-2N)` is STILL strictly summable — two full powers of `φ` *inside* the
`L^{1,∞}` critical `1/j` line. So even the natural carrier-weighted tower is trace-class.

EXACT MISSING ARTIFACT: a canonical refinement carrier with Perron eigenvalue `φ³` (the cube of the
forced golden rate; multiplicity growth `~φ^(3N)`) whose growth exactly cancels the `φ^(-3N)` weight
decay onto the critical line `s_j ~ mu_2/j` (i.e. `L^{1,∞} ∖ L¹` with a nonzero log-Cesàro limit).
Equivalently on the tower side: an isometric `J_N` embedding + metric defect bound upgrading the existing
DOWNWARD-projection inverse-limit tower (`D0-ARCHIVE-LIGHTPROFINITE-001`) to a critically-tuned isometric
tower — firewalled to `ASSUMP-RIEFFEL-GHP` / `ASSUMP-CONNES-RECONSTRUCTION`. No frozen D0 sequence
(φ-ladder, cylinder count, Boolean ledger depth = constant `2¹¹`, finite support growth) supplies it;
choosing one is forbidden. The external Dixmier-residue owner (`D0-DIXMIER-RESIDUE-OWNER-001`) and the
seam gap (`D0-ALPHA-FESHBACH-DIXMIER-OWNER-001`, PROOF-TARGET) stay unpromoted.
-/

namespace D0.Spectral.AlphaProfiniteTowerNoGo

open D0.Spectral.AlphaProfiniteSpectralTower Filter Topology

theorem mu2_pos : 0 < mu2 := by unfold mu2; norm_num

theorem mu2_ne_zero : mu2 ≠ 0 := ne_of_gt mu2_pos

/-- The number of singular values up to depth `M`: `2¹¹·(M+1)`. -/
noncomputable def numSV (M : ℕ) : ℝ := (towerMult : ℝ) * ((M : ℝ) + 1)

/-- The ordinary logarithmic Cesàro ratio of the canonical tower at depth `M`. -/
noncomputable def logCesaro (M : ℕ) : ℝ := towerPartialSum M / Real.log (1 + numSV M)

theorem numSV_pos (M : ℕ) : 0 < numSV M := by
  unfold numSV
  have ht : (0 : ℝ) < (towerMult : ℝ) := Nat.cast_pos.mpr (by unfold towerMult; norm_num)
  have hm : (0 : ℝ) < (M : ℝ) + 1 := by positivity
  exact mul_pos ht hm

theorem numSV_tendsto_atTop : Tendsto numSV atTop atTop := by
  unfold numSV
  have ht : (0 : ℝ) < (towerMult : ℝ) := Nat.cast_pos.mpr (by unfold towerMult; norm_num)
  apply Tendsto.const_mul_atTop ht
  exact tendsto_atTop_add_const_right atTop 1 tendsto_natCast_atTop_atTop

/-- `log(1 + #singular values) → ∞`. -/
theorem denom_tendsto_atTop :
    Tendsto (fun M : ℕ => Real.log (1 + numSV M)) atTop atTop :=
  Real.tendsto_log_atTop.comp (tendsto_atTop_add_const_left atTop 1 numSV_tendsto_atTop)

/-- **The canonical tower's log-Cesàro coefficient is `0`** (trace-class: bounded numerator over a
denominator that diverges). -/
theorem log_cesaro_tendsto_zero : Tendsto logCesaro atTop (𝓝 0) := by
  obtain ⟨C, hC⟩ := singular_value_partial_sum_bound
  apply squeeze_zero (g := fun M => C / Real.log (1 + numSV M))
  · intro M
    apply div_nonneg _ (Real.log_nonneg (by have := numSV_pos M; linarith))
    unfold towerPartialSum
    apply mul_nonneg (by positivity)
    exact Finset.sum_nonneg (fun i _ => pow_nonneg tower_weight_ratio_pos.le i)
  · intro M
    have hden : 0 < Real.log (1 + numSV M) := Real.log_pos (by have := numSV_pos M; linarith)
    simp only [logCesaro, div_eq_mul_inv]
    exact mul_le_mul_of_nonneg_right (hC M) (inv_nonneg.mpr hden.le)
  · exact tendsto_const_nhds.div_atTop denom_tendsto_atTop

/-- **D0-ALPHA-PROFINITE-TOWER-NOGO-001 (Outcome B).** The canonical tower's log-Cesàro coefficient is
`0`, while `mu_2 ≠ 0`: the canonical φ-ladder tower does NOT realize `mu_2` as a Dixmier-type logarithmic
trace coefficient. -/
theorem profinite_tower_log_cesaro_limit_zero_ne_mu2 :
    Tendsto logCesaro atTop (𝓝 0) ∧ mu2 ≠ 0 :=
  ⟨log_cesaro_tendsto_zero, mu2_ne_zero⟩

/-- The clean no-go: the log-Cesàro limit cannot equal `mu_2` (it is `0` by uniqueness of limits). -/
theorem profinite_tower_dixmier_nogo : ¬ Tendsto logCesaro atTop (𝓝 mu2) := by
  intro h
  exact mu2_ne_zero (tendsto_nhds_unique h log_cesaro_tendsto_zero)

end D0.Spectral.AlphaProfiniteTowerNoGo
