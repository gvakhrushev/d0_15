namespace D0.Bridge

namespace BridgeAssumption

structure ExternalHSTAssumptions where
  finiteSubgaussianSource : Prop
  externalTheoremApplies : Prop
  sourceProof : finiteSubgaussianSource
  theoremProof : externalTheoremApplies

end BridgeAssumption

abbrev ExternalHSTAssumptions :=
  BridgeAssumption.ExternalHSTAssumptions

end D0.Bridge
