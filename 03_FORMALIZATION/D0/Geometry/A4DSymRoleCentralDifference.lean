import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Data.Matrix.Basic
import Mathlib.Data.ZMod.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveRolePhaseGroup

namespace D0.Geometry

open D0

/-!
Finite local infrastructure for a symmetric role tensor and centered differences on the
group shadow of the archive role-phase carrier.

This file is deliberately only finite algebra.  In particular, the operators below are not
identified with continuum derivatives, and no curvature, Einstein, Bianchi, covariance, or
seam-metric statement is made here.
-/

/-- A real symmetric tensor on the existing four-role carrier. -/
structure SymRoleTensor where
  toMatrix : Matrix Role Role ℝ
  symmetric : ∀ a b, toMatrix a b = toMatrix b a

@[ext] theorem SymRoleTensor.ext {A B : SymRoleTensor}
    (h : A.toMatrix = B.toMatrix) : A = B := by
  cases A
  cases B
  simp only at h
  subst h
  rfl

theorem SymRoleTensor.entry_symmetric (A : SymRoleTensor) (a b : Role) :
    A.toMatrix a b = A.toMatrix b a :=
  A.symmetric a b

/-- A sitewise symmetric role-tensor field on the finite group carrier. -/
abbrev LocalSymRoleField (N : ℕ) := ArchiveRolePhaseGroup N → SymRoleTensor

/-- A sitewise role-vector field on the same finite group carrier. -/
abbrev LocalRoleVector (N : ℕ) := ArchiveRolePhaseGroup N → Role → ℝ

/-- The canonical unit step in one role coordinate. -/
def roleStep (N : ℕ) (r : Role) : ArchiveRolePhaseGroup N :=
  fun s => if s = r then 1 else 0

/-- Translation by an arbitrary group vector. -/
def roleTranslate (v x : ArchiveRolePhaseGroup N) : ArchiveRolePhaseGroup N := x + v

/-- Forward and backward translations in one canonical role direction. -/
def roleTranslatePlus (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :=
  roleTranslate (roleStep N r) x

def roleTranslateMinus (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :=
  roleTranslate (-roleStep N r) x

theorem roleTranslatePlus_apply (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslatePlus N r x = x + roleStep N r := rfl

theorem roleTranslateMinus_apply (N : ℕ) (r : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslateMinus N r x = x - roleStep N r := by
  simp [roleTranslateMinus, roleTranslate, sub_eq_add_neg]

/-- Translation is a permutation of the finite group carrier. -/
def roleTranslateEquiv (N : ℕ) (v : ArchiveRolePhaseGroup N) :
    ArchiveRolePhaseGroup N ≃ ArchiveRolePhaseGroup N where
  toFun x := x + v
  invFun x := x - v
  left_inv x := by
    simp only [sub_eq_add_neg]
    abel
  right_inv x := by
    simp only [sub_eq_add_neg]
    abel

theorem sum_translate (N : ℕ) (v : ArchiveRolePhaseGroup N)
    (F : ArchiveRolePhaseGroup N → ℝ) :
    (∑ x, F (x + v)) = ∑ x, F x := by
  simpa [roleTranslateEquiv] using
    (Equiv.sum_comp (roleTranslateEquiv N v) F)

/-- The centered difference scale is exactly `(N + 2) / 2`. -/
noncomputable def centeredDifferenceScale (N : ℕ) : ℝ :=
  (archiveFibers N : ℝ) / 2

theorem centeredDifferenceScale_eq (N : ℕ) :
    centeredDifferenceScale N = ((N + 2 : ℕ) : ℝ) / 2 := rfl

/-- Scaled centered difference in one canonical role direction. -/
noncomputable def centeredDifference (N : ℕ) (r : Role) :
    (ArchiveRolePhaseGroup N → ℝ) →ₗ[ℝ] (ArchiveRolePhaseGroup N → ℝ) where
  toFun f x := centeredDifferenceScale N *
    (f (roleTranslatePlus N r x) - f (roleTranslateMinus N r x))
  map_add' f g := by
    funext x
    simp only [Pi.add_apply]
    ring
  map_smul' c f := by
    funext x
    simp only [Pi.smul_apply, RingHom.id_apply]
    ring

@[simp] theorem centeredDifference_apply (N : ℕ) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) (x : ArchiveRolePhaseGroup N) :
    centeredDifference N r f x = centeredDifferenceScale N *
      (f (roleTranslatePlus N r x) - f (roleTranslateMinus N r x)) := rfl

theorem centeredDifference_add (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (f + g) = centeredDifference N r f + centeredDifference N r g :=
  (centeredDifference N r).map_add f g

theorem centeredDifference_smul (N : ℕ) (r : Role) (c : ℝ)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (c • f) = c • centeredDifference N r f :=
  (centeredDifference N r).map_smul c f

theorem centeredDifference_translate_plus (N : ℕ) (r s : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (fun x => f (roleTranslatePlus N s x)) =
      fun x => centeredDifference N r f (roleTranslatePlus N s x) := by
  funext x
  have h₁ :
      roleTranslatePlus N s (roleTranslatePlus N r x) =
        roleTranslatePlus N r (roleTranslatePlus N s x) := by
    dsimp [roleTranslatePlus, roleTranslate]
    abel
  have h₂ :
      roleTranslatePlus N s (roleTranslateMinus N r x) =
        roleTranslateMinus N r (roleTranslatePlus N s x) := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  simp only [centeredDifference_apply]
  rw [h₁, h₂]

theorem centeredDifference_comm (N : ℕ) (r s : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    centeredDifference N r (centeredDifference N s f) =
      centeredDifference N s (centeredDifference N r f) := by
  funext x
  have h₁ :
      roleTranslatePlus N s (roleTranslatePlus N r x) =
        roleTranslatePlus N r (roleTranslatePlus N s x) := by
    dsimp [roleTranslatePlus, roleTranslate]
    abel
  have h₂ :
      roleTranslateMinus N s (roleTranslatePlus N r x) =
        roleTranslatePlus N r (roleTranslateMinus N s x) := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  have h₃ :
      roleTranslateMinus N s (roleTranslateMinus N r x) =
        roleTranslateMinus N r (roleTranslateMinus N s x) := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  have h₄ :
      roleTranslatePlus N s (roleTranslateMinus N r x) =
        roleTranslateMinus N r (roleTranslatePlus N s x) := by
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate]
    abel
  simp only [centeredDifference_apply]
  rw [h₁, h₂, h₃, h₄]
  ring

theorem centeredDifference_const (N : ℕ) (r : Role) (c : ℝ) :
    centeredDifference N r (fun _ : ArchiveRolePhaseGroup N => c) = 0 := by
  funext x
  simp [centeredDifference_apply]

/-- At the minimal fiber `L = N + 2 = 2`, forward and backward steps coincide. -/
theorem roleTranslatePlus_eq_minus_at_zero (r : Role)
    (x : ArchiveRolePhaseGroup 0) :
    roleTranslatePlus 0 r x = roleTranslateMinus 0 r x := by
  funext s
  by_cases h : s = r
  · subst h
    dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate, roleStep]
    have hone : (1 : ZMod 2) = -1 := by
      apply eq_neg_of_add_eq_zero_left
      simpa [one_add_one_eq_two] using ZMod.natCast_self 2
    simp only [ite_true]
    have honeN : (1 : ZMod (archiveFibers 0)) = -(1 : ZMod (archiveFibers 0)) := by
      simpa only [archiveFibers] using hone
    exact congrArg (fun z : ZMod (archiveFibers 0) => x s + z) honeN
  · dsimp [roleTranslatePlus, roleTranslateMinus, roleTranslate, roleStep]
    simp [h]

/-- Consequently the scaled centered difference is identically zero at `L = 2`.
This records the finite degeneracy explicitly; no nontriviality is asserted at that level. -/
theorem centeredDifference_zero (r : Role) :
    centeredDifference 0 r = 0 := by
  apply LinearMap.ext
  intro f
  funext x
  rw [centeredDifference_apply, roleTranslatePlus_eq_minus_at_zero]
  simp

theorem centeredDifference_skew_adjoint (N : ℕ) (r : Role)
    (f g : ArchiveRolePhaseGroup N → ℝ) :
    (∑ x, centeredDifference N r f x * g x) =
      -∑ x, f x * centeredDifference N r g x := by
  classical
  let e : ArchiveRolePhaseGroup N := roleStep N r
  have hplus :
      (∑ x, f (x + e) * g x) = ∑ x, f x * g (x - e) := by
    simpa [e, roleTranslateEquiv] using
      (sum_translate N e (fun y => f y * g (y - e)))
  have hminus :
      (∑ x, f (x - e) * g x) = ∑ x, f x * g (x + e) := by
    have h := sum_translate N (-e) (fun y => f y * g (y + e))
    simpa [roleTranslateEquiv, sub_eq_add_neg] using h
  calc
    (∑ x, centeredDifference N r f x * g x) =
        ∑ x, (centeredDifferenceScale N * (f (x + e) * g x) -
          centeredDifferenceScale N * (f (x - e) * g x)) := by
      apply Finset.sum_congr rfl
      intro x hx
      simp only [centeredDifference_apply, e, roleTranslatePlus_apply,
        roleTranslateMinus_apply]
      ring
    _ = centeredDifferenceScale N * (∑ x, f (x + e) * g x) -
        centeredDifferenceScale N * (∑ x, f (x - e) * g x) := by
      rw [Finset.sum_sub_distrib]
      rw [← Finset.mul_sum, ← Finset.mul_sum]
    _ = centeredDifferenceScale N * (∑ x, f x * g (x - e)) -
        centeredDifferenceScale N * (∑ x, f x * g (x + e)) := by
      rw [hplus, hminus]
    _ = -∑ x, f x * centeredDifference N r g x := by
      simp only [centeredDifference_apply, e, roleTranslatePlus_apply,
        roleTranslateMinus_apply]
      simp only [mul_sub]
      rw [Finset.sum_sub_distrib]
      have hplus' :
          (∑ x, f x * (centeredDifferenceScale N * g (x + roleStep N r))) =
            centeredDifferenceScale N * (∑ x, f x * g (x + roleStep N r)) := by
        calc
          (∑ x, f x * (centeredDifferenceScale N * g (x + roleStep N r))) =
              ∑ x, centeredDifferenceScale N * (f x * g (x + roleStep N r)) := by
            apply Finset.sum_congr rfl
            intro x hx
            ring
          _ = centeredDifferenceScale N * (∑ x, f x * g (x + roleStep N r)) := by
            rw [Finset.mul_sum]
      have hminus' :
          (∑ x, f x * (centeredDifferenceScale N * g (x - roleStep N r))) =
            centeredDifferenceScale N * (∑ x, f x * g (x - roleStep N r)) := by
        calc
          (∑ x, f x * (centeredDifferenceScale N * g (x - roleStep N r))) =
              ∑ x, centeredDifferenceScale N * (f x * g (x - roleStep N r)) := by
            apply Finset.sum_congr rfl
            intro x hx
            ring
          _ = centeredDifferenceScale N * (∑ x, f x * g (x - roleStep N r)) := by
            rw [Finset.mul_sum]
      rw [hplus', hminus']
      ring

/-- The finite symmetric gradient of a local role vector. -/
noncomputable def symmetricRoleGradient (N : ℕ) (xi : LocalRoleVector N) : LocalSymRoleField N :=
  fun x =>
    { toMatrix := fun a b =>
        centeredDifference N a (fun y => xi y b) x +
          centeredDifference N b (fun y => xi y a) x
      symmetric := by
        intro a b
        ring }

theorem symmetricRoleGradient_entry (N : ℕ) (xi : LocalRoleVector N)
    (x : ArchiveRolePhaseGroup N) (a b : Role) :
    (symmetricRoleGradient N xi x).toMatrix a b =
      centeredDifference N a (fun y => xi y b) x +
        centeredDifference N b (fun y => xi y a) x := rfl

end D0.Geometry
