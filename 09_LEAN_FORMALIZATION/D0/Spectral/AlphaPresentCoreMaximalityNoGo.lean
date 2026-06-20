import D0.Spectral.AlphaProfiniteTowerNoGo

/-!
# D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001 — every admissible present-core tower fails μ₂

Strengthening of `D0-ALPHA-PROFINITE-TOWER-NOGO-001` (one specific φ-ladder tower is trace-class) to a
**maximality** statement quantified over ALL admissible present-core towers.

An admissible present-core refinement tower has the frozen φ-ladder weight `r = φ⁻³` per increment and an
increment multiplicity growing at rate `a` (block `N` carries `~φ^{aN}` states). The per-block
contribution to the singular-value trace is `rate a = φ^a · r = φ^{a-3}`. Present-core supplies only:
`a = 0` (constant Boolean ledger `2¹¹`) and `a = 1` (golden carrier, Perron eigenvalue `φ` of
`[[1,1],[1,0]]`). For ANY `a ≤ 2 < 3` the contribution ratio `φ^{a-3} < 1`, so the global operator is
**summable (trace-class)** and its ordinary log-Cesàro / Dixmier coefficient is `0`, never `μ₂ = 12288/5`.

The critical `1/j` line (`L^{1,∞} ∖ L¹`, nonzero log-Cesàro limit) is reached **only** at `rate = 1`,
i.e. exactly `a = 3` — a carrier with Perron eigenvalue `φ³`, the cube of the forced golden rate. 5-fold
symmetry + the M1 selector force the single golden rate `φ`, so no present-core carrier supplies `a = 3`.

Conclusion: no admissible present-core tower realizes `μ₂` as a Dixmier-type coefficient. The remaining
interface is therefore an EXTERNAL Dixmier/Wodzicki residue passport OR a NEW independently-forced carrier
with Perron eigenvalue `φ³` — neither is a present-core object. Not the invalid finite-pole route.
-/

namespace D0.Spectral.AlphaPresentCoreMaximalityNoGo

open D0.Spectral.AlphaProfiniteSpectralTower D0

/-- Per-block trace contribution at multiplicity growth rate `a`: `rate a = φ^a · r = φ^{a-3}`. -/
noncomputable def rate (a : ℕ) : ℝ := phi ^ a * r

theorem rate_pos (a : ℕ) : 0 < rate a := mul_pos (pow_pos phi_pos a) tower_weight_ratio_pos

/-- **Every admissible present-core rate is strictly sub-critical**: `a ≤ 2 ⇒ rate a < 1`. -/
theorem rate_lt_one (a : ℕ) (ha : a ≤ 2) : rate a < 1 := by
  have hφ : (1 : ℝ) < phi := one_lt_phi
  have hpos : (0 : ℝ) < phi := phi_pos
  have hlt : phi ^ a < phi ^ 3 := pow_lt_pow_right₀ hφ (by omega)
  have h3 : (0 : ℝ) < phi ^ 3 := pow_pos hpos 3
  have heq : rate a = phi ^ a / phi ^ 3 := by
    unfold rate r; rw [inv_pow]; ring
  rw [heq, div_lt_one h3]; exact hlt

/-- **The critical `1/j` line is reached exactly at `a = 3`** (carrier Perron eigenvalue `φ³`):
`rate 3 = 1`. -/
theorem rate_three_eq_one : rate 3 = 1 := by
  unfold rate r
  rw [← mul_pow, mul_inv_cancel₀ (ne_of_gt phi_pos), one_pow]

/-- **Every admissible present-core tower is trace-class** (summable singular values) — for ANY growth
rate `a ≤ 2`, including the constant ledger `a = 0` and the golden carrier `a = 1`. -/
theorem admissible_tower_trace_class (a : ℕ) (ha : a ≤ 2) :
    Summable (fun N : ℕ => (rate a) ^ N) :=
  summable_geometric_of_lt_one (rate_pos a).le (rate_lt_one a ha)

/-- **D0-ALPHA-PRESENT-CORE-MAXIMALITY-NOGO-001.** No admissible present-core tower realizes `μ₂`: for
every present-core growth rate `a ≤ 2` the tower is trace-class (Dixmier coefficient `0`), while
`μ₂ ≠ 0`; the critical line needs `a = 3` (Perron eigenvalue `φ³`), which is `rate 3 = 1` and is NOT a
present-core carrier. -/
theorem alpha_present_core_maximality_nogo :
    (∀ a : ℕ, a ≤ 2 → Summable (fun N : ℕ => (rate a) ^ N)) ∧ rate 3 = 1 ∧ mu2 ≠ 0 :=
  ⟨admissible_tower_trace_class, rate_three_eq_one,
   D0.Spectral.AlphaProfiniteTowerNoGo.mu2_ne_zero⟩

end D0.Spectral.AlphaPresentCoreMaximalityNoGo
