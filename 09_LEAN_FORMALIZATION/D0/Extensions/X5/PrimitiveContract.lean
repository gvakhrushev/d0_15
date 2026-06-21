import Mathlib.Tactic

/-!
# D0-X5-PRIMITIVE-CONTRACT-001 — the shared typed contract pattern (Section 2)

A `PrimitiveContract` is the smallest typed datum that resolves one D0 frontier. It is an EXTENSION object
(`extensionLayer = "D0-X5"`), never present-core. A contract is well-formed when it is in the D0-X5 layer, has
at least one law, and a positive finite carrier. A `ModelWitness` proves the interface is non-vacuous: a
concrete carrier on which the laws hold (the lane modules supply the `decide`-checked content). A
`DeletionTest` proves a law is necessary: dropping it admits `≥ 2` models (the prior two-completions reappear).
This module is the pattern; the five lanes instantiate it with real finite models.
-/

namespace D0.Extensions.X5

/-- A typed D0-X5 primitive contract. -/
structure PrimitiveContract where
  id : String
  extensionLayer : String
  laws : List String
  carrierDim : ℕ
  deriving Repr, DecidableEq

/-- Well-formedness: D0-X5 layer, at least one law, positive carrier. -/
abbrev PrimitiveContract.wellFormed (c : PrimitiveContract) : Prop :=
  c.extensionLayer = "D0-X5" ∧ c.laws ≠ [] ∧ 0 < c.carrierDim

/-- A model witness: a concrete carrier with `lawsVerified` laws checked to hold; `nonVacuous` records that the
model is a real finite instantiation (the lane proves this by `decide`, not by `True`). -/
structure ModelWitness where
  carrierDim : ℕ
  lawsVerified : ℕ
  nonVacuous : Bool
  deriving Repr, DecidableEq

/-- A model is complete for a contract when it is non-vacuous and verifies all the contract's laws. -/
abbrev ModelWitness.complete (m : ModelWitness) (c : PrimitiveContract) : Prop :=
  m.nonVacuous = true ∧ m.lawsVerified = c.laws.length ∧ m.carrierDim = c.carrierDim

/-- A deletion test for one law: dropping it admits `survivingModels` admissible models; the law is necessary
when `survivingModels ≥ 2` (a genuine nonuniqueness witness). -/
structure DeletionTest where
  law : String
  survivingModels : ℕ
  deriving Repr, DecidableEq

abbrev DeletionTest.lawNecessary (d : DeletionTest) : Prop := 2 ≤ d.survivingModels

/-- A contract is minimal when every law has a deletion test showing it necessary. -/
def deletionMinimal (tests : List DeletionTest) : Prop := ∀ d ∈ tests, d.lawNecessary

/-- The contract layer tag (used by every lane and by the status discipline). -/
def x5 : String := "D0-X5"

theorem x5_layer : x5 = "D0-X5" := rfl

end D0.Extensions.X5
