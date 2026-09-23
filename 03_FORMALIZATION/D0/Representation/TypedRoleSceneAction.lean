import D0.Foundation.M1RieszRepresentationGap
import D0.Geometry.TypedTowerResidualClosure
import D0.Representation.OrientationZoneDescentNoGo
import Mathlib.LinearAlgebra.Basis.Defs
import Mathlib.LinearAlgebra.StdBasis
import Mathlib.Tactic

/-!
# Perm Role on the typed Role summand

`Equiv.Perm Role` fixes the `V9` summand of `V13` and acts on the Role
summand.  The same permutation acts on `BalancedRole` and on the typed
Role-cut edges.  The Role cut is equivariant for that action.

This is not the Omega8 orientation flip, which fixes the Role summand and
flips the orientation bit inside `V9`.  The two actions commute on `V13`.

A bare equivalence `V13 ≃ Fin 13` does not choose the image of the Role
summand.  A structured bridge records that image, and only then transports
the typed Role cut onto the corresponding four-point set.  The canonical
cut theorems themselves stay on `D0.V9`, `D0.V11`, and `D0.V13`.

The archive Fock action is also indexed by `Equiv.Perm Role`, on a different
carrier.  This file does not identify the two carriers.
-/

namespace D0.Representation.TypedRoleSceneAction

open D0.Geometry.OppositeCutPairing
open D0.Geometry.TypedSceneOppositeCut
open D0.Geometry.TypedRoleOppositeCut
open D0.Foundation.M1RieszRepresentationGap
open D0.Representation.OrientationZoneDescentNoGo

/-! ## Action on V13 -/

/-- Fix the `V9` summand and apply `σ` on the Role summand. -/
def permuteV13RoleSummand (σ : Equiv.Perm Role) : V13 ≃ V13 where
  toFun
    | Sum.inl v => Sum.inl v
    | Sum.inr r => Sum.inr (σ r)
  invFun
    | Sum.inl v => Sum.inl v
    | Sum.inr r => Sum.inr (σ.symm r)
  left_inv
    | Sum.inl _ => rfl
    | Sum.inr r => by simp
  right_inv
    | Sum.inl _ => rfl
    | Sum.inr r => by simp

theorem permuteV13RoleSummand_one :
    permuteV13RoleSummand 1 = Equiv.refl V13 := by
  ext v
  cases v <;> simp [permuteV13RoleSummand]

theorem permuteV13RoleSummand_mul (σ τ : Equiv.Perm Role) :
    permuteV13RoleSummand (σ * τ) =
      permuteV13RoleSummand σ * permuteV13RoleSummand τ := by
  ext v
  cases v with
  | inl v => rfl
  | inr r =>
      simp [permuteV13RoleSummand, Equiv.Perm.coe_mul]

theorem permuteV13RoleSummand_inv (σ : Equiv.Perm Role) :
    (permuteV13RoleSummand σ).symm = permuteV13RoleSummand σ.symm := by
  ext v
  cases v <;> simp [permuteV13RoleSummand]

/-! ## Action on BalancedRole -/

def permRoleFun (σ : Equiv.Perm Role) (f : Role → ℚ) : Role → ℚ :=
  fun r => f (σ.symm r)

theorem sum_comp_perm {ι : Type} [Fintype ι] [DecidableEq ι]
    (e : ι ≃ ι) (f : ι → ℚ) :
    ∑ i, f (e i) = ∑ i, f i := by
  have himg : (Finset.univ : Finset ι).image (⇑e) = Finset.univ := by
    ext i
    simp
  calc
    ∑ i, f (e i) = ∑ i ∈ (Finset.univ : Finset ι).image (⇑e), f i :=
      (Finset.sum_image (f := f) (g := (⇑e)) (s := Finset.univ)
        (fun _ _ _ _ h => e.injective h)).symm
    _ = ∑ i, f i := by rw [himg]

theorem permRoleFun_sum (σ : Equiv.Perm Role) (f : Role → ℚ) :
    ∑ r, permRoleFun σ f r = ∑ r, f r := by
  simpa [permRoleFun] using sum_comp_perm σ.symm f

def balancedRole_perm (σ : Equiv.Perm Role) : BalancedRole →ₗ[ℚ] BalancedRole where
  toFun f := ⟨permRoleFun σ f.1, by
    change ∑ r, permRoleFun σ f.1 r = 0
    rw [permRoleFun_sum]
    exact f.2⟩
  map_add' f g := by
    ext r
    simp [permRoleFun]
  map_smul' c f := by
    ext r
    simp [permRoleFun, smul_eq_mul]

theorem balancedRole_perm_one :
    balancedRole_perm 1 = LinearMap.id := by
  ext f r
  simp [balancedRole_perm, permRoleFun, Equiv.Perm.one_symm]

theorem balancedRole_perm_mul (σ τ : Equiv.Perm Role) :
    balancedRole_perm (σ * τ) = (balancedRole_perm σ).comp (balancedRole_perm τ) := by
  ext f r
  simp only [balancedRole_perm, permRoleFun, LinearMap.coe_comp, Function.comp_apply]
  congr 1

/-! ## Extension is equivariant -/

def permV13Fun (σ : Equiv.Perm Role) (g : V13 → ℚ) : V13 → ℚ :=
  fun v => g ((permuteV13RoleSummand σ).symm v)

theorem extendRole_perm_equivariant (σ : Equiv.Perm Role) (f : Role → ℚ) :
    extendRoleToV13 (permRoleFun σ f) = permV13Fun σ (extendRoleToV13 f) := by
  funext v
  cases v with
  | inl w =>
      simp [extendRoleToV13, extendInrLin, permRoleFun, permV13Fun, permuteV13RoleSummand]
  | inr r =>
      simp [extendRoleToV13, extendInrLin, permRoleFun, permV13Fun, permuteV13RoleSummand]

/-! ## Induced edge permutation -/

def permuteTypedEdgeByRole (σ : Equiv.Perm Role) : TypedSceneEdge ≃ TypedSceneEdge where
  toFun
    | Sum.inl ab => Sum.inl ab
    | Sum.inr (Sum.inl (a, c)) => Sum.inr (Sum.inl (a, permuteV13RoleSummand σ c))
    | Sum.inr (Sum.inr (b, c)) => Sum.inr (Sum.inr (b, permuteV13RoleSummand σ c))
  invFun
    | Sum.inl ab => Sum.inl ab
    | Sum.inr (Sum.inl (a, c)) => Sum.inr (Sum.inl (a, (permuteV13RoleSummand σ).symm c))
    | Sum.inr (Sum.inr (b, c)) => Sum.inr (Sum.inr (b, (permuteV13RoleSummand σ).symm c))
  left_inv e := by
    rcases e with ⟨a, b⟩ | ⟨a, c⟩ | ⟨b, c⟩
    · rfl
    · cases c <;> simp [permuteV13RoleSummand]
    · cases c <;> simp [permuteV13RoleSummand]
  right_inv e := by
    rcases e with ⟨a, b⟩ | ⟨a, c⟩ | ⟨b, c⟩
    · rfl
    · cases c <;> simp [permuteV13RoleSummand]
    · cases c <;> simp [permuteV13RoleSummand]

theorem permuteTypedEdgeByRole_one :
    permuteTypedEdgeByRole 1 = Equiv.refl TypedSceneEdge := by
  ext e
  rcases e with ab | ac | bc <;> simp [permuteTypedEdgeByRole, permuteV13RoleSummand_one]

theorem permuteTypedEdgeByRole_mul (σ τ : Equiv.Perm Role) :
    permuteTypedEdgeByRole (σ * τ) =
      permuteTypedEdgeByRole σ * permuteTypedEdgeByRole τ := by
  ext e
  rcases e with ab | ac | bc
  · rfl
  · rcases ac with ⟨a, c⟩
    simp [permuteTypedEdgeByRole, permuteV13RoleSummand_mul]
  · rcases bc with ⟨b, c⟩
    simp [permuteTypedEdgeByRole, permuteV13RoleSummand_mul]

theorem permuteTypedEdgeByRole_inv (σ : Equiv.Perm Role) :
    (permuteTypedEdgeByRole σ).symm = permuteTypedEdgeByRole σ.symm := by
  ext e
  rcases e with ab | ac | bc <;>
    simp [permuteTypedEdgeByRole, permuteV13RoleSummand_inv]

def permEdgeFun (σ : Equiv.Perm Role) (X : TypedSceneEdge → ℚ) : TypedSceneEdge → ℚ :=
  fun e => X ((permuteTypedEdgeByRole σ).symm e)

theorem typedRoleOppositeCut_perm_equivariant (σ : Equiv.Perm Role) (f : BalancedRole) :
    typedRoleOppositeCut (balancedRole_perm σ f) = permEdgeFun σ (typedRoleOppositeCut f) := by
  funext e
  rcases e with ab | ac | bc
  · simp [typedRoleOppositeCut_apply, oppositeCutGamma, permEdgeFun, permuteTypedEdgeByRole]
  · rcases ac with ⟨a, c⟩
    simp [typedRoleOppositeCut_apply, oppositeCutGamma, permEdgeFun, permuteTypedEdgeByRole,
      permuteV13RoleSummand_inv, extendRole_perm_equivariant, balancedRole_perm, permV13Fun]
  · rcases bc with ⟨b, c⟩
    simp [typedRoleOppositeCut_apply, oppositeCutGamma, permEdgeFun, permuteTypedEdgeByRole,
      permuteV13RoleSummand_inv, extendRole_perm_equivariant, balancedRole_perm, permV13Fun]

/-! ## Weighted incidence equivariance -/

def permuteTypedVertexByRole (σ : Equiv.Perm Role) : TypedSceneVertex ≃ TypedSceneVertex :=
  Equiv.sumCongr (Equiv.refl V9)
    (Equiv.sumCongr (Equiv.refl V11) (permuteV13RoleSummand σ))

def permVertexFun (σ : Equiv.Perm Role) (Y : TypedSceneVertex → ℚ) : TypedSceneVertex → ℚ :=
  fun v => Y ((permuteTypedVertexByRole σ).symm v)

theorem blockScale_perm (σ : Equiv.Perm Role) (wAB wAC wBC : ℚ) (X : TypedSceneEdge → ℚ) :
    blockScale wAB wAC wBC (permEdgeFun σ X) =
      permEdgeFun σ (blockScale wAB wAC wBC X) := by
  funext e
  rcases e with ab | ac | bc <;>
    simp [blockScale, permEdgeFun, permuteTypedEdgeByRole]

theorem unsignedIncidence_perm (σ : Equiv.Perm Role) (X : TypedSceneEdge → ℚ) :
    unsignedIncidence (α := V9) (β := V11) (permEdgeFun σ X) =
      permVertexFun σ (unsignedIncidence (α := V9) (β := V11) X) := by
  funext v
  rcases v with a | b | c
  · have hAB : (∑ b : V11, permEdgeFun σ X (Sum.inl (a, b))) =
        ∑ b : V11, X (Sum.inl (a, b)) := by
      simp [permEdgeFun, permuteTypedEdgeByRole]
    have hAC : (∑ c : V13, permEdgeFun σ X (Sum.inr (Sum.inl (a, c)))) =
        ∑ c : V13, X (Sum.inr (Sum.inl (a, c))) := by
      simpa [permEdgeFun, permuteTypedEdgeByRole, permuteV13RoleSummand_inv] using
        sum_comp_perm (permuteV13RoleSummand σ).symm
          (fun c => X (Sum.inr (Sum.inl (a, c))))
    simp [unsignedIncidence, permVertexFun, permuteTypedVertexByRole, hAB, hAC]
  · have hAB : (∑ a : V9, permEdgeFun σ X (Sum.inl (a, b))) =
        ∑ a : V9, X (Sum.inl (a, b)) := by
      simp [permEdgeFun, permuteTypedEdgeByRole]
    have hBC : (∑ c : V13, permEdgeFun σ X (Sum.inr (Sum.inr (b, c)))) =
        ∑ c : V13, X (Sum.inr (Sum.inr (b, c))) := by
      simpa [permEdgeFun, permuteTypedEdgeByRole, permuteV13RoleSummand_inv] using
        sum_comp_perm (permuteV13RoleSummand σ).symm
          (fun c => X (Sum.inr (Sum.inr (b, c))))
    simp [unsignedIncidence, permVertexFun, permuteTypedVertexByRole, hAB, hBC]
  · simp [unsignedIncidence, permVertexFun, permuteTypedVertexByRole, permEdgeFun,
      permuteTypedEdgeByRole, permuteV13RoleSummand_inv]

theorem typed_role_weighted_incidence_perm_equivariant
    (σ : Equiv.Perm Role) (wAB wAC wBC : ℚ) (X : TypedSceneEdge → ℚ) :
    unsignedIncidence (blockScale wAB wAC wBC (permEdgeFun σ X)) =
      permVertexFun σ (unsignedIncidence (blockScale wAB wAC wBC X)) := by
  rw [blockScale_perm, unsignedIncidence_perm]

/-! ## Balanced Role basis -/

def roleIndicator (r : Role) : Role → ℚ :=
  fun s => if s = r then 1 else 0

def roleDifference (r : Role) : Role → ℚ :=
  fun s => roleIndicator r s - roleIndicator A s

theorem B_ne_A : B ≠ A := by decide
theorem C_ne_A : C ≠ A := by decide
theorem D_ne_A : D ≠ A := by decide

theorem sum_roleDifference (r : Role) (hr : r ≠ A) :
    ∑ s, roleDifference r s = 0 := by
  simp only [roleDifference, roleIndicator, Finset.sum_sub_distrib]
  have hr1 : ∑ s : Role, (if s = r then (1 : ℚ) else 0) = 1 := by
    simp [Finset.sum_ite_eq']
  have ha1 : ∑ s : Role, (if s = A then (1 : ℚ) else 0) = 1 := by
    simp [Finset.sum_ite_eq']
  simp [hr1, ha1]

def roleProbe (r : Role) (hr : r ≠ A) : BalancedRole :=
  ⟨roleDifference r, sum_roleDifference r hr⟩

def balancedRoleProbe : Fin 3 → BalancedRole
  | 0 => roleProbe B B_ne_A
  | 1 => roleProbe C C_ne_A
  | 2 => roleProbe D D_ne_A

def roleCoord (f : Role → ℚ) : Fin 3 → ℚ :=
  fun i => if i = 0 then f B else if i = 1 then f C else f D

theorem role_sum_four (f : Role → ℚ) :
    ∑ r, f r = f A + f B + f C + f D := by
  simp only [Role, Dyad, Fintype.sum_prod_type, Fin.sum_univ_two, A, B, C, D]
  ring

def roleReadout : BalancedRole →ₗ[ℚ] (Fin 3 → ℚ) where
  toFun f := roleCoord f.1
  map_add' f g := by
    ext i
    fin_cases i <;> simp [roleCoord]
  map_smul' c f := by
    ext i
    fin_cases i <;> simp [roleCoord, smul_eq_mul, RingHom.id_apply]

theorem roleDifference_apply_self {r : Role} (hr : r ≠ A) :
    roleDifference r r = 1 := by
  simp [roleDifference, roleIndicator, hr]

theorem roleDifference_apply_A {r : Role} (hr : r ≠ A) :
    roleDifference r A = -1 := by
  simp [roleDifference, roleIndicator, Ne.symm hr]

theorem roleDifference_apply_ne {r s : Role} (hsr : s ≠ r) (hsA : s ≠ A) :
    roleDifference r s = 0 := by
  simp [roleDifference, roleIndicator, hsr, hsA]

theorem B_ne_C : B ≠ C := by decide
theorem B_ne_D : B ≠ D := by decide
theorem C_ne_D : C ≠ D := by decide
theorem C_ne_B : C ≠ B := by decide
theorem D_ne_B : D ≠ B := by decide
theorem D_ne_C : D ≠ C := by decide

theorem roleReadout_probe (i : Fin 3) :
    roleReadout (balancedRoleProbe i) = fun j => if j = i then 1 else 0 := by
  fin_cases i <;> ext j <;> fin_cases j <;>
    simp [roleReadout, roleCoord, balancedRoleProbe, roleProbe, roleDifference_apply_self,
      roleDifference_apply_A, roleDifference_apply_ne, B_ne_A, C_ne_A, D_ne_A, B_ne_C, B_ne_D,
      C_ne_B, C_ne_D, D_ne_B, D_ne_C]

def probeMap : (Fin 3 → ℚ) →ₗ[ℚ] BalancedRole where
  toFun g :=
    g 0 • balancedRoleProbe 0 + g 1 • balancedRoleProbe 1 + g 2 • balancedRoleProbe 2
  map_add' g h := by ext; simp [add_mul, mul_add]; abel
  map_smul' c g := by
    ext r
    simp [smul_eq_mul, RingHom.id_apply]
    ring

theorem roleReadout_probeMap (g : Fin 3 → ℚ) :
    roleReadout (probeMap g) = g := by
  ext i
  fin_cases i
  · simp [probeMap, roleReadout, roleCoord, balancedRoleProbe, roleProbe, smul_eq_mul,
      roleDifference_apply_self B_ne_A, roleDifference_apply_ne B_ne_C B_ne_A,
      roleDifference_apply_ne B_ne_D B_ne_A]
  · simp [probeMap, roleReadout, roleCoord, balancedRoleProbe, roleProbe, smul_eq_mul,
      roleDifference_apply_ne C_ne_B C_ne_A, roleDifference_apply_self C_ne_A,
      roleDifference_apply_ne C_ne_D C_ne_A]
  · simp [probeMap, roleReadout, roleCoord, balancedRoleProbe, roleProbe, smul_eq_mul,
      roleDifference_apply_ne D_ne_B D_ne_A, roleDifference_apply_ne D_ne_C D_ne_A,
      roleDifference_apply_self D_ne_A]

theorem probeMap_roleReadout (f : BalancedRole) :
    probeMap (roleReadout f) = f := by
  apply Subtype.ext
  funext s
  have hsum : f.1 A + f.1 B + f.1 C + f.1 D = 0 := by
    have hzero : ∑ r, f.1 r = 0 := f.2
    rwa [role_sum_four] at hzero
  rcases s with ⟨a, b⟩
  fin_cases a <;> fin_cases b
  · simp [probeMap, roleReadout, roleCoord, balancedRoleProbe, roleProbe, smul_eq_mul,
      roleDifference, roleIndicator, A, B, C, D]
    have hcoord : f.1 (0, 0) + f.1 (1, 1) + f.1 (0, 1) + f.1 (1, 0) = 0 := by
      simpa [A, B, C, D] using hsum
    linarith
  · simp [probeMap, roleReadout, roleCoord, balancedRoleProbe, roleProbe, smul_eq_mul,
      roleDifference, roleIndicator, A, B, C, D]
  · simp [probeMap, roleReadout, roleCoord, balancedRoleProbe, roleProbe, smul_eq_mul,
      roleDifference, roleIndicator, A, B, C, D]
  · simp [probeMap, roleReadout, roleCoord, balancedRoleProbe, roleProbe, smul_eq_mul,
      roleDifference, roleIndicator, A, B, C, D]

theorem probeMap_bijective : Function.Bijective probeMap :=
  ⟨fun g h hgh => by
      have := congrArg roleReadout hgh
      simpa [roleReadout_probeMap] using this,
    fun f => ⟨roleReadout f, probeMap_roleReadout f⟩⟩

theorem balancedRole_probe_balanced (i : Fin 3) :
    ∑ r, (balancedRoleProbe i).1 r = 0 :=
  (balancedRoleProbe i).2

theorem probeMap_indicator (i : Fin 3) :
    probeMap (fun j => if j = i then 1 else 0) = balancedRoleProbe i := by
  simpa [roleReadout_probe] using probeMap_roleReadout (balancedRoleProbe i)

theorem balancedRole_probe_independent :
    LinearIndependent ℚ balancedRoleProbe := by
  have hstd : LinearIndependent ℚ (Pi.basisFun ℚ (Fin 3)) :=
    (Pi.basisFun ℚ (Fin 3)).linearIndependent
  have hmap := hstd.map' probeMap (LinearMap.ker_eq_bot.mpr probeMap_bijective.1)
  have hfam : (fun i => probeMap ((Pi.basisFun ℚ (Fin 3)) i)) = balancedRoleProbe := by
    funext i
    have hsingle : (fun j => if j = i then (1 : ℚ) else 0) = Pi.single i 1 := by
      funext j
      simp [Pi.single_apply]
    rw [Pi.basisFun_apply, ← hsingle]
    exact probeMap_indicator i
  exact hfam ▸ hmap

theorem balancedRole_probe_span :
    Submodule.span ℚ (Set.range balancedRoleProbe) = ⊤ := by
  ext f
  simp only [Submodule.mem_top, iff_true]
  rw [← probeMap_roleReadout f]
  change ((roleReadout f) 0 • balancedRoleProbe 0 +
      (roleReadout f) 1 • balancedRoleProbe 1 +
      (roleReadout f) 2 • balancedRoleProbe 2) ∈ _
  refine Submodule.add_mem _ (Submodule.add_mem _
      (Submodule.smul_mem _ _ (Submodule.subset_span ⟨0, rfl⟩))
      (Submodule.smul_mem _ _ (Submodule.subset_span ⟨1, rfl⟩)))
    (Submodule.smul_mem _ _ (Submodule.subset_span ⟨2, rfl⟩))

noncomputable def balancedRole_basis : Module.Basis (Fin 3) ℚ BalancedRole :=
  Module.Basis.mk balancedRole_probe_independent balancedRole_probe_span.ge

theorem balancedRole_basis_apply (i : Fin 3) :
    balancedRole_basis i = balancedRoleProbe i := by
  simp [balancedRole_basis, Module.Basis.coe_mk]

/-! ## Structured Fin bridge -/

/-- A cardinality equivalence that records the images of the three typed summands. -/
structure StructuredTypedSceneBridge where
  toFin9 : V9 ≃ Fin 9
  toFin11 : V11 ≃ Fin 11
  toFin13 : V13 ≃ Fin 13
  omega8Summand : Set (Fin 9)
  dyadSummand : Set (Fin 11)
  roleSummand : Set (Fin 13)
  omega8_carried : omega8Summand = Set.range (fun x : Omega8 => toFin9 (Sum.inl x))
  dyad_carried : dyadSummand = Set.range (fun d : Dyad => toFin11 (Sum.inr d))
  role_carried : roleSummand = Set.range (fun r : Role => toFin13 (Sum.inr r))

def roleLandingEquiv : D0.V13 ≃ Fin 13 where
  toFun := typedZone13Equiv
  invFun := typedZone13Equiv.symm
  left_inv := typedZone13Equiv.left_inv
  right_inv := typedZone13Equiv.right_inv

def roleLandingSwap : D0.V13 ≃ Fin 13 :=
  roleLandingEquiv.trans (Equiv.swap (8 : Fin 13) 9)

theorem roleLandingEquiv_A : roleLandingEquiv (Sum.inr A) = (9 : Fin 13) := by
  simp [roleLandingEquiv, typedZone13Equiv, typedZone13Index, A]

theorem roleLandingSwap_A : roleLandingSwap (Sum.inr A) = (8 : Fin 13) := by
  simp [roleLandingSwap, roleLandingEquiv, typedZone13Equiv, typedZone13Index, A,
    Equiv.swap_apply_right]

theorem eight_not_in_roleLanding
    (h : (8 : Fin 13) ∈ Set.range (fun r : Role => roleLandingEquiv (Sum.inr r))) : False := by
  rcases h with ⟨r, hr⟩
  rcases r with ⟨a, b⟩
  fin_cases a <;> fin_cases b <;>
    simp [roleLandingEquiv, typedZone13Equiv, typedZone13Index] at hr

/-- Two cardinality equivalences can send the Role summand to different
4-subsets of `Fin 13`. -/
theorem roleSummand_landing_not_forced_by_cardinality :
    ∃ e₁ e₂ : V13 ≃ Fin 13,
      Set.range (fun r : Role => e₁ (Sum.inr r)) ≠
        Set.range (fun r : Role => e₂ (Sum.inr r)) := by
  refine ⟨roleLandingEquiv, roleLandingSwap, ?_⟩
  intro hrange
  apply eight_not_in_roleLanding
  rw [hrange]
  exact ⟨A, roleLandingSwap_A⟩

def transportZoneFun {α β : Type} (e : α ≃ β) (g : α → ℚ) : β → ℚ :=
  fun i => g (e.symm i)

def transportTypedEdge (e9 : V9 ≃ Fin 9) (e11 : V11 ≃ Fin 11) (e13 : V13 ≃ Fin 13) :
    TypedSceneEdge ≃ Edge (Fin 9) (Fin 11) (Fin 13) where
  toFun
    | Sum.inl (a, b) => Sum.inl (e9 a, e11 b)
    | Sum.inr (Sum.inl (a, c)) => Sum.inr (Sum.inl (e9 a, e13 c))
    | Sum.inr (Sum.inr (b, c)) => Sum.inr (Sum.inr (e11 b, e13 c))
  invFun
    | Sum.inl (a, b) => Sum.inl (e9.symm a, e11.symm b)
    | Sum.inr (Sum.inl (a, c)) => Sum.inr (Sum.inl (e9.symm a, e13.symm c))
    | Sum.inr (Sum.inr (b, c)) => Sum.inr (Sum.inr (e11.symm b, e13.symm c))
  left_inv e := by
    rcases e with ab | ac | bc <;> simp
  right_inv e := by
    rcases e with ab | ac | bc <;> simp

/-- Along a structured bridge, the typed Role cut is the raw `Fin` cut of the
pushed Role extension, supported on the bridge's Role image. -/
theorem structuredBridge_transports_roleCut
    (B : StructuredTypedSceneBridge) (f : BalancedRole) :
    oppositeCutGamma (α := Fin 9) (β := Fin 11)
        (transportZoneFun B.toFin13 (extendRoleToV13 f.1)) =
      fun e =>
        typedRoleOppositeCut f
          ((transportTypedEdge B.toFin9 B.toFin11 B.toFin13).symm e) := by
  funext e
  rcases e with ab | ac | bc
  · simp [oppositeCutGamma, typedRoleOppositeCut_apply, transportTypedEdge]
  · rcases ac with ⟨i, k⟩
    simp [oppositeCutGamma, typedRoleOppositeCut_apply, transportTypedEdge, transportZoneFun,
      Fintype.card_fin, card_v11]
  · rcases bc with ⟨j, k⟩
    simp [oppositeCutGamma, typedRoleOppositeCut_apply, transportTypedEdge, transportZoneFun,
      Fintype.card_fin, card_v9]

theorem structuredBridge_role_extension_supported
    (B : StructuredTypedSceneBridge) (f : Role → ℚ) {i : Fin 13}
    (hi : i ∉ B.roleSummand) :
    transportZoneFun B.toFin13 (extendRoleToV13 f) i = 0 := by
  simp only [transportZoneFun]
  cases hpre : B.toFin13.symm i with
  | inl v =>
      simp [extendRoleToV13, extendInrLin, hpre]
  | inr r =>
      have hmem : i ∈ B.roleSummand := by
        rw [B.role_carried]
        refine ⟨r, ?_⟩
        have happly := B.toFin13.apply_symm_apply i
        rw [hpre] at happly
        exact happly
      exact absurd hmem hi

/-! ## Orientation is a different action -/

theorem role_summand_perm_ne_orientation_flip :
    (⇑(permuteV13RoleSummand (Equiv.swap A B)) : V13 → V13) ≠ flipV13 := by
  intro h
  have hpt := congrFun h (Sum.inr A)
  have hswap : (Equiv.swap A B) A = B := by
    exact Equiv.swap_apply_left (a := A) (b := B)
  simp [permuteV13RoleSummand, flipV13, hswap] at hpt
  exact B_ne_A hpt

theorem role_summand_perm_commutes_orientation (σ : Equiv.Perm Role) (v : V13) :
    flipV13 (permuteV13RoleSummand σ v) = permuteV13RoleSummand σ (flipV13 v) := by
  cases v with
  | inl x => simp [permuteV13RoleSummand, flipV13]
  | inr r => simp [permuteV13RoleSummand, flipV13]

end D0.Representation.TypedRoleSceneAction
