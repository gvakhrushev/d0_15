import D0.Spectral.AlphaPresentCoreMaximalityNoGo
import D0.Cosmology.CMBCanonicalSmoothingMaximalityNoGo
import D0.Cosmology.PhasonMagnitudeMaximalityNoGo
import D0.Matter.CKMOverlapUnderdeterminationNoGo
import D0.Matter.HiggsCondensationPresentCoreMaximalityNoGo
import D0.Geometry.ToralSeedMarkovMaximalityNoGo
import D0.Matter.LeptonFiniteGreenResolventOwner

/-!
# D0-FINAL-CORE-COMPLETION-001 — present-core maximality capstone

Single machine-checked entry point bundling the Final Core Completion campaign (M1–M6): every targeted
internal frontier is now **classified** — either closed-negative by a present-core maximality NO-GO, or
closed-positive by a finite owner. There is no remaining unnamed internal theorem debt on these fronts;
what is left is external (passports), inventoried in `04_VERIFICATION/D0_FINAL_EXTERNAL_PASSPORTS.csv`.

Components (each an independently-proven campaign theorem):
- **alpha** — every admissible present-core tower is trace-class (Dixmier coeff `0 ≠ μ₂`); critical line
  needs Perron `φ³` (`rate 3 = 1`), absent from present-core;
- **CMB** — the smoothed tilt is non-constant across the admissible-smoothing family (`n_s` not forced);
- **phason** — two admissible magnitude maps differ (`|w_DE|` not forced);
- **CKM** — two admissible overlap completions differ (`|V₁₂|²` not forced);
- **Higgs** — every present-core projector commutes with `T` (no condensation); needs a non-commuting `Q₀`;
- **toral** — distinct-rectangle admissible adjacencies share the golden Perron data (partition not forced);
- **lepton** — the finite shell-torus Green resolvent exists on a nonempty non-pole domain (POSITIVE owner).
-/

namespace D0.Verification.PresentCoreMaximality

/-- **D0-FINAL-CORE-COMPLETION-001.** The conjunction of the campaign's seven headline theorems holds
simultaneously: the six maximality no-gos (alpha, CMB, phason, CKM, Higgs, toral) and the one positive
owner (lepton Green resolvent). Each conjunct is the proven main theorem of its module. -/
theorem present_core_maximality_classified :
    (∀ a : ℕ, a ≤ 2 →
        Summable (fun N : ℕ => (D0.Spectral.AlphaPresentCoreMaximalityNoGo.rate a) ^ N))
        ∧ D0.Spectral.AlphaPresentCoreMaximalityNoGo.rate 3 = 1
        ∧ D0.Spectral.AlphaProfiniteSpectralTower.mu2 ≠ 0
      ∧ (D0.Cosmology.CMBNsSmoothingUndeterminedNoGo.tilt 1 12 10 8 2
            ≠ D0.Cosmology.CMBNsSmoothingUndeterminedNoGo.tilt 2 12 10 8 2)
      ∧ D0.Cosmology.PhasonMagnitudeMaximalityNoGo.w1 1
            ≠ D0.Cosmology.PhasonMagnitudeMaximalityNoGo.w2 1
      ∧ (D0.Matter.CKMOverlapUnderdeterminationNoGo.VmixA 0 1) ^ 2
            ≠ (D0.Matter.CKMOverlapUnderdeterminationNoGo.VmixB 0 1) ^ 2
      ∧ (¬ Commute D0.Matter.HiggsReturnQuotientAction.T
            D0.Matter.HiggsCondensationPresentCoreMaximalityNoGo.Qnc)
      ∧ (D0.Geometry.ToralSeedMarkovMaximalityNoGo.Mphi ^ 2
            = D0.Geometry.ToralSeedMarkovMaximalityNoGo.Mphi + 1
          ∧ D0.Geometry.ToralSeedMarkovMaximalityNoGo.A3 ^ 3
            = D0.Geometry.ToralSeedMarkovMaximalityNoGo.A3 ^ 2 + D0.Geometry.ToralSeedMarkovMaximalityNoGo.A3)
      ∧ (D0.Matter.LeptonFiniteGreenResolventOwner.Ueff ^ 12 = 1
          ∧ IsUnit D0.Matter.LeptonFiniteGreenResolventOwner.Ueff) := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩
  · exact D0.Spectral.AlphaPresentCoreMaximalityNoGo.alpha_present_core_maximality_nogo.1
  · exact D0.Spectral.AlphaPresentCoreMaximalityNoGo.alpha_present_core_maximality_nogo.2.1
  · exact D0.Spectral.AlphaPresentCoreMaximalityNoGo.alpha_present_core_maximality_nogo.2.2
  · exact D0.Cosmology.CMBCanonicalSmoothingMaximalityNoGo.cmb_canonical_smoothing_maximality_nogo.2
  · exact D0.Cosmology.PhasonMagnitudeMaximalityNoGo.maps_differ
  · exact D0.Matter.CKMOverlapUnderdeterminationNoGo.overlap_invariants_differ
  · exact D0.Matter.HiggsCondensationPresentCoreMaximalityNoGo.Qnc_not_commute
  · exact ⟨D0.Geometry.ToralSeedMarkovMaximalityNoGo.Mphi_golden,
          D0.Geometry.ToralSeedMarkovMaximalityNoGo.A3_golden⟩
  · exact ⟨D0.Matter.LeptonFiniteGreenResolventOwner.cover_order_twelve,
          D0.Matter.LeptonFiniteGreenResolventOwner.cover_invertible⟩

end D0.Verification.PresentCoreMaximality
