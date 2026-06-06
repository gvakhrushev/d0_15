import D0.Condensed.ProjectiveSystem

namespace D0

structure ProfinitePoint (S : ProjectiveSystem) where
  val : ∀ n, S.Stage n
  compatible : ∀ {m n : ℕ} (h : n ≤ m), S.proj h (val m) = val n

theorem profinite_projection_compatible (S : ProjectiveSystem) (x : ProfinitePoint S)
    {m n : ℕ} (h : n ≤ m) : S.proj h (x.val m) = x.val n :=
  x.compatible h

end D0
