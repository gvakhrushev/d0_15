import Mathlib.Data.Matrix.Basic
import Mathlib.Algebra.BigOperators.Fin
import D0.Geometry.ArchiveRolePhaseCarrier

open scoped BigOperators

namespace D0

/-!
# Metric role-product archive Laplacian

The scalar Weyl certificate uses the periodic finite-difference spectrum

```
lambda(k) = sum_r 4 L^2 sin(pi k_r / L)^2.
```

This module supplies the finite operator whose Gram spectrum has exactly that form.  The construction
is incidence-first rather than adjacency-first: every role and every product vertex supplies one
oriented forward difference.  This retains the two oriented incidences at the degenerate `L = 2`
stage, where a simple boolean cycle graph would collapse them into one undirected edge.

No continuum Weyl asymptotic is asserted here.
-/

/-- One oriented forward incidence for every role at every product vertex. -/
abbrev ArchiveRolePhaseEdge (n : Nat) : Type :=
  Role × ArchiveRolePhasePoint n

/-- Cyclic successor in a one-dimensional archive phase fibre. -/
def archivePhaseSucc (n : Nat) (i : archivePhaseIndex n) : archivePhaseIndex n :=
  ⟨(i.val + 1) % archiveFibers n, by
    have hpos : 0 < archiveFibers n := by
      unfold archiveFibers
      omega
    exact Nat.mod_lt _ hpos⟩

/-- Shift exactly one role coordinate forward by one cyclic phase step. -/
def archiveRolePhaseShift (n : Nat) (r : Role) (x : ArchiveRolePhasePoint n) :
    ArchiveRolePhasePoint n :=
  fun s => if s = r then archivePhaseSucc n (x s) else x s

/--
Metric forward coboundary.  The coefficient `archiveFibers n = L` is the inverse nearest-neighbour
phase spacing, so its Gram square carries the `L^2` continuum normalization without a new scale datum.
-/
def archiveRoleCoboundary (n : Nat) :
    Matrix (ArchiveRolePhaseEdge n) (ArchiveRolePhasePoint n) ℝ :=
  fun e y =>
    (archiveFibers n : ℝ) *
      ((if y = archiveRolePhaseShift n e.1 e.2 then (1 : ℝ) else 0) -
       (if y = e.2 then (1 : ℝ) else 0))

/-- The metric role-product Laplacian is the Gram operator `Bᵀ B`. -/
def archiveRoleProductLaplacian (n : Nat) :
    Matrix (ArchiveRolePhasePoint n) (ArchiveRolePhasePoint n) ℝ :=
  (archiveRoleCoboundary n).transpose * archiveRoleCoboundary n

/-- The product Laplacian is self-adjoint by its Gram construction. -/
theorem archiveRoleProductLaplacian_symmetric (n : Nat) :
    (archiveRoleProductLaplacian n).transpose = archiveRoleProductLaplacian n := by
  unfold archiveRoleProductLaplacian
  rw [Matrix.transpose_mul, Matrix.transpose_transpose]

/-- A constant potential has zero metric coboundary. -/
theorem archiveRoleCoboundary_constant_zero (n : Nat) (c : ℝ) :
    Matrix.mulVec (archiveRoleCoboundary n) (fun _ => c) = 0 := by
  classical
  funext e
  rcases e with ⟨r, x⟩
  simp [archiveRoleCoboundary, Matrix.mulVec, dotProduct]
  ring

/-- Consequently constants are zero modes of the role-product Laplacian. -/
theorem archiveRoleProductLaplacian_constant_zero (n : Nat) (c : ℝ) :
    Matrix.mulVec (archiveRoleProductLaplacian n) (fun _ => c) = 0 := by
  unfold archiveRoleProductLaplacian
  rw [← Matrix.mulVec_mulVec, archiveRoleCoboundary_constant_zero]
  simp

/-- Positive Dirichlet energy owned directly by the metric coboundary. -/
def archiveRoleMetricEnergy (n : Nat) (f : ArchiveRolePhasePoint n → ℝ) : ℝ :=
  ∑ e : ArchiveRolePhaseEdge n, (Matrix.mulVec (archiveRoleCoboundary n) f e) ^ 2

theorem archiveRoleMetricEnergy_nonnegative
    (n : Nat) (f : ArchiveRolePhasePoint n → ℝ) :
    0 ≤ archiveRoleMetricEnergy n f := by
  unfold archiveRoleMetricEnergy
  exact Finset.sum_nonneg (fun _ _ => sq_nonneg _)

/-- Packaging owner for the finite metric product operator. -/
theorem archive_role_product_laplacian_owner (n : Nat) :
    (archiveRoleProductLaplacian n).transpose = archiveRoleProductLaplacian n ∧
      (∀ c : ℝ, Matrix.mulVec (archiveRoleProductLaplacian n) (fun _ => c) = 0) ∧
      (∀ f : ArchiveRolePhasePoint n → ℝ, 0 ≤ archiveRoleMetricEnergy n f) := by
  exact ⟨archiveRoleProductLaplacian_symmetric n,
    archiveRoleProductLaplacian_constant_zero n,
    archiveRoleMetricEnergy_nonnegative n⟩

end D0
