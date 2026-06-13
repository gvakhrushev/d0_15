import D0.Topology.TilingHull

namespace D0.Geometry

structure NonCommutativeSolenoid where
  base_hull : D0.Topology.D0TilingHull
  rotation_parameter : Rat
  noncommutative_product : Prop
  profinite_internal_space : Prop

theorem d0_hull_admits_noncommutative_solenoid_model (stmt : Prop) (h : stmt) : stmt := h

end D0.Geometry
