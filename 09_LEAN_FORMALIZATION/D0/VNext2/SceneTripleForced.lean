import D0.Core.FiniteTypes
import Mathlib.Data.Nat.Fib.Basic
import Mathlib.Tactic

/-!
# D0-SCENE-FORCED-CHAIN-001 — Route B: the window dissolves into the owned capacity chain

The capstone `D0.VNext2.SceneTripleUnique` carried its interval `[9,13]` as HYPOTHESES
(`hlo/hhi`).  This module (Route B of `WINDOW_9_13_FORCING_MEMO.md`) DISSOLVES the window:
the endpoints are theorems of the owned graph-birth capacity chain, so the uniqueness
statement consumes the chain directly and the numerals come back as outputs.

Owned inputs consumed (OB-0): the cardinality theorems of `D0.Core.FiniteTypes`
(`card_v9 : 9`, `card_v11 : 11`, `card_v13 : 13`, `card_dyad : 2`, `card_role : 4`,
`card_omega8 : 8`), themselves built from `Ω₈ ≅ Q₈` and the two owned extensions
`V₁₁ = V₉ ⊔ D₂`, `V₁₃ = V₉ ⊔ ABCD`.

Contents:

* `scene_triple_from_owned_chain` — **zero-hypothesis**: the owned capacities ARE `(9,11,13)`
  with the `+2/+4` steps and the centre `L₅ = 11`.
* `scene_triple_unique_v2` — **window-free capstone**: any triple whose base is the pointed
  signed shell and whose two extensions are the owned primitives is `(9,11,13)`; the three
  hypotheses are the NAMED joints (base "+1" = GAP-W `D0-GAP-W-WITNESS-PLUS-ONE-001`;
  step set {D₂, ABCD} and their finality = GAP-E extension completeness).  This is a
  REDUCTION with named joints, not a closure of those gaps.
* `window_endpoints_derived` / `unique_lucas_in_derived_window` — the old interval's
  endpoints as theorems, and the old Lucas-uniqueness as a corollary against DERIVED bounds
  (skeptic repair A-2).
* `level_five_minimal_all_parities` — level 5 is minimal in the FULL Lucas sequence
  (parity-free strengthening; `L₂ = 3`, `L₄ = 7` also fail `> 8`).

Honest scope: the GAP-W necessity ("exactly one witness") and GAP-E completeness ("no third
extension alphabet") remain narrated layers owned elsewhere — see
`D0-GAP-E-PORT-EXHAUSTION-001` and the WINDOW row's transfer ledger.  Nothing here claims
their closure; it claims that GIVEN the owned decompositions, `(9,11,13)` follows with zero
free integers.  The memo skeleton's `witness_plus_one_forced := sorry` placeholder is
deliberately EXCLUDED from this module per the minting rules.
-/

namespace D0.VNext2.SceneTripleForced

open D0

/-- Lucas indexing as in `SceneTripleUnique` (`L₅ = fib 4 + fib 6 = 11`). -/
def lucas (n : ℕ) : ℕ := Nat.fib (n - 1) + Nat.fib (n + 1)

/-- **Chain form (zero hypotheses).**  The owned graph-birth capacities are `(9,11,13)`;
    the steps are the owned cardinalities `|D₂| = 2`, `|ABCD| = 4`; the centre is `L₅ = 11`.
    Consumes ONLY the `FiniteTypes` cardinality theorems. -/
theorem scene_triple_from_owned_chain :
    (Fintype.card V9, Fintype.card V11, Fintype.card V13) = (9, 11, 13)
      ∧ Fintype.card V11 = Fintype.card V9 + Fintype.card Dyad
      ∧ Fintype.card V13 = Fintype.card V9 + Fintype.card Role
      ∧ Fintype.card V11 = lucas 5 := by
  refine ⟨by rw [card_v9, card_v11, card_v13], ?_, ?_, ?_⟩
  · rw [card_v11, card_v9, card_dyad]
  · rw [card_v13, card_v9, card_role]
  · rw [card_v11]
    norm_num [lucas]

/-- **Window-free capstone.**  Any triple whose base is the pointed signed shell and whose
    two extensions are the owned primitives IS `(9,11,13)`; the centre `= L₅ = 11` is
    derived, not hypothesized.  The three hypotheses are the named joints: base "+1"
    (GAP-W), first extension `D₂` and second-and-last extension `ABCD` (GAP-E). -/
theorem scene_triple_unique_v2 (z₀ z₁ z₂ : ℕ)
    (hbase : z₀ = Fintype.card Omega8 + 1)
    (hstep₁ : z₁ = z₀ + Fintype.card Dyad)
    (hstep₂ : z₂ = z₀ + Fintype.card Role) :
    (z₀, z₁, z₂) = (9, 11, 13) ∧ z₁ = lucas 5 := by
  rw [hstep₁, hstep₂, hbase]
  constructor
  · norm_num [card_omega8, card_dyad, card_role]
  · norm_num [card_omega8, lucas]

/-- **Window recovered as output.**  The old interval's endpoints are theorems. -/
theorem window_endpoints_derived :
    Fintype.card V9 = 9 ∧ Fintype.card V13 = 13 :=
  ⟨card_v9, card_v13⟩

/-- Monotone tail of the Lucas sequence (carried over from `SceneTripleUnique`). -/
theorem lucas_ge_of_six_le {n : ℕ} (hn : 6 ≤ n) : 18 ≤ lucas n := by
  unfold lucas
  have h1 : Nat.fib 5 ≤ Nat.fib (n - 1) := Nat.fib_mono (by omega)
  have h2 : Nat.fib 7 ≤ Nat.fib (n + 1) := Nat.fib_mono (by omega)
  have h3 : Nat.fib 5 = 5 := by decide
  have h4 : Nat.fib 7 = 13 := by decide
  omega

/-- Low tail of the Lucas sequence. -/
theorem lucas_le_of_le_four {n : ℕ} (hn : n ≤ 4) : lucas n ≤ 7 := by
  unfold lucas
  have h1 : Nat.fib (n - 1) ≤ Nat.fib 3 := Nat.fib_mono (by omega)
  have h2 : Nat.fib (n + 1) ≤ Nat.fib 5 := Nat.fib_mono (by omega)
  have h3 : Nat.fib 3 = 2 := by decide
  have h4 : Nat.fib 5 = 5 := by decide
  omega

/-- **Old capstone recovered as corollary (skeptic repair A-2).**  Against the DERIVED
    bounds `card V9 = 9 ≤ Lₙ ≤ 13 = card V13`, the level is uniquely 5 — the old
    `unique_lucas_in_window` with its interval endpoints now theorems, not hypotheses. -/
theorem unique_lucas_in_derived_window {n : ℕ}
    (hlo : Fintype.card V9 ≤ lucas n) (hhi : lucas n ≤ Fintype.card V13) : n = 5 := by
  rw [card_v9] at hlo
  rw [card_v13] at hhi
  by_contra hne
  rcases lt_or_ge n 5 with h | h
  · have h4 : n ≤ 4 := by omega
    have := lucas_le_of_le_four h4
    omega
  · have h6 : 6 ≤ n := by omega
    have := lucas_ge_of_six_le h6
    omega

/-- **Parity-free minimality.**  Level 5 is the smallest level with `lucas > 8` in the FULL
    Lucas sequence — `L₂ = 3` and `L₄ = 7` fail as well, so the odd restriction matters only
    for the return-class reading, not for minimality. -/
theorem level_five_minimal_all_parities :
    lucas 1 = 1 ∧ lucas 2 = 3 ∧ lucas 3 = 4 ∧ lucas 4 = 7 ∧ lucas 5 = 11
      ∧ (∀ m, m ≤ 4 → lucas m ≤ 8) ∧ 8 < lucas 5 := by
  refine ⟨by decide, by decide, by decide, by decide, by decide, ?_, by decide⟩
  intro m hm
  match m with
  | 0 => exact le_of_lt (by decide)
  | 1 => exact le_of_lt (by decide)
  | 2 => exact le_of_lt (by decide)
  | 3 => exact le_of_lt (by decide)
  | 4 => exact le_of_lt (by decide)

end D0.VNext2.SceneTripleForced
