import D0.Core.Phi
import Mathlib.Tactic

/-!
# D0-PISOT-CONTRACTION-TIME-ARROW-001 — the arrow of time as Pisot contraction

BOOK_06 §06.36 reads the arrow of time as the Pisot contraction of the Galois conjugate: the dominant
root `φ` of the monic integer quadratic `x² − x − 1` expands (`φ > 1`) while its Galois conjugate
`ψ = (1−√5)/2` contracts (`|ψ| < 1`). Both are algebraic integers (roots of the monic `x²−x−1`:
`φ² = φ+1`, `ψ² = ψ+1`), so `φ` is a Pisot number and the contraction `|ψ| < 1` is the irreversible
direction. This module proves the contraction explicitly from `D0.Core.Phi`. (The full Mathlib
`Polynomial`/`IsIntegral` Pisot-number class is the named continuation; the operative contraction
inequalities are internal here.)
-/

namespace D0

open Real

/-- `√5 > 2` (since `(√5)² = 5 > 4`). -/
theorem sqrt_five_gt_two : Real.sqrt 5 > 2 := by
  nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]

/-- `√5 < 3` (since `(√5)² = 5 < 9`). -/
theorem sqrt_five_lt_three : Real.sqrt 5 < 3 := by
  nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]

/-- The dominant root expands: `φ > 1`. -/
theorem phi_gt_one : phi > 1 := by
  unfold phi; nlinarith [sqrt_five_gt_two]

/-- The Galois conjugate contracts: `|ψ| < 1`. -/
theorem abs_psi_lt_one : |psi| < 1 := by
  rw [abs_lt]; unfold psi
  exact ⟨by nlinarith [sqrt_five_lt_three], by nlinarith [Real.sqrt_nonneg 5]⟩

/-- The conjugate is strictly inside the unit interval and negative (the contracting, time-reversing
direction): `−1 < ψ < 0`. -/
theorem psi_neg : psi < 0 := by
  unfold psi; nlinarith [sqrt_five_gt_two]

/-- **Pisot contraction (arrow of time).** `φ` (dominant root of the monic `x²−x−1`) expands `> 1`;
its Galois conjugate `ψ` contracts `|ψ| < 1`; the pair are conjugate roots (`φ+ψ=1`, `φψ=−1`). So `φ`
is a Pisot number and `ψ` is the irreversible contraction. -/
theorem pisot_contraction :
    phi > 1 ∧ |psi| < 1 ∧ phi + psi = 1 ∧ phi * psi = -1 :=
  ⟨phi_gt_one, abs_psi_lt_one, phi_add_psi, phi_mul_psi⟩

end D0
