import D0.Condensed.ProfiniteSupport

namespace D0

structure CompatibleOperatorFamily (S : ProjectiveSystem) where
  op : ∀ n, S.Stage n → S.Stage n
  natural : ∀ {m n : ℕ} (h : n ≤ m) (x : S.Stage m),
    S.proj h (op m x) = op n (S.proj h x)

def inducedLimitOperator {S : ProjectiveSystem} (F : CompatibleOperatorFamily S)
    (x : ProfinitePoint S) : ProfinitePoint S where
  val n := F.op n (x.val n)
  compatible := by
    intro m n h
    rw [F.natural h, x.compatible h]

end D0
