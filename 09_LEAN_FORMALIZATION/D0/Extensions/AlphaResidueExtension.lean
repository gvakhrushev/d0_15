import D0.Spectral.AlphaLogCesaroMeasurability
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-POSTCORE-DIXMIER-WODZICKI-PASSPORT-001 — E5 (analytic residue extension)

The honest terminus is an EXTERNAL-PASSPORT, not an internal operator. The two admissible analytic functionals
applied to the SAME critical `a=3` operator diverge: the internal-measurable (ordinary log-Cesàro / Dixmier)
reading gives `1/(3·log φ)` — transcendental over ℚ by Lindemann (R5), hence never the rational moment
`μ₂ = 12288/5`; the external-Wodzicki reading (Connes trace theorem, an external spectral triple) is the only
route that reads `μ₂` as a residue. So no INTERNAL measurable trace realizes `μ₂`; the realization is the
external passport `D0-EXTERNAL-DIXMIER-WODZICKI-PASSPORT-001`. This module re-exports R5's no-go under the E5
framing (cites `D0-ALPHA-LOG-CESARO-MEASURABILITY-NOGO-001`; does not re-prove the transcendence).
-/

namespace D0.Extensions.AlphaResidueExtension

open D0 D0.Spectral

/-- **D0-POSTCORE-DIXMIER-WODZICKI-PASSPORT-001.** Under the cited Lindemann bridge, the internal ordinary
log-Cesàro residue `1/(3·log φ)` is never the rational moment `μ₂ = 12288/5`, so the residue realization is
the external Dixmier/Wodzicki passport, not an internal operator. -/
theorem alpha_residue_external_passport (hLW : LindemannLnPhi) :
    (1 : ℝ) / (3 * Real.log phi) ≠ (12288 / 5 : ℝ) :=
  D0.Spectral.AlphaLogCesaroMeasurability.alpha_log_cesaro_ne_mu2 hLW

end D0.Extensions.AlphaResidueExtension
