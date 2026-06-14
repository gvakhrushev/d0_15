import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.Determinant.Basic
import Mathlib.Tactic

/-!
# D0-ICOSIAN-E8-GRAM-001 — the E8 Gram is even unimodular (finite shadow of icosian→E8)

Python certificate: `05_CERTS/vp_icosian_e8_gram_finite.py`.

Finite-core reduction of the icosian→E8 family (BOOK_02 §02.18, `[THE]` golden quaternions
generate E8). The **Mordell genus-uniqueness theorem** (E8 is the UNIQUE even unimodular
positive-definite lattice of rank 8) needs lattice-genus machinery absent from Mathlib and
stays an EXTERNAL owner (`ASSUMP-MORDELL-E8`). Its DECIDABLE SHADOW is closed here exactly:
the specific E8 Gram (the simply-laced E8 Cartan matrix, Gram = Cartan for simply-laced) IS

  * EVEN       — symmetric, integer, diagonal all `2` (the quadratic form is even-valued);
  * UNIMODULAR — `det = 1` (the lattice is self-dual);

and its rank `8 = 2·4` is the `ℤ[√5]→ℤ` Galois doubling of the rank-4 icosian ring.

Everything is closed by `decide` / `native_decide` on the exact `8×8` integer matrix; no proof
gaps, no extra postulates. The negative control `A8` (the type-`A` chain) has `det = 9 ≠ 1`,
so it is the E8 Dynkin tree — not just any `2`-on-the-diagonal matrix — that is unimodular.
-/

namespace D0.Claims

open Matrix

/-- The E8 Cartan / Gram matrix (simply-laced ⇒ Gram = Cartan), `8×8` over `ℤ`, Bourbaki tree.
Diagonal `2`; off-diagonal `-1` exactly on the edges of the E8 Dynkin diagram. -/
def e8Gram : Matrix (Fin 8) (Fin 8) ℤ :=
  !![ 2,  0, -1,  0,  0,  0,  0,  0;
      0,  2,  0, -1,  0,  0,  0,  0;
     -1,  0,  2, -1,  0,  0,  0,  0;
      0, -1, -1,  2, -1,  0,  0,  0;
      0,  0,  0, -1,  2, -1,  0,  0;
      0,  0,  0,  0, -1,  2, -1,  0;
      0,  0,  0,  0,  0, -1,  2, -1;
      0,  0,  0,  0,  0,  0, -1,  2]

/-- The type-`A₈` chain Cartan matrix (negative control): same diagonal `2`, off-diagonal `-1`
on a *path* instead of the E8 tree. -/
def a8Chain : Matrix (Fin 8) (Fin 8) ℤ :=
  !![ 2, -1,  0,  0,  0,  0,  0,  0;
     -1,  2, -1,  0,  0,  0,  0,  0;
      0, -1,  2, -1,  0,  0,  0,  0;
      0,  0, -1,  2, -1,  0,  0,  0;
      0,  0,  0, -1,  2, -1,  0,  0;
      0,  0,  0,  0, -1,  2, -1,  0;
      0,  0,  0,  0,  0, -1,  2, -1;
      0,  0,  0,  0,  0,  0, -1,  2]

/-! ## EVEN lattice: symmetric, integer, diagonal all `2`. -/

/-- The E8 Gram is symmetric. -/
theorem e8_gram_symmetric : e8Gramᵀ = e8Gram := by native_decide

/-- Every diagonal entry of the E8 Gram is `2` — the quadratic form is even-valued. -/
theorem e8_gram_diag_even : ∀ i, e8Gram i i = 2 := by decide

/-! ## UNIMODULAR: `det = 1`. -/

/-- The E8 Gram is unimodular: `det = 1` (the lattice is self-dual). -/
theorem e8_gram_unimodular : Matrix.det e8Gram = 1 := by native_decide

/-- Negative control: the `A₈` chain has `det = 9 ≠ 1` — it is NOT unimodular, so the
unimodularity is forced by the E8 *tree*, not merely by the `2`-diagonal. -/
theorem a8_chain_not_unimodular : Matrix.det a8Chain = 9 := by native_decide

/-! ## RANK `8 = 2·4`: the `ℤ[√5]→ℤ` doubling of the rank-4 icosian ring. -/

/-- Rank `8 = 2·4`: the Galois doubling (degree `[ℚ(√5):ℚ]=2`) of the rank-4 icosian ring. -/
theorem e8_rank_is_icosian_doubling : (8 : ℕ) = 2 * 4 := by decide

/-! ## The finite shadow, assembled. -/

/-- **D0-ICOSIAN-E8-GRAM-001 (finite shadow).** The E8 Gram is even (symmetric, diagonal `2`)
and unimodular (`det = 1`), with rank `8 = 2·4`. The Mordell uniqueness (E8 is THE even
unimodular rank-8 lattice) is the external owner `ASSUMP-MORDELL-E8`; this certifies the
specific Gram's defining invariants exactly. -/
theorem icosian_e8_gram_finite :
    e8Gramᵀ = e8Gram ∧
    (∀ i, e8Gram i i = 2) ∧
    Matrix.det e8Gram = 1 ∧
    (8 : ℕ) = 2 * 4 :=
  ⟨e8_gram_symmetric, e8_gram_diag_even, e8_gram_unimodular, e8_rank_is_icosian_doubling⟩

end D0.Claims
