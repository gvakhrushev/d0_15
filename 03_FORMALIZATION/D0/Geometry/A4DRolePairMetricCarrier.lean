import Mathlib.Data.Matrix.Basic
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.Tactic
import D0.Geometry.A4DSymRoleCentralDifference
import D0.Geometry.ArchivePhaseEdgeMetricScale

noncomputable section

namespace D0.Geometry

open D0
open ArchivePhaseEdgeMetricScale

/-!
# A4D role-pair metric carrier

This file owns the finite typed comparison layer requested by E-METPROV.  A role-pair is
represented by its unique increasing representative for the explicit four-role code; hence
it is unordered data with the diagonal removed.  The six pair coordinates are a new
symmetric shear carrier.  In particular, they are not the oriented amplitudes of an
exterior/cochain carrier.

The target of the linear equivalence below is a submodule of matrix-valued fields.  This is
the linearized vector-space wrapper of `LocalSymRoleField`: it contains exactly the actual
sitewise symmetric matrices, while retaining the additive and scalar structure needed by a
literal `LinearEquiv`.

No metric provenance, signature, curvature, gravity response, continuum limit, or naturality
claim is made here.
-/

/-! A canonical code for the four roles, used only to choose an unordered representative. -/
def roleCode (r : Role) : Fin 4 :=
  ⟨2 * r.1.val + r.2.val, by omega⟩

theorem roleCode_injective : Function.Injective roleCode := by
  intro a b h
  rcases a with ⟨a₁, a₂⟩
  rcases b with ⟨b₁, b₂⟩
  fin_cases a₁ <;> fin_cases a₂ <;> fin_cases b₁ <;> fin_cases b₂ <;>
    simp [roleCode] at h ⊢

/-! Unordered distinct pairs: the increasing representative is unique. -/
def RolePair := {p : Role × Role // roleCode p.1 < roleCode p.2}

instance : Fintype RolePair :=
  Fintype.subtype (Finset.univ.filter (fun p : Role × Role => roleCode p.1 < roleCode p.2)) (by simp)

instance : DecidableEq RolePair := Subtype.instDecidableEq

theorem rolePair_ne (p : RolePair) : p.1.1 ≠ p.1.2 := by
  intro h
  have hlt := p.2
  rw [h] at hlt
  exact (lt_irrefl (roleCode p.1.2)) hlt

def rolePairOfDistinct (a b : Role) (h : a ≠ b) : RolePair :=
  if hab : roleCode a < roleCode b then
    ⟨(a, b), hab⟩
  else
    ⟨(b, a), (lt_or_gt_of_ne (fun hcode => h (roleCode_injective hcode))).resolve_left hab⟩

theorem rolePairOfDistinct_swap (a b : Role) (h : a ≠ b) :
    rolePairOfDistinct b a (Ne.symm h) = rolePairOfDistinct a b h := by
  have hcode : roleCode a ≠ roleCode b := fun hcode => h (roleCode_injective hcode)
  by_cases hab : roleCode a < roleCode b
  · have hba : ¬ roleCode b < roleCode a := not_lt_of_ge (le_of_lt hab)
    simp [rolePairOfDistinct, hab, hba]
  · have hba : roleCode b < roleCode a := (lt_or_gt_of_ne hcode).resolve_left hab
    simp [rolePairOfDistinct, hab, hba]

theorem rolePairOfDistinct_ordered (p : RolePair) :
    rolePairOfDistinct p.1.1 p.1.2 (rolePair_ne p) = p := by
  simp [rolePairOfDistinct, p.2]

def rolePairAC : RolePair := ⟨(A, C), by decide⟩
def rolePairAD : RolePair := ⟨(A, D), by decide⟩
def rolePairAB : RolePair := ⟨(A, B), by decide⟩
def rolePairCD : RolePair := ⟨(C, D), by decide⟩
def rolePairCB : RolePair := ⟨(C, B), by decide⟩
def rolePairDB : RolePair := ⟨(D, B), by decide⟩

theorem rolePair_card : Fintype.card RolePair = 6 := by
  native_decide

/-! The actual 4+6 finite local and sitewise carriers. -/
abbrev RoleVec := Role → ℝ
abbrev LocalAxisField (N : ℕ) := ArchiveRolePhaseGroup N → RoleVec
abbrev LocalShearField (N : ℕ) := ArchiveRolePhaseGroup N → RolePair → ℝ
abbrev MetricCarrier (N : ℕ) := LocalAxisField N × LocalShearField N

abbrev LocalAxisCarrier := RoleVec
abbrev LocalShearCarrier := RolePair → ℝ
abbrev LocalMetricCarrier := LocalAxisCarrier × LocalShearCarrier

/-! The symmetric matrix wrapper around `LocalSymRoleField`. -/
def localSymmetricMatrixSubmodule (N : ℕ) :
    Submodule ℝ (ArchiveRolePhaseGroup N → Matrix Role Role ℝ) where
  carrier := {M | ∀ x a b, M x a b = M x b a}
  zero_mem' := by
    intro x a b
    rfl
  add_mem' := by
    intro M K hM hK x a b
    simp only [Pi.add_apply, Matrix.add_apply]
    rw [hM x a b, hK x a b]
  smul_mem' := by
    intro c M hM x a b
    simp only [Pi.smul_apply, Matrix.smul_apply]
    rw [hM x a b]

def matrixFromMetricCarrier (N : ℕ) (m : MetricCarrier N) :
    ArchiveRolePhaseGroup N → Matrix Role Role ℝ :=
  fun x a b => if h : a = b then m.1 x a else m.2 x (rolePairOfDistinct a b h)

theorem matrixFromMetricCarrier_symmetric (N : ℕ) (m : MetricCarrier N) :
    ∀ x a b, matrixFromMetricCarrier N m x a b = matrixFromMetricCarrier N m x b a := by
  intro x a b
  by_cases hab : a = b
  · subst b
    simp [matrixFromMetricCarrier]
  · have hba : b ≠ a := Ne.symm hab
    simp only [matrixFromMetricCarrier, dif_neg hab, dif_neg hba]
    rw [rolePairOfDistinct_swap a b hab]

def metricCarrierToMatrix (N : ℕ) :
    MetricCarrier N →ₗ[ℝ] localSymmetricMatrixSubmodule N where
  toFun m := ⟨matrixFromMetricCarrier N m, matrixFromMetricCarrier_symmetric N m⟩
  map_add' u v := by
    apply Subtype.ext
    funext x a b
    by_cases h : a = b <;> simp [matrixFromMetricCarrier, h]
  map_smul' c u := by
    apply Subtype.ext
    funext x a b
    by_cases h : a = b <;> simp [matrixFromMetricCarrier, h]

def matrixToMetricCarrier (N : ℕ) (M : localSymmetricMatrixSubmodule N) : MetricCarrier N :=
  (fun x a => M.1 x a a, fun x p => M.1 x p.1.1 p.1.2)

def matrixToMetricCarrierMap (N : ℕ) :
    localSymmetricMatrixSubmodule N →ₗ[ℝ] MetricCarrier N where
  toFun := matrixToMetricCarrier N
  map_add' M K := by
    apply Prod.ext
    · funext x a
      simp [matrixToMetricCarrier]
    · funext x p
      simp [matrixToMetricCarrier]
  map_smul' c M := by
    apply Prod.ext
    · funext x a
      simp [matrixToMetricCarrier]
    · funext x p
      simp [matrixToMetricCarrier]

theorem matrixToMetricCarrier_matrixFrom (N : ℕ) (m : MetricCarrier N) :
    matrixToMetricCarrier N (metricCarrierToMatrix N m) = m := by
  apply Prod.ext
  · funext x a
    simp [matrixToMetricCarrier, metricCarrierToMatrix, matrixFromMetricCarrier]
  · funext x p
    change
      (if h : p.1.1 = p.1.2 then m.1 x p.1.1
        else m.2 x (rolePairOfDistinct p.1.1 p.1.2 h)) = m.2 x p
    rw [dif_neg (rolePair_ne p), rolePairOfDistinct_ordered p]

theorem matrixFromMetricCarrier_matrixTo (N : ℕ)
    (M : localSymmetricMatrixSubmodule N) :
    metricCarrierToMatrix N (matrixToMetricCarrier N M) = M := by
  apply Subtype.ext
  funext x a b
  by_cases hab : a = b
  · subst b
    simp [metricCarrierToMatrix, matrixFromMetricCarrier, matrixToMetricCarrier]
  · have hcode : roleCode a ≠ roleCode b := fun hcode => hab (roleCode_injective hcode)
    by_cases habCode : roleCode a < roleCode b
    · have hpair : rolePairOfDistinct a b hab = ⟨(a, b), habCode⟩ := by
        simp [rolePairOfDistinct, habCode]
      dsimp [metricCarrierToMatrix, matrixToMetricCarrier, matrixFromMetricCarrier]
      simp only [dif_neg hab]
      rw [hpair]
    · have hbaCode : roleCode b < roleCode a :=
        (lt_or_gt_of_ne hcode).resolve_left habCode
      have hpair : rolePairOfDistinct a b hab = ⟨(b, a), hbaCode⟩ := by
        simp [rolePairOfDistinct, habCode]
      dsimp [metricCarrierToMatrix, matrixToMetricCarrier, matrixFromMetricCarrier]
      simp only [dif_neg hab]
      rw [hpair]
      exact M.property x b a

/-! Literal finite equivalence: diagonal axis variables plus unordered shear variables. -/
def metricCarrierEquiv (N : ℕ) :
    MetricCarrier N ≃ₗ[ℝ] localSymmetricMatrixSubmodule N where
  toFun := metricCarrierToMatrix N
  invFun := matrixToMetricCarrierMap N
  left_inv := matrixToMetricCarrier_matrixFrom N
  right_inv := matrixFromMetricCarrier_matrixTo N
  map_add' := (metricCarrierToMatrix N).map_add
  map_smul' := (metricCarrierToMatrix N).map_smul

theorem metricCarrierEquiv_diagonal (N : ℕ) (m : MetricCarrier N) (x : ArchiveRolePhaseGroup N)
    (a : Role) :
    (metricCarrierEquiv N m).1 x a a = m.1 x a := by
  simp [metricCarrierEquiv, metricCarrierToMatrix, matrixFromMetricCarrier]

theorem metricCarrierEquiv_offDiagonal (N : ℕ) (m : MetricCarrier N)
    (x : ArchiveRolePhaseGroup N) (a b : Role) (h : a ≠ b) :
    (metricCarrierEquiv N m).1 x a b = m.2 x (rolePairOfDistinct a b h) := by
  simp [metricCarrierEquiv, metricCarrierToMatrix, matrixFromMetricCarrier, h]

/-! The existing directional sector is exactly the diagonal locus. -/
def axisEmbedding (N : ℕ) : LocalAxisField N →ₗ[ℝ] MetricCarrier N :=
  LinearMap.inl ℝ (LocalAxisField N) (LocalShearField N)

theorem axisEmbedding_shear_zero (N : ℕ) (a : LocalAxisField N) :
    (axisEmbedding N a).2 = 0 := rfl

theorem axisEmbedding_matrix_offDiagonal_zero (N : ℕ) (a : LocalAxisField N)
    (x : ArchiveRolePhaseGroup N) (r : RolePair) :
    (metricCarrierEquiv N (axisEmbedding N a)).1 x r.1.1 r.1.2 = 0 := by
  rw [metricCarrierEquiv_offDiagonal]
  · simp [axisEmbedding]
  · exact rolePair_ne r

/-! Local dimension accounting: 4 axis coordinates and 6 missing symmetric shears. -/
theorem local_axis_finrank : Module.finrank ℝ LocalAxisCarrier = 4 := by
  rw [Module.finrank_pi, card_role]

theorem local_shear_finrank : Module.finrank ℝ LocalShearCarrier = 6 := by
  rw [Module.finrank_pi, rolePair_card]

theorem local_metric_carrier_finrank : Module.finrank ℝ LocalMetricCarrier = 10 := by
  rw [Module.finrank_prod, local_axis_finrank, local_shear_finrank]

theorem local_axis_codimension_six :
    Module.finrank ℝ LocalMetricCarrier - Module.finrank ℝ LocalAxisCarrier = 6 := by
  rw [local_metric_carrier_finrank, local_axis_finrank]

theorem global_axis_finrank (N : ℕ) :
    Module.finrank ℝ (LocalAxisField N) = Fintype.card (ArchiveRolePhaseGroup N) * 4 := by
  change Module.finrank ℝ (∀ _ : ArchiveRolePhaseGroup N, LocalAxisCarrier) = _
  calc
    _ = ∑ _ : ArchiveRolePhaseGroup N, Module.finrank ℝ LocalAxisCarrier :=
      by
        simpa using
          (Module.finrank_pi_fintype ℝ (ι := ArchiveRolePhaseGroup N)
            (M := fun _ : ArchiveRolePhaseGroup N => LocalAxisCarrier))
    _ = Fintype.card (ArchiveRolePhaseGroup N) * Module.finrank ℝ LocalAxisCarrier := by
      simp
    _ = _ := by rw [local_axis_finrank]

theorem global_shear_finrank (N : ℕ) :
    Module.finrank ℝ (LocalShearField N) = Fintype.card (ArchiveRolePhaseGroup N) * 6 := by
  change Module.finrank ℝ (∀ _ : ArchiveRolePhaseGroup N, LocalShearCarrier) = _
  calc
    _ = ∑ _ : ArchiveRolePhaseGroup N, Module.finrank ℝ LocalShearCarrier :=
      by
        simpa using
          (Module.finrank_pi_fintype ℝ (ι := ArchiveRolePhaseGroup N)
            (M := fun _ : ArchiveRolePhaseGroup N => LocalShearCarrier))
    _ = Fintype.card (ArchiveRolePhaseGroup N) * Module.finrank ℝ LocalShearCarrier := by
      simp
    _ = _ := by rw [local_shear_finrank]

theorem global_metric_carrier_finrank (N : ℕ) :
    Module.finrank ℝ (MetricCarrier N) = Fintype.card (ArchiveRolePhaseGroup N) * 10 := by
  rw [Module.finrank_prod, global_axis_finrank, global_shear_finrank]
  omega

theorem global_axis_codimension_six (N : ℕ) :
    Module.finrank ℝ (MetricCarrier N) - Module.finrank ℝ (LocalAxisField N) =
      6 * archiveModes N := by
  rw [global_metric_carrier_finrank, global_axis_finrank,
    card_archive_role_phase_group N]
  omega

/-! A concrete pure shear point outside the diagonal/axis image. -/
def pureOffDiagonalWitness (N : ℕ) : MetricCarrier N :=
  (0, fun _ p => if p = rolePairAC then 1 else 0)

theorem pureOffDiagonalWitness_not_axisImage (N : ℕ) :
    pureOffDiagonalWitness N ∉ Set.range (axisEmbedding N) := by
  intro h
  rcases h with ⟨a, ha⟩
  have hs : (pureOffDiagonalWitness N).2 = (axisEmbedding N a).2 :=
    congrArg Prod.snd ha.symm
  have hv := congrFun hs (0 : ArchiveRolePhaseGroup N)
  have hv' := congrFun hv rolePairAC
  simp [pureOffDiagonalWitness, axisEmbedding] at hv'

theorem pureOffDiagonalWitness_has_unit_shear (N : ℕ) :
    (pureOffDiagonalWitness N).2 0 rolePairAC = 1 := by
  simp [pureOffDiagonalWitness]

/-! Conductance-to-metric scale is named and kept explicit; no physical interpretation is added. -/
noncomputable def conductanceToMetricScale (N : ℕ) : ℝ :=
  archiveMetricLaplacianScale N

theorem conductanceToMetricScale_pos (N : ℕ) : 0 < conductanceToMetricScale N := by
  exact archive_phase_edge_metric_scale_owner.2.2 N

/-! Exterior/cochain negative control: oriented amplitudes are antisymmetric, not shear data. -/
def OrientedRolePair := {p : Role × Role // p.1 ≠ p.2}

instance : Fintype OrientedRolePair :=
  Fintype.subtype (Finset.univ.filter (fun p : Role × Role => p.1 ≠ p.2)) (by simp)

instance : DecidableEq OrientedRolePair := Subtype.instDecidableEq

def orientedSwap (p : OrientedRolePair) : OrientedRolePair :=
  ⟨(p.1.2, p.1.1), p.2.symm⟩

abbrev ExteriorPairAmplitude := OrientedRolePair → ℝ

def IsExteriorPairAmplitude (u : ExteriorPairAmplitude) : Prop :=
  ∀ p, u (orientedSwap p) = -u p

def symmetricShearLift (s : LocalShearCarrier) : ExteriorPairAmplitude :=
  fun p => s (rolePairOfDistinct p.1.1 p.1.2 p.2)

theorem symmetricShearLift_swap (s : LocalShearCarrier) (p : OrientedRolePair) :
    symmetricShearLift s (orientedSwap p) = symmetricShearLift s p := by
  unfold symmetricShearLift orientedSwap
  rw [rolePairOfDistinct_swap p.1.1 p.1.2 p.2]

def orientedAC : OrientedRolePair := ⟨(A, C), by decide⟩

theorem symmetricShearLift_AC (s : LocalShearCarrier) :
    symmetricShearLift s orientedAC = s rolePairAC := by
  have hAC : roleCode A < roleCode C := by decide
  simp [symmetricShearLift, orientedAC, rolePairOfDistinct, rolePairAC, hAC]

def pureSymmetricShear : LocalShearCarrier :=
  fun p => if p = rolePairAC then 1 else 0

theorem pureSymmetricShear_not_exterior :
    ¬ IsExteriorPairAmplitude (symmetricShearLift pureSymmetricShear) := by
  intro h
  have hh := h orientedAC
  rw [symmetricShearLift_swap, symmetricShearLift_AC] at hh
  norm_num [pureSymmetricShear] at hh

end D0.Geometry
