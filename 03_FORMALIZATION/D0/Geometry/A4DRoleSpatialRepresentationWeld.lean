import D0.Geometry.TypedRoleOppositeCut
import D0.Representation.TypedRoleSceneAction
import D0.Geometry.ArchiveHodgeSpatialShellOperator
import Mathlib.Tactic

/-!
# A-stabilizer weld between balanced Role residuals and the spatial triad

This file identifies the three spatial coefficients with the restriction of a
zero-sum Role function after fixing Role A.  It does not identify the whole
typed scene carrier with an archive cochain or with the shell.
-/

namespace D0.Geometry

open D0.Geometry.TypedSceneOppositeCut
open D0.Geometry.TypedRoleOppositeCut
open D0.Representation.TypedRoleSceneAction
open RoleFockPermutation

noncomputable section

/-- Restrict a four-Role permutation fixing A to the three spatial Roles. -/
def spatialRolePerm (σ : SpatialRoleStabilizer) : SpatialRole ≃ SpatialRole where
  toFun := fun r => ⟨σ.1 r.1, by
    intro hA
    have hback : σ.1.symm A = A := FixesRoleA.symm σ.2
    have : r.1 = A := by
      calc
        r.1 = σ.1.symm (σ.1 r.1) := (σ.1.symm_apply_apply r.1).symm
        _ = σ.1.symm A := by rw [hA]
        _ = A := hback
    exact r.2 this⟩
  invFun := fun r => ⟨σ.1.symm r.1, by
    intro hA
    have : r.1 = A := by
      calc
        r.1 = σ.1 (σ.1.symm r.1) := (σ.1.apply_symm_apply r.1).symm
        _ = σ.1 A := by rw [hA]
        _ = A := σ.2
    exact r.2 this⟩
  left_inv r := by apply Subtype.ext; exact σ.1.symm_apply_apply r.1
  right_inv r := by apply Subtype.ext; exact σ.1.apply_symm_apply r.1

/-- The natural contravariant coefficient action of the A-stabilizer. -/
def spatialCoeffPerm (σ : SpatialRoleStabilizer) : (SpatialRole → ℚ) →ₗ[ℚ] (SpatialRole → ℚ) where
  toFun g r := g ((spatialRolePerm σ).symm r)
  map_add' g h := by ext r; rfl
  map_smul' c g := by ext r; rfl

def fin3SpatialAxisEquiv : Fin 3 ≃ SpatialAxis where
  toFun := ![SpatialAxis.b, SpatialAxis.c, SpatialAxis.d]
  invFun
    | .b => 0
    | .c => 1
    | .d => 2
  left_inv i := by fin_cases i <;> rfl
  right_inv a := by cases a <;> rfl

def fin3SpatialRoleEquiv : Fin 3 ≃ SpatialRole :=
  fin3SpatialAxisEquiv.trans spatialAxisEquivRole

def spatialCoeffToFin3 : (SpatialRole → ℚ) →ₗ[ℚ] (Fin 3 → ℚ) where
  toFun g i := g (fin3SpatialRoleEquiv i)
  map_add' g h := by ext i; rfl
  map_smul' c g := by ext i; rfl

def fin3ToSpatialCoeff : (Fin 3 → ℚ) →ₗ[ℚ] (SpatialRole → ℚ) where
  toFun g r := g (fin3SpatialRoleEquiv.symm r)
  map_add' g h := by ext r; rfl
  map_smul' c g := by ext r; rfl

/-- Extend spatial coefficients by the unique balancing value at Role A. -/
def balancedRoleOfSpatial : (SpatialRole → ℚ) →ₗ[ℚ] BalancedRole :=
  probeMap.comp spatialCoeffToFin3

/-- Restrict a balanced Role function to its three non-A coordinates. -/
def spatialOfBalancedRole : BalancedRole →ₗ[ℚ] (SpatialRole → ℚ) :=
  fin3ToSpatialCoeff.comp roleReadout

@[simp] theorem spatialOfBalancedRole_balancedRoleOfSpatial (g : SpatialRole → ℚ) :
    spatialOfBalancedRole (balancedRoleOfSpatial g) = g := by
  ext r
  change (roleReadout (probeMap (spatialCoeffToFin3 g)))
      (fin3SpatialRoleEquiv.symm r) = g r
  rw [roleReadout_probeMap]
  simp [spatialCoeffToFin3]

private theorem roleReadout_spatialRole (f : BalancedRole) :
    roleReadout f = spatialCoeffToFin3 (fun r => f.1 r.1) := by
  ext i
  fin_cases i <;>
    simp [roleReadout, roleCoord, spatialCoeffToFin3, fin3SpatialRoleEquiv,
      fin3SpatialAxisEquiv, spatialAxisEquivRole, spatialRoleB, spatialRoleC,
      spatialRoleD, A, B, C, D]

private theorem spatialOfBalancedRole_apply (f : BalancedRole) (r : SpatialRole) :
    spatialOfBalancedRole f r = f.1 r.1 := by
  change fin3ToSpatialCoeff (roleReadout f) r = f.1 r.1
  rw [roleReadout_spatialRole]
  simp [fin3ToSpatialCoeff, spatialCoeffToFin3]

private theorem spatialRole_sum_eq_fin3 (g : SpatialRole → ℚ) :
    (∑ r : SpatialRole, g r) = ∑ i : Fin 3, g (fin3SpatialRoleEquiv i) :=
  (Equiv.sum_comp fin3SpatialRoleEquiv g).symm

@[simp] theorem balancedRoleOfSpatial_apply_spatial
    (g : SpatialRole → ℚ) (r : SpatialRole) :
    (balancedRoleOfSpatial g).1 r.1 = g r := by
  have h := congrFun (spatialOfBalancedRole_balancedRoleOfSpatial g) r
  rw [spatialOfBalancedRole_apply] at h
  exact h

/-- The A-coordinate is exactly the unique zero-sum balancing value. -/
theorem balancedRoleOfSpatial_apply_A (g : SpatialRole → ℚ) :
    (balancedRoleOfSpatial g).1 A = -∑ r : SpatialRole, g r := by
  have hz := (balancedRoleOfSpatial g).2
  change ∑ r : Role, (balancedRoleOfSpatial g).1 r = 0 at hz
  rw [role_sum_four] at hz
  have hB := balancedRoleOfSpatial_apply_spatial g spatialRoleB
  have hC := balancedRoleOfSpatial_apply_spatial g spatialRoleC
  have hD := balancedRoleOfSpatial_apply_spatial g spatialRoleD
  have hsum : (∑ r : SpatialRole, g r) =
      g spatialRoleB + g spatialRoleC + g spatialRoleD := by
    rw [spatialRole_sum_eq_fin3]
    rw [Fin.sum_univ_succ, Fin.sum_univ_succ, Fin.sum_univ_succ]
    simp [fin3SpatialRoleEquiv, fin3SpatialAxisEquiv, spatialAxisEquivRole,
      spatialRoleB, spatialRoleC, spatialRoleD]
    ring
  have hB' : (balancedRoleOfSpatial g).1 B = g spatialRoleB := by
    simpa [spatialRoleB] using hB
  have hC' : (balancedRoleOfSpatial g).1 C = g spatialRoleC := by
    simpa [spatialRoleC] using hC
  have hD' : (balancedRoleOfSpatial g).1 D = g spatialRoleD := by
    simpa [spatialRoleD] using hD
  rw [hB', hC', hD'] at hz
  calc
    (balancedRoleOfSpatial g).1 A =
        -(g spatialRoleB + g spatialRoleC + g spatialRoleD) := by linarith
    _ = -∑ r : SpatialRole, g r := by rw [hsum]

@[simp] theorem balancedRoleOfSpatial_spatialOfBalancedRole (f : BalancedRole) :
    balancedRoleOfSpatial (spatialOfBalancedRole f) = f := by
  change probeMap (spatialCoeffToFin3 (fin3ToSpatialCoeff (roleReadout f))) = f
  rw [show spatialCoeffToFin3 (fin3ToSpatialCoeff (roleReadout f)) = roleReadout f by
    ext i
    simp [spatialCoeffToFin3, fin3ToSpatialCoeff]]
  exact probeMap_roleReadout f

/-- Canonical linear equivalence: spatial coefficients are balanced Role functions. -/
def balancedRoleOfSpatial_iso : (SpatialRole → ℚ) ≃ₗ[ℚ] BalancedRole where
  toFun := balancedRoleOfSpatial
  invFun := spatialOfBalancedRole
  left_inv := spatialOfBalancedRole_balancedRoleOfSpatial
  right_inv := balancedRoleOfSpatial_spatialOfBalancedRole
  map_add' := balancedRoleOfSpatial.map_add
  map_smul' := balancedRoleOfSpatial.map_smul

/-- Restriction/extension intertwines the natural A-stabilizer actions structurally. -/
theorem balancedRoleOfSpatial_stabilizer_intertwines
    (σ : SpatialRoleStabilizer) (g : SpatialRole → ℚ) :
    balancedRoleOfSpatial (spatialCoeffPerm σ g) =
      balancedRole_perm σ.1 (balancedRoleOfSpatial g) := by
  apply (balancedRoleOfSpatial_iso.symm).injective
  change spatialOfBalancedRole (balancedRoleOfSpatial (spatialCoeffPerm σ g)) =
    spatialOfBalancedRole (balancedRole_perm σ.1 (balancedRoleOfSpatial g))
  rw [spatialOfBalancedRole_balancedRoleOfSpatial]
  ext r
  have hrA : σ.1.symm r.1 ≠ A := by
    intro hA
    apply r.2
    calc
      r.1 = σ.1 (σ.1.symm r.1) := (σ.1.apply_symm_apply r.1).symm
      _ = σ.1 A := by rw [hA]
      _ = A := σ.2
  change g ((spatialRolePerm σ).symm r) =
    spatialOfBalancedRole (balancedRole_perm σ.1 (balancedRoleOfSpatial g)) r
  rw [spatialOfBalancedRole_apply]
  rw [balancedRole_perm]
  change g ((spatialRolePerm σ).symm r) =
    (balancedRoleOfSpatial g).1 (σ.1.symm r.1)
  rw [show (spatialRolePerm σ).symm r = ⟨σ.1.symm r.1, hrA⟩ by
    apply Subtype.ext
    rfl]
  rw [← balancedRoleOfSpatial_apply_spatial g ⟨σ.1.symm r.1, hrA⟩]

/-- The restricted Role-summand readout of the typed residual. -/
def typedRoleSpatialReadout (wAB wAC wBC : ℚ) (g : SpatialRole → ℚ) : SpatialRole → ℚ :=
  fun r => typedRoleResidual wAB wAC wBC (balancedRoleOfSpatial g)
    (Sum.inr (Sum.inr (Sum.inr r.1)))

/-- Exact scalar spatial-triad readout of the typed Role residual. -/
theorem typedRoleSpatialReadout_eq_scalar (wAB wAC wBC : ℚ) (g : SpatialRole → ℚ) :
    typedRoleSpatialReadout wAB wAC wBC g =
      (99 * (wAC - wBC)) • g := by
  funext r
  rw [typedRoleSpatialReadout, typed_role_residual_roleSummand]
  rw [balancedRoleOfSpatial_apply_spatial]
  simp [smul_eq_mul]

/-- Spatial residual is equivariant under the common A-stabilizer action. -/
theorem typedRoleSpatialReadout_stabilizer_equivariant
    (σ : SpatialRoleStabilizer) (wAB wAC wBC : ℚ) (g : SpatialRole → ℚ) :
    typedRoleSpatialReadout wAB wAC wBC (spatialCoeffPerm σ g) =
      spatialCoeffPerm σ (typedRoleSpatialReadout wAB wAC wBC g) := by
  rw [typedRoleSpatialReadout_eq_scalar, typedRoleSpatialReadout_eq_scalar]
  ext r
  rfl

/-- Package N capstone: exact spatial-triad readout and its stabilizer covariance. -/
theorem typedRoleCut_stabA_eq_spatialTriad
    (σ : SpatialRoleStabilizer) (wAB wAC wBC : ℚ) (g : SpatialRole → ℚ) :
    typedRoleSpatialReadout wAB wAC wBC g =
        (99 * (wAC - wBC)) • g ∧
      typedRoleSpatialReadout wAB wAC wBC (spatialCoeffPerm σ g) =
        spatialCoeffPerm σ (typedRoleSpatialReadout wAB wAC wBC g) :=
  ⟨typedRoleSpatialReadout_eq_scalar wAB wAC wBC g,
    typedRoleSpatialReadout_stabilizer_equivariant σ wAB wAC wBC g⟩

/-- Exact shell action: axis is permuted, harmonic label is fixed, and Fock state
is transported with its fermionic sign. -/
theorem spatialTriad_shell_action
    {N : ℕ} (σ : SpatialRoleStabilizer)
    (p : (SpatialAxis × ShellHarmonic) × ArchiveFockState) :
    diagonalRoleTransport σ.1 (shellCochain N p) =
      (RoleFockPermutation.fermionSign σ.1 p.2 : ℝ) • shellCochain N
        ((permutedShellAxis σ.1 σ.2 p.1.1, p.1.2), RoleFockPermutation.transportState σ.1 p.2) :=
  diagonalRoleTransport_shellCochain σ.1 σ.2 p

end

end D0.Geometry
