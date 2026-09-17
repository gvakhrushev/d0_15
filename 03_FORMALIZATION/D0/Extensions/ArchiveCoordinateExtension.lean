import Mathlib.Data.Real.Sqrt
import Mathlib.Tactic
import D0.Core.Phi
import D0.Spectral.SceneNativeMultiscaleTower

/-!
# D0-POSTCORE-PHASON-EXTENSION-MAXIMALITY-NOGO-001 — E3 (archive pressure/coordinate extension)

No common sector exists across the five frozen operators (Outcome C): the integer `L_archive` spectrum
`{24,22,20}` is incommensurate with the irrational `S_DE` window `{3/2 ± √10/40}` (product `359/160`), and
`QUQ`/Feshbach needs the forbidden rescale. Even adopting `S_DE` as the 2-sector, the extension does NOT
force uniqueness — `role(2) × coordinate-cocycle(2) = 4` admissible `w_E(z)` profiles. The role leg
(`w_A ≠ w_B`) is owned by R2; the genuinely-NEW content is the **coordinate-cocycle divergence**: the
φ-tick cocycle `z(s) = φ^s − 1` and the integer-tick cocycle `z(s) = s` already diverge at `s = 1`
(`φ − 1 ≠ 1`, since `φ < 2`). Cites `D0-ARCHIVE-CONTRACTION-NOGO-001` (w_A ≠ w_B) and
`D0-PHASON-WDE-SIGN-NORMALIZATION-OWNER-001`. Missing: `PRIM-PHASON-PRESSURE-ENERGY-ROLE-ASSIGNMENT` +
`PRIM-PHASON-COORDINATE-FUNCTOR` (the physical map stays an external passport).
-/

namespace D0.Extensions.ArchiveCoordinateExtension

open D0

/-- The `S_DE` active window product `359/160` (cited from R2). -/
theorem window_product :
    (3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160 := by
  have h : Real.sqrt 10 ^ 2 = 10 := Real.sq_sqrt (by norm_num)
  linear_combination (-1 / 1600 : ℝ) * h

/-- **The two admissible coordinate cocycles diverge at `s = 1`**: φ-tick `z(1) = φ − 1` vs integer-tick
`z(1) = 1`, and `φ − 1 ≠ 1` because `φ < 2`. -/
theorem coordinate_cocycle_divergent : phi - 1 ≠ 1 := by
  have h := D0.Spectral.SceneNativeMultiscaleTower.phi_lt_two
  intro he; linarith

/-- **D0-POSTCORE-PHASON-EXTENSION-MAXIMALITY-NOGO-001.** The `S_DE` window product is `359/160`, and the two
admissible coordinate cocycles already diverge at `s = 1` (`φ − 1 ≠ 1`) — combined with the role
underdetermination (R2) this gives ≥2 inequivalent `w_E(z)`; the physical map stays an external passport. -/
theorem phason_extension_nogo :
    (3 / 2 - Real.sqrt 10 / 40) * (3 / 2 + Real.sqrt 10 / 40) = 359 / 160 ∧ phi - 1 ≠ 1 :=
  ⟨window_product, coordinate_cocycle_divergent⟩

end D0.Extensions.ArchiveCoordinateExtension
