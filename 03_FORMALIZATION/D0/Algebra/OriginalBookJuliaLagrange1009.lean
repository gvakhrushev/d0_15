import D0.Algebra.OriginalBookRadicalMod1009
import Mathlib.Tactic

/-!
# Pinned modular Julia-root Lagrange identity

This is the polynomial from pinned modular source blob
 d111c5bfeae3c384a4fe725f4a6d19277ea0005a, lines 101–122, at commit
 eebcb5e467742df3e9cf7fa9702042d7294aa742. At prime 1009 the original
spectral constants are t1=969, t2=410 and the selected root values are
1, 4/5=808, and 278. The identities below are purely finite-field algebra:
no order or positivity is inferred from F1009. The later source application
must provide the actual two projectors and source Gram matrices.
-/
open Matrix
open D0.Algebra.OriginalBookRadicalMod1009

namespace D0.Algebra.OriginalBookJuliaLagrange1009

/-- Exact coefficients of the three source Lagrange terms. -/
theorem source_lagrange_coefficients :
    (1 / ((969 : ZMod 1009) * 410)) = 67 ∧
    ((4 / 5 : ZMod 1009) / (969 * (969 - 410))) = 431 ∧
    ((278 : ZMod 1009) / (410 * (410 - 969))) = 609 ∧
    (4 / 5 : ZMod 1009) = 808 := by decide

variable {n : Type*} [Fintype n] [DecidableEq n]

/-- The original three spectral interpolation terms, with exact field coefficients. -/
def sourceLagrange (T : Matrix n n (ZMod 1009)) : Matrix n n (ZMod 1009) :=
  (67 : ZMod 1009) • ((T - (969 : ZMod 1009) • 1) * (T - (410 : ZMod 1009) • 1)) +
  (431 : ZMod 1009) • (T * (T - (410 : ZMod 1009) • 1)) +
  (609 : ZMod 1009) • (T * (T - (969 : ZMod 1009) • 1))

/-- Normalized polynomial form over F1009. -/
theorem sourceLagrange_polynomial (T : Matrix n n (ZMod 1009)) :
    sourceLagrange T = 1 + (444 : ZMod 1009) • T + (98 : ZMod 1009) • (T * T) := by
  simp [sourceLagrange, sub_mul, mul_sub]
  match_scalars <;> decide

/-- Lagrange works for any two orthogonal idempotents, including degenerate blocks. -/
theorem sourceLagrange_projectors (P Q : Matrix n n (ZMod 1009))
    (hP : P * P = P) (hQ : Q * Q = Q) (hPQ : P * Q = 0) (hQP : Q * P = 0) :
    sourceLagrange ((969 : ZMod 1009) • P + (410 : ZMod 1009) • Q) =
      1 - P - Q + (808 : ZMod 1009) • P + (278 : ZMod 1009) • Q := by
  rw [sourceLagrange_polynomial]
  simp [add_mul, mul_add, smul_smul, hP, hQ, hPQ, hQP]
  match_scalars <;> decide

end D0.Algebra.OriginalBookJuliaLagrange1009
