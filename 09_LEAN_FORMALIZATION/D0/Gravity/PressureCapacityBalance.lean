import D0.Cosmology.FiniteFeedbackEquationOfState

namespace D0.Gravity

inductive PressureCapacityRegime where
  | expansion
  | stationaryHorizon
  | collapse
  deriving DecidableEq, Repr

def pressureCapacityRegime (pFb pCap : Int) : PressureCapacityRegime :=
  if pCap < pFb then PressureCapacityRegime.expansion
  else if pFb = pCap then PressureCapacityRegime.stationaryHorizon
  else PressureCapacityRegime.collapse

theorem pressure_capacity_balance_regimes :
    pressureCapacityRegime 3 2 = PressureCapacityRegime.expansion /\
    pressureCapacityRegime 2 2 = PressureCapacityRegime.stationaryHorizon /\
    pressureCapacityRegime 1 2 = PressureCapacityRegime.collapse := by
  simp [pressureCapacityRegime]

structure HorizonSaturation where
  nearCriticalFeedback : Bool
  capacityResistance : Bool

theorem horizon_saturation_feedback_limit (H : HorizonSaturation) :
    H.nearCriticalFeedback = true ->
    H.capacityResistance = true ->
    H.nearCriticalFeedback && H.capacityResistance = true := by
  intro hcrit hcap
  simp [hcrit, hcap]

structure A4TerminalCapacity where
  boundaryArea : Nat
  quarterUnits : Nat
  quarter_count : boundaryArea = 4 * quarterUnits

theorem a4_terminal_feedback_saturation (A : A4TerminalCapacity) :
    A.boundaryArea = 4 * A.quarterUnits := A.quarter_count

end D0.Gravity
