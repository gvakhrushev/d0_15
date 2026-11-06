import D0.Foundation.VerificationCore

open D0.Foundation.VerifiabilityNecessity
open D0.Foundation.VerificationCore

#check VerificationContract.correct
#check verification_lines_agree
#check representedComparison_catalogue_independent
#check privileged_catalogue_can_distinguish
#check privileged_catalogue_is_outcome_affecting
#check necessary_role_outsourced_loses_verifiability
#print axioms verification_lines_agree
#print axioms representedComparison_catalogue_independent
#print axioms privileged_catalogue_can_distinguish
#print axioms privileged_catalogue_is_outcome_affecting
#print axioms necessary_role_outsourced_loses_verifiability

example (l : privilegedCatalogueProtocol.Line) :
    privilegedCatalogueProtocol.compare l false
      (privilegedCatalogueProtocol.record false) (privilegedCatalogueProtocol.record true) = false ∧
    privilegedCatalogueProtocol.compare l true
      (privilegedCatalogueProtocol.record false) (privilegedCatalogueProtocol.record true) = true := by
  constructor <;> rfl
