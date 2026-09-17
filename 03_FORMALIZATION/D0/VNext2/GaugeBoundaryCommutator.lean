import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Trace
import Mathlib.Data.Complex.Basic
import Mathlib.Tactic

/-!
# Gauge-boundary commutator obstruction — algebraic core (`D0-CVFT-F6`, finite leg)

The finite Yang–Mills leakage / mass-gap *language* of the corpus needs a gauge-boundary commutator
obstruction. The quantitative statement (proved exactly in `vp_gauge_boundary_commutator_theorem.py`) is
`‖[P,g]‖_F² = 2‖QgP‖_F²` for Hermitian `g` and an orthogonal projection `P` (`Q = I − P`). The
*algebraic core* that drives it — proved here for any commutative-enough ring and any idempotent `P` with
`Q = 1 − P` — is the block decomposition

  `[P, g] = P g Q − Q g P`,

i.e. the commutator of a matrix with an idempotent has **no diagonal (PgP, QgQ) blocks**: it lives purely
in the two off-diagonal corners `PgQ` and `QgP`. This is exactly why a *zone-preserving* generator
(block-diagonal w.r.t. `P`, so `PgQ = QgP = 0`) has zero commutator/leakage, while a boundary-crossing
generator has a nonzero off-block corner and hence a nonzero commutator — the mechanism behind the
quantized gap.
-/

namespace D0.VNext2.GaugeBoundaryCommutator

open Matrix

variable {n : Type*} [Fintype n] [DecidableEq n] {R : Type*} [CommRing R]

/-- The commutator of two matrices. -/
def commutator (P g : Matrix n n R) : Matrix n n R := P * g - g * P

/-- For an idempotent `P` with complement `Q = 1 − P`, the commutator `[P,g]` decomposes into the two
off-diagonal corners: `[P,g] = P g Q − Q g P`. The diagonal `PgP`/`QgQ` blocks cancel. -/
theorem commutator_eq_offblocks (P g : Matrix n n R) :
    commutator P g = P * g * (1 - P) - (1 - P) * g * P := by
  unfold commutator
  have e1 : P * g * (1 - P) = P * g - P * g * P := by
    rw [mul_sub, mul_one]
  have e2 : (1 - P) * g * P = g * P - P * g * P := by
    rw [sub_mul, sub_mul, one_mul]
  rw [e1, e2]
  abel

/-- A **zone-preserving** generator — block-diagonal w.r.t. `P`, i.e. its two off-block corners vanish
(`P g Q = 0` and `Q g P = 0`) — commutes with `P`: zero leakage. -/
theorem zone_preserving_zero_commutator (P g : Matrix n n R)
    (hPgQ : P * g * (1 - P) = 0) (hQgP : (1 - P) * g * P = 0) :
    commutator P g = 0 := by
  rw [commutator_eq_offblocks P g, hPgQ, hQgP, sub_zero]

/-- The off-block corner `Q g P` equals `g P − P g P` (its explicit form), so a nonzero boundary-crossing
coupling forces a nonzero corner — the source of the quantized commutator gap. -/
theorem offblock_qgp (P g : Matrix n n R) :
    (1 - P) * g * P = g * P - P * g * P := by
  rw [sub_mul, sub_mul, one_mul]

end D0.VNext2.GaugeBoundaryCommutator
