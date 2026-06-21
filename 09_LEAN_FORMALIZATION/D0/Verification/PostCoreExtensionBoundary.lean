import D0.Extensions.RepresentationReadoutExtension
import D0.Extensions.SceneHistoryRefinementExtension
import D0.Extensions.ArchiveCoordinateExtension
import D0.Extensions.LeptonSelectorExtension
import D0.Extensions.AlphaResidueExtension
import D0.Extensions.ExtensionMinimality
import D0.Spectral.DeltaAlphaResidueBlocked

/-!
# D0-POSTCORE-EXTENSION-BOUNDARY-001 — capstone (Section 1)

Conjoins the five beyond-present-core extension outcomes: E1, E2, E3, E4 are TWO-COMPLETION-NOGO (each with
its own divergent observable), and E5 is EXTERNAL-PASSPORT (conditional on the cited Lindemann bridge). The
extension dependence graph has exactly two `a=3` exponent edges. No extension forces a unique completion from
admissible data alone; each remaining front is one named typed primitive (or external passport) away.
-/

namespace D0.Verification.PostCoreExtensionBoundary

open D0 D0.Spectral

/-- **D0-POSTCORE-EXTENSION-BOUNDARY-001.** The five extension boundaries: E1 neutral-current divergence
(`8 ≠ 12`), E2 `φ³ <` min-successor 19, E3 coordinate-cocycle divergence (`φ − 1 ≠ 1`), E4 orbit exponents
distinct (`1/4 ≠ 1/3`), E5 internal residue `≠ μ₂` (external passport), and exactly two extension proof-edges. -/
theorem postcore_extension_boundary (hLW : LindemannLnPhi) :
    (D0.Extensions.RepresentationReadoutExtension.ncCount 2 1 ≠
        D0.Extensions.RepresentationReadoutExtension.ncCount 3 0) ∧
      (phi ^ 3 < (D0.Extensions.SceneHistoryRefinementExtension.minSuccessor : ℝ)) ∧
      (phi - 1 ≠ 1) ∧
      ((1 / 4 : ℚ) ≠ 1 / 3) ∧
      ((1 : ℝ) / (3 * Real.log phi) ≠ (12288 / 5 : ℝ)) ∧
      (D0.Extensions.ExtensionMinimality.edgeCount = 2) :=
  ⟨D0.Extensions.RepresentationReadoutExtension.nc_divergent,
    D0.Extensions.SceneHistoryRefinementExtension.path_perron_above_phi3,
    D0.Extensions.ArchiveCoordinateExtension.coordinate_cocycle_divergent,
    D0.Extensions.LeptonSelectorExtension.orbit_exponents_distinct,
    D0.Extensions.AlphaResidueExtension.alpha_residue_external_passport hLW,
    D0.Extensions.ExtensionMinimality.two_exponent_edges⟩

end D0.Verification.PostCoreExtensionBoundary
