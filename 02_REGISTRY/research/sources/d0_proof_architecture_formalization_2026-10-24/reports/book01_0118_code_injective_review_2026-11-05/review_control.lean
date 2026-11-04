import D0.Foundation.UncoupledCenterRawWitness

open D0.Foundation.VerificationCore
open D0.Foundation.TheoryTransfer
open D0.Foundation.VerificationTransferApplication

#check CodePresentation
#check CodePresentation.decode_encode
#check CodePresentation.encode_injective
#check SigmaWitness.dmin_eq_iff
#check SigmaWitness.archiveCode_eq_iff
#print axioms CodePresentation.encode_injective
#print axioms SigmaWitness.dmin_eq_iff
#print axioms SigmaWitness.archiveCode_eq_iff
#print CodePresentation.encode_injective
#print SigmaWitness.dmin_eq_iff
#print SigmaWitness.archiveCode_eq_iff

-- A constant code for two different objects cannot have a single decoder
-- satisfying the stated round trip on both of them.
example : ¬ ∃ (decode : List Bool → Option Bool),
    ∀ x : Bool, decode ((fun _ : Bool => ([] : List Bool)) x) = some x := by
  rintro ⟨decode, h⟩
  have h0 := h false
  have h1 := h true
  have impossible : some false = some true := h0.symm.trans h1
  cases impossible

-- Conversely, an injective encoder by itself does not make an arbitrary
-- supplied decoder correct.
example : Function.Injective (fun b : Bool => [b]) ∧
    (fun _ : List Bool => (none : Option Bool)) [false] ≠ some false := by
  constructor
  · intro a b h
    simpa using h
  · decide

-- The injected objects are represented states, not arbitrary raw states.
-- This conditional witness keeps the same E and W in the existing example.
example (W : SigmaWitness visibleBitVerification) :
    ((false, false) : visibleBitSystem.State) ≠ (false, true) ∧
    W.dmin (false, false) = W.dmin (false, true) := by
  constructor
  · intro h
    have hbit : false = true := congrArg Prod.snd h
    cases hbit
  · exact (W.dmin_eq_iff _ _).mpr visibleBit_same_all_source_futures
