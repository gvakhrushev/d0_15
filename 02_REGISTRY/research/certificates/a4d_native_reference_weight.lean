import D0.Geometry.A4DLocatedMatterCellEnergy
import D0.Geometry.A4DRawSolderFrameAction
import D0.Geometry.ArchiveExteriorFrameLift

/-! Research operator analysis. The existing referenceCellWeight is used
literally. No new native action, coefficient choice or on-shell physical gate
is introduced. -/
open scoped BigOperators
open D0 D0.Geometry
namespace D0.Research.NativeReferenceWeight
noncomputable section

lemma carEnd_vacuum (s r : Role) (S : ArchiveFockState) :
    carEnd s r S fockVacuumState = 0 := by
  simp [carEnd, carAnnihilate, fockVacuumState]

lemma carEnd_scalar (N : ℕ) (s r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    cochainCarEnd N s r (scalarCochain N f) = 0 := by
  funext p
  simp [cochainCarEnd, scalarCochain, vacuumFockState, mul_ite, carEnd_vacuum]

lemma multiply_scalar (N : ℕ) (m f : ArchiveRolePhaseGroup N → ℝ) :
    cochainMultiply N m (scalarCochain N f) = scalarCochain N (fun x => m x * f x) := by
  funext p
  simp [cochainMultiply, scalarCochain, mul_ite]

lemma backwardShift_scalar (N : ℕ) (r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    cochainBackwardShift N r (scalarCochain N f) =
      scalarCochain N (fun x => f (roleTranslateMinus N r x)) := rfl

lemma forwardAverage_scalar (N : ℕ) (r : Role) (f : ArchiveRolePhaseGroup N → ℝ) :
    cochainForwardAverage N r (scalarCochain N f) =
      scalarCochain N (fun x => (f x + f (roleTranslatePlus N r x)) / 2) := by
  funext p
  by_cases h : p.2 = vacuumFockState <;> simp [cochainForwardAverage, scalarCochain, h]

lemma fluxAdjoint_scalar (N : ℕ) (s r : Role) (m f : ArchiveRolePhaseGroup N → ℝ) :
    cochainFluxAdjoint N m s r (scalarCochain N f) = 0 := by
  unfold cochainFluxAdjoint
  rw [multiply_scalar, backwardShift_scalar, forwardAverage_scalar, carEnd_scalar]

lemma fluxForward_scalar (N : ℕ) (s r : Role) (m f : ArchiveRolePhaseGroup N → ℝ) :
    cochainFluxForward N m s r (scalarCochain N f) = 0 := by
  funext p
  simp [cochainFluxForward, carEnd_scalar, cochainMultiply, cochainForwardShift,
    cochainBackwardAverage, backwardAverage]

/-- Exact scalar block, valid for every site-dependent coframe. -/
theorem scalar_weight (c : ℝ) (N : ℕ) (e : LocalCoframeField N)
    (f : ArchiveRolePhaseGroup N → ℝ) :
    referenceCellWeight c N e (scalarCochain N f) =
      scalarCochain N (fun x =>
        f x + (∑ r : Role, (e x r r * f (roleTranslatePlus N r x) +
          e (roleTranslateMinus N r x) r r * f (roleTranslateMinus N r x)) / 2) +
        c * (∑ r : Role, ∑ a : Role, (e x r a)^2) * f x) := by
  funext p
  simp only [referenceCellWeight, Pi.add_apply, Pi.smul_apply, smul_eq_mul,
    flatStaggeredH, fluxForward_scalar, fluxAdjoint_scalar, Pi.zero_apply,
    add_zero, Finset.sum_const_zero, sub_zero]
  by_cases h : p.2 = fockVacuumState
  · simp [cochainLinkSymmetric, scalarCochain, vacuumFockState,
      referenceQuadratic, cellQuadraticDensity, h]
    ring
  · simp [cochainLinkSymmetric, scalarCochain, vacuumFockState,
      referenceQuadratic, cellQuadraticDensity, h]

def scalarCoefficient (c : ℝ) (e : Matrix Role Role ℝ) : ℝ :=
  1 + (∑ r, e r r) + c * (∑ r, ∑ a, (e r a)^2)

theorem constant_scalar_weight (c : ℝ) (N : ℕ) (e : Matrix Role Role ℝ) :
    referenceCellWeight c N (fun _ => e) (scalarCochain N (fun _ => 1)) =
      scalarCochain N (fun _ => scalarCoefficient c e) := by
  rw [scalar_weight]
  congr 1
  funext x
  simp [scalarCoefficient]

lemma sum_role (f : Role → ℝ) : (∑ r, f r) = f A + f B + f C + f D := by
  simp [Fintype.sum_prod_type, Fin.sum_univ_two, A, B, C, D]
  ring

def halfIdentity : Matrix Role Role ℝ := Matrix.diagonal (fun _ => -(1/2 : ℝ))

theorem half_scalar_coefficient (c : ℝ) : scalarCoefficient c halfIdentity = c - 1 := by
  norm_num [scalarCoefficient, halfIdentity, Matrix.diagonal_apply, sum_role, A, B, C, D]
  ring

theorem scalar_unit_nonzero (N : ℕ) : scalarCochain N (fun _ => (1 : ℝ)) ≠ 0 := by
  intro h
  have hp := congrFun h ((0 : ArchiveRolePhaseGroup N), vacuumFockState)
  simp [scalarCochain] at hp

theorem coefficient_one_has_kernel (N : ℕ) :
    referenceCellWeight 1 N (fun _ => halfIdentity) (scalarCochain N (fun _ => 1)) = 0 := by
  rw [constant_scalar_weight]
  funext p
  simp [half_scalar_coefficient, scalarCochain]

theorem coefficient_two_same_field_nonzero (N : ℕ) :
    referenceCellWeight 2 N (fun _ => halfIdentity) (scalarCochain N (fun _ => 1)) ≠ 0 := by
  rw [constant_scalar_weight]
  simpa only [half_scalar_coefficient, show (2 : ℝ)-1=1 by norm_num] using scalar_unit_nonzero N

/-- The exact scalar block at the critical coframe; no continuum limit assumed. -/
theorem half_scalar_block (c : ℝ) (N : ℕ) (f : ArchiveRolePhaseGroup N → ℝ) :
    referenceCellWeight c N (fun _ => halfIdentity) (scalarCochain N f) =
      scalarCochain N (fun x => (c-1)*f x + (1/4 : ℝ) *
        ∑ r : Role, (2*f x-f (roleTranslatePlus N r x)-f (roleTranslateMinus N r x))) := by
  rw [scalar_weight]
  congr 1
  funext x
  norm_num [halfIdentity, Matrix.diagonal_apply, sum_role, A, B, C, D]
  ring

def boostAB : Matrix Role Role ℝ := fun r a =>
  if r = A then (if a = A then 5/4 else if a = B then 3/4 else 0)
  else if r = B then (if a = A then 3/4 else if a = B then 5/4 else 0)
  else if r = a then 1 else 0

def boostedPerturbation (e : Matrix Role Role ℝ) : Matrix Role Role ℝ :=
  (roleLorentzMetric + e) * boostAB - roleLorentzMetric

def secondPerturbation : Matrix Role Role ℝ := fun r a =>
  if r = B ∧ a = B then -1 else 0

theorem boost_lorentz : IsRoleLorentz boostAB := by
  unfold IsRoleLorentz
  ext ⟨a,b⟩ ⟨c,d⟩
  fin_cases a <;> fin_cases b <;> fin_cases c <;> fin_cases d <;>
    norm_num [boostAB, roleLorentzMetric, Matrix.mul_apply, Matrix.transpose_apply,
      Matrix.diagonal_apply, sum_role, A, B, C, D, roleLorentzSign, roleRoleSigEquiv, roleSign]

theorem scalar_flat_boost (c : ℝ) :
    scalarCoefficient c (boostedPerturbation 0) - scalarCoefficient c 0 = 5*c/4 := by
  norm_num [scalarCoefficient, boostedPerturbation, boostAB, roleLorentzMetric,
    Matrix.mul_apply, Matrix.sub_apply, Matrix.add_apply, Matrix.diagonal_apply,
    sum_role, A, B, C, D, roleLorentzSign, roleRoleSigEquiv, roleSign]
  ring

theorem scalar_second_boost (c : ℝ) :
    scalarCoefficient c (boostedPerturbation secondPerturbation) -
      scalarCoefficient c secondPerturbation = 33*c/8 - 1/4 := by
  norm_num [scalarCoefficient, boostedPerturbation, secondPerturbation, boostAB, roleLorentzMetric,
    Matrix.mul_apply, Matrix.sub_apply, Matrix.add_apply, Matrix.diagonal_apply,
    sum_role, A, B, C, D, roleLorentzSign, roleRoleSigEquiv, roleSign]
  have hc : (Finset.univ.filter (fun x : Role => x = (1, 1))).card = 1 := by decide
  norm_num [hc]
  ring

/-- No coefficient makes the literal scalar block invariant on every raw frame orbit. -/
theorem no_coefficient_scalar_descent (c : ℝ) :
    ¬ (∀ e : Matrix Role Role ℝ,
      scalarCoefficient c (boostedPerturbation e) = scalarCoefficient c e) := by
  intro h
  have h0 := scalar_flat_boost c
  rw [h 0] at h0
  have hc : c = 0 := by linarith
  have h1 := scalar_second_boost c
  rw [h secondPerturbation, hc] at h1
  norm_num at h1

/-- The critical coefficient's scalar readout has vanishing full first jet here. -/
theorem critical_scalar_completion (v : Matrix Role Role ℝ) (t : ℝ) :
    scalarCoefficient 1 (halfIdentity + t • v) =
      t^2 * (∑ r : Role, ∑ a : Role, (v r a)^2) := by
  norm_num [scalarCoefficient, halfIdentity, Matrix.diagonal_apply, Matrix.add_apply,
    Matrix.smul_apply, smul_eq_mul, sum_role, A, B, C, D]
  ring

/-- The actual raw solder right action, with constant data, is the one tested above. -/
theorem tested_frame_is_literal (N : ℕ) (e : Matrix Role Role ℝ) :
    rawFullSolderFrameAction N (fun _ => e) (fun _ => boostAB) =
      fun _ => boostedPerturbation e := by
  funext x r a
  rfl

/-- The tested transformation preserves the actual Gram for every input matrix. -/
theorem tested_gram_invariant (e : Matrix Role Role ℝ) :
    (roleLorentzMetric + boostedPerturbation e) * roleLorentzMetric *
        (roleLorentzMetric + boostedPerturbation e).transpose =
      (roleLorentzMetric + e) * roleLorentzMetric * (roleLorentzMetric + e).transpose := by
  have h : roleLorentzMetric + boostedPerturbation e = (roleLorentzMetric + e)*boostAB := by
    ext r a
    simp [boostedPerturbation]
  rw [h]
  exact rawSolderGram_frame_invariant _ _ boost_lorentz

local instance : LinearOrder Role := LinearOrder.lift' roleCode roleCode_injective

/-- Bind the actual scalar occupation vector to the exterior-algebra unit. -/
theorem exterior_vacuum_is_one : archiveFockExteriorBasis fockVacuumState = 1 := by
  have hs : archiveFockSupportEquiv fockVacuumState = ∅ := by
    ext r
    simp [archiveFockSupportEquiv, archiveFockSupport, fockVacuumState]
  simp only [archiveFockExteriorBasis, Module.Basis.reindex_apply, Equiv.symm_symm, hs]
  rw [ExteriorAlgebra.basis_apply]
  simp only [ExteriorAlgebra.ιMulti_family, Finset.card_empty]
  exact ExteriorAlgebra.ιMulti_zero_apply _

theorem exterior_fixes_actual_vacuum (L : RoleSpace ≃ₗ[ℝ] RoleSpace) :
    archiveExteriorFrameLift L (Pi.single fockVacuumState (1 : ℝ)) =
      Pi.single fockVacuumState (1 : ℝ) := by
  apply archiveFockExteriorEquiv.injective
  rw [archiveExteriorFrameLift_basis, archiveFockExteriorEquiv_single, exterior_vacuum_is_one]
  exact map_one _

/-- Sharp coefficient-independent lower bound on the two actual scalar frame defects. -/
theorem uniform_scalar_frame_defect (c : ℝ) :
    (5/86 : ℝ) ≤ max
      |scalarCoefficient c (boostedPerturbation 0) - scalarCoefficient c 0|
      |scalarCoefficient c (boostedPerturbation secondPerturbation) -
        scalarCoefficient c secondPerturbation| := by
  rw [scalar_flat_boost, scalar_second_boost]
  have h0 := (abs_le.mp (le_max_left |5*c/4| |33*c/8-1/4|)).2
  have h1 := (abs_le.mp (le_max_right |5*c/4| |33*c/8-1/4|)).1
  linarith

#print axioms scalar_weight
#print axioms constant_scalar_weight
#print axioms half_scalar_coefficient
#print axioms scalar_unit_nonzero
#print axioms coefficient_one_has_kernel
#print axioms coefficient_two_same_field_nonzero
#print axioms half_scalar_block
#print axioms boost_lorentz
#print axioms scalar_flat_boost
#print axioms scalar_second_boost
#print axioms no_coefficient_scalar_descent
#print axioms critical_scalar_completion
#print axioms tested_frame_is_literal
#print axioms tested_gram_invariant
#print axioms exterior_vacuum_is_one
#print axioms exterior_fixes_actual_vacuum
#print axioms uniform_scalar_frame_defect
end
end D0.Research.NativeReferenceWeight
