import D0.Condensed.ProfiniteSupport

namespace D0

structure AdmissibleSubfunctor (S : ProjectiveSystem) where
  predicate : ∀ n, S.Stage n → Prop
  stable : ∀ {m n : ℕ} (h : n ≤ m) (x : S.Stage m), predicate m x → predicate n (S.proj h x)

end D0
