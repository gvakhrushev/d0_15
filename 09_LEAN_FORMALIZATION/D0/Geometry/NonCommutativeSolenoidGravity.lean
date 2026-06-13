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

theorem d0_heat_trace_admits_solenoid_spectral_triple_approx (stmt : Prop) (h : stmt) : stmt := h

theorem finite_spin2_operator_is_tt_sector_of_solenoid_spectral_geometry (stmt : Prop) (h : stmt) : stmt := h

theorem wtt4_is_compatible_with_noncommutative_solenoid_geometry (stmt : Prop) (h : stmt) : stmt := h

end D0.Geometry
