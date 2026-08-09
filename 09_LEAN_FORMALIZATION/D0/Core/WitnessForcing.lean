import D0.Core.FiniteTypes
import D0.Tower.NoExtensionBoundary
import Mathlib.Tactic

/-!
# D0-GAP-W — witness "+1": the graph-birth base is `V₉ = Ω₈ ⊔ {ω₀}` (conditional capstone)

Backs `_TASKS_CENTER_ATTACK/GAP_W_WITNESS_MEMO.md` (OB-1 of the dissolve-window
Route-B ledger) and its companion `gap_w_witness_check.py` (10/10 check() PASS).

**Honest scope (BRIDGE-ASSUMPTIONS-EXPLICIT, NOT a core closure).**
`|V_base| = |Ω₈| + 1 = 9` is FORCED **only given three named joints** that this memo
forges from owned parts but which are NOT Lean-owned:

* **W-BRIDGE-1′** — the contract couples the halt quotient with a *stable re-detection
  class* (`BOOK_01:1166.5`); its realization as ≥ 1 stationary marked base element is
  narrated ×3 (`:1541`, `:1987-1990`, `:1993`). The halt-proper itself lands at +0
  (`:846`, `:858` — adverse). Enters as `h_halt : 1 ≤ m`.
* **W-T1** — the copy-catalogue schema (`≥2` indistinguishable copies ⇒ ⊥M1)
  instantiated on adjoined marks; now Lean-owned as an `M1Forced` uniqueness theorem under
  copy-relabelling invariance (`m1_forced_copy_family_has_card_lt_two`).
* **W-BIT** — `BOOK_01:1539`'s "no further bit" scope-transferred to labels on marks.

The legacy capstone still exposes `h_nocopy : m < 2` for compatibility. The strengthened capstone
derives that bound from W-T1's semantic hypotheses (M1-forced choice plus relabelling invariance),
so W-BIT is no longer needed for the copy cap. The remaining independent input is the stable
re-detection lower bound `h_halt : 1 ≤ m`.
The one genuinely NEW Lean content is the decidable `no_stationary_in_omega8` (the
computable half of the 8-kill — full-cycle translation is fixed-point-free on Ω₈).

This module does NOT claim unconditional forcing; it does NOT bridge the halt-proper to
the vertex (contradicted by `:846`/`:858`); it does NOT close GAP-E. See §VI of the memo.
-/

namespace D0.Core.WitnessForcing

open D0

/-- **OB-W0 (OWNED reuse): pointed-shell arithmetic — `|V₉| = |Ω₈| + 1`.**
Reuses `card_v9` (`FiniteTypes.lean:27`) and `card_omega8` (`:24`, = `omega8_cardinality`,
D0-OMEGA8-001). -/
theorem base_card_arith : Fintype.card V9 = Fintype.card Omega8 + 1 := by
  rw [card_v9, card_omega8]

/-- **OB-W1 (NEW, decidable — computable half of the 8-kill): no stationary element inside
Ω₈.** The full signed-role cycle (translation `+k`, `k ≠ 0`) is fixed-point-free on the 8
signed roles — nothing inside Ω₈ is stationary under any nontrivial circulation step.
Owned circulation model: `WitnessHalting.shiftMat` (translation) + `BOOK_01:1996`
(full-cycle traversal). Mirrors checks 3-4 of `gap_w_witness_check.py`. -/
theorem no_stationary_in_omega8 : ∀ k : Fin 8, k ≠ 0 → ∀ x : Fin 8, x + k ≠ x := by
  decide

/-- **OB-W2 (OWNED reuse — no-overfire at m = 1):** the single adjoined witness needs no
catalogue — the copy-kill does not fire at m = 1, `|S₁| = 1`. Reuses
`D0.Tower.first_instance_canonical` (`NoExtension.lean:52`). -/
theorem no_overfire_at_one : Fintype.card (Equiv.Perm (Fin 1)) = 1 :=
  D0.Tower.first_instance_canonical

/-- **OB-W3 arithmetic input:** two identical marks carry a nontrivial copy-symmetry
`1 < |S₂|`. The theorem immediately below supplies the missing M1/invariance argument; this
cardinality fact alone is not credited with the catalogue conclusion. -/
theorem copy_kill_arith : 1 < Fintype.card (Equiv.Perm (Fin 2)) :=
  D0.Tower.repeat_has_nontrivial_copy_symmetry

/-- **OB-W3 semantic closure.** An M1-forced mark under a constraint invariant under all
relabellings of the `m` indistinguishable marks forces `m < 2`. Unlike `copy_kill_arith`, this
proves the catalogue no-go itself rather than only counting `S₂`. -/
theorem copy_kill_m1
    (m : ℕ) (Forced : Fin m → Prop)
    (hInvariant : D0.Tower.NoExtensionBoundary.CopyRelabellingInvariant Forced)
    (hForced : ∃ a, D0.Foundation.M1Forced Forced a) :
    m < 2 :=
  D0.Tower.NoExtensionBoundary.m1_forced_copy_family_has_card_lt_two
    m Forced hInvariant hForced

/-- **Conditional capstone (honest form).** GIVEN the joints as hypotheses on the number
`m` of adjoined stationary marks — `1 ≤ m` (re-detection realization, **W-BRIDGE-1′**) and
`m < 2` (copy/bit kills, **W-T1** + **W-BIT**) — the base cardinal is forced:
`|Ω₈| + m = 9`. The arithmetic is trivial by design; all forcing content is in the named
hypotheses. This is the BRIDGE-ASSUMPTIONS-EXPLICIT statement, not a core closure. -/
theorem card_base_forced_conditional (m : ℕ)
    (h_halt : 1 ≤ m)      -- W-BRIDGE-1′: at least one stationary mark (8-kill)
    (h_nocopy : m < 2) :  -- W-T1 + W-BIT: at most one (10-kill)
    Fintype.card Omega8 + m = 9 := by
  rw [card_omega8]; omega

/-- **Strengthened capstone.** Replaces the numerical copy-cap hypothesis `m < 2` by its semantic
owner: the mark is M1-forced and its constraint is invariant under all relabellings of
indistinguishable marks. The only remaining forcing hypothesis is the independent lower bound
`1 ≤ m` supplied by stable re-detection. -/
theorem card_base_forced_from_m1_copy_invariance
    (m : ℕ) (h_halt : 1 ≤ m)
    (Forced : Fin m → Prop)
    (hInvariant : D0.Tower.NoExtensionBoundary.CopyRelabellingInvariant Forced)
    (hForced : ∃ a, D0.Foundation.M1Forced Forced a) :
    Fintype.card Omega8 + m = 9 :=
  card_base_forced_conditional m h_halt
    (copy_kill_m1 m Forced hInvariant hForced)

/-- **Sanity corollary:** the forced base IS the owned V₉ count. -/
theorem forced_base_is_v9 (m : ℕ) (h1 : 1 ≤ m) (h2 : m < 2) :
    Fintype.card Omega8 + m = Fintype.card V9 := by
  rw [card_base_forced_conditional m h1 h2, card_v9]

end D0.Core.WitnessForcing
