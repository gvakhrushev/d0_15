import Mathlib.Data.Matrix.Basic
import Mathlib.Data.Real.Basic
import Mathlib.Data.Fintype.Basic
import Mathlib.Tactic
import D0.Algebra.ArchiveCommutatorOperators

namespace D0.Gauge

open D0.Algebra

/-- Finite seam map B : C1 -> C1 (forgetting seam). -/
structure FiniteSeamMap (n : Type) [Fintype n] where
  B : Matrix n n ℝ

/-- Gauge generator representation rho(X). -/
noncomputable def gaugeAction {n : Type} [Fintype n] (X : Matrix n n ℝ) (A : Matrix n n ℝ) : Matrix n n ℝ :=
  commutator X A

/-- Seam commutator O_B(X) = [B, rho(X)]. -/
noncomputable def seamCommutator {n : Type} [Fintype n]
    (B : FiniteSeamMap n) (X : Matrix n n ℝ) : Matrix n n ℝ :=
  commutator B.B X

/-- Seam energy E_seam(X) = ||O_B(X)||_F^2 . -/
noncomputable def seamEnergy {n : Type} [Fintype n]
    (B : FiniteSeamMap n) (X : Matrix n n ℝ) : ℝ :=
  let O := seamCommutator B X
  ∑ i, ∑ j, (O i j)^2

theorem seam_energy_nonnegative {n : Type} [Fintype n]
    (B : FiniteSeamMap n) (X : Matrix n n ℝ) :
    seamEnergy B X ≥ 0 := by
  unfold seamEnergy
  apply Finset.sum_nonneg
  intro i _
  apply Finset.sum_nonneg
  intro j _
  nlinarith

-- The seam norm-zero <-> commutes equivalence, the finite positive-gap statement,
-- and the abelian zero-energy statement are owned at cert level and remain open as
-- Lean theorem-targets. The prior `theorem _ : Prop := True` placeholders were
-- removed: they declared a type `Prop` (rejected as "type of theorem is not a
-- proposition") and proved nothing. `seamEnergy` and its non-negativity stay real.

end D0.Gauge
