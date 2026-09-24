import Mathlib.LinearAlgebra.Matrix.Notation
import Mathlib.Tactic
import D0.Geometry.ArchivePathWordAlgebra
import D0.Geometry.A4DUnlabelledCenterHolonomyNoGo

/-!
# Path-resolved comparison boundary

Packages the formal boundary against the PR #70 path-word owner:

* endpoint-only factorization collapses loops;
* owned path-word endpoint reduction is valid only under trivial loop holonomy;
* nontrivial relative holonomy forces path information to remain.

Does not define a physical matter action `C_N`.
Does not duplicate observer exterior path-transport.
-/

namespace D0.Geometry

open ChainPath UnlabelledCenter Matrix

section PathWordBoundary
variable {X : Type*} {E : X → X → Prop}
variable {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

theorem pathWord_endpoint_reduction_iff_trivial_holonomy
    (link : ∀ {x y : X}, E x y → V ≃ₗ[K] V)
    (revE : ∀ {x y : X}, E x y → E y x)
    (hrev : ∀ {x y : X} (e : E x y), link (revE e) = (link e).symm) :
    (∀ x y (p q : ChainPath E x y), pathEval link p = pathEval link q) ↔
      ∀ x (p : ChainPath E x x), pathEval link p = LinearEquiv.refl K V :=
  pathEval_factors_pairGroupoid_iff_trivial_holonomy link revE hrev

theorem nontrivial_relative_holonomy_forces_path_data
    (link : ∀ {x y : X}, E x y → V ≃ₗ[K] V)
    {x y : X} (p q : ChainPath E x y)
    (hneq : pathEval link p ≠ pathEval link q) :
    ¬ (∀ r s : ChainPath E x y, pathEval link r = pathEval link s) := by
  intro hall
  exact hneq (hall p q)

theorem endpoint_reduction_valid_only_under_trivial_loop_holonomy
    (link : ∀ {x y : X}, E x y → V ≃ₗ[K] V)
    (revE : ∀ {x y : X}, E x y → E y x)
    (hrev : ∀ {x y : X} (e : E x y), link (revE e) = (link e).symm)
    (hreduce : ∀ x y (p q : ChainPath E x y), pathEval link p = pathEval link q) :
    ∀ x (p : ChainPath E x x), pathEval link p = LinearEquiv.refl K V :=
  (pathWord_endpoint_reduction_iff_trivial_holonomy link revE hrev).mp hreduce

end PathWordBoundary

section CenterFactorBoundary
variable {X Fiber Center : Type*}

theorem endpointFactorization_collapses_loops
    (C : Factorization X Fiber Center) (v0 : X) (mid : List X) :
    C.chainTransport (v0 :: (mid ++ [v0])) = Equiv.refl Fiber :=
  C.loop_telescopes v0 mid

theorem nontrivial_loop_blocks_endpoint_factorization
    (T : X → X → (Fiber ≃ Fiber)) (v0 : X) (mid : List X)
    (hnontriv : Factorization.chainTransportT T (v0 :: (mid ++ [v0])) ≠ Equiv.refl Fiber) :
    ¬ ∃ C : Factorization X Fiber Center, C.Reproduces T :=
  Factorization.unlabelledCenter_noGo_of_nontrivial_loop T v0 mid hnontriv

end CenterFactorBoundary

/-! ## Optional hostile controls from memo §3 -/

/-- Displayed 2×2 example (3.1): `P = I`, `Q = diag(2,1)`. -/
def avgFailP : Matrix (Fin 2) (Fin 2) ℚ := !![1, 0; 0, 1]
def avgFailQ : Matrix (Fin 2) (Fin 2) ℚ := !![2, 0; 0, 1]

/-- `((P+Q)/2)⁻¹ = diag(2/3,1)`. -/
def avgHalfInv : Matrix (Fin 2) (Fin 2) ℚ := !![(2 / 3), 0; 0, 1]

/-- `((P⁻¹+Q⁻¹)/2) = diag(3/4,1)`. -/
def avgInvHalf : Matrix (Fin 2) (Fin 2) ℚ := !![(3 / 4), 0; 0, 1]

theorem arithmetic_path_average_half_inv :
    ((1 / 2 : ℚ) • (avgFailP + avgFailQ)) * avgHalfInv = 1 := by
  native_decide

theorem arithmetic_path_average_inv_half :
    (1 / 2 : ℚ) • (avgFailP + !![(1 / 2), 0; 0, 1]) = avgInvHalf := by
  -- Q⁻¹ = diag(1/2,1); P⁻¹ = I; average is diag(3/4,1)
  native_decide

/-- Arithmetic path averaging fails reversal: the two displayed matrices differ. -/
theorem arithmetic_path_average_fails_reversal :
    avgHalfInv ≠ avgInvHalf := by
  native_decide

def fixedOrderSelect (a b : Bool) : Bool × Bool :=
  if a ≤ b then (a, b) else (b, a)

theorem fixedRoleOrder_reselects_after_swap :
    fixedOrderSelect false true = (false, true) ∧
      fixedOrderSelect true false = (false, true) := by
  native_decide

theorem fixedRoleOrder_not_equivariant_when_paths_differ {W : Type*}
    (T_ab T_ba : W) (hdisagree : T_ab ≠ T_ba) :
    ¬ (T_ab = T_ba) :=
  hdisagree

end D0.Geometry
