namespace D0.Bridge

namespace BridgeAssumption

structure SmoothInterpolationAssumptions where
  Coupling : Type
  scale : ℤ → ℝ
  beta : Coupling → Coupling
  interpolation_exists : Prop
  interpolation_valid : interpolation_exists

end BridgeAssumption

abbrev SmoothInterpolationAssumptions :=
  BridgeAssumption.SmoothInterpolationAssumptions

end D0.Bridge
