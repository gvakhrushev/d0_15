import Mathlib.Tactic

/-!
# D0-COMPLETION-ADMISSIBILITY-001 — the strengthened 5-item two-completion standard (Section 0)

A two-completion no-go witness is VALID only if all five items hold:
1. a precise admissible class `C_X`;
2. two explicit completions `E_A, E_B ∈ C_X`;
3. a frozen observable `O_X` with `O_X(E_A) ≠ O_X(E_B)`;
4. both completions preserve every prior owner / finite readout rule / symmetry / terminal projection;
5. either (a) an exhaustion theorem for `C_X`, or (b) a local universal-property theorem (no quotient /
   natural transformation / canonical equivalence identifies `E_A` and `E_B`).

Without item 4 the witness may be inadmissible; without item 5 it proves only that two examples differ.
-/

namespace D0.Extensions.CompletionAdmissibility

/-- The five checkable items of a two-completion witness, plus whether item-5a (exhaustion of the WHOLE class)
holds (vs only a scoped universal-property). -/
structure CompletionWitness where
  hasClass : Bool            -- item 1
  twoCompletions : Bool      -- item 2
  observableSeparates : Bool -- item 3
  preservesOwners : Bool     -- item 4
  item5 : Bool               -- item 5 (exhaustion OR universal-property holds, possibly scoped)
  exhaustionWhole : Bool     -- item 5a holds for the ENTIRE admissible class (=> full maximality)

/-- A witness is VALID iff all five items hold. -/
def valid (w : CompletionWitness) : Prop :=
  w.hasClass ∧ w.twoCompletions ∧ w.observableSeparates ∧ w.preservesOwners ∧ w.item5

/-- Decidable validity. -/
def validB (w : CompletionWitness) : Bool :=
  w.hasClass && w.twoCompletions && w.observableSeparates && w.preservesOwners && w.item5

theorem valid_iff_validB (w : CompletionWitness) : valid w ↔ validB w = true := by
  unfold valid validB; simp [Bool.and_eq_true, and_assoc]

/-- **Item 4 is necessary**: a witness failing owner-preservation is invalid. -/
theorem item4_necessary {w : CompletionWitness} (h : w.preservesOwners = false) : ¬ valid w := by
  rw [valid_iff_validB, validB, h]; simp

/-- **Item 5 is necessary**: a witness with no exhaustion/universal-property is invalid (two examples differing
is not structural nonuniqueness). -/
theorem item5_necessary {w : CompletionWitness} (h : w.item5 = false) : ¬ valid w := by
  rw [valid_iff_validB, validB, h]; simp

/-- A fully-specified valid witness with whole-class exhaustion. -/
def exemplarFull : CompletionWitness := ⟨true, true, true, true, true, true⟩
theorem exemplar_valid : valid exemplarFull := by rw [valid_iff_validB]; rfl

end D0.Extensions.CompletionAdmissibility
