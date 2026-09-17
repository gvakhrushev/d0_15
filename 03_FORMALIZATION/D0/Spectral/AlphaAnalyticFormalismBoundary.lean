import D0.Spectral.AlphaLogCesaroMeasurability
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-ALPHA-ANALYTIC-FORMALISM-BOUNDARY-001 — Section 5 (separate analytic layer)

The alpha analytic residue is a SEPARATE four-layer problem, not part of the self-reading functor decision:
- internal: `μ₁, μ₂, α_alg, Δα` exact (CORE);
- profinite construction: a singular-value operator and its ORDINARY logarithmic asymptotic;
- external formalism: a Dixmier/Wodzicki/spectral-triple residue reading (passport);
- empirical comparison: an `α` measurement passport.

PERMITTED (with its candidate class): *this* `a=3` candidate tower has an ordinary log-Cesàro coefficient
`1/(3·log φ) ≠ μ₂ = 12288/5`. This is conditional on `ASSUMP-LINDEMANN-LNPHI` (transcendence of `log φ`),
typed as a STANDARD external mathematical theorem, never CORE. FORBIDDEN (no full classification exists): "no
future profinite realization can produce `μ₂`". This module states only the permitted, class-scoped fact.
-/

namespace D0.Spectral.AlphaAnalyticFormalismBoundary

open D0 D0.Spectral

/-- **D0-ALPHA-ANALYTIC-FORMALISM-BOUNDARY-001.** The specific `a=3` candidate tower has ordinary log-Cesàro
coefficient `1/(3·log φ) ≠ μ₂` (class-scoped, conditional on the external transcendence assumption). The
positive residue realization stays an external Dixmier/Wodzicki passport; no universal "no μ₂ ever" claim. -/
theorem alpha_candidate_class_scoped (hLW : LindemannLnPhi) :
    (1 : ℝ) / (3 * Real.log phi) ≠ (12288 / 5 : ℝ) :=
  D0.Spectral.AlphaLogCesaroMeasurability.alpha_log_cesaro_ne_mu2 hLW

end D0.Spectral.AlphaAnalyticFormalismBoundary
