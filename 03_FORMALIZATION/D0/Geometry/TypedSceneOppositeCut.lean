import D0.Core.DyadABCD
import D0.Core.FiniteTypes
import D0.Geometry.OppositeCutPairing
import D0.SelfReading.TypedIncidenceCarriers
import Mathlib.LinearAlgebra.FiniteDimensional.Lemmas
import Mathlib.Tactic

/-!
# Typed scene opposite cut

The generic opposite-cut algebra accepts arbitrary finite zone types.  This
module instantiates it on the typed tower

```
V9  = Omega8 ⊕ Witness
V11 = V9 ⊕ Dyad
V13 = V9 ⊕ Role
```

The coefficients `143`, `117`, and `99` are the products of those typed
cardinalities.  The proofs do not pass through `Fin 9`, `Fin 11`, or `Fin 13`.

`Role` is the right summand of `V13`, not an element of `V13` and not the
whole zone.  `BalancedRole` is the 3-dimensional zero-sum representation on
the four roles.  It is not identified with physical 3-space.
-/

namespace D0.Geometry.TypedSceneOppositeCut

open D0.Geometry.OppositeCutPairing
open D0.SelfReading.TypedIncidenceCarriers

abbrev TypedSceneVertex := Vertex V9 V11 V13

abbrev TypedSceneEdge := Edge V9 V11 V13

theorem typedSceneEdge_eq_tripartite :
    TypedSceneEdge = TripartiteEdge V9 V11 V13 := rfl

theorem typedSceneEdge_eq_typedEdge :
    TypedSceneEdge = TypedEdge := rfl

theorem typed_scene_coeff_143 :
    (Fintype.card V11 : ℚ) * Fintype.card V13 = 143 := by
  rw [card_v11, card_v13]
  norm_num

theorem typed_scene_coeff_117 :
    (Fintype.card V9 : ℚ) * Fintype.card V13 = 117 := by
  rw [card_v9, card_v13]
  norm_num

theorem typed_scene_coeff_99 :
    (Fintype.card V9 : ℚ) * Fintype.card V11 = 99 := by
  rw [card_v9, card_v11]
  norm_num

/-- Weighted opposite-cut factorization on the typed zones themselves. -/
theorem typed_scene_opposite_cut_factorization
    (wAB wAC wBC : ℚ) (f9 : V9 → ℚ) (f11 : V11 → ℚ) (f13 : V13 → ℚ)
    (h9 : ∑ i : V9, f9 i = 0) (h11 : ∑ i : V11, f11 i = 0)
    (h13 : ∑ i : V13, f13 i = 0) :
    unsignedIncidence (blockScale wAB wAC wBC (oppositeCutAlpha (β := V11) (γ := V13) f9)) =
        (143 * (wAB - wAC)) • liftAlpha (β := V11) (γ := V13) f9 ∧
      unsignedIncidence (blockScale wAB wAC wBC (oppositeCutBeta (α := V9) (γ := V13) f11)) =
        (117 * (wAB - wBC)) • liftBeta (α := V9) (γ := V13) f11 ∧
      unsignedIncidence (blockScale wAB wAC wBC (oppositeCutGamma (α := V9) (β := V11) f13)) =
        (99 * (wAC - wBC)) • liftGamma (α := V9) (β := V11) f13 := by
  obtain ⟨hα, hβ, hγ⟩ :=
    opposite_cut_factorization (α := V9) (β := V11) (γ := V13)
      wAB wAC wBC f9 f11 f13 h9 h11 h13
  refine ⟨?_, ?_, ?_⟩
  · rw [typed_scene_coeff_143] at hα
    exact hα
  · rw [typed_scene_coeff_117] at hβ
    exact hβ
  · rw [typed_scene_coeff_99] at hγ
    exact hγ

/-! ## Zero-sum functions -/

variable {ι : Type} [Fintype ι] [DecidableEq ι]

/-- Sum of all values. -/
def coordinateSum : (ι → ℚ) →ₗ[ℚ] ℚ where
  toFun f := ∑ i, f i
  map_add' f g := by simp [Finset.sum_add_distrib]
  map_smul' r f := by
    simp only [smul_eq_mul, RingHom.id_apply]
    exact (Finset.mul_sum Finset.univ f r).symm

/-- Functions whose coordinates sum to zero. -/
abbrev BalancedOn (ι : Type) [Fintype ι] [DecidableEq ι] :=
  LinearMap.ker (coordinateSum (ι := ι))

theorem coordinateSum_surjective_of_witness (i0 : ι) :
    Function.Surjective (coordinateSum (ι := ι)) := by
  intro q
  refine ⟨fun i => if i = i0 then q else 0, ?_⟩
  simp [coordinateSum, Finset.sum_ite_eq']

theorem balancedOn_finrank (i0 : ι) :
    Module.finrank ℚ (BalancedOn ι) = Fintype.card ι - 1 := by
  have hrange : LinearMap.range (coordinateSum (ι := ι)) = ⊤ :=
    LinearMap.range_eq_top.mpr (coordinateSum_surjective_of_witness i0)
  have hadd := LinearMap.finrank_range_add_finrank_ker (coordinateSum (ι := ι))
  rw [hrange, finrank_top, Module.finrank_self, Module.finrank_fintype_fun_eq_card] at hadd
  have hsum : Fintype.card ι = Module.finrank ℚ (BalancedOn ι) + 1 := by
    rw [Nat.add_comm]
    exact hadd.symm
  exact (Nat.sub_eq_of_eq_add hsum).symm

/-- Extend a function on the right summand by zero on the left. -/
def extendInrLin {α β : Type} : (β → ℚ) →ₗ[ℚ] (α ⊕ β → ℚ) where
  toFun f
    | Sum.inl _ => 0
    | Sum.inr b => f b
  map_add' f g := by
    funext v
    cases v <;> simp
  map_smul' r f := by
    funext v
    cases v <;> simp [smul_eq_mul]

/-- Extend a function on the left summand by zero on the right. -/
def extendInlLin {α β : Type} : (α → ℚ) →ₗ[ℚ] (α ⊕ β → ℚ) where
  toFun f
    | Sum.inl a => f a
    | Sum.inr _ => 0
  map_add' f g := by
    funext v
    cases v <;> simp
  map_smul' r f := by
    funext v
    cases v <;> simp [smul_eq_mul]

theorem extendInrLin_injective {α β : Type} :
    Function.Injective (extendInrLin (α := α) (β := β)) := by
  intro f g h
  funext b
  have hb := congrFun h (Sum.inr b)
  simpa [extendInrLin] using hb

theorem extendInlLin_injective {α β : Type} :
    Function.Injective (extendInlLin (α := α) (β := β)) := by
  intro f g h
  funext a
  have ha := congrFun h (Sum.inl a)
  simpa [extendInlLin] using ha

theorem sum_extendInr {α β : Type} [Fintype α] [Fintype β] (f : β → ℚ) :
    ∑ x : α ⊕ β, extendInrLin (α := α) (β := β) f x = ∑ b, f b := by
  simp [extendInrLin, Fintype.sum_sum_type]

theorem sum_extendInl {α β : Type} [Fintype α] [Fintype β] (f : α → ℚ) :
    ∑ x : α ⊕ β, extendInlLin (α := α) (β := β) f x = ∑ a, f a := by
  simp [extendInlLin, Fintype.sum_sum_type]

/-! ## Role as the right summand of V13 -/

/-- `Role` is the right summand of `V13 = V9 ⊕ Role`. -/
def roleIntoV13 : Role → V13 := Sum.inr

/-- Points of `V13` that lie in the Role summand. -/
def V13RoleSummand : Set V13 := Set.range roleIntoV13

theorem roleIntoV13_injective : Function.Injective roleIntoV13 := by
  intro r s h
  exact Sum.inr.inj h

theorem role_card_four : Fintype.card Role = 4 := card_role

/-- Extend a Role function by zero on the `V9` summand of `V13`. -/
def extendRoleToV13 : (Role → ℚ) →ₗ[ℚ] (V13 → ℚ) :=
  extendInrLin (α := V9) (β := Role)

theorem extendRoleToV13_injective : Function.Injective extendRoleToV13 :=
  extendInrLin_injective

theorem extendRole_sum (f : Role → ℚ) :
    ∑ v : V13, extendRoleToV13 f v = ∑ r : Role, f r :=
  sum_extendInr (α := V9) (β := Role) f

/-- Zero-sum rational functions on the four roles. -/
abbrev BalancedRole := BalancedOn Role

theorem balancedRole_finrank : Module.finrank ℚ BalancedRole = 3 := by
  simpa [role_card_four] using balancedOn_finrank (ι := Role) A

theorem extendRole_balanced (f : BalancedRole) :
    ∑ v : V13, extendRoleToV13 f.1 v = 0 := by
  rw [extendRole_sum]
  exact f.2

end D0.Geometry.TypedSceneOppositeCut
