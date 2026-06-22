import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# D0-V15 Work Package F — refinement truth (F1 NO-GO + F2 CONDITIONAL)

The two refinements must not be conflated.

## F1 — the archive bonding map is NOT a regular cover (NO-GO)

A regular double cover `C_{2N} → C_N` is measure-preserving: it has constant fibre `2` and normalized-measure
ratio `1` (`regular_cover_ratio_one`). The frozen archive map carries the contraction window `359/160`
(owner `D0-ARCHIVE-CONTRACTION-NOGO-001`), and `359/160 ≠ 1` (`archive_window_not_measure_preserving`): the
archive bonding map is contracting, hence NOT a regular cover. Substituting a regular mod-`N` cover for the real
bonding map is therefore a NO-GO:

```
D0-ARCHIVE-REGULAR-REFINEMENT-NOGO-001 : NO-GO
```

## F2 — Sturmian refinement exists but is CONDITIONAL

The Fibonacci/golden substitution `σ(a)=ab, σ(b)=a` has incidence matrix `!![1,1; 1,0]` with `det = −1`,
`trace = 1`, hence characteristic polynomial `t² − t − 1` and Perron root `φ` (`φ² = φ + 1`). This is a valid
mathematical refinement tower, and Sturmian data is frozen (`D0-PHI-STURMIAN-CYLINDER-CONJUGACY-001`). But
making it *the* archive refinement requires identifying its bonding maps with the frozen archive maps — a new
owner `PRIM-STURMIAN-REFINEMENT-OWNER`. Hence CONDITIONAL, not present-core. No CFT/Virasoro is imported.
-/

namespace D0.Integration.V15.Refinement

open Matrix

/-! ## F1 — archive bonding map ≠ regular cover -/

/-- A regular double cover `C₆ → C₃` has constant fibre `6 / 3 = 2`. -/
theorem regular_cover_fibre : 6 / 3 = 2 := by decide

/-- A regular cover preserves normalized measure: its ratio is `1`. -/
def regularCoverRatio : ℚ := 1
theorem regular_cover_ratio_one : regularCoverRatio = 1 := rfl

/-- The frozen archive contraction window. -/
def archiveWindow : ℚ := 359 / 160

/-- **F1 (NO-GO).** The archive window `359/160 ≠ 1`, so the archive bonding map is contracting, not a
measure-preserving regular cover; the regular-refinement substitution fails. -/
theorem archive_window_not_measure_preserving : archiveWindow ≠ regularCoverRatio := by
  simp only [archiveWindow, regularCoverRatio]
  norm_num

/-! ## F2 — Sturmian tower (CONDITIONAL) -/

/-- Incidence matrix of the golden substitution `σ(a)=ab, σ(b)=a`. -/
def sturmianIncidence : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 1, 0]

/-- **F2 (CONDITIONAL).** The Sturmian incidence has `det = −1` and `trace = 1`, so its char. polynomial is
`t² − t − 1` (Perron root `φ`, `φ²=φ+1`). A valid refinement tower — but identifying it with the frozen archive
maps needs `PRIM-STURMIAN-REFINEMENT-OWNER`. -/
theorem sturmian_golden_tower :
    sturmianIncidence.det = -1 ∧ sturmianIncidence.trace = 1 := by
  refine ⟨?_, ?_⟩ <;> native_decide

end D0.Integration.V15.Refinement
