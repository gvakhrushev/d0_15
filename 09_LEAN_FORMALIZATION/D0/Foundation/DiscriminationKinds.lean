import D0.Foundation.DiscriminationRetyping

/-!
# A finitely-indexed classification of insufficiencies, and the lower map constructed

`DiscriminationRetyping.zoneAssignment_is_uninhabitable` shows why lifting the propositional cap is
not enough: distinguishing insufficiencies by *which pair* they fail on has no finite index, so a
zone-per-insufficiency assignment is impossible for any finite scene.

The repair is to classify by the **sort of datum** the record fails to separate, which is computed
from the discrimination by pattern match rather than declared as a count:

| discrimination | datum sort | the record that collapses it |
|---|---|---|
| `discComparison` | `reading` | a constant/monopoly acceptor |
| `discOneLoop` | `history` | one `ℤ` register |
| `discOrderMemory` | `opPair` | an abelian product |

`DatumKind` is finite, so `ZoneAssignmentK` is not empty — it is **proved inhabited**
(`zoneAssignmentThree`), the check the previous attempt failed.

**BUT THE ROUTE STILL FAILS, machine-checked.** `zoneAssignmentK_iff_bound` (companion file) proves
`Nonempty (ZoneAssignmentK S) ↔ 3 ≤ S.zoneCount`: the hypothesis is *equivalent to the conclusion*.
So `cascadeInterpretationK` does not derive the lower bound, it renames it — the same defect
`SceneCountRouteNoGo.reduction_is_bare_arithmetic` diagnoses in `SceneCountReduction`, in a new
dress. Two formulations were tried and both fail, in opposite directions: pair-indexed distinctness
is uninhabitable, sort-indexed distinctness is circular.

**What survives as content.** `three_distinct_kinds` is computed, not assumed: the three carried
floors genuinely fail on three different sorts of datum. What is *not* derived is the step from
"three sorts" to "three zones".

**What carries the 3.** The bound comes from the three *carried floors* discriminating three
different sorts of datum. That is a legitimate basis for a LOWER bound — it says the scene needs at
least as many zones as there are genuinely different things the cascade must tell apart — and it is
exactly what `CascadeCountInterpretation` asks the cascade side to supply.

**What this does NOT do.** It gives no upper bound. `DatumKind` has three constructors because the
corpus carries three such floors; carrying a fourth would add a fourth. Reading `3` off this type as
a *cap* would be the constructor-count circularity that `AdmissibleComparisonGrammar` was written to
remove, and it is not done here: the upper bound stays with
`NoExtensionCountInterpretation`, still unconstructed, still blocked on the classification theorem
`D0-TOWER-STOP-NOEXT-001` names. `D0-CASCADE-INSUFFICIENCY-CHAIN-001` remains a proof target.
-/

namespace D0.Foundation.DiscriminationKinds

open D0.Foundation
open D0.Foundation.SceneCountReduction
open D0.Foundation.DiscriminationRetyping

/-- The sort of datum a record fails to separate. Finite, and read off the discrimination. -/
inductive DatumKind
  | reading
  | history
  | opPair
  deriving DecidableEq, Fintype

/-- The classification, **computed** from the discrimination's designated datum. -/
def kindOf (D : Discrimination) : DatumKind :=
  match D.d₁ with
  | CascadeDatum.reading _ => DatumKind.reading
  | CascadeDatum.history _ => DatumKind.history
  | CascadeDatum.opPair _ _ => DatumKind.opPair

/-- Distinctness with a finite index: the failures are of different sorts. -/
def DistinctKind (D E : Discrimination) : Prop := kindOf D ≠ kindOf E

/-- **The three carried floors realise three different sorts.** Decided, not postulated. -/
theorem three_distinct_kinds :
    DistinctKind discComparison discOneLoop ∧
    DistinctKind discComparison discOrderMemory ∧
    DistinctKind discOneLoop discOrderMemory := by
  refine ⟨?_, ?_, ?_⟩ <;>
    simp [DistinctKind, kindOf, discComparison, discOneLoop, discOrderMemory]

/-- The classification is genuinely three-valued. -/
theorem card_datumKind : Fintype.card DatumKind = 3 := by decide

/-- **The interpretation, now finitely indexed.** A scene gives each *sort* of insufficiency its own
zone. Unlike `DiscriminationRetyping.ZoneAssignment` this is not vacuous — see `zoneAssignmentThree`
below, which inhabits it. -/
structure ZoneAssignmentK (S : SceneCandidate) where
  zoneOf : DatumKind → Fin S.zoneCount
  zoneOf_injective : Function.Injective zoneOf

/-- **The check the previous attempt failed: the hypothesis is satisfiable.** A three-zone scene
carries an assignment, so `ZoneAssignmentK` is not an empty type and the bound below is real. -/
def zoneAssignmentThree : ZoneAssignmentK ⟨3, by omega⟩ where
  zoneOf := fun k =>
    match k with
    | DatumKind.reading => (0 : Fin 3)
    | DatumKind.history => (1 : Fin 3)
    | DatumKind.opPair => (2 : Fin 3)
  zoneOf_injective := by
    intro a b hab
    cases a <;> cases b <;> first | rfl | (exact absurd hab (by decide))

/-- **CIRCULAR — see `zoneAssignmentK_iff_bound`.** Three sorts of insufficiency need three zones.
The hypothesis is equivalent to the conclusion, so this records the reduction, not a derivation. -/
theorem three_le_zoneCount_of_kinds (S : SceneCandidate) (Z : ZoneAssignmentK S) :
    3 ≤ S.zoneCount := by
  have h := Fintype.card_le_of_injective Z.zoneOf Z.zoneOf_injective
  rw [card_datumKind, Fintype.card_fin] at h
  exact h

/-- **CIRCULAR.** It inhabits the record `SceneCountReduction` reports as missing, from a hypothesis
that is equivalent to the bound it produces. Retained, labelled, as the record of a failed route:
the cascade side still supplies no independent `3`. -/
def cascadeInterpretationK (S : SceneCandidate) (Z : ZoneAssignmentK S) :
    CascadeCountInterpretation S where
  ownerFact_implies_three_distinct_zones :=
    fun _ => finEmbeddingOfLE (three_le_zoneCount_of_kinds S Z)

/-- **Summary of the three attempts, all negative.** Propositional typing caps at two; pair-indexed
typing is uninhabitable; sort-indexed typing is inhabitable but circular. The lower map is not
constructed by any of them. -/
theorem lower_route_repaired :
    (∀ A B C : Prop, ¬ (A ↔ B) → ¬ (A ↔ C) → ¬ (B ↔ C) → False) ∧
    (∀ S : SceneCandidate, ZoneAssignment S → False) ∧
    Nonempty (ZoneAssignmentK ⟨3, by omega⟩) ∧
    (∀ S : SceneCandidate, ZoneAssignmentK S → 3 ≤ S.zoneCount) :=
  ⟨D0.Foundation.SceneCountRouteNoGo.no_three_pairwise_inequivalent_props,
   zoneAssignment_is_uninhabitable,
   ⟨zoneAssignmentThree⟩,
   three_le_zoneCount_of_kinds⟩

end D0.Foundation.DiscriminationKinds
