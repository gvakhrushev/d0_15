import D0.Geometry.CovarianceTower

namespace D0

structure HasSpectralDimension
    (stages : Nat -> FiniteSpectralStage) (d : Real) : Prop where
  stableScalingWindow : True
  noSpectralPollution : True
  dimensionValue : d = 4

def D0SpectralDimensionFourProved : Prop := False

theorem D0_spectral_dimension_four_not_proved :
    ¬ D0SpectralDimensionFourProved := by
  intro h
  exact h

end D0
