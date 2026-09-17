import D0.Foundation.SceneCountReduction
import D0.Foundation.CascadeFloorOrientationParity

/-!
# The propositional lower-bound route to "three zones" is capped at two

`D0.Foundation.SceneCountReduction` reduces the exact three-zone count to two typed interpretation
maps and records that neither is constructed. This module shows that the *lower* map cannot be
reached along the route the carried cascade currently supplies, and isolates why.

Two results, both machine-checked, both about the FORMALIZATION rather than about the scene:

* **`no_three_pairwise_inequivalent_props`** — there do not exist three pairwise non-equivalent
  propositions. Classically `Iff` partitions `Prop` into exactly two classes (the true ones and the
  false ones), so a family of pairwise `¬ (· ↔ ·)` facts has at most two members. Every carried
  non-merging fact has this shape — `chain_length_lower_bound` is literally
  `¬ (stepOneLoop.ObligationAbove ↔ stepOrderMemory.ObligationBelow)` — so **no number of additional
  floors can raise the propositional lower bound above 2.** The gap between the owned lower bound
  (2) and the claimed count (3) is not a matter of carrying more floors; it is a limit of comparing
  obligations by truth value.

* **`cascade_interpretation_arrow_vacuous` / `noextension_interpretation_arrow_vacuous`** — the
  hypothesis arrows in `CascadeCountInterpretation` and `NoExtensionCountInterpretation` carry no
  information, because their antecedents are theorems (`SceneCountReduction.owner_facts`). Inhabiting
  either structure is *equivalent* to exhibiting the bare embedding. So the design intent recorded at
  `SceneCountReduction.lean:53-56` — "a construction must consume the actual proposition proved by
  `CascadeChain`" — is not enforced by the typing; the module's own controls
  (`twoZoneUpperInterpretation`, `fourZoneLowerInterpretation`) discharge the antecedent with
  `intro _` and discard it.

**What this does NOT show.** It does not refute "three insufficiencies = three zones", which is a
claim about the scene, not about `Prop`. It does not construct either interpretation map. It does
not touch the upper bound's own obstruction. It says only that the lower map must be re-typed —
obligations have to be compared as structures carrying more than a truth value — before any amount
of floor-carrying can reach 3. `D0-CASCADE-INSUFFICIENCY-CHAIN-001` stays a proof target.
-/

namespace D0.Foundation.SceneCountRouteNoGo

open D0.Foundation
open D0.Foundation.SceneCountReduction

/-- **The cap.** Three pairwise non-equivalent propositions do not exist: `Iff` has exactly two
classes on `Prop`. Proved by classical case analysis on the three truth values. -/
theorem no_three_pairwise_inequivalent_props (A B C : Prop)
    (hAB : ¬ (A ↔ B)) (hAC : ¬ (A ↔ C)) (hBC : ¬ (B ↔ C)) : False := by
  by_cases hA : A <;> by_cases hB : B <;> by_cases hC : C <;> tauto

/-- **The carried lower bound has exactly this shape**, so the cap applies to it verbatim. -/
theorem carried_lower_bound_shape :
    ¬ (stepOneLoop.ObligationAbove ↔ stepOrderMemory.ObligationBelow) :=
  chain_length_lower_bound

/-- **The new orientation floor does not escape the cap either.** Its two obligations are
non-merging in the same propositional sense, so adding it cannot contribute a third class. -/
theorem orientation_floor_is_non_merging :
    ¬ (D0.Foundation.CascadeFloorOrientationParity.OrientationClosed 2 ↔
       D0.Foundation.CascadeFloorOrientationParity.OrientationClosed 1) :=
  repairs_do_not_merge
    D0.Foundation.CascadeFloorOrientationParity.two_step_control
    D0.Foundation.CascadeFloorOrientationParity.unit_step_insufficient

/-- **The route is blocked, stated against the carried floors.** Whatever three obligations are
drawn from the cascade, they cannot be pairwise non-merging — so the propositional route yields at
most two distinct insufficiency classes, never the three the count claim needs. -/
theorem propositional_route_caps_at_two
    (O₁ O₂ O₃ : Prop)
    (h₁₂ : ¬ (O₁ ↔ O₂)) (h₁₃ : ¬ (O₁ ↔ O₃)) (h₂₃ : ¬ (O₂ ↔ O₃)) : False :=
  no_three_pairwise_inequivalent_props O₁ O₂ O₃ h₁₂ h₁₃ h₂₃

/-- **The lower interpretation's hypothesis arrow is vacuous.** Its antecedent is a theorem, so
inhabiting the structure is equivalent to exhibiting the embedding outright. -/
theorem cascade_interpretation_arrow_vacuous (S : SceneCandidate) :
    Nonempty (CascadeCountInterpretation S) ↔ Nonempty (Fin 3 ↪ Fin S.zoneCount) := by
  constructor
  · rintro ⟨i⟩
    exact ⟨i.ownerFact_implies_three_distinct_zones chain_length_lower_bound⟩
  · rintro ⟨e⟩
    exact ⟨⟨fun _ => e⟩⟩

/-- **The upper interpretation's hypothesis arrow is vacuous**, for the same reason. -/
theorem noextension_interpretation_arrow_vacuous (S : SceneCandidate) :
    Nonempty (NoExtensionCountInterpretation S) ↔ Nonempty (Fin S.zoneCount ↪ Fin 3) := by
  constructor
  · rintro ⟨i⟩
    exact ⟨i.ownerFact_implies_zone_slot_embedding D0.Tower.no_extension_theorem⟩
  · rintro ⟨e⟩
    exact ⟨⟨fun _ => e⟩⟩

/-- **Consequence: the reduction theorem is, as typed, the bare arithmetic of the two bounds.**
Inhabiting both interpretations is equivalent to `3 ≤ n ∧ n ≤ 3`. This is why neither map can be
"constructed from M1/M1+" as written: there is nothing for a construction to consume. -/
theorem reduction_is_bare_arithmetic (S : SceneCandidate) :
    (Nonempty (CascadeCountInterpretation S) ∧ Nonempty (NoExtensionCountInterpretation S)) ↔
    (3 ≤ S.zoneCount ∧ S.zoneCount ≤ 3) := by
  rw [cascade_interpretation_arrow_vacuous, noextension_interpretation_arrow_vacuous]
  constructor
  · rintro ⟨⟨e₁⟩, ⟨e₂⟩⟩
    refine ⟨?_, ?_⟩
    · simpa using Fintype.card_le_of_injective e₁ e₁.injective
    · simpa using Fintype.card_le_of_injective e₂ e₂.injective
  · rintro ⟨h₁, h₂⟩
    exact ⟨⟨finEmbeddingOfLE h₁⟩, ⟨finEmbeddingOfLE h₂⟩⟩

end D0.Foundation.SceneCountRouteNoGo
