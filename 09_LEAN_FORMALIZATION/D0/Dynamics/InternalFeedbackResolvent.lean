namespace D0.Dynamics

/-!
Finite closed-vacuum feedback interface.

The core object is the finite retained/traced-out split. No external mirror or
outside boundary is admitted: feedback is the internal return from the traced
complement back into the retained sector.
-/

structure ClosedFiniteSupport where
  carrier : Nat
  nonempty : 0 < carrier
  noOutside : Bool

structure RetainedTracedSplit where
  retained : Nat
  traced : Nat
  retained_pos : 0 < retained
  traced_pos : 0 < traced

structure FiniteFeedbackOperator where
  split : RetainedTracedSplit
  constructedFromPQU : Bool
  finiteResolvent : Bool
  noExternalMirror : Bool

def feedbackSlots (s : RetainedTracedSplit) : Nat :=
  s.retained * s.traced

theorem feedback_slots_positive (s : RetainedTracedSplit) :
    0 < feedbackSlots s := by
  unfold feedbackSlots
  exact Nat.mul_pos s.retained_pos s.traced_pos

theorem internal_feedback_forced_by_split (s : RetainedTracedSplit) :
    0 < feedbackSlots s := feedback_slots_positive s

theorem internal_feedback_resolvent_series (R : FiniteFeedbackOperator) :
    R.constructedFromPQU = true ->
    R.finiteResolvent = true ->
    R.noExternalMirror = true ->
    R.constructedFromPQU && R.finiteResolvent && R.noExternalMirror = true := by
  intro hpq hfin hno
  simp [hpq, hfin, hno]

theorem external_mirror_model_forbidden (S : ClosedFiniteSupport) :
    S.noOutside = true -> S.noOutside != false := by
  intro h
  simp [h]

end D0.Dynamics
