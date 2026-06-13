namespace D0.Bridge

namespace BridgeAssumption

structure HeatTraceWeylAssumptions where
  heatTraceConverges : Prop
  fourDimensionalWeyl : Prop
  lorentzSignature : Prop
  convergenceProof : heatTraceConverges
  weylProof : fourDimensionalWeyl
  signatureProof : lorentzSignature

end BridgeAssumption

abbrev HeatTraceWeylAssumptions :=
  BridgeAssumption.HeatTraceWeylAssumptions

end D0.Bridge
