import D0.Extensions.CompletionAdmissibility
import Mathlib.Tactic

/-!
# D0-TWO-COMPLETION-NOGO-STRENGTH-001 — no-go strength classification (Section 0)

Every two-completion no-go witness is reclassified, under the strengthened standard, as exactly one of four
strengths. `classify` is a total decidable function of the witness fields:
- `invalidWitness` — items 1–4 not all met (no well-formed admissible witness, e.g. a completion violates an owner);
- `witnessOnly` — items 1–4 hold but no item-5 exhaustion/universal-property (two examples differ, nothing more);
- `fullMaximality` — item-5a exhaustion holds for the ENTIRE admissible class;
- `classScoped` — item 5 holds only on a scoped subclass.
No status promotion occurs; this is a downgrade-allowed audit.
-/

namespace D0.Extensions.TwoCompletionNoGo

open D0.Extensions.CompletionAdmissibility

/-- The four admissible no-go strengths. -/
inductive NoGoStrength
  | fullMaximality
  | classScoped
  | witnessOnly
  | invalidWitness
  deriving DecidableEq, Repr

open NoGoStrength

/-- Items 1–4: a well-formed admissible witness (class, two completions, separating observable, owner-preserving). -/
def wellFormed (w : CompletionWitness) : Bool :=
  w.hasClass && w.twoCompletions && w.observableSeparates && w.preservesOwners

/-- `validB = wellFormed ∧ item5` (item 5 is the only piece beyond well-formedness). -/
theorem validB_eq_wf (w : CompletionWitness) : validB w = (wellFormed w && w.item5) := rfl

/-- Classify a witness by the strengthened standard (total, decidable). -/
def classify (w : CompletionWitness) : NoGoStrength :=
  if wellFormed w = false then invalidWitness
  else if w.item5 = false then witnessOnly
  else if w.exhaustionWhole then fullMaximality else classScoped

/-- An owner-violating witness is `invalidWitness`. -/
theorem classify_invalid {w : CompletionWitness} (h : w.preservesOwners = false) :
    classify w = invalidWitness := by
  have hwf : wellFormed w = false := by simp [wellFormed, h]
  simp [classify, hwf]

/-- A well-formed witness without whole-class exhaustion is `classScoped` (the typical post-core case). -/
theorem classify_class_scoped {w : CompletionWitness}
    (hwf : wellFormed w = true) (h5 : w.item5 = true) (hex : w.exhaustionWhole = false) :
    classify w = classScoped := by simp [classify, hwf, h5, hex]

/-- A well-formed witness with whole-class exhaustion is `fullMaximality`. -/
theorem classify_full {w : CompletionWitness}
    (hwf : wellFormed w = true) (h5 : w.item5 = true) (hex : w.exhaustionWhole = true) :
    classify w = fullMaximality := by simp [classify, hwf, h5, hex]

/-- A well-formed witness lacking item 5 is `witnessOnly`. -/
theorem classify_witness_only {w : CompletionWitness}
    (hwf : wellFormed w = true) (h5 : w.item5 = false) :
    classify w = witnessOnly := by simp [classify, hwf, h5]

/-- `fullMaximality` and `classScoped` both require a VALID witness (all five items). -/
theorem strong_classes_need_validity (w : CompletionWitness)
    (h : classify w = fullMaximality ∨ classify w = classScoped) : valid w := by
  have hwf : wellFormed w = true := by
    by_contra hc
    rw [Bool.not_eq_true] at hc
    have e : classify w = invalidWitness := by simp [classify, hc]
    rcases h with h | h
    · rw [e] at h; exact absurd h (by decide)
    · rw [e] at h; exact absurd h (by decide)
  have h5 : w.item5 = true := by
    by_contra hc
    rw [Bool.not_eq_true] at hc
    have e : classify w = witnessOnly := by simp [classify, hwf, hc]
    rcases h with h | h
    · rw [e] at h; exact absurd h (by decide)
    · rw [e] at h; exact absurd h (by decide)
  simp only [valid_iff_validB, validB_eq_wf, hwf, h5, Bool.and_true, Bool.true_and, Bool.and_self]

end D0.Extensions.TwoCompletionNoGo
