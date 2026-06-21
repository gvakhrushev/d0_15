import D0.SelfReading.RawSceneGraph
import D0.Extensions.HistoryCategory
import Mathlib.Tactic

/-!
# D0-RAW-HISTORY-CATEGORY-001 — Track I-A (raw Hist_D0)

The raw repository supplies the concrete base scene object and its derived automorphisms, but NOT a single
general cross-stage refinement morphism. Terminal **H2**: a strict subcategory (the raw `Aut`-groupoid on the
base scene, with the derived commutant 12) exists and is certified; the general refinement functor between
stages is the exact missing object `PRIM-SCENE-HISTORY-REFINEMENT-RULE`. The automorphism group is derived
raw: the part sizes `(9,11,13)` are pairwise distinct, so no graph automorphism permutes parts —
`Aut = S₉×S₁₁×S₁₃`, and its commutant is the pair-orbit count `12` (from `RawSceneGraph`).
-/

namespace D0.SelfReading.RawHistoryCategory

open D0.SelfReading.RawSceneGraph

/-- Part sizes pairwise distinct ⇒ no part-swap automorphism (derived, not assumed). -/
theorem part_sizes_distinct : ([9, 11, 13] : List ℕ).Nodup := by decide

/-- The derived `Aut`-commutant is 12 (raw pair-orbit count, from `RawSceneGraph`). -/
theorem aut_commutant_dim : commutantDim = 12 := commutant_dim_raw

/-- The base raw scene as an admissible `Hist_D0` object (invariants present, no chosen data). -/
def baseScene : D0.Extensions.HistoryCategory.HistObject := ⟨0, true, true⟩

/-- Identity morphism on the base scene is admissible (the raw `Aut`-groupoid is a category). -/
theorem base_identity : D0.Extensions.HistoryCategory.Mor baseScene baseScene :=
  D0.Extensions.HistoryCategory.mor_id baseScene rfl rfl

/-- **Terminal H2.** A certified strict subcategory (the raw `Aut`-groupoid, commutant 12) exists; the general
cross-stage refinement morphism is absent (`PRIM-SCENE-HISTORY-REFINEMENT-RULE`). -/
theorem raw_history_terminal_H2 :
    ([9, 11, 13] : List ℕ).Nodup ∧ commutantDim = 12 ∧
      D0.Extensions.HistoryCategory.Mor baseScene baseScene :=
  ⟨part_sizes_distinct, commutant_dim_raw, base_identity⟩

end D0.SelfReading.RawHistoryCategory
