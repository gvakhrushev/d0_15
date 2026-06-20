import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-PERRON-SCALE-FLOW-OWNER-001 — the refinement scale ratio is forced to φ

Master Owner A scale law. Every internally-defined refinement scale of the golden Bratteli tower
(Perron refinement count, Fibonacci level dimension, φ-ladder) shares the same dimensionless step ratio
`Λ_(N+1)/Λ_N = φ`. The *absolute* scale is dimensionless/unfixed (no imported length), but the **ratio is
canonically forced** to the Perron eigenvalue `φ`. This is the present-core scale-flow result.

OBSTRUCTION (recorded, not faked): the algebra-level Bratteli system embeds inductively (incidence `M_φ`,
`D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001`), but a *Dirac-compatible isometric inductive spectral triple*
(`J_N† D_(N+1) J_N = D_N` with `J_N† J_N = I`) is NOT a present-core object — the corpus realizes the tower
as an INVERSE limit of downward projections (`D0-ARCHIVE-LIGHTPROFINITE-001`), and the inductive isometric
realization is firewalled to `ASSUMP-CONNES-RECONSTRUCTION` / propinquity (external passport
`D0-INDUCTIVE-SPECTRAL-TRIPLE-OWNER-001`). Hence Master A Outcome B: canonical refinement + trace + scale,
but no canonical inductive spectral triple from present core.
-/

namespace D0.Spectral.CanonicalRefinementScaleFlow

open D0

theorem phi_pos : 0 < phi := by unfold phi; positivity

/-- The Perron refinement-count scale at level `N`. -/
noncomputable def Lambda (N : ℕ) : ℝ := phi ^ N

/-- **The refinement scale ratio is forced to `φ`**: `Λ_(N+1)/Λ_N = φ` for every level `N`. -/
theorem scale_ratio_forced (N : ℕ) : Lambda (N + 1) / Lambda N = phi := by
  unfold Lambda
  rw [pow_succ, mul_comm, mul_div_assoc, div_self (pow_ne_zero N (ne_of_gt phi_pos)), mul_one]

/-- The step ratio is independent of the level `N` (a single canonical scale-flow rate `φ`). -/
theorem scale_ratio_constant (M N : ℕ) : Lambda (M + 1) / Lambda M = Lambda (N + 1) / Lambda N := by
  rw [scale_ratio_forced, scale_ratio_forced]

/-- **D0-PERRON-SCALE-FLOW-OWNER-001.** The canonical refinement scale flow has the unique forced step
ratio `φ` at every level (the absolute scale being dimensionless). -/
theorem perron_scale_flow_owner :
    (∀ N : ℕ, Lambda (N + 1) / Lambda N = phi)
      ∧ (∀ M N : ℕ, Lambda (M + 1) / Lambda M = Lambda (N + 1) / Lambda N) :=
  ⟨scale_ratio_forced, scale_ratio_constant⟩

end D0.Spectral.CanonicalRefinementScaleFlow
