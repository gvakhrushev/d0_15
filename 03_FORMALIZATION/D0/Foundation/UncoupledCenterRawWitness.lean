import D0.Foundation.VerificationCore
import D0.Foundation.VerificationTransferApplication

/-!
# Raw states and observational equivalence

This finite countermodel witnesses the distinction needed to interpret Book01
§01.1.6. It uses the existing future-profile and verified-record constructions;
it does not assert that this interface is an admitted physical D0 execution or
decide the original GOLDEN theorem's physical and ontological premises.
-/

namespace D0.Foundation.UncoupledCenterRawWitness

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerificationCore
open D0.Foundation.VerifiabilityNecessity

/-- A one-state execution with one possible action, test, and outcome. -/
def unitExecution : FutureExecution where
  State := Unit
  Action := Unit
  Test := Unit
  Outcome := Unit
  step := fun _ s => s
  observe := fun _ _ => ()

/-- Two different raw states coincide under every allowed future experiment. -/
theorem distinct_raw_same_future :
    ∃ x y : unitExecution.uncoupledCenter.State,
      x ≠ y ∧ unitExecution.uncoupledCenter.profile x =
        unitExecution.uncoupledCenter.profile y := by
  refine ⟨((), false), ((), true), ?_, ?_⟩
  · intro h
    have hbit : false = true := congrArg Prod.snd h
    cases hbit
  · exact unitExecution.uncoupledCenter_profile_independent () false true

/-- With the representation explicitly supplied, the same raw pair has one record. -/
theorem distinct_raw_same_future_and_record
    (F : FutureExecution) (s : F.State)
    (E : TheoryVerification F.uncoupledCenter.futureEmpiricalTheory) :
    ∃ x y : F.uncoupledCenter.State,
      x ≠ y ∧ F.uncoupledCenter.profile x =
          F.uncoupledCenter.profile y ∧
        representedRecord E x = representedRecord E y := by
  refine ⟨(s, false), (s, true), ?_, ?_, ?_⟩
  · intro h
    have hbit : false = true := congrArg Prod.snd h
    cases hbit
  · exact F.uncoupledCenter_profile_independent s false true
  · exact uncoupledCenter_records_equal F E s false true

/-- An existing nontrivial verification supplies an actual represented example. -/
theorem concrete_distinct_raw_same_future_and_record :
    ∃ x y : D0.Foundation.TheoryTransfer.visibleBitSystem.State,
      x ≠ y ∧ D0.Foundation.TheoryTransfer.visibleBitSystem.profile x =
          D0.Foundation.TheoryTransfer.visibleBitSystem.profile y ∧
        representedRecord
            D0.Foundation.VerificationTransferApplication.visibleBitVerification x =
          representedRecord
            D0.Foundation.VerificationTransferApplication.visibleBitVerification y := by
  refine ⟨(false, false), (false, true), ?_, ?_, ?_⟩
  · intro h
    have hbit : false = true := congrArg Prod.snd h
    cases hbit
  · exact D0.Foundation.TheoryTransfer.visibleBit_same_all_source_futures
  · exact D0.Foundation.VerificationTransferApplication.visibleBit_records_follow_complete_future_equivalence

end D0.Foundation.UncoupledCenterRawWitness
