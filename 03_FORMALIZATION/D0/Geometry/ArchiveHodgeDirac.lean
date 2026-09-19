import Mathlib.Data.Matrix.Basic
import D0.Geometry.ArchiveRoleProductLaplacian

namespace D0

/-!
# Finite Hodge--Dirac owner for the role-product archive

The metric coboundary `B : C^0 -> C^1` already owns the scalar product Laplacian
`B^T B`.  This module packages the associated finite Hodge--Dirac operator on
`C^0 ⊕ C^1`:

```
      [ 0   B^T ]
D_H = [         ].
      [ B    0  ]
```

Its square is block diagonal with `B^T B` on vertices and `B B^T` on oriented
one-forms.  This is an exact finite operator theorem.  It is not yet an
identification with a Lorentz spinor Dirac operator or with the continuum
Lichnerowicz curvature term.
-/

/-- Finite Hodge carrier: scalar states plus oriented metric one-forms. -/
abbrev ArchiveRoleHodgeCarrier (n : Nat) : Type :=
  Sum (ArchiveRolePhasePoint n) (ArchiveRolePhaseEdge n)

/-- One-form Hodge Laplacian paired with the scalar Gram Laplacian. -/
def archiveRoleOneFormLaplacian (n : Nat) :
    Matrix (ArchiveRolePhaseEdge n) (ArchiveRolePhaseEdge n) ℝ :=
  archiveRoleCoboundary n * (archiveRoleCoboundary n).transpose

/-- The exact finite Hodge--Dirac `d + d^*` on `C^0 ⊕ C^1`. -/
def archiveRoleHodgeDirac (n : Nat) :
    Matrix (ArchiveRoleHodgeCarrier n) (ArchiveRoleHodgeCarrier n) ℝ :=
  fun i j =>
    match i, j with
    | Sum.inl _, Sum.inl _ => 0
    | Sum.inl x, Sum.inr e => archiveRoleCoboundary n e x
    | Sum.inr e, Sum.inl x => archiveRoleCoboundary n e x
    | Sum.inr _, Sum.inr _ => 0

/-- The finite Hodge--Dirac is self-adjoint. -/
theorem archiveRoleHodgeDirac_symmetric (n : Nat) :
    (archiveRoleHodgeDirac n).transpose = archiveRoleHodgeDirac n := by
  ext i j
  cases i <;> cases j <;> rfl

/-- The scalar block of `D_H^2` is exactly the metric role-product Laplacian. -/
theorem archiveRoleHodgeDirac_sq_vertex_block
    (n : Nat) (x y : ArchiveRolePhasePoint n) :
    (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
        (Sum.inl x) (Sum.inl y) =
      archiveRoleProductLaplacian n x y := by
  classical
  simp [archiveRoleHodgeDirac, archiveRoleProductLaplacian,
    Matrix.mul_apply, Fintype.sum_sum_type]

/-- The one-form block of `D_H^2` is `B B^T`. -/
theorem archiveRoleHodgeDirac_sq_edge_block
    (n : Nat) (e f : ArchiveRolePhaseEdge n) :
    (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
        (Sum.inr e) (Sum.inr f) =
      archiveRoleOneFormLaplacian n e f := by
  classical
  simp [archiveRoleHodgeDirac, archiveRoleOneFormLaplacian,
    Matrix.mul_apply, Fintype.sum_sum_type]

/-- The upper-right block of `D_H^2` vanishes. -/
theorem archiveRoleHodgeDirac_sq_vertex_edge_zero
    (n : Nat) (x : ArchiveRolePhasePoint n) (e : ArchiveRolePhaseEdge n) :
    (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
        (Sum.inl x) (Sum.inr e) = 0 := by
  classical
  simp [archiveRoleHodgeDirac, Matrix.mul_apply, Fintype.sum_sum_type]

/-- The lower-left block of `D_H^2` vanishes. -/
theorem archiveRoleHodgeDirac_sq_edge_vertex_zero
    (n : Nat) (e : ArchiveRolePhaseEdge n) (x : ArchiveRolePhasePoint n) :
    (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
        (Sum.inr e) (Sum.inl x) = 0 := by
  classical
  simp [archiveRoleHodgeDirac, Matrix.mul_apply, Fintype.sum_sum_type]

/-- Packaging owner for the exact finite Hodge--Dirac square. -/
theorem archive_hodge_dirac_square_owner (n : Nat) :
    (archiveRoleHodgeDirac n).transpose = archiveRoleHodgeDirac n ∧
      (∀ x y : ArchiveRolePhasePoint n,
        (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
            (Sum.inl x) (Sum.inl y) =
          archiveRoleProductLaplacian n x y) ∧
      (∀ e f : ArchiveRolePhaseEdge n,
        (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
            (Sum.inr e) (Sum.inr f) =
          archiveRoleOneFormLaplacian n e f) ∧
      (∀ x e,
        (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
            (Sum.inl x) (Sum.inr e) = 0) ∧
      (∀ e x,
        (archiveRoleHodgeDirac n * archiveRoleHodgeDirac n)
            (Sum.inr e) (Sum.inl x) = 0) := by
  exact ⟨archiveRoleHodgeDirac_symmetric n,
    archiveRoleHodgeDirac_sq_vertex_block n,
    archiveRoleHodgeDirac_sq_edge_block n,
    archiveRoleHodgeDirac_sq_vertex_edge_zero n,
    archiveRoleHodgeDirac_sq_edge_vertex_zero n⟩

end D0
