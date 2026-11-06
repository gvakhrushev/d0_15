import D0.Foundation.VerificationCore
import Mathlib.Data.List.Shortlex
import Mathlib.Data.Fintype.Card
import Mathlib.Order.WellFounded

/-!
# Existence of shortlex-minimal codes

For a well-founded linearly ordered alphabet, every nonempty set of finite
words has a least word in the book's length-then-lexicographic order. In
particular, a finite linearly ordered alphabet has this property.

The application below fills the minimality field of `CodePresentation` for
any supplied decoder with a nonempty fibre for every object. The chosen
encoding is noncomputable in general. No algorithm deciding equivalence,
computable encoder, physically selected alphabet or single code ontology is
derived here.
-/

namespace D0.Foundation.VerificationCore

/-- A nonempty set of finite words has a least word in shortlex order whenever
the strict order on letters is well-founded. -/
theorem exists_shortlex_minimal_word {Symbol : Type} [LinearOrder Symbol]
    [WellFoundedLT Symbol] (P : List Symbol → Prop) (hne : ∃ c, P c) :
    ∃ m, P m ∧ ∀ c, P c → ShortlexLE m c := by
  classical
  have hwf : WellFounded (List.Shortlex (fun a b : Symbol => a < b)) :=
    List.Shortlex.wf wellFounded_lt
  obtain ⟨m, hm, hmin⟩ := hwf.has_min {c | P c} hne
  refine ⟨m, hm, ?_⟩
  intro c hc
  have htri : List.Shortlex (fun a b : Symbol => a < b) m c ∨ m = c ∨
      List.Shortlex (fun a b : Symbol => a < b) c m :=
    trichotomous_of _ m c
  rcases htri with hlt | rfl | hgt
  · rcases List.shortlex_def.mp hlt with hlen | ⟨hlen, hlex⟩
    · exact Or.inl hlen
    · exact Or.inr ⟨hlen, Or.inr hlex⟩
  · exact Or.inr ⟨rfl, Or.inl rfl⟩
  · exact False.elim (hmin c hc hgt)

/-- The source's finite-alphabet case is a specialization of the general
well-founded result. No decidability of the set of words is required. -/
theorem exists_finite_alphabet_shortlex_minimal_word {Symbol : Type}
    [LinearOrder Symbol] [Finite Symbol] (P : List Symbol → Prop)
    (hne : ∃ c, P c) : ∃ m, P m ∧ ∀ c, P c → ShortlexLE m c :=
  exists_shortlex_minimal_word P hne

namespace CodePresentation

/-- A supplied decoder with a nonempty fibre for each object admits a
shortlex-minimal code presentation. This chooses codes classically and makes
no computability claim. -/
noncomputable def ofSurjectiveDecode {Symbol Object : Type}
    [LinearOrder Symbol] [WellFoundedLT Symbol]
    (decode : List Symbol → Option Object)
    (hdecode : ∀ x, ∃ c, decode c = some x) : CodePresentation Symbol Object := by
  classical
  let minimal (x : Object) :=
    exists_shortlex_minimal_word (fun c => decode c = some x) (hdecode x)
  refine {
    encode := fun x => Classical.choose (minimal x)
    decode := decode
    decode_encode := ?_
    shortlex_minimal := ?_ }
  · intro x
    exact (Classical.choose_spec (minimal x)).1
  · intro x c hc
    exact (Classical.choose_spec (minimal x)).2 c hc

end CodePresentation

/-- Concrete application to an arbitrary supplied decoder over a finite
alphabet. A nonempty fibre is required for each represented object. -/
theorem finite_alphabet_code_presentation_exists {Symbol Object : Type}
    [LinearOrder Symbol] [Finite Symbol]
    (decode : List Symbol → Option Object)
    (hdecode : ∀ x, ∃ c, decode c = some x) :
    ∃ K : CodePresentation Symbol Object, K.decode = decode := by
  let K := CodePresentation.ofSurjectiveDecode decode hdecode
  exact ⟨K, rfl⟩

end D0.Foundation.VerificationCore
