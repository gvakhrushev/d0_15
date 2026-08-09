import D0.Foundation.CurrentDataComparisonCanonicity
import Mathlib.Tactic

/-!
# Complete Boolean current-data axis classification

`D0.Foundation.CurrentDataComparisonCanonicity` proves that reflexivity resolves
the explicit equality/inequality fork.  That two-completion result is not yet a
classification of all Boolean comparisons.  This module closes that finite
problem and records every load-bearing hypothesis.

## One Boolean coordinate

For an arbitrary comparison `f : Bool → Bool → Bool`, the conjunction

* operational — both `true` and `false` occur;
* reflexive — `f x x = true`;
* symmetric — `f x y = f y x`;

forces `f` to be equality.  The proof is exhaustive over the four entries of
the Boolean comparison table, not restricted to a predeclared candidate pair.

Each hypothesis is necessary:

* without operationality, the constant-`true` comparison survives;
* without reflexivity, inequality survives;
* without symmetry, Boolean implication survives.

## Two current-data coordinates

Current data are `(membership, value)`.  `AxisLocal f i` says that `f` factors
through exactly one coordinate `i : Fin 2`.  Combining axis-locality with the
three conditions above gives exactly one comparison per axis: equality of
membership or equality of value.  The admissible comparison carrier is
therefore equivalent to `Fin 2`, hence has cardinality exactly two.

Axis-locality is independently load-bearing: equality of the whole pair is
operational, reflexive and symmetric, but it depends jointly on both axes and
does not factor through either one.

This closes the full finite Boolean canonicity theorem hidden behind the
earlier equality/complement example.  Honest residual: D0 still needs a
stratification theorem deriving history-invariance, axis-locality, reflexivity
and symmetry from the primitive M1 detector protocol.  None is assumed to
follow from the others here.
-/

namespace D0.Foundation.CurrentDataAxisClassification

open D0.Foundation.CurrentDataComparisonCanonicity

/-- Symmetry of a Boolean comparison. -/
def Symmetric (cmp : Bool → Bool → Bool) : Prop :=
  ∀ x y, cmp x y = cmp y x

/-- Constant acceptance: the negative control when operationality is absent. -/
def acceptAll : Bool → Bool → Bool := fun _ _ => true

/-- Boolean implication: reflexive and operational, but not symmetric. -/
def implicationComparison : Bool → Bool → Bool :=
  fun x y => (!x) || y

theorem eq_symmetric : Symmetric eqComparison := by
  intro x y
  cases x <;> cases y <;> decide

theorem ne_symmetric : Symmetric neComparison := by
  intro x y
  cases x <;> cases y <;> decide

theorem acceptAll_reflexive : Reflexive acceptAll := by
  intro x
  rfl

theorem acceptAll_symmetric : Symmetric acceptAll := by
  intro x y
  rfl

theorem acceptAll_not_operational : ¬ Operational acceptAll := by
  rintro ⟨_, ⟨x, y, hfalse⟩⟩
  simp [acceptAll] at hfalse

theorem implication_operational : Operational implicationComparison := by
  exact ⟨⟨false, false, by decide⟩, ⟨true, false, by decide⟩⟩

theorem implication_reflexive : Reflexive implicationComparison := by
  intro x
  cases x <;> decide

theorem implication_not_symmetric : ¬ Symmetric implicationComparison := by
  intro h
  have := h false true
  decide

/-- **Complete one-axis classification.** Every operational, reflexive,
symmetric Boolean comparison is equality. -/
theorem operational_reflexive_symmetric_eq
    (cmp : Bool → Bool → Bool)
    (hop : Operational cmp)
    (hrefl : Reflexive cmp)
    (hsymm : Symmetric cmp) :
    cmp = eqComparison := by
  funext x y
  cases x <;> cases y
  · simpa [eqComparison] using hrefl false
  · have h01 : cmp false true = false := by
      rcases Bool.dichotomy (cmp false true) with hfalse | htrue
      · exact hfalse
      · exfalso
        rcases hop.2 with ⟨a, b, hab⟩
        cases a <;> cases b
        · simpa [hrefl false] using hab
        · simpa [htrue] using hab
        · have h10 : cmp true false = true := by
            rw [hsymm true false, htrue]
          simpa [h10] using hab
        · simpa [hrefl true] using hab
    simp [eqComparison, h01]
  · have h10 : cmp true false = false := by
      rw [hsymm true false]
      have h01 : cmp false true = false := by
        rcases Bool.dichotomy (cmp false true) with hfalse | htrue
        · exact hfalse
        · exfalso
          rcases hop.2 with ⟨a, b, hab⟩
          cases a <;> cases b
          · simpa [hrefl false] using hab
          · simpa [htrue] using hab
          · have : cmp true false = true := by rw [hsymm true false, htrue]
            simpa [this] using hab
          · simpa [hrefl true] using hab
      exact h01
    simp [eqComparison, h10]
  · simpa [eqComparison] using hrefl true

/-! ## Two-axis current data -/

/-- Current observation data: membership bit and value bit. -/
abbrev Current := Bool × Bool

/-- Read one current-data axis.  Axis `0` is membership, axis `1` is value. -/
def axisValue (i : Fin 2) (x : Current) : Bool :=
  if i = 0 then x.1 else x.2

/-- A comparison factors through a single named current-data axis. -/
def AxisLocal (cmp : Current → Current → Bool) (i : Fin 2) : Prop :=
  ∃ base : Bool → Bool → Bool,
    cmp = fun x y => base (axisValue i x) (axisValue i y)

/-- Equality comparison on one current-data axis. -/
def axisEquality (i : Fin 2) : Current → Current → Bool :=
  fun x y => eqComparison (axisValue i x) (axisValue i y)

/-- Operationality on the two-axis current carrier. -/
def CurrentOperational (cmp : Current → Current → Bool) : Prop :=
  (∃ x y, cmp x y = true) ∧ (∃ x y, cmp x y = false)

/-- Reflexivity on current data. -/
def CurrentReflexive (cmp : Current → Current → Bool) : Prop :=
  ∀ x, cmp x x = true

/-- Symmetry on current data. -/
def CurrentSymmetric (cmp : Current → Current → Bool) : Prop :=
  ∀ x y, cmp x y = cmp y x

theorem axisEquality_local (i : Fin 2) : AxisLocal (axisEquality i) i :=
  ⟨eqComparison, rfl⟩

theorem axisEquality_operational (i : Fin 2) :
    CurrentOperational (axisEquality i) := by
  fin_cases i
  · exact ⟨⟨(false, false), (false, true), by decide⟩,
      ⟨(false, false), (true, false), by decide⟩⟩
  · exact ⟨⟨(false, false), (true, false), by decide⟩,
      ⟨(false, false), (false, true), by decide⟩⟩

theorem axisEquality_reflexive (i : Fin 2) :
    CurrentReflexive (axisEquality i) := by
  intro x
  simp [axisEquality, eqComparison]

theorem axisEquality_symmetric (i : Fin 2) :
    CurrentSymmetric (axisEquality i) := by
  intro x y
  simp only [axisEquality]
  exact eq_symmetric _ _

/-- Axis locality transports the three physical conditions to the underlying
one-coordinate Boolean comparison. -/
theorem local_base_conditions
    (cmp : Current → Current → Bool) (i : Fin 2)
    (hlocal : AxisLocal cmp i)
    (hop : CurrentOperational cmp)
    (hrefl : CurrentReflexive cmp)
    (hsymm : CurrentSymmetric cmp) :
    ∃ base,
      cmp = fun x y => base (axisValue i x) (axisValue i y) ∧
      Operational base ∧ Reflexive base ∧ Symmetric base := by
  rcases hlocal with ⟨base, rfl⟩
  refine ⟨base, rfl, ?_, ?_, ?_⟩
  · constructor
    · rcases hop.1 with ⟨x, y, hxy⟩
      exact ⟨axisValue i x, axisValue i y, hxy⟩
    · rcases hop.2 with ⟨x, y, hxy⟩
      exact ⟨axisValue i x, axisValue i y, hxy⟩
  · intro b
    let x : Current := if i = 0 then (b, false) else (false, b)
    have hx : axisValue i x = b := by
      fin_cases i <;> simp [x, axisValue]
    simpa [hx] using hrefl x
  · intro a b
    let x : Current := if i = 0 then (a, false) else (false, a)
    let y : Current := if i = 0 then (b, false) else (false, b)
    have hx : axisValue i x = a := by
      fin_cases i <;> simp [x, axisValue]
    have hy : axisValue i y = b := by
      fin_cases i <;> simp [y, axisValue]
    simpa [hx, hy] using hsymm x y

/-- **Complete axis-local classification.** -/
theorem axisLocal_operational_reflexive_symmetric_eq
    (cmp : Current → Current → Bool) (i : Fin 2)
    (hlocal : AxisLocal cmp i)
    (hop : CurrentOperational cmp)
    (hrefl : CurrentReflexive cmp)
    (hsymm : CurrentSymmetric cmp) :
    cmp = axisEquality i := by
  rcases local_base_conditions cmp i hlocal hop hrefl hsymm with
    ⟨base, hcmp, hbop, hbref, hbsym⟩
  have hbase := operational_reflexive_symmetric_eq base hbop hbref hbsym
  rw [hcmp, hbase]
  rfl

/-- Membership equality and value equality are distinct functions. -/
theorem axisEquality_injective : Function.Injective axisEquality := by
  intro i j hij
  fin_cases i <;> fin_cases j
  · rfl
  · exfalso
    have h := congrFun (congrFun hij (false, false)) (false, true)
    decide
  · exfalso
    have h := congrFun (congrFun hij (false, false)) (true, false)
    decide
  · rfl

/-- Carrier of all axis-local, operational, reflexive and symmetric current
comparisons, with the axis recorded as part of the public comparison kind. -/
abbrev CanonicalAxisCarrier :=
  {p : Fin 2 × (Current → Current → Bool) //
    AxisLocal p.2 p.1 ∧
    CurrentOperational p.2 ∧
    CurrentReflexive p.2 ∧
    CurrentSymmetric p.2}

/-- The full admissible carrier is equivalent to the two axes. -/
noncomputable def canonicalAxisEquiv : CanonicalAxisCarrier ≃ Fin 2 where
  toFun p := p.1.1
  invFun i :=
    ⟨(i, axisEquality i),
      axisEquality_local i,
      axisEquality_operational i,
      axisEquality_reflexive i,
      axisEquality_symmetric i⟩
  left_inv := by
    rintro ⟨⟨i, cmp⟩, hlocal, hop, hrefl, hsymm⟩
    apply Subtype.ext
    apply Prod.ext
    · rfl
    · exact (axisLocal_operational_reflexive_symmetric_eq
        cmp i hlocal hop hrefl hsymm).symm
  right_inv := by
    intro i
    rfl

/-- **Exactly two canonical current-data comparison kinds.** -/
theorem canonicalAxis_card_eq_two :
    Nat.card CanonicalAxisCarrier = 2 := by
  rw [Nat.card_congr canonicalAxisEquiv,
    Nat.card_eq_fintype_card, Fintype.card_fin]

/-! ## Axis-locality negative control -/

/-- Equality of the complete `(membership,value)` pair. -/
def jointEquality : Current → Current → Bool :=
  fun x y => decide (x = y)

theorem jointEquality_operational : CurrentOperational jointEquality :=
  ⟨⟨(false, false), (false, false), by decide⟩,
   ⟨(false, false), (false, true), by decide⟩⟩

theorem jointEquality_reflexive : CurrentReflexive jointEquality := by
  intro x
  simp [jointEquality]

theorem jointEquality_symmetric : CurrentSymmetric jointEquality := by
  intro x y
  cases x
  cases y
  simp only [jointEquality]
  apply decide_eq_decide.mpr
  exact eq_comm

theorem jointEquality_not_axisLocal (i : Fin 2) :
    ¬ AxisLocal jointEquality i := by
  rintro ⟨base, hbase⟩
  fin_cases i
  · have hsame := congrFun (congrFun hbase (false, false)) (false, false)
    have hdiff := congrFun (congrFun hbase (false, false)) (false, true)
    simp [jointEquality, axisValue] at hsame hdiff
  · have hsame := congrFun (congrFun hbase (false, false)) (false, false)
    have hdiff := congrFun (congrFun hbase (false, false)) (true, false)
    simp [jointEquality, axisValue] at hsame hdiff

/-- **D0-CURRENT-DATA-AXIS-CLASSIFICATION-001.** Complete classification over
all Boolean comparisons plus exact two-axis cardinality and a joint-axis
negative control. -/
theorem current_data_axis_classification :
    (∀ cmp : Bool → Bool → Bool,
      Operational cmp → Reflexive cmp → Symmetric cmp →
      cmp = eqComparison) ∧
    Nat.card CanonicalAxisCarrier = 2 ∧
    CurrentOperational jointEquality ∧
    CurrentReflexive jointEquality ∧
    CurrentSymmetric jointEquality ∧
    (∀ i : Fin 2, ¬ AxisLocal jointEquality i) ∧
    (¬ Operational acceptAll) ∧
    (¬ Reflexive neComparison) ∧
    (¬ Symmetric implicationComparison) :=
  ⟨operational_reflexive_symmetric_eq, canonicalAxis_card_eq_two,
   jointEquality_operational, jointEquality_reflexive,
   jointEquality_symmetric, jointEquality_not_axisLocal,
   acceptAll_not_operational, ne_not_reflexive,
   implication_not_symmetric⟩

end D0.Foundation.CurrentDataAxisClassification
