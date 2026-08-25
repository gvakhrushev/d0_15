import Mathlib.Algebra.Algebra.Subalgebra.Basic
import Mathlib.Tactic

/-!
# Unital subalgebras of `V → ℚ` are exactly partition algebras

`D0.Foundation.InvariantMinimal` records this as a gap, verbatim (`InvariantMinimal.lean:32`):

> "finite unital subalgebras of `ℚ^V` closed under pointwise multiplication are
> exactly partition algebras — standard finite fact, **cited not formalized**"

It is load-bearing there: that module's universal is over *partition classifiers*, and the step
from those to *observable algebras* runs through exactly this equivalence. This module supplies it.

For a finite `V` and a unital subalgebra `A ⊆ (V → ℚ)`, write `v ≈ w` when every member of `A`
agrees at `v` and `w`. Then `A` is precisely the set of functions constant on the `≈`-classes
(`mem_iff_constant_on_classes`).

Proof: finite Stone–Weierstrass. For `v ≉ w` choose a separator in `A` and normalise it to take
the value `1` at `v` and `0` at `w`; the product of these over all `w ≉ v` is the indicator of
`v`'s class and lies in `A`. A function constant on classes is then the `A`-combination of those
indicators, normalised by the class sizes.
-/

namespace D0.Foundation.PartitionAlgebra

open scoped Classical

variable {V : Type*} [Fintype V]

/-- Two points are inseparable by `A` when every member of `A` agrees on them. -/
def Insep (A : Subalgebra ℚ (V → ℚ)) (v w : V) : Prop := ∀ f ∈ A, f v = f w

theorem insep_refl (A : Subalgebra ℚ (V → ℚ)) (v : V) : Insep A v v := fun _ _ => rfl

theorem insep_symm {A : Subalgebra ℚ (V → ℚ)} {v w : V} (h : Insep A v w) : Insep A w v :=
  fun f hf => (h f hf).symm

theorem insep_trans {A : Subalgebra ℚ (V → ℚ)} {u v w : V}
    (h₁ : Insep A u v) (h₂ : Insep A v w) : Insep A u w :=
  fun f hf => (h₁ f hf).trans (h₂ f hf)

section Witness

variable {A : Subalgebra ℚ (V → ℚ)} {v w : V}

/-- Separability unpacked. -/
theorem exists_separator (h : ¬ Insep A v w) : ∃ f, f ∈ A ∧ f v ≠ f w := by
  simpa [Insep, not_forall] using h

/-- A chosen separator of a separable pair. -/
noncomputable def wit (h : ¬ Insep A v w) : V → ℚ := (exists_separator h).choose

theorem wit_mem (h : ¬ Insep A v w) : wit h ∈ A := (exists_separator h).choose_spec.1

theorem wit_ne (h : ¬ Insep A v w) : wit h v ≠ wit h w := (exists_separator h).choose_spec.2

theorem wit_den_ne (h : ¬ Insep A v w) : wit h v - wit h w ≠ 0 := sub_ne_zero.mpr (wit_ne h)

end Witness

/-- The normalised separator: `1` at `v`, `0` at `w`, and a member of `A`. -/
noncomputable def sep (A : Subalgebra ℚ (V → ℚ)) (v w : V) : V → ℚ :=
  if h : ¬ Insep A v w then (fun x => (wit h x - wit h w) / (wit h v - wit h w)) else 1

theorem sep_mem (A : Subalgebra ℚ (V → ℚ)) (v w : V) : sep A v w ∈ A := by
  unfold sep
  by_cases h : ¬ Insep A v w
  · rw [dif_pos h]
    have hrw : (fun x => (wit h x - wit h w) / (wit h v - wit h w)) =
        (wit h - (fun _ => wit h w)) * (fun _ => (wit h v - wit h w)⁻¹) := by
      funext x; simp [div_eq_mul_inv]
    rw [hrw]
    exact A.mul_mem (A.sub_mem (wit_mem h) (A.algebraMap_mem _)) (A.algebraMap_mem _)
  · rw [dif_neg h]; exact A.one_mem

theorem sep_self (A : Subalgebra ℚ (V → ℚ)) {v w : V} (h : ¬ Insep A v w) :
    sep A v w v = 1 := by
  unfold sep; rw [dif_pos h]; exact div_self (wit_den_ne h)

theorem sep_other (A : Subalgebra ℚ (V → ℚ)) {v w : V} (h : ¬ Insep A v w) :
    sep A v w w = 0 := by
  unfold sep; rw [dif_pos h]; simp

/-- Inside the class the normalised separator is `1`: `v ≈ u` forces numerator to equal
denominator. -/
theorem sep_inside (A : Subalgebra ℚ (V → ℚ)) {v w u : V} (hvu : Insep A v u)
    (h : ¬ Insep A v w) : sep A v w u = 1 := by
  unfold sep; rw [dif_pos h]
  have hu : wit h u = wit h v := (hvu _ (wit_mem h)).symm
  rw [hu]
  exact div_self (wit_den_ne h)

/-- The indicator of the `≈`-class of `v`. -/
noncomputable def classInd (A : Subalgebra ℚ (V → ℚ)) (v : V) : V → ℚ :=
  ∏ w ∈ Finset.univ.filter (fun w => ¬ Insep A v w), sep A v w

theorem classInd_mem (A : Subalgebra ℚ (V → ℚ)) (v : V) : classInd A v ∈ A :=
  Subalgebra.prod_mem _ fun w _ => sep_mem A v w

theorem classInd_inside (A : Subalgebra ℚ (V → ℚ)) {v u : V} (h : Insep A v u) :
    classInd A v u = 1 := by
  unfold classInd
  rw [Finset.prod_apply]
  exact Finset.prod_eq_one fun w hw => sep_inside A h (Finset.mem_filter.mp hw).2

theorem classInd_outside (A : Subalgebra ℚ (V → ℚ)) {v u : V} (h : ¬ Insep A v u) :
    classInd A v u = 0 := by
  unfold classInd
  rw [Finset.prod_apply]
  exact Finset.prod_eq_zero (Finset.mem_filter.mpr ⟨Finset.mem_univ u, h⟩) (sep_other A h)

/-- **Members are constant on classes** — immediate from the definition. -/
theorem constant_on_classes_of_mem (A : Subalgebra ℚ (V → ℚ)) {f : V → ℚ} (hf : f ∈ A)
    {v w : V} (h : Insep A v w) : f v = f w := h f hf

/-- The size of the `≈`-class of `v`. -/
noncomputable def csize (A : Subalgebra ℚ (V → ℚ)) (v : V) : ℕ :=
  (Finset.univ.filter (fun w => Insep A v w)).card

theorem csize_pos (A : Subalgebra ℚ (V → ℚ)) (v : V) : 0 < csize A v :=
  Finset.card_pos.mpr ⟨v, Finset.mem_filter.mpr ⟨Finset.mem_univ v, insep_refl A v⟩⟩

theorem csize_eq_of_insep (A : Subalgebra ℚ (V → ℚ)) {v u : V} (h : Insep A v u) :
    csize A v = csize A u := by
  unfold csize
  congr 1
  apply Finset.filter_congr
  intro x _
  exact ⟨fun hvx => insep_trans (insep_symm h) hvx, fun hux => insep_trans h hux⟩

/-- **The content: every function constant on `≈`-classes lies in `A`.** -/
theorem mem_of_constant_on_classes (A : Subalgebra ℚ (V → ℚ)) (f : V → ℚ)
    (hf : ∀ v w : V, Insep A v w → f v = f w) : f ∈ A := by
  have key : f = ∑ v ∈ Finset.univ, (fun _ : V => f v / (csize A v : ℚ)) * classInd A v := by
    funext u
    rw [Finset.sum_apply]
    have hterm : ∀ v ∈ Finset.univ,
        ((fun _ : V => f v / (csize A v : ℚ)) * classInd A v) u
          = if Insep A v u then f u / (csize A u : ℚ) else 0 := by
      intro v _
      by_cases h : Insep A v u
      · rw [if_pos h, Pi.mul_apply, classInd_inside A h, mul_one, hf v u h,
          csize_eq_of_insep A h]
      · rw [if_neg h, Pi.mul_apply, classInd_outside A h, mul_zero]
    rw [Finset.sum_congr rfl hterm, ← Finset.sum_filter, Finset.sum_const]
    have hcard : (Finset.univ.filter (fun v => Insep A v u)).card = csize A u := by
      unfold csize
      congr 1
      apply Finset.filter_congr
      intro x _
      exact ⟨fun hx => insep_symm hx, fun hx => insep_symm hx⟩
    rw [hcard, nsmul_eq_mul]
    have hpos : (csize A u : ℚ) ≠ 0 := Nat.cast_ne_zero.mpr (csize_pos A u).ne'
    field_simp
  rw [key]
  exact Subalgebra.sum_mem _ fun v _ => A.mul_mem (A.algebraMap_mem _) (classInd_mem A v)

/-- **The equivalence.** `A` is exactly the algebra of functions constant on the blocks of the
partition it induces — the fact `InvariantMinimal.lean:32` cites without formalizing. -/
theorem mem_iff_constant_on_classes (A : Subalgebra ℚ (V → ℚ)) (f : V → ℚ) :
    f ∈ A ↔ ∀ v w : V, Insep A v w → f v = f w :=
  ⟨fun hf v w h => constant_on_classes_of_mem A hf h, mem_of_constant_on_classes A f⟩

end D0.Foundation.PartitionAlgebra
