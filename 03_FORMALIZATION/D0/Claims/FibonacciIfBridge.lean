import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-FIBONACCI-IF-FORCING-001 — I_f = log φ via two routes (Lean core, status LEM)

Python certificate: `04_CERTIFICATES/vp_fibonacci_if_bridge.py`.

Self-calibrated status **LEM, not THE**: both routes give `log φ`, but the categorical↔toral
ISOMORPHISM is open (named gap). This module closes the algebraic "one number, two ways":

  * **Fibonacci anyons.** `d_τ = φ` is the positive root of the fusion relation `d² = d + 1`
    (`τ⊗τ = 1⊕τ`; Nayak et al., Rev. Mod. Phys. 80, 1083, 2008). State growth `~φⁿ` ⇒
    distinguishability per step `= log φ = I_f`.
  * **Toral automorphism.** `T = [[0,1],[1,-1]]` has characteristic polynomial `x² + x - 1`
    (trace `-1`, det `-1`); `-φ` is its eigenvalue of largest magnitude, so the spectral
    radius is `|-φ| = φ` and `h_KS = log φ`.

Hence `I_f = log φ = h_KS` — the SAME `φ` two ways. NOTE the fusion quadratic `x²-x-1` and the
toral charpoly `x²+x-1` differ by a sign: `φ` and `-φ` are different roots sharing magnitude
`φ`; they are not conflated. The categorical↔toral isomorphism (`Fib` state growth ≅ symbolic
dynamics of `T`) is NOT constructed here — the open gap that keeps this LEM, not THE.
-/

namespace D0.Claims

open D0

/-- `0 < φ`. -/
theorem phi_pos : 0 < phi := by
  unfold phi
  have h : 0 ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  linarith

/-- **Route 1 (Fibonacci).** `d_τ = φ` satisfies the fusion relation `d² = d + 1`. -/
theorem fibonacci_dim_fusion : phi ^ 2 = phi + 1 := phi_sq

/-- **Route 2 (toral).** `-φ` is a root of the toral characteristic polynomial `x² + x - 1`
(`T = [[0,1],[1,-1]]`, trace `-1`, det `-1`): `(-φ)² + (-φ) - 1 = 0`. -/
theorem neg_phi_toral_eigenvalue : (-phi) ^ 2 + (-phi) - 1 = 0 := by
  linear_combination phi_sq

/-- The toral spectral radius is `φ`: `|-φ| = φ`. So `h_KS = log|λ_max(T)| = log φ`, the same
`φ` as the Fibonacci quantum dimension `d_τ`. -/
theorem toral_spectral_radius_eq_phi : |(-phi)| = phi := by
  rw [abs_neg, abs_of_pos phi_pos]

/-- **D0-FIBONACCI-IF-FORCING-001 (LEM core).** The Fibonacci fusion dimension `d_τ = φ`
(`φ² = φ + 1`) and the toral spectral radius `|λ_max(T)| = φ` (`-φ` root of `x² + x - 1`,
`|-φ| = φ`) are the SAME number `φ`; hence `I_f = log φ = h_KS`. The categorical↔toral
isomorphism remains an open named gap (status LEM, not THE). -/
theorem fibonacci_if_bridge :
    phi ^ 2 = phi + 1 ∧ (-phi) ^ 2 + (-phi) - 1 = 0 ∧ |(-phi)| = phi :=
  ⟨fibonacci_dim_fusion, neg_phi_toral_eigenvalue, toral_spectral_radius_eq_phi⟩

end D0.Claims
