import D0.Foundation.ShortlexCodeExistence

/-!
# Canonical codes for supplied equivalence classes of words

For an arbitrary supplied setoid on finite words, use the shortlex existence
theorem to construct a code presentation of its quotient. The representative
is chosen classically, so neither the equivalence relation nor the canonical
representative is claimed computable. The setoid is an input: connecting it to
future-execution profiles requires a separate code/state map and proof.
-/

namespace D0.Foundation.VerificationCore

variable {Symbol : Type}

/-- The quotient map represents every quotient class. -/
def wordClassDecode (r : Setoid (List Symbol)) (c : List Symbol) :
    Option (Quotient r) := some (Quotient.mk r c)

theorem wordClassDecode_surjective (r : Setoid (List Symbol))
    (q : Quotient r) : ∃ c, wordClassDecode r c = some q := by
  induction q using Quotient.inductionOn with
  | _ c => exact ⟨c, rfl⟩

variable [LinearOrder Symbol] [WellFoundedLT Symbol]

/-- The code presentation of a supplied word equivalence. -/
noncomputable def wordClassPresentation (r : Setoid (List Symbol)) :
    CodePresentation Symbol (Quotient r) :=
  CodePresentation.ofSurjectiveDecode (wordClassDecode r) (wordClassDecode_surjective r)

/-- The selected representative lies in the original equivalence class. -/
theorem wordClass_canon_related (r : Setoid (List Symbol)) (c : List Symbol) :
    r.r ((wordClassPresentation r).canon c) c := by
  let K := wordClassPresentation r
  change r.r (K.encode (Quotient.mk r c)) c
  apply Quotient.exact
  have h := K.decode_encode (Quotient.mk r c)
  change some (Quotient.mk r (K.encode (Quotient.mk r c))) = some (Quotient.mk r c) at h
  exact Option.some.inj h

/-- The representative is no larger than any word in that same class. -/
theorem wordClass_canon_minimal (r : Setoid (List Symbol)) (c d : List Symbol)
    (h : r.r c d) : ShortlexLE ((wordClassPresentation r).canon c) d := by
  let K := wordClassPresentation r
  change ShortlexLE (K.encode (Quotient.mk r c)) d
  apply K.shortlex_minimal
  change some (Quotient.mk r d) = some (Quotient.mk r c)
  exact congrArg some (Quotient.sound h).symm

/-- Exactly the words in the same supplied class have the same canonical code. -/
theorem wordClass_canon_eq_iff (r : Setoid (List Symbol)) (c d : List Symbol) :
    (wordClassPresentation r).canon c = (wordClassPresentation r).canon d ↔ r.r c d := by
  let K := wordClassPresentation r
  change K.encode (Quotient.mk r c) = K.encode (Quotient.mk r d) ↔ r.r c d
  constructor
  · intro h
    exact Quotient.exact (K.encode_injective h)
  · intro h
    exact congrArg K.encode (Quotient.sound h)

/-- Nontrivial example: distinct one-bit words are equivalent by equal length
and therefore receive the same canonical code. This is a mathematical example,
not a selection of a physical observational equivalence. -/
theorem equal_length_distinct_codes_share_canon :
    (wordClassPresentation (Setoid.ker (List.length : List Bool → Nat))).canon [true] =
      (wordClassPresentation (Setoid.ker (List.length : List Bool → Nat))).canon [false] ∧
    ([true] : List Bool) ≠ [false] := by
  constructor
  · exact (wordClass_canon_eq_iff _ _ _).2 rfl
  · decide

end D0.Foundation.VerificationCore
