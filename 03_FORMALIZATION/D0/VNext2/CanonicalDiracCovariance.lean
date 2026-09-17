import D0.VNext.CanonicalMartingaleDiracScale
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001 — the covariance cocycle is determined once the scale is canonical

The covariance owner asks for a canonical **scale cocycle** `ω : ℕ → ℝ`, `ω(N) = λ_{N+1}/λ_N`, governing how
the martingale Dirac transforms under refinement `N → N+1`. The Iter23 NO-GO filed this as blocked on
`PRIM-DIRAC-SCALE-SELECTION`: with the scale `λ_N` underdetermined (Christensen–Ivan freedom), the cocycle
is not fixed.

That primitive has since been resolved positively (`D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001`):
the canonical, internally-sourced scale is `λ_N = λ_0 · φ^N`. **With the scale fixed, the covariance cocycle
is determined**: for any internally-sourced scale, `ω(N) = λ_{N+1}/λ_N = φ` for every `N` — a *constant*
1-cocycle, independent of the base `λ_0` and of the level `N`. This is the positive companion to the
Outcome-C NO-GO: the residual scale freedom (the base `λ_0`) drops out of the cocycle entirely, so the
covariance datum the owner asked for exists and is canonical.

Honest scope: this fixes the *scale* cocycle (the covariance owner's actual content). It does NOT assert a
scene↔AF spectral congruence — that stronger lift stays NO-GO (`D0-VNEXT2-SCENE-SPECTRAL-LIFT-OWNER-001`),
now on the sharp grounds that the compressed scene spectrum is not the geometric φ-ladder.
-/

namespace D0.VNext2.CanonicalDiracCovariance

open D0 D0.VNext.CanonicalMartingaleDiracScale

/-- The **covariance (scale) cocycle** of a scale law: `ω(N) = λ(N+1)/λ(N)`. -/
noncomputable def covarianceCocycle (lam : ℕ → ℝ) (N : ℕ) : ℝ := lam (N + 1) / lam N

/-- **For any internally-sourced scale the covariance cocycle is the constant φ.** This is immediate from
the definition of `InternallySourced`, but it is the load-bearing covariance fact: the cocycle does not
depend on `N`. -/
theorem cocycle_constant_phi (lam : ℕ → ℝ) (hsrc : InternallySourced lam) :
    ∀ N, covarianceCocycle lam N = phi := by
  intro N; exact hsrc N

/-- The canonical φ-ladder has constant covariance cocycle φ, for every base `λ_0 ≠ 0`. -/
theorem phiLadder_cocycle_constant (lam0 : ℝ) (h0 : lam0 ≠ 0) :
    ∀ N, covarianceCocycle (fun N => lam0 * phi ^ N) N = phi :=
  cocycle_constant_phi _ (phiLadder_internallySourced lam0 h0)

/-- **Base-independence.** Two canonical scales with different bases have the *same* covariance cocycle:
the residual scale freedom `λ_0` is invisible to the covariance datum. -/
theorem cocycle_base_independent (a b : ℝ) (ha : a ≠ 0) (hb : b ≠ 0) :
    ∀ N, covarianceCocycle (fun N => a * phi ^ N) N
       = covarianceCocycle (fun N => b * phi ^ N) N := by
  intro N
  rw [phiLadder_cocycle_constant a ha N, phiLadder_cocycle_constant b hb N]

/-- **D0-VNEXT2-SCENE-DIRAC-COVARIANCE-OWNER-001.** Packaging: once the scale is canonical (internally
sourced), the covariance cocycle (1) is the constant φ at every level, and (2) is independent of the base
`λ_0`. So the covariance datum exists and is canonical — the owner is discharged by the resolved
scale-selection primitive, not blocked by it. -/
theorem canonical_dirac_covariance_owner :
    (∀ lam : ℕ → ℝ, InternallySourced lam → ∀ N, covarianceCocycle lam N = phi)
    ∧ (∀ a b : ℝ, a ≠ 0 → b ≠ 0 → ∀ N,
        covarianceCocycle (fun N => a * phi ^ N) N
      = covarianceCocycle (fun N => b * phi ^ N) N) :=
  ⟨cocycle_constant_phi, cocycle_base_independent⟩

end D0.VNext2.CanonicalDiracCovariance
