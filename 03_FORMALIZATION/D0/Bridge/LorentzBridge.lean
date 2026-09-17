import D0.Algebra.LieCarrierFinite

namespace D0.Bridge

namespace BridgeAssumption

structure LorentzBridgeAssumptions where
  macroLimitExists : Prop
  spinCoverIntegrates : Prop
  macroLimitProof : macroLimitExists
  spinProof : spinCoverIntegrates

end BridgeAssumption

abbrev LorentzBridgeAssumptions :=
  BridgeAssumption.LorentzBridgeAssumptions

theorem lorentz_bridge_promoted (h : LorentzBridgeAssumptions) :
    h.macroLimitExists ∧ h.spinCoverIntegrates :=
  ⟨h.macroLimitProof, h.spinProof⟩

end D0.Bridge
