import D0.Bridge.Assumptions.HeatTraceWeyl

namespace D0.Bridge

namespace BridgeAssumption

structure CovarianceSystem where
  compatible : Prop
  nondegenerate : Prop
  compatibleProof : compatible
  nondegenerateProof : nondegenerate

end BridgeAssumption

abbrev CovarianceSystem := BridgeAssumption.CovarianceSystem

theorem smooth_metric_bridge_conditional
    (C : CovarianceSystem) (H : HeatTraceWeylAssumptions) :
    C.compatible ∧ C.nondegenerate ∧ H.heatTraceConverges ∧
      H.fourDimensionalWeyl ∧ H.lorentzSignature :=
  ⟨C.compatibleProof, C.nondegenerateProof, H.convergenceProof, H.weylProof, H.signatureProof⟩

end D0.Bridge
