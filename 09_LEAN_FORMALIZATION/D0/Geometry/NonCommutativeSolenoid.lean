import D0.Topology.TilingHull

namespace D0.Geometry

structure NonCommutativeSolenoid where
  base_hull : D0.Topology.D0TilingHull
  rotation_parameter : Rat
  noncommutative_product : Prop
  profinite_internal_space : Prop


end D0.Geometry
