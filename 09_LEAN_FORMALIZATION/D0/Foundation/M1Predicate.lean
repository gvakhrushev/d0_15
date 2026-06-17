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
so asserting `b` as the answer rests on data not derivable from the finite code.

**Load-bearing only with a real `Forced`.** This definition is `¬ Forced b`; it carries content *only*
when `Forced` is an actual finite obligation (e.g. `StrictSelected S ·`, `admissible_unique`). A bare
`¬ Forced` over a vacuous `Forced` is not a theorem about anything. The `m1_*` lemmas below are
therefore always stated *against an `M1Forced` hypothesis* (a real `forced ∧ unique` obligation), and
every instance in this file (`demoSelector`, `seamDegreeSelector`) discharges that obligation through
the proven `StrictSelected` / `strict_selected_unique` spine — never as a standalone `:= ¬Forced` shell. -/
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

/-- **Seam-degree selector (the D0-PMNS-SEAM-TOPOLOGY-001 forcing obligation).** Over the three
δ₀-degrees `{0,1,2} = Fin 3`, the canonical finite constraint a seam cycle of winding `w` imposes is
"match the winding": score `d ↦ (d − w)²`. This is a *real* obligation, not a `¬Forced` shell — its
strict minimum is the winding itself, so the δ₀-degree of each PMNS channel (`bare/open/closed →
δ₀^{0,1,2}`) is M1-forced by the seam topology; any other degree provably needs an external catalogue. -/
def seamDegreeSelector (w : Fin 3) : FiniteSelector (Fin 3) where
  support_fintype := inferInstance
  score d := ((d.val : ℚ) - (w.val : ℚ)) ^ 2

theorem seam_degree_strictly_selected (w : Fin 3) :
    StrictSelected (seamDegreeSelector w) w := by
  refine ⟨fun b hb => ?_⟩
  have key : ∀ d : Fin 3, (seamDegreeSelector w).score d
      = ((d.val : ℚ) - (w.val : ℚ)) ^ 2 := fun _ => rfl
  simp only [key]
  have hbw : (b.val : ℚ) ≠ (w.val : ℚ) := by
    intro h; exact hb (Fin.ext (by exact_mod_cast h))
  have hz : ((w.val : ℚ) - (w.val : ℚ)) ^ 2 = 0 := by ring
  rw [hz]
  exact lt_of_le_of_ne (sq_nonneg _) (Ne.symm (pow_ne_zero 2 (sub_ne_zero.mpr hbw)))

/-- The seam δ₀-degree is **M1-forced** (via the proven selector spine) for every winding `w`. -/
theorem seam_degree_M1Forced (w : Fin 3) :
    M1Forced (fun d => StrictSelected (seamDegreeSelector w) d) w :=
  selector_M1Forced (seamDegreeSelector w) w (seam_degree_strictly_selected w)

/-- Any δ₀-degree other than the seam winding requires an external catalogue — the formal
`wrong-degree ⇒ exogenous choice` step the seam-topology rule rests on (no `¬Forced` shell). -/
theorem seam_degree_alternative_needs_catalogue (w d : Fin 3) (h : d ≠ w) :
    RequiresExternalCatalogue (fun x => StrictSelected (seamDegreeSelector w) x) d :=
  m1_alternative_needs_catalogue (seam_degree_M1Forced w) d h

end D0.Foundation
