import D0.Core.Phi
import D0.Dynamics.PisotContraction
import D0.Core.FiniteTypes
import Mathlib.Tactic

/-!
# D0-IM-005 — fractal continuum + witness halting (corrected layer)

BOOK_01/06. Python certificate: `05_CERTS/vp_continuum_from_fractal_tick.py` (+ siblings).

The corrected continuum/witness layer: the continuum is the envelope of a discrete φ-tick semigroup
(rate `q = 1/φ = primitiveRoot`), the active substrate `Aₙ = qⁿ` decays while the archive
`Bₙ = 1 − qⁿ` accumulates the lost amount (total conserved), the archive grows monotonically; and the
"witness halting" half lives on the finite signed-role state space `Ω₈` (card 8) extended by the witness
to `V₉` (card 9).

This module machine-checks the finite core: `q = primitiveRoot`, conservation `Aₙ + Bₙ = 1`, strict
archive growth, and the `Ω₈`/`V₉` cardinalities (reused verbatim from `D0.Core.FiniteTypes`). The
matrix-exponential continuum bridge and the halting-quotient interpretation stay in the cert.
-/

namespace D0.IM

open D0

/-- Active substrate after `n` ticks: `Aₙ = (1/φ)ⁿ`. -/
noncomputable def fcwActive (n : ℕ) : ℝ := phi⁻¹ ^ n

/-- Accumulated archive after `n` ticks: `Bₙ = 1 − (1/φ)ⁿ`. -/
noncomputable def fcwArchive (n : ℕ) : ℝ := 1 - phi⁻¹ ^ n

/-- The contraction rate is the golden root: `1/φ = primitiveRoot`. -/
theorem fcw_rate_eq_primitiveRoot : phi⁻¹ = primitiveRoot := phi_inv_eq_primitiveRoot

/-- **Substrate conserved:** `Aₙ + Bₙ = 1` for every `n`. -/
theorem fcw_substrate_conserved (n : ℕ) : fcwActive n + fcwArchive n = 1 := by
  unfold fcwActive fcwArchive; ring

/-- **Archive strictly grows:** `Bₙ < Bₙ₊₁` for every `n` (irreversible trace accumulation). -/
theorem fcw_archive_strictly_grows (n : ℕ) : fcwArchive n < fcwArchive (n + 1) := by
  unfold fcwArchive
  have hpos : (0 : ℝ) < phi⁻¹ := inv_pos.mpr (by linarith [phi_gt_one])
  have h1 : phi⁻¹ - 1 < 0 := by
    rw [phi_inv_eq_primitiveRoot]; unfold primitiveRoot; linarith [sqrt_five_lt_three]
  have hn : (0 : ℝ) < phi⁻¹ ^ n := pow_pos hpos n
  have key : phi⁻¹ ^ (n + 1) < phi⁻¹ ^ n := by
    rw [pow_succ]; nlinarith [mul_neg_of_pos_of_neg hn h1]
  linarith

/-- The witness state space: `|Ω₈| = 8`, `|V₉| = 9` (reused from `D0.Core.FiniteTypes`). -/
theorem fcw_witness_card : Fintype.card Omega8 = 8 ∧ Fintype.card V9 = 9 :=
  ⟨card_omega8, card_v9⟩

/-- **D0-IM-005.** `q = primitiveRoot`; substrate conserved and archive strictly growing for every `n`;
and the finite witness state space has `|Ω₈| = 8`, `|V₉| = 9`. -/
theorem fractal_continuum_witness_halting_corrected :
    phi⁻¹ = primitiveRoot ∧
    (∀ n : ℕ, fcwActive n + fcwArchive n = 1) ∧
    (∀ n : ℕ, fcwArchive n < fcwArchive (n + 1)) ∧
    Fintype.card Omega8 = 8 ∧ Fintype.card V9 = 9 :=
  ⟨fcw_rate_eq_primitiveRoot, fcw_substrate_conserved, fcw_archive_strictly_grows,
   card_omega8, card_v9⟩

end D0.IM
