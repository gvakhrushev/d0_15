import D0.Core.Phi

/-!
# D0-ALPHA-ZETA-RESIDUE-001 — spectral zeta of the edge operator → α (finite moments)

Python certificate: `05_CERTS/vp_zeta_residue_alpha.py`.

The 1-skeleton (edge) feedback operator of the scene `K(9,11,13)` is
`F_E = φ⁻² · I₃₅₉ − φ⁻⁵ · |ω₀⟩⟨ω₀|` (357+1 spectrum: `φ⁻²` with multiplicity 358 and
the single seam eigenvalue `φ⁻² − φ⁻⁵`).  Its spectral zeta
`ζ_E(s) = Σ_k μ_k^{-s}` carries the electromagnetic data at integer moments:

  * `ζ_E(0)  = 359 = |E|`            — the topological capacity (edge count),
  * `ζ_E(-1) = 359·φ⁻² − φ⁻⁵`        — exactly `α_top⁻¹`,

so ONE zeta function produces both the capacity `359` (at `s = 0`) and the
fine-structure value `α_top⁻¹` (at `s = -1`), with the seam term `φ⁻⁵ = ξ₅` proved
separately (`D0.Claims.Xi5TorusDefect`: `φ⁵ = 11 + φ⁻⁵`).

HONEST scope (mirrors the cert): the scene is FINITE, so `ζ_E` is an entire finite
sum with NO dimension pole — `α_top⁻¹` is the `s = -1` *moment* (a trace), not a
residue.  The full "residue at the dimension pole" route (GOLDEN THE 15.4.2) needs
the profinite/archive limit and stays a theorem-target; this module proves only the
finite-moment identities, which are real (trace = sum of eigenvalues), not a
restatement.
-/

namespace D0.Spectral

open D0

/-- Bulk edge eigenvalue `φ⁻²` (multiplicity 358). -/
noncomputable def edgeBulk : ℝ := phi ^ (-2 : ℤ)

/-- Seam edge eigenvalue `φ⁻² − φ⁻⁵` (the single ω₀ edge). -/
noncomputable def edgeSeam : ℝ := phi ^ (-2 : ℤ) - phi ^ (-5 : ℤ)

/-- Spectral zeta of the edge operator: `ζ_E(s) = 358·μ_bulk^{-s} + μ_seam^{-s}`. -/
noncomputable def zetaEdge (s : ℤ) : ℝ := 358 * edgeBulk ^ (-s) + edgeSeam ^ (-s)

/-- The topological writing of `α⁻¹`: `359·φ⁻² − φ⁻⁵`. -/
noncomputable def alphaTopInv : ℝ := 359 * phi ^ (-2 : ℤ) - phi ^ (-5 : ℤ)

/-- `ζ_E(0) = 359 = |E|`: at `s = 0` the zeta counts the edge dimension (capacity). -/
theorem zetaEdge_zero : zetaEdge 0 = 359 := by
  simp only [zetaEdge, neg_zero, zpow_zero]; norm_num

/-- `ζ_E(-1) = 359·φ⁻² − φ⁻⁵ = α_top⁻¹`: the `s = -1` moment is the edge trace, i.e.
the fine-structure value. (`358·φ⁻² + (φ⁻² − φ⁻⁵) = 359·φ⁻² − φ⁻⁵`.) -/
theorem zetaEdge_neg_one : zetaEdge (-1) = alphaTopInv := by
  have h : (-(-1) : ℤ) = 1 := by ring
  simp only [zetaEdge, h, zpow_one, edgeBulk, edgeSeam, alphaTopInv]
  ring

/-- **D0-ALPHA-ZETA-RESIDUE-001 (finite moments).** One spectral zeta of the edge
operator yields both the capacity `359` (at `s = 0`) and `α_top⁻¹` (at `s = -1`). -/
theorem zeta_residue_alpha_finite :
    zetaEdge 0 = 359 ∧ zetaEdge (-1) = alphaTopInv :=
  ⟨zetaEdge_zero, zetaEdge_neg_one⟩

end D0.Spectral
