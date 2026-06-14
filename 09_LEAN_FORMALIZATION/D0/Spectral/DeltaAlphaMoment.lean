import D0.Spectral.DeltaAlphaExact

/-!
# D0-DELTA-ALPHA-MOMENT-001 — α_alg⁻¹ is the depth-2 π₀-phase moment of W_eff (Lean)

Python certificate: `05_CERTS/vp_delta_alpha_pi0_moment.py`.

Sharpening (not closure) of §05.6 obligation 4. The exact value of `α_alg⁻¹` is already closed
(`D0-DELTA-ALPHA-EXACT-001`). This module proves the FINITE SHADOW of the analytic owner: with
`δ₀ = ½φ⁻³`, the algebraic writing collapses into a polynomial in the single rank-3 archive unit
`u = φ⁻³`,

    α_alg⁻¹ = 2¹¹·(6/5)φ²·φ⁻⁸ + (2/3)·(½)φ⁻³ = μ₂·u² + μ₁·u ,  μ₂ = 12288/5, μ₁ = 1/3, u = φ⁻³,

with NO constant term (`P 0 = 0`). That is exactly the shape of a depth-≤2 resolvent moment
expansion `W_eff(z) = A + Σₖ z⁻⁽ᵏ⁺¹⁾·B Dᵏ C` (`D0-GENERATIVE-DYNAMICS-001`): the exponents `−6, −3`
are `−2·rank, −1·rank`, the second moment `μ₂` carries the `π₀` feedback phase, and `μ₀ = 0` means
zero archive depth ⇒ zero anomaly (the mechanistic sign, forced).

HONESTY BOUNDARY. What is Lean-proved here is the exact `ℚ(φ)` SHAPE — the degree-2 polynomial in
`u=φ⁻³`, no constant term, the value. The two residue amplitudes `μ₂=2¹¹π₀φ⁻²` and `μ₁=1/3` are the
`s→pole` continuation data (profinite spectral measure) and are NOT derived here; this SHARPENS
CVFT-F1, it does not close it. `Δ_α` keeps its honest status.
-/

namespace D0.Spectral

open D0

private lemma hpos' : (0 : ℝ) < phi := by unfold phi; positivity
private lemma hne' : phi ≠ 0 := ne_of_gt hpos'

/-- The depth-≤2 archive moment polynomial `P(u) = μ₂·u² + μ₁·u` (no constant term). -/
def momentPoly (mu2 mu1 u : ℝ) : ℝ := mu2 * u ^ 2 + mu1 * u

/-- **No constant term.** `P(0) = 0`: zero archive depth ⇒ zero anomaly contribution. -/
theorem momentPoly_zero (mu2 mu1 : ℝ) : momentPoly mu2 mu1 0 = 0 := by
  unfold momentPoly; ring

/-- The algebraic writing of `α_alg⁻¹` IS the depth-2 moment polynomial in the rank-3 unit
`u = φ⁻³`, with second-moment residue `μ₂ = 12288/5 (= 2¹¹·π₀·φ⁻²)` and first-moment residue
`μ₁ = 1/3`. -/
theorem alphaAlg_as_moment :
    2048 * ((6 / 5) * phi ^ 2) * phi⁻¹ ^ 8 + (2 / 3) * ((1 / 2) * phi⁻¹ ^ 3)
      = momentPoly (12288 / 5) (1 / 3) (phi⁻¹ ^ 3) := by
  unfold momentPoly
  have h22 : phi ^ 2 * phi⁻¹ ^ 2 = 1 := by
    rw [← mul_pow, mul_inv_cancel₀ hne', one_pow]
  have key : phi ^ 2 * phi⁻¹ ^ 8 = phi⁻¹ ^ 6 := by
    have e8 : phi⁻¹ ^ 8 = phi⁻¹ ^ 2 * phi⁻¹ ^ 6 := by ring
    rw [e8, ← mul_assoc, h22, one_mul]
  have hu2 : (phi⁻¹ ^ 3) ^ 2 = phi⁻¹ ^ 6 := by ring
  have e : 2048 * ((6 / 5) * phi ^ 2) * phi⁻¹ ^ 8 = (12288 / 5) * (phi ^ 2 * phi⁻¹ ^ 8) := by ring
  rw [hu2, e, key]; ring

/-- The moment polynomial evaluates to the closed `ℚ(φ)` value of `α_alg⁻¹`. -/
theorem alphaAlg_moment_value :
    momentPoly (12288 / 5) (1 / 3) (phi⁻¹ ^ 3) = 159739 / 5 - 294902 / 15 * phi := by
  unfold momentPoly
  have hu2 : (phi⁻¹ ^ 3) ^ 2 = phi⁻¹ ^ 6 := by ring
  rw [hu2, phi_inv6, phi_inv3]; ring

/-- **D0-DELTA-ALPHA-MOMENT-001.** The algebraic writing of `α_alg⁻¹` is exactly the depth-2
archive moment polynomial in the rank-3 unit `u = φ⁻³` — (i) it equals `μ₂·u² + μ₁·u`, (ii) which
evaluates to the closed value `159739/5 − (294902/15)φ`, (iii) and has no constant term (`P 0 = 0`).
The two residue amplitudes stay the `s→pole` continuation (CVFT-F1 frontier). -/
theorem delta_alpha_moment :
    (2048 * ((6 / 5) * phi ^ 2) * phi⁻¹ ^ 8 + (2 / 3) * ((1 / 2) * phi⁻¹ ^ 3)
        = momentPoly (12288 / 5) (1 / 3) (phi⁻¹ ^ 3))
      ∧ (momentPoly (12288 / 5) (1 / 3) (phi⁻¹ ^ 3) = 159739 / 5 - 294902 / 15 * phi)
      ∧ (momentPoly (12288 / 5) (1 / 3) 0 = 0) :=
  ⟨alphaAlg_as_moment, alphaAlg_moment_value, momentPoly_zero _ _⟩

end D0.Spectral
