import D0.Foundation.TheoryTransfer
open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.VerificationCore
open D0.Foundation.TheoryTransfer
example {F G : FutureExecution} (I : Interpretation F G)
    (E : TheoryVerification F.futureEmpiricalTheory) (s : F.State) :
    I.verifiedStateImageEquiv E (representedState E s) =
      I.imageEquiv (Quotient.mk F.futureSetoid s) := by
  apply Subtype.ext
  have h := I.verifiedRun_image E [] s
  change (I.verifiedStateImageEquiv E (representedState E s)).val =
    Quotient.mk I.commonExecution.futureSetoid (I.stateMap s) at h
  exact h
