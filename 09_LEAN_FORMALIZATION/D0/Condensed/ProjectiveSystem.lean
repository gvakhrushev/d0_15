import Mathlib.Data.Fintype.Basic
import Mathlib.Order.Basic

namespace D0

structure ProjectiveSystem where
  Stage : ℕ → Type
  finite : ∀ n, Fintype (Stage n)
  proj : ∀ {m n : ℕ}, n ≤ m → Stage m → Stage n
  proj_id : ∀ n (x : Stage n), proj (m := n) (n := n) (le_refl n) x = x

end D0
