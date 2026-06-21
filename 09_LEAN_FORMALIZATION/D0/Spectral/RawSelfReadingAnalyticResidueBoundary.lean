import D0.Spectral.AlphaAnalyticFormalismBoundary
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-RAW-ALPHA-ANALYTIC-RESIDUE-BOUNDARY-001 — Track IV terminal (A3)

The alpha analytic residue stays a SEPARATE four-layer line. Terminal **A3**: only an external
Dixmier/Wodzicki passport is presently admissible — the `a=3` candidate's ordinary log-Cesàro coefficient
`1/(3·log φ) ≠ μ₂` (class-scoped, conditional on the external `ASSUMP-LINDEMANN-LNPHI`, never CORE). This is
NOT a full-class exhaustion (`A4`): no claim is made that no future profinite realization can produce `μ₂`.
-/

namespace D0.Spectral.RawSelfReadingAnalyticResidueBoundary

open D0.Spectral

/-- **Track IV terminal A3.** The `a=3` candidate ordinary log-Cesàro coefficient `1/(3·log φ) ≠ μ₂`
(class-scoped, external Lindemann); positive realization stays the external Dixmier/Wodzicki passport. -/
theorem raw_alpha_terminal_A3 (hLW : LindemannLnPhi) :
    (1 : ℝ) / (3 * Real.log D0.phi) ≠ (12288 / 5 : ℝ) :=
  D0.Spectral.AlphaAnalyticFormalismBoundary.alpha_candidate_class_scoped hLW

end D0.Spectral.RawSelfReadingAnalyticResidueBoundary
