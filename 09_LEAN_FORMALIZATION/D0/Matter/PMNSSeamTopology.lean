import D0.Core.Phi
import D0.Core.Delta
import D0.Dynamics.PisotContraction
import Mathlib.Tactic

/-!
# D0-PMNS-SEAM-TOPOLOGY-001 — the three PMNS angles from one rule (δ₀-degree = seam topology)

The closure-holonomy, projected onto the three channels of the kernel `30 = 8⊕10⊕12`, gives one rule:
the **degree of δ₀** in an angle correction equals the seam-cycle topology —
`bare/open/closed → δ₀^{0,1,2}`:
* `sin²θ₁₃ = φ⁻⁵/4`        (bare seam, δ₀⁰),
* `sin²θ₂₃ = 1/2 + δ₀/2`   (open tilt, δ₀¹),
* `sin²θ₁₂ = 1/3 − 2δ₀²`   (closed loop, δ₀²),
with `δ₀ = ½φ⁻³` (forced; `D0.Core.Delta`). This module proves the **structural directional content** of
the rule — each correction pushes its baseline the right way (θ₂₃ above maximal, θ₁₂ below trimaximal,
θ₁₃ positive). The numeric VALUES (all <1σ vs JUNO-2026 + NuFIT-6.0) and the degree-permutation
discriminating test stay in the cert `05_CERTS/vp_pmns_seam_topology.py` (CHK, empirical).
-/

namespace D0.Matter

open D0

/-- `sin²θ₁₃ = φ⁻⁵/4` — bare seam (δ₀⁰). -/
noncomputable def seamTh13 : ℝ := phi ^ (-5 : ℤ) / 4

/-- `sin²θ₂₃ = 1/2 + δ₀/2` — open tilt (δ₀¹). -/
noncomputable def seamTh23 : ℝ := 1 / 2 + delta0 / 2

/-- `sin²θ₁₂ = 1/3 − 2δ₀²` — closed loop (δ₀²). -/
noncomputable def seamTh12 : ℝ := 1 / 3 - 2 * delta0 ^ 2

theorem delta0_pos : 0 < delta0 := by
  rw [delta_phi_cubed]; have := phi_gt_one; positivity

/-- Bare seam is strictly populated: `sin²θ₁₃ > 0`. -/
theorem seamTh13_pos : 0 < seamTh13 := by
  unfold seamTh13; have := phi_gt_one; positivity

/-- Open tilt sits strictly ABOVE the maximal-mixing baseline `1/2` (δ₀¹ correction). -/
theorem seamTh23_gt_half : 1 / 2 < seamTh23 := by
  unfold seamTh23; have := delta0_pos; linarith

/-- Closed loop sits strictly BELOW the trimaximal baseline `1/3` (δ₀² correction). -/
theorem seamTh12_lt_third : seamTh12 < 1 / 3 := by
  unfold seamTh12; have := delta0_pos; nlinarith

/-- **D0-PMNS-SEAM-TOPOLOGY-001 (structure).** The three channels carry the three δ₀-degrees with the
forced directions: `θ₁₃ > 0` (bare), `θ₂₃ > 1/2` (open, above maximal), `θ₁₂ < 1/3` (closed, below
trimaximal). Numeric agreement with data is the cert's CHK content. -/
theorem pmns_seam_topology :
    0 < seamTh13 ∧ 1 / 2 < seamTh23 ∧ seamTh12 < 1 / 3 :=
  ⟨seamTh13_pos, seamTh23_gt_half, seamTh12_lt_third⟩

end D0.Matter
