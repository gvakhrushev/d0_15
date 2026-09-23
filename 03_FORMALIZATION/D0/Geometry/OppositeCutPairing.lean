import Mathlib.Data.Fintype.Card
import Mathlib.Tactic
import D0.SelfReading.TypedIncidenceCarriers

/-!
# Opposite-cut pairing on a complete tripartite scene

For zones `α`, `β`, `γ`, an edge is a pair from exactly two zones.  The
unsigned incidence operator adds the two endpoint contributions of every edge.
The opposite-cut embedding of a function on one zone uses only the
cardinalities of the other two zones:

* on the first complementary block the value is `(card of the second) * f`;
* on the second complementary block the value is the negative of
  `(card of the first) * f`;
* the untouched block is zero.

No scene constant is part of the definition.  The product of the two
complementary cardinalities appears as the coefficient of the weighted
incidence, once a block-scalar metric scales the three edge blocks.
-/

namespace D0.Geometry.OppositeCutPairing

open BigOperators
open D0.SelfReading.TypedIncidenceCarriers

variable {α β γ : Type}
  [Fintype α] [Fintype β] [Fintype γ]
  [DecidableEq α] [DecidableEq β] [DecidableEq γ]

abbrev Vertex (α β γ : Type) := α ⊕ (β ⊕ γ)

abbrev Edge (α β γ : Type) := TripartiteEdge α β γ

abbrev ECochain (α β γ : Type) := Edge α β γ → ℚ

abbrev VCochain (α β γ : Type) := Vertex α β γ → ℚ

/-- Unsigned endpoint sum.  Each edge contributes to both of its zones. -/
def unsignedIncidence (X : ECochain α β γ) : VCochain α β γ := fun v =>
  match v with
  | Sum.inl a =>
      (∑ b : β, X (Sum.inl (a, b))) +
        ∑ c : γ, X (Sum.inr (Sum.inl (a, c)))
  | Sum.inr (Sum.inl b) =>
      (∑ a : α, X (Sum.inl (a, b))) +
        ∑ c : γ, X (Sum.inr (Sum.inr (b, c)))
  | Sum.inr (Sum.inr c) =>
      (∑ a : α, X (Sum.inr (Sum.inl (a, c)))) +
        ∑ b : β, X (Sum.inr (Sum.inr (b, c)))

/-- Block-scalar metric.  The three weights sit on the three edge blocks. -/
def blockScale (wAB wAC wBC : ℚ) (X : ECochain α β γ) : ECochain α β γ := fun e =>
  match e with
  | Sum.inl _ => wAB * X e
  | Sum.inr (Sum.inl _) => wAC * X e
  | Sum.inr (Sum.inr _) => wBC * X e

def liftAlpha (f : α → ℚ) : VCochain α β γ := fun v =>
  match v with
  | Sum.inl a => f a
  | Sum.inr _ => 0

def liftBeta (f : β → ℚ) : VCochain α β γ := fun v =>
  match v with
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl b) => f b
  | Sum.inr (Sum.inr _) => 0

def liftGamma (f : γ → ℚ) : VCochain α β γ := fun v =>
  match v with
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inr c) => f c

/-- Opposite cut of a function on `α`: coefficients are the complementary
zone cardinalities. -/
def oppositeCutAlpha (f : α → ℚ) : ECochain α β γ := fun e =>
  match e with
  | Sum.inl (a, _) => (Fintype.card γ : ℚ) * f a
  | Sum.inr (Sum.inl (a, _)) => -((Fintype.card β : ℚ) * f a)
  | Sum.inr (Sum.inr _) => 0

/-- Opposite cut of a function on `β`. -/
def oppositeCutBeta (f : β → ℚ) : ECochain α β γ := fun e =>
  match e with
  | Sum.inl (_, b) => (Fintype.card γ : ℚ) * f b
  | Sum.inr (Sum.inl _) => 0
  | Sum.inr (Sum.inr (b, _)) => -((Fintype.card α : ℚ) * f b)

/-- Opposite cut of a function on `γ`. -/
def oppositeCutGamma (f : γ → ℚ) : ECochain α β γ := fun e =>
  match e with
  | Sum.inl _ => 0
  | Sum.inr (Sum.inl (_, c)) => (Fintype.card β : ℚ) * f c
  | Sum.inr (Sum.inr (_, c)) => -((Fintype.card α : ℚ) * f c)

def unsignedIncidenceLin : ECochain α β γ →ₗ[ℚ] VCochain α β γ where
  toFun := unsignedIncidence
  map_add' X Y := by
    funext v
    rcases v with a | b | c <;>
      simp only [unsignedIncidence, Pi.add_apply, Finset.sum_add_distrib] <;>
      abel
  map_smul' r X := by
    funext v
    rcases v with a | b | c <;>
      simp only [unsignedIncidence, Pi.smul_apply, smul_eq_mul,
        ← Finset.mul_sum, mul_add, RingHom.id_apply]

def blockScaleLin (wAB wAC wBC : ℚ) : ECochain α β γ →ₗ[ℚ] ECochain α β γ where
  toFun := blockScale wAB wAC wBC
  map_add' X Y := by
    funext e
    rcases e with e | e | e <;> simp [blockScale, Pi.add_apply, mul_add]
  map_smul' r X := by
    funext e
    rcases e with e | e | e <;> simp [blockScale, Pi.smul_apply, smul_eq_mul, mul_left_comm]

def oppositeCutAlphaLin : (α → ℚ) →ₗ[ℚ] ECochain α β γ where
  toFun := oppositeCutAlpha
  map_add' f g := by
    funext e
    rcases e with e | e | e <;> simp [oppositeCutAlpha, mul_add] <;> abel
  map_smul' r f := by
    funext e
    rcases e with e | e | e <;> simp [oppositeCutAlpha, smul_eq_mul, mul_left_comm]

def oppositeCutBetaLin : (β → ℚ) →ₗ[ℚ] ECochain α β γ where
  toFun := oppositeCutBeta
  map_add' f g := by
    funext e
    rcases e with e | e | e <;> simp [oppositeCutBeta, mul_add] <;> abel
  map_smul' r f := by
    funext e
    rcases e with e | e | e <;> simp [oppositeCutBeta, smul_eq_mul, mul_left_comm]

def oppositeCutGammaLin : (γ → ℚ) →ₗ[ℚ] ECochain α β γ where
  toFun := oppositeCutGamma
  map_add' f g := by
    funext e
    rcases e with e | e | e <;> simp [oppositeCutGamma, mul_add] <;> abel
  map_smul' r f := by
    funext e
    rcases e with e | e | e <;> simp [oppositeCutGamma, smul_eq_mul, mul_left_comm]

private lemma sum_const_mul {ι : Type} [Fintype ι] (q : ℚ) :
    (∑ _i : ι, q) = (Fintype.card ι : ℚ) * q := by
  simp [Finset.sum_const, Finset.card_univ, nsmul_eq_mul]

private lemma sum_scale_zero {ι : Type} [Fintype ι] (c : ℚ) {f : ι → ℚ}
    (hf : ∑ i, f i = 0) :
    (∑ i, c * f i) = 0 := by
  rw [← Finset.mul_sum, hf, mul_zero]

private lemma sum_assoc_scale_zero {ι : Type} [Fintype ι] (c d : ℚ) {f : ι → ℚ}
    (hf : ∑ i, f i = 0) :
    (∑ i, c * (d * f i)) = 0 := by
  have hrewrite : (∑ i, c * (d * f i)) = ∑ i, (c * d) * f i := by
    refine Finset.sum_congr rfl ?_
    intro i _
    ring
  rw [hrewrite]
  exact sum_scale_zero (c * d) hf

theorem unsignedIncidence_block_oppositeCutAlpha
    (wAB wAC wBC : ℚ) (f : α → ℚ) (hf : ∑ a : α, f a = 0) :
    unsignedIncidence (blockScale wAB wAC wBC (oppositeCutAlpha (β := β) (γ := γ) f)) =
      ((Fintype.card β : ℚ) * (Fintype.card γ : ℚ) * (wAB - wAC)) •
        liftAlpha (β := β) (γ := γ) f := by
  funext v
  rcases v with a | b | c
  · simp only [unsignedIncidence, blockScale, oppositeCutAlpha, liftAlpha,
      Pi.smul_apply, smul_eq_mul]
    rw [sum_const_mul (ι := β), sum_const_mul (ι := γ)]
    ring
  · simp only [unsignedIncidence, blockScale, oppositeCutAlpha, liftAlpha,
      Pi.smul_apply, smul_eq_mul]
    have hAB : (∑ a : α, wAB * ((Fintype.card γ : ℚ) * f a)) = 0 :=
      sum_assoc_scale_zero wAB (Fintype.card γ) hf
    have hBC : (∑ c : γ, wBC * (0 : ℚ)) = 0 := by simp
    rw [hAB, hBC]
    simp
  · simp only [unsignedIncidence, blockScale, oppositeCutAlpha, liftAlpha,
      Pi.smul_apply, smul_eq_mul]
    have hAC : (∑ a : α, wAC * (-((Fintype.card β : ℚ) * f a))) = 0 := by
      have hrewrite : (∑ a : α, wAC * (-((Fintype.card β : ℚ) * f a))) =
          ∑ a : α, (-(wAC * (Fintype.card β : ℚ))) * f a := by
        refine Finset.sum_congr rfl ?_
        intro a _
        ring
      rw [hrewrite]
      exact sum_scale_zero _ hf
    have hBC : (∑ b : β, wBC * (0 : ℚ)) = 0 := by simp
    rw [hAC, hBC]
    simp

theorem unsignedIncidence_block_oppositeCutBeta
    (wAB wAC wBC : ℚ) (f : β → ℚ) (hf : ∑ b : β, f b = 0) :
    unsignedIncidence (blockScale wAB wAC wBC (oppositeCutBeta (α := α) (γ := γ) f)) =
      ((Fintype.card α : ℚ) * (Fintype.card γ : ℚ) * (wAB - wBC)) •
        liftBeta (α := α) (γ := γ) f := by
  funext v
  rcases v with a | b | c
  · simp only [unsignedIncidence, blockScale, oppositeCutBeta, liftBeta,
      Pi.smul_apply, smul_eq_mul]
    have hAB : (∑ b : β, wAB * ((Fintype.card γ : ℚ) * f b)) = 0 :=
      sum_assoc_scale_zero wAB (Fintype.card γ) hf
    have hAC : (∑ c : γ, wAC * (0 : ℚ)) = 0 := by simp
    rw [hAB, hAC]
    simp
  · simp only [unsignedIncidence, blockScale, oppositeCutBeta, liftBeta,
      Pi.smul_apply, smul_eq_mul]
    rw [sum_const_mul (ι := α), sum_const_mul (ι := γ)]
    ring
  · simp only [unsignedIncidence, blockScale, oppositeCutBeta, liftBeta,
      Pi.smul_apply, smul_eq_mul]
    have hAC : (∑ a : α, wAC * (0 : ℚ)) = 0 := by simp
    have hBC : (∑ b : β, wBC * (-((Fintype.card α : ℚ) * f b))) = 0 := by
      have hrewrite : (∑ b : β, wBC * (-((Fintype.card α : ℚ) * f b))) =
          ∑ b : β, (-(wBC * (Fintype.card α : ℚ))) * f b := by
        refine Finset.sum_congr rfl ?_
        intro b _
        ring
      rw [hrewrite]
      exact sum_scale_zero _ hf
    rw [hAC, hBC]
    simp

theorem unsignedIncidence_block_oppositeCutGamma
    (wAB wAC wBC : ℚ) (f : γ → ℚ) (hf : ∑ c : γ, f c = 0) :
    unsignedIncidence (blockScale wAB wAC wBC (oppositeCutGamma (α := α) (β := β) f)) =
      ((Fintype.card α : ℚ) * (Fintype.card β : ℚ) * (wAC - wBC)) •
        liftGamma (α := α) (β := β) f := by
  funext v
  rcases v with a | b | c
  · simp only [unsignedIncidence, blockScale, oppositeCutGamma, liftGamma,
      Pi.smul_apply, smul_eq_mul]
    have hAB : (∑ b : β, wAB * (0 : ℚ)) = 0 := by simp
    have hAC : (∑ c : γ, wAC * ((Fintype.card β : ℚ) * f c)) = 0 :=
      sum_assoc_scale_zero wAC (Fintype.card β) hf
    rw [hAB, hAC]
    simp
  · simp only [unsignedIncidence, blockScale, oppositeCutGamma, liftGamma,
      Pi.smul_apply, smul_eq_mul]
    have hAB : (∑ a : α, wAB * (0 : ℚ)) = 0 := by simp
    have hBC : (∑ c : γ, wBC * (-((Fintype.card α : ℚ) * f c))) = 0 := by
      have hrewrite : (∑ c : γ, wBC * (-((Fintype.card α : ℚ) * f c))) =
          ∑ c : γ, (-(wBC * (Fintype.card α : ℚ))) * f c := by
        refine Finset.sum_congr rfl ?_
        intro c _
        ring
      rw [hrewrite]
      exact sum_scale_zero _ hf
    rw [hAB, hBC]
    simp
  · simp only [unsignedIncidence, blockScale, oppositeCutGamma, liftGamma,
      Pi.smul_apply, smul_eq_mul]
    rw [sum_const_mul (ι := α), sum_const_mul (ι := β)]
    ring

/-- The weighted incidence of an opposite cut is the complementary-cardinality
coefficient times the zone lift.  This is an equality of the composed operators
on balanced functions. -/
theorem opposite_cut_factorization
    (wAB wAC wBC : ℚ) (fα : α → ℚ) (fβ : β → ℚ) (fγ : γ → ℚ)
    (hα : ∑ a, fα a = 0) (hβ : ∑ b, fβ b = 0) (hγ : ∑ c, fγ c = 0) :
    unsignedIncidence (blockScale wAB wAC wBC (oppositeCutAlpha (β := β) (γ := γ) fα)) =
        ((Fintype.card β : ℚ) * (Fintype.card γ : ℚ) * (wAB - wAC)) •
          liftAlpha (β := β) (γ := γ) fα ∧
    unsignedIncidence (blockScale wAB wAC wBC (oppositeCutBeta (α := α) (γ := γ) fβ)) =
        ((Fintype.card α : ℚ) * (Fintype.card γ : ℚ) * (wAB - wBC)) •
          liftBeta (α := α) (γ := γ) fβ ∧
    unsignedIncidence (blockScale wAB wAC wBC (oppositeCutGamma (α := α) (β := β) fγ)) =
        ((Fintype.card α : ℚ) * (Fintype.card β : ℚ) * (wAC - wBC)) •
          liftGamma (α := α) (β := β) fγ :=
  ⟨unsignedIncidence_block_oppositeCutAlpha wAB wAC wBC fα hα,
   unsignedIncidence_block_oppositeCutBeta wAB wAC wBC fβ hβ,
   unsignedIncidence_block_oppositeCutGamma wAB wAC wBC fγ hγ⟩

/-! ## Cardinality controls

The coefficient is the product of the complementary zone sizes.  Changing the
scene changes the product.  The scene constants `143`, `117`, `99` are the
products for zone sizes `9,11,13` and do not persist on the control scenes.
-/

theorem scene_zone_products :
    (Fintype.card (Fin 11) : ℚ) * Fintype.card (Fin 13) = 143 ∧
    (Fintype.card (Fin 9) : ℚ) * Fintype.card (Fin 13) = 117 ∧
    (Fintype.card (Fin 9) : ℚ) * Fintype.card (Fin 11) = 99 := by
  simp [Fintype.card_fin]
  norm_num

theorem control_K266_products :
    (Fintype.card (Fin 6) : ℚ) * Fintype.card (Fin 6) = 36 ∧
    (Fintype.card (Fin 2) : ℚ) * Fintype.card (Fin 6) = 12 ∧
    (Fintype.card (Fin 6) : ℚ) * Fintype.card (Fin 6) ≠ 143 ∧
    (Fintype.card (Fin 2) : ℚ) * Fintype.card (Fin 6) ≠ 117 := by
  simp [Fintype.card_fin]
  norm_num

theorem control_K338_products :
    (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 8) = 24 ∧
    (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 3) = 9 ∧
    (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 8) ≠ 143 ∧
    (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 3) ≠ 99 := by
  simp [Fintype.card_fin]
  norm_num

theorem control_K234_products :
    (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 4) = 12 ∧
    (Fintype.card (Fin 2) : ℚ) * Fintype.card (Fin 4) = 8 ∧
    (Fintype.card (Fin 2) : ℚ) * Fintype.card (Fin 3) = 6 ∧
    (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 4) ≠ 143 := by
  simp [Fintype.card_fin]
  norm_num

/-- On `K(2,6,6)` the `α`-sector coefficient is `6 * 6`, not the scene value. -/
theorem k266_alpha_cut_coefficient
    (wAB wAC wBC : ℚ) (f : Fin 2 → ℚ) (hf : ∑ a : Fin 2, f a = 0) (a : Fin 2) :
    unsignedIncidence (α := Fin 2) (β := Fin 6) (γ := Fin 6)
        (blockScale wAB wAC wBC (oppositeCutAlpha f)) (Sum.inl a) =
      36 * (wAB - wAC) * f a := by
  have h := unsignedIncidence_block_oppositeCutAlpha (α := Fin 2) (β := Fin 6)
    (γ := Fin 6) wAB wAC wBC f hf
  have ha := congrFun h (Sum.inl a)
  simp only [liftAlpha, Pi.smul_apply, smul_eq_mul, Fintype.card_fin] at ha
  norm_num at ha
  exact ha

/-- On `K(3,3,8)` the `γ`-sector coefficient is `3 * 3`. -/
theorem k338_gamma_cut_coefficient
    (wAB wAC wBC : ℚ) (f : Fin 8 → ℚ) (hf : ∑ c : Fin 8, f c = 0) (c : Fin 8) :
    unsignedIncidence (α := Fin 3) (β := Fin 3) (γ := Fin 8)
        (blockScale wAB wAC wBC (oppositeCutGamma f)) (Sum.inr (Sum.inr c)) =
      9 * (wAC - wBC) * f c := by
  have h := unsignedIncidence_block_oppositeCutGamma (α := Fin 3) (β := Fin 3)
    (γ := Fin 8) wAB wAC wBC f hf
  have hc := congrFun h (Sum.inr (Sum.inr c))
  simp only [liftGamma, Pi.smul_apply, smul_eq_mul, Fintype.card_fin] at hc
  norm_num at hc
  exact hc

/-- On `K(2,3,4)` all three complementary products are distinct from the scene
products. -/
theorem k234_coefficients_follow_zones :
    (Fintype.card (Fin 3) : ℚ) * Fintype.card (Fin 4) = 12 ∧
    (Fintype.card (Fin 2) : ℚ) * Fintype.card (Fin 4) = 8 ∧
    (Fintype.card (Fin 2) : ℚ) * Fintype.card (Fin 3) = 6 :=
  ⟨control_K234_products.1, control_K234_products.2.1, control_K234_products.2.2.1⟩

end D0.Geometry.OppositeCutPairing
