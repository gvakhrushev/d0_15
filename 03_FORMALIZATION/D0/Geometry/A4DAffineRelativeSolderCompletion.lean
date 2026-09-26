import Mathlib.Tactic
import Mathlib.LinearAlgebra.Matrix.NonsingularInverse
import D0.Geometry.A4DObserverPositiveExterior
import D0.Geometry.A4DRawSolderFrameAction
import D0.Geometry.ArchiveAffineCartanConnection

/-!
# Affine relative-solder completion (merged #184). Research-only: L=2 192-rank.
-/

namespace D0.Geometry

open D0
open scoped BigOperators Matrix

noncomputable section

def observerRow (n v : RoleVector) : Role → ℝ :=
  fun s => ∑ r : Role, v r * observerMetric n r s

@[simp] theorem observerRow_apply (n v : RoleVector) (s : Role) :
    observerRow n v s = ∑ r : Role, v r * observerMetric n r s := rfl

theorem observerRow_eq_vecMul (n v : RoleVector) :
    observerRow n v = v ᵥ* observerMetric n := by
  ext s
  simp [observerRow, Matrix.vecMul, dotProduct]

theorem observerMetric_left_transport_congruence
    (g : Matrix Role Role ℝ) (hg : IsRoleLorentz g) (n : RoleVector) :
    observerMetric (g *ᵥ n) =
      (g⁻¹).transpose * observerMetric n * g⁻¹ := by
  have hunit : IsUnit g.det := isRoleLorentz_det_isUnit g hg
  have hown := observerMetric_vector_congruence g hg (g *ᵥ n)
  have hcancel : g⁻¹ *ᵥ (g *ᵥ n) = n := by
    ext i
    simp [Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul g hunit, Matrix.one_mulVec]
  rw [hcancel] at hown
  exact hown.symm

theorem observerRow_lorentz_contragredient
    (g : Matrix Role Role ℝ) (hg : IsRoleLorentz g) (n v : RoleVector) :
    observerRow (g *ᵥ n) (g *ᵥ v) = observerRow n v ᵥ* g⁻¹ := by
  have hmet := observerMetric_left_transport_congruence g hg n
  have hunit : IsUnit g.det := isRoleLorentz_det_isUnit g hg
  have hcancel : g⁻¹ *ᵥ (g *ᵥ v) = v := by
    ext i
    simp [Matrix.mulVec_mulVec, Matrix.nonsing_inv_mul g hunit, Matrix.one_mulVec]
  have hform (A B : Matrix Role Role ℝ) (w : Role → ℝ) :
      w ᵥ* (A.transpose * B) = (A *ᵥ w) ᵥ* B := by
    ext s
    simp only [Matrix.vecMul, Matrix.mulVec, dotProduct, Matrix.mul_apply,
      Matrix.transpose_apply]
    calc
      ∑ i, w i * ∑ j, A.transpose i j * B j s =
          ∑ i, ∑ j, w i * (A j i * B j s) := by
            simp only [Matrix.transpose_apply, Finset.mul_sum, mul_assoc]
      _ = ∑ j, ∑ i, (A j i * w i) * B j s := by
            rw [Finset.sum_comm]
            refine Finset.sum_congr rfl ?_
            intro j _
            refine Finset.sum_congr rfl ?_
            intro i _
            ring
      _ = ∑ j, (∑ i, A j i * w i) * B j s := by
            refine Finset.sum_congr rfl ?_
            intro j _
            simp [Finset.sum_mul, mul_assoc]
  ext s
  have hassoc :
      (g⁻¹).transpose * observerMetric n * g⁻¹ =
        (g⁻¹).transpose * (observerMetric n * g⁻¹) := by
    simp [Matrix.mul_assoc]
  have hL : observerRow (g *ᵥ n) (g *ᵥ v) =
      (g *ᵥ v) ᵥ* ((g⁻¹).transpose * (observerMetric n * g⁻¹)) := by
    rw [observerRow_eq_vecMul, hmet, hassoc]
  have hM : (g *ᵥ v) ᵥ* ((g⁻¹).transpose * (observerMetric n * g⁻¹)) =
      (g⁻¹ *ᵥ (g *ᵥ v)) ᵥ* (observerMetric n * g⁻¹) := hform g⁻¹ _ _
  have hR : (g⁻¹ *ᵥ (g *ᵥ v)) ᵥ* (observerMetric n * g⁻¹) =
      v ᵥ* (observerMetric n * g⁻¹) := by rw [hcancel]
  have hS : v ᵥ* (observerMetric n * g⁻¹) = (v ᵥ* observerMetric n) ᵥ* g⁻¹ := by
    ext t
    simp only [Matrix.vecMul, Matrix.mul_apply, dotProduct, Finset.mul_sum,
      Finset.sum_mul, mul_assoc]
    rw [Finset.sum_comm]
  have : observerRow (g *ᵥ n) (g *ᵥ v) = observerRow n v ᵥ* g⁻¹ := by
    calc
      observerRow (g *ᵥ n) (g *ᵥ v) =
          (g *ᵥ v) ᵥ* ((g⁻¹).transpose * (observerMetric n * g⁻¹)) := hL
      _ = (g⁻¹ *ᵥ (g *ᵥ v)) ᵥ* (observerMetric n * g⁻¹) := hM
      _ = v ᵥ* (observerMetric n * g⁻¹) := hR
      _ = (v ᵥ* observerMetric n) ᵥ* g⁻¹ := hS
      _ = observerRow n v ᵥ* g⁻¹ := by rw [← observerRow_eq_vecMul]
  exact congrArg (fun w : Role → ℝ => w s) this

def affineLinkShift (g : Matrix Role Role ℝ) (b τ : RoleVector) : RoleVector :=
  g *ᵥ b + τ

def affineSolderRowShift (g : Matrix Role Role ℝ) (n' : RoleVector)
    (Θ τ : Role → ℝ) : Role → ℝ :=
  Θ ᵥ* g⁻¹ + observerRow n' τ

theorem affineLinkShift_observerRow
    (g : Matrix Role Role ℝ) (hg : IsRoleLorentz g)
    (n b τ : RoleVector) :
    observerRow (g *ᵥ n) (affineLinkShift g b τ) =
      observerRow n b ᵥ* g⁻¹ + observerRow (g *ᵥ n) τ := by
  unfold affineLinkShift
  have hadd : observerRow (g *ᵥ n) (g *ᵥ b + τ) =
      observerRow (g *ᵥ n) (g *ᵥ b) + observerRow (g *ᵥ n) τ := by
    ext s
    simp [observerRow, Pi.add_apply, add_mul, Finset.sum_add_distrib]
  rw [hadd, observerRow_lorentz_contragredient g hg n b]

def relativeSolderRow (lam : ℝ) (n : RoleVector) (Θ b : Role → ℝ) : Role → ℝ :=
  fun s => Θ s - lam * observerRow n b s

@[simp] theorem relativeSolderRow_apply (lam : ℝ) (n : RoleVector)
    (Θ b : Role → ℝ) (s : Role) :
    relativeSolderRow lam n Θ b s = Θ s - lam * observerRow n b s := rfl

theorem relativeSolderRow_affine_transform
    (g : Matrix Role Role ℝ) (hg : IsRoleLorentz g)
    (lam : ℝ) (n : RoleVector) (Θ b τ : Role → ℝ) :
    relativeSolderRow lam (g *ᵥ n)
        (affineSolderRowShift g (g *ᵥ n) Θ τ)
        (affineLinkShift g b τ) =
      relativeSolderRow lam n Θ b ᵥ* g⁻¹ +
        (1 - lam) • observerRow (g *ᵥ n) τ := by
  have hrow := affineLinkShift_observerRow g hg n b τ
  ext s
  have hrow_s : observerRow (g *ᵥ n) (affineLinkShift g b τ) s =
      (observerRow n b ᵥ* g⁻¹) s + observerRow (g *ᵥ n) τ s :=
    congrArg (fun w : Role → ℝ => w s) hrow
  have hfactor :
      ∑ x, (lam * observerRow n b x) * g⁻¹ x s =
        lam * ∑ x, observerRow n b x * g⁻¹ x s := by
    calc
      ∑ x, (lam * observerRow n b x) * g⁻¹ x s =
          ∑ x, lam * (observerRow n b x * g⁻¹ x s) := by
            refine Finset.sum_congr rfl ?_
            intro x _; ring
      _ = lam * ∑ x, observerRow n b x * g⁻¹ x s :=
            (Finset.mul_sum _ (fun x => observerRow n b x * g⁻¹ x s) lam).symm
  have hlin :
      ((fun t => Θ t - lam * observerRow n b t) ᵥ* g⁻¹) s =
        (Θ ᵥ* g⁻¹) s - lam * (observerRow n b ᵥ* g⁻¹) s := by
    simp only [Matrix.vecMul, dotProduct, sub_mul, Finset.sum_sub_distrib]
    change (∑ x, Θ x * g⁻¹ x s) - ∑ x, (lam * observerRow n b x) * g⁻¹ x s =
      (∑ x, Θ x * g⁻¹ x s) - lam * ∑ x, observerRow n b x * g⁻¹ x s
    rw [hfactor]
  have hLHS :
      relativeSolderRow lam (g *ᵥ n)
          (affineSolderRowShift g (g *ᵥ n) Θ τ)
          (affineLinkShift g b τ) s =
        (Θ ᵥ* g⁻¹) s + observerRow (g *ᵥ n) τ s -
          lam * observerRow (g *ᵥ n) (affineLinkShift g b τ) s := by
    simp [relativeSolderRow, affineSolderRowShift, Pi.add_apply]
  have hstep :
      (Θ ᵥ* g⁻¹) s + observerRow (g *ᵥ n) τ s -
          lam * observerRow (g *ᵥ n) (affineLinkShift g b τ) s =
        (Θ ᵥ* g⁻¹) s - lam * (observerRow n b ᵥ* g⁻¹) s +
          (1 - lam) * observerRow (g *ᵥ n) τ s := by
    rw [hrow_s]; ring
  have hfold :
      (Θ ᵥ* g⁻¹) s - lam * (observerRow n b ᵥ* g⁻¹) s +
          (1 - lam) * observerRow (g *ᵥ n) τ s =
        (relativeSolderRow lam n Θ b ᵥ* g⁻¹) s +
          ((1 - lam) • observerRow (g *ᵥ n) τ) s := by
    have hrel :
        (relativeSolderRow lam n Θ b ᵥ* g⁻¹) s =
          (Θ ᵥ* g⁻¹) s - lam * (observerRow n b ᵥ* g⁻¹) s := by
      simpa [relativeSolderRow] using hlin
    simp only [Pi.smul_apply, smul_eq_mul, Pi.add_apply, hrel]
  calc
    relativeSolderRow lam (g *ᵥ n)
        (affineSolderRowShift g (g *ᵥ n) Θ τ)
        (affineLinkShift g b τ) s =
        (Θ ᵥ* g⁻¹) s + observerRow (g *ᵥ n) τ s -
          lam * observerRow (g *ᵥ n) (affineLinkShift g b τ) s := hLHS
    _ = (Θ ᵥ* g⁻¹) s - lam * (observerRow n b ᵥ* g⁻¹) s +
          (1 - lam) * observerRow (g *ᵥ n) τ s := hstep
    _ = (relativeSolderRow lam n Θ b ᵥ* g⁻¹ +
          (1 - lam) • observerRow (g *ᵥ n) τ) s := by
            simpa [Pi.add_apply] using hfold

theorem relativeSolderRow_homogeneous_at_one
    (g : Matrix Role Role ℝ) (hg : IsRoleLorentz g)
    (n : RoleVector) (Θ b τ : Role → ℝ) :
    relativeSolderRow 1 (g *ᵥ n)
        (affineSolderRowShift g (g *ᵥ n) Θ τ)
        (affineLinkShift g b τ) =
      relativeSolderRow 1 n Θ b ᵥ* g⁻¹ := by
  have h := relativeSolderRow_affine_transform g hg 1 n Θ b τ
  simp only [sub_self, zero_smul, add_zero] at h
  exact h

theorem relativeSolder_lambda_eq_one_of_witness
    (g : Matrix Role Role ℝ) (hg : IsRoleLorentz g)
    (lam : ℝ) (n : RoleVector) (Θ b τ : Role → ℝ)
    (hτ : observerRow (g *ᵥ n) τ ≠ 0)
    (hcov :
      relativeSolderRow lam (g *ᵥ n)
          (affineSolderRowShift g (g *ᵥ n) Θ τ)
          (affineLinkShift g b τ) =
        relativeSolderRow lam n Θ b ᵥ* g⁻¹) :
    lam = 1 := by
  have h := relativeSolderRow_affine_transform g hg lam n Θ b τ
  have hres : (1 - lam) • observerRow (g *ᵥ n) τ = (0 : Role → ℝ) := by
    have h' :
        relativeSolderRow lam n Θ b ᵥ* g⁻¹ +
          (1 - lam) • observerRow (g *ᵥ n) τ =
        relativeSolderRow lam n Θ b ᵥ* g⁻¹ := by
      rw [← h, hcov]
    exact add_left_cancel (a := relativeSolderRow lam n Θ b ᵥ* g⁻¹)
      (by simpa [add_zero] using h')
  have hz : (1 - lam) = 0 ∨ observerRow (g *ᵥ n) τ = 0 :=
    (smul_eq_zero.mp hres)
  cases hz with
  | inl h0 => exact (sub_eq_zero.mp h0).symm
  | inr h0 => exact (hτ h0).elim

theorem relativeSolder_rest_basis_witness (r : Role) :
    observerRow restObserver (archiveRoleBasis r) ≠ 0 := by
  intro h
  have hs := congrArg (fun w : Role → ℝ => w r) h
  have hsum :
      (∑ i : Role, (archiveRoleBasis r : RoleVector) i *
          observerMetric restObserver i r) =
        observerMetric restObserver r r := by
    rw [Finset.sum_eq_single r]
    · simp [archiveRoleBasis, Pi.basisFun_apply]
    · intro i _ hir
      simp [archiveRoleBasis, Pi.basisFun_apply, hir]
    · intro hr
      exact (hr (Finset.mem_univ r)).elim
  have hI : observerMetric restObserver r r = 1 := by
    simp [observerMetric_restObserver]
  simp only [observerRow] at hs
  rw [hsum, hI] at hs
  exact one_ne_zero hs

def matchedEdgeShift (n u : RoleVector) (Θ b : Role → ℝ) :
    (Role → ℝ) × (Role → ℝ) :=
  (Θ + observerRow n u, b + u)

theorem relativeSolderRow_matchedEdge_residual
    (lam : ℝ) (n u : RoleVector) (Θ b : Role → ℝ) :
    relativeSolderRow lam n (Θ + observerRow n u) (b + u) =
      relativeSolderRow lam n Θ b + (1 - lam) • observerRow n u := by
  ext s
  have hrow : observerRow n (b + u) s =
      observerRow n b s + observerRow n u s := by
    simp [observerRow, Pi.add_apply, add_mul, Finset.sum_add_distrib]
  simp only [relativeSolderRow, Pi.add_apply, Pi.smul_apply, smul_eq_mul, hrow,
    mul_add]
  ring

theorem relativeSolderRow_one_matchedEdge_invariant
    (n u : RoleVector) (Θ b : Role → ℝ) :
    relativeSolderRow 1 n (Θ + observerRow n u) (b + u) =
      relativeSolderRow 1 n Θ b := by
  have h := relativeSolderRow_matchedEdge_residual 1 n u Θ b
  simpa using h

theorem matchedEdge_invisible_of_relative_factor
    {α : Type*} (F : (Role → ℝ) → α)
    (n u : RoleVector) (Θ b : Role → ℝ) :
    F (relativeSolderRow 1 n (Θ + observerRow n u) (b + u)) =
      F (relativeSolderRow 1 n Θ b) := by
  rw [relativeSolderRow_one_matchedEdge_invariant]

theorem matchedEdge_rest_basis_changes_raw_but_not_relative (r : Role) :
    let u := (archiveRoleBasis r : RoleVector)
    let Θ : Role → ℝ := 0
    let b : Role → ℝ := 0
    (b + u ≠ b) ∧
      relativeSolderRow 1 restObserver (Θ + observerRow restObserver u) (b + u) =
        relativeSolderRow 1 restObserver Θ b := by
  intro u Θ b
  refine ⟨?_, relativeSolderRow_one_matchedEdge_invariant restObserver u Θ b⟩
  intro h
  have hs := congrArg (fun w : Role → ℝ => w r) h
  simp [u, b, archiveRoleBasis, Pi.basisFun_apply, Pi.add_apply] at hs

def relativeSolder_edgeDiagonalRank_researchOnly : True := trivial

def relativeSolder_not_final_physical_action : True := trivial

end
end D0.Geometry
