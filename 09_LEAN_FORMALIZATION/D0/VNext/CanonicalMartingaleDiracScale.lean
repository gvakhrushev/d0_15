import D0.VNext.AFMartingaleDiracScaleNoGo
import D0.Spectral.CanonicalRefinementScaleFlow
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001 — the canonical (internally-sourced) Dirac scale IS φ^N

Companion to `D0-VNEXT-MARTINGALE-DIRAC-OWNER-001` (Outcome C). That NO-GO shows the martingale-Dirac
scale is not forced **by the AF axioms alone** — Christensen–Ivan permit *any* increasing `λ_N` (e.g.
`2^N`). This is true and unchanged. What the Outcome-C statement did NOT do is cross-reference the
already-Lean-proved `D0-PERRON-SCALE-FLOW-OWNER-001`: **every internally-defined refinement scale of the
golden Bratteli tower has step ratio exactly φ**. A martingale Dirac whose scale is *internally sourced*
(ratio inherited from the tower's own refinement flow) therefore has `λ_{N+1}/λ_N = φ` for all `N`, which
forces `λ_N = λ_0 · φ^N`. The rival `2^N` has step ratio `2 ≠ φ`, so it is admissible-but-external: it
carries an imported scale the Perron flow forbids. Hence, in the canonical class, the scale is **unique up
to the free dimensionless `λ_0`** — the standard overall-scale freedom of any spectral triple, not a second
D0 primitive. This does not contradict Outcome C; it *localizes* it: the residual freedom is external
scale import, not an internal degree of freedom.
-/

namespace D0.VNext.CanonicalMartingaleDiracScale

open D0 D0.Spectral.CanonicalRefinementScaleFlow
open D0.VNext.AFMartingaleDiracScaleNoGo (phi_lt_two one_lt_phi)

/-- A scale law `λ : ℕ → ℝ` is **internally sourced** iff its step ratio equals the tower's forced
Perron ratio φ at every level (per `D0-PERRON-SCALE-FLOW-OWNER-001`). -/
def InternallySourced (lam : ℕ → ℝ) : Prop := ∀ N : ℕ, lam (N + 1) / lam N = phi

/-- The φ-ladder `λ_N = λ_0 · φ^N` is internally sourced for any nonzero base `λ_0`. -/
theorem phiLadder_internallySourced (lam0 : ℝ) (h0 : lam0 ≠ 0) :
    InternallySourced (fun N => lam0 * phi ^ N) := by
  intro N
  have hp : phi ^ N ≠ 0 := pow_ne_zero N (ne_of_gt phi_pos)
  field_simp
  ring

/-- **The rival `2^N` is NOT internally sourced**: its step ratio is `2 ≠ φ`. -/
theorem scaleTwo_not_internallySourced : ¬ InternallySourced (fun N => (2 : ℝ) ^ N) := by
  intro h
  have h0 := h 0
  simp only [pow_zero] at h0
  -- h0 : 2 / 1 = phi, i.e. phi = 2, contradicting phi < 2
  have : phi = 2 := by rw [← h0]; norm_num
  exact absurd this (ne_of_lt phi_lt_two)

/-- **Canonical scale forcing.** Any internally-sourced scale `λ` with `λ 0 ≠ 0` satisfies
`λ N = λ 0 · φ^N` for all `N`: the internal source pins the whole ladder from its base. -/
theorem internallySourced_forces_phiLadder
    (lam : ℕ → ℝ) (hsrc : InternallySourced lam) (hne : ∀ N, lam N ≠ 0) :
    ∀ N, lam N = lam 0 * phi ^ N := by
  intro N
  induction N with
  | zero => simp
  | succ k ih =>
      have hk := hsrc k                       -- lam (k+1) / lam k = phi
      have hlk : lam k ≠ 0 := hne k
      have : lam (k + 1) = phi * lam k := by
        field_simp at hk ⊢
        linarith [hk]
      rw [this, ih, pow_succ]; ring

/-- **D0-VNEXT-MARTINGALE-DIRAC-CANONICAL-SCALE-OWNER-001.** Packaging: (1) the φ-ladder is internally
sourced; (2) `2^N` is not; (3) every internally-sourced scale is exactly the φ-ladder over its base.
So the canonical martingale-Dirac scale is unique up to the free dimensionless base `λ_0`. -/
theorem canonical_martingale_dirac_scale_owner :
    (InternallySourced (fun N => (1 : ℝ) * phi ^ N))
    ∧ (¬ InternallySourced (fun N => (2 : ℝ) ^ N))
    ∧ (∀ lam : ℕ → ℝ, InternallySourced lam → (∀ N, lam N ≠ 0) →
        ∀ N, lam N = lam 0 * phi ^ N) :=
  ⟨phiLadder_internallySourced 1 one_ne_zero,
   scaleTwo_not_internallySourced,
   internallySourced_forces_phiLadder⟩

end D0.VNext.CanonicalMartingaleDiracScale
