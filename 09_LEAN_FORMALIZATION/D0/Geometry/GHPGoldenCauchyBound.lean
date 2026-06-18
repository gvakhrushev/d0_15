import D0.Core.Delta
import Mathlib.Analysis.SpecificLimits.Basic

/-!
# D0-GHP-GOLDEN-CAUCHY-BOUND-001 — the golden refinement series converges (Lean)

Python certificate: `05_CERTS/vp_ghp_golden_cauchy_bound.py`.

Front E construction. The internal graph-refinement sequence `G_k → G_{k+1}` contracts at the golden
scale `δ₀ = 1/(2φ³)` (the dimension-quantum half-gap, `D0.Core.Delta`). Because `0 ≤ δ₀ < 1`, the
step-bound series `Σ_k C·δ₀^k` is **summable** (a convergent geometric majorant), so the refinement
sequence is GHP-Cauchy *for the internal step bound* — the finite, owned half of the
Rieffel/GHP continuum question.

HONESTY BOUNDARY. What is proved here is the internal-metric Cauchy/summability bound from `δ₀ < 1`.
The full Gromov–Hausdorff(-Prokhorov) convergence to a *smooth* manifold, and the identification of
the limit object, stay the external owners `D0-RIEFFEL-GHP-CONTINUUM-OWNER-001` (ASSUMP-RIEFFEL-GHP)
and `D0-CONNES-RECONSTRUCTION-OWNER-001` (ASSUMP-CONNES-RECONSTRUCTION); the smooth manifold itself
stays `D0-SMOOTH-MANIFOLD-PASSPORT-001`. This module owns only the geometric-series step bound.
-/

namespace D0.Geometry

open D0

/-- `2 < √5` (from `(√5)² = 5` and `√5 ≥ 0`). -/
private lemma two_lt_sqrt5 : (2 : ℝ) < Real.sqrt 5 := by
  nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]

/-- `1 < φ`. -/
private lemma one_lt_phi : (1 : ℝ) < phi := by
  unfold phi; nlinarith [two_lt_sqrt5]

/-- `φ³ = 2φ + 1` (from `φ² = φ + 1`), so cube bounds stay linear. -/
private lemma phi_cube : phi ^ 3 = 2 * phi + 1 := by
  linear_combination (phi + 1) * phi_sq

/-- `0 < 2φ³`. -/
private lemma two_phi_cube_pos : (0 : ℝ) < 2 * phi ^ 3 := by
  nlinarith [phi_cube, one_lt_phi]

/-- **The golden refinement ratio is strictly below one:** `δ₀ = 1/(2φ³) < 1`. -/
theorem delta0_lt_one : delta0 < 1 := by
  rw [delta_phi_cubed, div_lt_one two_phi_cube_pos]
  nlinarith [phi_cube, one_lt_phi]

/-- **The golden refinement ratio is positive:** `0 < δ₀`. -/
theorem delta0_pos : 0 < delta0 := by
  rw [delta_phi_cubed]; exact div_pos one_pos two_phi_cube_pos

/-- `0 ≤ δ₀`. -/
theorem delta0_nonneg : 0 ≤ delta0 := le_of_lt delta0_pos

/-- **The golden refinement series is summable** (geometric majorant, ratio `δ₀ < 1`). -/
theorem ghp_refinement_summable : Summable (fun k : ℕ => delta0 ^ k) :=
  summable_geometric_of_lt_one delta0_nonneg delta0_lt_one

/-- **D0-GHP-GOLDEN-CAUCHY-BOUND-001 (scaled).** For any step constant `C`, the GHP step-bound
series `Σ_k C·δ₀^k` is summable — the refinement sequence is Cauchy for the internal step bound. -/
theorem ghp_golden_cauchy_bound (C : ℝ) : Summable (fun k : ℕ => C * delta0 ^ k) :=
  (ghp_refinement_summable).mul_left C

/-- The exact geometric sum: `Σ_k δ₀^k = (1 − δ₀)⁻¹` (finite, since `δ₀ < 1`). -/
theorem ghp_golden_cauchy_sum : ∑' k : ℕ, delta0 ^ k = (1 - delta0)⁻¹ :=
  tsum_geometric_of_lt_one delta0_nonneg delta0_lt_one

/-- **Owner package.** `0 ≤ δ₀ < 1`, the refinement series is summable, and the scaled step-bound
series converges for every `C` — the internal-metric GHP-Cauchy bound. (The smooth-manifold limit
stays the external Rieffel/GHP + Connes-reconstruction owners; this is the finite owned half.) -/
theorem ghp_golden_cauchy_owner :
    (0 ≤ delta0 ∧ delta0 < 1)
      ∧ Summable (fun k : ℕ => delta0 ^ k)
      ∧ (∀ C : ℝ, Summable (fun k : ℕ => C * delta0 ^ k)) :=
  ⟨⟨delta0_nonneg, delta0_lt_one⟩, ghp_refinement_summable, ghp_golden_cauchy_bound⟩

end D0.Geometry
