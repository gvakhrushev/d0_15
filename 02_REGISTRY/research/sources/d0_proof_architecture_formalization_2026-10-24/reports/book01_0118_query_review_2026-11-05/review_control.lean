import D0.Foundation.VerificationCore

open D0.Foundation.EmpiricalTheoryFactorization
open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.VerificationCore

#check SigmaWitness.query
#check SigmaWitness.query_computable
#check SigmaWitness.query_archive
#check SigmaWitness.query_append_retains
#check SigmaWitness.coded_verification_core
#print axioms SigmaWitness.query_computable
#print axioms SigmaWitness.query_archive
#print axioms SigmaWitness.query_append_retains
#print axioms SigmaWitness.coded_verification_core

-- A previously missing position is not protected by the append theorem:
-- appending creates a value at that position. This is a list control only.
example {F : FutureExecution} {E : TheoryVerification F.futureEmpiricalTheory}
    (W : SigmaWitness E) (c : List W.Symbol) :
    W.query [] 0 = none ∧ W.query ([] ++ [c]) 0 = some c := by
  constructor <;> rfl
