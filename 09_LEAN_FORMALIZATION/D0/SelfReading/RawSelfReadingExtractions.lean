import D0.SelfReading.RawSceneGraph
import D0.Extensions.RepresentationReadoutExtension
import D0.Extensions.SceneHistoryRefinementExtension
import D0.Extensions.LeptonSelectorExtension
import D0.Extensions.ArchiveCoordinateExtension
import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-RAW-SELF-READING-EXTRACTIONS-001 — Track II terminals (against the raw S₃ functor)

Run against the raw partial functor. For each front the FORCED part is a raw graph invariant and the DISPUTED
part remains a two-completion (cite the prior post-core owners). Terminals: II-A grading → **G2**, II-B
refinement/CMB → **C4** (no forced window), II-C lepton → **L3** (swap-invariant), II-D archive → **P3** (no
common sector in the typed diagram class).
-/

namespace D0.SelfReading.RawSelfReadingExtractions

open D0 D0.SelfReading.RawSceneGraph

/-- **II-A grading (G2).** Forced: commutant 12 (raw). Disputed: neutral-current `8 ≠ 12` (two gradings). -/
theorem extraction_grading_G2 :
    commutantDim = 12 ∧ D0.Extensions.RepresentationReadoutExtension.ncCount 2 1 ≠
      D0.Extensions.RepresentationReadoutExtension.ncCount 3 0 :=
  ⟨commutant_dim_raw, D0.Extensions.RepresentationReadoutExtension.nc_divergent⟩

/-- **II-B refinement (C4).** Forced: no-`φ³` (min-successor 19). Disputed: refinement carrier `15708 ≠ 14990`
(no forced smoothing window). -/
theorem extraction_refinement_C4 :
    phi ^ 3 < (D0.Extensions.SceneHistoryRefinementExtension.minSuccessor : ℝ) ∧ (15708 : ℕ) ≠ 14990 :=
  ⟨D0.Extensions.SceneHistoryRefinementExtension.path_perron_above_phi3,
    D0.Extensions.SceneHistoryRefinementExtension.refinement_two_completion⟩

/-- **II-C lepton (L3).** Forced: orbit exponents `1/4 ≠ 1/3`. Disputed: swap-invariant (`2 orbits < 3 gen`). -/
theorem extraction_lepton_L3 :
    (1 / 4 : ℚ) ≠ 1 / 3 ∧ D0.Extensions.LeptonSelectorExtension.orbitSizes.length <
      D0.Extensions.LeptonSelectorExtension.numGenerations :=
  ⟨D0.Extensions.LeptonSelectorExtension.orbit_exponents_distinct,
    D0.Extensions.LeptonSelectorExtension.orbits_fewer_than_generations⟩

/-- **II-D archive (P3).** Forced: window `359/160` (no common sector). Disputed: coordinate `φ−1 ≠ 1`. -/
theorem extraction_archive_P3 :
    (3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160 ∧ phi - 1 ≠ 1 :=
  ⟨D0.Extensions.ArchiveCoordinateExtension.window_product,
    D0.Extensions.ArchiveCoordinateExtension.coordinate_cocycle_divergent⟩

end D0.SelfReading.RawSelfReadingExtractions
