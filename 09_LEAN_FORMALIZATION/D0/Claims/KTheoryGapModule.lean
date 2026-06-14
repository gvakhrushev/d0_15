import D0.Core.Phi

/-!
# D0-KTHEORY-GAP-MODULE-001 — gap labels lie in the rank-2 module Z+Zφ⁻¹ (finite shadow)

Python certificate: `05_CERTS/vp_ktheory_gap_labels_finite.py`.

Finite-core reduction of the Bellissard gap-labeling family. The Bellissard THEOREM
(IDS-on-gaps = image of the K0 trace) needs operator K-theory absent from Mathlib and stays
EXTERNAL-GAP. Its DECIDABLE SHADOW is exact: for the φ quasicrystal the gap-labeling group
is the rank-2 module `Z + Z·φ⁻¹ = Z[φ]`, closed under the φ-action by the primitive relation
`φ⁻¹ + φ⁻² = 1`, and the two principal gap labels are the Sturmian letter frequencies
`φ⁻¹` (common) and `φ⁻²` (rare), which lie in the unit interval and sum to `1` (total IDS).

This module proves that structural shadow (reusing the frozen `D0.Core.Phi`). It does NOT
prove the Bellissard identity — that stays the frontier obligation.
-/

namespace D0.Claims

open D0

/-- The rank-2 closure relation of the gap-labeling module `Z+Zφ⁻¹`: `φ⁻¹ + φ⁻² = 1`. -/
theorem gap_module_closure : phi⁻¹ + phi⁻¹ ^ 2 = 1 := phi_inv_satisfies_primitive

/-- The rare-letter gap label `φ⁻² = 1 − φ⁻¹` — coordinates `(1, −1)` in `Z + Z·φ⁻¹`. -/
theorem gap_rare_label : phi⁻¹ ^ 2 = 1 - phi⁻¹ := by
  have h := phi_inv_satisfies_primitive; linarith

/-- `1 < φ`, hence the common-letter gap label `φ⁻¹` lies strictly in the unit interval. -/
theorem phi_gt_one : (1 : ℝ) < phi := by
  unfold phi
  have h : (1 : ℝ) < Real.sqrt 5 := by
    have : Real.sqrt 1 < Real.sqrt 5 := Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    simpa using this
  linarith

theorem gap_label_in_unit_interval : 0 < phi⁻¹ ∧ phi⁻¹ < 1 := by
  have hp : (0 : ℝ) < phi := lt_trans one_pos phi_gt_one
  exact ⟨inv_pos.mpr hp, inv_lt_one_of_one_lt₀ phi_gt_one⟩

/-- **D0-KTHEORY-GAP-MODULE-001 (shadow).** The gap-labeling module `Z+Zφ⁻¹` is closed
(`φ⁻¹+φ⁻²=1`), the rare label is `φ⁻² = 1−φ⁻¹`, the two principal labels `φ⁻¹, φ⁻²` lie in
`(0,1)` and sum to `1` (total IDS). The Bellissard `IDS = K0-trace` identity is NOT claimed. -/
theorem ktheory_gap_module :
    (phi⁻¹ + phi⁻¹ ^ 2 = 1) ∧
    (phi⁻¹ ^ 2 = 1 - phi⁻¹) ∧
    (0 < phi⁻¹ ∧ phi⁻¹ < 1) :=
  ⟨gap_module_closure, gap_rare_label, gap_label_in_unit_interval⟩

end D0.Claims
