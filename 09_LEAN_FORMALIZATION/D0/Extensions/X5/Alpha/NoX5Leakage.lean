import D0.Extensions.X5.Base
import D0.Spectral.AlphaAnalyticFormalismBoundary
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-X5-ALPHA-NOLEAKAGE-001 — alpha stays outside X5 (Section 9)

No X5 contract modifies or claims alpha closure. Alpha keeps its five-layer separation (internal seam /
candidate profinite carrier / ordinary log-Cesàro / external Dixmier-Wodzicki / empirical). The `a=3` candidate
ordinary log-Cesàro `1/(3·log φ) ≠ μ₂` is conditional on the external Lindemann assumption, never present-core,
and consumes NO X5 contract slot (empty dependency).
-/

namespace D0.Extensions.X5.Alpha

open D0.Spectral

/-- Alpha consumes no X5 contract slot (no leakage). -/
theorem alpha_no_x5_slot : D0.Extensions.X5.presentCoreDeps = ([] : D0.Extensions.X5.Dependencies) := rfl

/-- **D0-X5-ALPHA-NOLEAKAGE-001.** The `a=3` candidate log-Cesàro `≠ μ₂` (external Lindemann), and alpha uses no
X5 slot — no cross-contamination, no bridge-as-core. -/
theorem alpha_no_leakage (hLW : LindemannLnPhi) :
    (1 : ℝ) / (3 * Real.log D0.phi) ≠ (12288 / 5 : ℝ) ∧
      D0.Extensions.X5.presentCoreDeps = ([] : D0.Extensions.X5.Dependencies) :=
  ⟨D0.Spectral.AlphaAnalyticFormalismBoundary.alpha_candidate_class_scoped hLW, rfl⟩

end D0.Extensions.X5.Alpha
