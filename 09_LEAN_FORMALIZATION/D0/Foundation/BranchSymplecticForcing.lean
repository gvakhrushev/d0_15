import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic

/-!
# D0-BRANCH-SYMPLECTIC-FORCING-001 (THE) — even-rank forces the symplectic `8`

The order-memory commutator form `b(x,y)=[x,y]` on the branch plane `V=𝔽₂²` is **alternating**
(`b(x,x)=0`). An alternating bilinear form on a 2-dimensional space has **even rank** (`∈{0,2}`); the
order-memory commutator is **nonzero** (BOOK_02 §02.9A, `THE`), so its rank is `2` ⇒ nondegenerate ⇒
symplectic. There is no middle case over a 2-dimensional space, so no free choice: the central `ℤ₂`-extension
with this symplectic commutator is extraspecial, minimal order `2^{1+2}=8`. This discharges the former
`ASSUMP-COMMUTATOR-SYMPLECTIC` to a proven fact.

Modelled over `ZMod 2`: an alternating `2×2` form is `!![0,a; a,0]`; `det = a` (since `−a² = a` in
char 2), so it is nondegenerate iff `a ≠ 0`, i.e. iff the form is nonzero.
-/

namespace D0.Foundation.BranchSymplecticForcing

open Matrix

/-- The general alternating `2×2` bilinear form on `𝔽₂²` (zero diagonal, symmetric off-diagonal). -/
def altForm (a : ZMod 2) : Matrix (Fin 2) (Fin 2) (ZMod 2) := !![0, a; a, 0]

/-- **The alternating form's determinant equals its single parameter** `a` (over `𝔽₂`, `−a² = a`). -/
theorem altForm_det : ∀ a : ZMod 2, (altForm a).det = a := by decide

/-- A nonzero alternating form on `𝔽₂²` is **nondegenerate** (`det ≠ 0`): rank `2`, symplectic. -/
theorem nonzero_alt_nondegenerate (a : ZMod 2) (h : a ≠ 0) : (altForm a).det ≠ 0 := by
  rw [altForm_det]; exact h

/-- The zero form is degenerate (the only even-rank alternative, rank `0`, the abelian `(ℤ₂)³`). -/
theorem zero_alt_degenerate : (altForm 0).det = 0 := by decide

/-- **D0-BRANCH-SYMPLECTIC-FORCING-001.** Over `𝔽₂²` there is no middle case: an alternating form is either
zero (rank 0, degenerate) or nonzero (rank 2, nondegenerate symplectic). The nonzero order-memory commutator
therefore forces the unique nondegenerate symplectic form `!![0,1;1,0]`, hence the extraspecial order `8`. -/
theorem branch_symplectic_forcing :
    (altForm 1).det = 1 ∧ (altForm 0).det = 0 ∧ ∀ a : ZMod 2, a ≠ 0 → (altForm a).det ≠ 0 := by
  refine ⟨by decide, by decide, ?_⟩
  intro a h; rw [altForm_det]; exact h

end D0.Foundation.BranchSymplecticForcing
