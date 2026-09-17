import D0.Interface.Poisson
import D0.Interface.MatterAnomaly

namespace D0.Matter

structure MatterArchiveLocalization (n : Nat) (R : MatterRep) where
  source : archivePhaseIndex n → ℝ
  total_source_eq_anomaly_or_charge :
    (∑ i, source i) = R.anomalySum

theorem localized_matter_source_neutral_if_anomaly_free
  (n : Nat)
  (R : MatterRep)
  (loc : MatterArchiveLocalization n R)
  (h : R.anomalySum = 0) :
  NeutralSource loc.source := by
  unfold NeutralSource
  rw [loc.total_source_eq_anomaly_or_charge, h]
  simp

noncomputable def canonicalMatterLocalization (n : Nat) (R : MatterRep) :
    MatterArchiveLocalization n R :=
  { source := fun _ => (R.anomalySum : ℝ) / (archiveFibers n : ℝ),
    total_source_eq_anomaly_or_charge := by
      simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin]
      have h_fibers : 0 < archiveFibers n := by unfold archiveFibers; omega
      have h_ne : (archiveFibers n : ℝ) ≠ 0 := Nat.cast_pos.mpr h_fibers |>.ne'
      rw [nsmul_eq_mul]
      field_simp [h_ne]
  }

theorem canonical_localization_is_neutral_if_anomaly_free (n : Nat) (R : MatterRep)
    (h : R.anomalySum = 0) :
    NeutralSource (canonicalMatterLocalization n R).source :=
  localized_matter_source_neutral_if_anomaly_free n R (canonicalMatterLocalization n R) h

theorem canonical_localization_source_val (n : Nat) (R : MatterRep)
    (h : R.anomalySum = 0) :
    ∀ i : archivePhaseIndex n, (canonicalMatterLocalization n R).source i = 0 := by
  intro i
  unfold canonicalMatterLocalization
  simp [h]

end D0.Matter
