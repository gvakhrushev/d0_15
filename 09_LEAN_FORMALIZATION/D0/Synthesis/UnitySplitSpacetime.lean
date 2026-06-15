import D0.Core.Phi

/-!
# D0-UNITY-SPLIT-SPACETIME-001 — unity split ⇒ space (symmetric) + time (antisymmetric δ₀) (Lean)

Python certificate: `05_CERTS/vp_unity_split_spacetime.py`.

Splitting the unit around ½ gives two canonical cuts — honest `1 = ½+½` (symmetric) and
self-consistent `1 = φ⁻¹+φ⁻²` (forced by `p²+p=1`) — separated by exactly `δ₀ = φ⁻¹ − ½ =
(√5−2)/2`. The symmetric part is exchange-invariant ⇒ space; the antisymmetric part `s = δ₀`
flips sign ⇒ time (one arrow). The operator `T = [[0,1],[1,−1]]` has `det = −1 = ψ·φ` and spectrum
`{φ⁻¹, −φ}` (roots of `λ²+λ−1`): one positive eigenvalue (space) and exactly one negative
(the arrow).

This module proves the decidable SHADOW (δ₀ exact, `det = −1 = ψφ`, the two eigenvalues and their
signs). Status is **LEM**: the step "the symmetric part is specifically rank-3 adjacency" routes to
the rank-3 = causal-cone node, which is ALREADY FORCED (`D0-RANK3-CAUSAL-CONE-FORCING-001`,
Iter-11) — so the residual is that one identification and the cone-speed (Connes) unit, not a fresh
open gap. Not promoted past LEM.
-/

namespace D0.Synthesis

open D0

/-- `δ₀ = φ⁻¹ − ½ = (√5 − 2)/2`, the separation of the two canonical cuts of unity. -/
theorem delta0_exact : phi⁻¹ - 1 / 2 = (Real.sqrt 5 - 2) / 2 := by
  rw [phi_inv_eq_primitiveRoot]; unfold primitiveRoot; ring

/-- `det T = −1 = ψ·φ` (Vieta) for `T = [[0,1],[1,−1]]`. -/
theorem det_T_eq_psi_phi : (0 : ℝ) * (-1) - 1 * 1 = psi * phi := by
  rw [mul_comm psi phi, phi_mul_psi]; norm_num

/-- `φ⁻¹` is an eigenvalue of `T`: it solves `λ² + λ − 1 = 0`. -/
theorem phi_inv_is_eigenvalue : phi⁻¹ ^ 2 + phi⁻¹ - 1 = 0 := by
  linear_combination phi_inv_satisfies_primitive

/-- `−φ` is the other eigenvalue of `T`: it solves `λ² + λ − 1 = 0`. -/
theorem neg_phi_is_eigenvalue : (-phi) ^ 2 + (-phi) - 1 = 0 := by
  linear_combination phi_sq

private lemma phi_pos : (0 : ℝ) < phi := by unfold phi; positivity

/-- **D0-UNITY-SPLIT-SPACETIME-001.** Unity split gives space (symmetric) + time (antisymmetric):
`δ₀` exact, `det T = −1 = ψφ`, the two eigenvalues `φ⁻¹` (positive ⇒ space) and `−φ` (negative ⇒
the single time arrow). -/
theorem unity_split_spacetime :
    (phi⁻¹ - 1 / 2 = (Real.sqrt 5 - 2) / 2) ∧
    ((0 : ℝ) * (-1) - 1 * 1 = psi * phi) ∧
    (phi⁻¹ ^ 2 + phi⁻¹ - 1 = 0) ∧
    ((-phi) ^ 2 + (-phi) - 1 = 0) ∧
    (0 < phi⁻¹) ∧ (-phi < 0) :=
  ⟨delta0_exact, det_T_eq_psi_phi, phi_inv_is_eigenvalue, neg_phi_is_eigenvalue,
    inv_pos.mpr phi_pos, by linarith [phi_pos]⟩

end D0.Synthesis
