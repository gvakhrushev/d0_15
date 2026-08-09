import D0.Foundation.GeneralComparisonGrammar
import Mathlib.Tactic

/-!
# Detection capability boundary: a third history/order capability survives

`D0.Foundation.GeneralComparisonGrammar` proves that the number of primitive
comparison kinds is exactly the number of independent capabilities.  The
remaining root question is therefore whether the D0 detection protocol forces
the capability count to be exactly two.

This module tests that claim without defining a two-element answer type.  A
finite observation carries three independently variable fields:

* `member`  — category/membership data;
* `value`   — value data inside a category;
* `history` — an order/history bit.

A comparison is any Boolean predicate on a pair of observations.  Three literal
comparisons read the three coordinates separately.  Capability dependence is
defined extensionally: a comparison uses a coordinate when changing only that
coordinate can change its result.  The theorem then computes the exact
capability vectors:

* membership equality uses only membership;
* value equality uses only value;
* history equality uses only history.

Each comparison is operational: it both accepts and rejects explicit input
pairs.  The history comparison is therefore a third primitive comparison in
the general capability grammar.  Moreover, membership and value data can be
held fixed while the history comparison changes, so no representation using
only membership/value capabilities can preserve its observable behaviour.

This is a boundary/no-go result, not a claim that history must be counted as a
new *detection* capability in the intended D0 typing.  It proves that the
existing operational/no-catalogue prose does not itself exclude that reading.
To recover exactly two detection capabilities, the theory needs a typed
stratification theorem placing history/order in the memory layer and proving
that primitive detector comparison factors through the current observation,
not through history.
-/

namespace D0.Foundation.DetectionCapabilityBoundary

open D0.Foundation.GeneralComparisonGrammar

/-- A minimal finite observation with independently variable membership,
value, and history/order coordinates. -/
structure Observation where
  member : Bool
  value : Bool
  history : Bool
deriving DecidableEq, Fintype

/-- A comparison is a Boolean test on two observations. -/
abbrev Comparison := Observation → Observation → Bool

/-- A comparison is operational when it can both accept and reject. -/
def OperationalComparison (cmp : Comparison) : Prop :=
  (∃ x y, cmp x y = true) ∧ (∃ x y, cmp x y = false)

/-- Membership/category equality. -/
def membershipComparison : Comparison := fun x y => decide (x.member = y.member)

/-- Value equality. -/
def valueComparison : Comparison := fun x y => decide (x.value = y.value)

/-- History/order equality. -/
def historyComparison : Comparison := fun x y => decide (x.history = y.history)

/-- A pair differs only in membership data. -/
def MembershipOnlyChange (x x' : Observation) : Prop :=
  x.value = x'.value ∧ x.history = x'.history

/-- A pair differs only in value data. -/
def ValueOnlyChange (x x' : Observation) : Prop :=
  x.member = x'.member ∧ x.history = x'.history

/-- A pair differs only in history/order data. -/
def HistoryOnlyChange (x x' : Observation) : Prop :=
  x.member = x'.member ∧ x.value = x'.value

/-- Extensional dependence on membership: changing only membership of one
argument can change the comparison result. -/
def UsesMembership (cmp : Comparison) : Prop :=
  ∃ x x' y, MembershipOnlyChange x x' ∧ cmp x y ≠ cmp x' y

/-- Extensional dependence on value. -/
def UsesValue (cmp : Comparison) : Prop :=
  ∃ x x' y, ValueOnlyChange x x' ∧ cmp x y ≠ cmp x' y

/-- Extensional dependence on history/order. -/
def UsesHistory (cmp : Comparison) : Prop :=
  ∃ x x' y, HistoryOnlyChange x x' ∧ cmp x y ≠ cmp x' y

/-- Capability vector extracted from the observable behaviour of a comparison.
The coordinates are membership, value, and history/order.  It is noncomputable
only because it packages propositions into a Boolean vector; the concrete
vectors below are proved from explicit witnesses and invariance lemmas. -/
noncomputable def capabilityVector (cmp : Comparison) : GenComparison 3 :=
  by
    classical
    exact
      ![if UsesMembership cmp then true else false,
        if UsesValue cmp then true else false,
        if UsesHistory cmp then true else false]

/-- Membership equality is operational. -/
theorem membership_operational : OperationalComparison membershipComparison := by
  refine ⟨⟨⟨false, false, false⟩, ⟨false, true, true⟩, by decide⟩,
    ⟨⟨false, false, false⟩, ⟨true, false, false⟩, by decide⟩⟩

/-- Value equality is operational. -/
theorem value_operational : OperationalComparison valueComparison := by
  refine ⟨⟨⟨false, false, false⟩, ⟨true, false, true⟩, by decide⟩,
    ⟨⟨false, false, false⟩, ⟨false, true, false⟩, by decide⟩⟩

/-- History equality is operational. -/
theorem history_operational : OperationalComparison historyComparison := by
  refine ⟨⟨⟨false, false, false⟩, ⟨true, true, false⟩, by decide⟩,
    ⟨⟨false, false, false⟩, ⟨false, false, true⟩, by decide⟩⟩

/-- Membership equality genuinely depends on membership. -/
theorem membership_uses_membership :
    UsesMembership membershipComparison := by
  exact ⟨⟨false, false, false⟩, ⟨true, false, false⟩,
    ⟨false, false, false⟩, ⟨rfl, rfl⟩, by decide⟩

/-- Membership equality is invariant under value-only changes. -/
theorem membership_not_uses_value :
    ¬ UsesValue membershipComparison := by
  rintro ⟨x, x', y, ⟨hm, _⟩, hne⟩
  exact hne (by simp [membershipComparison, hm])

/-- Membership equality is invariant under history-only changes. -/
theorem membership_not_uses_history :
    ¬ UsesHistory membershipComparison := by
  rintro ⟨x, x', y, ⟨hm, _⟩, hne⟩
  exact hne (by simp [membershipComparison, hm])

/-- Value equality genuinely depends on value. -/
theorem value_uses_value :
    UsesValue valueComparison := by
  exact ⟨⟨false, false, false⟩, ⟨false, true, false⟩,
    ⟨false, false, false⟩, ⟨rfl, rfl⟩, by decide⟩

/-- Value equality is invariant under membership-only changes. -/
theorem value_not_uses_membership :
    ¬ UsesMembership valueComparison := by
  rintro ⟨x, x', y, ⟨hv, _⟩, hne⟩
  exact hne (by simp [valueComparison, hv])

/-- Value equality is invariant under history-only changes. -/
theorem value_not_uses_history :
    ¬ UsesHistory valueComparison := by
  rintro ⟨x, x', y, ⟨_, hv⟩, hne⟩
  exact hne (by simp [valueComparison, hv])

/-- History equality genuinely depends on history. -/
theorem history_uses_history :
    UsesHistory historyComparison := by
  exact ⟨⟨false, false, false⟩, ⟨false, false, true⟩,
    ⟨false, false, false⟩, ⟨rfl, rfl⟩, by decide⟩

/-- History equality is invariant under membership-only changes. -/
theorem history_not_uses_membership :
    ¬ UsesMembership historyComparison := by
  rintro ⟨x, x', y, ⟨_, hh⟩, hne⟩
  exact hne (by simp [historyComparison, hh])

/-- History equality is invariant under value-only changes. -/
theorem history_not_uses_value :
    ¬ UsesValue historyComparison := by
  rintro ⟨x, x', y, ⟨_, hh⟩, hne⟩
  exact hne (by simp [historyComparison, hh])

/-- Exact extensional capability vector of membership equality. -/
theorem membership_capability_vector :
    capabilityVector membershipComparison = atomicOf (0 : Fin 3) := by
  funext i
  fin_cases i <;>
    simp [capabilityVector, atomicOf, membership_uses_membership,
      membership_not_uses_value, membership_not_uses_history]

/-- Exact extensional capability vector of value equality. -/
theorem value_capability_vector :
    capabilityVector valueComparison = atomicOf (1 : Fin 3) := by
  funext i
  fin_cases i <;>
    simp [capabilityVector, atomicOf, value_uses_value,
      value_not_uses_membership, value_not_uses_history]

/-- Exact extensional capability vector of history equality. -/
theorem history_capability_vector :
    capabilityVector historyComparison = atomicOf (2 : Fin 3) := by
  funext i
  fin_cases i <;>
    simp [capabilityVector, atomicOf, history_uses_history,
      history_not_uses_membership, history_not_uses_value]

/-- The history/order comparison is a third primitive comparison in the
three-capability grammar. -/
theorem history_is_third_primitive :
    Primitive (capabilityVector historyComparison) := by
  rw [history_capability_vector, primitive_iff_atomic]
  exact atomicOf_atomic 2

/-- The three explicit operational comparisons realize all three primitive
capability atoms. -/
theorem three_operational_primitive_capabilities :
    OperationalComparison membershipComparison ∧
    OperationalComparison valueComparison ∧
    OperationalComparison historyComparison ∧
    Primitive (capabilityVector membershipComparison) ∧
    Primitive (capabilityVector valueComparison) ∧
    Primitive (capabilityVector historyComparison) := by
  refine ⟨membership_operational, value_operational, history_operational, ?_, ?_,
    history_is_third_primitive⟩
  · rw [membership_capability_vector, primitive_iff_atomic]
    exact atomicOf_atomic 0
  · rw [value_capability_vector, primitive_iff_atomic]
    exact atomicOf_atomic 1

/-- Same current membership/value data, different history, and the history
comparison separates the two cases. -/
theorem history_not_determined_by_membership_value :
    ∃ x x' y : Observation,
      x.member = x'.member ∧
      x.value = x'.value ∧
      historyComparison x y ≠ historyComparison x' y := by
  exact ⟨⟨false, false, false⟩, ⟨false, false, true⟩,
    ⟨false, false, false⟩, rfl, rfl, by decide⟩

/-- A comparison factors through current membership/value data when changing
history alone cannot change its output. -/
def FactorsThroughCurrentData (cmp : Comparison) : Prop :=
  ∀ x x' y,
    x.member = x'.member →
    x.value = x'.value →
    cmp x y = cmp x' y

/-- History comparison does not factor through current membership/value data. -/
theorem history_not_factor_through_current_data :
    ¬ FactorsThroughCurrentData historyComparison := by
  rintro h
  obtain ⟨x, x', y, hm, hv, hne⟩ :=
    history_not_determined_by_membership_value
  exact hne (h x x' y hm hv)

/-- Any comparison represented solely by membership/value capabilities must
factor through current data.  Therefore such a representation cannot preserve
the history comparison. -/
theorem no_membership_value_representation_of_history
    (represented : Bool → Bool → Bool)
    (hrep : ∀ x y,
      historyComparison x y = represented
        (decide (x.member = y.member))
        (decide (x.value = y.value))) :
    False := by
  apply history_not_factor_through_current_data
  intro x x' y hm hv
  rw [hrep x y, hrep x' y, hm, hv]

/-- If comparisons are explicitly restricted to the current-data layer, the
history capability is absent.  This is the exact typed hypothesis needed to
recover the two-capability conclusion. -/
theorem current_data_factorization_excludes_history
    (cmp : Comparison) (h : FactorsThroughCurrentData cmp) :
    ¬ UsesHistory cmp := by
  rintro ⟨x, x', y, ⟨hm, hv⟩, hne⟩
  exact hne (h x x' y hm hv)

/-- **D0-DETECTION-CAPABILITY-THIRD-HISTORY-NOGO-001.** The current finite
protocol admits three independent operational capability atoms unless a typed
current-data factorization excludes history/order from the detector layer. -/
theorem detection_capability_third_history_boundary :
    OperationalComparison membershipComparison ∧
    OperationalComparison valueComparison ∧
    OperationalComparison historyComparison ∧
    capabilityVector membershipComparison = atomicOf (0 : Fin 3) ∧
    capabilityVector valueComparison = atomicOf (1 : Fin 3) ∧
    capabilityVector historyComparison = atomicOf (2 : Fin 3) ∧
    Primitive (capabilityVector historyComparison) ∧
    (¬ FactorsThroughCurrentData historyComparison) :=
  ⟨membership_operational, value_operational, history_operational,
   membership_capability_vector, value_capability_vector,
   history_capability_vector, history_is_third_primitive,
   history_not_factor_through_current_data⟩

end D0.Foundation.DetectionCapabilityBoundary
