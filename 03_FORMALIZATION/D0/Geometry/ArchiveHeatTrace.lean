import D0.Geometry.ArchiveRefinementTower
import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Algebra.BigOperators.Fin

open scoped BigOperators

namespace D0

def archiveEigenvalue (n : Nat) (x : ArchivePoints n) : Real :=
  x.val

noncomputable def archiveHeatTrace (n : Nat) (u : Real) : Real :=
  ∑ x : ArchivePoints n, Real.exp (-u * archiveEigenvalue n x)

def archivePointLift (n : Nat) (x : ArchivePoints n) : ArchivePoints (n + 1) :=
  ⟨x.val, by
    have hmono : (archiveTower n).modes ≤ (archiveTower (n + 1)).modes :=
      Nat.le_of_lt (spectral_modes_strictly_increase n)
    exact lt_of_lt_of_le x.isLt hmono⟩

theorem archive_eigenvalue_nonnegative (n : Nat) (x : ArchivePoints n) :
    0 ≤ archiveEigenvalue n x := by
  unfold archiveEigenvalue
  exact_mod_cast Nat.zero_le x.val

theorem heat_trace_positive (n : Nat) {u : Real} (_hu : 0 < u) :
    0 ≤ archiveHeatTrace n u := by
  classical
  unfold archiveHeatTrace
  exact Finset.sum_nonneg (fun x _hx => le_of_lt (Real.exp_pos _))

theorem archive_projection_lift (n : Nat) (x : ArchivePoints n) :
    archiveProjection n (archivePointLift n x) = x := by
  apply Fin.ext
  simp [archiveProjection, archivePointLift, Nat.mod_eq_of_lt x.isLt]

theorem archive_eigenvalue_lift_compatible (n : Nat) (x : ArchivePoints n) :
    archiveEigenvalue (n + 1) (archivePointLift n x) =
      archiveEigenvalue n x := by
  rfl

noncomputable def archiveProjectedHeatTrace (n : Nat) (u : Real) : Real :=
  ∑ x : ArchivePoints n, Real.exp (-u * archiveEigenvalue (n + 1) (archivePointLift n x))

theorem heat_trace_projection_compatible (n : Nat) (u : Real) :
    archiveProjectedHeatTrace n u = archiveHeatTrace n u := by
  classical
  simp [archiveProjectedHeatTrace, archiveHeatTrace, archive_eigenvalue_lift_compatible]

end D0
