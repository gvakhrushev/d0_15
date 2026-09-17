import D0.Extensions.X5.Base
import D0.Spectral.AlphaAnalyticFormalismBoundary
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-X5-ALPHA-BOUNDARY-001 — alpha is outside the five contracts (Section 9)

The alpha analytic residue is explicitly OUTSIDE the five D0-X5 primitive contracts. Five separated layers:
internal (`μ₁,μ₂,α_alg,Δα`), candidate profinite carrier, ordinary log-Cesàro asymptotic, external
Dixmier/Wodzicki formalism, empirical comparison. D0-X5 does NOT solve the residue: the `a=3` candidate's
ordinary log-Cesàro `1/(3·log φ) ≠ μ₂` (external Lindemann, never CORE). No cross-contamination: alpha consumes
no D0-X5 contract slot (empty dependency).
-/

namespace D0.Extensions.X5.Alpha

open D0.Spectral

/-- Alpha consumes NO D0-X5 contract slot (empty dependency = present-core-relative, separate line). -/
theorem alpha_no_x5_dependency : D0.Extensions.X5.presentCoreDeps = ([] : D0.Extensions.X5.Dependencies) := rfl

/-- **Alpha boundary (terminal A3).** The `a=3` candidate ordinary log-Cesàro `1/(3·log φ) ≠ μ₂` (class-scoped,
external Lindemann bridge); D0-X5 does not produce an internal residue realization. -/
theorem alpha_outside_x5 (hLW : LindemannLnPhi) :
    (1 : ℝ) / (3 * Real.log D0.phi) ≠ (12288 / 5 : ℝ) :=
  D0.Spectral.AlphaAnalyticFormalismBoundary.alpha_candidate_class_scoped hLW

end D0.Extensions.X5.Alpha
