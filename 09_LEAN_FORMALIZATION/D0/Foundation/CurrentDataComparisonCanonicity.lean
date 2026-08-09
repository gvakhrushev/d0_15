import D0.Foundation.CurrentDataFactorization
import Mathlib.Tactic

/-!
# Current-data comparison canonicity boundary

`D0.Foundation.CurrentDataFactorization` closes the detector/memory quotient:
history-invariant comparisons descend uniquely to current data.  That alone does
not imply there are only two **physical comparison kinds**.  Even on one current
Boolean coordinate, equality and inequality are distinct operational
comparisons and both use exactly the same capability.

This module names and proves that next boundary.

For Boolean current data:

* `eqComparison` and `neComparison` are both operational;
* both are sensitive to the same Boolean coordinate;
* they are distinct (indeed pointwise complements);
* therefore a capability map recording only "uses this coordinate" is not
  injective on physical comparisons.

Thus the representation contract's injectivity field cannot be derived from
history factorization or capability support alone.  A separate canonicity rule
is necessary.

The positive half gives the exact sufficient rule: fix a polarity
(`accept equal` versus `accept unequal`) and require reflexivity at the detector
floor.  Among the two separated Boolean comparisons, reflexivity uniquely
selects equality.  The negative control shows that dropping reflexivity admits
inequality.  This is not yet a universal classification of all Boolean
functions; it is the exact two-completion canonicity theorem for the equality
versus complement ambiguity created by the same capability support.

Honest residual: to close the physical two-kind theorem, D0 must justify the
detector-floor polarity/reflexivity requirement from M1 or the registration
protocol, and then extend canonicity from this two-completion family to the full
admissible comparison class.
-/

namespace D0.Foundation.CurrentDataComparisonCanonicity

/-- Equality comparison on one current Boolean coordinate. -/
def eqComparison : Bool → Bool → Bool := fun x y => decide (x = y)

/-- Inequality comparison on the same coordinate. -/
def neComparison : Bool → Bool → Bool := fun x y => decide (x ≠ y)

/-- Operationality: the comparison can both accept and reject. -/
def Operational (cmp : Bool → Bool → Bool) : Prop :=
  (∃ x y, cmp x y = true) ∧ (∃ x y, cmp x y = false)

/-- Extensional use of the current coordinate. -/
def UsesCurrent (cmp : Bool → Bool → Bool) : Prop :=
  ∃ x x' y, cmp x y ≠ cmp x' y

/-- Detector-floor reflexivity: a current reading agrees with itself. -/
def Reflexive (cmp : Bool → Bool → Bool) : Prop :=
  ∀ x, cmp x x = true

theorem eq_operational : Operational eqComparison := by
  exact ⟨⟨false, false, by decide⟩, ⟨false, true, by decide⟩⟩

theorem ne_operational : Operational neComparison := by
  exact ⟨⟨false, true, by decide⟩, ⟨false, false, by decide⟩⟩

theorem eq_uses_current : UsesCurrent eqComparison := by
  exact ⟨false, true, false, by decide⟩

theorem ne_uses_current : UsesCurrent neComparison := by
  exact ⟨false, true, false, by decide⟩

theorem eq_ne_distinct : eqComparison ≠ neComparison := by
  intro h
  have := congrFun (congrFun h false) false
  simp [eqComparison, neComparison] at this

/-- Equality and inequality are pointwise complements. -/
theorem ne_eq_not_eq (x y : Bool) :
    neComparison x y = !eqComparison x y := by
  cases x <;> cases y <;> decide

theorem eq_reflexive : Reflexive eqComparison := by
  intro x
  simp [eqComparison]

theorem ne_not_reflexive : ¬ Reflexive neComparison := by
  intro h
  have := h false
  simp [neComparison] at this

/-- Two distinct physical comparisons share the same one-coordinate capability
support.  Therefore support alone is not an injective classifier. -/
inductive SameCapabilityComparison
  | equality
  | inequality
deriving DecidableEq, Fintype

def interpretation : SameCapabilityComparison → (Bool → Bool → Bool)
  | .equality => eqComparison
  | .inequality => neComparison

/-- The coarse capability support is identical for both comparisons. -/
def support (_ : SameCapabilityComparison) : Fin 1 → Bool :=
  fun _ => true

theorem support_not_injective :
    ¬ Function.Injective support := by
  intro h
  have : SameCapabilityComparison.equality =
      SameCapabilityComparison.inequality :=
    h rfl
  cases this

theorem interpretations_distinct :
    interpretation .equality ≠ interpretation .inequality :=
  eq_ne_distinct

/-- Exactly one member of the same-capability pair is reflexive. -/
theorem reflexive_iff_equality (c : SameCapabilityComparison) :
    Reflexive (interpretation c) ↔ c = .equality := by
  cases c
  · simp [interpretation, eq_reflexive]
  · simp [interpretation, ne_not_reflexive]

/-- **Canonicity inside the equality/complement family.** Reflexivity selects
equality uniquely. -/
theorem equality_unique_reflexive :
    ∃! c : SameCapabilityComparison,
      Reflexive (interpretation c) := by
  refine ⟨.equality, eq_reflexive, ?_⟩
  intro c hc
  exact (reflexive_iff_equality c).mp hc

/-- Dropping reflexivity leaves two operational comparisons with the same
capability support. -/
theorem operational_support_underdetermination :
    Operational (interpretation .equality) ∧
    Operational (interpretation .inequality) ∧
    support .equality = support .inequality ∧
    interpretation .equality ≠ interpretation .inequality :=
  ⟨eq_operational, ne_operational, rfl, interpretations_distinct⟩

/-- **D0-CURRENT-DATA-COMPARISON-CANONICITY-NOGO-001.** Bundle: same-support
underdetermination and the exact reflexive canonicity condition that resolves
the equality/complement fork. -/
theorem current_data_comparison_canonicity_boundary :
    Operational eqComparison ∧
    Operational neComparison ∧
    UsesCurrent eqComparison ∧
    UsesCurrent neComparison ∧
    eqComparison ≠ neComparison ∧
    (¬ Function.Injective support) ∧
    (∃! c : SameCapabilityComparison,
      Reflexive (interpretation c)) :=
  ⟨eq_operational, ne_operational, eq_uses_current, ne_uses_current,
   eq_ne_distinct, support_not_injective, equality_unique_reflexive⟩

end D0.Foundation.CurrentDataComparisonCanonicity
