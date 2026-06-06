import D0.Bridge.Assumptions.ExternalHST

namespace D0.Bridge

theorem convex_response_bridge_conditional (h : ExternalHSTAssumptions) :
    h.finiteSubgaussianSource ∧ h.externalTheoremApplies :=
  ⟨h.sourceProof, h.theoremProof⟩

end D0.Bridge
