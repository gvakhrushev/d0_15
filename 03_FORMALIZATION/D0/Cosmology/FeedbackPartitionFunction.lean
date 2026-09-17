import D0.Dynamics.InternalFeedbackResolvent

namespace D0.Cosmology

structure FeedbackPartitionFunction where
  heatTraceFinite : Bool
  determinantFinite : Bool
  determinantNonzero : Bool
  returnCycleExpansion : Bool

structure ReturnCycle where
  length : Nat
  positive_length : 0 < length
  traceWeight : Int

def returnCycleDepth (depth : Nat) : List Nat :=
  List.range depth

theorem return_cycle_depth_card (depth : Nat) :
    (returnCycleDepth depth).length = depth := by
  unfold returnCycleDepth
  simp

theorem feedback_determinant_return_cycles
    (Z : FeedbackPartitionFunction) :
    Z.determinantFinite = true ->
    Z.determinantNonzero = true ->
    Z.returnCycleExpansion = true ->
    Z.determinantFinite && Z.determinantNonzero && Z.returnCycleExpansion = true := by
  intro hfin hnz hexp
  simp [hfin, hnz, hexp]

structure FeedbackVariationSource where
  resolventFinite : Bool
  sourceFinite : Bool
  sourceFromInternalFeedback : Bool

theorem feedback_variation_universal_source
    (S : FeedbackVariationSource) :
    S.resolventFinite = true ->
    S.sourceFinite = true ->
    S.sourceFromInternalFeedback = true ->
    S.resolventFinite && S.sourceFinite && S.sourceFromInternalFeedback = true := by
  intro hres hsrc hint
  simp [hres, hsrc, hint]

end D0.Cosmology
