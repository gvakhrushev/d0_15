import D0.Foundation.CascadeChain
import D0.Tower.NoExtension
import Mathlib.Tactic

/-!
# D0-SCENE-COUNT-REDUCTION-001 — exact boundary for the three-zone claim

The corpus wants the number of scene zones to be an output. The two existing owner modules do not
yet state that output:

* `CascadeChain.chain_length_lower_bound` proves that two carried cascade obligations cannot be
  merged. It does not assign a number of zones to an arbitrary scene candidate.
* `Tower.no_extension_theorem` proves the quadratic reduction and copy-symmetry facts used by the
  no-extension argument. It does not quantify over scene candidates or state that a fourth zone is
  inadmissible.

This module makes that seam typed. A candidate has a variable `zoneCount`; the two interpretation
records below are exactly the missing maps from the proved owner facts to a lower and an upper bound
on that count. Once both maps exist, `zoneCount = 3` is mechanical. The negative controls show that
neither map can be dropped.

This is a **reduction theorem**, not closure of `D0-CASCADE-INSUFFICIENCY-CHAIN-001`: current Lean
constructs neither interpretation record from M1/M1+.
-/

namespace D0.Foundation.SceneCountReduction

open D0
open D0.Foundation

/-- A scene candidate before the number of zones has been selected. -/
structure SceneCandidate where
  zoneCount : ℕ
  zoneCount_pos : 0 < zoneCount

/-- The exact proposition currently owned by the carried cascade lower-bound theorem. -/
abbrev CascadeOwnerFact : Prop :=
  ¬ (stepOneLoop.ObligationAbove ↔ stepOrderMemory.ObligationBelow)

/-- The exact algebraic/symmetry package currently owned by `Tower.no_extension_theorem`. -/
abbrev NoExtensionOwnerFact : Prop :=
  (phi⁻¹ + phi⁻¹ ^ 2 = 1) ∧
  (phi⁻¹ ^ 3 = 2 * phi⁻¹ - 1) ∧
  (1 < Fintype.card (Equiv.Perm (Fin 2)))

/-- The canonical inclusion of a smaller finite index type into a larger one. -/
def finEmbeddingOfLE {m n : ℕ} (h : m ≤ n) : Fin m ↪ Fin n where
  toFun i := ⟨i.val, lt_of_lt_of_le i.isLt h⟩
  inj' := by
    intro i j hij
    exact Fin.ext (congrArg (fun x : Fin n => x.val) hij)

/-- Missing lower-bound semantics: construct three genuinely distinct zones from the carried
non-merging fact. This field is deliberately not a Boolean flag or a ready-made inequality: a
construction must consume the actual proposition proved by `CascadeChain` and return an embedding
whose injectivity Lean checks. -/
structure CascadeCountInterpretation (S : SceneCandidate) where
  ownerFact_implies_three_distinct_zones :
    CascadeOwnerFact → Fin 3 ↪ Fin S.zoneCount

/-- Missing upper-bound semantics: classify every candidate zone injectively into the three
quadratic slots. Constructing this record requires a formal notion of zone type and admissibility;
the present `NoExtension` module does not provide one. Returning an embedding makes both
exhaustivity and non-duplication load-bearing. -/
structure NoExtensionCountInterpretation (S : SceneCandidate) where
  ownerFact_implies_zone_slot_embedding :
    NoExtensionOwnerFact → Fin S.zoneCount ↪ Fin 3

/-- The two owner facts themselves are already machine-checked. -/
theorem owner_facts :
    CascadeOwnerFact ∧ NoExtensionOwnerFact :=
  ⟨chain_length_lower_bound, D0.Tower.no_extension_theorem⟩

/-- **D0-SCENE-COUNT-REDUCTION-001.** Exact three-zone closure reduces to two typed semantic maps.
No count is assumed in `SceneCandidate`: the two bounds are derived from the injectivity of the
embeddings supplied by the cascade and no-extension interpretations. -/
theorem exact_zone_count_of_interpretations
    (S : SceneCandidate)
    (lower : CascadeCountInterpretation S)
    (upper : NoExtensionCountInterpretation S) :
    S.zoneCount = 3 := by
  let lowerEmbedding : Fin 3 ↪ Fin S.zoneCount :=
    lower.ownerFact_implies_three_distinct_zones chain_length_lower_bound
  let upperEmbedding : Fin S.zoneCount ↪ Fin 3 :=
    upper.ownerFact_implies_zone_slot_embedding D0.Tower.no_extension_theorem
  have hLower : 3 ≤ S.zoneCount := by
    simpa using
      (Fintype.card_le_of_injective lowerEmbedding lowerEmbedding.injective)
  have hUpper : S.zoneCount ≤ 3 := by
    simpa using
      (Fintype.card_le_of_injective upperEmbedding upperEmbedding.injective)
  omega

/-! ## Load-bearing controls

Each interpretation can hold while the conclusion fails if the other one is absent. These are
small finite countermodels to any accidental weakening of the reduction theorem.
-/

private def twoZoneCandidate : SceneCandidate :=
  ⟨2, by omega⟩

private def fourZoneCandidate : SceneCandidate :=
  ⟨4, by omega⟩

/-- The no-extension-to-upper map alone permits a two-zone candidate. -/
def twoZoneUpperInterpretation :
    NoExtensionCountInterpretation twoZoneCandidate where
  ownerFact_implies_zone_slot_embedding := by
    intro _
    exact finEmbeddingOfLE (by simp [twoZoneCandidate])

/-- The cascade-to-lower map alone permits a four-zone candidate. -/
def fourZoneLowerInterpretation :
    CascadeCountInterpretation fourZoneCandidate where
  ownerFact_implies_three_distinct_zones := by
    intro _
    exact finEmbeddingOfLE (by simp [fourZoneCandidate])

theorem lower_interpretation_is_load_bearing :
    twoZoneCandidate.zoneCount ≠ 3 ∧
    twoZoneCandidate.zoneCount < 4 := by
  simp [twoZoneCandidate]

theorem upper_interpretation_is_load_bearing :
    fourZoneCandidate.zoneCount ≠ 3 ∧
    3 ≤ fourZoneCandidate.zoneCount := by
  simp [fourZoneCandidate]

end D0.Foundation.SceneCountReduction
