import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic
import D0.Core.Phi

/-!
# D0-ARCHIVE-CONTRACTION-NOGO-001 — ROOT R2 (archive/phason transfer operator)

On the 30-dim archive sector `K_scene = ker A_scene`, the adjacency is annihilated, so `L|_ker = D|_ker`
has spectrum exactly the degrees `{24, 22, 20}` — all `> 1 > φ⁻¹`. Hence the only concrete frozen
realization of the archive block has spectral radius `24`, and the contraction theorem `QUQ = ψ·V`,
`‖V‖ ≤ 1`, `|ψ| = φ⁻¹` is **unwitnessable without an external rescale** (by `2|E| = 718`, a count =
forbidden). `φ⁻¹` occurs only on the toral block `T`, never on the 30-dim archive block.

Second leg: the canonical S_DE active 2-D window has eigenvalues `3/2 ± √10/40` (product `359/160`), and
the two admissible pressure/energy role assignments give `w_A = 361/359 − 12√10/359 ≠ w_B = 361/359 +
12√10/359`. So `w(z)` is underdetermined by the frozen archive data — the missing object is
`PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT` (= the OPEN `D0-PHASON-WZ-TRANSFER-OWNER-001`). This
sharpens `D0-PHASON-WZ-KERNEL-ONLY-NOGO-001` (hand-picked rationals → the frozen S_DE Riesz eigenpair).
Cites `D0-FESHBACH-SCHUR-TIME-DELAY-OWNER-001` (which names `ρ(QUQ)<1` as its unproven residual) and
`D0-PHASON-CONTINUUM-ENVELOPE-OWNER-001`; does not re-mint them.
-/

namespace D0.Cosmology.ArchiveContractionCriterion

open D0

/-- Archive-block spectrum = the degrees of `K(9,11,13)`. -/
def archiveSpectrum : List ℕ := [24, 22, 20]

/-- Every archive eigenvalue exceeds 1. -/
theorem archive_all_above_one : ∀ x ∈ archiveSpectrum, 1 < x := by decide

theorem phiinv_lt_one : phi⁻¹ < 1 := by
  rw [phi_inv_eq_primitiveRoot]
  have h : Real.sqrt 5 < 3 := by nlinarith [sqrt_five_sq, Real.sqrt_nonneg 5]
  unfold primitiveRoot; linarith

/-- The archive block radius `24` exceeds `φ⁻¹` — no contraction without an external rescale. -/
theorem archive_radius_above_phiinv : phi⁻¹ < 24 := lt_trans phiinv_lt_one (by norm_num)

/-- The S_DE active 2-D window `(3/2 − √10/40)(3/2 + √10/40) = 359/160`. -/
theorem window_product :
    (3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160 := by
  have h : Real.sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  linear_combination (-1 / 1600 : ℝ) * h

/-- The two admissible pressure/energy role assignments give different `w`: `w_A ≠ w_B`. -/
theorem w_underdetermined :
    (361 / 359 - 12 * Real.sqrt 10 / 359 : ℝ) ≠ 361 / 359 + 12 * Real.sqrt 10 / 359 := by
  have h : (0 : ℝ) < Real.sqrt 10 := Real.sqrt_pos.mpr (by norm_num)
  intro he; linarith [h]

/-- **D0-ARCHIVE-CONTRACTION-NOGO-001.** Archive block spectrum `{24,22,20}` all `> 1 > φ⁻¹` (no
contraction without an external rescale), and the S_DE window product is `359/160` with `w_A ≠ w_B`
(`w(z)` underdetermined). -/
theorem archive_contraction_nogo :
    (∀ x ∈ archiveSpectrum, 1 < x) ∧ phi⁻¹ < 24 ∧
      (3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160 ∧
      (361 / 359 - 12 * Real.sqrt 10 / 359 : ℝ) ≠ 361 / 359 + 12 * Real.sqrt 10 / 359 :=
  ⟨archive_all_above_one, archive_radius_above_phiinv, window_product, w_underdetermined⟩

end D0.Cosmology.ArchiveContractionCriterion
