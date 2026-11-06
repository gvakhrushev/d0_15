import D0.Foundation.UncoupledCenterRawWitness

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerificationCore
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.UncoupledCenterRawWitness

#check FutureExecution.uncoupledCenter_profile_independent
#check uncoupledCenter_records_equal
#check SigmaWitness.dmin_eq_iff
#check distinct_raw_same_future
#check distinct_raw_same_future_and_record
#check concrete_distinct_raw_same_future_and_record
#print axioms FutureExecution.uncoupledCenter_profile_independent
#print axioms uncoupledCenter_records_equal
#print axioms SigmaWitness.dmin_eq_iff
#print axioms distinct_raw_same_future
#print axioms distinct_raw_same_future_and_record
#print axioms concrete_distinct_raw_same_future_and_record

-- F, its verification E and code witness W are supplied independently.
-- Different raw states may have identical codes in this abstract interface.
example (F : FutureExecution) (s : F.State)
    (E : TheoryVerification F.uncoupledCenter.futureEmpiricalTheory)
    (W : SigmaWitness E) :
    ∃ x y : F.uncoupledCenter.State, x ≠ y ∧
      F.uncoupledCenter.profile x = F.uncoupledCenter.profile y ∧
      W.dmin x = W.dmin y := by
  obtain ⟨x, y, hne, hprofile, _⟩ := distinct_raw_same_future_and_record F s E
  exact ⟨x, y, hne, hprofile, (W.dmin_eq_iff x y).2 hprofile⟩
