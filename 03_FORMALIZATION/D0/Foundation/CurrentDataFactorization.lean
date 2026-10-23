import D0.Foundation.DetectionCapabilityBoundary
import Mathlib.Tactic

/-!
# Current-data quotient factorization

This module solves a quotient question for a declared product observation
Current x History: when does a Boolean comparison descend through the
projection that forgets History? With inhabited history the answer is
exactly invariance under changing either history coordinate, with a unique
descended comparison. The empty-history boundary, explicit descent and
concrete positive/negative controls are retained below.

This theorem concerns that SPECIFIC forgetting projection. It does not
require a physical D0 comparison to ignore memory. In a closed system the
retained consequences of previous interactions belong to its CURRENT complete
state; an internal readout of those consequences can use the original
comparison without adding a fundamental history-comparison primitive.
Consequently the three-coordinate model in DetectionCapabilityBoundary
proves an access/representation boundary, not a third D0 detector operation.

The concrete map named currentData below keeps only (member, value).
It is not asserted to be the full current physical observation when the
history bit is retained and accessible. The actual memory-minimal quotient
is instead the already-owned complete-future profile in FutureExecution:
it forgets only distinctions invisible to every admitted future interaction
and internal readout. Its physical realization and the classification of
primitive D0 comparisons remain separate proof obligations. History
invariance under this coarse projection is not imposed as a replacement for
them. No theorem statement or proof below is changed by this clarification.
-/

namespace D0.Foundation.CurrentDataFactorization

open D0.Foundation.DetectionCapabilityBoundary

universe u v

variable (Current : Type u) (History : Type v)

/-- Full observation before forgetting/quotienting the history layer. -/
abbrev FullObservation := Current × History

/-- Boolean comparison on full observations. -/
abbrev FullComparison := FullObservation Current History →
  FullObservation Current History → Bool

/-- Boolean comparison on current observation data only. -/
abbrev CurrentComparison := Current → Current → Bool

/-- Lift a current-data comparison to full observations by forgetting both
history coordinates. -/
def liftCurrent (base : CurrentComparison Current) :
    FullComparison Current History :=
  fun x y => base x.1 y.1

/-- A full comparison is invariant under changing either history coordinate
while current data are held fixed. -/
def HistoryInvariant (cmp : FullComparison Current History) : Prop :=
  ∀ c₁ c₂ h₁ h₁' h₂ h₂',
    cmp (c₁, h₁) (c₂, h₂) = cmp (c₁, h₁') (c₂, h₂')

/-- Every lifted current-data comparison is history-invariant. -/
theorem liftCurrent_historyInvariant (base : CurrentComparison Current) :
    HistoryInvariant Current History (liftCurrent Current History base) := by
  intro c₁ c₂ h₁ h₁' h₂ h₂'
  rfl

/-- Lift is injective whenever the history type is inhabited: evaluate both
lifts at the same reference history. -/
theorem liftCurrent_injective [Nonempty History] :
    Function.Injective (liftCurrent Current History) := by
  intro a b hab
  obtain ⟨h⟩ := ‹Nonempty History›
  funext x y
  exact congrFun (congrFun hab (x, h)) (y, h)

/-- Explicit descent through a chosen reference history. -/
def descendAt (h₀ : History) (cmp : FullComparison Current History) :
    CurrentComparison Current :=
  fun x y => cmp (x, h₀) (y, h₀)

/-- Descent reconstructs every history-invariant comparison. -/
theorem lift_descendAt_eq (h₀ : History)
    (cmp : FullComparison Current History)
    (hinv : HistoryInvariant Current History cmp) :
    liftCurrent Current History (descendAt Current History h₀ cmp) = cmp := by
  funext x y
  exact hinv x.1 y.1 h₀ x.2 h₀ y.2

/-- The descended current comparison is independent of the chosen reference
history. -/
theorem descendAt_independent
    (cmp : FullComparison Current History)
    (hinv : HistoryInvariant Current History cmp)
    (h₀ h₁ : History) :
    descendAt Current History h₀ cmp =
      descendAt Current History h₁ cmp := by
  funext x y
  exact hinv x y h₀ h₁ h₀ h₁

/-- Uniqueness of a current-data factorization. -/
theorem factorization_unique [Nonempty History]
    (cmp : FullComparison Current History)
    {a b : CurrentComparison Current}
    (ha : liftCurrent Current History a = cmp)
    (hb : liftCurrent Current History b = cmp) :
    a = b :=
  liftCurrent_injective Current History (ha.trans hb.symm)

/-- **Inhabited-history quotient theorem.** History invariance is equivalent to
existence of a unique current-data comparison whose lift is the full
comparison. -/
theorem historyInvariant_iff_existsUnique_factorization
    [Nonempty History] (cmp : FullComparison Current History) :
    HistoryInvariant Current History cmp ↔
      ∃! base : CurrentComparison Current,
        liftCurrent Current History base = cmp := by
  constructor
  · intro hinv
    obtain ⟨h₀⟩ := ‹Nonempty History›
    refine ⟨descendAt Current History h₀ cmp,
      lift_descendAt_eq Current History h₀ cmp hinv, ?_⟩
    intro base hbase
    exact factorization_unique Current History cmp hbase
      (lift_descendAt_eq Current History h₀ cmp hinv)
  · rintro ⟨base, hbase, _⟩
    rw [← hbase]
    exact liftCurrent_historyInvariant Current History base

/-- Any factorization through current data implies history invariance, with no
inhabitedness assumption. -/
theorem factorization_implies_historyInvariant
    (cmp : FullComparison Current History)
    {base : CurrentComparison Current}
    (hbase : liftCurrent Current History base = cmp) :
    HistoryInvariant Current History cmp := by
  rw [← hbase]
  exact liftCurrent_historyInvariant Current History base

/-! ## Empty-history boundary

When `History` is empty there are no full observations, so all full comparisons
are extensionally equal.  A base comparison still need not be unique unless
`Current` is also empty, which is exactly why the unique-factorization theorem
above requires `Nonempty History`.  This boundary is named rather than hidden.
-/

/-- With empty history, any two full comparisons are equal because their input
type is empty. -/
theorem fullComparison_subsingleton_of_isEmpty [IsEmpty History]
    (a b : FullComparison Current History) :
    a = b := by
  funext x
  exact isEmptyElim x.2

/-- Negative boundary control: if history is empty but current data admit two
different comparisons, lift cannot be injective. -/
theorem empty_history_lift_not_injective :
    ¬ Function.Injective
      (liftCurrent Bool Empty) := by
  intro hinj
  let a : CurrentComparison Bool := fun _ _ => false
  let b : CurrentComparison Bool := fun _ _ => true
  have hlift : liftCurrent Bool Empty a = liftCurrent Bool Empty b :=
    fullComparison_subsingleton_of_isEmpty Bool Empty _ _
  have hab : a = b := hinj hlift
  have h := congrFun (congrFun hab false) false
  simp [a, b] at h

/-! ## Concrete D0 connection -/

/-- Current-data quotient of the concrete D0 observation. -/
def currentData (x : Observation) : Bool × Bool := (x.member, x.value)

/-- Repackage the concrete D0 observation as current data plus history. -/
def splitObservation : Observation ≃ (Bool × Bool) × Bool where
  toFun x := (currentData x, x.history)
  invFun x := ⟨x.1.1, x.1.2, x.2⟩
  left_inv := by intro x; cases x; rfl
  right_inv := by intro x; cases x; rfl

/-- Transport a concrete D0 comparison to the generic split carrier. -/
def transportComparison (cmp : Comparison) :
    FullComparison (Bool × Bool) Bool :=
  fun x y => cmp (splitObservation.symm x) (splitObservation.symm y)

/-- Membership comparison factors through the current-data quotient. -/
def membershipBase : CurrentComparison (Bool × Bool) :=
  fun x y => decide (x.1 = y.1)

theorem membership_transport_factors :
    liftCurrent (Bool × Bool) Bool membershipBase =
      transportComparison membershipComparison := by
  funext x y
  rfl

/-- Value comparison factors through the current-data quotient. -/
def valueBase : CurrentComparison (Bool × Bool) :=
  fun x y => decide (x.2 = y.2)

theorem value_transport_factors :
    liftCurrent (Bool × Bool) Bool valueBase =
      transportComparison valueComparison := by
  funext x y
  rfl

/-- History comparison remains history-sensitive after transport. -/
theorem history_transport_not_invariant :
    ¬ HistoryInvariant (Bool × Bool) Bool
      (transportComparison historyComparison) := by
  intro h
  have := h (false, false) (false, false)
    false true false false
  simp [transportComparison, splitObservation, historyComparison] at this

/-- Hence history comparison has no current-data factorization. -/
theorem history_transport_no_factorization :
    ¬ ∃ base : CurrentComparison (Bool × Bool),
      liftCurrent (Bool × Bool) Bool base =
        transportComparison historyComparison := by
  rintro ⟨base, hbase⟩
  exact history_transport_not_invariant
    (factorization_implies_historyInvariant (Bool × Bool) Bool _
      hbase)

/-- **D0-CURRENT-DATA-FACTORIZATION-001.** Bundle: the universal quotient
theorem, explicit descent/uniqueness, empty-history boundary, and concrete D0
positive/negative controls. -/
theorem current_data_factorization :
    (∀ (C H : Type) (_hH : Nonempty H)
      (cmp : FullComparison C H),
      HistoryInvariant C H cmp ↔
        ∃! base : CurrentComparison C,
          liftCurrent C H base = cmp) ∧
    liftCurrent (Bool × Bool) Bool membershipBase =
      transportComparison membershipComparison ∧
    liftCurrent (Bool × Bool) Bool valueBase =
      transportComparison valueComparison ∧
    (¬ HistoryInvariant (Bool × Bool) Bool
      (transportComparison historyComparison)) ∧
    (¬ Function.Injective (liftCurrent Bool Empty)) := by
  refine ⟨?_, membership_transport_factors,
    value_transport_factors, history_transport_not_invariant,
    empty_history_lift_not_injective⟩
  intro C H hH cmp
  letI : Nonempty H := hH
  exact historyInvariant_iff_existsUnique_factorization C H cmp

end D0.Foundation.CurrentDataFactorization
