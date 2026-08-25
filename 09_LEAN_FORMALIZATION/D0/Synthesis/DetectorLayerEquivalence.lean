import D0.Foundation.CurrentDataFactorization
import D0.Synthesis.DetectorCatalogueFreedom

/-!
# Detector layer equivalence: catalogue-free = history-invariant = current-data comparison

There are now two independent descriptions of an instantaneous detector comparison:

1. `CatalogueFree` — invariant under changing an external orientation catalogue;
2. `HistoryInvariant` — invariant under changing the stored history coordinates of full
   observations.

Both are exactly comparisons on current data. This module packages the universal equivalences:

`CatalogueFree comparisons ≃ BareComparison Current`

`HistoryInvariant full comparisons ≃ CurrentComparison Current`

and therefore, for Boolean history,

`CatalogueFree comparisons ≃ HistoryInvariant full comparisons`.

This closes the mathematical detector/memory layer architecture. It does not by itself connect
the class to the repository's unique-answer `M1Forced` predicate; that exact seam is the separate
no-go `DetectorM1PredicateBoundary`.
-/

namespace D0.Synthesis.DetectorLayerEquivalence

open D0.Foundation.CurrentDataFactorization
open D0.Synthesis.DetectorCatalogueFreedom

/-- Carrier of catalogue-free detector comparisons. -/
abbrev CatalogueFreeCarrier (Current : Type*) :=
  {cmp : CatalogueComparison Current // CatalogueFree cmp}

/-- Carrier of history-invariant full comparisons. -/
abbrev HistoryInvariantCarrier (Current History : Type*) :=
  {cmp : FullComparison Current History // HistoryInvariant Current History cmp}

/-- Bare current-data comparisons are equivalent to catalogue-free comparisons. -/
def bareEquivCatalogueFree (Current : Type*) :
    BareComparison Current ≃ CatalogueFreeCarrier Current where
  toFun base := ⟨liftCat base, liftCat_catalogueFree base⟩
  invFun cmp := bareOf cmp.1
  left_inv := by
    intro base
    rfl
  right_inv := by
    intro cmp
    apply Subtype.ext
    exact (catalogueFree_factors cmp.1 cmp.2).symm

/-- Current-data comparisons are equivalent to history-invariant full comparisons whenever the
history type is inhabited. The inverse is independent of the chosen reference history. -/
noncomputable def currentEquivHistoryInvariant
    (Current History : Type*) [Nonempty History] :
    CurrentComparison Current ≃ HistoryInvariantCarrier Current History where
  toFun base := ⟨liftCurrent Current History base,
    liftCurrent_historyInvariant Current History base⟩
  invFun cmp :=
    descendAt Current History (Classical.choice ‹Nonempty History›) cmp.1
  left_inv := by
    intro base
    funext x y
    rfl
  right_inv := by
    intro cmp
    apply Subtype.ext
    exact lift_descendAt_eq Current History
      (Classical.choice ‹Nonempty History›) cmp.1 cmp.2

/-- **Canonical detector/memory layer equivalence.** On Boolean history, a comparison is
catalogue-free exactly when the corresponding full comparison is history-invariant; both are
canonically the same bare current-data comparison. -/
noncomputable def catalogueFreeEquivHistoryInvariant (Current : Type*) :
    CatalogueFreeCarrier Current ≃ HistoryInvariantCarrier Current Bool :=
  (bareEquivCatalogueFree Current).symm.trans
    (currentEquivHistoryInvariant Current Bool)

/-- The equivalence preserves the underlying bare current-data comparison. -/
theorem catalogueFreeEquivHistoryInvariant_bare (Current : Type*)
    (cmp : CatalogueFreeCarrier Current) :
    (currentEquivHistoryInvariant Current Bool).symm
        (catalogueFreeEquivHistoryInvariant Current cmp)
      = bareOf cmp.1 := by
  rfl

/-- Concrete positive controls: membership and value comparisons lie in the history-invariant
detector layer. -/
theorem membership_value_in_detector_layer :
    HistoryInvariant (Bool × Bool) Bool
        (transportComparison
          D0.Foundation.DetectionCapabilityBoundary.membershipComparison)
      ∧ HistoryInvariant (Bool × Bool) Bool
        (transportComparison
          D0.Foundation.DetectionCapabilityBoundary.valueComparison) := by
  constructor
  · rw [← membership_transport_factors]
    exact liftCurrent_historyInvariant _ _ _
  · rw [← value_transport_factors]
    exact liftCurrent_historyInvariant _ _ _

/-- Concrete negative control: history comparison is outside the detector layer. -/
theorem history_outside_detector_layer :
    ¬ HistoryInvariant (Bool × Bool) Bool
      (transportComparison
        D0.Foundation.DetectionCapabilityBoundary.historyComparison) :=
  history_transport_not_invariant

/-- Capstone: both nuisance-variable formulations reduce uniquely to bare current data, and the
concrete D0 membership/value/history split lands on the intended sides. -/
theorem detector_layer_equivalence :
    Nonempty (CatalogueFreeCarrier Bool ≃
      HistoryInvariantCarrier Bool Bool)
      ∧ HistoryInvariant (Bool × Bool) Bool
        (transportComparison
          D0.Foundation.DetectionCapabilityBoundary.membershipComparison)
      ∧ HistoryInvariant (Bool × Bool) Bool
        (transportComparison
          D0.Foundation.DetectionCapabilityBoundary.valueComparison)
      ∧ ¬ HistoryInvariant (Bool × Bool) Bool
        (transportComparison
          D0.Foundation.DetectionCapabilityBoundary.historyComparison) :=
  ⟨⟨catalogueFreeEquivHistoryInvariant Bool⟩,
    membership_value_in_detector_layer.1,
    membership_value_in_detector_layer.2,
    history_outside_detector_layer⟩

end D0.Synthesis.DetectorLayerEquivalence
