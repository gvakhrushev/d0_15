import D0.Foundation.ArchivePairCapacity

open D0.Foundation.VerificationCore
open D0.Foundation.ArchivePairCapacity

#check finiteSigmaWitness
#check singletonCodePresentation
#check singletonCodePresentation_canon
#check singletonCodePresentation_canonical_computable
#check singletonCodePresentation_comparison_computable
#check visibleArchiveWitness
#check visibleArchive_bound_attained
#print axioms finiteSigmaWitness
#print axioms singletonCodePresentation_canon
#print axioms singletonCodePresentation_canonical_computable
#print axioms singletonCodePresentation_comparison_computable
#print axioms visibleArchiveWitness
#print axioms visibleArchive_bound_attained

-- Empty list is fixed by this canonizer but is not a decodable code.
example {Object : Type} {n : Nat} (e : Object ≃ Fin n) :
    (singletonCodePresentation e).decode [] = none ∧
      (singletonCodePresentation e).canon [] = [] := by
  constructor <;> rfl
