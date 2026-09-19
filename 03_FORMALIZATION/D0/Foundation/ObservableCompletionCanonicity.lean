import D0.Foundation.M1Predicate
import Mathlib.Tactic

/-!
# D0.Foundation.ObservableCompletionCanonicity

Theoretical owner: `D0-OBSERVABLE-COMPLETION-CANONICITY-001`.

Formalization of the fundamental canonicity principle:
"All admissible completions give the same observable ↔ the observable is M1-forced".

In D0, equivariance alone does not imply uniqueness (`equivariant ⇏ unique`),
since multiple distinct objects can share the exact same equivariance properties.
Instead, canonicity is structured by:
1. An admissible completion class `Admissible : C → Prop`;
2. An observable evaluation map `readout : C → O`;
3. The predicate `CompletionForcesReadout Admissible readout o : Prop` asserting
   that every admissible completion produces observable value `o`.

Main results:
* `constant_readout_m1_forced`: If `Admissible c₀` and all admissible completions
  agree on `readout c₀`, then `readout c₀` is `M1Forced`.
* `distinct_readouts_no_m1_forced`: If two admissible completions produce distinct
  readouts, no readout value can be `M1Forced` (abstract two-completion no-go).
* `observable_canonicity_criterion`: Given at least one admissible completion,
  an observable is `M1Forced` if and only if all admissible completions yield
  the identical readout.
* `readout_separates_object_uniqueness`: When the readout separates admissible
  completions (`ReadoutSeparates`), forcing the observable elevates to uniqueness
  of the completion itself (`Subsingleton {c // Admissible c}`).
-/

namespace D0.Foundation.ObservableCompletionCanonicity

open D0.Foundation

variable {C O : Type}

/-- Every admissible completion produces the exact observable value `o`. -/
def CompletionForcesReadout
    (Admissible : C → Prop) (readout : C → O) (o : O) : Prop :=
  ∀ c, Admissible c → readout c = o

/-- **Theorem 1: Constant readout ⇒ M1-forced observable.**
When there exists at least one admissible completion `c₀` and all admissible
completions evaluate to `readout c₀`, the observable `readout c₀` is `M1Forced`. -/
theorem constant_readout_m1_forced
    (Admissible : C → Prop) (readout : C → O) (c₀ : C)
    (hc₀ : Admissible c₀)
    (hconst : ∀ c, Admissible c → readout c = readout c₀) :
    M1Forced
      (CompletionForcesReadout Admissible readout)
      (readout c₀) where
  forced := hconst
  unique := by
    intro o ho
    -- Since ho forces all admissible completions to evaluate to o,
    -- evaluating at c₀ gives readout c₀ = o.
    have h_at_c₀ : readout c₀ = o := ho c₀ hc₀
    exact h_at_c₀.symm

/-- **Theorem 2: Two distinct observable completions ⇒ NO M1 forcing.**
Abstract form of all TWO-COMPLETION-NOGO theorems in D0.
If two admissible completions produce distinct observables, then no observable
value is M1-forced under `CompletionForcesReadout`. -/
theorem distinct_readouts_no_m1_forced
    (Admissible : C → Prop) (readout : C → O)
    {a b : C}
    (ha : Admissible a)
    (hb : Admissible b)
    (hne : readout a ≠ readout b) :
    ¬ ∃ o,
      M1Forced
        (CompletionForcesReadout Admissible readout)
        o := by
  intro ⟨o, ho⟩
  have hoa : readout a = o := ho.forced a ha
  have hob : readout b = o := ho.forced b hb
  have heq : readout a = readout b := by rw [hoa, hob]
  exact hne heq

/-- **Theorem 3: Exact canonicity criterion.**
Assuming at least one admissible completion exists (`∃ c, Admissible c`),
an observable value is M1-forced if and only if all pairs of admissible
completions yield identical readouts. -/
theorem observable_canonicity_criterion
    (Admissible : C → Prop) (readout : C → O)
    (hex : ∃ c, Admissible c) :
    (∃ o, M1Forced (CompletionForcesReadout Admissible readout) o) ↔
    (∀ a b, Admissible a → Admissible b → readout a = readout b) := by
  constructor
  · rintro ⟨o, ho⟩ a b ha hb
    have hoa : readout a = o := ho.forced a ha
    have hob : readout b = o := ho.forced b hb
    rw [hoa, hob]
  · intro hconst
    rcases hex with ⟨c₀, hc₀⟩
    have h_c₀_forced : ∀ c, Admissible c → readout c = readout c₀ := by
      intro c hc
      exact hconst c c₀ hc hc₀
    exact ⟨readout c₀, constant_readout_m1_forced Admissible readout c₀ hc₀ h_c₀_forced⟩

/-- Injectivity / separation property: the readout map distinguishes distinct
admissible completions. -/
def ReadoutSeparates
    (Admissible : C → Prop) (readout : C → O) : Prop :=
  ∀ a b, Admissible a → Admissible b → readout a = readout b → a = b

/-- **Theorem 4: Lifting observable canonicity to object uniqueness.**
If the observable is M1-forced and the readout separates admissible completions,
then the subtype `{c // Admissible c}` is a subsingleton (unique completion). -/
theorem readout_separates_object_uniqueness
    (Admissible : C → Prop) (readout : C → O)
    (h_sep : ReadoutSeparates Admissible readout)
    (h_forced : ∃ o, M1Forced (CompletionForcesReadout Admissible readout) o) :
    Subsingleton {c : C // Admissible c} := by
  constructor
  rintro ⟨a, ha⟩ ⟨b, hb⟩
  rcases h_forced with ⟨o, ho⟩
  have hoa : readout a = o := ho.forced a ha
  have hob : readout b = o := ho.forced b hb
  have h_readout_eq : readout a = readout b := by rw [hoa, hob]
  have hab : a = b := h_sep a b ha hb h_readout_eq
  exact Subtype.ext hab

/-- Complete foundational summary for `D0-OBSERVABLE-COMPLETION-CANONICITY-001`. -/
theorem observable_completion_canonicity_summary :
    (∀ (Admissible : C → Prop) (readout : C → O) (c₀ : C)
       (hc₀ : Admissible c₀)
       (hconst : ∀ c, Admissible c → readout c = readout c₀),
       M1Forced (CompletionForcesReadout Admissible readout) (readout c₀)) ∧
    (∀ (Admissible : C → Prop) (readout : C → O) (a b : C)
       (ha : Admissible a) (hb : Admissible b) (hne : readout a ≠ readout b),
       ¬ ∃ o, M1Forced (CompletionForcesReadout Admissible readout) o) ∧
    (∀ (Admissible : C → Prop) (readout : C → O) (hex : ∃ c, Admissible c),
       (∃ o, M1Forced (CompletionForcesReadout Admissible readout) o) ↔
       (∀ a b, Admissible a → Admissible b → readout a = readout b)) := by
  refine ⟨fun Admissible readout c₀ hc₀ hconst => constant_readout_m1_forced Admissible readout c₀ hc₀ hconst,
          fun Admissible readout a b ha hb hne => distinct_readouts_no_m1_forced Admissible readout ha hb hne,
          fun Admissible readout hex => observable_canonicity_criterion Admissible readout hex⟩

end D0.Foundation.ObservableCompletionCanonicity
