import D0.Matter.FiniteSelector
import Mathlib.Tactic

/-!
# D0-M1-PREDICATE-001 — M1 as a formal proof-theoretic predicate (the integration keystone)

**M1 is not a D0-axiom or a finitist preference — it is proof-theoretic rigor.** A complete proof may
not depend on an unprovable input: a chain `A → B → C` is not a proof if `A` is postulated from thin
air, however cleanly `B, C` follow from it. In D0 terms, an *exogenous parameter / external catalogue*
is **exactly that-which-cannot-be-proven** from the canonical finite data — an obligatory choice not
determined by the finite distinguishability code.

This module makes that principle a reusable, **proven** Lean predicate (no new axiom, no `sorry`): it
generalizes the already-proven `D0.Matter.FiniteSelector` / `StrictSelected` uniqueness spine into an
abstract *forced-answer* predicate `M1Forced`, whose two core lemmas are the reductio engine the
§24–§30 millennium reformulations instantiate:

* `m1_forced_unique` — the canonical finite data forces **at most one** admissible answer;
* `m1_alternative_needs_catalogue` — once the answer is forced, **any** alternative fails the canonical
  constraint, i.e. selecting it would require data beyond the finite code (an external catalogue =
  an unprovable input). This is the formal `¬conclusion ⇒ exogenous parameter` step.

`M1Forced` subsumes the selector form (`StrictSelected` = strict score-minimum), the forced-value form
(unique solution of a canonical constraint), and the fixed-point/uniqueness forms used downstream.
-/

namespace D0.Foundation

open D0.Matter

/-- **M1-forced answer.** `a` is M1-forced by a canonical finite constraint `Forced : α → Prop` when
`a` satisfies it and it is the *unique* such candidate. Reading: the canonical finite data determines
`a`; nothing outside the finite code is needed. -/
structure M1Forced {α : Type} (Forced : α → Prop) (a : α) : Prop where
  /-- the canonical constraint holds at the answer -/
  forced : Forced a
  /-- the answer is the unique witness — no exogenous choice between alternatives -/
  unique : ∀ b, Forced b → b = a

/-- **Requires an external catalogue (= an unprovable input).** A candidate `b` requires an external
catalogue (relative to the canonical constraint `Forced`) when it does *not* satisfy the constraint —
so asserting `b` as the answer rests on data not derivable from the finite code. -/
def RequiresExternalCatalogue {α : Type} (Forced : α → Prop) (b : α) : Prop := ¬ Forced b

/-- **M1 uniqueness.** The canonical finite data forces at most one admissible answer: two M1-forced
answers are equal. (No two distinct "provable from the finite code" answers can coexist.) -/
theorem m1_forced_unique {α : Type} {Forced : α → Prop} {a b : α}
    (ha : M1Forced Forced a) (hb : M1Forced Forced b) : a = b :=
  (ha.unique b hb.forced).symm

/-- **M1 reductio (the load-bearing step for §24–§30).** Once the answer `a` is M1-forced, any
alternative `b ≠ a` requires an external catalogue — it fails the canonical constraint, so selecting
it would depend on an unprovable input. This is the formal `¬conclusion ⇒ exogenous parameter ⇒ ⊥`. -/
theorem m1_alternative_needs_catalogue {α : Type} {Forced : α → Prop} {a : α}
    (ha : M1Forced Forced a) (b : α) (hb : b ≠ a) : RequiresExternalCatalogue Forced b := by
  intro hFb
  exact hb (ha.unique b hFb)

/-- An M1-forced answer is not itself an external catalogue (admissibility ↔ ¬catalogue at the answer). -/
theorem m1_forced_not_catalogue {α : Type} {Forced : α → Prop} {a : α}
    (ha : M1Forced Forced a) : ¬ RequiresExternalCatalogue Forced a := by
  intro h; exact h ha.forced

/-- **Selector bridge.** A strictly-selected candidate of a finite score selector is M1-forced by the
constraint `StrictSelected S ·` — reusing the proven `strict_selected_unique`. This connects the
abstract predicate to the existing CORE selector spine used across the Book-04 claims. -/
theorem selector_M1Forced {α : Type} (S : FiniteSelector α) (a : α)
    (ha : StrictSelected S a) : M1Forced (fun x => StrictSelected S x) a where
  forced := ha
  unique := fun b hb => strict_selected_unique S hb ha

/-- Non-vacuous witness: a concrete 2-candidate score selector whose minimum (`0`) is M1-forced, and
the alternative (`1`) provably requires an external catalogue. -/
def demoSelector : FiniteSelector (Fin 2) where
  support_fintype := inferInstance
  score i := (i.val : ℚ)

theorem demo_zero_strictly_selected : StrictSelected demoSelector 0 := by
  refine ⟨fun b hb => ?_⟩
  fin_cases b
  · exact absurd rfl hb
  · norm_num [demoSelector]

theorem demo_zero_m1_forced : M1Forced (fun x => StrictSelected demoSelector x) 0 :=
  selector_M1Forced demoSelector 0 demo_zero_strictly_selected

theorem demo_one_needs_catalogue :
    RequiresExternalCatalogue (fun x => StrictSelected demoSelector x) 1 :=
  m1_alternative_needs_catalogue demo_zero_m1_forced 1 (by decide)

end D0.Foundation
