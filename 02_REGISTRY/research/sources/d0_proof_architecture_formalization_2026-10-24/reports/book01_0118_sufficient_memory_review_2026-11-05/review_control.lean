import D0.Foundation.FutureShortlexAdapter

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerificationCore
open D0.Foundation.FutureShortlexAdapter

#check sufficient_memory_preserves_record
#check FutureExecution.sufficient_memory_reflects_future
#check representedRecord_eq_iff
#check stateCode_eq_iff_record
#check hiddenBit_same_current
#check hiddenBit_different_future
#check hiddenBit_records_distinct
#check FutureExecution.uncoupledCenter_profile_independent
#check uncoupledCenter_records_equal
#print axioms sufficient_memory_preserves_record
#print axioms stateCode_eq_iff_record
#print axioms hiddenBit_same_current
#print axioms hiddenBit_different_future
#print axioms hiddenBit_records_distinct
#print axioms FutureExecution.uncoupledCenter_profile_independent
#print axioms uncoupledCenter_records_equal
#print stateCode_eq_iff_record

-- A sufficient memory may preserve extra raw distinctions: the converse
-- of the reviewed implication is false on the abstract uncoupled carrier.
example (F : FutureExecution) (s : F.State)
    (E : D0.Foundation.VerifiabilityNecessity.TheoryVerification
      F.uncoupledCenter.futureEmpiricalTheory) :
    (∀ x : F.uncoupledCenter.State,
      F.uncoupledCenter.profile (id x) = F.uncoupledCenter.profile x) ∧
    id (s, false) ≠ id (s, true) ∧
    representedRecord E (s, false) = representedRecord E (s, true) := by
  refine ⟨fun _ => rfl, ?_, uncoupledCenter_records_equal F E s false true⟩
  intro h
  have hbit : false = true := congrArg Prod.snd h
  cases hbit
