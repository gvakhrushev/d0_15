import Mathlib.Data.Matrix.Basic
import Mathlib.Tactic
import D0.Core.Phi
import D0.Algebra.FibonacciPerronTraceCanonicity
import D0.Algebra.FibonacciAFTower
import D0.Spectral.CanonicalRefinementScaleFlow

set_option linter.unusedSimpArgs false

/-!
# D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001 — incidence M_φ RECOVERED from the cylinder language

The golden cylinder language is the golden-mean shift of finite type: words over `{0,1}` forbidding the
factor `11`. Its refinement/Bratteli incidence is therefore **derived, not inserted**: the allowed-word
rule `goldenAllowed i j = (0 if i=j=1 else 1)` reproduces `M_φ = !![1,1;1,0]`. The Perron eigenvalue is
`φ` (`M_φ² = M_φ + 1`, charpoly `x²−x−1`), and the level dimensions grow as Fibonacci. The explicit
positive left-Perron vector has component ratio `φ`; uniqueness of the normalized positive Perron
profile is proved by the separate `D0-FIBONACCI-PERRON-PROFILE-CANONICITY-001` theorem and applied
below. Neither result proves uniqueness of all compatible AF traces on the inductive limit. That
stronger trace statement remains under the existing owner and its research/formalization boundary.
-/

namespace D0.Geometry.FibonacciBratteliRefinement

open Matrix D0

/-- The golden cylinder language rule: a transition `i → j` is allowed unless it is the forbidden `11`. -/
def goldenAllowed (i j : Fin 2) : ℤ := if i = 1 ∧ j = 1 then 0 else 1

/-- The golden incidence matrix. -/
def Mphi : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]

/-- **The incidence matrix is RECOVERED from the allowed-word rule** (not inserted): `M_φ` equals the
adjacency of the golden-mean SFT (forbid `11`). -/
theorem incidence_recovered_from_language :
    Mphi = Matrix.of (fun i j => goldenAllowed i j) := by
  decide

/-- **The Perron eigenvalue is `φ`**: `M_φ² = M_φ + 1` (charpoly `x²−x−1`). -/
theorem perron_eigenvalue_golden : Mphi ^ 2 = Mphi + 1 := by decide

/-- **Fibonacci level growth**: applying `M_φ` to the uniform level-0 vector gives `(2,1)` (then
`3,2 → 5,3 → …`), the Fibonacci dimensions of the refinement tower. -/
theorem fibonacci_level_growth :
    Mphi.mulVec ![1, 1] 0 = 2 ∧ Mphi.mulVec ![1, 1] 1 = 1 := by
  constructor <;> simp [Mphi, Matrix.mulVec, dotProduct, Fin.sum_univ_two]

theorem phi_pos : 0 < phi := by unfold phi; positivity

/-- **An explicit positive left-Perron vector has ratio `φ`**: `w = (φ, 1)` satisfies
`wᵀ M_φ = φ wᵀ` (`w₀ = φ·w₁` and `w₀ + w₁ = φ·w₀`). This is a vector identity, not a normalized
state or a uniqueness theorem for AF traces. -/
theorem golden_bratteli_trace_ratio :
    ∃ w : Fin 2 → ℝ, 0 < w 0 ∧ 0 < w 1 ∧ w 0 = phi * w 1 ∧ w 0 + w 1 = phi * w 0 := by
  refine ⟨![phi, 1], phi_pos, one_pos, by simp, ?_⟩
  simp only [Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons]
  have := phi_sq; nlinarith [this]

/-- Apply the separate normalized positive eigenprofile result to the Fibonacci incidence profile.
This proves uniqueness of the two-component profile, not uniqueness of every compatible AF trace. -/
theorem fibonacci_bratteli_profile_application :
    D0.Foundation.M1Forced
      D0.Algebra.FibonacciPerronTraceCanonicity.CanonicalPerronProfile
      (phi⁻¹, phi⁻¹ ^ 2) :=
  D0.Algebra.FibonacciPerronTraceCanonicity.perron_profile_m1_forced

/-- **D0-BRATTELI-FIBONACCI-REFINEMENT-OWNER-001 (formalized finite incidence slice).** The golden
cylinder language determines the finite incidence `M_φ` (recovered from the forbid-`11` rule), with
quadratic identity and Fibonacci growth. It also constructs an explicit positive left-Perron vector;
uniqueness of the normalized positive eigenprofile is applied in `fibonacci_bratteli_profile_application`.
The owner does not thereby prove uniqueness of every compatible AF trace on an inductive limit. -/
theorem fibonacci_bratteli_refinement_owner :
    Mphi = Matrix.of (fun i j => goldenAllowed i j)
      ∧ Mphi ^ 2 = Mphi + 1
      ∧ (∃ w : Fin 2 → ℝ, 0 < w 0 ∧ 0 < w 1 ∧ w 0 = phi * w 1 ∧ w 0 + w 1 = phi * w 0) :=
  ⟨incidence_recovered_from_language, perron_eigenvalue_golden, golden_bratteli_trace_ratio⟩

/-- **D0-CANONICAL-RENORMALIZATION-SPECTRAL-TOWER-001 (finite composition).** Bind the recovered
incidence, the actual all-level finite-real refinement functional, the normalized Perron profile, and
the dimensionless scale step into one checked application. The functional is not asserted here to be a
positive state on a complex AF limit. -/
theorem finite_renormalization_refinement_composition :
    Mphi = Matrix.of (fun i j => goldenAllowed i j)
      ∧ (∀ n : ℕ, ∀ z : D0.Algebra.FibonacciAFTower.FibonacciAFLevel n,
          D0.Algebra.FibonacciAFTower.fibonacciAFTrace (n + 1)
              (D0.Algebra.FibonacciAFTower.fibonacciAFRefinementHom n z) =
            D0.Algebra.FibonacciAFTower.fibonacciAFTrace n z)
      ∧ (∀ n : ℕ,
          D0.Spectral.CanonicalRefinementScaleFlow.Lambda (n + 1) /
              D0.Spectral.CanonicalRefinementScaleFlow.Lambda n = phi)
      ∧ D0.Foundation.M1Forced
          D0.Algebra.FibonacciPerronTraceCanonicity.CanonicalPerronProfile
          (phi⁻¹, phi⁻¹ ^ 2) := by
  refine ⟨incidence_recovered_from_language, ?_, ?_, fibonacci_bratteli_profile_application⟩
  · intro n z
    exact D0.Algebra.FibonacciAFTower.fibonacciAFRefinement_trace_preserving n z
  · exact D0.Spectral.CanonicalRefinementScaleFlow.scale_ratio_forced

end D0.Geometry.FibonacciBratteliRefinement
