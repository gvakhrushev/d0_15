import Mathlib.Data.Matrix.Basic

namespace D0

structure IncidencePair (m n k : ℕ) where
  d1 : Matrix (Fin m) (Fin n) ℤ
  d2 : Matrix (Fin n) (Fin k) ℤ
  compatible : d1 * d2 = 0

end D0
