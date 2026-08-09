import D0.Core.FiniteTypes

/-!
# Zone-tower cardinal legs (DRAFT v2 — post-kill reduction, skeptic #15)

Source: `_TASKS_CENTER_ATTACK/F3_FORK_ADJUDICATION_MEMO.md` (F3 reading fork, FORK-OPEN) and
registry row `D0-ZONE-TOWER-READING-FORK-001` (OPEN, PROOF-TARGET).

**Kill record (accepted in full, skeptic #15, 2026-07-17).** v1 of this module claimed a
machine-checked lift of the memo's §2b contradiction via `¬(zone11 ⊆ zone13)` on an authored
carrier `Sum V9 (Sum V11 V13)`. KILLED with an executable second object: the identical method
proves `¬(zone9 ⊆ zone11)` — refuting the base inclusion Reading A itself owns
(`Sum.inl : V9 ↪ V11`, `FiniteTypes.lean`) — so the statement was a disjoint-union tautology
begging the question against Reading C, and the carrier's ownership claim was false (no owned
Lean type equals it; M2's consumer carrier is a zone-9 diagonal with identity padding, not this
Sum). Errors of record: (EoR-1) authored carrier presented as owned; (EoR-2) tautology presented
as the §2b adjudication. The §2b contradiction — the ABSENCE of any owned `V11 ↪ V13` among the
sibling Sum types — is an OWNERSHIP fact (memo §1, grep-verified) with no Lean-internal
formalization; it stays memo-grade.

What survives (this file): the cardinal legs only.
* The cardinal ladder `9, 11, 13` (owned, `FiniteTypes.lean`, re-exported in the bundle).
* **A/B compatibility is cardinal-only** (`role_card_split`): the over-base jump alphabet `Role`
  and the coproduct of two consecutive dyad steps agree in CARDINALITY (`4 = 2 + 2`). `Role` is
  a PRODUCT (`Dyad × Dyad`), `Dyad ⊕ Dyad` a COPRODUCT; their equinumerosity does not
  canonically identify them (memo §6 ATT-B — the non-canonicity is the narrated leg; Lean checks
  only the cardinal agreement).

This module does NOT adjudicate or close the fork; FORK-OPEN stands; the reopening hooks
(`radius → vertex-set` functor, or an owner identification of `Role` with `Dyad ⊕ Dyad`) are the
memo's, untouched here.
-/

namespace D0

/-- **A/B compatibility is cardinal-only.** `|Role| = |Dyad ⊕ Dyad| = 4 = 2 + 2` — an equality
of CARDINALS between a product and a coproduct; no structure-preserving identification is claimed
(memo §6 ATT-B, narrated leg). -/
theorem role_card_split :
    Fintype.card Role = Fintype.card (Sum Dyad Dyad) ∧ Fintype.card Role = 2 + 2 := by
  constructor <;> simp [Role, Dyad]

/-- **Zone-tower cardinal legs (bundle).** The three readings of the zone tower agree on the
cardinal ladder `9, 11, 13`, and the over-base/consecutive agreement is cardinal-only. Nothing
here adjudicates the F3 fork. -/
theorem zone_tower_cardinal_legs :
    (Fintype.card V9 = 9 ∧ Fintype.card V11 = 11 ∧ Fintype.card V13 = 13) ∧
    Fintype.card Role = Fintype.card (Sum Dyad Dyad) :=
  ⟨⟨card_v9, card_v11, card_v13⟩, role_card_split.1⟩

end D0
