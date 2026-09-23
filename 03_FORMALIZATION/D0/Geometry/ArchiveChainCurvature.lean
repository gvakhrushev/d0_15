import Mathlib.Algebra.Module.Equiv.Basic
import Mathlib.Tactic
import D0.Geometry.ArchiveChainConnection

/-!
# Open-path curvature of a finite link connection

`squarePathA` and `squarePathB` are the two transports from `x+r+s` to `x`.
`openCurvature` is their difference. It changes the fibre endpoint.
`basedHolonomy` is the based endomorphism `A B⁻¹`.

Flat unit links have vanishing plaquette curvature. That fact is not a
centered-Cartan closure statement.
-/

namespace D0.Geometry

open D0

variable {N : ℕ} {K V : Type*} [Field K] [AddCommGroup V] [Module K V]

def squarePathA (U : LinkConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : V ≃ₗ[K] V :=
  (U (roleTranslatePlus N r x) s).trans (U x r)

def squarePathB (U : LinkConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : V ≃ₗ[K] V :=
  (U (roleTranslatePlus N s x) r).trans (U x s)

/-- Open-path defect `F_rs(x) : V_{x+r+s} → V_x`. -/
def openCurvature (U : LinkConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : V →ₗ[K] V :=
  (squarePathA U r s x).toLinearMap - (squarePathB U r s x).toLinearMap

/-- Based holonomy `P_rs(x) = A_rs(x) ∘ B_rs(x)⁻¹ : V_x → V_x`. -/
def basedHolonomy (U : LinkConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) : V ≃ₗ[K] V :=
  (squarePathB U r s x).symm.trans (squarePathA U r s x)

theorem roleTranslate_comm (r s : Role) (x : ArchiveRolePhaseGroup N) :
    roleTranslatePlus N s (roleTranslatePlus N r x) =
      roleTranslatePlus N r (roleTranslatePlus N s x) := by
  simp only [roleTranslatePlus_apply]
  abel

theorem transport_commutator_apply (U : LinkConnection N K V) (r s : Role)
    (ψ : CoefficientSection N V) (x : ArchiveRolePhaseGroup N) :
    linkTransport U r (linkTransport U s ψ) x -
        linkTransport U s (linkTransport U r ψ) x =
      openCurvature U r s x
        (ψ (roleTranslatePlus N s (roleTranslatePlus N r x))) := by
  simp only [linkTransport, openCurvature, squarePathA, squarePathB,
    LinearEquiv.trans_apply, LinearMap.sub_apply, LinearEquiv.coe_toLinearMap,
    roleTranslate_comm]

theorem squarePathA_gauge (g : NodeGauge N K V) (U : LinkConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    squarePathA (fun y t => gaugeLink g U y t) r s x =
      ((g (roleTranslatePlus N s (roleTranslatePlus N r x))).symm.trans
        (squarePathA U r s x)).trans (g x) := by
  simp only [squarePathA, gaugeLink]
  have hcomm :
      roleTranslatePlus N s (roleTranslatePlus N r x) =
        roleTranslatePlus N r (roleTranslatePlus N s x) :=
    roleTranslate_comm r s x
  simp only [hcomm]
  ext v
  simp only [LinearEquiv.trans_apply, LinearEquiv.symm_apply_apply]

theorem squarePathB_gauge (g : NodeGauge N K V) (U : LinkConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    squarePathB (fun y t => gaugeLink g U y t) r s x =
      ((g (roleTranslatePlus N r (roleTranslatePlus N s x))).symm.trans
        (squarePathB U r s x)).trans (g x) := by
  simp only [squarePathB, gaugeLink]
  have hcomm :
      roleTranslatePlus N r (roleTranslatePlus N s x) =
        roleTranslatePlus N s (roleTranslatePlus N r x) :=
    (roleTranslate_comm r s x).symm
  simp only [hcomm]
  ext v
  simp only [LinearEquiv.trans_apply, LinearEquiv.symm_apply_apply]

theorem curvature_gauge (g : NodeGauge N K V) (U : LinkConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    openCurvature (fun y t => gaugeLink g U y t) r s x =
      (g x).toLinearMap.comp
        ((openCurvature U r s x).comp
          (g (roleTranslatePlus N s (roleTranslatePlus N r x))).symm.toLinearMap) := by
  ext v
  simp only [openCurvature, LinearMap.sub_apply, LinearMap.comp_apply,
    LinearEquiv.coe_toLinearMap, squarePathA_gauge, squarePathB_gauge,
    LinearEquiv.trans_apply, roleTranslate_comm, map_sub]

theorem basedHolonomy_gauge (g : NodeGauge N K V) (U : LinkConnection N K V)
    (r s : Role) (x : ArchiveRolePhaseGroup N) :
    basedHolonomy (fun y t => gaugeLink g U y t) r s x =
      ((g x).symm.trans (basedHolonomy U r s x)).trans (g x) := by
  ext v
  simp only [basedHolonomy, squarePathA_gauge, squarePathB_gauge, LinearEquiv.trans_apply,
    LinearEquiv.symm_trans_apply, LinearEquiv.symm_symm, roleTranslate_comm,
    LinearEquiv.symm_apply_apply]

theorem curvature_eq_holonomy_defect (U : LinkConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    openCurvature U r s x =
      ((basedHolonomy U r s x).toLinearMap - LinearMap.id).comp
        (squarePathB U r s x).toLinearMap := by
  ext v
  simp only [openCurvature, basedHolonomy, LinearMap.sub_apply, LinearMap.comp_apply,
    LinearMap.id_apply, LinearEquiv.coe_toLinearMap, LinearEquiv.trans_apply,
    LinearEquiv.symm_apply_apply]

theorem curvature_swap (U : LinkConnection N K V) (r s : Role)
    (x : ArchiveRolePhaseGroup N) :
    openCurvature U s r x = -openCurvature U r s x := by
  simp only [openCurvature, squarePathA, squarePathB]
  abel

def trivialLink (N : ℕ) (K V : Type*) [Field K] [AddCommGroup V] [Module K V] :
    LinkConnection N K V :=
  fun _ _ => LinearEquiv.refl K V

theorem trivialLink_squarePathA_refl (r s : Role) (x : ArchiveRolePhaseGroup N) :
    squarePathA (trivialLink N K V) r s x = LinearEquiv.refl K V := by
  simp [squarePathA, trivialLink]

theorem trivialLink_curvature_zero (r s : Role) (x : ArchiveRolePhaseGroup N) :
    openCurvature (trivialLink N K V) r s x = 0 := by
  ext v
  simp [openCurvature, squarePathA, squarePathB, trivialLink]

/-- At period 2 the plaquette in one repeated direction multiplies the two
independent oriented slots and returns to the base. -/
theorem period_two_square_uses_both_slots
    (hL : archiveFibers N = 2) (U : LinkConnection N K V) (r : Role)
    (x : ArchiveRolePhaseGroup N) :
    squarePathA U r r x =
      (U (roleTranslatePlus N r x) r).trans (U x r) ∧
      roleTranslatePlus N r (roleTranslatePlus N r x) = x := by
  exact ⟨rfl, period_two_double_step hL r x⟩

/-! ## Nonabelian 2×2 witness

Constant links valued in two noncommuting shears have a nonzero open-path defect.
-/

def shearA (v : Fin 2 → ℚ) : Fin 2 → ℚ :=
  fun i => if i = 0 then v 0 + v 1 else v 1

def shearAInv (v : Fin 2 → ℚ) : Fin 2 → ℚ :=
  fun i => if i = 0 then v 0 - v 1 else v 1

def shearB (v : Fin 2 → ℚ) : Fin 2 → ℚ :=
  fun i => if i = 0 then v 0 else v 0 + v 1

def shearBInv (v : Fin 2 → ℚ) : Fin 2 → ℚ :=
  fun i => if i = 0 then v 0 else v 1 - v 0

theorem shearA_left_inv (v : Fin 2 → ℚ) : shearA (shearAInv v) = v := by
  funext i
  fin_cases i <;> simp [shearA, shearAInv]

theorem shearA_right_inv (v : Fin 2 → ℚ) : shearAInv (shearA v) = v := by
  funext i
  fin_cases i <;> simp [shearA, shearAInv]

theorem shearB_left_inv (v : Fin 2 → ℚ) : shearB (shearBInv v) = v := by
  funext i
  fin_cases i <;> simp [shearB, shearBInv]

theorem shearB_right_inv (v : Fin 2 → ℚ) : shearBInv (shearB v) = v := by
  funext i
  fin_cases i <;> simp [shearB, shearBInv]

noncomputable def shearAEquiv : (Fin 2 → ℚ) ≃ₗ[ℚ] (Fin 2 → ℚ) :=
  LinearEquiv.ofLinear
    { toFun := shearA, map_add' := by intro a b; funext i; fin_cases i <;> simp [shearA]; ring,
      map_smul' := by intro c a; funext i; fin_cases i <;> simp [shearA, smul_eq_mul]; ring }
    { toFun := shearAInv, map_add' := by intro a b; funext i; fin_cases i <;> simp [shearAInv]; ring,
      map_smul' := by intro c a; funext i; fin_cases i <;> simp [shearAInv, smul_eq_mul]; ring }
    (by
      refine LinearMap.ext ?_
      intro v
      simpa [LinearMap.comp_apply] using shearA_left_inv v)
    (by
      refine LinearMap.ext ?_
      intro v
      simpa [LinearMap.comp_apply] using shearA_right_inv v)

noncomputable def shearBEquiv : (Fin 2 → ℚ) ≃ₗ[ℚ] (Fin 2 → ℚ) :=
  LinearEquiv.ofLinear
    { toFun := shearB, map_add' := by intro a b; funext i; fin_cases i <;> simp [shearB]; ring,
      map_smul' := by intro c a; funext i; fin_cases i <;> simp [shearB, smul_eq_mul]; ring }
    { toFun := shearBInv, map_add' := by intro a b; funext i; fin_cases i <;> simp [shearBInv]; ring,
      map_smul' := by intro c a; funext i; fin_cases i <;> simp [shearBInv, smul_eq_mul]; ring }
    (by
      refine LinearMap.ext ?_
      intro v
      simpa [LinearMap.comp_apply] using shearB_left_inv v)
    (by
      refine LinearMap.ext ?_
      intro v
      simpa [LinearMap.comp_apply] using shearB_right_inv v)

noncomputable def nonabelianLink (N : ℕ) : LinkConnection N ℚ (Fin 2 → ℚ) :=
  fun _ r =>
    if r = D0.A then shearAEquiv
    else if r = D0.B then shearBEquiv
    else LinearEquiv.refl ℚ (Fin 2 → ℚ)

theorem nonabelian_curvature_nonzero (N : ℕ) (x : ArchiveRolePhaseGroup N) :
    openCurvature (nonabelianLink N) D0.A D0.B x ≠ 0 := by
  intro h
  have hAB : D0.A ≠ D0.B := by decide
  let e0 : Fin 2 → ℚ := fun i => if i = 0 then 1 else 0
  have hA : nonabelianLink N x D0.A = shearAEquiv := by
    simp [nonabelianLink]
  have hB : nonabelianLink N x D0.B = shearBEquiv := by
    simp only [nonabelianLink]
    rw [if_neg (Ne.symm hAB), if_true]
  have hAs : nonabelianLink N (roleTranslatePlus N D0.A x) D0.B = shearBEquiv := by
    simp only [nonabelianLink]
    rw [if_neg (Ne.symm hAB), if_true]
  have hBs : nonabelianLink N (roleTranslatePlus N D0.B x) D0.A = shearAEquiv := by
    simp [nonabelianLink]
  have hvec := congrFun (congrArg DFunLike.coe h) e0
  simp only [openCurvature, LinearMap.sub_apply, LinearEquiv.coe_toLinearMap, LinearMap.zero_apply,
    squarePathA, squarePathB, LinearEquiv.trans_apply, hA, hB, hAs, hBs,
    shearAEquiv, shearBEquiv, LinearEquiv.ofLinear_apply] at hvec
  have h0 := congrFun hvec 0
  simp [shearA, shearB, e0] at h0

end D0.Geometry
