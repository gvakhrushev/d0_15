import Mathlib.Tactic
import D0.Geometry.ArchiveHodgeCARDirac

/-!
# Role permutation action on the archive site group

`permuteRoleSite σ` is the coordinate pullback

`(σ · x)(r) = x(σ⁻¹ r)`.

It is an action of `Perm Role`, and it sends the unit step `e_r` to `e_{σ r}`.
-/

namespace D0.Geometry

open D0

variable {N : ℕ}

def permuteRoleSite (σ : Equiv.Perm Role) (x : ArchiveRolePhaseGroup N) :
    ArchiveRolePhaseGroup N :=
  fun r => x (σ.symm r)

theorem permuteRoleSite_one (x : ArchiveRolePhaseGroup N) :
    permuteRoleSite (1 : Equiv.Perm Role) x = x := by
  funext r
  rfl

theorem permuteRoleSite_mul (σ τ : Equiv.Perm Role) (x : ArchiveRolePhaseGroup N) :
    permuteRoleSite (σ * τ) x = permuteRoleSite σ (permuteRoleSite τ x) := by
  funext r
  simp [permuteRoleSite, Equiv.Perm.mul_def, Equiv.Perm.mul_apply]

theorem permuteRoleSite_inv (σ : Equiv.Perm Role) (x : ArchiveRolePhaseGroup N) :
    permuteRoleSite σ.symm (permuteRoleSite σ x) = x := by
  funext r
  simp [permuteRoleSite]

theorem permuteRoleSite_right_inv (σ : Equiv.Perm Role) (x : ArchiveRolePhaseGroup N) :
    permuteRoleSite σ (permuteRoleSite σ.symm x) = x := by
  simpa [Equiv.Perm.mul_def] using permuteRoleSite_inv σ.symm x

theorem permuteRoleSite_roleStep (σ : Equiv.Perm Role) (r : Role) :
    permuteRoleSite σ (roleStep N r) = roleStep N (σ r) := by
  funext s
  simp only [permuteRoleSite, roleStep]
  by_cases h : σ.symm s = r
  · have hs : s = σ r := by
      simpa using congrArg σ h
    simp [h, hs]
  · have hs : s ≠ σ r := by
      intro hs
      apply h
      rw [hs]
      simp
    simp [h, hs]

theorem permuteRoleSite_add (σ : Equiv.Perm Role)
    (x v : ArchiveRolePhaseGroup N) :
    permuteRoleSite σ (x + v) = permuteRoleSite σ x + permuteRoleSite σ v := by
  funext s
  simp [permuteRoleSite]

theorem permuteRoleSite_translatePlus (σ : Equiv.Perm Role) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    permuteRoleSite σ (roleTranslatePlus N r x) =
      roleTranslatePlus N (σ r) (permuteRoleSite σ x) := by
  simp only [roleTranslatePlus_apply, permuteRoleSite_add, permuteRoleSite_roleStep]

theorem permuteRoleSite_neg (σ : Equiv.Perm Role) (v : ArchiveRolePhaseGroup N) :
    permuteRoleSite σ (-v) = -permuteRoleSite σ v := by
  funext s
  simp [permuteRoleSite]

theorem permuteRoleSite_translateMinus (σ : Equiv.Perm Role) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    permuteRoleSite σ (roleTranslateMinus N r x) =
      roleTranslateMinus N (σ r) (permuteRoleSite σ x) := by
  simp only [roleTranslateMinus_apply, permuteRoleSite_add, permuteRoleSite_roleStep,
    permuteRoleSite_neg, sub_eq_add_neg]

def pullRoleScalar (σ : Equiv.Perm Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    ArchiveRolePhaseGroup N → ℝ :=
  fun x => f (permuteRoleSite σ.symm x)

theorem pullRoleScalar_forwardDifference (σ : Equiv.Perm Role) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    forwardDifference N (σ r) (pullRoleScalar σ f) =
      pullRoleScalar σ (forwardDifference N r f) := by
  funext x
  simp only [forwardDifference_apply, pullRoleScalar]
  have hplus := permuteRoleSite_translatePlus σ.symm (σ r) x
  simp only [Equiv.symm_apply_apply] at hplus
  rw [hplus]

theorem pullRoleScalar_backwardDifference (σ : Equiv.Perm Role) (r : Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    backwardDifference N (σ r) (pullRoleScalar σ f) =
      pullRoleScalar σ (backwardDifference N r f) := by
  funext x
  simp only [backwardDifference_apply, pullRoleScalar]
  have hminus := permuteRoleSite_translateMinus σ.symm (σ r) x
  simp only [Equiv.symm_apply_apply] at hminus
  rw [hminus]

theorem pullRoleScalar_laplacian (σ : Equiv.Perm Role)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    scalarDifferenceLaplacian N (pullRoleScalar σ f) =
      pullRoleScalar σ (scalarDifferenceLaplacian N f) := by
  funext x
  simp only [scalarDifferenceLaplacian, pullRoleScalar]
  have hreindex :
      (∑ r : Role, -backwardDifference N r
          (forwardDifference N r (pullRoleScalar σ f)) x) =
        ∑ r : Role, -backwardDifference N (σ r)
          (forwardDifference N (σ r) (pullRoleScalar σ f)) x := by
    simpa using (Equiv.sum_comp σ
      (fun r => -backwardDifference N r
        (forwardDifference N r (pullRoleScalar σ f)) x)).symm
  rw [hreindex]
  refine Finset.sum_congr rfl ?_
  intro r _
  rw [pullRoleScalar_forwardDifference, pullRoleScalar_backwardDifference]
  rfl

end D0.Geometry
