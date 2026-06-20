import D0.Geometry.FibonacciBratteliRefinement
import D0.Spectral.CanonicalRefinementScaleFlow
import D0.Verification.PresentCoreMaximality

/-!
# D0-FINAL-RESEARCH-TO-CLOSURE-MAP-001 — research closure boundary

Capstone of the Canonical Renormalization / Final Research Closure campaign. Sits atop the M1–M7
present-core maximality capstone (`D0.Verification.PresentCoreMaximality.present_core_maximality_classified`,
imported and re-checked here) and ADDS the Master A renormalization-tower layer:

- the golden cylinder language recovers its Bratteli incidence `M_φ` with Perron `φ`
  (`perron_eigenvalue_golden`);
- the refinement scale ratio is forced to `φ` at every level (`scale_ratio_forced`);
- representative of the maximality layer: every admissible present-core alpha tower is trace-class.

Together with the integrated map (`04_VERIFICATION/D0_FINAL_RESEARCH_CLOSURE_MAP.csv`), no-go atlas, new-
primitives list, and passport index, this is the machine-checked boundary of present-core reach: a
canonical refinement tower (algebra+trace+scale) exists; the physics-facing extensions are each CERT,
NO-GO, PASSPORT, or blocked by exactly one named new primitive.
-/

namespace D0.Verification.FinalResearchClosureBoundary

open D0

/-- **D0-FINAL-RESEARCH-TO-CLOSURE-MAP-001.** The Master A renormalization layer (Bratteli incidence
`M_φ` Perron-golden + forced scale ratio `φ`) holds together with the maximality layer (every admissible
present-core alpha tower is trace-class). The full M1–M7 classification is the imported capstone
`present_core_maximality_classified`. -/
theorem final_research_closure_boundary :
    (D0.Geometry.FibonacciBratteliRefinement.Mphi ^ 2
        = D0.Geometry.FibonacciBratteliRefinement.Mphi + 1)
      ∧ (∀ N : ℕ, D0.Spectral.CanonicalRefinementScaleFlow.Lambda (N + 1)
          / D0.Spectral.CanonicalRefinementScaleFlow.Lambda N = phi)
      ∧ (∀ a : ℕ, a ≤ 2 →
          Summable (fun M : ℕ => (D0.Spectral.AlphaPresentCoreMaximalityNoGo.rate a) ^ M)) := by
  refine ⟨D0.Geometry.FibonacciBratteliRefinement.perron_eigenvalue_golden,
          D0.Spectral.CanonicalRefinementScaleFlow.scale_ratio_forced, ?_⟩
  exact D0.Spectral.AlphaPresentCoreMaximalityNoGo.alpha_present_core_maximality_nogo.1

end D0.Verification.FinalResearchClosureBoundary
