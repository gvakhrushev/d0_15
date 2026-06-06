import D0.Geometry.ArchiveFiberGraph
import D0.Geometry.ArchiveDirichletEnergy

namespace D0

structure ArchiveLocalQuadraticForm (n : Nat) where
  Q : (archiveFiberGraph n).V → (archiveFiberGraph n).V → Real
  symmetric : ∀ a b, Q a b = Q b a
  nonnegative : ∀ f : (archiveFiberGraph n).V → Real, 0 ≤ graphQuadraticForm (archiveFiberGraph n) Q f
  local_on_fiber_graph : ∀ u v, ¬ (archiveFiberGraph n).adj u v → u ≠ v → Q u v = 0
  projection_compatible : Prop
  constant_mode_zero : ∀ f : (archiveFiberGraph n).V → Real, (∀ u v, f u = f v) → graphQuadraticForm (archiveFiberGraph n) Q f = 0

end D0
