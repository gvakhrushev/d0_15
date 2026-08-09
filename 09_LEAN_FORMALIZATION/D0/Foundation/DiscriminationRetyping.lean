import D0.Foundation.CascadeChain
import D0.Foundation.SceneCountRouteNoGo

/-!
# Re-typing the cascade obligations: the cap of two is lifted

`D0.Foundation.SceneCountRouteNoGo.no_three_pairwise_inequivalent_props` shows that comparing
cascade obligations as *propositions* caps the number of distinguishable insufficiencies at two,
because `Iff` has exactly two classes on `Prop`. The count claim of §01.6.1c needs three. So the
propositional route cannot reach it, however many floors are carried.

`CascadeChain.lean:43-46` gives the reason the propositional encoding was chosen:

> "Carrying it as an abstract predicate over types would force a uniform structure class the floors
> do not share (one is a register model, the next a group)."

This module shows the floors **do** share a uniform structure class, and that it is not a predicate
over types. Every carried floor has the same shape: *a record map fails to separate two things that
must be told apart.*

| floor | what must be told apart | the record that collapses them |
|---|---|---|
| 2→3 | two readings | a monopoly (constant) acceptor |
| 4→5 | two operation histories | one `ℤ` register, via `runOne` |
| 5→6 | `ab` from `ba` | an abelian carrier, via the product |

Packaging that shape as `Discrimination` puts all three floors on one common datum type — the
disjoint union of what each floor discriminates — at which point insufficiencies are distinguished
by *which pair they fail to separate*, not by a truth value. Distinctness then has as many values as
there are pairs, and the cap disappears: `three_distinct_insufficiencies` exhibits three, and
`retyped_route_is_not_capped` states the contrast with the propositional theorem directly.

**RESULT OF THE ATTEMPT (negative, machine-checked).** Lifting the cap is not enough. The naive
distinctness notion below (`DistinctInsufficiency` = "different designated pair") over-counts so
badly that `ZoneAssignment` is **provably uninhabitable** for every finite scene
(`zoneAssignment_is_uninhabitable`): the family `trivialDisc n` is endlessly pairwise distinct, so a
zone-per-insufficiency assignment would need infinitely many zones. Consequently
`three_le_zoneCount` and `cascadeInterpretationOfZoneAssignment` below are **vacuous** — hypotheses
from an empty type — which is the same defect this module's companion diagnoses in
`SceneCountReduction`. They are kept, explicitly labelled, as the record of a failed route.

The precise requirement this exposes: the distinctness notion must be coarse enough to have a
**finite** index — i.e. a classification of insufficiency *kinds*, not of designated pairs. That is
exactly the "semantic classification theorem mapping every admissible necessity-type injectively
into three owned slots" that `D0-TOWER-STOP-NOEXT-001`'s 2026-07-29 status correction names as
missing. Both routes converge on it.

**Honest scope — what is still missing.** This lifts the *obstruction*; it does not by itself
discharge `CascadeCountInterpretation`. Turning three distinct insufficiencies into three distinct
zones still needs the interpretation "a genuinely distinct insufficiency occupies its own zone",
which is a semantic postulate about the scene and is stated here as an explicit hypothesis
(`ZoneAssignment`), never assumed. The difference from the propositional typing is that this
postulate is **not vacuous**: it consumes the three discriminations, and cannot be discharged by
`intro _` the way `SceneCountReduction`'s own controls discharge theirs
(`SceneCountRouteNoGo.cascade_interpretation_arrow_vacuous`).

`D0-CASCADE-INSUFFICIENCY-CHAIN-001` stays a proof target. The upper bound is untouched.
-/

namespace D0.Foundation.DiscriminationRetyping

open D0.Foundation
open D0.Foundation.SceneCountReduction

/-- The two group elements whose order the abelian carrier cannot record. -/
def ga : Multiplicative (ℤ × ℤ) := Multiplicative.ofAdd ((1 : ℤ), (0 : ℤ))
def gb : Multiplicative (ℤ × ℤ) := Multiplicative.ofAdd ((0 : ℤ), (1 : ℤ))

/-- The common datum type: the disjoint union of what the carried floors discriminate. This is the
uniform structure class `CascadeChain.lean:43-46` reports the floors as lacking. -/
inductive CascadeDatum
  | reading (n : ℕ)                                   -- floor 2→3
  | history (h : List Op)                             -- floor 4→5
  | opPair (x y : Multiplicative (ℤ × ℤ))             -- floor 5→6

/-- **The shared shape of every carried floor.** A record map on the common datum type, together
with the designated pair it must tell apart, and the proof that it does not. Unlike a `Prop`, this
carries *what* is not separated. -/
structure Discrimination where
  Record : Type
  readOut : CascadeDatum → Record
  d₁ : CascadeDatum
  d₂ : CascadeDatum
  data_distinct : d₁ ≠ d₂
  record_collapses : readOut d₁ = readOut d₂

/-- Floor 2→3 as a discrimination: a monopoly acceptor gives every reading the same verdict. -/
def discComparison : Discrimination where
  Record := Bool
  readOut := fun _ => true                       -- the constant/monopoly record
  d₁ := CascadeDatum.reading 0
  d₂ := CascadeDatum.reading 1
  data_distinct := by simp
  record_collapses := rfl

/-- Floor 4→5 as a discrimination: one `ℤ` register cannot separate the two histories the corpus
uses, `one_loop_insufficient` supplying the collapse. -/
def discOneLoop : Discrimination where
  Record := ℤ
  readOut := fun d => match d with
    | CascadeDatum.history h => runOne h 0
    | _ => 0
  d₁ := CascadeDatum.history h₁
  d₂ := CascadeDatum.history h₂
  data_distinct := by
    simp only [ne_eq, CascadeDatum.history.injEq]
    exact histories_differ
  record_collapses := one_loop_insufficient 0

/-- Floor 5→6 as a discrimination: an abelian carrier records `ab` and `ba` identically. -/
def discOrderMemory : Discrimination where
  Record := Multiplicative (ℤ × ℤ)
  readOut := fun d => match d with
    | CascadeDatum.opPair x y => x * y
    | _ => 1
  d₁ := CascadeDatum.opPair ga gb
  d₂ := CascadeDatum.opPair gb ga
  data_distinct := by
    simp only [ne_eq, CascadeDatum.opPair.injEq, not_and]
    intro h
    exfalso
    have : ((1 : ℤ), (0 : ℤ)) = ((0 : ℤ), (1 : ℤ)) := h
    simp at this
  record_collapses := mul_comm _ _

/-- Two discriminations are **genuinely distinct insufficiencies** when they fail on different
data — a distinction with as many values as there are pairs, not two. -/
def DistinctInsufficiency (D E : Discrimination) : Prop :=
  D.d₁ ≠ E.d₁ ∨ D.d₂ ≠ E.d₂

/-- **The cap is lifted: three pairwise distinct insufficiencies, from the carried floors.** This is
exactly what `no_three_pairwise_inequivalent_props` forbids in the propositional typing. -/
theorem three_distinct_insufficiencies :
    DistinctInsufficiency discComparison discOneLoop ∧
    DistinctInsufficiency discComparison discOrderMemory ∧
    DistinctInsufficiency discOneLoop discOrderMemory := by
  refine ⟨Or.inl ?_, Or.inl ?_, Or.inl ?_⟩ <;> simp [discComparison, discOneLoop, discOrderMemory]

/-- **The contrast, stated in one place.** Propositionally, three pairwise-inequivalent obligations
are impossible; in the re-typing they exist and are exhibited. The obstruction was the encoding. -/
theorem retyped_route_is_not_capped :
    (∀ A B C : Prop, ¬ (A ↔ B) → ¬ (A ↔ C) → ¬ (B ↔ C) → False) ∧
    (DistinctInsufficiency discComparison discOneLoop ∧
     DistinctInsufficiency discComparison discOrderMemory ∧
     DistinctInsufficiency discOneLoop discOrderMemory) :=
  ⟨D0.Foundation.SceneCountRouteNoGo.no_three_pairwise_inequivalent_props,
   three_distinct_insufficiencies⟩

/-- **The interpretation, stated as an explicit hypothesis and never assumed.** A scene assigns a
zone to each insufficiency, and genuinely distinct insufficiencies land in distinct zones. This is
the semantic content `SceneCountReduction` asks for; it consumes the discriminations, so it cannot
be discharged by discarding its argument. -/
structure ZoneAssignment (S : SceneCandidate) where
  zoneOf : Discrimination → Fin S.zoneCount
  separates : ∀ D E : Discrimination, DistinctInsufficiency D E → zoneOf D ≠ zoneOf E

/-- **VACUOUS — see `zoneAssignment_is_uninhabitable`.** Given the interpretation, the three carried
insufficiencies occupy three distinct zones. The hypothesis is uninhabitable for every finite scene,
so this theorem carries no content; it is retained as the record of the failed route. -/
theorem three_le_zoneCount (S : SceneCandidate) (Z : ZoneAssignment S) : 3 ≤ S.zoneCount := by
  obtain ⟨h₁₂, h₁₃, h₂₃⟩ := three_distinct_insufficiencies
  have e₁₂ : Z.zoneOf discComparison ≠ Z.zoneOf discOneLoop := Z.separates _ _ h₁₂
  have e₁₃ : Z.zoneOf discComparison ≠ Z.zoneOf discOrderMemory := Z.separates _ _ h₁₃
  have e₂₃ : Z.zoneOf discOneLoop ≠ Z.zoneOf discOrderMemory := Z.separates _ _ h₂₃
  have hf : Function.Injective
      (fun i : Fin 3 =>
        if i = 0 then Z.zoneOf discComparison
        else if i = 1 then Z.zoneOf discOneLoop
        else Z.zoneOf discOrderMemory) := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all
  have hcard := Fintype.card_le_of_injective _ hf
  simpa using hcard

/-- **VACUOUS — a function from an empty type.** It would construct the map `SceneCountReduction`
reports as missing, but `ZoneAssignment` is uninhabitable, so nothing is constructed. Retained,
labelled, so the failure is in the record rather than in a later reviewer's notes. -/
def cascadeInterpretationOfZoneAssignment (S : SceneCandidate) (Z : ZoneAssignment S) :
    CascadeCountInterpretation S where
  ownerFact_implies_three_distinct_zones := fun _ => finEmbeddingOfLE (three_le_zoneCount S Z)

/-! ## The route fails: the naive distinctness notion has no finite index -/

/-- An endless family of discriminations, pairwise distinct by this module's own notion: each
collapses a different pair of readings under a constant record. -/
def trivialDisc (n : ℕ) : Discrimination where
  Record := Bool
  readOut := fun _ => true
  d₁ := CascadeDatum.reading n
  d₂ := CascadeDatum.reading (n + 1)
  data_distinct := by simp
  record_collapses := rfl

/-- **The attempt fails, machine-checked.** `ZoneAssignment` demands a distinct zone for every
pairwise-distinct insufficiency; `trivialDisc` supplies infinitely many, so no finite scene admits
one. Lifting the propositional cap therefore does **not** deliver the missing lower map: the
distinctness notion must additionally be finitely indexed. -/
theorem zoneAssignment_is_uninhabitable (S : SceneCandidate) (Z : ZoneAssignment S) : False := by
  have hinj : Function.Injective (fun n : ℕ => Z.zoneOf (trivialDisc n)) := by
    intro m n h
    by_contra hmn
    exact Z.separates (trivialDisc m) (trivialDisc n)
      (Or.inl (by simp [trivialDisc, hmn])) h
  haveI : Finite ℕ := Finite.of_injective _ hinj
  exact not_finite ℕ

end D0.Foundation.DiscriminationRetyping
