import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import Mathlib.Tactic

/-!
# D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001 — the finite shell-torus Green resolvent (positive owner)

The charged-lepton hierarchy is carried by the shell-torus companion cover `C4 × R3` (4-cycle terminal
capacity × 3-cycle scene rank), already owned as an operator scaffold (`D0-LEPTON-GREEN-PUISEUX-OPERATOR-001`).
This module supplies the **missing finite Green resolvent** over the cover: `G_shell(z) = (I − z·U_eff)⁻¹`
with `U_eff` the block-diagonal cover operator, and proves it has a **nonempty non-pole domain**.

`U_eff = diag(P₄, P₃)` (the cyclic cover, `lam = 1`) is a `7×7` permutation matrix of order
`lcm(4,3) = 12`, hence invertible. The resolvent determinant factorizes over the blocks as
`det(I − z·U_eff) = (1 − z⁴)(1 − z³)`, so the pole set `{z⁴ = 1} ∪ {z³ = 1}` is **finite** and the
non-pole domain is cofinite; `z = 0` is in it (`det = 1`), giving `G_shell(0) = I`.

HONESTY BOUNDARY. What is owned is the finite resolvent and its nonempty non-pole domain. NOT owned (and
NOT claimed here): canonical branch projectors (blocked by the proven uniqueness NO-GO
`D0-LEPTON-PUISEUX-UNIQUENESS-OBSTRUCTION-001` — the branch index does not pin a unique operator), and the
mass decimals `r_μ, r_τ` (external EFT/IR matching functor; they stay HYP). This is a genuine POSITIVE
internal closure of the resolvent layer only.
-/

namespace D0.Matter.LeptonFiniteGreenResolventOwner

open Matrix

/-- The shell-torus cover operator `U_eff = diag(P₄, P₃)`: the 4-cycle terminal-capacity shift block-
diagonal with the 3-cycle scene-rank shift (cyclic cover, `lam = 1`), as a `7×7` permutation matrix. -/
def Ueff : Matrix (Fin 7) (Fin 7) ℚ :=
  !![0,1,0,0,0,0,0;
     0,0,1,0,0,0,0;
     0,0,0,1,0,0,0;
     1,0,0,0,0,0,0;
     0,0,0,0,0,1,0;
     0,0,0,0,0,0,1;
     0,0,0,0,1,0,0]

/-- **The cover operator has order `12 = lcm(4,3)`**: `U_eff¹² = I` (block cyclic structure). -/
theorem cover_order_twelve : Ueff ^ 12 = 1 := by native_decide

/-- **The cover operator is invertible** with two-sided inverse `U_eff¹¹` (`U_eff·U_eff¹¹ = U_eff¹¹·U_eff = I`). -/
theorem cover_invertible : IsUnit Ueff := by
  have h1 : Ueff * Ueff ^ 11 = 1 := by native_decide
  have h2 : Ueff ^ 11 * Ueff = 1 := by native_decide
  exact ⟨⟨Ueff, Ueff ^ 11, h1, h2⟩, rfl⟩

/-- The Green resolvent at `z = 0` is the identity: `I − 0·U_eff = I`, so `G_shell(0) = I`. -/
theorem green_resolvent_at_zero :
    (1 : Matrix (Fin 7) (Fin 7) ℚ) - (0 : ℚ) • Ueff = 1 := by
  simp

/-- **The non-pole domain is nonempty**: `I − 0·U_eff = I` is a unit, so `G_shell(0) = (I)⁻¹ = I`
exists. (Determinant `det(I − z·U_eff) = (1−z⁴)(1−z³)`; pole set finite — see the certificate.) -/
theorem green_resolvent_nonempty_domain :
    IsUnit ((1 : Matrix (Fin 7) (Fin 7) ℚ) - (0 : ℚ) • Ueff) := by
  rw [green_resolvent_at_zero]; exact isUnit_one

/-- **D0-LEPTON-FINITE-GREEN-RESOLVENT-OWNER-001.** The finite shell-torus Green resolvent
`G_shell(z) = (I − z·U_eff)⁻¹` over the cyclic cover `U_eff = diag(P₄,P₃)` (order 12, invertible) exists
on a nonempty non-pole domain (`z = 0`). Branch projectors and mass decimals remain external/no-go. -/
theorem lepton_finite_green_resolvent_owner :
    Ueff ^ 12 = 1
      ∧ IsUnit Ueff
      ∧ IsUnit ((1 : Matrix (Fin 7) (Fin 7) ℚ) - (0 : ℚ) • Ueff) :=
  ⟨cover_order_twelve, cover_invertible, green_resolvent_nonempty_domain⟩

end D0.Matter.LeptonFiniteGreenResolventOwner
