import D0.Geometry.NonCommutativeSolenoid

namespace D0.Geometry

structure SpectralTripleApprox where
  algebra : Type
  hilbert_carrier : Type
  dirac_operator : Type
  bounded_commutators : Prop
  finite_approximant : Prop

structure D0SolenoidSpectralGeometry where
  solenoid : NonCommutativeSolenoid
  spectral_triple : SpectralTripleApprox
  heat_trace_owner : Prop
  tt_operator_owner : Prop


end D0.Geometry
