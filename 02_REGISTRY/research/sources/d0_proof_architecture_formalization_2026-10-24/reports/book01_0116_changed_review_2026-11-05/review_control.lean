import D0.Foundation.FutureShortlexAdapter
import D0.Foundation.VerificationCore

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerificationCore
open D0.Foundation.VerifiabilityNecessity


#check SigmaWitness.delta_dmin_iff
#check SigmaWitness.coded_verification_core
#check SigmaWitness.archiveCode_eq_iff
#check SigmaWitness.query_archive
#check D0.Foundation.FutureShortlexAdapter.hiddenBit_current_same_but_codes_different
#print axioms SigmaWitness.delta_dmin_iff
#print axioms SigmaWitness.coded_verification_core
#print axioms SigmaWitness.archiveCode_eq_iff
#print axioms SigmaWitness.query_archive
#print axioms D0.Foundation.FutureShortlexAdapter.hiddenBit_current_same_but_codes_different

-- A changed profile yields the comparison while the independently supplied
-- archive may still be empty. This is a logical control, not a physical model.
example {F : FutureExecution} (E : TheoryVerification F.futureEmpiricalTheory)
    (W : SigmaWitness E) (s t : F.State) (h : F.profile s ≠ F.profile t) :
    W.coding.delta (W.dmin s) (W.dmin t) = true ∧
      W.archive ([] : List (F.State × E.protocol.Line)) = [] := by
  exact ⟨(W.delta_dmin_iff s t).2 h, rfl⟩
