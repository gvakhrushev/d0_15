import D0.Core.Phi

/-!
# D0-ALPHA-ZETA-RESIDUE-001 — spectral zeta of the edge operator → α (finite moments)

Python certificate: `04_CERTIFICATES/vp_zeta_residue_alpha.py`.

The intended 1-skeleton (edge) feedback model of the scene `K(9,11,13)` uses
`F_E = φ⁻² · I₃₅₉ − φ⁻⁵ · |ω₀⟩⟨ω₀|` (357+1 spectrum: `φ⁻²` with multiplicity 358 and
the single seam eigenvalue `φ⁻² − φ⁻⁵`).  Its spectral zeta
`ζ_E(s) = Σ_k μ_k^{-s}` carries the electromagnetic data at integer moments:

  * `ζ_E(0)  = 359 = |E|`            — the topological capacity (edge count),
  * `ζ_E(-1) = 359·φ⁻² − φ⁻⁵`        — exactly `α_top⁻¹`,

The definitions below supply that scalar expression and prove its two finite
identities. This module does not construct the operator `F_E`, its spectrum,
or a map equating its matrix trace with `zetaEdge (-1)`. The seam relation
`φ⁻⁵ = ξ₅` is proved separately (`D0.Claims.Xi5TorusDefect`).

HONEST scope (mirrors the cert): the scene is FINITE, so `ζ_E` is an entire finite
sum with NO dimension pole — `α_top⁻¹` is the proposed `s = -1` *moment*, not a
residue.  The full "residue at the dimension pole" route (GOLDEN THE 15.4.2) needs
the profinite/archive limit and stays a theorem-target; this module proves only the
scalar finite-moment identities. The operator-to-scalar trace binding remains
an independent obligation.
-/

namespace D0.Spectral

open D0

/-- Bulk edge eigenvalue `φ⁻²` (multiplicity 358). -/
noncomputable def edgeBulk : ℝ := phi ^ (-2 : ℤ)

/-- Seam edge eigenvalue `φ⁻² − φ⁻⁵` (the single ω₀ edge). -/
noncomputable def edgeSeam : ℝ := phi ^ (-2 : ℤ) - phi ^ (-5 : ℤ)

/-- Scalar expression prescribed for the edge spectral zeta. -/
noncomputable def zetaEdge (s : ℤ) : ℝ := 358 * edgeBulk ^ (-s) + edgeSeam ^ (-s)

/-- The topological writing of `α⁻¹`: `359·φ⁻² − φ⁻⁵`. -/
noncomputable def alphaTopInv : ℝ := 359 * phi ^ (-2 : ℤ) - phi ^ (-5 : ℤ)

/-- The prescribed scalar expression takes value 359 at `s = 0`. -/
theorem zetaEdge_zero : zetaEdge 0 = 359 := by
  simp only [zetaEdge, neg_zero, zpow_zero]; norm_num

/-- The prescribed scalar `s = -1` expression equals `α_top⁻¹`. -/
theorem zetaEdge_neg_one : zetaEdge (-1) = alphaTopInv := by
  have h : (-(-1) : ℤ) = 1 := by ring
  simp only [zetaEdge, h, zpow_one, edgeBulk, edgeSeam, alphaTopInv]
  ring

/-- **D0-ALPHA-ZETA-RESIDUE-001 (scalar finite moments).** The defined scalar
expression takes the displayed values at `s = 0` and `s = -1`. -/
theorem zeta_residue_alpha_finite :
    zetaEdge 0 = 359 ∧ zetaEdge (-1) = alphaTopInv :=
  ⟨zetaEdge_zero, zetaEdge_neg_one⟩

end D0.Spectral
