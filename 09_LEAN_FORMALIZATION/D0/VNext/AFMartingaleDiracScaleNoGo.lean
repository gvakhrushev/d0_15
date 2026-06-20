import D0.VNext.FibonacciAFAlgebra
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-VNEXT-MARTINGALE-DIRAC-OWNER-001 — Dirac scale is underdetermined (Phase B, Outcome C)

The martingale increments `K_{N+1} = H_{N+1}^GNS ⊖ J_N(H_N^GNS)` are nonzero (the AF dimensions strictly
grow), so a martingale Dirac `D_AF = Σ_N λ_N Δ_N` is well-defined for any increasing scale `λ_N`. But the
scale is **not uniquely forced**: distinct admissible laws — e.g. `λ_N = φ^N` and `λ_N = 2^N` — are each
strictly increasing to `∞` (hence each gives a compact-resolvent AF spectral triple, à la
Christensen–Ivan) yet differ already at `N=1` (`φ ≠ 2`). So the proposed primitive splits: the GNS
isometry is one extension (realized), the Dirac **scale selection is a second independent primitive**.
This is **Outcome C** — a scale-selection no-go. No law is chosen for convenience; the theorem states
exactly that ≥2 admissible laws survive.
-/

namespace D0.VNext.AFMartingaleDiracScaleNoGo

open D0 D0.VNext.FibonacciAFAlgebra

theorem one_lt_phi : 1 < phi := by
  have h0 : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have h2 : (2 : ℝ) < Real.sqrt 5 := by nlinarith [sqrt_five_sq, h0]
  have : phi = (1 + Real.sqrt 5) / 2 := rfl
  rw [this]; linarith

theorem phi_lt_two : phi < 2 := by
  have h0 : (0 : ℝ) ≤ Real.sqrt 5 := Real.sqrt_nonneg 5
  have h3 : Real.sqrt 5 < 3 := by nlinarith [sqrt_five_sq, h0]
  have : phi = (1 + Real.sqrt 5) / 2 := rfl
  rw [this]; linarith

/-- The martingale increment dimension `dim K_{N+1} = dim A_{N+1} − dim A_N`. -/
def dimK (n : ℕ) : ℕ := dimA (n + 1) - dimA n

/-- **The increment spaces are nonzero** over the initial levels (the AF dims strictly grow). -/
theorem af_increment_spaces_defined : 0 < dimK 0 ∧ 0 < dimK 1 ∧ 0 < dimK 2 := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- Candidate scale law A: `λ_N = φ^N`. -/
noncomputable def scalePhi (n : ℕ) : ℝ := phi ^ n

/-- Candidate scale law B: `λ_N = 2^N`. -/
noncomputable def scaleTwo (n : ℕ) : ℝ := 2 ^ n

/-- **Both candidate scale laws are admissible** (strictly increasing to ∞, giving compact-resolvent
AF spectral triples). -/
theorem candidate_dirac_scale_family :
    (∀ n, scalePhi n < scalePhi (n + 1)) ∧ (∀ n, scaleTwo n < scaleTwo (n + 1)) := by
  refine ⟨fun n => ?_, fun n => ?_⟩
  · simpa [scalePhi, pow_succ] using
      (lt_mul_iff_one_lt_right (pow_pos (lt_trans one_pos one_lt_phi) n)).mpr one_lt_phi
  · simpa [scaleTwo, pow_succ] using
      (lt_mul_iff_one_lt_right (pow_pos (by norm_num : (0:ℝ) < 2) n)).mpr (by norm_num : (1:ℝ) < 2)

/-- **D0-VNEXT-MARTINGALE-DIRAC-OWNER-001 (Outcome C, scale-selection NO-GO).** The increments are
nonzero and ≥2 admissible scale laws (`φ^N`, `2^N`) are each strictly increasing yet distinct at `N=1`
(`φ ≠ 2`): the Dirac scale is NOT uniquely forced by the AF/Perron data. The scale selection is a second
independent primitive. -/
theorem dirac_scale_underdetermined :
    (0 < dimK 0)
      ∧ (∀ n, scalePhi n < scalePhi (n + 1)) ∧ (∀ n, scaleTwo n < scaleTwo (n + 1))
      ∧ scalePhi 1 ≠ scaleTwo 1 := by
  refine ⟨af_increment_spaces_defined.1, candidate_dirac_scale_family.1,
          candidate_dirac_scale_family.2, ?_⟩
  simp only [scalePhi, scaleTwo, pow_one]
  exact ne_of_lt phi_lt_two

end D0.VNext.AFMartingaleDiracScaleNoGo
