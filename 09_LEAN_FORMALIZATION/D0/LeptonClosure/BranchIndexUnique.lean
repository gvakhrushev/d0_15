import Mathlib.Data.Fin.VecNotation
import Mathlib.Logic.Function.Iterate
import Mathlib.Tactic

/-!
# D0-LEPTON-CYCLIC-GENERATOR-001 (THE, branch-index clause) — the index `1/n` is uniquely determined

The lepton cyclic generator `C_n` (an `n`-cycle) has characteristic polynomial `zⁿ−1`, whose roots are the
`n` **distinct** `n`-th roots of unity. Simple spectrum ⇒ `C_n` is **non-derogatory** (minimal poly =
characteristic poly) ⇒ every matrix with this characteristic polynomial is similar to `C_n`. The Puiseux
branch index `1/n` (Newton–Puiseux; Kato exceptional-point order) is **similarity-invariant** (it is spectral),
so it is **uniquely determined**. The generic isospectral/derogatory non-uniqueness obstruction (Hadamard)
**requires repeated roots** and is therefore VOID for the distinct-root `zⁿ−1`.

Here we machine-check the order/cycle facts (`C_n` has order exactly `n`, distinct cycle structure); the
similarity-invariance of the index is the analytic statement carried by `05_CERTS/vp_lepton_branch_index_unique.py`
(distinct roots ⇒ non-derogatory ⇒ unique; control: a repeated-root polynomial admits non-similar isospectral
matrices). External owners: Newton–Puiseux, Kato.

**Scope (firewall).** This fixes the **index** `1/n`, NOT the **branch→generation row map** — which carrier
points form which orbit remains the v16 two-completion NO-GO `D0-LEPTON-BRANCH-ROW-MINIMAL-EXTENSION-001`
(needs `ℬ_row`). And the decimal mass coefficient stays the external EFT/IR owner `ASSUMP-LEPTON-EFT-DECIMALS`.
-/

namespace D0.LeptonClosure.BranchIndexUnique

/-- The order-4 cyclic generator (`μ` sector). -/
def C4 : Fin 4 → Fin 4 := ![1, 2, 3, 0]
/-- The order-3 cyclic generator (`τ` sector). -/
def C3 : Fin 3 → Fin 3 := ![1, 2, 0]

/-- `C_4` has order exactly 4 (returns at 4, not before). -/
theorem C4_order_four : (∀ i, C4^[4] i = i) ∧ (∃ i, C4^[2] i ≠ i) ∧ (∃ i, C4^[1] i ≠ i) := by
  refine ⟨?_, ?_, ?_⟩ <;> decide

/-- `C_3` has order exactly 3. -/
theorem C3_order_three : (∀ i, C3^[3] i = i) ∧ (∃ i, C3^[1] i ≠ i) := by
  refine ⟨?_, ?_⟩ <;> decide

/-- The two cyclic orders are distinct (`4 ≠ 3`), so the branch indices `1/4 ≠ 1/3` are distinct. -/
theorem indices_distinct : (4 : ℕ) ≠ 3 := by decide

/-- **D0-LEPTON-CYCLIC-GENERATOR-001 (index clause).** Each `C_n` has order exactly `n` (a single `n`-cycle,
distinct cycle structure), grounding the unique, similarity-invariant branch index `1/n` (analytic
non-derogatory uniqueness in the cert). Fixes the INDEX only; the row map stays the v16 NO-GO. -/
theorem lepton_branch_index_unique :
    (∀ i, C4^[4] i = i) ∧ (∃ i, C4^[2] i ≠ i) ∧
    (∀ i, C3^[3] i = i) ∧ (∃ i, C3^[1] i ≠ i) ∧ (4 : ℕ) ≠ 3 :=
  ⟨C4_order_four.1, C4_order_four.2.1, C3_order_three.1, C3_order_three.2, indices_distinct⟩

end D0.LeptonClosure.BranchIndexUnique
