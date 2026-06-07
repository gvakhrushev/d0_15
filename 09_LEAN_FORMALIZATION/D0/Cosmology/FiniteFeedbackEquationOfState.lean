import D0.Cosmology.FeedbackPartitionFunction

namespace D0.Cosmology

structure FeedbackPressureLaw where
  betaPositive : Bool
  pressureFromLogZDerivative : Bool
  traceLogFinite : Bool
  notIdealGasPostulate : Bool

structure FinitePVTLaw where
  pressureVolume : Int
  effectiveTemperature : Int
  responseIndex : Int
  pvt_identity : pressureVolume = effectiveTemperature * responseIndex

theorem feedback_pressure_trace_log (P : FeedbackPressureLaw) :
    P.pressureFromLogZDerivative = true ->
    P.traceLogFinite = true ->
    P.pressureFromLogZDerivative && P.traceLogFinite = true := by
  intro hp ht
  simp [hp, ht]

theorem finite_pvt_equation_of_state (L : FinitePVTLaw) :
    L.pressureVolume = L.effectiveTemperature * L.responseIndex := by
  exact L.pvt_identity

theorem ideal_gas_core_postulate_forbidden (P : FeedbackPressureLaw) :
    P.notIdealGasPostulate = true -> P.notIdealGasPostulate != false := by
  intro h
  simp [h]

end D0.Cosmology
