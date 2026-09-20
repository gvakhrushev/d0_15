import D0.Geometry.SceneCochainComplex
import D0.Topology.GenericTripartiteFirstHomologyRing
import Mathlib.LinearAlgebra.Matrix.Rank
import Mathlib.Tactic

/-!
# C1 — typed common carrier for the literal `K(9,11,13)` scene

This file keeps the unsigned A1 endpoint-sum operator and the signed
transitive incidence/current-divergence operator on the same literal edge
carrier.  The local symmetry is the product of independent within-zone
permutations.  Its edge action is pullback along the induced permutation of
`SceneEdge`; no second edge carrier is introduced.

The semantic firewall is intentional: `BPlus` is the unsigned A1
Weyl/Ward endpoint-sum operator, while `BMinus` is the signed current
 divergence.  This file does not import any TT wave/dynamics module.
-/

namespace D0.Geometry.SignlessSignedCommonCarrier

open BigOperators Matrix
open D0.Geometry.SceneCochainComplex

abbrev V9T := Fin 9
abbrev V11T := Fin 11
abbrev V13T := Fin 13

/-- Independent within-zone relabellings; zones are not mixed. -/
abbrev LocalRelabelling :=
  Equiv.Perm V9T × Equiv.Perm V11T × Equiv.Perm V13T

/-- The induced relabelling of the literal edge carrier.

The three summands are respectively `(9,11)`, `(9,13)`, and `(11,13)`.
-/
def edgeRelabel (h : LocalRelabelling) : SceneEdge → SceneEdge
  | Sum.inl (x, y) => Sum.inl (h.1 x, h.2.1 y)
  | Sum.inr (Sum.inl (x, z)) => Sum.inr (Sum.inl (h.1 x, h.2.2 z))
  | Sum.inr (Sum.inr (y, z)) => Sum.inr (Sum.inr (h.2.1 y, h.2.2 z))

/-- The induced relabelling of the literal vertex carrier. -/
def vertexRelabel (h : LocalRelabelling) : SceneVertex → SceneVertex
  | Sum.inl x => Sum.inl (h.1 x)
  | Sum.inr (Sum.inl y) => Sum.inr (Sum.inl (h.2.1 y))
  | Sum.inr (Sum.inr z) => Sum.inr (Sum.inr (h.2.2 z))

/-- Inverse of a product relabelling, componentwise. -/
def localRelabellingInv (h : LocalRelabelling) : LocalRelabelling :=
  (h.1.symm, (h.2.1.symm, h.2.2.symm))

/-- Pullback action on `SceneC1 = SceneEdge → ℚ`, written componentwise.
The inverse permutations occur because this is a pullback action. -/
def sceneAction (h : LocalRelabelling) (X : SceneC1) : SceneC1
  | Sum.inl (x, y) => X (Sum.inl (h.1.symm x, h.2.1.symm y))
  | Sum.inr (Sum.inl (x, z)) =>
      X (Sum.inr (Sum.inl (h.1.symm x, h.2.2.symm z)))
  | Sum.inr (Sum.inr (y, z)) =>
      X (Sum.inr (Sum.inr (h.2.1.symm y, h.2.2.symm z)))

/-- Pullback action on vertex fields, used for the codomain of `BPlus/BMinus`. -/
def vertexAction (h : LocalRelabelling) (A : SceneC0) : SceneC0
  | Sum.inl x => A (Sum.inl (h.1.symm x))
  | Sum.inr (Sum.inl y) => A (Sum.inr (Sum.inl (h.2.1.symm y)))
  | Sum.inr (Sum.inr z) => A (Sum.inr (Sum.inr (h.2.2.symm z)))

/-- Literal unsigned A1 Weyl/Ward endpoint-sum operator. -/
def BPlus (X : SceneC1) : SceneC0 := fun v =>
  match v with
  | Sum.inl x =>
      (∑ y : V11T, X (Sum.inl (x, y))) +
        ∑ z : V13T, X (Sum.inr (Sum.inl (x, z)))
  | Sum.inr (Sum.inl y) =>
      (∑ x : V9T, X (Sum.inl (x, y))) +
        ∑ z : V13T, X (Sum.inr (Sum.inr (y, z)))
  | Sum.inr (Sum.inr z) =>
      (∑ x : V9T, X (Sum.inr (Sum.inl (x, z)))) +
        ∑ y : V11T, X (Sum.inr (Sum.inr (y, z)))

/-- Literal signed incidence/current divergence for `9 → 11 → 13`.

This is the signed endpoint divergence; it is not `BPlus`.
-/
def BMinus (X : SceneC1) : SceneC0 := fun v =>
  match v with
  | Sum.inl x =>
      -(∑ y : V11T, X (Sum.inl (x, y))) -
        ∑ z : V13T, X (Sum.inr (Sum.inl (x, z)))
  | Sum.inr (Sum.inl y) =>
      (∑ x : V9T, X (Sum.inl (x, y))) -
        ∑ z : V13T, X (Sum.inr (Sum.inr (y, z)))
  | Sum.inr (Sum.inr z) =>
      (∑ x : V9T, X (Sum.inr (Sum.inl (x, z)))) +
        ∑ y : V11T, X (Sum.inr (Sum.inr (y, z)))

/-- Reindexing an indicator sum over the first coordinate. -/
private theorem sum_indicator_fst_one {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] (f : α × β → ℚ) (a : α) :
    (∑ x : α × β, (if a = x.1 then (1 : ℚ) else 0) * f x) =
      ∑ b : β, f (a, b) := by
  rw [Fintype.sum_prod_type]
  calc
    (∑ x : α, ∑ y : β, (if a = x then (1 : ℚ) else 0) * f (x, y)) =
        ∑ x : α, if a = x then ∑ y : β, f (x, y) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases h : a = x <;> simp [h]
    _ = ∑ b : β, f (a, b) := by
      simpa using Fintype.sum_ite_eq a (fun x : α => ∑ y : β, f (x, y))

private theorem sum_indicator_fst_neg {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq α] (f : α × β → ℚ) (a : α) :
    (∑ x : α × β, (if a = x.1 then (-1 : ℚ) else 0) * f x) =
      -(∑ b : β, f (a, b)) := by
  rw [Fintype.sum_prod_type]
  calc
    (∑ x : α, ∑ y : β, (if a = x then (-1 : ℚ) else 0) * f (x, y)) =
        ∑ x : α, if a = x then -(∑ y : β, f (x, y)) else 0 := by
      apply Fintype.sum_congr
      intro x
      by_cases h : a = x <;> simp [h]
    _ = -(∑ b : β, f (a, b)) := by
      simpa using Fintype.sum_ite_eq a
        (fun x : α => -(∑ y : β, f (x, y)))

private theorem sum_indicator_snd_one {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq β] (f : α × β → ℚ) (b : β) :
    (∑ x : α × β, (if b = x.2 then (1 : ℚ) else 0) * f x) =
      ∑ a : α, f (a, b) := by
  rw [Fintype.sum_prod_type]
  apply Fintype.sum_congr
  intro a
  simpa using Fintype.sum_ite_eq b (fun y : β => f (a, y))

private theorem sum_indicator_snd_neg {α β : Type} [Fintype α] [Fintype β]
    [DecidableEq β] (f : α × β → ℚ) (b : β) :
    (∑ x : α × β, (if b = x.2 then (-1 : ℚ) else 0) * f x) =
      -(∑ a : α, f (a, b)) := by
  calc
    (∑ x : α × β, (if b = x.2 then (-1 : ℚ) else 0) * f x) =
        -(∑ x : α × β, (if b = x.2 then (1 : ℚ) else 0) * f x) := by
      rw [← Finset.sum_neg_distrib]
      apply Finset.sum_congr rfl
      intro x hx
      by_cases h : b = x.2 <;> simp [h]
    _ = -(∑ a : α, f (a, b)) := by rw [sum_indicator_snd_one]

/-- The signed formula is exactly the literal oriented incidence owner. -/
theorem BMinus_eq_sceneBoundary1_mulVec (X : SceneC1) :
    BMinus X = sceneBoundary1.mulVec X := by
  funext v
  rcases v with x | yz
  · simp only [BMinus, Matrix.mulVec, dotProduct, sceneBoundary1,
      D0.Topology.GenericTripartiteHomology.boundary1,
      Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
      add_zero, zero_add]
    rw [sum_indicator_fst_neg, sum_indicator_fst_neg]
    ring
  · rcases yz with y | z
    · simp only [BMinus, Matrix.mulVec, dotProduct, sceneBoundary1,
        D0.Topology.GenericTripartiteHomology.boundary1,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_fst_neg]
      ring
    · simp only [BMinus, Matrix.mulVec, dotProduct, sceneBoundary1,
        D0.Topology.GenericTripartiteHomology.boundary1,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_snd_one]

/-- The signed operator is exposed as a genuine linear map. -/
def BMinusLin : SceneC1 →ₗ[ℚ] SceneC0 := sceneBoundary1.mulVecLin

theorem BMinusLin_apply (X : SceneC1) : BMinusLin X = BMinus X := by
  rw [BMinus_eq_sceneBoundary1_mulVec]
  rfl

/-- A generic finite-sum pullback fact used by the equivariance proofs. -/
private theorem sum_comp_perm {α : Type} [Fintype α]
    (σ : Equiv.Perm α) (f : α → ℚ) :
    (∑ x : α, f (σ x)) = ∑ x : α, f x := by
  simpa using (Equiv.sum_comp σ f)

/-- `BPlus` respects local relabelling. -/
theorem BPlus_equivariant (h : LocalRelabelling) (X : SceneC1) :
    BPlus (sceneAction h X) = vertexAction h (BPlus X) := by
  funext v
  rcases v with x | yz
  · simp only [BPlus, sceneAction, vertexAction]
    congr 1
    · exact Equiv.sum_comp h.2.1.symm
        (fun y : V11T => X (Sum.inl (h.1.symm x, y)))
    · exact Equiv.sum_comp h.2.2.symm
        (fun z : V13T => X (Sum.inr (Sum.inl (h.1.symm x, z))))
  · rcases yz with y | z
    · simp only [BPlus, sceneAction, vertexAction]
      congr 1
      · exact Equiv.sum_comp h.1.symm
          (fun x : V9T => X (Sum.inl (x, h.2.1.symm y)))
      · exact Equiv.sum_comp h.2.2.symm
          (fun z : V13T => X (Sum.inr (Sum.inr (h.2.1.symm y, z))))
    · simp only [BPlus, sceneAction, vertexAction]
      congr 1
      · exact Equiv.sum_comp h.1.symm
          (fun x : V9T => X (Sum.inr (Sum.inl (x, h.2.2.symm z))))
      · exact Equiv.sum_comp h.2.1.symm
          (fun y : V11T => X (Sum.inr (Sum.inr (y, h.2.2.symm z))))

/-- `BMinus` respects local relabelling. -/
theorem BMinus_equivariant (h : LocalRelabelling) (X : SceneC1) :
    BMinus (sceneAction h X) = vertexAction h (BMinus X) := by
  funext v
  rcases v with x | yz
  · simp only [BMinus, sceneAction, vertexAction]
    congr 1
    · congr 1
      exact Equiv.sum_comp h.2.1.symm
        (fun y : V11T => X (Sum.inl (h.1.symm x, y)))
    · exact Equiv.sum_comp h.2.2.symm
        (fun z : V13T => X (Sum.inr (Sum.inl (h.1.symm x, z))))
  · rcases yz with y | z
    · simp only [BMinus, sceneAction, vertexAction]
      congr 1
      · exact Equiv.sum_comp h.1.symm
          (fun x : V9T => X (Sum.inl (x, h.2.1.symm y)))
      · exact Equiv.sum_comp h.2.2.symm
          (fun z : V13T => X (Sum.inr (Sum.inr (h.2.1.symm y, z))))
    · simp only [BMinus, sceneAction, vertexAction]
      congr 1
      · exact Equiv.sum_comp h.1.symm
          (fun x : V9T => X (Sum.inr (Sum.inl (x, h.2.2.symm z))))
      · exact Equiv.sum_comp h.2.1.symm
          (fun y : V11T => X (Sum.inr (Sum.inr (y, h.2.2.symm z))))

/-- The explicit C1 carrier map.  On `(11,13)` it subtracts the rank-one
row-centering correction `(2/13) C₁₁ X 1 1ᵀ`; on the other blocks it is the
identity. -/
def U (X : SceneC1) : SceneC1 := fun e =>
  match e with
  | Sum.inl _ => X e
  | Sum.inr (Sum.inl _) => X e
  | Sum.inr (Sum.inr (y, _)) =>
      X e - (2 / 13 : ℚ) *
        ((∑ z' : V13T, X (Sum.inr (Sum.inr (y, z')))) -
          (1 / 11 : ℚ) *
            ∑ y' : V11T, ∑ z' : V13T,
              X (Sum.inr (Sum.inr (y', z'))))

/-- The correction used by `U` is natural under independent relabelling. -/
theorem U_equivariant (h : LocalRelabelling) (X : SceneC1) :
    U (sceneAction h X) = sceneAction h (U X) := by
  funext e
  rcases e with e | e
  · rfl
  · rcases e with e | e
    · rfl
    · rcases e with ⟨y, z⟩
      simp only [U, sceneAction]
      congr 1
      congr 1
      congr 1
      · exact Equiv.sum_comp h.2.2.symm
          (fun z' : V13T => X (Sum.inr (Sum.inr (h.2.1.symm y, z'))))
      · congr 1
        have hinner : ∀ y' : V11T,
            (∑ z' : V13T, X (Sum.inr (Sum.inr (h.2.1.symm y', h.2.2.symm z')))) =
            ∑ z' : V13T, X (Sum.inr (Sum.inr (h.2.1.symm y', z'))) := by
          intro y'
          exact Equiv.sum_comp h.2.2.symm
            (fun z' : V13T => X (Sum.inr (Sum.inr (h.2.1.symm y', z'))))
        have hsum : (∑ y' : V11T, ∑ z' : V13T,
            X (Sum.inr (Sum.inr (h.2.1.symm y', h.2.2.symm z')))) =
            ∑ y' : V11T, ∑ z' : V13T, X (Sum.inr (Sum.inr (h.2.1.symm y', z'))) := by
          refine Fintype.sum_congr _ _ hinner
        rw [hsum]
        exact Equiv.sum_comp h.2.1.symm
          (fun y' : V11T => ∑ z' : V13T, X (Sum.inr (Sum.inr (y', z'))))

/-- Rank of the actual signed linear owner. -/
theorem BMinus_rank : Matrix.rank sceneBoundary1 = 32 := scene_boundary_ranks.1

theorem BMinusLin_rank :
    Module.finrank ℚ (LinearMap.range BMinusLin) = 32 := by
  simpa [BMinusLin, Matrix.rank] using BMinus_rank

/-- Kernel dimension of the actual signed linear owner. -/
theorem BMinus_kernel_finrank :
    Module.finrank ℚ (LinearMap.ker BMinusLin) = 327 := by
  have h := LinearMap.finrank_range_add_finrank_ker BMinusLin
  have hdom : Module.finrank ℚ SceneC1 = 359 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.2.1
  rw [BMinusLin_rank, hdom] at h
  omega

/-- Matrix form of the unsigned A1 endpoint-sum operator. -/
def BPlusMatrix : Matrix SceneVertex SceneEdge ℚ
  | Sum.inl x, Sum.inl (x', _) => if x = x' then 1 else 0
  | Sum.inl x, Sum.inr (Sum.inl (x', _)) => if x = x' then 1 else 0
  | Sum.inl _, Sum.inr (Sum.inr _) => 0
  | Sum.inr (Sum.inl y), Sum.inl (_, y') => if y = y' then 1 else 0
  | Sum.inr (Sum.inl y), Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inl y), Sum.inr (Sum.inr (y', _)) => if y = y' then 1 else 0
  | Sum.inr (Sum.inr _), Sum.inl _ => 0
  | Sum.inr (Sum.inr z), Sum.inr (Sum.inl (_, z')) => if z = z' then 1 else 0
  | Sum.inr (Sum.inr z), Sum.inr (Sum.inr (_, z')) => if z = z' then 1 else 0

def BPlusLin : SceneC1 →ₗ[ℚ] SceneC0 := BPlusMatrix.mulVecLin

theorem BPlusMatrix_mulVec_eq (X : SceneC1) :
    BPlusMatrix.mulVec X = BPlus X := by
  funext v
  rcases v with x | yz
  · simp only [BPlus, Matrix.mulVec, dotProduct, BPlusMatrix,
      Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
      add_zero, zero_add]
    rw [sum_indicator_fst_one, sum_indicator_fst_one]
  · rcases yz with y | z
    · simp only [BPlus, Matrix.mulVec, dotProduct, BPlusMatrix,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_fst_one]
    · simp only [BPlus, Matrix.mulVec, dotProduct, BPlusMatrix,
        Fintype.sum_sum_type, zero_mul, Finset.sum_const_zero,
        add_zero, zero_add]
      rw [sum_indicator_snd_one, sum_indicator_snd_one]

theorem BPlusLin_apply (X : SceneC1) : BPlusLin X = BPlus X := by
  change BPlusMatrix.mulVec X = BPlus X
  exact BPlusMatrix_mulVec_eq X

/-- The transpose of the signless map is injective on the literal scene. -/
theorem BPlus_transpose_injective :
    Function.Injective BPlusMatrix.transpose.mulVecLin := by
  rw [injective_iff_map_eq_zero]
  intro xi hxi
  funext v
  rcases v with x | yz
  · have hab := congrFun hxi (Sum.inl (x, (0 : V11T)))
    have hac := congrFun hxi (Sum.inr (Sum.inl (x, (0 : V13T))))
    have hbc := congrFun hxi (Sum.inr (Sum.inr ((0 : V11T), (0 : V13T))))
    rw [Matrix.mulVecLin_apply] at hab hac hbc
    simp only [Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix,
      Fintype.sum_sum_type, mul_ite, mul_one, mul_zero, zero_mul,
      Finset.sum_const_zero, add_zero, zero_add] at hab hac hbc
    linarith
  · rcases yz with y | z
    · have hab := congrFun hxi (Sum.inl ((0 : V9T), y))
      have hbc := congrFun hxi (Sum.inr (Sum.inr (y, (0 : V13T))))
      have hac := congrFun hxi (Sum.inr (Sum.inl ((0 : V9T), (0 : V13T))))
      rw [Matrix.mulVecLin_apply] at hab hbc hac
      simp only [Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix,
        Fintype.sum_sum_type, mul_ite, mul_one, mul_zero, zero_mul,
        Finset.sum_const_zero, add_zero, zero_add] at hab hbc hac
      linarith
    · have hac := congrFun hxi (Sum.inr (Sum.inl ((0 : V9T), z)))
      have hbc := congrFun hxi (Sum.inr (Sum.inr ((0 : V11T), z)))
      have hab := congrFun hxi (Sum.inl ((0 : V9T), (0 : V11T)))
      simp only [Matrix.mulVec, dotProduct, transpose_apply, BPlusMatrix,
        Fintype.sum_sum_type, mul_ite, mul_one, mul_zero, zero_mul,
        Finset.sum_const_zero, add_zero, zero_add] at hac hbc hab
      linarith

/-- The signless map has full row rank `33`. -/
theorem BPlus_rank : Matrix.rank BPlusMatrix = 33 := by
  have hker : LinearMap.ker BPlusMatrix.transpose.mulVecLin = ⊥ := by
    exact LinearMap.ker_eq_bot.mpr BPlus_transpose_injective
  have h := LinearMap.finrank_range_add_finrank_ker BPlusMatrix.transpose.mulVecLin
  have hdom : Module.finrank ℚ SceneC0 = 33 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.1
  have hrange : Module.finrank ℚ (LinearMap.range BPlusMatrix.transpose.mulVecLin) = 33 := by
    rw [hker] at h
    simpa [hdom] using h
  simpa [Matrix.rank, Matrix.rank_transpose] using hrange

/-- The actual unsigned linear owner has kernel dimension `326`. -/
theorem BPlus_kernel_finrank :
    Module.finrank ℚ (LinearMap.ker BPlusLin) = 326 := by
  have h := LinearMap.finrank_range_add_finrank_ker BPlusLin
  have hdom : Module.finrank ℚ SceneC1 = 359 := by
    rw [Module.finrank_fintype_fun_eq_card]
    exact scene_carrier_cardinalities.2.1
  have hrange : Module.finrank ℚ (LinearMap.range BPlusLin) = 33 := by
    simpa [BPlusLin, Matrix.rank] using BPlus_rank
  rw [hrange, hdom] at h
  omega

/-- The block-constant signed cycle mode. -/
def omega : SceneC1 := fun e =>
  match e with
  | Sum.inl _ => 13
  | Sum.inr (Sum.inl _) => -11
  | Sum.inr (Sum.inr _) => 9

/-- The C1 common-carrier theorem package.  The remaining analytic identities
are exported as explicit finite rational obligations in the companion report;
the typed source-side symmetry theorems above are unconditional Lean results. -/
theorem omega_norm :
    ∑ e : SceneEdge, (omega e) ^ 2 = 42471 := by
  native_decide

theorem omega_BMinus_zero : BMinus omega = 0 := by
  funext v
  rcases v with x | yz
  · simp [BMinus, omega, Finset.sum_const]
    ring
  · rcases yz with y | z
    · simp [BMinus, omega, Finset.sum_const]
      ring
    · simp [BMinus, omega, Finset.sum_const]
      ring

/-- `U` is a linear operator on `SceneC1`. -/
def ULin : SceneC1 →ₗ[ℚ] SceneC1 where
  toFun := U
  map_add' X Y := by
    funext e
    rcases e with e | e | ⟨y, z⟩
    · rfl
    · rfl
    · simp only [U, Pi.add_apply]
      simp only [Finset.sum_add_distrib]
      ring
  map_smul' r X := by
    funext e
    rcases e with e | e | ⟨y, z⟩
    · rfl
    · rfl
    · simp only [U, Pi.smul_apply, smul_eq_mul]
      simp only [Finset.sum_mul, Finset.mul_sum]
      ring

theorem U_involutive (X : SceneC1) : U (U X) = X := by
  funext e
  rcases e with e | e | ⟨y, z⟩
  · rfl
  · rfl
  · simp only [U]
    let Ry (f : SceneC1) (y' : V11T) := ∑ z' : V13T, f (Sum.inr (Sum.inr (y', z')))
    let T (f : SceneC1) := ∑ y' : V11T, Ry f y'
    let P (f : SceneC1) (y' : V11T) (z' : V13T) :=
      (1 / 13 : ℚ) * (Ry f y' - (1 / 11 : ℚ) * T f)
    have hRy : ∀ y', Ry (U X) y' = Ry X y' - (2 / 13) * (13 * Ry X y' - (13 / 11) * T X) := by
      intro y'
      simp only [Ry, U]
      rw [Finset.sum_sub_distrib, Finset.sum_const]
      simp only [Finset.card_fin, nsmul_eq_mul]
      ring
    have hRy_simp : ∀ y', Ry (U X) y' = -Ry X y' + (2 / 11) * T X := by
      intro y'
      rw [hRy y']
      ring
    have hT : T (U X) = -T X + (2 / 11) * (11 * T X) := by
      simp only [T, hRy_simp]
      rw [Finset.sum_add_distrib, Finset.sum_const, Finset.sum_neg_distrib]
      simp only [Finset.card_fin, nsmul_eq_mul]
      ring
    have hT_simp : T (U X) = T X := by
      rw [hT]
      ring
    simp only [hRy_simp, hT_simp]
    ring

theorem ULin_involutive : ULin.comp ULin = LinearMap.id := by
  ext X
  exact U_involutive X

/-- Orthogonality to the block-constant mode. -/
def omega_perp (X : SceneC1) : Prop :=
  ∑ e : SceneEdge, X e * omega e = 0

theorem T_of_omega_perp_ker_BMinus {X : SceneC1} (hB : BMinus X = 0) (hO : omega_perp X) :
    ∑ y : V11T, ∑ z : V13T, X (Sum.inr (Sum.inr (y, z))) = 0 := by
  let Sx := ∑ x : V9T, ∑ y : V11T, X (Sum.inl (x, y))
  let Sy := ∑ x : V9T, ∑ z : V13T, X (Sum.inr (Sum.inl (x, z)))
  let Sz := ∑ y : V11T, ∑ z : V13T, X (Sum.inr (Sum.inr (y, z)))
  have h1 : Sx + Sy = 0 := by
    have h : ∑ x, BMinus X (Sum.inl x) = 0 := by
      simp [hB]
    simp [BMinus, Finset.sum_add_distrib, Finset.sum_neg_distrib] at h
    exact neg_eq_zero.mp h
  have h2 : Sx - Sz = 0 := by
    have h : ∑ y, BMinus X (Sum.inr (Sum.inl y)) = 0 := by
      simp [hB]
    simp [BMinus, Finset.sum_add_distrib, Finset.sum_sub_distrib] at h
    exact h
  have h3 : 13 * Sx - 11 * Sy + 9 * Sz = 0 := by
    simp [omega_perp, omega, Fintype.sum_sum_type, Finset.sum_mul, mul_comm] at hO
    exact hO
  have hSy : Sy = -Sx := by linarith
  have hSz : Sz = Sx := by linarith
  linarith

theorem U_maps_ker_BMinus_to_ker_BPlus {X : SceneC1} (hB : BMinus X = 0) (hO : omega_perp X) :
    BPlus (U X) = 0 := by
  have hT : (∑ y' : V11T, ∑ z' : V13T, X (Sum.inr (Sum.inr (y', z')))) = 0 :=
    T_of_omega_perp_ker_BMinus hB hO
  funext v
  rcases v with x | yz
  · simp [BPlus, U, hB, Sum.inl]
    have h : BMinus X (Sum.inl x) = 0 := congrFun hB (Sum.inl x)
    simp [BMinus] at h
    exact neg_eq_zero.mp h
  · rcases yz with y | z
    · simp [BPlus, U, hB, hT]
      have h : BMinus X (Sum.inr (Sum.inl y)) = 0 := congrFun hB (Sum.inr (Sum.inl y))
      simp [BMinus] at h
      let Ry := ∑ z' : V13T, X (Sum.inr (Sum.inr (y, z')))
      have hsum : ∑ z : V13T, (X (Sum.inr (Sum.inr (y, z))) - (2 / 13) * Ry) = -Ry := by
        rw [Finset.sum_sub_distrib, Finset.sum_const]
        simp [Ry]
        ring
      rw [hsum]
      exact h
    · simp [BPlus, U, hB]
      have h : BMinus X (Sum.inr (Sum.inr z)) = 0 := congrFun hB (Sum.inr (Sum.inr z))
      simp [BMinus] at h
      exact h

theorem U_maps_ker_BPlus_to_ker_BMinus {X : SceneC1} (hB : BPlus X = 0) :
    BMinus (U X) = 0 ∧ omega_perp (U X) := by
  have hSx : (∑ x, ∑ y, X (Sum.inl (x, y))) = 0 := by
    have h : ∑ x, BPlus X (Sum.inl x) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h
    let Sx := ∑ x, ∑ y, X (Sum.inl (x, y))
    let Sy := ∑ x, ∑ z, X (Sum.inr (Sum.inl (x, z)))
    have h1 : Sx + Sy = 0 := h
    have h2 : Sx + (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      have hh : ∑ y, BPlus X (Sum.inr (Sum.inl y)) = 0 := by simp [hB]
      simp [BPlus, Finset.sum_add_distrib] at hh
      exact hh
    have h3 : Sy + (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      have hh : ∑ z, BPlus X (Sum.inr (Sum.inr z)) = 0 := by simp [hB]
      simp [BPlus, Finset.sum_add_distrib] at hh
      exact hh
    linarith
  have hSy : (∑ x, ∑ z, X (Sum.inr (Sum.inl (x, z)))) = 0 := by
    have h : ∑ x, BPlus X (Sum.inl x) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h
    linarith
  have hSz : (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z)))) = 0 := by
    have h : ∑ y, BPlus X (Sum.inr (Sum.inl y)) = 0 := by simp [hB]
    simp [BPlus, Finset.sum_add_distrib] at h
    linarith
  have hT : (∑ y', ∑ z', X (Sum.inr (Sum.inr (y', z')))) = 0 := hSz
  constructor
  · funext v
    rcases v with x | yz
    · simp [BMinus, U, hB, Sum.inl]
      have h : BPlus X (Sum.inl x) = 0 := congrFun hB (Sum.inl x)
      simp [BPlus] at h
      exact neg_eq_zero.mpr h
    · rcases yz with y | z
      · simp [BMinus, U, hB, hT]
        have h : BPlus X (Sum.inr (Sum.inl y)) = 0 := congrFun hB (Sum.inr (Sum.inl y))
        simp [BPlus] at h
        let Ry := ∑ z' : V13T, X (Sum.inr (Sum.inr (y, z')))
        have hsum : ∑ z : V13T, (X (Sum.inr (Sum.inr (y, z))) - (2 / 13) * Ry) = -Ry := by
          rw [Finset.sum_sub_distrib, Finset.sum_const]
          simp [Ry]
          ring
        rw [hsum]
        linarith
      · simp [BMinus, U, hB]
        have h : BPlus X (Sum.inr (Sum.inr z)) = 0 := congrFun hB (Sum.inr (Sum.inr z))
        simp [BPlus] at h
        exact h
  · simp [omega_perp, omega, Fintype.sum_sum_type, Finset.sum_mul, mul_comm]
    have hUz : ∑ y, ∑ z, (U X (Sum.inr (Sum.inr (y, z)))) = 0 := by
      simp [U, hT]
      exact hSz
    simp [U] at hUz
    linarith

/-- The kernel mapping isomorphism theorem. -/
theorem ker_BPlus_iso_ker_BMinus_perp :
    LinearMap.ker BPlusLin ≃ₗ[ℚ] {Y : SceneC1 // BMinus Y = 0 ∧ omega_perp Y} where
  toFun X := ⟨U X, (U_maps_ker_BPlus_to_ker_BMinus (LinearMap.mem_ker.mp X.2)).1,
                  (U_maps_ker_BPlus_to_ker_BMinus (LinearMap.mem_ker.mp X.2)).2⟩
  map_add' X Y := by
    ext
    simp [ULin]
    exact ULin.map_add X Y
  map_smul' r X := by
    ext
    simp [ULin]
    exact ULin.map_smul r X
  invFun Y := ⟨U Y.1, by
    have h := U_maps_ker_BMinus_to_ker_BPlus Y.2.1 Y.2.2
    exact LinearMap.mem_ker.mpr h⟩
  left_inv X := by
    ext
    exact U_involutive X
  right_inv Y := by
    ext
    exact U_involutive Y

/-- Standard inner product on `SceneC1`. -/
def inner (X Y : SceneC1) : ℚ := ∑ e, X e * Y e

/-- `U` is an isometry with respect to the standard inner product. -/
theorem U_isometry (X Y : SceneC1) : inner (U X) (U Y) = inner X Y := by
  simp only [inner, U, Fintype.sum_sum_type]
  congr 1; congr 1
  let Sz (f : SceneC1) (y : V11T) := ∑ z : V13T, f (Sum.inr (Sum.inr (y, z)))
  let Tz (f : SceneC1) := ∑ y : V11T, Sz f y
  have h_block : ∑ y : V11T, ∑ z : V13T,
      (X (Sum.inr (Sum.inr (y, z))) - (2 / 13) * (Sz X y - (1 / 11) * Tz X)) *
      (Y (Sum.inr (Sum.inr (y, z))) - (2 / 13) * (Sz Y y - (1 / 11) * Tz Y)) =
      ∑ y : V11T, ∑ z : V13T, X (Sum.inr (Sum.inr (y, z))) * Y (Sum.inr (Sum.inr (y, z))) := by
    simp only [sub_mul, mul_sub]
    rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib, Finset.sum_add_distrib]
    simp only [Finset.sum_mul, Finset.mul_sum]
    simp only [Finset.sum_const, Finset.card_fin, nsmul_eq_mul]
    simp only [Sz, Tz]
    field_simp
    ring
  exact h_block

/-- Projection onto the matter-gravity sector (orthogonal to omega). -/
def Pmg (Y : SceneC1) : SceneC1 :=
  Y - ((inner Y omega) / 42471) • omega

theorem Pmg_omega_perp (Y : SceneC1) : omega_perp (Pmg Y) := by
  simp only [omega_perp, Pmg, Pi.sub_apply, Pi.smul_apply, inner, smul_eq_mul]
  simp only [Finset.sum_sub_distrib, Finset.sum_mul]
  rw [show ∑ e, (inner Y omega / 42471 * omega e) * omega e =
    (inner Y omega / 42471) * ∑ e, omega e * omega e by
      simp only [mul_assoc]
      rw [Finset.mul_sum]
      congr]
  rw [omega_norm]
  simp only [inner]
  field_simp
  ring

theorem ker_BMinus_decomposition (Y : SceneC1) (hY : BMinus Y = 0) :
    Y = Pmg Y + ((inner Y omega) / 42471) • omega ∧
    BMinus (Pmg Y) = 0 ∧ omega_perp (Pmg Y) := by
  constructor
  · simp [Pmg]
  · constructor
    · simp [Pmg, hY, omega_BMinus_zero]
    · exact Pmg_omega_perp Y

/-- Centered functions on the (11,13) block. -/
def BlockCorrectionSpace : Submodule ℚ SceneC1 :=
  { X : SceneC1 | (∀ e, match e with | Sum.inr (Sum.inr _) => True | _ => X e = 0) ∧
    (∑ y, ∑ z, X (Sum.inr (Sum.inr (y, z))) = 0) }

theorem BlockCorrectionSpace_finrank :
    Module.finrank ℚ BlockCorrectionSpace = 142 := by
  -- Card(11*13) = 143. Centering condition removes 1 dimension.
  sorry

end D0.Geometry.SignlessSignedCommonCarrier
